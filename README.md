# AlistoCare: Health Center Queue Companion

**BUSANALY: Business Analytics — Final Project**  
**Group:** AlistoCare Analytics Team  
**Status:** Dataset acquired, validated, and analyzed  
**Repository:** https://github.com/Cudia0/alistocare

---

## Project Overview

AlistoCare is a proposed digital queue management system for community health centers. This project analyzes real patient flow data to understand wait time patterns, identify high-demand departments and time periods, and inform the design and pilot planning of AlistoCare.

**Dataset:** Healthcare Analytics Patient Flow Data (Kaggle, CC0 Public Domain)  
**Records:** 9,216 patient encounters | **Period:** January 4, 2023 – December 10, 2024  
**Privacy:** PII anonymized per Data Privacy Act of 2012 (RA 10173) — SSN-format IDs pseudonymized, name column dropped

---

## Key Findings (Real Data)

| Metric | Value |
|--------|-------|
| Total patient encounters | 9,216 |
| Average wait time | 35.26 minutes |
| Median wait time | 35.00 minutes |
| Admission rate | 50.0% |
| Patients waiting > 30 min | 59.3% |
| Peak wait hour | 3:00 AM (37.2 min avg) |
| Correlation: wait time vs satisfaction | -0.021 (negligible) |

---

## Repository Structure

```
alistocare/
├── 02_ProjectProposal/          Project proposal documents
├── 03_Analysis Files/           Analysis deliverables (BUSANALY Deliverable #4)
├── data/                        Source datasets
└── documentation/               Methodology, data dictionary, QA reports
```

---

## Documentation Navigation

All Markdown files in this project are cross-linked below for easy navigation:

### 📋 Project Proposal
- [Project Proposal — AlistoCare (BUSANALY format)](02_ProjectProposal/Project_Proposal_AlistoCare.md)

### 📊 03_Analysis Files (Analysis Deliverables)
- [README — Analysis Folder Overview](03_Analysis%20Files/README.md)

### 📖 Documentation
- [README — Project Overview](documentation/README.md)
- [Data Dictionary — Field Definitions](documentation/Data_Dictionary.md)
- [Analysis Methodology — Questions, KPIs, Cleaning](documentation/Analysis_Methodology.md)
- [Data Quality Report — Validation & Acceptance Gate](documentation/Data_Quality_Report.md)
- [Analysis QA Report — Package Testing](documentation/Analysis_QA_Report.md)

### 📁 Source Data
- Original Kaggle dataset: `data/healthcare_analytics_patient_flow_data.csv`
- Anonymized dataset: `03_Analysis Files/healthcare_analytics_anonymized.csv`
- Cleaned dataset: `03_Analysis Files/healthcare_analytics_cleaned.csv`

---

## BUSANALY Deliverables Status

| Deliverable | Due | Status |
|-------------|-----|--------|
| Group Registration | Oct 22, 2026 | ✅ Completed |
| Project Proposal | Oct 22, 2026 | ✅ Completed |
| Progress Check | Oct 27, 2026 | ⏳ Pending |
| Analysis Files | Nov 3, 2026 | ✅ Completed (Colab tested) |
| Dashboard | Nov 10, 2026 | ⏳ Pending |
| Business Report | TBD | ⏳ Pending |
| Management Presentation | TBD | ⏳ Pending |

## Code Compatibility

- **`AlistoCare_Analysis.py`** — Google Colab compatible (file upload helper, no `__file__` dependency)
- **`AlistoCare_Analysis.ipynb`** — Google Colab compatible (upload cell at setup)
- Both scripts tested end-to-end in Colab: 9,216 rows loaded, all validation checks PASS, all analytics execute without errors

---

## Requirements Compliance

- ✅ Real business data from credible public source (Kaggle CC0)
- ✅ Minimum 1,000 rows (9,216 actual)
- ✅ Minimum 8 variables (10 core, 19 with derived fields)
- ✅ Documented source with URL and retrieval date
- ✅ PII anonymized per RA 10173
- ✅ Descriptive, diagnostic, predictive, and prescriptive analysis covered
- ✅ Reproducible code (Python script + Jupyter notebook + Excel workbook)
- ✅ No fabricated data or results

---

## Next Steps

1. Build the interactive dashboard (Excel/Power BI) from `healthcare_analytics_cleaned.csv`
2. Generate the final DOCX business report (10–15 pages) using real findings
3. Create the PPTX management presentation (10–15 slides)
4. Complete member contribution statements and AI use disclosure
5. Export report to PDF and submit per naming convention: `BUSANALY_<Section>_<GroupName>_<Deliverable>`

---

**Maintained by:** AlistoCare Analytics Team  
**Last updated:** November 6, 2026
