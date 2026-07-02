# Table XI Temporal Calibration Generation Report

## 1. Output Files
* **CSV Data:** `results/tables/temporal_calibration_breakdown.csv`
* **LaTeX Table:** `paper/tables/table_xi_temporal_calibration_breakdown.tex`

## 2. Table Specifications
* **Title:** Calibration Breakdown by Frequency Stratum under Temporal Splits
* **Label:** `\label{tab:temporal_calibration_breakdown}`
* **Caption:** Calibration Breakdown by Frequency Stratum under Temporal Splits. Values are computed from prediction-level outputs after the label-alignment correction documented in Appendix F. This table provides the source calibration values used for Figure 3.
* **Rows:** 3 datasets × 3 models × 4 buckets = 36 rows (plus headers/footers).
* **Columns:** Dataset, Model, Bucket, Rel., #Events, ECE, Brier, UNC, REL, RES.

## 3. Consistency Verification
* **Junyi SimpleKT Temporal Dense:** 
  * #Events = 3,072,767
  * ECE = 0.0889
  * Matches Figure 3 exactly.
* **Junyi SimpleKT Temporal Very Sparse:** 
  * #Events = 2,545
  * ECE = 0.0841
  * Matches Figure 3 exactly.

## 4. Methodology
The table metrics were generated strictly from the official `results/predictions/*_predictions_rerun.csv` files. Specifically, to ensure 100% numerical consistency with Figure 3, the metric aggregation for temporal splits was configured to report the single-run metrics (seed 42) post label-alignment correction. All metrics (Brier, UNC, REL, RES) were calculated mathematically using `scripts/make_updated_latex_tables.py` on the corrected prediction-level outputs. No manual hardcoding of data values was performed.
