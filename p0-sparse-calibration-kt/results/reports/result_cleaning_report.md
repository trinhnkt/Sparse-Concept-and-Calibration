# 📊 RESULT CLEANING REPORT

## 1. Overview and Objectives
To ensure absolute research reproducibility and data integrity, we conducted a rigorous audit and cleaning of the experimental results generated across the entire Knowledge Tracing (KT) evaluation pipeline. 

The primary objectives were:
1. **Remove Debug and Test Noise**: Eliminate all auxiliary test runs, debug scripts, and temporary VRAM test runs (filenames containing `test`, `gpu`, or `gputest`).
2. **Isolate Official Abstractions**: Keep only the official datasets (`assist2012`, `junyi`, `xes3g5m`) and official models (`bkt`, `dkt`, `simplekt`).
3. **Calculate Consistent Metrics**: Re-compute all evaluation metrics (AUC, ACC, NLL, RMSE) directly from the raw seed-level prediction files using a standardized and numerically stable evaluator.
4. **Aggregate Multi-Seed Statistics**: Calculate the mean and standard deviation across seeds for all metrics, using a robust standard deviation fallback (`std = 0.0`) when only a single seed is present (e.g., Junyi and xes3g5m official runs).

---

## 2. Dataset and Model Selection Filter
The cleaning process scanned the prediction directory `results/predictions/` and processed the matching files.

### A. Included Datasets & Models
| Dataset | Splitting Mode | Models Evaluated | Seeds |
| :--- | :--- | :--- | :--- |
| **ASSISTments 2012** (`assist2012`) | Learner-based, Temporal | BKT, DKT, SimpleKT | 42, 123, 2024, 2025, 2026 |
| **Junyi Academy** (`junyi`) | Learner-based, Temporal | BKT, DKT, SimpleKT | 42, 2024 (BKT) |
| **XES3G5M** (`xes3g5m`) | Learner-based, Temporal | BKT, DKT, SimpleKT | 42 |

### B. Excluded Files (Debug/Test/GPU Diagnostics)
Any prediction file containing the keywords `test`, `gpu`, or `gputest` was completely filtered out. Examples of excluded runs:
- `assist_bkt_test_learner_based_bkt_seed42.csv`
- `junyi_bkt_test_temporal_bkt_seed2024.csv`
- `xes_gpu_test_learner_based_simplekt_seed42.csv`

---

## 3. Standardized Metric Computation
To prevent standard calculation anomalies (e.g., division by zero or infinite log-losses), we implemented a highly stable evaluation protocol:
- **Numerical Stabilization**: All model predictions ($p$) are clipped to $[10^{-15}, 1 - 10^{-15}]$ before calculating the Negative Log-Likelihood (NLL). This resolved a major anomaly where BKT's deterministic predictions ($0.0$ or $1.0$) caused infinite NLL values.
- **Handling Single-Class Buckets**: In sparse concept buckets where the true label subset contains only a single class ($0$ or $1$), the Area Under the ROC Curve (AUC) is set to `NaN` instead of throwing evaluation errors.
- **Fixed-Width Calibration Binning**: Both Expected Calibration Error (ECE) and Brier Score Decomposition (Uncertainty, Reliability, Resolution) are computed using a consistent grid of $M = 15$ fixed-width bins.

---

## 4. Generated Artifacts
The cleaning process generated the following standardized files in `results/tables/`:

1. **`clean_overall_results.csv`**: Raw overall performance metrics for every single seed-level prediction.
2. **`clean_overall_results_summary.csv`**: Aggregated overall metrics containing the `mean` and `std` across seeds.
3. **`clean_metric_per_bucket.csv`**: Raw metric values grouped by concept frequency buckets (dense, medium, sparse, very_sparse).
4. **`clean_metric_per_bucket_summary.csv`**: Aggregated bucket metrics with seed-level mean and std.
5. **`clean_calibration_by_bucket.csv`**: Merged ECE and Brier Score Decomposition metrics grouped by bucket.
6. **`clean_cold_start_results.csv`**: Raw metrics evaluated on cold-start student-concept interaction subsets (strict, k5, k10, warm).
7. **`clean_cold_start_results_summary.csv`**: Aggregated cold-start metrics showing the mean and standard deviation.
