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
    y_true_bkt = dfs['irt_1pl']['y_true'].values
    y_true_dkt = dfs['dkt']['y_true'].values
    y_true_skt = dfs['simplekt']['y_true'].values
    
    # check lengths and values
    if not (len(y_true_bkt) == len(y_true_dkt) == len(y_true_skt)):
        print(f"[{ds}] Length mismatch! BKT:{len(y_true_bkt)}, DKT:{len(y_true_dkt)}, SKT:{len(y_true_skt)}")
        continue
        
    if not (np.array_equal(y_true_bkt, y_true_dkt) and np.array_equal(y_true_bkt, y_true_skt)):
        print(f"[{ds}] y_true values do not align perfectly. Sorting by some index if exists...")
        # Since we just have them, let's assume they might not be aligned.
        # But if they are from the same split and same seed, they should be aligned.
        # Let's check if there's an index column we can align by.
        # BKT might drop NaNs or something? Wait, BKT predictions are generated separately.
        # If lengths are equal but y_true not equal, let's check alignment columns.
        cols = ['user_id', 'item_id', 'timestamp']
        if all(c in dfs['irt_1pl'].columns for c in cols):
            for m in MODELS:
                dfs[m] = dfs[m].sort_values(cols).reset_index(drop=True)
            y_true_bkt = dfs['irt_1pl']['y_true'].values
            y_true_dkt = dfs['dkt']['y_true'].values
            y_true_skt = dfs['simplekt']['y_true'].values
            if not (np.array_equal(y_true_bkt, y_true_dkt) and np.array_equal(y_true_bkt, y_true_skt)):
                print(f"[{ds}] Still not aligned after sorting! Skipping.")
                continue
        else:
            print(f"[{ds}] Not aligned and no alignment columns found. Skipping.")
            continue
            
    print(f"[{ds}] Successfully aligned. Running DeLong...")
    
    y = y_true_bkt
    p_bkt = dfs['irt_1pl']['p_pred'].values
    p_dkt = dfs['dkt']['p_pred'].values
    p_skt = dfs['simplekt']['p_pred'].values
        
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
