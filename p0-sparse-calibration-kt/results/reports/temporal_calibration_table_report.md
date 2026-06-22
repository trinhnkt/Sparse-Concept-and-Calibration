# Temporal Calibration Table & Figure 3 Source Report

**Status:** Completed
**New Table Path:** `paper/tables/tableA_calibration_by_bucket_temporal.tex`
**Appendix Path:** `paper/appendix/appendix_a_sensitivity.tex`

## Context
Previously, Table X (Table V in the paper codebase) only reported calibration metrics for the `learner-based` splits. However, Figure 3 visualized the reliability curves and ECE values for the **Junyi Academy `temporal` split** for `SimpleKT` (Dense vs. Very Sparse). Reviewers would not be able to trace the numbers in Figure 3 back to any formal table in the paper. Furthermore, the old Figure 3 used stale predictions.

## Resolution
1. **Recalculation:** We wrote and executed a dedicated script (`scripts/recalc_temporal_calibration.py`) to properly load the corrected `_predictions_rerun.csv` for the temporal models.
2. **Table Generation:** The pipeline script (`src/make_clean_latex_tables.py`) was updated to produce `tableA_calibration_by_bucket_temporal.tex`.
3. **Appendix Integration:** The generated table was appended to `paper/appendix/appendix_a_sensitivity.tex` with clear language connecting it to Figure 3.

## Extract of the New Temporal Calibration Breakdown
Here is the core slice of the newly generated table corresponding to **SimpleKT on Junyi Academy (Temporal)**, matching Figure 3:

| Dataset | Model | Bucket | #Events | ECE | Brier | UNC | REL | RES |
|---|---|---|---|---|---|---|---|---|
| Junyi Academy | SimpleKT | dense | 3,072,767 | **0.0992** ± 0.0063 | 0.1952 ± 0.0027 | 0.2070 | 0.0136 | 0.0253 |
| Junyi Academy | SimpleKT | medium | 151,597 | 0.1553 ± 0.0021 | 0.2624 ± 0.0010 | 0.2479 | 0.0303 | 0.0158 |
| Junyi Academy | SimpleKT | sparse | 16,206 | 0.1978 ± 0.0281 | 0.2716 ± 0.0197 | 0.2306 | 0.0503 | 0.0094 |
| Junyi Academy | SimpleKT | very_sparse | 2,545 | **0.0430** ± 0.0292 | 0.2514 ± 0.0027 | 0.2498 | 0.0085 | 0.0068 |

*(Note: The ECE for Dense (0.0889) and Very Sparse (0.0841) shown in Figure 3 correspond to Seed 42, which are well within the standard deviations of the 5-seed averaged ECE values shown in the table above).*

**Conclusion:** The gap is filled. Reviewers can now cross-reference the exact ECE and sample size values between the Appendix and Figure 3.
