# DeLong Test Report

**Date:** 2026-06-13  
**Status:** ✅ Completed

---

## 1. Scope & Execution
- **Datasets:** ASSISTments 2012, Junyi Academy, XES3G5M
- **Models:** BKT, DKT, SimpleKT
- **Comparisons:** Pairwise (BKT vs DKT, BKT vs SimpleKT, DKT vs SimpleKT) — 3 comparisons per dataset, totaling **9 tests**.
- **Prediction Files Used:** `learner_based` split, Seed `42`.
  - e.g., `assist2012_learner_based_dkt_seed42.csv`
- **DeLong Implementation:** Python via `compare_auc_delong_xu.py` (fast DeLong algorithm).
- **Alignment Method:** Both models' predictions and ground truth were verified for exact length match and exact sequential array equality of `y_true`. All arrays matched perfectly (no missing rows).

## 2. Statistical Settings
- **Base Alpha:** 0.05
- **Bonferroni Correction:** $\alpha_{bonf} = 0.05 / 9 \approx 0.0056$
- **Significance Criterion:** $p < 0.0056$

## 3. Results Summary

| Dataset | Comparison | p-value | Significant after Bonferroni? |
|---------|------------|---------|-------------------------------|
| ASSISTments 2012 | BKT vs DKT | $< 0.001$ | Yes |
| ASSISTments 2012 | BKT vs SimpleKT | $< 0.001$ | Yes |
| ASSISTments 2012 | DKT vs SimpleKT | $< 0.001$ ($1.09 \times 10^{-84}$) | Yes |
| Junyi Academy | BKT vs DKT | $< 0.001$ | Yes |
| Junyi Academy | BKT vs SimpleKT | $< 0.001$ | Yes |
| Junyi Academy | DKT vs SimpleKT | $< 0.001$ ($8.96 \times 10^{-119}$) | Yes |
| XES3G5M | BKT vs DKT | $< 0.001$ | Yes |
| XES3G5M | BKT vs SimpleKT | $< 0.001$ | Yes |
| XES3G5M | DKT vs SimpleKT | $< 0.001$ | Yes |

*Note: BKT predictions have degenerate probability outputs, making its AUC comparisons mathematically significant against DKT/SimpleKT, but practically non-informative. This is explicitly noted in the paper.*

## 4. Updates to Manuscript
- **Table Inserted:** A new LaTeX table `table_delong_overall_auc.tex` was created and inserted into `Section IV.C`, right after Table III (Overall Results).
- **Text Inserted:** The following interpretation text was added right below the table:
  *"Overall AUC differences between DKT and SimpleKT are statistically significant on all three datasets after Bonferroni correction, confirming that aggregate predictive quality differs between the two deep baselines. BKT comparisons are reported for completeness but should be interpreted in light of its degenerate probability outputs."*
- **Constraints Verified:**
  - ✅ No re-run of model training.
  - ✅ No changes to raw data, Table III, Table IV, or Table V.
  - ✅ DeLong table fits directly into Section IV.C without breaking the narrative flow.
  - ✅ Hedging regarding BKT degenerate outputs applied correctly.

*(Note: The local environment does not have a working LaTeX compiler, so `P0_delong_tests_added.pdf` could not be built. However, all source files have been fully and safely updated.)*
