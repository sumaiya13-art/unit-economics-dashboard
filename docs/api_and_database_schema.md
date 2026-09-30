# API Endpoints & Database Schema Specification

This document details the HTTP web server API endpoints, data models, response formats, and CSV database dictionary schemas for the Unit Economics Dashboard.

---

## 1. HTTP Web Server API Endpoints (`src/dashboard.py`)

The Unit Economics Dashboard includes a built-in, lightweight HTTP web server built using Python's standard `http.server` library.

### Server Execution Command:
```bash
python src/dashboard.py
```
- **Default Host**: `localhost` (`127.0.0.1`)
- **Default Port**: `8000`

---

### Endpoint Reference Table

| HTTP Method | Route / Endpoint | Description | Content Type | Response Payload / Behavior |
|---|---|---|---|---|
| `GET` | `/` | Root web route | `text/html` | Serves the interactive `dashboard.html` single-page UI. |
| `GET` | `/dashboard` | Dashboard web route | `text/html` | Alias for `/dashboard.html`. |
| `GET` | `/dashboard.html` | Static dashboard asset | `text/html` | Serves `dashboard.html` with embedded CSS and JavaScript. |

---

## 2. CSV Database Dictionary Schemas

The data layer uses standard CSV files stored in `data/` and `data/cleaned/`.

### Table 1: Raw Cloud Billing (`data/billing.csv` & `data/cleaned/billing.csv`)
- **Description**: Contains daily cloud infrastructure spending breakdowns per service, product, and customer.

| Column Name | Data Type | Key Type | Description | Example Value |
|---|---|---|---|---|
| `billing_id` | String | Primary Key | Unique billing line item identifier | `BILL-000001` |
| `date` | String (YYYY-MM-DD) | Dimension | Date of billing entry | `2026-03-21` |
| `cloud_service` | String | Dimension | Cloud service type (`Compute`, `Storage`, `Data Transfer`) | `Compute` |
| `product_id` | String | Foreign Key | Accountable product ID (`PROD_VOD`, `PROD_LIVE`, `UNALLOCATED_RECOVERY`)| `PROD_VOD` |
| `customer_id` | String | Foreign Key | Accountable customer ID (`CUST_101` through `CUST_106`) | `CUST_106` |
| `compute_cost` | Float | Metric | Compute cost incurred ($) | `55.75` |
| `storage_cost` | Float | Metric | Storage cost incurred ($) | `12.81` |
| `transfer_cost` | Float | Metric | Network data transfer cost ($) | `38.93` |
| `total_cost` | Float | Metric | Sum of compute, storage, and transfer costs ($) | `107.49` |

---

### Table 2: Usage Telemetry (`data/usage_telemetry.csv` & `data/cleaned/usage_telemetry.csv`)
- **Description**: Contains fine-grained event telemetry logged during video processing sessions.

| Column Name | Data Type | Key Type | Description | Example Value |
|---|---|---|---|---|
| `event_id` | String | Primary Key | Unique telemetry event log identifier | `EVT-000001` |
| `timestamp` | String (ISO 8601) | Dimension | ISO timestamp of video processing session | `2026-03-01 08:04:00` |
| `product_id` | String | Foreign Key | Product line executing processing session | `PROD_LIVE` |
| `customer_id` | String | Foreign Key | Customer owning video asset | `CUST_103` |
| `video_id` | String | Dimension | Unique video asset identifier | `VID-01001` |
| `processing_minutes` | Float | Metric | Duration of video transcode/stream (minutes) | `32.6` |
| `storage_gb` | Float | Metric | Output video file size (GB) | `12.04` |
| `transfer_gb` | Float | Metric | Bandwidth transferred/streamed (GB) | `12.37` |
| `event_status` | String | Dimension | Status (`normal`, `delayed`, `duplicate`, `out_of_order`, `reconciled`)| `normal` |

---

### Table 3: Allocation Tags (`data/allocation_tags.csv` & `data/cleaned/allocation_tags.csv`)
- **Description**: Contains resource tagging metadata linking cloud infrastructure to accountable engineering teams.

| Column Name | Data Type | Key Type | Description | Example Value |
|---|---|---|---|---|
| `tag_id` | String | Primary Key | Unique allocation tag identifier | `TAG-000001` |
| `product_id` | String | Foreign Key | Product line mapped to resource | `PROD_OTT` |
| `customer_id` | String | Foreign Key | Customer account mapped to resource | `CUST_102` |
| `team` | String | Dimension | Accountable engineering team | `Media-Core` |
| `environment` | String | Dimension | Deployment environment (`Production`, `Development`) | `Production` |
| `service` | String | Dimension | Corresponding cloud service | `Compute` |
| `tag_status` | String | Dimension | Quality status (`Valid`, `Missing`, `Invalid`, `Valid_Recovered`) | `Valid` |

---

### Table 4: Product Activity (`data/product_activity.csv` & `data/cleaned/product_activity.csv`)
- **Description**: Contains daily aggregated business volume, workload metrics, and customer revenue.

| Column Name | Data Type | Key Type | Description | Example Value |
|---|---|---|---|---|
| `activity_id` | String | Primary Key | Unique product activity record identifier | `ACT-000001` |
| `date` | String (YYYY-MM-DD) | Dimension | Activity summary date | `2026-03-02` |
| `product_id` | String | Foreign Key | Product line identifier | `PROD_LIVE` |
| `customer_id` | String | Foreign Key | Customer account identifier | `CUST_104` |
| `videos_processed` | Integer | Metric | Total video assets processed | `58` |
| `processing_hours` | Float | Metric | Total video processing duration (hours) | `9.38` |
| `storage_gb` | Float | Metric | Total storage volume accumulated (GB) | `121.68` |
| `transfer_gb` | Float | Metric | Total bandwidth consumed (GB) | `463.06` |
| `revenue` | Float | Metric | Customer subscription/usage revenue ($) | `1111.38` |
