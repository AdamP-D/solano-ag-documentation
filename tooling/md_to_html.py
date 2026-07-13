"""
md_to_html.py — Convert a Markdown document to a clean, print-ready HTML file.

No third-party libraries required (runs on the ArcGIS Pro bundled Python or any
Python 3). The output HTML uses the Solano County "blue" design system —
county-seal masthead, numbered section badges, an auto Table of Contents,
callout boxes, themed tables, and a developed-by footer — and is styled for
letter-size printing (Print -> Save as PDF, or open in Word).

Usage:
    python md_to_html.py "path/to/draft.md" ["Output Title"]

If no output title is given, the document's first H1 is used. The .html file is
written next to the .md file (same name, .html extension).

Supports the Markdown subset used by the Solano Ag documents: # / ## / ###
headings, paragraphs, **bold**, *italic*, `code`, > blockquote callouts, bullet
and numbered lists, pipe tables, fenced ``` code blocks, and --- rules.
"""

import base64
import html
import os
import re
import sys

# --- Brand assets (county seal + developer logo), embedded as data URIs so each
# --- page is fully self-contained for offline viewing and clean PDF printing.
_ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "assets")
_ASSET_CACHE = {}


def _data_uri(filename, mime):
    if filename in _ASSET_CACHE:
        return _ASSET_CACHE[filename]
    path = os.path.join(_ASSET_DIR, filename)
    uri = ""
    try:
        with open(path, "rb") as fh:
            uri = "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))
    except OSError:
        uri = ""
    _ASSET_CACHE[filename] = uri
    return uri


def _seal_uri():
    return _data_uri("seal.jpg", "image/jpeg")


def _logo_uri():
    return _data_uri("kci.png", "image/png")


def _inline(text):
    """Inline formatting: escape HTML, then apply bold/italic/code."""
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def _is_table_sep(line):
    return bool(re.match(r"^\s*\|?\s*:?-{2,}.*$", line)) and "-" in line and "|" in line


def _render_blocks(lines):
    """Render a list of Markdown lines to an HTML body fragment."""
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # Blank line
        if not line.strip():
            i += 1
            continue

        # Fenced code block (```lang ... ```): render as a labeled code box.
        m = re.match(r"^\s*```+\s*([A-Za-z0-9_+#-]*)\s*$", line)
        if m:
            lang = m.group(1)
            i += 1
            code_lines = []
            while i < n and not re.match(r"^\s*```+\s*$", lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # consume the closing fence
            label = (lang or "text").upper()
            code_html = html.escape("\n".join(code_lines))
            out.append(
                "<div class='codeblock'>"
                f"<div class='codelang'>{html.escape(label)}</div>"
                f"<pre><code class='language-{html.escape(lang or 'text')}'>{code_html}</code></pre>"
                "</div>"
            )
            continue

        # Horizontal rule
        if re.match(r"^\s*---+\s*$", line):
            out.append("<hr/>")
            i += 1
            continue

        # Blockquote callout (one or more consecutive > lines)
        if re.match(r"^\s*>\s?", line):
            quote = []
            while i < n and re.match(r"^\s*>\s?", lines[i]):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            paras = []
            buf = []
            for q in quote:
                if q.strip():
                    buf.append(q.strip())
                elif buf:
                    paras.append(" ".join(buf))
                    buf = []
            if buf:
                paras.append(" ".join(buf))
            body = "".join(f"<p>{_inline(p)}</p>" for p in paras) or "<p></p>"
            out.append(f"<blockquote>{body}</blockquote>")
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            if level == 2:
                num = re.match(r"^(\d+)\.\s+(.*)$", text)
                if num:
                    out.append(
                        f"<h2 id='sec-{num.group(1)}'>"
                        f"<span class='secnum'>{num.group(1)}</span>"
                        f"<span class='sectitle'>{_inline(num.group(2))}</span></h2>"
                    )
                else:
                    out.append(f"<h2>{_inline(text)}</h2>")
            else:
                out.append(f"<h{level}>{_inline(text)}</h{level}>")
            i += 1
            continue

        # Table: a pipe line followed by a separator line
        if "|" in line and i + 1 < n and _is_table_sep(lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2  # skip header + separator
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{_inline(c)}</th>" for c in header)
            tbody = ""
            for r in rows:
                r = (r + [""] * len(header))[: len(header)]
                tbody += "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>"
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        # Unordered list
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(_inline(re.sub(r"^\s*[-*]\s+", "", lines[i])))
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        # Ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(_inline(re.sub(r"^\s*\d+\.\s+", "", lines[i])))
                i += 1
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue

        # Paragraph (gather consecutive non-structural lines)
        para = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|\s*[-*]\s|\s*\d+\.\s|\s*>|\s*---+\s*$|\s*```)", lines[i]
        ) and not ("|" in lines[i]):
            para.append(lines[i])
            i += 1
        out.append("<p>" + _inline(" ".join(s.strip() for s in para)) + "</p>")

    return "\n".join(out)


def _masthead(title, doctype, subtitle, pdf_href=None):
    seal = _seal_uri()
    seal_img = (f"<img class='seal' src='{seal}' alt='Solano County Seal'/>" if seal else "")
    eyebrow = (f"<p class='doctype'>{html.escape(doctype.upper())}</p>" if doctype else "")
    sub = (f"<p class='subtitle'>{_inline(subtitle)}</p>" if subtitle else "")
    btn = (f"<a class='pdf-btn screen-only' href='{html.escape(pdf_href)}' download>"
           "&#8595;&nbsp;Download PDF</a>" if pdf_href else "")
    return (
        "<header class='masthead'>"
        f"<div class='mast-row'>{seal_img}<h1>{_inline(title)}</h1>{btn}</div>"
        f"{eyebrow}{sub}</header>"
    )


def _toc(sections):
    if len(sections) < 3:
        return ""
    items = "".join(
        f"<li><a href='#sec-{num}'>{html.escape(num)}. {_inline(title)}</a></li>"
        for num, title in sections
    )
    return (
        "<nav class='toc screen-safe'>"
        "<div class='toc-label'>Contents</div>"
        f"<ol>{items}</ol></nav>"
    )


def _footer(title):
    seal, logo = _seal_uri(), _logo_uri()
    left_img = (f"<img src='{seal}' alt='Solano County Seal'/>" if seal else "")
    right = ""
    if logo:
        right = (
            "<div class='foot-right'>"
            "<span class='lbl'>Solution developed by</span>"
            f"<img src='{logo}' alt='KCI Technologies'/></div>"
        )
    return (
        "<footer class='docfoot'>"
        f"<div class='foot-left'>{left_img}"
        f"<span>Solano County Agricultural Program — {html.escape(title)}</span></div>"
        f"{right}</footer>"
    )


def md_to_html_body(md, pdf_href=None):
    """Convert a Markdown document to an HTML body.

    A document that opens with an H1 (and optional italic subtitle) is wrapped in
    the branded .doc shell (masthead + auto TOC + footer). Bare fragments (no
    leading H1) render as a plain body so the function stays usable for snippets.
    When ``pdf_href`` is given, a screen-only "Download PDF" button is added to
    the masthead (omitted for print/PDF output).
    """
    # Strip HTML comments (e.g. the <!-- GENERATED:key --> injection markers)
    # so they never surface as escaped, visible text. Non-greedy so each comment
    # is removed individually and the content between paired markers is kept.
    md = re.sub(r"<!--.*?-->", "", md.lstrip("﻿"), flags=re.S)
    lines = md.splitlines()

    # Detect a leading H1 + optional italic subtitle -> masthead.
    j = 0
    while j < len(lines) and not lines[j].strip():
        j += 1
    h1 = re.match(r"^#\s+(.*)$", lines[j]) if j < len(lines) else None
    if not h1:
        return _render_blocks(lines)

    heading = h1.group(1).strip()
    if " — " in heading:
        title, doctype = heading.rsplit(" — ", 1)
    else:
        title, doctype = heading, ""
    rest = lines[j + 1:]
    # optional italic subtitle line (e.g. *Solano County ... · ...*)
    k = 0
    while k < len(rest) and not rest[k].strip():
        k += 1
    subtitle = ""
    if k < len(rest):
        sm = re.match(r"^\*(?!\*)(.+?)\*$", rest[k].strip())
        if sm:
            subtitle = sm.group(1).strip()
            rest = rest[k + 1:]

    sections = re.findall(r"(?m)^##\s+(\d+)\.\s+(.*)$", "\n".join(rest))
    body = _render_blocks(rest)
    return (
        "<article class='doc'>"
        + _masthead(title, doctype, subtitle, pdf_href)
        + _toc(sections)
        + body
        + _footer(title)
        + "</article>"
    )


CSS = """
:root{--blue:#00629e;--blue-dark:#045a90;--blue-050:#eef5fb;--blue-100:#cde1ef;
--ink:#1d2418;--ink-soft:#222;--muted:#555;--muted-blue:#4d6779;--paper:#fefefe;}
*{box-sizing:border-box;}
@page{size:letter;margin:0.7in;}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
 line-height:1.65;-webkit-font-smoothing:antialiased;}
.doc{max-width:840px;margin:0 auto;padding:32px clamp(18px,4vw,40px) 48px;}

/* masthead */
.masthead .mast-row{display:flex;align-items:center;gap:18px;border-bottom:3px solid var(--blue);
 padding-bottom:14px;margin:0 0 8px;}
.masthead .seal{width:58px;height:58px;object-fit:contain;border-radius:50%;flex:0 0 auto;}
.masthead h1{font-size:30px;font-weight:700;font-family:Georgia,'Times New Roman',serif;
 color:var(--blue);margin:0;letter-spacing:-.01em;line-height:1.15;}
.doctype{font-size:13px;font-weight:600;letter-spacing:.04em;color:var(--muted-blue);
 margin:10px 0 6px;text-transform:uppercase;}
.subtitle{font-size:14.5px;color:var(--muted);font-style:italic;margin:0 0 32px;}
.pdf-btn{margin-left:auto;flex:0 0 auto;align-self:center;display:inline-flex;align-items:center;
 background:var(--blue);color:#fff;text-decoration:none;font-size:12.5px;font-weight:600;
 font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
 padding:8px 15px;border-radius:8px;white-space:nowrap;}
.pdf-btn:hover{background:var(--blue-dark);}

/* table of contents */
nav.toc{margin:0 0 40px;padding:20px 24px;border:1px solid var(--blue-100);
 border-radius:12px;background:var(--blue-050);}
nav.toc .toc-label{font-size:11px;text-transform:uppercase;letter-spacing:.08em;
 color:var(--muted-blue);font-weight:700;margin-bottom:12px;}
nav.toc ol{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:8px 24px;}
nav.toc li{margin:0;}
nav.toc a{color:var(--blue);text-decoration:none;font-weight:600;font-size:14px;}
nav.toc a:hover{text-decoration:underline;}

/* headings */
h1{font-size:30px;font-family:Georgia,serif;color:var(--blue);}
h2{display:flex;align-items:center;gap:12px;font-size:21px;font-weight:700;
 font-family:Georgia,'Times New Roman',serif;color:var(--blue);margin:40px 0 18px;
 padding-bottom:10px;border-bottom:1px solid var(--blue-100);scroll-margin-top:16px;}
h2 .secnum{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;
 border-radius:8px;background:var(--blue);color:#fff;font-size:13px;font-weight:700;flex:0 0 auto;}
h3{font-size:16px;font-weight:700;font-family:Georgia,'Times New Roman',serif;
 color:var(--blue-dark);margin:26px 0 10px;}
h4{font-size:14px;font-weight:700;color:var(--ink);margin:18px 0 8px;}

/* body */
p{font-size:15px;color:var(--ink-soft);margin:0 0 14px;}
ul,ol{margin:0 0 14px 22px;padding:0;font-size:15px;color:var(--ink-soft);}
li{margin-bottom:6px;}
strong{font-weight:700;} em{color:var(--muted);}
a{color:var(--blue);}
hr{border:none;border-top:1px solid var(--blue-100);margin:26px 0;}

/* callouts */
blockquote{margin:16px 0;padding:12px 16px 12px 16px;background:var(--blue-050);
 border:1px solid var(--blue-100);border-left:4px solid var(--blue);border-radius:8px;
 font-size:14.5px;color:var(--ink-soft);}
blockquote p{margin:0 0 6px;font-size:14.5px;} blockquote p:last-child{margin:0;}

/* inline + block code */
code{background:#eaf1f8;padding:1px 5px;border-radius:3px;
 font-family:Consolas,'Courier New',monospace;font-size:.86em;color:#0b3a5b;}
.codeblock{margin:16px 0;border:1px solid var(--blue-100);border-radius:8px;overflow:hidden;}
.codelang{background:var(--blue);color:#fff;font-family:Consolas,'Courier New',monospace;
 font-size:8.5pt;letter-spacing:.06em;padding:4px 12px;text-transform:uppercase;}
pre{margin:0;padding:12px 14px;background:#f4f8fc;overflow-x:auto;}
pre code{background:none;padding:0;border-radius:0;color:#12354f;
 font-family:Consolas,'Courier New',monospace;font-size:12px;white-space:pre;}

/* tables */
table{width:100%;border-collapse:collapse;margin:6px 0 16px;font-size:13.5px;}
th{background:var(--blue);color:#fff;font-weight:600;text-align:left;padding:10px 14px;font-size:12.5px;}
td{padding:9px 14px;border-bottom:1px solid var(--blue-100);vertical-align:top;color:var(--ink-soft);}
td:first-child{font-weight:600;}
tbody tr:nth-child(odd) td{background:var(--blue-050);}

/* footer */
.docfoot{margin-top:52px;padding-top:20px;border-top:1px solid var(--blue-100);
 display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;}
.docfoot .foot-left{display:flex;align-items:center;gap:10px;}
.docfoot .foot-left img{width:22px;height:22px;object-fit:contain;border-radius:50%;flex:0 0 auto;}
.docfoot .foot-left span{font-size:12px;color:#8a8a8a;}
.docfoot .foot-right{display:flex;align-items:center;gap:10px;}
.docfoot .foot-right .lbl{font-size:10.5px;color:#8a8a8a;text-transform:uppercase;letter-spacing:.07em;}
.docfoot .foot-right img{height:26px;width:auto;display:block;}

@media print{
 html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 .doc{max-width:none;padding:0;}
 h1,h2,h3{break-after:avoid;}
 table,tr{break-inside:avoid;}
 .codeblock,blockquote{break-inside:avoid;}
 p,li{orphans:3;widows:3;}
 pre code{white-space:pre-wrap;word-break:break-word;}
 .screen-only{display:none !important;}
}
"""


def convert(md_path, title=None):
    with open(md_path, encoding="utf-8") as fh:
        md = fh.read()
    if not title:
        m = re.search(r"^#\s+(.*)$", md, re.M)
        title = m.group(1).strip() if m else os.path.splitext(os.path.basename(md_path))[0]
    body = md_to_html_body(md)
    doc = (
        "<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='utf-8'/>\n"
        f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n"
        f"<body>\n{body}\n</body>\n</html>\n"
    )
    out_path = os.path.splitext(md_path)[0] + ".html"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    out = convert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print("Wrote:", out)
