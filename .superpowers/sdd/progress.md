# SDD Progress Ledger — Solano Ag Documentation System

Plan: `docs/superpowers/plans/2026-07-01-documentation-system.md`
Started: 2026-07-01

(Supersedes the 2026-06-29 KB/Requirements ledger. GWSS, W&I, and IST Knowledge
Base + Requirements were authored inline earlier this session; PQ and
Plant/Pest/Other are folded into Task 12 below.)

## Task Status

- Task 1: COMPLETE (commit de6e843, verified clean) — repository skeleton, git, shared renderer
- Task 2: COMPLETE (commit 0700ef3, compiles) — copy JSON extractor into tooling/
- Task 3: COMPLETE (commit c2ca0ec, all 3 apps have content+json-export) — migrate finished apps
- Task 4: COMPLETE (commits 372e208..b4cdc2a, spec ✅, Important fix applied) — generate_tech_reference.py
- Task 5: COMPLETE (commits 4d47e38..f59961e, spec ✅, Important+Minor fixes applied) — build_site.py
- Task 6: COMPLETE (commit dab787e, spec ✅ quality approved; Edge confirmed present) — build_pdf.py
- Task 7: COMPLETE (commit 479d012, verified: 8 site pages built) — build.py orchestrator
- Task 8: COMPLETE (commit 8569a71, 6 marker keys match generator) — document templates
- Task 9: COMPLETE (commits 4acbdbf..ba18c27, spec ✅, no secrets, 8/8 views w/ SQL) — GWSS technical reference (pilot)
- Task 10: COMPLETE (W&I 7bced18, IST e0dc16e, fixes 049f095; spec ✅ both, no secrets; IST 2 views + 5 rules verbatim) — W&I and IST technical references
- Task 11: COMPLETE (commit 11569b6, verified: 9 html + 9 pdf, no secrets, legacy removed) — full build, verification, cleanup
- Task 12: COMPLETE — PQ (commit 0ef970a) + Plant/Pest/Other (commit 3c6655a); vendor source material later incorporated (commit 1da989c). 17 site pages + 15 PDFs, 12/12 tests pass, no secrets in deliverables.
  - Source-material pass (1da989c): read KCI tech docs + user guides for both apps; added notes/source-material-notes.md for each. **PQ fix:** tech ref had wrongly said "no views" — actually has v_pq_inspection_tracking_all + v_pq_inspection_tracking_status (SQL added), plus PQ_Inspection_Tracking_Views MapServer, Pro path, Inbox lifecycle, CSVs, enhancement history, POC Daniel Machado. **PPO fix:** rewrote to the true related-records model (Address Points from SC_Prime + Inspection Points → 1:M Plant Pest and Other Inspections table + 2 combining views), inspection types (SOD/SLF/BW/AWB/ESFY + Resident Complaint/CDFA/County Follow Up), POC Matthew Carl.
  - Still-open follow-up: PPO PPS_Plant_Pest_Other_Insp FeatureServer + PlantPestandSurveys_Views MapServer were offline at export — insp_type/insp_status domains and the two PPO view SQL defs still need retrieval from the live service / pgAdmin (umbrella vendor doc appendix holds GWSS views, not PPO's).

## Visual design system (commit bf14373, 2026-07-10)

The build pipeline now renders every app in the **Solano-blue design system**,
reverse-engineered from the GWSS Knowledge Base template artifact the user
placed in build/site (a self-extracting Claude-artifact bundle; the real HTML +
assets were base64/gzip inside `<script type="__bundler/template">` and
`__bundler/manifest`). Design lives entirely in `tooling/md_to_html.py` CSS +
`build_site.py` shell — no per-doc markup. Components: county-seal masthead
(from H1 + italic subtitle + uppercase doc-type eyebrow), auto 2-col "Contents"
TOC from numbered `## N.` sections, blue section-number badges on H2, callout
boxes from `>` blockquotes (also fixed a latent bug where `>` leaked as literal
text), themed tables (blue header/zebra/bold first col), blue SQL/code blocks,
KCI footer. Seal + KCI logo live at `source/assets/{seal.jpg,kci.png}` and are
embedded as base64 data URIs so pages are self-contained for offline + PDF.
Palette: --blue #00629e, --blue-dark #045a90, --blue-050 #eef5fb, --blue-100
#cde1ef; headings Georgia serif, body system sans. Both build_site and build_pdf
flow through md_to_html, so the site and PDFs share the design.

## Completed Tasks

ALL TASKS COMPLETE (Tasks 1–12) + visual design system applied. Final
deliverable: build/site (17 pages + index + search) and build/pdf (15 PDFs).
12/12 tests pass, no secrets. Post-review fix d2bc24e: PDF intermediate HTML
renders under build/. Task 12 follow-up needed: Plant/Pest/Other
schema/domains/views are incomplete — PPS_Plant_Pest_Other_Insp service was
offline at export time; re-export when service is running to fill gaps.

Deferred cleanup follow-ups (non-blocking, see Minor findings): lexicographic
_latest_export sort, hardcoded ../ sidebar depth, broad services filter, prefix
match in _find_item_dir.

## Minor findings (for final review)

- Task 4 (generate_tech_reference.py): `domain_map` is last-writer-wins on domain-name collisions across layers (no dedup/warning). Unlikely within a single-app export.
- Task 4 (generate_tech_reference.py): `_latest_export` uses lexicographic `sorted(subs)[-1]`; correct only while export folders keep the date-stamped `json_export_YYYYMMDD…` naming. Worth a code comment.
- Task 5 (build_site.py): `_page_html` hardcodes `../` for sidebar links, assuming every doc page is exactly one level deep. Correct today; would break if `out_rel` ever became deeper. Worth a comment/guard.
- Task 9/generator (generate_tech_reference.py): the `services` section includes any item with layers or "Service" in its type, so basemap/imagery services appear alongside the app's core services (broad but not wrong). Consider tightening the services filter, or renaming the section to "Services & Referenced Layers".
- Task 10 (W&I): generated schema shows the layer by alias "WI - Treatment Tracking" while narrative refers to db name "wi_treatment_tracking" — cosmetic alias-vs-dbname mismatch.
- Task 10 (IST): Section 3 notes the shared ArcGIS Pro project path (PlantsPestSurvey_Prod) — accurate to source (shared project), but may surprise a reader expecting an IST-specific path.
