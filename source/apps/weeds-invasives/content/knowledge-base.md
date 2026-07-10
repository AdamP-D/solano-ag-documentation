# Weeds & Invasives Treatment Application — Knowledge Base

*Solano County Agricultural Program · Prepared for end users and stakeholders*

---

## 1. App Overview

Solano County's Agriculture Department treats weeds and invasive plant species — such as the Tree of Heaven — to protect local agriculture and natural areas. The Weeds & Invasives Treatment Application is the set of map-based tools staff use to document that work from the first time a plant is spotted through to the final verification that a treatment worked. It keeps a single, shared record for each treatment so that field crews and office staff always see the same up-to-date status.

The solution was originally built to track Tree of Heaven treatments, but the department and project team quickly realized it could serve all of their weed and invasive-species treatment efforts, so it was expanded to cover them all. It has three connected parts that share the same live data: a **Survey123 form** used in the field to record each treatment, a **mobile map** (used in Esri Field Maps) for finding parcels and launching that form, and a **desktop web application** for tracking progress, editing locations, and managing photos and files. The solution was developed for the County in late 2022 through mid-2023 and is maintained by the County's GIS team.

---

## 2. User Roles

| Role | Description | Primary Activities in the App |
|------|-------------|-------------------------------|
| Field Staff (Observer / Treater) | Agriculture Department staff who identify plants and apply treatments in the field | Launch the Survey123 form from a parcel, record observations and treatments through each stage, add photos and files |
| Office Staff | Staff who manage and track treatments from a desktop | Review progress, create and edit tracking points, adjust point/area locations, manage attachments in the web app |
| Manager / Stakeholder | Agriculture Department leadership | View overall treatment progress on the map and in the data |
| GIS Administrator / Maintainer | County GIS team and the original developer | Maintain the form, services, web map, and application |

*Point of contact for the program: the Agriculture Department's designated GIS lead.*

---

## 3. Key Workflows

### Starting a New Treatment Record (from the field)

1. Open the **Weeds and Invasives – Tracking and Field Map** in **Esri Field Maps**.
2. Use your location or the search to find the parcel (by address, Site/Parcel Address, Site Parcel ID, or Parcel ID).
3. Tap the parcel to open its information panel.
4. Tap the **Launch Treatment Application** link. The **Survey123** form opens and starts a new record, automatically carrying over the parcel's owner and address details.
5. Complete the form for the current stage and submit.

*[Screenshot placeholder: parcel pop-up with the "Launch Treatment Application" link.]*

### Working Through the Treatment Stages

The Survey123 form is organized into pages that follow the life of a treatment. **One record is used per treatment**, updated over time rather than creating a new form each visit:

1. **Initial Observation** — record who observed the plant, when, the species (Scientific/Common Name), and confirmation details.
2. **Seeking Approval** — record whether the property owner (assessee) and any tenant approved the treatment.
3. **Initial Treatment** — record the treatment date, who performed it, and the result.
4. **Follow-Up Treatment** — record any additional treatment visits.
5. **Post-Verification Revisit** — record the check that confirms the treatment worked.
6. **Complete** — mark the treatment finished.

To continue an existing record, open Survey123, go to the **Inbox**, tap **Refresh**, and search for the record (you can search by observer, observation date, scientific name, assessee, or treatment stage).

*[Screenshot placeholder: Survey123 form page navigation showing the treatment stages.]*

### Managing Treatments in the Web Application

1. Open the **Weeds and Invasives Treatment App – Tracking and Field Data** web application from the GIS Portal.
2. Use the **Search** widget to find a parcel or address.
3. Use the **Edit** widget to:
   - Create a **WI – Treatment Tracking** point (note: **Ready to Treat** defaults to "No" so the point stays visible on the map).
   - Adjust the location of a treatment point or reshape a treatment area (attribute editing of Survey123 points/areas is intentionally disabled to protect the Survey123 record).
   - Add, view, or delete photo and file attachments, organized by treatment stage.
4. Use the **Layer List**, **Legend**, **Basemap**, and **Bookmarks** widgets to control what the map shows.

*[Screenshot placeholder: web app Edit widget with the WI – Treatment Tracking template.]*

### Adding Photos and Files

1. Select a treatment point and open it for editing (via the Edit widget or the pop-up's Edit menu).
2. Scroll to **Attachments** and choose a file to attach a photo or document directly to the point.
3. For files organized by stage, open the **WI Treatment Files** related records, add a new record, set the **Treatment Stage**, and attach the file.

*[Screenshot placeholder: attachment section of a treatment point pop-up.]*

---

## 4. Data Captured

Field names below use the plain-language labels shown in the app.

### Treatment Tracking Points (WI Treatment Tracking)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Observation Confirmed | Whether the observation is confirmed (Yes/No/N-A/Pending/Refused) | Confirms there is a real treatment need |
| Assessee Approval Received | Whether the property owner approved treatment | Required before treating |
| Tenant Approval Received | Whether a tenant approved treatment | Captures approval when a tenant is involved |
| Treatment Stage | The current stage (Initial Observation → Complete) | Shows where each treatment stands |
| Ready to Treat | Whether the site is ready for treatment | Controls visibility/priority; defaults to "No" |
| Follow Up Date / Post Verification Date / Treatment Complete Date | Key dates in the treatment timeline | Track scheduling and completion |
| Treatment Comment | Free-text notes | Captures context |

### Survey123 Treatment Records (WI Treatment Points)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Assessee / Assessee Address / Site info | Property owner and location details | Passed automatically from the selected parcel |
| Site Parcel ID / Site/Parcel Address | The property identifier and address | Ties the treatment to a specific property |
| Scientific Name / Common Name | The plant species (from the Calflora list) | Identifies what is being treated |
| Initial Observation Date/Time, Observer(s), Confirmed | Who first observed the plant and when | Starts the treatment record |
| Approval Confirmation | Whether treatment was approved | Gate before treating |
| Initial Treatment Date/Time, Observer(s), Result | Details of the first treatment | Records the treatment and its outcome |
| Follow-Up Treatment Date/Time, Observer(s) | Details of any follow-up treatment | Tracks repeat treatments |
| Post-Verification Date/Time, Observer(s), Complete | The verification check after treatment | Confirms the treatment worked |
| Stage | The overall treatment stage | Mirrors the tracking stage |
| Latitude / Longitude / Accuracy | The recorded location | Places the treatment on the map |

### Supporting Data

- **WI Treatment Areas** — polygons drawn to show the extent of a treatment, related to a treatment record.
- **WI Treatment Files** — file and document attachments, organized by treatment stage.
- Photo and file **attachments** are supported on treatment records.

---

## 5. Map & Layers Overview

The map lets staff find parcels, launch the treatment form, and see the status of treatments. Layers can be toggled on and off with the Layer List widget, and the basemap can be changed with the Basemap Gallery.

| Layer Name | What It Shows | Symbology |
|------------|---------------|-----------|
| WI Treatment Tracking Points | Office/field tracking points for each treatment | Symbolized by treatment progress; "Ready to Treat = No" keeps new points visible |
| WI Treatment Points (Survey123) | The treatment records submitted through Survey123 | Point locations of each treatment |
| WI Treatment Areas | The area/extent of a treatment | Polygons added via the Treatment Areas question in the form |
| Parcels REGIS | The County's authoritative parcels | Used to select a property and launch the treatment form |

*[Screenshot placeholder: web application map with the legend visible.]*

---

## 6. System Integrations

The solution runs on the County's ArcGIS Enterprise platform (Portal and Server) at solanocountygis.com. All Weeds & Invasives data is stored in the County's enterprise **PostgreSQL "agdept" database** and shared to the platform as **referenced services**, so the maps read directly from the database.

The pieces work together as follows:

- **Survey123** provides the field data-entry form and its Inbox-based editing workflow.
- **The Parcels REGIS layer** is the authoritative source of parcel information; its map pop-up contains a hyperlink that launches Survey123 and passes the parcel's owner and address details into the form.
- **Esri Field Maps** hosts the web map crews use to find parcels and launch the form on mobile devices.
- **The Web AppBuilder application** provides desktop tracking, geometry editing, and attachment management.
- **Archiving (sync)** is enabled on the data to support offline work and to make future change-tracking possible.

Because the Survey123 form points to the same feature service that the maps and web app read from, a treatment recorded in the field appears immediately in the tracking tools.

---

## 7. Glossary

| Term | Definition |
|------|------------|
| Assessee | The property owner of record for a parcel |
| Attachment | A photo or file attached to a treatment record |
| Calflora | The plant-name reference used for the Scientific Name list |
| Field Maps | The Esri mobile app used to find parcels and launch the treatment form |
| Inbox (Survey123) | Where submitted forms are retrieved to be edited and resubmitted |
| Invasive Species | A non-native plant that spreads and causes harm |
| Parcel / Parcel ID | A property and its unique identifying number |
| Parcels REGIS | The County's authoritative parcel map layer |
| Post-Verification | The check after treatment to confirm it worked |
| Referenced Service | A map layer that reads directly from the County database rather than a separate copy |
| Survey123 | The Esri app used to fill out the treatment form |
| Tenant | An occupant (other than the owner) whose approval may be needed |
| Treatment Area | A polygon showing the extent of a treatment |
| Treatment Stage | The step a treatment is at (Initial Observation through Complete) |
| Tree of Heaven (ToH) | The invasive species the application was originally built to track |
| Web AppBuilder | The Esri tool used to build the desktop web application |
