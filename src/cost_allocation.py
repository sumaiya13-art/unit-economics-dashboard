"""
Usage-Based Cost Allocation & Unit Economics Engine for Media Platform.

This module attributes cloud compute, storage, and bandwidth spend down to individual
product lines and customer accounts based on operational telemetry usage shares.

Calculates 11 Core Unit Economics KPIs:
1. Total Cloud Cost ($)
2. Allocated Cloud Cost ($)
3. Unallocated Cloud Cost ($)
4. Allocation Coverage % (%)
5. Cost per Video Asset ($)
6. Cost per Processing Hour ($)
7. Average Cost per Product ($)
8. Average Cost per Customer ($)
9. Total Revenue ($)
10. Cost-to-Revenue Ratio (%)
11. Gross Margin ($)

Author: Unit Economics Engineering Team
"""

import os
import pandas as pd


def load_data():
    """
    Load datasets for cost allocation.
    
    Prefers cleaned datasets in data/cleaned/ if available, otherwise falls back to data/.
    """
    if os.path.exists("data/cleaned/billing.csv"):
        billing_df = pd.read_csv("data/cleaned/billing.csv")
        telemetry_df = pd.read_csv("data/cleaned/usage_telemetry.csv")
        activity_df = pd.read_csv("data/cleaned/product_activity.csv")
    else:
        billing_df = pd.read_csv("data/billing.csv")
        telemetry_df = pd.read_csv("data/usage_telemetry.csv")
        activity_df = pd.read_csv("data/product_activity.csv")
    return billing_df, telemetry_df, activity_df


def calculate_usage_shares(telemetry_df):
    """
    Calculate usage proportions by product and customer from clean event telemetry.

    Formula:
        Usage Share = Product Processing Minutes / Total Processing Minutes

    Returns:
        product_usage (DataFrame): Product IDs, total minutes, and usage shares.
        customer_usage (DataFrame): Customer IDs, total minutes, and usage shares.
        total_minutes (float): Total processing duration across valid telemetry.
    """
    valid_telemetry = telemetry_df[
        (telemetry_df["processing_minutes"] > 0) & 
        (telemetry_df["product_id"].notnull()) &
        (telemetry_df["customer_id"].notnull()) &
        (telemetry_df["product_id"] != "UNALLOCATED_RECOVERY")
    ]

    total_minutes = valid_telemetry["processing_minutes"].sum()

    # Product level usage share calculation
    product_usage = valid_telemetry.groupby("product_id")["processing_minutes"].sum().reset_index()
    product_usage["usage_share"] = product_usage["processing_minutes"] / total_minutes

    # Customer level usage share calculation
    customer_usage = valid_telemetry.groupby("customer_id")["processing_minutes"].sum().reset_index()
    customer_usage["usage_share"] = customer_usage["processing_minutes"] / total_minutes

    return product_usage, customer_usage, total_minutes


def perform_cost_allocation():
    """
    Perform usage-based cost allocation and calculate unit economics KPIs.
    """
    billing_df, telemetry_df, activity_df = load_data()

    # 1. Total Cloud Cost from Billing dataset
    total_cloud_cost = billing_df["total_cost"].sum()

    # Valid billing records (attributed products)
    valid_billing = billing_df[
        (billing_df["product_id"].notnull()) & 
        (billing_df["product_id"] != "UNALLOCATED_RECOVERY") &
        (billing_df["total_cost"] >= 0)
    ]
    allocatable_cost = valid_billing["total_cost"].sum()
    unallocated_cost = total_cloud_cost - allocatable_cost

    # Calculate usage shares
    product_usage, customer_usage, total_minutes = calculate_usage_shares(telemetry_df)

    # 2. Product-level Allocation: Allocated Cost = Usage Share * Allocatable Cost
    product_allocation = product_usage.copy()
    product_allocation["allocated_cost"] = product_allocation["usage_share"] * allocatable_cost

    # 3. Customer-level Allocation: Allocated Cost = Usage Share * Allocatable Cost
    customer_allocation = customer_usage.copy()
    customer_allocation["allocated_cost"] = customer_allocation["usage_share"] * allocatable_cost

    # 4. Coverage calculation
    allocated_cloud_cost = product_allocation["allocated_cost"].sum()
    coverage_pct = (allocated_cloud_cost / total_cloud_cost) * 100 if total_cloud_cost > 0 else 0

    # 5. Activity totals for Unit Economics KPIs
    total_videos = activity_df["videos_processed"].sum()
    total_hours = activity_df["processing_hours"].sum()
    total_revenue = activity_df["revenue"].sum()

    # 6. Unit Economics KPIs
    cost_per_video = allocated_cloud_cost / total_videos if total_videos > 0 else 0
    cost_per_hour = allocated_cloud_cost / total_hours if total_hours > 0 else 0
    avg_cost_per_product = allocated_cloud_cost / len(product_allocation) if len(product_allocation) > 0 else 0
    avg_cost_per_customer = allocated_cloud_cost / len(customer_allocation) if len(customer_allocation) > 0 else 0
    cost_to_revenue_pct = (allocated_cloud_cost / total_revenue) * 100 if total_revenue > 0 else 0
    gross_margin = total_revenue - allocated_cloud_cost

    print("==================================================")
    print("         UNIT ECONOMICS DASHBOARD (50% MILESTONE) ")
    print("==================================================")
    print(f"1. Total Cloud Cost:          ${total_cloud_cost:,.2f}")
    print(f"2. Allocated Cloud Cost:      ${allocated_cloud_cost:,.2f}")
    print(f"3. Unallocated Cloud Cost:    ${unallocated_cost:,.2f}")
    print(f"4. Allocation Coverage %:     {coverage_pct:.2f}%")
    print("--------------------------------------------------")
    print(f"5. Cost per Video:            ${cost_per_video:.2f}")
    print(f"6. Cost per Processing Hour:  ${cost_per_hour:.2f}")
    print(f"7. Cost per Product (Avg):    ${avg_cost_per_product:,.2f}")
    print(f"8. Cost per Customer (Avg):   ${avg_cost_per_customer:,.2f}")
    print("--------------------------------------------------")
    print(f"9. Total Revenue:             ${total_revenue:,.2f}")
    print(f"10. Cost-to-Revenue %:        {cost_to_revenue_pct:.2f}%")
    print(f"11. Gross Margin:             ${gross_margin:,.2f}")
    print("==================================================\n")

    print("--- PRODUCT LEVEL COST ALLOCATION ---")
    for _, row in product_allocation.iterrows():
        print(f"Product: {row['product_id']:<12} | Usage Share: {row['usage_share']*100:6.2f}% | Allocated Cost: ${row['allocated_cost']:10.2f}")

    print("\n--- CUSTOMER LEVEL COST ALLOCATION ---")
    for _, row in customer_allocation.iterrows():
        print(f"Customer: {row['customer_id']:<12} | Usage Share: {row['usage_share']*100:6.2f}% | Allocated Cost: ${row['allocated_cost']:10.2f}")


if __name__ == "__main__":
    perform_cost_allocation()
