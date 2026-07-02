# 📊 Mini-Test Baseline Results Summary Report

**Date & Time:** 2026-05-17 15:43:53
**Source File:** `results/tables/overall_results.csv`

## 🔍 1. Compact Performance Matrix (Mean ± Std)

| Dataset | Split Mode | Model | AUC | ACC | NLL | RMSE |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| assist_gpu_test | learner_based | bkt | 0.4981 ± 0.0010 | 0.3040 ± 0.0030 | 25.0209 ± 0.0953 | 0.8336 ± 0.0016 |
| assist_gpu_test | learner_based | dkt | 0.5451 ± 0.0046 | 0.6491 ± 0.0032 | 0.9969 ± 0.0270 | 0.5245 ± 0.0038 |
| assist_gpu_test | learner_based | simplekt | 0.5545 ± 0.0023 | 0.6339 ± 0.0075 | 1.4421 ± 0.0192 | 0.5551 ± 0.0033 |
| assist_gpu_test | temporal | bkt | 0.4850 ± 0.0000 | 0.3454 ± 0.0000 | 22.2080 ± 0.0000 | 0.8004 ± 0.0000 |
| assist_gpu_test | temporal | dkt | 0.5015 ± 0.0027 | 0.6404 ± 0.0015 | 0.9284 ± 0.0069 | 0.5303 ± 0.0014 |
| assist_gpu_test | temporal | simplekt | 0.4948 ± 0.0040 | 0.6233 ± 0.0025 | 1.4291 ± 0.0170 | 0.5641 ± 0.0012 |
| junyi_bkt_test | learner_based | bkt | 0.4990 ± 0.0031 | 0.3963 ± 0.0109 | 21.6806 ± 0.3084 | 0.7762 ± 0.0059 |
| junyi_bkt_test | temporal | bkt | 0.5026 ± 0.0000 | 0.3966 ± 0.0000 | 21.7209 ± 0.0000 | 0.7771 ± 0.0000 |
| xes_bkt_test | learner_based | bkt | 0.5013 ± 0.0003 | 0.3229 ± 0.0204 | 24.3932 ± 0.7311 | 0.8230 ± 0.0123 |
| xes_bkt_test | temporal | bkt | 0.4937 ± 0.0000 | 0.3408 ± 0.0000 | 22.1637 ± 0.0000 | 0.8202 ± 0.0000 |
| xes_dkt_test | learner_based | dkt | 0.8586 ± 0.0097 | 0.8475 ± 0.0168 | 0.3670 ± 0.0251 | 0.3370 ± 0.0149 |
| xes_dkt_test | temporal | dkt | 0.5001 ± 0.0012 | 0.6615 ± 0.0139 | 0.7095 ± 0.0258 | 0.4809 ± 0.0082 |
| xes_gpu_test | learner_based | bkt | 0.5013 ± 0.0003 | 0.3229 ± 0.0204 | 24.3932 ± 0.7311 | 0.8230 ± 0.0123 |
| xes_gpu_test | learner_based | dkt | 0.8586 ± 0.0097 | 0.8475 ± 0.0168 | 0.3670 ± 0.0251 | 0.3370 ± 0.0149 |
| xes_gpu_test | learner_based | simplekt | 0.8672 ± 0.0059 | 0.8410 ± 0.0145 | 0.3800 ± 0.0234 | 0.3422 ± 0.0131 |
| xes_gpu_test | temporal | bkt | 0.4937 ± 0.0000 | 0.3408 ± 0.0000 | 22.1637 ± 0.0000 | 0.8202 ± 0.0000 |
| xes_gpu_test | temporal | dkt | 0.5001 ± 0.0012 | 0.6615 ± 0.0139 | 0.7095 ± 0.0258 | 0.4809 ± 0.0082 |
| xes_gpu_test | temporal | simplekt | 0.5043 ± 0.0027 | 0.5931 ± 0.0358 | 0.8073 ± 0.0553 | 0.5199 ± 0.0215 |
| xes_simplekt_test | learner_based | simplekt | 0.8673 ± 0.0060 | 0.8410 ± 0.0130 | 0.3796 ± 0.0226 | 0.3421 ± 0.0121 |
| xes_simplekt_test | temporal | simplekt | 0.5043 ± 0.0028 | 0.5951 ± 0.0337 | 0.8060 ± 0.0539 | 0.5193 ± 0.0206 |

## 🚨 2. Suspicious Results Audit

| Dataset | Split | Model | Seed | AUC | ACC | NLL | RMSE | Suspicious Reason |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| assist_gpu_test | learner_based | bkt | 2024 | 0.4978 | 0.3011 | 25.1095 | 0.8353 | **Suspicious AUC: 0.4978279429489755, Extremely high/low ACC: 0.3011494252873563** |
| assist_gpu_test | learner_based | bkt | 2025 | 0.4972 | 0.3038 | 25.0332 | 0.8336 | **Suspicious AUC: 0.4971830985915493, Extremely high/low ACC: 0.3037865748709122** |
| assist_gpu_test | learner_based | bkt | 42 | 0.4992 | 0.3072 | 24.9200 | 0.8320 | **Suspicious AUC: 0.4991607894592969, Extremely high/low ACC: 0.3071646341463415** |
| assist_gpu_test | temporal | bkt | 2024 | 0.4850 | 0.3454 | 22.2080 | 0.8004 | **Suspicious AUC: 0.4849848069369302, Extremely high/low ACC: 0.3454356846473029** |
| assist_gpu_test | temporal | bkt | 2025 | 0.4850 | 0.3454 | 22.2080 | 0.8004 | **Suspicious AUC: 0.4849848069369302, Extremely high/low ACC: 0.3454356846473029** |
| assist_gpu_test | temporal | bkt | 42 | 0.4850 | 0.3454 | 22.2080 | 0.8004 | **Suspicious AUC: 0.4849848069369302, Extremely high/low ACC: 0.3454356846473029** |
| assist_gpu_test | temporal | dkt | 2025 | 0.4984 | 0.6388 | 0.9343 | 0.5319 | **Suspicious AUC: 0.4984444004408894** |
| assist_gpu_test | temporal | simplekt | 2024 | 0.4980 | 0.6248 | 1.4102 | 0.5629 | **Suspicious AUC: 0.4980324007370922** |
| assist_gpu_test | temporal | simplekt | 2025 | 0.4960 | 0.6246 | 1.4341 | 0.5640 | **Suspicious AUC: 0.4960145996571334** |
| assist_gpu_test | temporal | simplekt | 42 | 0.4904 | 0.6204 | 1.4431 | 0.5653 | **Suspicious AUC: 0.4904018887376679** |
| junyi_bkt_test | learner_based | bkt | 42 | 0.4954 | 0.3839 | 22.0344 | 0.7829 | **Suspicious AUC: 0.495420499004736** |
| xes_bkt_test | learner_based | bkt | 2024 | 0.5016 | 0.3402 | 23.7716 | 0.8125 | **Extremely high/low ACC: 0.3402181972248702** |
| xes_bkt_test | learner_based | bkt | 2025 | 0.5010 | 0.3003 | 25.1987 | 0.8366 | **Extremely high/low ACC: 0.300337803255195** |
| xes_bkt_test | learner_based | bkt | 42 | 0.5014 | 0.3280 | 24.2093 | 0.8200 | **Extremely high/low ACC: 0.3280121626757887** |
| xes_bkt_test | temporal | bkt | 2024 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_bkt_test | temporal | bkt | 2025 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_bkt_test | temporal | bkt | 42 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_dkt_test | temporal | dkt | 2024 | 0.4995 | 0.6568 | 0.7043 | 0.4841 | **Suspicious AUC: 0.499535296938028** |
| xes_dkt_test | temporal | dkt | 2025 | 0.4992 | 0.6507 | 0.7374 | 0.4871 | **Suspicious AUC: 0.4992256333742931** |
| xes_gpu_test | learner_based | bkt | 2024 | 0.5016 | 0.3402 | 23.7716 | 0.8125 | **Extremely high/low ACC: 0.3402181972248702** |
| xes_gpu_test | learner_based | bkt | 2025 | 0.5010 | 0.3003 | 25.1987 | 0.8366 | **Extremely high/low ACC: 0.300337803255195** |
| xes_gpu_test | learner_based | bkt | 42 | 0.5014 | 0.3280 | 24.2093 | 0.8200 | **Extremely high/low ACC: 0.3280121626757887** |
| xes_gpu_test | temporal | bkt | 2024 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_gpu_test | temporal | bkt | 2025 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_gpu_test | temporal | bkt | 42 | 0.4937 | 0.3408 | 22.1637 | 0.8202 | **Suspicious AUC: 0.4937357026518826, Extremely high/low ACC: 0.3407883986928104** |
| xes_gpu_test | temporal | dkt | 2024 | 0.4995 | 0.6568 | 0.7043 | 0.4841 | **Suspicious AUC: 0.499535296938028** |
| xes_gpu_test | temporal | dkt | 2025 | 0.4992 | 0.6507 | 0.7374 | 0.4871 | **Suspicious AUC: 0.4992256333742931** |

### 💡 Interpretation of Suspicious Findings:
- **BKT Low ACC / High NLL:** In BKT runs, BKT frequently outputs NaN for cold-start concepts, which degrades overall performance metrics or causes high NLL due to lack of probability estimates on unseen skills.
- **Low AUC in Temporal Split:** As demonstrated in our paper, the temporal split causes deep learning models (DKT and SimpleKT) to lose diagnostic power, leading to AUC values near 0.50 (random guessing).
