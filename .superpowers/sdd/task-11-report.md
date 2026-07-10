# Task 11 Report — Full Build, Verification, and Legacy Cleanup
Date: 2026-07-01

## Build Output
```
generated tech-ref sections: gwss
generated tech-ref sections: incoming-shipment-tracking
generated tech-ref sections: weeds-invasives
site pages: 11 -> C:\Projects\Solano\Ag\Documentation\build\site
pdfs: 9
```

## Site Structure (build/site)
- index.html, search-index.json
- gwss/: knowledge-base.html, requirements.html, technical-reference.html
- weeds-invasives/: knowledge-base.html, requirements.html, technical-reference.html
- incoming-shipment-tracking/: knowledge-base.html, requirements.html, technical-reference.html

## PDF Output (build/pdf)
- gwss/: knowledge-base.pdf (216 KB), requirements.pdf (148 KB), technical-reference.pdf (2.15 MB)
- weeds-invasives/: knowledge-base.pdf (173 KB), requirements.pdf (131 KB), technical-reference.pdf (412 KB)
- incoming-shipment-tracking/: knowledge-base.pdf (178 KB), requirements.pdf (129 KB), technical-reference.pdf (1.01 MB)

## Secret Check
Pattern: <REDACTED-DB-PASSWORD>
Searched: build/ and source/apps/*/content/
Result: clean

## Legacy Folder Removal
Removed via `git rm -r`:
- GWSS/
- Weeds & Invasives Treatment Application (ToH)/
- Incoming Shipment Tracking/
All content is preserved under source/apps/ and in git history.

## Final Structure
source/apps/: gwss, incoming-shipment-tracking, plant-pest-other, pq-inspection-tracking, weeds-invasives
tooling/: build.py, build_pdf.py, build_site.py, extract_item_json.py, generate_tech_reference.py, md_to_html.py, tests/

## Commit
Hash: 11569b6
Message: chore: full build verified; remove legacy app folders
247 files changed, 490 insertions(+), 172809 deletions(-)

## Status
DONE

---

# Task 11 Addendum — Cohesion Fix: PDF HTML under build/
Date: 2026-07-01

## Fix Applied
Modified `tooling/build_pdf.py` `build()` to write intermediate HTML to `out_dir/<slug>/<doc>.html` instead of calling `md_to_html.convert()` (which wrote next to the source .md). Removed 9 stray committed `.html` files from `source/apps/*/content/`.

## Results
- Unit test: OK (2 tests)
- PDFs generated: 9
- Stray source HTML: 0
- Commit: d2bc24e — fix: render PDF intermediate HTML under build/, not in source tree

## Status
DONE
