# PQ Inspection Tracking — Requirements Document

*Solano County Agricultural Program · As-built documentation of current functionality*

---

## 1. Background & Purpose

Solano County's Agriculture Department conducts plant quarantine (PQ) inspections on agricultural fields to enforce state and county quarantine regulations that restrict the movement of specific commodities. Managing these inspections requires capturing detailed field information, tracking progress through multiple walk-throughs, and recording the time and mileage for each walk for cost-recovery billing. Previously this information was tracked informally; the PQ Inspection Tracking solution provides a shared, map-based system that ties inspection records to field boundaries on the map and gives managers real-time visibility into inspection status.

The solution was built on the Solano County GIS platform using ArcGIS Survey123 for field data collection and ArcGIS Web AppBuilder for office review, published on the enterprise portal. Data is stored in the enterprise PostgreSQL database as a referenced feature service.

---

## 2. Stakeholders

| Name / Role | Relationship to System |
|-------------|------------------------|
| Solano County Agriculture Department | System Owner / Program Owner |
| Agriculture Department field inspectors | Primary Users (field data collection via Survey123) |
| Agriculture Department office staff | Primary Users (record review and management via web app) |
| Agriculture Department management | Dashboard users / oversight |
| Solano County DOIT–GIS | System owner (GIS platform); maintainer |

---

## 3. Current Functional Requirements (As-Built)

The following requirements describe what the system does today.

| # | Requirement |
|---|-------------|
| FR-01 | The system shall record each PQ inspection as a record in the `pq_inspection_tracking` table. |
| FR-02 | The system shall allow inspectors to draw a field boundary polygon on the map to define the geographic extent of the inspection site. |
| FR-03 | The system shall link each inspection record to its corresponding field boundary polygon via a stored Global ID (`fieldboundary_guid`). |
| FR-04 | The system shall provide a Survey123 form as the primary data collection interface for field inspectors. |
| FR-05 | The system shall provide a Web AppBuilder application for office staff to review, manage, and export records. |
| FR-06 | The system shall provide a dashboard summarizing inspection status counts and records. |
| FR-07 | The system shall capture the PQ number, site ID, commodity, commodity notes, variety, and acreage for each inspection. |
| FR-08 | The system shall capture the applicant, grower, contact name, phone number, and pesticide permit number. |
| FR-09 | The system shall capture the field's PLSS location (Section, Township, Range) and address. |
| FR-10 | The system shall capture approximate plant and harvest dates. |
| FR-11 | The system shall capture the quarantine status (None, Hold, or Quarantine) and allow it to be updated as the inspection progresses. |
| FR-12 | The system shall capture the inspection status (Standby, Priority, 1st Walk Complete, 2nd Walk Complete, 3rd Walk Complete, or Complete). |
| FR-13 | The system shall support up to three walk-throughs per inspection record (First Walk, Second Walk, Third Walk). |
| FR-14 | The system shall capture, for each walk: date, lead inspector, total number of inspectors, inspection start and end times, inspection time, drive time, additional time, total billable time, total number of vehicles, miles per vehicle, total billable miles, PDR number, and notes. |
| FR-15 | The system shall allow users to link a PQ inspection record to an Incoming Shipment Tracking record by storing the IST Global ID (`incoming_id`). |
| FR-16 | The system shall allow photo and file attachments to be added to inspection records. |
| FR-17 | The system shall capture estimated days and dates for the first and second walks. |
| FR-18 | The system shall track who created and last edited each record, and when. |
| FR-19 | The system shall support offline data collection and sync for the Survey123 form. |
| FR-20 | The system shall allow users to search, filter, sort, and export records in the web app attribute table. |
| FR-21 | The system shall display field boundaries on the map symbolized by their quarantine or inspection status. |
| FR-22 | The system shall initiate new inspection records from a field-boundary pop-up ("Launch Survey123"), so every record is tied to a field, and shall carry the triggering record's Global ID into the form. |
| FR-23 | The system shall support editing existing records through the Survey123 Inbox so that all of a field's values are consolidated into a single table record; the Inbox shall exclude records with a "Complete" status. |
| FR-24 | The system shall provide database views that join inspection records to their field-boundary geometry and consolidate the quarantine and inspection statuses into a single combined status for symbology, filtering the status view to the current calendar year and excluding "Complete" records. |
| FR-25 | The system shall auto-populate Address, Contact Name, and Phone from the selected Applicant, and the Pesticide Permit Number from the selected Grower, using linked-content CSV files. |

---

## 4. Current Data Requirements

| Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
|-----------------|---------|----------------------------|---------------|---------------|
| Field Boundaries (polygon feature layer) | Defines the geographic footprint of the inspection site on the map | Polygon geometry; edit-tracking fields only | Field inspectors (Survey123) | Provides the spatial record for each inspection; displayed on the web map |
| pq_inspection_tracking (table, no geometry) | The PQ inspection records | PQ Number, Site ID, Commodity, Variety, Acreage, Applicant, Grower, Contact, PLSS location, Quarantine Status, Inspection Status, Plant/Harvest dates, per-walk time and mileage fields, PDR numbers, incoming IST link | Field inspectors (Survey123) and office staff | The authoritative record of each PQ inspection from intake through completion |

Inspection records support photo and file attachments. Archiving (change tracking) is enabled on both the Field Boundaries layer and the pq_inspection_tracking table, providing a full edit history.

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Informal link between field boundary and inspection record.** The `fieldboundary_guid` field stores the polygon's Global ID but is not a registered ArcGIS relationship class; the join is resolved by the database views, not enforced by the service. | Display works via the views, but there is no referential integrity — an inspection record with a missing or wrong `fieldboundary_guid` will not draw on the map. | Records are initiated from a field boundary (which sets the GUID); avoid editing the GUID manually. |
| 2 | **Inspection status is manually maintained.** There are no attribute rules to auto-advance the status when walk dates are populated. | Inspector must update the Inspection Status field manually at each walk; inconsistency is possible if this step is skipped. | Enforce through training; consider adding a Survey123 relevant expression or attribute rule to prompt the update. |
| 3 | **No parcel ID / address link.** Records use PLSS coordinates (Section, Township, Range) rather than a parcel ID tied to the County's land records system. | Cannot automatically associate PQ records with the County's standard parcel or address datasets. | The field boundary polygon provides the spatial anchor; PLSS description serves as the written location reference. |
| 4 | **Dashboard is read-only.** The dashboard cannot be used to edit records; field edits must go through Survey123 or the web app. | Managers reviewing the dashboard cannot correct data errors without switching to another app. | Use the web app for any record corrections. |
| 5 | **Linked-content CSVs only refresh when the form is opened directly in Survey123.** Launching the form via a hyperlink from Field Maps, the Dashboard, or the Web App does not pull the latest Applicant/Grower/Commodity CSVs. | Users may see stale choice lists after a CSV update. | Open the PQ Inspection Tracking form directly in the Survey123 app once after any CSV update so the new lists download. |
