import pandas as pd
import numpy as np
from pathlib import Path
from src.metrics import compute_metrics
from src.calibration_eval import compute_ece

def get_bucket(freq, thresholds):
    if freq == 0:
        return "strict_cold_start"
    elif freq < thresholds[0]:
        return "very_sparse"
    elif freq < thresholds[1]:
        return "sparse"
    elif freq < thresholds[2]:
        return "medium"
    else:
        return "dense"

settings = {
    "Main": [20, 100, 500],
    "Alt_1": [10, 50, 250],
    "Alt_2": [30, 150, 750]
}

strata_df = pd.read_csv("results/tables/kc_strata.csv")
strata_df['kc_id'] = strata_df['kc_id'].astype(str)

results = []
pred_dir = Path("results/predictions")

files_to_process = [
    ("assist2012", "irt_1pl", "assist2012_learner_based_irt_1pl_seed42_predictions_rerun.csv"),
    ("assist2012", "dkt", "assist2012_learner_based_dkt_seed42_predictions_rerun.csv"),
    ("assist2012", "simplekt", "assist2012_learner_based_simplekt_seed42_predictions_rerun.csv"),
    ("xes3g5m", "irt_1pl", "xes3g5m_learner_based_irt_1pl_seed42_predictions_rerun.csv"),
    ("xes3g5m", "dkt", "xes3g5m_learner_based_dkt_seed42_predictions_rerun.csv"),
    ("xes3g5m", "simplekt", "xes3g5m_learner_based_simplekt_seed42_predictions_rerun.csv")
]

print("Starting subset sensitivity analysis...")
for ds, model, f_name in files_to_process:
    f_path = pred_dir / f_name
    if not f_path.exists():
        f_path = pred_dir / f_name.replace("_predictions_rerun", "")
    if not f_path.exists():
        print(f"Skipping {f_path}")
        continue
        
    df = pd.read_csv(f_path)
    if df.empty: continue
    
    # Cast kc_id to string and convert float representation like "123.0" to "123"
    df['kc_id'] = df['kc_id'].astype(str).str.replace('\.0$', '', regex=True)
    
    # We are doing learner_based, fold 0 (seed 42)
    exp_strata = strata_df[(strata_df['dataset'] == ds) & (strata_df['split'] == 'learner_based') & (strata_df['fold'] == 0)].copy()
    exp_strata['kc_id'] = exp_strata['kc_id'].str.replace('\.0$', '', regex=True)
    
    for s_name, thresholds in settings.items():
        kc_to_bucket = {str(row['kc_id']): get_bucket(row['train_freq'], thresholds) for _, row in exp_strata.iterrows()}
        temp_df = df.copy()
        temp_df['bucket'] = temp_df['kc_id'].map(kc_to_bucket)
        
        # Drop unmapped ones
        temp_df = temp_df.dropna(subset=['bucket'])
        
        for bucket, b_group in temp_df.groupby('bucket'):
            m = compute_metrics(b_group['y_true'].values, b_group['p_pred'].values)
            ece, _, _, _, _ = compute_ece(b_group['y_true'].values, b_group['p_pred'].values)
            results.append({
                "dataset": ds, "split_mode": 'learner_based', "model": model, "seed": 42,
                "setting": s_name, "bucket": bucket,
                "auc": m['auc'], "ece": ece, "brier": m['rmse']**2,
                "n_events": len(b_group)
            })
            
    q = exp_strata['train_freq'].quantile([0.25, 0.5, 0.75]).values
    q = sorted(list(set(q)))
    if len(q) < 3:
        q = [q[0], q[0]+1, q[0]+2] if len(q) > 0 else [1, 2, 3]
        while len(q) < 3: q.append(q[-1]+1)
        
    kc_to_bucket_q = {str(row['kc_id']): get_bucket(row['train_freq'], q[:3]) for _, row in exp_strata.iterrows()}
    temp_df_q = df.copy()
    temp_df_q['bucket'] = temp_df_q['kc_id'].map(kc_to_bucket_q)
    temp_df_q = temp_df_q.dropna(subset=['bucket'])
    
    for bucket, b_group in temp_df_q.groupby('bucket'):
        m = compute_metrics(b_group['y_true'].values, b_group['p_pred'].values)
        ece, _, _, _, _ = compute_ece(b_group['y_true'].values, b_group['p_pred'].values)
        results.append({
            "dataset": ds, "split_mode": 'learner_based', "model": model, "seed": 42,
            "setting": "Alt_Quantile", "bucket": bucket,
            "auc": m['auc'], "ece": ece, "brier": m['rmse']**2,
            "n_events": len(b_group)
        })

print(f"Total new rows: {len(results)}")
old_df = pd.read_csv("results/tables/sensitivity_analysis.csv")
new_df = pd.DataFrame(results)
final_df = pd.concat([old_df[old_df['dataset'] == 'junyi'], new_df], ignore_index=True)
final_df.to_csv("results/tables/sensitivity_analysis.csv", index=False)
print("Saved to results/tables/sensitivity_analysis.csv")
