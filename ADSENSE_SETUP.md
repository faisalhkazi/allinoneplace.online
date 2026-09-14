# Google AdSense setup for All In One Place

The website is prepared for AdSense but does not contain a fake publisher ID.

1. Create/sign in to Google AdSense.
2. Add `https://allinoneplace.online` under Sites.
3. Google will provide the site connection/ad code and review the site.
4. Send the exact AdSense publisher ID (`ca-pub-...`) to the site maintainer so it can be inserted into `site.js`, or paste Google's exact code into the `<head>` of the pages if Google asks for that method.
5. After Google provides an ads.txt entry, create `/ads.txt` at the site root using the exact line Google provides. Do not use the example file as a real ads.txt file.
6. For EEA/UK/Switzerland traffic, configure a Google-certified consent management platform through AdSense Privacy & messaging as required by Google's current consent requirements.

Do not invent a publisher ID or ads.txt line. Use only values supplied by Google.
