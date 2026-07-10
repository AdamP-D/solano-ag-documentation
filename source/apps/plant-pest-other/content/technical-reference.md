# Plant, Pest & Other Inspections — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

The Plant, Pest & Other Inspections (PPO) solution is part of the broader **"Ag Inspection Tool"** built by KCI. That tool originally bundled Incoming Shipment Tracking, PQ, and PPO, then split into separate portal groups for access control; PPO lives in the **"Incoming Shipments and PPO Inspections"** group (id `325f3033…`), shared with IST. The PPO solution is built on a **referenced feature service** (data in the enterprise PostgreSQL geodatabase) plus a companion **views map service**, with two front-end components:

**Front-end components:**

- **Plant Pest Other Insp - Field Map** (Web Map, item `97652afc…`) — configured for the **Esri Field Maps** mobile application. Inspectors select an Address Point or Inspection Point, open its related Plant Pest and Other Inspections table, and add/edit the inspection record and attachments. Item snippet: *"…backed by the AgDept SDE."*
- **Plant Pest Other Insp Web App** (Web AppBuilder application, item `24f20646…`) — used by office and field staff to create/edit points and related records, manage attachments, run predefined queries, and review data from a desktop browser.

There is no Survey123 form and no PPO-specific ArcGIS Dashboard. (A solution-level "Plant Pest and Surveys – Management Dashboard" exists for the umbrella solution but is not part of the PPO export.)

**Data architecture — related-records model:**

PPO uses a **related-records design** (the same pattern as IST), not a standalone inspection layer. Two parent **point feature classes** each relate one-to-many to a single child **inspection table**:

- **Address Points** — the parent point for sites that have an address. Sourced from the County **SC_Prime** database (NG911/NENA standard fields: `site_nguid`, `apn`, `fulladdress`, street components, lat/long). Searchable by Full Address or APN.
- **Inspection Points (PPO)** — the parent point for inspections where **no address is available**. Carries `insp_type`, `insp_status`, `insp_date`, `inspector`, `address`, `comments`; `insp_type` defaults to "Plant Pest & Other Inspection." Offered as three symbology templates (users generally choose "Active").
- **Plant Pest and Other Inspections** — the child **related table** that stores the actual inspection record and its photo/file attachments. Each record relates to exactly one parent point; the intent is a single record per inspection, edited until complete. The relationship is **1:M** from either parent to this table.

These are published in the feature service `PlantPestandSurveys/PPS_Plant_Pest_Other_Insp/FeatureServer`. A companion **views map service** (`PlantPestandSurveys/PlantPestandSurveys_Views/MapServer`) publishes two dynamic, non-editable views that combine each parent point with its related record for display and symbology (see §8).

> **Schema gap:** Both the PPS feature service and the views map service were **not running** when the JSON export was taken, so layer schemas, `insp_type` / `insp_status` domain values, relationship definitions, and view SQL could not be captured automatically. The architecture above is taken from the KCI vendor documentation (authoritative); field-level details must be verified against the live services or pgAdmin.

**Reference layers on the map:**

- **GWSS Trap Grids** (polygon feature layer) — shows GWSS monitoring trap grid boundaries as geographic context for field inspectors. Not editable via this solution.
- **Human Geography Base / Detail** (vector tile basemaps) — standard county basemap.
- **Aerial2022_WGS84** (map service) — 2022 aerial imagery.

## 2. Portal Items

<!-- GENERATED:portal-items -->
| Title | Type | Source | Item ID |
|---|---|---|---|
| Plant Pest Other Insp - Field Map | Web Map | requested | 97652afc76f2480eaa9fabc05764feed |
| Plant Pest Other Insp Web App | Web Mapping Application | requested | 24f20646bd814e2c97848927c473260f |
| Human Geography Base | Vector Tile Service | referenced | 2afe5b807fa74006be6363fd243ffb30 |
| GWSS Trap Grids | Feature Service | referenced | 6504dcbc61ac4778b42630b691557294 |
| Aerial2022_WGS84 | Map Service | referenced | 76e948d75558400daee67e9ebfe3f246 |
| PPS Plant Pest Other Insp | Feature Service | referenced | 7cc79e513d53498b8bda9af4d75d03c5 |
| Human Geography Detail | Vector Tile Service | referenced | 97fa1365da1e43eabb90d0364326bc2d |
| PlantPestandSurveys_Views | Map Service | referenced | b82f8fe744144507a92446ef52f68f4b |
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

All data for this solution exists in the enterprise PostgreSQL database and is exposed through ArcGIS Server as referenced services — pointing back to PostgreSQL rather than storing a hosted copy.

**PPS Plant Pest Other Insp** (FeatureServer, item `7cc79e513d53498b8bda9af4d75d03c5`) — the primary editable feature service containing the **Inspection Points (PPO)** and **Address Points** feature classes and the **Plant Pest and Other Inspections** related table. ArcGIS Server path: `PlantPestandSurveys/PPS_Plant_Pest_Other_Insp/FeatureServer`. Service was offline at export time; capabilities, time zone, and archiving status not confirmed from the export.

**PlantPestandSurveys_Views** (MapServer, item `b82f8fe744144507a92446ef52f68f4b`) — read-only Map Service exposing the two combining database views. ArcGIS Server path: `PlantPestandSurveys/PlantPestandSurveys_Views/MapServer`. Snippet: *"Plant Pest and Surveys – Database views production feature service."* Service was offline at export time; view SQL is not available from the export (see §8).

**Spatial reference:** NAD 1983 2011 StatePlane California II FIPS 0402 (Feet) — WKID 6418 / legacy WKID 103004.

**ArcGIS Pro project:** The KCI umbrella Technical Documentation lists the publishing Pro project as `C:\Users\kci-5\Documents\ArcGIS\Projects\GWSS` — but that path is on a KCI developer machine and is labeled for GWSS, so treat it as **unverified for PPO**. Confirm the current .aprx location with the GIS team.

> **Note — shared umbrella solution:** The KCI *"Plant, Pest, and Surveys"* Technical Documentation covers IST, PQ, and PPO together. It lists the enterprise datasets as Inspection Points, Address Points, Field Boundaries, three inspection tables (Incoming Shipment Tracking, Plant Pest and Other Inspections, PQ Inspection Tracking), and County Boundary, plus eight database views. Its Data Services section and appendix, however, describe GWSS services and `v_gwss_*` views (copied from the GWSS document template) and do **not** reflect this solution's actual services or views.

<!-- GENERATED:services -->
| Service / Item | Type | Item ID |
|---|---|---|
| Human Geography Base | Vector Tile Service | 2afe5b807fa74006be6363fd243ffb30 |
| GWSS Trap Grids | Feature Service | 6504dcbc61ac4778b42630b691557294 |
| Aerial2022_WGS84 | Map Service | 76e948d75558400daee67e9ebfe3f246 |
| PPS Plant Pest Other Insp | Feature Service | 7cc79e513d53498b8bda9af4d75d03c5 |
| Human Geography Detail | Vector Tile Service | 97fa1365da1e43eabb90d0364326bc2d |
| PlantPestandSurveys_Views | Map Service | b82f8fe744144507a92446ef52f68f4b |
<!-- /GENERATED:services -->

## 4. Database Schema

> **Note:** The PPS Plant Pest Other Insp feature service was offline when the JSON export was taken. The auto-generated schema below reflects only the layer that successfully exported (GWSS Trap Grids, a reference layer). The solution's own datasets — **Inspection Points (PPO)**, **Address Points**, and the **Plant Pest and Other Inspections** related table — are documented manually in Section 11 from the vendor documentation and web map popup config; field types, lengths, and domains require verification against the live service.

<!-- GENERATED:schema -->
#### GWSS Trap Grids (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| name | Name | String | 320 | True | True |  |
| folderpath | FolderPath | String | 320 | True | True |  |
| symbolid | SymbolID | Integer |  | True | True |  |
| altmode | AltMode | SmallInteger |  | True | True |  |
| base | Base | Double |  | True | True |  |
| clamped | Clamped | SmallInteger |  | True | True |  |
| extruded | Extruded | SmallInteger |  | True | True |  |
| snippet | Snippet | String | 1073741822 | True | True |  |
| popupinfo | PopupInfo | String | 1073741822 | True | True |  |
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
_No domains._
<!-- /GENERATED:domains -->

> **Note:** Domain values were not captured because the feature service was offline at export time. From the vendor documentation, `insp_type` defaults to **"Plant Pest & Other Inspection,"** and the umbrella solution covers survey types **SOD, SLF, BW, AWB, ESFY** plus a **Resident Complaint / CDFA / County Follow Up** ("other") type — these are the likely `insp_type` coded values but must be confirmed. `insp_status` values are unconfirmed. Query the live service REST endpoint or pgAdmin to retrieve the exact domain definitions, then update this section.

## 6. Subtypes

<!-- GENERATED:subtypes -->
_No subtypes._
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
_No relationships._
<!-- /GENERATED:relationships -->

> **Note:** The generator reports no relationships because the feature service was offline at export time. Per the KCI vendor documentation, the solution **does** use registered one-to-many relationships: both **Inspection Points (PPO)** and **Address Points** relate 1:M to the **Plant Pest and Other Inspections** table. Confirm the relationship class names and keys against the live service.

## 8. Database View Definitions

The **PlantPestandSurveys_Views** Map Service (`b82f8fe744144507a92446ef52f68f4b`) exposes two PostgreSQL database views that combine a parent point feature with its related Plant Pest and Other Inspections record, symbolized to surface the status and type values. The views are non-editable and update dynamically as the point feature or related records change:

- **PPS IP PlantPestOther Inspections (View)** — combines **Inspection Points (PPO)** with their related inspection records.
- **PPS PlantPestOther Inspections (View)** — combines **Address Points** with their related inspection records.

**View SQL is not available** from this export (the map service was offline), and it is **not** in the KCI umbrella Technical Documentation appendix — that appendix contains the GWSS `v_gwss_*` views (a template copy), not these PPO views. To retrieve the real definitions, connect to the PostgreSQL database in pgAdmin and run:

```sql
SELECT viewname, definition
FROM pg_views
WHERE definition ILIKE '%plantpestother%'
   OR viewname ILIKE '%plant%pest%'
ORDER BY viewname;
```

Once retrieved, document each view here in the format used by the PQ and IST technical references.

Once obtained, document each view here in the format used by the GWSS and IST technical references.

## 9. Attribute Rules

No attribute rules have been confirmed for this solution. Inspection status (`insp_status`) appears to be set manually by the inspector in Field Maps. Verify in ArcGIS Pro by opening the feature class properties > Attribute Rules tab when connected to the enterprise geodatabase.

## 10. Geoprocessing / Automation

None confirmed. There are no geoprocessing services or scheduled scripts known to be associated with this solution. All record creation and updates are performed by users through Field Maps or the web app.

## 11. Map / App Layer Definitions

### Feature Service Structure — parents and related table

Per the KCI vendor documentation, the feature service publishes two parent point feature classes and one child related table (exact REST layer IDs need verification against the live `PPS_Plant_Pest_Other_Insp/FeatureServer` endpoint, which was offline at export):

| Component | Type | Role |
|-----------|------|------|
| Inspection Points (PPO) | Feature Layer (Point) | Parent for address-less sites; carries `insp_type`, `insp_status`, `insp_date`, `inspector`, `address`, `comments`; 1:M to the inspection table |
| Address Points | Feature Layer (Point) | Parent for sites with an address; NG911/NENA fields sourced from SC_Prime; 1:M to the inspection table |
| Plant Pest and Other Inspections | Table (related) | Child inspection records + attachments; one record per inspection |

The map's full layer list (from the user guide) is: GWSS Trap Grids, Inspection Points (PPO), Address Points, **PPS IP PlantPestOther Inspections (View)** (off by default), **PPS PlantPestOther Inspections (View)** (off by default), County Boundary, and the Plant Pest and Other Inspections data table.

### Inspection Points (PPO) — Fields from Popup Configuration

The following fields are confirmed from the web map popup configuration; the point carries these for identification and symbology, with the full inspection record held in the related table. Field types, lengths, and domain definitions require verification against the live service.

| Field Name | Popup Label | Notes |
|-----------|-------------|-------|
| `insp_type` | Inspection Type | Coded value; defaults to "Plant Pest & Other Inspection." Umbrella doc lists survey types SOD, SLF, BW, AWB, ESFY and the Resident Complaint/CDFA/County Follow Up ("other") type — confirm exact domain against live service |
| `insp_status` | Inspection Status | Coded value; preset from the Edit widget template chosen for the point; values unconfirmed from export |
| `insp_date` | Inspection Date | Date field |
| `inspector` | Inspector | String; inspector name |
| `address` | Address | String; site address (also how Inspection Points are searched) |
| `comments` | Comments | String; notes from the inspection |
| `globalid` | globalid | GUID; Global ID |
| `created_user` / `created_date` / `last_edited_user` / `last_edited_date` | — | Edit tracking (system-managed) |

### Address Points — NG911 Parent Layer (from SC_Prime)

Address Points is the County's master address/site point dataset (NG911/NENA standard), sourced from the **SC_Prime** database. Unlike a passive reference layer, it is an editable parent in this solution — users can add address points (with placeholder values for required fields, reconciled later against SC_Prime) and attach inspection records to them. Searchable by Full Address or APN. Key fields include `site_nguid` (Site NENA GUID), `apn` (Assessor Parcel Number), `fulladdress`, lat/long, and the full complement of NENA street-component and jurisdictional fields.

### Web Application Widgets

Search (place / address / APN / Inspection Point), Select (point or rectangle), **Edit** (create/edit Inspection Points, Address Points, and related inspection records; manage attachments; auto-saves; deletes are immediate and not undoable), **Query** (predefined tasks against Inspection Points, Address Points, and both views), Legend, Layer List, Basemap Gallery, and Bookmarks.

### GWSS Trap Grids (Referenced Layer)

The GWSS Trap Grids polygon layer (item `6504dcbc61ac4778b42630b691557294`, FeatureServer) is displayed on the field map as geographic context showing where GWSS monitoring trap grids are established. It is not editable via this solution. The layer was originally created from a KML import and retains KML-artifact fields (`folderpath`, `symbolid`, `altmode`, `base`, `clamped`, `extruded`, `snippet`, `popupinfo`). The meaningful display field is `name` (trap grid name). Archiving is not enabled on this layer.

### Field Maps Configuration

The web map (`97652afc76f2480eaa9fabc05764feed`) carries the typeKeyword `CollectorDisabled`, which is an Esri internal flag indicating the map was configured for Field Maps (formerly Collector) but has Collector compatibility explicitly disabled. The map is used exclusively through the Esri Field Maps app, not through the legacy ArcGIS Collector app.
