# REVIEW 1 REPORT: Unit Economics Dashboard for Media Workloads (50% Milestone)

---

## 1. PROJECT TITLE
**Unit Economics Dashboard for Media Workloads (50% Milestone Prototype)**

---

## 2. PROBLEM STATEMENT
A media platform processes unpredictable, highly variable video workloads including video encoding, streaming, storage, and content distribution. While the platform operates effectively, the organization faces a critical financial transparency challenge:

- Product and engineering teams receive aggregate monthly cloud provider bills (e.g. AWS/GCP invoices).
- Cloud spend cannot be attributed back to specific products (e.g., Live Streaming vs. On-Demand VOD), features, or customer workloads.
- As a result, product managers cannot calculate gross margins per customer, set data-driven subscription pricing, or identify unprofitable video processing workloads.

---

## 3. PROJECT OBJECTIVE
The goal of this project is to build an automated, usage-based financial cost allocation system that links raw cloud provider billing data with operational video telemetry logs. The system attributes cloud costs to accountable products and customers, calculates foundational Unit Economics KPIs (Cost per Video, Cost per Processing Hour, Allocation Coverage %, Gross Margin), audits data quality flaws, and performs automated flaw recovery without data corruption.

---

## 4. WHAT HAS BEEN COMPLETED SO FAR (50% Milestone)

The following core components have been fully built, executed, and verified:

- [x] **Problem Analysis**: Documented business context and financial transparency challenges ([`docs/problem.md`](file:///d:/RAALE%20PROJECT/docs/problem.md)).
- [x] **Stakeholder Identification**: Defined needs for Product Owners, Engineering Leads, and FinOps Teams ([`docs/problem.md`](file:///d:/RAALE%20PROJECT/docs/problem.md)).
- [x] **Project Assumptions**: Defined telemetry, cost drivers, and allocation boundaries ([`docs/assumptions.md`](file:///d:/RAALE%20PROJECT/docs/assumptions.md)).
- [x] **Basic Architecture**: Designed modular, file-based pipeline with Mermaid workflow diagrams ([`docs/architecture.md`](file:///d:/RAALE%20PROJECT/docs/architecture.md)).
- [x] **Data Schema Specification**: Formatted exact schema specs across all 4 datasets ([`docs/data_schema.md`](file:///d:/RAALE%20PROJECT/docs/data_schema.md)).
- [x] **Technical Approach Comparison**: Evaluated Tag-based vs. Usage-based cost allocation and justified selecting Usage-based allocation ([`docs/technical_approaches.md`](file:///d:/RAALE%20PROJECT/docs/technical_approaches.md)).
- [x] **Synthetic Datasets Generator**: Created 4 datasets (~10,000 total rows) with realistic workload scaling and intentional data flaws ([`src/generate_data.py`](file:///d:/RAALE%20PROJECT/src/generate_data.py)).
- [x] **Data Validation Engine**: Built automated flaw detector generating summary report ([`src/validate_data.py`](file:///d:/RAALE%20PROJECT/src/validate_data.py)).
- [x] **Automated Data Flaw Recovery Engine**: Built automated state recovery engine achieving 100% flaw resolution ([`src/recover_data.py`](file:///d:/RAALE%20PROJECT/src/recover_data.py)).
- [x] **Usage-Based Cost Allocation Engine**: Implemented usage-based cost allocation logic on cleaned datasets ([`src/cost_allocation.py`](file:///d:/RAALE%20PROJECT/src/cost_allocation.py)).
- [x] **Product-Level Cost Attribution**: Calculated usage shares and cost allocations per product ([`src/cost_allocation.py`](file:///d:/RAALE%20PROJECT/src/cost_allocation.py)).
- [x] **Customer-Level Cost Attribution**: Calculated usage shares and cost allocations per customer ([`src/cost_allocation.py`](file:///d:/RAALE%20PROJECT/src/cost_allocation.py)).
- [x] **Unit Economics Calculations**: Calculated all 11 core KPIs including Cost per Video, Cost per Processing Hour, Revenue, and Gross Margin.
- [x] **Working Python Scripts**: Simple, well-commented Python scripts (~70–120 lines per file).
- [x] **README & Documentation**: Created GitHub-ready documentation and reproducibility steps.

---

## 5. KEY FEATURES / MODULES COMPLETED

### Module 1: Synthetic Data Generator (`src/generate_data.py`)
- **Purpose**: Generates realistic synthetic datasets simulating media platform operational telemetry, cloud billing, resource tagging, and product activity.
- **Input**: Target row parameters (2,000–5,000 rows per dataset).
- **Output**: 4 CSV files in `data/`.
- **Status**: **COMPLETED**. Fully functional.

### Module 2: Data Quality Validation Engine (`src/validate_data.py`)
- **Purpose**: Audits raw input datasets to detect data quality flaws.
- **Input**: 4 raw CSV datasets in `data/`.
- **Output**: Console report and `reports/validation_report.csv`.
- **Status**: **COMPLETED**. Accurately detects missing, duplicate, invalid, delayed, and out-of-order records.

### Module 3: Automated Data Recovery Engine (`src/recover_data.py`)
- **Purpose**: Performs automated flaw cleaning and state recovery without data corruption.
- **What it does**: Deduplicates records, chronologically re-orders telemetry, repairs negative values, re-attributes delayed events, and maps fallback tags.
- **Input**: Raw CSV datasets in `data/`.
- **Output**: Cleaned datasets in `data/cleaned/` and `reports/recovery_report.csv`.
- **Status**: **COMPLETED**. Achieves 100.0% recovery success rate across 376 raw flaws.

### Module 4: Usage-Based Cost Allocation & Unit Economics Engine (`src/cost_allocation.py`)
- **Purpose**: Attributes cloud spend to products/customers and computes Unit Economics KPIs.
- **Input**: Cleaned datasets from `data/cleaned/`.
- **Output**: Formatted console report with 11 Unit Economics KPIs.
- **Status**: **COMPLETED**. Verified on clean data.

---

## 6. WHAT IS CURRENTLY WORKING

The entire 50% milestone pipeline can be executed end-to-end via command line:

```bash
# 1. Generate Synthetic Datasets
python src/generate_data.py

# 2. Run Data Quality Validation Engine
python src/validate_data.py

# 3. Run Automated Data Flaw Recovery Engine
python src/recover_data.py

# 4. Run Cost Allocation & Unit Economics Engine
python src/cost_allocation.py
```

---

## 7. DATASET DETAILS

| Dataset File | Purpose | Row Count | Column Count | Key Columns |
|---|---|---|---|---|
| [`data/billing.csv`](file:///d:/RAALE%20PROJECT/data/billing.csv) | Raw Cloud Billing Logs | **2,525 rows** | **9 cols** | `billing_id`, `date`, `cloud_service`, `product_id`, `customer_id`, `compute_cost`, `storage_cost`, `transfer_cost`, `total_cost` |
| [`data/usage_telemetry.csv`](file:///d:/RAALE%20PROJECT/data/usage_telemetry.csv) | Telemetry Event Logs | **3,030 rows** | **9 cols** | `event_id`, `timestamp`, `product_id`, `customer_id`, `video_id`, `processing_minutes`, `storage_gb`, `transfer_gb`, `event_status` |
| [`data/allocation_tags.csv`](file:///d:/RAALE%20PROJECT/data/allocation_tags.csv) | Tag Metadata & Team Mapping | **2,000 rows** | **7 cols** | `tag_id`, `product_id`, `customer_id`, `team`, `environment`, `service`, `tag_status` |
| [`data/product_activity.csv`](file:///d:/RAALE%20PROJECT/data/product_activity.csv) | Business Activity & Revenue | **2,400 rows** | **9 cols** | `activity_id`, `date`, `product_id`, `customer_id`, `videos_processed`, `processing_hours`, `storage_gb`, `transfer_gb`, `revenue` |
| **`data/cleaned/` Datasets** | Cleaned Recovered Datasets | **9,900 rows** | **Cleaned** | Reconstructed & normalized clean data |

---

## 8. CURRENT RESULTS (Empirical Pipeline Outputs)

### A. Unit Economics KPIs (`src/cost_allocation.py`)

| Metric # | Unit Economics Metric | Calculated Actual Result |
|---|---|---|
| 1 | **Total Cloud Cost** | **$509,561.11** |
| 2 | **Allocated Cloud Cost** | **$500,537.12** |
| 3 | **Unallocated Cloud Cost** | **$9,023.99** |
| 4 | **Allocation Coverage %** | **98.23%** |
| 5 | **Cost per Video** | **$2.62** |
| 6 | **Cost per Processing Hour** | **$10.49** |
| 7 | **Cost per Product (Average)** | **$125,134.28** |
| 8 | **Cost per Customer (Average)** | **$83,422.85** |
| 9 | **Total Revenue** | **$3,141,431.21** |
| 10 | **Cost-to-Revenue %** | **15.93%** |
| 11 | **Gross Margin** | **$2,640,894.09** |

---

## 9. PENDING WORK (Remaining 50% Roadmap)

- [ ] **Interactive Web Dashboard UI**: Responsive role-based web interface (Executive, Product Manager, FinOps views).
- [ ] **Empirical Baseline vs Target Allocation Experiments**: Quantitative comparison testing Tag-Based vs. Usage-Based allocation.
- [ ] **Synthetic Failure Resilience Demonstrations**: Automated edge-case fault injection suite.
- [ ] **Kubernetes Container Orchestration**: Dockerfiles and Helm charts for cluster deployment.
- [ ] **Real-Time Streaming Ingestion**: Real-time event streaming pipeline via Apache Kafka & Spark.

---

## 10. REPRODUCIBILITY GUIDE FOR EVALUATORS

```bash
python src/generate_data.py
python src/validate_data.py
python src/recover_data.py
python src/cost_allocation.py
```
