# Temporal Split Debug Report

## 1. Files Inspected
- Data splits in `data/processed/*/temporal/fold1/`
- Data loaders and runner scripts (`baseline_runner.py`)

## 2. Temporal Ordering Audit
- Checked ASSISTments fold 1.
- No temporal ordering bug found. `max_train_time < min_test_time` holds for all learners.

## 3. Label Distribution Audit
- XES3G5M exhibits a SEVERE label shift (train ~0.56, test ~0.80). This naturally degrades temporal evaluation.

## 4. Sequence Handling Audit
- Misalignment bug previously caused AUC to drop to ~0.50.
- The bug was found to be a **Prediction-Label Misalignment** and was already fixed in `baseline_runner.py`.

## 5. Final Conclusion
**TEMPORAL_SEQUENCE_ALIGNMENT_BUG_FOUND** (and already fixed).
