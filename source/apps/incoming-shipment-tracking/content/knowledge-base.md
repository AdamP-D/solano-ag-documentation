# Incoming Shipment Tracking — Knowledge Base

*Solano County Agricultural Program · Prepared for end users and stakeholders*

---

## 1. App Overview

Solano County's Agriculture Department inspects incoming shipments of plants and agricultural goods to keep pests and diseases from entering the county. The Incoming Shipment Tracking (IST) solution is the set of map-based tools staff use to manage that work — from the moment the department is notified that a shipment is coming, through its arrival and inspection, to the final result. It replaces informal tracking with a single, shared system so office staff, field inspectors, and managers can all see what shipments are expected, what needs inspection today, and what has been completed.

Each shipment is recorded against the property (parcel) it is associated with, and the system automatically works out the shipment's status from the dates that staff enter. The solution has several connected parts that share the same live data: a **desktop web application** for office staff to create and manage records, a **mobile map** (used in Esri Field Maps) for inspectors in the field, and **dashboards** (a web version for the office and a mobile version for the field) that give managers and inspectors a clear, at-a-glance view of the day's workload. The solution was originally built in late 2022 through mid-2023 and reworked in early 2024 to better fit the department's office and field workflows.

---

## 2. User Roles

| Role | Description | Primary Activities in the App |
|------|-------------|-------------------------------|
| Office Staff / Inspector | Staff who enter and manage shipment records and coordinate the day's work | Create and edit IST records on parcels, add attachments, review and export records, use the dashboard to dispatch inspections |
| Field Inspector | Staff who inspect shipments on-site | Open a parcel in Field Maps (often from the mobile dashboard), add or update the IST record, attach photos |
| Manager / Supervisor | Staff overseeing daily operations | Use the dashboards to see counts of incoming, action-required, and completed shipments and assign work |
| GIS Administrator / Maintainer | County GIS team and the original developer | Maintain the services, views, dashboards, and the automated status rules |

*Point of contact for the program: the Agriculture Department's designated lead.*

---

## 3. Key Workflows

### Creating a New Shipment Record (Office / Web App)

1. Open the **Incoming Shipment Tracking** web application.
2. Use the **Search** bar to find a parcel by Parcel ID, address, or invoice number — or zoom to it on the map.
3. Click the parcel to open its pop-up, then under **Related tables** choose **Incoming Shipment Tracking**.
4. Click the **…** menu and select **Edit**, then the **+** button to create a new record.
5. Enter the shipment details (inspection type, invoice number, shipper, notified date, etc.). The **Status**, **IST ID**, **Parcel ID**, and **Address** fill in automatically.
6. Attach any files, then click **Close** — records save automatically.

*[Screenshot placeholder: web app parcel pop-up with the "Incoming Shipment Tracking" related records.]*

### Updating a Shipment Through Its Lifecycle

As staff enter dates, the shipment's status updates itself:

1. Enter **Notified of Shipment** → status becomes **Incoming Shipment** (the parcel appears yellow).
2. Enter **Arrived** → status becomes **Requires Inspection** (the parcel appears orange).
3. If the shipment is partially released or put on hold → status becomes **Reinspection Needed – On Hold**.
4. Enter **Completed** and choose a **Result** → status becomes **Complete** (with the result, e.g., "Complete – Inspected and Released"; the parcel appears blue for records completed today).

*[Screenshot placeholder: an IST record showing the date fields that drive status.]*

### Working in the Field (Field Maps)

1. From the **mobile dashboard**, tap the hyperlink for a parcel — Field Maps opens and searches for that Parcel ID. (You can also open Field Maps directly and search.)
2. Select the parcel under **PARCELS (ADD/EDIT IST RECORDS)**.
3. Under **Related**, open **Incoming Shipment Tracking**, then **Add** a new record or select an existing one to **Edit**.
4. Add attachments with **Take Photo** or **Attach**, populate the attributes, and **Submit**.

*[Screenshot placeholder: Field Maps parcel with the related Incoming Shipment Tracking records.]*

### Using the Dashboards

1. Open the **web dashboard** (office) or **mobile dashboard** (field).
2. Review the **Inspector View** list, which groups parcels by action status (Action Needed, Incoming Shipments, Completed Today) to help assign work.
3. Select a parcel to see its related shipment records and zoom the map to it.
4. Use the indicator widgets to see counts of Incoming Shipments, Action Required, and Completed Today.

*[Screenshot placeholder: web dashboard with Inspector View list, record details, and indicators.]*

### Creating a Placeholder Parcel

1. If a shipment's parcel does not exist, open the **Edit** widget and choose the **Parcels REGIS** template.
2. Draw the parcel polygon and enter placeholder Parcel ID, address, and city.
3. Save, then add the shipment record as above. (Parcel shapes cannot be reshaped after creation, to protect existing boundaries.)

*[Screenshot placeholder: Edit widget with the Parcels REGIS template.]*

---

## 4. Data Captured

Each shipment is one record in the Incoming Shipment Tracking table, related to a parcel. Field names below use the labels shown in the app.

### Shipment Record (Incoming Shipment Tracking)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Status | The shipment's current stage | Calculated automatically from the dates; drives map color and dashboards |
| Inspection Type | The kind of inspection (e.g., GWSS, Spongy Moth, Spotted Lanternfly, Seed 008, Truck – Plant, Other) | Categorizes the work |
| Invoice Number | The shipment's invoice number | Identifies the shipment |
| 008 Notice Number | The 008 notice number, when applicable | Regulatory reference |
| Shipper | Who sent the shipment | Records the source |
| Inspector Initials | The inspector handling it | Identifies who is responsible |
| Notified of Shipment | Date the department was notified | Starts the record as an incoming shipment |
| Arrived | Date the shipment arrived | Moves the record to "requires inspection" |
| Partial Release / On Hold | Dates for a partial release or hold | Moves the record to "reinspection needed – on hold" |
| Completed | Date the inspection was completed | Moves the record to "complete" |
| Result | The outcome (Inspected and Released, Reconditioned and Released, Forwarded to Other Agency, Rejected/Returned/Destroyed, Released by Phone) | Records the final disposition |
| Comments | Free-text notes | Captures context |
| IST ID | An automatically generated identifier | Uniquely labels each record |

### Parcel Information (Parcels REGIS)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Parcel ID | The property's parcel number | Ties the shipment to a location |
| Parcel Address / Site City | The property's address | Identifies where the shipment is |
| Common Name | A friendly name for the site (e.g., a business name) | Makes sites easier to recognize |

Shipment records support photo and file **attachments**, and the system records who created and last edited each record.

---

## 5. Map & Layers Overview

The map and its layers let staff view shipments by status and by time period. Because each shipment is shown using its related parcel's shape, several records can stack on the same parcel. Colors indicate status: **yellow** for incoming (notified) shipments, **orange** for shipments that require inspection, and **blue** for records completed today.

| Layer / Group | What It Shows | Notes |
|---------------|---------------|-------|
| Inspector View | One entry per parcel, grouped by action status, with counts | Powers the dashboard's dispatch list |
| Status group | Separate layers for Incoming Shipments, Requires Inspection, Reinspection Needed – On Hold, and Complete | Records shown on their related parcel |
| All Records | Every IST record | On related parcel geometry |
| Tracking By Period group | Today's Records; Completed This Month; Completed Current/Previous Fiscal Year; Completed Current/Previous Calendar Year | Dynamic, time-based views |
| Parcels REGIS | The properties shipments are tied to | Copy of the County parcels for this app |
| GWSS Trap Grids | Reference trap grid | Shared reference layer |
| County Boundary | The Solano County boundary | Reference |

The layers under Inspector View and Tracking By Period are **dynamic** — they update automatically as records change and as time passes (for example, "Today's Records" always reflects the current day).

*[Screenshot placeholder: web app layer list showing the layer groups.]*

---

## 6. System Integrations

The solution runs on the County's ArcGIS Enterprise platform (Portal and Server) at solanocountygis.com. All IST data lives in the County's enterprise **PostgreSQL "agdept" database** and is shared as **referenced services**.

Key pieces work together automatically:

- **Parcels REGIS** (a copy of the County parcel data kept in the Agriculture Department database) is related to the Incoming Shipment Tracking table, so each shipment is tied to a property.
- **Automated rules** fill in each record's Parcel ID, address, common name, and IST ID from the related parcel, and **calculate the Status** from the dates and result the user enters — so status is always consistent without manual selection.
- **Database views** aggregate the records (for example, one summary per parcel, or records by time period) to power the maps and dashboards.
- **Esri Field Maps** provides the mobile experience, and a hyperlink in the mobile dashboard launches Field Maps directly to the right parcel.
- **The dashboards** (built in ArcGIS Dashboards) read the same live data to show counts and lists for daily operations.

---

## 7. Glossary

| Term | Definition |
|------|------------|
| 008 Notice | A regulatory notice number associated with certain shipments |
| Action Status | The category the dashboard uses to group parcels (Action Needed, Incoming Shipments, Completed Today) |
| Attribute Rule | An automated rule that fills in or calculates a field (e.g., Status, IST ID) |
| Dashboard | A summary screen showing counts and lists of shipments (web and mobile versions) |
| Field Maps | The Esri mobile app inspectors use in the field |
| Incoming Shipment | A shipment the department has been notified about but that has not yet arrived |
| Inspector View | The summary layer/list that shows one entry per parcel with its action status and counts |
| IST / IST Record | An Incoming Shipment Tracking record |
| IST ID | The automatically generated identifier for a record |
| Inspection Type | The category of inspection (GWSS, Spongy Moth, Spotted Lanternfly, Seed 008, etc.) |
| Parcel / Parcel ID | A property and its unique identifying number |
| Parcels REGIS | The County's parcel layer (a copy is used in this app) |
| Reinspection Needed – On Hold | A shipment that was partially released or placed on hold |
| Result | The final disposition of an inspected shipment |
| Status | The shipment's current stage, calculated automatically |
| Web AppBuilder | The Esri tool used to build the desktop web application |
