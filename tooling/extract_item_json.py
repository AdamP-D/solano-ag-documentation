"""
extract_item_json.py

READ-ONLY extraction of every piece of JSON that defines how a set of ArcGIS
Enterprise items behave. Give it a list of item IDs and it dumps, for each item:

  1. item.json        - the item description (type, typeKeywords, url, metadata)
  2. data.json        - item.get_data() (Web Map, Dashboard, Web AppBuilder /
                        Web Mapping Application config, Experience Builder appitem,
                        Form/Survey config, etc.)
  3. resources/...    - every item resource (Experience Builder & Web AppBuilder
                        store their real config here as JSON files; binary
                        resources are saved as-is). This is where editing widget
                        and app layout JSON usually lives.
  4. service.json     - for Feature/Map Service items: the full service definition
     layers/<id>.json   plus every layer & table definition, which includes the
                        feature editing templates, types/subtypes, edit forms
                        (formInfo), fields, domains, drawingInfo and popupInfo.

By default it also FOLLOWS references: a web map / dashboard / app refers to its
feature layers by itemId, so the script discovers those referenced items and
extracts them too — meaning you can list just the web maps and still capture the
backing feature services and their editing templates/types/formInfo. Disable
with --no-follow; limit recursion with --depth.

Nothing is modified anywhere in the portal. Every call is a GET. The script
never posts, updates, deletes, or shares.

This mirrors the extraction approach used by the SignalTrack DEV->PROD scripts
(audit_prod.py / update_prod_apps.py / clone_portal_folder.py) — get_data() for
app config, item.resources for Experience/AppBuilder, and per-layer service JSON
for editing templates/types/formInfo — but pulls from an explicit ID list and
writes everything to disk instead of pushing it anywhere.

Usage:
    # Use the constants below (edit ITEM_IDS), prompt for password:
    python extract_item_json.py

    # Or override on the command line:
    python extract_item_json.py \
        --url https://bou.howardcountymd.gov/arcgis/ \
        --username jbussiere \
        --ids-file item_ids.txt \
        --out json_export

    # Or pass IDs directly:
    python extract_item_json.py abcd1234... ef567890...

Requirements:
    pip install arcgis            (or run with the ArcGIS Pro bundled Python)
"""

import argparse
import datetime
import getpass
import json
import os
import re
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from arcgis.gis import GIS


# ---------------------------------------------------------------------------
# Configuration — edit these, or override with command-line arguments.
# ---------------------------------------------------------------------------

PORTAL_URL = "https://solanocountygis.com/portal/"
USERNAME   = ""   # leave blank to be prompted, or set it / pass --username

# Put your item IDs here (one per line is easiest), or use --ids-file / args.
ITEM_IDS = [
    # "cb66d80875fe45ada1426226c64b24b5",
    # "a09fa3fb1d05447585e9aa9f1349fc05",
]

# Item types whose backing service should be walked layer-by-layer.
SERVICE_TYPES = {"Feature Service", "Map Service", "Feature Layer", "Table",
                 "Image Service", "Vector Tile Service", "Scene Service"}

# A URL is treated as a REST service only if it ends in one of these endpoints
# (optionally followed by a layer index). App item URLs do not match this.
_SERVICE_URL_RE = re.compile(
    r"/(?:Feature|Map|Image|VectorTile|Scene|GP|Geometry|Stream)Server"
    r"(?:/\d+)?/?$",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_name(text, maxlen=60):
    """Make a filesystem-safe slug from an item title."""
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", (text or "").strip())
    return (text or "untitled")[:maxlen].strip("_") or "untitled"


def write_json(path, obj):
    """Write any JSON-serialisable object with indentation; fall back to str()."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        try:
            json.dump(obj, fh, indent=2, ensure_ascii=False, sort_keys=True)
        except TypeError:
            json.dump(str(obj), fh, indent=2, ensure_ascii=False)


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def rest_get(gis, url, params=None):
    """Authenticated GET returning parsed JSON (read-only)."""
    p = {"f": "json"}
    if params:
        p.update(params)
    return gis._con.get(url, params=p)


# Matches an ArcGIS item ID: 32 lowercase hex characters.
_ITEM_ID_RE = re.compile(r"\b[0-9a-f]{32}\b")


def find_item_id_refs(blobs):
    """
    Return the set of candidate item IDs referenced anywhere in the given JSON
    blobs (web map operationalLayers[].itemId, dashboard/app data sources,
    Experience Builder & Web AppBuilder configs, etc.). Web maps and apps refer
    to their feature layers by itemId, so following these lets the script pull
    the backing feature services — and their editing templates/types/formInfo —
    without having to list every layer ID by hand. Candidates are validated
    against the portal before being followed, so stray hex strings are harmless.
    """
    ids = set()
    for blob in blobs:
        if blob is None:
            continue
        try:
            text = json.dumps(blob)
        except TypeError:
            text = str(blob)
        ids.update(_ITEM_ID_RE.findall(text.lower()))
    return ids


# ---------------------------------------------------------------------------
# Per-item extraction
# ---------------------------------------------------------------------------

def extract_item_description(gis, item, item_dir, summary):
    """The item record itself: type, typeKeywords, url, tags, extent, etc."""
    try:
        desc = rest_get(
            gis,
            f"{gis.url.rstrip('/')}/sharing/rest/content/items/{item.id}",
        )
        write_json(os.path.join(item_dir, "item.json"), desc)
        summary["files"].append("item.json")
    except Exception as exc:
        summary["errors"].append(f"item description: {exc}")


def extract_item_data(gis, item, item_dir, summary, blobs):
    """item.get_data() — the main config blob for maps, dashboards, apps, forms."""
    try:
        data = item.get_data()
        if data in (None, "", b""):
            return
        if isinstance(data, (bytes, bytearray)):
            # Non-JSON data payload (rare for config items) — save raw.
            write_bytes(os.path.join(item_dir, "data.bin"), data)
            summary["files"].append("data.bin")
        else:
            write_json(os.path.join(item_dir, "data.json"), data)
            summary["files"].append("data.json")
            blobs.append(data)
    except Exception as exc:
        summary["errors"].append(f"get_data: {exc}")


def extract_resources(gis, item, item_dir, summary, blobs):
    """
    Item resources. Experience Builder and Web AppBuilder store their real
    application/widget config here as JSON files. Saved preserving folder paths.
    """
    try:
        resources = item.resources.list()
    except Exception as exc:
        summary["errors"].append(f"resources.list: {exc}")
        return
    if not resources:
        return
    res_dir = os.path.join(item_dir, "resources")
    for r in resources:
        path = r.get("resource", "")
        if not path:
            continue
        out_path = os.path.join(res_dir, *path.split("/"))
        try:
            content = item.resources.get(path)
            if isinstance(content, (dict, list)):
                if not out_path.endswith(".json"):
                    out_path += ".json"
                write_json(out_path, content)
                blobs.append(content)
            elif isinstance(content, (bytes, bytearray)):
                write_bytes(out_path, content)
            elif isinstance(content, str):
                # Could be JSON-as-text; store verbatim.
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "w", encoding="utf-8") as fh:
                    fh.write(content)
            else:
                write_json(out_path + ".json", content)
            summary["files"].append(f"resources/{path}")
        except Exception as exc:
            summary["errors"].append(f"resource '{path}': {exc}")


def extract_service(gis, item, item_dir, summary):
    """
    Full service + per-layer/table JSON. This is where the feature editing
    configuration lives: templates, types/subtypes, formInfo (edit forms),
    fields, domains, drawingInfo (symbology), and popupInfo.
    """
    service_url = (item.url or "").rstrip("/")
    if not service_url:
        return
    # Only treat the URL as a service endpoint. App items (Web AppBuilder /
    # Web Mapping Application, Experience Builder) also have a `url`, but it
    # points to the app's HTML page, not a REST service — skip those.
    if not _SERVICE_URL_RE.search(service_url):
        return
    try:
        service = rest_get(gis, service_url)
    except Exception as exc:
        summary["errors"].append(f"service definition: {exc}")
        return
    if not isinstance(service, dict):
        summary["errors"].append("service definition: non-JSON response (skipped)")
        return
    write_json(os.path.join(item_dir, "service.json"), service)
    summary["files"].append("service.json")

    layer_dir = os.path.join(item_dir, "layers")
    for group_key in ("layers", "tables"):
        for entry in (service.get(group_key) or []):
            lid = entry.get("id")
            if lid is None:
                continue
            try:
                layer_def = rest_get(gis, f"{service_url}/{lid}")
                lname = safe_name(layer_def.get("name") or f"{group_key}_{lid}")
                fname = f"{lid}_{lname}.json"
                write_json(os.path.join(layer_dir, fname), layer_def)
                summary["files"].append(f"layers/{fname}")
            except Exception as exc:
                summary["errors"].append(f"layer {lid}: {exc}")


def extract_one(gis, item_id, out_root, source="requested", item=None):
    if item is None:
        item = gis.content.get(item_id)
    summary = {"id": item_id, "source": source, "files": [], "errors": []}

    if item is None:
        summary["title"] = None
        summary["type"] = None
        summary["referenced_ids"] = []
        summary["errors"].append("item not found or not accessible")
        print(f"  [MISSING] {item_id}: not found / no access")
        return summary, set()

    summary["title"] = item.title
    summary["type"] = item.type
    item_dir = os.path.join(out_root, f"{item_id}_{safe_name(item.title)}")

    blobs = []
    extract_item_description(gis, item, item_dir, summary)
    extract_item_data(gis, item, item_dir, summary, blobs)
    extract_resources(gis, item, item_dir, summary, blobs)
    if item.url:
        # extract_service itself checks the URL is a real service endpoint,
        # so app items (whose url is an HTML page) are skipped safely.
        extract_service(gis, item, item_dir, summary)

    # itemId references found inside this item's config (minus a self-reference).
    refs = find_item_id_refs(blobs) - {item_id}
    summary["referenced_ids"] = sorted(refs)

    status = "OK" if not summary["errors"] else "PARTIAL"
    tag = "" if source == "requested" else " (referenced)"
    print(f"  [{status}] [{item.type}] {item.title}{tag} "
          f"({len(summary['files'])} file(s)"
          f"{', ' + str(len(summary['errors'])) + ' error(s)' if summary['errors'] else ''})")
    for err in summary["errors"]:
        print(f"           ! {err}")
    return summary, refs


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def load_ids(args):
    ids = list(args.item_ids)
    if args.ids_file:
        with open(args.ids_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    ids.append(line)
    if not ids:
        ids = list(ITEM_IDS)
    # De-duplicate, preserve order.
    seen, ordered = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    return ordered


def parse_args():
    p = argparse.ArgumentParser(
        description="Read-only export of all configuration JSON for a list of "
                    "ArcGIS Enterprise items."
    )
    p.add_argument("item_ids", nargs="*", help="Item IDs to extract.")
    p.add_argument("--url", default=PORTAL_URL, help="Portal URL.")
    p.add_argument("--username", default=USERNAME, help="Portal username.")
    p.add_argument("--ids-file", help="Text file of item IDs (one per line; # comments allowed).")
    p.add_argument("--search", action="append", metavar="QUERY",
                   help="Find items by an ArcGIS search query and extract the "
                        "matches (e.g. --search \"title:GWSS\", --search "
                        "\"tags:GWSS type:Web Map\"). Repeatable.")
    p.add_argument("--folder", action="append", metavar="NAME",
                   help="Extract every item in this portal folder. Repeatable. "
                        "Use \"/\" or \"root\" for the top-level (no folder).")
    p.add_argument("--owner", metavar="USERNAME",
                   help="Owner whose folder(s) to read for --folder "
                        "(default: the authenticated user).")
    p.add_argument("--max-search", type=int, default=1000,
                   help="Max items returned per --search query (default 1000).")
    p.add_argument("--out", default=None, help="Output directory (default: json_export_<timestamp>).")
    p.add_argument("--no-follow", action="store_true",
                   help="Do not follow itemId references found in web maps, apps, "
                        "and dashboards. By default, referenced items (e.g. the "
                        "feature services a web map uses) are also extracted so "
                        "their editing templates/types/formInfo are captured.")
    p.add_argument("--depth", type=int, default=5,
                   help="Max levels of reference-following (default 5). "
                        "Ignored with --no-follow.")
    return p.parse_args()


def collect_seed_ids(gis, args, explicit_ids):
    """
    Build the ordered, de-duplicated list of seed item IDs from explicit IDs
    plus any --search queries and --folder listings (resolved against the portal).
    """
    ids = list(explicit_ids)

    for query in (args.search or []):
        try:
            results = gis.content.search(query=query, max_items=args.max_search)
            print(f"  search {query!r}: {len(results)} match(es)")
            for r in results:
                print(f"      [{r.type}] {r.title} ({r.id})")
                ids.append(r.id)
        except Exception as exc:
            print(f"  search {query!r} failed: {exc}", file=sys.stderr)

    if args.folder:
        owner = args.owner or gis.users.me.username
        user = gis.users.get(owner)
        for folder in args.folder:
            folder_arg = None if folder.lower() in ("/", "root", "") else folder
            try:
                items = user.items(folder=folder_arg, max_items=10000)
                label = folder_arg or "(root)"
                print(f"  folder {label!r} (owner {owner}): {len(items)} item(s)")
                for it in items:
                    print(f"      [{it.type}] {it.title} ({it.id})")
                    ids.append(it.id)
            except Exception as exc:
                print(f"  folder {folder!r} failed: {exc}", file=sys.stderr)

    seen, ordered = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    return ordered


def main():
    args = parse_args()
    explicit_ids = load_ids(args)
    if not explicit_ids and not args.search and not args.folder:
        print("No items specified. Provide item IDs (args, --ids-file, or the "
              "ITEM_IDS constant), or use --search / --folder.", file=sys.stderr)
        sys.exit(1)

    out_root = args.out or f"json_export_{datetime.datetime.now():%Y%m%d_%H%M%S}"
    os.makedirs(out_root, exist_ok=True)

    username = args.username or input("Portal username: ").strip()
    if not username:
        print("No username provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to {args.url} as {username}...")
    password = getpass.getpass(f"Password for '{username}': ")
    try:
        gis = GIS(url=args.url, username=username, password=password)
    except Exception as exc:
        print(f"ERROR: could not connect — {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"  Connected as: {gis.users.me.username}")
    print(f"  Output: {os.path.abspath(out_root)}\n")

    if args.search or args.folder:
        print("Resolving items from --search / --folder...")
    ids = collect_seed_ids(gis, args, explicit_ids)
    if not ids:
        print("No items matched. Nothing to extract.", file=sys.stderr)
        sys.exit(1)

    follow = not args.no_follow
    mode = (f"following references up to depth {args.depth}"
            if follow else "no reference following")
    print(f"Extracting {len(ids)} requested item(s) (read-only, {mode})...")

    item_cache = {}                               # item_id -> Item or None

    def resolve(item_id):
        if item_id not in item_cache:
            try:
                item_cache[item_id] = gis.content.get(item_id)
            except Exception:
                item_cache[item_id] = None
        return item_cache[item_id]

    manifest = []
    seen = set()                                  # item IDs already extracted
    queue = [(i, 0, "requested") for i in ids]    # (item_id, depth, source)
    while queue:
        item_id, depth, source = queue.pop(0)
        if item_id in seen:
            continue
        seen.add(item_id)

        summary, refs = extract_one(gis, item_id, out_root,
                                    source=source, item=resolve(item_id))
        manifest.append(summary)

        if follow and summary["title"] and depth < args.depth:
            for ref in sorted(refs):
                # Only follow references that resolve to real, accessible items,
                # so stray hex strings don't become spurious "missing" entries.
                if ref not in seen and resolve(ref) is not None:
                    queue.append((ref, depth + 1, "referenced"))

    write_json(os.path.join(out_root, "_manifest.json"), {
        "portal": args.url,
        "extracted_by": gis.users.me.username,
        "extracted_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "follow_references": follow,
        "max_depth": args.depth if follow else 0,
        "requested_ids": ids,
        "item_count": len(manifest),
        "items": manifest,
    })

    requested = sum(1 for m in manifest if m["source"] == "requested")
    referenced = sum(1 for m in manifest if m["source"] == "referenced")
    ok = sum(1 for m in manifest if m["title"] and not m["errors"])
    partial = sum(1 for m in manifest if m["title"] and m["errors"])
    missing = sum(1 for m in manifest if not m["title"])
    print(f"\nDone. {len(manifest)} item(s) total "
          f"({requested} requested, {referenced} discovered): "
          f"{ok} clean, {partial} partial, {missing} missing.")
    print(f"Wrote output and _manifest.json to: {os.path.abspath(out_root)}")


if __name__ == "__main__":
    main()
