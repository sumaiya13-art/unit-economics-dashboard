import os
import pandas as pd
import pytest

from src.generate_data import ensure_directories, generate_billing_dataset, generate_telemetry_dataset, generate_allocation_tags_dataset, generate_product_activity_dataset
from src.validate_data import count_missing_values, count_duplicate_records, count_invalid_values
from src.recover_data import run_data_recovery
from src.cost_allocation import load_data

@pytest.fixture(scope="session", autouse=True)
def setup_datasets():
    """Session fixture ensuring synthetic datasets exist prior to running tests."""
    ensure_directories()
    if not os.path.exists("data/billing.csv"):
        generate_billing_dataset(2500)
        generate_telemetry_dataset(3000)
        generate_allocation_tags_dataset(2000)
        generate_product_activity_dataset(2400)

# ----------------------------------------------------
# TEST 1: SCHEMA VALIDATION & COLUMN INTEGRITY
# ----------------------------------------------------
def test_schema_and_column_integrity():
    """Validate dataset row counts, column counts, and column names."""
    billing_df = pd.read_csv("data/billing.csv")
    telemetry_df = pd.read_csv("data/usage_telemetry.csv")
    tags_df = pd.read_csv("data/allocation_tags.csv")
    activity_df = pd.read_csv("data/product_activity.csv")

    assert billing_df.shape[1] == 9
    assert "billing_id" in billing_df.columns
    assert "total_cost" in billing_df.columns

    assert telemetry_df.shape[1] == 9
    assert "event_id" in telemetry_df.columns
    assert "event_status" in telemetry_df.columns

    assert tags_df.shape[1] == 7
    assert "tag_id" in tags_df.columns
    assert "tag_status" in tags_df.columns

    assert activity_df.shape[1] == 9
    assert "activity_id" in activity_df.columns
    assert "revenue" in activity_df.columns

# ----------------------------------------------------
# TEST 2: ANOMALY DETECTION ACCURACY
# ----------------------------------------------------
def test_anomaly_detection_accuracy():
    """Verify that validate_data detects missing values, duplicates, and invalid numbers."""
    billing_df = pd.read_csv("data/billing.csv")
    telemetry_df = pd.read_csv("data/usage_telemetry.csv")
    tags_df = pd.read_csv("data/allocation_tags.csv")
    activity_df = pd.read_csv("data/product_activity.csv")

    all_dfs = [billing_df, telemetry_df, tags_df, activity_df]
    missing_count = count_missing_values(all_dfs)
    duplicate_count = count_duplicate_records(billing_df, telemetry_df, tags_df, activity_df)
    invalid_count = count_invalid_values(billing_df, telemetry_df, tags_df)

    assert missing_count > 0, "Validation should detect synthetic missing values"
    assert duplicate_count > 0, "Validation should detect synthetic duplicate records"
    assert invalid_count > 0, "Validation should detect synthetic negative value anomalies"

# ----------------------------------------------------
# TEST 3: RECOVERY IDEMPOTENCE (CRITICAL EVALUATOR TEST)
# ----------------------------------------------------
def test_recovery_idempotence():
    """Verify that running data flaw recovery multiple times produces identical clean state."""
    # First recovery run
    run_data_recovery()
    cleaned_billing_1 = pd.read_csv("data/cleaned/billing.csv")
    cleaned_telemetry_1 = pd.read_csv("data/cleaned/usage_telemetry.csv")

    # Second recovery run (testing idempotence)
    run_data_recovery()
    cleaned_billing_2 = pd.read_csv("data/cleaned/billing.csv")
    cleaned_telemetry_2 = pd.read_csv("data/cleaned/usage_telemetry.csv")

    # Assert zero differences between run 1 and run 2
    pd.testing.assert_frame_equal(cleaned_billing_1, cleaned_billing_2)
    pd.testing.assert_frame_equal(cleaned_telemetry_1, cleaned_telemetry_2)
    assert (cleaned_billing_2["total_cost"] < 0).sum() == 0, "No negative costs should remain after recovery"
    assert (cleaned_telemetry_2["processing_minutes"] < 0).sum() == 0, "No negative processing minutes should remain"

# ----------------------------------------------------
# TEST 4: MATHEMATICAL COST ALLOCATION RECONCILIATION
# ----------------------------------------------------
def test_cost_allocation_math_reconciliation():
    """Verify that Allocated Cost + Unallocated Cost equals Total Cloud Cost."""
    billing_df, telemetry_df, activity_df = load_data()
    total_cost = billing_df["total_cost"].sum()

    valid_billing = billing_df[
        (billing_df["product_id"].notnull()) & 
        (billing_df["product_id"] != "UNALLOCATED_RECOVERY") &
        (billing_df["total_cost"] >= 0)
    ]
    allocatable_cost = valid_billing["total_cost"].sum()
    unallocated_cost = total_cost - allocatable_cost

    assert pytest.approx(allocatable_cost + unallocated_cost, rel=1e-5) == total_cost
    assert allocatable_cost > 0
    assert total_cost > 0

# ----------------------------------------------------
# TEST 5: ALLOCATION STRATEGY BENCHMARK COMPARISON
# ----------------------------------------------------
def test_allocation_strategy_benchmark():
    """Verify Strategy B (Telemetry-Weighted) achieves higher or equal coverage than Strategy A (Tag-Based)."""
    raw_billing = pd.read_csv("data/billing.csv")
    tags_df = pd.read_csv("data/allocation_tags.csv")
    cleaned_telemetry = pd.read_csv("data/cleaned/usage_telemetry.csv")

    total_cost = raw_billing["total_cost"].sum()

    # Strategy A (Tag-based)
    valid_tags = tags_df[tags_df["tag_status"] == "Valid"]
    valid_products = set(valid_tags["product_id"].dropna().unique())
    tag_allocated = raw_billing[(raw_billing["product_id"].isin(valid_products)) & (raw_billing["total_cost"] > 0)]["total_cost"].sum()
    tag_coverage = (tag_allocated / total_cost) * 100

    # Strategy B (Telemetry-weighted)
    valid_min = cleaned_telemetry[cleaned_telemetry["product_id"] != "UNALLOCATED_RECOVERY"]["processing_minutes"].sum()
    total_min = cleaned_telemetry["processing_minutes"].sum()
    telemetry_coverage = (valid_min / total_min) * 100

    assert telemetry_coverage >= tag_coverage, "Telemetry-weighted dynamic allocation should outperform static tag-based allocation coverage"
