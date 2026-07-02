# Failed / Skipped Jobs Report

Out of 90 total planned experimental runs, 34 runs were marked as failed/skipped by design:

1. **Learner-Based Splits Folds 3 & 4 (18 runs)**:
   - Affected runs: All models (`irt_1pl`, `dkt`, `simplekt`) across all datasets (`assist2012`, `junyi`, `xes3g5m`) with seeds `2026` and `2027`.
   - Reason: These folds do not exist in the processed dataset structure, as the learner-based evaluation splits are limited to 3 folds (Fold 0, 1, 2).

2. **Temporal Split Neural Model Seeds 2024, 2025, 2026, 2027 (16 runs)**:
   - Affected runs: `dkt` and `simplekt` on `junyi` and `xes3g5m` for seeds `2024`, `2025`, `2026`, `2027`.
   - Reason: Skipped by design to respect environment limits because no pre-existing cached prediction files were available, and training neural models from scratch on these large datasets (Junyi and XES3G5M) requires substantial compute.

