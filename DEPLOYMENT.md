# All in One Place — automatic Office conversion deployment

The browser cannot start Microsoft Word/LibreOffice on a visitor's computer. For automatic DOCX/XLSX/PPTX → PDF conversion, deploy this project as a web application so the conversion engine runs on the server. Visitors then only upload and click **Convert & Download**.

## Docker (recommended)

On a Linux server with Docker + Compose:

```bash
docker compose up -d --build
```

Open `http://YOUR-SERVER:8765/`. The same origin serves the website and `/api/convert`; no batch file is required for visitors. The container includes LibreOffice Writer/Calc/Impress.

## Reverse proxy / HTTPS

Put Nginx, Caddy, Cloudflare Tunnel, or your hosting provider in front of port 8765 and point your domain at it. Keep `/api/convert` on the same origin as the website.

## Windows development

`start-converter-server.bat` remains available for local development, but it is **not part of the visitor workflow**. In production, use a process manager or Docker `restart: unless-stopped` so the server starts automatically after reboot.

## Fidelity

DOCX/XLSX/PPTX → PDF is rendered by LibreOffice on the server. If Microsoft Office automation is available on a Windows server, `converter-server.py` can prefer Word/Excel/PowerPoint for their respective formats.
