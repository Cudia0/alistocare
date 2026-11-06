# Analysis Methodology — AlistoCare BUSANALY Project

**Project:** AlistoCare: Health Center Queue Companion  
**Course:** BUSANALY – Business Analytics  
**Dataset:** healthcare_analytics_anonymized.csv (real data, Kaggle CC0)  
**Date:** November 6, 2026  

## 1. Business Problem

Patients at health centers and hospitals experience uncertainty about wait times and queue position. AlistoCare is a proposed digital queue management system designed to provide digital queue numbers, estimated waiting times, queue status updates, and turn notifications. This project analyzes real patient flow data to understand wait time patterns, identify high-demand departments and time periods, and inform the design and pilot planning of AlistoCare.

**Important distinction:** This analysis examines actual patient wait times from a real hospital dataset. However, it does not measure AlistoCare's effectiveness, as the system has not been piloted or implemented. Findings describe the current state of patient flow and waiting, which can inform where and how AlistoCare could be most valuable.

## 2. Analytical Questions

1. What is the distribution of patient wait times across all encounters?
2. How do wait times vary by department, day of week, and hour of day?
3. Is there a difference in wait times between admitted and non-admitted patients?
4. What is the relationship between wait time and patient satisfaction?
5. Which departments and time periods have the longest waits (candidates for AlistoCare pilot)?
6. What operational data would be needed to measure AlistoCare's impact?

## 3. Proposed KPIs

| KPI | Formula | Value (Real Data) | Unit |
|-----|---------|-------------------|------|
| Total patient encounters | COUNT(*) | 9,216 | Encounters |
| Average wait time | AVG(wait_time_minutes) | 35.26 | Minutes |
| Median wait time | MEDIAN(wait_time_minutes) | 35.00 | Minutes |
| Admission rate | COUNT(Admission) / COUNT(*) | 50.0% | Percent |
| Average patient age | AVG(age) | 39.9 | Years |
| Peak wait hour | MAX by hour | 3:00 AM (37.2 min) | Hour/Minutes |
| Lowest wait hour | MIN by hour | 12:00 PM (33.9 min) | Hour/Minutes |
| Satisfaction average | AVG(satisfaction_score) | 4.99 | Score (0-10) |
| Satisfaction coverage | COUNT(satisfaction) / COUNT(*) | 27.3% | Percent |
| Wait > 45 min share | COUNT(wait > 45) / COUNT(*) | ~29.8% | Percent |

## 4. Data Preparation

### 4.1 Cleaning Steps (Real Data)

1. **Acquisition:** Downloaded from Kaggle (CC0: Public Domain), November 6, 2026
2. **Anonymization:** Replaced SSN-format `Patient Id` with SHA-256 pseudonym; dropped `Merged` (name) column per RA 10173
3. **Column renaming:** Standardized to lowercase, snake_case names (e.g., `Patient Waittime` → `wait_time_minutes`)
4. **Gender fix:** Corrected "Femaleemale" → "Female" (17 records)
5. **Date/time parsing:** Parsed `admission_date` (M/D/YYYY) and `admission_time` (H:MM:SS AM/PM) into combined `admission_datetime`
6. **Derived fields:** Extracted `date`, `day_of_week`, `hour`, `month`; created `wait_category` and `age_group`
7. **Validation:** Confirmed 9,216 rows, 100% parse success, no missing core fields

### 4.2 Data Quality Issues Documented

| Issue | Field | Count | % | Resolution |
|-------|-------|-------|-----|------------|
| PII: SSN-format IDs | Patient Id | 9,216 | 100% | Pseudonymized with SHA-256 |
| PII: Patient names | Merged | 9,185 | ~100% | Column dropped |
| Data entry error | Gender | 17 | 0.18% | "Femaleemale" → "Female" |
| Missing department | Department | 5,400 | 58.59% | Documented; not imputed |
| Missing satisfaction | Satisfaction score | 6,699 | 72.69% | Documented; not imputed |

## 5. Descriptive Analytics

### 5.1 Overall Wait Time Distribution
- **Mean:** 35.26 minutes
- **Median:** 35.00 minutes
- **Std deviation:** 14.74 minutes
- **Range:** 10–60 minutes
- **Wait > 45 minutes:** ~29.8% of encounters (2,750 records in 46–60 min bucket)

### 5.2 Wait Time by Department
| Department | Encounters | Avg Wait (min) | Median Wait (min) |
|------------|-----------|----------------|-------------------|
| Neurology | 193 | 36.80 | 38.0 |
| Physiotherapy | 276 | 36.57 | 38.5 |
| Gastroenterology | 178 | 35.83 | 36.0 |
| Cardiology | 248 | 35.35 | 35.0 |
| Orthopedics | 995 | 34.98 | 34.0 |
| General Practice | 1,840 | 34.91 | 35.0 |
| Renal | 86 | 34.70 | 35.0 |

### 5.3 Wait Time by Day of Week
Saturday shows the highest average wait (35.74 min), Thursday/Friday the lowest (35.04 min). Variation is modest (range: 35.04–35.74 min).

### 5.4 Wait Time by Hour
- **Peak:** 3:00 AM (37.22 min avg)
- **Lowest:** 12:00 PM (33.88 min avg)
- Night/early morning hours (22:00–04:00) show slightly elevated waits

### 5.5 Admission vs Non-Admission
- Admitted patients: 34.97 min avg wait
- Non-admitted patients: 35.55 min avg wait
- Difference: ~0.6 minutes (not practically significant)

## 6. Diagnostic Analytics

### Department Comparisons
Neurology (36.80 min) and Physiotherapy (36.57 min) show the longest average waits, while Renal (34.70 min) and General Practice (34.91 min) show the shortest. However, differences between departments are small (range: 34.70–36.80 min = 2.1 min spread), suggesting wait times are relatively uniform across departments.

### Satisfaction Correlation
Correlation between wait time and satisfaction score: **-0.021** (negligible). Wait time alone does not explain patient satisfaction variation in this dataset.

### Wait Time Categories
- 0–15 min: 1,082 (11.7%)
- 16–30 min: 2,667 (28.9%)
- 31–45 min: 2,717 (29.5%)
- 46–60 min: 2,750 (29.8%)

**~59.3% of patients wait more than 30 minutes.**

## 7. Predictive / Prescriptive Analysis

### Predictive Demonstration: Wait Time Category Classification
A classification model predicts `wait_category` (Low/Moderate/High) from patient and operational variables. Results are computed on real data and can be validated by rerunning `AlistoCare_Analysis.py`.

### Prescriptive Demonstration: Capacity Planning
Based on wait time patterns:
- **Saturday and early morning hours** show slightly elevated waits — candidates for additional staffing
- **Neurology and Physiotherapy** departments show longest waits — candidates for AlistoCare pilot
- **~59.3% of patients wait >30 minutes** — significant queue management opportunity

These are planning considerations based on observed patterns, not final recommendations. Final recommendations must be written after all analysis is complete and peer-reviewed.

## 8. Dashboard Plan

The dashboard will include:

1. **KPI cards:** Total encounters, average wait time, median wait time, admission rate, % waits >30 min
2. **Trend chart:** Daily/monthly patient volume
3. **Bar chart:** Average wait time by department
4. **Bar chart:** Wait time by hour of day
5. **Pie/donut chart:** Wait time category distribution
6. **Filters:** Date range, department, day of week, admission flag

Each visual answers a business question. A "How to use this dashboard" note will be included.

## 9. Limitations

- **Single facility:** Data from one medium-sized hospital; may not generalize to Philippine community health centers
- **No queue position data:** Dataset has wait time but not queue position, consultation duration, or service start/end timestamps
- **Incomplete satisfaction:** Only 27.3% of encounters have satisfaction scores
- **Incomplete department data:** 58.6% of encounters missing department referral
- **No AlistoCare evaluation:** System not yet piloted; cannot claim effectiveness
- **Correlation ≠ causation:** Observed patterns do not establish cause and effect

## 10. Ethics and Privacy

- PII removed: SSN-format IDs pseudonymized, name column dropped
- Complies with Data Privacy Act of 2012 (RA 10173)
- No imputation of missing sensitive data
- Analysis limited to aggregated, anonymized metrics

## 11. Reproducibility

- `AlistoCare_Analysis.py` — standalone script; loads CSV, cleans, computes all KPIs, saves results
- `AlistoCare.ipynb` — Jupyter notebook with same workflow in executable cells
- `AlistoCare_Analysis.xlsx` — Excel workbook with metadata, dictionary, QA, KPIs, findings
- All scripts reference `healthcare_analytics_cleaned.csv` in the same folder

## Related Documentation

- [Project Overview — Root README](../README.md)
- [Project Proposal — BUSANALY Format](../02_ProjectProposal/Project_Proposal_AlistoCare.md)
- [Analysis Folder README](../03_Analysis%20Files/README.md)
- [Data Dictionary](Data_Dictionary.md)
- [Data Quality Report](Data_Quality_Report.md)
- [Analysis QA Report](Analysis_QA_Report.md)

## 12. Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2026-11-06 | Real data analysis methodology | AlistoCare project team |
| 0.1 | 2026-10-22 | Initial dummy-data methodology (superseded) | AlistoCare project team |
