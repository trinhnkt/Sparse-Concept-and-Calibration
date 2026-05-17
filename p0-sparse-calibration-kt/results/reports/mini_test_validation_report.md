# 📋 Mini-Test Baseline Experiment Validation Report

**Date & Time:** 2026-05-17 15:41:15
**Target Directory:** `c:\TRINH\P0\p0-sparse-calibration-kt\results\predictions`

## 🔍 1. Execution Summary
- **Total Prediction Files Found:** 87
- **Validated Test Files:** 42
- **Failed Validations (Critical Errors):** 0

## 📝 2. Column & Data Quality Verification
| Check Point | Status | Details |
| :--- | :---: | :--- |
| Columns presence | ✅ PASS | Verified columns `user_id`, `item_id`, `kc_id`, `timestamp`, `y_true`, `p_pred`, `dataset`, `split_mode`, `model`, `seed` |
| y_true Binary Check | ✅ PASS | Verified labels are strictly binary (0 or 1) |
| p_pred Range Check | ✅ PASS | Verified probability predictions are strictly in range [0, 1] |
| Missing p_pred Check | ✅ PASS | Verified no missing probability predictions for deep models. (BKT NaNs are normal and accounted for: Note: BKT naturally outputs NaN for cold-start/unseen concept IDs since BKT is skill-specific.) |
| Missing kc_id Check | ✅ PASS | Checked for NaN values in concept/skill IDs |
| overall_results.csv | ✅ PASS | `overall_results.csv` exists and is formatted |
| overall_results_summary.csv | ✅ PASS | `overall_results_summary.csv` exists and is formatted |

## 🚀 3. Run Matrix Status (Seeds: 42, 2024, 2025)

### ✅ Completed Runs
- [x] `assist2012 | bkt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | bkt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | bkt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | dkt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | dkt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | dkt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | simplekt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | simplekt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `assist2012 | simplekt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `junyi | bkt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `junyi | bkt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `junyi | bkt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | bkt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | bkt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | bkt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | dkt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | dkt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | dkt | Seed 2025` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | simplekt | Seed 42` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | simplekt | Seed 2024` (Both `learner_based` & `temporal` splits present)
- [x] `xes3g5m | simplekt | Seed 2025` (Both `learner_based` & `temporal` splits present)

### ❌ Failed or Missing Runs
*None. All expected test runs completed successfully!*
