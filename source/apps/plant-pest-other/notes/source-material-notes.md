# Plant, Pest & Other Inspections — Source Material Synthesis Notes

Sources reviewed:
- `Plant, Pest, and Surveys - Technical Documentation.docx` (KCI / Andrew Blowers, v1.0 6/16/2023) — the **umbrella** technical doc covering the whole "Plant, Pest, and Surveys" solution (IST + PQ + PPO)
- `Plant Pest and Other  - User Documentation.docx` (KCI / Andrew Blowers, v1.0 12/18/2023) — PPO-specific user guide
- `README.docx`
- Extracted ArcGIS JSON: `json_export_20260709_163857/` (8 items) — **note: the PPS feature service and views map service were OFFLINE at export**, so JSON schema is incomplete; the vendor docs are the authoritative architecture source here.

> The umbrella Technical Documentation contains a database password in plain text — excluded from all deliverables.

## Overview / Background
- Part of the "Ag Inspection Tool" (KCI, late 2022–mid 2023). The tool split into groups: one for **Incoming Shipments + Plant/Pest/Other**, another for PQ. PPO lives in the **"Incoming Shipments and PPO Inspections"** portal group (id 325f3033…).
- Supports inspections for various plants/pests and an "other" bucket = **Resident Complaint / CDFA / County Follow Up**. Umbrella doc lists survey types **SOD, SLF, BW, AWB, ESFY** plus the resident-complaint/CDFA/county-follow-up type. Inspection Type defaults to **"Plant Pest & Other Inspection."**
- Stakeholder: Agriculture Department. POC: **Matthew Carl**. Developer: KCI (Andrew Blowers).

## Architecture (CORRECTS the JSON-only draft — it is a related-records model, like IST, not a standalone point layer)
- **Two parent point feature classes**, each 1:M to one related table:
  - **Address Points** — pulled from the **SC_Prime** database (County NG911/NENA address points). Used when the inspection site has an address.
  - **Inspection Points (PPO)** — created for inspections where **no address is available**. Has three symbology templates (Active etc.); users generally pick "Active."
- **Plant Pest and Other Inspections** — the **related table** holding the actual inspection record (+ photo/file attachments). One record per inspection, edited until complete. 1:M from either parent point.
- **Two database views** combine parent point + related record for display (non-editable, update dynamically):
  - **PPS IP PlantPestOther Inspections (View)** — Inspection Points (PPO) + related record
  - **PPS PlantPestOther Inspections (View)** — Address Points + related record
  - View SQL is **not reliably available**: the umbrella tech doc's appendix contains `v_gwss_*` views (copy-pasted from the GWSS doc template), NOT these PPO views. Retrieve real SQL from pgAdmin.
- Point features carry `insp_type` / `insp_status` (symbology drivers; JSON popup also showed `insp_date`, `inspector`, `address`, `comments`). Address Points carry the full NG911 field set (`site_nguid`, `apn`, `fulladdress`, street components, lat/long).

## Services (from JSON manifest + umbrella doc)
- **PPS Plant Pest Other Insp** — `PlantPestandSurveys/PPS_Plant_Pest_Other_Insp/FeatureServer` (OFFLINE at export). Holds Inspection Points, Address Points, and the related table.
- **PlantPestandSurveys_Views** — `PlantPestandSurveys/PlantPestandSurveys_Views/MapServer` (OFFLINE at export). Holds the combining views.
- Spatial reference: NAD 1983 2011 StatePlane California II FIPS 0402 (Feet), WKID 6418 / legacy 103004.
- ArcGIS Pro project (umbrella doc, note this is a KCI dev path and is GWSS-labeled): `C:\Users\kci-5\Documents\ArcGIS\Projects\GWSS` — treat as unverified for PPO; confirm with GIS team.

## Front ends (PPO-specific)
- **Plant Pest Other Insp – Field Map** (web map, id 97652afc…) for Esri Field Maps — select an Address Point or Inspection Point, open the related table, add/edit the inspection record + attachments.
- **Plant Pest Other Insp Web App** (Web AppBuilder, id 24f20646…). Widgets: Search (place/address/APN/Inspection Point), Select, **Edit** (create/edit points + related records + attachments; auto-saves, deletes are not undoable), **Query** (predefined tasks against points and both views), Legend, Layer List, Basemap Gallery, Bookmarks.
- No Survey123 form and no PPO-specific dashboard. (The umbrella "Plant Pest and Surveys – Management Dashboard" exists at the solution level but is not part of the PPO export.)

## Map layers (from user doc)
GWSS Trap Grids, Inspection Points (PPO), Address Points, PPS IP PlantPestOther Inspections (View) [off by default], PPS PlantPestOther Inspections (View) [off by default], County Boundary, Plant Pest and Other Inspections (data table).

## Known Issues & Gaps
- **Schema not captured**: PPS feature service + views map service were offline at export; field types, lengths, and `insp_type`/`insp_status` domain values need verification against the live service/pgAdmin.
- **View SQL missing/wrong in vendor doc**: umbrella appendix holds GWSS views, not PPO views — get real SQL from pgAdmin.
- **Address Points required fields**: can be filled with placeholder data in the field and reconciled later against SC_Prime.
- **Edit widget deletes** (features, related records, attachments) are immediate and cannot be undone.
- Address Points is a copy sourced from SC_Prime and will drift from the authoritative cadastral/address source over time.
