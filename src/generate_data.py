"""
Synthetic Data Generator Module for Media Platform Unit Economics Dashboard.

This module generates 4 correlated synthetic datasets simulating a media platform's
cloud billing exports, operational video telemetry logs, resource allocation tags,
and daily product activity/revenue figures.

Datasets Generated:
1. data/billing.csv (2,525 rows | 9 columns)
2. data/usage_telemetry.csv (3,030 rows | 9 columns)
3. data/allocation_tags.csv (2,000 rows | 7 columns)
4. data/product_activity.csv (2,400 rows | 9 columns)

Author: Unit Economics Engineering Team
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd

# Set fixed random seed for 100% reproducible synthetic data generation
random.seed(42)

# Platform Entity Constants
PRODUCTS = ["PROD_VOD", "PROD_LIVE", "PROD_OTT", "PROD_ENCODE"]
CUSTOMERS = ["CUST_101", "CUST_102", "CUST_103", "CUST_104", "CUST_105", "CUST_106"]
TEAMS = ["Media-Core", "Streaming-Team", "Encoding-Team", "Platform-Team"]
ENVIRONMENTS = ["Production", "Development"]
SERVICES = ["Compute", "Storage", "Data Transfer"]


def ensure_directories():
    """
    Ensure output storage directories ('data' and 'reports') exist.
    
    Prevents FileNotFoundError during CSV writing operations.
    """
    for folder in ["data", "reports"]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def generate_billing_dataset(num_rows=2500):
    """
    Generate 9-column billing.csv dataset with correlated cloud compute/storage/transfer costs.

    Parameters:
        num_rows (int): Target number of primary billing records to generate (default 2500).

    Data Flaws Injected (~2%):
        - Missing product_id values (null tags)
        - Invalid negative cost values (-45.0)
        - Duplicate billing line items
    """
    start_date = datetime(2026, 3, 1)
    data = []

    for i in range(1, num_rows + 1):
        billing_id = f"BILL-{i:06d}"
        day_offset = random.randint(0, 29)
        record_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        service = random.choice(SERVICES)
        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)

        # Higher workload multiplier for Enterprise customer tiers (CUST_101, CUST_102)
        multiplier = 2.5 if customer in ["CUST_101", "CUST_102"] else 1.0

        compute = round(random.uniform(20.0, 150.0) * multiplier, 2)
        storage = round(random.uniform(5.0, 40.0) * multiplier, 2)
        transfer = round(random.uniform(8.0, 50.0) * multiplier, 2)

        # Inject synthetic data quality flaws for validation testing
        if i % 50 == 0:
            product = None  # Missing tag anomaly
        if i % 75 == 0:
            compute = -45.0  # Invalid negative cost anomaly

        total = round(compute + storage + transfer, 2) if compute > 0 else -10.0
        data.append([billing_id, record_date, service, product, customer, compute, storage, transfer, total])

    # Inject duplicate billing records
    for i in range(25):
        data.append(data[i * 10].copy())

    columns = [
        "billing_id", "date", "cloud_service", "product_id", "customer_id",
        "compute_cost", "storage_cost", "transfer_cost", "total_cost"
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("data/billing.csv", index=False)
    print(f"Generated data/billing.csv with {len(df)} rows and {len(columns)} columns.")


def generate_telemetry_dataset(num_rows=3000):
    """
    Generate 9-column usage_telemetry.csv dataset representing event logs.

    Parameters:
        num_rows (int): Target number of event log records (default 3000).

    Data Flaws Injected:
        - Delayed event arrivals (event_status='delayed')
        - Out-of-order log timestamps (event_status='out_of_order')
        - Negative processing durations
        - Duplicate event records (event_status='duplicate')
    """
    start_date = datetime(2026, 3, 1, 8, 0, 0)
    data = []

    for i in range(1, num_rows + 1):
        event_id = f"EVT-{i:06d}"
        minute_offset = i * 4
        event_time = start_date + timedelta(minutes=minute_offset)

        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)
        video_id = f"VID-{(i % 400) + 1000:05d}"

        multiplier = 2.0 if customer in ["CUST_101", "CUST_102"] else 1.0
        proc_min = round(random.uniform(5.0, 60.0) * multiplier, 1)
        storage_gb = round(random.uniform(1.0, 15.0) * multiplier, 2)
        transfer_gb = round(random.uniform(2.0, 35.0) * multiplier, 2)
        event_status = "normal"

        if i % 80 == 0:
            event_time = event_time + timedelta(days=7)
            event_status = "delayed"
        elif i % 90 == 0:
            event_time = event_time - timedelta(hours=36)
            event_status = "out_of_order"
        elif i % 100 == 0:
            proc_min = -15.0
            event_status = "normal"

        time_str = event_time.strftime("%Y-%m-%d %H:%M:%S")
        data.append([event_id, time_str, product, customer, video_id, proc_min, storage_gb, transfer_gb, event_status])

    for i in range(30):
        dup_row = data[i * 20].copy()
        dup_row[8] = "duplicate"
        data.append(dup_row)

    columns = [
        "event_id", "timestamp", "product_id", "customer_id", "video_id",
        "processing_minutes", "storage_gb", "transfer_gb", "event_status"
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("data/usage_telemetry.csv", index=False)
    print(f"Generated data/usage_telemetry.csv with {len(df)} rows and {len(columns)} columns.")


def generate_allocation_tags_dataset(num_rows=2000):
    """
    Generate 7-column allocation_tags.csv dataset containing resource tagging metadata.
    """
    data = []
    for i in range(1, num_rows + 1):
        tag_id = f"TAG-{i:06d}"
        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)
        team = random.choice(TEAMS)
        env = random.choice(ENVIRONMENTS)
        service = random.choice(SERVICES)
        tag_status = "Valid"

        if i % 35 == 0:
            tag_status = "Missing"
            product = None
        elif i % 45 == 0:
            tag_status = "Invalid"

        data.append([tag_id, product, customer, team, env, service, tag_status])

    columns = ["tag_id", "product_id", "customer_id", "team", "environment", "service", "tag_status"]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("data/allocation_tags.csv", index=False)
    print(f"Generated data/allocation_tags.csv with {len(df)} rows and {len(columns)} columns.")


def generate_product_activity_dataset(num_rows=2400):
    """
    Generate 9-column product_activity.csv dataset containing daily business revenue and volume.
    """
    start_date = datetime(2026, 3, 1)
    data = []

    for i in range(1, num_rows + 1):
        activity_id = f"ACT-{i:06d}"
        day_offset = (i % 30)
        record_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        product = random.choice(PRODUCTS)
        customer = random.choice(CUSTOMERS)

        videos = random.randint(10, 150)
        proc_hours = round(videos * random.uniform(0.1, 0.4), 2)
        storage_gb = round(videos * random.uniform(2.0, 5.0), 2)
        transfer_gb = round(videos * random.uniform(4.0, 10.0), 2)
        revenue = round(videos * random.uniform(8.0, 25.0), 2)

        data.append([activity_id, record_date, product, customer, videos, proc_hours, storage_gb, transfer_gb, revenue])

    columns = [
        "activity_id", "date", "product_id", "customer_id", "videos_processed",
        "processing_hours", "storage_gb", "transfer_gb", "revenue"
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("data/product_activity.csv", index=False)
    print(f"Generated data/product_activity.csv with {len(df)} rows and {len(columns)} columns.")


if __name__ == "__main__":
    ensure_directories()
    generate_billing_dataset(num_rows=2500)
    generate_telemetry_dataset(num_rows=3000)
    generate_allocation_tags_dataset(num_rows=2000)
    generate_product_activity_dataset(num_rows=2400)
    print("\nAll 4 updated synthetic datasets created successfully.")
