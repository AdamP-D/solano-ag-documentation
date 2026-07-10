# Solano County Ag — Solution Documentation

Central documentation repository for Solano County's agricultural GIS solutions:
**GWSS**, **Weeds & Invasives Treatment**, **Incoming Shipment Tracking**,
**PQ Inspection Tracking**, and **Plant, Pest & Other Inspections**.

Each solution has three documents — **Knowledge Base**, **Requirements**, and
**Technical Reference** — authored in Markdown and built into a self-contained
static website (with client-side search) and a set of print-ready PDFs, styled
in the Solano County design system.

Maintained by **KCI Technologies**; delivered to Solano County.

## Layout

- `source/apps/<app>/content/` — authored Markdown (the source of truth)
- `source/apps/<app>/notes/` — synthesis notes distilled from KCI vendor docs
- `source/assets/` — brand images (county seal, KCI logo) used by the build
- `tooling/` — the build pipeline (standard-library Python only)
- `tooling/tests/` — unit tests for the renderer and generator
- `build/` — generated site + PDFs (regenerable; not committed)

### Kept local, not in this repo

Two inputs are intentionally excluded (see `.gitignore`) because they contain
internal material and are not needed to build or host the site:

- `source/apps/<app>/source-material/` — original KCI vendor documents. The
  vendor technical docs contain a plain-text database password, so these are
  kept local only.
- `source/apps/<app>/json-export/` — raw read-only ArcGIS JSON extracts used to
  regenerate the factual Technical Reference sections. `build.py` skips
  regeneration automatically when they are absent and builds from the
  already-generated Markdown.

Credentials removed from the docs are preserved locally in `SECRETS.local.md`
(also git-ignored). Never commit secrets to this repository.

## Build

Uses only the Python standard library (PDF export additionally uses Microsoft
Edge headless, bundled with Windows). With the ArcGIS Pro bundled Python:

```
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" tooling/build.py
```

Add `--no-pdf` to build only the HTML site. Output lands in `build/site`
(open `build/site/index.html`) and `build/pdf`.

Run the tests with:

```
python tooling/tests/test_md_to_html.py
python tooling/tests/test_generate_tech_reference.py
```

## Updating the documentation

1. Edit the Markdown in `source/apps/<app>/content/`.
2. Rebuild: `python tooling/build.py` (the search index refreshes automatically).
3. Deploy the contents of `build/site` to the host.

## Hosting

`build/site` is a fully static, self-contained site (inlined CSS, embedded
images, a JavaScript search index) — it can be served from any static host or
opened directly from disk. Recommended: publish from this repository to a
static host (e.g. Cloudflare Pages or Azure Static Web Apps) with access
restricted to KCI and Solano County. KCI controls updates by controlling this
repository.
