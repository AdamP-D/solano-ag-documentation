# GWSS — Source Material Synthesis Notes

Working notes mapping source material to each document section. Sources reviewed:

- `GWSS Technical Documentation KCI.docx` (KCI / Dave Thompson, v1.3, 4/25/2022)
- `Development/GWSS Inspection - High Level Requirements.docx`
- `Development/GWSS Workflow.pptx`
- `Development/GWSS GP Service.docx`
- `GWSS Maintenance Enhancement - Symbology Update.docx`
- `Esri Bug Writeup - Updating Domain in Feature Service.docx`
- `From Matthew Carl/` data logs (Trap Routes, Pesticide & Survey Log, Treatment Log, Confirmed Counts)
- Extracted ArcGIS JSON: `json_export_20260630_134912/` (24 items; authoritative current field/domain/subtype data)

> Note: the High Level Requirements file contains some content copied from an unrelated **Fire District Inspection** project (Cordelia, LE-100 form). That content was ignored; only GWSS-relevant material was used.

> Note: the Technical Documentation contains a database password in plain text. It has been deliberately excluded from all deliverables.

---

## App Overview ← Technical Doc (Overview), High Level Requirements
- Glassy-Winged Sharpshooter (GWSS): pest harmful to Solano County agriculture; vector of Pierce's Disease, a threat to grapevines/vineyards.
- Solution developed late 2021 / early 2022 by KCI for Solano County DOIT–GIS, on behalf of the Agricultural Commissioner's program. Point of contact: Matthew Carl.
- Purpose: replace spreadsheet/Google-Maps tracking with a GIS solution for trapping, lab-confirmed findings, quarter-mile survey response, and pesticide treatment.

## User Roles ← High Level Requirements ("Account set up"), Technical Doc
- Viewers (upper management, view-only): Ed King, Pricilla Yeaney
- Creators / office staff: David Jagdeo, Matthew Perryman, Matthew Carl
- Field workers / biologists: Addison Meinke, Catherine Blazy, Tony Avina, Samantha Benavente
- GIS administrator / maintainer: KCI + Solano County DOIT–GIS

## Key Workflows ← GWSS Workflow.pptx, GP Service doc, High Level Requirements
1. Place & document traps (Field Maps)
2. Record a GWSS finding; send sample to lab; record PDR# (web app or Field Maps)
3. Confirm lab result → toggle "1/4 Mile Survey Required" → run GP tool → buffer + tag parcels
4. Field visual survey of tagged parcels (Field Maps); record survey, findings
5. Treatment "knock & talk", consent, foliage/soil pesticide application
6. Track status on the map / export lists

## Data Captured ← extracted JSON (authoritative), Workflow.pptx schema slides, Technical Doc views
Datasets: GWSS Traps, GWSS Findings, GWSS Survey Areas, GWSS Tracking (parcels), GWSS Tracking History, GWSS Surveys (table), GWSS Treatment (table), GWSS Biological Control, GWSS Trap Grids, Quar Boundary. Field aliases/domains taken from JSON layer definitions.

## Map & Layers ← Symbology Update doc, Workflow.pptx (Map Layers slides), web map JSON
- Parcels symbolized by `gwss_action` / `status`, `survey_result`, and `treatment_status` (driven by database views).
- Red = requires inspection; purple = partial refusal; notice colors Green/Yellow/Blue/Pink for treatment stage. Trap grids labeled, not selectable, off by default. Biological Control off by default.

## System Integrations ← Technical Doc (Components, Data Services, GP Tool)
- Enterprise PostgreSQL DB (referenced services, not hosted). ArcGIS Enterprise (Portal/Server) at solanocountygis.com.
- Esri Field Maps (mobile), Web AppBuilder app (desktop), Smart Editor widget, Geoprocessing widget.
- GP service `GWSSQuarterMileAnalysis_ParcelInspectionTag` for buffer/tag automation.
- 8 database views power holistic/most-recent symbology and analysis.

## Glossary ← all sources
GWSS, Pierce's Disease, PDR#, APN/ParcelID, quarter-mile survey, knock & talk, foliage vs soil treatment, infested vs adjacent, Field Maps, Web AppBuilder, referenced service, domain, GP service.

## Background & Purpose (Req) ← Technical Doc, High Level Requirements
See App Overview. Replaced manual spreadsheets ("Confirmed GWSS Counts", "Pesticide & Survey Log") and Google-Maps visual survey method.

## Stakeholders (Req) ← High Level Requirements, Technical Doc
Owner: Solano County Agricultural Commissioner / DOIT–GIS. POC: Matthew Carl. Developer/Maintainer: KCI (Dave Thompson). Plus roles above.

## Functional Requirements (Req) ← High Level Requirements (baseline) + Workflow.pptx + JSON (as-built confirmation)
Map view, trap logging, finding logging, lab/PDR tracking, survey-required toggle, GP buffer/tag tool, field survey entry, treatment entry & consent, status symbology, list export, role-based access.

## Data Requirements (Req) ← JSON layer definitions, Technical Doc datasets/views
Every dataset + the 8 views.

## Known Issues & Gaps (Req) ← Esri Bug Writeup, Technical Doc (Enhancements/Bug Fixes), High Level Requirements (offline discussion)
- Esri domain-update bug: domain changes don't cascade unless all GWSS services are stopped/republished together.
- Smart Editor relationship-ID bug: republishing reordered relationship IDs, broke desktop Survey/Treatment editing; fixed by editing app JSON.
- Biological Control symbology: feature service can't preserve the intended semi-transparent ~4-house polygon symbology without a duplicate map service; only feature service was kept (editing prioritized).
- Offline Field Maps: complex; not fully implemented.
