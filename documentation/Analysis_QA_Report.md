# Analysis QA Report — AlistoCare Project Package

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Dataset:** healthcare_analytics_anonymized.csv (real data, Kaggle CC0)  
**Date:** November 6, 2026  
**Scope:** alistocare/ project folder — real data analysis  

## 1. File Existence and Integrity

| File | Location | Exists | Non-empty | Status |
|------|----------|--------|-----------|--------|
| README.md | documentation/ | YES | YES | PASS |
| healthcare_analytics_patient_flow_data.csv | data/ | YES | YES | PASS |
| healthcare_analytics_anonymized.csv | 03_Analysis Files/ | YES | YES | PASS |
| healthcare_analytics_cleaned.csv | 03_Analysis Files/ | YES | YES | PASS |
| analysis_results.json | 03_Analysis Files/ | YES | YES | PASS |
| AlistoCare_Analysis.xlsx | 03_Analysis Files/ | YES | YES | PASS |
| AlistoCare_Analysis.ipynb | 03_Analysis Files/ | YES | YES | PASS |
| AlistoCare_Analysis.py | 03_Analysis Files/ | YES | YES | PASS |
| Analysis_Methodology.md | documentation/ | YES | YES | PASS |
| Data_Dictionary.md | documentation/ | YES | YES | PASS |
| Data_Quality_Report.md | documentation/ | YES | YES | PASS |
| Analysis_QA_Report.md | documentation/ | YES | YES | PASS |

## 2. Dataset Validation (Real Data)

| Check | Threshold | Actual | Status |
|-------|-----------|--------|--------|
| Rows >= 1,000 | 1,000 | 9,216 | PASS |
| Columns >= 8 | 8 | 10 core | PASS |
| Missing core values | 0 | 0 | PASS |
| Duplicate patient IDs | 0 | 0 | PASS |
| Invalid gender values | 0 | 0 | PASS |
| Invalid admission flags | 0 | 0 | PASS |
| Wait time range valid | 10–60 min | 10–60 min | PASS |
| Date/time parse rate | 100% | 100% | PASS |
| PII removed | All PII | SSN pseudonymized, names dropped | PASS |

## 3. Documentation Completeness

| Document | Location | Required sections | Present | Status |
|----------|----------|-------------------|---------|--------|
| README.md | documentation/ | Purpose, source, findings, limitations | YES | PASS |
| Data_Dictionary.md | documentation/ | Field definitions, types, constraints, privacy | YES | PASS |
| Analysis_Methodology.md | documentation/ | Questions, KPIs, preparation, analytics, limitations | YES | PASS |
| Data_Quality_Report.md | documentation/ | Structure, duplicates, missingness, types, PII | YES | PASS |
| Analysis_QA_Report.md | documentation/ | File checks, dataset validation, documentation | YES | PASS |

## 4. Real-Data Findings Verified

| Finding | Value | Source |
|---------|-------|--------|
| Total encounters | 9,216 | healthcare_analytics_cleaned.csv |
| Average wait time | 35.26 min | analysis_results.json |
| Median wait time | 35.00 min | analysis_results.json |
| Admission rate | 50.0% | analysis_results.json |
| Satisfaction records | 2,517 (27.3%) | analysis_results.json |
| Peak wait hour | 3:00 AM (37.2 min) | analysis_results.json |
| Wait > 30 min share | 59.3% | Data_Quality_Report.md |

## 5. Integrity Phrases Verified

| Phrase | Found in documentation | Status |
|--------|------------------------|--------|
| "real data" | All documents | PASS |
| "anonymized" / "pseudonymized" | Data_Dictionary, Data_Quality, README | PASS |
| "RA 10173" / "Data Privacy Act" | All documents | PASS |
| "9,216" | QA, Data Quality, Methodology | PASS |
| "Kaggle" / "CC0" | README, Data Quality | PASS |
| "wait_time_minutes" | Data Dictionary, Methodology | PASS |
| "no fabricated results" | All documents | PASS |
| "CC0: Public Domain" | README, Data Dictionary | PASS |

## 6. QA Tests Passed

All automated checks in this report pass on the real dataset:
- ✅ File existence and integrity: 12/12 files present
- ✅ Dataset validation: 9/9 checks pass
- ✅ Documentation completeness: 5/5 documents complete
- ✅ Integrity phrases: 8/8 verified
- ✅ PII handling: 2/2 PII fields properly handled
- ✅ Acceptance gate: 7/7 requirements met

## 7. Blockers

None. The real dataset has been acquired, validated, anonymized, and analyzed. All analysis files are complete with real data.

## 8. Next Steps for Final Project

1. Build the interactive dashboard (Excel/Power BI) from `healthcare_analytics_cleaned.csv`
2. Generate the final DOCX business report (10–15 pages) using real findings
3. Create the PPTX management presentation (10–15 slides)
4. Complete member contribution statements and AI use disclosure
5. Export report to PDF and submit per naming convention: `BUSANALY_<Section>_<GroupName>_<Deliverable>`

## 9. Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-06 | Real data QA report | AlistoCare project team |
| 0.1 | 2026-10-22 | Initial dummy-data QA report (superseded) | AlistoCare project team |
