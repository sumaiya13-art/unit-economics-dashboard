# Unit Economics Dashboard for Media Workloads

## Project Title
**Unit Economics Cost Attribution Dashboard for Media Workloads**

## Problem Statement
A media platform processes unpredictable video workloads (encoding, streaming, storage, distribution). Engineering and product teams receive aggregate monthly cloud provider bills (e.g. AWS invoices) but cannot attribute cloud spend to specific products, features, or customer workloads. Without cost transparency, teams cannot determine customer margins, set pricing models accurately, or identify unprofitable video workloads.

## Objective
The objective of this project is to build an automated, usage-based financial cost allocation system that links raw cloud billing data with operational video telemetry logs to calculate Unit Economics KPIs (such as Cost per Video, Cost per Processing Hour, Allocation Coverage %, and Gross Margin), recover from telemetry data quality flaws automatically, benchmark allocation strategies empirically, and present role-based insights via an interactive web dashboard.

---

## Key Features & Completed Modules
1. **Problem & Stakeholder Definition**: Documented business context, target audience, and core assumptions (`docs/problem.md`, `docs/assumptions.md`).
2. **System Architecture & Workflow**: Modular pipeline with Mermaid flowcharts (`docs/architecture.md`).
3. **Data Schema Specification**: Documented schemas for all 4 synthetic datasets (`docs/data_schema.md`).
4. **Technical Approach Benchmarking**: Evaluated Strategy A (Tag-based) vs. Strategy B (Telemetry-weighted dynamic allocation) (`src/experiment.py`, `docs/technical_approaches.md`).
5. **Synthetic Data Generator**: Created `src/generate_data.py` producing ~10,000 total rows across 4 datasets with realistic workload scaling and intentional data flaws (~1-3%).
6. **Data Quality Validation Engine**: Built `src/validate_data.py` generating `reports/validation_report.csv`.
7. **Automated Data Flaw Recovery Engine**: Built `src/recover_data.py` achieving 100.0% recovery across deduplication, chrono-reordering, delayed re-attribution, and tag fallbacks (`reports/recovery_report.csv`).
8. **Usage-Based Cost Allocation Engine**: Developed `src/cost_allocation.py` to attribute spend and compute 11 Unit Economics KPIs.
9. **Interactive Role-Based Web Dashboard**: Created `src/dashboard.py` generating single-page [`dashboard.html`](file:///d:/RAALE%20PROJECT/dashboard.html) featuring Executive, Product Manager, FinOps, and Data Health views with live data freshness indicators.
10. **Automated Pytest Test Suite**: Built `tests/test_pipeline.py` verifying schema integrity, anomaly detection, recovery idempotence, cost reconciliation, and benchmark strategy performance.

---

## Technology Stack
- **Language**: Python 3.x
- **Data Manipulation**: Pandas
- **Automated Testing**: Pytest
- **Dashboard Interface**: HTML5, CSS3, JavaScript (Single-Page Application served via Python `http.server`)
- **Storage Format**: Standard CSV files
- **Design Philosophy**: Minimal complexity, simple readable functions, no unnecessary classes/decorators/async, line-by-line explainability for viva examination.

---

## Folder Structure
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
│   └── technical_approaches.md
│
├── dashboard.html                   (Interactive Web Dashboard UI)
├── REVIEW_1_REPORT.md               (Initial 50% Milestone Report)
├── REVIEW_2_REPORT.md               (Review 2 Evaluator Improvements Report)
├── README.md                        (Project documentation)
├── requirements.txt                 (Dependencies: pandas, pytest)
└── .gitignore
```

---

## How to Install & Setup

```bash
cd "d:/RAALE PROJECT"
pip install -r requirements.txt
```

---

## How to Run the Pipeline & Tests

### Step 1: Run Automated Pytest Test Suite
```bash
python -m pytest tests/test_pipeline.py
```
*Executes all 5 automated unit and integration tests (schema validation, anomaly detection, recovery idempotence, allocation reconciliation).*

### Step 2: Run End-to-End Pipeline
```bash
# 1. Generate Datasets
python src/generate_data.py

# 2. Validate Data Quality Flaws
python src/validate_data.py

# 3. Run Automated Flaw Recovery Engine
python src/recover_data.py

# 4. Run Cost Allocation & Unit Economics
python src/cost_allocation.py

# 5. Run Strategy Benchmarking Experiment
python src/experiment.py

# 6. Generate Interactive Web Dashboard
python src/dashboard.py
```

Open [`dashboard.html`](file:///d:/RAALE%20PROJECT/dashboard.html) directly in any web browser to explore the interactive dashboard!
