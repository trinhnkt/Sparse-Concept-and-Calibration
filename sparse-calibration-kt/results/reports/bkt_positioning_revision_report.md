# BKT Positioning Revision Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/04_experiments.tex` (Baseline Implementations)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to refine the baseline positioning of Bayesian Knowledge Tracing (BKT). Because BKT models often suffer from parameter saturation (slip/guess converging to extreme boundaries under EM on small cohorts), their probability predictions quickly become deterministic (0 or 1). Reporting BKT ECE or Brier scores as if they represent standard soft probabilistic miscalibration would mislead reviewers. We repositioned BKT to act as a **classical baseline reference** rather than a primary calibration baseline.

---

## 2. Integrated Positioning Details
1. **Identified BKT as a Reference:**
   - Framed BKT explicitly as a classical benchmark.
   - Instructed readers to interpret its extremely high ECE/Brier scores as a **diagnostic warning** (symptom of parameter saturation and binary prediction collapse) rather than a competitive calibration score.
   - Focused the main calibration degradation analysis of RQ2 on deep, representation-based sequential baselines (DKT and SimpleKT), which produce softer, more continuous probability estimates.

2. **Maintained Academic Footnote:**
   - Retained the mathematically rigorous footnote in Table V clarifying the EM saturation effect and binary convergence of MAE, ECE, and Brier.
