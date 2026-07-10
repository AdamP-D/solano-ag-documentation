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


def load_export(export_dir):
    with open(os.path.join(export_dir, "_manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    items = manifest.get("items", [])
    layers = {}
    for it in items:
        item_dir = _find_item_dir(export_dir, it["id"])
        if not item_dir:
            continue
        defs = []
        for fp in sorted(glob.glob(os.path.join(item_dir, "layers", "*.json"))):
            with open(fp, encoding="utf-8") as f:
                defs.append(json.load(f))
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
    seen_rels = set()

    def _is_group(d):
        return "Group" in (d.get("type") or "") or bool(d.get("subLayers"))

    def _render_leaf(d, level):
        # A data layer/table: heading + field table, and collect domains/
        # subtypes/relationships from its fields.
        schema_parts.append("%s %s (%s)\n" % ("#" * level, d.get("name"), d.get("type", "")))
        frows = []
        for f in (d.get("fields") or []):
            if f.get("name", "").lower() in SKIP_FIELDS:
                continue
            dom = f.get("domain") or {}
            dom_name = dom.get("name", "")
            if dom.get("codedValues"):
                domain_map[dom_name] = [(cv.get("code"), cv.get("name")) for cv in dom["codedValues"]]
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
            tup = (d.get("name"), r.get("name"), r.get("cardinality", ""))
            if tup not in seen_rels:
                seen_rels.add(tup)
                rel_rows.append(tup)

    for it in items:
        defs = layers.get(it["id"], [])
        if not defs:
            continue
        by_id = {d.get("id"): d for d in defs if d.get("id") is not None}
        rendered = set()

        def _render_node(d, level):
            # Group layers have no fields — render them as a heading that
            # visually contains their child layers (nested one level deeper),
            # rather than emitting an empty field table.
            did = d.get("id")
            if did in rendered:
                return
            rendered.add(did)
            if _is_group(d):
                schema_parts.append("%s %s (%s)\n" % ("#" * level, d.get("name"), d.get("type", "")))
                schema_parts.append("*Group layer — contains the layers below.*\n")
                for sub in (d.get("subLayers") or []):
                    child = by_id.get(sub.get("id"))
                    if child is not None:
                        _render_node(child, level + 1)
            else:
                _render_leaf(d, level)

        # Render top-level layers (no parent) first, nesting children under groups.
        for d in defs:
            pl = d.get("parentLayer")
            if pl and pl.get("id") is not None:
                continue
            _render_node(d, 4)
        # Safety net: render any layer not reached above (e.g. an orphaned child
        # whose parent group is absent from the export) at the base level.
        for d in defs:
            if d.get("id") not in rendered:
                _render_node(d, 4)

    schema = "\n".join(schema_parts) if schema_parts else "_No layers/tables._"
    domains = "\n\n".join(
        "**%s**\n\n" % (k or "(unnamed)") + _table(["Coded Value", "Alias"], vals)
        for k, vals in sorted(domain_map.items())) or "_No domains._"
    subtypes = "\n".join(subtype_parts) if subtype_parts else "_No subtypes._"
    relationships = _table(["Layer/Table", "Relationship", "Cardinality"], rel_rows) if rel_rows else "_No relationships._"

    return {"portal-items": portal, "services": services, "schema": schema,
            "domains": domains, "subtypes": subtypes, "relationships": relationships}


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
    with open(tr_path, encoding="utf-8") as f:
        text = f.read()
    with open(tr_path, "w", encoding="utf-8") as f:
        f.write(inject(text, sections))
    print("Injected generated sections into", tr_path)


if __name__ == "__main__":
    main()
