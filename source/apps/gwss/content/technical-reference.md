# GWSS Data Collection and Management Solution — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

The GWSS Data Collection and Management Solution consists of two front-end components backed by referenced PostgreSQL feature services and a geoprocessing service.

**Front-end components:**

- **Field Data Collection Map** — an Esri Field Maps web map used by field biologists on mobile devices. Provides map-based data entry for traps, findings, surveys, and treatments. URL: `https://solanocountygis.com/portal/home/webmap/viewer.html?webmap=8bc48a1f058a4d1fa980f28fe7d9adf1`
- **GWSS Tracking and Management Application** — a Web AppBuilder application used from the desktop for managing findings, running analysis, and reviewing status. URL: `https://solanocountygis.com/portal/apps/webappviewer/index.html?id=db56ca2b2cf0468c87ba34f4149a085d`. This app uses the Smart Editor widget for creating and editing Survey and Treatment records related to parcels, and the Geoprocessing widget to invoke the quarter-mile buffer tool.

**Supporting portal items:**

- A web map underlying the web application (owned by Matthew Carl; must be transferred back to him after any GIS-team edits).
- The `GWSSQuarterMileAnalysis_ParcelInspectionTag` geoprocessing service, accessible from the Geoprocessing widget in the web app.

**Data layer:**

All data is stored in the enterprise PostgreSQL database and served as **referenced services** (not hosted). As of April 2022, there are no hosted feature services in this solution. The four published services are:

- `GWSS_Data_Collection` (FeatureServer) — used in the Field Maps web map.
- `GWSS_Tracking_Management` (FeatureServer) — used in the web app map.
- `GWSS_Supporting_Analysis_Layers___Field_Map` (MapServer) — analysis layers for the field map.
- `GWSS_Supporting_Analysis_Layers` (MapServer) — analysis layers for the web app.

Additional referenced services provide the Quarantine Boundary, Trap Grids, and Biological Control layers. Eight PostgreSQL database views drive the holistic and most-recent-per-parcel symbology throughout the solution.

## 2. Portal Items

<!-- GENERATED:portal-items -->
| Title | Type | Source | Item ID |
|---|---|---|---|
| GWSS WebApp | Web Mapping Application | requested | db56ca2b2cf0468c87ba34f4149a085d |
| GWSS Web App Map | Web Map | requested | c3d24d3b49ef44e2b5b26f4b3d47ea0f |
| 8_10_2023_TreatmentBuffer | Feature Service | referenced | 0871806dde30400f95275ca0e0b6f842 |
| 10_2_23_TreatmentBuffer | Feature Service | referenced | 170533e9bfec4fc394a794866923d696 |
| GWSS Supporting Analysis Layers - Web App | Map Service | referenced | 22939663c19b4ffb8626fa68f48a596a |
| Priority_Soil_Treatments_2025 | Feature Service | referenced | 26ab5106a32c4c8e915e7bcea65b49af |
| 02022026_ParcelsWithin150m | Feature Service | referenced | 4115cfa2901a4d709bde8d94f5dfaca0 |
| 8_26_23_TreatmentBuffer | Feature Service | referenced | 41bf33e5c6f148efb670017d0dc537a6 |
| 150_Meter_Buffer_7_31_23 | Feature Service | referenced | 453e7d8cad5f440c82f65254e6bfa019 |
| 2_8_24_Treatment_Buffer | Feature Service | referenced | 4feeee2cdb4b478cb348d019b6782084 |
| Aerial2024_WGS84 | Map Service | referenced | 541130b8a82b4caf9991c87c1506a531 |
| 7_3_24_Treatment_Buffer | Feature Service | referenced | 57631a8c2dff47a2928d7b0523734b15 |
| Soil_Treatments_2025_corrected | Feature Service | referenced | 5dd1db719b5f4e509d504a96769d617c |
| GWSS Trap Grids | Feature Service | referenced | 6504dcbc61ac4778b42630b691557294 |
| Aerial2023_WGS84 | Map Service | referenced | 7614c0545d9144c6965ffa352d3040aa |
| Aerial2022_WGS84 | Map Service | referenced | 76e948d75558400daee67e9ebfe3f246 |
| World Topographic Map | Vector Tile Service | referenced | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| 02022026_GWSSFinding_150m_Buffer | Feature Service | referenced | 838546ad6d014bd9bf43e4af8d86873d |
| Address Points | Feature Service | referenced | a1be2d4601144f02ac056e1e288e461e |
| GWSS Tracking Management | Feature Service | referenced | c9229d7734a74168964e6fe0fb4a3976 |
| Aerial2021_WGS84 | Map Service | referenced | ca7e251636ca4d9d8b18a54978bd9575 |
| GWSS Biological Control | Feature Service | referenced | f0068cae52a14964b1d6ddd8084217b2 |
| GWSS Quar Boundary | Feature Service | referenced | f9ccb5c48d924b6e92041bec4558a3e6 |
| Buffer_of_Non_Viable_Eggmass_2 | Feature Service | referenced | fbb78a39710949bfabf0c6fc9a31559c |
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

All data for this solution exists in an enterprise PostgreSQL database and is exposed through ArcGIS Server as **referenced services** — that is, the services point back to the PostgreSQL database rather than storing their own copy of the data. There are no hosted feature services in this solution as of April 2022 (the Quarantine Boundary layer was the last hosted service; it was converted to a referenced service on 4/8/22).

The ArcGIS Pro project used to publish all services is located on the GIS server at:

```text
\\gis.solanocountygis.local\E\ServiceUpdates\GWSS
```

**Domain update procedure:** When a coded-value domain is modified in the database, the updated values do not automatically cascade to the running services on republish. To propagate domain changes, all GWSS services must be **stopped and restarted together**. Because each dataset participates in multiple services (directly or through views), restarting a single service is insufficient — all four services must be stopped and restarted. This behavior was confirmed with Esri during a support call and is documented in the Esri Bug Writeup on file.

**Relationship ID note:** Republishing a service can reorder internal relationship IDs. After the April 2022 republish, the relationship IDs in `GWSS_Tracking_Management` changed from `[0,1,2]` to `[0,2,1]`, breaking the Smart Editor widget's ability to add Survey and Treatment records from the desktop app. The fix was to edit the app's underlying JSON configuration to reference the corrected IDs. If editing from the desktop stops working after a republish, check the relationship IDs in the service REST endpoint and update the app JSON accordingly.

*Note: the generated Portal Items and Services tables below reflect the items captured in this export — the GWSS web-application web map and the services it references. The GWSS Data Collection feature service used by Esri Field Maps is part of the overall solution (see Section 1) but is not enumerated in these generated tables.*

<!-- GENERATED:services -->
| Service / Item | Type | Item ID |
|---|---|---|
| 8_10_2023_TreatmentBuffer | Feature Service | 0871806dde30400f95275ca0e0b6f842 |
| 10_2_23_TreatmentBuffer | Feature Service | 170533e9bfec4fc394a794866923d696 |
| GWSS Supporting Analysis Layers - Web App | Map Service | 22939663c19b4ffb8626fa68f48a596a |
| Priority_Soil_Treatments_2025 | Feature Service | 26ab5106a32c4c8e915e7bcea65b49af |
| 02022026_ParcelsWithin150m | Feature Service | 4115cfa2901a4d709bde8d94f5dfaca0 |
| 8_26_23_TreatmentBuffer | Feature Service | 41bf33e5c6f148efb670017d0dc537a6 |
| 150_Meter_Buffer_7_31_23 | Feature Service | 453e7d8cad5f440c82f65254e6bfa019 |
| 2_8_24_Treatment_Buffer | Feature Service | 4feeee2cdb4b478cb348d019b6782084 |
| Aerial2024_WGS84 | Map Service | 541130b8a82b4caf9991c87c1506a531 |
| 7_3_24_Treatment_Buffer | Feature Service | 57631a8c2dff47a2928d7b0523734b15 |
| Soil_Treatments_2025_corrected | Feature Service | 5dd1db719b5f4e509d504a96769d617c |
| GWSS Trap Grids | Feature Service | 6504dcbc61ac4778b42630b691557294 |
| Aerial2023_WGS84 | Map Service | 7614c0545d9144c6965ffa352d3040aa |
| Aerial2022_WGS84 | Map Service | 76e948d75558400daee67e9ebfe3f246 |
| World Topographic Map | Vector Tile Service | 7dc6cea0b1764a1f9af2e679f642f0f5 |
| 02022026_GWSSFinding_150m_Buffer | Feature Service | 838546ad6d014bd9bf43e4af8d86873d |
| Address Points | Feature Service | a1be2d4601144f02ac056e1e288e461e |
| GWSS Tracking Management | Feature Service | c9229d7734a74168964e6fe0fb4a3976 |
| Aerial2021_WGS84 | Map Service | ca7e251636ca4d9d8b18a54978bd9575 |
| GWSS Biological Control | Feature Service | f0068cae52a14964b1d6ddd8084217b2 |
| GWSS Quar Boundary | Feature Service | f9ccb5c48d924b6e92041bec4558a3e6 |
| Buffer_of_Non_Viable_Eggmass_2 | Feature Service | fbb78a39710949bfabf0c6fc9a31559c |
<!-- /GENERATED:services -->

## 4. Database Schema

<!-- GENERATED:schema -->
#### 8_10_2023_TreatmentBuffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### 10_2_23_TreatmentBuffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### GWSS - All Finding Records (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| date_collected | date_collected | Date | 8 |  |  |  |
| life_stage | life_stage | String | 50 |  |  |  |
| found_in_trap | found_in_trap | String | 3 |  |  |  |
| location | location | String | 255 |  |  |  |
| host_material | host_material | String | 255 |  |  |  |
| comments | comments | String | 255 |  |  |  |
| sent_to_lab | sent_to_lab | Date | 8 |  |  |  |
| pdr_number | pdr_number | String | 30 |  |  |  |
| lab_confirmed | lab_confirmed | String | 3 |  |  |  |
| quarter_mile_survey_required | quarter_mile_survey_required | String | 3 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS - All Treatment Records (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| infested_adjacent | infested_adjacent | String | 255 |  |  |  |
| infested_pdr | infested_pdr | String | 255 |  |  |  |
| knock_talk_date | knock_talk_date | Date | 8 |  |  |  |
| knock_talk_attempts | knock_talk_attempts | String | 255 |  |  |  |
| renter_leasee | renter_leasee | String | 3 |  |  |  |
| property_manager | property_manager | String | 255 |  |  |  |
| phone | phone | String | 50 |  |  |  |
| email | email | String | 100 |  |  |  |
| contact_made | contact_made | String | 10 |  |  |  |
| consent_to_spray | consent_to_spray | String | 30 |  |  |  |
| info_left | info_left | String | 3 |  |  |  |
| fy_approval | fy_approval | String | 3 |  |  |  |
| by_approval | by_approval | String | 3 |  |  |  |
| preferred_date | preferred_date | Date | 8 |  |  |  |
| preferred_time | preferred_time | String | 5 |  |  |  |
| planned_date | planned_date | Date | 8 |  |  |  |
| planned_time | planned_time | String | 5 |  |  |  |
| neighbors_for_notification | neighbors_for_notification | String | 500 |  |  |  |
| host_size | host_size | String | 255 |  |  |  |
| comments | comments | String | 500 |  |  |  |
| response_assigned_to | response_assigned_to | String | 100 |  |  |  |
| notified | notified | Date | 8 |  |  |  |
| neighbors_notified | neighbors_notified | Date | 8 |  |  |  |
| missed_treatment | missed_treatment | Date | 8 |  |  |  |
| treatment_inspector | treatment_inspector | String | 100 |  |  |  |
| treatment_date | treatment_date | Date | 8 |  |  |  |
| notice_color | notice_color | String | 50 |  |  |  |
| soil_treatment_date | soil_treatment_date | Date | 8 |  |  |  |
| soil_missed_treatment | soil_missed_treatment | Date | 8 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| treatment_status | treatment_status | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS - All Survey Records (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| biologists | biologists | String | 50 |  |  |  |
| survey_date | survey_date | Date | 8 |  |  |  |
| survey_refusal | survey_refusal | String | 3 |  |  |  |
| fy_inspected | fy_inspected | String | 3 |  |  |  |
| by_inspected | by_inspected | String | 3 |  |  |  |
| infested | infested | String | 3 |  |  |  |
| adjacent | adjacent | String | 3 |  |  |  |
| information_left | information_left | String | 3 |  |  |  |
| sample_collected | sample_collected | String | 3 |  |  |  |
| comments | comments | String | 255 |  |  |  |
| revisit_biologists | revisit_biologists | String | 50 |  |  |  |
| revisit_date | revisit_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| survey_result | survey_result | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS Parcel Survey (Last Six Weeks Only) (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| biologists | biologists | String | 50 |  |  |  |
| survey_date | survey_date | Date | 8 |  |  |  |
| survey_refusal | survey_refusal | String | 3 |  |  |  |
| fy_inspected | fy_inspected | String | 3 |  |  |  |
| by_inspected | by_inspected | String | 3 |  |  |  |
| infested | infested | String | 3 |  |  |  |
| adjacent | adjacent | String | 3 |  |  |  |
| information_left | information_left | String | 3 |  |  |  |
| sample_collected | sample_collected | String | 3 |  |  |  |
| comments | comments | String | 255 |  |  |  |
| revisit_biologists | revisit_biologists | String | 50 |  |  |  |
| revisit_date | revisit_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| survey_result | survey_result | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### Parcels Tagged from GWSS 1/4 mi. Buffer Analysis (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| quarter_mile_buffer_name | quarter_mile_buffer_name | String | 255 |  |  |  |
| gwss_finding_causing_survey | gwss_finding_causing_survey | String | 60000 |  |  |  |
| pdr_number | pdr_number | String | 30 |  |  |  |
| life_stage | life_stage | String | 50 |  |  |  |
| date_collected | date_collected | Date | 8 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| gwss_action | gwss_action | String | 50 |  |  |  |
| parcel_globalid | parcel_globalid | String | 38 |  |  |  |
| combined_buffer_parcel_globals | combined_buffer_parcel_globals | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS Treatments - Treatments In Past Year (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| infested_adjacent | infested_adjacent | String | 255 |  |  |  |
| infested_pdr | infested_pdr | String | 255 |  |  |  |
| knock_talk_date | knock_talk_date | Date | 8 |  |  |  |
| knock_talk_attempts | knock_talk_attempts | String | 255 |  |  |  |
| renter_leasee | renter_leasee | String | 3 |  |  |  |
| property_manager | property_manager | String | 255 |  |  |  |
| phone | phone | String | 50 |  |  |  |
| email | email | String | 100 |  |  |  |
| contact_made | contact_made | String | 10 |  |  |  |
| consent_to_spray | consent_to_spray | String | 30 |  |  |  |
| info_left | info_left | String | 3 |  |  |  |
| fy_approval | fy_approval | String | 3 |  |  |  |
| by_approval | by_approval | String | 3 |  |  |  |
| preferred_date | preferred_date | Date | 8 |  |  |  |
| preferred_time | preferred_time | String | 5 |  |  |  |
| planned_date | planned_date | Date | 8 |  |  |  |
| planned_time | planned_time | String | 5 |  |  |  |
| neighbors_for_notification | neighbors_for_notification | String | 500 |  |  |  |
| host_size | host_size | String | 255 |  |  |  |
| comments | comments | String | 500 |  |  |  |
| response_assigned_to | response_assigned_to | String | 100 |  |  |  |
| notified | notified | Date | 8 |  |  |  |
| neighbors_notified | neighbors_notified | Date | 8 |  |  |  |
| missed_treatment | missed_treatment | Date | 8 |  |  |  |
| treatment_inspector | treatment_inspector | String | 100 |  |  |  |
| treatment_date | treatment_date | Date | 8 |  |  |  |
| notice_color | notice_color | String | 50 |  |  |  |
| soil_treatment_date | soil_treatment_date | Date | 8 |  |  |  |
| soil_missed_treatment | soil_missed_treatment | Date | 8 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| treatment_status | treatment_status | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS Treatments - Most Recent Record per Parcel (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| infested_adjacent | infested_adjacent | String | 255 |  |  |  |
| infested_pdr | infested_pdr | String | 255 |  |  |  |
| knock_talk_date | knock_talk_date | Date | 8 |  |  |  |
| knock_talk_attempts | knock_talk_attempts | String | 255 |  |  |  |
| renter_leasee | renter_leasee | String | 3 |  |  |  |
| property_manager | property_manager | String | 255 |  |  |  |
| phone | phone | String | 50 |  |  |  |
| email | email | String | 100 |  |  |  |
| contact_made | contact_made | String | 10 |  |  |  |
| consent_to_spray | consent_to_spray | String | 30 |  |  |  |
| info_left | info_left | String | 3 |  |  |  |
| fy_approval | fy_approval | String | 3 |  |  |  |
| by_approval | by_approval | String | 3 |  |  |  |
| preferred_date | preferred_date | Date | 8 |  |  |  |
| preferred_time | preferred_time | String | 5 |  |  |  |
| planned_date | planned_date | Date | 8 |  |  |  |
| planned_time | planned_time | String | 5 |  |  |  |
| neighbors_for_notification | neighbors_for_notification | String | 500 |  |  |  |
| host_size | host_size | String | 255 |  |  |  |
| comments | comments | String | 500 |  |  |  |
| response_assigned_to | response_assigned_to | String | 100 |  |  |  |
| notified | notified | Date | 8 |  |  |  |
| neighbors_notified | neighbors_notified | Date | 8 |  |  |  |
| missed_treatment | missed_treatment | Date | 8 |  |  |  |
| treatment_inspector | treatment_inspector | String | 100 |  |  |  |
| treatment_date | treatment_date | Date | 8 |  |  |  |
| notice_color | notice_color | String | 50 |  |  |  |
| soil_treatment_date | soil_treatment_date | Date | 8 |  |  |  |
| soil_missed_treatment | soil_missed_treatment | Date | 8 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| treatment_status | treatment_status | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### GWSS Surveys - Most Recent Record per Parcel (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | parcelid | String | 30 |  |  |  |
| sitenum | sitenum | String | 6 |  |  |  |
| siteroad | siteroad | String | 30 |  |  |  |
| parceladdress | parceladdress | String | 37 |  |  |  |
| sitecity | sitecity | String | 14 |  |  |  |
| zip | zip | String | 10 |  |  |  |
| biologists | biologists | String | 50 |  |  |  |
| survey_date | survey_date | Date | 8 |  |  |  |
| survey_refusal | survey_refusal | String | 3 |  |  |  |
| fy_inspected | fy_inspected | String | 3 |  |  |  |
| by_inspected | by_inspected | String | 3 |  |  |  |
| infested | infested | String | 3 |  |  |  |
| adjacent | adjacent | String | 3 |  |  |  |
| information_left | information_left | String | 3 |  |  |  |
| sample_collected | sample_collected | String | 3 |  |  |  |
| comments | comments | String | 255 |  |  |  |
| revisit_biologists | revisit_biologists | String | 50 |  |  |  |
| revisit_date | revisit_date | Date | 8 |  |  |  |
| rel_globalid | rel_globalid | String | 38 |  |  |  |
| created_user | created_user | String | 255 |  |  |  |
| created_date | created_date | Date | 8 |  |  |  |
| last_edited_user | last_edited_user | String | 255 |  |  |  |
| last_edited_date | last_edited_date | Date | 8 |  |  |  |
| survey_result | survey_result | String | 60000 |  |  |  |
| ESRI_OID | ESRI_OID | OID |  |  |  |  |

#### Priority_Soil_Treatments_2025 (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| join_count | Join_Count | Integer |  | True | True |  |
| target_fid | TARGET_FID | Integer |  | True | True |  |
| site_nguid | Site NENA Globally Unique ID | String | 254 | True | True |  |
| apn | APN | String | 30 | True | True |  |
| fulladdress | Full Address | String | 255 | True | True |  |
| fulladdr_label_abbrv | Abbreviated Label | String | 255 | True | True |  |
| fulladdr_label | Full Address Label | String | 255 | True | True |  |
| gtg_flag | GTG_Flag | SmallInteger |  | True | True |  |
| gtg_notes | GTG_Notes | String | 255 | True | True |  |
| addnum_pre | Address Number Prefix | String | 15 | True | True |  |
| add_number | Address Number | Integer |  | True | True |  |
| addnum_suf | Address Number Suffix | String | 15 | True | True |  |
| st_premod | Street name Pre Modifier | String | 15 | True | True |  |
| st_predir | Street Name Pre Directional | String | 9 | True | True |  |
| st_pretyp | Street Name Pre Type | String | 50 | True | True |  |
| st_presep | Street Name Pre Type Separator | String | 20 | True | True |  |
| st_name | Street Name | String | 60 | True | True |  |
| st_postyp | Street Name Post Type | String | 50 | True | True |  |
| st_posdir | Street Name Post Directional | String | 9 | True | True |  |
| st_posmod | Street Name Post Modifier | String | 25 | True | True |  |
| discrpagid | Discrepancy Agency ID | String | 75 | True | True |  |
| dateupdate | Date Updated | Date | 29 | True | True |  |
| effective | Effective Date | Date | 29 | True | True |  |
| expire | Expiration Date | Date | 29 | True | True |  |
| country | Country | String | 2 | True | True |  |
| state | State | String | 2 | True | True |  |
| county | County | String | 40 | True | True |  |
| addcode | Additional Code | String | 6 | True | True |  |
| adddatauri | Additional Data URI | String | 254 | True | True |  |
| inc_muni | Incorporated Municipality | String | 100 | True | True |  |
| uninc_comm | Unincorporated Community | String | 100 | True | True |  |
| nbrhd_comm | Neighborhood Community | String | 100 | True | True |  |
| lst_predir | Legacy Street Name Pre Directional | String | 2 | True | True |  |
| lst_name | Legacy Street Name | String | 75 | True | True |  |
| lst_type | Legacy Street Name Type | String | 4 | True | True |  |
| lst_posdir | Legacy Street Name Post Directional | String | 2 | True | True |  |
| esn | ESN | String | 5 | True | True |  |
| msagcomm | MSAG Community Name | String | 30 | True | True |  |
| post_comm | Postal Community Name | String | 40 | True | True |  |
| post_code | Postal Code | String | 7 | True | True |  |
| post_code4 | ZIP Plus 4 | String | 4 | True | True |  |
| building | Building | String | 75 | True | True |  |
| floor | Floor | String | 75 | True | True |  |
| unit | Unit | String | 75 | True | True |  |
| room | Room | String | 75 | True | True |  |
| seat | Seat | String | 75 | True | True |  |
| addtl_loc | Additional Location Information | String | 225 | True | True |  |
| landmkname | Complete Landmark Name | String | 150 | True | True |  |
| mile_post | Milepost | String | 150 | True | True |  |
| place_type | Place Type | String | 50 | True | True |  |
| placement | Placement Method | String | 25 | True | True |  |
| long | Longitude | Double |  | True | True |  |
| lat | Latitude | Double |  | True | True |  |
| elev | Elevation | SmallInteger |  | True | True |  |
| gc_exception | GC QC Exception Code | SmallInteger |  | True | True |  |
| address_id | ADDRESS_ID | Integer |  | True | True |  |
| segment_id | SEGMENT_ID | Integer |  | True | True |  |
| name_id | NAME_ID | Integer |  | True | True |  |
| side | SIDE | String | 255 | True | True |  |
| anomaly | ANOMALY | String | 255 | True | True |  |
| unit_num | UNIT_NUM | String | 255 | True | True |  |
| unit_type | UNIT_TYPE | String | 255 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 29 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 29 | True | True |  |
| date_collected | Date Collected | Date | 29 | True | True |  |
| life_stage | Life Stage | String | 50 | True | True |  |
| found_in_trap | Found in Trap | String | 3 | True | True |  |
| location | Location | String | 255 | True | True |  |
| host_material | Host Material | String | 255 | True | True |  |
| comments | Comments | String | 255 | True | True |  |
| sent_to_lab | Sent to Lab | Date | 29 | True | True |  |
| pdr_number | PDR # | String | 30 | True | True |  |
| lab_confirmed | Lab Confirmed | String | 3 | True | True |  |
| quarter_mile_survey_required | 1/4 Mile Survey Required | String | 3 | True | True |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user_1 | created_user | String | 255 | True | True |  |
| created_date_1 | created_date | Date | 29 | True | True |  |
| last_edited_user_1 | last_edited_user | String | 255 | True | True |  |
| last_edited_date_1 | last_edited_date | Date | 29 | True | True |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| orig_fid | orig_fid | Integer |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### 02022026_ParcelsWithin150m (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| fid | fid | OID | 4 | False | False |  |
| parcelid | parcelid | String | 30 | True | True |  |
| data_notes | data_notes | String | 254 | True | True |  |
| taxmapnumb | taxmapnumb | String | 10 | True | True |  |
| gis_acreag | gis_acreag | Double |  | True | True |  |
| xcentroid | xcentroid | Double |  | True | True |  |
| ycentroid | ycentroid | Double |  | True | True |  |
| assessorma | assessorma | String | 254 | True | True |  |
| propertych | propertych | String | 254 | True | True |  |
| taxinfo | taxinfo | String | 254 | True | True |  |
| rollyear | rollyear | Integer |  | True | True |  |
| acres | acres | Double |  | True | True |  |
| lotsize | lotsize | Integer |  | True | True |  |
| usecode | usecode | String | 4 | True | True |  |
| use_desc | use_desc | String | 30 | True | True |  |
| subdiv | subdiv | String | 30 | True | True |  |
| qclass | qclass | Double |  | True | True |  |
| yrblt | yrblt | String | 4 | True | True |  |
| status | status | String | 2 | True | True |  |
| valland | valland | Integer |  | True | True |  |
| valimp | valimp | Integer |  | True | True |  |
| valtv | valtv | Integer |  | True | True |  |
| valfme | valfme | Integer |  | True | True |  |
| valpp | valpp | Integer |  | True | True |  |
| valpen | valpen | Integer |  | True | True |  |
| assessee | assessee | String | 30 | True | True |  |
| addr1 | addr1 | String | 30 | True | True |  |
| addr2 | addr2 | String | 30 | True | True |  |
| addr3 | addr3 | String | 20 | True | True |  |
| addr3_city | addr3_city | String | 20 | True | True |  |
| addr3_stat | addr3_stat | String | 2 | True | True |  |
| addrzip | addrzip | String | 10 | True | True |  |
| situs | situs | String | 2 | True | True |  |
| sitenum | sitenum | String | 6 | True | True |  |
| siteroad | siteroad | String | 30 | True | True |  |
| parceladdr | parceladdr | String | 37 | True | True |  |
| sitecity | sitecity | String | 14 | True | True |  |
| unitbldg | unitbldg | String | 7 | True | True |  |
| williamson | williamson | String | 2 | True | True |  |
| wa_status | wa_status | String | 2 | True | True |  |
| wa_contrac | wa_contrac | String | 8 | True | True |  |
| wa_prime | wa_prime | String | 8 | True | True |  |
| wa_nonprim | wa_nonprim | String | 8 | True | True |  |
| wa_exclude | wa_exclude | String | 8 | True | True |  |
| pcl_create | pcl_create | Integer |  | True | True |  |
| pcl_inactd | pcl_inactd | Integer |  | True | True |  |
| first_area | first_area | Integer |  | True | True |  |
| second_are | second_are | Integer |  | True | True |  |
| third_area | third_area | Integer |  | True | True |  |
| other_area | other_area | Integer |  | True | True |  |
| garage_are | garage_are | Integer |  | True | True |  |
| total_area | total_area | Double |  | True | True |  |
| stories | stories | Integer |  | True | True |  |
| bedroom | bedroom | String | 2 | True | True |  |
| bathroom | bathroom | String | 4 | True | True |  |
| dining | dining | String | 2 | True | True |  |
| family | family | String | 2 | True | True |  |
| other_room | other_room | String | 2 | True | True |  |
| utility | utility | String | 2 | True | True |  |
| total_room | total_room | String | 2 | True | True |  |
| fireplc | fireplc | String | 2 | True | True |  |
| hvac | hvac | String | 2 | True | True |  |
| pool | pool | String | 2 | True | True |  |
| solar | solar | String | 2 | True | True |  |
| tac | tac | Integer |  | True | True |  |
| tac_city | tac_city | String | 14 | True | True |  |
| govt_owned | govt_owned | String | 2 | True | True |  |
| hotype | hotype | String | 2 | True | True |  |
| zone1 | zone1 | String | 6 | True | True |  |
| zone2 | zone2 | String | 6 | True | True |  |
| z2acres | z2acres | Double |  | True | True |  |
| remark | remark | String | 30 | True | True |  |
| lndivnum | lndivnum | String | 40 | True | True |  |
| lndivdate | lndivdate | Integer |  | True | True |  |
| site_statu | site_statu | String | 2 | True | True |  |
| pudnum | pudnum | String | 40 | True | True |  |
| datevar | datevar | Integer |  | True | True |  |
| varnum | varnum | String | 6 | True | True |  |
| plfiltyp1 | plfiltyp1 | String | 2 | True | True |  |
| plfilno1 | plfilno1 | Integer |  | True | True |  |
| plfiltyp2 | plfiltyp2 | String | 2 | True | True |  |
| plfilno2 | plfilno2 | Integer |  | True | True |  |
| fund_fire | fund_fire | String | 4 | True | True |  |
| desc_fire | desc_fire | String | 30 | True | True |  |
| fund_schoo | fund_schoo | String | 4 | True | True |  |
| desc_schoo | desc_schoo | String | 30 | True | True |  |
| fund_water | fund_water | String | 4 | True | True |  |
| desc_water | desc_water | String | 30 | True | True |  |
| fund_air_b | fund_air_b | String | 4 | True | True |  |
| desc_air_b | desc_air_b | String | 30 | True | True |  |
| fund_soil_ | fund_soil_ | String | 4 | True | True |  |
| desc_soil_ | desc_soil_ | String | 30 | True | True |  |
| acreage_di | acreage_di | Double |  | True | True |  |
| st_area_sh | st_area_sh | Double |  | True | True |  |
| st_length_ | st_length_ | Double |  | True | True |  |

#### 8_26_23_TreatmentBuffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### 150_Meter_Buffer_7_31_23 (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| date_collected | Date Collected | Date | 29 | True | True |  |
| life_stage | Life Stage | String | 50 | True | True |  |
| found_in_trap | Found in Trap | String | 3 | True | True |  |
| location | Location | String | 255 | True | True |  |
| host_material | Host Material | String | 255 | True | True |  |
| comments | Comments | String | 255 | True | True |  |
| sent_to_lab | Sent to Lab | Date | 29 | True | True |  |
| pdr_number | PDR # | String | 30 | True | True |  |
| lab_confirmed | Lab Confirmed | String | 3 | True | True |  |
| quarter_mile_survey_required | 1/4 Mile Survey Required | String | 3 | True | True |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 29 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 29 | True | True |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| orig_fid | ORIG_FID | Integer |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### 2_8_24_Treatment_Buffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### 7_3_24_Treatment_Buffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| date_collected | Date Collected | Date | 29 | True | True |  |
| life_stage | Life Stage | String | 50 | True | True |  |
| found_in_trap | Found in Trap | String | 3 | True | True |  |
| location | Location | String | 255 | True | True |  |
| host_material | Host Material | String | 255 | True | True |  |
| comments | Comments | String | 255 | True | True |  |
| sent_to_lab | Sent to Lab | Date | 29 | True | True |  |
| pdr_number | PDR # | String | 30 | True | True |  |
| lab_confirmed | Lab Confirmed | String | 3 | True | True |  |
| quarter_mile_survey_required | 1/4 Mile Survey Required | String | 3 | True | True |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 29 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 29 | True | True |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| orig_fid | ORIG_FID | Integer |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

#### Soil_Treatments_2025_corrected (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| join_count | Join_Count | Integer |  | True | True |  |
| target_fid | TARGET_FID | Integer |  | True | True |  |
| site_nguid | Site NENA Globally Unique ID | String | 254 | True | True |  |
| apn | APN | String | 30 | True | True |  |
| fulladdress | Full Address | String | 255 | True | True |  |
| fulladdr_label_abbrv | Abbreviated Label | String | 255 | True | True |  |
| fulladdr_label | Full Address Label | String | 255 | True | True |  |
| gtg_flag | GTG_Flag | SmallInteger |  | True | True |  |
| gtg_notes | GTG_Notes | String | 255 | True | True |  |
| addnum_pre | Address Number Prefix | String | 15 | True | True |  |
| add_number | Address Number | Integer |  | True | True |  |
| addnum_suf | Address Number Suffix | String | 15 | True | True |  |
| st_premod | Street name Pre Modifier | String | 15 | True | True |  |
| st_predir | Street Name Pre Directional | String | 9 | True | True |  |
| st_pretyp | Street Name Pre Type | String | 50 | True | True |  |
| st_presep | Street Name Pre Type Separator | String | 20 | True | True |  |
| st_name | Street Name | String | 60 | True | True |  |
| st_postyp | Street Name Post Type | String | 50 | True | True |  |
| st_posdir | Street Name Post Directional | String | 9 | True | True |  |
| st_posmod | Street Name Post Modifier | String | 25 | True | True |  |
| discrpagid | Discrepancy Agency ID | String | 75 | True | True |  |
| dateupdate | Date Updated | Date | 29 | True | True |  |
| effective | Effective Date | Date | 29 | True | True |  |
| expire | Expiration Date | Date | 29 | True | True |  |
| country | Country | String | 2 | True | True |  |
| state | State | String | 2 | True | True |  |
| county | County | String | 40 | True | True |  |
| addcode | Additional Code | String | 6 | True | True |  |
| adddatauri | Additional Data URI | String | 254 | True | True |  |
| inc_muni | Incorporated Municipality | String | 100 | True | True |  |
| uninc_comm | Unincorporated Community | String | 100 | True | True |  |
| nbrhd_comm | Neighborhood Community | String | 100 | True | True |  |
| lst_predir | Legacy Street Name Pre Directional | String | 2 | True | True |  |
| lst_name | Legacy Street Name | String | 75 | True | True |  |
| lst_type | Legacy Street Name Type | String | 4 | True | True |  |
| lst_posdir | Legacy Street Name Post Directional | String | 2 | True | True |  |
| esn | ESN | String | 5 | True | True |  |
| msagcomm | MSAG Community Name | String | 30 | True | True |  |
| post_comm | Postal Community Name | String | 40 | True | True |  |
| post_code | Postal Code | String | 7 | True | True |  |
| post_code4 | ZIP Plus 4 | String | 4 | True | True |  |
| building | Building | String | 75 | True | True |  |
| floor | Floor | String | 75 | True | True |  |
| unit | Unit | String | 75 | True | True |  |
| room | Room | String | 75 | True | True |  |
| seat | Seat | String | 75 | True | True |  |
| addtl_loc | Additional Location Information | String | 225 | True | True |  |
| landmkname | Complete Landmark Name | String | 150 | True | True |  |
| mile_post | Milepost | String | 150 | True | True |  |
| place_type | Place Type | String | 50 | True | True |  |
| placement | Placement Method | String | 25 | True | True |  |
| long | Longitude | Double |  | True | True |  |
| lat | Latitude | Double |  | True | True |  |
| elev | Elevation | SmallInteger |  | True | True |  |
| gc_exception | GC QC Exception Code | SmallInteger |  | True | True |  |
| address_id | ADDRESS_ID | Integer |  | True | True |  |
| segment_id | SEGMENT_ID | Integer |  | True | True |  |
| name_id | NAME_ID | Integer |  | True | True |  |
| side | SIDE | String | 255 | True | True |  |
| anomaly | ANOMALY | String | 255 | True | True |  |
| unit_num | UNIT_NUM | String | 255 | True | True |  |
| unit_type | UNIT_TYPE | String | 255 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 29 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 29 | True | True |  |
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |

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

#### 02022026_GWSSFinding_150m_Buffer (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| fid | fid | OID | 4 | False | False |  |
| date_colle | date_colle | Date | 29 | True | True |  |
| life_stage | life_stage | String | 50 | True | True |  |
| found_in_t | found_in_t | String | 3 | True | True |  |
| location | location | String | 254 | True | True |  |
| host_mater | host_mater | String | 254 | True | True |  |
| comments | comments | String | 254 | True | True |  |
| sent_to_la | sent_to_la | Date | 29 | True | True |  |
| pdr_number | pdr_number | String | 30 | True | True |  |
| lab_confir | lab_confir | String | 3 | True | True |  |
| quarter_mi | quarter_mi | String | 3 | True | True |  |
| rel_global | rel_global | String | 38 | True | True |  |
| created_us | created_us | String | 254 | True | True |  |
| created_da | created_da | Date | 29 | True | True |  |
| last_edite | last_edite | String | 254 | True | True |  |
| last_edi_1 | last_edi_1 | Date | 29 | True | True |  |
| parcelid_t | parcelid_t | String | 30 | True | True |  |
| buff_dist | BUFF_DIST | Double |  | True | True |  |
| orig_fid | ORIG_FID | Integer |  | True | True |  |

#### Address Points (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| site_nguid | Site NENA Globally Unique ID | String | 254 | True | True |  |
| apn | APN | String | 30 | True | True |  |
| fulladdress | Full Address | String | 255 | True | True |  |
| fulladdr_label_abbrv | Abbreviated Label | String | 255 | True | True |  |
| fulladdr_label | Full Address Label | String | 255 | True | True |  |
| gtg_flag | GTG_Flag | SmallInteger |  | True | True | AP_GTG_Flag |
| gtg_notes | GTG_Notes | String | 255 | True | True |  |
| addnum_pre | Address Number Prefix | String | 15 | True | True |  |
| add_number | Address Number | Integer |  | True | True |  |
| addnum_suf | Address Number Suffix | String | 15 | True | True |  |
| st_premod | Street name Pre Modifier | String | 15 | True | True |  |
| st_predir | Street Name Pre Directional | String | 9 | True | True |  |
| st_pretyp | Street Name Pre Type | String | 50 | True | True |  |
| st_presep | Street Name Pre Type Separator | String | 20 | True | True |  |
| st_name | Street Name | String | 60 | True | True |  |
| st_postyp | Street Name Post Type | String | 50 | True | True |  |
| st_posdir | Street Name Post Directional | String | 9 | True | True |  |
| st_posmod | Street Name Post Modifier | String | 25 | True | True |  |
| discrpagid | Discrepancy Agency ID | String | 75 | True | True |  |
| dateupdate | Date Updated | Date | 8 | True | True |  |
| effective | Effective Date | Date | 8 | True | True |  |
| expire | Expiration Date | Date | 8 | True | True |  |
| country | Country | String | 2 | True | True |  |
| state | State | String | 2 | True | True |  |
| county | County | String | 40 | True | True |  |
| addcode | Additional Code | String | 6 | True | True |  |
| adddatauri | Additional Data URI | String | 254 | True | True |  |
| inc_muni | Incorporated Municipality | String | 100 | True | True |  |
| uninc_comm | Unincorporated Community | String | 100 | True | True |  |
| nbrhd_comm | Neighborhood Community | String | 100 | True | True |  |
| lst_predir | Legacy Street Name Pre Directional | String | 2 | True | True |  |
| lst_name | Legacy Street Name | String | 75 | True | True |  |
| lst_type | Legacy Street Name Type | String | 4 | True | True |  |
| lst_posdir | Legacy Street Name Post Directional | String | 2 | True | True |  |
| esn | ESN | String | 5 | True | True |  |
| msagcomm | MSAG Community Name | String | 30 | True | True |  |
| post_comm | Postal Community Name | String | 40 | True | True |  |
| post_code | Postal Code | String | 7 | True | True |  |
| post_code4 | ZIP Plus 4 | String | 4 | True | True |  |
| building | Building | String | 75 | True | True |  |
| floor | Floor | String | 75 | True | True |  |
| unit | Unit | String | 75 | True | True |  |
| room | Room | String | 75 | True | True |  |
| seat | Seat | String | 75 | True | True |  |
| addtl_loc | Additional Location Information | String | 225 | True | True |  |
| landmkname | Complete Landmark Name | String | 150 | True | True |  |
| mile_post | Milepost | String | 150 | True | True |  |
| place_type | Place Type | String | 50 | True | True |  |
| placement | Placement Method | String | 25 | True | True |  |
| long | Longitude | Double |  | True | True |  |
| lat | Latitude | Double |  | True | True |  |
| elev | Elevation | SmallInteger |  | True | True |  |
| gc_exception | GC QC Exception Code | SmallInteger |  | True | True |  |
| address_id | ADDRESS_ID | Integer |  | True | True |  |
| segment_id | SEGMENT_ID | Integer |  | True | True |  |
| name_id | NAME_ID | Integer |  | True | True |  |
| side | SIDE | String | 255 | True | True |  |
| anomaly | ANOMALY | String | 255 | True | True |  |
| unit_num | UNIT_NUM | String | 255 | True | True |  |
| unit_type | UNIT_TYPE | String | 255 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 8 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 8 | True | True |  |

#### GWSS Traps (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| route | Route | String | 15 | True | True | trap routes |
| address | Address | String | 100 | True | True |  |
| trap_id | Trap ID | String | 50 | True | True |  |
| location_description | Location description | String | 100 | True | True |  |
| comments | comments | String | 255 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### GWSS Findings (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| date_collected | Date Collected | Date | 8 | True | True |  |
| life_stage | Life Stage | String | 50 | True | True | life_stage |
| found_in_trap | Found in Trap | String | 3 | True | True | yes no |
| location | Location | String | 255 | True | True |  |
| host_material | Host Material | String | 255 | True | True |  |
| comments | Comments | String | 255 | True | True |  |
| sent_to_lab | Sent to Lab | Date | 8 | True | True |  |
| pdr_number | PDR # | String | 30 | True | True |  |
| lab_confirmed | Lab Confirmed | String | 3 | True | True | yes no |
| quarter_mile_survey_required | 1/4 Mile Survey Required | String | 3 | True | True | yes no |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |

#### GWSS Survey Areas (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| gwss_findings_rel_global | gwss_findings_rel_global | GUID | 38 | True | True |  |
| survey_area_name | Survey Area Name | String | 255 | True | True |  |

#### GWSS Tracking (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| parcelid | ParcelID | String | 30 | True | True |  |
| data_notes | Data Notes | String | 255 | True | True |  |
| asmtnum | asmtnum | String | 10 | True | True |  |
| rollyear | rollyear | String | 6 | True | True |  |
| acres | Acres | Double |  | True | True |  |
| lotsize | Lot Size | Double |  | True | True |  |
| usecode | usecode | String | 4 | True | True |  |
| desusecode | desusecode | String | 30 | True | True |  |
| subdiv | Subdivision | String | 32 | True | True |  |
| pdqclass | pdqclass | Double |  | True | True |  |
| pdyrblt | pdyrblt | String | 4 | True | True |  |
| status | status | String | 2 | True | True |  |
| landval | landval | Double |  | True | True |  |
| improveval | improveval | Double |  | True | True |  |
| trevineval | trevineval | Double |  | True | True |  |
| fixedeqval | fixedeqval | Double |  | True | True |  |
| perpropval | perpropval | Double |  | True | True |  |
| penaltyval | penaltyval | Double |  | True | True |  |
| situs | situs | String | 2 | True | True |  |
| sitenum | sitenum | String | 6 | True | True |  |
| siteroad | siteroad | String | 30 | True | True |  |
| parceladdress | parceladdress | String | 37 | True | True |  |
| sitecity | sitecity | String | 14 | True | True |  |
| zip | zip | String | 10 | True | True |  |
| unitbldg | unitbldg | String | 7 | True | True |  |
| williamson_act | williamson_act | String | 2 | True | True |  |
| pcl_createdate | pcl_createdate | Double |  | True | True |  |
| pcl_inactdate | pcl_inactdate | Double |  | True | True |  |
| gwss_action | gwss_action | String | 50 | True | True | gwss_tracking_action |
| gwss_action_dow | gwss_action_dow | String | 255 | True | True | DayOfWeek |
| gwss_infested_adjacent | gwss_infested_adjacent | String | 255 | True | True | infested_adjacent |
| gwss_comments | gwss_comments | String | 1000 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### GWSS Tracking History (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| gwss_findings_rel_globalid | gwss_findings_rel_globalid | GUID | 38 | True | True |  |
| parcelid | ParcelID | String | 30 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### GWSS Surveys (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| biologists | Biologists | String | 50 | True | True |  |
| survey_date | Survey Date | Date | 8 | True | True |  |
| survey_refusal | Survey Refusal | String | 3 | True | True | yes no |
| fy_inspected | Front Yard Inspected | String | 3 | True | True | inspected_y_n_r |
| by_inspected | Back Yard Inspected | String | 3 | True | True | inspected_y_n_r |
| infested | Infested | String | 3 | True | True | yes no |
| adjacent | Adjacent | String | 3 | True | True | yes no |
| information_left | Information Left | String | 3 | True | True | yes no |
| sample_collected | Sample Collected | String | 3 | True | True | yes no |
| comments | Comments | String | 255 | True | True |  |
| revisit_biologists | Biologists Revisted | String | 50 | True | True |  |
| revisit_date | Date Revisited | Date | 8 | True | True |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |

#### GWSS Treatment (Table)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| infested_adjacent | Infested or Adjacent Treatment | String | 255 | True | True | infested_adjacent |
| infested_pdr | Infested PDR Number | String | 255 | True | True |  |
| knock_talk_date | Knock & Talk Completed | Date | 8 | True | True |  |
| knock_talk_attempts | Knock & Talk Attempt Dates (if applicable) | String | 255 | True | True |  |
| renter_leasee | Renter or Leasee | String | 3 | True | True | yes no |
| property_manager | Property Manager | String | 255 | True | True |  |
| phone | Phone Number | String | 50 | True | True |  |
| email | email | String | 100 | True | True |  |
| contact_made | Contact Made With Homeowner | String | 10 | True | True | yes no |
| consent_to_spray | Consent to Spray | String | 30 | True | True | gwss_treatment_consent |
| info_left | Information Left | String | 3 | True | True | yes no |
| fy_approval | Front Yard Approval | String | 3 | True | True | yes no |
| by_approval | Back Yard Approval | String | 3 | True | True | yes no |
| preferred_date | Preferred Date of Treatment | Date | 8 | True | True |  |
| preferred_time | Preferred Time of Treatment | String | 5 | True | True | AM PM |
| planned_date | planned_date | Date | 8 | True | True |  |
| planned_time | planned_time | String | 5 | True | True | AM PM |
| neighbors_for_notification | neighbors_for_notification | String | 500 | True | True |  |
| host_size | Size of Host | String | 255 | True | True |  |
| comments | Comments | String | 500 | True | True |  |
| response_assigned_to | Response Assigned To | String | 100 | True | True |  |
| notified | Date Notified | Date | 8 | True | True |  |
| neighbors_notified | Date Neighbors Notified | Date | 8 | True | True |  |
| missed_treatment | Missed Treatment Date | Date | 8 | True | True |  |
| treatment_inspector | Treatment Inspector | String | 100 | True | True |  |
| treatment_date | treatment_date | Date | 8 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| notice_color | Notice Color Left at Address | String | 50 | True | True | notice_color |
| soil_treatment_date | Soil Treatment Date | Date | 8 | True | True |  |
| soil_missed_treatment | Soil Missed Treatement Date | Date | 8 | True | True |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |

#### Biological Control (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| date | Date | Date | 8 | True | True |  |
| address | Address | String | 255 | True | True |  |
| comment | Comment | String | 300 | True | True |  |
| created_user | created_user | String | 255 | True | False |  |
| created_date | created_date | Date | 8 | True | False |  |
| last_edited_user | last_edited_user | String | 255 | True | False |  |
| last_edited_date | last_edited_date | Date | 8 | True | False |  |

#### QuarBoundary (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| id | Id | Integer |  | True | True |  |

#### Buffer_of_Non_Viable_Eggmass_2 (Feature Layer)

| Field | Alias | Type | Length | Nullable | Editable | Domain |
|---|---|---|---|---|---|---|
| date_collected | Date Collected | Date | 29 | True | True |  |
| life_stage | Life Stage | String | 50 | True | True |  |
| found_in_trap | Found in Trap | String | 3 | True | True |  |
| location | Location | String | 255 | True | True |  |
| host_material | Host Material | String | 255 | True | True |  |
| comments | Comments | String | 255 | True | True |  |
| sent_to_lab | Sent to Lab | Date | 29 | True | True |  |
| pdr_number | PDR # | String | 30 | True | True |  |
| lab_confirmed | Lab Confirmed | String | 3 | True | True |  |
| quarter_mile_survey_required | 1/4 Mile Survey Required | String | 3 | True | True |  |
| rel_globalid | rel_globalid | GUID | 38 | True | True |  |
| created_user | created_user | String | 255 | True | True |  |
| created_date | created_date | Date | 29 | True | True |  |
| last_edited_user | last_edited_user | String | 255 | True | True |  |
| last_edited_date | last_edited_date | Date | 29 | True | True |  |
| parcelid_temp | parcelID_temp | String | 30 | True | True |  |
| buff_dist | Buffer distance in Meters | Double |  | True | True |  |
| orig_fid | ORIG_FID | Integer |  | True | True |  |
| analysisarea | Area in Square Kilometers | Double |  | True | True |  |
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
**AM PM**

| Coded Value | Alias |
|---|---|
| AM | AM |
| PM | PM |

**AP_GTG_Flag**

| Coded Value | Alias |
|---|---|
| 1 | See GTG Notes field |
| 2 | Multiunit verification |
| 3 | Contact city of Benicia |
| 4 | Contact city of Rio Vista |
| 5 | Contact city of Fairfield |
| 6 | Contact city of Vallejo |
| 7 | Contact city of Vacaville |
| 8 | Contact city of Suisun |
| 9 | Contact city of Dixon |
| 10 | Contact Solano/Unincorp Area |
| 11 | New AP by GTG |
| 12 | Address not in assessor table |

**DayOfWeek**

| Coded Value | Alias |
|---|---|
| Mon | Monday |
| Tue | Tuesday |
| Wed | Wednesday |
| Thu | Thursday |
| Fri | Friday |

**gwss_tracking_action**

| Coded Value | Alias |
|---|---|
| Action Completed / No Action Needed | Action Completed / No Action Needed |
| Requires Treatment (Foliage) - Infested Property | Requires Treatment (Foliage) - Infested Property |
| Requires Treatment (Soil) - Infested Property | Requires Treatment (Soil) - Infested Property |
| Requires Treatment (Foliage) - Adjacent Property | Requires Treatment (Foliage) - Adjacent Property |
| Requires Treatment (Soil) - Adjacent Property | Requires Treatment (Soil) - Adjacent Property |
| Requires Inspection | Requires Inspection |

**gwss_treatment_consent**

| Coded Value | Alias |
|---|---|
| Awaiting Consent | Awaiting Consent |
| Consent Received | Consent Received |
| Refused Treatment | Refused Treatment |

**infested_adjacent**

| Coded Value | Alias |
|---|---|
| Infested | Infested |
| Adjacent | Adjacent |

**inspected_y_n_r**

| Coded Value | Alias |
|---|---|
| Yes | Yes |
| No | No |
| Ref | Refused |

**life_stage**

| Coded Value | Alias |
|---|---|
| Adult | Adult |
| Nymph | Nymph |
| Adult Male | Adult Male |
| Adult Female | Adult Female |
| Nymph Molt | Nymph Molt |
| Eggmass | Eggmass |
| Viable Eggmass | Viable Eggmass |
| To Be Determined | To Be Determined |
| Parasitized Eggmass | Parasitized Eggmass |
| Non-Viable Eggmass | Non-Viable Eggmass |

**notice_color**

| Coded Value | Alias |
|---|---|
| Green | Green |
| Yellow | Yellow |
| Blue | Blue |
| Pink | Pink |

**trap routes**

| Coded Value | Alias |
|---|---|
| Red | Red |
| Blue | Blue |
| Delim 1 | Delim 1 |
| Delim 2 | Delim 2 |
| Delim 3 | Delim 3 |
| Delim 4 | Delim 4 |
| Delim 5 | Delim 5 |
| Delim 6 | Delim 6 |
| Delim 7 | Delim 7 |
| Delim 8 | Delim 8 |
| Delim 9 | Delim 9 |
| Delim 10 | Delim 10 |

**yes no**

| Coded Value | Alias |
|---|---|
| Yes | Yes |
| No | No |
<!-- /GENERATED:domains -->

## 6. Subtypes

<!-- GENERATED:subtypes -->
- **GWSS Tracking**: Action Completed / No Action Needed
- **GWSS Tracking**: Requires Inspection
- **GWSS Tracking**: Requires Treatment (Foliage) - Adjacent Property
- **GWSS Tracking**: Requires Treatment (Foliage) - Infested Property
- **GWSS Tracking**: Requires Treatment (Soil) - Adjacent Property
- **GWSS Tracking**: Requires Treatment (Soil) - Infested Property
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
| Layer/Table | Relationship | Cardinality |
|---|---|---|
| GWSS Findings | solano_prod.gisadm.GWSS_Tracking | esriRelCardinalityOneToMany |
| GWSS Tracking | solano_prod.gisadm.GWSS_Surveys | esriRelCardinalityOneToMany |
| GWSS Tracking | solano_prod.gisadm.GWSS_Findings | esriRelCardinalityOneToMany |
| GWSS Tracking | solano_prod.gisadm.GWSS_Treatment | esriRelCardinalityOneToMany |
| GWSS Surveys | solano_prod.gisadm.GWSS_Tracking | esriRelCardinalityOneToMany |
| GWSS Treatment | solano_prod.gisadm.GWSS_Tracking | esriRelCardinalityOneToMany |
<!-- /GENERATED:relationships -->

## 8. Database View Definitions

Eight views expose combined and most-recent data from the relational tables. They are used as the data sources for the map service layers that drive symbology and enable list exports. A ninth view (`v_gwss_what_parcels_in_buffer_have_surveys`) exists only for back-end analysis and is not published as a service layer.

All views are defined in the enterprise PostgreSQL database. The authoritative definitions are best accessed via pgAdmin; the SQL below is copied verbatim from the Appendix of the GWSS Technical Documentation (KCI, v1.3, 4/25/2022).

---

### v_gwss_all_findings

**Purpose:** Joins all GWSS finding records to their parent parcel (tracking record) to expose parcel address fields alongside each finding — enabling holistic display and export of findings with location context.

```sql
SELECT gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    gwss_findings.objectid,
    gwss_findings.shape,
    gwss_findings.globalid,
    gwss_findings.date_collected,
    gwss_findings.life_stage,
    gwss_findings.found_in_trap,
    gwss_findings.location,
    gwss_findings.host_material,
    gwss_findings.comments,
    gwss_findings.sent_to_lab,
    gwss_findings.pdr_number,
    gwss_findings.lab_confirmed,
    gwss_findings.quarter_mile_survey_required,
    gwss_findings.rel_globalid,
    gwss_findings.created_user,
    gwss_findings.created_date,
    gwss_findings.last_edited_user,
    gwss_findings.last_edited_date
   FROM gwss_findings
     JOIN gwss_tracking ON gwss_findings.rel_globalid::text = gwss_tracking.globalid::text;
```

---

### v_gwss_all_surveys

**Purpose:** Joins all survey records to their parent parcel and computes a `survey_result` classification (Infested / Adjacent / Clear / Survey Incomplete / Refused Survey) via a CASE expression — enabling holistic display and export of all surveys with address context and derived status.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    gwss_surveys.objectid,
    gwss_surveys.biologists,
    gwss_surveys.survey_date,
    gwss_surveys.survey_refusal,
    gwss_surveys.fy_inspected,
    gwss_surveys.by_inspected,
    gwss_surveys.infested,
    gwss_surveys.adjacent,
    gwss_surveys.information_left,
    gwss_surveys.sample_collected,
    gwss_surveys.comments,
    gwss_surveys.revisit_biologists,
    gwss_surveys.revisit_date,
    gwss_surveys.rel_globalid,
    gwss_surveys.globalid,
    gwss_surveys.created_user,
    gwss_surveys.created_date,
    gwss_surveys.last_edited_user,
    gwss_surveys.last_edited_date,
        CASE
            WHEN gwss_surveys.infested::text = 'Yes'::text THEN 'Infested'::text
            WHEN gwss_surveys.adjacent::text = 'Yes'::text THEN 'Adjacent'::text
            WHEN gwss_surveys.fy_inspected::text = 'Yes'::text AND gwss_surveys.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN gwss_surveys.fy_inspected::text = 'Yes'::text OR gwss_surveys.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN (gwss_surveys.fy_inspected IS NULL OR gwss_surveys.fy_inspected::text = 'No'::text) AND (gwss_surveys.by_inspected IS NULL OR gwss_surveys.by_inspected::text = 'No'::text) AND gwss_surveys.survey_refusal::text = 'No'::text THEN 'Survey Incomplete'::text
            WHEN gwss_surveys.survey_refusal::text = 'Yes'::text THEN 'Refused Survey'::text
            ELSE NULL::text
        END AS survey_result
   FROM gwss_tracking
     JOIN gwss_surveys ON gwss_tracking.globalid::text = gwss_surveys.rel_globalid::text;
```

---

### v_gwss_all_treatments

**Purpose:** Joins all treatment records to their parent parcel and computes a `treatment_status` classification (covering treatment completion, foliage/soil combinations, missed treatments, consent stages, and refusals) — enabling holistic display and export of all treatment activity with address context.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    gwss_treatment.objectid,
    gwss_treatment.infested_adjacent,
    gwss_treatment.infested_pdr,
    gwss_treatment.knock_talk_date,
    gwss_treatment.knock_talk_attempts,
    gwss_treatment.renter_leasee,
    gwss_treatment.property_manager,
    gwss_treatment.phone,
    gwss_treatment.email,
    gwss_treatment.contact_made,
    gwss_treatment.consent_to_spray,
    gwss_treatment.info_left,
    gwss_treatment.fy_approval,
    gwss_treatment.by_approval,
    gwss_treatment.preferred_date,
    gwss_treatment.preferred_time,
    gwss_treatment.planned_date,
    gwss_treatment.planned_time,
    gwss_treatment.neighbors_for_notification,
    gwss_treatment.host_size,
    gwss_treatment.comments,
    gwss_treatment.response_assigned_to,
    gwss_treatment.notified,
    gwss_treatment.neighbors_notified,
    gwss_treatment.missed_treatment,
    gwss_treatment.treatment_inspector,
    gwss_treatment.treatment_date,
    gwss_treatment.notice_color,
    gwss_treatment.soil_treatment_date,
    gwss_treatment.soil_missed_treatment,
    gwss_treatment.created_user,
    gwss_treatment.created_date,
    gwss_treatment.last_edited_user,
    gwss_treatment.last_edited_date,
    gwss_treatment.globalid,
    gwss_treatment.rel_globalid,
        CASE
            WHEN gwss_treatment.treatment_date IS NOT NULL AND gwss_treatment.soil_treatment_date IS NOT NULL THEN 'Treatments Complete (Both Foliage and Soil)'::text
            WHEN gwss_treatment.treatment_date IS NOT NULL AND gwss_treatment.soil_treatment_date IS NULL AND gwss_treatment.soil_missed_treatment IS NULL THEN 'Foliage Treatment Complete, Awaiting Soil Treatment'::text
            WHEN gwss_treatment.treatment_date IS NULL AND gwss_treatment.missed_treatment IS NULL AND gwss_treatment.soil_treatment_date IS NOT NULL THEN 'Soil Treatment Complete, Awaiting Foliage Treatment'::text
            WHEN gwss_treatment.treatment_date IS NOT NULL AND gwss_treatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Complete)'::text
            WHEN gwss_treatment.missed_treatment IS NOT NULL AND gwss_treatment.soil_treatment_date IS NOT NULL THEN 'Missed Foliage Treatment (Soil Treatment Complete)'::text
            WHEN gwss_treatment.missed_treatment IS NOT NULL AND gwss_treatment.soil_missed_treatment IS NOT NULL THEN 'Missed Foliage AND Soil Treatment'::text
            WHEN gwss_treatment.missed_treatment IS NOT NULL AND gwss_treatment.soil_treatment_date IS NULL THEN 'Missed Foliage Treatment (Soil Treatment Not Yet Attempted)'::text
            WHEN gwss_treatment.treatment_date IS NULL AND gwss_treatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Not Yet Attempted)'::text
            WHEN gwss_treatment.consent_to_spray::text = 'Refused Treatment'::text THEN 'Treatment Refused'::text
            WHEN gwss_treatment.consent_to_spray::text = 'Consent Received'::text THEN 'Treatement Consent Received'::text
            ELSE 'Advanced Treatment Notice'::text
        END AS treatment_status
   FROM gwss_tracking
     JOIN gwss_treatment ON gwss_tracking.globalid::text = gwss_treatment.rel_globalid::text;
```

---

### v_gwss_most_recent_survey_per_parcel

**Purpose:** Returns only the most recently created survey record per parcel (using a subquery that selects the `MAX(created_date)` per `rel_globalid`), joined to the parent parcel for address context, with the same `survey_result` CASE expression as `v_gwss_all_surveys`. This view is the data source for the map layer that symbolizes parcel survey status.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    mostrecentgwsssurvey.objectid,
    mostrecentgwsssurvey.biologists,
    mostrecentgwsssurvey.survey_date,
    mostrecentgwsssurvey.survey_refusal,
    mostrecentgwsssurvey.fy_inspected,
    mostrecentgwsssurvey.by_inspected,
    mostrecentgwsssurvey.infested,
    mostrecentgwsssurvey.adjacent,
    mostrecentgwsssurvey.information_left,
    mostrecentgwsssurvey.sample_collected,
    mostrecentgwsssurvey.comments,
    mostrecentgwsssurvey.revisit_biologists,
    mostrecentgwsssurvey.revisit_date,
    mostrecentgwsssurvey.rel_globalid,
    mostrecentgwsssurvey.globalid,
    mostrecentgwsssurvey.created_user,
    mostrecentgwsssurvey.created_date,
    mostrecentgwsssurvey.last_edited_user,
    mostrecentgwsssurvey.last_edited_date,
        CASE
            WHEN mostrecentgwsssurvey.infested::text = 'Yes'::text THEN 'Infested'::text
            WHEN mostrecentgwsssurvey.adjacent::text = 'Yes'::text THEN 'Adjacent'::text
            WHEN mostrecentgwsssurvey.fy_inspected::text = 'Yes'::text AND mostrecentgwsssurvey.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN mostrecentgwsssurvey.fy_inspected::text = 'Yes'::text OR mostrecentgwsssurvey.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN (mostrecentgwsssurvey.fy_inspected IS NULL OR mostrecentgwsssurvey.fy_inspected::text = 'No'::text) AND (mostrecentgwsssurvey.by_inspected IS NULL OR mostrecentgwsssurvey.by_inspected::text = 'No'::text) AND mostrecentgwsssurvey.survey_refusal::text = 'No'::text THEN 'Survey Incomplete'::text
            WHEN mostrecentgwsssurvey.survey_refusal::text = 'Yes'::text THEN 'Refused Survey'::text
            ELSE NULL::text
        END AS survey_result
   FROM gwss_tracking
     JOIN ( SELECT gwss_surveys.objectid,
            gwss_surveys.biologists,
            gwss_surveys.survey_date,
            gwss_surveys.survey_refusal,
            gwss_surveys.fy_inspected,
            gwss_surveys.by_inspected,
            gwss_surveys.infested,
            gwss_surveys.adjacent,
            gwss_surveys.information_left,
            gwss_surveys.sample_collected,
            gwss_surveys.comments,
            gwss_surveys.revisit_biologists,
            gwss_surveys.revisit_date,
            gwss_surveys.rel_globalid,
            gwss_surveys.globalid,
            gwss_surveys.created_user,
            gwss_surveys.created_date,
            gwss_surveys.last_edited_user,
            gwss_surveys.last_edited_date
           FROM gwss_surveys
             JOIN ( SELECT max(gwss_surveys_1.created_date) AS mostrecent_createddate,
                    gwss_surveys_1.rel_globalid
                   FROM gwss_surveys gwss_surveys_1
                  GROUP BY gwss_surveys_1.rel_globalid) mostrecentsurvey ON gwss_surveys.rel_globalid::text = mostrecentsurvey.rel_globalid::text AND gwss_surveys.created_date = mostrecentsurvey.mostrecent_createddate) mostrecentgwsssurvey ON gwss_tracking.globalid::text = mostrecentgwsssurvey.rel_globalid::text;
```

---

### v_gwss_most_recent_treatment_per_parcel

**Purpose:** Returns only the most recently created treatment record per parcel, joined to the parent parcel for address context, with the full `treatment_status` CASE expression (including the Partial Refusal cases added 3/16/22). This view is the data source for the map layer that symbolizes parcel treatment status and drives the purple "Partial Refusal" symbology.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    mostrecentgwsstreatment.objectid,
    mostrecentgwsstreatment.infested_adjacent,
    mostrecentgwsstreatment.infested_pdr,
    mostrecentgwsstreatment.knock_talk_date,
    mostrecentgwsstreatment.knock_talk_attempts,
    mostrecentgwsstreatment.renter_leasee,
    mostrecentgwsstreatment.property_manager,
    mostrecentgwsstreatment.phone,
    mostrecentgwsstreatment.email,
    mostrecentgwsstreatment.contact_made,
    mostrecentgwsstreatment.consent_to_spray,
    mostrecentgwsstreatment.info_left,
    mostrecentgwsstreatment.fy_approval,
    mostrecentgwsstreatment.by_approval,
    mostrecentgwsstreatment.preferred_date,
    mostrecentgwsstreatment.preferred_time,
    mostrecentgwsstreatment.planned_date,
    mostrecentgwsstreatment.planned_time,
    mostrecentgwsstreatment.neighbors_for_notification,
    mostrecentgwsstreatment.host_size,
    mostrecentgwsstreatment.comments,
    mostrecentgwsstreatment.response_assigned_to,
    mostrecentgwsstreatment.notified,
    mostrecentgwsstreatment.neighbors_notified,
    mostrecentgwsstreatment.missed_treatment,
    mostrecentgwsstreatment.treatment_inspector,
    mostrecentgwsstreatment.treatment_date,
    mostrecentgwsstreatment.notice_color,
    mostrecentgwsstreatment.soil_treatment_date,
    mostrecentgwsstreatment.soil_missed_treatment,
    mostrecentgwsstreatment.created_user,
    mostrecentgwsstreatment.created_date,
    mostrecentgwsstreatment.last_edited_user,
    mostrecentgwsstreatment.last_edited_date,
    mostrecentgwsstreatment.globalid,
    mostrecentgwsstreatment.rel_globalid,
        CASE
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Treatments Complete (Both Foliage and Soil)'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NULL THEN 'Foliage Treatment Complete, Awaiting Soil Treatment'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NULL AND mostrecentgwsstreatment.missed_treatment IS NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Soil Treatment Complete, Awaiting Foliage Treatment'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Complete)'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Missed Foliage Treatment (Soil Treatment Complete)'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Foliage AND Soil Treatment'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NULL THEN 'Missed Foliage Treatment (Soil Treatment Not Yet Attempted)'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Not Yet Attempted)'::text
            WHEN mostrecentgwsstreatment.fy_approval::text = 'Yes'::text AND mostrecentgwsstreatment.by_approval::text = 'No'::text AND mostrecentgwsstreatment.consent_to_spray::text = 'Refused Treatment'::text THEN 'Partial Refusal - FY Approved, Refused treatment for BY'::text
            WHEN mostrecentgwsstreatment.fy_approval::text = 'No'::text AND mostrecentgwsstreatment.by_approval::text = 'Yes'::text AND mostrecentgwsstreatment.consent_to_spray::text = 'Refused Treatment'::text THEN 'Partial Refusal - BY Approved, Refused treatment for FY'::text
            WHEN mostrecentgwsstreatment.consent_to_spray::text = 'Refused Treatment'::text THEN 'Treatment Refused'::text
            WHEN mostrecentgwsstreatment.consent_to_spray::text = 'Consent Received'::text THEN 'Treatement Consent Received'::text
            ELSE 'Advanced Treatment Notice'::text
        END AS treatment_status
   FROM gwss_tracking
     JOIN ( SELECT gwss_treatment.objectid,
            gwss_treatment.infested_adjacent,
            gwss_treatment.infested_pdr,
            gwss_treatment.knock_talk_date,
            gwss_treatment.knock_talk_attempts,
            gwss_treatment.renter_leasee,
            gwss_treatment.property_manager,
            gwss_treatment.phone,
            gwss_treatment.email,
            gwss_treatment.contact_made,
            gwss_treatment.consent_to_spray,
            gwss_treatment.info_left,
            gwss_treatment.fy_approval,
            gwss_treatment.by_approval,
            gwss_treatment.preferred_date,
            gwss_treatment.preferred_time,
            gwss_treatment.planned_date,
            gwss_treatment.planned_time,
            gwss_treatment.neighbors_for_notification,
            gwss_treatment.host_size,
            gwss_treatment.comments,
            gwss_treatment.response_assigned_to,
            gwss_treatment.notified,
            gwss_treatment.neighbors_notified,
            gwss_treatment.missed_treatment,
            gwss_treatment.treatment_inspector,
            gwss_treatment.treatment_date,
            gwss_treatment.notice_color,
            gwss_treatment.soil_treatment_date,
            gwss_treatment.soil_missed_treatment,
            gwss_treatment.created_user,
            gwss_treatment.created_date,
            gwss_treatment.last_edited_user,
            gwss_treatment.last_edited_date,
            gwss_treatment.globalid,
            gwss_treatment.rel_globalid
           FROM gwss_treatment
             JOIN ( SELECT max(gwss_treatment_1.created_date) AS mostrecent_createddate,
                    gwss_treatment_1.rel_globalid
                   FROM gwss_treatment gwss_treatment_1
                  GROUP BY gwss_treatment_1.rel_globalid) mostrecenttreatment ON gwss_treatment.rel_globalid::text = mostrecenttreatment.rel_globalid::text AND gwss_treatment.created_date = mostrecenttreatment.mostrecent_createddate) mostrecentgwsstreatment ON gwss_tracking.globalid::text = mostrecentgwsstreatment.rel_globalid::text;
```

---

### v_gwss_parcels_related_quarter_mile_buffer

**Purpose:** Links parcels that were tagged for inspection (via the GP tool) back to the specific GWSS finding that caused the tagging, and to the quarter-mile survey area buffer polygon. Provides a combined display field (`gwss_finding_causing_survey`) showing PDR#, life stage, and date collected. Used for analysis of survey progress per buffer.

```sql
SELECT gwssbuffers.survey_area_name AS quarter_mile_buffer_name,
    concat('PDR#: ', gwsstrackinghistory_wparcelinfo.pdr_number, '  |  Life Stage: ', gwsstrackinghistory_wparcelinfo.life_stage, '  |  Found on: ', gwsstrackinghistory_wparcelinfo.date_collected) AS gwss_finding_causing_survey,
    gwsstrackinghistory_wparcelinfo.pdr_number,
    gwsstrackinghistory_wparcelinfo.life_stage,
    gwsstrackinghistory_wparcelinfo.date_collected,
    gwsstrackinghistory_wparcelinfo.sitenum,
    gwsstrackinghistory_wparcelinfo.siteroad,
    gwsstrackinghistory_wparcelinfo.parceladdress,
    gwsstrackinghistory_wparcelinfo.sitecity,
    gwsstrackinghistory_wparcelinfo.zip,
    gwsstrackinghistory_wparcelinfo.gwss_action,
    gwsstrackinghistory_wparcelinfo.globalid AS parcel_globalid,
    replace(replace(concat(gwsstrackinghistory_wparcelinfo.globalid, ' - ', gwssbuffers.globalid), '{'::text, ''::text), '}'::text, ''::text) AS combined_buffer_parcel_globals,
    gwsstrackinghistory_wparcelinfo.shape
   FROM ( SELECT gwssfindings.date_collected,
            gwssfindings.pdr_number,
            gwssfindings.life_stage,
            gwsstrackinghistory.gwss_findings_rel_globalid,
            gwsstrackinghistory.parcelid,
            gwssparcels.objectid,
            gwssparcels.shape,
            gwssparcels.globalid,
            gwssparcels.parcelid,
            gwssparcels.data_notes,
            gwssparcels.asmtnum,
            gwssparcels.rollyear,
            gwssparcels.acres,
            gwssparcels.lotsize,
            gwssparcels.usecode,
            gwssparcels.desusecode,
            gwssparcels.subdiv,
            gwssparcels.pdqclass,
            gwssparcels.pdyrblt,
            gwssparcels.status,
            gwssparcels.landval,
            gwssparcels.improveval,
            gwssparcels.trevineval,
            gwssparcels.fixedeqval,
            gwssparcels.perpropval,
            gwssparcels.penaltyval,
            gwssparcels.situs,
            gwssparcels.sitenum,
            gwssparcels.siteroad,
            gwssparcels.parceladdress,
            gwssparcels.sitecity,
            gwssparcels.zip,
            gwssparcels.unitbldg,
            gwssparcels.williamson_act,
            gwssparcels.pcl_createdate,
            gwssparcels.pcl_inactdate,
            gwssparcels.gwss_action,
            gwssparcels.gwss_comments,
            gwssparcels.created_user,
            gwssparcels.created_date,
            gwssparcels.last_edited_user,
            gwssparcels.last_edited_date
           FROM gwss_tracking_history gwsstrackinghistory
             JOIN gwss_tracking gwssparcels ON gwsstrackinghistory.parcelid::text = gwssparcels.parcelid::text
             JOIN gwss_findings gwssfindings ON gwsstrackinghistory.gwss_findings_rel_globalid::text = gwssfindings.globalid::text) gwsstrackinghistory_wparcelinfo(date_collected, pdr_number, life_stage, gwss_findings_rel_globalid, parcelid, objectid, shape, globalid, parcelid_1, data_notes, asmtnum, rollyear, acres, lotsize, usecode, desusecode, subdiv, pdqclass, pdyrblt, status, landval, improveval, trevineval, fixedeqval, perpropval, penaltyval, situs, sitenum, siteroad, parceladdress, sitecity, zip, unitbldg, williamson_act, pcl_createdate, pcl_inactdate, gwss_action, gwss_comments, created_user, created_date, last_edited_user, last_edited_date)
     JOIN gwss_survey_areas gwssbuffers ON gwsstrackinghistory_wparcelinfo.gwss_findings_rel_globalid::text = gwssbuffers.gwss_findings_rel_global::text;
```

---

### v_gwss_recent_surveys_six_weeks

**Purpose:** Returns the most recent survey per parcel where the `survey_date` falls within the past 42 days (six weeks), joined to the parent parcel with the `survey_result` CASE expression. This view powers the Field Maps layer that highlights parcels recently surveyed, providing field crews with a current-activity indicator.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    surveyslastsixweeks.objectid,
    surveyslastsixweeks.biologists,
    surveyslastsixweeks.survey_date,
    surveyslastsixweeks.survey_refusal,
    surveyslastsixweeks.fy_inspected,
    surveyslastsixweeks.by_inspected,
    surveyslastsixweeks.infested,
    surveyslastsixweeks.adjacent,
    surveyslastsixweeks.information_left,
    surveyslastsixweeks.sample_collected,
    surveyslastsixweeks.comments,
    surveyslastsixweeks.revisit_biologists,
    surveyslastsixweeks.revisit_date,
    surveyslastsixweeks.rel_globalid,
    surveyslastsixweeks.globalid,
    surveyslastsixweeks.created_user,
    surveyslastsixweeks.created_date,
    surveyslastsixweeks.last_edited_user,
    surveyslastsixweeks.last_edited_date,
        CASE
            WHEN surveyslastsixweeks.infested::text = 'Yes'::text THEN 'Infested'::text
            WHEN surveyslastsixweeks.adjacent::text = 'Yes'::text THEN 'Adjacent'::text
            WHEN surveyslastsixweeks.fy_inspected::text = 'Yes'::text AND surveyslastsixweeks.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN surveyslastsixweeks.fy_inspected::text = 'Yes'::text OR surveyslastsixweeks.by_inspected::text = 'Yes'::text THEN 'Clear'::text
            WHEN (surveyslastsixweeks.fy_inspected IS NULL OR surveyslastsixweeks.fy_inspected::text = 'No'::text) AND (surveyslastsixweeks.by_inspected IS NULL OR surveyslastsixweeks.by_inspected::text = 'No'::text) AND surveyslastsixweeks.survey_refusal::text = 'No'::text THEN 'Survey Incomplete'::text
            WHEN surveyslastsixweeks.survey_refusal::text = 'Yes'::text THEN 'Refused Survey'::text
            ELSE NULL::text
        END AS survey_result
   FROM gwss_tracking
     JOIN ( SELECT gwss_surveys.objectid,
            gwss_surveys.biologists,
            gwss_surveys.survey_date,
            gwss_surveys.survey_refusal,
            gwss_surveys.fy_inspected,
            gwss_surveys.by_inspected,
            gwss_surveys.infested,
            gwss_surveys.adjacent,
            gwss_surveys.information_left,
            gwss_surveys.sample_collected,
            gwss_surveys.comments,
            gwss_surveys.revisit_biologists,
            gwss_surveys.revisit_date,
            gwss_surveys.rel_globalid,
            gwss_surveys.globalid,
            gwss_surveys.created_user,
            gwss_surveys.created_date,
            gwss_surveys.last_edited_user,
            gwss_surveys.last_edited_date
           FROM gwss_surveys
             JOIN ( SELECT max(gwss_surveys_1.created_date) AS mostrecent_createddate,
                    gwss_surveys_1.rel_globalid
                   FROM gwss_surveys gwss_surveys_1
                  GROUP BY gwss_surveys_1.rel_globalid) mostrecenttreatment ON gwss_surveys.rel_globalid::text = mostrecenttreatment.rel_globalid::text AND gwss_surveys.created_date = mostrecenttreatment.mostrecent_createddate
          WHERE gwss_surveys.survey_date > (CURRENT_DATE - '42 days'::interval)) surveyslastsixweeks ON gwss_tracking.globalid::text = surveyslastsixweeks.rel_globalid::text;
```

---

### v_gwss_treatments_past_year

**Purpose:** Returns the most recent treatment record per parcel where either the foliage or soil treatment date falls within the past year, joined to the parent parcel with the full `treatment_status` CASE expression. Used to track recent treatment activity and as a data source for reporting on the past year's treatment program.

```sql
SELECT gwss_tracking.shape,
    gwss_tracking.parcelid,
    gwss_tracking.sitenum,
    gwss_tracking.siteroad,
    gwss_tracking.parceladdress,
    gwss_tracking.sitecity,
    gwss_tracking.zip,
    mostrecentgwsstreatment.objectid,
    mostrecentgwsstreatment.infested_adjacent,
    mostrecentgwsstreatment.infested_pdr,
    mostrecentgwsstreatment.knock_talk_date,
    mostrecentgwsstreatment.knock_talk_attempts,
    mostrecentgwsstreatment.renter_leasee,
    mostrecentgwsstreatment.property_manager,
    mostrecentgwsstreatment.phone,
    mostrecentgwsstreatment.email,
    mostrecentgwsstreatment.contact_made,
    mostrecentgwsstreatment.consent_to_spray,
    mostrecentgwsstreatment.info_left,
    mostrecentgwsstreatment.fy_approval,
    mostrecentgwsstreatment.by_approval,
    mostrecentgwsstreatment.preferred_date,
    mostrecentgwsstreatment.preferred_time,
    mostrecentgwsstreatment.planned_date,
    mostrecentgwsstreatment.planned_time,
    mostrecentgwsstreatment.neighbors_for_notification,
    mostrecentgwsstreatment.host_size,
    mostrecentgwsstreatment.comments,
    mostrecentgwsstreatment.response_assigned_to,
    mostrecentgwsstreatment.notified,
    mostrecentgwsstreatment.neighbors_notified,
    mostrecentgwsstreatment.missed_treatment,
    mostrecentgwsstreatment.treatment_inspector,
    mostrecentgwsstreatment.treatment_date,
    mostrecentgwsstreatment.notice_color,
    mostrecentgwsstreatment.soil_treatment_date,
    mostrecentgwsstreatment.soil_missed_treatment,
    mostrecentgwsstreatment.created_user,
    mostrecentgwsstreatment.created_date,
    mostrecentgwsstreatment.last_edited_user,
    mostrecentgwsstreatment.last_edited_date,
    mostrecentgwsstreatment.globalid,
    mostrecentgwsstreatment.rel_globalid,
        CASE
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Treatments Complete (Both Foliage and Soil)'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NULL THEN 'Foliage Treatment Complete, Awaiting Soil Treatment'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NULL AND mostrecentgwsstreatment.missed_treatment IS NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Soil Treatment Complete, Awaiting Foliage Treatment'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NOT NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Complete)'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NOT NULL THEN 'Missed Foliage Treatment (Soil Treatment Complete)'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Foliage AND Soil Treatment'::text
            WHEN mostrecentgwsstreatment.missed_treatment IS NOT NULL AND mostrecentgwsstreatment.soil_treatment_date IS NULL THEN 'Missed Foliage Treatment (Soil Treatment Not Yet Attempted)'::text
            WHEN mostrecentgwsstreatment.treatment_date IS NULL AND mostrecentgwsstreatment.soil_missed_treatment IS NOT NULL THEN 'Missed Soil Treatment (Foliage Treatment Not Yet Attempted)'::text
            WHEN mostrecentgwsstreatment.consent_to_spray::text = 'Refused Treatment'::text THEN 'Treatment Refused'::text
            WHEN mostrecentgwsstreatment.consent_to_spray::text = 'Consent Received'::text THEN 'Treatement Consent Received'::text
            ELSE 'Advanced Treatment Notice'::text
        END AS treatment_status
   FROM gwss_tracking
     JOIN ( SELECT gwss_treatment.objectid,
            gwss_treatment.infested_adjacent,
            gwss_treatment.infested_pdr,
            gwss_treatment.knock_talk_date,
            gwss_treatment.knock_talk_attempts,
            gwss_treatment.renter_leasee,
            gwss_treatment.property_manager,
            gwss_treatment.phone,
            gwss_treatment.email,
            gwss_treatment.contact_made,
            gwss_treatment.consent_to_spray,
            gwss_treatment.info_left,
            gwss_treatment.fy_approval,
            gwss_treatment.by_approval,
            gwss_treatment.preferred_date,
            gwss_treatment.preferred_time,
            gwss_treatment.planned_date,
            gwss_treatment.planned_time,
            gwss_treatment.neighbors_for_notification,
            gwss_treatment.host_size,
            gwss_treatment.comments,
            gwss_treatment.response_assigned_to,
            gwss_treatment.notified,
            gwss_treatment.neighbors_notified,
            gwss_treatment.missed_treatment,
            gwss_treatment.treatment_inspector,
            gwss_treatment.treatment_date,
            gwss_treatment.notice_color,
            gwss_treatment.soil_treatment_date,
            gwss_treatment.soil_missed_treatment,
            gwss_treatment.created_user,
            gwss_treatment.created_date,
            gwss_treatment.last_edited_user,
            gwss_treatment.last_edited_date,
            gwss_treatment.globalid,
            gwss_treatment.rel_globalid
           FROM gwss_treatment
             JOIN ( SELECT max(gwss_treatment_1.created_date) AS mostrecent_createddate,
                    gwss_treatment_1.rel_globalid
                   FROM gwss_treatment gwss_treatment_1
                  GROUP BY gwss_treatment_1.rel_globalid) mostrecenttreatment ON gwss_treatment.rel_globalid::text = mostrecenttreatment.rel_globalid::text AND gwss_treatment.created_date = mostrecenttreatment.mostrecent_createddate) mostrecentgwsstreatment ON gwss_tracking.globalid::text = mostrecentgwsstreatment.rel_globalid::text
  WHERE mostrecentgwsstreatment.soil_treatment_date > (CURRENT_DATE - '1 year'::interval) OR mostrecentgwsstreatment.treatment_date > (CURRENT_DATE - '1 year'::interval);
```

## 9. Attribute Rules

None documented. Status and symbology are driven by the database views in Section 8, not by attribute rules on the feature classes.

## 10. Geoprocessing / Automation

### GWSSQuarterMileAnalysis_ParcelInspectionTag

**Service:** `https://solanocountygis.com/server/rest/services/GWSS/GWSSQuarterMileAnalysis_ParcelInspectionTag/GPServer`

**Portal item:** `https://solanocountygis.com/portal/home/item.html?id=d5f45b5be35d42e387bea50c62ba2636`

**Source location:** The Python script behind this tool is stored in the ArcGIS Server folder:
```text
\\gis.solanocountygis.local\GWSS\GWSSQuarterMileAnalysis_ParcelInspectionTag.GPServer\extracted\p20\solano
```

**Functionality:**

The tool is invoked from the Geoprocessing widget in the GWSS Tracking and Management web app. Its purpose is to automate the regulatory response to a lab-confirmed GWSS finding by identifying all parcels within a quarter mile and flagging them for inspection.

The process flow is:

1. **Select findings requiring survey** — the tool identifies GWSS Findings records where `quarter_mile_survey_required` is set to `Yes` (i.e., a lab-confirmed finding has been flagged by office staff as needing a quarter-mile response).
2. **Generate quarter-mile buffer** — for each qualifying finding, a quarter-mile (1,320-foot) buffer polygon is created and written to the `GWSS Survey Areas` feature class, linked back to the finding via `gwss_findings_rel_global`.
3. **Select intersecting parcels** — all parcels in the `GWSS Tracking` feature class that intersect the buffer polygon are selected.
4. **Tag parcels for inspection** — the `gwss_action` field on each intersecting parcel is updated to `"Requires Inspection"`.
5. **Write tracking history** — for each parcel tagged, a record is written to the `GWSS Tracking History` table linking the parcel (by `parcelid`) to the finding (by `gwss_findings_rel_globalid`). This history record provides an audit trail of which finding caused which parcel to be flagged.

After the tool runs, the map refreshes and the newly flagged parcels appear in red on the parcel layer. Office staff can subsequently add or remove the "Requires Inspection" status on individual parcels manually if needed.

## 11. Map / App Layer Definitions

Parcel symbology is driven by the `gwss_action` / `status`, `survey_result`, and `treatment_status` fields, which are computed by the database views and exposed through the map service layers.

### Survey Result Symbology (v_gwss_most_recent_survey_per_parcel, v_gwss_all_surveys)

The `survey_result` field is a derived CASE expression. Possible values and their intended map symbols:

| survey_result value | Meaning |
|---|---|
| `Infested` | GWSS found during survey — parcel is infested |
| `Adjacent` | Property adjacent to an infested parcel |
| `Clear` | Front yard and/or back yard inspected; no GWSS found |
| `Survey Incomplete` | Survey record exists but neither yard was inspected and no refusal recorded |
| `Refused Survey` | Property owner/occupant refused the survey |
| *(null)* | No survey record; parcel has not yet been surveyed |

### Treatment Status Symbology (v_gwss_most_recent_treatment_per_parcel, v_gwss_all_treatments)

The `treatment_status` field is a derived CASE expression. Possible values:

| treatment_status value | Meaning |
|---|---|
| `Treatments Complete (Both Foliage and Soil)` | Both foliage and soil pesticide treatments have been applied |
| `Foliage Treatment Complete, Awaiting Soil Treatment` | Foliage applied; soil not yet attempted or missed |
| `Soil Treatment Complete, Awaiting Foliage Treatment` | Soil applied; foliage not yet attempted or missed |
| `Missed Soil Treatment (Foliage Treatment Complete)` | Foliage done; soil treatment was missed |
| `Missed Foliage Treatment (Soil Treatment Complete)` | Soil done; foliage treatment was missed |
| `Missed Foliage AND Soil Treatment` | Both treatment types were missed |
| `Missed Foliage Treatment (Soil Treatment Not Yet Attempted)` | Foliage missed; soil not yet started |
| `Missed Soil Treatment (Foliage Treatment Not Yet Attempted)` | Soil missed; foliage not yet started |
| `Partial Refusal - FY Approved, Refused treatment for BY` | Front yard approved, back yard refused — parcel symbolized purple |
| `Partial Refusal - BY Approved, Refused treatment for FY` | Back yard approved, front yard refused — parcel symbolized purple |
| `Treatment Refused` | Owner refused all treatment — parcel symbolized red |
| `Treatement Consent Received` | Consent obtained; treatment not yet applied (note: "Treatement" is a typo in the original SQL, preserved here for accuracy) |
| `Advanced Treatment Notice` | Default/fallback: outreach has begun but consent stage not yet completed |

**Partial Refusal (purple):** The two Partial Refusal cases were added to the solution on 3/16/22 at the request of the program team. They arise when a property owner consents to treat one yard but refuses the other. The `CASE` expression in both `v_gwss_most_recent_treatment_per_parcel` and `v_gwss_all_treatments` evaluates `fy_approval`, `by_approval`, and `consent_to_spray` together to produce the correct partial-refusal category. Parcels matching either partial-refusal case are symbolized in purple in both the GWSS Supporting Analysis Layers services (web app and Field Maps).

### GWSS Action / Parcel Status (gwss_tracking.gwss_action)

The `gwss_action` field on the `gwss_tracking` (parcels) feature class drives the primary parcel color when no survey or treatment record exists:

| gwss_action value | Meaning | Symbol |
|---|---|---|
| `Requires Inspection` | Parcel is within the quarter-mile buffer and must be surveyed | Red |
| *(blank / null)* | Parcel is not currently flagged for inspection | Default/no fill |

### Reference Layers

- **GWSS Trap Grids:** Labels on by default in Field Maps; off by default in the web app. Layer is non-selectable (popup disabled). Grid numbers correlate with the naming convention used for trap IDs and are used as a verification reference.
- **Quarantine Boundary (Quar Boundary):** Reference layer showing the regulated GWSS quarantine area. Referenced service (converted from hosted on 4/8/22).
- **Biological Control:** Point layer recording beneficial-insect release locations. Off by default in the web app; positioned at the top of the layer list in both maps. Editing must be enabled by toggling the layer on before adding points.
