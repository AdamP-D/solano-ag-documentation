# Task 10b Report — Incoming Shipment Tracking Technical Reference

## Sections Authored

- **Section 1 (Solution Architecture):** Web AppBuilder app + Esri Field Maps + Web Dashboard + Mobile Dashboard; PostgreSQL "agdept" referenced services; IST records related to Parcels REGIS (copy of sc_prime cadastral); five attribute rules + two database views drive automation.
- **Section 3 (Services & Publishing — narrative):** Three referenced services (main FeatureServer, Field Map FeatureServer with archiving, Views MapServer); Pacific-time-zone configuration; archiving on Field Map service only with offline limitation noted; ArcGIS Pro project path included. One-sentence note that generated tables reflect items captured in the JSON export.
- **Section 8 (Database View Definitions):** 2 views with verbatim SQL from source doc.
  - `v_ist_all_records`: joins IST table to Parcels REGIS; provides flat geometry-bearing record set for All Records layer.
  - `v_ist_inspector_view`: aggregates per-parcel, computes action status + counts; drives dispatch list. Hard-coded DST offset ("minus 7 hours") noted with explicit instruction to change to "minus 8 hours" in three locations when DST ends.
- **Section 9 (Attribute Rules):** 5 calculation rules with verbatim Arcade from source doc: ParcelID (Insert), Parcel_Address (Insert), Parcel Common Name (Insert/Update), IST ID (Insert/Update), Status (Insert/Update).
- **Section 10 (Geoprocessing / Automation):** "None." statement as specified.
- **Section 11 (Map / App Layer Definitions):** Status group layers, Inspector View layer, All Records layer, Tracking By Period group (6 definition-query layers: Today's Records; Completed This Month / Current & Previous Fiscal Year / Current & Previous Calendar Year). Dashboard color coding: yellow = Incoming Shipment, orange = Requires Inspection / Reinspection Needed - On Hold, blue = Complete.

## Generated Sections (auto-injected, markers left intact)

- Section 2 (Portal Items): 10 items from JSON export
- Section 3 (Services table): 6 services from JSON export
- Section 4 (Database Schema): full field tables from JSON export
- Section 5 (Domains): all coded-value and range domains from JSON export
- Section 6 (Subtypes): from JSON export
- Section 7 (Relationships): from JSON export

## Verification Results

- `grep -c "insp_type\|Requires Inspection\|v_ist_inspector_view"`: **36** (non-zero — PASS)
- `grep -c "<REDACTED-DB-PASSWORD>"`: **0** → `no-secret-good` (PASS — database password excluded)

## Views and Attribute Rules Included

- **2 views** with verbatim SQL: `v_ist_all_records`, `v_ist_inspector_view`
- **5 attribute rules** with verbatim Arcade: ParcelID, Parcel_Address, Parcel Common Name, IST ID, Status

## Commit

`e0dc16e` — "docs: Incoming Shipment Tracking technical reference"
