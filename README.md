# Unit Economics Cost Attribution Dashboard for Media Workloads

## Project Title
**Unit Economics Cost Attribution Dashboard for Media Workloads**

## Problem Statement
A media platform processes unpredictable video workloads (encoding, streaming, storage, distribution). Engineering and product teams receive aggregate monthly cloud provider bills (e.g. AWS invoices) but cannot attribute cloud spend to specific products, features, or customer workloads. Without cost transparency, teams cannot determine customer margins, set pricing models accurately, or identify unprofitable video workloads.

## Objective
The objective of this project is to build an automated, usage-based financial cost allocation system that links raw cloud billing data with operational video telemetry logs to calculate Unit Economics KPIs (such as Cost per Video, Cost per Processing Hour, Allocation Coverage %, and Gross Margin), recover from telemetry data quality flaws automatically, benchmark allocation strategies empirically, pass automated Pytest testing suites, and present role-based insights via an interactive web dashboard.

---

## 1. Key Features & Completed Modules

1. **Problem & Stakeholder Definition**: Documented business context, target audience, and core assumptions (`docs/problem.md`, `docs/assumptions.md`).
2. **System Architecture & Workflow**: Modular pipeline with Mermaid flowcharts (`docs/architecture.md`).
3. **Data Schema & API Specifications**: Documented CSV database schemas and HTTP API endpoints (`docs/data_schema.md`, `docs/api_and_database_schema.md`).
4. **Technical Approach Benchmarking**: Evaluated Strategy A (Tag-based static) vs. Strategy B (Telemetry-weighted dynamic allocation) (`src/experiment.py`, `docs/technical_approaches.md`).
5. **Synthetic Data Generator**: Created `src/generate_data.py` producing ~10,000 total rows across 4 datasets with realistic workload scaling and intentional data flaws (~1-3%).
6. **Data Quality Validation Engine**: Built `src/validate_data.py` generating `reports/validation_report.csv`.
7. **Automated Data Flaw Recovery Engine**: Built `src/recover_data.py` achieving 100.0% recovery across deduplication, chrono-reordering, delayed re-attribution, and tag fallbacks (`reports/recovery_report.csv`).
8. **Usage-Based Cost Allocation Engine**: Developed `src/cost_allocation.py` to attribute spend and compute 11 Unit Economics KPIs.
9. **Interactive Role-Based Web Dashboard**: Created `src/dashboard.py` generating single-page [`dashboard.html`](file:///d:/RAALE%20PROJECT/dashboard.html) featuring Executive, Product Manager, FinOps, and Data Health views with live data freshness indicators.
10. **Automated Pytest Test Suite**: Built `tests/test_pipeline.py` verifying schema integrity, anomaly detection, recovery idempotence, cost reconciliation, and benchmark strategy performance (`docs/testing_and_error_boundaries.md`).

---

## 2. HTTP Web Server API Endpoints

The dashboard includes a lightweight Python HTTP server (`src/dashboard.py`) running on `localhost:8000`.

| HTTP Method | Route / Endpoint | Description | Content Type | Response Payload / Behavior |
|---|---|---|---|---|
| `GET` | `/` | Root web route | `text/html` | Serves interactive `dashboard.html` single-page UI. |
| `GET` | `/dashboard` | Dashboard web route | `text/html` | Alias for `/dashboard.html`. |
| `GET` | `/dashboard.html` | Static dashboard asset | `text/html` | Serves `dashboard.html` with CSS & JavaScript. |

---

## 3. CSV Database Schemas

The data layer consists of standard relational CSV files stored in `data/` and `data/cleaned/`:

- **`billing.csv`** (2,525 rows | 9 cols): `billing_id`, `date`, `cloud_service`, `product_id`, `customer_id`, `compute_cost`, `storage_cost`, `transfer_cost`, `total_cost`.
- **`usage_telemetry.csv`** (3,030 rows | 9 cols): `event_id`, `timestamp`, `product_id`, `customer_id`, `video_id`, `processing_minutes`, `storage_gb`, `transfer_gb`, `event_status`.
- **`allocation_tags.csv`** (2,000 rows | 7 cols): `tag_id`, `product_id`, `customer_id`, `team`, `environment`, `service`, `tag_status`.
- **`product_activity.csv`** (2,400 rows | 9 cols): `activity_id`, `date`, `product_id`, `customer_id`, `videos_processed`, `processing_hours`, `storage_gb`, `transfer_gb`, `revenue`.

For complete database field descriptions, key types, and example values, see [`docs/api_and_database_schema.md`](file:///d:/RAALE%20PROJECT/docs/api_and_database_schema.md).

---

## 4. System Error Boundaries & Fault Isolation

The system enforces 5 explicit error boundaries:
1. **File System Boundary**: Automatic directory initialization prevents `FileNotFoundError` exceptions.
2. **Numerical Value Boundary**: Absolute value transformations eliminate negative cost and processing duration anomalies.
3. **Missing Tag Fallback Boundary**: Null tag entries fall back to `"UNALLOCATED_RECOVERY"` to prevent null-pointer crashes.
4. **Timestamp Monotonicity Boundary**: Chronological log re-ordering resolves non-monotonic event logs.
5. **Recovery Idempotence Boundary**: Ensures repeated recovery execution produces zero data mutation or side effects.

For detailed unit testing specs and fault isolation mechanisms, see [`docs/testing_and_error_boundaries.md`](file:///d:/RAALE%20PROJECT/docs/testing_and_error_boundaries.md).

---

## 5. Technology Stack
- **Language**: Python 3.x
- **Data Manipulation**: Pandas
- **Automated Testing**: Pytest
- **Dashboard Interface**: HTML5, CSS3, JavaScript (Single-Page Application served via Python `http.server`)
- **Storage Format**: Standard CSV files

---

## 6. Folder Structure
```
d:/RAALE PROJECT/
│
├── data/
│   ├── billing.csv                  (2,525 rows | 9 cols)
│   ├── usage_telemetry.csv          (3,030 rows | 9 cols)
│   ├── allocation_tags.csv          (2,000 rows | 7 cols)
│   ├── product_activity.csv         (2,400 rows | 9 cols)
│   └── cleaned/                     (9,900 recovered clean rows)
│
├── src/
│   ├── __init__.py                  (Package initialization)
│   ├── generate_data.py             (Synthetic data generator)
│   ├── validate_data.py             (Data quality flaw detector)
│   ├── recover_data.py              (Automated data flaw recovery engine)
│   ├── cost_allocation.py           (Usage-based allocation & Unit Economics engine)
│   ├── experiment.py                (Allocation strategy benchmarking engine)
│   └── dashboard.py                 (Web dashboard generator & server)
│
├── tests/
│   ├── __init__.py                  (Test package initialization)
│   └── test_pipeline.py             (Pytest suite testing schema, idempotence, allocation math)
│
├── reports/
│   ├── validation_report.csv
│   ├── recovery_report.csv
│   └── experiment_results.csv
│
├── docs/
│   ├── problem.md
│   ├── assumptions.md
│   ├── architecture.md
│   ├── data_schema.md
│   ├── technical_approaches.md
│   ├── api_and_database_schema.md   (API endpoints & database dictionary)
│   └── testing_and_error_boundaries.md (Pytest specs & system error boundaries)
│
├── dashboard.html                   (Interactive Web Dashboard UI)
├── REVIEW_1_REPORT.md               (Initial 50% Milestone Report)
├── REVIEW_2_REPORT.md               (Review 2 Progress Report)
├── REVIEW_3_REPORT.md               (Review 3 Evaluator Progress Report)
├── README.md                        (Project documentation)
├── requirements.txt                 (Dependencies: pandas, pytest)
└── .gitignore
```

---

## 7. How to Install & Run

```bash
cd "d:/RAALE PROJECT"
pip install -r requirements.txt

# Run Pytest Automated Test Suite
python -m pytest tests/test_pipeline.py

# Run Full Data Pipeline
python src/generate_data.py
python src/validate_data.py
python src/recover_data.py
python src/cost_allocation.py
python src/experiment.py
python src/dashboard.py
```

Open [`dashboard.html`](file:///d:/RAALE%20PROJECT/dashboard.html) directly in any web browser to explore the interactive dashboard!
