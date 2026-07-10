# Incoming Shipment Tracking — Requirements Document

*Solano County Agricultural Program · As-built documentation of current functionality*

---

## 1. Background & Purpose

Solano County's Agriculture Department is responsible for inspecting incoming shipments of plants and agricultural goods to prevent the introduction of pests and diseases into the county. Managing this work means keeping track of many shipments at once — which are expected, which have arrived and need inspection, which are on hold, and which are finished — and coordinating that work between office staff and field inspectors. Doing this without a shared system is difficult and error-prone.

The Incoming Shipment Tracking (IST) solution was built for Solano County by KCI, working with the County's DOIT–GIS team and the Agriculture Department. It was first developed in late 2022 through mid-2023 and reworked in early 2024 to provide a more cohesive experience for office and field users. Its purpose is to give the department a single, shared, map-based system that records each shipment against its parcel, automatically tracks the shipment's status, and gives managers and inspectors clear, up-to-date visibility into the day's workload through dashboards.

---

## 2. Stakeholders

| Name / Role | Relationship to System |
|-------------|------------------------|
| Solano County Agriculture Department | System Owner / Program Owner |
| David Jagdeo | Primary Point of Contact |
| Agriculture Department office staff / inspectors | Primary Users (record management and dispatch) |
| Agriculture Department field inspectors | Primary Users (field data collection) |
| Agriculture Department management | Dashboard users / oversight |
| Solano County DOIT–GIS | System owner (GIS platform); maintainer |
| KCI (Andrew Blowers, author of documentation) | Developer / Maintainer |

---

## 3. Current Functional Requirements (As-Built)

The following requirements describe what the system does today.

| # | Requirement |
|---|-------------|
| FR-01 | The system shall record each incoming shipment as a record related to a parcel. |
| FR-02 | The system shall provide a desktop web application for creating, editing, viewing, and exporting shipment records. |
| FR-03 | The system shall provide a mobile map (Esri Field Maps) for creating, editing, and viewing shipment records in the field. |
| FR-04 | The system shall provide web and mobile dashboards summarizing the current workload. |
| FR-05 | The system shall allow users to create a shipment record by selecting a parcel and adding a related record. |
| FR-06 | The system shall capture shipment details including inspection type, invoice number, 008 notice number, shipper, inspector initials, and comments. |
| FR-07 | The system shall capture the key dates: notified of shipment, arrived, partial release, on hold, and completed. |
| FR-08 | The system shall capture the inspection result from a defined list of outcomes. |
| FR-09 | The system shall automatically calculate each record's status from its dates and result. |
| FR-10 | The system shall automatically populate each record's IST ID, Parcel ID, parcel address, and common name from the related parcel. |
| FR-11 | The system shall allow users to add, view, and open photo and file attachments on shipment records. |
| FR-12 | The system shall allow users to create placeholder parcel features when a needed parcel does not exist. |
| FR-13 | The system shall disable editing of parcel geometry after creation to protect existing boundaries. |
| FR-14 | The system shall symbolize parcels by shipment status (incoming, requires inspection, reinspection/on hold, complete). |
| FR-15 | The system shall provide dynamic, pre-configured layers for status and for time periods (today, this month, current/previous fiscal year, current/previous calendar year). |
| FR-16 | The system shall provide an Inspector View that summarizes records per parcel by action status with record counts. |
| FR-17 | The system shall provide dashboard indicators for total today, incoming shipments, action required, and completed today. |
| FR-18 | The system shall allow dashboard users to select parcels and view their related shipment records. |
| FR-19 | The system shall provide a mobile dashboard link that launches Field Maps and searches for the selected parcel. |
| FR-20 | The system shall allow users to search by parcel ID, address, and invoice number. |
| FR-21 | The system shall allow users to view and export records to CSV from the attribute table. |
| FR-22 | The system shall hide the Result field until the Completed date is populated. |
| FR-23 | The system shall support an offline field workflow for the field-map shipment data. |
| FR-24 | The system shall track who created and last edited each record, and when. |

---

## 4. Current Data Requirements

| Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
|-----------------|---------|----------------------------|---------------|---------------|
| Incoming Shipment Tracking (table) | The shipment records | Status (calculated), Inspection Type, Invoice Number, 008 Notice Number, Shipper, Inspector Initials, Notified/Arrived/Partial Release/On Hold/Completed dates, Result, Comments, IST ID | Office & field staff | The core record of each shipment through its lifecycle |
| Parcels REGIS | The properties shipments relate to | Parcel ID, Parcel Address, Site City, Common Name | Office staff (placeholders) / GIS | Ties each shipment to a location and supplies its parcel info |
| All Records view (v_ist_all_records) | Combine records with parcel geometry | (derived) | System (automated) | Displays all records on the map |
| Inspector View (v_ist_inspector_view) | Summarize records per parcel by action status | (derived) | System (automated) | Powers the dashboard dispatch list and counts |

Shipment records support photo and file attachments, and track who created and last edited each record.

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Daylight saving time is hard-coded.** The Inspector View calculation uses a fixed "minus 7 hours" time offset rather than an automatic time-zone function. | When daylight saving time starts or ends, "today"-based counts and lists can be off until corrected. | The view's SQL definition must be manually updated (change the offset to minus 8 hours in three places) when DST ends, and reverted when it begins. Documented in the Technical Documentation. |
| 2 | **Offline support is incomplete.** Only the field-map shipment service supports offline use; the view layers, County Boundary, and GWSS Trap Grids do not. | Full offline field use is not currently possible. | A separate offline web map would need to be created, or those services reconfigured for offline. |
| 3 | **Parcels are a copy, not live.** The Parcels REGIS layer used here was copied from the County's authoritative cadastral data and will not stay in sync with it. | Parcel boundaries/attributes may drift from the authoritative source over time. | Placeholder parcels can be created as needed; periodic reconciliation with the authoritative source would be required to stay aligned. |
| 4 | **Stacked geometry on parcels.** Because each shipment is shown using its related parcel's shape, multiple records stack on the same parcel. | Map layers can show overlapping symbols on a single parcel. | The Inspector View avoids duplicates by showing one entry per parcel; the status/period layers intentionally show each record. |
| 5 | **Parcel geometry is locked after creation.** New placeholder parcels cannot be reshaped after they are drawn. | Correcting a mis-drawn placeholder parcel is not possible in the app. | Recreate the parcel if it was drawn incorrectly. |

---

*This document describes the system as built. It intentionally does not include future enhancements or prioritization.*
