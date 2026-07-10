# Incoming Shipment Tracking — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

The Incoming Shipment Tracking (IST) solution provides field data collection and office workflow management for tracking incoming agricultural shipments that require inspection by Solano County's Agriculture Department. The solution was developed by KCI Technologies in late 2022 through mid-2023 and reworked in early 2024.

**Front-end components:**
- **Incoming Shipment Tracking** (Web AppBuilder desktop/web application) — primary office tool for creating, editing, viewing, and exporting shipment records.
- **Incoming Shipment Tracking – Field Map** (Esri Field Maps) — mobile map for field inspectors to create and update shipment records in the field.
- **Incoming Shipment Tracking – Web Map** — supporting web map for the desktop application context.
- **Incoming Shipment Tracking** (Web Dashboard) — management and dispatch dashboard summarizing daily workloads, pending actions, and completed inspections.
- **Incoming Shipment Tracking (Mobile)** (Mobile Dashboard) — mobile-optimized dashboard with Inspector View dispatch list; includes a hyperlink that launches Field Maps and searches by ParcelID.

**Data architecture:** IST records are stored in the **Incoming Shipment Tracking** table (attachments enabled) in the enterprise PostgreSQL "agdept" database. Records are related to the **Parcels REGIS** feature class — a copy of the County's sc_prime cadastral data stored in the agdept SDE. All data services are referenced (not hosted); the PostgreSQL database is the authoritative source.

**Automation:** Five calculation attribute rules on the Incoming Shipment Tracking table auto-populate ParcelID, parcel address, common name, IST ID, and status. Two database views — `v_ist_all_records` and `v_ist_inspector_view` — support the map layers and dashboards without requiring a geoprocessing service.

## 2. Portal Items

<!-- GENERATED:portal-items -->
| Title | Type | Source | Item ID |
|---|---|---|---|
| Incoming Shipment Tracking - Web Map | Web Map | requested | 817f7aaa0bcf4c29affd00736b841004 |
| Incoming Shipment Tracking - Field Map | Web Map | requested | 3e1ca65e69634a86b4726e2f77b68f28 |
| Incoming Shipment Tracking | Web Mapping Application | requested | 09544f5e328b4480aba349baa9eecc3a |
| Solano County - Boundary | Feature Service | referenced | 44671cce1cbe42d38b520dfec0a664c9 |
| GWSS Trap Grids | Map Service | referenced | 656ccc0b9a7f47bcb4eccca9a727229e |
| Incoming Shipment Tracking Views | Map Service | referenced | 7ca5db3200184506b4545be5541656b4 |
| World Topographic Map | Vector Tile Service | referenced | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| Incoming Shipment Tracking | Feature Service | referenced | d55ab83e55554f3ea53d993351048c32 |
| Incoming Shipment Tracking Field Map | Feature Service | referenced | 61edad06db74486fa5131b399bae9f78 |
| Incoming Shipment Tracking | Dashboard | referenced | e42711f164ad456995aa765347416a9e |
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

All data services for this solution are **referenced** from the enterprise PostgreSQL "agdept" database — no data is hosted in the ArcGIS portal. Three feature/map services support the solution:

- **Incoming Shipment Tracking** (FeatureServer) — used in the Web Map and Web AppBuilder app for data collection and review; also configured for use in the web and mobile dashboards.
- **Incoming Shipment Tracking Field Map** (FeatureServer) — configured specifically for use in Esri Field Maps; this is the only service with **archiving enabled** to support an offline sync workflow.
- **Incoming Shipment Tracking Views** (MapServer) — map service containing the view layers (Inspector View, Status layers, Tracking By Period layers, All Records).

**Time-zone configuration:** All feature services are published with the time zone set to **Pacific Time adjusted for daylight saving**. This setting ensures accurate date display and facilitates the "today"-based logic in the Inspector View query layer and dashboards.

**Archiving and offline:** Archiving is enabled only on the Field Map service. The Incoming Shipment Tracking Views service, County Boundary, and GWSS Trap Grids do not support offline. A complete offline workflow would require a new web map or reconfiguration of those services.

**ArcGIS Pro project:** All services are published from the Pro project at `E:\ServiceUpdates\AgInspectionTool\PlantsPestSurvey_Prod`.

The generated table below reflects the portal items captured in the JSON export for this solution.

<!-- GENERATED:services -->
| Service / Item | Type | Item ID |
|---|---|---|
| Solano County - Boundary | Feature Service | 44671cce1cbe42d38b520dfec0a664c9 |
| GWSS Trap Grids | Map Service | 656ccc0b9a7f47bcb4eccca9a727229e |
| Incoming Shipment Tracking Views | Map Service | 7ca5db3200184506b4545be5541656b4 |
| World Topographic Map | Vector Tile Service | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| Incoming Shipment Tracking | Feature Service | d55ab83e55554f3ea53d993351048c32 |
| Incoming Shipment Tracking Field Map | Feature Service | 61edad06db74486fa5131b399bae9f78 |
<!-- /GENERATED:services -->

## 4. Database Schema

<!-- GENERATED:schema -->
#### County_Boundary (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| objectid_1 | objectid_1 | OID |  | False | False |  |
| name | NAME | String | 13 | True | True |  |
| shape__are | Shape__Are | Double |  | True | True |  |
| shape__len | Shape__Len | Double |  | True | True |  |

#### GWSS Trap Grids (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| name | Name | String | 320 |  |  |  |
| folderpath | FolderPath | String | 320 |  |  |  |
| symbolid | SymbolID | Integer |  |  |  |  |
| altmode | AltMode | SmallInteger |  |  |  |  |
| base | Base | Double |  |  |  |  |
| clamped | Clamped | SmallInteger |  |  |  |  |
| extruded | Extruded | SmallInteger |  |  |  |  |
| snippet | Snippet | String | 1073741822 |  |  |  |
| popupinfo | PopupInfo | String | 1073741822 |  |  |  |
| st_area(shape) | st_area(shape) | Double |  |  |  |  |
| st_length(shape) | st_length(shape) | Double |  |  |  |  |

#### Inspector View (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | ParcelID | String | 30 |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parceladdress | Parcel Address | String | 60000 |  |  |  |
| countrelatedrecords | Count - Related Records | String | 60000 |  |  |  |
| countactionrequiredrecords | Count - Action Required Records | String | 60000 |  |  |  |
| countincomingshipmentrecords | Count - Incoming Shipment Records | String | 60000 |  |  |  |
| countcompletedtodayrecords | Count - Completed Today Records | String | 60000 |  |  |  |
| actionstatus | Action Status | String | 60000 |  |  |  |
| details_wheading | Details - wHeading | String | 60000 |  |  |  |
| details | Details | String | 60000 |  |  |  |
| arriveddate_insptype | Arrived Date - Insp Type | String | 60000 |  |  |  |
| notifiedofshipmentdate_insptype | Notified of Shipment Date - Insp Type | String | 60000 |  |  |  |
| completeddate_insptype | Completed Date - Insp Type | String | 60000 |  |  |  |
| priority | Priority | Integer |  |  |  |  |

#### Tracking By Period (Group Layer)

*Group layer — contains the layers below.*

##### Todays Records (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Released by Phone - Past 7 Days (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - This Month (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - Previous Month (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - Current Fiscal Year (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - Previous Fiscal Year (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - Current Calendar Year (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Completed - Previous Calendar Year (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

#### Status (Group Layer)

*Group layer — contains the layers below.*

##### Incoming Shipments (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Requires Inspection (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Reinspection Needed - On Hold (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

##### Complete (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

#### All Records (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| ist_objectid | ist_objectid | OID |  |  |  |  |
| parcel_common_name | Common Name | String | 255 |  |  |  |
| parcelid | ParcelID | String | 255 |  |  |  |
| ist_id | IST ID | String | 255 |  |  |  |
| address | Address | String | 255 |  |  |  |
| shipper | Shipper | String | 255 |  |  |  |
| notice_number | 008 Notice Number | String | 255 |  |  |  |
| invoice_number | Invoice Number | String | 255 |  |  |  |
| insp_type | Inspection Type | String | 255 |  |  |  |
| inspctr_initials | Inspector Initials | String | 255 |  |  |  |
| notified_of_shipment | Notified of Shipment | Date | 8 |  |  |  |
| arrived | Arrived | Date | 8 |  |  |  |
| partial_release | Partial Release | Date | 8 |  |  |  |
| on_hold | On Hold | Date | 8 |  |  |  |
| completed | Completed | Date | 8 |  |  |  |
| result | Result | String | 255 |  |  |  |
| status | Status | String | 255 |  |  |  |
| comments | Comments | String | 255 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |

#### Parcels REGIS (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcel_common_name | Common Name | String | 255 | True | True |  |
| parcelid | Parcel ID | String | 30 | True | True |  |
| parceladdress | Parcel Address | String | 37 | True | True |  |
| sitecity | Site City | String | 14 | True | True |  |

#### Incoming Shipment Tracking (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| status | Status | String | 255 | True | True | IST_Status |
| parcel_common_name | Common Name | String | 255 | True | True |  |
| ist_id | IST ID | String | 255 | True | True |  |
| parcelid | Parcel ID | String | 255 | True | True |  |
| address | Address | String | 255 | True | True |  |
| invoice_number | Invoice Number | String | 255 | True | True |  |
| insp_type | Inspection Type | String | 255 | True | True | IST_Insp_Type |
| shipper | Shipper | String | 255 | True | True |  |
| inspctr_initials | Inspector Initials | String | 255 | True | True |  |
| notice_number | 008 Notice Number | String | 255 | True | True |  |
| notified_of_shipment | Notified of Shipment | Date | 8 | True | True |  |
| arrived | Arrived | Date | 8 | True | True |  |
| partial_release | Partial Release | Date | 8 | True | True |  |
| on_hold | On Hold | Date | 8 | True | True |  |
| completed | Completed | Date | 8 | True | True |  |
| result | Result | String | 255 | True | True | IST_Result |
| comments | Comments | String | 255 | True | True |  |
| rel_globalid | REL_GLOBALID | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### Parcels REGIS (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcel_common_name | Common Name | String | 255 | True | True |  |
| parceladdress | parceladdress | String | 37 | True | True |  |
| sitecity | sitecity | String | 14 | True | True |  |
| parcelid | PARCELID | String | 30 | True | True |  |

#### Incoming Shipment Tracking (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| status | Status | String | 255 | True | True | IST_Status |
| parcel_common_name | Common Name | String | 255 | True | True |  |
| ist_id | IST ID | String | 255 | True | True |  |
| parcelid | ParcelID | String | 255 | True | True |  |
| address | Address | String | 255 | True | True |  |
| invoice_number | Invoice Number | String | 255 | True | True |  |
| shipper | Shipper | String | 255 | True | True |  |
| insp_type | Inspection Type | String | 255 | True | True | IST_Insp_Type |
| inspctr_initials | Inspector Initials | String | 255 | True | True |  |
| notice_number | 008 Notice Number | String | 255 | True | True |  |
| notified_of_shipment | Notified of Shipment | Date | 8 | True | True |  |
| arrived | Arrived | Date | 8 | True | True |  |
| partial_release | Partial Release | Date | 8 | True | True |  |
| on_hold | On Hold | Date | 8 | True | True |  |
| completed | Completed | Date | 8 | True | True |  |
| result | Result | String | 255 | True | True | IST_Result |
| comments | Comments | String | 255 | True | True |  |
| rel_globalid | REL_GLOBALID | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
**IST_Insp_Type**

| Coded Value | Alias |
|---|---|
| GWSS | GWSS |
| Other | Other |
| Seed 008 | Seed 008 |
| SM/SLF | Spongy Moth/Spotted Lanternfly |
| Southern State 008 | Southern State 008 |
| Spongy Moth | Spongy Moth |
| Spotted Lanternfly | Spotted Lanternfly |
| Spotted Lanternfly, 008 | Spotted Lanternfly, 008 |
| Truck – Plant | Truck – Plant |

**IST_Result**

| Coded Value | Alias |
|---|---|
| Forwarded to Other Agency | Forwarded to Other Agency |
| Inspected and Released | Inspected and Released |
| Reconditioned and Released | Reconditioned and Released |
| Rejected / Returned / Destroyed | Rejected / Returned / Destroyed |
| Released by Phone | Released by Phone |

**IST_Status**

| Coded Value | Alias |
|---|---|
| Incoming Shipment | Incoming Shipment |
| Requires Inspection | Requires Inspection |
| Complete | Complete |
| Complete - Forwarded to Other Agency | Complete - Forwarded to Other Agency |
| Complete - Inspected and Released | Complete - Inspected and Released |
| Complete - Reconditioned and Released | Complete - Reconditioned and Released |
| Complete - Rejected / Returned / Destroyed | Complete - Rejected / Returned / Destroyed |
| Complete - Released by Phone | Complete - Released by Phone |
| Reinspection Needed - On Hold | Reinspection Needed - On Hold |
<!-- /GENERATED:domains -->

## 6. Subtypes

<!-- GENERATED:subtypes -->
_No subtypes._
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
| Layer/Table | Relationship | Cardinality |
|---|---|---|
| Parcels REGIS | Incoming Shipment Tracking | esriRelCardinalityOneToMany |
| Incoming Shipment Tracking | Parcels REGIS | esriRelCardinalityOneToMany |
<!-- /GENERATED:relationships -->

## 8. Database View Definitions

Two database views in the agdept SDE support the IST solution. Both were developed in pgAdmin and then used as the definition for view layers published via ArcGIS Pro. The production SQL definitions are provided below.

### v_ist_all_records

**Purpose:** Joins the Incoming Shipment Tracking table to the Parcels REGIS feature class to produce a flat, geometry-bearing record set of all IST records. Used for the All Records map layer and attribute table export.

```sql
SELECT i.objectid as ist_objectid,
i.parcel_common_name,
i.parcelid,
i.ist_id,
i.address,
i.invoice_number,
i.insp_type,
i.inspctr_initials,
i.notified_of_shipment,
i.arrived,
i.partial_release,
i.on_hold,
i.completed,
i.result,
i.status,
i.comments,
i.created_user,
i.created_date,
i.last_edited_user,
i.last_edited_date,
pr.shape
FROM Parcels_REGIS_20240202_evw pr
JOIN Incoming_Shipment_Tracking_evw i ON pr.globalid = i.rel_globalid;
```

### v_ist_inspector_view

**Purpose:** Aggregates IST records per parcel, determines an action status for each parcel (Action Needed, Incoming Shipment, or Completed Today), and computes record counts by category. Drives the Inspector View dispatch list in both the web and mobile dashboards. One row per parcel is returned (no duplicate geometry per parcel), ordered by priority.

**Daylight saving time note:** This view contains a hard-coded UTC offset of **"minus 7 hours"** in three places (the `TodaysRecordsUnique`, `CompletedTodayUnique`, and `DatesInsptypes_Completed` subqueries) to determine "today" in Pacific Daylight Time. When DST ends, all three occurrences must be manually changed to **"minus 8 hours"** to reflect Pacific Standard Time; they must be reverted to "minus 7 hours" when DST begins again. The `timezone()` SQL function could not be used in the view definition due to ArcGIS Pro query-layer limitations.

```sql
select cast(row_number() OVER (ORDER BY ist_inspector.objectid) AS int) as objectid,
    ist_inspector.parcelid,
    ist_inspector.parcel_common_name,
    ist_inspector.parceladdress,
    ist_inspector.countrelatedrecords::text,
    ist_inspector.countactionrequiredrecords::text,
    ist_inspector.countincomingshipmentrecords::text,
    ist_inspector.countcompletedtodayrecords::text,
    ist_inspector.actionstatus,
    ist_inspector.details_wheading,
    ist_inspector.details,
    ist_inspector.arriveddate_insptype,
    ist_inspector.notifiedofshipmentdate_insptype,
    ist_inspector.completeddate_insptype,
    ist_inspector.priority,
    ist_inspector.shape
from
(SELECT 
pr.objectid,
pr.parcelid,
 pr.parcel_common_name,
(pr.parceladdress || ', ') || pr.sitecity AS parceladdress,
 TodaysRecordsUnique.CountOfTodaysRecords as CountRelatedRecords,
 coalesce(ActionNeededUnique.CountOfActionRequiredRecords, 0) as CountActionRequiredRecords,
 coalesce(IncomingShipmentUnique.CountOfIncomingShipmentRecords, 0) as CountIncomingShipmentRecords,
 coalesce(CompletedTodayUnique.CountOfCompletedTodayRecords, 0) as CountCompletedTodayRecords,
CASE
WHEN (ActionNeededUnique.rel_globalid IS NOT NULL) THEN 'Action Needed – Inspection(s) - Reinspection(s)'
WHEN (IncomingShipmentUnique.rel_globalid IS NOT NULL) THEN 'Incoming Shipments'
WHEN (CompletedTodayUnique.rel_globalid IS NOT NULL) THEN 'Completed Today'
END AS actionstatus,
CASE
WHEN (ActionNeededUnique.rel_globalid IS NOT NULL) THEN concat('Arrived Date - Inspection Type: ', DatesInsptypes_ActionNeeded.arriveddate_insptype)
WHEN (IncomingShipmentUnique.rel_globalid IS NOT NULL) THEN concat('Notified of Shipment Date - Inspection Type: ', DatesInsptypes_IncomingShipment.notifiedofshipmentdate_insptype)
WHEN (CompletedTodayUnique.rel_globalid IS NOT NULL) THEN concat('Completed Date - Inspection Type: ', DatesInsptypes_Completed.completeddate_insptype)
END AS details_wheading,
CASE
WHEN (ActionNeededUnique.rel_globalid IS NOT NULL) THEN DatesInsptypes_ActionNeeded.arriveddate_insptype
WHEN (IncomingShipmentUnique.rel_globalid IS NOT NULL) THEN DatesInsptypes_IncomingShipment.notifiedofshipmentdate_insptype
WHEN (CompletedTodayUnique.rel_globalid IS NOT NULL) THEN DatesInsptypes_Completed.completeddate_insptype
END AS details,
 DatesInsptypes_ActionNeeded.arriveddate_insptype,
 DatesInsptypes_IncomingShipment.notifiedofshipmentdate_insptype,
 DatesInsptypes_Completed.completeddate_insptype, 
CASE
WHEN (ActionNeededUnique.rel_globalid IS NOT NULL) THEN 1
WHEN (IncomingShipmentUnique.rel_globalid IS NOT NULL) THEN 2
WHEN (CompletedTodayUnique.rel_globalid IS NOT NULL) THEN 3
END AS priority,
pr.shape
FROM parcels_regis_evw pr
left join
(select
todaysrecords.rel_globalid,
count(rel_globalid) as CountOfTodaysRecords
FROM
(SELECT 
incoming_shipment_tracking_evw.rel_globalid,
incoming_shipment_tracking_evw.globalid,
incoming_shipment_tracking_evw.status
FROM incoming_shipment_tracking_evw
WHERE (incoming_shipment_tracking_evw.status IN ('Requires Inspection', 'Reinspection Needed - On Hold') or incoming_shipment_tracking_evw.status IN ('Incoming Shipment') or incoming_shipment_tracking_evw.completed > cast(now() - interval '7 hours' as date))) as todaysrecords
GROUP BY todaysrecords.rel_globalid) as TodaysRecordsUnique
on pr.globalid = TodaysRecordsUnique.rel_globalid
left join
(select
actionneeded.rel_globalid,
count(rel_globalid) as CountOfActionRequiredRecords
FROM
(SELECT 
incoming_shipment_tracking_evw.rel_globalid,
incoming_shipment_tracking_evw.globalid,
incoming_shipment_tracking_evw.status
FROM incoming_shipment_tracking_evw
WHERE incoming_shipment_tracking_evw.status IN ('Requires Inspection', 'Reinspection Needed - On Hold')) as actionneeded
GROUP BY actionneeded.rel_globalid) as ActionNeededUnique
on pr.globalid = ActionNeededUnique.rel_globalid
left join
(select
incomingshipment.rel_globalid,
count(rel_globalid) as CountOfIncomingShipmentRecords
FROM
(SELECT 
incoming_shipment_tracking_evw.rel_globalid,
incoming_shipment_tracking_evw.globalid,
incoming_shipment_tracking_evw.status
FROM incoming_shipment_tracking_evw
WHERE incoming_shipment_tracking_evw.status IN ('Incoming Shipment')) as incomingshipment
GROUP BY incomingshipment.rel_globalid) as IncomingShipmentUnique
on pr.globalid = IncomingShipmentUnique.rel_globalid
left join
(select
completedtoday.rel_globalid,
count(rel_globalid) as CountOfCompletedTodayRecords
FROM
(SELECT 
incoming_shipment_tracking_evw.rel_globalid,
incoming_shipment_tracking_evw.globalid,
incoming_shipment_tracking_evw.status
FROM incoming_shipment_tracking_evw
WHERE incoming_shipment_tracking_evw.completed > cast(now() - interval '7 hours' as date)) as completedtoday
GROUP BY completedtoday.rel_globalid) as CompletedTodayUnique
on pr.globalid = CompletedTodayUnique.rel_globalid
left join
(SELECT 
 rel_globalid, 
string_agg(concat((cast((extract(month from arrived)) as text)), '.', (cast((extract(day from arrived)) as text)), '.', (cast((extract(year from arrived)) as text))), ', ' order by arrived desc) AS arriveddate,
string_agg(concat((cast((extract(month from arrived)) as text)), '.', (cast((extract(day from arrived)) as text)), '.', (cast((extract(year from arrived)) as text)), ' - ', coalesce(insp_type, '[No Insp Type Entered]')), '  |  ' order by arrived desc) AS arriveddate_insptype,
string_agg(coalesce(insp_type, '[No Insp Type Entered]'), ', ' order by arrived desc) AS insp_type
FROM   incoming_shipment_tracking_evw
where (incoming_shipment_tracking_evw.status IN ('Requires Inspection', 'Reinspection Needed - On Hold'))
GROUP  BY rel_globalid) DatesInsptypes_ActionNeeded
 on pr.globalid = DatesInsptypes_ActionNeeded.rel_globalid
left join
(SELECT 
 rel_globalid, 
string_agg(concat((cast((extract(month from notified_of_shipment)) as text)), '.', (cast((extract(day from notified_of_shipment)) as text)), '.', (cast((extract(year from notified_of_shipment)) as text))), ', ' order by notified_of_shipment desc) AS notifiedofshipmentdate,
string_agg(concat((cast((extract(month from notified_of_shipment)) as text)), '.', (cast((extract(day from notified_of_shipment)) as text)), '.', (cast((extract(year from notified_of_shipment)) as text)), ' - ', coalesce(insp_type, '[No Insp Type Entered]')), '  |  ' order by notified_of_shipment desc) AS notifiedofshipmentdate_insptype,
string_agg(coalesce(insp_type, '[No Insp Type Entered]'), ', ' order by notified_of_shipment desc) AS insp_type
FROM   incoming_shipment_tracking_evw
where (incoming_shipment_tracking_evw.status IN ('Incoming Shipment'))
GROUP  BY rel_globalid) DatesInsptypes_IncomingShipment
 on pr.globalid = DatesInsptypes_IncomingShipment.rel_globalid
left join
(SELECT 
 rel_globalid, 
string_agg(concat((cast((extract(month from completed)) as text)), '.', (cast((extract(day from completed)) as text)), '.', (cast((extract(year from completed)) as text))), ', ' order by completed desc) AS completeddate,
string_agg(concat((cast((extract(month from completed)) as text)), '.', (cast((extract(day from completed)) as text)), '.', (cast((extract(year from completed)) as text)), ' - ', coalesce(insp_type, '[No Insp Type Entered]')), '  |  ' order by completed desc) AS completeddate_insptype,
string_agg(coalesce(insp_type, '[No Insp Type Entered]'), ', ' order by completed desc) AS insp_type
FROM   incoming_shipment_tracking_evw
where (incoming_shipment_tracking_evw.completed > cast(now() - interval '7 hours' as date))
GROUP  BY rel_globalid) DatesInsptypes_Completed
 on pr.globalid = DatesInsptypes_Completed.rel_globalid
) 
as ist_inspector
where ist_inspector.actionstatus is not null
order by ist_inspector.priority
```

## 9. Attribute Rules

Five calculation attribute rules are applied to the Incoming Shipment Tracking table in the agdept SDE. All five are calculation rules (not constraint or validation rules). They auto-populate fields from the related parent parcel or from data within the IST record itself.

### ParcelID — Insert

**Field:** `parcelid`  
**Trigger:** Insert

```arcade
// calculation attribute rule on child
// field: if you want to get only one field from the parent, then chose 
// that field. if you want to get multiple fields, leave empty
// triggers: Insert(, update)

// load the related parent features using one of these methods
// if you have a relationship class between parent and child:

var parent_fs = FeatureSetByRelationshipName($feature, "agdept.gisadm.Parcels_REGIS_Has_Incoming_Shipment_Tracking")

// return nothing if no parent feature was found
var parent = First(parent_fs)
if(parent == null) { return }

// if you want to return only one field:
return text(parent.parcelid);
```

### Parcel_Address — Insert

**Field:** `address`  
**Trigger:** Insert

```arcade
// calculation attribute rule on child
// field: if you want to get only one field from the parent, then chose 
// that field. if you want to get multiple fields, leave empty
// triggers: Insert(, update)

// load the related parent features using one of these methods
// if you have a relationship class between parent and child:

var parent_fs = FeatureSetByRelationshipName($feature, "agdept.gisadm.Parcels_REGIS_Has_Incoming_Shipment_Tracking")

// return nothing if no parent feature was found
var parent = First(parent_fs)
if(parent == null) { return }

// if you want to return only one field:
return parent.parceladdress + ", " + parent.sitecity;
```

### Parcel Common Name — Insert / Update

**Field:** `parcel_common_name`  
**Trigger:** Insert, Update

```arcade
// calculation attribute rule on child
// field: if you want to get only one field from the parent, then chose 
// that field. if you want to get multiple fields, leave empty
// triggers: Insert(, update)

// load the related parent features using one of these methods
// if you have a relationship class between parent and child:

var parent_fs = FeatureSetByRelationshipName($feature, "agdept.gisadm.Parcels_REGIS_Has_Incoming_Shipment_Tracking")

// return nothing if no parent feature was found
var parent = First(parent_fs)
if(parent == null) { return }

// if you want to return only one field:
return text(parent.parcel_common_name);
```

### IST ID — Insert / Update

**Field:** `ist_id`  
**Trigger:** Insert, Update

```arcade
text("48" + "_" + text($feature.notified_of_shipment, 'MMDDYY') + "_" +$feature.inspctr_initials + "_" +$feature.parcelid + "_" + $feature.objectid)
```

### Status — Insert / Update

**Field:** `status`  
**Trigger:** Insert, Update

This rule calculates the shipment status from the dates and result fields. The lifecycle is: Incoming Shipment → Requires Inspection → Reinspection Needed - On Hold → Complete (with result-specific variants). If no conditions are met, the rule returns null.

```arcade
var today = Now();
var status = null; // Initialize status to null

// If the 'completed' field is not empty, determine the appropriate "Complete" status
if (!IsEmpty($feature.completed)) {
    status = "Complete"; // Default to "Complete" if no further conditions are met

    // Update the status variable based on the result value
    if ($feature.result == "Forwarded to Other Agency") {
        status = "Complete - Forwarded to Other Agency";
    } else if ($feature.result == "Inspected and Released") {
        status = "Complete - Inspected and Released";
    } else if ($feature.result == "Reconditioned and Released") {
        status = "Complete - Reconditioned and Released";
    } else if ($feature.result == "Rejected / Returned / Destroyed") {
        status = "Complete - Rejected / Returned / Destroyed";
    } else if ($feature.result == "Released by Phone") {
        status = "Complete - Released by Phone";
    }
    return status; // Return the determined status
}

// Check for incoming shipments with a future arrival date or if the 'notified_of_shipment' field is not empty
if (!IsEmpty($feature.notified_of_shipment) && IsEmpty($feature.arrived)) {
    return "Incoming Shipment";
}

// If the 'arrived' date is in the future, even if 'notified_of_shipment' is empty
//if (!IsEmpty($feature.arrived) && $feature.arrived > today) {
  //  return "Incoming Shipment";
//}

// If the 'arrived' date is today or in the past and other conditions indicating processing or action required are empty
if (!IsEmpty($feature.arrived) && IsEmpty($feature.partial_release) && IsEmpty($feature.on_hold) && IsEmpty($feature.completed)) {
    return "Requires Inspection";
}

// If any of the conditions indicating reinspection or on hold are met
if (!IsEmpty($feature.partial_release) || !IsEmpty($feature.on_hold)) {
    return "Reinspection Needed - On Hold";
}

// If none of the conditions are met, this implies an uncovered scenario; thus, return null
return null;
```

## 10. Geoprocessing / Automation

None. Record status is maintained by the Status attribute rule (Section 9) and the database views (Section 8), not by a geoprocessing service.

## 11. Map / App Layer Definitions

The IST solution uses a layered structure in both the Web Map and Field Map that combines dynamic definition-query layers with status-based symbology.

### Status Group Layer

Contains individual sub-layers for each shipment status, each displaying IST records using their related parcel geometry. Stacked geometry is expected on parcels with multiple records.

| Layer | Definition |
|-------|------------|
| Incoming Shipments | Status = "Incoming Shipment" |
| Requires Inspection | Status = "Requires Inspection" |
| Reinspection Needed – On Hold | Status = "Reinspection Needed - On Hold" |
| Complete | Status contains "Complete" |

**Dashboard color coding** (IST Records list widget): yellow background (`#A8A800`) = Incoming Shipment; orange background (`#38A800`) = Requires Inspection or Reinspection Needed - On Hold; blue background (`#004DA8`) = any Complete status. (Note: the hex `#38A800` renders as green; the "orange" label follows the original dashboard code comment rather than the actual color.)

### Inspector View Layer

A single-geometry-per-parcel view layer (`v_ist_inspector_view`) that aggregates records by parcel and assigns an action status priority:
1. **Action Needed – Inspection(s) - Reinspection(s):** parcel has at least one record in Requires Inspection or Reinspection Needed - On Hold status.
2. **Incoming Shipments:** parcel has at least one Incoming Shipment record (and no action-needed records).
3. **Completed Today:** parcel has records completed today (and no pending records).

Only parcels with a non-null action status appear in this view. The layer is used as the dispatch list in both the web and mobile dashboards.

### All Records Layer

Displays all IST records with parcel geometry. Stacked geometry is expected.

### Tracking By Period Group Layer

Contains six pre-configured definition-query layers. IST records are shown with their related parcel geometry; stacked geometry is expected.

| Layer | Definition |
|-------|------------|
| Today's Records | Status in (Incoming Shipment, Requires Inspection, Reinspection Needed – On Hold) OR (status contains Complete AND completed date = today) |
| Completed – This Month | Status contains Complete AND completed date within the current calendar month |
| Completed – Current Fiscal Year | Status contains Complete AND completed date within the current fiscal year |
| Completed – Previous Fiscal Year | Status contains Complete AND completed date within the previous fiscal year |
| Completed – Current Calendar Year | Status contains Complete AND completed date within the current calendar year |
| Completed – Previous Calendar Year | Status contains Complete AND completed date within the previous calendar year |

Definition query SQL for the Tracking By Period layers is saved in the ArcGIS Pro project folder at `E:\ServiceUpdates\AgInspectionTool\IST View Definition Queries`.
