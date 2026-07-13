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
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)  # drop HTML comment markers
    text = re.sub(r"[#*`|>_]+", " ", md)
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
                         searchjs="../search-index.js", root="..")


def build(source_root, out_dir):
    pages = discover(source_root)
    written = []
    os.makedirs(out_dir, exist_ok=True)
    search = []
    for page in pages:
        with open(page["md_path"], encoding="utf-8") as fh:
            md = fh.read()
        body = md_to_html.md_to_html_body(md, pdf_href=page["doc"] + ".pdf")
        out_path = os.path.join(out_dir, *page["out_rel"].split("/"))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(_page_html(page, pages, body))
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
    index_body = ("<div class='home-wrap'>"
                  "<h1>Solano County Ag — Solution Documentation</h1>"
                  "<p>Select a solution and document below, or search.</p>"
                  "<div class='cards'>%s</div></div>" % "".join(cards))
    index_html = _SHELL.format(title="Solano County Ag Documentation", css=md_to_html.CSS,
                               sidebar="", body=index_body, home="index.html",
                               searchjs="search-index.js", root=".")
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index_html)
    written.append(os.path.join(out_dir, "index.html"))
    # Emit the index as a JS global (not JSON) so it loads via <script src> — a
    # plain fetch() of a local file is blocked by the browser under file://.
    with open(os.path.join(out_dir, "search-index.js"), "w", encoding="utf-8") as fh:
        fh.write("window.SEARCH_INDEX=" + json.dumps(search, ensure_ascii=False) + ";")
    written.append(os.path.join(out_dir, "search-index.js"))
    return written


_SHELL = """<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>
<meta name='viewport' content='width=device-width, initial-scale=1'/>
<title>{title}</title><style>{css}
body{{display:grid;grid-template-columns:288px 1fr;gap:0;}}
nav.side{{background:var(--blue-050);border-right:1px solid var(--blue-100);padding:18px 16px;
 height:100vh;overflow:auto;position:sticky;top:0;font-size:14px;}}
nav.side>a{{color:var(--blue);text-decoration:none;font-family:Georgia,serif;}}
nav.side a{{color:var(--blue);text-decoration:none}} nav.side .cur>a{{font-weight:700;text-decoration:underline}}
nav.side ul{{list-style:none;margin:4px 0 14px 6px;padding:0;font-size:14px}}
nav.side li{{margin:2px 0}} .app{{font-weight:700;color:var(--blue-dark);font-family:Georgia,serif;font-size:13.5px}}
main{{padding:0;min-width:0}}
.home-wrap{{max-width:840px;margin:0 auto;padding:40px clamp(18px,4vw,40px);}}
.home-wrap h1{{font-size:30px;font-family:Georgia,serif;color:var(--blue);border-bottom:3px solid var(--blue);padding-bottom:12px;margin:0 0 8px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:24px}}
.card{{border:1px solid var(--blue-100);border-radius:12px;padding:18px;background:#fff}}
.card h3{{margin:0 0 8px;font-family:Georgia,serif;color:var(--blue-dark);font-size:16px}}
#q{{width:100%;padding:8px 10px;margin:14px 0 6px;border:1px solid var(--blue-100);border-radius:8px;font-size:13.5px}}
#results{{margin-bottom:10px}}
#results a{{display:block;padding:7px 9px;font-size:12.5px;text-decoration:none;border-radius:8px;border:1px solid transparent}}
#results a:hover{{background:#fff;border-color:var(--blue-100)}}
#results .rt{{font-weight:700;color:var(--blue);display:block}}
#results .rs{{color:#555;display:block;margin-top:2px;line-height:1.45}}
#results mark{{background:#ffe39a;color:inherit;padding:0 1px;border-radius:2px}}
#results .empty{{font-size:12px;color:#8a8a8a;padding:4px 2px}}</style></head><body>
<nav class='side'><a href='{home}'><strong>&#8962; Home</strong></a>
<input id='q' placeholder='Search…'/><div id='results'></div><ul>{sidebar}</ul></nav>
<main>{body}</main>
<script src="{searchjs}"></script>
<script>
(function(){{
 var ROOT="{root}";
 function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
 function snippet(text,t){{
  var lt=text.toLowerCase(),i=lt.indexOf(t);
  if(i<0)return esc(text.slice(0,150));
  var start=Math.max(0,i-55),end=Math.min(text.length,i+t.length+90);
  return (start>0?'… ':'')+esc(text.slice(start,i))+'<mark>'+esc(text.slice(i,i+t.length))
        +'</mark>'+esc(text.slice(i+t.length,end))+(end<text.length?' …':'');
 }}
 function run(){{
  var idx=window.SEARCH_INDEX||[];
  var q=document.getElementById('q'),res=document.getElementById('results');
  if(!q)return;
  q.addEventListener('input',function(){{
   var t=q.value.trim().toLowerCase();res.innerHTML='';
   if(t.length<2)return;
   var hits=idx.filter(function(e){{
     return e.text.toLowerCase().indexOf(t)>=0||e.title.toLowerCase().indexOf(t)>=0;}}).slice(0,12);
   if(!hits.length){{res.innerHTML="<div class='empty'>No matches</div>";return;}}
   hits.forEach(function(e){{
    var a=document.createElement('a');a.href=ROOT+'/'+e.url;
    a.innerHTML="<span class='rt'>"+esc(e.title)+"</span><span class='rs'>"+snippet(e.text,t)+"</span>";
    res.appendChild(a);}});
  }});
 }}
 if(document.readyState!=='loading')run();else document.addEventListener('DOMContentLoaded',run);
}})();
</script></body></html>"""


if __name__ == "__main__":
    HERE = os.path.dirname(os.path.abspath(__file__))
    REPO = os.path.dirname(HERE)
    src = os.path.join(REPO, "source")
    out = os.path.join(REPO, "build", "site")
    written = build(src, out)
    print("Wrote %d files to %s" % (len(written), out))
