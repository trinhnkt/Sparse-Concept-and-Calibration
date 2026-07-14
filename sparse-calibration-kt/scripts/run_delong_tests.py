import pandas as pd
import numpy as np
import os
from pathlib import Path
from compare_auc_delong_xu import delong_roc_test

PRED_DIR = Path("results/predictions")
OUT_DIR = Path("results/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = ["assist2012", "junyi", "xes3g5m"]
MODELS = ["irt_1pl", "dkt", "simplekt"]
SEED = "42"

def load_preds(dataset, model):
    filename = f"{dataset}_learner_based_{model}_seed{SEED}_predictions_rerun.csv"
    path = PRED_DIR / filename
    if not path.exists():
        print(f"Warning: {path} not found.")
        return None
    df = pd.read_csv(path)
    if 'y_true' not in df.columns and 'correct' in df.columns:
        df = df.rename(columns={'correct': 'y_true'})
    return df

results = []
ALPHA_BONFERRONI = 0.05 / 9

for ds in DATASETS:
    dfs = {m: load_preds(ds, m) for m in MODELS}
    
    # Check if any is missing
    missing = [m for m, df in dfs.items() if df is None]
    if missing:
        print(f"[{ds}] Missing files for: {missing}. Skipping.")
        continue
    
    # Ensure alignment
    cols = ['user_id', 'item_id', 'timestamp']
    if all(c in df.columns for df in dfs.values() for c in cols):
        for m in MODELS:
            dfs[m] = dfs[m].sort_values(['user_id', 'item_id', 'timestamp', 'kc_id'])
            dfs[m]['dup_idx'] = dfs[m].groupby(['user_id', 'item_id', 'timestamp', 'kc_id']).cumcount()
            dfs[m]['instance_id'] = dfs[m]['user_id'].astype(str) + "_" + dfs[m]['item_id'].astype(str) + "_" + dfs[m]['timestamp'].astype(str) + "_" + dfs[m]['kc_id'].astype(str) + "_" + dfs[m]['dup_idx'].astype(str)

            
        # Inner join all 3 dfs to get exact intersection
        merged = pd.merge(dfs['irt_1pl'], dfs['dkt'], on='instance_id', suffixes=('_irt', '_dkt'))
        merged = pd.merge(merged, dfs['simplekt'].rename(columns={'y_true': 'y_true_skt', 'p_pred': 'p_pred_skt'}), on='instance_id')
        
        y = merged['y_true_irt'].values
        p_bkt = merged['p_pred_irt'].values
        p_dkt = merged['p_pred_dkt'].values
        p_skt = merged['p_pred_skt'].values
        
        print(f"[{ds}] Successfully aligned. Intersection N: {len(merged)}")
    else:
        print(f"[{ds}] Missing alignment columns! Skipping.")
        continue
        
    comparisons = [
        ('irt_1pl', 'dkt', p_bkt, p_dkt),
        ('irt_1pl', 'simplekt', p_bkt, p_skt),
        ('dkt', 'simplekt', p_dkt, p_skt)
    ]
    
    for m1, m2, p1, p2 in comparisons:
        # compare_auc_delong_xu returns log10(p-value), we use delong_roc_test from it or similar, let's see.
        # wait, compare_auc_delong_xu usually returns 10 ** log10_pvalue
        try:
            log10_p = delong_roc_test(y, p1, p2)
            p_val = 10 ** log10_p[0][0]
        except Exception as e:
            print(f"Error in DeLong {m1} vs {m2}: {e}")
            p_val = np.nan
            
        from sklearn.metrics import roc_auc_score
        auc1 = roc_auc_score(y, p1)
        auc2 = roc_auc_score(y, p2)
        
        results.append({
            'dataset': ds,
            'split': 'learner_based',
            'comparison': f"{m1.upper()} vs {m2.upper()}",
            'model_1': m1.upper(),
            'model_2': m2.upper(),
            'auc_model_1': round(auc1, 4),
            'auc_model_2': round(auc2, 4),
            'delta_auc': round(abs(auc1 - auc2), 4),
            'raw_p_value': p_val,
            'bonferroni_alpha': ALPHA_BONFERRONI,
            'significant_after_bonferroni': bool(p_val < ALPHA_BONFERRONI) if not np.isnan(p_val) else False,
            'n_test_events': len(y),
            'note': 'IRT model predictions have cold-start constraint (unseen users AUC=0.5)' if 'irt_1pl' in [m1, m2] else ''
        })

df_res = pd.DataFrame(results)
out_csv = OUT_DIR / "delong_overall_auc.csv"
df_res.to_csv(out_csv, index=False)
print(f"\nSaved results to {out_csv}")
