#!/usr/bin/env python3
"""Build FINAL_CLAIM_EVIDENCE.csv from frozen sources. Fail if any row is not VERIFIED."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REV = HERE.parent
ROOT = REV.parent
OUT = HERE / "FINAL_CLAIM_EVIDENCE.csv"
LOG = HERE / "reproduction_rebuild_locked_tables.log"

ASSIST = REV / "analysis" / "summary_4part_bucket.csv"
XES = REV / "a2b" / "analysis" / "summary_4part_bucket.csv"
S7 = REV / "analysis" / "si_threecut_tkt_dkt.csv"
S7_TKT = REV / "analysis" / "si_threecut_tkt.csv"
PUNCH = REV / "tables" / "punchline_ece.csv"
OFFICIAL = ROOT / "results" / "reports" / "p0_official_simplekt_assist_ece.json"
COLD = ROOT / "results" / "tables" / "clean_cold_start_results_summary.csv"
REBUILD = ROOT / "scripts" / "p0_rebuild_locked_tables.py"


def tkt_assist(df: pd.DataFrame, bucket: str, col: str) -> float:
    sl = df[(df["dataset"] == "assist2012") & (df["model"] == "simplekt") & (df["bucket"] == bucket)]
    return float(sl.iloc[0][col])


def xes_cell(df: pd.DataFrame, model: str, bucket: str, col: str) -> float:
    sl = df[(df["dataset"] == "xes3g5m") & (df["model"] == model) & (df["bucket"] == bucket)]
    return float(sl.iloc[0][col])


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    assist = pd.read_csv(ASSIST)
    xes = pd.read_csv(XES)
    rows: list[dict[str, str]] = []

    # 1. Sparse AUC not universally worse (XES DKT/T-KT)
    dkt_d = xes_cell(xes, "dkt", "dense", "auc_mean")
    dkt_s = xes_cell(xes, "dkt", "sparse", "auc_mean")
    tkt_d = xes_cell(xes, "simplekt", "dense", "auc_mean")
    tkt_s = xes_cell(xes, "simplekt", "sparse", "auc_mean")
    ok1 = dkt_s > dkt_d and tkt_s > tkt_d
    rows.append(
        {
            "Claim": "Sparse AUC not universally worse",
            "Dataset": "XES",
            "Model": "DKT/T-KT",
            "Source": "S8; IJIET_FINAL_REVISION/a2b/analysis/summary_4part_bucket.csv",
            "Status": "VERIFIED" if ok1 else "NOT TRACEABLE",
        }
    )

    # 2. ASSIST sparse ECE higher (T-KT lock + official SimpleKT on Table 5)
    e_d = tkt_assist(assist, "dense", "ece_mean")
    e_s = tkt_assist(assist, "sparse", "ece_mean")
    punch = pd.read_csv(PUNCH)
    p4 = punch[punch["agg"] == "4part"]
    p_d = float(p4.loc[p4["bucket"] == "dense", "ece"].iloc[0])
    p_s = float(p4.loc[p4["bucket"] == "sparse", "ece"].iloc[0])
    js = json.loads(OFFICIAL.read_text(encoding="utf-8"))
    o_d = float(js["strata"]["dense"]["ece"])
    o_s = float(js["strata"]["sparse"]["ece"])
    ok2 = (
        round(e_d, 4) == 0.1136
        and round(e_s, 4) == 0.2280
        and round(p_d, 4) == 0.1136
        and round(p_s, 4) == 0.2280
        and o_s > o_d
        and js["positive_dense_to_sparse"] is True
    )
    rows.append(
        {
            "Claim": "ASSIST sparse ECE higher",
            "Dataset": "Assist",
            "Model": "T-KT; official SimpleKT [4]",
            "Source": "Table 5; analysis/summary_4part_bucket.csv; tables/punchline_ece.csv; results/reports/p0_official_simplekt_assist_ece.json",
            "Status": "VERIFIED" if ok2 else "NOT TRACEABLE",
        }
    )

    # 3. Junyi sparse empty
    j = assist[assist["dataset"] == "junyi"]
    ok3 = "sparse" not in set(j["bucket"]) and not j.empty
    rows.append(
        {
            "Claim": "Junyi sparse empty",
            "Dataset": "Junyi",
            "Model": "—",
            "Source": "IJIET_FINAL_REVISION/analysis/summary_4part_bucket.csv (no sparse row)",
            "Status": "VERIFIED" if ok3 else "NOT TRACEABLE",
        }
    )

    # 4. XES ECE flat (T-KT Table 5 series)
    x_d = xes_cell(xes, "simplekt", "dense", "ece_mean")
    x_m = xes_cell(xes, "simplekt", "medium", "ece_mean")
    x_s = xes_cell(xes, "simplekt", "sparse", "ece_mean")
    ok4 = (
        round(x_d, 4) == 0.1176
        and round(x_m, 4) == 0.1129
        and round(x_s, 4) == 0.1254
        and abs(x_s - x_d) < 0.02
    )
    rows.append(
        {
            "Claim": "XES ECE flat",
            "Dataset": "XES",
            "Model": "T-KT",
            "Source": "Table 5; IJIET_FINAL_REVISION/a2b/analysis/summary_4part_bucket.csv",
            "Status": "VERIFIED" if ok4 else "NOT TRACEABLE",
        }
    )

    # 5. k5/k10 groups exist in the cold-start export (supporting; main Table 7 is f=0 / 0<f<20)
    cold = pd.read_csv(COLD)
    groups = set(cold["group"].astype(str))
    assist_k = cold[
        (cold["dataset"] == "assist2012")
        & (cold["split_mode"] == "learner_based")
        & (cold["model"].isin(("dkt", "simplekt")))
        & (cold["group"].isin(("k5", "k10")))
    ]
    ok5 = {"k5", "k10", "strict"}.issubset(groups) and not assist_k.empty
    rows.append(
        {
            "Claim": "k5/k10 cold-start",
            "Dataset": "Assist",
            "Model": "DKT/T-KT",
            "Source": "results/tables/clean_cold_start_results_summary.csv (export groups; main Table 7 uses f=0 and 0<f<20, not k5/k10)",
            "Status": "VERIFIED" if ok5 else "NOT TRACEABLE",
        }
    )

    # 6. Frequency-cut (bucket-threshold) ECE ordering stable — S7, not τ
    s7 = pd.read_csv(S7 if S7.exists() else S7_TKT)
    if "delta" in s7.columns:
        deltas = [float(x) for x in s7["delta"]]
    elif "Sparse ECE" in s7.columns:
        deltas = []
    else:
        # si_threecut_tkt_dkt.csv schema from living file
        deltas = []
        for _, r in s7.iterrows():
            if "delta" in r.index:
                deltas.append(float(r["delta"]))
            elif "sparse_ece" in r.index and "dense_ece" in r.index:
                deltas.append(float(r["sparse_ece"]) - float(r["dense_ece"]))
    if not deltas:
        tkt_only = pd.read_csv(S7_TKT)
        deltas = [float(x) for x in tkt_only["delta"]]
        if S7.exists():
            extra = pd.read_csv(S7)
            if "delta" in extra.columns:
                deltas = [float(x) for x in extra["delta"]]
            elif {"dense_ece", "sparse_ece"}.issubset(extra.columns):
                deltas = [
                    float(r["sparse_ece"]) - float(r["dense_ece"]) for _, r in extra.iterrows()
                ]
    ok6 = len(deltas) >= 3 and all(d > 0 for d in deltas)
    rows.append(
        {
            "Claim": "threshold sensitivity stable",
            "Dataset": "Assist",
            "Model": "T-KT/DKT",
            "Source": "S7; IJIET_FINAL_REVISION/analysis/si_threecut_tkt.csv (frequency-cut grids 20/100/500, 10/50/250, 30/150/750; not τ)",
            "Status": "VERIFIED" if ok6 else "NOT TRACEABLE",
        }
    )

    # 7. One-command rebuild from frozen summaries (C3). Not train-from-scratch.
    proc = subprocess.run(
        [sys.executable, str(REBUILD)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    LOG.write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
    ok7 = proc.returncode == 0 and "0.1136" in proc.stdout and "0.2280" in proc.stdout
    rows.append(
        {
            "Claim": "reproducibility one-command",
            "Dataset": "Assist",
            "Model": "T-KT",
            "Source": "scripts/rebuild_locked_tables.sh; scripts/p0_rebuild_locked_tables.py; IJIET_FINAL_REVISION/audit/reproduction_rebuild_locked_tables.log",
            "Status": "VERIFIED" if ok7 else "NOT TRACEABLE",
        }
    )

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Claim", "Dataset", "Model", "Source", "Status"])
        w.writeheader()
        w.writerows(rows)

    bad = [r for r in rows if r["Status"] != "VERIFIED"]
    print(f"wrote {OUT}", flush=True)
    for r in rows:
        print(f"{r['Status']}\t{r['Claim']}", flush=True)
    if bad:
        raise SystemExit(f"primary claims not VERIFIED: {[r['Claim'] for r in bad]}")
    if any(r["Status"] in {"NOT TRACEABLE", "MANUAL ONLY"} for r in rows):
        raise SystemExit("forbidden status present")


if __name__ == "__main__":
    main()
