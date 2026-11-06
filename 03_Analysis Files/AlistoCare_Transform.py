"""
AlistoCare Data Transformation Script — BUSANALY Final Project
==============================================================

Transforms the original Kaggle Healthcare Analytics Patient Flow Data into:
1. Anonymized dataset (PII removed per RA 10173)
2. Cleaned dataset (parsed dates, derived fields, ready for analysis)

DATA SOURCE:
  Title: Healthcare Analytics Patient Flow Data
  Creator: Hassan Jameel Ahmed
  Platform: Kaggle
  URL: https://www.kaggle.com/datasets/hassanjameelahmed/healthcare-analytics-patient-flow-data
  License: CC0: Public Domain — safe to share publicly, including on GitHub

PRIVACY COMPLIANCE:
  - Patient Id (SSN format XXX-XX-XXXX) → SHA-256 pseudonym (PID-XXXXXXXXXXXX)
  - Merged column (patient names) → dropped entirely
  - Complies with Data Privacy Act of 2012 (RA 10173)

USAGE IN GOOGLE COLAB:
  1. Upload healthcare_analytics_patient_flow_data.csv to the Colab session
  2. Run this script — outputs saved to current directory
  3. Download healthcare_analytics_anonymized.csv and healthcare_analytics_cleaned.csv

USAGE LOCALLY:
  python AlistoCare_Transform.py
  (Place healthcare_analytics_patient_flow_data.csv in the same folder)

REQUIREMENTS:
    pandas
"""

import hashlib
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Configuration — Colab compatible (no __file__ dependency)
# ---------------------------------------------------------------------------

ORIGINAL_FILE = Path("healthcare_analytics_patient_flow_data.csv")
ANONYMIZED_FILE = Path("healthcare_analytics_anonymized.csv")
CLEANED_FILE = Path("healthcare_analytics_cleaned.csv")

# ---------------------------------------------------------------------------
# Colab file upload helper
# ---------------------------------------------------------------------------

def upload_file_to_colab(filename: str = "healthcare_analytics_patient_flow_data.csv"):
    """In Google Colab, prompt the user to upload the CSV file."""
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
        return Path(filename).is_file()


def ensure_original_file(path: Path) -> bool:
    """Check if the original data file exists; if not, offer Colab upload."""
    if path.is_file():
        return True
    print(f"⚠️  Original data file not found: {path.resolve()}")
    return upload_file_to_colab(path.name)


# ---------------------------------------------------------------------------
# Transformation steps
# ---------------------------------------------------------------------------

def load_original(path: Path) -> pd.DataFrame:
    """Load the original Kaggle CSV dataset."""
    if not path.is_file():
        raise FileNotFoundError(f"Original data file not found: {path}")
    df = pd.read_csv(path)
    print(f"Loaded original dataset: {len(df):,} rows, {df.shape[1]} columns")
    return df


def anonymize_pii(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove / pseudonymize personally identifiable information per RA 10173.

    - Patient Id (SSN format XXX-XX-XXXX) → SHA-256 pseudonym
    - Merged column (patient names) → dropped entirely
    """
    df = df.copy()

    # Pseudonymize Patient Id using SHA-256 (first 12 hex chars)
    if "Patient Id" in df.columns:
        df["Patient Id"] = df["Patient Id"].apply(
            lambda x: "PID-" + hashlib.sha256(str(x).encode()).hexdigest()[:12]
        )
        print("✅ Patient Id pseudonymized (SHA-256 → PID-XXXXXXXXXXXX)")

    # Drop Merged column (contains patient names — direct PII)
    if "Merged" in df.columns:
        df = df.drop(columns=["Merged"])
        print("✅ Merged column dropped (contained patient names)")

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase snake_case."""
    column_map = {
        "Patient Id": "patient_id",
        "Patient Admission Date": "admission_date",
        "Patient Admission Time": "admission_time",
        "Patient Gender": "gender",
        "Patient Age": "age",
        "Patient Race": "race",
        "Department Referral": "department",
        "Patient Admission Flag": "admission_flag",
        "Patient Satisfaction Score": "satisfaction_score",
        "Patient Waittime": "wait_time_minutes",
    }
    df = df.rename(columns=column_map)
    print("✅ Columns renamed to snake_case")
    return df


def fix_data_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Correct known data entry errors."""
    df = df.copy()

    # Fix "Femaleemale" → "Female" (17 records observed in source data)
    if "gender" in df.columns:
        bad = int((df["gender"] == "Femaleemale").sum())
        if bad > 0:
            df["gender"] = df["gender"].replace("Femaleemale", "Female")
            print(f"✅ Fixed {bad} gender data entry error(s): 'Femaleemale' → 'Female'")

    return df


def parse_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """Parse admission_date and admission_time into combined admission_datetime."""
    df = df.copy()

    # Parse date (format: M/D/YYYY)
    df["admission_date_parsed"] = pd.to_datetime(df["admission_date"], format="%m/%d/%Y", errors="coerce")

    # Parse time (format: H:MM:SS AM/PM)
    df["admission_time_parsed"] = pd.to_datetime(
        df["admission_time"], format="%I:%M:%S %p", errors="coerce"
    ).dt.time

    # Combine into full datetime
    df["admission_datetime"] = pd.to_datetime(
        df["admission_date_parsed"].dt.strftime("%Y-%m-%d") + " " +
        df["admission_time_parsed"].astype(str),
        errors="coerce"
    )

    parse_failures = int(df["admission_datetime"].isna().sum())
    if parse_failures > 0:
        print(f"⚠️  {parse_failures} records could not be parsed ({parse_failures/len(df)*100:.1f}%)")
    else:
        print("✅ Date/time parsed successfully for all records")

    return df


def add_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived analytical fields."""
    df = df.copy()

    # Extract date components
    df["date"] = df["admission_datetime"].dt.date
    df["day_of_week"] = df["admission_datetime"].dt.day_name()
    df["hour"] = df["admission_datetime"].dt.hour
    df["month"] = df["admission_datetime"].dt.month_name()

    # Wait time categories
    df["wait_category"] = pd.cut(
        df["wait_time_minutes"],
        bins=[0, 15, 30, 45, 60, float("inf")],
        labels=["0-15 min", "16-30 min", "31-45 min", "46-60 min", "60+ min"],
    )

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 17, 30, 45, 60, 75, float("inf")],
        labels=["0-17", "18-30", "31-45", "46-60", "61-75", "76+"],
    )

    print("✅ Derived fields added (date, day_of_week, hour, month, wait_category, age_group)")
    return df


def validate_cleaned(df: pd.DataFrame) -> dict:
    """Run validation checks on the cleaned dataset."""
    checks = {}
    checks["rows"] = len(df)
    checks["columns"] = df.shape[1]
    checks["duplicate_rows"] = int(df.duplicated().sum())
    checks["duplicate_patient_ids"] = int(df["patient_id"].duplicated().sum()) if "patient_id" in df.columns else None
    checks["missing_core"] = int(
        df[["patient_id", "admission_date", "admission_time", "gender", "age",
            "race", "admission_flag", "wait_time_minutes"]].isna().sum().sum()
    ) if all(c in df.columns for c in ["patient_id", "admission_date", "admission_time",
                                      "gender", "age", "race", "admission_flag", "wait_time_minutes"]) else None
    checks["missing_department"] = int(df["department"].isna().sum()) if "department" in df.columns else None
    checks["missing_satisfaction"] = int(df["satisfaction_score"].isna().sum()) if "satisfaction_score" in df.columns else None
    return checks


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Transform original Kaggle dataset into anonymized and cleaned versions."""
    print("=" * 60)
    print("ALISTOCARE DATA TRANSFORMATION")
    print("=" * 60)
    print()

    # Ensure original file exists
    if not ensure_original_file(ORIGINAL_FILE):
        print(f"\n❌ Cannot proceed without {ORIGINAL_FILE.name}")
        print("   Upload the file to this Colab session and re-run.")
        sys.exit(1)

    # Step 1: Load original
    print("Step 1: Loading original dataset...")
    df = load_original(ORIGINAL_FILE)
    print()

    # Step 2: Anonymize PII
    print("Step 2: Anonymizing PII (RA 10173 compliance)...")
    df = anonymize_pii(df)
    print()

    # Step 3: Rename columns
    print("Step 3: Renaming columns to snake_case...")
    df = rename_columns(df)
    print()

    # Step 4: Fix data errors
    print("Step 4: Fixing data entry errors...")
    df = fix_data_errors(df)
    print()

    # Step 5: Parse datetime
    print("Step 5: Parsing date/time fields...")
    df = parse_datetime(df)
    print()

    # Step 6: Add derived fields
    print("Step 6: Adding derived fields...")
    df = add_derived_fields(df)
    print()

    # Step 7: Save anonymized version (no derived fields, just anonymized core)
    print("Step 7: Saving anonymized dataset...")
    anonymized_cols = [
        "patient_id", "admission_date", "admission_time", "gender", "age",
        "race", "department", "admission_flag", "satisfaction_score", "wait_time_minutes",
    ]
    # Keep only columns that exist
    existing_anon_cols = [c for c in anonymized_cols if c in df.columns]
    anonymized_df = df[existing_anon_cols].copy()
    anonymized_df.to_csv(ANONYMIZED_FILE, index=False)
    print(f"✅ Saved: {ANONYMIZED_FILE} ({len(anonymized_df):,} rows × {len(existing_anon_cols)} columns)")
    print()

    # Step 8: Save cleaned version (with derived fields)
    print("Step 8: Saving cleaned dataset...")
    df.to_csv(CLEANED_FILE, index=False)
    print(f"✅ Saved: {CLEANED_FILE} ({len(df):,} rows × {df.shape[1]} columns)")
    print()

    # Step 9: Validate
    print("Step 9: Validation checks...")
    checks = validate_cleaned(df)
    print(f"  Rows: {checks['rows']:,} (≥1,000: {'PASS' if checks['rows'] >= 1000 else 'FAIL'})")
    print(f"  Columns: {checks['columns']} (≥8: {'PASS' if checks['columns'] >= 8 else 'FAIL'})")
    print(f"  Duplicate rows: {checks['duplicate_rows']}")
    print(f"  Duplicate patient_ids: {checks['duplicate_patient_ids']}")
    print(f"  Missing core fields: {checks['missing_core']}")
    print(f"  Missing department: {checks['missing_department']} (documented, not imputed)")
    print(f"  Missing satisfaction: {checks['missing_satisfaction']} (documented, not imputed)")
    print()

    # Summary
    print("=" * 60)
    print("TRANSFORMATION COMPLETE")
    print("=" * 60)
    print()
    print("Output files:")
    print(f"  • {ANONYMIZED_FILE} — PII removed, core fields only")
    print(f"  • {CLEANED_FILE} — cleaned + derived fields, ready for analysis")
    print()
    print("Privacy: SSN-format IDs pseudonymized, name column dropped (RA 10173)")
    print("Source: Kaggle CC0 Public Domain — safe for public sharing including GitHub")
    print("=" * 60)


# Colab-compatible: runs when cell is executed
main()