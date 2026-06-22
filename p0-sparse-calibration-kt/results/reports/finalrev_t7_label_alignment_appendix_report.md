# T7 Label Alignment Appendix Report

## Status
Completed adding Appendix F detailing the temporal alignment audit.

## Files Updated
- `paper/appendix/appendix_a_sensitivity.tex` (appended the new section here as it holds all appendices)

## Changes Made
- **Appendix F Added:** Created the section "Prediction--Label Alignment Audit for Temporal Splits". It thoroughly explains the transient row order vs stable instance identifier issue, how it was detected (near-random AUC on warm cohorts despite IRT baseline performance), and the two sanity checks used (warm-cohort AUC floor and prediction-label correlation).
- **Cross-Referencing:** Ensured `04_experiments.tex` properly references this new appendix using `Appendix~\ref{app:alignment}` when mentioning the label-alignment correction.
