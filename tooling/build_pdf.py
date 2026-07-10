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
        with open(md_path, encoding="utf-8") as fh:
            md = fh.read()
        html_str = ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
                    + md_to_html.CSS + "</style></head><body>"
                    + md_to_html.md_to_html_body(md) + "</body></html>")
        html_path = os.path.join(out_dir, slug, doc + ".html")
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(html_str)
        pdf_path = os.path.join(out_dir, slug, doc + ".pdf")
        html_to_pdf(edge, html_path, pdf_path)
        written.append(pdf_path)
    return written


if __name__ == "__main__":
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "pdf")
    for p in build(root, out):
        print("Wrote", p)
