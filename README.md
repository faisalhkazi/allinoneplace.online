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

## 2026-09-14 (round 3) — new Loans section, ad slots, background, file converter

- **New Loans section.** Added a "Loans" nav item (with a dropdown, matching the Calculators/Business/Career pattern) and six new pages: `loans.html` (a hub explaining how loans work in general, with a loan-type picker and a "best deals" list) plus `home-loan.html`, `car-loan.html`, `bike-loan.html`, `personal-loan.html` and `education-loan.html`, each with a plain-language "how it works" walkthrough specific to that loan type, typical numbers, eligibility/fees, and a REPLACE-style affiliate deal list ready for real lender links and rates (same pattern as the Credit Cards page). A "Loans" quick-access card was also added to the homepage.
- **Fixed the File Converter's core bug.** Converting to PDF always failed with an error, because the page depends on an optional local backend that isn't running in a normal browser-only deployment. It now falls back to opening a formatted, print-ready preview and prompting the visitor to use their browser's "Save as PDF" print option — so PDF output always produces a usable file instead of failing outright. Also added a clear error (instead of silently producing garbled text) when a source format the browser can't parse (PDF, RTF, ODT, ODS, ODP) is selected without the optional backend.
- **File Converter color-coding.** DOCX/XLSX/PPTX format cards and the selected-file chip now pick up a distinct color per format (blue/green/orange), and the three capability cards (Office → PDF, Formatted fallback, No visitor setup) each have their own accent color, instead of everything sharing one blue tone.
- **Every ad slot is now full-width.** Ad placeholders were constrained to the ~1180px content column (visually "half the page"). They now break out to the full browser width edge-to-edge on every page, while surrounding content keeps its normal width.
- **Fixed sitewide centering.** On screens wider than ~1180px, the header, hero and every page section were flush against the left edge with a large empty gap on the right — the `.wrap`/`.site-header-inner` containers had a max-width but no centering margin anywhere in the stylesheet. Centering is fixed everywhere, which also made the ad full-width fix behave correctly.
- **Reworked the ambient background.** The previous aurora glow only lit up a band near the very top/bottom of the viewport, leaving the middle of the screen — where most content and ad slots sit — visually flat. The gradients are now larger, reach the center of the viewport, and a subtle grain/noise texture was added; the grid texture mask was softened so it's visible across most of the screen instead of fading out quickly.
- **Small sitewide additions:** an SVG favicon, Open Graph/Twitter meta tags on all 36 pages (for clean link previews when shared), a styled 404 page, a shared "back to top" button that appears after scrolling, and toast confirmation feedback ("Copied to clipboard") on the site's Copy buttons.
- **Homepage tagline.** Added a highlighted "best solution for everything" badge to the homepage hero.
- Full Playwright crawl of all 37 pages (desktop + mobile, every tool modal) after these changes: no console errors, no JavaScript exceptions, and no broken local references. The only failed network requests are third-party services (YouTube thumbnails, QR/barcode generators, AdSense) blocked by this sandbox's network policy, not by the site itself.

## Suggested further enhancements

These weren't implemented (they either need real content/keys from you, or are a bigger scope decision) but would be worth considering next:

- **Fill in real content:** the Loans and Credit Cards pages currently show REPLACE placeholders — add real lender/card names, rates and your actual affiliate links, and keep `AD_URLS`/`ADSENSE_PUBLISHER_ID` in `site.js` up to date.
- **Cookie consent banner** — worth adding once AdSense/analytics are live, for regions that require it (GDPR/similar).
- **Analytics** (e.g. a privacy-respecting option, or GA4) to see which tools and loan pages actually get used.
- **PWA manifest + service worker** so the site can be "installed" and the calculators work offline.
- **A dedicated Open Graph share image** (currently OG tags use text only, no image) — a simple branded 1200×630 image would make shared links look more polished on social apps.
- **Light/dark theme toggle**, if some visitors would prefer a light mode.
- **A real backend for Website Monitor** — the browser-only uptime check is CORS-limited; a small server worker would allow real scheduled checks and reliable alerts.

## 2026-09-14 professional polish + QA pass
- Fixed a real bug in the Zakat Calculator (Islamic Tools): an invalid `Math.max(0, ...)` spread over a plain number threw a JavaScript error on "Calculate estimated zakat" and the tool never produced a result. It now returns the correct zakatable amount and 2.5% estimate.
- Fixed the Credit Cards page hero: leftover CSS from an older light theme (transparent white panel + large reserved padding for an image that no longer renders) made the "Credit Card Picks" heading almost unreadable. It now uses the same dark card styling as the rest of the site.
- Fixed the File Converter page: several elements (`status-badge`, `feature-card`, `feature-icon`, the drop zone, the DOCX/XLSX/PPTX preview cards) had no matching dark-theme styles and rendered unstyled or in the old light palette. All now match the site's dark theme.
- Fixed low-contrast icon badges: `.collection-icon` (used on the Business, Career, Testing, Website Tools, API, AI Tools and Islamic hub pages) kept a light background after the icon color was themed dark, making plain-text icons (GST, JSON, JWT, QA, CV…) hard to read. Badges are now dark with light accent text/emoji everywhere.
- Unified the homepage category icons and a few tool icons that mixed full-color emoji with the site's flat icon language (now `∑`, `BIZ`, `</>`, `QA`, `CV`, `GST`, `MKP`, `B/E`, `INV`, `PWD`, `ID`, matching the existing style used elsewhere).
- Softened the unconfigured ad-slot placeholder copy so visitors see "Advertisement space — Reserved for a future ad placement" instead of internal file/variable names; the technical instructions for the site owner are now in a hover tooltip instead.
- Automated a full Playwright crawl of all 30 pages (desktop + mobile) plus every modal tool: no console errors, no JavaScript exceptions, and no broken local references after the fixes above.

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

## 2026-09-14 (later) — Loans/Credit Cards spotlight, AI Tools rewrite, stronger resume builder, more ad inventory

- **Loans and Credit Cards are now the first thing a visitor sees.** Added a bold, high-contrast "featured strip" of two large gradient cards (Loans in green/gold, Credit Cards in purple) as the very first element on the homepage, above the hero — with a pulsing hover animation and clear calls to action ("Explore Loans →", "Compare Cards →"). This is in addition to the existing quick-access cards and nav entries, so both sections get emphasized from the moment the site loads, on both desktop and mobile.
- **AI Tools page fully rewritten.** Replaced the old single-goal filter (which only showed 3 tools at a time) with a complete, always-visible catalog organized into 8 categories — Writing & Content, Image Generation & Design, Video, Coding & Development, Research & Studying, Audio & Voice, Productivity & Meetings, and Business & Marketing — each with a jump-to-section nav, a short blurb on what the category is for, and 3 tools per category (24 tools total) with a "Best for: …" line explaining exactly what each tool is strongest at (e.g. Runway for generating new video vs. CapCut for editing existing footage, Claude for long-form reasoning vs. ChatGPT for general writing). One top pick per category is badged. Every tool card has a "Try this tool" button wired to `AI_AFFILIATE_LINKS` in `site.js` — add a URL for any tool key there and the button automatically activates with a `nofollow sponsored` link; until then it shows "Affiliate link not added yet" instead of a broken link.
- **ATS Resume Builder is stronger.** Added a live "Resume Strength Score" panel (0–100, with a color-coded ring and an 8-item checklist) that updates as you type. It checks: contact-info completeness, summary length/focus, having 2+ roles, 2+ bullet points per role, whether achievements are quantified (numbers/%/currency in bullet points), whether bullets avoid weak phrases like "responsible for"/"worked on" in favor of strong action verbs, education present, and 5+ skills listed. Each failed check shows a specific, actionable tip. This gives visitors real, concrete feedback instead of just a static form.
- **More ad inventory sitewide, including the homepage.** Added an additional "in-content" ad slot to all 35 non-homepage pages and a 4th slot to the homepage (top/incontent/middle/auto-bottom). While adding these, found and fixed two ad-layout bugs this introduced or exposed: (1) the new slot landing directly against an existing ad slot with no content between them on ~14 pages (all loan pages, several calculators, videos, and several tool-hub pages) — relocated each to a spot with real content on both sides instead of stacking; (2) a pre-existing issue on 6 calculator pages (GST, Business hub, Break-even, Invoice, Markup, Profit Margin) where the "top" and "middle" ad slots were already stacked back-to-back before the calculator tool — relocated the "middle" slot to a natural mid-page break instead. Verified with an automated scan across all 37 pages that no two ad slots are adjacent with no content between them.
- Full Playwright regression crawl of all 37 pages (desktop + mobile) after all of the above: no console errors, no JavaScript exceptions, every ad slot renders, and the new homepage strip, AI Tools catalog and resume-strength panel were each verified with real interaction tests (anchor-jump navigation, live score updates when editing form fields, mobile layout).
