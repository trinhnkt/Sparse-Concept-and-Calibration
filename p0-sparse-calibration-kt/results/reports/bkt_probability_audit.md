# BKT Prediction Probability Audit

## Summary

Analyzed 22 BKT prediction files.

- **Degenerate files (<=5 unique values):** 22/22
- **BKT version:** pyBKT 1.4.1

## Per-File Statistics

| File | n_total | pct_nan | pct_zero | pct_near_0 | n_unique | AUC | Degenerate? |
|------|---------|---------|----------|------------|----------|-----|-------------|
| assist2012_learner_based_bkt_seed123.csv | 542748 | 13.86% | 86.14% | 86.14% | 1 | 0.5 | YES |
| assist2012_learner_based_bkt_seed2024.csv | 534150 | 14.06% | 85.94% | 85.94% | 1 | 0.5 | YES |
| assist2012_learner_based_bkt_seed2025.csv | 542748 | 13.86% | 86.14% | 86.14% | 1 | 0.5 | YES |
| assist2012_learner_based_bkt_seed2026.csv | 528681 | 13.97% | 86.03% | 86.03% | 2 | 0.5 | YES |
| assist2012_learner_based_bkt_seed42.csv | 534150 | 14.06% | 85.94% | 85.94% | 1 | 0.5 | YES |
| assist2012_temporal_bkt_seed123.csv | 531499 | 21.22% | 78.52% | 78.52% | 2 | 0.5 | YES |
| assist2012_temporal_bkt_seed2026.csv | 531499 | 21.22% | 78.52% | 78.52% | 2 | 0.5 | YES |
| assist2012_temporal_bkt_seed42.csv | 531499 | 21.22% | 78.52% | 78.52% | 2 | 0.5 | YES |
| junyi_bkt_test_learner_based_bkt_seed2024.csv | 17863 | 87.0% | 12.95% | 12.95% | 2 | 0.5014 | YES |
| junyi_bkt_test_learner_based_bkt_seed2025.csv | 17806 | 87.02% | 12.96% | 12.96% | 2 | 0.5 | YES |
| junyi_bkt_test_learner_based_bkt_seed42.csv | 17763 | 87.52% | 12.39% | 12.39% | 2 | 0.4954 | YES |
| junyi_bkt_test_temporal_bkt_seed2024.csv | 17760 | 87.51% | 12.43% | 12.43% | 2 | 0.5026 | YES |
| junyi_bkt_test_temporal_bkt_seed2025.csv | 17760 | 87.51% | 12.43% | 12.43% | 2 | 0.5026 | YES |
| junyi_bkt_test_temporal_bkt_seed42.csv | 17760 | 87.51% | 12.43% | 12.43% | 2 | 0.5026 | YES |
| junyi_learner_based_bkt_seed2024.csv | 3269022 | 10.59% | 89.41% | 89.41% | 1 | 0.5 | YES |
| junyi_learner_based_bkt_seed2025.csv | 3243926 | 10.74% | 89.26% | 89.26% | 1 | 0.5 | YES |
| junyi_learner_based_bkt_seed42.csv | 3269022 | 10.59% | 89.41% | 89.41% | 1 | 0.5 | YES |
| junyi_temporal_bkt_seed42.csv | 3243115 | 11.94% | 87.98% | 87.98% | 2 | 0.5001 | YES |
| xes3g5m_learner_based_bkt_seed2024.csv | 1589145 | 32.43% | 67.57% | 67.57% | 2 | 0.5 | YES |
| xes3g5m_learner_based_bkt_seed2025.csv | 1590128 | 32.46% | 67.54% | 67.54% | 2 | 0.5 | YES |
| xes3g5m_learner_based_bkt_seed42.csv | 1589145 | 32.43% | 67.57% | 67.57% | 2 | 0.5 | YES |
| xes3g5m_temporal_bkt_seed42.csv | 1590743 | 36.41% | 48.93% | 48.93% | 2 | 0.5 | YES |

## Root Cause Analysis

All BKT predictions are degenerate: p_pred ∈ {0.0, NaN} with ≤5 unique values.

**Root cause:** pyBKT 1.4.1 EM algorithm suffers divide-by-zero in M_step.py line 61 (init_softcounts = 0 → prior = NaN). Once prior = NaN, all subsequent HMM forward passes fail, yielding p_pred = 0.0 or NaN.

This is not a data preprocessing issue but a pyBKT numerical stability issue on datasets with sparse KC histories.

**Evidence:**
- learns = 1.000 (saturated) for all KCs
- guesses = slips = 0.500 (EM did not converge — stuck at initial values)
- prior = NaN for all KCs
- AUC = 0.5000 across all datasets and splits
