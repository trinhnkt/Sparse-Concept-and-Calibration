# Statistical Uncertainty Revision Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/04_experiments.tex` (Experimental Setup) and `paper/sections/05_discussion_limitations.tex` (Limitations)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to explicitly address **statistical uncertainty** and **seed-level variability** to satisfy rigorous peer-review expectations. By detailing the seeds, how standard deviations are formatted, and warning against overclaiming baseline superiority, we ensure high mathematical credibility.

---

## 2. Integrated Statistical Grounding Details
1. **Reporting standard deviations:**
   - Documented that all reported metrics in our tables (Table III, IV, V, VI, etc.) represent the mean $\pm$ standard deviation across random seeds (specifically, seeds 42, 43, 44, 2024, and 2025).
   - Indicated that reporting seed-level variability is essential to prevent over-interpreting minor single-run differences, particularly in sparse strata.

2. **Repositioning BKT's standard deviation:**
   - Explained that BKT's deterministic outputs under EM parameter saturation have negligible seed-level variation.

3. **Academic humility in baseline comparison:**
   - Explicitly stated in the limitations that while we report seed-level variations, we make no strong claims of statistical superiority among baselines, as the rankings remain highly baseline-dependent and dataset-dependent.
