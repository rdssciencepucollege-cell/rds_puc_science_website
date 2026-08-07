# Link & Asset Audit — RDS PU Science Website

Generated: 2026-08-07

Summary
- Pages scanned: 11 HTML files
- External assets found: Google Fonts, Tailwind CDN, Google Drive links, Google Maps, WhatsApp links
- Local images: all referenced `images/` files exist in the repository
- PDFs: not stored in repo; downloads link to Google Drive folders

Per-page findings

- about.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; local images: `rds-founder.png`, `chairman-rds.jpg`, `principal-rds.png`.
- academics.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; local images: `vid-teach-collage-hori.png`, `vid-teaching-bio-vert.png`, `rds-corridor.png`, `rds-chem-lab.png`.
- admissions.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; external link to WhatsApp `https://wa.me/#` (placeholder) and `https://wa.me/918312400000` (contact); no local PDFs.
- contact.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; external links: `https://maps.google.com`, `https://wa.me/918312400000`; mailto links present; local images none beyond standard header/footer.
- downloads.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; multiple links to Google Drive folders (these host the PDF documents). Several in-page PDF indicators exist but files are remote (Google Drive). No local `.pdf` files are tracked (covered by .gitignore).
- events.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; no external documents detected.
- facilities.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; local images: `rds-rightwing-building.png`, `vid-teaching-bio-vert.png`, `rds-physics-lab.png`, `rds-chem-lab.png`, `rds-bio-lab.png`, `vid-teaching-hori.png`, `college-from-ground.jpg`, `rds-sports.png`, `rds-corridor.png`.
- faculty.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; local images: various `vid-teach*` and `rds-*` images.
- gallery.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; local images: `college-from-ground.jpg`, `rds-corridor.png`, `rds-chem-lab.png`, `rds-sports.png`, `rds-bio-lab.png`.
- index.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`; many local images used in hero and sections: `college-from-ground.jpg`, `vid-teaching-hori.png`, `rds-college-aerial-view.jpg`, `vid-teaching-bio.png`, `rds-founder.png`, `chairman-rds.jpg`, `principal-rds.png`, `vid-teaching-bio-vert.png`, `vid-teach-collage-hori.png`.
- news.html: external CSS `fonts.googleapis.com`; external JS `cdn.tailwindcss.com`.

Notes & Recommendations
- Local images: all referenced images exist in `images/` directory.
- External resources: Google Fonts and Tailwind CDN are used site-wide; consider self-hosting fonts and bundling Tailwind for full offline availability and to avoid external dependencies.
- Downloads: actual PDFs are hosted on Google Drive. If you want PDFs in the repo, download them and add to `downloads/` (note: they will be ignored by current `.gitignore` which includes `*.pdf`). Remove `*.pdf` from `.gitignore` if you intend to commit them.
- Broken / placeholder links: `https://wa.me/#` in `admissions.html` is a placeholder — replace with a valid number or remove.
- Security: external links opening in new tabs use `rel="noreferrer noopener"` in `downloads.html` which is good practice.

Optional next steps
- Run HTTP HEAD checks for external links (I can do this on request).
- Replace external assets (Google Fonts / CDN) with local copies for performance and offline use.
- Optionally produce a CSV of all assets for automated checks.

Report file: [link-audit-report.md](link-audit-report.md)
