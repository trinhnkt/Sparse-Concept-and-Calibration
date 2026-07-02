# BKT Smoothing Sanity Report

- Adding smoothing prior did not resolve the issue. pyBKT 1.4.1 has a division-by-zero bug in the M-step that still triggers or causes parameters to stick at initialization.
- Probability output remains heavily saturated near 0.0.
- AUC remains exactly 0.5000.
