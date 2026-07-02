import pandas as pd
import numpy as np
from pathlib import Path
import glob
from src.metrics import compute_metrics
from src.calibration_eval import compute_ece

def get_bucket(freq, thresholds):
    if freq == 0:
        return 'strict_cold_start'
    elif freq < thresholds[0]:
        return 'very_sparse'
    elif freq < thresholds[1]:
        return 'sparse'
    elif freq < thresholds[2]:
        return 'medium'
    else:
        return 'dense'

def main():
    pred_dir = Path('results/predictions')
    strata_path = Path('results/tables/kc_strata.csv')
    
    strata_df = pd.read_csv(strata_path)
    strata_df['kc_id'] = strata_df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True)
    
    pred_files = glob.glob(str(pred_dir / '*.csv'))
    
    file_map = {}
    for f in pred_files:
        name = Path(f).name
        if 'test' in name or 'gpu' in name:
            continue
        
        dataset = name.split('_')[0]
        if 'learner_based' in name:
            split_mode = 'learner_based'
        elif 'temporal' in name:
            split_mode = 'temporal'
        else:
            continue
            
        model = None
        for p in ['irt_1pl', 'dkt', 'simplekt', 'bkt']:
            if p in name:
                model = p
                break
                
        if not model:
            continue
        
        seed = 42
        import re
        seed_match = re.search(r'seed(\d+)', name)
        if seed_match:
            seed = int(seed_match.group(1))
                
        key = (dataset, split_mode, model, seed)
        
        if key not in file_map:
            file_map[key] = f
        else:
            if 'rerun' in f:
                file_map[key] = f

    settings = {
        'Main': [20, 100, 500],
        'Alt_1': [10, 50, 250],
        'Alt_2': [30, 150, 750],
    }
    
    results = []
    print(f'Running sensitivity analysis for {len(file_map)} valid prediction files...')
    
    for (dataset, split_mode, model, seed), f_path in sorted(file_map.items()):
        df = pd.read_csv(f_path)
        if df.empty:
            continue
        
        df['kc_id'] = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True)
        
        fold_idx = {42: 0, 2024: 0, 123: 1, 2025: 1, 2026: 2, 2027: 3}.get(seed, 0)
        
        exp_strata = strata_df[(strata_df['dataset'] == dataset) & 
                               (strata_df['split'] == split_mode) & 
                               (strata_df['fold'] == (fold_idx if split_mode == 'learner_based' else 0))]
                               
        if exp_strata.empty:
            continue
        
        kc_freq_map = dict(zip(exp_strata['kc_id'].astype(str), exp_strata['train_freq']))
        
        for s_name, thresholds in settings.items():
            df['bucket'] = df['kc_id'].apply(lambda k: get_bucket(kc_freq_map.get(k, 0), thresholds))
            
            for bucket, b_df in df.groupby('bucket'):
                b_y_true = b_df['y_true'].values.astype(int)
                b_p_pred = b_df['p_pred'].values.astype(float)
                
                try:
                    metrics_dict = compute_metrics(b_y_true, b_p_pred)
                    auc_val = metrics_dict.get('auc', np.nan)
                    ece_val, _, _, _, _ = compute_ece(b_y_true, b_p_pred)
                except Exception as e:
                    auc_val = np.nan
                    ece_val = np.nan
                    
                results.append({
                    'dataset': dataset,
                    'split_mode': split_mode,
                    'model': model,
                    'seed': seed,
                    'setting': s_name,
                    'bucket': bucket,
                    'auc': auc_val,
                    'ece': ece_val,
                })
                
    out_df = pd.DataFrame(results)
    out_df.to_csv('results/tables/sensitivity_analysis.csv', index=False)
    non_nan = out_df[out_df['auc'].notna()]
    print(f'Saved sensitivity_analysis.csv: {len(out_df)} rows, {len(non_nan)} non-NaN AUC')

if __name__ == '__main__':
    main()
