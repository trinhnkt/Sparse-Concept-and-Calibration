#!/usr/bin/env python3
"""
scripts/create_new_folds.py

Creates fold_3 (seed 2026) and fold_4 (seed 2027) for learner-based splits
across all 3 datasets: assist2012, junyi, xes3g5m.

Usage:
    python scripts/create_new_folds.py
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))

# New folds to create: {fold_index: shuffle_seed}
NEW_FOLDS = {3: 2026, 4: 2027}

DATASETS = {
    "assist2012": {
        "processed_data_path": project_root / "data/processed/assist2012/interactions.csv",
        "split_ratios": {"valid": 0.1, "test": 0.2},
    },
    "junyi": {
        "processed_data_path": project_root / "data/processed/junyi/interactions.csv",
        "split_ratios": {"valid": 0.1, "test": 0.2},
    },
    "xes3g5m": {
        "processed_data_path": project_root / "data/processed/xes3g5m/interactions.csv",
        "split_ratios": {"valid": 0.1, "test": 0.2},
    },
}


def save_split(df, dataset, mode, fold, name):
    output_dir = project_root / f"data/processed/{dataset}/splits/{mode}/fold_{fold}"
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{name}.csv"
    df.to_csv(out_path, index=False)
    print(f"      Saved {name}.csv ({len(df):,} rows) -> {out_path}")


def create_learner_based_split(df, dataset, fold, seed, ratios):
    """
    Create a learner-based split:
    - shuffle users with given seed
    - 20% test users, 10% valid users, rest train users
    """
    users = list(df['user_id'].dropna().unique())
    np.random.seed(seed)
    np.random.shuffle(users)

    n_users = len(users)
    n_test = int(n_users * ratios.get('test', 0.2))
    n_valid = int(n_users * ratios.get('valid', 0.1))

    test_users = set(users[:n_test])
    valid_users = set(users[n_test:n_test + n_valid])
    train_users = set(users[n_test + n_valid:])

    train_df = df[df['user_id'].isin(train_users)]
    valid_df = df[df['user_id'].isin(valid_users)]
    test_df  = df[df['user_id'].isin(test_users)]

    print(f"    Users -> train: {len(train_users):,} | valid: {len(valid_users):,} | test: {len(test_users):,}")
    print(f"    Rows  -> train: {len(train_df):,} | valid: {len(valid_df):,} | test: {len(test_df):,}")

    save_split(train_df, dataset, "learner_based", fold, "train")
    save_split(valid_df, dataset, "learner_based", fold, "valid")
    save_split(test_df,  dataset, "learner_based", fold, "test")

    return train_df, valid_df, test_df


def main():
    for dataset, cfg in DATASETS.items():
        print(f"\n{'='*55}")
        print(f"Dataset: {dataset.upper()}")
        print(f"{'='*55}")

        data_path = cfg["processed_data_path"]
        if not data_path.exists():
            print(f"  [ERROR] interactions.csv not found at {data_path}")
            continue

        print(f"  Loading {data_path.name} ...")
        df = pd.read_csv(data_path)
        print(f"  Loaded {len(df):,} rows, {df['user_id'].nunique():,} unique users")

        for fold, seed in NEW_FOLDS.items():
            # Skip if fold already exists
            fold_dir = project_root / f"data/processed/{dataset}/splits/learner_based/fold_{fold}"
            if (fold_dir / "train.csv").exists():
                print(f"\n  [SKIP] fold_{fold} already exists at {fold_dir}")
                continue

            print(f"\n  Creating fold_{fold} (shuffle seed={seed}) ...")
            create_learner_based_split(df, dataset, fold, seed, cfg["split_ratios"])
            print(f"  fold_{fold} created successfully.")

    print(f"\n{'='*55}")
    print("All new folds created!")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
