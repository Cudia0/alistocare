# Data Dictionary — AlistoCare Analysis Dataset

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Dataset:** healthcare_analytics_anonymized.csv (real data)  
**Source:** Kaggle — Healthcare Analytics Patient Flow Data (CC0: Public Domain)  
**Date:** November 6, 2026  

## Dataset Overview

| Property | Value |
|----------|-------|
| File name | `healthcare_analytics_cleaned.csv` |
| Original file | `healthcare_analytics_patient_flow_data.csv` |
| Format | Comma-separated values (CSV) |
| Rows | 9,216 patient encounters |
| Variables | 10 core fields + 9 derived fields |
| Unit of observation | One patient encounter record |
| Coverage period | January 4, 2023 – December 10, 2024 |
| Geographic scope | Single medium-sized hospital facility (location not specified) |
| License | CC0: Public Domain |
| Status | **Real data — anonymized per RA 10173** |

## Anonymization Summary (RA 10173 Compliance)

| Original Field | PII Type | Action |
|----------------|----------|--------|
| `Patient Id` | SSN-format identifier (XXX-XX-XXXX) | Replaced with SHA-256 pseudonym `PID-XXXXXXXXXXXX` |
| `Merged` | Patient names | Column dropped entirely |

## Core Fields (from Source Dataset)

| # | Field | Type | Description | Example values | Constraints |
|---|-------|------|-------------|----------------|-------------|
| 1 | `patient_id` | String (Text) | Pseudonymized patient identifier | PID-a1b2c3d4e5f6 | Unique per patient; no missing values |
| 2 | `admission_date` | Date | Patient admission date | 9/9/2024 | Format: M/D/YYYY; no missing values |
| 3 | `admission_time` | Time | Patient admission time | 9:25:00 AM | Format: H:MM:SS AM/PM; no missing values |
| 4 | `gender` | Category | Patient gender | Female, Male | No missing values |
| 5 | `age` | Integer | Patient age in years | 63 | Range: 0–100+; no missing values |
| 6 | `race` | Category | Patient race/ethnicity | African American, White, Asian | 7 categories; no missing values |
| 7 | `department` | Category | Department referred to | General Practice, Orthopedics, Cardiology | 7 departments; 58.6% missing |
| 8 | `admission_flag` | Category | Whether patient was admitted | Admission, Not Admission | No missing values |
| 9 | `satisfaction_score` | Numeric (float) | Patient satisfaction rating (0–10) | 5.0, 7.0 | 72.7% missing |
| 10 | `wait_time_minutes` | Integer | Patient wait time in minutes | 32, 15 | Range: 10–60; no missing values |

## Derived Fields (Computed During Analysis)

| # | Field | Type | Formula / Derivation | Description |
|---|-------|------|----------------------|-------------|
| 11 | `admission_datetime` | DateTime | Combination of `admission_date` + `admission_time` | Full admission timestamp |
| 12 | `date` | Date | Extracted from `admission_datetime` | Service date (YYYY-MM-DD) |
| 13 | `day_of_week` | Category | Extracted from `admission_datetime` | Monday–Sunday |
| 14 | `hour` | Integer | Extracted from `admission_datetime` | Hour of day (0–23) |
| 15 | `month` | Category | Extracted from `admission_datetime` | January–December |
| 16 | `wait_category` | Category | `pd.cut(wait_time_minutes, [0,15,30,45,60,inf])` | 0-15, 16-30, 31-45, 46-60, 60+ min |
| 17 | `age_group` | Category | `pd.cut(age, [0,17,30,45,60,75,inf])` | 0-17, 18-30, 31-45, 46-60, 61-75, 76+ |

## Data Constraints and Validation Rules

| Rule | Field(s) | Expected behavior |
|------|----------|-------------------|
| Uniqueness | `patient_id` | Every value must be unique |
| Non-null (core) | `patient_id`, `admission_date`, `admission_time`, `gender`, `age`, `race`, `admission_flag`, `wait_time_minutes` | No missing values permitted |
| Positive | `wait_time_minutes` | Must be > 0; observed range: 10–60 |
| Positive | `age` | Must be > 0 |
| Range | `wait_time_minutes` | 10–60 minutes observed |
| Range | `satisfaction_score` | 0–10 scale when present |
| Enum | `gender` | Female, Male |
| Enum | `admission_flag` | Admission, Not Admission |
| Enum | `wait_category` | 0-15 min, 16-30 min, 31-45 min, 46-60 min, 60+ min |
| Enum | `department` | Cardiology, Gastroenterology, General Practice, Neurology, Orthopedics, Physiotherapy, Renal |

## Missing Value Policy

| Field | Missing Count | Missing % | Policy |
|-------|--------------|-----------|--------|
| `department` | 5,400 | 58.59% | Documented missing; do not impute |
| `satisfaction_score` | 6,699 | 72.69% | Documented missing; do not impute |
| All core fields | 0 | 0.00% | Complete |

Zero values in `wait_time_minutes` are valid (minimum observed is 10 minutes), not missing.

## Privacy and Ethics

- No patient names, contact details, or direct identifiers remain
- Patient IDs are pseudonymized using SHA-256 hashing
- Satisfaction scores and department data are incomplete but not imputed
- Analysis complies with Data Privacy Act of 2012 (RA 10173)
- Data stored securely; access limited to project team

## Related Documentation

- [Project Overview — Root README](../README.md)
- [Project Proposal — BUSANALY Format](../02_ProjectProposal/Project_Proposal_AlistoCare.md)
- [Analysis Folder README](../03_Analysis%20Files/README.md)
- [Data Dictionary](Data_Dictionary.md)
- [Analysis Methodology](Analysis_Methodology.md)
- [Data Quality Report](Data_Quality_Report.md)
- [Analysis QA Report](Analysis_QA_Report.md)

## Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-06 | Real dataset acquired, anonymized, and documented | AlistoCare project team |
| 0.1 | 2026-10-22 | Initial dummy-data dictionary (superseded) | AlistoCare project team |
