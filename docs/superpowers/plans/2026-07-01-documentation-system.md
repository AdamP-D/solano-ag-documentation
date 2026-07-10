# Solano Ag Documentation System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the Solano Ag documentation into a central `source/` + `build/` repository with a pure-Python build pipeline that generates a navigable static site plus PDFs, and add a hybrid-generated Technical Reference document per app.

**Architecture:** Markdown is the source of truth under `source/apps/<app>/content/`. A tooling pipeline (`tooling/*.py`, standard-library only) generates the factual Technical Reference sections from each app's read-only ArcGIS JSON export, renders all Markdown into a self-contained static site with search, and exports PDFs via Edge headless. `build/` is fully regenerable and is what ships to Solano.

**Tech Stack:** ArcGIS Pro bundled Python 3 (standard library only for build scripts; `arcgis` package only for the extractor), Microsoft Edge headless (PDF), vanilla HTML/CSS/JS (site), Markdown (content), git (version control), `unittest` (tests).

## Global Constraints

- Python interpreter for all commands: `C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe`
- Build scripts use the **standard library only** — no pip installs into the ArcGIS Pro environment.
- **No secrets** in any content or generated output — never include credentials, connection strings, or passwords (the KCI technical docs contain a plain-text database password; always exclude it).
- `extract_item_json.py` is **read-only** — it never modifies the portal.
- Repository root: `C:\Projects\Solano\Ag\Documentation`
- Five apps and their `source/apps/` slugs: `gwss`, `weeds-invasives`, `incoming-shipment-tracking`, `pq-inspection-tracking`, `plant-pest-other`
- Three document types per app, standardized filenames: `knowledge-base.md`, `requirements.md`, `technical-reference.md`
- Tests use stdlib `unittest`; run a test file directly, e.g. `python tooling/tests/test_generate_tech_reference.py`
- Tone by audience: Knowledge Base = end users (plain language); Requirements = stakeholders; Technical Reference = GIS admins/developers.

---

### Task 1: Repository skeleton, git, and shared renderer

**Files:**
- Create: `source/`, `source/apps/`, `source/shared/`, `source/templates/`, `tooling/`, `tooling/tests/`, `build/` (directories)
- Create: `.gitignore`
- Create: `README.md`
- Move: `docs/md_to_html.py` → `tooling/md_to_html.py`

**Interfaces:**
- Produces: `tooling/md_to_html.py` exposing `convert(md_path, title=None) -> out_path`, `md_to_html_body(md) -> str`, and the module constant `CSS`.

- [ ] **Step 1: Initialize git if not already a repo**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && git rev-parse --is-inside-work-tree 2>/dev/null || git init
```
Expected: either `true`, or `Initialized empty Git repository`.

- [ ] **Step 2: Create the directory skeleton**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && mkdir -p source/apps source/shared source/templates tooling/tests build
```
Expected: no output; directories exist.

- [ ] **Step 3: Move the shared renderer into tooling/**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && git mv docs/md_to_html.py tooling/md_to_html.py 2>/dev/null || mv "docs/md_to_html.py" "tooling/md_to_html.py"
```
Expected: `tooling/md_to_html.py` exists; `docs/md_to_html.py` gone.

- [ ] **Step 4: Write `.gitignore`**

Create `.gitignore`:
```
# Generated output — regenerable from source/
/build/
__pycache__/
*.pyc
```

- [ ] **Step 5: Write `README.md`**

Create `README.md`:
```markdown
# Solano County Ag — Solution Documentation

Central documentation repository for the County's agricultural GIS solutions
(GWSS, Weeds & Invasives, Incoming Shipment Tracking, PQ Inspection Tracking,
Plant/Pest/Other). Maintained by KCI; delivered to Solano County as a static
site plus PDFs.

## Layout
- `source/apps/<app>/content/` — authored Markdown (source of truth)
- `source/apps/<app>/source-material/` — original KCI documents
- `source/apps/<app>/json-export/` — read-only ArcGIS JSON extract
- `source/templates/` — document templates
- `tooling/` — the build pipeline (standard-library Python)
- `build/` — generated site + PDFs (regenerable; not committed)

## Build
Use the ArcGIS Pro bundled Python:
`"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" tooling/build.py`

Deliver the contents of `build/` to Solano.
```

- [ ] **Step 6: Verify the renderer still imports from its new location**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" -c "import sys; sys.path.insert(0,'tooling'); import md_to_html; print('ok', hasattr(md_to_html,'convert'))"
```
Expected: `ok True`

- [ ] **Step 7: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "chore: scaffold source/build/tooling repository structure"
```

---

### Task 2: Copy the JSON extractor into tooling/

**Files:**
- Create: `tooling/extract_item_json.py` (copy of the canonical extractor)

**Interfaces:**
- Produces: `tooling/extract_item_json.py` runnable as `python tooling/extract_item_json.py --ids-file <file>`.

- [ ] **Step 1: Copy the extractor from the Code project**

Run:
```bash
cp "/c/Users/adam.phippsdickerson/Code/Item JSON Export/extract_item_json.py" "/c/Projects/Solano/Ag/Documentation/tooling/extract_item_json.py"
```
Expected: file copied.

- [ ] **Step 2: Verify it compiles**

Run:
```bash
"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" -m py_compile "/c/Projects/Solano/Ag/Documentation/tooling/extract_item_json.py" && echo OK
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "chore: add read-only JSON extractor to tooling"
```

---

### Task 3: Migrate the three finished apps into `source/apps/`

**Files:**
- Move existing GWSS, Weeds & Invasives, Incoming Shipment Tracking files into the standardized layout.

**Interfaces:**
- Produces, for each of `gwss`, `weeds-invasives`, `incoming-shipment-tracking`:
  `source/apps/<slug>/content/knowledge-base.md`, `.../content/requirements.md`,
  `source/apps/<slug>/json-export/`, `source/apps/<slug>/source-material/`, `source/apps/<slug>/notes/`.

- [ ] **Step 1: Create per-app subfolders**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation/source/apps"
for a in gwss weeds-invasives incoming-shipment-tracking pq-inspection-tracking plant-pest-other; do
  mkdir -p "$a/content" "$a/source-material" "$a/json-export" "$a/notes"
done
```
Expected: no output; folders exist.

- [ ] **Step 2: Migrate GWSS content and rename to standard filenames**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
G="GWSS"; D="source/apps/gwss"
cp "$G/Knowledge Base/GWSS-Knowledge-Base-draft.md" "$D/content/knowledge-base.md"
cp "$G/Requirements/GWSS-Requirements-draft.md" "$D/content/requirements.md"
cp "$G/Development/source-material-notes.md" "$D/notes/source-material-notes.md"
cp -r "$G"/json_export_* "$D/json-export/" 2>/dev/null
echo done
```
Expected: `done`; the two content files and json-export present.

- [ ] **Step 3: Move GWSS original source material**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation/GWSS"
find . -maxdepth 2 -type f \( -iname "*.docx" -o -iname "*.pdf" -o -iname "*.pptx" -o -iname "*.xlsx" -o -iname "*.mp4" -o -iname "*.csv" \) -not -path "*/json_export_*" -exec cp --parents {} "../source/apps/gwss/source-material/" \;
echo done
```
Expected: `done`; original GWSS documents copied under `source-material/`.

- [ ] **Step 4: Repeat migration for Weeds & Invasives**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
W="Weeds & Invasives Treatment Application (ToH)"; D="source/apps/weeds-invasives"
cp "$W/Knowledge Base/W&I-Knowledge-Base-draft.md" "$D/content/knowledge-base.md"
cp "$W/Requirements/W&I-Requirements-draft.md" "$D/content/requirements.md"
cp "$W/Development/source-material-notes.md" "$D/notes/source-material-notes.md"
cp -r "$W"/json_export_* "$D/json-export/" 2>/dev/null
cp "$W"/*.docx "$W"/*.pdf "$D/source-material/" 2>/dev/null
echo done
```
Expected: `done`.

- [ ] **Step 5: Repeat migration for Incoming Shipment Tracking**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
I="Incoming Shipment Tracking"; D="source/apps/incoming-shipment-tracking"
cp "$I/Knowledge Base/IST-Knowledge-Base-draft.md" "$D/content/knowledge-base.md"
cp "$I/Requirements/IST-Requirements-draft.md" "$D/content/requirements.md"
cp "$I/Development/source-material-notes.md" "$D/notes/source-material-notes.md"
cp -r "$I"/json_export_* "$D/json-export/" 2>/dev/null
cp -r "$I/Technical Documentation" "$D/source-material/" 2>/dev/null
cp "$I"/*.docx "$I"/*.pptx "$D/source-material/" 2>/dev/null
echo done
```
Expected: `done`.

- [ ] **Step 6: Verify each migrated app has its two content files**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation/source/apps"
for a in gwss weeds-invasives incoming-shipment-tracking; do
  echo "$a:"; ls "$a/content"; ls -d "$a"/json-export/* 2>/dev/null | head -1
done
```
Expected: each app lists `knowledge-base.md` and `requirements.md`, and a json-export folder.

- [ ] **Step 7: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "refactor: migrate finished apps into source/apps standardized layout"
```

> Note: the original per-app folders (`GWSS/`, `Weeds & Invasives…/`, `Incoming Shipment Tracking/`) are left in place for now; a later cleanup task removes them once the build is verified.

---

### Task 4: `generate_tech_reference.py` — factual sections from JSON

**Files:**
- Create: `tooling/generate_tech_reference.py`
- Create: `tooling/tests/test_generate_tech_reference.py`

**Interfaces:**
- Produces:
  - `load_export(export_dir: str) -> dict` — returns `{"manifest": <dict>, "items": [<item summary dicts>], "layers": {item_id: [<layer json>]}}`.
  - `render_sections(export: dict) -> dict[str, str]` — returns Markdown strings keyed by section name: `"portal-items"`, `"services"`, `"schema"`, `"domains"`, `"subtypes"`, `"relationships"`.
  - `inject(md_text: str, sections: dict[str, str]) -> str` — replaces each `<!-- GENERATED:<key> -->…<!-- /GENERATED:<key> -->` region in `md_text` with the matching section content (keeping the markers).
  - CLI: `python tooling/generate_tech_reference.py <app-slug>` reads `source/apps/<slug>/json-export/<latest>/` and injects into `source/apps/<slug>/content/technical-reference.md` in place.

- [ ] **Step 1: Write the failing test for `inject`**

Create `tooling/tests/test_generate_tech_reference.py`:
```python
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import generate_tech_reference as g


class TestInject(unittest.TestCase):
    def test_replaces_marked_region_and_keeps_markers(self):
        md = "Intro\n<!-- GENERATED:schema -->\nOLD\n<!-- /GENERATED:schema -->\nOutro\n"
        out = g.inject(md, {"schema": "NEW TABLE"})
        self.assertIn("<!-- GENERATED:schema -->", out)
        self.assertIn("<!-- /GENERATED:schema -->", out)
        self.assertIn("NEW TABLE", out)
        self.assertNotIn("OLD", out)
        self.assertTrue(out.startswith("Intro"))
        self.assertTrue(out.rstrip().endswith("Outro"))

    def test_leaves_unmatched_sections_untouched(self):
        md = "<!-- GENERATED:schema -->\nX\n<!-- /GENERATED:schema -->\n"
        out = g.inject(md, {"domains": "Y"})
        self.assertIn("X", out)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_generate_tech_reference.py
```
Expected: FAIL / ImportError (`generate_tech_reference` not found or `inject` missing).

- [ ] **Step 3: Implement `inject` and module scaffold**

Create `tooling/generate_tech_reference.py`:
```python
"""Generate the factual sections of an app's Technical Reference from its
read-only ArcGIS JSON export, and inject them into technical-reference.md at
<!-- GENERATED:<key> --> markers. Standard library only."""
import glob
import json
import os
import re
import sys

SKIP_FIELDS = {"objectid", "globalid", "shape", "shape_length", "shape_area",
               "shape__area", "shape__length", "se_anno_cad_data"}


def inject(md_text, sections):
    for key, content in sections.items():
        pattern = re.compile(
            r"(<!-- GENERATED:%s -->)(.*?)(<!-- /GENERATED:%s -->)" % (re.escape(key), re.escape(key)),
            re.S,
        )
        md_text = pattern.sub(lambda m: m.group(1) + "\n" + content.strip() + "\n" + m.group(3), md_text)
    return md_text
```

- [ ] **Step 4: Run the test to verify it passes**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_generate_tech_reference.py
```
Expected: PASS (2 tests OK).

- [ ] **Step 5: Add the failing test for `load_export` and `render_sections`**

Append to `tooling/tests/test_generate_tech_reference.py` (before `if __name__`):
```python
class TestRender(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()
        exp = os.path.join(self.dir, "json_export_test")
        os.makedirs(os.path.join(exp, "svc1_Demo_Service", "layers"))
        json.dump({"portal": "https://p/", "items": [
            {"id": "svc1", "title": "Demo Service", "type": "Feature Service", "source": "requested"}
        ]}, open(os.path.join(exp, "_manifest.json"), "w"))
        json.dump({"name": "Demo Layer", "type": "Feature Layer", "fields": [
            {"name": "status", "alias": "Status", "type": "esriFieldTypeString", "length": 50,
             "nullable": True, "editable": True,
             "domain": {"type": "codedValue", "name": "d_status",
                        "codedValues": [{"name": "Open"}, {"name": "Closed"}]}}
        ], "relationships": [{"name": "Demo_Rel", "cardinality": "esriRelCardinalityOneToMany"}]},
            open(os.path.join(exp, "svc1_Demo_Service", "layers", "0_Demo_Layer.json"), "w"))
        self.export = g.load_export(exp)

    def test_load_export_reads_items_and_layers(self):
        self.assertEqual(len(self.export["items"]), 1)
        self.assertIn("svc1", self.export["layers"])

    def test_render_sections_has_all_keys_and_content(self):
        s = g.render_sections(self.export)
        for k in ("portal-items", "services", "schema", "domains", "subtypes", "relationships"):
            self.assertIn(k, s)
        self.assertIn("Demo Service", s["portal-items"])
        self.assertIn("Status", s["schema"])
        self.assertIn("Open", s["domains"])
        self.assertIn("Demo_Rel", s["relationships"])
```

- [ ] **Step 6: Run to verify the new tests fail**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_generate_tech_reference.py
```
Expected: FAIL (`load_export` / `render_sections` not defined).

- [ ] **Step 7: Implement `load_export` and `render_sections`**

Append to `tooling/generate_tech_reference.py`:
```python
def load_export(export_dir):
    manifest = json.load(open(os.path.join(export_dir, "_manifest.json"), encoding="utf-8"))
    items = manifest.get("items", [])
    layers = {}
    for it in items:
        item_dir = _find_item_dir(export_dir, it["id"])
        if not item_dir:
            continue
        defs = []
        for fp in sorted(glob.glob(os.path.join(item_dir, "layers", "*.json"))):
            defs.append(json.load(open(fp, encoding="utf-8")))
        if defs:
            layers[it["id"]] = defs
    return {"manifest": manifest, "items": items, "layers": layers}


def _find_item_dir(export_dir, item_id):
    hits = glob.glob(os.path.join(export_dir, item_id + "_*"))
    return hits[0] if hits else None


def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join("" if c is None else str(c) for c in r) + " |")
    return "\n".join(out)


def render_sections(export):
    items = export["items"]
    layers = export["layers"]

    portal_rows = [(it.get("title"), it.get("type"), it.get("source"), it["id"]) for it in items]
    portal = _table(["Title", "Type", "Source", "Item ID"], portal_rows)

    svc_rows = []
    for it in items:
        if it["id"] in layers or "Service" in (it.get("type") or ""):
            svc_rows.append((it.get("title"), it.get("type"), it["id"]))
    services = _table(["Service / Item", "Type", "Item ID"], svc_rows) if svc_rows else "_No services._"

    schema_parts, domain_map, subtype_parts, rel_rows = [], {}, [], []
    for it in items:
        for d in layers.get(it["id"], []):
            schema_parts.append("#### %s (%s)\n" % (d.get("name"), d.get("type", "")))
            frows = []
            for f in (d.get("fields") or []):
                if f.get("name", "").lower() in SKIP_FIELDS:
                    continue
                dom = f.get("domain") or {}
                dom_name = dom.get("name", "")
                if dom.get("codedValues"):
                    domain_map[dom_name] = [cv.get("name") for cv in dom["codedValues"]]
                frows.append((f.get("name"), f.get("alias"),
                              (f.get("type", "") or "").replace("esriFieldType", ""),
                              f.get("length", ""), f.get("nullable", ""),
                              f.get("editable", ""), dom_name))
            schema_parts.append(_table(
                ["Field", "Alias", "Type", "Length", "Nullable", "Editable", "Domain"], frows))
            schema_parts.append("")
            for t in (d.get("types") or []):
                subtype_parts.append("- **%s**: %s" % (d.get("name"), t.get("name")))
            for r in (d.get("relationships") or []):
                rel_rows.append((d.get("name"), r.get("name"), r.get("cardinality", "")))

    schema = "\n".join(schema_parts) if schema_parts else "_No layers/tables._"
    domains = "\n\n".join(
        "**%s**: %s" % (k or "(unnamed)", ", ".join(str(v) for v in vals))
        for k, vals in sorted(domain_map.items())) or "_No domains._"
    subtypes = "\n".join(subtype_parts) if subtype_parts else "_No subtypes._"
    relationships = _table(["Layer/Table", "Relationship", "Cardinality"], rel_rows) if rel_rows else "_No relationships._"

    return {"portal-items": portal, "services": services, "schema": schema,
            "domains": domains, "subtypes": subtypes, "relationships": relationships}
```

- [ ] **Step 8: Run to verify all tests pass**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_generate_tech_reference.py
```
Expected: PASS (all tests OK).

- [ ] **Step 9: Add the CLI entry point**

Append to `tooling/generate_tech_reference.py`:
```python
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _latest_export(slug):
    base = os.path.join(REPO, "source", "apps", slug, "json-export")
    subs = [d for d in glob.glob(os.path.join(base, "*")) if os.path.isdir(d)]
    if not subs:
        raise SystemExit("No json-export found for %s" % slug)
    return sorted(subs)[-1]


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: generate_tech_reference.py <app-slug>")
    slug = sys.argv[1]
    export = load_export(_latest_export(slug))
    sections = render_sections(export)
    tr_path = os.path.join(REPO, "source", "apps", slug, "content", "technical-reference.md")
    if not os.path.exists(tr_path):
        raise SystemExit("Missing %s — author it from the template first." % tr_path)
    text = open(tr_path, encoding="utf-8").read()
    open(tr_path, "w", encoding="utf-8").write(inject(text, sections))
    print("Injected generated sections into", tr_path)


if __name__ == "__main__":
    main()
```

- [ ] **Step 10: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "feat: generate_tech_reference — factual tech-ref sections from JSON export"
```

---

### Task 5: `build_site.py` — navigable static site with search

**Files:**
- Create: `tooling/build_site.py`
- Create: `tooling/tests/test_build_site.py`

**Interfaces:**
- Consumes: `md_to_html.md_to_html_body(md) -> str`, `md_to_html.CSS`.
- Produces:
  - `discover(source_root: str) -> list[dict]` — returns page records `{"app": slug, "app_title": str, "doc": "knowledge-base"|"requirements"|"technical-reference", "doc_title": str, "md_path": str, "out_rel": "<app>/<doc>.html"}` for every existing `source/apps/*/content/*.md`.
  - `build(source_root: str, out_dir: str) -> list[str]` — writes `index.html`, each page, and `search-index.json`; returns the list of written paths.
  - `APP_TITLES: dict[str,str]` and `DOC_TITLES: dict[str,str]` mapping slugs to display names.

- [ ] **Step 1: Write the failing test**

Create `tooling/tests/test_build_site.py`:
```python
import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build_site as bs


class TestBuildSite(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        c = os.path.join(self.root, "source", "apps", "gwss", "content")
        os.makedirs(c)
        open(os.path.join(c, "knowledge-base.md"), "w", encoding="utf-8").write(
            "# GWSS KB\n\n## Overview\n\nText about traps and findings.\n")
        open(os.path.join(c, "requirements.md"), "w", encoding="utf-8").write(
            "# GWSS Requirements\n\n## Background\n\nStuff.\n")
        self.out = os.path.join(self.root, "build", "site")

    def test_discover_finds_pages(self):
        pages = bs.discover(os.path.join(self.root, "source"))
        docs = sorted(p["doc"] for p in pages)
        self.assertEqual(docs, ["knowledge-base", "requirements"])

    def test_build_writes_index_pages_and_search_index(self):
        written = bs.build(os.path.join(self.root, "source"), self.out)
        self.assertTrue(os.path.exists(os.path.join(self.out, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(self.out, "gwss", "knowledge-base.html")))
        idx = json.load(open(os.path.join(self.out, "search-index.json"), encoding="utf-8"))
        self.assertTrue(any("traps" in e["text"].lower() for e in idx))
        html = open(os.path.join(self.out, "index.html"), encoding="utf-8").read()
        self.assertIn("GWSS", html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_site.py
```
Expected: FAIL (`build_site` not found).

- [ ] **Step 3: Implement `build_site.py`**

Create `tooling/build_site.py`:
```python
"""Render source/apps/*/content/*.md into a self-contained static site with a
landing page, per-app sidebar nav, and client-side search. Standard library only."""
import glob
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_to_html

APP_TITLES = {
    "gwss": "GWSS",
    "weeds-invasives": "Weeds & Invasives Treatment",
    "incoming-shipment-tracking": "Incoming Shipment Tracking",
    "pq-inspection-tracking": "PQ Inspection Tracking",
    "plant-pest-other": "Plant, Pest & Other",
}
DOC_TITLES = {
    "knowledge-base": "Knowledge Base",
    "requirements": "Requirements",
    "technical-reference": "Technical Reference",
}
DOC_ORDER = ["knowledge-base", "requirements", "technical-reference"]


def discover(source_root):
    pages = []
    for md_path in glob.glob(os.path.join(source_root, "apps", "*", "content", "*.md")):
        doc = os.path.splitext(os.path.basename(md_path))[0]
        if doc not in DOC_TITLES:
            continue
        slug = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
        pages.append({"app": slug, "app_title": APP_TITLES.get(slug, slug),
                      "doc": doc, "doc_title": DOC_TITLES[doc], "md_path": md_path,
                      "out_rel": "%s/%s.html" % (slug, doc)})
    pages.sort(key=lambda p: (p["app_title"], DOC_ORDER.index(p["doc"])))
    return pages


def _plain_text(md):
    text = re.sub(r"[#*`|>_-]+", " ", md)
    return re.sub(r"\s+", " ", text).strip()


def _page_html(page, pages, body):
    apps = {}
    for p in pages:
        apps.setdefault(p["app"], (p["app_title"], []))[1].append(p)
    sidebar = []
    for slug, (title, plist) in sorted(apps.items(), key=lambda kv: kv[1][0]):
        active = " class='active'" if slug == page["app"] else ""
        sidebar.append("<li%s><span class='app'>%s</span><ul>" % (active, html.escape(title)))
        for p in sorted(plist, key=lambda x: DOC_ORDER.index(x["doc"])):
            rel = "../%s" % p["out_rel"]
            cur = " class='cur'" if p is page else ""
            sidebar.append("<li%s><a href='%s'>%s</a></li>" % (cur, rel, html.escape(p["doc_title"])))
        sidebar.append("</ul></li>")
    return _SHELL.format(title=html.escape("%s — %s" % (page["app_title"], page["doc_title"])),
                         css=md_to_html.CSS, sidebar="".join(sidebar), body=body, home="../index.html",
                         search="../search-index.json", root="..")


def build(source_root, out_dir):
    pages = discover(source_root)
    written = []
    os.makedirs(out_dir, exist_ok=True)
    search = []
    for page in pages:
        md = open(page["md_path"], encoding="utf-8").read()
        body = md_to_html.md_to_html_body(md)
        out_path = os.path.join(out_dir, *page["out_rel"].split("/"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        open(out_path, "w", encoding="utf-8").write(_page_html(page, pages, body))
        written.append(out_path)
        search.append({"title": "%s — %s" % (page["app_title"], page["doc_title"]),
                       "url": page["out_rel"], "text": _plain_text(md)[:5000]})
    # landing page
    cards = []
    apps = {}
    for p in pages:
        apps.setdefault(p["app"], (p["app_title"], []))[1].append(p)
    for slug, (title, plist) in sorted(apps.items(), key=lambda kv: kv[1][0]):
        links = " · ".join("<a href='%s'>%s</a>" % (p["out_rel"], html.escape(p["doc_title"]))
                           for p in sorted(plist, key=lambda x: DOC_ORDER.index(x["doc"])))
        cards.append("<div class='card'><h3>%s</h3><p>%s</p></div>" % (html.escape(title), links))
    index_body = ("<h1>Solano County Ag — Solution Documentation</h1>"
                  "<p>Select a solution and document below, or search.</p>"
                  "<div class='cards'>%s</div>" % "".join(cards))
    index_html = _SHELL.format(title="Solano County Ag Documentation", css=md_to_html.CSS,
                               sidebar="", body=index_body, home="index.html",
                               search="search-index.json", root=".")
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(index_html)
    written.append(os.path.join(out_dir, "index.html"))
    json.dump(search, open(os.path.join(out_dir, "search-index.json"), "w", encoding="utf-8"))
    written.append(os.path.join(out_dir, "search-index.json"))
    return written


_SHELL = """<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>
<meta name='viewport' content='width=device-width, initial-scale=1'/>
<title>{title}</title><style>{css}
body{{max-width:none;display:grid;grid-template-columns:280px 1fr;gap:0;padding:0}}
nav.side{{background:#f4f7f1;border-right:1px solid #cdd8c4;padding:16px;height:100vh;overflow:auto;position:sticky;top:0}}
nav.side a{{color:#2e5b1e;text-decoration:none}} nav.side .cur>a{{font-weight:700}}
nav.side ul{{list-style:none;margin:4px 0 12px 8px;padding:0}} .app{{font-weight:700;color:#3d6b27}}
main{{padding:24px 40px;max-width:8in}} .cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.card{{border:1px solid #b9c4ae;border-radius:8px;padding:16px;background:#fff}}
#q{{width:100%;padding:8px;margin-bottom:12px;border:1px solid #b9c4ae;border-radius:6px}}
#results a{{display:block;padding:4px 0}}</style></head><body>
<nav class='side'><a href='{home}'><strong>&#8962; Home</strong></a>
<input id='q' placeholder='Search…'/><div id='results'></div><ul>{sidebar}</ul></nav>
<main>{body}</main>
<script>
var ROOT="{root}";
fetch("{search}").then(r=>r.json()).then(function(idx){{
 var q=document.getElementById('q'),res=document.getElementById('results');
 q.addEventListener('input',function(){{
  var t=q.value.toLowerCase();res.innerHTML='';
  if(t.length<3)return;
  idx.filter(e=>e.text.toLowerCase().includes(t)||e.title.toLowerCase().includes(t))
     .slice(0,10).forEach(function(e){{
      var a=document.createElement('a');a.href=ROOT+'/'+e.url;a.textContent=e.title;res.appendChild(a);}});
 }});}});
</script></body></html>"""
```

- [ ] **Step 4: Run to verify tests pass**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_site.py
```
Expected: PASS (both tests OK).

- [ ] **Step 5: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "feat: build_site — static documentation site with nav and search"
```

---

### Task 6: `build_pdf.py` — HTML → PDF via Edge headless

**Files:**
- Create: `tooling/build_pdf.py`
- Create: `tooling/tests/test_build_pdf.py`

**Interfaces:**
- Consumes: `md_to_html.convert(md_path, title) -> html_path`.
- Produces:
  - `find_edge() -> str|None` — path to `msedge.exe` (checks common install paths and PATH).
  - `html_to_pdf(edge: str, html_path: str, pdf_path: str) -> None` — runs Edge headless print-to-pdf.
  - `build(source_root: str, out_dir: str) -> list[str]` — for each `content/*.md`, render HTML (temp) and export `build/pdf/<app>/<doc>.pdf`; returns written PDF paths. If Edge is not found, prints guidance and returns `[]`.

- [ ] **Step 1: Write the failing test (Edge discovery + command build, no Edge required)**

Create `tooling/tests/test_build_pdf.py`:
```python
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build_pdf as bp


class TestBuildPdf(unittest.TestCase):
    def test_find_edge_returns_str_or_none(self):
        r = bp.find_edge()
        self.assertTrue(r is None or isinstance(r, str))

    def test_command_uses_headless_and_print_flag(self):
        cmd = bp.edge_command("C:/edge.exe", "in.html", "out.pdf")
        self.assertIn("--headless", cmd)
        self.assertTrue(any(a.startswith("--print-to-pdf=") for a in cmd))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify it fails**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_pdf.py
```
Expected: FAIL (`build_pdf` not found).

- [ ] **Step 3: Implement `build_pdf.py`**

Create `tooling/build_pdf.py`:
```python
"""Export each app document to PDF by rendering Markdown to HTML and printing it
with Microsoft Edge headless. Standard library only (plus Edge, bundled with Windows)."""
import glob
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md_to_html

_EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_edge():
    for p in _EDGE_PATHS:
        if os.path.exists(p):
            return p
    return shutil.which("msedge")


def edge_command(edge, html_path, pdf_path):
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    return [edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            "--print-to-pdf=" + os.path.abspath(pdf_path), url]


def html_to_pdf(edge, html_path, pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    subprocess.run(edge_command(edge, html_path, pdf_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build(source_root, out_dir):
    edge = find_edge()
    if not edge:
        print("Microsoft Edge not found — open the build/site HTML in a browser "
              "and use Print > Save as PDF instead.")
        return []
    written = []
    for md_path in glob.glob(os.path.join(source_root, "apps", "*", "content", "*.md")):
        slug = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
        doc = os.path.splitext(os.path.basename(md_path))[0]
        html_path = md_to_html.convert(md_path)  # writes <name>.html next to the md
        pdf_path = os.path.join(out_dir, slug, doc + ".pdf")
        html_to_pdf(edge, html_path, pdf_path)
        written.append(pdf_path)
    return written


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "pdf")
    for p in build(root, out):
        print("Wrote", p)
```

- [ ] **Step 4: Run to verify tests pass**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/tests/test_build_pdf.py
```
Expected: PASS (both tests OK).

- [ ] **Step 5: Smoke-test real PDF generation (skip gracefully if Edge missing)**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" -c "import sys; sys.path.insert(0,'tooling'); import build_pdf as b; print('edge:', b.find_edge())"
```
Expected: prints a path to `msedge.exe` (or `None`). If a path prints, PDF export will work; if `None`, the browser Print-to-PDF fallback applies.

- [ ] **Step 6: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "feat: build_pdf — Edge headless HTML-to-PDF export"
```

---

### Task 7: `build.py` orchestrator

**Files:**
- Create: `tooling/build.py`

**Interfaces:**
- Consumes: `generate_tech_reference` (per-slug injection), `build_site.build`, `build_pdf.build`.
- Produces: CLI `python tooling/build.py [--no-pdf]` that regenerates tech-ref sections for every app that has both a `technical-reference.md` and a `json-export/`, then builds the site and (unless `--no-pdf`) the PDFs.

- [ ] **Step 1: Implement `build.py`**

Create `tooling/build.py`:
```python
"""Orchestrate the documentation build: regenerate tech-ref factual sections from
JSON, build the static site, and export PDFs. Standard library only."""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import generate_tech_reference as gtr
import build_site
import build_pdf


def main():
    no_pdf = "--no-pdf" in sys.argv
    source = os.path.join(REPO, "source")

    # 1) Regenerate factual tech-ref sections where possible
    for tr in glob.glob(os.path.join(source, "apps", "*", "content", "technical-reference.md")):
        slug = os.path.basename(os.path.dirname(os.path.dirname(tr)))
        exports = glob.glob(os.path.join(source, "apps", slug, "json-export", "*"))
        if not any(os.path.isdir(e) for e in exports):
            print("skip tech-ref generation (no json-export):", slug)
            continue
        export = gtr.load_export(gtr._latest_export(slug))
        text = open(tr, encoding="utf-8").read()
        open(tr, "w", encoding="utf-8").write(gtr.inject(text, gtr.render_sections(export)))
        print("generated tech-ref sections:", slug)

    # 2) Build the site
    site_out = os.path.join(REPO, "build", "site")
    written = build_site.build(source, site_out)
    print("site pages:", len(written), "->", site_out)

    # 3) Build PDFs
    if not no_pdf:
        pdfs = build_pdf.build(source, os.path.join(REPO, "build", "pdf"))
        print("pdfs:", len(pdfs))
    else:
        print("skipped PDFs (--no-pdf)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the full build (site only) to verify orchestration**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/build.py --no-pdf
```
Expected: prints generated/skip lines per app and `site pages: N -> …/build/site`; `build/site/index.html` exists.

- [ ] **Step 3: Open the site to sanity-check (manual)**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && ls build/site && ls build/site/gwss
```
Expected: `index.html`, `search-index.json`, and `gwss/knowledge-base.html`, `gwss/requirements.html`.

- [ ] **Step 4: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "feat: build.py orchestrator (generate -> site -> pdf)"
```

---

### Task 8: Document templates

**Files:**
- Create: `source/templates/knowledge-base.md`
- Create: `source/templates/requirements.md`
- Create: `source/templates/technical-reference.md`

**Interfaces:**
- Produces: the Technical Reference template with `<!-- GENERATED:<key> -->` markers matching the six keys emitted by `render_sections` (`portal-items`, `services`, `schema`, `domains`, `subtypes`, `relationships`).

- [ ] **Step 1: Copy the existing KB and Requirements templates**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
cp docs/templates/knowledge-base-template.md source/templates/knowledge-base.md
cp docs/templates/requirements-template.md source/templates/requirements.md
echo done
```
Expected: `done`.

- [ ] **Step 2: Create the Technical Reference template with generation markers**

Create `source/templates/technical-reference.md`:
```markdown
# [App Name] — Technical Reference

*Solano County Agricultural Program · GIS administrator / developer reference*

## 1. Solution Architecture

[Components (web maps, apps, dashboards, Survey123, GP services) and how they
connect. Hand-authored from the technical documentation.]

## 2. Portal Items

<!-- GENERATED:portal-items -->
<!-- /GENERATED:portal-items -->

## 3. Services & Publishing

[Narrative: referenced vs. hosted, source ArcGIS Pro project, sync/archiving,
time-zone configuration. Hand-authored.]

<!-- GENERATED:services -->
<!-- /GENERATED:services -->

## 4. Database Schema

<!-- GENERATED:schema -->
<!-- /GENERATED:schema -->

## 5. Domains

<!-- GENERATED:domains -->
<!-- /GENERATED:domains -->

## 6. Subtypes

<!-- GENERATED:subtypes -->
<!-- /GENERATED:subtypes -->

## 7. Relationships

<!-- GENERATED:relationships -->
<!-- /GENERATED:relationships -->

## 8. Database View Definitions

[Each view: purpose + verbatim SQL in a code block. Hand-authored from the
technical documentation / database.]

## 9. Attribute Rules

[Each rule: field, trigger, and Arcade expression in a code block. Hand-authored.]

## 10. Geoprocessing / Automation

[GP tools/services and their logic. Hand-authored.]

## 11. Map / App Layer Definitions

[Definition queries and dynamic-layer criteria. Hand-authored.]
```

- [ ] **Step 3: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "feat: add document templates incl. technical-reference with generation markers"
```

---

### Task 9: Author the GWSS Technical Reference (pilot)

**Files:**
- Create: `source/apps/gwss/content/technical-reference.md`

**Interfaces:**
- Consumes: `source/templates/technical-reference.md`; `generate_tech_reference.py`; the GWSS `json-export/` and `notes/source-material-notes.md`.

- [ ] **Step 1: Start from the template**

Run:
```bash
cp "/c/Projects/Solano/Ag/Documentation/source/templates/technical-reference.md" "/c/Projects/Solano/Ag/Documentation/source/apps/gwss/content/technical-reference.md"
```
Expected: file created.

- [ ] **Step 2: Author the hand-written narrative sections**

Edit `source/apps/gwss/content/technical-reference.md`, replacing the H1 with `# GWSS Data Collection and Management Solution — Technical Reference` and filling sections 1, 3 (narrative), 8, 9, 10, 11 from the GWSS technical documentation already reviewed this project:
- **Architecture:** Field Maps map + GWSS Tracking Management Web AppBuilder app; PostgreSQL referenced services; GP quarter-mile tool.
- **Services & Publishing narrative:** all data referenced (not hosted) from the GWSS PostgreSQL DB; published from the ArcGIS Pro project on the service-updates share; domain updates require stopping/restarting all GWSS services.
- **View Definitions (section 8):** include the eight views (`v_gwss_all_findings`, `v_gwss_all_surveys`, `v_gwss_all_treatments`, `v_gwss_most_recent_survey_per_parcel`, `v_gwss_most_recent_treatment_per_parcel`, `v_gwss_parcels_related_quarter_mile_buffer`, `v_gwss_recent_surveys_six_weeks`, `v_gwss_treatments_past_year`) with a one-line purpose each and the SQL in code blocks (from the GWSS Technical Documentation appendix).
- **Attribute Rules (section 9):** none documented for GWSS — state "None documented; status/symbology is driven by the database views in section 8."
- **GP/Automation (section 10):** the quarter-mile buffer & parcel-tagging tool logic.
- **Layer Definitions (section 11):** the survey/treatment status symbology categories.
- Do not include the database password.

- [ ] **Step 3: Inject the generated factual sections**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/generate_tech_reference.py gwss
```
Expected: `Injected generated sections into …/gwss/content/technical-reference.md`.

- [ ] **Step 4: Verify the generated tables populated**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && grep -c "GWSS Tracking" "source/apps/gwss/content/technical-reference.md" && grep -c "DOMAIN\|Requires Inspection\|gwss_action" "source/apps/gwss/content/technical-reference.md"
```
Expected: non-zero counts (schema and domain content present between the markers).

- [ ] **Step 5: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "docs: GWSS technical reference (pilot)"
```

---

### Task 10: Author the Weeds & Invasives and IST Technical References

**Files:**
- Create: `source/apps/weeds-invasives/content/technical-reference.md`
- Create: `source/apps/incoming-shipment-tracking/content/technical-reference.md`

**Interfaces:**
- Consumes: the template, `generate_tech_reference.py`, each app's `json-export/`, `source-material/`, and `notes/`.

- [ ] **Step 1: Author the Weeds & Invasives technical reference**

Copy the template to `source/apps/weeds-invasives/content/technical-reference.md`, set the H1, and author narrative sections from the W&I technical documentation:
- **Architecture:** Survey123 form + Field Maps map + Web AppBuilder tracking app; PostgreSQL "agdept" referenced services; Parcels REGIS pop-up hyperlink launches Survey123.
- **Services & Publishing:** referenced services; Survey123 points to an SDE-backed feature service; archiving/sync enabled.
- **Views (section 8):** state "None; edit-tracking views are a documented future option, not implemented."
- **Attribute Rules (9):** none documented — state so.
- **GP/Automation (10):** none — state "No geoprocessing services; the Survey123 form drives the workflow."
- **Layer Definitions (11):** the tracking "Ready to Treat" default and treatment-stage symbology.
Then run: `"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/generate_tech_reference.py weeds-invasives`
Expected: injection confirmation printed.

- [ ] **Step 2: Author the IST technical reference**

Copy the template to `source/apps/incoming-shipment-tracking/content/technical-reference.md`, set the H1, and author narrative sections from the IST technical documentation:
- **Architecture:** Web AppBuilder app + Field Maps + web/mobile Dashboards; PostgreSQL "agdept" referenced services; records related to a Parcels REGIS copy.
- **Services & Publishing:** referenced services; Pacific-time zone configuration; archiving on the field-map service only.
- **Views (section 8):** `v_ist_all_records` and `v_ist_inspector_view` — purpose + verbatim SQL (from the IST Technical Documentation), and note the hard-coded daylight-saving offset.
- **Attribute Rules (9):** ParcelID, Parcel Address, Parcel Common Name, IST ID, and Status — purpose + Arcade expressions (from the IST Technical Documentation).
- **GP/Automation (10):** none — state so.
- **Layer Definitions (11):** the Status and Tracking-By-Period definition-query layers and dashboard list formatting.
Then run: `"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/generate_tech_reference.py incoming-shipment-tracking`
Expected: injection confirmation printed.

- [ ] **Step 3: Verify both files have populated generated sections**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
grep -c "Scientific Name\|treatment_stage" "source/apps/weeds-invasives/content/technical-reference.md"
grep -c "Inspection Type\|insp_type\|Requires Inspection" "source/apps/incoming-shipment-tracking/content/technical-reference.md"
```
Expected: non-zero counts for both.

- [ ] **Step 4: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "docs: Weeds & Invasives and IST technical references"
```

---

### Task 11: Full build, verification, and old-folder cleanup

**Files:**
- Modify: remove the legacy top-level app folders after verifying the migration.

- [ ] **Step 1: Run the complete build (site + PDF)**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/build.py
```
Expected: generation lines per app, `site pages:` count, and either `pdfs: N` or the Edge-not-found guidance.

- [ ] **Step 2: Verify the delivered site structure**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && ls build/site && echo "---apps---" && ls build/site/gwss build/site/weeds-invasives build/site/incoming-shipment-tracking
```
Expected: `index.html`, `search-index.json`, and three HTML files per finished app (knowledge-base, requirements, technical-reference).

- [ ] **Step 3: Verify PDFs (if Edge present)**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && ls build/pdf/gwss 2>/dev/null || echo "no pdf dir (Edge fallback in use)"
```
Expected: three PDFs per finished app, or the fallback message.

- [ ] **Step 4: Confirm no secrets leaked into the build**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && grep -ri "<REDACTED-DB-PASSWORD>" build source/apps/*/content && echo "FOUND SECRET" || echo "clean"
```
Expected: `clean`.

- [ ] **Step 5: Remove the legacy top-level app folders**

Run only after Steps 1–4 pass:
```bash
cd "C:/Projects/Solano/Ag/Documentation"
git rm -r "GWSS" "Weeds & Invasives Treatment Application (ToH)" "Incoming Shipment Tracking" 2>/dev/null || rm -rf "GWSS" "Weeds & Invasives Treatment Application (ToH)" "Incoming Shipment Tracking"
echo done
```
Expected: `done`; legacy folders gone, content preserved under `source/apps/`.

- [ ] **Step 6: Move remaining meta docs and finalize**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && rm -rf docs/templates 2>/dev/null; ls source/apps && ls tooling
echo done
```
Expected: `done`; five app slugs under `source/apps`, pipeline scripts under `tooling`.

- [ ] **Step 7: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "chore: full build verified; remove legacy app folders"
```

---

### Task 12: Remaining apps (PQ Inspection Tracking, Plant/Pest/Other)

**Note:** These two apps still need their JSON extracted and their full document set authored. This task is a placeholder describing the repeatable process; execute it per app once the JSON export is dropped into `source/apps/<slug>/json-export/`.

**Files (per app):**
- Create: `source/apps/<slug>/content/knowledge-base.md`
- Create: `source/apps/<slug>/content/requirements.md`
- Create: `source/apps/<slug>/content/technical-reference.md`

- [ ] **Step 1: Extract the JSON (read-only)**

Run (with the app's item IDs in a file):
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/extract_item_json.py --ids-file <ids.txt> --out "source/apps/<slug>/json-export/json_export"
```
Expected: manifest + per-item folders under the app's `json-export/`.

- [ ] **Step 2: Author Knowledge Base and Requirements**

Copy `source/templates/knowledge-base.md` and `requirements.md` into the app's `content/`, and author them from the app's source material and JSON, following the tone and structure of the three completed apps.

- [ ] **Step 3: Author the Technical Reference and inject generated sections**

Copy `source/templates/technical-reference.md` into `content/`, author the narrative sections from the app's technical documentation, then run:
```bash
"/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/generate_tech_reference.py <slug>
```
Expected: injection confirmation.

- [ ] **Step 4: Rebuild and verify**

Run:
```bash
cd "C:/Projects/Solano/Ag/Documentation" && "/c/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" tooling/build.py && ls build/site/<slug>
```
Expected: three HTML pages for the app in the site.

- [ ] **Step 5: Commit**

```bash
cd "C:/Projects/Solano/Ag/Documentation" && git add -A && git commit -m "docs: <slug> full document set"
```

---

## Final Deliverables Checklist

- [ ] `source/` + `build/` + `tooling/` repository structure in place, under git
- [ ] `tooling/` pipeline: `extract_item_json.py`, `generate_tech_reference.py`, `build_site.py`, `build_pdf.py`, `md_to_html.py`, `build.py` (all tests passing)
- [ ] Three finished apps migrated into `source/apps/<slug>/`
- [ ] Technical References authored for GWSS, Weeds & Invasives, IST
- [ ] `build/site/` navigable hub with search + `build/pdf/` exports generated
- [ ] No secrets in `source/` content or `build/`
- [ ] PQ Inspection Tracking and Plant/Pest/Other completed per Task 12 (when JSON provided)
