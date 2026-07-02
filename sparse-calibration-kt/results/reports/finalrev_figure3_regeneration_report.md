# Figure 3 Regeneration Report

## Status
The reliability diagram for SimpleKT on Junyi temporal split has already been successfully regenerated using the post-correction prediction outputs (from the T8 rerun). 

## Output Files
The new figures reside in `paper/figures/`:
- `junyi_temporal_simplekt_dense.pdf`
- `junyi_temporal_simplekt_very_sparse.pdf`

The script `make_updated_figures.py` pulled from the latest updated `predictions_rerun` directories. Consequently, Figure 3 reflects the newly corrected ECE and Brier metrics for Junyi Academy temporal predictions. No stale data warnings are required.
