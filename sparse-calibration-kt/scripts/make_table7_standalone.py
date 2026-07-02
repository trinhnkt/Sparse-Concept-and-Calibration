import pandas as pd
from pathlib import Path
import sys

def fmt(mean, std):
    if pd.isna(mean) or mean is None:
        return "-"
    if pd.isna(std) or std is None:
        return f"${mean:.4f}$"
    return f"${mean:.4f} \pm {std:.4f}$"

def make_table7(filepath):
    df_sens = pd.read_csv("results/tables/sensitivity_analysis.csv")
    df_sens = df_sens[df_sens['split_mode'] == 'learner_based'].copy()
    df_sens = df_sens[df_sens['model'].isin(['irt_1pl', 'dkt', 'simplekt'])].copy()
    df_sens['model_type'] = df_sens['model'].apply(lambda x: 'IRT' if x == 'irt_1pl' else 'Deep baselines')
    
    summary_sens = df_sens.groupby(['dataset', 'model_type', 'setting', 'bucket'])[['auc', 'ece']].agg(['mean', 'std']).reset_index()
    summary_sens.columns = ['dataset', 'model_type', 'setting', 'bucket', 'auc_mean', 'auc_std', 'ece_mean', 'ece_std']
    
    pivot_df = summary_sens.pivot_table(
        index=['dataset', 'setting', 'bucket'],
        columns='model_type',
        values=['auc_mean', 'auc_std', 'ece_mean', 'ece_std']
    ).reset_index()
    
    pivot_df.columns = [f"{col[1]}_{col[0]}" if col[1] else col[0] for col in pivot_df.columns]
    
    pivot_df['dataset_sort'] = pivot_df['dataset'].map({'assist2012': 0, 'junyi': 1, 'xes3g5m': 2})
    pivot_df['setting_sort'] = pivot_df['setting'].map({'Main': 0, 'Alt_1': 1, 'Alt_2': 2, 'Alt_Quantile': 3})
    pivot_df['bucket_sort'] = pivot_df['bucket'].map({'dense': 0, 'medium': 1, 'sparse': 2, 'very_sparse': 3})
    pivot_df = pivot_df.sort_values(['dataset_sort', 'setting_sort', 'bucket_sort'])
    
    tex = []
    tex.append("\\begin{table}[H]")
    tex.append("\\caption{Threshold sensitivity by dataset and model group. Deep baselines denote the mean over DKT and SimpleKT; standard deviations reflect between-baseline variation.}")
    tex.append("\\label{tab:sensitivity}")
    tex.append("\\centering")
    tex.append("\\resizebox{\\textwidth}{!}{%")
    tex.append("\\begin{tabular}{lllcccc}")
    tex.append("\\toprule")
    tex.append("& & & \\multicolumn{2}{c}{Deep baselines} & \\multicolumn{2}{c}{IRT} \\\\")
    tex.append("\\cmidrule(lr){4-5} \\cmidrule(lr){6-7}")
    tex.append("Dataset & Setting & Bucket & AUC & ECE & AUC & ECE \\\\")
    tex.append("\\midrule")
    
    last_ds = None
    last_set = None
    for _, row in pivot_df.iterrows():
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
            last_set = None
        else:
            ds_col = ""
            
        set_name = row['setting'].replace("_", "\\_")
        if set_name != last_set:
            set_col = set_name
            last_set = set_name
        else:
            set_col = ""
            
        bucket_display = row['bucket'].replace("_", "\\_")
        
        deep_auc_str = fmt(row.get('Deep baselines_auc_mean'), row.get('Deep baselines_auc_std')) if 'Deep baselines_auc_mean' in row and pd.notna(row['Deep baselines_auc_mean']) else "-"
        deep_ece_str = fmt(row.get('Deep baselines_ece_mean'), row.get('Deep baselines_ece_std')) if 'Deep baselines_ece_mean' in row and pd.notna(row['Deep baselines_ece_mean']) else "-"
        irt_auc_str = fmt(row.get('IRT_auc_mean'), row.get('IRT_auc_std')) if 'IRT_auc_mean' in row and pd.notna(row['IRT_auc_mean']) else "-"
        irt_ece_str = fmt(row.get('IRT_ece_mean'), row.get('IRT_ece_std')) if 'IRT_ece_mean' in row and pd.notna(row['IRT_ece_mean']) else "-"
        
        tex.append(f"{ds_col} & {set_col} & {bucket_display} & {deep_auc_str} & {deep_ece_str} & {irt_auc_str} & {irt_ece_str} \\\\")
        
    tex.append("\\bottomrule")
    tex.append("\\end{tabular}")
    tex.append("}")
    tex.append("\\end{table}")
    
    with open(filepath, "w") as f:
        f.write("\n".join(tex) + "\n")

out_dir = Path('springer_upload_folder/tables')
make_table7(out_dir / "tableA1_sensitivity.tex")
make_table7(out_dir / "table_vii_threshold_sensitivity_updated.tex")

out_dir = Path('jedm_upload_folder/tables')
make_table7(out_dir / "tableA1_sensitivity.tex")
make_table7(out_dir / "table_vii_threshold_sensitivity_updated.tex")

out_dir = Path('paper/tables')
make_table7(out_dir / "tableA1_sensitivity.tex")
make_table7(out_dir / "table_vii_threshold_sensitivity_updated.tex")

print("Done generating all Table 7!")
