"""
AlistoCare Analysis Script — BUSANALY Final Project
====================================================

Google Colab COMPATIBLE version for testing and submission.

This script performs the complete AlistoCare analysis on real, anonymized
patient encounter data from Kaggle (Healthcare Analytics Patient Flow Data,
CC0 Public Domain). No synthetic or fabricated records are included.

Compatibility:
  - Google Colab: Upload healthcare_analytics_cleaned.csv to the session,
    then run all cells. File paths use relative paths that work in Colab.
  - Local: Run with `python AlistoCare_Analysis.py` from the same folder
    as the CSV file.

Usage in Google Colab:
  1. Upload healthcare_analytics_cleaned.csv to the Colab session files pane
  2. Run this script cell by cell or all at once
  3. Output files are saved to the current working directory

Requirements:
    pandas, scikit-learn, openpyxl
"""

import json
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Configuration — Colab compatible (no __file__ dependency)
# ---------------------------------------------------------------------------

# In Colab, __file__ is not defined. Use a configurable path that defaults
# to the current working directory (where the uploaded CSV lives).
DATA_FILE = Path("healthcare_analytics_cleaned.csv")
OUTPUT_DIR = Path("analysis_output")

MIN_ROWS = 1000
MIN_COLUMNS = 8

VALID_GENDERS = {"Female", "Male"}
VALID_ADMISSION_FLAGS = {"Admission", "Not Admission"}
VALID_DEPARTMENTS = {
    "Cardiology", "Gastroenterology", "General Practice", "Neurology",
    "Orthopedics", "Physiotherapy", "Renal"
}
VALID_WAIT_CATEGORIES = {"0-15 min", "16-30 min", "31-45 min", "46-60 min", "60+ min"}
VALID_AGE_GROUPS = {"0-17", "18-30", "31-45", "46-60", "61-75", "76+"}

# ---------------------------------------------------------------------------
# Colab file upload helper
# ---------------------------------------------------------------------------

def upload_file_to_colab(filename: str = "healthcare_analytics_cleaned.csv"):
    """
    In Google Colab, prompt the user to upload the CSV file.
    Returns True if the file exists after upload, False otherwise.
    """
    try:
        from google.colab import files
        print(f"📁 Please upload '{filename}' to this Colab session.")
        uploaded = files.upload()
        if filename in uploaded:
            print(f"✅ {filename} uploaded successfully.")
            return True
        else:
            print(f"❌ {filename} was not uploaded. Available files: {list(uploaded.keys())}")
            return False
    except ImportError:
        # Not running in Colab — skip upload
        return Path(filename).is_file()


def ensure_data_file(path: Path) -> bool:
    """Check if the data file exists; if not, offer Colab upload."""
    if path.is_file():
        return True
    print(f"⚠️  Data file not found: {path.resolve()}")
    return upload_file_to_colab(path.name)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV dataset."""
    if not path.is_file():
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    return df


def validate_structure(df: pd.DataFrame) -> dict:
    """Run structural validation checks and return a results dict."""
    checks = {}
    checks["rows"] = len(df)
    checks["columns"] = df.shape[1]
    checks["rows_pass"] = checks["rows"] >= MIN_ROWS
    checks["columns_pass"] = checks["columns"] >= MIN_COLUMNS
    checks["duplicate_rows"] = int(df.duplicated().sum())
    checks["duplicate_patient_ids"] = (
        int(df["patient_id"].duplicated().sum()) if "patient_id" in df.columns else None
    )
    checks["missing_total"] = int(df.isna().sum().sum())
    checks["missing_by_column"] = df.isna().sum().to_dict()
    checks["empty_rows"] = int(df.isna().all(axis=1).sum())
    checks["empty_columns"] = int(df.isna().all(axis=0).sum())
    return checks


def validate_types_and_enums(df: pd.DataFrame) -> dict:
    """Validate data types and allowed values."""
    issues = {}
    issues["invalid_genders"] = (
        int(~df["gender"].isin(VALID_GENDERS).fillna(False))
        if "gender" in df.columns else None
    )
    issues["invalid_admission_flags"] = (
        int(~df["admission_flag"].isin(VALID_ADMISSION_FLAGS).fillna(False))
        if "admission_flag" in df.columns else None
    )
    issues["invalid_departments"] = (
        int(~df["department"].dropna().isin(VALID_DEPARTMENTS))
        if "department" in df.columns else None
    )
    issues["non_positive_wait_time"] = (
        int((df["wait_time_minutes"] <= 0).sum())
        if "wait_time_minutes" in df.columns else None
    )
    issues["non_positive_age"] = (
        int((df["age"] <= 0).sum()) if "age" in df.columns else None
    )
    issues["invalid_satisfaction"] = (
        int(((df["satisfaction_score"] < 0) | (df["satisfaction_score"] > 10)).sum())
        if "satisfaction_score" in df.columns else None
    )
    return issues


def compute_derived(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived analytical fields."""
    df = df.copy()

    # Ensure admission_datetime is parsed
    if "admission_datetime" in df.columns:
        df["admission_datetime"] = pd.to_datetime(df["admission_datetime"], errors="coerce")
    elif "admission_date" in df.columns and "admission_time" in df.columns:
        df["admission_datetime"] = pd.to_datetime(
            df["admission_date"].astype(str) + " " + df["admission_time"].astype(str),
            errors="coerce"
        )

    if "admission_datetime" in df.columns and df["admission_datetime"].notna().any():
        df["date"] = df["admission_datetime"].dt.date
        df["day_of_week"] = df["admission_datetime"].dt.day_name()
        df["hour"] = df["admission_datetime"].dt.hour
        df["month"] = df["admission_datetime"].dt.month_name()

    # Wait time categories
    if "wait_time_minutes" in df.columns:
        df["wait_category"] = pd.cut(
            df["wait_time_minutes"],
            bins=[0, 15, 30, 45, 60, float("inf")],
            labels=["0-15 min", "16-30 min", "31-45 min", "46-60 min", "60+ min"],
        )

    # Age groups
    if "age" in df.columns:
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 17, 30, 45, 60, 75, float("inf")],
            labels=["0-17", "18-30", "31-45", "46-60", "61-75", "76+"],
        )

    return df


def descriptive_analytics(df: pd.DataFrame) -> dict:
    """Compute descriptive statistics."""
    results = {}

    results["total_encounters"] = int(len(df))
    results["average_wait_time"] = round(float(df["wait_time_minutes"].mean()), 2)
    results["median_wait_time"] = float(df["wait_time_minutes"].median())
    results["min_wait_time"] = int(df["wait_time_minutes"].min())
    results["max_wait_time"] = int(df["wait_time_minutes"].max())
    results["std_wait_time"] = round(float(df["wait_time_minutes"].std()), 2)
    results["average_age"] = round(float(df["age"].mean()), 1)
    results["admission_rate"] = round(
        float((df["admission_flag"] == "Admission").mean() * 100), 1
    )
    results["satisfaction_records"] = int(df["satisfaction_score"].notna().sum())
    results["satisfaction_pct"] = round(
        float(df["satisfaction_score"].notna().mean() * 100), 1
    )
    results["department_records"] = int(df["department"].notna().sum())
    results["department_pct"] = round(
        float(df["department"].notna().mean() * 100), 1
    )

    # Wait time category distribution
    results["wait_category_distribution"] = (
        df["wait_category"].value_counts().to_dict()
    )

    # By department
    results["by_department"] = (
        df.groupby("department")["wait_time_minutes"]
        .agg(["count", "mean", "median"])
        .round(2)
        .to_dict("index")
    )

    # By day of week
    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]
    results["by_day_of_week"] = (
        df.groupby("day_of_week")["wait_time_minutes"]
        .agg(["count", "mean"])
        .round(2)
        .reindex(day_order)
        .to_dict("index")
    )

    # By hour
    results["by_hour"] = (
        df.groupby("hour")["wait_time_minutes"]
        .agg(["count", "mean"])
        .round(2)
        .to_dict("index")
    )

    # Admission vs non-admission
    results["by_admission_flag"] = (
        df.groupby("admission_flag")["wait_time_minutes"]
        .agg(["count", "mean"])
        .round(2)
        .to_dict("index")
    )

    # Date range
    if "date" in df.columns:
        results["date_range_start"] = str(min(df["date"].dropna()))
        results["date_range_end"] = str(max(df["date"].dropna()))

    return results


def diagnostic_analytics(df: pd.DataFrame) -> dict:
    """Compute diagnostic comparisons."""
    results = {}

    # Department wait time comparison
    results["dept_wait_comparison"] = (
        df.groupby("department")["wait_time_minutes"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
        .to_dict("index")
    )

    # Satisfaction correlation
    sat_df = df.dropna(subset=["satisfaction_score", "wait_time_minutes"])
    if len(sat_df) > 10:
        corr = sat_df["wait_time_minutes"].corr(sat_df["satisfaction_score"])
        results["satisfaction_wait_correlation"] = round(float(corr), 4)
        results["satisfaction_sample_size"] = int(len(sat_df))
        results["average_satisfaction"] = round(
            float(sat_df["satisfaction_score"].mean()), 2
        )

    # Wait > 30 min share
    results["wait_over_30_share"] = round(
        float((df["wait_time_minutes"] > 30).mean() * 100), 1
    )
    results["wait_over_45_share"] = round(
        float((df["wait_time_minutes"] > 45).mean() * 100), 1
    )

    # Peak and low hours
    hour_stats = (
        df.groupby("hour")["wait_time_minutes"]
        .mean()
        .round(2)
    )
    peak_hour = hour_stats.idxmax()
    low_hour = hour_stats.idxmin()
    results["peak_wait_hour"] = int(peak_hour)
    results["peak_wait_hour_avg"] = round(float(hour_stats[peak_hour]), 2)
    results["lowest_wait_hour"] = int(low_hour)
    results["lowest_wait_hour_avg"] = round(float(hour_stats[low_hour]), 2)

    return results


def predictive_demonstration(df: pd.DataFrame) -> dict:
    """
    Demonstration-only classification of wait_category.
    Results are computed on real data but are illustrative, not validated for production.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report

    model_df = df.dropna(subset=["wait_category"]).copy()
    features = ["gender", "age", "department", "admission_flag", "hour"]
    model_df = model_df.dropna(subset=features)

    X = pd.get_dummies(model_df[features], drop_first=True)
    y = model_df["wait_category"].astype(str)

    if len(y) < 10 or y.nunique() < 2:
        return {"error": "Insufficient data for classification demonstration"}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    return {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "classification_report": classification_report(
            y_test, y_pred, output_dict=True, zero_division=0
        ),
        "note": "REAL DATA — illustrative classification, not validated for production use",
    }


def prescriptive_demonstration(df: pd.DataFrame) -> dict:
    """
    Demonstration-only capacity planning scenario.
    Illustrates staffing implications based on observed wait time patterns.
    """
    # Identify departments with longest waits
    dept_waits = (
        df.groupby("department")["wait_time_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    # Identify hours with longest waits
    hour_waits = (
        df.groupby("hour")["wait_time_minutes"]
        .mean()
        .sort_values(ascending=False)
    )

    # Patients waiting > 30 minutes by department
    long_waits = df[df["wait_time_minutes"] > 30]
    long_waits_by_dept = (
        long_waits.groupby("department").size()
    )

    summary = {
        "longest_wait_department": str(dept_waits.idxmax()),
        "longest_wait_department_avg": round(float(dept_waits.max()), 2),
        "shortest_wait_department": str(dept_waits.idxmin()),
        "shortest_wait_department_avg": round(float(dept_waits.min()), 2),
        "peak_wait_hour": int(hour_waits.idxmax()),
        "peak_wait_hour_avg": round(float(hour_waits.max()), 2),
        "patients_waiting_over_30_min": int((df["wait_time_minutes"] > 30).sum()),
        "patients_waiting_over_30_min_pct": round(
            float((df["wait_time_minutes"] > 30).mean() * 100), 1
        ),
        "long_waits_by_department": long_waits_by_dept.to_dict(),
        "note": "REAL DATA — planning illustration based on observed patterns, not a final recommendation",
    }
    return summary


def save_results(df: pd.DataFrame, descriptive: dict, diagnostic: dict,
                 predictive: dict, prescriptive: dict, validation: dict) -> None:
    """Save cleaned data and summary results to CSV and JSON files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Cleaned dataset with derived fields
    df.to_csv(OUTPUT_DIR / "alistocare_cleaned.csv", index=False)

    # Validation summary
    val_rows = []
    for k, v in validation.items():
        if k == "missing_by_column":
            for col, val in v.items():
                val_rows.append({"check": f"missing_{col}", "value": str(val)})
        else:
            val_rows.append({"check": k, "value": str(v)})
    pd.DataFrame(val_rows).to_csv(OUTPUT_DIR / "validation_summary.csv", index=False)

    # Descriptive summary
    desc_rows = []
    for k, v in descriptive.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                desc_rows.append({"metric": f"{k}.{sub_k}", "value": str(sub_v)})
        else:
            desc_rows.append({"metric": k, "value": str(v)})
    pd.DataFrame(desc_rows).to_csv(OUTPUT_DIR / "descriptive_summary.csv", index=False)

    # Diagnostic summary
    diag_rows = []
    for k, v in diagnostic.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                diag_rows.append({"metric": f"{k}.{sub_k}", "value": str(sub_v)})
        else:
            diag_rows.append({"metric": k, "value": str(v)})
    pd.DataFrame(diag_rows).to_csv(OUTPUT_DIR / "diagnostic_summary.csv", index=False)

    # Predictive summary
    if isinstance(predictive, dict) and "error" not in predictive:
        pred_rows = [
            {"metric": "accuracy", "value": str(predictive["accuracy"])},
            {"metric": "note", "value": predictive.get("note", "")},
        ]
        pd.DataFrame(pred_rows).to_csv(OUTPUT_DIR / "predictive_summary.csv", index=False)

    # Prescriptive summary
    pres_rows = []
    for k, v in prescriptive.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                pres_rows.append({"metric": f"{k}.{sub_k}", "value": str(sub_v)})
        else:
            pres_rows.append({"metric": k, "value": str(v)})
    pd.DataFrame(pres_rows).to_csv(OUTPUT_DIR / "prescriptive_summary.csv", index=False)

    # Save combined JSON results
    combined = {
        "descriptive": descriptive,
        "diagnostic": diagnostic,
        "predictive": predictive,
        "prescriptive": prescriptive,
        "validation": {k: v for k, v in validation.items() if k != "missing_by_column"},
    }
    with open(OUTPUT_DIR / "analysis_results.json", "w") as f:
        json.dump(combined, f, indent=2, default=str)


def print_summary(validation: dict, descriptive: dict, diagnostic: dict,
                  predictive: dict, prescriptive: dict) -> None:
    """Print a human-readable summary to stdout."""
    print("=" * 60)
    print("ALISTOCARE ANALYSIS SUMMARY — REAL DATA")
    print("=" * 60)
    print()

    print("--- Validation ---")
    print(f"Rows: {validation['rows']:,} (minimum {MIN_ROWS}: {'PASS' if validation['rows_pass'] else 'FAIL'})")
    print(f"Columns: {validation['columns']} (minimum {MIN_COLUMNS}: {'PASS' if validation['columns_pass'] else 'FAIL'})")
    print(f"Duplicate rows: {validation['duplicate_rows']}")
    print(f"Duplicate patient_ids: {validation['duplicate_patient_ids']}")
    print(f"Missing values (total): {validation['missing_total']}")
    print()

    print("--- Descriptive ---")
    print(f"Total encounters: {descriptive['total_encounters']:,}")
    print(f"Average wait time: {descriptive['average_wait_time']:.2f} minutes")
    print(f"Median wait time: {descriptive['median_wait_time']:.2f} minutes")
    print(f"Wait time range: {descriptive['min_wait_time']} – {descriptive['max_wait_time']} minutes")
    print(f"Standard deviation: {descriptive['std_wait_time']:.2f} minutes")
    print(f"Average patient age: {descriptive['average_age']:.1f} years")
    print(f"Admission rate: {descriptive['admission_rate']:.1f}%")
    print(f"Satisfaction records: {descriptive['satisfaction_records']:,} ({descriptive['satisfaction_pct']:.1f}%)")
    print(f"Department records: {descriptive['department_records']:,} ({descriptive['department_pct']:.1f}%)")
    print(f"Patients waiting >30 min: {descriptive['wait_over_30_share']}%")
    print(f"Patients waiting >45 min: {descriptive['wait_over_45_share']}%")
    print()

    print("--- Diagnostic ---")
    print(f"Correlation: wait time vs satisfaction: {diagnostic.get('satisfaction_wait_correlation', 'N/A')}")
    print(f"Peak wait hour: {diagnostic.get('peak_wait_hour', 'N/A')}:00 ({diagnostic.get('peak_wait_hour_avg', 'N/A')} min)")
    print(f"Lowest wait hour: {diagnostic.get('lowest_wait_hour', 'N/A')}:00 ({diagnostic.get('lowest_wait_hour_avg', 'N/A')} min)")
    print()

    print("--- Predictive (real data demo) ---")
    if isinstance(predictive, dict) and "error" not in predictive:
        print(f"Classification accuracy: {predictive['accuracy']:.3f}")
    else:
        print(f"Predictive demo skipped: {predictive.get('error', 'unknown')}")
    print()

    print("--- Prescriptive (real data demo) ---")
    print(f"Longest wait department: {prescriptive.get('longest_wait_department', 'N/A')}")
    print(f"Longest wait avg: {prescriptive.get('longest_wait_department_avg', 'N/A')} min")
    print(f"Patients waiting >30 min: {prescriptive.get('patients_waiting_over_30_min', 'N/A'):,}")
    print()

    print("=" * 60)
    print("SOURCE: healthcare_analytics_cleaned.csv (real data, Kaggle CC0)")
    print("PII handled: SSN-format IDs pseudonymized, name column dropped")
    print("Complies with Data Privacy Act of 2012 (RA 10173)")
    print("=" * 60)


def main() -> None:
    """Main entry point — works in both Colab and local environments."""
    # Ensure data file exists (Colab upload if needed)
    if not ensure_data_file(DATA_FILE):
        print(f"\n❌ Cannot proceed without {DATA_FILE.name}")
        print("   Upload the file to this Colab session and re-run.")
        sys.exit(1)

    print(f"Loading data from: {DATA_FILE.resolve()}")
    df = load_data(DATA_FILE)

    print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")
    print()

    # Validate
    validation = validate_structure(df)
    enum_issues = validate_types_and_enums(df)
    validation.update(enum_issues)

    # Compute derived fields
    df = compute_derived(df)

    # Analytics
    descriptive = descriptive_analytics(df)
    diagnostic = diagnostic_analytics(df)
    predictive = predictive_demonstration(df)
    prescriptive = prescriptive_demonstration(df)

    # Save outputs
    save_results(df, descriptive, diagnostic, predictive, prescriptive, validation)

    # Print summary
    print_summary(validation, descriptive, diagnostic, predictive, prescriptive)

    print(f"\nOutputs saved to: {OUTPUT_DIR.resolve()}")


# Colab-compatible: runs when cell is executed, no __main__ guard needed
main()