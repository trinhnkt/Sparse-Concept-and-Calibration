# T10 L8 Predictive Sanity Check & Figure 1 Report

## Status
Completed adding L8 to the Leakage Audit Checklist. Figure 1 requires a manual update by the authors.

## Files Updated
- `paper/tables/table1_leakage_audit.tex`
- `paper/sections/03_protocol.tex`
- `paper/sections/01_introduction.tex`
- `paper/sections/06_conclusion.tex`
- `paper/main.tex`
- `paper/main_submit_candidate.tex`

## Changes Made
- **Table I (Leakage Audit Checklist):** Added a new row for `L8`: "Predictive sanity check" with the description "Warm-cohort AUC vs static reference" under `temporal_audit.py`.
- **Text Alignment:** Replaced all instances of "seven-channel" (or "seven-channel leakage checklist (L1--L7)") with "eight-channel" (or "eight-channel leakage checklist (L1--L8)") across the abstract, introduction, protocol, and conclusion sections to ensure absolute consistency.
- **Figure 1 (Pipeline Diagram):** The file `paper/figures/figure1_pipeline.pdf` currently displays "strict/k-shot cold-start splits". As requested, this terminology should be updated to "strict/limited cold-start". However, the source vector graphics file (`.drawio`, `.ai`, or `.svg`) is not present in the repository. **Action Required by Authors:** Please manually edit the source file of Figure 1 to apply this text change and re-export `figure1_pipeline.pdf`.
