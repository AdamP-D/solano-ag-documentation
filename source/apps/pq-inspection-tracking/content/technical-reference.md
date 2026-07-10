# PQ Inspection Tracking — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

The PQ Inspection Tracking solution is built around a **referenced feature service** (data lives in the enterprise PostgreSQL geodatabase) plus a companion **views map service**, with four front-end components:

**Front-end components:**

- **PQ Inspection Tracking** (Survey123 form) — the data collection interface for field inspectors. New records are **always initiated from Field Maps** (or the Dashboard / Web App) via the "Launch Survey123" hyperlink on a Field Boundaries polygon; subsequent edits are made through the Survey123 **Inbox**, which consolidates each field's values into a single table record.
- **PQ Inspection Tracking** (Field Map / Web Map, item `73ef5034…`) — used in Esri Field Maps on mobile devices to locate a field boundary, launch a new Survey123 record, and view the status view layers.
- **PQ Inspection Tracking - Web App** (Web AppBuilder desktop application) — used by office staff to review/manage records, launch Survey123 from a field-boundary popup, and export the attribute table. Embedded in the Dashboard for convenience.
- **PQ Inspection Tracking - Dashboard** — provides a management-level status list, a complete Survey123 record view with attachments, and an embedded copy of the Web App.

**Data architecture:**

Two datasets are stored in the enterprise geodatabase (PostgreSQL) and published as a single referenced feature service (`PQ_Inspection_Tracking/PQ_Inspection_Tracking/FeatureServer`):

- **Field Boundaries** (polygon feature layer, **Layer 0**) — captures the geographic extent of each inspection site. A reference layer, but users can add new fields via the Edit widget or Field Maps. Has no user-attribute fields; contains only edit-tracking fields and geometry.
- **pq_inspection_tracking** (table, **Layer 1**, no geometry) — the inspection records table that Survey123 writes to. Stores all inspection attributes: PQ number, commodity, applicant, quarantine/inspection status, per-walk time and mileage data, and a stored Global ID (`fieldboundary_guid`) linking each record to its Field Boundaries polygon.

A separate **views map service** (`PQ_Inspection_Tracking/PQ_Inspection_Tracking_Views/MapServer`) publishes two dynamic database views — "Inspection/Quarantine Status" and "All Records" — that join the inspection table to the field-boundary geometry (see §8). This map service was not part of the JSON export but is central to how records are displayed and symbolized.

The inspection table is linked to Field Boundaries through the `fieldboundary_guid` field (stores the Field Boundaries `globalid`) and to Incoming Shipment Tracking through the `incoming_id` field (stores the related IST Global ID). Neither link is a registered ArcGIS relationship class — both are soft references, resolved by the database views rather than enforced by the service.

Archiving (change tracking) is enabled on both layers. The service supports offline sync for use in Esri Field Maps or Survey123 offline mode. Data is not hosted in the portal's managed data store; the enterprise PostgreSQL geodatabase is authoritative (the views reference `pq_inspection_tracking_evw` / `fieldboundaries_evw`, confirming enterprise geodatabase versioned views).

## 2. Portal Items

<!-- GENERATED:portal-items -->
| Title | Type | Source | Item ID |
|---|---|---|---|
| PQ Inspection Tracking | Web Map | requested | 73ef5034cdb84bd696b4adc883fafd3a |
| PQ Inspection Tracking - Web App | Web Mapping Application | requested | 00ba255a6c3e48ee9e59c060aa55f8d7 |
| PQ Inspection Tracking - Dashboard | Dashboard | requested | 27edc16d7c314a5581b93e9bc6a32d3b |
| PQ Inspection Tracking | Form | requested | 2cec2a099a764b928fe343334569d4f4 |
| PQ Inspection Tracking | Feature Service | referenced | 015b5008eac34e49bea220d63edb2bd8 |
| Human Geography Base | Vector Tile Service | referenced | 2afe5b807fa74006be6363fd243ffb30 |
| Solano County - Boundary | Feature Service | referenced | 44671cce1cbe42d38b520dfec0a664c9 |
| Aerial2022_WGS84 | Map Service | referenced | 76e948d75558400daee67e9ebfe3f246 |
| Human Geography Detail | Vector Tile Service | referenced | 97fa1365da1e43eabb90d0364326bc2d |
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

All data for this solution exists in the enterprise PostgreSQL "agdept" (or equivalent) database and is exposed through ArcGIS Server as a **referenced feature service** — pointing back to PostgreSQL rather than storing a hosted copy. There are no hosted feature layers in this solution.

**PQ Inspection Tracking** (FeatureServer, item `015b5008eac34e49bea220d63edb2bd8`) — single service containing both the Field Boundaries polygon layer (Layer 0) and the pq_inspection_tracking table (Layer 1). Capabilities: Query, Create, Update, Delete, Uploads, Editing, Sync, Extract, ChangeTracking.

**Time-zone configuration:** The service is published with time zone set to **Pacific Standard Time** with daylight saving respected. Date fields in the feature service are stored in UTC and displayed in Pacific time.

**Archiving:** Both layers have archiving enabled (enabled May 17, 2024). This provides a full edit history and supports the `ChangeTracking` capability used by Survey123 offline sync.

**Views map service:** `PQ_Inspection_Tracking/PQ_Inspection_Tracking_Views/MapServer` publishes the two database views as the "Inspection/Quarantine Status" and "All Records" layers. It was not captured in the JSON export (only the FeatureServer's dependencies were followed) but is a required part of the deployed solution.

**Additional reference layers** used by the maps but outside the core service: **Road Centerlines** and **County Boundary** (hosted in the County's ArcGIS Online organization `SCn6czzcqKAFwdGU`).

**Survey123 linked-content CSVs** (portal items supporting the form's choice lists and auto-population): `applicant_address.csv` (Applicant → Address, and Contact Name & Phone), `grower_pesticide_perm_num.csv` (Grower → Pesticide Permit Number), and `commodity_walk_days.csv` (Commodity → estimated 1st/2nd walk days). Launching the form via a map/dashboard hyperlink does **not** refresh these lists — the form must be opened directly in Survey123 for updated CSVs to download.

**Spatial reference:** NAD 1983 StatePlane California II FIPS 0402 (Feet) — WKID 103004.

**ArcGIS Pro project:** `\\gis.solanocountygis.local\E\ServiceUpdates\PQ Inspection Tracking\PQ Inspection Tracking\PQ Inspection Tracking.aprx` (per KCI Technical Documentation v1.2).

<!-- GENERATED:services -->
| Service / Item | Type | Item ID |
|---|---|---|
| PQ Inspection Tracking | Feature Service | 015b5008eac34e49bea220d63edb2bd8 |
| Human Geography Base | Vector Tile Service | 2afe5b807fa74006be6363fd243ffb30 |
| Solano County - Boundary | Feature Service | 44671cce1cbe42d38b520dfec0a664c9 |
| Aerial2022_WGS84 | Map Service | 76e948d75558400daee67e9ebfe3f246 |
| Human Geography Detail | Vector Tile Service | 97fa1365da1e43eabb90d0364326bc2d |
<!-- /GENERATED:services -->

## 4. Database Schema

<!-- GENERATED:schema -->
#### Field Boundaries (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### pq_inspection_tracking (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| form_start | form_start | Date | 8 | True | True |  |
| form_end | form_end | Date | 8 | True | True |  |
| fo_s123_username | fo_s123_username | String | 255 | True | True |  |
| form_version | Form Version | String | 255 | True | True |  |
| incoming_id | Incoming GID | String | 255 | True | True |  |
| fieldboundary_guid | Field Boundary Global ID | GUID | 38 | True | True |  |
| pq_number | PQ Number | String | 255 | True | True |  |
| additional_pest | Additional Pest | String | 255 | True | True |  |
| additional_pest_notes | Additional Pest Notes | String | 2000 | True | True |  |
| quarantine_status | Quarantine Status | String | 255 | True | True | pq_quarantine_status |
| inspection_status | Inspection Status | String | 255 | True | True | pq_inspection_status |
| commodity | commodity | String | 255 | True | True |  |
| commodity_other_notes | Commodity Notes | String | 255 | True | True |  |
| acreage | Acreage | Double |  | True | True |  |
| applicant | Applicant | String | 255 | True | True |  |
| address | Address | String | 255 | True | True |  |
| plss_section | PLSS Section | String | 255 | True | True |  |
| plss_township | PLSS Township | String | 255 | True | True |  |
| plss_range | PLSS Range | String | 255 | True | True |  |
| contactname | Contact Name | String | 255 | True | True |  |
| phonenumber | Phone Number | String | 255 | True | True |  |
| variety | Variety | String | 255 | True | True |  |
| approx_plant_date | Approx. Plant Date | Date | 8 | True | True |  |
| approx_harvest_date | Approx. Harvest Date | Date | 8 | True | True |  |
| fw_est_days | Estimated Days Until 1st Walk | SmallInteger |  | True | True |  |
| fw_est_date | Estimated 1st Walk Date | Date | 8 | True | True |  |
| sw_est_days | Estimated Days Until 2nd Walk | SmallInteger |  | True | True |  |
| sw_est_date | Estimated 2nd Walk Date | Date | 8 | True | True |  |
| grower | Grower | String | 255 | True | True |  |
| pesticide_permit_number | Pesticide Permit Number | String | 255 | True | True |  |
| site_id | Site ID | String | 255 | True | True |  |
| first_walk_date | 1st Walk Date | Date | 8 | True | True |  |
| fw_lead_inspector | FW - Lead Inspector | String | 150 | True | True |  |
| fw_total_number_inspectors | FW - Total # of Inspectors | Integer |  | True | True |  |
| fw_insp_start_time | FW - Insp. Start Time | Date | 8 | True | True |  |
| fw_insp_start_time_m | FW - Insp. Start Time (24) | String | 255 | True | True |  |
| fw_insp_end_time | FW - Insp. End Time | Date | 8 | True | True |  |
| fw_insp_end_time_m | FW - Insp. End Time (24) | String | 255 | True | True |  |
| fw_insp_time | FW - Inspection Time | Double |  | True | True |  |
| fw_drive_time | FW - Drive Time (Decimal) | Double |  | True | True |  |
| fw_additional_time | FW - Additional Time (Decimal) | Double |  | True | True |  |
| fw_total_billable_time | FW - Total Billable Time | Double |  | True | True |  |
| fw_total_number_of_vehicles | FW - Total Number of Vehicles | Integer |  | True | True |  |
| fw_miles_per_vehicle | FW - Miles Per Vehicle | Double |  | True | True |  |
| fw_total_billable_miles | FW - Total Billable Miles | Double |  | True | True |  |
| fw_pdr_number | FW - PDR Number | String | 255 | True | True |  |
| first_walk_notes | FW - Notes | String | 255 | True | True |  |
| second_walk_date | 2nd Walk Date | Date | 8 | True | True |  |
| sw_lead_inspector | SW - Lead Inspector | String | 150 | True | True |  |
| sw_total_number_inspectors | SW - Total # of Inspectors | Integer |  | True | True |  |
| sw_insp_start_time | SW - Insp. Start Time | Date | 8 | True | True |  |
| sw_insp_start_time_m | SW - Insp. Start Time (24) | String | 255 | True | True |  |
| sw_insp_end_time | SW - Insp. End Time | Date | 8 | True | True |  |
| sw_insp_end_time_m | SW - Insp. End Time (24) | String | 255 | True | True |  |
| sw_insp_time | SW - Inspection Time | Double |  | True | True |  |
| sw_drive_time | SW - Drive Time (Decimal) | Double |  | True | True |  |
| sw_additional_time | SW - Additional Time (Decimal) | Double |  | True | True |  |
| sw_total_billable_time | SW - Total Billable Time | Double |  | True | True |  |
| sw_total_number_of_vehicles | SW - Total Number of Vehicles | Integer |  | True | True |  |
| sw_miles_per_vehicle | SW - Miles Per Vehicle | Double |  | True | True |  |
| sw_total_billable_miles | SW - Total Billable Miles | Double |  | True | True |  |
| sw_pdr_number | SW - PDR Number | String | 255 | True | True |  |
| second_walk_notes | SW - Notes | String | 255 | True | True |  |
| third_walk_date | 3rd Walk Date | Date | 8 | True | True |  |
| tw_lead_inspector | TW - Lead Inspector | String | 150 | True | True |  |
| tw_total_number_inspectors | TW - Total # of Inspectors | Integer |  | True | True |  |
| tw_insp_start_time | TW - Insp. Start Time | Date | 8 | True | True |  |
| tw_insp_start_time_m | TW - Insp. Start Time (24) | String | 255 | True | True |  |
| tw_insp_end_time | TW - Insp. End Time | Date | 8 | True | True |  |
| tw_insp_end_time_m | TW - Insp. End Time (24) | String | 255 | True | True |  |
| tw_insp_time | TW - Inspection Time | Double |  | True | True |  |
| tw_drive_time | TW - Drive Time (Decimal) | Double |  | True | True |  |
| tw_additional_time | TW - Additional Time (Decimal) | Double |  | True | True |  |
| tw_total_billable_time | TW - Total Billable Time | Double |  | True | True |  |
| tw_total_number_of_vehicles | TW - Total Number of Vehicles | Integer |  | True | True |  |
| tw_miles_per_vehicle | TW - Miles Per Vehicle | Double |  | True | True |  |
| tw_total_billable_miles | TW - Total Billable Miles | Double |  | True | True |  |
| tw_pdr_number | TW - PDR Number | String | 255 | True | True |  |
| third_walk_notes | TW - Notes | String | 255 | True | True |  |
| created_date | created_date | Date | 8 | True | False |  |
| created_user | created_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |

#### County_Boundary (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| objectid_1 | objectid_1 | OID |  | False | False |  |
| name | NAME | String | 13 | True | True |  |
| shape__are | Shape__Are | Double |  | True | True |  |
| shape__len | Shape__Len | Double |  | True | True |  |
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
**pq_inspection_status**

| Coded Value | Alias |
|---|---|
| Standby | Standby |
| Priority | Priority |
| 1st Walk Complete | 1st Walk Complete |
| 2nd Walk Complete | 2nd Walk Complete |
| 3rd Walk Complete | 3rd Walk Complete |
| Complete | Complete |

**pq_quarantine_status**

| Coded Value | Alias |
|---|---|
| None | None |
| Hold | Hold |
| Quarantine | Quarantine |
<!-- /GENERATED:domains -->

## 6. Subtypes

<!-- GENERATED:subtypes -->
_No subtypes._
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
_No relationships._
<!-- /GENERATED:relationships -->

## 8. Database View Definitions

This solution uses **two PostgreSQL database views**, published through the `PQ_Inspection_Tracking_Views` map service. Both join the inspection table (`pq_inspection_tracking_evw`) to the field-boundary feature class (`fieldboundaries_evw`) on `fieldboundary_guid = globalid`, so each inspection record can be displayed with its field-boundary geometry. The views update dynamically as individual PQ records change. SQL below is reproduced verbatim from the KCI Technical Documentation (v1.2) appendix.

### `v_pq_inspection_tracking_all` — "All Records" layer

Returns every PQ inspection field plus the related field-boundary geometry. Not filtered by date, so it includes all submissions (expect stacked geometry where multiple PQ records share one field boundary).

```sql
SELECT pq.objectid,
    pq.globalid,
    pq.form_start,
    pq.form_end,
    pq.fo_s123_username,
    pq.form_version,
    pq.fieldboundary_guid,
    pq.pq_number,
    pq.quarantine_status,
    pq.inspection_status,
    pq.acreage,
    pq.applicant,
    pq.address,
    pq.contactname,
    pq.phonenumber,
    pq.variety,
    pq.approx_plant_date,
    pq.approx_harvest_date,
    pq.grower,
    pq.pesticide_permit_number,
    pq.site_id,
    pq.first_walk_date,
    pq.fw_lead_inspector,
    pq.fw_total_number_inspectors,
    pq.fw_insp_start_time_m,
    pq.fw_insp_end_time_m,
    pq.fw_insp_time,
    pq.fw_drive_time,
    pq.fw_additional_time,
    pq.fw_total_billable_time,
    pq.fw_total_number_of_vehicles,
    pq.fw_miles_per_vehicle,
    pq.fw_total_billable_miles,
    pq.fw_pdr_number,
    pq.first_walk_notes,
    pq.second_walk_date,
    pq.sw_lead_inspector,
    pq.sw_total_number_inspectors,
    pq.sw_insp_start_time_m,
    pq.sw_insp_end_time_m,
    pq.sw_insp_time,
    pq.sw_drive_time,
    pq.sw_additional_time,
    pq.sw_total_billable_time,
    pq.sw_total_number_of_vehicles,
    pq.sw_miles_per_vehicle,
    pq.sw_total_billable_miles,
    pq.sw_pdr_number,
    pq.second_walk_notes,
    pq.third_walk_date,
    pq.tw_lead_inspector,
    pq.tw_total_number_inspectors,
    pq.tw_insp_start_time_m,
    pq.tw_insp_end_time_m,
    pq.tw_insp_time,
    pq.tw_drive_time,
    pq.tw_additional_time,
    pq.tw_total_billable_time,
    pq.tw_total_number_of_vehicles,
    pq.tw_miles_per_vehicle,
    pq.tw_total_billable_miles,
    pq.tw_pdr_number,
    pq.third_walk_notes,
    pq.created_date,
    pq.created_user,
    pq.last_edited_date,
    pq.last_edited_user,
    pq.incoming_id,
    pq.commodity,
    pq.commodity_other_notes,
    pq.additional_pest,
    pq.additional_pest_notes,
    pq.fw_est_date,
    pq.sw_est_date,
    pq.fw_est_days,
    pq.sw_est_days,
    pq.fw_insp_start_time,
    pq.fw_insp_end_time,
    pq.sw_insp_start_time,
    pq.sw_insp_end_time,
    pq.tw_insp_start_time,
    pq.tw_insp_end_time,
    fb.objectid AS fb_objectid,
    fb.globalid AS fb_globalid,
    fb.shape
   FROM pq_inspection_tracking_evw pq
     JOIN fieldboundaries_evw fb ON pq.fieldboundary_guid::text = fb.globalid::text;
```

### `v_pq_inspection_tracking_status` — "Inspection/Quarantine Status" layer

Consolidates the two status fields (`inspection_status` and `quarantine_status`) into a single `status` field via a CASE expression, so a field boundary can be symbolized by one combined status. As deployed, the published layer is further filtered to exclude `Complete` records and records whose walk/created date falls outside the current calendar year.

```sql
SELECT pq.objectid,
    pq.pq_number,
    pq.commodity,
    pq.applicant,
    pq.grower,
    pq.inspection_status,
    pq.quarantine_status,
    pq.first_walk_date,
    pq.second_walk_date,
    pq.third_walk_date,
    pq.created_user,
    pq.created_date,
    pq.last_edited_user,
    pq.last_edited_date,
    pq.incoming_id,
    pq.fieldboundary_guid,
    fb.shape,
        CASE
            WHEN pq.inspection_status::text = 'Standby'::text AND pq.quarantine_status::text = 'None'::text THEN 'Standby'::text
            WHEN pq.inspection_status::text = 'Priority'::text AND pq.quarantine_status::text = 'None'::text THEN 'Priority'::text
            WHEN pq.inspection_status::text = '1st Walk Complete'::text AND pq.quarantine_status::text = 'None'::text THEN '1st Walk Complete'::text
            WHEN pq.inspection_status::text = '2nd Walk Complete'::text AND pq.quarantine_status::text = 'None'::text THEN '2nd Walk Complete'::text
            WHEN pq.inspection_status::text = '3rd Walk Complete'::text AND pq.quarantine_status::text = 'None'::text THEN '3rd Walk Complete'::text
            WHEN pq.inspection_status::text = 'Standby'::text AND pq.quarantine_status::text = 'Hold'::text THEN 'Hold'::text
            WHEN pq.inspection_status::text = 'Priority'::text AND pq.quarantine_status::text = 'Hold'::text THEN 'Hold'::text
            WHEN pq.inspection_status::text = '1st Walk Complete'::text AND pq.quarantine_status::text = 'Hold'::text THEN 'Hold'::text
            WHEN pq.inspection_status::text = '2nd Walk Complete'::text AND pq.quarantine_status::text = 'Hold'::text THEN 'Hold'::text
            WHEN pq.inspection_status::text = '3rd Walk Complete'::text AND pq.quarantine_status::text = 'Hold'::text THEN 'Hold'::text
            WHEN pq.inspection_status::text = 'Standby'::text AND pq.quarantine_status::text = 'Quarantine'::text THEN 'Quarantine'::text
            WHEN pq.inspection_status::text = 'Priority'::text AND pq.quarantine_status::text = 'Quarantine'::text THEN 'Quarantine'::text
            WHEN pq.inspection_status::text = '1st Walk Complete'::text AND pq.quarantine_status::text = 'Quarantine'::text THEN 'Quarantine'::text
            WHEN pq.inspection_status::text = '2nd Walk Complete'::text AND pq.quarantine_status::text = 'Quarantine'::text THEN 'Quarantine'::text
            WHEN pq.inspection_status::text = '3rd Walk Complete'::text AND pq.quarantine_status::text = 'Quarantine'::text THEN 'Quarantine'::text
            WHEN pq.inspection_status::text = 'Complete'::text THEN 'Complete'::text
            ELSE NULL::text
        END AS status
   FROM pq_inspection_tracking_evw pq
     JOIN fieldboundaries_evw fb ON pq.fieldboundary_guid::text = fb.globalid::text;
```

## 9. Attribute Rules

No attribute rules are registered on either dataset in this service. Status fields (`quarantine_status`, `inspection_status`) are updated manually by the inspector through the Survey123 form or the web app. If auto-population or auto-status behavior is needed in the future, it would be implemented as a calculation attribute rule on the `pq_inspection_tracking` table in ArcGIS Pro.

## 10. Geoprocessing / Automation

None. There are no geoprocessing services, scheduled scripts, or external automation associated with this solution. All record creation and updates are performed by users through Survey123 or the web app.

## 11. Map / App Layer Definitions

### Feature Service Layer Structure

**Feature service** (`PQ_Inspection_Tracking/FeatureServer`):

| Layer ID | Name | Type | Key Note |
|----------|------|------|----------|
| 0 | Field Boundaries | Feature Layer (Polygon) | No user-editable attributes; geometry only |
| 1 | pq_inspection_tracking | Table (no geometry) | All inspection attributes; linked to Layer 0 via `fieldboundary_guid` |

**Views map service** (`PQ_Inspection_Tracking_Views/MapServer`), grouped in the maps as "PQ Inspection Tracking Views":

| Layer | Backing View | Key Note |
|-------|--------------|----------|
| Inspection/Quarantine Status | `v_pq_inspection_tracking_status` | Combined single-status symbology; filtered to exclude Complete and out-of-year records |
| All Records | `v_pq_inspection_tracking_all` | All PQ records shown on their related field-boundary geometry (stacked where a field has multiple records) |

Additional map layers: **Field Boundaries** (editable via Edit widget / Field Maps), **Road Centerlines**, **County Boundary**, and the **PQ Inspection Tracking (S123 Submissions)** table (unfiltered; backs the dashboard and views).

### Survey123 Form

The Survey123 form (`Form` item `2cec2a099a764b928fe343334569d4f4`) submits records to the `pq_inspection_tracking` table (Layer 1). New records are **initiated from Field Maps** (or the Dashboard / Web App): the inspector selects a Field Boundaries polygon and taps the **Launch Survey123** hyperlink in its popup. The popup HTML launches an `arcgis-survey123://` link that passes `field:incoming_id={GLOBALID}` into the form. Existing records are edited through the Survey123 **Inbox** (which excludes Complete records). The form stores version and submission metadata in `form_start`, `form_end`, `form_version`, and `fo_s123_username`, and uses three linked-content CSVs (`applicant_address`, `grower_pesticide_perm_num`, `commodity_walk_days`) to drive choice lists and auto-population.

### Soft Relationship Fields

Two fields on `pq_inspection_tracking` carry Global IDs from other datasets. These are soft references — they are populated by the user and not enforced by the database or service:

- **`fieldboundary_guid`** — stores the `globalid` of the Field Boundaries polygon that corresponds to this inspection record.
- **`incoming_id`** ("Incoming GID") — stores the `globalid` of a related Incoming Shipment Tracking (IST) record, when the PQ inspection was triggered by an incoming shipment.

### Time and Mileage Tracking

The pq_inspection_tracking table supports up to three walk-throughs, each with parallel time/mileage fields (prefix `fw_` for First Walk, `sw_` for Second Walk, `tw_` for Third Walk). Each set captures:

- Lead inspector and total number of inspectors
- Inspection start and end times (stored as Date; also captured as 24-hour string via `*_insp_start_time_m` / `*_insp_end_time_m` for display)
- Calculated inspection time, drive time, and additional time (Decimal hours)
- Total billable time (decimal hours) and total billable miles
- PDR number and notes for that walk

These values feed into cost-recovery billing and reporting outside the GIS system.

## 12. Enhancement History

From the KCI Technical Documentation change log (post-initial-deployment enhancements):

| Date | Change |
|------|--------|
| 5/3/2024 | Initial documentation (v1.0, Andrew Blowers). |
| 2/27/2025 | **Additional Pest Notes** field length increased 255 → 2,000 characters. **Applicant** selection now auto-populates **Contact Name & Phone** (via `applicant_address.csv`), in addition to Address. Added a **Lead Inspector** field (150 chars) to each of the three walks. Added an **Additional Time** field to each walk, rolled into the total-billable-time calculation. |
| 5/9/2025 | Added **Survey123 web-form compatibility**: the field-boundary popup now offers a second link to open the form in a browser (pinned to Survey123 `version=3.21` to avoid a 3.22 web-form bug). CSV headers were de-capitalized/de-spaced for web-form compatibility, and form questions were moved into `field-list` groups so the Pages layout works in the web form. |

> The IT/GIS point of contact for this solution is **Daniel Machado**. Original development by KCI (Andrew Blowers); 2025 enhancements by KCI (Darbie Gibbs).
