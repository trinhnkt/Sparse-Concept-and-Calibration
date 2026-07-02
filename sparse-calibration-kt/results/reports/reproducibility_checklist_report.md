# Reproducibility Checklist Report

**Date:** May 17, 2026  
**Section Revised:** `paper/main.tex` (Artifact Availability)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to introduce a comprehensive, itemized **"Reproducibility Checklist"** inside the `Artifact Availability` section. Since this study advocates strongly for reproducibility and rigorous diagnostic pipelines, providing a clear checklist gives reviewers absolute confidence in the availability and structural cleanliness of the released codebase.

---

## 2. Checklist Items Integrated
The checklist details ten distinct, key software components prepared for release upon paper acceptance:
1. **Dataset Preprocessing:** Scripts normalizing raw logs to standard schema.
2. **Split Construction:** Reproducible fold logs and multi-seed split constructors.
3. **Prediction-level Exports:** Standardized raw predictions for downstream decoupling.
4. **KC-Strata Assignment:** Dynamic, train-only frequency bucketing.
5. **Calibration Verification:** Clean Expected Calibration Error calculations.
6. **Brier Decomposition:** Mathematical equations tracking Uncertainty, Reliability, and Resolution.
7. **Reliability Diagrams:** Scripts mapping reliability curves per frequency stratum.
8. **Leakage Audit:** Verifiable, automated test logs checking channels L1--L7.
9. **LaTeX Table Exporters:** Automated Python scripts generating clean booktabs tables.
10. **One-Command Reproduction:** Unified execution scripts wrapping all pipeline steps.
