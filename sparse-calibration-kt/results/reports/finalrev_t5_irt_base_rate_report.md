# T5 IRT Base-Rate Explanation Report

## Status
Completed the explanation of the IRT base-rate predictor behavior as requested in T5.

## Files Updated
- `paper/sections/04_experiments.tex`
- `scripts/make_updated_latex_tables.py` (which updates `table_v_calibration_by_bucket_updated.tex`, `table5_calibration_per_bucket.tex`, `table_v_calibration_with_reliability.tex`, etc.)

## Changes Made
- **RQ2 Text Addition:** Added a paragraph explicitly noting that while IRT exhibits very low ECE on dense strata, its RES = 0 and learner-based AUC = 0.50. It correctly explains this is the signature of a base-rate predictor predicting close to the global correctness rate for unseen learners, illustrating why calibration must be interpreted jointly with resolution and discrimination.
- **Table Note Update:** Updated the Note below Table V / Table X to explicitly state: "IRT shows low ECE in several learner-based cohorts, but RES = 0 across strata indicates base-rate-like behavior with no resolving power. Thus, IRT calibration should be interpreted jointly with AUC and Brier resolution."
