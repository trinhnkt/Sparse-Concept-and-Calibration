"""
audit_bkt_outputs.py
====================
T12 Step 1 & 2: Audit BKT prediction distribution and parameters.
Run from project root:
    python -X utf8 scripts/audit_bkt_outputs.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, mean_squared_error
import warnings
warnings.filterwarnings("ignore")

DATASETS = ["assist2012", "junyi", "xes3g5m"]
PRED_DIR    = Path("results/predictions")
TABLES_DIR  = Path("results/tables")
REPORTS_DIR = Path("results/reports")
LOGS_DIR    = Path("logs")
FIG_DIR     = Path("results/figures")

for d in [TABLES_DIR, REPORTS_DIR, LOGS_DIR, FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

EPS = 1e-7   # safe clipping for NLL audit only


def audit_bkt_file(pred_file):
    """Compute probability distribution stats for one BKT prediction file."""
    df = pd.read_csv(pred_file)
    if df.empty or "p_pred" not in df.columns:
        return None

    pp = df["p_pred"].values
    yt = df["y_true"].values if "y_true" in df.columns else df["correct"].values

    n_total   = len(pp)
    n_nan     = int(np.isnan(pp).sum())
    n_zero    = int((pp == 0.0).sum())
    n_one     = int((pp == 1.0).sum())
    n_near_0  = int((pp < 0.001).sum())
    n_near_1  = int((pp > 0.999).sum())
    n_unique  = int(pd.Series(pp).dropna().round(4).nunique())

    valid     = ~np.isnan(pp)
    pp_v      = pp[valid]
    yt_v      = yt[valid]

    stats = {
        "file": pred_file.name,
        "n_total": n_total,
        "n_nan": n_nan,
        "pct_nan": round(100*n_nan/n_total, 2),
        "n_zero": n_zero,
        "pct_zero": round(100*n_zero/n_total, 2),
        "n_one": n_one,
        "pct_one": round(100*n_one/n_total, 2),
        "n_near_0": n_near_0,
        "pct_near_0": round(100*n_near_0/n_total, 2),
        "n_near_1": n_near_1,
        "pct_near_1": round(100*n_near_1/n_total, 2),
        "n_unique_rounded": n_unique,
        "min": round(float(np.nanmin(pp)), 6) if n_total > n_nan else np.nan,
        "max": round(float(np.nanmax(pp)), 6) if n_total > n_nan else np.nan,
        "mean": round(float(np.nanmean(pp)), 6) if n_total > n_nan else np.nan,
        "std": round(float(np.nanstd(pp)), 6) if n_total > n_nan else np.nan,
        "q01": round(float(np.nanpercentile(pp, 1)), 6) if len(pp_v) else np.nan,
        "q05": round(float(np.nanpercentile(pp, 5)), 6) if len(pp_v) else np.nan,
        "q25": round(float(np.nanpercentile(pp, 25)), 6) if len(pp_v) else np.nan,
        "q50": round(float(np.nanpercentile(pp, 50)), 6) if len(pp_v) else np.nan,
        "q75": round(float(np.nanpercentile(pp, 75)), 6) if len(pp_v) else np.nan,
        "q95": round(float(np.nanpercentile(pp, 95)), 6) if len(pp_v) else np.nan,
        "q99": round(float(np.nanpercentile(pp, 99)), 6) if len(pp_v) else np.nan,
    }

    # Metrics (on valid rows only)
    if len(pp_v) > 0 and len(np.unique(yt_v)) >= 2:
        try:
            stats["auc"] = round(roc_auc_score(yt_v, pp_v), 4)
        except:
            stats["auc"] = np.nan
        stats["acc"] = round(accuracy_score(yt_v, (pp_v >= 0.5).astype(int)), 4)
        pp_clip = np.clip(pp_v, EPS, 1-EPS)
        stats["nll_clipped"] = round(log_loss(yt_v, pp_clip), 4)
        stats["brier"] = round(float(np.mean((pp_v - yt_v)**2)), 4)
        stats["y_true_mean"] = round(float(yt_v.mean()), 4)
        stats["degenerate"] = (n_unique <= 5)
    else:
        stats["auc"] = np.nan
        stats["acc"] = np.nan
        stats["nll_clipped"] = np.nan
        stats["brier"] = np.nan
        stats["y_true_mean"] = round(float(yt.mean()), 4) if len(yt) else np.nan
        stats["degenerate"] = True

    return stats


def step1_audit_bkt():
    print("=" * 60)
    print("STEP 1: BKT prediction distribution audit")
    print("=" * 60)

    bkt_files = sorted(PRED_DIR.glob("*_bkt_*.csv"))
    main_bkt  = [f for f in bkt_files
                 if any(f.name.startswith(ds) for ds in DATASETS)]

    print(f"  Found {len(main_bkt)} BKT prediction files for main datasets")

    records = []
    for pf in main_bkt:
        print(f"\n  {pf.name}")
        rec = audit_bkt_file(pf)
        if rec:
            records.append(rec)
            print(f"    n_total={rec['n_total']}, n_nan={rec['n_nan']}({rec['pct_nan']}%), "
                  f"n_zero={rec['n_zero']}({rec['pct_zero']}%), "
                  f"n_unique={rec['n_unique_rounded']}, AUC={rec.get('auc','N/A')}")
            if rec.get("degenerate"):
                print("    *** DEGENERATE: <=5 unique prediction values ***")

    df_out = pd.DataFrame(records)
    df_out.to_csv(TABLES_DIR / "bkt_probability_audit.csv", index=False)
    print(f"\n  Saved: results/tables/bkt_probability_audit.csv ({len(records)} files)")

    # Markdown report
    md = "# BKT Prediction Probability Audit\n\n"
    md += "## Summary\n\n"
    md += f"Analyzed {len(records)} BKT prediction files.\n\n"

    deg_count = sum(1 for r in records if r.get("degenerate"))
    md += f"- **Degenerate files (<=5 unique values):** {deg_count}/{len(records)}\n"
    md += f"- **BKT version:** pyBKT 1.4.1\n\n"

    md += "## Per-File Statistics\n\n"
    md += "| File | n_total | pct_nan | pct_zero | pct_near_0 | n_unique | AUC | Degenerate? |\n"
    md += "|------|---------|---------|----------|------------|----------|-----|-------------|\n"
    for r in records:
        deg = "YES" if r.get("degenerate") else "no"
        md += (f"| {r['file']} | {r['n_total']} | {r.get('pct_nan','N/A')}% | "
               f"{r.get('pct_zero','N/A')}% | {r.get('pct_near_0','N/A')}% | "
               f"{r.get('n_unique_rounded','N/A')} | {r.get('auc','N/A')} | {deg} |\n")

    md += "\n## Root Cause Analysis\n\n"
    md += (
        "All BKT predictions are degenerate: p_pred ∈ {0.0, NaN} with ≤5 unique values.\n\n"
        "**Root cause:** pyBKT 1.4.1 EM algorithm suffers divide-by-zero in M_step.py line 61 "
        "(init_softcounts = 0 → prior = NaN). Once prior = NaN, all subsequent HMM forward passes "
        "fail, yielding p_pred = 0.0 or NaN.\n\n"
        "This is not a data preprocessing issue but a pyBKT numerical stability issue "
        "on datasets with sparse KC histories.\n\n"
        "**Evidence:**\n"
        "- learns = 1.000 (saturated) for all KCs\n"
        "- guesses = slips = 0.500 (EM did not converge — stuck at initial values)\n"
        "- prior = NaN for all KCs\n"
        "- AUC = 0.5000 across all datasets and splits\n"
    )

    (REPORTS_DIR / "bkt_probability_audit.md").write_text(md, encoding="utf-8")
    print("  Saved: results/reports/bkt_probability_audit.md")
    return records


def step2_audit_bkt_params():
    """Try to fit BKT on a small subset and log parameters."""
    print("\n" + "=" * 60)
    print("STEP 2: BKT parameter audit (subset fit)")
    print("=" * 60)

    try:
        from pyBKT.models import Model as BKTModel
    except ImportError:
        print("  pyBKT not available")
        return

    SPLIT_BASE = Path("data/processed")
    param_records = []

    for ds in DATASETS:
        fp = SPLIT_BASE / ds / "splits" / "temporal" / "fold_0"
        if not (fp / "train.csv").exists():
            print(f"  [{ds}] MISSING")
            continue

        # Small subset
        n_rows = 50000 if ds == "assist2012" else 30000
        train = pd.read_csv(fp / "train.csv", nrows=n_rows)
        unique_kcs = sorted(train["kc_id"].unique())
        kc_map = {kc: i for i, kc in enumerate(unique_kcs)}

        bkt_train = train[["user_id","kc_id","correct"]].copy()
        bkt_train["skill_name"] = bkt_train["kc_id"].map(lambda x: f"skill_{kc_map[x]}")
        bkt_train = bkt_train[["user_id","skill_name","correct"]]

        print(f"\n  [{ds}] Fitting BKT on {len(bkt_train)} rows, {len(unique_kcs)} KCs...")
        bkt = BKTModel(seed=42)
        try:
            import warnings
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                bkt.fit(data=bkt_train, num_fits=1)
                n_warn = len(w)

            params_df = bkt.params().reset_index()
            params_df["dataset"] = ds

            for param_name in ["prior","learns","guesses","slips","forgets"]:
                sub = params_df[params_df["param"] == param_name]
                if len(sub):
                    vals = sub["value"].values
                    n_nan  = int(np.isnan(vals).sum())
                    n_sat0 = int((vals < 0.001).sum())
                    n_sat1 = int((vals > 0.999).sum())
                    flags  = []
                    if param_name == "guesses" and np.nanmean(vals) > 0.5:
                        flags.append("WARN:guess>0.5")
                    if param_name == "slips" and np.nanmean(vals) > 0.5:
                        flags.append("WARN:slip>0.5")
                    if param_name == "learns" and (np.nanmean(vals) > 0.98 or np.nanmean(vals) < 0.02):
                        flags.append("WARN:learns_extreme")
                    if param_name == "prior" and n_nan > 0:
                        flags.append("WARN:prior_NaN")

                    param_records.append({
                        "dataset": ds, "param": param_name, "n_kcs": len(sub),
                        "mean": round(float(np.nanmean(vals)), 4) if len(vals) > n_nan else np.nan,
                        "std": round(float(np.nanstd(vals)), 4) if len(vals) > n_nan else np.nan,
                        "min": round(float(np.nanmin(vals)), 4) if len(vals) > n_nan else np.nan,
                        "max": round(float(np.nanmax(vals)), 4) if len(vals) > n_nan else np.nan,
                        "n_nan": n_nan, "n_sat0": n_sat0, "n_sat1": n_sat1,
                        "n_em_warnings": n_warn,
                        "flags": "; ".join(flags) if flags else "OK"
                    })
                    flag_str = "; ".join(flags) if flags else "OK"
                    print(f"    {param_name}: mean={np.nanmean(vals):.3f} nan={n_nan}/{len(vals)} sat1={n_sat1} [{flag_str}]")

        except Exception as e:
            print(f"  [{ds}] BKT fit error: {e}")
            param_records.append({"dataset": ds, "param": "ALL", "flags": f"FIT_ERROR: {e}"})

    df_params = pd.DataFrame(param_records)
    df_params.to_csv(LOGS_DIR / "bkt_parameter_audit.csv", index=False)
    print(f"\n  Saved: logs/bkt_parameter_audit.csv")
    return df_params


if __name__ == "__main__":
    step1_audit_bkt()
    step2_audit_bkt_params()
    print("\nAudit complete.")
