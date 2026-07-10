# Solano Ag Documentation System — Design Spec

**Date:** 2026-07-01
**Status:** Approved (design); pending implementation plan

## Purpose

Turn the Solano County Ag documentation effort from a set of ad-hoc per-app
documents into a maintainable **central documentation repository** that KCI owns
and can regenerate, and that is easy to hand over to the client (Solano County)
as a browsable, self-contained package.

This extends the existing effort (per-app Knowledge Base + Requirements documents
for five ag web applications) with:
1. A third document type per app — a **Technical Reference** for a GIS-admin /
   developer audience.
2. A repository structure, build pipeline, and delivery format that make the
   whole body of documentation central, regenerable, and portable.

## Goals

- **Central repository:** one place holding all documentation for all five
  solutions, cleanly separated into source (authored) vs. build (generated).
- **Easy handoff:** Solano receives a self-contained, navigable static site
  (single landing page → every app → every doc type, with search) plus PDF
  exports of each document for formal records.
- **Easy to maintain:** KCI owns a Markdown source-of-truth and a one-command
  build. Factual technical content is auto-generated from the read-only ArcGIS
  JSON export, so it stays current with minimal manual effort.

## Non-Goals

- Solano staff editing the source directly (KCI maintains and re-delivers).
- A hosted/live web service or database-connected documentation (the delivered
  site is static HTML).
- Future-enhancement / prioritization sections (excluded per the original scope).

## Audiences (per document type)

| Document | Audience | Tone |
|----------|----------|------|
| Knowledge Base | End users / stakeholders | Plain language, task-oriented |
| Requirements | Stakeholders | As-built functional/data requirements |
| Technical Reference | GIS administrators / developers / maintainers | Precise, technical |

## The five applications

GWSS, Weeds & Invasives Treatment (ToH), Incoming Shipment Tracking, PQ Inspection
Tracking, Plant/Pest/Other. Knowledge Base + Requirements are complete for the
first three; Technical References are new for all five.

---

## Repository structure (`source/` + `build/` split)

```
C:\Projects\Solano\Ag\Documentation\
├── source/                         # KCI-authored source of truth
│   ├── apps/
│   │   ├── gwss/
│   │   │   ├── source-material/    # KCI originals (docx, pdf, pptx, xlsx)
│   │   │   ├── json-export/        # extract_item_json output (dated)
│   │   │   ├── content/            # authored Markdown (source of truth)
│   │   │   │   ├── knowledge-base.md
│   │   │   │   ├── requirements.md
│   │   │   │   └── technical-reference.md
│   │   │   └── notes/              # synthesis / working notes
│   │   ├── weeds-invasives/
│   │   ├── incoming-shipment-tracking/
│   │   ├── pq-inspection-tracking/
│   │   └── plant-pest-other/
│   ├── shared/                     # landing-page intro; shared services (agdept DB, GWSS Trap Grids)
│   └── templates/                  # knowledge-base, requirements, technical-reference templates
├── tooling/                        # pure-Python build pipeline (no third-party installs)
│   ├── extract_item_json.py        # read-only ArcGIS JSON extractor (canonical copy)
│   ├── generate_tech_reference.py  # JSON export -> factual tech-ref sections (Markdown)
│   ├── build_site.py               # Markdown -> navigable static site (nav + search)
│   ├── build_pdf.py                # HTML -> PDF via Edge headless
│   ├── md_to_html.py               # shared Markdown -> HTML renderer
│   └── build.py                    # orchestrator (generate -> site -> pdf)
├── build/                          # GENERATED output (regenerable); the deliverable
│   ├── site/                       # index.html hub + per-app pages + search index
│   └── pdf/                        # per-app, per-doc-type PDFs
├── docs/superpowers/               # specs & plans (project meta; not delivered)
└── README.md                       # repo overview + build/deliver instructions
```

Run with the ArcGIS Pro bundled Python:
`C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`.
`arcgis` is only needed for `extract_item_json.py`; the build scripts are pure
standard-library Python.

---

## Build pipeline

All build scripts are pure standard-library Python (no pip installs), consistent
with the existing `md_to_html.py`.

1. **`extract_item_json.py`** (already built) — read-only extraction of each app's
   portal/service JSON into `source/apps/<app>/json-export/`. KCI runs this per
   app whenever a solution changes.

2. **`generate_tech_reference.py`** (new) — reads an app's `json-export/` and emits
   the **factual** Technical Reference sections as Markdown:
   - Portal Items (title, type, id)
   - Services & Publishing (service type, referenced vs. hosted, capabilities,
     sync/archiving, time-zone config, source service URL)
   - Database Schema (per layer/table: field name, alias, type, length, nullable,
     editable, domain reference)
   - Domains (each coded-value domain, full value list, and the fields that use it)
   - Subtypes (where present)
   - Relationships (name, cardinality, origin/destination, keys)

   Output is injected into the authored `technical-reference.md` at marker
   comments (`<!-- GENERATED:schema -->` … `<!-- /GENERATED:schema -->`). The
   build replaces marker regions in place, so the file stays a single readable
   document and the factual tables are always regenerable.

3. **`md_to_html.py`** (already built, moved to `tooling/`) — shared Markdown→HTML
   renderer used by both the site and PDF steps.

4. **`build_site.py`** (new) — renders every `source/apps/*/content/*.md` into a
   self-contained static site under `build/site/`:
   - `index.html` landing page listing every app × document type
   - per-document HTML pages sharing a template with a top nav (apps) and a left
     sidebar (this app's three docs + section anchors)
   - a client-side search over a prebuilt JSON index (vanilla JS, no CDN — works
     offline and when hosted internally)

5. **`build_pdf.py`** (new) — converts each document's HTML to PDF using Microsoft
   Edge headless (`msedge --headless --print-to-pdf`), which ships with Windows —
   no install, fully automated. Output to `build/pdf/<app>/<doc-type>.pdf`.
   Fallback: open the HTML in a browser and Print → Save as PDF.

6. **`build.py`** (new) — orchestrates: generate tech-ref sections → build site →
   build PDFs, in one command.

---

## Technical Reference document (per app)

Eleven sections; **hybrid** production (auto-generated facts + hand-authored
narrative):

Auto-generated from JSON:
1. Portal Items
2. Services & Publishing
3. Database Schema
4. Domains
5. Subtypes
6. Relationships

Hand-authored from the KCI technical documentation / database:
7. Solution Architecture (components and how they connect)
8. Database View Definitions (purpose + verbatim SQL)
9. Attribute Rules (purpose + Arcade expression)
10. Geoprocessing / Automation (GP tools and their logic)
11. Map/App Layer Definitions (definition queries, dynamic-layer criteria)

The view SQL, attribute rules, and GP logic are **not** in the portal JSON; they
are carried in from the KCI technical documents and the database.

---

## Delivery & maintenance

**Delivery to Solano:** zip `build/` (site + PDFs), or Solano hosts `build/site/`
internally. The site is the browsable hub; the PDFs are formal per-document copies.

**Maintenance workflow (when a solution changes):**
1. Re-run `extract_item_json.py` for the affected app.
2. Run `build.py` — regenerates the factual tech-ref tables, the site, and the PDFs.
3. Review/adjust the hand-authored narrative sections.
4. Re-deliver `build/`.

---

## Migration of completed work

The three finished apps (GWSS, Weeds & Invasives, Incoming Shipment Tracking) and
their files move into the new `source/apps/<app>/` layout with standardized
filenames (`knowledge-base.md`, `requirements.md`). Existing source material,
JSON exports, and notes relocate to `source-material/`, `json-export/`, and
`notes/` respectively. Then Technical References are authored for all five apps.

## Cross-cutting constraints

- **No secrets:** credentials, connection strings, and passwords are never
  included in any document or generated output. (The KCI technical documents
  contain a plain-text database password — always excluded.)
- **No installs:** the pipeline uses only the ArcGIS Pro bundled Python and its
  standard library, plus Edge headless for PDF. Nothing is pip-installed into the
  ArcGIS Pro environment.
- **Read-only extraction:** `extract_item_json.py` never modifies the portal.

## Open implementation details (to resolve in the plan)

- Exact marker syntax and injection mechanism in `generate_tech_reference.py`.
- Site template look/branding (align with the doc styling already in `md_to_html.py`).
- Whether `build/` is git-ignored (regenerable) if the repo is later put under git.
- Verify Edge headless PDF output quality; confirm the Edge executable path.
