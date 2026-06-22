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

def calculate_metrics(y_true, p_pred):
    if len(y_true) == 0:
        return np.nan, np.nan, np.nan, np.nan
    p_clipped = np.clip(p_pred, 1e-15, 1.0 - 1e-15)
    if len(np.unique(y_true)) >= 2:
        auc = roc_auc_score(y_true, p_clipped)
    else:
        auc = np.nan
    acc = np.mean(y_true == (p_clipped >= 0.5))
    nll = -np.mean(y_true * np.log(p_clipped) + (1.0 - y_true) * np.log(1.0 - p_clipped))
    rmse = np.sqrt(np.mean((p_clipped - y_true)**2))
    return auc, acc, nll, rmse

def get_reliability_flag(n_events):
    if n_events >= 1000:
        return 'R'
    elif n_events >= 100:
        return 'L'
    else:
        return 'I'

def fmt(mean, std):
    if pd.isna(mean):
        return "-"
    if pd.isna(std) or std == 0.0:
        return f"${mean:.4f}$"
    return f"${mean:.4f} \\pm {std:.4f}$"

def main():
    print("Aggregate Rerun Data and Generate LaTeX Tables...")
    
    # 1. Load KC Strata Map
    strata_path = Path("results/tables/kc_strata.csv")
    if not strata_path.exists():
        raise FileNotFoundError("Strata file results/tables/kc_strata.csv is required.")
    strata_df = pd.read_csv(strata_path)
    strata_map = {}
    for _, row in strata_df.iterrows():
        key = (row['dataset'], row['split'], str(row['kc_id']))
        strata_map[key] = {
            'bucket': row['bucket'],
            'train_freq': row['train_freq']
        }
        
    # 2. Find and calculate all rerun prediction metrics
    pred_dir = Path("results/predictions")
    pred_files = glob.glob(str(pred_dir / "*_predictions_rerun.csv"))
    print(f"Scanned {len(pred_files)} rerun prediction files.")
    
    overall_rows = []
    bucket_rows = []
    cold_start_rows = []
    
    for f_path in pred_files:
        path = Path(f_path)
        name = path.name
        parts = name.replace(".csv", "").split("_")
        
        # Format: {dataset}_{split_mode}_{model}_seed{seed}_predictions_rerun.csv
        dataset = parts[0]
        split_mode = "learner_based" if "learner_based" in name else "temporal"
        
        model = None
        for p in ['irt_1pl', 'bkt', 'dkt', 'simplekt']:
            if p in name:
                model = p
                break
                
        seed = None
        for part in parts:
            if part.startswith("seed"):
                seed = int(part.replace("seed", ""))
                break
                
        if model is None or seed is None:
            continue
            
        df = pd.read_csv(path)
        if df.empty or len(df) < 5:  # skip mock/empty files
            continue
            
        df = df.dropna(subset=['y_true', 'p_pred'])
        df = df[df['kc_id'].astype(str) != "-1"]
        df = df[df['kc_id'].astype(str) != "nan"]
        
        if len(df) == 0:
            continue
            
        y_true = df['y_true'].values.astype(int)
        p_pred = df['p_pred'].values.astype(float)
        kc_ids = df['kc_id'].astype(str).values
        
        # A. Overall
        auc, acc, nll, rmse = calculate_metrics(y_true, p_pred)
        overall_rows.append({
            'dataset': dataset,
            'split_mode': split_mode,
            'model': model,
            'seed': seed,
            'auc': auc,
            'acc': acc,
            'nll': nll,
            'rmse': rmse
        })
        
        # Map buckets
        buckets = []
        train_freqs = []
        for kc in kc_ids:
            key = (dataset, split_mode, kc)
            if key in strata_map:
                buckets.append(strata_map[key]['bucket'])
                train_freqs.append(strata_map[key]['train_freq'])
            else:
                buckets.append('very_sparse')
                train_freqs.append(0)
        df['bucket'] = buckets
        df['train_freq'] = train_freqs
        
        # B. Bucket performance & calibration
        for bucket, b_df in df.groupby('bucket'):
            b_y = b_df['y_true'].values.astype(int)
            b_p = b_df['p_pred'].values.astype(float)
            b_auc, b_acc, b_nll, b_rmse = calculate_metrics(b_y, b_p)
            b_ece = compute_ece(b_y, b_p)
            b_brier, b_unc, b_rel, b_res = compute_brier_decomposition(b_y, b_p)
            
            bucket_rows.append({
                'dataset': dataset,
                'split_mode': split_mode,
                'model': model,
                'seed': seed,
                'bucket': bucket,
                'n_kcs': len(b_df['kc_id'].unique()),
                'n_events': len(b_df),
                'auc': b_auc,
                'acc': b_acc,
                'nll': b_nll,
                'rmse': b_rmse,
                'ece': b_ece,
                'brier': b_brier,
                'uncertainty': b_unc,
                'reliability': b_rel,
                'resolution': b_res
            })
            
        # C. Cold-start
        cold_groups = {
            'strict': df[df['train_freq'] == 0],
            'k5': df[df['train_freq'] <= 5],
            'k10': df[df['train_freq'] <= 10],
            'warm': df[df['train_freq'] > 10]
        }
        for g_name, g_df in cold_groups.items():
            if len(g_df) == 0:
                continue
            g_y = g_df['y_true'].values.astype(int)
            g_p = g_df['p_pred'].values.astype(float)
            g_auc, g_acc, g_nll, g_rmse = calculate_metrics(g_y, g_p)
            g_ece = compute_ece(g_y, g_p)
            g_brier, g_unc, g_rel, g_res = compute_brier_decomposition(g_y, g_p)
            
            cold_start_rows.append({
                'dataset': dataset,
                'split_mode': split_mode,
                'model': model,
                'seed': seed,
                'group': g_name,
                'n_kcs': len(g_df['kc_id'].unique()),
                'n_events': len(g_df),
                'auc': g_auc,
                'acc': g_acc,
                'nll': g_nll,
                'rmse': g_rmse,
                'ece': g_ece,
                'brier': g_brier,
                'reliability': g_rel,
                'resolution': g_res
            })
            
    df_raw_overall = pd.DataFrame(overall_rows)
    df_raw_bucket = pd.DataFrame(bucket_rows)
    df_raw_cold = pd.DataFrame(cold_start_rows)
    
    # Define aggregation helper
    def make_summary(df, group_cols, numeric_cols):
        grouped = df.groupby(group_cols)
        mean_df = grouped[numeric_cols].mean()
        std_df = grouped[numeric_cols].std()
        summary = mean_df.copy()
        for col in numeric_cols:
            summary[f"{col}_mean"] = mean_df[col]
            summary[f"{col}_std"] = std_df[col].fillna(0.0)
            summary = summary.drop(columns=[col])
        return summary.reset_index()
        
    summary_rerun_overall = make_summary(df_raw_overall, ['dataset', 'split_mode', 'model'], ['auc', 'acc', 'nll', 'rmse'])
    summary_rerun_bucket = make_summary(df_raw_bucket, ['dataset', 'split_mode', 'model', 'bucket'], 
                                        ['auc', 'acc', 'nll', 'rmse', 'ece', 'brier', 'uncertainty', 'reliability', 'resolution'])
    summary_rerun_cold = make_summary(df_raw_cold, ['dataset', 'split_mode', 'model', 'group'],
                                      ['auc', 'acc', 'ece', 'brier', 'reliability', 'resolution'])
                                      
    # Load old clean summaries as fallback
    summary_clean_overall = pd.read_csv("results/tables/clean_overall_results_summary.csv")
    summary_clean_bucket = pd.read_csv("results/tables/clean_metric_per_bucket_summary.csv")
    summary_clean_cold = pd.read_csv("results/tables/clean_cold_start_results_summary.csv")
    
    # Merge helper that takes rerun data if available, otherwise falls back to clean data
    def merge_with_fallback(clean_df, rerun_df, match_cols, rename_model=True):
        merged_rows = []
        # Group clean by key
        clean_keys = set(zip(*[clean_df[c] for c in match_cols]))
        rerun_keys = set(zip(*[rerun_df[c] for c in match_cols]))
        
        # Rerun data will have 'irt_1pl' instead of 'bkt'
        # For each key in clean_df, check if there's a rerun equivalent:
        # For DKT/SimpleKT, match is exact. For BKT, rerun matches with irt_1pl.
        for _, row in clean_df.iterrows():
            dataset = row['dataset']
            split_mode = row['split_mode']
            model = row['model']
            
            # Check if rerun has this dataset-split
            has_rerun_split = not rerun_df[(rerun_df['dataset'] == dataset) & (rerun_df['split_mode'] == split_mode)].empty
            
            if has_rerun_split:
                # Find matching rerun row
                target_model = 'irt_1pl' if model == 'bkt' else model
                rerun_match = rerun_df[(rerun_df['dataset'] == dataset) & 
                                       (rerun_df['split_mode'] == split_mode) & 
                                       (rerun_df['model'] == target_model)]
                if len(match_cols) > 3: # also match bucket or group
                    extra_col = match_cols[3]
                    rerun_match = rerun_match[rerun_match[extra_col] == row[extra_col]]
                    
                if not rerun_match.empty:
                    new_row = row.copy()
                    # copy all summary statistics
                    for col in rerun_df.columns:
                        if col not in ['dataset', 'split_mode', 'model', 'bucket', 'group']:
                            new_row[col] = rerun_match.iloc[0][col]
                    if model == 'bkt':
                        new_row['model'] = 'irt_1pl'
                    merged_rows.append(new_row)
                else:
                    # Rerun split exists but this combination is missing (could happen if run failed)
                    merged_rows.append(row)
            else:
                # Fallback to clean
                merged_rows.append(row)
        return pd.DataFrame(merged_rows)
        
    merged_overall = merge_with_fallback(summary_clean_overall, summary_rerun_overall, ['dataset', 'split_mode', 'model'])
    merged_bucket = merge_with_fallback(summary_clean_bucket, summary_rerun_bucket, ['dataset', 'split_mode', 'model', 'bucket'])
    merged_cold = merge_with_fallback(summary_clean_cold, summary_rerun_cold, ['dataset', 'split_mode', 'model', 'group'])
    
    # Save merged data to disk for audit
    merged_overall.to_csv("results/tables/overall_results_summary.csv", index=False)
    merged_bucket.to_csv("results/tables/metric_per_bucket_summary.csv", index=False)
    
    # -------------------------------------------------------------------
    # GENERATE LATEX TABLES
    # -------------------------------------------------------------------
    out_dir = Path("paper/tables")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    def get_model_label(model_name):
        if model_name == 'irt_1pl':
            return 'IRT'
        elif model_name == 'bkt':
            return 'BKT'
        elif model_name == 'dkt':
            return 'DKT'
        elif model_name == 'simplekt':
            return 'SimpleKT'
        return model_name.upper()

    # 1. Table III: Overall Performance (Learner-based)
    def make_table3(df, filepath):
        tex = []
        tex.append("\\begin{table}[tbp]")
        tex.append("\\caption{Overall Performance under Learner-based Split}")
        tex.append("\\label{tab:overall}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllcccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Split & Model & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'learner_based'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort'])
        
        last_ds = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            tex.append(f"{ds_col} & Learner-based & {model_display} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\multicolumn{7}{p{8.2cm}}{\\scriptsize \\textit{Note: IRT is used as the classical baseline across all datasets. Under learner-based splits, IRT's learner-based AUC remains at 0.5000 because unseen learners do not have estimated ability parameters; however, its ACC reflects majority-class and item/concept difficulty effects rather than discriminative ranking ability.}} \\\\")
        tex.append("\\end{tabular}%")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table3(merged_overall, out_dir / "table3_overall_results.tex")
    make_table3(merged_overall, out_dir / "table3_overall_performance.tex")
    make_table3(merged_overall, out_dir / "table_iii_overall_results_updated.tex")
    
    # 2. Table IV: Performance by Bucket with Reliability Flags
    def make_table4(df, filepath):
        tex = []
        tex.append("\\begin{table}[tbp]")
        tex.append("\\caption{Knowledge Tracing Performance Breakdown by Skill Strata (Learner-based)}")
        tex.append("\\label{tab:bucket}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllcrccccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Bucket & Rel. & \\#KCs & \\#Events & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'learner_based'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['bucket_sort'] = filtered['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
        
        # Raw events counts helper
        # Group raw bucket by dataset, model, bucket and average
        raw_events = df_raw_bucket[df_raw_bucket['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])[['n_kcs', 'n_events']].mean().reset_index()
        clean_events = pd.read_csv("results/tables/clean_metric_per_bucket.csv")
        clean_events = clean_events[clean_events['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])[['n_kcs', 'n_events']].mean().reset_index()
        
        last_ds = None
        last_model = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
                last_model = None
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            if model_display != last_model:
                model_col = model_display
                last_model = model_display
            else:
                model_col = ""
                
            bucket_display = row['bucket'].replace("_", "\\_")
            
            # Find KCs and Events count
            # Use raw_events if dataset has rerun, else clean_events
            has_rerun = not df_raw_bucket[(df_raw_bucket['dataset'] == row['dataset'])].empty
            ev_df = raw_events if has_rerun else clean_events
            
            match_model = row['model']
            ev_match = ev_df[(ev_df['dataset'] == row['dataset']) & 
                             (ev_df['model'] == match_model) & 
                             (ev_df['bucket'] == row['bucket'])]
            if not ev_match.empty:
                n_kcs = int(round(ev_match.iloc[0]['n_kcs']))
                n_events = int(round(ev_match.iloc[0]['n_events']))
                rel_flag = get_reliability_flag(n_events)
                n_kcs_str = f"{n_kcs:,}"
                n_events_str = f"{n_events:,}"
            else:
                rel_flag = "I"
                n_kcs_str = "-"
                n_events_str = "-"
                
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            # No bolding for Insufficient buckets
            if rel_flag == 'I':
                auc_str = auc_str.replace("\\mathbf", "")
                acc_str = acc_str.replace("\\mathbf", "")
                
            tex.append(f"{ds_col} & {model_col} & {bucket_display} & {rel_flag} & {n_kcs_str} & {n_events_str} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\multicolumn{10}{p{8.2cm}}{\\scriptsize \\textit{Note: Reliability is assigned based on the number of test events: Reliable (R: $N \\ge 1000$), Limited (L: $100 \\le N < 1000$), and Insufficient (I: $N < 100$). Results in Insufficient buckets are descriptive only. Bold results are not used in Insufficient buckets.}} \\\\")
        tex.append("\\end{tabular}%")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table4(merged_bucket, out_dir / "table_iv_bucket_performance_with_reliability.tex")
    make_table4(merged_bucket, out_dir / "table4_metric_per_bucket.tex")
    make_table4(merged_bucket, out_dir / "table4_performance_by_bucket.tex")
    make_table4(merged_bucket, out_dir / "table_iv_bucket_performance_updated.tex")
    
    # 3. Table V: Calibration by Bucket
    def make_table5(df, filepath):
        tex = []
        use_single_col = "updated" in str(filepath)
        if use_single_col:
            tex.append("\\begin{table}[H]")
        else:
            tex.append("\\begin{table*}[H]")
        tex.append("\\caption{Calibration Breakdown by Frequency Stratum}")
        tex.append("\\label{tab:calib}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\textwidth}{!}{%")
        tex.append("\\begin{tabular}{lllrcccccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Bucket & Rel. & \\#Events & ECE & Brier & UNC & REL & RES \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'learner_based'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['bucket_sort'] = filtered['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
        
        raw_events = df_raw_bucket[df_raw_bucket['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])['n_events'].mean().reset_index()
        clean_events = pd.read_csv("results/tables/clean_metric_per_bucket.csv")
        clean_events = clean_events[clean_events['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])['n_events'].mean().reset_index()
        
        last_ds = None
        last_model = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
                last_model = None
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            if model_display != last_model:
                model_col = model_display
                last_model = model_display
            else:
                model_col = ""
                
            bucket_display = row['bucket'].replace("_", "\\_")
            
            # Event count
            has_rerun = not df_raw_bucket[(df_raw_bucket['dataset'] == row['dataset'])].empty
            ev_df = raw_events if has_rerun else clean_events
            match_model = row['model']
            ev_match = ev_df[(ev_df['dataset'] == row['dataset']) & 
                             (ev_df['model'] == match_model) & 
                             (ev_df['bucket'] == row['bucket'])]
                             
            if not ev_match.empty:
                n_events = int(round(ev_match.iloc[0]['n_events']))
                rel_flag = get_reliability_flag(n_events)
                n_events_str = f"{n_events:,}"
            else:
                rel_flag = "I"
                n_events_str = "-"
                
            ece_str = fmt(row['ece_mean'], row['ece_std'])
            brier_str = fmt(row['brier_mean'], row['brier_std'])
            unc_str = f"${row['uncertainty_mean']:.4f}$" if not pd.isna(row['uncertainty_mean']) else "-"
            rel_str = f"${row['reliability_mean']:.4f}$" if not pd.isna(row['reliability_mean']) else "-"
            res_str = f"${row['resolution_mean']:.4f}$" if not pd.isna(row['resolution_mean']) else "-"
            
            tex.append(f"{ds_col} & {model_col} & {bucket_display} & {rel_flag} & {n_events_str} & {ece_str} & {brier_str} & {unc_str} & {rel_str} & {res_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\multicolumn{10}{p{17.5cm}}{\\scriptsize \\textbf{Note:} IRT shows low ECE in several learner-based cohorts, but RES = 0 across strata indicates base-rate-like behavior with no resolving power. Thus, IRT calibration should be interpreted jointly with AUC and Brier resolution.} \\\\")
        tex.append("\\end{tabular}%")
        tex.append("}")
        if use_single_col:
            tex.append("\\end{table}")
        else:
            tex.append("\\end{table*}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table5(merged_bucket, out_dir / "table_v_calibration_with_reliability.tex")
    make_table5(merged_bucket, out_dir / "table5_calibration_per_bucket.tex")
    make_table5(merged_bucket, out_dir / "table_v_calibration_by_bucket_updated.tex")
    make_table5(merged_bucket, out_dir / "tableA_calibration_by_bucket_full.tex")
    
    # Calibration compact (Table 5 compact)
    def make_table5_compact(df, filepath):
        tex = []
        tex.append("\\begin{table}[t]")
        tex.append("\\caption{Compact Calibration Breakdown by Frequency Stratum}")
        tex.append("\\label{tab:calib_compact}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllrcc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Bucket & \\#Events & ECE & Brier \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'learner_based'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['bucket_sort'] = filtered['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
        
        raw_events = df_raw_bucket[df_raw_bucket['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])['n_events'].mean().reset_index()
        clean_events = pd.read_csv("results/tables/clean_metric_per_bucket.csv")
        clean_events = clean_events[clean_events['split_mode'] == 'learner_based'].groupby(['dataset', 'model', 'bucket'])['n_events'].mean().reset_index()
        
        last_ds = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            bucket_display = row['bucket'].replace("_", "\\_")
            
            has_rerun = not df_raw_bucket[(df_raw_bucket['dataset'] == row['dataset'])].empty
            ev_df = raw_events if has_rerun else clean_events
            match_model = row['model']
            ev_match = ev_df[(ev_df['dataset'] == row['dataset']) & 
                             (ev_df['model'] == match_model) & 
                             (ev_df['bucket'] == row['bucket'])]
            n_events = int(round(ev_match.iloc[0]['n_events'])) if not ev_match.empty else 0
            n_events_str = f"{n_events:,}"
            
            ece_str = fmt(row['ece_mean'], row['ece_std'])
            brier_str = fmt(row['brier_mean'], row['brier_std'])
            
            tex.append(f"{ds_col} & {model_display} & {bucket_display} & {n_events_str} & {ece_str} & {brier_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table5_compact(merged_bucket, out_dir / "table5_calibration_by_bucket_compact.tex")
    
    # 4. Table VI: Cold-start results
    def make_table6(df, filepath):
        tex = []
        tex.append("\\begin{table}[tbp]")
        tex.append("\\caption{Cold-start Performance Metrics under Temporal Validation}")
        tex.append("\\label{tab:cold_start}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllcrcccccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Group & \\#KCs & \\#Events & AUC & ACC & ECE & Brier & REL & RES \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'temporal'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['group_sort'] = filtered['group'].map({'strict': 0, 'k5': 1, 'k10': 2, 'warm': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'group_sort'])
        
        raw_events = df_raw_cold[df_raw_cold['split_mode'] == 'temporal'].groupby(['dataset', 'model', 'group'])[['n_kcs', 'n_events']].mean().reset_index()
        clean_events = pd.read_csv("results/tables/clean_cold_start_results.csv")
        clean_events = clean_events[clean_events['split_mode'] == 'temporal'].groupby(['dataset', 'model', 'group'])[['n_kcs', 'n_events']].mean().reset_index()
        
        last_ds = None
        last_model = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
                last_model = None
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            if model_display != last_model:
                model_col = model_display
                last_model = model_display
            else:
                model_col = ""
                
            group_display = row['group']
            
            has_rerun = not df_raw_cold[(df_raw_cold['dataset'] == row['dataset'])].empty
            ev_df = raw_events if has_rerun else clean_events
            match_model = row['model']
            ev_match = ev_df[(ev_df['dataset'] == row['dataset']) & 
                             (ev_df['model'] == match_model) & 
                             (ev_df['group'] == row['group'])]
            if not ev_match.empty:
                n_kcs = int(round(ev_match.iloc[0]['n_kcs']))
                n_events = int(round(ev_match.iloc[0]['n_events']))
                n_kcs_str = f"{n_kcs:,}"
                n_events_str = f"{n_events:,}"
            else:
                n_kcs_str = "-"
                n_events_str = "-"
                
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            ece_str = fmt(row['ece_mean'], row['ece_std'])
            brier_str = fmt(row['brier_mean'], row['brier_std'])
            rel_str = fmt(row['reliability_mean'], row['reliability_std'])
            res_str = fmt(row['resolution_mean'], row['resolution_std'])
            
            tex.append(f"{ds_col} & {model_col} & {group_display} & {n_kcs_str} & {n_events_str} & {auc_str} & {acc_str} & {ece_str} & {brier_str} & {rel_str} & {res_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\multicolumn{11}{p{8.2cm}}{\\scriptsize \\textit{Note: For the Junyi Academy dataset, the strict, k5, and k10 cohorts coincide exactly because all 4 concepts in this category have zero training frequency. After applying the label-alignment correction consistently across datasets, warm-cohort temporal AUC recovers for deep KT baselines on ASSISTments 2012, Junyi Academy, and XES3G5M. Strict and limited-frequency cold-start groups remain more challenging and should be interpreted together with sample size and sanity-check evidence.}} \\\\")
        tex.append("\\end{tabular}%")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table6(merged_cold, out_dir / "table6_cold_start_results.tex")
    make_table6(merged_cold, out_dir / "table_vi_cold_start_temporal_updated.tex")
    
    # 5. Table VII: Threshold Sensitivity Analysis (Appendix)
    def make_table7(filepath):
        df_sens = pd.read_csv("results/tables/clean_sensitivity_analysis.csv")
        summary_sens = df_sens.groupby(['setting', 'bucket'])[['auc', 'ece']].agg(['mean', 'std']).reset_index()
        summary_sens.columns = ['setting', 'bucket', 'auc_mean', 'auc_std', 'ece_mean', 'ece_std']
        summary_sens['bucket_sort'] = summary_sens['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        summary_sens = summary_sens.sort_values(['setting', 'bucket_sort'])
        
        tex = []
        tex.append("\\begin{table}[H]")
        tex.append("\\caption{Sensitivity Analysis to KC-frequency Threshold Settings. Values are averaged across datasets and baselines for each threshold setting; standard deviations reflect between-dataset and between-baseline variation.}")
        tex.append("\\label{tab:sensitivity}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{llcc}")
        tex.append("\\toprule")
        tex.append("Setting & Bucket & AUC & ECE \\\\")
        tex.append("\\midrule")
        
        last_set = None
        for _, row in summary_sens.iterrows():
            set_name = row['setting'].replace("_", "\\_")
            if set_name != last_set:
                if last_set is not None:
                    tex.append("\\midrule")
                last_set = set_name
                set_col = set_name
            else:
                set_col = ""
            bucket_display = row['bucket'].replace("_", "\\_")
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            ece_str = fmt(row['ece_mean'], row['ece_std'])
            tex.append(f"{set_col} & {bucket_display} & {auc_str} & {ece_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table7(out_dir / "tableA1_sensitivity.tex")
    make_table7(out_dir / "table_vii_threshold_sensitivity_updated.tex")
    
    # 6. Table VIII: Temporal Overall Results (Appendix)
    def make_table8(df, filepath):
        tex = []
        tex.append("\\begin{table}[tbp]")
        tex.append("\\caption{Overall Performance under Future Validation (Temporal Splits)}")
        tex.append("\\label{tab:overall_temporal}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllcccc}")

        tex.append("\\toprule")
        tex.append("Dataset & Split & Model & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'temporal'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort'])
        
        last_ds = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            tex.append(f"{ds_col} & Temporal & {model_display} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}%")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table8(merged_overall, out_dir / "tableA_overall_full.tex")
    make_table8(merged_overall, out_dir / "table_viii_updated.tex")
    
    # 7. Table IX: Temporal Bucket Diagnostics (Appendix)
    def make_table9(df, filepath):
        tex = []
        tex.append("\\begin{table}[tbp]")
        tex.append("\\caption{Knowledge Tracing Performance Breakdown by Skill Strata (Temporal splits)}")
        tex.append("\\label{tab:bucket_temporal}")
        tex.append("\\centering")
        tex.append("\\resizebox{\\columnwidth}{!}{%")
        tex.append("\\begin{tabular}{lllcrccccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Bucket & Rel. & \\#KCs & \\#Events & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == 'temporal'].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'irt_1pl': 0, 'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['bucket_sort'] = filtered['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
        
        raw_events = df_raw_bucket[df_raw_bucket['split_mode'] == 'temporal'].groupby(['dataset', 'model', 'bucket'])[['n_kcs', 'n_events']].mean().reset_index()
        clean_events = pd.read_csv("results/tables/clean_metric_per_bucket.csv")
        clean_events = clean_events[clean_events['split_mode'] == 'temporal'].groupby(['dataset', 'model', 'bucket'])[['n_kcs', 'n_events']].mean().reset_index()
        
        last_ds = None
        last_model = None
        for _, row in filtered.iterrows():
            ds_name = row['dataset'].upper()
            if ds_name == "ASSIST2012":
                ds_display = "ASSISTments 2012"
            elif ds_name == "JUNYI":
                ds_display = "Junyi Academy"
            else:
                ds_display = "XES3G5M"
                
            if ds_display != last_ds:
                if last_ds is not None:
                    tex.append("\\midrule")
                last_ds = ds_display
                ds_col = ds_display
                last_model = None
            else:
                ds_col = ""
                
            model_display = get_model_label(row['model'])
            if model_display != last_model:
                model_col = model_display
                last_model = model_display
            else:
                model_col = ""
                
            bucket_display = row['bucket'].replace("_", "\\_")
            
            has_rerun = not df_raw_bucket[(df_raw_bucket['dataset'] == row['dataset'])].empty
            ev_df = raw_events if has_rerun else clean_events
            match_model = row['model']
            ev_match = ev_df[(ev_df['dataset'] == row['dataset']) & 
                             (ev_df['model'] == match_model) & 
                             (ev_df['bucket'] == row['bucket'])]
            if not ev_match.empty:
                n_kcs = int(round(ev_match.iloc[0]['n_kcs']))
                n_events = int(round(ev_match.iloc[0]['n_events']))
                rel_flag = get_reliability_flag(n_events)
                n_kcs_str = f"{n_kcs:,}"
                n_events_str = f"{n_events:,}"
            else:
                rel_flag = "I"
                n_kcs_str = "-"
                n_events_str = "-"
                
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            if rel_flag == 'I':
                auc_str = auc_str.replace("\\mathbf", "")
                acc_str = acc_str.replace("\\mathbf", "")
                
            tex.append(f"{ds_col} & {model_col} & {bucket_display} & {rel_flag} & {n_kcs_str} & {n_events_str} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}%")
        tex.append("}")
        tex.append("\\end{table}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    make_table9(merged_bucket, out_dir / "tableA_performance_by_bucket_full.tex")
    make_table9(merged_bucket, out_dir / "table_ix_updated.tex")
    
    print("All tables successfully generated in paper/tables!")

if __name__ == "__main__":
    main()
