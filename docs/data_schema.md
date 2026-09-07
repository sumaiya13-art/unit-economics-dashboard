# Data Schema Specification (Updated)

This document details the updated data schema, exact columns, data types, example values, and entity relationships for all 4 synthetic datasets stored in `data/`.

---

## 1. Billing Dataset (`data/billing.csv`) — 9 Columns
Contains daily cloud provider spending breakdowns per service, product, and customer.

| # | Column Name | Data Type | Business Meaning | Example Value | Relationship |
|---|---|---|---|---|---|
| 1 | `billing_id` | String | Unique billing line item ID | `BILL-000001` | Primary Key |
| 2 | `date` | String (YYYY-MM-DD) | Date of billing entry | `2026-03-01` | Dimension |
| 3 | `cloud_service` | String | Cloud service type (`Compute`, `Storage`, `Data Transfer`) | `Compute` | Dimension |
| 4 | `product_id` | String | Associated product ID | `PROD_VOD`, `PROD_LIVE` | Foreign Key -> `allocation_tags.product_id` |
| 5 | `customer_id` | String | Associated customer ID | `CUST_101` | Foreign Key -> `allocation_tags.customer_id` |
| 6 | `compute_cost` | Float | Cost incurred for compute ($) | `145.20` | Metric |
| 7 | `storage_cost` | Float | Cost incurred for storage ($) | `32.50` | Metric |
| 8 | `transfer_cost` | Float | Cost incurred for bandwidth transfer ($) | `18.40` | Metric |
| 9 | `total_cost` | Float | Sum of compute, storage, & transfer cost ($) | `196.10` | Metric |

---

## 2. Usage Telemetry Dataset (`data/usage_telemetry.csv`) — 9 Columns
Contains event-level processing telemetry logged during video processing operations.

| # | Column Name | Data Type | Business Meaning | Example Value | Relationship |
|---|---|---|---|---|---|
| 1 | `event_id` | String | Unique telemetry event ID | `EVT-000001` | Primary Key |
| 2 | `timestamp` | String (ISO 8601) | Event logging timestamp | `2026-03-01 10:15:30` | Dimension |
| 3 | `product_id` | String | Product processing the video | `PROD_VOD` | Foreign Key |
| 4 | `customer_id` | String | Customer owning the video | `CUST_101` | Foreign Key |
| 5 | `video_id` | String | Video asset identifier | `VID-10024` | Dimension |
| 6 | `processing_minutes` | Float | Duration of video processing | `24.5` | Metric |
| 7 | `storage_gb` | Float | Output video file size (GB) | `6.8` | Metric |
| 8 | `transfer_gb` | Float | Bandwidth streamed/transferred (GB) | `14.2` | Metric |
| 9 | `event_status` | String | Quality status (`normal`, `delayed`, `duplicate`, `out_of_order`) | `normal` | Dimension |

---

## 3. Allocation Tags Dataset (`data/allocation_tags.csv`) — 7 Columns
Contains tagging metadata used to link cloud resources to accountable teams and environments.

| # | Column Name | Data Type | Business Meaning | Example Value | Relationship |
|---|---|---|---|---|---|
| 1 | `tag_id` | String | Unique allocation tag ID | `TAG-000001` | Primary Key |
| 2 | `product_id` | String | Product identifier | `PROD_VOD` | Foreign Key |
| 3 | `customer_id` | String | Customer identifier | `CUST_101` | Foreign Key |
| 4 | `team` | String | Accountable engineering team | `Media-Core` | Dimension |
| 5 | `environment` | String | Deployment environment (`Production`, `Development`) | `Production` | Dimension |
| 6 | `service` | String | Corresponding cloud service | `Compute` | Dimension |
| 7 | `tag_status` | String | Tag quality status (`Valid`, `Missing`, `Invalid`) | `Valid` | Dimension |

---

## 4. Product Activity Dataset (`data/product_activity.csv`) — 9 Columns
Contains daily aggregated business volume, workload metrics, and customer revenue.

| # | Column Name | Data Type | Business Meaning | Example Value | Relationship |
|---|---|---|---|---|---|
| 1 | `activity_id` | String | Unique product activity record ID | `ACT-000001` | Primary Key |
| 2 | `date` | String (YYYY-MM-DD) | Activity summary date | `2026-03-01` | Dimension |
| 3 | `product_id` | String | Product identifier | `PROD_VOD` | Foreign Key |
| 4 | `customer_id` | String | Customer identifier | `CUST_101` | Foreign Key |
| 5 | `videos_processed` | Integer | Total videos processed on date | `35` | Metric |
| 6 | `processing_hours` | Float | Total video processing duration (hours) | `14.2` | Metric |
| 7 | `storage_gb` | Float | Total storage accumulated (GB) | `240.5` | Metric |
| 8 | `transfer_gb` | Float | Total bandwidth consumed (GB) | `510.0` | Metric |
| 9 | `revenue` | Float | Customer subscription/usage revenue ($) | `1250.00` | Metric |
