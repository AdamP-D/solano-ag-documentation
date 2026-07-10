# PQ Inspection Tracking — Source Material Synthesis Notes

Sources reviewed:
- `PQ Inspection Tracking - Technical Documentation.docx` (KCI; v1.0 Andrew Blowers 5/3/2024, v1.1 Darbie Gibbs 2/27/2025, v1.2 Darbie Gibbs 5/9/2025)
- `PQ User Guide - DEV - V1.docx` (KCI / Andrew Blowers, v1.0 5/3/2024 — **DEV** version; URLs/item IDs are dev, not production)
- `README.docx`
- Extracted ArcGIS JSON: `json_export_20260709_155340/` (9 items; authoritative production field/domain data)

> The Technical Documentation contains a database password in plain text — excluded from all deliverables.

## Overview / Background
- Part of the "Ag Inspection Tool" built by KCI. The tool originally bundled Incoming Shipment Tracking, Plant/Pest/Other, and PQ Inspection Tracking, then split into groups/Portal content for access control. PQ became its own group ("Dev - PQ Inspection Tracking" in dev; production group separate).
- IT/GIS POC: **Daniel Machado**. Original dev Andrew Blowers (KCI); 2025 enhancements Darbie Gibbs (KCI).

## Architecture (corrects the JSON-only draft)
- **Data IS in the enterprise geodatabase (PostgreSQL).** Views reference `pq_inspection_tracking_evw` and `fieldboundaries_evw` — the `_evw` suffix confirms enterprise (versioned) geodatabase. Published through the Solano Enterprise Portal as a referenced service.
- Feature service `PQ_Inspection_Tracking/PQ_Inspection_Tracking/FeatureServer`: **Layer 0 = Field Boundaries** (polygon), **Layer 1 = pq_inspection_tracking** (table, Survey123 target).
- **Views MapServer** `PQ_Inspection_Tracking/PQ_Inspection_Tracking_Views/MapServer` — this is the piece the JSON export missed. Contains the "Inspection/Quarantine Status" and "All Records" view layers.
- **Four front ends**: Survey123 form, Web/Desktop App (Web AppBuilder), Dashboard, and Field Maps (the field map). The web app is embedded in the dashboard.
- **ArcGIS Pro project** (corrects "unknown"): `\\gis.solanocountygis.local\E\ServiceUpdates\PQ Inspection Tracking\PQ Inspection Tracking\PQ Inspection Tracking.aprx`

## Database Views (JSON export could not see these — from tech doc appendix)
- **`v_pq_inspection_tracking_all`** — joins `pq_inspection_tracking_evw` to `fieldboundaries_evw` on `fieldboundary_guid = globalid`; exposes every PQ field plus the field-boundary geometry ("All Records" layer). Not date-filtered.
- **`v_pq_inspection_tracking_status`** — same join, plus a CASE expression that consolidates `inspection_status` + `quarantine_status` into ONE `status` field (Standby, Priority, 1st/2nd/3rd Walk Complete, Hold, Quarantine, Complete). Drives the "Inspection/Quarantine Status" layer, which is filtered to exclude Complete and records outside the current calendar year.
- Full SQL for both is preserved verbatim in the Technical Reference §8.

## Record lifecycle (Survey123 Inbox model)
- **New records are ALWAYS initiated from Field Maps** — select a Field Boundary polygon → "Launch Survey123" hyperlink in the popup. Survey123 creates the record; the popup passes `field:incoming_id={GLOBALID}` via an `arcgis-survey123://` link.
- **Edits happen through the Survey123 Inbox** to consolidate all values into one table record. Inbox excludes "Complete" records. Refresh Inbox before going offline to avoid overwriting another user's edits.
- 5-page form; Send Now / Save in Outbox (all-or-nothing) / Save in Drafts (device-local).

## Survey123 linked-content CSVs (support the form's choice lists / auto-populate)
- `applicant_address.csv` — Applicant → Address (and, after 2/27/2025, Contact Name & Phone) auto-populate.
- `grower_pesticide_perm_num.csv` — Grower → Pesticide Permit Number pair.
- `commodity_walk_days.csv` — Commodity → estimated days to 1st/2nd walk (`fw_est_days`, `sw_est_days`).

## Enhancement history (from tech doc)
- **2/27/2025**: Additional Pest Notes 255→2000 chars; Applicant now also auto-populates Contact Name & Phone (via CSV); added **Lead Inspector** field (150 chars) to each walk; added **Additional Time** field to each walk (rolled into total billable time calc).
- **5/9/2025**: Survey123 **web-form** compatibility (popup now offers a browser link, pinned to Survey123 `version=3.21` to dodge a 3.22 webform bug; CSV headers de-capitalized/de-spaced; form questions moved into field-list groups for Pages mode).

## Map / App layers
Field Boundaries (reference, but editable via Edit widget/Field Maps), Road Centerlines (from AGOL org SCn6czzcqKAFwdGU), County Boundary, PQ Inspection Tracking Views group (Inspection/Quarantine Status, All Records), PQ Inspection Tracking (S123 Submissions) table.

## Known Issues & Gaps
- Field-boundary ↔ inspection link is a stored Global ID (`fieldboundary_guid`), not a registered relationship class — the views enforce the join, not the database.
- Inspection Status is set manually by the inspector; no attribute rule auto-advances it (contrast IST, which auto-calculates status).
- Records use PLSS (Section/Township/Range), not a parcel ID.
- Field Maps/Dashboard/Web app hyperlink launches do NOT refresh the linked CSV lists — the form must be opened directly in Survey123 for CSV updates to download.
- Stacked geometry: multiple PQ records for one field all draw on the same boundary polygon.
