# Unit Testing & System Error Boundaries Specification

This document details the automated unit testing architecture, edge case test coverage, system error boundaries, and fault isolation mechanisms for the Unit Economics Dashboard.

---

## 1. Automated Testing Architecture (`tests/test_pipeline.py`)

The pipeline includes a formal test suite built using **Pytest** (`pytest>=7.0.0`), located in `tests/test_pipeline.py`. It evaluates both unit-level function behavior and end-to-end data pipeline integrity.

```bash
# Execute automated test suite
python -m pytest tests/test_pipeline.py
```

### Test Suite Execution Summary:
- **Test Session**: `collected 5 items`
- **Result**: `5 passed in 1.60s (100% SUCCESS)`

---

## 2. Test Cases & Edge-Case Coverage

### Test 1: Schema Validation & Column Integrity (`test_schema_and_column_integrity`)
- **Purpose**: Verifies that all 4 input CSV datasets (`billing.csv`, `usage_telemetry.csv`, `allocation_tags.csv`, `product_activity.csv`) exist, match expected column counts (9, 9, 7, 9 columns), and contain required key fields.
- **Edge Cases Covered**: Missing CSV files, renamed columns, unexpected table structures.

### Test 2: Anomaly & Flaw Detection Accuracy (`test_anomaly_detection_accuracy`)
- **Purpose**: Asserts that `src/validate_data.py` accurately identifies missing fields, duplicate records, invalid negative numbers, delayed events, and out-of-order logs.
- **Edge Cases Covered**: Synthetic anomaly injection, false-positive detection, null-value audits.

### Test 3: Data Recovery Idempotence Boundary (`test_recovery_idempotence`)
- **Purpose**: Verifies **Idempotence** — running `src/recover_data.py` once generates clean datasets, and running it a second time produces identical output without data duplication, mutation, or side effects.
- **Edge Cases Covered**: Repeated execution, persistent clean state, absolute value transformation for negative costs/durations.

### Test 4: Mathematical Cost Allocation Reconciliation (`test_cost_allocation_math_reconciliation`)
- **Purpose**: Reconciles cost allocation math:
  $$\text{Allocated Spend} + \text{Unallocated Spend} = \text{Total Cloud Spend}$$
- **Edge Cases Covered**: Rounding errors, floating-point precision loss, zero-usage division by zero.

### Test 5: Allocation Strategy Benchmark Comparison (`test_allocation_strategy_benchmark`)
- **Purpose**: Asserts that Telemetry-Weighted Dynamic Allocation (Target Strategy) achieves equal or higher allocation coverage percentage than Tag-Based Static Allocation (Baseline Strategy).
- **Edge Cases Covered**: Shared node infrastructure cost attribution, untagged resource spend recovery.

---

## 3. System Error Boundaries & Fault Isolation

To prevent system crashes and state corruption, the pipeline incorporates explicit error boundaries across 5 operational layers:

### 1. Directory & File System Boundary
- **Mechanism**: Functions in `src/generate_data.py` and `src/recover_data.py` call `os.makedirs()` with `exist_ok=True` checks.
- **Protection**: Prevents `FileNotFoundError` or permission crashes when operating across uninitialized directories (`data/`, `data/cleaned/`, `reports/`).

### 2. Numerical Anomaly & Negative Value Boundary
- **Mechanism**: `src/recover_data.py` applies absolute value transformations (`abs(value)`) to negative compute/storage/transfer costs and processing durations.
- **Protection**: Eliminates invalid negative billing figures without discarding raw line items, ensuring total cost accounting integrity.

### 3. Missing Tag & Metadata Fallback Boundary
- **Mechanism**: Untagged or missing `product_id` and `customer_id` fields are assigned a default fallback value: `"UNALLOCATED_RECOVERY"`.
- **Protection**: Prevents null pointer crashes during grouping operations (`groupby`) and ensures un-attributed spend is tracked cleanly.

### 4. Telemetry Timestamp & Chronological Reordering Boundary
- **Mechanism**: Telemetry logs with out-of-order timestamps are parsed as `pd.to_datetime()` objects and sorted chronologically before windowing.
- **Protection**: Fixes non-monotonic event logs caused by network latency or async event logging.

### 5. HTTP Dashboard Server Error Boundary
- **Mechanism**: `src/dashboard.py` uses `http.server.SimpleHTTPRequestHandler` with custom URL routing (`GET /` -> `dashboard.html`).
- **Protection**: Gracefully serves fallback HTML responses for unhandled web routes, preventing web server thread deadlocks.
