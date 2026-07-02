import pandas as pd
import glob
from pathlib import Path
from src.calibration_eval import compute_ece, compute_brier_decomposition
import numpy as np

def main():
    strata_df = pd.read_csv('results/tables/kc_strata.csv')
    
    # Pre-clean kc_id to string, removing .0
    strata_df['kc_id'] = strata_df['kc_id'].astype(str).str.replace('\.0$', '', regex=True)
    
    strata_map = {}
    for _, row in strata_df.iterrows():
        key = (row['dataset'], row['split'], row['kc_id'])
        strata_map[key] = row['bucket']
        
    pred_dir = Path("results/predictions")
    pred_files = glob.glob(str(pred_dir / "*temporal*.csv"))
    
    file_map = {}
    for f in pred_files:
        name = Path(f).name
        if "test" in name: continue
        
        parts = name.split('_')
        dataset = parts[0]
        if "irt_1pl" in name:
            model = "irt_1pl"
        elif "dkt" in name:
            model = "dkt"
        elif "simplekt" in name:
            model = "simplekt"
        elif "bkt" in name:
            model = "bkt"
        else:
            continue
            
        seed_str = [p for p in parts if 'seed' in p]
        if seed_str:
            seed = int(seed_str[0].replace('seed', ''))
        else:
            seed = 42
            
        file_map[(dataset, model, seed)] = f

    bucket_rows = []
    
    for (dataset, model, seed), f_path in file_map.items():
        df = pd.read_csv(f_path)
        if df.empty: continue
            
        # Clean kc_id
        df['kc_id'] = df['kc_id'].astype(str).str.replace('\.0$', '', regex=True)
        kc_ids = df['kc_id'].values
        
        buckets = []
        for kc in kc_ids:
            b = strata_map.get((dataset, 'temporal', kc), 'strict_cold_start') # missing in strata means it had 0 train freq!
            buckets.append(b)
        df['bucket'] = buckets
        
        for bucket, b_df in df.groupby('bucket'):
            b_y_true = b_df['y_true'].values.astype(int)
            b_p_pred = b_df['p_pred'].values.astype(float)
            
            b_ece, _, _, _, _ = compute_ece(b_y_true, b_p_pred)
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
    grouped = df_clean_bucket.groupby(['dataset', 'split_mode', 'model', 'bucket'])
    numeric_cols = ['n_events', 'ece', 'brier', 'uncertainty', 'reliability', 'resolution']
    
    mean_df = grouped[numeric_cols].mean()
    std_df = grouped[numeric_cols].std()
    
    summary = mean_df.copy()
    summary = summary.rename(columns={col: f"{col}_mean" for col in numeric_cols})
    
    for col in numeric_cols:
        summary[f"{col}_std"] = std_df[col].fillna(0.0)
    summary = summary.reset_index()
    
    summary['n_events'] = summary['n_events_mean']
    
    out_dir = Path("results/tables")
    summary.to_csv(out_dir / "clean_calibration_by_bucket_temporal.csv", index=False)
    print("Saved clean_calibration_by_bucket_temporal.csv")

if __name__ == "__main__":
    main()
