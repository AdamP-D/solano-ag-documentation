# Plant, Pest & Other Inspections — Requirements Document

*Solano County Agricultural Program · As-built documentation of current functionality*

---

## 1. Background & Purpose

The Solano County Agriculture Department conducts plant and pest inspections and surveys that fall outside the GWSS trap monitoring and plant quarantine programs — including pest/disease surveys (SOD, SLF, BW, AWB, ESFY) and an "other" category for Resident Complaint / CDFA / County Follow Up visits. Tracking these inspections in a shared, map-based system gives field staff a consistent way to log visits in real time from mobile devices and gives office staff immediate visibility into field activity without phone calls or paper logs.

The solution is part of KCI's "Ag Inspection Tool" and shares a portal group ("Incoming Shipments and PPO Inspections") with Incoming Shipment Tracking. It was built using Esri Field Maps for mobile data collection and ArcGIS Web AppBuilder for office review, published on the enterprise portal. Data is stored in the enterprise PostgreSQL geodatabase as a referenced feature service in the `PlantPestandSurveys` service folder, using a **related-records model**: inspection records are stored in a **Plant Pest and Other Inspections** table related one-to-many to two parent point feature classes — **Address Points** (from the County SC_Prime database) and **Inspection Points (PPO)** (for sites without an address). Two database views combine each point with its related record for display. Both the feature service and the views service were offline during the JSON export, so some schema details are inferred from the vendor documentation and web map popup configuration and require verification against the live service.

---

## 2. Stakeholders

| Name / Role | Relationship to System |
|-------------|------------------------|
| Solano County Agriculture Department | System Owner / Program Owner |
| Matthew Carl (Agriculture Department) | Point of Contact |
| Agriculture Department field inspectors | Primary Users (field data collection via Esri Field Maps) |
| Agriculture Department office staff | Primary Users (record review, editing, and export via web app) |
| KCI Technologies (Andrew Blowers) | Developer / vendor |
| Solano County DOIT–GIS | System owner (GIS platform); maintainer |

---

## 3. Current Functional Requirements (As-Built)

The following requirements describe what the system does today. Field and domain details marked with † are inferred from the web map popup configuration because the feature service was offline at export time; verify against the live service before using for schema-dependent work.

| # | Requirement |
|---|-------------|
| FR-01 | The system shall store each plant, pest, or other inspection as a record in the Plant Pest and Other Inspections related table in the enterprise PostgreSQL geodatabase. |
| FR-02 | The system shall relate each inspection record one-to-many to a parent point: an existing **Address Point** (from SC_Prime) when the site has an address, or an **Inspection Point (PPO)** created by the inspector when no address is available. |
| FR-03 | The system shall provide an Esri Field Maps–compatible web map for field inspectors to create and edit points and their related inspection records on mobile devices. |
| FR-04 | The system shall capture the inspection type for each record, defaulting to "Plant Pest & Other Inspection."† |
| FR-05 | The system shall capture the inspection status for each record.† |
| FR-06 | The system shall capture the inspection date, inspector name, site address, and comments for each record.† |
| FR-07 | The system shall allow photo and file attachments to be added to inspection records. |
| FR-08 | The system shall provide a Web AppBuilder application with Search, Select, Edit, Query, Legend, Layer List, Basemap Gallery, and Bookmarks widgets for office staff to create, edit, review, query, and export records and manage attachments. |
| FR-09 | The system shall provide two database views that combine each parent point (Inspection Point or Address Point) with its related inspection record for display and symbology. |
| FR-10 | The system shall allow inspectors to add new Address Points in the field, permitting placeholder values for required fields to be reconciled against SC_Prime later. |
| FR-11 | The system shall display GWSS Trap Grid polygons and the County Boundary as reference layers for geographic context. |
| FR-12 | The system shall track who created and last edited each record, and when. |

---

## 4. Current Data Requirements

| Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
|-----------------|---------|----------------------------|---------------|---------------|
| Plant Pest and Other Inspections (related table) | The inspection records — the core editable dataset (with attachments) | Inspection Type†, Inspection Status†, Inspection Date†, Inspector†, Comments†, attachments, edit tracking | Field inspectors (Field Maps) and office staff (web app) | Authoritative record of each plant/pest/other inspection; one record per inspection |
| Inspection Points (PPO) (point feature layer) | Parent point for sites without an address | Inspection Type†, Inspection Status†, Address†, edit tracking | Field inspectors / office staff | Anchors an inspection record to a map location where no Address Point exists |
| Address Points (point feature layer) | County address/site points (NG911/NENA standard), sourced from SC_Prime | Site NENA GUID, APN, Full Address, street components, lat/long, edit tracking | Sourced from SC_Prime; editable in-app | Parent point for sites with an address; searchable by Full Address / APN |
| GWSS Trap Grids (polygon, referenced service) | GWSS trap grid coverage polygons displayed as map context | Name, Folder Path | County GIS (maintained separately) | Provides geographic context for field inspectors; not editable via this app |

† Field and domain details inferred from the vendor documentation and web map popup configuration. The PPS feature service and views service were offline during the JSON export; full schema (field types, lengths, domain values) and view SQL must be verified against the live service or database.

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Schema not captured in export.** The PPS feature service (FeatureServer) was not running at export time. Field types, lengths, and domain values are not documented. | Technical Reference schema and domain sections are partly inferred. | Query schema from the ArcGIS Server REST endpoint or pgAdmin when the service is running; update the Technical Reference. |
| 2 | **Views service offline; view SQL not in vendor docs.** The PlantPestandSurveys_Views map service failed to export, and the KCI umbrella Technical Documentation appendix contains GWSS views (a template copy), not the PPO views. | The two PPO views' SQL definitions are undocumented. | Retrieve view SQL from pgAdmin (see Technical Reference §8). |
| 3 | **Edit-widget deletes cannot be undone.** Deleting a point, related record, or attachment in the web app Edit widget is immediate, with no confirmation. | Risk of accidental data loss. | Confirm the correct record before deleting. |
| 4 | **Address Points drift from SC_Prime.** The address dataset is a copy sourced from SC_Prime and will not stay aligned with the authoritative source. | Address data may be stale; field-added points may hold placeholder values. | Reconcile field-added address points against SC_Prime in the office. |
| 5 | **No dashboard.** The solution has no PPO-specific ArcGIS Dashboard component. | No at-a-glance summary of inspection counts or status. | Use the web app attribute table and Query widget. |
