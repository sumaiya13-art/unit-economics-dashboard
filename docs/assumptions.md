# Project Assumptions

This document outlines the core assumptions made for the Unit Economics Dashboard (35% Foundation Prototype).

## 1. Data Availability & Frequency
- Billing exports and product activity reports are summarized at a daily level.
- Usage telemetry events are recorded at event-level timestamps for video processing sessions.

## 2. Resource & Cost Drivers
- Video processing workloads are driven by three main cloud cost categories:
  1. **Compute Cost**: Driven by video processing minutes (encoding, rendering).
  2. **Storage Cost**: Driven by stored video file sizes (Storage GB).
  3. **Data Transfer Cost**: Driven by streaming bandwidth and download volume (Transfer GB).

## 3. Allocation Tagging
- Allocation tags attempt to map resource IDs to products, customers, and teams.
- Not all cloud resources are tagged perfectly; untagged or unmapped usage is categorized as **Unallocated Cost**.

## 4. Financial & Revenue Assumptions
- Each product and customer has associated monthly subscription or usage revenue recorded in `product_activity.csv`.
- Revenue is compared against allocated cloud cost to compute product and customer-level Gross Margins.

## 5. Scope Boundary (35% Prototype)
- Data quality validation focuses on **Detection** of data flaws (missing values, duplicates, invalid values, delayed events, and out-of-order records).
- Data recovery, automated retry pipelines, interactive UI dashboards, and machine learning predictions are reserved for future phases (remaining 65%).
