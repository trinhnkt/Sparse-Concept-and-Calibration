# Metric Instability vs Performance Degradation Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/04_experiments.tex` (Results: RQ1)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to clearly decouple **true predictive performance degradation** (where the model is intrinsically weaker on low-frequency concepts) from **metric instability** (where statistical small-sample size issues cause the metrics to fluctuate widely). 

---

## 2. Key Clarifications Integrated
1. **Defined the Dual Phenonema:**
   - **True Performance Degradation:** Highlighted that sparse KCs represent more challenging learning trajectories, making it physically harder for deep sequences to converge on high-quality embeddings.
   - **Metric Instability:** Explicitly linked the extremely high standard deviations (and seemingly high AUC values in very sparse strata) to small sample-size constraints (e.g., as few as 3 to 10 events per seed).

2. **Formulated Cautious Interpretation Guidelines:**
   - Warned against over-interpreting any sparse bucket results without active consultation of the accompanying event counts.
   - Grounded the number of KCs and interaction events as **compulsory diagnostic context** rather than auxiliary metadata.
   - Utilized cautious language ("may", "under our experimental conditions", "sample-size-aware") to satisfy peer-review rigor.
