# GWSS Data Collection and Management Solution — Knowledge Base

*Solano County Agricultural Program · Prepared for end users and stakeholders*

---

## 1. App Overview

The Glassy-Winged Sharpshooter (GWSS) is an insect that poses a serious threat to Solano County agriculture. It spreads Pierce's Disease, which can kill grapevines and damage other crops, so quickly finding, surveying, and treating infested areas is a priority for the County's agricultural program. The GWSS Data Collection and Management Solution is the set of map-based tools the County uses to do exactly that: it keeps track of where traps are placed, where the insect has been found and lab-confirmed, which nearby properties need to be surveyed, and what pesticide treatments have been carried out.

The solution replaces the spreadsheets and manual map-marking that the program relied on previously. It has two main parts that share the same live data: a **mobile map** (used in the field on phones and tablets through Esri Field Maps) for collecting information on-site, and a **desktop web application** (the GWSS Tracking and Management app) for managing findings, running the quarter-mile survey analysis, and watching overall progress. Field crews, office staff, and managers all work from the same up-to-date picture, which makes it easier to coordinate the County's response to each confirmed find. The solution was built for Solano County in late 2021 and early 2022 and is maintained by the County's GIS team together with the program's primary contact.

---

## 2. User Roles

| Role | Description | Primary Activities in the App |
|------|-------------|-------------------------------|
| Field Worker / Biologist | Staff who visit properties to place traps, survey for the insect, and apply treatments | Place and document traps; complete property surveys; record findings; log treatment visits — all from the mobile map in Field Maps |
| Office Staff / Creator | Program coordinators who manage the data from the desktop | Record and confirm findings, enter lab/PDR numbers, run the quarter-mile survey analysis, tag or untag parcels, review and export lists |
| Manager / Viewer | Upper management and decision-makers | View the map and overall progress; they do not create or edit records |
| GIS Administrator / Maintainer | County GIS team and the original developer | Maintain the maps, services, symbology, and the quarter-mile analysis tool; publish updates |

*The County's map owner makes day-to-day symbology and small map adjustments; larger changes are coordinated with the GIS team.*

---

## 3. Key Workflows

### Placing and Documenting a Trap

1. In the field, open the GWSS map in **Esri Field Maps**.
2. Tap the **Add** ( + ) button and choose to add a **Trap** location.
3. Tap the spot on the map where the trap is placed.
4. Fill in the trap details — Route, Address, Trap ID, and a location description.
5. Submit the record. When a trap is removed, its location can be deleted to show it is no longer there.

*[Screenshot placeholder: Field Maps "Add Trap" form with the location pin on the map.]*

### Recording a GWSS Finding and Sending a Sample to the Lab

1. From the property being inspected (in Field Maps or the web app), select the parcel and add a related **GWSS Finding** point where the insect was found.
2. Record the finding details — Date Collected, Life Stage, whether it was Found in a Trap, Location, and Host Material. Add a photo if helpful.
3. When a sample is sent to the state lab, edit the finding to enter the **Sent to Lab** date.
4. When the lab responds, enter the **PDR #** (the case number the state assigns).

*[Screenshot placeholder: GWSS Finding record form showing Life Stage and PDR # fields.]*

### Confirming a Find and Triggering the Quarter-Mile Survey

1. In the desktop web app, open the confirmed GWSS finding.
2. Set **Lab Confirmed** to "Yes" and toggle **1/4 Mile Survey Required** to "Yes" for each finding that needs a survey.
3. Run the **quarter-mile analysis tool** (the geoprocessing button in the app). The tool automatically draws a quarter-mile buffer around the finding and tags every parcel inside it as **Requires Inspection** — those parcels turn red on the map.
4. If needed, manually add or remove the "Requires Inspection" status on individual parcels.
5. Export the list of properties requiring inspection for the field crews.

*[Screenshot placeholder: web app after running the tool, showing the buffer and red "requires inspection" parcels.]*

### Performing a Field Survey

1. In Field Maps, navigate to a red **Requires Inspection** parcel. (Parcels surveyed in the last six weeks appear with hash marks.)
2. Select the parcel and add a related **Survey** record.
3. Complete the survey: Biologists, Survey Date, whether the Front Yard / Back Yard were inspected (or refused), whether the property is Infested or Adjacent, whether Information was Left, and any comments.
4. If the insect is found, also add a **GWSS Finding** point as above.
5. Once the property has been surveyed, update the parcel status to remove the "Requires Inspection" tag.

*[Screenshot placeholder: Field Maps survey form with Front/Back Yard inspected fields.]*

### Logging a Pesticide Treatment ("Knock & Talk" and Application)

1. Select the parcel and add a related **Treatment** record.
2. Record the outreach ("Knock & Talk") details — date, attempts, contact made, renter/property-manager info, and phone/email.
3. Record consent — **Consent to Spray** (Awaiting Consent / Consent Received / Refused Treatment) and separate Front Yard and Back Yard approvals.
4. Schedule and record the treatment — preferred date/time, planned date, and the actual **Treatment Date** (foliage) and **Soil Treatment Date**. Note the color of the notice left at the address (Green, Yellow, Blue, or Pink).
5. Submit the record. The parcel's color on the map updates to reflect the treatment stage.

*[Screenshot placeholder: Treatment record showing Consent to Spray and Front/Back Yard approval fields.]*

### Viewing Progress and Exporting Lists

1. Open the desktop web app to see the current status of every parcel, color-coded by survey and treatment stage.
2. Use the map layers to see which parcels still need inspection, which refused, and which are complete.
3. Export lists as needed — for example, the most recent survey per parcel, all surveys, or parcels requiring inspection.

*[Screenshot placeholder: web app map legend showing the status color-coding.]*

---

## 4. Data Captured

The solution records information in several connected datasets. Field names below use the plain-language labels shown in the app.

### Trap Information (GWSS Traps)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Route | The trap route (e.g., Red, Blue) | Organizes traps into field routes for checking |
| Address | Where the trap is located | Identifies the trap's location |
| Trap ID | The trap's identifying number | Matches a physical trap to its map record |
| Location description | Notes on the exact placement | Helps crews find the trap again |

### Finding Information (GWSS Findings)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Date Collected | When the insect was found | Establishes the timeline of the find |
| Life Stage | The insect's stage (Adult, Nymph, Eggmass, Viable/Non-Viable Eggmass, etc.) | Indicates severity and breeding activity |
| Found in Trap | Whether it came from a trap | Distinguishes trap catches from visual finds |
| Location / Host Material | Where on the property and on what plant it was found | Supports analysis of where the pest lives |
| Sent to Lab | Date a sample went to the state lab | Tracks lab submission |
| PDR # | The case number assigned by the state | Official identifier for a confirmed find |
| Lab Confirmed | Whether the lab confirmed it is GWSS | Confirmed finds trigger the survey response |
| 1/4 Mile Survey Required | Whether a quarter-mile survey is needed | Starts the buffer-and-tag analysis |

### Parcel / Property Tracking (GWSS Tracking)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Parcel ID / Address | The property's parcel number and address | Ties all activity to a specific property |
| GWSS Action | The required action (Requires Inspection; Requires Treatment — Foliage/Soil for Infested/Adjacent; Action Completed / No Action Needed) | Drives the map color and the crew's to-do list |
| Infested or Adjacent | Whether the property is infested or next to an infested one | Determines treatment type |
| Comments / Data Notes | Free-text notes | Captures context not covered by other fields |
| Parcel attributes (acres, land use, owner/site info) | Standard County parcel details | Provides property context to crews |

### Survey Information (GWSS Surveys)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Biologists / Survey Date | Who surveyed and when | Records who did the work and when |
| Survey Refusal | Whether the occupant refused the survey | Tracks access problems |
| Front Yard / Back Yard Inspected | Whether each area was inspected (Yes/No/Refused) | Shows how complete the survey was |
| Infested / Adjacent | Survey result for the property | Feeds the map status and treatment planning |
| Information Left / Sample Collected | Whether materials were left or a sample taken | Documents outreach and evidence |
| Biologists Revisited / Date Revisited | Follow-up visit details | Tracks repeat visits |

### Treatment Information (GWSS Treatment)

| Field (Plain Language) | What It Means | Why It's Collected |
|------------------------|---------------|--------------------|
| Knock & Talk Completed / Attempt Dates | Outreach contact dates | Documents the consent process |
| Contact Made / Renter or Leasee / Property Manager / Phone / Email | Who was contacted and how | Supports scheduling and notification |
| Consent to Spray | Awaiting Consent / Consent Received / Refused Treatment | Controls whether treatment can proceed |
| Front Yard / Back Yard Approval | Approval for each area | Allows partial approvals |
| Preferred / Planned / Treatment Date | When treatment is wanted, planned, and done (foliage) | Tracks the treatment schedule |
| Soil Treatment Date / Missed Treatment Dates | Soil treatment and any missed visits | Tracks both treatment types and gaps |
| Notice Color Left at Address | Green / Yellow / Blue / Pink notice | Communicates treatment stage in the field |

### Supporting Data

- **Survey Areas** — the quarter-mile buffer polygons created by the analysis tool around each confirmed finding.
- **Tracking History** — a record of which finding caused which parcels to be tagged for inspection.
- **GWSS Trap Grids** — reference grid labels used to verify trap naming.
- **Biological Control** — points marking where beneficial insects were released.
- **Quar Boundary** — the GWSS quarantine boundary.

---

## 5. Map & Layers Overview

The map is the heart of the solution. Parcels and points are color-coded so that, at a glance, anyone can see where the program stands. Layers can be turned on and off; some (like Trap Grids and Biological Control) are turned off by default to keep the map uncluttered.

| Layer Name | What It Shows | Symbology |
|------------|---------------|-----------|
| GWSS Tracking (Parcels) | Every tracked property and its required action | Red = requires inspection; other colors indicate survey/treatment status |
| GWSS Findings | Points where the insect was found | Symbolized by finding; confirmed finds drive the survey response |
| Survey Areas | Quarter-mile buffers around confirmed finds | Outlined polygons showing the area to be surveyed |
| Most Recent Survey per Parcel | The latest survey result for each property | Infested, Adjacent, Clear, Refused, or Incomplete |
| Most Recent Treatment per Parcel | The latest treatment status for each property | Color-coded by stage, including a distinct color for **Partial Refusal** (one yard approved, one refused) |
| Recent Surveys (Past Six Weeks) | Properties surveyed within six weeks | Shown with hash marks in the field map |
| GWSS Traps | Trap locations | Point symbols along routes |
| GWSS Trap Grids | Reference grid with labels | Labeled, not selectable, off by default, drawn above traps |
| Biological Control | Beneficial-insect release points | Semi-transparent points; off by default |
| Quar Boundary | The GWSS quarantine area | Boundary outline |

**Notice colors used in the field:** Pink = Advance Treatment Notice, Blue = Adjacent Property (no treatment), Green = Missed Treatment, Yellow = Completed Treatment. These match the colored notices crews leave at properties.

*[Screenshot placeholder: full map with the legend visible.]*

---

## 6. System Integrations

The solution is built on the County's ArcGIS Enterprise platform (Portal and Server) hosted at solanocountygis.com. All of the GWSS data lives in the County's enterprise **PostgreSQL** database and is shared to the platform as **referenced services** — meaning the maps read directly from the database rather than from separate hosted copies.

Several pieces work together:

- **Esri Field Maps** provides the mobile experience for field crews.
- **The GWSS Tracking and Management web application** (built with Web AppBuilder) provides the desktop experience, including the **Smart Editor** tool for entering survey and treatment records and a **geoprocessing button** for the quarter-mile analysis.
- **The quarter-mile analysis service** is an automated geoprocessing tool that buffers confirmed findings, tags the intersecting parcels as "Requires Inspection," and records the history of which finding caused which parcels to be flagged.
- **Database views** (eight in total) combine related records — for example, joining a survey to its parcel address, or showing only the most recent treatment per parcel — so the map can symbolize the data in a meaningful way.

Because survey, treatment, and finding records are related to each parcel (rather than stored on the parcel directly), crews can log multiple visits over time to the same property and the program can always see the most recent status.

---

## 7. Glossary

| Term | Definition |
|------|------------|
| Adjacent Property | A property next to an infested one, included in the treatment response as a precaution |
| Biological Control | The release of beneficial insects to help control GWSS naturally |
| Domain | A fixed list of allowed values for a field (e.g., Yes/No), used to keep data consistent |
| Field Maps | The Esri mobile app crews use on phones and tablets to collect data on-site |
| Finding | A record of where a GWSS insect was located |
| Foliage Treatment | Pesticide applied to plant leaves (distinct from soil treatment) |
| GWSS | Glassy-Winged Sharpshooter — the insect this program tracks and controls |
| Infested Property | A property where GWSS has been confirmed |
| Knock & Talk | The outreach visit to a property owner to obtain consent before treatment |
| Life Stage | The development stage of the insect (e.g., Adult, Nymph, Eggmass) |
| Parcel / Parcel ID (APN) | A property and its unique identifying number from County records |
| PDR # | Pest Damage Record number — the case identifier assigned by the state lab |
| Pierce's Disease | The plant disease spread by GWSS that threatens grapevines |
| Quarter-Mile Survey | The survey of all properties within a quarter mile of a confirmed find |
| Referenced Service | A map layer that reads directly from the County database rather than a separate copy |
| Smart Editor | The tool in the web app used to add and edit survey and treatment records |
| Soil Treatment | Pesticide applied to the soil (distinct from foliage treatment) |
| Survey Area | The quarter-mile buffer polygon created around a confirmed finding |
| Trap / Trap Grid | A device placed to catch GWSS, and the reference grid used to label trap locations |
| Web AppBuilder | The Esri tool used to build the desktop web application |
