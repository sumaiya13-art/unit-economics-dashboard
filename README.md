# Unit Economics Dashboard for Media Workloads (50% Milestone)

## Project Title
**Unit Economics Dashboard - 50% Milestone Prototype**

## Problem Statement
A media platform processes unpredictable video workloads (encoding, streaming, storage, distribution). Engineering and product teams receive aggregate monthly cloud provider bills (e.g. AWS invoices) but cannot attribute cloud spend to specific products, features, or customer workloads. Without cost transparency, teams cannot determine customer margins, set pricing models accurately, or identify unprofitable video workloads.

## Objective
The objective of this project is to build an automated, usage-based financial cost allocation system that links raw cloud billing data with operational video telemetry logs to calculate Unit Economics KPIs (such as Cost per Video, Cost per Processing Hour, Allocation Coverage %, and Gross Margin), recover from telemetry data quality flaws automatically, and present clear unit economics outputs.

This codebase represents **Phase 1 (50% Total Milestone)** of the project vision.

---

## 50% Milestone Features Completed
1. **Problem & Stakeholder Definition**: Documented business context, target audience, and core assumptions (`docs/problem.md`, `docs/assumptions.md`).
2. **System Architecture & Workflow**: Modular pipeline with Mermaid flowcharts (`docs/architecture.md`).
3. **Data Schema Specification**: Documented schemas for all 4 synthetic datasets (`docs/data_schema.md`).
4. **Technical Approach Comparison**: Evaluated Tag-based vs. Usage-based cost allocation (`docs/technical_approaches.md`).
5. **Synthetic Data Generator**: Created `src/generate_data.py` producing ~10,000 total rows across 4 datasets with realistic workload scaling and intentional data flaws (~1-3%).
6. **Data Quality Validation Engine**: Built `src/validate_data.py` generating `reports/validation_report.csv`.
7. **Automated Data Flaw Recovery Engine**: Built `src/recover_data.py` achieving 100% recovery across deduplication, chrono-reordering, delayed re-attribution, and tag fallbacks (`reports/recovery_report.csv`).
8. **Usage-Based Cost Allocation Engine**: Developed `src/cost_allocation.py` to attribute spend and compute 11 Unit Economics KPIs.
9. **Complete Evaluation Report**: Created [`REVIEW_1_REPORT.md`](file:///d:/RAALE%20PROJECT/REVIEW_1_REPORT.md) formatted specifically for evaluator review.

---

## Technology Stack
- **Language**: Python 3.x
- **Data Manipulation**: Pandas
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
│   ├── generate_data.py             (Synthetic data generator)
│   ├── validate_data.py             (Data quality flaw detector)
│   ├── recover_data.py              (Automated data flaw recovery engine)
│   └── cost_allocation.py           (Usage-based allocation & Unit Economics engine)
│
├── reports/
│   ├── validation_report.csv        (Validation flaw summary)
│   └── recovery_report.csv          (100.0% recovery success report)
│
├── docs/
│   ├── problem.md
│   ├── assumptions.md
│   ├── architecture.md
│   ├── data_schema.md
│   └── technical_approaches.md
│
├── REVIEW_1_REPORT.md               (50% Milestone Evaluation Report)
├── README.md                        (Project documentation)
├── requirements.txt                 (Dependencies: pandas)
└── .gitignore
```

---

## How to Install & Setup

```bash
cd "d:/RAALE PROJECT"
pip install -r requirements.txt
```

---

## How to Run the Pipeline

Run the pipeline steps sequentially:

```bash
# 1. Generate Synthetic Datasets
python src/generate_data.py

# 2. Validate Data Quality Flaws
python src/validate_data.py

# 3. Run Automated Flaw Recovery Engine
python src/recover_data.py

# 4. Run Cost Allocation & Unit Economics Engine
python src/cost_allocation.py
```

---

## Current Limitations & Pending Work (Remaining 50%)
- **Interactive Web Dashboard UI**: Web interface with role-based navigation.
- **Empirical Experiments Engine**: Tag-Based Baseline vs. Usage-Based Target allocation comparison.
- **Synthetic Failure Resilience Demos**: Automated fault injection test suite.
- **Production Kubernetes & Kafka**: Streaming ingestion & cluster container manifests.
