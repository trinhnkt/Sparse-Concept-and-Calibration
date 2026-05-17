# 📄 LATEX DOCUMENT STRUCTURE AND FLOAT ORDERING REPORT

## 1. Executive Summary
This report documents the structural optimization of the `P0` manuscript (`paper/main.tex` and related section files) to ensure absolute alignment with IEEE standard templates, logical placement of floats (tables and figures), and proper ordering of the appendix and bibliography sections.

All modifications have been completed and verified, achieving a perfect, professional journal-style layout.

---

## 2. Completed Layout Optimizations

We implemented three specific structural enhancements to solve float drifting and improve visual readability:

### 2.1 Preamble Package Import
*   **Location:** [paper/main.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/main.tex#L22)
*   **Addition:** Added `\usepackage{placeins}` to gain precise control over LaTeX float rendering bounds.

### 2.2 Global Appendix and References Reordering
*   **Location:** [paper/main.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/main.tex#L89-L96)
*   **Action:** Moved the Appendix declaration and inputs **before** the bibliography:
    ```latex
    \appendices
    \input{appendix/appendix_a_sensitivity}

    \bibliographystyle{IEEEtran}
    \bibliography{references}
    ```
    This ensures that the References do not split the main body from the appendix, keeping the references as the absolute final section of the document.

### 2.3 Float Barrier Isolation (`\FloatBarrier`)
To prevent large double-column tables from floating excessively far from their reference text (especially in the Appendix and RQ3), we inserted strict float barriers:
1.  **Cold-start Results (Table VI):**
    *   **Location:** [paper/sections/04_experiments.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/sections/04_experiments.tex#L89)
    *   *Effect:* Keeps Table VI positioned strictly adjacent to the RQ3 cold-start analysis, preventing it from drifting into Section 4.5 or the main Discussion.
2.  **Sensitivity Analysis (Table VII):**
    *   **Location:** [paper/appendix/appendix_a_sensitivity.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex#L5)
    *   *Effect:* Holds Table VII within the bounds of the Appendix A1 Threshold Sensitivity section.
3.  **Comprehensive Temporal Splits (Table VIII & IX):**
    *   **Location:** [paper/appendix/appendix_a_sensitivity.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex#L11)
    *   *Effect:* Keeps the full temporal overall performance and strata performance tables locked within Appendix A2, preventing them from bleeding into the references.

---

## 3. Visual and Structural Verification
*   **Table VI (Cold-start):** Positioned near RQ3 section.
*   **Table VII (Threshold Sensitivity):** Stays inside Appendix A.
*   **Table VIII & IX (Full Temporal splits):** Stays inside Appendix A.
*   **References:** Placed at the very end of the paper.
