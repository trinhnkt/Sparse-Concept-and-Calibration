
# P0 Pre-submission Checklist

## Scope
- [x] The paper is framed as protocol/diagnostic/resource study.
- [x] No SSL, GNN, graph augmentation, path recommendation, or distillation appears in Method/Experiments.
- [x] No “first” or universal claim is made without literature verification.

## Experiments
- [x] At least three datasets: ASSISTments 2012, Junyi Academy, and XES3G5M.
- [x] At least three baselines: IRT, DKT, and SimpleKT.
- [x] At least five random seeds (42, 2024, 2025, 2026, 2027).
- [x] Predictions are saved with user_id, item_id, kc_id, timestamp, y_true, p_pred, dataset, model, split, seed.
- [x] KC buckets are based only on train_freq.
- [x] ECE 15-bin and Brier decomposition are computed per bucket.
- [x] Reliability diagrams are generated.
- [x] Limited cold-start KC analysis is reported.
- [x] Threshold sensitivity is reported or placed in appendix.

## Leakage audit
- [x] L1 split leakage checked.
- [x] L2 preprocessing leakage checked.
- [x] L3 Q-matrix/KC mapping provenance documented.
- [x] L4 sparse-bucket leakage checked.
- [x] L5 calibration leakage checked.
- [x] L6 hyperparameter leakage checked.
- [x] L7 cold-start leakage checked.
- [x] L8 predictive sanity check verified.

## Artifact
- [x] README includes installation and reproduction commands.
- [x] `reproduce_one_dataset.sh` runs successfully.
- [x] Result tables are generated from scripts, not manually edited.
- [x] Figure files are generated from scripts.
