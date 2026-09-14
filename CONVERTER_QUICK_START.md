# All in One Place — Converter Quick Start

## Exact Office PDF conversion

1. Install Microsoft Office (Word/Excel/PowerPoint) **or** LibreOffice.
2. Install Python 3.10+ if it is not already installed.
3. Extract the complete ZIP.
4. Double-click `start-converter-server.bat`.
5. Wait for the launcher to report that the Office conversion engine is ONLINE.
6. Use the browser page that the launcher opens.
7. Choose the DOCX/XLSX/PPTX file and click **Convert & Download**.

The server prefers native Microsoft Office on Windows because it uses the actual Word/Excel/PowerPoint rendering engine. If Microsoft Office is not installed, it uses LibreOffice.

Do **not** double-click `file-converter.html` when you need exact Office PDF conversion; a browser cannot launch Office by itself.

If conversion still fails, run `converter-server.py --check` from a command prompt in this folder. It prints the detected rendering engines.
