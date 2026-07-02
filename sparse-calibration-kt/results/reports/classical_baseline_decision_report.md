# Classical Baseline Decision Report (T12)

**Date:** 2026-06-13  
**Decision:** **REPLACE BKT WITH IRT 1PL** ✅

---

## 1. Current BKT Problem Summary

BKT via pyBKT 1.4.1 produces **completely degenerate predictions** on all three datasets:

| Dataset | Split | AUC | p_pred unique values | p_pred distribution |
|---------|-------|-----|---------------------|---------------------|
| assist2012 | learner_based | 0.5000 | 1–2 | 86% = 0.0, 14% = NaN |
| assist2012 | temporal | 0.5001 | 2 | 79% = 0.0, 21% = NaN |
| junyi | learner_based | 0.5000 | 1 | 89% = 0.0, 11% = NaN |
| junyi | temporal | 0.5001 | 2 | 88% = 0.0, 12% = NaN |
| xes3g5m | learner_based | 0.5000 | 2 | 68% = 0.0, 32% = NaN |
| xes3g5m | temporal | 0.5000 | 2 | 49% = 0.0, 36% = NaN |

All 22 BKT prediction files are degenerate (≤5 unique prediction values).

---

## 2. Evidence from Probability Audit (Step 1)

- **22/22 BKT files flagged DEGENERATE** (≤5 unique values)
- **p_pred ∈ {0.0, NaN}** across all datasets and splits
- **AUC = 0.5000 ± 0.0013** across all experiments (random classifier)
- **NLL = 23.7–28.0** (mathematically derived from 70–81% correct rate × log(ε) with ε=1e-15)
- **Brier = 0.69–0.90** (degenerate: Brier ≈ error rate since all predictions binary)

---

## 3. Evidence from Parameter/Config Audit (Steps 2 & 3)

### BKT Parameters (from subset fit, verified across all 3 datasets):

| Parameter | Mean | Expected Range | Status |
|-----------|------|----------------|--------|
| prior | NaN | [0.0, 1.0] | ❌ CRITICAL: divide-by-zero in M-step |
| learns | 1.000 | [0.0, 0.5] typically | ❌ Saturated at maximum |
| guesses | 0.500 | [0.1, 0.4] typically | ❌ Did not converge (stuck at init) |
| slips | 0.500 | [0.05, 0.3] typically | ❌ Did not converge (stuck at init) |
| forgets | 0.000 | [0.0, 0.1] | ✅ OK (fixed at 0) |

**Root cause:** `pyBKT/fit/M_step.py` line 61: `model['pi_0'] = init_softcounts[:] / np.sum(init_softcounts[:])` — divides by zero when `init_softcounts = [0, 0]`, yielding `prior = NaN`. All subsequent HMM forward passes fail.

### Config used:
- `num_fits=5` (default) — all 5 restarts fail identically
- No fixed parameters, no smoothing, no regularization
- pyBKT 1.4.1 does not expose Laplace smoothing or parameter bounds via public API

---

## 4. What Fixes Were Tried (Step 4)

| Fix | Code | Result |
|-----|------|--------|
| `manual_param_init` | `bkt.manual_param_init = {'prior': {s: 0.5}, ...}` | ❌ NaN persists |
| `fixed={'skill': {'prior': 0.5}}` | Fixed prior via API | ⚠️ Prior no longer NaN, but learns=1.0 and p_pred={0,0.5} |
| Restrict to top-20 densest KCs | Only KCs with >3000 train interactions | ❌ Same saturation |
| All three combined | fixed + manual_init + top KCs, num_fits=3 | ❌ AUC=0.50, 2 unique p_pred values |

**Conclusion: BKT cannot be fixed with pyBKT 1.4.1 on these datasets.**

---

## 5. Subset Results Before/After Fix Attempt

| Dataset | Split | Model | AUC | NLL | Brier | p_unique | Status |
|---------|-------|-------|-----|-----|-------|----------|--------|
| assist2012 | learner_based | BKT (original) | 0.5000 | 24.54 | 0.71 | 1 | ❌ Degenerate |
| assist2012 | temporal | BKT (original) | 0.5001 | 23.71 | 0.69 | 2 | ❌ Degenerate |
| assist2012 | learner_based | BKT fixed-prior | 0.5000 | — | — | 2 | ❌ Still degenerate |
| assist2012 | learner_based | **IRT 1PL** | **0.5000** | **0.613** | **0.211** | **many** | ⚠️ See note |
| assist2012 | temporal | **IRT 1PL** | **0.5913** | **0.605** | **0.208** | **7409** | ✅ Meaningful |

> **Note on IRT 1PL learner_based AUC=0.50:**  
> IRT 1PL uses only user and KC identity parameters. In learner_based split, test users are
> **disjoint** from train users (20% held-out users). IRT cannot predict for OOV test users
> (→ falls back to global mean for all of them → near-random ranking → AUC ≈ 0.50).
> This is expected behavior for learner-based splits, not a model bug.  
> For temporal split (same users, future interactions), IRT achieves AUC=0.5913 — clearly better than BKT.

---

## 6. Decision: **REPLACE WITH IRT 1PL**

### Rationale:
1. **BKT is unfixable** with the available pyBKT version — not a data issue but a library bug
2. **IRT 1PL** provides:
   - Continuous probability outputs (7409 unique values on temporal test)
   - Normal NLL range (0.61 vs 24.54 for BKT) 
   - Meaningful AUC on temporal split (0.59 vs 0.50 for BKT)
   - Theoretically grounded in educational measurement (Rasch model)
   - Train-only fit — no data leakage
3. **IRT 1PL is a well-established baseline** in educational data mining (Embretson & Reise, 2000; Lord, 1980)
4. **IRT 1PL limitations are well-understood** and documentable:
   - Cannot generalize to cold-start users (OOV → global mean) 
   - Does not model learning progression within session (static ability estimate)
   - This is a meaningful contrast with DKT/SimpleKT which do model progression

### What NOT to do:
- ❌ Do NOT use the existing BKT results in paper tables
- ❌ Do NOT fabricate expected BKT AUC
- ❌ Do NOT claim "BKT is competitive" — the degenerate behavior is real

---

## 7. Risks and Implications for Paper Tables

| Table | Current content | Action needed |
|-------|-----------------|---------------|
| Table III (Overall Results) | BKT AUC=0.50, NLL=24-28 | Replace BKT rows with IRT 1PL after T13 re-run |
| Table IV (Per-bucket) | BKT degenerate across buckets | Replace after T13 |
| Table V (Cold-start groups) | BKT degenerate for all groups | Replace after T13 |

**Risk:** IRT 1PL has lower AUC than DKT/SimpleKT for learner_based split (cold-start OOV issue). This should be documented clearly in the paper as a known limitation of IRT.

**Opportunity:** IRT's failure on learner_based split (OOV users) vs. competitiveness on temporal split provides an interesting contrast that strengthens the paper's diagnostic framework.

---

## 8. Recommendation for T13 Re-run

1. **Replace BKT with IRT 1PL** in the experiment pipeline:
   - Update `src/full_baseline_runner.py` to include `irt_1pl` in baselines list
   - Use `src/models/irt_baseline.py` implementation
   - Use `configs/irt_1pl.yaml` config

2. **Re-run full experiments** for all 3 datasets × 2 splits × 3 seeds

3. **Do NOT delete existing BKT prediction files** — keep as historical record

4. **Update paper text** to explain:
   - BKT was replaced due to pyBKT numerical instability
   - IRT 1PL is used as the classical educational measurement baseline
   - IRT limitations (no learning progression, OOV handling) are documented

5. **T11 fix also required** before T13: The prediction-label misalignment bug in DKT/SimpleKT must be re-run after the fix in `src/full_baseline_runner.py`

---

## Files Created in T12

| File | Description |
|------|-------------|
| `scripts/audit_bkt_outputs.py` | BKT prediction distribution audit script |
| `results/tables/bkt_probability_audit.csv` | Per-file BKT probability statistics |
| `logs/bkt_parameter_audit.csv` | BKT parameters from subset fit |
| `results/reports/bkt_probability_audit.md` | Probability distribution audit report |
| `results/reports/bkt_config_audit.md` | Configuration and EM saturation analysis |
| `results/tables/bkt_debug_subset_results.csv` | BKT vs IRT 1PL comparison on subset |
| `configs/bkt_debug.yaml` | Failed BKT fix config (documented) |
| `configs/irt_1pl.yaml` | IRT 1PL configuration |
| `src/models/irt_baseline.py` | IRT 1PL implementation |

---

*Report generated by Antigravity (T12 audit) — 2026-06-13*
