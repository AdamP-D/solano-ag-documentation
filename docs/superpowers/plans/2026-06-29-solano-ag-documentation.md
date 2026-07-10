# Solano County Ag App Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce 10 PDF documents — one Knowledge Base and one Requirements Document per app — for five Solano County agricultural web applications, using existing documentation, extracted ArcGIS JSON, and schema data as source material.

**Architecture:** Phase 1 (GWSS pilot) produces both GWSS documents and finalizes the templates. Phase 2 applies those templates to the remaining four apps. Content is authored in Markdown, converted to Word (.docx) for formatting, and exported to PDF.

**Tech Stack:** Markdown (content authoring), Microsoft Word (formatting and PDF export), pandoc (optional Markdown → Word conversion), ArcGIS Online (JSON extraction — manual step).

## Global Constraints

- Audience is end users and stakeholders — no technical jargon; translate all field names and system terms to plain language
- Output format is PDF; retain Word (.docx) source files alongside each PDF
- No future enhancements or prioritization sections in any document
- Each document must be complete enough for a reader with zero prior knowledge of the app
- Knowledge Base sections: App Overview, User Roles, Key Workflows, Data Captured, Map & Layers Overview, System Integrations, Glossary
- Requirements sections: Background & Purpose, Stakeholders, Current Functional Requirements (As-Built), Current Data Requirements, Known Issues & Gaps

---

### Task 1: Set Up Directory Structure and Templates

**Files:**
- Create: `GWSS/Knowledge Base/` (directory)
- Create: `GWSS/Requirements/` (directory)
- Create: `docs/templates/knowledge-base-template.md`
- Create: `docs/templates/requirements-template.md`

- [ ] **Step 1: Create output directories for GWSS**

  Create the following folders:
  - `GWSS/Knowledge Base/`
  - `GWSS/Requirements/`

- [ ] **Step 2: Create the Knowledge Base template**

  Save to `docs/templates/knowledge-base-template.md`:

  ```markdown
  # [App Name] — Knowledge Base

  ## 1. App Overview

  [What the app does, the problem it solves, and the business context.
  Written for a stakeholder who has never seen it. 1-2 paragraphs.]

  ## 2. User Roles

  | Role | Description | Primary Activities in the App |
  |------|-------------|-------------------------------|
  | [Role] | [Who they are] | [What they do] |

  ## 3. Key Workflows

  ### [Workflow Name]

  1. [Step 1]
  2. [Step 2]
  3. [Step 3]

  *[Screenshot placeholder: description of what screenshot to insert]*

  ## 4. Data Captured

  | Field (Plain Language) | What It Means | Why It's Collected |
  |------------------------|---------------|--------------------|
  | [Field] | [Meaning] | [Purpose] |

  ## 5. Map & Layers Overview

  | Layer Name | What It Shows | Symbology |
  |------------|---------------|-----------|
  | [Layer] | [Description] | [What the colors/icons mean] |

  ## 6. System Integrations

  [How the app connects to ArcGIS Online, databases, and other county systems.]

  ## 7. Glossary

  | Term | Definition |
  |------|------------|
  | [Term] | [Plain-language definition] |
  ```

- [ ] **Step 3: Create the Requirements Document template**

  Save to `docs/templates/requirements-template.md`:

  ```markdown
  # [App Name] — Requirements Document

  ## 1. Background & Purpose

  [Why the app was built, what it replaced (manual process, spreadsheet, etc.),
  and its role in the county's ag program.]

  ## 2. Stakeholders

  | Name / Role | Relationship to System |
  |-------------|------------------------|
  | [Name/Role] | [Owner / Primary user / Data consumer / etc.] |

  ## 3. Current Functional Requirements (As-Built)

  The following requirements describe what the system does today.

  | # | Requirement |
  |---|-------------|
  | FR-01 | The system shall [verb] [object]. |
  | FR-02 | The system shall [verb] [object]. |

  ## 4. Current Data Requirements

  | Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used |
  |-----------------|---------|----------------------------|---------------|---------------|
  | [Dataset] | [Purpose] | [Fields] | [Role] | [Use] |

  ## 5. Known Issues & Gaps

  | # | Issue / Gap | Impact | Workaround (if any) |
  |---|-------------|--------|----------------------|
  | 1 | [Description] | [Who/what is affected] | [Current workaround] |
  ```

- [ ] **Step 4: Verify both templates contain all required sections per the spec**

  Confirm Knowledge Base has: App Overview, User Roles, Key Workflows, Data Captured, Map & Layers Overview, System Integrations, Glossary.
  Confirm Requirements has: Background & Purpose, Stakeholders, Current Functional Requirements, Current Data Requirements, Known Issues & Gaps.

---

### Task 2: Extract GWSS JSON from ArcGIS Online (Manual Step)

**Note: This task requires manual action in ArcGIS Online — it cannot be automated. Complete before Task 3.**

**Files:**
- Create: `GWSS/Development/JSON/` (directory for extracted files)

- [ ] **Step 1: Create the JSON output directory**

  Create folder: `GWSS/Development/JSON/`

- [ ] **Step 2: Extract Experience Builder app JSON (if applicable)**

  In ArcGIS Online:
  1. Open the GWSS Experience Builder app → Edit
  2. Click the three-dot menu (top right) → Export
  3. Save the downloaded ZIP to `GWSS/Development/JSON/`
  4. Unzip and locate `experience.json` (main config) and `datasources/` folder

- [ ] **Step 3: Extract Web AppBuilder app JSON (if applicable)**

  In ArcGIS Online:
  1. Open the GWSS Web AppBuilder app → Edit
  2. Click the app menu → Download
  3. Save the downloaded ZIP to `GWSS/Development/JSON/`
  4. Unzip and locate `config.json` in the root and `widgets/` folder

- [ ] **Step 4: Extract Survey123 form schema (if applicable)**

  Option A — Survey123 Connect:
  1. Open Survey123 Connect → Open the GWSS survey
  2. File → Export → XLSForm
  3. Save to `GWSS/Development/JSON/`

  Option B — ArcGIS Online:
  1. Navigate to the survey item → Settings → Download
  2. Save to `GWSS/Development/JSON/`

- [ ] **Step 5: Review and note key information from extracted JSON**

  From each extracted file, record:
  - App/form name and description
  - All widget or component names (what tools are available to users)
  - All layer names the app connects to
  - All field names visible in the app (popups, forms, tables)
  - Any configured workflows or automations

  Save notes to `GWSS/Development/JSON/json-review-notes.md`

---

### Task 3: Review and Catalog GWSS Source Material

**Files to read:**
- `GWSS/GWSS Technical Documentation KCI.docx`
- `GWSS/GWSS - User Guidance.pdf` or `GWSS - User Guidance.pptx`
- `GWSS/GWSS Maintenance Enhancement - Symbology Update.docx`
- `GWSS/Development/GWSS_Schema.docx`
- `GWSS/Development/GWSS Inspection - High Level Requirements.docx`
- `GWSS/Development/GWSS GP Service.docx`
- `GWSS/Development/GWSS GP Workflow Functionality.pdf`
- `GWSS/Development/GWSS Workflow.pptx`
- `GWSS/Development/JSON/json-review-notes.md`
- `GWSS/From Matthew Carl/` (scan data files for context on actual usage)

**Files to create:**
- `GWSS/Development/source-material-notes.md`

- [ ] **Step 1: Read Technical Documentation**

  Extract and note: system architecture, how the app was built, integrations with other systems, any technical constraints relevant to understanding what the app can/cannot do.

- [ ] **Step 2: Read User Guidance**

  Extract and note: who uses the app, step-by-step user workflows with any screenshots, menu/button names, how inspectors interact with the map.

- [ ] **Step 3: Read Schema document**

  Extract and note: every feature class/table name, every field name with its data type and description. For each field, write a plain-language translation (e.g., `APN` → "Assessor Parcel Number — the unique ID for each property").

- [ ] **Step 4: Read High Level Requirements document**

  Extract and note: original stated requirements. These become the baseline for the as-built functional requirements section. Note any requirements that appear to not have been implemented (these become Known Issues).

- [ ] **Step 5: Read GP Service, Workflow Functionality, and Workflow PPT**

  Extract and note: what geoprocessing steps run, what they do, when they run (on-demand vs. scheduled), what outputs they produce.

- [ ] **Step 6: Read Symbology Update document**

  Extract and note: all map layers, what each layer represents, what the symbology (colors, icons, sizes) means for each layer.

- [ ] **Step 7: Scan Matthew Carl data files**

  Review: `Trap Routes.xlsx`, `GWSS Pesticide & Survey Log.xlsx`, `Treatment Log`, `Confirmed GWSS Counts` — note what data is actually being collected in practice, any patterns, column headers (these cross-check the schema).

- [ ] **Step 8: Save synthesis notes**

  Create `GWSS/Development/source-material-notes.md` with sections mapped to each document section:
  - App Overview ← [sources]
  - User Roles ← [sources]
  - Key Workflows ← [sources]
  - Data Captured ← [sources]
  - Map & Layers ← [sources]
  - System Integrations ← [sources]
  - Glossary terms ← [sources]
  - Background & Purpose ← [sources]
  - Stakeholders ← [sources]
  - Functional Requirements ← [sources]
  - Data Requirements ← [sources]
  - Known Issues ← [sources]

---

### Task 4: Write GWSS Knowledge Base

**Files:**
- Create: `GWSS/Knowledge Base/GWSS-Knowledge-Base-draft.md`
- Create: `GWSS/Knowledge Base/GWSS - Knowledge Base.docx`
- Create: `GWSS/Knowledge Base/GWSS - Knowledge Base.pdf`

- [ ] **Step 1: Write Section 1 — App Overview**

  Source: Technical Documentation, High Level Requirements, JSON app description.
  Write 1-2 paragraphs covering:
  - What GWSS is (Glassy-Winged Sharpshooter — a pest threatening the wine grape industry)
  - What problem the app solves (tracking inspections, treatments, trap results across parcels)
  - Who manages it and why it matters to the county

  Avoid: abbreviations without definition, technical system details, ArcGIS jargon.

- [ ] **Step 2: Write Section 2 — User Roles**

  Source: User Guidance, Technical Documentation.
  Create a table with columns: Role | Description | Primary Activities in the App.
  Cover all roles found in source material (e.g., Field Inspector, Supervisor, GIS Administrator, Data Viewer).

- [ ] **Step 3: Write Section 3 — Key Workflows**

  Source: User Guidance, GP Workflow docs, Workflow PPT.
  Write a numbered walkthrough for each main workflow found (e.g., Recording a Trap Inspection, Logging a Treatment, Viewing the GWSS Map, Running a Report).
  For each step: use plain language, reference the actual button/menu names from the app, note "[Screenshot: description]" where a screenshot should be inserted.

- [ ] **Step 4: Write Section 4 — Data Captured**

  Source: Schema document, JSON field lists, Matthew Carl data files.
  Create a table with columns: Field (Plain Language) | What It Means | Why It's Collected.
  Group fields by their feature class/form (e.g., "Trap Inspection Fields", "Treatment Record Fields").
  Use plain-language field names throughout — no raw database column names.

- [ ] **Step 5: Write Section 5 — Map & Layers Overview**

  Source: Symbology Update doc, Technical Documentation, JSON config layer list.
  Create a table with columns: Layer Name | What It Shows | Symbology (what colors/icons mean).
  Add a brief introductory paragraph explaining how to navigate the map.

- [ ] **Step 6: Write Section 6 — System Integrations**

  Source: Technical Documentation, GP Service doc.
  Write 1-2 paragraphs covering: ArcGIS Online connection, any backend databases, any connections to other county systems, any automated processes (scheduled GP services, etc.).

- [ ] **Step 7: Write Section 7 — Glossary**

  Source: all of the above.
  Create an alphabetical table of all domain-specific terms: Term | Plain-Language Definition.
  Include: pest names, inspection types, parcel terminology, any ArcGIS terms that appear in user-facing workflows, regulatory/program terms.

- [ ] **Step 8: Review the complete draft**

  Read the full draft and check:
  - No unexplained acronyms or jargon
  - Each section is complete (no "[TBD]" or empty tables)
  - Tone is consistent — written for a non-technical reader
  - Workflows are accurate based on source material

- [ ] **Step 9: Convert to Word and format**

  Option A (pandoc): Run `pandoc "GWSS-Knowledge-Base-draft.md" -o "GWSS - Knowledge Base.docx"`
  Option B (manual): Copy content into a Word document and apply consistent heading styles.
  Apply: page numbers, header with app name and document type, consistent fonts and table styles.

- [ ] **Step 10: Export to PDF**

  In Word: File → Save As → PDF (or File → Export → Create PDF/XPS).
  Save as: `GWSS/Knowledge Base/GWSS - Knowledge Base.pdf`
  Verify: open PDF, confirm all sections present, all tables render correctly, no missing content.

---

### Task 5: Write GWSS Requirements Document

**Files:**
- Create: `GWSS/Requirements/GWSS-Requirements-draft.md`
- Create: `GWSS/Requirements/GWSS - Requirements Document.docx`
- Create: `GWSS/Requirements/GWSS - Requirements Document.pdf`

- [ ] **Step 1: Write Section 1 — Background & Purpose**

  Source: Technical Documentation, High Level Requirements, Maintenance Enhancement doc.
  Write 1-2 paragraphs covering:
  - Why the app was built (what problem or county program need it addresses)
  - What it replaced (manual tracking, spreadsheets, paper forms, etc.)
  - When it was built and by whom (KCI based on doc title)
  - Its current role in the county's GWSS response and monitoring program

- [ ] **Step 2: Write Section 2 — Stakeholders**

  Source: Technical Documentation, Matthew Carl data files (he appears to be a primary data contributor), High Level Requirements.
  Create a table: Name / Role | Relationship to System.
  Relationship types: System Owner, Primary User, Data Consumer, Program Manager, IT Support, Developer/Maintainer, External Stakeholder.
  Include all roles found in source material. Use "Solano County Agricultural Commissioner's Office" as the owner if no individual is named.

- [ ] **Step 3: Write Section 3 — Current Functional Requirements (As-Built)**

  Source: High Level Requirements (baseline), User Guidance (confirms implemented features), Technical Documentation, JSON config (confirms what's actually in the app).
  Write numbered requirement statements in the format: "The system shall [verb] [object]."
  Aim for 15-30 statements covering:
  - Map viewing and navigation
  - Data entry (inspections, treatments, trap results)
  - Search and filter capabilities
  - Reporting or data export
  - User access and roles
  - Any automated processes (GP services)
  Number as FR-01, FR-02, etc.

  Example statements:
  - "FR-01: The system shall display all GWSS inspection properties on an interactive map."
  - "FR-02: The system shall allow authorized users to log trap check results by parcel."
  - "FR-03: The system shall distinguish confirmed GWSS properties from unconfirmed properties using distinct map symbology."

- [ ] **Step 4: Write Section 4 — Current Data Requirements**

  Source: Schema document, JSON field lists, Matthew Carl data files.
  Create a table: Dataset / Table | Purpose | Key Fields (Plain Language) | Who Enters It | How It's Used.
  Cover every feature class and table in the schema. Group logically (e.g., Inspection Data, Treatment Data, Property Data, Trap Data).

- [ ] **Step 5: Write Section 5 — Known Issues & Gaps**

  Source: `GWSS/Esri Bug Writeup - Updating Domain in Feature Service.docx`, `GWSS Maintenance Enhancement - Symbology Update.docx`, any notes in Technical Documentation about limitations.
  Create a table: # | Issue / Gap | Impact | Workaround (if any).
  Include: the Esri bug documented in the bug writeup, any requirements from the High Level Requirements doc that don't appear to be implemented, any known usability issues from the User Guidance.

- [ ] **Step 6: Review the complete draft**

  Check:
  - Functional requirements are complete (cover all major system functionality)
  - Requirement statements are unambiguous — each could only be interpreted one way
  - No requirements reference features not found in the source material
  - Known Issues section is honest and specific (not vague)

- [ ] **Step 7: Convert to Word, format, and export to PDF**

  Same process as Task 4, Steps 9-10.
  Save as: `GWSS/Requirements/GWSS - Requirements Document.docx` and `GWSS - Requirements Document.pdf`

---

### Task 6: GWSS Review Gate (User Action Required)

- [ ] **Step 1: Present both GWSS documents to the user for review**

  Share:
  - `GWSS/Knowledge Base/GWSS - Knowledge Base.pdf`
  - `GWSS/Requirements/GWSS - Requirements Document.pdf`

- [ ] **Step 2: Collect and apply feedback**

  Gather feedback on: accuracy, completeness, tone, missing content, formatting issues.
  Apply all revisions and re-export PDFs.

- [ ] **Step 3: Update templates if structural changes are needed**

  If the review reveals that a section should be restructured, renamed, or added/removed, update:
  - `docs/templates/knowledge-base-template.md`
  - `docs/templates/requirements-template.md`
  before starting Phase 2.

---

### Task 7: Weeds & Invasives Treatment Application

**Source material:** `Weeds & Invasives Treatment Application (ToH)/`
- Available: `W&I Treatment Application - Technical Documentation.docx/.pdf`, `W&I Treatment Application - User Documentation.docx/.pdf`

- [ ] Extract JSON from ArcGIS Online (follow Task 2 process; save to `Weeds & Invasives Treatment Application (ToH)/JSON/`)
- [ ] Review all source docs and create synthesis notes
- [ ] Write Knowledge Base using template → export to `Weeds & Invasives Treatment Application (ToH)/Knowledge Base/W&I - Knowledge Base.pdf`
- [ ] Write Requirements Document using template → export to `Weeds & Invasives Treatment Application (ToH)/Requirements/W&I - Requirements Document.pdf`
- [ ] User review and revisions

---

### Task 8: Incoming Shipment Tracking

**Source material:** `Incoming Shipment Tracking/`
- Available: Technical Documentation, Testing Document, User Guide, Whiteboarding PPT, README

- [ ] Extract JSON from ArcGIS Online (save to `Incoming Shipment Tracking/JSON/`)
- [ ] Review all source docs and create synthesis notes
- [ ] Write Knowledge Base → export to `Incoming Shipment Tracking/Knowledge Base/IST - Knowledge Base.pdf`
- [ ] Write Requirements Document → export to `Incoming Shipment Tracking/Requirements/IST - Requirements Document.pdf`
- [ ] User review and revisions

---

### Task 9: PQ Inspection Tracking

**Source material:** `PQ Inspection Tracking/`
- Available: Technical Documentation, User Guide (Dev v1.0), README

- [ ] Extract JSON from ArcGIS Online (save to `PQ Inspection Tracking/JSON/`)
- [ ] Review all source docs and create synthesis notes
- [ ] Write Knowledge Base → export to `PQ Inspection Tracking/Knowledge Base/PQ - Knowledge Base.pdf`
- [ ] Write Requirements Document → export to `PQ Inspection Tracking/Requirements/PQ - Requirements Document.pdf`
- [ ] User review and revisions

---

### Task 10: Plant, Pest, & Other

**Source material:** `Plant, Pest, & Other/`
- Available: User Documentation, Technical Documentation, README

- [ ] Extract JSON from ArcGIS Online (save to `Plant, Pest, & Other/JSON/`)
- [ ] Review all source docs and create synthesis notes
- [ ] Write Knowledge Base → export to `Plant, Pest, & Other/Knowledge Base/PP&O - Knowledge Base.pdf`
- [ ] Write Requirements Document → export to `Plant, Pest, & Other/Requirements/PP&O - Requirements Document.pdf`
- [ ] User review and revisions

---

## Final Deliverables Checklist

- [ ] `GWSS/Knowledge Base/GWSS - Knowledge Base.pdf`
- [ ] `GWSS/Requirements/GWSS - Requirements Document.pdf`
- [ ] `Weeds & Invasives Treatment Application (ToH)/Knowledge Base/W&I - Knowledge Base.pdf`
- [ ] `Weeds & Invasives Treatment Application (ToH)/Requirements/W&I - Requirements Document.pdf`
- [ ] `Incoming Shipment Tracking/Knowledge Base/IST - Knowledge Base.pdf`
- [ ] `Incoming Shipment Tracking/Requirements/IST - Requirements Document.pdf`
- [ ] `PQ Inspection Tracking/Knowledge Base/PQ - Knowledge Base.pdf`
- [ ] `PQ Inspection Tracking/Requirements/PQ - Requirements Document.pdf`
- [ ] `Plant, Pest, & Other/Knowledge Base/PP&O - Knowledge Base.pdf`
- [ ] `Plant, Pest, & Other/Requirements/PP&O - Requirements Document.pdf`
