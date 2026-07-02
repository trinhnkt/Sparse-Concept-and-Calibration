#!/usr/bin/env python3
import os
import glob
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import roc_auc_score

def compute_ece(y_true, p_pred, n_bins=15):
    N = len(y_true)
    if N == 0:
        return np.nan
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    ece = 0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (p_pred > bin_lower) & (p_pred <= bin_upper)
        if bin_lower == 0:
            in_bin |= (p_pred == 0)
        
        n_m = np.sum(in_bin)
        if n_m > 0:
            acc_m = np.mean(y_true[in_bin])
            conf_m = np.mean(p_pred[in_bin])
            ece += (n_m / N) * np.abs(conf_m - acc_m)
            
    return ece

def compute_brier_decomposition(y_true, p_pred, n_bins=15):
    N = len(y_true)
    if N == 0:
        return np.nan, np.nan, np.nan, np.nan
    
    y_bar = np.mean(y_true)
    unc = y_bar * (1.0 - y_bar)
    
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    rel = 0
    res = 0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (p_pred > bin_lower) & (p_pred <= bin_upper)
        if bin_lower == 0:
            in_bin |= (p_pred == 0)
            
        n_m = np.sum(in_bin)
        if n_m > 0:
            acc_m = np.mean(y_true[in_bin])
            conf_m = np.mean(p_pred[in_bin])
            rel += n_m * (conf_m - acc_m)**2
            res += n_m * (acc_m - y_bar)**2
            
    rel /= N
    res /= N
    brier = np.mean((p_pred - y_true)**2)
    return brier, unc, rel, res

def main():
    print("Recalculating Temporal Calibration metrics from rerun files...")
    
    # 1. Load KC strata mapping
    strata_path = Path("results/tables/kc_strata.csv")
    strata_df = pd.read_csv(strata_path)
    strata_df = strata_df[strata_df['dataset'].isin(['assist2012', 'junyi', 'xes3g5m'])]
    strata_df = strata_df[strata_df['split'] == 'temporal']
    
    strata_map = {}
    for _, row in strata_df.iterrows():
        key = (row['dataset'], str(row['kc_id']).replace('.0', ''))
        strata_map[key] = row['bucket']
    
    # 2. Get unique temporal files
    pred_dir = Path("results/predictions")
    pred_files = glob.glob(str(pred_dir / "*temporal*.csv"))
    
    # Map (dataset, model, seed) to file path, preferring _predictions_rerun.csv
    file_map = {}
    for f in pred_files:
        name = Path(f).name
        if "test" in name.lower() or "gpu" in name.lower():
            continue
        parts = name.replace(".csv", "").replace("_predictions_rerun", "").split("_")
        
        dataset = parts[0]
        if dataset not in ['assist2012', 'junyi', 'xes3g5m']:
            continue
            
        model = None
        seed = None
        for idx, p in enumerate(parts):
            if p in ['bkt', 'dkt', 'simplekt', 'irt', '1pl']:
                # handle irt_1pl
                if p == 'irt' and len(parts) > idx+1 and parts[idx+1] == '1pl':
                    model = 'irt' # Map to irt for output consistency
                    seed_part = parts[idx + 2]
                else:
                    model = p if p != 'irt' else 'irt' # just in case
                    seed_part = parts[idx + 1]
                if 'seed' in seed_part:
                    seed = int(seed_part.replace("seed", ""))
                break
                
        if model is None or seed is None:
            continue
            
        key = (dataset, model, seed)
        if key not in file_map:
            file_map[key] = f
        else:
            # If we already have a file, overwrite it if the current one is rerun
            if "_predictions_rerun.csv" in f:
                file_map[key] = f
                
    print(f"Found {len(file_map)} valid temporal files.")
    
    bucket_rows = []
    
    for (dataset, model, seed), f_path in file_map.items():
        print(f"Processing: {dataset} | {model} | seed {seed} from {Path(f_path).name}")
        df = pd.read_csv(f_path)
        if df.empty:
            continue
            
        df = df.dropna(subset=['y_true', 'p_pred'])
        df = df[df['kc_id'].astype(str) != "-1"]
        df = df[df['kc_id'].astype(str) != "nan"]
        
        if len(df) == 0:
            continue
            
        kc_ids = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True).values
        buckets = []
        for kc in kc_ids:
            b = strata_map.get((dataset, kc), 'strict_cold_start')
            buckets.append(b)
        df['bucket'] = buckets
        
        for bucket, b_df in df.groupby('bucket'):
            b_y_true = b_df['y_true'].values.astype(int)
            b_p_pred = b_df['p_pred'].values.astype(float)
            
            b_ece = compute_ece(b_y_true, b_p_pred)
            brier, unc, rel, res = compute_brier_decomposition(b_y_true, b_p_pred)
            
            bucket_rows.append({
                'dataset': dataset,
                'split_mode': 'temporal',
                'model': model,
                'seed': seed,
                'bucket': bucket,
                'n_events': len(b_df),
                'ece': b_ece,
                'brier': brier,
                'uncertainty': unc,
                'reliability': rel,
                'resolution': res
            })
            
    df_clean_bucket = pd.DataFrame(bucket_rows)
    
    # Generate summary across seeds
    grouped = df_clean_bucket.groupby(['dataset', 'split_mode', 'model', 'bucket'])
    numeric_cols = ['n_events', 'ece', 'brier', 'uncertainty', 'reliability', 'resolution']
    
    mean_df = grouped[numeric_cols].mean()
    std_df = grouped[numeric_cols].std()
    
    summary = pd.DataFrame()
    for col in numeric_cols:
        summary[f"{col}_mean"] = mean_df[col]
        summary[f"{col}_std"] = std_df[col].fillna(0.0)
    summary = summary.reset_index()
    
    # Also save the raw bucket-level n_events correctly just like clean_metric_per_bucket does.
    # We will rename n_events_mean to n_events
    summary['n_events'] = summary['n_events_mean']
    
    out_dir = Path("results/tables")
    summary.to_csv(out_dir / "clean_calibration_by_bucket_temporal.csv", index=False)
    print("Done! Saved clean_calibration_by_bucket_temporal.csv")

if __name__ == "__main__":
    main()
