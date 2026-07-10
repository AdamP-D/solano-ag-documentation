# Task 9 Report: GWSS Technical Reference (Pilot)

**File:** `source/apps/gwss/content/technical-reference.md`
**Commit:** `4acbdbf`

## Sections Authored (hand-written narrative)

| Section | Content |
|---|---|
| 1. Solution Architecture | Field Maps web map + GWSS Tracking and Management Web AppBuilder app; four referenced PostgreSQL services (no hosted services); GP quarter-mile buffer/tagging tool; Smart Editor widget; Geoprocessing widget |
| 3. Services & Publishing (narrative) | All data referenced from GWSS PostgreSQL DB; ArcGIS Pro project on `\\gis.solanocountygis.local\E\ServiceUpdates\GWSS`; domain updates require stopping and restarting ALL four GWSS services; relationship ID re-ordering caveat documented |
| 8. Database View Definitions | All 8 published views with one-line purpose and verbatim SQL from KCI Technical Documentation appendix |
| 9. Attribute Rules | "None documented; status and symbology are driven by the database views in Section 8" |
| 10. Geoprocessing / Automation | GWSSQuarterMileAnalysis_ParcelInspectionTag: 5-step process (select findings, buffer, select parcels, tag gwss_action="Requires Inspection", write tracking history) |
| 11. Map / App Layer Definitions | survey_result categories (Infested/Adjacent/Clear/Survey Incomplete/Refused Survey); treatment_status categories (13 values including partial refusal); gwss_action; reference layers (Trap Grids, Quar Boundary, Biological Control); purple "Partial Refusal" case documented |

## Auto-Generated Sections (injected by generate_tech_reference.py)

Sections 2, 4, 5, 6, 7 (portal-items, schema, domains, subtypes, relationships) — injected from `json_export_20260630_134912/`.

## Views Included with SQL

**8 of 8** views included with verbatim SQL:
1. v_gwss_all_findings
2. v_gwss_all_surveys
3. v_gwss_all_treatments
4. v_gwss_most_recent_survey_per_parcel
5. v_gwss_most_recent_treatment_per_parcel
6. v_gwss_parcels_related_quarter_mile_buffer
7. v_gwss_recent_surveys_six_weeks
8. v_gwss_treatments_past_year

(The ninth back-end-only view, `v_gwss_what_parcels_in_buffer_have_surveys`, is mentioned by name but its SQL is not included since it is not published as a service layer.)

## Step-5 Grep Results

```
grep -c "GWSS Tracking"  → 17  (non-zero: PASS)
grep -c "gwss_action|Requires Inspection" → 15  (non-zero: PASS)
grep -c "<REDACTED-DB-PASSWORD>" → 0 + "no-secret-good"  (PASS — no password in output)
```

## Commit

`4acbdbf` — "docs: GWSS technical reference (pilot)"
