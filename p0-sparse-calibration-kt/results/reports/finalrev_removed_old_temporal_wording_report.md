# T9 Removed Old Temporal Wording Report

## Status
All instances of outdated claims regarding "near-random AUC" for Junyi Academy and XES3G5M under the warm cohort temporal split have been purged and updated. 

## Files Updated
- `paper/sections/04_experiments.tex`
- `scripts/make_updated_latex_tables.py` (which regenerates `table_vi_cold_start_temporal_updated.tex` and `table6_cold_start_results.tex`)

## Changes Made
- The text now correctly explains that deep KT baselines recover meaningful predictive signal on the warm cohorts, citing the updated AUCs (Junyi: ~0.6949-0.7129, XES3G5M: ~0.6573-0.6613).
- The term "dataset-specific temporal generalization challenges" was removed as requested since the difficulty was an alignment artifact, not a dataset-specific property.
- The distinction between strict cold-start (unseen KCs) and warm (seen KCs) is now correctly established.
