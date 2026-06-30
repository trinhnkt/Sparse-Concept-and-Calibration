# JEDM Final Submission: Three Major Formatting & Consistency Fixes Report

**Date:** June 30, 2026
**Target:** JEDM Upload Folder (`jedm_upload_folder/`)

This report documents the three final major groups of fixes implemented to ensure the LaTeX manuscript fully complies with the Journal of Educational Data Mining (JEDM) formatting and submission guidelines, both for the camera-ready version and the double-blind anonymous version.

---

## 1. Structural Ordering and Typographical Fixes

### 1.1. JEDM Template Backmatter Ordering
*   **Issue:** The template strictly requires the backmatter to follow a specific sequential order, but the sections were previously scrambled, with the Appendix improperly placed before the References.
*   **Action:** Restructured both `main_jedm.tex` and `main_jedm_anonymous.tex` to rigorously follow the correct order:
    1.  `Declaration of Generative AI Software Tools in the Writing Process`
    2.  `Acknowledgements` (and `ORCID` in the non-anonymous version)
    3.  `References` (`\input{references.bbl}`)
    4.  `Appendix` (Placed at the very end using `\appendix`)

### 1.2. Cross-referencing and Hyphenation
*   **"Appendix Appendix" Bug:** Removed hardcoded `Appendix~` prefixes in the main text's `\ref{}` calls because the global `\gdef\thesection{Appendix \Alph{section}}` already automatically injects the word "Appendix" into the label, avoiding redundant rendering like "Appendix Appendix C".
*   **Title Hyphenation:** Removed a manual line-break (`\\`) in the title of Appendix E within `appendix_a_sensitivity.tex` that caused an ugly hyphenation artifact ("Insta-bility") when rendered by the JEDM class file.

---

## 2. Table Layout and Sizing Optimization

### 2.1. Splitting Table 5 (Cold-start Temporal)
*   **Issue:** The temporal cold-start table was a single massive tabular block that was visually dense and hard to parse within the JEDM margins.
*   **Action:** Maintained the single Table 5 (`tableorg`) environment to preserve numbering, but logically split the content into three separate `tabular` blocks corresponding to the three datasets: **(a) ASSISTments 2012**, **(b) Junyi Academy**, and **(c) XES3G5M**. The `Dataset` column was dropped from each to save space, significantly improving scannability.

### 2.2. Sizing Table 7 (Sensitivity Analysis)
*   **Issue:** Table 7 (`tableA1_sensitivity.tex`) was only 4 columns wide and lacked a `\resizebox` boundary, meaning it did not span the full text width symmetrically like the other tables.
*   **Action:** Wrapped the tabular inside `\resizebox{\textwidth}{!}{...}` to ensure it uniformly scales and aligns perfectly with the standard paper margins, ensuring a consistent typographical aesthetic across all tables.

---

## 3. Comprehensive Bibliography Standardization

### 3.1. BibTeX Polishing
*   **Issue:** The raw BibTeX output contained common academic formatting errors, including lowercased model acronyms, abbreviated conference names, truncated author lists (`and others`), and improperly rendered diacritics.
*   **Action:** Executed a global polishing script on `references.bib` fixing the following:
    *   **Acronym Preservation:** Enforced casing using `{}` brackets for `{simpleKT}`, `{pyKT}`, `{XES3G5M}`, `{GIKT}`, and `{DAS3H}`.
    *   **Author Expansions:** Replaced `and others` with full author lists for the XES3G5M and CL4KT benchmark papers to give proper attribution.
    *   **Conference Standardization:** Replaced abbreviated or track-specific names with the official conference proceedings names (e.g., ICLR, NeurIPS Datasets and Benchmarks Track, ECML PKDD).
    *   **Diacritic Correction:** Standardized accented characters for Pelánek (`Pel{\'a}nek, Radek`) and Choffin (`Choffin, Beno{\^\i}t`) to prevent rendering bugs (e.g., `Pelanek R ... ´`).

### 3.2. GitHub Artifact Availability
*   **Action:** Confirmed that the reproducible artifact link (`https://github.com/trinhnkt/P0`) is fully active in `main_jedm.tex`, and appropriately replaced with a placeholder in `main_jedm_anonymous.tex` to maintain strict double-blind anonymity requirements. All changes have been accurately documented in the repository's `README.md`.

---
**Status:** All JEDM LaTeX files compile cleanly with no unresolved references (`??`), and the GitHub repository has been synced with these final refinements. The manuscript is fully ready for submission.
