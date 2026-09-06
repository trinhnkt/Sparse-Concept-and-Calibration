#!/usr/bin/env python3
"""Stable 4-parameter BKT (Corbett & Anderson 1995) with Laplace-smoothed EM.

pyBKT 1.4.1 is known-degenerate on these logs (prior=NaN, p=0). This script
does not call pyBKT. It does not overwrite T-KT ECE/FAR locks or the manuscript.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score

ROOT = Path(__file__).resolve().parents[1]

EPS = 1e-4
CLIP = (1e-3, 1.0 - 1e-3)
SMOOTH = 1.0
DEFAULT = dict(pL=0.3, pT=0.1, pG=0.2, pS=0.1)


def _clip(x: float) -> float:
    return float(np.clip(x, CLIP[0], CLIP[1]))


def _emit(y: int, pG: float, pS: float) -> tuple[float, float]:
    # P(obs=y | unknown), P(obs=y | known)
    if y == 1:
        return pG, 1.0 - pS
    return 1.0 - pG, pS


def fit_skill(seqs: list[np.ndarray], max_iter: int = 25) -> dict[str, float]:
    pL, pT, pG, pS = DEFAULT["pL"], DEFAULT["pT"], DEFAULT["pG"], DEFAULT["pS"]
    if not seqs:
        return dict(DEFAULT)
    n_obs = int(sum(len(s) for s in seqs))
    if n_obs < 8:
        return dict(DEFAULT)

    for _ in range(max_iter):
        c_l0 = c_l1 = SMOOTH
        c_t01 = c_t00 = SMOOTH
        c_g1 = c_g0 = SMOOTH
        c_s0 = c_s1 = SMOOTH
        for y in seqs:
            T = len(y)
            if T == 0:
                continue
            alpha = np.zeros((T, 2))
            e0, e1 = _emit(int(y[0]), pG, pS)
            alpha[0, 0] = (1.0 - pL) * e0
            alpha[0, 1] = pL * e1
            scale = alpha[0].sum() + EPS
            alpha[0] /= scale
            scales = [scale]
            for t in range(1, T):
                e0, e1 = _emit(int(y[t]), pG, pS)
                a0 = alpha[t - 1, 0] * (1.0 - pT)
                a1 = alpha[t - 1, 0] * pT + alpha[t - 1, 1]
                alpha[t, 0] = a0 * e0
                alpha[t, 1] = a1 * e1
                s = alpha[t].sum() + EPS
                alpha[t] /= s
                scales.append(s)
            beta = np.ones((T, 2))
            for t in range(T - 2, -1, -1):
                e0, e1 = _emit(int(y[t + 1]), pG, pS)
                beta[t, 0] = (1.0 - pT) * e0 * beta[t + 1, 0] + pT * e1 * beta[t + 1, 1]
                beta[t, 1] = e1 * beta[t + 1, 1]
                beta[t] /= scales[t + 1] + EPS
            gamma = alpha * beta
            gamma /= gamma.sum(axis=1, keepdims=True) + EPS
            c_l0 += gamma[0, 0]
            c_l1 += gamma[0, 1]
            for t in range(T - 1):
                e0, e1 = _emit(int(y[t + 1]), pG, pS)
                xi01 = alpha[t, 0] * pT * e1 * beta[t + 1, 1]
                xi00 = alpha[t, 0] * (1.0 - pT) * e0 * beta[t + 1, 0]
                z = xi01 + xi00 + EPS
                c_t01 += xi01 / z
                c_t00 += xi00 / z
            unk, knw = gamma[:, 0], gamma[:, 1]
            c_g1 += float((unk * (y == 1)).sum())
            c_g0 += float((unk * (y == 0)).sum())
            c_s0 += float((knw * (y == 0)).sum())
            c_s1 += float((knw * (y == 1)).sum())
        pL = _clip(c_l1 / (c_l0 + c_l1))
        pT = _clip(c_t01 / (c_t01 + c_t00))
        pG = _clip(c_g1 / (c_g0 + c_g1))
        pS = _clip(c_s0 / (c_s0 + c_s1))
    return dict(pL=pL, pT=pT, pG=pG, pS=pS)


def predict_seq(y: np.ndarray, par: dict[str, float]) -> np.ndarray:
    pL, pT, pG, pS = par["pL"], par["pT"], par["pG"], par["pS"]
    out = np.empty(len(y), dtype=float)
    p_know = pL
    for t, yt in enumerate(y):
        out[t] = p_know * (1.0 - pS) + (1.0 - p_know) * pG
        like_u, like_k = _emit(int(yt), pG, pS)
        post_k = p_know * like_k
        post_u = (1.0 - p_know) * like_u
        p_know = post_k / (post_k + post_u + EPS)
        p_know = p_know + (1.0 - p_know) * pT
    return out


def load_split(dataset: str, split: str, fold: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = ROOT / "data/processed" / dataset / "splits" / split / f"fold_{fold}"
    train = pd.read_csv(base / "train.csv", usecols=["user_id", "kc_id", "timestamp", "correct"])
    test = pd.read_csv(base / "test.csv")
    train = train.dropna(subset=["user_id", "kc_id", "correct"])
    test = test.dropna(subset=["user_id", "kc_id", "correct"])
    train["correct"] = train["correct"].astype(int)
    test["correct"] = test["correct"].astype(int)
    train = train.sort_values(["user_id", "kc_id", "timestamp"])
    test = test.sort_values(["user_id", "kc_id", "timestamp"])
    return train, test


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="assist2012")
    ap.add_argument("--split", default="learner_based")
    ap.add_argument("--fold", type=int, default=0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-skills", type=int, default=0)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    np.random.seed(args.seed)

    train, test = load_split(args.dataset, args.split, args.fold)
    skills = sorted(train["kc_id"].unique())
    if args.max_skills:
        skills = skills[: args.max_skills]
    print(f"train={len(train)} test={len(test)} skills={len(skills)}", flush=True)

    params: dict = {}
    for i, sk in enumerate(skills, 1):
        sub = train.loc[train["kc_id"] == sk]
        seqs = [g["correct"].to_numpy(dtype=int) for _, g in sub.groupby("user_id", sort=False)]
        params[sk] = fit_skill(seqs)
        if i % 25 == 0 or i == len(skills):
            print(f"  fit {i}/{len(skills)}", flush=True)

    p_pred = np.full(len(test), 0.5, dtype=float)
    idx = test.index.to_numpy()
    test_work = test.reset_index(drop=True)
    for (uid, sk), g in test_work.groupby(["user_id", "kc_id"], sort=False):
        par = params.get(sk, DEFAULT)
        pred = predict_seq(g["correct"].to_numpy(dtype=int), par)
        p_pred[g.index.to_numpy()] = pred

    out = test.copy()
    # test was sorted; restore original row order via merge on a key if needed
    out["p_pred"] = p_pred
    out["y_true"] = out["correct"]
    out["dataset"] = args.dataset
    out["split_mode"] = args.split
    out["model"] = "bkt_stable"
    out["seed"] = args.seed
    pred_path = (
        ROOT
        / "results/predictions"
        / f"{args.dataset}_{args.split}_bkt_stable_seed{args.seed}.csv"
    )
    pred_path.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "dataset",
        "split_mode",
        "model",
        "seed",
        "user_id",
        "item_id",
        "kc_id",
        "timestamp",
        "y_true",
        "p_pred",
    ]
    keep = [c for c in cols if c in out.columns]
    out[keep].to_csv(pred_path, index=False)

    y = out["y_true"].to_numpy()
    p = out["p_pred"].to_numpy()
    auc = float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else float("nan")
    brier = float(brier_score_loss(y, p))
    nuniq = int(pd.Series(p).nunique())
    summary = {
        "dataset": args.dataset,
        "split": args.split,
        "fold": args.fold,
        "seed": args.seed,
        "n": int(len(out)),
        "auc": auc,
        "brier": brier,
        "p_unique": nuniq,
        "p_min": float(p.min()),
        "p_max": float(p.max()),
        "p_mean": float(p.mean()),
        "implementation": "local_4param_BKT_laplace_EM",
        "not_pyBKT": True,
        "wrote": str(pred_path),
    }
    sum_path = ROOT / "results/reports" / f"p0_bkt_stable_{args.dataset}_seed{args.seed}.json"
    sum_path.parent.mkdir(parents=True, exist_ok=True)
    sum_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)
    if not (nuniq > 20 and 0.52 <= auc <= 0.90):
        print("WARNING: BKT metrics look weak or unexpected; do not write into the manuscript.", flush=True)


if __name__ == "__main__":
    main()
