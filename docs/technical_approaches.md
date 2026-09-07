# Technical Approach Comparison

To attribute cloud spend accurately to products, features, and customer workloads, two main cost allocation strategies were evaluated: **Tag-Based Allocation** and **Usage-Based Allocation**.

---

## Technical Approach Matrix

| Evaluation Criteria | Approach 1: Tag-Based Allocation | Approach 2: Usage-Based Allocation (Selected) |
|---|---|---|
| **Description** | Relies on cloud infrastructure resource tags (e.g., AWS/GCP resource tags `Product: VOD`, `Customer: CUST_101`) set by engineers. | Uses fine-grained operational event telemetry (processing minutes, storage GB, bandwidth GB) to split costs proportionally. |
| **Accuracy** | **Moderate to Low**. Resources shared across multiple products or customers (e.g., shared databases or encoding clusters) cannot be tagged accurately for a single entity. | **High**. Dynamically divides shared resource costs based on actual consumption ratios per workload. |
| **Simplicity** | **High conceptually**, but requires 100% disciplined tagging infrastructure across all cloud resources. | **High implementation simplicity**. Requires simple proportional math: `Product Cost = Total Cost * (Product Usage / Total Usage)`. |
| **Explainability** | **Easy to understand**, but hard to explain why untagged shared resources cause large unallocated cost spikes. | **Very High**. Fully transparent and traceable back to raw telemetry logs (e.g., customer X used 40% of encoding time, so they bear 40% of compute cost). |
| **Data Requirements** | Requires strict cloud tag metadata attached to every cloud billing line item. | Requires cloud billing export data and event-level usage telemetry. |
| **Maintenance** | **High operational overhead**. Requires continuous enforcement, linting, and manual tag updates across engineering teams. | **Low maintenance**. Adapts automatically as new video workloads, products, or customers are added. |
| **Missing Data Handling** | Untagged resources default to 100% "Unallocated Cost", lowering allocation coverage. | Telemetry gaps can be audited against aggregate billing totals, ensuring total cost reconciliation. |

---

## Selected Approach & Justification

**Selected Approach: Approach 2 — Usage-Based Allocation**

### Rationale:
1. **Handles Shared Workloads**: Media platform workloads heavily rely on shared infrastructure (e.g., shared encoding nodes and distribution networks). Tag-based allocation fails to split shared infrastructure spend cleanly.
2. **Transparent & Traceable**: Usage-based allocation uses simple mathematical proportions, making cost allocation completely transparent and easy to explain line-by-line during technical reviews and viva examinations.
3. **High Allocation Coverage**: Allows attributing shared billing totals across active workloads based on usage telemetry ratios, drastically reducing unallocated cost percentages.
