import os
import pandas as pd

def load_all_datasets():
    """Load all 4 datasets from the data folder."""
    billing_df = pd.read_csv("data/billing.csv")
    telemetry_df = pd.read_csv("data/usage_telemetry.csv")
    tags_df = pd.read_csv("data/allocation_tags.csv")
    activity_df = pd.read_csv("data/product_activity.csv")
    return billing_df, telemetry_df, tags_df, activity_df

def count_missing_values(all_dfs):
    """Count null or missing values across all datasets."""
    total_missing = 0
    for df in all_dfs:
        total_missing += int(df.isnull().sum().sum())
    return total_missing

def count_duplicate_records(billing_df, telemetry_df, tags_df, activity_df):
    """Count duplicate rows across datasets including telemetry marked duplicates."""
    dups = 0
    dups += int(billing_df.duplicated(subset=["billing_id"]).sum())
    dups += int(telemetry_df[telemetry_df["event_status"] == "duplicate"].shape[0])
    dups += int(tags_df.duplicated(subset=["tag_id"]).sum())
    dups += int(activity_df.duplicated(subset=["activity_id"]).sum())
    return dups

def count_invalid_values(billing_df, telemetry_df, tags_df):
    """Count negative costs, negative usage, or invalid tag statuses."""
    invalid = 0
    # Negative costs in billing
    invalid += len(billing_df[billing_df["total_cost"] < 0])
    # Negative processing minutes in telemetry
    invalid += len(telemetry_df[telemetry_df["processing_minutes"] < 0])
    # Invalid tag status
    invalid += len(tags_df[tags_df["tag_status"] == "Invalid"])
    return invalid

def count_delayed_records(telemetry_df):
    """Count telemetry records flagged as delayed or arriving past normal range."""
    delayed = len(telemetry_df[telemetry_df["event_status"] == "delayed"])
    return delayed

def count_out_of_order_records(telemetry_df):
    """Count telemetry events logged out of chronological order."""
    out_of_order = len(telemetry_df[telemetry_df["event_status"] == "out_of_order"])
    return out_of_order

def run_data_validation():
    """Perform data validation across all 4 datasets and write report."""
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
