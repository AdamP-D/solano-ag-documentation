# PQ Inspection Tracking — Knowledge Base

*Solano County Agricultural Program · Prepared for end users and stakeholders*

---

## 1. App Overview

Solano County's Agriculture Department is required to inspect agricultural fields that are under a plant quarantine (PQ) — a regulatory designation that restricts the movement of specific commodities out of an area to prevent the spread of pests or diseases. The PQ Inspection Tracking solution is the set of tools inspectors and staff use to manage those inspections from start to finish.

Each inspection record is tied to a specific **field boundary** — a polygon drawn on the map to mark the geographic extent of the site being inspected. From there, inspectors record all the details of the inspection: the commodity, the applicant, the grower, the PQ number, the quarantine status, and the results of each inspection walk. A PQ inspection can require up to **three separate walk-throughs** of the field, and the system tracks the date, inspectors, billable time, and miles for each one.

The solution has three connected parts that share the same live data: a **Survey123 form** for data collection in the field, a **desktop web application** for office staff to review and manage records, and a **dashboard** that gives managers a summary view of the current inspection workload.

---

## 2. User Roles

| Role | Description | Primary Activities in the App |
|------|-------------|-------------------------------|
| Field Inspector | Staff who conduct the field inspections | Use the Survey123 form to create and update inspection records; draw field boundaries on the map |
| Office Staff | Staff who manage records and coordinate inspections | Review and edit records in the web app; track quarantine and inspection status |
| Manager / Supervisor | Staff overseeing the program | Use the dashboard to monitor inspection workloads and status counts |
| GIS Administrator / Maintainer | County GIS team | Maintain the feature service, Survey123 form, web app, and dashboard |

---

## 3. Key Workflows

### Creating a New PQ Inspection Record

New records always start from a **field boundary** on the map — not from a blank form. This keeps every inspection tied to a specific field.

1. In **Field Maps** (or the Dashboard / Web App), find the field: search by address or navigate the map. If the field boundary doesn't exist yet, add it with the Edit tool in the Web App or Field Maps.
2. Tap/click the **field boundary** polygon to open its pop-up.
3. Select the **Launch Survey123** hyperlink in the pop-up. This opens the Survey123 form and starts a new record for that field.
4. Enter the inspection details:
   - **PQ Number**, **Site ID**, **Commodity**, **Variety**, **Acreage**
   - **Applicant**, **Grower**, **Contact Name**, **Phone Number**, **Pesticide Permit Number** (selecting the Applicant auto-fills Address, Contact Name & Phone; selecting the Grower auto-fills the Pesticide Permit Number)
   - **PLSS location** (Section, Township, Range) for rural fields
   - **Approximate Plant Date** and **Harvest Date**
   - **Quarantine Status** (None, Hold, or Quarantine)
   - **Inspection Status** (Standby or Priority at intake)
5. For any incoming shipment that triggered the PQ, the **Incoming GID** is carried over automatically from the launch link.
6. Submit the form (page 5 of 5). Choose **Send Now** if online, or **Save in Outbox / Drafts** if offline.

*[Screenshot placeholder: Field Maps field-boundary pop-up with the Launch Survey123 hyperlink.]*

### Completing a Walk (Survey123 Inbox — First, Second, or Third Walk)

Existing records are updated through the Survey123 **Inbox** (not by starting a new form), so all of a field's values stay consolidated in one record. Open the **PQ Inspection Tracking** form in Survey123, open the **Inbox**, refresh, and search for the record (by PQ Number, Applicant, Grower, etc.). Then fill in the walk section:

1. Enter the **Walk Date** and **Lead Inspector**.
2. Enter **Total Number of Inspectors** and **Number of Vehicles**.
3. Record the **Inspection Start Time** and **End Time** — the form calculates **Total Inspection Time**.
4. Enter **Drive Time**, **Additional Time**, and **Miles Per Vehicle** — the form calculates **Total Billable Time** and **Total Billable Miles**.
5. Enter the **PDR Number** for this walk and any **Notes**.
6. Update the **Inspection Status** to reflect the walk completed (1st Walk Complete, 2nd Walk Complete, or 3rd Walk Complete).
7. If the field has been fully cleared, set **Inspection Status** to **Complete** and **Quarantine Status** to **None**; if a quarantine or hold is being placed or lifted, update **Quarantine Status** accordingly.

> **Tip:** Refresh the Inbox before going offline so you're editing the latest values and don't overwrite another user's edits. Records marked **Complete** drop out of the Inbox.

*[Screenshot placeholder: Survey123 form — First Walk section showing time and mileage fields.]*

### Reviewing Records in the Web App

1. Open the **PQ Inspection Tracking - Web App**.
2. Use the map or search tools to locate a field boundary.
3. Click a field to open its pop-up and view the linked inspection record details.
4. Use the attribute table to view, filter, sort, and export records.

*[Screenshot placeholder: web app with a field boundary selected and inspection pop-up visible.]*

### Using the Dashboard

The **PQ Inspection Tracking - Dashboard** gives managers a summary view of inspection status counts and records. Use it to see how many inspections are at each status (Standby, Priority, In Progress, Complete) and to identify fields under Hold or Quarantine.

*[Screenshot placeholder: dashboard overview showing status summary counts.]*

---

## 4. Data Collected

| Field / Group | What It Captures |
|---------------|-----------------|
| Field Boundary | Polygon drawn on the map marking the inspection site |
| PQ Number | The regulatory plant quarantine number |
| Site ID | Internal site identifier |
| Quarantine Status | Current regulatory status: None, Hold, or Quarantine |
| Inspection Status | Progress through the inspection lifecycle |
| Commodity / Variety | The crop or commodity being inspected |
| Acreage | Size of the field |
| Applicant / Grower | Who applied for the inspection and who is growing the crop |
| Contact Name & Phone | Point of contact at the site |
| Pesticide Permit Number | Permit number if pesticides are involved |
| PLSS Section / Township / Range | Legal land description for rural fields |
| Approx. Plant & Harvest Dates | Estimated growing season timing |
| Estimated Walk Dates | Projected dates for the 1st and 2nd walk-throughs |
| Per Walk (×3): Date, Lead Inspector, # Inspectors, Start/End Time, Inspection Time, Drive Time, Additional Time, Billable Time, # Vehicles, Miles per Vehicle, Total Billable Miles, PDR Number, Notes | Full time and mileage record for each inspection walk — used for cost recovery |
| Incoming GID | Link to a related Incoming Shipment Tracking record, if the PQ was triggered by a shipment |
| Attachments | Photos or files attached to the inspection record |

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Field boundary is separate from the inspection record.** The polygon (Field Boundaries layer) and the record (pq_inspection_tracking table) are linked only by a Global ID stored in the table — not by a formal registered relationship. | Pop-ups and related record queries depend on the `fieldboundary_guid` field being set correctly at intake. An orphaned inspection record (no linked boundary) will not display on the map. | Ensure field boundary is drawn before submitting the Survey123 form; verify the GUID is populated. |
| 2 | **No automated status progression.** Unlike IST, the Inspection Status field is set manually by the inspector — there is no attribute rule that auto-advances the status when a walk date is entered. | Inspectors must remember to update the Inspection Status field at each walk. | Reinforce through training; the Survey123 form can use relevant/hidden logic to prompt status updates. |
| 3 | **PLSS coordinates only.** Rural agricultural fields are identified by PLSS description (Section, Township, Range) rather than a parcel ID or street address. | Records cannot be automatically linked to the County's parcel/address system. | Use the field boundary polygon as the spatial anchor; the PLSS fields serve as the written location description. |
