# Design Principles Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/03_protocol.tex` (Design Principles)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to introduce a formal **"Design Principles"** subsection (Section III.G) to ground the diagnostic protocol mathematically and operationally. This makes the paper read as a high-quality methodological contribution, rather than a simple benchmarking paper.

---

## 2. Core Principles Integrated
We have formalized four core design principles that govern the protocol:

1. **P1. Train-only Definitions:** 
   - *Rationale:* Ensures that all KC frequency bucketing and cold-start classifications utilize *only* training-fold data.
   - *Impact:* Prevents sparse-bucket leakage, wherein future/testing information pollutes the pipeline.

2. **P2. Prediction-level Export:** 
   - *Rationale:* Decouples model execution from evaluation metrics by exporting prediction-level CSV files containing predicted probabilities and true labels.
   - *Impact:* Guarantees post-hoc calculation alignment and immune system scoring, enabling independent, plug-and-play evaluation of future baselines.

3. **P3. Sample-size-aware Interpretation:** 
   - *Rationale:* Mandates reporting strata performance alongside the active number of KCs and interaction events.
   - *Impact:* Provides essential statistical context to distinguish true predictive degradation from simple metric instability due to small sample constraints.

4. **P4. Leakage-audited Reporting:** 
   - *Rationale:* Requires that every result is explicitly paired with a leakage audit status.
   - *Impact:* Enforces strict evaluation hygiene across all evaluation steps.
