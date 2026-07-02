import pandas as pd
import numpy as np
from pathlib import Path
import glob
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

def main():
    pred_dir = Path("results/predictions")
    strata_path = Path("results/tables/kc_strata.csv")
    
    strata_df = pd.read_csv(strata_path)
    # Preclean kc_id in strata_df
    strata_df['kc_id'] = strata_df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    # We only care about learner_based and temporal
    pred_files = glob.glob(str(pred_dir / "*.csv"))
    
    # Filter files: prefer rerun over original
    # Group by base name
    file_map = {}
    for f in pred_files:
        name = Path(f).name
        if "test" in name or "gpu" in name: continue
        
        # Determine dataset, model, seed, split from name
        parts = name.replace(".csv", "").replace("_predictions_rerun", "").split("_")
        
        dataset = parts[0]
        if "learner_based" in name:
            split_mode = "learner_based"
        elif "temporal" in name:
            split_mode = "temporal"
        else:
            continue
            
        model = None
        for p in ['irt_1pl', 'dkt', 'simplekt', 'bkt']:
            if p in name:
                model = p
                break
                
        if not model: continue
        
        seed = 42
        for p in parts:
            if 'seed' in p:
                seed = int(p.replace('seed', ''))
                break
                
        key = (dataset, split_mode, model, seed)
        
        if key not in file_map:
            file_map[key] = f
        else:
            # If we already have a file, prefer rerun
            if "rerun" in f:
                file_map[key] = f

    settings = {
        "Main": [20, 100, 500],
        "Alt_1": [10, 50, 250],
        "Alt_2": [30, 150, 750]
    }
    
    results = []
    print(f"Running sensitivity analysis for {len(file_map)} valid prediction files...")
    
    for (dataset, split_mode, model, seed), f_path in file_map.items():
        df = pd.read_csv(f_path)
        if df.empty: continue
        
        # Clean kc_id
        df['kc_id'] = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True)
        
        # Filter strata
        # We need the strata for this dataset and split_mode.
        # But wait, learner_based has folds? The strata_df doesn't differentiate seed directly, 
        # it uses fold. Seed 42 -> Fold 0.
        fold_idx = 0
        if seed in [42, 2024]: fold_idx = 0
        elif seed in [123, 2025]: fold_idx = 1
        elif seed in [2026]: fold_idx = 2
        elif seed in [2027]: fold_idx = 3
        else: fold_idx = 0 # fallback
        
        exp_strata = strata_df[(strata_df['dataset'] == dataset) & 
                               (strata_df['split'] == split_mode) & 
                               (strata_df['fold'] == (fold_idx if split_mode == 'learner_based' else 0))]
                               
        if exp_strata.empty: continue
        
        kc_freq_map = dict(zip(exp_strata['kc_id'].astype(str), exp_strata['train_freq']))
        
        for s_name, thresholds in settings.items():
            df['bucket'] = df['kc_id'].apply(lambda k: get_bucket(kc_freq_map.get(k, 0), thresholds))
            
            # Now compute metrics
            for bucket, b_df in df.groupby('bucket'):
                b_y_true = b_df['y_true'].values.astype(int)
                b_p_pred = b_df['p_pred'].values.astype(float)
                
                # We need compute_metrics which returns auc, acc, nll, rmse
                try:
                    auc, acc, nll, rmse = compute_metrics(b_y_true, b_p_pred)
                    ece, _, _, _, _ = compute_ece(b_y_true, b_p_pred)
                except Exception as e:
                    auc, acc, nll, rmse, ece = np.nan, np.nan, np.nan, np.nan, np.nan
                    
                results.append({
                    'dataset': dataset,
                    'split_mode': split_mode,
                    'model': model,
                    'seed': seed,
                    'setting': s_name,
                    'bucket': bucket,
                    'auc': auc,
                    'ece': ece
                })
                
    out_df = pd.DataFrame(results)
    out_df.to_csv("results/tables/sensitivity_analysis.csv", index=False)
    print("Saved clean sensitivity_analysis.csv")

if __name__ == "__main__":
    main()
