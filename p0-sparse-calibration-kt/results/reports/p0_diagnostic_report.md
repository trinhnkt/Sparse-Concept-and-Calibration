# P0 Diagnostic Report

**Paper title:** Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing

**Report type:** protocol / diagnostic / resource report

**Generated at:** 2026-05-17 11:57:15

This report summarizes sparse-concept diagnostics, calibration diagnostics, cold-start concept analysis, and leakage auditing for Knowledge Tracing baselines. It does not report results for any new KT model, SSL module, GNN module, path recommendation method, or distillation method.


## 1. Dataset statistics

Source file: `results/tables/dataset_stats.csv`

| dataset | raw_interactions | processed_interactions | n_users | n_items | n_kcs | avg_seq_len | sparsity_kc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | 100000 | 88796 | 16988 | 18697 | 1309 | 5.2270 | 0.9960 |
| assist_gpu_test | 100000 | 37592 | 8113 | 18727 | 238 | 4.6336 | 0.9805 |
| assist_bkt_test | 100000 | 37592 | 8113 | 18727 | 238 | 4.6336 | 0.9805 |
| xes_gpu_test | 76164 | 76164 | 185 | 5236 | 713 | 411.6973 | 0.4226 |
| xes_bkt_test | 76164 | 76164 | 185 | 5236 | 713 | 411.6973 | 0.4226 |
| xes_dkt_test | 76164 | 76164 | 185 | 5236 | 713 | 411.6973 | 0.4226 |
| xes_simplekt_test | 76164 | 76164 | 185 | 5236 | 713 | 411.6973 | 0.4226 |
| assist2012 | 6123270 | 2657490 | 27806 | 52672 | 265 | 95.5725 | 0.6393 |
| xes3g5m | 7953709 | 7953709 | 18066 | 7653 | 866 | 440.2584 | 0.4916 |
| junyi | 16217311 | 16215567 | 71014 | 25784 | 1326 | 228.3432 | 0.8278 |


## 2. Split summary

Source file: `results/tables/split_report.csv`

| dataset | split_mode | fold | n_train | n_valid | n_test | status | violation_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| assist2012 | learner_based | 0 | 1865217 | 258123 | 534150 | PASS | 0.0000 |
| assist2012 | temporal | 0 | 1860242 | 265749 | 531499 | PASS | 0.0000 |
| assist2012 | cold_start_test_strict | 0 | 1865217 | 0 | 0 | PASS | 0.0000 |
| assist2012 | cold_start_test_k5 | 0 | 1865217 | 0 | 5 | PASS | 0.0000 |
| assist2012 | cold_start_test_k10 | 0 | 1865217 | 0 | 6 | PASS | 0.0000 |


## 3. Baseline overall results

Source file: `results/tables/overall_results_summary.csv`

| dataset | split_mode | model | auc_mean | auc_std | acc_mean | acc_std | nll_mean | nll_std | rmse_mean | rmse_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| assist2012 | learner_based | bkt | 0.5000 | 0.0000 | 0.2896 | 0.0005 | 25.6066 | 0.0162 | 0.8429 | 0.0003 |
| assist2012 | learner_based | dkt | 0.6989 |  | 0.7186 |  | 0.5803 |  | 0.4392 |  |
| assist2012 | temporal | bkt | 0.5000 | 0.0000 | 0.3125 | 0.0000 | 24.7458 | 0.0000 | 0.8291 | 0.0000 |
| assist2012 | temporal | dkt | 0.4992 |  | 0.6129 |  | 0.8100 |  | 0.5177 |  |
| assist_bkt_test | learner_based | bkt | 0.4981 | 0.0010 | 0.3040 | 0.0030 | 25.0209 | 0.0953 | 0.8336 | 0.0016 |
| assist_bkt_test | temporal | bkt | 0.4850 | 0.0000 | 0.3454 | 0.0000 | 22.2080 | 0.0000 | 0.8004 | 0.0000 |
| assist_gpu_test | learner_based | bkt | 0.4981 | 0.0010 | 0.3040 | 0.0030 | 25.0209 | 0.0953 | 0.8336 | 0.0016 |
| assist_gpu_test | learner_based | dkt | 0.5451 | 0.0046 | 0.6491 | 0.0032 | 0.9969 | 0.0270 | 0.5245 | 0.0038 |
| assist_gpu_test | learner_based | simplekt | 0.5545 | 0.0023 | 0.6339 | 0.0075 | 1.4421 | 0.0192 | 0.5551 | 0.0033 |
| assist_gpu_test | temporal | bkt | 0.4850 | 0.0000 | 0.3454 | 0.0000 | 22.2080 | 0.0000 | 0.8004 | 0.0000 |
| assist_gpu_test | temporal | dkt | 0.5015 | 0.0027 | 0.6404 | 0.0015 | 0.9284 | 0.0069 | 0.5303 | 0.0014 |
| assist_gpu_test | temporal | simplekt | 0.4948 | 0.0040 | 0.6233 | 0.0025 | 1.4291 | 0.0170 | 0.5641 | 0.0012 |
| junyi_bkt_test | learner_based | bkt | 0.4990 | 0.0031 | 0.3963 | 0.0109 | 21.6806 | 0.3084 | 0.7762 | 0.0059 |
| junyi_bkt_test | temporal | bkt | 0.5026 | 0.0000 | 0.3966 | 0.0000 | 21.7209 | 0.0000 | 0.7771 | 0.0000 |
| xes3g5m | learner_based | dkt | 0.9176 |  | 0.8657 |  | 0.3129 |  | 0.3121 |  |
| xes3g5m | learner_based | simplekt | 0.8889 |  | 0.8444 |  | 0.4922 |  | 0.3510 |  |
| xes3g5m | temporal | simplekt | 0.4997 |  | 0.6551 |  | 1.2517 |  | 0.5207 |  |
| xes_bkt_test | learner_based | bkt | 0.5013 | 0.0003 | 0.3229 | 0.0204 | 24.3932 | 0.7311 | 0.8230 | 0.0123 |
| xes_bkt_test | temporal | bkt | 0.4937 | 0.0000 | 0.3408 | 0.0000 | 22.1637 | 0.0000 | 0.8202 | 0.0000 |
| xes_dkt_test | learner_based | dkt | 0.8586 | 0.0097 | 0.8475 | 0.0168 | 0.3670 | 0.0251 | 0.3370 | 0.0149 |
| xes_dkt_test | temporal | dkt | 0.5001 | 0.0012 | 0.6615 | 0.0139 | 0.7095 | 0.0258 | 0.4809 | 0.0082 |
| xes_gpu_test | learner_based | bkt | 0.5013 | 0.0003 | 0.3229 | 0.0204 | 24.3932 | 0.7311 | 0.8230 | 0.0123 |
| xes_gpu_test | learner_based | dkt | 0.8586 | 0.0097 | 0.8475 | 0.0168 | 0.3670 | 0.0251 | 0.3370 | 0.0149 |
| xes_gpu_test | learner_based | simplekt | 0.8672 | 0.0059 | 0.8410 | 0.0145 | 0.3800 | 0.0234 | 0.3422 | 0.0131 |
| xes_gpu_test | temporal | bkt | 0.4937 | 0.0000 | 0.3408 | 0.0000 | 22.1637 | 0.0000 | 0.8202 | 0.0000 |

_Showing first 25 of 29 rows._


## 4. KC bucket distribution

Source file: `results/tables/bucket_distribution.csv`

| dataset | split | fold | bucket | n_kcs |
| --- | --- | --- | --- | --- |
| assist2012 | learner_based | 0 | dense | 147 |
| assist2012 | learner_based | 0 | medium | 68 |
| assist2012 | learner_based | 0 | sparse | 39 |
| assist2012 | learner_based | 0 | very_sparse | 11 |
| assist2012 | learner_based | 1 | dense | 148 |
| assist2012 | learner_based | 1 | medium | 67 |
| assist2012 | learner_based | 1 | sparse | 39 |
| assist2012 | learner_based | 1 | very_sparse | 11 |
| assist2012 | learner_based | 2 | dense | 145 |
| assist2012 | learner_based | 2 | medium | 70 |
| assist2012 | learner_based | 2 | sparse | 38 |
| assist2012 | learner_based | 2 | very_sparse | 12 |
| assist2012 | temporal | 0 | dense | 145 |
| assist2012 | temporal | 0 | medium | 35 |
| assist2012 | temporal | 0 | sparse | 35 |
| assist2012 | temporal | 0 | very_sparse | 50 |
| assist_bkt_test | learner_based | 0 | dense | 12 |
| assist_bkt_test | learner_based | 0 | medium | 58 |
| assist_bkt_test | learner_based | 0 | sparse | 55 |
| assist_bkt_test | learner_based | 0 | very_sparse | 113 |
| assist_bkt_test | learner_based | 1 | dense | 11 |
| assist_bkt_test | learner_based | 1 | medium | 59 |
| assist_bkt_test | learner_based | 1 | sparse | 55 |
| assist_bkt_test | learner_based | 1 | very_sparse | 113 |
| assist_bkt_test | learner_based | 2 | dense | 12 |

_Showing first 25 of 109 rows._


## 5. Sparse-concept performance metrics

Source file: `results/tables/metric_per_bucket_summary.csv`

| dataset | split_mode | model | bucket | auc_mean | auc_std | acc_mean | acc_std | nll_mean | nll_std | rmse_mean | rmse_std | n_events_sum | n_kcs_first |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | learner_based | bkt | medium | 0.5000 |  | 0.3570 |  | 23.1759 |  | 0.8019 |  | 6597 | 153 |
| junyi_bkt_test | learner_based | bkt | sparse | 0.5000 |  | 0.4080 |  | 21.3376 |  | 0.7694 |  | 9902 | 726 |
| junyi_bkt_test | learner_based | bkt | very_sparse | 0.4397 |  | 0.4048 |  | 18.3959 |  | 0.7346 |  | 1264 | 360 |
| junyi_bkt_test | temporal | bkt | medium | 0.5022 | 0.0000 | 0.3468 | 0.0000 | 23.5450 | 0.0000 | 0.8086 | 0.0000 | 17340 | 142 |
| junyi_bkt_test | temporal | bkt | sparse | 0.5020 | 0.0000 | 0.4166 | 0.0000 | 20.9779 | 0.0000 | 0.7638 | 0.0000 | 31767 | 749 |
| junyi_bkt_test | temporal | bkt | very_sparse | 0.5092 | 0.0000 | 0.4368 | 0.0000 | 20.3056 | 0.0000 | 0.7522 | 0.0000 | 4173 | 295 |


## 6. Calibration diagnostics

### 6.1. ECE by KC bucket

Source file: `results/tables/ece_per_bucket.csv`

| dataset | split_mode | model | seed | bucket | ece | n_events | n_bins |
| --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | learner_based | bkt | 42 | medium | 0.6430 | 6597 | 15 |
| junyi_bkt_test | learner_based | bkt | 42 | sparse | 0.5920 | 9902 | 15 |
| junyi_bkt_test | learner_based | bkt | 42 | very_sparse | 0.5317 | 1264 | 15 |
| junyi_bkt_test | temporal | bkt | 2024 | medium | 0.6546 | 5780 | 15 |
| junyi_bkt_test | temporal | bkt | 2024 | sparse | 0.5834 | 10589 | 15 |
| junyi_bkt_test | temporal | bkt | 2024 | very_sparse | 0.5684 | 1391 | 15 |
| junyi_bkt_test | temporal | bkt | 2025 | medium | 0.6546 | 5780 | 15 |
| junyi_bkt_test | temporal | bkt | 2025 | sparse | 0.5834 | 10589 | 15 |
| junyi_bkt_test | temporal | bkt | 2025 | very_sparse | 0.5684 | 1391 | 15 |
| junyi_bkt_test | temporal | bkt | 42 | medium | 0.6546 | 5780 | 15 |
| junyi_bkt_test | temporal | bkt | 42 | sparse | 0.5834 | 10589 | 15 |
| junyi_bkt_test | temporal | bkt | 42 | very_sparse | 0.5684 | 1391 | 15 |

### 6.2. Brier decomposition

Source file: `results/tables/brier_decomposition_summary.csv`

| dataset | split_mode | model | bucket | brier_mean | brier_std | uncertainty_mean | reliability_mean | resolution_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | learner_based | bkt | medium | 0.6430 |  | 0.2296 | 0.4134 | 0.0000 |
| junyi_bkt_test | learner_based | bkt | sparse | 0.5920 |  | 0.2415 | 0.3505 | 0.0000 |
| junyi_bkt_test | learner_based | bkt | very_sparse | 0.5397 |  | 0.2477 | 0.3000 | 0.0080 |
| junyi_bkt_test | temporal | bkt | medium | 0.6539 | 0.0000 | 0.2256 | 0.4286 | 0.0003 |
| junyi_bkt_test | temporal | bkt | sparse | 0.5834 | 0.0000 | 0.2425 | 0.3410 | 0.0002 |
| junyi_bkt_test | temporal | bkt | very_sparse | 0.5658 | 0.0000 | 0.2446 | 0.3232 | 0.0019 |


## 7. Reliability diagram links

_No reliability diagrams found._


## 8. Cold-start diagnostics

Source file: `results/tables/cold_start_results.csv`

| dataset | split_mode | model | seed | group | n_events | auc | acc | nll | ece | brier | reliability | resolution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | learner_based | bkt | 42 | strict | 16 | 0.5000 | 0.3125 | 0.6931 | 0.1875 | 0.2500 | 0.0352 | 0.0000 |
| junyi_bkt_test | learner_based | bkt | 42 | k5 | 162 | 0.4265 | 0.4074 | 7.0855 | 0.2963 | 0.3333 | 0.1050 | 0.0049 |
| junyi_bkt_test | learner_based | bkt | 42 | k10 | 419 | 0.3925 | 0.3962 | 14.4907 | 0.4528 | 0.4717 | 0.2355 | 0.0137 |
| junyi_bkt_test | learner_based | bkt | 42 | warm | 17344 | 0.5000 | 0.3835 | 22.2191 | 0.6165 | 0.6165 | 0.3800 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 2024 | strict | 12 | 0.5000 | 0.5000 | 18.0218 | 0.5000 | 0.5000 | 0.2500 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 2024 | k5 | 174 | 0.5000 | 0.3871 | 22.0913 | 0.6129 | 0.6129 | 0.3757 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 2024 | k10 | 511 | 0.5128 | 0.4242 | 20.7629 | 0.5833 | 0.5795 | 0.3404 | 0.0026 |
| junyi_bkt_test | temporal | bkt | 2024 | warm | 17249 | 0.5023 | 0.3957 | 21.7503 | 0.6050 | 0.6046 | 0.3664 | 0.0002 |
| junyi_bkt_test | temporal | bkt | 2025 | strict | 12 | 0.5000 | 0.5000 | 18.0218 | 0.5000 | 0.5000 | 0.2500 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 2025 | k5 | 174 | 0.5000 | 0.3871 | 22.0913 | 0.6129 | 0.6129 | 0.3757 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 2025 | k10 | 511 | 0.5128 | 0.4242 | 20.7629 | 0.5833 | 0.5795 | 0.3404 | 0.0026 |
| junyi_bkt_test | temporal | bkt | 2025 | warm | 17249 | 0.5023 | 0.3957 | 21.7503 | 0.6050 | 0.6046 | 0.3664 | 0.0002 |
| junyi_bkt_test | temporal | bkt | 42 | strict | 12 | 0.5000 | 0.5000 | 18.0218 | 0.5000 | 0.5000 | 0.2500 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 42 | k5 | 174 | 0.5000 | 0.3871 | 22.0913 | 0.6129 | 0.6129 | 0.3757 | 0.0000 |
| junyi_bkt_test | temporal | bkt | 42 | k10 | 511 | 0.5128 | 0.4242 | 20.7629 | 0.5833 | 0.5795 | 0.3404 | 0.0026 |
| junyi_bkt_test | temporal | bkt | 42 | warm | 17249 | 0.5023 | 0.3957 | 21.7503 | 0.6050 | 0.6046 | 0.3664 | 0.0002 |


## 9. Sensitivity analysis

Source file: `results/tables/sensitivity_analysis.csv`

| dataset | split_mode | model | seed | setting | bucket | auc | ece | brier | n_events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| junyi_bkt_test | learner_based | bkt | 42 | Main | medium | 0.5000 | 0.6430 | 0.6430 | 6597 |
| junyi_bkt_test | learner_based | bkt | 42 | Main | sparse | 0.5000 | 0.5920 | 0.5920 | 9902 |
| junyi_bkt_test | learner_based | bkt | 42 | Main | very_sparse | 0.4397 | 0.5317 | 0.5397 | 1264 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_1 | dense | 0.5000 | 0.7853 | 0.7853 | 1251 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_1 | medium | 0.5000 | 0.6086 | 0.6086 | 11244 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_1 | sparse | 0.5000 | 0.5800 | 0.5800 | 4910 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_1 | very_sparse | 0.3650 | 0.4681 | 0.4894 | 358 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_2 | medium | 0.5000 | 0.6931 | 0.6931 | 3131 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_2 | sparse | 0.5000 | 0.5955 | 0.5955 | 12138 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_2 | very_sparse | 0.4674 | 0.5542 | 0.5582 | 2494 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_Quantile | dense | 0.5000 | 0.6208 | 0.6208 | 10673 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_Quantile | medium | 0.5000 | 0.6132 | 0.6132 | 4165 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_Quantile | sparse | 0.5000 | 0.5829 | 0.5829 | 2256 |
| junyi_bkt_test | learner_based | bkt | 42 | Alt_Quantile | very_sparse | 0.4010 | 0.5256 | 0.5385 | 669 |
| junyi_bkt_test | temporal | bkt | 2024 | Main | medium | 0.5022 | 0.6546 | 0.6539 | 5780 |
| junyi_bkt_test | temporal | bkt | 2024 | Main | sparse | 0.5020 | 0.5834 | 0.5834 | 10589 |
| junyi_bkt_test | temporal | bkt | 2024 | Main | very_sparse | 0.5092 | 0.5684 | 0.5658 | 1391 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_1 | dense | 0.5041 | 0.8813 | 0.8795 | 1033 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_1 | medium | 0.5013 | 0.5883 | 0.5884 | 11160 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_1 | sparse | 0.5038 | 0.5840 | 0.5828 | 5133 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_1 | very_sparse | 0.5152 | 0.5508 | 0.5466 | 434 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_2 | medium | 0.5022 | 0.7467 | 0.7459 | 2372 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_2 | sparse | 0.5022 | 0.5862 | 0.5861 | 12809 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_2 | very_sparse | 0.5050 | 0.5609 | 0.5595 | 2579 |
| junyi_bkt_test | temporal | bkt | 2024 | Alt_Quantile | dense | 0.5023 | 0.6144 | 0.6140 | 9817 |

_Showing first 25 of 56 rows._


## 10. Leakage audit L1-L7

Source file: `results/tables/leakage_audit_log.csv`

| channel | description | evidence_file | status | notes |
| --- | --- | --- | --- | --- |
| L1 | Split leakage (user overlap, temporal order) | logs/split_audit.csv | PASS | No user overlap or temporal inversions detected |
| L2 | Preprocessing leakage (transformations fit scope) | src/preprocess.py | PASS | No global normalization detected |
| L3 | Q-matrix / KC mapping leakage | data/processed/assist2012/kc_map.json | PASS | Static mapping from dataset |
| L4 | Sparse-bucket leakage | results/tables/kc_strata.csv | PASS | Bucket assignment is strictly based on training frequency |
| L5 | Calibration leakage (test-based tuning) | src/baseline_runner.py | PASS | No post-hoc tuning on test set |
| L6 | Hyperparameter leakage (model selection) | src/baseline_runner.py | PASS | Validation-based selection only |
| L7 | Cold-start leakage | src/three_split_constructor.py | PASS | Classification uses train_freq only |

### Leakage status summary

| status | count |
| --- | --- |
| PASS | 7 |


## 11. Missing outputs or warnings

### 11.2. Warnings

- No reliability diagram files found under results/figures/.

