# System Architecture (50% Milestone)

The Unit Economics Dashboard uses a modular, file-based Python data pipeline incorporating data flaw detection, automated state recovery, usage-based cost allocation, and unit economics calculations.

## Pipeline Architecture Diagram

```mermaid
graph TD
    A[Billing Data billing.csv] --> E[Data Validation Engine validate_data.py]
    B[Usage Telemetry usage_telemetry.csv] --> E
    C[Allocation Tags allocation_tags.csv] --> E
    D[Product Activity product_activity.csv] --> E

    E --> F[Validation Report validation_report.csv]

    A --> G[Data Recovery Engine recover_data.py]
    B --> G
    C --> G
    D --> G

    G --> H[Clean Datasets data/cleaned/]
    G --> I[Recovery Report recovery_report.csv]

    H --> J[Cost Allocation Engine cost_allocation.py]

    J --> K[Unit Economics KPIs & Summary Report]
    K -.-> L[Future Dashboard UI & Recovery Systems (Remaining 50%)]
```

## System Modules (50% Milestone)

1. **Synthetic Data Generator (`src/generate_data.py`)**:
   - Generates ~10,000 total rows across 4 datasets simulating media platform workloads with intentional data quality flaws (~1–3%).

2. **Data Validation Engine (`src/validate_data.py`)**:
   - Audits raw datasets for missing values, duplicates, invalid negative values, delayed event timestamps, and out-of-order logs.

3. **Automated Data Recovery Engine (`src/recover_data.py`)**:
   - Performs automated flaw cleaning: deduplication, chronological re-sorting, negative value repair, delayed event re-alignment, and tag fallback mapping. Generates clean datasets in `data/cleaned/`.

4. **Cost Allocation & Unit Economics Engine (`src/cost_allocation.py`)**:
   - Computes usage shares from clean telemetry, attributes cloud costs, and calculates 11 core Unit Economics KPIs.
