# 03_Analysis Files — AlistoCare BUSANALY Final Project

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Status:** Real data analysis complete  
**Date:** November 6, 2026  

## Purpose

This folder contains the data analysis deliverables for the AlistoCare BUSANALY final project, as required by Section 5, Deliverable #4 of the project guidelines:

> **Analysis Files:** Excel workbook, Python/R notebook, and/or SQL scripts with data (Due: November 3, 2026)

All files use a verified real-world dataset — no synthetic or fabricated records.

## Files in This Folder

| File | Description |
|------|-------------|
| `AlistoCare_Transform.py` | Data transformation script — original → anonymized → cleaned (Colab compatible) |
| `healthcare_analytics_cleaned.csv` | Cleaned dataset with parsed dates and derived fields (9,216 rows, 19 columns) |
| `healthcare_analytics_anonymized.csv` | Anonymized version (PII removed per RA 10173) |
| `analysis_results.json` | Computed summary statistics and key metrics |
| `AlistoCare_Analysis.xlsx` | Excel workbook (6 sheets: Source_Metadata, Data_Dictionary, QA_Checklist, KPI_Definitions, Findings_Log, Recommendations) |
| `AlistoCare_Analysis.py` | Standalone Python analysis script |
| `AlistoCare_Analysis.ipynb` | Jupyter notebook with the same workflow |

## Dataset Source

**Title:** Healthcare Analytics Patient Flow Data  
**Creator:** Hassan Jameel Ahmed  
**Platform:** Kaggle  
**URL:** https://www.kaggle.com/datasets/hassanjameelahmed/healthcare-analytics-patient-flow-data  
**License:** CC0: Public Domain  
**Download date:** November 6, 2026  
**Rows:** 9,216 | **Columns:** 10 core fields  
**Coverage:** January 4, 2023 – December 10, 2024  

## Anonymization (RA 10173 Compliance)

| Original Field | PII Type | Action Taken |
|----------------|----------|--------------|
| `Patient Id` | SSN-format (XXX-XX-XXXX) | SHA-256 pseudonymized → `patient_id` |
| `Merged` | Patient names | Column dropped entirely |

No patient names, contact details, or direct identifiers remain.

## Key Findings (Real Data)

| Metric | Value |
|--------|-------|
| Total patient encounters | 9,216 |
| Average wait time | 35.26 minutes |
| Median wait time | 35.00 minutes |
| Wait time range | 10 – 60 minutes |
| Admission rate | 50.0% |
| Average patient age | 39.9 years |
| Satisfaction records | 2,517 (27.3%) |
| Department records | 3,816 (41.4%) |
| Peak wait hour | 3:00 AM (37.2 min avg) |
| Patients waiting >30 min | 59.3% |

## Requirements Met (BUSANALY Guidelines)

- ✅ Real business data from credible public source (Kaggle CC0)
- ✅ Minimum 1,000 rows (9,216 actual)
- ✅ Minimum 8 variables (10 core, 19 with derived)
- ✅ Documented source with URL and retrieval date
- ✅ PII anonymized per RA 10173
- ✅ Descriptive, diagnostic, predictive, and prescriptive analysis
- ✅ Reproducible code (Python script + Jupyter notebook)
- ✅ No fabricated data or results

## Related Documentation

Additional documentation is in the `documentation/` folder:
- `README.md` — Project overview and source details
- `Data_Dictionary.md` — Field definitions and constraints
- `Analysis_Methodology.md` — Questions, KPIs, cleaning steps, analytics plan
- `Data_Quality_Report.md` — Validation results and acceptance gate
- `Analysis_QA_Report.md` — QA test results

## Project Proposal

The BUSANALY-formatted project proposal is in `02_ProjectProposal/Project_Proposal_AlistoCare.md`, which connects to this analysis work using the same real dataset.
