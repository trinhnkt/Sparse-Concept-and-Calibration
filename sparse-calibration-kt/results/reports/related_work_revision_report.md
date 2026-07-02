# Related Work Revision Report

**Date:** 2026-06-13  
**Status:** ✅ Completed

---

## 1. Restructuring of Section II
Section II has been systematically expanded and restructured into 5 required subsections:
1.  **II.A. Knowledge Tracing Models and Benchmarking:** Establishes the KT task, standard sequential baselines (BKT, IRT, DKT, DKVMN, AKT, SimpleKT), and benchmarking tools like pyKT. Ends by confirming we do not propose a new architecture but focus on diagnostic evaluation of these baselines.
2.  **II.B. Graph-Augmented Knowledge Tracing:** Discusses graph-based and contrastive models (GKT, GIKT, CL4KT). Ends by connecting to the paper: these complex models require robust calibration and sparse-strata evaluation to prevent leakage.
3.  **II.C. Sparse and Cold-start Knowledge Components:** Clearly distinguishes between traditional user/item cold-start in Recommender Systems and KC-level sparsity in KT. Relates directly to P0's sparse-bucket stratification (very sparse, sparse, medium, dense) to prevent overall AUC from hiding local degradation.
4.  **II.D. Calibration of Probabilistic Predictions:** Details why high-AUC models can be poorly calibrated. Explains ECE and Brier score decomposition. Connects to P0 by explaining that we report these metrics explicitly across KC-frequency strata.
5.  **II.E. Reproducibility, Leakage Control, and Statistical Testing:** Covers data leakage vectors (split, preprocessing, KC mapping, sparse-bucket, calibration, etc.). Mentions DeLong and Wilcoxon tests, with appropriate hedging indicating that statistical tests are only used where paired prediction-level outputs permit.

---

## 2. New Verified References Added
All new references were meticulously verified for accurate authors, titles, venues, and years:
*   `lee2022cl4kt`: Contrastive learning for knowledge tracing (Lee et al., WWW 2022)
*   `kapoor2023leakage`: Leakage and the reproducibility crisis in machine-learning-based science (Kapoor & Narayanan, Patterns 2023)
*   `wilcoxon1945individual`: Individual comparisons by ranking methods (Wilcoxon, 1945)
*   `nakagawa2019graph`: Graph-based knowledge tracing (GKT)
*   `yang2021gikt`: GIKT (Yang et al., ECML PKDD 2021 — noted as 2021 formally)
*   `naeini2015obtaining`: Bayesian binning / ECE (Naeini et al., AAAI 2015)
*   `guo2017calibration`: Calibration of Modern Neural Networks (Guo et al., ICML 2017)
*   *Other foundational papers for Brier, DeGroot, DeLong, IRT (Rasch, Embretson) were also verified and included.*

---

## 3. Unverified References (Excluded)
The following references were **not** added to the manuscript or `references.bib` due to failed verification. They have been logged in `results/reports/related_work_references_to_verify.md`:
*   **DECKT (Bai et al., Entropy 2025):** Not verifiable on major academic indexes.
*   **Pelánek (2020):** While Pelánek 2015 is verified and cited, a specific 2020 calibration paper could not be uniquely confirmed.

---

## 4. Constraint Confirmations
*   ✅ **No Experimental Data Changed:** Tables, figures, and experimental numbers remain untouched.
*   ✅ **Scope Preserved:** The text consistently uses hedging (e.g., "we focus on diagnostics rather than proposing a new architecture") and maintains the spirit of a protocol/diagnostic paper.
*   ✅ **BibTeX Keys Consistent:** Existing keys were reused; new keys followed the requested pattern without duplicates. The `piech2015deep` year bug was fixed.
*   ✅ **Total References:** 25 references in total.

---
*Note: Local LaTeX compilation to `P0_related_work_expanded.pdf` could not be executed because `pdflatex` / `latexmk` are not installed in the current Windows environment. The `.tex` and `.bib` files are fully updated and ready for compilation on an environment with a TeX distribution.*
