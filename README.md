# All in One Place — Professional Functional Build

## Navigation
The shared `site.js` injects the same professional navigation on every page:
Home | Calculators | Business | AI Tools | Website Tools | Developer | Testing | Career | Islamic | Videos.
Dropdowns and the mobile menu are keyboard/click friendly and show the current page.

## Ads
Edit `site.js`:
- `AD_URLS.top`
- `AD_URLS.middle`
- `AD_URLS.bottom`

The site has top, middle and bottom ad slots. If an advertiser blocks iframe embedding, the visitor can use the Open ad link.

## AI affiliate links
Edit `AI_AFFILIATE_LINKS` in `site.js`. Empty links are displayed as "Affiliate link not added yet" instead of broken links.

## Functional tools
Website, API, testing, career and Islamic collection pages now open real browser-side tools rather than generic placeholders. Examples include JSON formatting/validation, Base64, UUID, password generation, QR/barcode generation, invoice preview, regex testing, test-case generation, bug reports, CSV test data, JWT decoding, resume/JD analysis, Tasbeeh, Zakat and Islamic quiz.

## File converter
The converter provides local browser-side text/data conversion plus an optional high-fidelity LibreOffice engine. Office → PDF should use the LibreOffice engine so the original DOCX/XLSX/PPTX document is rendered instead of reconstructed from extracted text. The browser formatting preview is explicitly a fallback approximation, not an exact Office conversion.

## Website monitoring
The browser check is functional but CORS-limited. Production monitoring requires a backend worker for scheduled checks, uptime history and reliable Email/WhatsApp/Telegram alerts.

## Network access
No Google Fonts or external font/CDN is required for the site's normal UI. External network access is used only when a user explicitly opens an external resource or uses a tool that needs an online service (for example QR generation or URL shortening).

## Latest visual / QA pass
- Premium ambient artwork added via `assets/bg-premium-strong.svg`.
- Page-specific artwork remains visible behind the content.
- Navigation dropdowns now use a dedicated high stacking layer so they stay above hero sections and advertisements.
- Dropdowns close on outside click and Escape.
- 24 HTML pages were scanned for inline JavaScript syntax errors: none found.
- Local HTML/CSS/JS/image references: no broken local references found.
- 43 interactive tool buttons were checked against shared tool handlers: all mapped.
- Representative calculator logic checks: 8/8 passed.
- No Google Fonts/CDN font dependency remains.

## High-fidelity file conversion

The file converter now has two modes:

1. **High-fidelity Office engine** — `converter-server.py` uses LibreOffice to render DOCX/XLSX/PPTX and other supported formats. For Office → PDF this is the production-quality path because it renders the source document rather than flattening extracted text.
2. **Browser conversion** — simple text/data conversions can run without a backend. The **Preview source formatting (fallback)** button reconstructs common Office formatting for inspection, but it is intentionally not presented as an exact Office-to-PDF conversion.

### Run the high-fidelity converter locally

Install LibreOffice on the machine, then from the project folder run:

```bash
python converter-server.py --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/file-converter.html`. The page will show **High-fidelity Office engine ready** when the backend is available.

The server accepts files through `POST /api/convert` and exposes `GET /api/health`. It has a 50 MB input limit, adds CORS headers for local/static-site use, and does not send documents to a third-party conversion service. Markdown/JSON/CSV/TXT PDF inputs are converted through a generated HTML print layout; Office documents are rendered by LibreOffice.

### Windows shortcut

If Python and LibreOffice are installed, double-click `start-converter-server.bat` and open the converter page at `http://127.0.0.1:8765/file-converter.html`.


## High-fidelity File Converter (important)

For exact DOCX/XLSX/PPTX → PDF rendering, do not double-click `file-converter.html`. Run `start-converter-server.bat`. It starts the local conversion service on `http://127.0.0.1:8765` and opens the converter page automatically. The service uses LibreOffice's native PDF export filters, so the original Office document is rendered instead of being rebuilt from extracted plain text. LibreOffice documents that PDF export is performed through format-specific filters such as Writer/Calc/Impress PDF export.

If the engine badge says **High-fidelity engine offline**, LibreOffice or Python is not available/running. Install LibreOffice and Python 3, then run the BAT file again.
