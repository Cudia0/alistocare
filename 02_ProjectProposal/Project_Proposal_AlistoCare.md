# Project Proposal — AlistoCare: Health Center Queue Companion

**Course:** BUSANALY – Business Analytics  
**Project Type:** Final Project (Group)  
**Date:** November 6, 2026  
**Status:** Draft for instructor approval

---

## 1. Project Title, Group Name, and Members

**Project Title:** AlistoCare: Health Center Queue Companion — Patient Flow and Wait Time Analytics  
**Group Name:** AlistoCare Analytics Team  
**Section:** To be assigned by instructor

| Member | Role |
|--------|------|
| Member 1 | Engagement Lead — partner coordination, proposal, executive summary, implementation plan, final editing |
| Member 2 | Data Analyst — data collection, cleaning, data model, data dictionary |
| Member 3 | Insights / Modeling Analyst — diagnostic, predictive, prescriptive analysis, impact estimates |
| Member 4 | Visualization & Strategy Lead — dashboard design, recommendations, presentation design |

*(Maximum of 4 members per group, per BUSANALY guidelines Section 3.)*

---

## 2. Organization or Industry Profile

**Sector:** Healthcare / Community Health Services  
**Organization Type:** Public health center / hospital outpatient department  
**Focus Area:** Patient flow management, queue wait times, service delivery efficiency  

AlistoCare is a proposed digital queue management system for community health centers. Its intended features include digital queue numbers, estimated waiting times, queue status updates, turn notifications, and a staff dashboard for managing patient flow. The system aims to reduce patient uncertainty while waiting and improve health center staff's ability to communicate queue status.

This project analyzes real patient encounter data to understand current wait time patterns, identify high-demand departments and time periods, and inform the design and pilot planning of AlistoCare.

---

## 3. Business Problem and Decision to be Supported

### Business Problem
Patients at health centers experience uncertainty about queue position and waiting time. Without clear visibility into wait times or queue status, patients may arrive unprepared, experience frustration, and make suboptimal visit timing decisions. Health center staff also lack data-driven tools to manage patient flow efficiently.

### Decision to be Supported
This analysis supports the decision of **where and how to pilot AlistoCare** by identifying:
- Which departments have the longest average wait times (priority candidates for pilot)
- Which time periods (hours, days) experience peak congestion
- What proportion of patients experience extended waits (>30 minutes)
- Whether wait time correlates with patient satisfaction

The decision output will be a prioritized list of departments and time slots for AlistoCare deployment, along with recommended staffing adjustments.

---

## 4. Key Stakeholders

| Stakeholder | How They Will Use the Results |
|-------------|------------------------------|
| Health Center Administrators | Decide where to pilot AlistoCare, allocate staffing resources |
| Department Heads (Neurology, Physiotherapy, etc.) | Understand their department's wait time patterns relative to others |
| Frontline Staff | Adjust schedules and patient communication based on peak wait periods |
| Patients | Benefit from reduced wait uncertainty and improved queue transparency |
| Project Team / Academic Evaluator | Review analysis validity, completeness, and adherence to BUSANALY guidelines |

---

## 5. Analytical Questions and Proposed KPIs

| # | Analytical Question | Proposed KPI |
|---|---------------------|--------------|
| Q1 | What is the overall distribution of patient wait times? | Average wait time (minutes), median wait time, wait time range |
| Q2 | How do wait times vary by department? | Average wait time by department, department ranking |
| Q3 | How do wait times vary by day of week and hour of day? | Peak wait hour, busiest day, wait time by time slot |
| Q4 | Is there a difference in wait times between admitted and non-admitted patients? | Average wait time by admission flag |
| Q5 | What is the relationship between wait time and patient satisfaction? | Correlation coefficient (wait time vs. satisfaction score) |
| Q6 | What share of patients experience extended waits (>30 min)? | Percentage of encounters with wait > 30 minutes |

---

## 6. Data Description

| Property | Value |
|----------|-------|
| **Source** | Kaggle — Healthcare Analytics Patient Flow Data (CC0: Public Domain) |
| **Source URL** | https://www.kaggle.com/datasets/hassanjameelahmed/healthcare-analytics-patient-flow-data |
| **Retrieval Date** | November 6, 2026 |
| **Period Covered** | January 4, 2023 – December 10, 2024 |
| **Dataset Size** | 9,216 patient encounter records |
| **Variables** | 10 core fields (patient_id, admission_date, admission_time, gender, age, race, department, admission_flag, satisfaction_score, wait_time_minutes) |
| **Unit of Observation** | One patient encounter |
| **Permission Status** | Public domain (CC0 license) — no partner permission letter required |
| **Privacy Compliance** | PII anonymized: SSN-format patient IDs pseudonymized via SHA-256; patient name column dropped. Complies with Data Privacy Act of 2012 (RA 10173). |

**Data Quality Notes:**
- Department referral missing for 58.6% of records (documented, not imputed)
- Satisfaction score missing for 72.7% of records (documented, not imputed)
- Gender data entry error ("Femaleemale") corrected to "Female" (17 records)
- All core fields (wait_time_minutes, admission_flag, age, gender, race, dates) are complete

---

## 7. Planned Analytics Techniques and Tools

| Technique | Purpose | Tool |
|-----------|---------|------|
| Descriptive analytics | Wait time distributions, volume by department/day/hour | Python (pandas), Excel |
| Diagnostic analytics | Department comparisons, admission vs. non-admitted patterns, satisfaction correlation | Python (pandas), Excel |
| Predictive (classification) | Wait time category prediction (Low/Moderate/High) from patient & operational variables | Python (scikit-learn) |
| Prescriptive (scenario) | Staffing and capacity planning based on wait time patterns | Python, Excel |
| Data cleaning & preparation | PII removal, date/time parsing, derived field creation, validation | Python (pandas) |
| Dashboard | Interactive KPI cards, trend charts, department comparisons, filters | Excel or Power BI |

---

## 8. Initial Work Plan and Task Assignment

| Phase | Task | Owner | Timeline |
|-------|------|-------|----------|
| Phase 1 | Data acquisition, anonymization, cleaning, validation | Data Analyst | Week 1 |
| Phase 2 | Descriptive and diagnostic analysis | Insights / Modeling Analyst | Week 2 |
| Phase 3 | Predictive and prescriptive analysis | Insights / Modeling Analyst | Week 2 |
| Phase 4 | Dashboard design and build | Visualization & Strategy Lead | Week 3 |
| Phase 5 | Business report writing (10–15 pages) | Engagement Lead (consolidation) | Week 4 |
| Phase 6 | Management presentation (10–15 slides) | Visualization & Strategy Lead | Week 5 |
| Phase 7 | Final review, QA, submission preparation | All members | Week 6 |

**Documentation Location:** All analysis files are maintained in the `alistocare/` project folder with subfolders:
- `alistocare/data/` — raw, anonymized, and cleaned datasets
- `alistocare/documentation/` — methodology, data dictionary, QA report, findings
- `alistocare/scripts/` — Python analysis script and notebook
- `alistocare/outputs/` — Excel workbook with analysis results
- `alistocare/02_ProjectProposal/` — this proposal document

---

## 9. Compliance Statement

- **Real data:** All analysis uses verified real patient encounter data from Kaggle (CC0 license). No fabricated or synthetic records.
- **Data privacy:** PII removed per RA 10173; patient IDs pseudonymized, name column dropped.
- **Original work:** All analysis, code, and writing are the group's own work. AI tools (if used) will be disclosed in an AI Use Disclosure appendix.
- **Reproducibility:** All code, cleaning steps, and calculations are documented and reproducible from the raw dataset.

---

**Prepared by:** AlistoCare Analytics Team  
**Date:** November 6, 2026  
**For:** BUSANALY Final Project — Instructor Approval
