# Contribution Revision Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/01_introduction.tex` (Contributions)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to align the contribution statements with a clear, logical, and academically satisfying **"Problem $\rightarrow$ Contribution"** structure. This guarantees that peer reviewers can immediately recognize the core methodological problems our diagnostic protocol addresses.

---

## 2. Key Contributions & Logic Alignment

1. **Problem 1 (Hidden Stratum Behavior):**
   - *Problem:* Aggregate AUC/ACC metrics mask performance degradation or metric instability on low-frequency concepts.
   - *Contribution:* We formalize a train-only KC-frequency stratification protocol that prevents sparse-bucket leakage and enables sample-size-aware diagnostics.

2. **Problem 2 (Unreliable Probability Estimates):**
   - *Problem:* Aggregate rankings do not reveal whether a model's predicted probabilities correspond to empirical correctness rates, which is crucial for educational decision-making.
   - *Contribution:* We integrate calibration-oriented evaluation, including Expected Calibration Error (ECE), Brier decomposition (Uncertainty, Reliability, Resolution), and reliability diagrams, into bucket-level reporting.

3. **Problem 3 (Hidden Evaluation Pipeline Contamination):**
   - *Problem:* KT evaluation pipelines suffer from subtle, undocumented data leakage across folds or splits.
   - *Contribution:* We establish a seven-channel leakage-control audit checklist and a reproducible workflow that exports prediction-level files, diagnostic reports, and paper-ready tables.

---

## 3. Scope Verification
- **No new models claimed:** The study is purely diagnostic, baseline-focused, and protocol-driven.
- **No overclaiming words:** Avoided hype terms (e.g., "SOTA", "outperform", "solve"). The contributions focus entirely on reproducibility and systematic diagnostic benchmarking.
