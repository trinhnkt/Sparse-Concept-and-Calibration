# T3 Threats to Validity and Conclusion Update Report

## Status
Completed the update for Threats to Validity and Conclusion sections to integrate the temporal alignment findings.

## Files Updated
- `paper/sections/05_discussion_limitations.tex`
- `paper/sections/06_conclusion.tex`

## Changes Made
- **Internal Validity:** Appended `(which motivated the explicit temporal alignment audit described below)` to the mention of sequence-label alignment errors.
- **Temporal Alignment Validity:** Added a new dedicated bullet point under Threats to Validity, explaining that the temporal-split audit identified a prediction-label alignment issue. The text clarifies that this was detected via warm-cohort AUC and prediction-label correlation checks, and justifies why temporal cold-start results must be interpreted alongside sanity checks.
- **Conclusion:** Added a final summarizing sentence stating: `More broadly, our temporal-split audit shows that cold-start diagnostics should be accompanied by warm-cohort and prediction--label sanity checks to distinguish genuine concept-level cold-start failure from alignment artifacts.`
