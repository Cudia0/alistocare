# 03_Analysis Files — AlistoCare BUSANALY Final Project

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Status:** Real data analysis complete  
**Date:** November 6, 2026  
**Location:** `03_Analysis Files/`

## Purpose

This folder contains the data analysis materials for the AlistoCare BUSANALY final project, built on a verified real-world dataset acquired from Kaggle.

| File | Description | Location |
|------|-------------|----------|
| `healthcare_analytics_patient_flow_data.csv` | Original dataset downloaded from Kaggle (9,216 rows, 11 columns) | `data/` |
| `healthcare_analytics_anonymized.csv` | Anonymized version (PII removed per RA 10173) | `03_Analysis Files/` |
| `healthcare_analytics_cleaned.csv` | Cleaned dataset with parsed dates, derived fields (9,216 rows) | `03_Analysis Files/` |
| `analysis_results.json` | Computed summary statistics and key metrics | `03_Analysis Files/` |
| `AlistoCare_Analysis.xlsx` | Excel workbook with metadata, data dictionary, QA, KPIs, findings | `03_Analysis Files/` |
| `AlistoCare_Analysis.ipynb` | Reproducible Python analysis notebook | `03_Analysis Files/` |
| `AlistoCare_Analysis.py` | Standalone Python analysis script | `03_Analysis Files/` |
| `Analysis_Methodology.md` | Methods, formulas, assumptions, limitations, reproducibility | `documentation/` |
| `Data_Dictionary.md` | Field definitions, types, units, constraints | `documentation/` |
| `Data_Quality_Report.md` | Validation results: duplicates, missingness, types, PII handling | `documentation/` |
| `Analysis_QA_Report.md` | Package-level QA test results | `documentation/` |
| `README.md` | Project overview and real-data findings | `documentation/` |

## Dataset Source

**Title:** Healthcare Analytics Patient Flow Data  
**Creator:** Hassan Jameel Ahmed  
**Platform:** Kaggle  
**URL:** https://www.kaggle.com/datasets/hassanjameelahmed/healthcare-analytics-patient-flow-data  
**License:** CC0: Public Domain  
**Download date:** November 6, 2026  
**Original rows:** 9,216 | **Original columns:** 11  
**Date range:** January 4, 2023 – December 10, 2024  
**File size:** 864,047 bytes

## Anonymization (RA 10173 Compliance)

The original dataset contained personally identifiable information (PII):

| Field | PII Type | Action Taken |
|-------|----------|--------------|
| `Patient Id` | SSN-format identifier (XXX-XX-XXXX) | Replaced with SHA-256 pseudonym (PID-XXXXXXXXXXXX) |
| `Merged` | Patient names (e.g., "W. Breede") | Column dropped entirely |

No patient names, contact details, or direct identifiers remain in the analysis dataset. Complies with the Data Privacy Act of 2012 (RA 10173).

## Key Findings (Real Data)

| Metric | Value |
|--------|-------|
| Total patient encounters | 9,216 |
| Average wait time | 35.26 minutes |
| Median wait time | 35.00 minutes |
| Wait time range | 10 – 60 minutes |
| Admission rate | 50.0% |
| Average patient age | 39.9 years |
| Satisfaction records | 2,517 (27.3% of total) |
| Department records | 3,816 (41.4% of total) |
| Peak wait hour | 3:00 AM (37.2 min avg) |
| Lowest wait hour | 12:00 PM (33.9 min avg) |
| Correlation: wait time vs satisfaction | -0.021 (negligible) |

## Analysis Scope

1. **Descriptive analytics:** Patient volume by date, department, day of week, hour; wait time distributions
2. **Diagnostic analytics:** Department-level wait time comparisons; admission vs non-admission wait patterns; satisfaction correlation
3. **Predictive demonstration:** Wait time category classification using patient and operational variables
4. **Prescriptive demonstration:** Staffing and capacity planning scenarios based on wait time patterns

## Data Status

✅ **Real dataset acquired and validated** — This analysis uses actual patient encounter data. No synthetic or fabricated records are included.

## Limitations

- Dataset covers a single medium-sized hospital facility; may not represent Philippine community health centers nationwide
- Satisfaction scores only available for 27.3% of encounters
- Department referral missing for 58.6% of encounters
- No patient-level queue position or consultation duration data
- Cannot directly measure AlistoCare effectiveness (system not yet piloted)
