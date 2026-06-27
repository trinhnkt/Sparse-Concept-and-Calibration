# Table B2 Layout Fix Report

- **Source File:** `tables/tableA_overall_full.tex`
- **Issue Investigated:** The "sticky numbers" (e.g., `0.59130.69080.60490.4563`) were caused by a previous regex replacement that corrupted the `&` delimiters when attempting to enforce `tabular*`.
- **Action Taken:** 
  - Completely rewrote the table using the `tabularx` package to explicitly enforce the A4 layout.
  - Re-inserted all missing `&` column separators.
  - Used `\large` for legibility.
  - Defined a custom column type `\newcolumntype{Y}{>{\centering\arraybackslash}X}` to evenly space the numerical columns across the page without stripping spaces.
- **Verification:** All numbers now perfectly align under their respective columns (AUC, ACC, NLL, RMSE). The exact values requested by the user are preserved intact.
