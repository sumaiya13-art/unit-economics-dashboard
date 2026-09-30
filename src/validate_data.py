"""
Data Quality Validation Engine for Media Platform Unit Economics Dashboard.

This module audits input datasets for 5 specific data quality flaw types:
1. Missing fields (null tag values)
2. Duplicate records (duplicate primary keys)
3. Invalid values (negative cost or processing minute figures)
4. Delayed event records (events logged outside normal processing windows)
5. Out-of-order records (non-monotonic timestamps)

Output:
- Console summary audit report
- reports/validation_report.csv

Author: Unit Economics Engineering Team
"""

import os
import pandas as pd


def load_all_datasets():
    """Load all 4 datasets from the data/ directory."""
    billing_df = pd.read_csv("data/billing.csv")
    telemetry_df = pd.read_csv("data/usage_telemetry.csv")
    tags_df = pd.read_csv("data/allocation_tags.csv")
    activity_df = pd.read_csv("data/product_activity.csv")
    return billing_df, telemetry_df, tags_df, activity_df


def count_missing_values(all_dfs):
    """Count total null or missing values across all datasets."""
    total_missing = 0
    for df in all_dfs:
        total_missing += int(df.isnull().sum().sum())
    return total_missing


def count_duplicate_records(billing_df, telemetry_df, tags_df, activity_df):
    """Count duplicate primary key records and flagged duplicate events."""
    dups = 0
    dups += int(billing_df.duplicated(subset=["billing_id"]).sum())
    dups += int(telemetry_df[telemetry_df["event_status"] == "duplicate"].shape[0])
    dups += int(tags_df.duplicated(subset=["tag_id"]).sum())
    dups += int(activity_df.duplicated(subset=["activity_id"]).sum())
    return dups


def count_invalid_values(billing_df, telemetry_df, tags_df):
    """Count negative cost figures, negative processing durations, or invalid tags."""
    invalid = 0
    invalid += len(billing_df[billing_df["total_cost"] < 0])
    invalid += len(telemetry_df[telemetry_df["processing_minutes"] < 0])
    invalid += len(tags_df[tags_df["tag_status"] == "Invalid"])
    return invalid


def count_delayed_records(telemetry_df):
    """Count telemetry records flagged as delayed (>7 days late)."""
    return len(telemetry_df[telemetry_df["event_status"] == "delayed"])


def count_out_of_order_records(telemetry_df):
    """Count telemetry events logged out of chronological sequence."""
    return len(telemetry_df[telemetry_df["event_status"] == "out_of_order"])


def run_data_validation():
    """Execute complete data quality validation audit across all datasets."""
    billing_df, telemetry_df, tags_df, activity_df = load_all_datasets()
    all_dfs = [billing_df, telemetry_df, tags_df, activity_df]

    total_rows = sum(len(df) for df in all_dfs)

    missing_cnt = count_missing_values(all_dfs)
    duplicate_cnt = count_duplicate_records(billing_df, telemetry_df, tags_df, activity_df)
    invalid_cnt = count_invalid_values(billing_df, telemetry_df, tags_df)
    delayed_cnt = count_delayed_records(telemetry_df)
    out_of_order_cnt = count_out_of_order_records(telemetry_df)

    report_rows = [
        ["Missing Values", missing_cnt],
        ["Duplicate Records", duplicate_cnt],
        ["Invalid Values", invalid_cnt],
        ["Delayed Records", delayed_cnt],
        ["Out-of-Order Records", out_of_order_cnt]
    ]

    table_data = []
    for metric_name, count in report_rows:
        pct = round((count / total_rows) * 100, 2)
        status = "WARNING" if count > 0 else "PASSED"
        table_data.append([metric_name, count, f"{pct}%", status])

    report_df = pd.DataFrame(table_data, columns=["Metric", "Count", "Percentage", "Status"])

    if not os.path.exists("reports"):
        os.makedirs("reports")
    report_df.to_csv("reports/validation_report.csv", index=False)

    print("--- DATA VALIDATION REPORT ---")
    print(report_df.to_string(index=False))
    print("\nReport exported to reports/validation_report.csv")


if __name__ == "__main__":
    run_data_validation()
