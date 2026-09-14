# Converter QA Report

## Tested in the build environment
- Python syntax: PASS
- site.js syntax: PASS
- Converter health endpoint: PASS
- DOCX -> PDF through HTTP endpoint: PASS
- XLSX -> PDF through HTTP endpoint: PASS
- PPTX -> PDF through HTTP endpoint: PASS
- PDF output validation: PASS

## Windows engine design
- Microsoft Word COM export is preferred for DOC/DOCX/RTF/ODT when Word is installed.
- Microsoft Excel COM export is preferred for XLS/XLSX/CSV/ODS when Excel is installed.
- Microsoft PowerPoint COM export is preferred for PPT/PPTX/ODP when PowerPoint is installed.
- LibreOffice is the fallback Office rendering engine.
- The launcher checks the actual engine before opening the converter page.

## Important
A browser-only HTML page cannot perform exact Microsoft Office rendering without a local or hosted Office rendering engine. The converter therefore uses a local engine rather than silently converting Office documents into plain text.
