# Plant, Pest & Other Inspections — Knowledge Base

*Solano County Agricultural Program · Prepared for end users and stakeholders*

---

## 1. App Overview

The Solano County Agriculture Department conducts a variety of plant and pest inspections and surveys that do not fall under the GWSS trap monitoring or plant quarantine programs. These include pest/disease surveys — such as SOD (Sudden Oak Death), SLF, BW, AWB, and ESFY — and an "other" category for **Resident Complaint / CDFA / County Follow Up** visits. The Plant, Pest & Other Inspections solution is the set of tools used to record and manage these inspections. It is part of the County's broader "Ag Inspection Tool," sharing a portal group with Incoming Shipment Tracking.

Each inspection is tied to a location on the map in one of two ways: to an existing **Address Point** (the County's address dataset) when the site has an address, or to an **Inspection Point** the inspector drops on the map when there is no address. The inspection details themselves — type, status, date, inspector, comments, and any photos or files — are stored as a **related record** attached to that point. The intent is one inspection record per visit, updated until the inspection is complete.

The solution has two connected components that share the same live data: a **Field Map** configured for the Esri Field Maps mobile app, and a **Web AppBuilder application** for desktop use. The point of contact for this solution is **Matthew Carl** (Agriculture Department).

---

## 2. User Roles

| Role | Description | Primary Activities in the App |
|------|-------------|-------------------------------|
| Field Inspector | Staff conducting field inspections | Open Field Maps, navigate to a site, create or update inspection records |
| Office Staff | Staff managing records | Review, filter, and export records in the web app |
| GIS Administrator / Maintainer | County GIS team | Maintain the feature service, web map, and web app |

---

## 3. Key Workflows

### Recording an Inspection (Field Maps)

1. Open the **Plant Pest Other Insp - Field Map** in the Esri Field Maps app on a mobile device.
2. Locate the site: use your device location or search by **Full Address** / **APN** (Address Points) or by the address on an existing Inspection Point.
3. Choose the point the inspection belongs to:
   - If the site has an address, select the existing **Address Point**.
   - If there's no address, add an **Inspection Point (PPO)** at the location (drop the point with the crosshair, set the location, and submit).
4. With the point selected, open its **Plant Pest and Other Inspections** related table (tap the link icon or scroll to the related table) and tap **Add** to create a new inspection record.
5. Enter the inspection details (Inspection Type defaults to "Plant Pest & Other Inspection"), and attach photos or files with **Take Photo** / **Attach**.
6. Submit. The record is immediately visible to office staff in the web app.

*[Screenshot placeholder: Field Maps showing a point selected with its related Plant Pest and Other Inspections record open.]*

### Reviewing and Editing Records in the Web App

1. Open the **Plant Pest Other Insp Web App**.
2. Use the **Search** widget (place, address, APN, or Inspection Point) to find a site, or the **Query** widget to run a predefined search by Inspection Type or address.
3. Click a point to open its pop-up, then open the **Plant Pest and Other Inspections** related record to view details and attachments.
4. Use the **Edit** widget to create or edit points and related records and to add/remove attachments. Edits save automatically.

> **Note:** In the Edit widget, deleting a feature, related record, or attachment happens immediately and **cannot be undone**.

*[Screenshot placeholder: Web app Edit widget with a related inspection record open.]*

---

## 4. Data Collected

| Field / Group | What It Captures |
|---------------|-----------------|
| Location | Either an existing **Address Point** (County address dataset) or an **Inspection Point** dropped where there is no address |
| Inspection Type | The category of inspection/survey (defaults to "Plant Pest & Other Inspection"; survey types include SOD, SLF, BW, AWB, ESFY, and Resident Complaint/CDFA/County Follow Up) |
| Inspection Status | The current status of the inspection |
| Inspection Date | The date the inspection was performed |
| Inspector | Name of the inspector who conducted the visit |
| Address | The site address (typed on an Inspection Point, or carried from the Address Point) |
| Comments | Notes or observations recorded during the inspection |
| Attachments | Photos or files attached to the inspection record |

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Deletes cannot be undone.** In the web app Edit widget, deleting a point, related inspection record, or attachment happens immediately with no confirmation and no undo. | Accidental data loss. | Delete carefully; confirm the correct record is selected first. |
| 2 | **Address Points are a copy from SC_Prime.** The address dataset is sourced from the County's SC_Prime database and drifts from the authoritative source over time. New address points added in the field can use placeholder values for required fields. | Address data may be out of date or need reconciliation. | Review field-added address points against SC_Prime in the office; keep required fields accurate. |
| 3 | **Schema documentation is incomplete.** The PPS feature service and views map service were offline when the JSON export was run, so domain values, full field schema, and view definitions were not captured. | The Technical Reference schema, domain, and view sections are partly inferred and need verification. | Re-export when the services are running, and retrieve view SQL from pgAdmin; update the Technical Reference. |
| 4 | **No dashboard.** The solution has no PPO-specific ArcGIS Dashboard component. | Managers have no at-a-glance summary of inspection counts or status breakdown. | Use the web app attribute table and Query widget for summary views. |
