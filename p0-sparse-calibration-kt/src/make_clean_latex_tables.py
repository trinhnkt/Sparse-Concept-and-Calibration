#!/usr/bin/env python3
"""
src/make_clean_latex_tables.py

Generate highly professional, beautifully formatted, double-column and single-column
LaTeX tables for the peer-review revision of the P0 paper.
"""

import pandas as pd
from pathlib import Path

def fmt(mean, std):
    if pd.isna(mean):
        return "-"
    if pd.isna(std) or std == 0.0:
        return f"${mean:.4f}$"
    return f"${mean:.4f} \\pm {std:.4f}$"

def main():
    print("Initializing Generation of Clean LaTeX Tables...")
    out_dir = Path("paper/tables")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. Table II: Dataset Statistics (table1_dataset_stats.tex)
    # -------------------------------------------------------------
    # Columns: Dataset, Split Mode, #Learners, #Items, #KCs, #Interactions, #Train, #Valid, #Test, Avg. Seq. Len.
    stats_data = [
        # assist2012
        {"dataset": "ASSISTments 2012", "split": "Learner-based", "users": "27,806", "items": "52,672", "kcs": "265", "total": "2,657,490", "train": "1,865,217", "valid": "258,123", "test": "534,150", "avg_seq": "95.57"},
        {"dataset": "ASSISTments 2012", "split": "Temporal", "users": "27,806", "items": "52,672", "kcs": "265", "total": "2,657,490", "train": "1,860,242", "valid": "265,749", "test": "531,499", "avg_seq": "95.57"},
        # junyi
        {"dataset": "Junyi Academy", "split": "Learner-based", "users": "71,014", "items": "25,784", "kcs": "1,326", "total": "16,215,567", "train": "11,373,990", "valid": "1,572,555", "test": "3,269,022", "avg_seq": "228.34"},
        {"dataset": "Junyi Academy", "split": "Temporal", "users": "71,014", "items": "25,784", "kcs": "1,326", "total": "16,215,567", "train": "11,350,896", "valid": "1,621,556", "test": "3,243,115", "avg_seq": "228.34"},
        # xes3g5m
        {"dataset": "XES3G5M", "split": "Learner-based", "users": "18,066", "items": "7,653", "kcs": "866", "total": "7,953,709", "train": "5,572,247", "valid": "792,317", "test": "1,589,145", "avg_seq": "440.26"},
        {"dataset": "XES3G5M", "split": "Temporal", "users": "18,066", "items": "7,653", "kcs": "866", "total": "7,953,709", "train": "5,567,596", "valid": "795,370", "test": "1,590,743", "avg_seq": "440.26"}
    ]
    
    tex_stats = []
    tex_stats.append("\\begin{table*}[t]")
    tex_stats.append("\\caption{Dataset and Splitting Cohort Statistics}")
    tex_stats.append("\\label{tab:datasets}")
    tex_stats.append("\\centering")
    tex_stats.append("\\small")
    tex_stats.append("\\begin{tabular}{llrrrrrrrr}")
    tex_stats.append("\\toprule")
    tex_stats.append("Dataset & Split Mode & \\#Learners & \\#Items & \\#KCs & \\#Interactions & \\#Train & \\#Valid & \\#Test & Avg. Seq. Len. \\\\")
    tex_stats.append("\\midrule")
    for row in stats_data:
        tex_stats.append(f"{row['dataset']} & {row['split']} & {row['users']} & {row['items']} & {row['kcs']} & {row['total']} & {row['train']} & {row['valid']} & {row['test']} & {row['avg_seq']} \\\\")
    tex_stats.append("\\bottomrule")
    tex_stats.append("\\end{tabular}")
    tex_stats.append("\\end{table*}")
    
    with open(out_dir / "table1_dataset_stats.tex", "w") as f:
        f.write("\n".join(tex_stats) + "\n")
        
    # -------------------------------------------------------------
    # 2. Table I: Leakage Audit (table2_leakage_audit.tex)
    # -------------------------------------------------------------
    # Standard Leakage table using \path{} for files
    tex_leakage = []
    tex_leakage.append("\\begin{table*}[t]")
    tex_leakage.append("\\caption{Rigorous Multi-Channel Leakage Prevention Checklist}")
    tex_leakage.append("\\label{tab:leakage}")
    tex_leakage.append("\\centering")
    tex_leakage.append("\\small")
    tex_leakage.append("\\begin{tabular}{lllll}")
    tex_leakage.append("\\toprule")
    tex_leakage.append("Channel & Description & Evidence File & Status & Notes \\\\")
    tex_leakage.append("\\midrule")
    tex_leakage.append("L1 & Split leakage (user overlap, temporal order) & \\path{logs/split_audit.csv} & PASS & No user overlap or temporal inversions detected \\\\")
    tex_leakage.append("L2 & Preprocessing leakage (transformations fit scope) & \\path{src/preprocess.py} & PASS & No global normalization detected \\\\")
    tex_leakage.append("L3 & Q-matrix / KC mapping leakage & \\path{data/processed/assist2012/kc_map.json} & PASS & Static mapping from dataset \\\\")
    tex_leakage.append("L4 & Sparse-bucket leakage & \\path{results/tables/kc_strata.csv} & PASS & Bucket assignment is strictly based on training frequency \\\\")
    tex_leakage.append("L5 & Calibration leakage (test-based tuning) & \\path{src/baseline_runner.py} & PASS & No post-hoc tuning on test set \\\\")
    tex_leakage.append("L6 & Hyperparameter leakage (model selection) & \\path{src/baseline_runner.py} & PASS & Validation-based selection only \\\\")
    tex_leakage.append("L7 & Cold-start leakage & \\path{src/three_split_constructor.py} & PASS & Classification uses train\\_freq only \\\\")
    tex_leakage.append("\\bottomrule")
    tex_leakage.append("\\end{tabular}")
    tex_leakage.append("\\end{table*}")
    
    with open(out_dir / "table2_leakage_audit.tex", "w") as f:
        f.write("\n".join(tex_leakage) + "\n")
        
    # -------------------------------------------------------------
    # 3. Table III: Overall Performance (table3_overall_results.tex & tableA_overall_full.tex)
    # -------------------------------------------------------------
    df_overall = pd.read_csv("results/tables/clean_overall_results_summary.csv")
    
    def generate_overall_tex(df, split_mode, title, label, filepath, is_appendix=False):
        tex = []
        if is_appendix:
            tex.append("\\begin{table*}[h]")
        else:
            tex.append("\\begin{table*}[t]")
        tex.append(f"\\caption{{{title}}}")
        tex.append(f"\\label{{{label}}}")
        tex.append("\\centering")
        tex.append("\\small")
        tex.append("\\begin{tabular}{lllcccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Split Mode & Model & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == split_mode].copy()
        
        # Sort values for consistency
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'bkt': 0, 'dkt': 1, 'simplekt': 2})
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
                
            model_display = row['model'].upper() if row['model'] != "simplekt" else "SimpleKT"
            
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            tex.append(f"{ds_col} & {row['split_mode']} & {model_display} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("\\end{table*}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    generate_overall_tex(df_overall, "learner_based", "Overall Performance under Population Cross-Validation (Learner-based)", "tab:overall", out_dir / "table3_overall_results.tex")
    generate_overall_tex(df_overall, "temporal", "Overall Performance under Future Validation (Temporal Splits) [Appendix]", "tab:overall_temporal", out_dir / "tableA_overall_full.tex", is_appendix=True)
    
    # -------------------------------------------------------------
    # 4. Table IV: Performance by Bucket (table4_metric_per_bucket.tex & tableA_performance_by_bucket_full.tex)
    # -------------------------------------------------------------
    df_bucket = pd.read_csv("results/tables/clean_metric_per_bucket_summary.csv")
    
    def generate_bucket_tex(df, split_mode, title, label, filepath):
        tex = []
        tex.append("\\begin{table*}[t]")
        tex.append(f"\\caption{{{title}}}")
        tex.append(f"\\label{{{label}}}")
        tex.append("\\centering")
        tex.append("\\small")
        tex.append("\\begin{tabular}{lllccccc}")
        tex.append("\\toprule")
        tex.append("Dataset & Model & Bucket & AUC & ACC & NLL & RMSE \\\\")
        tex.append("\\midrule")
        
        filtered = df[df['split_mode'] == split_mode].copy()
        filtered['dataset_sort'] = filtered['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
        filtered['model_sort'] = filtered['model'].map({'bkt': 0, 'dkt': 1, 'simplekt': 2})
        filtered['bucket_sort'] = filtered['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
        filtered = filtered.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
        
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
                
            model_display = row['model'].upper() if row['model'] != "simplekt" else "SimpleKT"
            if model_display != last_model:
                model_col = model_display
                last_model = model_display
            else:
                model_col = ""
                
            bucket_display = row['bucket'].replace("_", "\\_")
            
            auc_str = fmt(row['auc_mean'], row['auc_std'])
            acc_str = fmt(row['acc_mean'], row['acc_std'])
            nll_str = fmt(row['nll_mean'], row['nll_std'])
            rmse_str = fmt(row['rmse_mean'], row['rmse_std'])
            
            tex.append(f"{ds_col} & {model_col} & {bucket_display} & {auc_str} & {acc_str} & {nll_str} & {rmse_str} \\\\")
            
        tex.append("\\bottomrule")
        tex.append("\\end{tabular}")
        tex.append("\\end{table*}")
        
        with open(filepath, "w") as f:
            f.write("\n".join(tex) + "\n")
            
    generate_bucket_tex(df_bucket, "learner_based", "Knowledge Tracing Performance Breakdown by Skill Strata (Learner-based)", "tab:bucket", out_dir / "table4_metric_per_bucket.tex")
    generate_bucket_tex(df_bucket, "temporal", "Knowledge Tracing Performance Breakdown by Skill Strata (Temporal splits) [Appendix]", "tab:bucket_temporal", out_dir / "tableA_performance_by_bucket_full.tex")
    
    # -------------------------------------------------------------
    # 5. Table V: Calibration by Bucket (table5_calibration_per_bucket.tex)
    # -------------------------------------------------------------
    # Calibration ECE and Brier score decomposition (UNC, REL, RES)
    df_calib = pd.read_csv("results/tables/clean_calibration_by_bucket.csv")
    df_calib = df_calib[df_calib['split_mode'] == 'learner_based'].copy()
    
    df_calib['dataset_sort'] = df_calib['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
    df_calib['model_sort'] = df_calib['model'].map({'bkt': 0, 'dkt': 1, 'simplekt': 2})
    df_calib['bucket_sort'] = df_calib['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
    df_calib = df_calib.sort_values(['dataset_sort', 'model_sort', 'bucket_sort'])
    
    tex_cal = []
    tex_cal.append("\\begin{table}[t]")
    tex_cal.append("\\caption{Calibration Breakdown and Brier Score Decomposition}")
    tex_cal.append("\\label{tab:calib}")
    tex_cal.append("\\centering")
    tex_cal.append("\\resizebox{\\columnwidth}{!}{%")
    tex_cal.append("\\begin{tabular}{lllccccc}")
    tex_cal.append("\\toprule")
    tex_cal.append("Dataset & Model & Bucket & ECE & Brier & UNC & REL & RES \\\\")
    tex_cal.append("\\midrule")
    
    last_ds = None
    last_model = None
    for _, row in df_calib.iterrows():
        ds_name = row['dataset'].upper()
        if ds_name == "ASSIST2012":
            ds_display = "A12"
        elif ds_name == "JUNYI":
            ds_display = "Junyi"
        else:
            ds_display = "XES"
            
        if ds_display != last_ds:
            if last_ds is not None:
                tex_cal.append("\\midrule")
            last_ds = ds_display
            ds_col = ds_display
            last_model = None
        else:
            ds_col = ""
            
        model_display = row['model'].upper() if row['model'] != "simplekt" else "SimpleKT"
        if model_display != last_model:
            model_col = model_display
            last_model = model_display
        else:
            model_col = ""
            
        bucket_display = row['bucket'].replace("_", "\\_")
        
        ece_str = fmt(row['ece_mean'], row['ece_std'])
        brier_str = fmt(row['brier_mean'], row['brier_std'])
        unc_str = f"${row['uncertainty_mean']:.4f}$" if not pd.isna(row['uncertainty_mean']) else "-"
        rel_str = f"${row['reliability_mean']:.4f}$" if not pd.isna(row['reliability_mean']) else "-"
        res_str = f"${row['resolution_mean']:.4f}$" if not pd.isna(row['resolution_mean']) else "-"
        
        tex_cal.append(f"{ds_col} & {model_col} & {bucket_display} & {ece_str} & {brier_str} & {unc_str} & {rel_str} & {res_str} \\\\")
        
    tex_cal.append("\\bottomrule")
    tex_cal.append("\\end{tabular}")
    tex_cal.append("}")
    tex_cal.append("\\end{table}")
    
    with open(out_dir / "table5_calibration_per_bucket.tex", "w") as f:
        f.write("\n".join(tex_cal) + "\n")
        
    # -------------------------------------------------------------
    # 6. Table VI: Cold-start Results (table6_cold_start_results.tex)
    # -------------------------------------------------------------
    df_cold = pd.read_csv("results/tables/clean_cold_start_results_summary.csv")
    df_cold = df_cold[df_cold['split_mode'] == 'temporal'].copy()
    
    df_cold['dataset_sort'] = df_cold['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
    df_cold['model_sort'] = df_cold['model'].map({'bkt': 0, 'dkt': 1, 'simplekt': 2})
    df_cold['group_sort'] = df_cold['group'].map({'strict': 0, 'k5': 1, 'k10': 2, 'warm': 3})
    df_cold = df_cold.sort_values(['dataset_sort', 'model_sort', 'group_sort'])
    
    tex_cold = []
    tex_cold.append("\\begin{table}[h]")
    tex_cold.append("\\caption{Cold-start Performance Metrics under Temporal Validation}")
    tex_cold.append("\\label{tab:cold_start}")
    tex_cold.append("\\centering")
    tex_cold.append("\\resizebox{\\columnwidth}{!}{%")
    tex_cold.append("\\begin{tabular}{lllcccccc}")
    tex_cold.append("\\toprule")
    tex_cold.append("Dataset & Model & Group & AUC & ACC & ECE & Brier & REL & RES \\\\")
    tex_cold.append("\\midrule")
    
    last_ds = None
    last_model = None
    for _, row in df_cold.iterrows():
        ds_name = row['dataset'].upper()
        if ds_name == "ASSIST2012":
            ds_display = "A12"
        elif ds_name == "JUNYI":
            ds_display = "Junyi"
        else:
            ds_display = "XES"
            
        if ds_display != last_ds:
            if last_ds is not None:
                tex_cold.append("\\midrule")
            last_ds = ds_display
            ds_col = ds_display
            last_model = None
        else:
            ds_col = ""
            
        model_display = row['model'].upper() if row['model'] != "simplekt" else "SimpleKT"
        if model_display != last_model:
            model_col = model_display
            last_model = model_display
        else:
            model_col = ""
            
        group_display = row['group']
        
        auc_str = fmt(row['auc_mean'], row['auc_std'])
        acc_str = fmt(row['acc_mean'], row['acc_std'])
        ece_str = fmt(row['ece_mean'], row['ece_std'])
        brier_str = fmt(row['brier_mean'], row['brier_std'])
        rel_str = fmt(row['reliability_mean'], row['reliability_std'])
        res_str = fmt(row['resolution_mean'], row['resolution_std'])
        
        tex_cold.append(f"{ds_col} & {model_col} & {group_display} & {auc_str} & {acc_str} & {ece_str} & {brier_str} & {rel_str} & {res_str} \\\\")
        
    tex_cold.append("\\bottomrule")
    tex_cold.append("\\end{tabular}")
    tex_cold.append("}")
    tex_cold.append("\\end{table}")
    
    with open(out_dir / "table6_cold_start_results.tex", "w") as f:
        f.write("\n".join(tex_cold) + "\n")
        
    # -------------------------------------------------------------
    # 7. Table A1: Sensitivity Analysis (tableA1_sensitivity.tex)
    # -------------------------------------------------------------
    df_sens = pd.read_csv("results/tables/clean_sensitivity_analysis.csv")
    # Group by setting and bucket to generate Mean ± Std
    summary_sens = df_sens.groupby(['setting', 'bucket'])[['auc', 'ece']].agg(['mean', 'std']).reset_index()
    summary_sens.columns = ['setting', 'bucket', 'auc_mean', 'auc_std', 'ece_mean', 'ece_std']
    
    summary_sens['bucket_sort'] = summary_sens['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
    summary_sens = summary_sens.sort_values(['setting', 'bucket_sort'])
    
    tex_sens = []
    tex_sens.append("\\begin{table}[h]")
    tex_sens.append("\\caption{Sensitivity Analysis to Bin Count and Binning Strategies}")
    tex_sens.append("\\label{tab:sensitivity}")
    tex_sens.append("\\centering")
    tex_sens.append("\\resizebox{\\columnwidth}{!}{%")
    tex_sens.append("\\begin{tabular}{llcc}")
    tex_sens.append("\\toprule")
    tex_sens.append("Setting & Bucket & AUC & ECE \\\\")
    tex_sens.append("\\midrule")
    
    last_set = None
    for _, row in summary_sens.iterrows():
        set_name = row['setting'].replace("_", "\\_")
        if set_name != last_set:
            if last_set is not None:
                tex_sens.append("\\midrule")
            last_set = set_name
            set_col = set_name
        else:
            set_col = ""
            
        bucket_display = row['bucket'].replace("_", "\\_")
        auc_str = fmt(row['auc_mean'], row['auc_std'])
        ece_str = fmt(row['ece_mean'], row['ece_std'])
        
        tex_sens.append(f"{set_col} & {bucket_display} & {auc_str} & {ece_str} \\\\")
        
    tex_sens.append("\\bottomrule")
    tex_sens.append("\\end{tabular}")
    tex_sens.append("}")
    tex_sens.append("\\end{table}")
    
    with open(out_dir / "tableA1_sensitivity.tex", "w") as f:
        f.write("\n".join(tex_sens) + "\n")
        
    print("Flawless LaTeX Tables generated successfully under paper/tables/")

if __name__ == "__main__":
    main()
