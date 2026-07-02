# Split Rationale Revision Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/04_experiments.tex` (Experimental Setup)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to clarify the **split rationale** across the entire evaluation matrix, ensuring that the usage of learner-based and temporal splits is clean, logical, and structurally distinct.

---

## 2. Split Partitioning & Rationale
We explicitly documented and structured the partitioning as follows:

1. **Learner-based Splits (Tables III, IV, V):**
   - *Rationale:* Tests generalization to completely unseen student cohorts (the standard KT deployment setting) while preserving the absolute maximum number of interaction counts in sparse buckets.
   - *Active Usage:* Formulates the main baseline performance and calibration breakdown tables.

2. **Temporal Splits (Table VI, Figure 3, Appendix B):**
   - *Rationale:* Tests generalization to future concept states (stress-testing), forcing models to forecast masteries under extreme timeline shifts and cold-start conditions.
   - *Active Usage:* Formulates the reliability diagrams and cold-start diagnostics tables.
