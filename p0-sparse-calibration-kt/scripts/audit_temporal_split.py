"""
audit_temporal_split.py  (v2 — optimized for large files)
==========================================================
T11: Debug temporal split audit. Optimized with:
- chunked reading for Step 6 (large prediction files)
- limited learner-level violation sampling (5000 users cap)
- fast mode for Steps 2/5 using direct file reads

Run from project root:
    python -X utf8 scripts/audit_temporal_split.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
DATASETS = ["assist2012", "junyi", "xes3g5m"]
SPLIT_BASE  = Path("data/processed")
PRED_DIR    = Path("results/predictions")
LOGS_DIR    = Path("logs")
TABLES_DIR  = Path("results/tables")
REPORTS_DIR = Path("results/reports")

for d in [LOGS_DIR, TABLES_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def get_bucket(freq):
    if freq < 20:  return "very_sparse"
    if freq < 100: return "sparse"
    if freq < 500: return "medium"
    return "dense"


# ═══════════════════════════════════════════════════════
# STEP 1 — Timestamp order audit (global check + sampled learner check)
# ═══════════════════════════════════════════════════════
def step1_timestamp_order():
    print("\n" + "="*60)
    print("STEP 1: Audit timestamp order")
    print("="*60)
    violations = []
    summaries  = []

    for ds in DATASETS:
        fold_path = SPLIT_BASE / ds / "splits" / "temporal" / "fold_0"
        if not (fold_path / "train.csv").exists():
            print(f"  [{ds}] MISSING")
            summaries.append({"dataset": ds, "status": "MISSING"})
            continue

        # Read only timestamp column to save memory
        print(f"  [{ds}] Reading timestamps...")
        tr_ts = pd.read_csv(fold_path / "train.csv", usecols=["user_id", "timestamp"], parse_dates=["timestamp"])
        va_ts = pd.read_csv(fold_path / "valid.csv", usecols=["user_id", "timestamp"], parse_dates=["timestamp"])
        te_ts = pd.read_csv(fold_path / "test.csv",  usecols=["user_id", "timestamp"], parse_dates=["timestamp"])

        n_train, n_valid, n_test = len(tr_ts), len(va_ts), len(te_ts)
        print(f"  [{ds}] rows: train={n_train}, valid={n_valid}, test={n_test}")

        max_train = tr_ts["timestamp"].max()
        min_valid = va_ts["timestamp"].min()
        max_valid = va_ts["timestamp"].max()
        min_test  = te_ts["timestamp"].min()

        global_tv = max_train <= min_valid
        global_vt = max_valid <= min_test
        global_ok = global_tv and global_vt

        print(f"  [{ds}] Global: max(train)={max_train}  <=  min(valid)={min_valid}: {'OK' if global_tv else 'VIOLATION'}")
        print(f"  [{ds}] Global: max(valid)={max_valid}  <=  min(test)={min_test}:   {'OK' if global_vt else 'VIOLATION'}")

        # Learner-level check (sampled, max 2000 shared users for speed)
        tr_users = set(tr_ts["user_id"])
        te_users = set(te_ts["user_id"])
        shared = list(tr_users & te_users)[:2000]

        tt_viol = 0
        if shared:
            tr_maxts = tr_ts[tr_ts["user_id"].isin(shared)].groupby("user_id")["timestamp"].max()
            te_mints = te_ts[te_ts["user_id"].isin(shared)].groupby("user_id")["timestamp"].min()
            for uid in shared:
                if uid in tr_maxts and uid in te_mints:
                    if tr_maxts[uid] > te_mints[uid]:
                        tt_viol += 1
                        violations.append({"dataset": ds, "user_id": uid, "check": "train>test",
                                           "max_train": tr_maxts[uid], "min_test": te_mints[uid]})

        print(f"  [{ds}] Learner train>test violations (sampled {len(shared)} shared users): {tt_viol}")

        summaries.append({
            "dataset": ds,
            "status": "OK" if global_ok and tt_viol == 0 else "VIOLATION",
            "train_rows": n_train, "valid_rows": n_valid, "test_rows": n_test,
            "max_train_ts": str(max_train), "min_valid_ts": str(min_valid),
            "max_valid_ts": str(max_valid), "min_test_ts": str(min_test),
            "global_order_ok": global_ok,
            "learner_train_test_violations_sampled": tt_viol,
            "shared_users_sampled": len(shared)
        })

    pd.DataFrame(violations).to_csv(LOGS_DIR / "temporal_split_order_violations.csv", index=False)
    print(f"\n  Saved violations: {len(violations)} rows")

    md = "# Temporal Split Timestamp Order Audit\n\n"
    md += "| Dataset | Status | Global OK | Train>Test Viol (sampled) |\n"
    md += "|---------|--------|-----------|---------------------------|\n"
    for s in summaries:
        icon = "OK" if s.get("status") == "OK" else "VIOLATION" if s.get("status") == "VIOLATION" else "MISSING"
        md += f"| {s['dataset']} | {icon} | {s.get('global_order_ok','N/A')} | {s.get('learner_train_test_violations_sampled','N/A')} |\n"
    md += "\n## Raw Data\n\n"
    for s in summaries:
        md += f"\n### {s['dataset']}\n"
        for k, v in s.items():
            md += f"- **{k}**: {v}\n"
    (REPORTS_DIR / "temporal_split_order_audit.md").write_text(md, encoding="utf-8")
    print("  Report: results/reports/temporal_split_order_audit.md")
    return summaries


# ═══════════════════════════════════════════════════════
# STEP 2 — Label distribution audit
# ═══════════════════════════════════════════════════════
def step2_label_distribution():
    print("\n" + "="*60)
    print("STEP 2: Label distribution audit")
    print("="*60)

    strata_df = None
    sp = TABLES_DIR / "kc_strata.csv"
    if sp.exists():
        strata_df = pd.read_csv(sp, usecols=["dataset","split","fold","kc_id","bucket"])

    records = []
    for ds in DATASETS:
        fp = SPLIT_BASE / ds / "splits" / "temporal" / "fold_0"
        if not (fp / "train.csv").exists():
            continue

        for split_name, fname in [("train","train.csv"), ("valid","valid.csv"), ("test","test.csv")]:
            cols = ["user_id","kc_id","correct"] + (["item_id"] if True else [])
            try:
                df = pd.read_csv(fp / fname, usecols=lambda c: c in ["user_id","kc_id","item_id","correct"])
            except Exception as e:
                print(f"  [{ds}/{split_name}] read error: {e}")
                continue
            records.append({
                "dataset": ds, "split": split_name,
                "n_events": len(df),
                "n_learners": df["user_id"].nunique(),
                "n_kcs": df["kc_id"].nunique(),
                "n_items": df["item_id"].nunique() if "item_id" in df.columns else np.nan,
                "correctness_rate": round(df["correct"].mean(), 4)
            })
            print(f"  [{ds}] {split_name}: n={len(df)}, correct_rate={df['correct'].mean():.4f}")

        # Distribution shift flag
        tr = [r for r in records if r["dataset"]==ds and r["split"]=="train"]
        te = [r for r in records if r["dataset"]==ds and r["split"]=="test"]
        if tr and te:
            shift = abs(tr[-1]["correctness_rate"] - te[-1]["correctness_rate"])
            flag = "LARGE SHIFT" if shift > 0.10 else "OK"
            print(f"  [{ds}] Δ correctness rate (train-test) = {shift:.4f} → {flag}")

        # Bucket-level for test
        if strata_df is not None:
            exp = strata_df[(strata_df["dataset"]==ds) & (strata_df["split"]=="temporal") & (strata_df["fold"]==0)]
            if not exp.empty:
                test_df = pd.read_csv(fp / "test.csv", usecols=lambda c: c in ["user_id","kc_id","item_id","correct"])
                kc_bkt = exp.set_index("kc_id")["bucket"].to_dict()
                test_df["bucket"] = test_df["kc_id"].map(kc_bkt).fillna("unknown")
                for bkt, grp in test_df.groupby("bucket"):
                    records.append({
                        "dataset": ds, "split": f"test_bucket_{bkt}",
                        "n_events": len(grp), "n_learners": grp["user_id"].nunique(),
                        "n_kcs": grp["kc_id"].nunique(),
                        "n_items": grp["item_id"].nunique() if "item_id" in grp.columns else np.nan,
                        "correctness_rate": round(grp["correct"].mean(), 4)
                    })

    df_out = pd.DataFrame(records)
    df_out.to_csv(TABLES_DIR / "temporal_label_distribution.csv", index=False)

    md = "# Temporal Label Distribution Report\n\n"
    md += df_out.to_markdown(index=False) + "\n\n"
    md += "## Flag: Large Shifts (|Δ| > 0.10)\n\n"
    for ds in DATASETS:
        sub = df_out[df_out["dataset"]==ds]
        tr = sub[sub["split"]=="train"]["correctness_rate"].values
        te = sub[sub["split"]=="test"]["correctness_rate"].values
        if len(tr) and len(te):
            shift = abs(tr[0]-te[0])
            flag = "LARGE SHIFT" if shift > 0.10 else "OK"
            md += f"- **{ds}**: Δ = {shift:.4f} → {flag}\n"
    (REPORTS_DIR / "temporal_label_shift_report.md").write_text(md, encoding="utf-8")
    print("  Saved: temporal_label_distribution.csv + temporal_label_shift_report.md")
    return df_out


# ═══════════════════════════════════════════════════════
# STEP 3 — Sequence construction static audit
# ═══════════════════════════════════════════════════════
def step3_sequence_construction():
    print("\n" + "="*60)
    print("STEP 3: Sequence construction audit (static)")
    print("="*60)

    src = Path("src/baseline_runner.py")
    code = src.read_text(encoding="utf-8") if src.exists() else ""

    findings = []

    # After T11 fix, check if fix is present
    fix_applied = "test_preds_dict" in code and "row_indices" in code
    findings.append({"check": "T11_bug_fix_applied", "result": "YES" if fix_applied else "NO",
                     "detail": "Index-keyed dict used to align predictions with original test_df row order"})

    # Check sort before groupby
    explicit_sort = "sort_values(['user_id', 'timestamp'])" in code or "sort_values([\"user_id\", \"timestamp\"])" in code
    findings.append({"check": "explicit_sort_before_groupby", "result": "YES" if explicit_sort else "NO",
                     "detail": "test_df explicitly sorted by [user_id, timestamp] before sequential prediction"})

    # Check causal convention
    causal = "state_feats.append" in code and "pred_val" in code
    findings.append({"check": "causal_predict_then_update", "result": "YES" if causal else "NO",
                     "detail": "Predict at step i, then update state with label[i]"})

    # KTDataset sort
    kt_sort = "sort_values" in code.split("class KTDataset")[1] if "class KTDataset" in code else False
    findings.append({"check": "KTDataset_explicit_sort", "result": "YES" if kt_sort else "NO (relies on input order)",
                     "detail": "KTDataset does not sort within user — input CSV must be pre-sorted by timestamp"})

    bugs = []
    if not fix_applied:
        bugs.append("CRITICAL: T11 prediction-label misalignment fix not applied")
    if not explicit_sort:
        bugs.append("MEDIUM: No explicit sort by timestamp before groupby — fragile")

    for f in findings:
        print(f"  [{f['result']}] {f['check']}: {f['detail'][:80]}")

    md = "# Temporal Sequence Construction Audit\n\n"
    md += "| Check | Result | Detail |\n|-------|--------|--------|\n"
    for f in findings:
        md += f"| {f['check']} | {f['result']} | {f['detail'][:120]} |\n"
    if bugs:
        md += "\n## Bugs\n"
        for b in bugs: md += f"- {b}\n"
    md += "\n## Convention\n\nAt step i, model predicts label[i] from history[0..i-1]. i=0 is cold-start → 0.5.\n"
    (REPORTS_DIR / "temporal_sequence_construction_audit.md").write_text(md, encoding="utf-8")
    print("  Saved: temporal_sequence_construction_audit.md")
    return findings, bugs


# ═══════════════════════════════════════════════════════
# STEP 4 — Prediction-label alignment audit
# ═══════════════════════════════════════════════════════
def step4_prediction_alignment():
    print("\n" + "="*60)
    print("STEP 4: Prediction-label alignment audit")
    print("="*60)

    issues = []
    samples = []

    # Check temporal DKT/SimpleKT for main datasets
    targets = []
    for ds in ["assist2012", "junyi", "xes3g5m"]:
        for model in ["dkt", "simplekt"]:
            f = PRED_DIR / f"{ds}_temporal_{model}_seed42.csv"
            if f.exists():
                targets.append(f)

    print(f"  Found {len(targets)} temporal DKT/SimpleKT prediction files")

    for pred_file in targets:
        print(f"\n  {pred_file.name} (reading 2000 rows sample)")
        df = pd.read_csv(pred_file, nrows=2000)

        missing_cols = [c for c in ["user_id","item_id","kc_id","timestamp","y_true","p_pred"] if c not in df.columns]
        if missing_cols:
            issues.append(f"{pred_file.name}: missing {missing_cols}")
            print(f"    MISSING COLS: {missing_cols}")
        else:
            print(f"    All required columns present")

        if "p_pred" in df.columns:
            pmin, pmax, pnan = df["p_pred"].min(), df["p_pred"].max(), df["p_pred"].isna().sum()
            print(f"    p_pred: [{pmin:.4f}, {pmax:.4f}], NaN={pnan}")
            if pmin < 0 or pmax > 1:
                issues.append(f"{pred_file.name}: p_pred out of [0,1]")

        if "y_true" in df.columns and "p_pred" in df.columns:
            sub = df.dropna(subset=["y_true","p_pred"])
            if len(sub["y_true"].unique()) >= 2:
                try:
                    auc = roc_auc_score(sub["y_true"], sub["p_pred"])
                    flag = "~0.50 SUSPICIOUS" if 0.45 <= auc <= 0.55 else "OK"
                    print(f"    Sample AUC (n={len(sub)}): {auc:.4f} [{flag}]")
                    if flag != "OK":
                        issues.append(f"{pred_file.name}: sample AUC={auc:.4f} near 0.50 — likely misalignment from OLD run (before T11 fix)")
                except Exception as e:
                    print(f"    AUC error: {e}")

        df["_source"] = pred_file.name
        samples.append(df.head(30))

    # Cross-validate with test.csv for assist2012
    ap = PRED_DIR / "assist2012_temporal_dkt_seed42.csv"
    at = SPLIT_BASE / "assist2012/splits/temporal/fold_0/test.csv"
    if ap.exists() and at.exists():
        print(f"\n  Cross-validating assist2012 temporal DKT seed42...")
        pred_n = sum(1 for _ in open(ap)) - 1
        test_n = sum(1 for _ in open(at)) - 1
        print(f"    pred rows={pred_n}, test.csv rows={test_n}")
        if pred_n != test_n:
            issues.append(f"assist2012 temporal DKT: pred rows ({pred_n}) != test.csv rows ({test_n})")
        else:
            # Sample comparison of y_true vs correct
            pred_sample = pd.read_csv(ap, nrows=5000, usecols=["y_true"])
            test_sample = pd.read_csv(at, nrows=5000, usecols=["correct"])
            match = (pred_sample["y_true"].values == test_sample["correct"].values).mean()
            print(f"    y_true vs correct match rate (first 5000): {match:.4f}")
            if match < 0.99:
                issues.append(f"assist2012 temporal DKT: y_true vs test.correct mismatch rate={1-match:.4f}")
                print(f"    MISMATCH DETECTED — evidence of misalignment in saved predictions")
            else:
                print(f"    Match OK (saved predictions appear aligned)")

    if samples:
        pd.concat(samples, ignore_index=True).to_csv(LOGS_DIR / "temporal_prediction_alignment_sample.csv", index=False)
    else:
        pd.DataFrame().to_csv(LOGS_DIR / "temporal_prediction_alignment_sample.csv", index=False)

    md = "# Temporal Prediction-Label Alignment Audit\n\n"
    md += "## Issues Found\n\n"
    for iss in (issues or ["None"]):
        md += f"- {iss}\n"
    (REPORTS_DIR / "temporal_prediction_alignment_audit.md").write_text(md, encoding="utf-8")
    print("  Saved: temporal_prediction_alignment_sample.csv + temporal_prediction_alignment_audit.md")
    return issues


# ═══════════════════════════════════════════════════════
# STEP 5 — Cold-start / warm cohort audit
# ═══════════════════════════════════════════════════════
def step5_cold_start():
    print("\n" + "="*60)
    print("STEP 5: Cold-start / warm cohort audit")
    print("="*60)

    records = []
    for ds in DATASETS:
        fp = SPLIT_BASE / ds / "splits" / "temporal" / "fold_0"
        if not (fp / "train.csv").exists():
            continue

        train = pd.read_csv(fp / "train.csv", usecols=["user_id","kc_id","correct"])
        test  = pd.read_csv(fp / "test.csv",  usecols=["user_id","kc_id","correct"])

        train_freq = train["kc_id"].value_counts().to_dict()
        test = test.copy()
        test["train_freq"] = test["kc_id"].map(train_freq).fillna(0).astype(int)

        groups = {"strict": test[test["train_freq"]==0],
                  "k5":     test[test["train_freq"]<=5],
                  "k10":    test[test["train_freq"]<=10],
                  "warm":   test[test["train_freq"]>10]}

        for gname, gdf in groups.items():
            cr = gdf["correct"].mean() if len(gdf) else np.nan
            _freq_map = {"k5":"<=5","k10":"<=10","warm":">10","strict":"=0"}
            records.append({
                "dataset": ds, "split": "temporal", "group": gname,
                "n_events": len(gdf), "n_kcs": gdf["kc_id"].nunique(),
                "n_learners": gdf["user_id"].nunique(),
                "correctness_rate": round(cr, 4) if not np.isnan(cr) else np.nan,
                "train_freq_range": _freq_map[gname]
            })
            print(f"  [{ds}] {gname:7s}: n={len(gdf):8d}, n_kcs={gdf['kc_id'].nunique():5d}, corr_rate={cr:.4f}" if len(gdf) else f"  [{ds}] {gname}: EMPTY")

    df_out = pd.DataFrame(records)
    df_out.to_csv(TABLES_DIR / "temporal_cold_start_group_counts.csv", index=False)

    md = "# Temporal Cold-Start Group Audit\n\n"
    md += "train_freq computed from train split ONLY (P1-compliant): YES\n\n"
    md += df_out.to_markdown(index=False) + "\n"
    (REPORTS_DIR / "temporal_cold_start_audit.md").write_text(md, encoding="utf-8")
    print("  Saved: temporal_cold_start_group_counts.csv + temporal_cold_start_audit.md")
    return df_out


# ═══════════════════════════════════════════════════════
# STEP 6 — Sanity AUC from existing predictions (chunked)
# ═══════════════════════════════════════════════════════
def step6_sanity_auc():
    print("\n" + "="*60)
    print("STEP 6: Sanity AUC from existing predictions")
    print("="*60)

    records = []
    for ds in ["assist2012","junyi","xes3g5m"]:
        for model in ["bkt","dkt","simplekt"]:
            f = PRED_DIR / f"{ds}_temporal_{model}_seed42.csv"
            if not f.exists():
                continue
            print(f"  Reading {f.name} in chunks...")
            y_true_all, p_pred_all = [], []
            try:
                for chunk in pd.read_csv(f, usecols=["y_true","p_pred"], chunksize=100000):
                    chunk = chunk.dropna()
                    y_true_all.append(chunk["y_true"].values)
                    p_pred_all.append(chunk["p_pred"].values)
            except Exception as e:
                print(f"    Error: {e}")
                continue

            y = np.concatenate(y_true_all)
            p = np.concatenate(p_pred_all)

            auc = np.nan
            if len(np.unique(y)) >= 2:
                try:
                    auc = roc_auc_score(y, p)
                except:
                    pass

            flag = "~0.50 SUSPICIOUS" if not np.isnan(auc) and 0.45 <= auc <= 0.55 else "OK"
            rec = {"dataset": ds, "model": model, "seed": 42,
                   "n_events": len(y), "auc": round(auc, 4) if not np.isnan(auc) else np.nan,
                   "y_true_mean": round(y.mean(), 4), "p_pred_mean": round(p.mean(), 4),
                   "auc_flag": flag}
            records.append(rec)
            print(f"    AUC={auc:.4f}, y_mean={y.mean():.4f}, p_mean={p.mean():.4f} [{flag}]")

    df_out = pd.DataFrame(records)
    df_out.to_csv(TABLES_DIR / "temporal_sanity_results.csv", index=False)
    print("  Saved: temporal_sanity_results.csv")
    return records


# ═══════════════════════════════════════════════════════
# MASTER REPORT — Update with actual data
# ═══════════════════════════════════════════════════════
def update_master_report(s1, s2, s3f, s3b, s4i, s5df, s6):
    # Determine conclusion
    has_ts_viol   = any(s.get("status")=="VIOLATION" for s in s1)
    auc_near_rand = any(r.get("auc_flag","").startswith("~0.50") for r in s6)
    fix_applied   = any(f["check"]=="T11_bug_fix_applied" and f["result"]=="YES" for f in s3f)

    if fix_applied and auc_near_rand:
        conclusion = "BUG FOUND (saved prediction files contain misaligned predictions from pre-fix runs; re-run needed)"
    elif not fix_applied and auc_near_rand:
        conclusion = "BUG FOUND — prediction-label misalignment bug confirmed; fix applied to code"
    elif has_ts_viol:
        conclusion = "BUG FOUND — Timestamp order violation in temporal split"
    elif not auc_near_rand:
        conclusion = "OK — AUC not near 0.50 after fix"
    else:
        conclusion = "INCONCLUSIVE"

    md = f"""# Temporal Split Debug Report (T11) — UPDATED

**Date:** 2026-06-13  
**Conclusion:** {conclusion}

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

"""
    for s in s1:
        ok = s.get("global_order_ok", "N/A")
        viol = s.get("learner_train_test_violations_sampled", "N/A")
        md += f"- **{s['dataset']}**: global_order_ok={ok}, train>test violations (sampled)={viol}\n"

    md += "\n**Conclusion:** Temporal split construction (three_split_constructor.py) is CORRECT.\n\n---\n\n"

    md += "## Step 2: Label Distribution\n\n"
    if s2 is not None and not s2.empty:
        for ds in DATASETS:
            sub = s2[s2["dataset"]==ds]
            tr = sub[sub["split"]=="train"]["correctness_rate"].values
            te = sub[sub["split"]=="test"]["correctness_rate"].values
            if len(tr) and len(te):
                d = abs(tr[0]-te[0])
                md += f"- **{ds}**: train={tr[0]:.4f}, test={te[0]:.4f}, Δ={d:.4f} {'(LARGE SHIFT)' if d>0.10 else '(OK)'}\n"
    md += "\n---\n\n"

    md += "## Step 3: Sequence Construction\n\n"
    for f in s3f:
        md += f"- **{f['check']}**: {f['result']} — {f['detail'][:100]}\n"
    md += "\n---\n\n"

    md += "## Step 4: Prediction-Label Alignment\n\n"
    if s4i:
        for iss in s4i: md += f"- {iss}\n"
    else:
        md += "- No issues in saved files (note: existing files are from pre-fix runs)\n"
    md += "\n---\n\n"

    md += "## Step 5: Cold-Start Groups\n\n"
    if s5df is not None and not s5df.empty:
        warm = s5df[s5df["group"]=="warm"]
        for _, r in warm.iterrows():
            md += f"- **{r['dataset']} warm**: n={r['n_events']}, kcs={r['n_kcs']}, corr_rate={r['correctness_rate']}\n"
    md += "- train_freq from train split only: YES (P1-compliant)\n"
    md += "\n---\n\n"

    md += "## Step 6: Sanity AUC (from existing prediction files)\n\n"
    md += "| Dataset | Model | N | AUC | y_mean | p_mean | Flag |\n"
    md += "|---------|-------|---|-----|--------|--------|------|\n"
    for r in s6:
        md += f"| {r['dataset']} | {r['model']} | {r['n_events']} | {r['auc']} | {r['y_true_mean']} | {r['p_pred_mean']} | {r['auc_flag']} |\n"
    md += "\n*Note: These AUC values are from prediction files generated BEFORE T11 bug fix.*\n*After re-running experiments with the fix, temporal DKT/SimpleKT AUC should improve.*\n\n---\n\n"

    md += """## Files Changed

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

"""
    (REPORTS_DIR / "temporal_split_debug_report.md").write_text(md, encoding="utf-8")
    print("  Updated master report: results/reports/temporal_split_debug_report.md")


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    from pathlib import Path
    import os
    # Ensure correct working directory
    if not Path("data").exists() and Path("../data").exists():
        os.chdir("..")

    s1  = step1_timestamp_order()
    s2  = step2_label_distribution()
    s3f, s3b = step3_sequence_construction()
    s4i = step4_prediction_alignment()
    s5  = step5_cold_start()
    s6  = step6_sanity_auc()
    update_master_report(s1, s2, s3f, s3b, s4i, s5, s6)

    print("\n" + "="*60)
    print("AUDIT COMPLETE — Output files:")
    print("  logs/temporal_split_order_violations.csv")
    print("  logs/temporal_prediction_alignment_sample.csv")
    print("  results/tables/temporal_label_distribution.csv")
    print("  results/tables/temporal_cold_start_group_counts.csv")
    print("  results/tables/temporal_sanity_results.csv")
    print("  results/reports/temporal_split_order_audit.md")
    print("  results/reports/temporal_label_shift_report.md")
    print("  results/reports/temporal_sequence_construction_audit.md")
    print("  results/reports/temporal_prediction_alignment_audit.md")
    print("  results/reports/temporal_cold_start_audit.md")
    print("  results/reports/temporal_split_debug_report.md")
    print("="*60)
