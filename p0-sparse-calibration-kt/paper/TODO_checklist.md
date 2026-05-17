
# P0 Pre-submission Checklist

## Scope
- [ ] The paper is framed as protocol/diagnostic/resource study.
- [ ] No SSL, GNN, graph augmentation, path recommendation, or distillation appears in Method/Experiments.
- [ ] No “first” or universal claim is made without literature verification.

## Experiments
- [ ] At least two datasets: ASSISTments 2012 and Junyi Academy.
- [ ] At least three baselines: BKT, DKT, and simpleKT or AKT.
- [ ] At least three random seeds.
- [ ] Predictions are saved with user_id, item_id, kc_id, timestamp, y_true, p_pred, dataset, model, split, seed.
- [ ] KC buckets are based only on train_freq.
- [ ] ECE 15-bin and Brier decomposition are computed per bucket.
- [ ] Reliability diagrams are generated.
- [ ] Limited cold-start KC analysis is reported.
- [ ] Threshold sensitivity is reported or placed in appendix.

## Leakage audit
- [ ] L1 split leakage checked.
- [ ] L2 preprocessing leakage checked.
- [ ] L3 Q-matrix/KC mapping provenance documented.
- [ ] L4 sparse-bucket leakage checked.
- [ ] L5 calibration leakage checked.
- [ ] L6 hyperparameter leakage checked.
- [ ] L7 cold-start leakage checked.

## Artifact
- [ ] README includes installation and reproduction commands.
- [ ] `reproduce_one_dataset.sh` runs successfully.
- [ ] Result tables are generated from scripts, not manually edited.
- [ ] Figure files are generated from scripts.
