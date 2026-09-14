#!/usr/bin/env python3
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import re
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
HOST = '127.0.0.1'
PORT = 8765


def find_soffice():
    candidates = []
    found = shutil.which('soffice') or shutil.which('libreoffice')
    if found:
        candidates.append(found)
    if os.name == 'nt':
        for base in (os.environ.get('PROGRAMFILES'), os.environ.get('PROGRAMFILES(X86)'), os.environ.get('LOCALAPPDATA')):
            if base:
                candidates += [
                    str(Path(base) / 'LibreOffice' / 'program' / 'soffice.com'),
                    str(Path(base) / 'LibreOffice' / 'program' / 'soffice.exe'),
                ]
    for p in candidates:
        if p and Path(p).exists():
            return p
    return None


def windows_office_apps():
    if os.name != 'nt':
        return []
    apps = []
    try:
        for app, progid in [('Word', 'Word.Application'), ('Excel', 'Excel.Application'), ('PowerPoint', 'PowerPoint.Application')]:
            cmd = ['reg', 'query', rf'HKCR\\{progid}\\CLSID']
            r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            if r.returncode == 0:
                apps.append(app)
    except Exception:
        pass
    return apps


def engines():
    lo = find_soffice()
    office = windows_office_apps()
    return lo, office


def health_payload():
    lo, office = engines()
    if office:
        primary = 'Microsoft Office'
    elif lo:
        primary = 'LibreOffice'
    else:
        primary = None
    return {
        'ok': bool(primary),
        'engine': primary,
        'officeApps': office,
        'soffice': bool(lo),
        'sofficePath': lo,
        'python': sys.version.split()[0],
        'port': PORT,
    }


def safe_name(name):
    name = os.path.basename(name or 'upload')
    return ''.join(ch for ch in name if ch.isalnum() or ch in ' ._-').strip() or 'upload'


def run_word(input_path, output_path):
    script = r'''
param([string]$InputPath,[string]$OutputPath)
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $doc = $word.Documents.Open($InputPath, $false, $true)
  # 17 = wdExportFormatPDF
  $doc.ExportAsFixedFormat($OutputPath, 17, $false, 0, 0, 0, 0, 0, $true, $false, 0, $true, $true, $false)
  $doc.Close($false)
  $doc = $null
  $word.Quit()
  $word = $null
} finally {
  if ($doc) { try { $doc.Close($false) } catch {} }
  if ($word) { try { $word.Quit() } catch {} }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
'''
    ps = Path(tempfile.mkdtemp(prefix='aop-word-'))
    try:
        script_path = ps / 'convert.ps1'
        script_path.write_text(script, encoding='utf-8')
        cmd = ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script_path), '-InputPath', str(input_path), '-OutputPath', str(output_path)]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
        if proc.returncode != 0 or not output_path.exists():
            raise RuntimeError((proc.stderr or proc.stdout or '').strip() or 'Microsoft Word PDF export failed.')
    finally:
        shutil.rmtree(ps, ignore_errors=True)


def run_excel(input_path, output_path):
    script = r'''
param([string]$InputPath,[string]$OutputPath)
$ErrorActionPreference = 'Stop'
$excel=$null; $book=$null
try {
  $excel=New-Object -ComObject Excel.Application
  $excel.Visible=$false; $excel.DisplayAlerts=$false
  $book=$excel.Workbooks.Open($InputPath, $null, $true)
  # 0 = xlTypePDF
  $book.ExportAsFixedFormat(0, $OutputPath)
  $book.Close($false); $book=$null
  $excel.Quit(); $excel=$null
} finally {
  if($book){try{$book.Close($false)}catch{}}
  if($excel){try{$excel.Quit()}catch{}}
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
'''
    ps=Path(tempfile.mkdtemp(prefix='aop-excel-'))
    try:
        sp=ps/'convert.ps1'; sp.write_text(script,encoding='utf-8')
        proc=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(sp),'-InputPath',str(input_path),'-OutputPath',str(output_path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=180)
        if proc.returncode!=0 or not output_path.exists(): raise RuntimeError((proc.stderr or proc.stdout or '').strip() or 'Microsoft Excel PDF export failed.')
    finally: shutil.rmtree(ps,ignore_errors=True)


def run_powerpoint(input_path, output_path):
    script = r'''
param([string]$InputPath,[string]$OutputPath)
$ErrorActionPreference='Stop'
$ppt=$null;$pres=$null
try{
  $ppt=New-Object -ComObject PowerPoint.Application
  $pres=$ppt.Presentations.Open($InputPath,$true,$true,$false)
  # 32 = ppSaveAsPDF
  $pres.SaveAs($OutputPath,32)
  $pres.Close();$pres=$null
  $ppt.Quit();$ppt=$null
}finally{
  if($pres){try{$pres.Close()}catch{}}
  if($ppt){try{$ppt.Quit()}catch{}}
  [GC]::Collect();[GC]::WaitForPendingFinalizers()
}
'''
    ps=Path(tempfile.mkdtemp(prefix='aop-ppt-'))
    try:
        sp=ps/'convert.ps1';sp.write_text(script,encoding='utf-8')
        proc=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(sp),'-InputPath',str(input_path),'-OutputPath',str(output_path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=180)
        if proc.returncode!=0 or not output_path.exists(): raise RuntimeError((proc.stderr or proc.stdout or '').strip() or 'Microsoft PowerPoint PDF export failed.')
    finally: shutil.rmtree(ps,ignore_errors=True)


def run_office(input_path, output_dir, target):
    lo, office = engines()
    ext = Path(input_path).suffix.lower()
    output = output_dir / (Path(input_path).stem + '.' + target)
    # Prefer native Microsoft Office on Windows for highest DOCX/XLSX/PPTX fidelity.
    if target == 'pdf' and os.name == 'nt':
        if ext in {'.doc', '.docx', '.rtf', '.odt'} and 'Word' in office:
            run_word(input_path, output); return output
        if ext in {'.xls', '.xlsx', '.csv', '.ods'} and 'Excel' in office:
            run_excel(input_path, output); return output
        if ext in {'.ppt', '.pptx', '.odp'} and 'PowerPoint' in office:
            run_powerpoint(input_path, output); return output
    if not lo:
        raise RuntimeError('No Office rendering engine was found. Install Microsoft Office (Word/Excel/PowerPoint) or LibreOffice, then restart the converter server.')
    if target == 'pdf':
        if ext in {'.doc', '.docx', '.odt', '.rtf', '.txt', '.html', '.htm', '.xml', '.md'}:
            filt = 'pdf:writer_pdf_Export'
        elif ext in {'.xls', '.xlsx', '.ods', '.csv'}:
            filt = 'pdf:calc_pdf_Export'
        elif ext in {'.ppt', '.pptx', '.odp'}:
            filt = 'pdf:impress_pdf_Export'
        else:
            filt = 'pdf'
    else:
        filt = target
    profile = Path(tempfile.mkdtemp(prefix='aop-lo-profile-'))
    try:
        cmd = [lo, '--headless', '--nologo', '--nodefault', '--nolockcheck', '--norestore', f'-env:UserInstallation={profile.as_uri()}', '--convert-to', filt, '--outdir', str(output_dir), str(input_path)]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=180)
        if proc.returncode != 0 or not output.exists():
            detail=(proc.stderr or proc.stdout or '').strip()
            raise RuntimeError(detail or f'LibreOffice conversion failed with exit code {proc.returncode}.')
        return output
    finally: shutil.rmtree(profile,ignore_errors=True)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers','Content-Type'); super().end_headers()
    def do_OPTIONS(self): self.send_response(204); self.end_headers()
    def do_GET(self):
        if urlparse(self.path).path=='/api/health':
            body=json.dumps(health_payload()).encode(); self.send_response(200); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!='/api/convert': self.send_error(404,'Not found'); return
        try:
            ctype=self.headers.get('Content-Type','')
            if not ctype.startswith('multipart/form-data'): raise RuntimeError('Expected multipart/form-data upload.')
            m=re.search(r'boundary=(?:"([^"]+)"|([^;]+))',ctype)
            if not m: raise RuntimeError('Multipart boundary missing.')
            boundary=(m.group(1) or m.group(2)).encode(); length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>100*1024*1024: raise RuntimeError('Upload is empty or exceeds the 100 MB limit.')
            raw=self.rfile.read(length); marker=b'--'+boundary; parts=raw.split(marker); uploaded=None; target='pdf'
            for part in parts:
                if not part or part in (b'--\r\n',b'--'): continue
                part=part.lstrip(b'\r\n'); head,sep,body=part.partition(b'\r\n\r\n')
                if not sep: continue
                body=body.rstrip(b'\r\n-'); headers=head.decode('utf-8','replace')
                disp=re.search(r'Content-Disposition:.*?name="([^"]+)"(?:;\s*filename="([^"]*)")?',headers,re.I)
                if not disp: continue
                name,filename=disp.group(1),disp.group(2)
                if name=='target': target=body.decode('utf-8','replace').strip().lower() or 'pdf'
                elif name=='file' and filename: uploaded=(safe_name(filename),body)
            if not uploaded: raise RuntimeError('No file was uploaded.')
            allowed={'pdf','txt','html','md','json','csv','docx','xlsx','pptx','odt','ods','odp','rtf'}
            if target not in allowed: raise RuntimeError(f'Unsupported target format: {target}')
            with tempfile.TemporaryDirectory(prefix='aop-convert-') as td:
                inp=Path(td)/uploaded[0]; outdir=Path(td)/'out'; outdir.mkdir(); inp.write_bytes(uploaded[1])
                output=run_office(inp,outdir,target); data=output.read_bytes(); mime=mimetypes.guess_type(output.name)[0] or 'application/octet-stream'
                self.send_response(200); self.send_header('Content-Type',mime); self.send_header('Content-Length',str(len(data))); self.send_header('Content-Disposition',f'attachment; filename="{output.name}"'); self.end_headers(); self.wfile.write(data)
        except Exception as exc:
            body=json.dumps({'ok':False,'error':str(exc)}).encode(); self.send_response(500); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)


def main():
    payload=health_payload()
    if '--check' in sys.argv:
        print(json.dumps(payload))
        return 0 if payload['ok'] else 2
    if not payload['ok']:
        print('ERROR: No Microsoft Office or LibreOffice rendering engine was found.',file=sys.stderr)
        print('Install Microsoft Office or LibreOffice, then run this script again.',file=sys.stderr)
        return 2
    server=ThreadingHTTPServer((HOST,PORT),Handler)
    print(f'All in One Place converter server running at http://{HOST}:{PORT}/')
    print(f'Primary engine: {payload["engine"]}; LibreOffice: {payload["sofficePath"] or "not found"}; Office apps: {", ".join(payload["officeApps"]) or "none"}')
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
    return 0

if __name__=='__main__': raise SystemExit(main())
