# JEDM Author-Year Citation Final Fix Report

## Overview
This report summarizes the modifications made to transition the manuscript to the JEDM author-year citation format and the successful compilation of the final PDF using Tectonic (a modern, robust XeTeX/BibTeX engine).

## Tasks Completed

### 1. Citation Grammar Fixes (`\citep` and `\citet`)
- All occurrences of `\cite{...}` were converted to `\citep{...}` across all `.tex` files to correctly render parenthetical citations (e.g., *(Corbett and Anderson, 1994)* instead of *[1]* or incorrect narrative forms).
- The narrative citation in `02_related_work.tex` was explicitly rephrased:
  **Old:** "The introduction of Deep Knowledge Tracing (DKT) \citep{piech2015deep} shifted..."
  **New:** "\citet{piech2015deep} introduced Deep Knowledge Tracing (DKT), shifting..."

### 2. Bibliography Order (Alphabetical via BibTeX)
- Restored `main_jedm.tex` and `main_jedm_anonymous.tex` to natively use JEDM's BibTeX pipeline:
  ```latex
  \bibliographystyle{acmtrans}
  \bibliography{references}
  ```
- This allows `acmtrans.bst` to natively resolve citations and automatically sort the References section alphabetically by the first author's last name, complying with JEDM guidelines.

### 3. Updating Table 5 Interpretations in `04_experiments.tex`
- The conclusion drawn from Table 5 regarding medium and sparse strata was updated to reflect non-monotonic, heterogeneous degradation rather than a simplistic "lower performance" claim.
  **New text:** *"In contrast, medium and sparse strata do not show a simple monotonic AUC degradation pattern; instead, they exhibit heterogeneous behavior, including higher AUC in some strata but worse calibration, larger NLL/RMSE, or sample-size-sensitive instability. This supports our central point that aggregate AUC alone is insufficient for diagnosing KT reliability."*

### 4. Final Compilation
- The project was compiled using **Tectonic** (a self-contained LaTeX/BibTeX engine) to ensure the complete `LaTeX -> BibTeX -> LaTeX -> LaTeX` toolchain executed flawlessly.
- **Verification Checks Passed:**
  - No undefined references (`Citation ??`, `Figure ??`, `Table ??`).
  - Author-year citations render perfectly.
  - References are sorted alphabetically without losing DOI links.
  - Figure 2, Figure 3, and Table 10 were verified untouched and completely preserved.
  - Experimental results remain unchanged.

## Outputs
- Final Compiled PDF: `paper/JEDM_P0_FINAL_AUTHOR_YEAR_CITATION_FIXED.pdf`
- Anonymized Draft is also ready to be compiled if needed using the same setup.
