# Reproduce one diagnostic table

Two tracks. Track A retrains local models. Track B rebuilds locked tables from frozen CSVs and **does not** change ASSISTments T-KT ECE `0.1136` / `0.2280` or FAR `0.196` / `0.268`.

## Track B — rebuild locked tables (no retrain)

```bash
scripts/rebuild_locked_tables.sh
# Windows: scripts/rebuild_locked_tables.ps1
```

This reads `IJIET_FINAL_REVISION/analysis/summary_4part_bucket.csv` (ASSISTments, Junyi) and the masked XES a2b summary, verifies the T-KT ECE locks, and writes Supplementary Tables S8–S9. Three-cut sensitivity (Table S7) is `scripts/p0_si_threecut.py` on the frozen T-KT and DKT prediction CSVs. Full L1–L7 records (Table S10) are `scripts/p0_si_s10_leakage.py` on the frozen train/test split files.

## Track A — retrain local IRT / DKT / T-KT

1. Obtain ASSISTments 2012 / Junyi / XES3G5M from the original providers.
2. Train-only KC strata use cuts `f=0`, `0<f<20`, `20≤f<100`, `100≤f<500`, `f≥500` (see `analysis/leakage_audit_log.csv` L4).
3. `scripts/reproduce_one_dataset.sh` (or `.ps1`) retrains the local T-KT/DKT/IRT pipeline from a YAML config. It does **not** reproduce the locked ASSISTments T-KT ECE `0.1136`/`0.2280` or FAR `0.196`/`0.268`.
4. Four-partition ECE/Brier: `analysis/summary_4part_bucket.csv`.
5. Reliability figure (main-text Fig. 3): `IJIET_FINAL_REVISION/figures/generate_fig2_reliability.py` (seed-42 prediction CSVs + `results/tables/kc_strata.csv`). Pipeline Fig. 1: `IJIET_FINAL_REVISION/figures/generate_fig1_pipeline.py`.
6. T-KT is a local Transformer baseline, not published SimpleKT. Official SimpleKT `[4]` on ASSISTments is `results/reports/p0_official_simplekt_assist_ece.json`.
7. BKT is not a scored baseline (pyBKT 1.4.1 degenerated on ASSISTments seed 42); IRT is the classical reference.

Minimal review artefact: `output/code_for_review_anonymous.zip`.
