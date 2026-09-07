# Problem Understanding & Project Context

## Problem Statement
A media platform processes highly unpredictable video workloads including video encoding, streaming, storage, and distribution. While the platform operates effectively, the organization faces a critical financial visibility challenge:

- Engineering and product teams receive aggregate monthly cloud bills (e.g., AWS/GCP invoice totals).
- Cloud spend cannot be mapped back to specific products (e.g., Live Streaming vs. On-Demand VOD), features, or customer workloads.
- As a result, product managers cannot calculate margins per customer or determine whether pricing models cover true cloud infrastructure costs.

## Objective
The primary goal of the Unit Economics Dashboard project is to build an automated financial allocation system that attributes cloud spend to specific products, features, and customer workloads.

This repository implements **Phase 1 (First 35% Foundation Prototype)**, focusing on building a transparent, verifiable data pipeline that links billing data with usage telemetry to perform usage-based cost allocation and calculate fundamental unit economics KPIs.

## Key Stakeholders

1. **Product Owners & Business Managers**
   - Need clear cost per product, cost per customer, and gross margins to make pricing and feature strategy decisions.

2. **Engineering & Infrastructure Leads**
   - Need visibility into processing, storage, and bandwidth consumption per service to optimize resource usage.

3. **Finance & FinOps Teams**
   - Need transparent, verifiable cost allocation mechanisms to reconcile monthly cloud vendor invoices with internal business metrics.

4. **Executive Leadership**
   - Requires high-level gross margin and cost-to-revenue tracking across customer segments.
