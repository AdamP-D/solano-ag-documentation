---
name: solano-ag-documentation
description: Design spec for comprehensive knowledge base and requirements documents for Solano County agricultural web apps
metadata:
  type: project
---

# Solano County Ag Web Apps — Documentation Design Spec

**Date:** 2026-06-29  
**Audience:** End users and stakeholders  
**Output format:** PDF (one per app per deliverable type)

---

## Overview

Create two documentation deliverables for each of five Solano County agricultural web applications:

1. **Knowledge Base / Wiki** — comprehensive, accessible reference document explaining what each app is, how it works, and what data it manages
2. **Requirements Document** — captures current functional state (as-built) and known issues/gaps

Ten documents total: one Knowledge Base + one Requirements Document per app.

---

## Applications in Scope

1. GWSS (Glassy-Winged Sharpshooter)
2. Weeds & Invasives Treatment Application
3. Incoming Shipment Tracking
4. PQ Inspection Tracking
5. Plant, Pest, & Other

---

## Source Materials

For each app:
- Existing documentation (Word/PDF files in each app's folder)
- Extracted JSON from ArcGIS apps (Experience Builder, Web AppBuilder, or Survey123 — varies per app; **extraction not yet complete**)
- Feature class / database schema documentation
- Any raw data files (e.g., spreadsheets, CSVs)

Note: JSON extraction is a prerequisite step that must be completed before documentation can be finalized.

---

## Knowledge Base Document Structure

Each app gets one Knowledge Base PDF with the following sections:

1. **App Overview** — What the app does, the problem it solves, and business context (written for a stakeholder who has never seen it)
2. **User Roles** — Who uses the app and their relationship to it (field inspector, supervisor, admin, etc.)
3. **Key Workflows** — Step-by-step walkthroughs of main use cases in plain language, with screenshots where available
4. **Data Captured** — What information the app collects and stores, explained in non-technical terms (field names translated to plain language)
5. **Map & Layers Overview** — What the map shows, what each layer represents, and how to interpret symbology
6. **System Integrations** — How the app connects to other systems (ArcGIS Online, databases, other county systems)
7. **Glossary** — Key terms defined for non-technical readers (pest names, inspection types, ag terminology)

---

## Requirements Document Structure

Each app gets one Requirements PDF with the following sections:

1. **Background & Purpose** — Why the app was built, what it replaced, and its role in the county's ag program
2. **Stakeholders** — Who owns, uses, and is affected by the system (with names/roles where known)
3. **Current Functional Requirements (As-Built)** — What the app does today, written as numbered requirement statements
4. **Current Data Requirements** — What data the app captures, stores, and reports on (sourced from schema and JSON)
5. **Known Issues & Gaps** — Current pain points, workarounds in use, or functionality intended but not delivered

---

## Production Workflow

### Phase 1 — Pilot: GWSS

GWSS is selected as the pilot app because it has the most complete existing source material (technical docs, user guidance, schema, development specs, data files from Matthew Carl).

Steps:
1. Extract JSON from GWSS app(s) in ArcGIS Online
2. Review all existing GWSS source material
3. Write GWSS Knowledge Base PDF
4. Write GWSS Requirements PDF
5. User reviews both documents and provides feedback
6. Finalize document templates based on pilot results

### Phase 2 — Remaining Four Apps

Apply the templates and workflow established in Phase 1 to each remaining app:
- Weeds & Invasives Treatment Application
- Incoming Shipment Tracking
- PQ Inspection Tracking
- Plant, Pest, & Other

Each follows the same cycle: extract → review source material → write → approve.

---

## Approach Selected

**App-by-App (Phased / Pilot-First)** — chosen over template-first or source-complete approaches because GWSS's rich existing documentation makes it the ideal pilot, and the templates can be validated before committing to all five apps.
