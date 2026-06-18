# BKT Parameter Saturation Report

- `learns` typically saturates at 1.0.
- `guesses` and `slips` stick at initialization (0.50).
- `prior` occasionally becomes NaN due to divide-by-zero in pyBKT M-step.
- Output probability is saturated: > 86% of predictions are exactly 0.0 or 0.50.
