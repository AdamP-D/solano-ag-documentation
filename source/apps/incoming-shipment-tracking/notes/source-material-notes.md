# Incoming Shipment Tracking (IST) — Source Material Synthesis Notes

Sources reviewed:
- `Technical Documentation/Incoming Shipment Tracking - Technical Documentation.docx` (KCI / Andrew Blowers, v1.0, 4/17/2024)
- `Technical Documentation/IST User Guide.docx` (v1.1, 4/17/2024)
- `Technical Documentation/Incoming Shipment Tracking - Testing Document.docx`
- `Incoming Shipment Tracking - Whiteboarding.pptx`, `README.docx`
- Extracted ArcGIS JSON: `json_export_20260701_153734/` (10 items; authoritative fields/domains)

> Excluded: the database password in the Technical Documentation; the archived "OLD DO NOT USE" user doc.

## Overview / Background
- Tracks incoming agricultural shipments that require Ag Department inspection.
- Built by KCI late 2022–mid 2023; reworked early 2024 for a more cohesive office/field experience. POC: David Jagdeo.
- Components: Field Map + Web Map, Web AppBuilder desktop app, Web Dashboard + Mobile Dashboard. Data in PostgreSQL "agdept", referenced services.

## Data model
- IST records are stored in the **Incoming Shipment Tracking table** (attachments enabled), **related to Parcels REGIS** (a copy of the County cadastral). Records are created against a parcel.
- **Attribute rules** auto-populate ParcelID, Parcel Address, Parcel Common Name (from parent parcel), the **IST ID**, and the **Status** (calculated from the dates/result).
- Two database views: `v_ist_all_records`, `v_ist_inspector_view` (aggregates records per parcel, action status + counts; drives the dashboard).

## Status lifecycle (auto-calculated)
Incoming Shipment (notified, not arrived) → Requires Inspection (arrived, not completed) → Reinspection Needed - On Hold (partial release / on hold) → Complete (+ result variant: Inspected and Released, Reconditioned and Released, Forwarded to Other Agency, Rejected/Returned/Destroyed, Released by Phone).

## Fields (authoritative)
status (calc, domain), insp_type (GWSS, Other, Seed 008, Spongy Moth/Spotted Lanternfly, 008, Truck – Plant, etc.), invoice_number, notice_number (008), shipper, inspctr_initials, notified_of_shipment, arrived, partial_release, on_hold, completed, result (domain), comments, ist_id (calc), parcelid/address/common_name (calc).

## Map & Layers
Inspector View; Status group (Incoming Shipments, Requires Inspection, Reinspection Needed – On Hold, Complete); All Records; Tracking By Period group (Today's Records, Completed This Month / Current & Previous Fiscal Year / Current & Previous Calendar Year); Parcels REGIS; GWSS Trap Grids; County Boundary. Symbology by status — yellow (incoming/notified), orange (requires inspection/arrived), blue (completed today).

## Dashboards
Web + Mobile. Inspector View list (by Action Status) for dispatch; IST records list (details); indicators: Total Today, Incoming Shipments, Action Required, Completed Today. Mobile dashboard list item has a hyperlink that launches Field Maps and searches the ParcelID.

## Roles
- Office staff / inspectors (create/edit records, dispatch via dashboard), field inspectors (Field Maps), management (dashboards). POC David Jagdeo. Developer KCI (Andrew Blowers).

## Workflows
Create IST record on a parcel (web app or Field Maps) → populate notified/arrived/completed dates + result → status auto-updates and drives symbology/dashboards. Create placeholder Parcels REGIS polygon if none exists. Export via attribute table CSV.

## Known Issues & Gaps
- **Daylight saving time is hard-coded** in `v_ist_inspector_view` ("minus 7 hours"); the view SQL must be manually updated (subtract 8 hours in three places) when DST ends, and reverted when it begins.
- **Offline limited**: only the Field Map feature service supports offline; the Views, County Boundary, and GWSS Trap Grids do not. Full offline needs a new map or reconfigured services.
- **Parcels REGIS is a copy** from the authoritative sc_prime cadastral and will not stay in alignment.
- Parcel geometry editing is disabled after creation; the Result field is hidden until Completed is populated.
