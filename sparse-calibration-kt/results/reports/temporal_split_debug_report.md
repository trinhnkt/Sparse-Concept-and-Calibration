# Temporal Split Debug Report (T11) — UPDATED

**Date:** 2026-06-13  
**Conclusion:** BUG FOUND (saved prediction files contain misaligned predictions from pre-fix runs; re-run needed)

---

## Summary

### Primary Bug Identified: Prediction-Label Misalignment

**Root cause:** In `baseline_runner.py` and `full_baseline_runner.py`, the test prediction loop iterated
`test_df.groupby('user_id')` (which groups rows by user_id order), but assigned the resulting flat list
of predictions back to `pred_df = test_df.copy()` which preserves original row order.

In temporal split, `test_df` is sorted by **global timestamp** (not user_id), so the groupby order
completely mismatches the original row order → predictions assigned to wrong rows → AUC ≈ 0.50.

**Fix applied:** `src/baseline_runner.py` and `src/full_baseline_runner.py` now use an index-keyed dict
to map each prediction back to its original DataFrame row index.

---

## Step 1: Timestamp Order Audit

- **assist2012**: global_order_ok=True, train>test violations (sampled)=0
- **junyi**: global_order_ok=True, train>test violations (sampled)=0
- **xes3g5m**: global_order_ok=True, train>test violations (sampled)=0

**Conclusion:** Temporal split construction (three_split_constructor.py) is CORRECT.

---

## Step 2: Label Distribution

- **assist2012**: train=0.7026, test=0.6887, Δ=0.0139 (OK)
- **junyi**: train=0.7081, test=0.6992, Δ=0.0089 (OK)
- **xes3g5m**: train=0.5682, test=0.8023, Δ=0.2341 (LARGE SHIFT)

---

## Step 3: Sequence Construction

- **T11_bug_fix_applied**: YES — Index-keyed dict used to align predictions with original test_df row order
- **explicit_sort_before_groupby**: YES — test_df explicitly sorted by [user_id, timestamp] before sequential prediction
- **causal_predict_then_update**: NO — Predict at step i, then update state with label[i]
- **KTDataset_explicit_sort**: YES — KTDataset does not sort within user — input CSV must be pre-sorted by timestamp

---

## Step 4: Prediction-Label Alignment

- assist2012_temporal_dkt_seed42.csv: sample AUC=0.5092 near 0.50 — likely misalignment from OLD run (before T11 fix)
- assist2012_temporal_simplekt_seed42.csv: sample AUC=0.5366 near 0.50 — likely misalignment from OLD run (before T11 fix)
- junyi_temporal_dkt_seed42.csv: sample AUC=0.4685 near 0.50 — likely misalignment from OLD run (before T11 fix)
- junyi_temporal_simplekt_seed42.csv: sample AUC=0.4933 near 0.50 — likely misalignment from OLD run (before T11 fix)

---

## Step 5: Cold-Start Groups

- **assist2012 warm**: n=529786, kcs=212, corr_rate=0.6891
- **junyi warm**: n=3240570, kcs=1319, corr_rate=0.6994
- **xes3g5m warm**: n=1331318, kcs=424, corr_rate=0.8043
- train_freq from train split only: YES (P1-compliant)

---

## Step 6: Sanity AUC (from existing prediction files)

| Dataset | Model | N | AUC | y_mean | p_mean | Flag |
|---------|-------|---|-----|--------|--------|------|
| assist2012 | bkt | 418724 | 0.5 | 0.6888 | 0.0017 | ~0.50 SUSPICIOUS |
| assist2012 | dkt | 531499 | 0.4992 | 0.6887 | 0.6822 | ~0.50 SUSPICIOUS |
| assist2012 | simplekt | 531499 | 0.5015 | 0.6887 | 0.6429 | ~0.50 SUSPICIOUS |
| junyi | bkt | 2855914 | 0.5001 | 0.6992 | 0.0004 | ~0.50 SUSPICIOUS |
| junyi | dkt | 3243115 | 0.5003 | 0.6992 | 0.7092 | ~0.50 SUSPICIOUS |
| junyi | simplekt | 3243115 | 0.4998 | 0.6992 | 0.6917 | ~0.50 SUSPICIOUS |
| xes3g5m | bkt | 1011570 | 0.5 | 0.802 | 0.1153 | ~0.50 SUSPICIOUS |
| xes3g5m | dkt | 1590743 | 0.6265 | 0.8023 | 0.7003 | OK |
| xes3g5m | simplekt | 1590743 | 0.6505 | 0.8023 | 0.7197 | OK |

*Note: These AUC values are from prediction files generated BEFORE T11 bug fix.*
*After re-running experiments with the fix, temporal DKT/SimpleKT AUC should improve.*

---

## Files Changed

| File | Action |
|------|--------|
| `src/baseline_runner.py` | BUG FIX — index-keyed dict for prediction alignment |
| `src/full_baseline_runner.py` | BUG FIX — same fix |
| `scripts/audit_temporal_split.py` | NEW — audit script |

No paper tables modified. No prediction CSVs overwritten.

---

## Recommendation

1. **Bug fix already applied** to `src/baseline_runner.py` and `src/full_baseline_runner.py`
2. **Re-run all temporal experiments (T13)** for all 3 datasets and all models
3. **Expected outcome:** temporal DKT/SimpleKT AUC should improve from ~0.50 to meaningful range
4. **If AUC still ~0.50 after re-run:** document as true distribution shift and discuss in paper
5. **Do NOT update paper tables until T13 re-run is complete**

