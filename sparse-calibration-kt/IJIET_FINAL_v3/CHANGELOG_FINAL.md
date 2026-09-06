# CHANGELOG_FINAL — IJIET_FINAL_v3 freeze

**Frozen:** 2026-09-06  
**Source living pack:** `IJIET_FINAL_REVISION/`  
**Baseline (do not overwrite):** `manuscript/main_ijiet_blind.pdf`  
**Also stored as:** `manuscript/BASELINE_main_ijiet_blind.pdf`  
**Pages at freeze:** named 9 / blind 9  
**SHA-256 baseline blind PDF:** `96b58bf700c598b18c222c0b25479b01fceac27f03b5a118dfe32136675252a6`

This folder is a snapshot. It is not a licence to rewrite numbers.

## Locked printed cells (baseline)

Do not change these unless a new script output is reviewed and the old cell is marked obsolete.

| Cell | Value | Trace |
|---|---|---|
| ASSISTments T-KT ECE dense / sparse | 0.1136 / 0.2280 (N=415 L) | `results/analysis/summary_4part_bucket.csv` (`simplekt`) |
| ASSISTments T-KT FAR seed-42 dense / sparse | 0.196 / 0.268 | SI S5; `results/analysis/ijiet08_seed42_gate_points.csv` |
| ΔFAR partition mean (4 unique) | 0.056 (range 0.015–0.087) | `results/analysis/far_partition_robustness.csv` |
| ΔFAR five-run mean | 0.047 (sd 0.033) | same; not five independent folds |
| FAR CI seed-42 | [0.006, 0.138] | `results/analysis/c2_fivefold_verdict.txt` |
| XES T-KT ECE (masked) | 0.1176 / 0.1129 / 0.1254 | `results/a2b_analysis/summary_4part_bucket.csv` |
| Table 9 XES very-sparse | N=114; T-KT 0.184; DKT 0.173 | same a2b file |
| Official SimpleKT Assist AUC / ACC | 0.7700±0.0013 / 0.7522±0.0014 | `results/reports/p0_official_simplekt_assist_ece.json` |
| Official SimpleKT Assist ECE d/m/s | 0.0203 / 0.0262 / 0.0884 | same JSON |

T-KT is the local Transformer. It is not published SimpleKT `[4]`.  
BKT is not a scored baseline. IRT is the classical reference.  
GKT / CL4KT are not scored.

## What this freeze contains

```
IJIET_FINAL_v3/
├── manuscript/          baseline blind PDF + named/blind Word + SI PDF
├── scripts/             rebuild / reproduce / SI compile only
├── results/             CSVs and JSON that back printed tables
├── supplementary/       S1–S9 tex + compiled PDF
├── figures/             Fig. 1–2 PNG + generators
├── audit/               SCIENTIFIC_LOCKS.md + CHANGELOG_P0.md
└── reproducibility/     how_to_reproduce.md + BASELINE_MANIFEST.txt
```

Hashes: `reproducibility/BASELINE_MANIFEST.txt`.

Some files under `results/tables/` are older pipeline traces. They must not overwrite the locked printed cells above.

## Rules from this freeze onward

1. **Do not change a printed number** without a new script output and an obsolete mark on the old cell.
2. **Do not “beautify” results** (no rounding to look nicer, no silent series swap).
3. **Do not add GNN / SSL / MCP / path / distillation** to Contribution, Method, Experiments, or Results.
4. **Do not score GKT / CL4KT** or bring them back into main tables.
5. **Every new result must trace** to a script path and an output file in `results/` or `supplementary/`.
6. **Do not overwrite** `manuscript/main_ijiet_blind.pdf` or `manuscript/BASELINE_main_ijiet_blind.pdf`.

## Rebuild without retraining

`scripts/rebuild_locked_tables.sh` (or `.ps1`) verifies ASSISTments T-KT ECE 0.1136 / 0.2280 from frozen summaries and writes SI S8–S9. It does not retrain.  
`scripts/reproduce_one_dataset.sh` retrains local IRT/DKT/T-KT and does **not** recreate those locked cells.

## History before this freeze

See `audit/CHANGELOG_P0.md` (rows 1–16), including official SimpleKT Assist ECE, S8–S9, and Table 9 XES a2b alignment.
