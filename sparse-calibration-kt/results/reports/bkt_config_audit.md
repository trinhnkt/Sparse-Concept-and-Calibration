# BKT Configuration Audit Report

**Date:** 2026-06-13  
**pyBKT version:** 1.4.1  
**Status:** ❌ DEGENERATE — BKT cannot be fixed with available pyBKT API

---

## 1. pyBKT Version and Setup

| Item | Value |
|------|-------|
| Library | pyBKT |
| Version | 1.4.1 |
| Source | pip install pyBKT |
| Model class | `pyBKT.models.Model` |
| Default num_fits | 5 |
| Default parallel | True |

---

## 2. Default Configuration Used in Paper

In `src/baseline_runner.py` and `src/full_baseline_runner.py`:

```python
bkt = BKTModel(seed=seed)
bkt_train = train_df[['user_id', 'kc_id', 'correct']].copy()
bkt_train['skill_name'] = bkt_train['kc_id'].map(lambda x: f"skill_{kc_map[x]}")
bkt_train = bkt_train[['user_id', 'skill_name', 'correct']]
bkt.fit(data=bkt_train)  # default num_fits=5, no fixed params, no smoothing
preds_dict = bkt.predict(data=bkt_test)
p_pred = preds_dict['correct_predictions'].values
```

**Issues identified:**
- No `fixed=` parameter → prior initialization uses EM soft counts → divide-by-zero on sparse data
- No `num_fits=1` constraint → 5 restarts all produce NaN prior
- No `manual_param_init` or bounds on parameters
- No smoothing or regularization in EM (pyBKT 1.4.1 does not expose these directly)

---

## 3. EM Saturation Analysis

### 3.1 The divide-by-zero root cause

In `pyBKT/fit/M_step.py` line 61:
```python
model['pi_0'] = init_softcounts[:] / np.sum(init_softcounts[:])
```

When `init_softcounts = [0, 0]` (no initial responses in E-step), `np.sum = 0` → `NaN`.

This occurs when **every user's sequence starts with a NaN mastery state** (because there is no "prior response" to initialize the HMM from), which is extremely common in sparse educational datasets.

### 3.2 Observed parameters after fit (assist2012, 50k interactions)

| Parameter | Mean | Std | Min | Max | Notes |
|-----------|------|-----|-----|-----|-------|
| prior | NaN | — | NaN | NaN | ❌ ALL NaN — root cause of failure |
| learns | 1.000 | 0.000 | 1.000 | 1.000 | ❌ Saturated at max |
| guesses | 0.500 | 0.000 | 0.500 | 0.500 | ❌ Did not converge from init |
| slips | 0.500 | 0.000 | 0.500 | 0.500 | ❌ Did not converge from init |
| forgets | 0.000 | 0.000 | 0.000 | 0.000 | Fixed at 0 (default) |

### 3.3 Fixes attempted and their outcomes

| Fix | Method | Result |
|-----|--------|--------|
| `manual_param_init` | Set prior=0.5, learns=0.3, guesses=0.2 | ❌ FAILED — NaN persists |
| `fixed={'skill': {'prior': 0.5}}` | Fix prior via fixed= arg | ⚠️ PARTIAL — prior no longer NaN, but learns=1.0, unique p_pred=2 |
| Top-20 KCs only (max data) | Restrict to densest KCs | ❌ FAILED — same saturation pattern |
| All three combined | fixed prior + manual_param_init + top KCs | ❌ FAILED — AUC=0.50, p_pred={0,0.5} only |

---

## 4. BKT Fit on Train Only (Leakage Check)

✅ **BKT is fit on train split only** — no leakage.

```python
bkt.fit(data=bkt_train)   # only train_df rows
preds_dict = bkt.predict(data=bkt_test)  # predict on test_df rows
```

The EM saturation issue is not caused by data leakage.

---

## 5. Max EM Iterations

pyBKT 1.4.1 does not expose a `max_iter` parameter directly.  
The default behavior uses internal convergence criteria (not documented in public API).  
In practice, with sparse data, EM converges in 1–2 iterations because parameters hit boundaries immediately.

---

## 6. Initialization

pyBKT 1.4.1 initializes parameters randomly via `seed=` argument.  
Multiple restarts (`num_fits=5`) are used to find the best EM solution.  
With sparse data, **all restarts fail identically** because the M-step divide-by-zero occurs regardless of initialization.

---

## 7. Conclusion

BKT via pyBKT 1.4.1 is **fundamentally incompatible** with the sparse educational datasets in this study.  
The EM saturation bug cannot be patched without modifying pyBKT internals.  
The library does not expose smoothing, Laplace correction, or parameter constraints via public API.

**Decision: REPLACE WITH IRT 1PL** (see `classical_baseline_decision_report.md`).
