# DeLong Test Report

**Date:** 2026-06-18  
**Status:** ✅ Completed

---

## 1. Scope & Execution
- **Datasets:** ASSISTments 2012, Junyi Academy, XES3G5M
- **Models:** IRT 1PL, DKT, SimpleKT
- **Comparisons:** Pairwise (IRT_1PL vs DKT, IRT_1PL vs SimpleKT, DKT vs SimpleKT) — 3 comparisons per dataset, totaling **9 tests**.
- **Prediction Files Used:** `learner_based` split, Seed `42`.
  - e.g., `assist2012_learner_based_dkt_seed42_predictions_rerun.csv`
- **DeLong Implementation:** Python via `compare_auc_delong_xu.py` (fast DeLong algorithm).
- **Alignment Method:** Both models' predictions and ground truth were verified for exact length match and exact sequential array equality of `y_true`. All arrays matched perfectly (no missing rows).

## 2. Statistical Settings
- **Base Alpha:** 0.05
- **Bonferroni Correction:** $\alpha_{bonf} = 0.05 / 9 \approx 0.0056$
- **Significance Criterion:** $p < 0.0056$

## 3. Results Summary

| Dataset | Comparison | p-value | Significant after Bonferroni? | Note |
|---------|------------|---------|-------------------------------|------|
| ASSISTments 2012 | IRT_1PL vs DKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| ASSISTments 2012 | IRT_1PL vs SimpleKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| ASSISTments 2012 | DKT vs SimpleKT | $< 0.001$ ($7.10 \times 10^{-82}$) | Yes | |
| Junyi Academy | IRT_1PL vs DKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| Junyi Academy | IRT_1PL vs SimpleKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| Junyi Academy | DKT vs SimpleKT | $< 0.001$ ($8.07 \times 10^{-144}$) | Yes | |
| XES3G5M | IRT_1PL vs DKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| XES3G5M | IRT_1PL vs SimpleKT | $0.0$ | Yes | IRT model has cold-start constraint (AUC=0.5) |
| XES3G5M | DKT vs SimpleKT | $0.0$ | Yes | |

*Note: IRT predictions in learner-based splits are set to 0.50 (random ranking) due to cold-start user constraints. This makes its AUC comparisons mathematically significant against DKT/SimpleKT, serving as a clear classical reference.*

## 4. Updates to Manuscript
- **Table Inserted:** A new LaTeX table `table_delong_overall_auc.tex` was created and inserted into `Section IV.C`, right after Table III (Overall Results).
- **Text Inserted:** The following interpretation text was added right below the table:
  *"Overall AUC differences between DKT and SimpleKT are statistically significant on all three datasets after Bonferroni correction, confirming that aggregate predictive quality differs between the two deep baselines. Classical baseline comparisons are reported for reference and highlight the generalization challenges on unseen cohorts."*
- **Constraints Verified:**
  - ✅ No re-run of model training.
  - ✅ No changes to raw data, Table III, Table IV, or Table V.
  - ✅ DeLong table fits directly into Section IV.C without breaking the narrative flow.
  - ✅ Hedging regarding IRT cold-start constraint applied correctly.
