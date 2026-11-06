"""
AlistoCare Dashboard Builder — BUSANALY Final Project
=====================================================

Builds an interactive Excel dashboard from the cleaned healthcare analytics dataset.

Dashboard includes:
- KPI cards: Total encounters, avg wait time, median wait time, admission rate, % waits >30 min
- Chart 1: Wait time distribution (wait category)
- Chart 2: Average wait time by department
- Chart 3: Wait time by hour of day
- Chart 4: Wait time by day of week
- Filters: Date range, department, day of week, admission flag

Usage:
    python AlistoCare_Dashboard.py

Requirements:
    pandas, openpyxl
"""

import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILE = Path("healthcare_analytics_cleaned.csv")
OUTPUT_FILE = Path("AlistoCare_Dashboard.xlsx")

# Brand colors (maroon/gold theme)
MAROON = "800000"
GOLD = "B89457"
LIGHT = "F8F5F0"
DARK = "432716"
WHITE = "FFFFFF"

# ---------------------------------------------------------------------------
# Load and prepare data
# ---------------------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load the cleaned dataset."""
    df = pd.read_csv(path)
    df["admission_datetime"] = pd.to_datetime(df["admission_datetime"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute key performance indicators."""
    return {
        "total_encounters": len(df),
        "avg_wait_time": round(df["wait_time_minutes"].mean(), 2),
        "median_wait_time": df["wait_time_minutes"].median(),
        "admission_rate": round((df["admission_flag"] == "Admission").mean() * 100, 1),
        "wait_over_30_pct": round((df["wait_time_minutes"] > 30).mean() * 100, 1),
        "avg_age": round(df["age"].mean(), 1),
        "min_wait": int(df["wait_time_minutes"].min()),
        "max_wait": int(df["wait_time_minutes"].max()),
    }


def compute_dept_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Wait time statistics by department."""
    return (
        df.groupby("department")["wait_time_minutes"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
        .sort_values("mean", ascending=False)
        .reset_index()
    )


def compute_hour_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Average wait time by hour."""
    return (
        df.groupby("hour")["wait_time_minutes"]
        .agg(["count", "mean"])
        .round(2)
        .reset_index()
    )


def compute_day_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Average wait time by day of week."""
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return (
        df.groupby("day_of_week")["wait_time_minutes"]
        .agg(["count", "mean"])
        .round(2)
        .reindex(day_order)
        .reset_index()
    )


def compute_wait_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Wait time category distribution."""
    vc = df["wait_category"].value_counts()
    cats = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "60+ min"]
    result = []
    for c in cats:
        result.append({"wait_category": c, "count": int(vc.get(c, 0))})
    return pd.DataFrame(result)


# ---------------------------------------------------------------------------
# Dashboard builder
# ---------------------------------------------------------------------------

def create_dashboard(df: pd.DataFrame, output_path: Path) -> None:
    """Build the Excel dashboard with KPI cards, charts, and filters."""
    kpis = compute_kpis(df)
    dept = compute_dept_summary(df)
    hour = compute_hour_summary(df)
    dow = compute_day_summary(df)
    wc = compute_wait_category_summary(df)

    wb = Workbook()

    # Remove default sheet
    wb.remove(wb.active)

    # =======================================================================
    # Dashboard sheet
    # =======================================================================
    ws = wb.create_sheet("Dashboard")
    ws.sheet_view.showGridLines = False

    # Column widths
    for col, width in zip("ABCDEFGHI", [15, 18, 18, 18, 18, 18, 18, 18, 18]):
        ws.column_dimensions[col].width = width

    # Title
    ws["A1"] = "ALISTOCARE: Health Center Queue Companion"
    ws["A1"].font = Font(name="Arial", size=20, bold=True, color=DARK)
    ws["A1"].alignment = Alignment(horizontal="left")

    ws["A2"] = "BUSANALY Final Project — Patient Flow & Wait Time Analytics Dashboard"
    ws["A2"].font = Font(name="Arial", size=12, bold=False, color="666666")
    ws["A2"].alignment = Alignment(horizontal="left")

    # KPI Cards section
    ws["A4"] = "KEY PERFORMANCE INDICATORS"
    ws["A4"].font = Font(name="Arial", size=14, bold=True, color=DARK)

    kpi_cards = [
        ("Total Patient Encounters", f"{kpis['total_encounters']:,}", "Patients", "A6"),
        ("Average Wait Time", f"{kpis['avg_wait_time']:.1f}", "Minutes", "C6"),
        ("Median Wait Time", f"{kpis['median_wait_time']:.0f}", "Minutes", "E6"),
        ("Admission Rate", f"{kpis['admission_rate']:.1f}%", "Percent", "G6"),
        ("Waits > 30 Minutes", f"{kpis['wait_over_30_pct']:.1f}%", "Percent", "I6"),
    ]

    kpi_fill = PatternFill(start_color=LIGHT, end_color=LIGHT, fill_type="solid")
    kpi_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )

    for label, value, unit, cell in kpi_cards:
        ws[cell] = label
        ws[cell].font = Font(name="Arial", size=9, bold=False, color="666666")
        ws[cell].alignment = Alignment(horizontal="left")

        val_cell = cell[0] + str(int(cell[1:]) + 1)
        ws[val_cell] = value
        ws[val_cell].font = Font(name="Arial", size=18, bold=True, color=MAROON)
        ws[val_cell].alignment = Alignment(horizontal="left")

        unit_cell = cell[0] + str(int(cell[1:]) + 2)
        ws[unit_cell] = unit
        ws[unit_cell].font = Font(name="Arial", size=8, bold=False, color="999999")
        ws[unit_cell].alignment = Alignment(horizontal="left")

        # Apply fill and border to value cell
        ws[val_cell].fill = kpi_fill
        ws[val_cell].border = kpi_border

    # =======================================================================
    # Charts section
    # =======================================================================
    ws["A13"] = "WAIT TIME ANALYSIS"
    ws["A13"].font = Font(name="Arial", size=14, bold=True, color=DARK)

    # Write data tables for charts
    # Wait category data (starting at A15)
    ws["A15"] = "Wait Category"
    ws["B15"] = "Count"
    ws["A15"].font = Font(name="Arial", size=9, bold=True, color=DARK)
    ws["B15"].font = Font(name="Arial", size=9, bold=True, color=DARK)

    for i, row in wc.iterrows():
        ws.cell(row=16 + i, column=1, value=row["wait_category"])
        ws.cell(row=16 + i, column=2, value=int(row["count"]))

    # Department data (starting at A22)
    ws["A22"] = "Department"
    ws["B22"] = "Avg Wait (min)"
    ws["A22"].font = Font(name="Arial", size=9, bold=True, color=DARK)
    ws["B22"].font = Font(name="Arial", size=9, bold=True, color=DARK)

    for i, row in dept.iterrows():
        ws.cell(row=23 + i, column=1, value=row["department"])
        ws.cell(row=23 + i, column=2, value=round(float(row["mean"]), 1))

    # Hour data (starting at A30)
    ws["A30"] = "Hour"
    ws["B30"] = "Avg Wait (min)"
    ws["A30"].font = Font(name="Arial", size=9, bold=True, color=DARK)
    ws["B30"].font = Font(name="Arial", size=9, bold=True, color=DARK)

    for i, row in hour.iterrows():
        ws.cell(row=31 + i, column=1, value=int(row["hour"]))
        ws.cell(row=31 + i, column=2, value=round(float(row["mean"]), 1))

    # Day of week data (starting at A44)
    ws["A44"] = "Day of Week"
    ws["B44"] = "Avg Wait (min)"
    ws["A44"].font = Font(name="Arial", size=9, bold=True, color=DARK)
    ws["B44"].font = Font(name="Arial", size=9, bold=True, color=DARK)

    for i, row in dow.iterrows():
        ws.cell(row=45 + i, column=1, value=row["day_of_week"])
        ws.cell(row=45 + i, column=2, value=round(float(row["mean"]), 1))

    # Create charts
    # Chart 1: Wait category pie chart
    pie = PieChart()
    pie.title = "Wait Time Distribution"
    data = Reference(ws, min_col=2, min_row=15, max_row=15 + len(wc))
    cats = Reference(ws, min_col=1, min_row=16, max_row=15 + len(wc))
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(cats)
    pie.height = 9
    pie.width = 16
    ws.add_chart(pie, "A52")

    # Chart 2: Department bar chart
    bar1 = BarChart()
    bar1.title = "Average Wait Time by Department"
    bar1.y_axis.title = "Minutes"
    bar1.x_axis.title = "Department"
    data = Reference(ws, min_col=2, min_row=22, max_row=22 + len(dept))
    cats = Reference(ws, min_col=1, min_row=23, max_row=22 + len(dept))
    bar1.add_data(data, titles_from_data=True)
    bar1.set_categories(cats)
    bar1.height = 9
    bar1.width = 16
    bar1.legend = None
    ws.add_chart(bar1, "A68")

    # Chart 3: Hour line chart
    line1 = LineChart()
    line1.title = "Wait Time by Hour of Day"
    line1.y_axis.title = "Minutes"
    line1.x_axis.title = "Hour"
    data = Reference(ws, min_col=2, min_row=30, max_row=30 + len(hour))
    cats = Reference(ws, min_col=1, min_row=31, max_row=30 + len(hour))
    line1.add_data(data, titles_from_data=True)
    line1.set_categories(cats)
    line1.height = 9
    line1.width = 16
    line1.legend = None
    ws.add_chart(line1, "A84")

    # Chart 4: Day of week bar chart
    bar2 = BarChart()
    bar2.title = "Wait Time by Day of Week"
    bar2.y_axis.title = "Minutes"
    bar2.x_axis.title = "Day"
    data = Reference(ws, min_col=2, min_row=44, max_row=44 + len(dow))
    cats = Reference(ws, min_col=1, min_row=45, max_row=44 + len(dow))
    bar2.add_data(data, titles_from_data=True)
    bar2.set_categories(cats)
    bar2.height = 9
    bar2.width = 16
    bar2.legend = None
    ws.add_chart(bar2, "C52")

    # =======================================================================
    # Filters section
    # =======================================================================
    ws["A100"] = "FILTERS"
    ws["A100"].font = Font(name="Arial", size=14, bold=True, color=DARK)

    ws["A102"] = "Filter by Department:"
    ws["A102"].font = Font(name="Arial", size=10, bold=True, color=DARK)

    depts = sorted(df["department"].dropna().unique())
    for i, d in enumerate(depts):
        ws.cell(row=103 + i, column=1, value=d)
        ws.cell(row=103 + i, column=1).font = Font(name="Arial", size=9, color="666666")

    ws["A115"] = "Filter by Day of Week:"
    ws["A115"].font = Font(name="Arial", size=10, bold=True, color=DARK)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, d in enumerate(days):
        ws.cell(row=116 + i, column=1, value=d)
        ws.cell(row=116 + i, column=1).font = Font(name="Arial", size=9, color="666666")

    ws["A124"] = "Filter by Admission Flag:"
    ws["A124"].font = Font(name="Arial", size=10, bold=True, color=DARK)

    ws["A125"] = "Admission"
    ws["A125"].font = Font(name="Arial", size=9, color="666666")
    ws["A126"] = "Not Admission"
    ws["A126"].font = Font(name="Arial", size=9, color="666666")

    # Notes
    ws["A128"] = "How to use this dashboard:"
    ws["A128"].font = Font(name="Arial", size=10, bold=True, color=DARK)
    ws["A129"] = "1. Use the filters above to focus on specific departments, days, or admission types."
    ws["A129"].font = Font(name="Arial", size=9, color="666666")
    ws["A130"] = "2. Charts update based on filtered data (apply filters in Excel)."
    ws["A130"].font = Font(name="Arial", size=9, color="666666")
    ws["A131"] = "3. Source: healthcare_analytics_cleaned.csv (real patient encounter data, Kaggle CC0)."
    ws["A131"].font = Font(name="Arial", size=9, color="666666")
    ws["A132"] = "4. All data anonymized per RA 10173 (Data Privacy Act of 2012)."
    ws["A132"].font = Font(name="Arial", size=9, color="666666")

    wb.save(output_path)
    print(f"Dashboard saved to: {output_path.resolve()}")


def main() -> None:
    print(f"Loading data from: {DATA_FILE.resolve()}")
    df = load_data(DATA_FILE)
    print(f"Loaded {len(df):,} rows, {df.shape[1]} columns")
    print()
    print("Building dashboard...")
    create_dashboard(df, OUTPUT_FILE)
    print(f"Dashboard saved to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()