# Task 10a Report — Weeds & Invasives Technical Reference

## Sections Authored

- **Section 1 (Solution Architecture):** Survey123 form + Field Maps web map + Web AppBuilder tracking app; PostgreSQL "agdept" referenced services; arcgis-survey123:// hyperlink structure with parcel attribute field mappings (no credentials included).
- **Section 3 (Services & Publishing narrative):** Referenced (not hosted) services; ArcGIS Pro project path; Survey123 form publish workflow; archiving/sync enabled on all four datasets; one-sentence note that generated tables reflect items in JSON export.
- **Section 8 (Database View Definitions):** None — edit-tracking views documented as future option, not implemented.
- **Section 9 (Attribute Rules):** None documented.
- **Section 10 (Geoprocessing / Automation):** None — Survey123 Inbox workflow drives the process; no GP services.
- **Section 11 (Map / App Layer Definitions):** "Ready to Treat" default of No (keeps points visible); six-stage treatment progression table (Initial Observation → Seeking Approval → Initial Treatment → Follow Up Treatment → Post Verification Revisit → Complete).
- Sections 2, 4, 5, 6, 7 and services table in 3: AUTO-GENERATED between markers (injected by generate_tech_reference.py).

## Grep Results

- `grep -c "Scientific Name\|treatment_stage\|Initial Observation"`: **13** (generated schema + authored narrative both present)
- `grep -c "<REDACTED-DB-PASSWORD>"`: **0** → `no-secret-good`

## Commit

Hash: `7bced18`
Message: `docs: Weeds & Invasives technical reference`
Files: `source/apps/weeds-invasives/content/technical-reference.md` (created, 240 insertions)
