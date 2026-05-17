# setup_EXPERIMENT.md

## Project

**Project name:** `p0-sparse-calibration-kt`  
**Paper title:** *Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing*  
**Paper type:** Protocol / diagnostic / resource paper  
**Research context:** First conference paper for the SA-SSL-KT PhD roadmap  
**Primary goal:** Build a reproducible experimental project that evaluates Knowledge Tracing baselines under sparse-concept, calibration, limited cold-start concept, and leakage-audit settings.

---

## 0. Non-negotiable scope constraints

This project is **P0**. It must remain a diagnostic/evaluation project.

### Allowed

- Run existing Knowledge Tracing baselines.
- Construct learner-based, temporal, and limited cold-start concept splits.
- Stratify Knowledge Components (KCs) by training frequency.
- Compute AUC, ACC, NLL/BCE, RMSE.
- Compute calibration metrics: ECE 15-bin, Brier score, Brier decomposition.
- Generate reliability diagrams by KC stratum.
- Perform limited cold-start concept diagnostics.
- Run leakage audit L1–L7.
- Generate tables, figures, and a reproducible diagnostic report.

### Forbidden in P0

Do **not** implement or add:

- New KT model architecture.
- SSL, contrastive learning, masked concept prediction, generative SSL.
- GNN or graph neural message passing.
- Multi-relational concept graph learning.
- Prerequisite-preserving graph augmentation.
- Learning path recommendation.
- Reinforcement learning.
- Knowledge distillation or compressed student models.
- Claims of SOTA or model improvement.

If any of these are requested later, place them in `docs/backlog_P1_P2_P3.md`, not in P0.

---

## 1. Expected repository structure

Create the following repository:

```text
p0-sparse-calibration-kt/
├── README.md
├── requirements.txt
├── pyproject.toml                         # optional, for formatting/tests
├── configs/
│   ├── default.yaml
│   ├── assist2012.yaml
│   ├── junyi.yaml
│   └── xes3g5m.yaml                       # optional extension
├── data/
│   ├── raw/                               # gitignored
│   ├── processed/                         # gitignored except tiny sample
│   └── sample/                            # small synthetic/demo data allowed
├── src/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── three_split_constructor.py
│   ├── split_checker.py
│   ├── kc_strata.py
│   ├── cold_start_split.py
│   ├── baseline_runner.py
│   ├── prediction_exporter.py
│   ├── metrics.py
│   ├── calibration_eval.py
│   ├── brier_decomposition.py
│   ├── reliability_diagram_plotter.py
│   ├── sensitivity_analysis.py
│   ├── statistical_tests.py
│   ├── leakage_checklist_runner.py
│   └── report_generator.py
├── scripts/
│   ├── run_assist_minimal.sh
│   ├── run_junyi_minimal.sh
│   ├── reproduce_one_dataset.sh
│   ├── make_all_tables.sh
│   └── make_all_figures.sh
├── notebooks/
│   ├── 01_dataset_stats.ipynb
│   ├── 02_bucket_distribution.ipynb
│   ├── 03_baseline_reproduction.ipynb
│   ├── 04_calibration_per_bucket.ipynb
│   └── 05_cold_start_diagnostic.ipynb
├── results/
│   ├── predictions/
│   ├── tables/
│   ├── figures/
│   └── reports/
├── logs/
│   ├── experiment_log.csv
│   ├── leakage_audit_log.csv
│   ├── calibration_log.csv
│   └── literature_search_log.csv
├── docs/
│   ├── scope_note_1p.md
│   ├── claim_dictionary.md
│   ├── leakage_definitions.md
│   ├── qmatrix_provenance.md
│   ├── how_to_reproduce.md
│   └── backlog_P1_P2_P3.md
├── paper/
│   ├── main.tex
│   ├── references.bib
│   ├── tables/
│   └── figures/
└── tests/
    ├── test_metrics.py
    ├── test_brier_decomposition.py
    ├── test_ece.py
    ├── test_split_checker.py
    └── test_kc_strata.py
```

---

## 2. Environment requirements

Use Python 3.10+.

Suggested `requirements.txt`:

```text
numpy>=1.24
pandas>=2.0
scikit-learn>=1.3
scipy>=1.10
matplotlib>=3.7
pyyaml>=6.0
tqdm>=4.66
pytest>=7.0
```

Optional dependencies:

```text
torch
pykt-toolkit
```

If pyKT is not installed or not stable, implement a lightweight adapter that can read prediction CSVs exported from external pyKT runs. P0 only requires reproducible predictions and metrics, not a full reimplementation of all KT models.

---

## 3. Dataset schema

All datasets must be normalized to the following canonical schema:

```text
user_id,item_id,kc_id,timestamp,correct
```

Field definitions:

| Field | Meaning |
|---|---|
| `user_id` | Learner identifier |
| `item_id` | Exercise/question/problem identifier |
| `kc_id` | Knowledge component / skill identifier |
| `timestamp` | Interaction timestamp, integer or ISO datetime |
| `correct` | Binary label, 1 = correct, 0 = incorrect |

### Supported datasets

Minimal:

```text
ASSISTments 2012
Junyi Academy
```

Optional:

```text
XES3G5M
```

Do not include EdNet KT1 in the minimal P0 pipeline unless explicitly approved. It is large and may slow down the first paper.

---

## 4. Configuration files

Create `configs/default.yaml`:

```yaml
project:
  name: p0-sparse-calibration-kt
  paper_type: diagnostic_protocol

random_seeds: [42, 123, 2026]

splits:
  learner_based:
    test_ratio: 0.2
    valid_ratio_from_train: 0.1
  temporal:
    train_ratio: 0.7
    valid_ratio: 0.1
    test_ratio: 0.2
  cold_start:
    strict: true
    limited_k_values: [5, 10]
    primary_k: 10

kc_strata:
  main_thresholds: [20, 100, 500]
  labels: [very_sparse, sparse, medium, dense]
  alternative_thresholds:
    - [10, 50, 250]
    - [30, 150, 750]
    - quantile

calibration:
  n_bins: 15
  binning: fixed_width
  temperature_scaling: false

baselines:
  minimal: [BKT, DKT, simpleKT]
  fallback: [BKT, DKT, AKT]
  optional: [DKVMN, sparseKT]

leakage_audit:
  channels: [L1_split, L2_preprocessing, L3_qmatrix, L4_sparse_bucket, L5_calibration, L6_hyperparameter, L7_cold_start]
```

Create dataset-specific configs:

`configs/assist2012.yaml`:

```yaml
dataset:
  name: assist2012
  raw_path: data/raw/assist2012.csv
  processed_path: data/processed/assist2012/interactions.csv
  user_col: user_id
  item_col: problem_id
  kc_col: skill_id
  timestamp_col: timestamp
  correct_col: correct
  qmatrix_provenance: caution_required
```

`configs/junyi.yaml`:

```yaml
dataset:
  name: junyi
  raw_path: data/raw/junyi_log.csv
  processed_path: data/processed/junyi/interactions.csv
  user_col: user_id
  item_col: exercise
  kc_col: exercise
  timestamp_col: time_done
  correct_col: correct
  qmatrix_provenance: expert_or_static_mapping
```

---

## 5. Core scripts to implement

### 5.1 `src/preprocess.py`

Purpose: normalize raw dataset into canonical schema.

Input:

```text
configs/{dataset}.yaml
```

Output:

```text
data/processed/{dataset}/interactions.csv
results/tables/dataset_stats.csv
logs/preprocess_log.json
```

Required behavior:

- Rename raw columns to canonical schema.
- Sort interactions by `user_id`, then `timestamp`.
- Drop rows with missing `user_id`, `kc_id`, or `correct`.
- Preserve timestamp ordering.
- Log every transformation.
- Do not fit normalization on full data if normalization is used.

Acceptance checks:

- `correct` is binary.
- No missing `user_id`, `kc_id`, `correct` after preprocessing.
- Every dataset has at least one KC and one learner.
- Output schema exactly equals `user_id,item_id,kc_id,timestamp,correct`.

---

### 5.2 `src/three_split_constructor.py`

Purpose: create learner-based, temporal, and cold-start concept splits.

Output:

```text
data/processed/{dataset}/splits/learner/fold_{k}/train.csv
.../valid.csv
.../test.csv

data/processed/{dataset}/splits/temporal/fold_0/train.csv
.../valid.csv
.../test.csv

data/processed/{dataset}/splits/cold_start_k10/fold_{k}/train.csv
.../valid.csv
.../test.csv
```

Learner-based split:

- No learner overlap across train/valid/test.
- Default test ratio: 20% learners.
- Validation split from train learners.

Temporal split:

- Split by global timestamp or per-dataset timestamp cutoff.
- Train contains earliest interactions, then valid, then test.

Cold-start concept split:

- Compute `freq_train(c)` from train only.
- Strict cold-start: `freq_train(c) = 0`.
- Limited cold-start: `freq_train(c) <= k`, with `k=10` as primary.

---

### 5.3 `src/split_checker.py`

Purpose: audit L1 split leakage.

Output:

```text
results/tables/split_report.csv
logs/split_audit.csv
```

Checks:

- Learner overlap is zero for learner-based split.
- Temporal order is respected for temporal split.
- Split sizes are non-empty.
- Test set is not used during training.

Required fields in `split_report.csv`:

```text
dataset,split,fold,n_train,n_valid,n_test,n_train_users,n_valid_users,n_test_users,user_overlap,temporal_valid,status
```

---

### 5.4 `src/kc_strata.py`

Purpose: assign KC-frequency buckets using train-only frequency.

Output:

```text
results/tables/kc_strata.csv
results/tables/bucket_distribution.csv
results/figures/kc_bucket_distribution.pdf
```

Bucket rules:

```text
very_sparse: freq_train(c) < 20
sparse: 20 <= freq_train(c) < 100
medium: 100 <= freq_train(c) < 500
dense: freq_train(c) >= 500
```

Required fields:

```text
dataset,split,fold,kc_id,train_freq,valid_freq,test_freq,bucket
```

Acceptance check:

- Bucket assignment uses only `train_freq`.
- `valid_freq` and `test_freq` are logged only for audit.

---

### 5.5 `src/baseline_runner.py`

Purpose: run or orchestrate existing KT baselines.

Minimal baselines:

```text
BKT
DKT
simpleKT or AKT
```

Recommended seeds:

```text
42, 123, 2026
```

Output:

```text
results/predictions/{dataset}_{split}_{model}_seed{seed}.csv
results/tables/overall_results.csv
logs/experiment_log.csv
```

Prediction CSV schema:

```text
dataset,split,fold,model,seed,user_id,item_id,kc_id,timestamp,y_true,p_pred
```

Acceptance checks:

- `p_pred` is in [0, 1].
- `y_true` is binary.
- Every prediction has a `kc_id`.
- The test set is loaded only after training/model selection.

If pyKT is used externally, implement this script as an adapter that reads pyKT predictions and converts them to the required prediction CSV schema.

---

### 5.6 `src/metrics.py`

Purpose: compute predictive metrics.

Required metrics:

- AUC-ROC
- Accuracy
- NLL/BCE
- RMSE

Output:

```text
results/tables/overall_results.csv
results/tables/metric_per_bucket.csv
```

For accuracy, default threshold is 0.5. If threshold tuning is added later, it must be tuned only on validation and logged. For P0 minimal pipeline, do not tune threshold.

---

### 5.7 `src/calibration_eval.py`

Purpose: compute ECE 15-bin and per-bin calibration data.

ECE formula:

```text
ECE = sum_m (|B_m| / N) * |acc(B_m) - conf(B_m)|
```

Fixed-width bins:

```text
M = 15
bin edges = linspace(0, 1, 16)
```

Output:

```text
results/tables/ece_per_bucket.csv
results/tables/calibration_bins.csv
logs/calibration_log.csv
```

Required fields in `ece_per_bucket.csv`:

```text
dataset,split,fold,model,seed,bucket,n_events,ece,n_bins
```

Required fields in `calibration_bins.csv`:

```text
dataset,split,fold,model,seed,bucket,bin_id,bin_left,bin_right,n_bin,conf_bin,acc_bin,gap_bin
```

Acceptance checks:

- Empty bins are handled safely.
- No calibration parameter is fitted on test data.
- `n_bins=15` unless config explicitly changes it for a documented sensitivity run.

---

### 5.8 `src/brier_decomposition.py`

Purpose: compute Brier score and decomposition.

Formulas:

```text
BS = mean((p_i - y_i)^2)
BS = UNC - RES + REL
UNC = y_bar * (1 - y_bar)
REL = (1/N) * sum_m n_m * (conf_m - acc_m)^2
RES = (1/N) * sum_m n_m * (acc_m - y_bar)^2
```

Output:

```text
results/tables/brier_decomposition.csv
```

Required fields:

```text
dataset,split,fold,model,seed,bucket,n_events,brier,uncertainty,reliability,resolution
```

Acceptance tests:

- Direct Brier score equals `UNC - RES + REL` within numerical tolerance.
- On a perfectly calibrated synthetic dataset, REL should be near 0.
- On an over-confident synthetic dataset, REL should increase.

---

### 5.9 `src/reliability_diagram_plotter.py`

Purpose: generate reliability diagrams.

Output:

```text
results/figures/reliability_diagram_sparse_dense.pdf
results/figures/reliability_per_bucket/{dataset}_{model}_{bucket}.pdf
```

Requirements:

- Plot empirical accuracy vs predicted confidence.
- Include diagonal `y=x` reference line.
- Include ECE and sample size in title or caption metadata.
- Produce publication-ready PDF figures.

Do not use seaborn. Use matplotlib.

---

### 5.10 `src/cold_start_split.py`

Purpose: compute strict and limited cold-start concept groups.

Definitions:

```text
strict cold-start: freq_train(c) = 0
limited cold-start: freq_train(c) <= k
primary k = 10
```

Output:

```text
results/tables/cold_start_feasibility.csv
results/tables/cold_start_results.csv
logs/cold_start_audit.csv
```

Required fields in `cold_start_results.csv`:

```text
dataset,split,fold,model,seed,k_value,group,n_kcs,n_events,auc,acc,ece,brier,reliability,resolution
```

Terminology rule:

- Do not call the whole `very_sparse` bucket “cold-start”.
- Use “limited cold-start KC with k=10”.
- Always report `k_value`.

---

### 5.11 `src/sensitivity_analysis.py`

Purpose: evaluate sensitivity to KC-bucket thresholds.

Alternative settings:

```text
main: [20, 100, 500]
alt_1: [10, 50, 250]
alt_2: [30, 150, 750]
alt_3: quantile-based 25/50/75
```

Output:

```text
results/tables/sensitivity_analysis.csv
```

Required fields:

```text
dataset,split,fold,model,seed,threshold_setting,bucket,auc,ece,brier,reliability,n_events
```

If ranking or conclusions are unstable, report this as a limitation rather than hiding it.

---

### 5.12 `src/leakage_checklist_runner.py`

Purpose: run leakage audit L1–L7.

Channels:

| Channel | Meaning | Evidence |
|---|---|---|
| L1 | Split leakage | `split_report.csv` |
| L2 | Preprocessing leakage | `preprocess_log.json` |
| L3 | Q-matrix / KC mapping leakage | `qmatrix_provenance.md` |
| L4 | Sparse-bucket leakage | `kc_strata.csv` |
| L5 | Calibration leakage | `calibration_log.csv` |
| L6 | Hyperparameter leakage | `experiment_log.csv` |
| L7 | Cold-start leakage | `cold_start_audit.csv` |

Output:

```text
results/tables/leakage_audit_log.csv
logs/leakage_audit_log.csv
```

Required fields:

```text
dataset,split,fold,channel,status,evidence_file,notes
```

Status values:

```text
PASS
FAIL
CAUTION
NOT_APPLICABLE
```

---

### 5.13 `src/report_generator.py`

Purpose: generate a Markdown diagnostic report.

Output:

```text
results/reports/p0_diagnostic_report.md
```

Report sections:

1. Dataset statistics
2. Split audit
3. Baseline reproduction
4. KC bucket distribution
5. Overall metrics
6. Sparse-concept performance
7. Calibration diagnostics
8. Reliability diagrams
9. Cold-start concept diagnostics
10. Threshold sensitivity
11. Leakage audit L1–L7
12. Files generated

---

## 6. Experiments to run

### E0. Dataset statistics

Output:

```text
results/tables/dataset_stats.csv
results/figures/kc_bucket_distribution.pdf
```

### E1. Split construction and audit

Output:

```text
results/tables/split_report.csv
```

### E2. Baseline reproduction

Output:

```text
results/tables/overall_results.csv
results/predictions/*.csv
```

### E3. KC-frequency stratification

Output:

```text
results/tables/kc_strata.csv
results/tables/bucket_distribution.csv
```

### E4. Sparse-KC predictive diagnostics

Output:

```text
results/tables/metric_per_bucket.csv
```

### E5. Calibration diagnostics

Output:

```text
results/tables/ece_per_bucket.csv
results/tables/brier_decomposition.csv
```

### E6. Reliability diagrams

Output:

```text
results/figures/reliability_diagram_sparse_dense.pdf
```

### E7. Limited cold-start concept diagnostics

Output:

```text
results/tables/cold_start_results.csv
```

### E8. Threshold sensitivity analysis

Output:

```text
results/tables/sensitivity_analysis.csv
```

### E9. Statistical testing

Output:

```text
results/tables/stats_report.csv
```

Minimal submission requires E0–E7. E8 is strongly recommended. E9 is recommended if enough seeds/folds are available.

---

## 7. Commands to support

### Minimal one-dataset reproduction

```bash
bash scripts/reproduce_one_dataset.sh --dataset assist2012 --split learner --models BKT,DKT,simpleKT --seeds 42,123,2026
```

### Run Junyi minimal

```bash
bash scripts/run_junyi_minimal.sh
```

### Run ASSISTments minimal

```bash
bash scripts/run_assist_minimal.sh
```

### Generate all tables

```bash
bash scripts/make_all_tables.sh
```

### Generate all figures

```bash
bash scripts/make_all_figures.sh
```

---

## 8. Paper-ready outputs

The project must generate these files for the LaTeX paper:

```text
paper/tables/table_dataset_statistics.tex
paper/tables/table_leakage_audit.tex
paper/tables/table_overall_results.tex
paper/tables/table_strata_performance.tex
paper/tables/table_calibration_results.tex
paper/tables/table_cold_start.tex
paper/tables/table_sensitivity_appendix.tex

paper/figures/diagnostic_pipeline.pdf
paper/figures/kc_bucket_distribution.pdf
paper/figures/reliability_diagram_sparse_dense.pdf
paper/figures/ece_by_bucket.pdf
paper/figures/brier_rel_by_bucket.pdf
```

Tables may also be generated as CSV first and manually converted to LaTeX after verification.

---

## 9. Testing requirements

Implement unit tests for:

### `test_ece.py`

- Perfect calibration gives ECE close to 0.
- Over-confident predictions give larger ECE.
- Empty bins do not crash.

### `test_brier_decomposition.py`

- Direct Brier equals `UNC - RES + REL` within tolerance.
- REL is near 0 on synthetic calibrated data.

### `test_split_checker.py`

- Learner overlap is detected.
- Temporal violation is detected.

### `test_kc_strata.py`

- Buckets are assigned only from `train_freq`.
- Boundary cases work correctly: 19, 20, 99, 100, 499, 500.

Run tests:

```bash
pytest tests/
```

---

## 10. Minimal completion criteria

The project is complete at the minimal level when:

- [ ] ASSISTments 2012 and Junyi are preprocessed.
- [ ] Learner-based split works without learner overlap.
- [ ] Temporal split works with correct ordering.
- [ ] Limited cold-start split works with `k=10`.
- [ ] BKT, DKT, and simpleKT or AKT run on both datasets.
- [ ] At least 3 seeds are completed.
- [ ] Prediction CSVs are exported.
- [ ] Overall AUC, ACC, NLL, RMSE are computed.
- [ ] KC buckets are assigned using train-only frequency.
- [ ] AUC/ACC/NLL by bucket are computed.
- [ ] ECE 15-bin by bucket is computed.
- [ ] Brier decomposition by bucket is computed.
- [ ] Reliability diagrams are generated.
- [ ] Limited cold-start concept diagnostics are computed.
- [ ] Leakage audit L1–L7 is generated.
- [ ] `reproduce_one_dataset.sh` runs successfully.
- [ ] `p0_diagnostic_report.md` is generated.

---

## 11. Writing rules for generated report and paper

Use safe claims:

```text
We propose a reproducible diagnostic protocol.
We report calibration diagnostics by KC-frequency stratum.
Under our experimental conditions, model rankings under overall AUC may differ from rankings under sparse-KC calibration metrics.
```

Avoid unsafe claims:

```text
We propose a new KT model.
We outperform pyKT.
We solve cold-start KT.
We prove that deep KT is worse on sparse KCs.
We are the first to evaluate calibration in KT.
```

Always include:

```text
under our experimental conditions
on ASSISTments 2012 and Junyi Academy
to our knowledge after literature verification
may differ
```

---

## 12. Deliverable summary

At the end, Antigravity should produce:

```text
1. A complete Python project under p0-sparse-calibration-kt/
2. Reproducible scripts for one-dataset and two-dataset runs
3. All result CSV files in results/tables/
4. All figures in results/figures/
5. Leakage audit logs
6. A Markdown diagnostic report
7. Paper-ready LaTeX tables and figures
8. A README that explains installation, data preparation, and reproduction
```

The project must support the first conference paper: **Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing**.
