# Calibration vs Discrimination Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/03_protocol.tex` (Calibration Metrics)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to clearly explain the mathematical and pedagogical difference between **discrimination** (measured by AUC) and **calibration** (measured by ECE and Brier score), and why this distinction is critical for downstream student-facing decisions.

---

## 2. Integrated Discussion Details
We have integrated a rigorous paragraph under Section III.D detailing:
1. **Discrimination (AUC):** Measures the relative pairwise ranking ability of the model (does the model place correct student responses above incorrect ones?).
2. **Calibration (ECE/Brier Score):** Measures the absolute correctness of predicted probability outputs (does a confidence of 80% correspond to 80% empirical correctness?).
3. **Pedagogical Impact:** Grounded this in educational decision support where absolute probability thresholds are used to:
   - Trigger automated remediation.
   - Assign additional practice problems.
   - Gate or license student concept advancement.
4. **Warning on Miscalibration:** Explained that a model with high AUC but poor calibration can lead to inappropriate or biased instructional interventions.
