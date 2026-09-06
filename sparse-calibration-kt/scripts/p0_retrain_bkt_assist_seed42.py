#!/usr/bin/env python3
"""P0 D: pyBKT on ASSISTments 2012 learner-based fold 0, seed 42.

Does not overwrite T-KT locked ECE/FAR cells. Official pyKT simpleKT is a
separate pipeline (pyKT data format) and is not launched from this file.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from pyBKT.models import Model as BKTModel

ROOT = Path(__file__).resolve().parents[1]
TRAIN = ROOT / "data/processed/assist2012/splits/learner_based/fold_0/train.csv"
TEST = ROOT / "data/processed/assist2012/splits/learner_based/fold_0/test.csv"
OUT = ROOT / "results/predictions/assist2012_learner_based_bkt_seed42_official.csv"
LOG = ROOT / "logs/p0_retrain_bkt_assist_seed42.log"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not TRAIN.exists() or not TEST.exists():
        raise SystemExit(f"missing {TRAIN} or {TEST}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    print(f"load train {TRAIN}", flush=True)
    train = pd.read_csv(TRAIN, usecols=["user_id", "kc_id", "correct"])
    test = pd.read_csv(TEST, usecols=["user_id", "kc_id", "correct"])
    train = train.dropna(subset=["user_id", "kc_id", "correct"])
    test = test.dropna(subset=["user_id", "kc_id", "correct"])
    train["skill_name"] = train["kc_id"].astype(str)
    test["skill_name"] = test["kc_id"].astype(str)
    bkt_train = train[["user_id", "skill_name", "correct"]]
    bkt_test = test[["user_id", "skill_name", "correct"]].copy()
    print(f"train rows={len(bkt_train)} test rows={len(bkt_test)}", flush=True)
    model = BKTModel(seed=42)
    model.fit(data=bkt_train)
    preds = model.predict(data=bkt_test)
    if isinstance(preds, dict):
        col = preds.get("correct_predictions", preds.get("state_predictions"))
        bkt_test = bkt_test.copy()
        bkt_test["p"] = col
    else:
        bkt_test = preds
    bkt_test.to_csv(OUT, index=False)
    print(f"wrote {OUT} rows={len(bkt_test)}", flush=True)


if __name__ == "__main__":
    main()
