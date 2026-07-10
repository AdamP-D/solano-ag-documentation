# Weeds & Invasives Treatment Application — Requirements Document

*Solano County Agricultural Program · As-built documentation of current functionality*

---

## 1. Background & Purpose

Solano County's Agriculture Department is responsible for treating weeds and invasive plant species that threaten local agriculture and natural areas. Managing that work requires tracking each treatment over time — from the first observation of a plant, through obtaining the property owner's approval, applying one or more treatments, and finally verifying that the treatment succeeded. Doing this consistently across many properties and staff members is difficult with paper forms or spreadsheets.

The Weeds & Invasives Treatment Application was built for Solano County by KCI, working with the County's DOIT–GIS team and the Agriculture Department, in late 2022 through mid-2023. It was initially designed to track treatments of the Tree of Heaven (ToH) invasive species, but the team determined it could support all of the department's weed and invasive-species treatment efforts and expanded it accordingly. Its purpose is to give the department a single, shared, map-based system that follows the entire treatment lifecycle in one record per treatment, collected in the field with Survey123 and managed from a desktop web application.

---

## 2. Stakeholders

| Name / Role | Relationship to System |
|-------------|------------------------|
| Solano County Agriculture Department | System Owner / Program Owner |
| Matthew Carl | Primary Point of Contact |
| Agriculture Department field staff | Primary Users (field data collection and treatment) |
| Agriculture Department office staff | Primary Users (tracking and editing) |
| Agriculture Department leadership | View-only stakeholders |
| Solano County DOIT–GIS | System owner (GIS platform); maintainer |
| KCI (Andrew Blowers, author of documentation) | Developer / Maintainer |

---

## 3. Current Functional Requirements (As-Built)

The following requirements describe what the system does today.

| # | Requirement |
|---|-------------|
| FR-01 | The system shall display treatment tracking points, treatment records, treatment areas, and parcels on an interactive map. |
| FR-02 | The system shall provide a mobile map (Esri Field Maps) for locating parcels and launching the treatment form. |
| FR-03 | The system shall provide a Survey123 form for recording treatments in the field and on the desktop. |
| FR-04 | The system shall launch the Survey123 form from a parcel pop-up and pass the parcel's owner and address attributes into the form. |
| FR-05 | The system shall record a treatment as a single record maintained through its full lifecycle (Initial Observation, Seeking Approval, Initial Treatment, Follow-Up Treatment, Post-Verification Revisit, Complete). |
| FR-06 | The system shall allow users to record the plant species using a standardized scientific/common name list, with an option to enter other names. |
| FR-07 | The system shall record, for each stage, the date/time, observer(s), result, and comments. |
| FR-08 | The system shall record owner (assessee) and tenant approval status for a treatment. |
| FR-09 | The system shall allow users to retrieve and edit previously submitted treatment records through the Survey123 Inbox. |
| FR-10 | The system shall allow users to search treatment records by observer, observation date, scientific name, assessee, and treatment stage. |
| FR-11 | The system shall provide a desktop web application for tracking, editing, and reviewing treatments. |
| FR-12 | The system shall allow users to create and edit WI Treatment Tracking points, including observation confirmation, approval status, readiness, stage, and key dates. |
| FR-13 | The system shall default new tracking points to "Ready to Treat = No" so that they remain visible on the map. |
| FR-14 | The system shall allow users to adjust the location of treatment points and reshape treatment areas in the web application. |
| FR-15 | The system shall disable attribute editing of Survey123-sourced points and areas in the web application to prevent conflicts with the Survey123 record. |
| FR-16 | The system shall allow users to add, view, and delete photo and file attachments on treatment records. |
| FR-17 | The system shall organize file attachments by treatment stage. |
| FR-18 | The system shall support drawing a treatment area polygon associated with a treatment record. |
| FR-19 | The system shall provide search, select, edit, legend, layer list, basemap gallery, and bookmarks tools in the web application. |
| FR-20 | The system shall support offline field use through archiving/sync on the data. |
| FR-21 | The system shall track who created and last edited each record, and when. |

---

## 4. Current Data Requirements

| Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
|-----------------|---------|----------------------------|---------------|---------------|
| WI Treatment Tracking (wi_treatment_tracking) | Track treatment progress and approvals | Observation Confirmed, Assessee/Tenant Approval Received, Treatment Stage, Ready to Treat, Follow Up / Post Verification / Complete dates, Comment | Field & office staff | Drives tracking and map status |
| WI Treatment Points (wi_treatmentpoints) | Survey123 treatment records | Assessee & site info, Scientific/Common Name, per-stage date/observer/result/comment fields, location | Field staff (via Survey123) | The main treatment record through its lifecycle |
| WI Treatment Areas (wi_r_treatment_areas) | Treatment extent polygons | Related record ID | Field staff (via the form) | Shows the area treated |
| WI Treatment Files (wi_r_files) | File attachments by stage | Treatment Stage, related record ID | Field & office staff | Stores supporting documents/photos per stage |
| Parcels REGIS | Authoritative parcel data | Parcel ID, assessee, address | GIS (reference) | Used to select a property and launch the form |

All treatment records support photo and file attachments, and track who created and last edited each record.

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Change/edit tracking not implemented.** Automatic tracking of edits (for example, when a treatment's stage changes) was not part of the original project scope. | Progress changes are not automatically surfaced as a change history. | Documented as a future option: database views could look for stage changes and feed them into the web application. |
| 2 | **Survey123 Outbox is all-or-nothing.** When forms are saved to the Outbox, sending one submits all of them. | A user may unintentionally submit incomplete records. | Save in-progress records as **Drafts** rather than the Outbox; submit only when complete. |
| 3 | **Attachments not visible in the Inbox.** Photo and file attachments do not appear when a record is reopened from the Survey123 Inbox after submission. | Users cannot review previously added attachments within the form. | View/manage attachments through the web application instead. |
| 4 | **Survey123 point/area attributes locked in the web app.** To protect the Survey123 record, attribute editing of treatment points and areas is disabled in the web application (only geometry can be edited). | Attribute corrections must be made through Survey123, not the web app. | Edit attributes via the Survey123 Inbox. |
| 5 | **Some edits cannot be undone.** Individual vertex edits and attachment deletions in the web application cannot be reversed. | Accidental changes may require manual correction. | Work carefully; the Edit widget's Undo reverts all changes in a session, not individual vertex edits. |
| 6 | **One-record-per-treatment discipline required.** The workflow depends on users editing the single existing record via the Inbox rather than launching Survey123 directly and creating duplicates. | Launching the form directly can create duplicate/incomplete records. | Always launch from the parcel hyperlink for new treatments; use the Inbox to update existing ones. |

---

*This document describes the system as built. It intentionally does not include future enhancements or prioritization.*
