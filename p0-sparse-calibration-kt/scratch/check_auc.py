import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from pathlib import Path

def calculate_auc(y_true, p_pred):
    if len(np.unique(y_true)) >= 2:
        return roc_auc_score(y_true, p_pred)
    return np.nan

def main():
    strata_df = pd.read_csv("results/tables/kc_strata.csv")
    
    # Files to evaluate
    pred_dir = Path("results/predictions")
    files = [
        ("xes_dkt_test", "temporal", "dkt", 42),
        ("xes_simplekt_test", "temporal", "simplekt", 42),
        ("junyi_dkt_test", "temporal", "dkt", 42),
        ("junyi_dkt_test", "temporal", "simplekt", 42),
    ]
    
    for ds, split, model, seed in files:
        fpath = pred_dir / f"{ds}_{split}_{model}_seed{seed}.csv"
        if not fpath.exists():
            print(f"File not found: {fpath.name}")
            continue
            
        df = pd.read_csv(fpath)
        
        # Merge with strata to get train_freq
        ds_strata = strata_df[
            (strata_df["dataset"] == ds) & 
            (strata_df["split"] == split) & 
            (strata_df["fold"] == 0)
        ].copy()
        
        # Map kc_id to train_freq
        freq_map = dict(zip(ds_strata["kc_id"].astype(str), ds_strata["train_freq"]))
        
        df["train_freq"] = df["kc_id"].astype(str).map(freq_map).fillna(0)
        
        # Overall
        overall_auc = calculate_auc(df["y_true"], df["p_pred"])
        
        # Warm cohort (train_freq > 10)
        warm_df = df[df["train_freq"] > 10]
        warm_auc = calculate_auc(warm_df["y_true"], warm_df["p_pred"])
        
        print(f"Dataset: {ds} | Model: {model}")
        print(f"  Total events: {len(df)} | Overall AUC: {overall_auc:.4f}")
        print(f"  Warm events:  {len(warm_df)} | Warm AUC:    {warm_auc:.4f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
