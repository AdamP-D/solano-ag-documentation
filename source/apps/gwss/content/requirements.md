# GWSS Data Collection and Management Solution — Requirements Document

*Solano County Agricultural Program · As-built documentation of current functionality*

---

## 1. Background & Purpose

The Glassy-Winged Sharpshooter (GWSS) is an insect that threatens Solano County agriculture because it spreads Pierce's Disease, which is harmful to grapevines and other crops. Responding to a confirmed GWSS find requires the County to survey every nearby property within a quarter mile, obtain consent from owners, and apply pesticide treatments — all while keeping accurate records of what was done where. Before this solution, the program managed that work with spreadsheets (such as the "Confirmed GWSS Counts" and "Pesticide & Survey Log" files) and by visually marking survey areas in Google Maps, which was time-consuming and difficult to keep current across a team.

The GWSS Data Collection and Management Solution was built for Solano County by KCI, working with the County's DOIT–GIS team, in late 2021 and early 2022. Its purpose is to give the agricultural program a single, shared, map-based system for the full GWSS response: documenting traps, recording and lab-confirming findings, automatically identifying the properties within a quarter mile that must be surveyed, capturing survey results in the field, and tracking pesticide treatments and consent. It serves the County's ongoing GWSS monitoring and response program, with field crews collecting data on mobile devices and office staff and managers coordinating and reviewing the work from a desktop application.

---

## 2. Stakeholders

| Name / Role | Relationship to System |
|-------------|------------------------|
| Solano County Agricultural Commissioner's Office | System Owner / Program Owner |
| Matthew Carl | Primary Point of Contact; map owner; primary data contributor |
| David Jagdeo, Matthew Perryman | Office staff / Creators (data management) |
| Addison Meinke, Catherine Blazy, Tony Avina, Samantha Benavente | Field workers / Biologists (data collection) |
| Ed King, Pricilla Yeaney | Management / View-only stakeholders |
| Solano County DOIT–GIS | System owner (GIS platform); maintainer |
| KCI (David Thompson, author of technical documentation) | Developer / Maintainer |

---

## 3. Current Functional Requirements (As-Built)

The following requirements describe what the system does today.

| # | Requirement |
|---|-------------|
| FR-01 | The system shall display GWSS traps, findings, parcels, and survey areas on an interactive map. |
| FR-02 | The system shall provide a mobile map (Esri Field Maps) for collecting and editing data in the field. |
| FR-03 | The system shall provide a desktop web application for managing findings, running analysis, and reviewing progress. |
| FR-04 | The system shall allow authorized users to add and edit trap locations, including route, address, trap ID, and location description. |
| FR-05 | The system shall allow authorized users to record GWSS findings, including date collected, life stage, host material, and whether the insect was found in a trap. |
| FR-06 | The system shall allow users to record that a sample was sent to the lab and to enter the state-assigned PDR number. |
| FR-07 | The system shall allow users to mark a finding as lab-confirmed. |
| FR-08 | The system shall allow users to flag a finding as requiring a quarter-mile survey. |
| FR-09 | The system shall provide an on-demand analysis tool that creates a quarter-mile buffer around flagged findings and tags all intersecting parcels as requiring inspection. |
| FR-10 | The system shall record the relationship between each finding and the parcels it caused to be flagged (tracking history). |
| FR-11 | The system shall allow users to manually add or remove the "requires inspection" status on individual parcels. |
| FR-12 | The system shall allow field users to record property surveys, including who surveyed, the date, front-yard and back-yard inspection results, infested/adjacent status, refusals, and whether information was left. |
| FR-13 | The system shall allow users to record pesticide treatment activity, including knock-and-talk outreach, contact information, and consent. |
| FR-14 | The system shall capture separate front-yard and back-yard treatment approvals, supporting partial consent. |
| FR-15 | The system shall record both foliage and soil treatment dates, as well as missed-treatment dates. |
| FR-16 | The system shall allow multiple survey, finding, and treatment records to be related to a single parcel over time. |
| FR-17 | The system shall symbolize parcels by their current survey and treatment status, including a distinct symbol for partial refusals. |
| FR-18 | The system shall indicate, on the field map, parcels surveyed within the last six weeks. |
| FR-19 | The system shall allow users to export lists of properties (e.g., parcels requiring inspection, most recent survey per parcel, all surveys). |
| FR-20 | The system shall support attachments (such as photos) on findings, surveys, treatments, and traps. |
| FR-21 | The system shall track who created and last edited each record, and when. |
| FR-22 | The system shall provide view-only access for management users and editing access for field and office users. |
| FR-23 | The system shall display reference layers, including trap grids (labeled, non-selectable, off by default) and the GWSS quarantine boundary. |
| FR-24 | The system shall allow authorized users to record beneficial-insect (biological control) release locations. |

---

## 4. Current Data Requirements

| Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
|-----------------|---------|----------------------------|---------------|---------------|
| GWSS Traps | Track trap locations | Route, Address, Trap ID, Location description | Field workers | Manage trapping program; verify against trap grid labels |
| GWSS Findings | Record where the insect was found | Date Collected, Life Stage, Found in Trap, Host Material, Sent to Lab, PDR #, Lab Confirmed, 1/4 Mile Survey Required | Field & office staff | Trigger the survey response; track confirmed finds |
| GWSS Tracking (Parcels) | Track required action per property | Parcel ID, Address, GWSS Action, Infested/Adjacent, Comments, parcel attributes | Office staff / analysis tool | Drives map color and the crew to-do list |
| GWSS Survey Areas | Quarter-mile buffer polygons | Survey Area Name, related finding ID | Analysis tool (automated) | Defines the area to be surveyed |
| GWSS Tracking History | Link findings to flagged parcels | Related finding ID, Parcel ID | Analysis tool (automated) | Records why each parcel was flagged |
| GWSS Surveys | Store property survey results | Biologists, Survey Date, Survey Refusal, Front/Back Yard Inspected, Infested, Adjacent, Information Left, Sample Collected, Revisit details | Field workers | Track survey progress and results per property |
| GWSS Treatment | Store outreach and treatment data | Knock & Talk dates, Contact Made, Consent to Spray, Front/Back Yard Approval, Preferred/Planned/Treatment Date, Soil Treatment Date, Notice Color | Field & office staff | Track consent and treatment; drive treatment-status symbology |
| GWSS Biological Control | Record beneficial-insect releases | Date, Address, Comment | Field & office staff | Document biological control efforts |
| GWSS Trap Grids | Reference grid for trap naming | Grid label | GIS (reference) | Verify trap numbering |
| Quar Boundary | GWSS quarantine boundary | Boundary geometry | GIS (reference) | Show the regulated area |
| Database Views (8) | Combine related records for display/analysis | (derived) | System (automated) | Show holistic and most-recent-per-parcel data and power symbology |

All editing datasets track who created and last edited each record, and support attachments such as photos.

---

## 5. Known Issues & Gaps

| # | Issue / Gap | Impact | Workaround (if any) |
|---|-------------|--------|----------------------|
| 1 | **Domain updates do not cascade to services.** When a list of allowed values (a domain) is changed in the database, the change does not appear in the map services on republish. | New picklist values may not show up for users until corrected. | All GWSS services that share the dataset must be stopped and republished together for the new values to take effect. Documented in the Esri bug write-up. |
| 2 | **Relationship IDs can change on republish.** Republishing a service reordered the internal relationship IDs, which broke the ability to add Survey and Treatment records from the desktop app's Smart Editor. | Desktop editing of surveys/treatments stopped working (mobile still worked) until fixed. | The app's underlying configuration was edited to point at the corrected relationship IDs. Restored in April 2022. |
| 3 | **Biological Control layer symbology limitation.** The desired look (a semi-transparent circle roughly four houses wide) cannot be preserved by an editable feature service. | The release points do not display exactly as originally specified. | To both edit the points and show the intended symbol, the layer would need to appear twice (an editable feature service plus a display-only map service). To avoid confusing users, only the editable feature service was kept. |
| 4 | **Offline field use is limited.** Working offline in Field Maps is technically complex; each layer must be specially configured, and the setup process is error-prone. | Crews in areas with poor cell coverage may experience reduced functionality. | The program accepts occasional coverage drops rather than maintaining a full offline configuration. |
| 5 | **Map ownership coordination required.** The web map must remain owned by the County's program contact so the team can make symbology tweaks; it must be transferred back after any GIS team edits. | If ownership is not returned, the program team cannot make their own map adjustments. | Process note: always transfer the map back to the program contact after making changes. |

---

*This document describes the system as built. It intentionally does not include future enhancements or prioritization.*
