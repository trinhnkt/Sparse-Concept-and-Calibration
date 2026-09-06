#!/usr/bin/env python3
"""Queue remaining P0 D retrains: stable BKT + official simpleKT.

Seed→fold (learner_based): 42→0, 2024→1, 2025→2, 2026→3, 2027→4.
Skips finished prediction CSVs. Does not edit the manuscript.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 2024, 2025, 2026, 2027)
DATASETS = ("assist2012", "xes3g5m", "junyi")  # Junyi last (largest)


def pred_path(dataset: str, model: str, seed: int) -> Path:
    tag = "bkt_stable" if model == "bkt" else "simplekt_official"
    return ROOT / "results/predictions" / f"{dataset}_learner_based_{tag}_seed{seed}.csv"


def jobs(model: str):
    out = []
    for ds in DATASETS:
        for seed in SEEDS:
            fold = SEEDS.index(seed)
            out.append((ds, seed, fold))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["bkt", "simplekt"], required=True)
    ap.add_argument("--datasets", default="", help="Comma list to subset, e.g. junyi")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    script = (
        ROOT / "scripts/p0_retrain_bkt_stable.py"
        if args.model == "bkt"
        else ROOT / "scripts/p0_retrain_official_simplekt.py"
    )
    allow = {x.strip() for x in args.datasets.split(",") if x.strip()}
    failed = 0
    for ds, seed, fold in jobs(args.model):
        if allow and ds not in allow:
            continue
        dest = pred_path(ds, args.model, seed)
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"SKIP {args.model} {ds} seed={seed} fold={fold}", flush=True)
            continue
        extra = []
        if args.model == "simplekt" and ds == "junyi":
            extra = ["--batch-size", "4"]
        cmd = [
            sys.executable,
            str(script),
            "--dataset",
            ds,
            "--split",
            "learner_based",
            "--fold",
            str(fold),
            "--seed",
            str(seed),
            *extra,
        ]
        print(f"RUN {args.model} {ds} seed={seed} fold={fold}", flush=True)
        r = subprocess.run(cmd, cwd=str(ROOT))
        if r.returncode != 0:
            failed += 1
            print(f"FAIL {args.model} {ds} seed={seed} code={r.returncode}", flush=True)
    print(f"QUEUE DONE {args.model} failed={failed}", flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
