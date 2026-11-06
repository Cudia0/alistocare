# Data Quality Report — AlistoCare Analysis Dataset

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Dataset:** healthcare_analytics_anonymized.csv (real data)  
**Source:** Kaggle — Healthcare Analytics Patient Flow Data (CC0: Public Domain)  
**Date:** November 6, 2026  

## 1. Dataset Identity

| Property | Value |
|----------|-------|
| Original file name | `healthcare_analytics_patient_flow_data.csv` |
| Anonymized file name | `healthcare_analytics_anonymized.csv` |
| Cleaned file name | `healthcare_analytics_cleaned.csv` |
| Format | CSV (UTF-8) |
| Total rows | 9,216 |
| Total columns (core) | 10 |
| Total columns (with derived) | 19 |
| Unit of observation | One patient encounter |
| Coverage period | January 4, 2023 – December 10, 2024 |
| License | CC0: Public Domain |
| Download date | November 6, 2026 |
| Source URL | https://www.kaggle.com/datasets/hassanjameelahmed/healthcare-analytics-patient-flow-data |
| Status | Real data — anonymized per RA 10173 |

## 2. Structural Validation

| Check | Result | Detail |
|-------|--------|--------|
| Minimum 1,000 rows | PASS | 9,216 rows |
| Minimum 8 variables | PASS | 10 core variables (19 with derived) |
| Column count matches header | PASS | All columns present |
| No duplicate column names | PASS | All unique |
| File encoding valid | PASS | UTF-8 |
| No completely empty rows | PASS | 0 empty rows |
| No completely empty columns | PASS | 0 empty columns |
| Date/time parsing success | PASS | 100% of records parsed |

## 3. Duplicate Row Check

| Check | Result | Count |
|-------|--------|-------|
| Exact duplicate rows | PASS | 0 |
| Duplicate `patient_id` values | PASS | 0 (all unique) |

## 4. Missing Value Analysis (Core Fields)

| Field | Missing count | Missing % | Policy |
|-------|---------------|-----------|--------|
| patient_id | 0 | 0.00% | Complete — required |
| admission_date | 0 | 0.00% | Complete — required |
| admission_time | 0 | 0.00% | Complete — required |
| gender | 0 | 0.00% | Complete — required |
| age | 0 | 0.00% | Complete — required |
| race | 0 | 0.00% | Complete — required |
| admission_flag | 0 | 0.00% | Complete — required |
| wait_time_minutes | 0 | 0.00% | Complete — required |
| department | 5,400 | 58.59% | Documented missing; not imputed |
| satisfaction_score | 6,699 | 72.69% | Documented missing; not imputed |

**Total missing values in core required fields: 0**  
**Total missing values across all fields: 12,099**

## 5. PII and Privacy Handling (RA 10173)

| Original Field | PII Type | Action | Status |
|----------------|----------|--------|--------|
| `Patient Id` | SSN-format (XXX-XX-XXXX) | SHA-256 pseudonymized → `patient_id` | ✅ Resolved |
| `Merged` | Patient names | Column dropped | ✅ Resolved |

No direct identifiers remain in the anonymized dataset.

## 6. Data Type Validation

| Field | Expected type | Observed type | Status |
|-------|---------------|---------------|--------|
| patient_id | String | object | PASS |
| admission_date | Date | object (string) | PASS (parsed as datetime) |
| admission_time | Time | object (string) | PASS (parsed as time) |
| gender | Category | object | PASS |
| age | Integer | int64 | PASS |
| race | Category | object | PASS |
| department | Category | object | PASS |
| admission_flag | Category | object | PASS |
| satisfaction_score | Numeric | float64 | PASS |
| wait_time_minutes | Integer | int64 | PASS |

## 7. Value Range and Enum Validation

| Field | Allowed values | Invalid count | Status |
|-------|---------------|---------------|--------|
| gender | Female, Male | 0 (after fix) | PASS |
| admission_flag | Admission, Not Admission | 0 | PASS |
| wait_time_minutes | 10–60 (observed range) | 0 | PASS |
| satisfaction_score | 0–10 | 0 | PASS |
| age | 0–100+ | 0 | PASS |
| department | 7 valid departments | 0 invalid values | PASS (missing ≠ invalid) |

**Gender fix applied:** "Femaleemale" (17 records) → "Female"

## 8. Distinct Value Counts

| Field | Distinct values |
|-------|-----------------|
| patient_id | 9,216 |
| admission_date | 579 unique dates |
| admission_time | 1,437 unique times |
| gender | 2 |
| age | 79 unique values |
| race | 7 |
| department | 7 |
| admission_flag | 2 |
| satisfaction_score | 11 (0–10) |
| wait_time_minutes | 51 |

## 9. Department Coverage

| Department | Encounters | % of department-reported |
|------------|-----------|-------------------------|
| General Practice | 1,840 | 48.2% |
| Orthopedics | 995 | 26.1% |
| Physiotherapy | 276 | 7.2% |
| Cardiology | 248 | 6.5% |
| Neurology | 193 | 5.1% |
| Gastroenterology | 178 | 4.7% |
| Renal | 86 | 2.3% |
| **Total with department** | **3,816** | **100%** |
| Missing department | 5,400 | 58.6% of all records |

## 10. Wait Time Distribution

| Category | Count | % |
|----------|-------|-----|
| 0–15 min | 1,082 | 11.7% |
| 16–30 min | 2,667 | 28.9% |
| 31–45 min | 2,717 | 29.5% |
| 46–60 min | 2,750 | 29.8% |

**59.3% of patients wait more than 30 minutes.**

## 11. Data Quality Issues Identified

| Issue | Severity | Resolution |
|-------|----------|------------|
| PII in Patient Id (SSN format) | High | Pseudonymized with SHA-256 hash |
| PII in Merged column (patient names) | High | Column dropped entirely |
| Gender data entry error ("Femaleemale") | Low | Corrected to "Female" |
| Missing department (58.6%) | Medium | Documented; not imputed; excluded from dept-level analysis where needed |
| Missing satisfaction (72.7%) | High | Documented; not imputed; satisfaction analysis limited to available records |
| Single facility scope | Medium | Documented limitation; results may not generalize |

## 12. Acceptance Gate (Real Data)

| Requirement | Threshold | Actual | Status |
|-------------|-----------|--------|--------|
| At least 1,000 usable rows | 1,000 | 9,216 | PASS |
| At least 8 usable variables | 8 | 10 core (19 with derived) | PASS |
| Core fields complete (no missing) | 0 missing | 0 missing in core fields | PASS |
| No duplicate patient IDs | 0 duplicates | 0 duplicates | PASS |
| Date/time parseable | 100% | 100% parsed | PASS |
| PII removed/anonymized | All PII handled | SSN pseudonymized; names dropped | PASS |
| Real, verifiable data | N/A | Kaggle CC0 dataset | PASS |

**Dataset meets all BUSANALY Final Project requirements.**

## Related Documentation

- [Project Overview — Root README](../README.md)
- [Project Proposal — BUSANALY Format](../02_ProjectProposal/Project_Proposal_AlistoCare.md)
- [Analysis Folder README](../03_Analysis%20Files/README.md)
- [Data Dictionary](Data_Dictionary.md)
- [Analysis Methodology](Analysis_Methodology.md)
- [Analysis QA Report](Analysis_QA_Report.md)

## 13. Next Steps

1. Use `healthcare_analytics_cleaned.csv` for all analysis
2. Run `AlistoCare_Analysis.py` or `AlistoCare.ipynb` to reproduce results
3. Update `AlistoCare_Analysis.xlsx` with computed findings
4. Build dashboard from validated outputs
5. Write final report with real-data findings and recommendations

## 14. Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-06 | Real data quality report | AlistoCare project team |
| 0.1 | 2026-10-22 | Initial dummy-data quality report (superseded) | AlistoCare project team |
