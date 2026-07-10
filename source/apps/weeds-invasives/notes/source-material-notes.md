# Weeds & Invasives Treatment Application — Source Material Synthesis Notes

Sources reviewed:
- `W&I Treatment Application -  Technical Documentation.docx` (KCI / Andrew Blowers, v1.0, 6/16/2023)
- `W&I Treatment Application - User Documentation.docx` (KCI / Andrew Blowers, v1.1, 12/22/2023)
- Extracted ArcGIS JSON: `json_export_20260701_104733/` (6 items; authoritative field/domain data)

> Note: the Technical Documentation contains a database password in plain text. It has been excluded from all deliverables.

## Overview / Background
- Built by KCI for Solano County DOIT / Agriculture Department, late 2022 – mid 2023.
- Originally for Tree of Heaven (ToH); expanded to cover all weed/invasive species treatments.
- A Survey123 form drives the whole treatment lifecycle in ONE record per treatment. Supported by a Field Maps web map and a Web AppBuilder tracking/editing app.
- Data in enterprise PostgreSQL "agdept" DB, published as referenced services. 4 datasets: wi_treatment_tracking, wi_treatmentpoints, wi_r_treatment_areas, wi_r_files.

## Components / Integrations
- Survey123 form "Weeds and Invasives Treatment Application" (id 5b176ab3…) — launched from the Parcels REGIS pop-up hyperlink, which passes parcel attributes into the form.
- Web map "Weeds and Invasives – Tracking and Field Map" (Field Maps).
- Web AppBuilder app "Weeds and Invasives Treatment App – Tracking and Field Data" (edit/search/select/legend/layer list/basemap/bookmarks widgets).
- Feature services: WI Treatment Application S123 (Survey123 submissions + related areas/files), WI Treatment Tracking (tracking points). Parcels REGIS (authoritative cadastral).
- Archiving/sync enabled for offline.

## Roles
- Agriculture Department field staff (collect via Survey123 / Field Maps), office staff (edit/track via web app), GIS staff (maintain). POC: Matthew Carl. Developer: KCI (Andrew Blowers).

## Workflow (treatment lifecycle stages)
Initial Observation → Seeking Approval → Initial Treatment → Follow Up Treatment → Post Verification Revisit → Complete. One Survey123 record edited through the Inbox across stages. Tracking points capture approval/readiness separately.

## Data (authoritative from JSON)
- **WI Treatment Tracking** (points): Observation Confirmed, Assessee/Tenant Approval Received, Follow Up Date, Post Verification Date, Treatment Stage, Ready to Treat (default No), Treatment Complete Date.
- **wi_treatmentpoints** (Survey123 submissions): assessee/site info (passed from parcel), Scientific/Common Name (Calflora domain), per-stage date/observer/result/comment fields, lat/long/accuracy.
- **wi_r_treatment_areas**: treatment area polygons related to a point.
- **wi_r_files**: file attachments by treatment stage.

## Map & Layers
WI Treatment Tracking Points, WI Treatment Points (Survey123), WI Treatment Areas, Parcels REGIS. "Ready to Treat" default No so points remain visible.

## Known Issues & Gaps
- Edit tracking on wi_treatmentpoints not in initial scope (future: stage-change views into the app).
- Survey123 Outbox is all-or-nothing (sending one sends all) — use Drafts for in-progress records.
- Attachments not visible in the Inbox after submission.
- In the web app, Survey123 point/area attribute editing is disabled (geometry only) to avoid conflicts with the Survey123 record.
- Individual vertex edits and attachment deletes cannot be undone.
- Discipline required: one form per treatment, edited via Inbox — do not launch Survey123 directly.
