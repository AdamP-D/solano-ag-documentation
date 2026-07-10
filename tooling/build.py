"""Orchestrate the documentation build: regenerate tech-ref factual sections from
JSON, build the static site, and export PDFs. Standard library only."""
import glob
import os
import shutil
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

    # 3) Build PDFs, then copy them into the site tree so the on-page
    #    "Download PDF" buttons resolve when only build/site is hosted.
    if not no_pdf:
        pdf_out = os.path.join(REPO, "build", "pdf")
        pdfs = build_pdf.build(source, pdf_out)
        print("pdfs:", len(pdfs))
        for pdf in pdfs:
            dest = os.path.join(site_out, os.path.relpath(pdf, pdf_out))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(pdf, dest)
        if pdfs:
            print("copied", len(pdfs), "PDFs into", site_out)
    else:
        print("skipped PDFs (--no-pdf) — Download PDF buttons will 404 until a full build")


if __name__ == "__main__":
    main()
