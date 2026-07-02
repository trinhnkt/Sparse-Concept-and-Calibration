import sys, re

def update_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace 'DeepKT' with 'Deep baselines' inside lambda
    content = content.replace("apply(lambda x: 'IRT' if x == 'irt_1pl' else 'DeepKT')", 
                              "apply(lambda x: 'IRT' if x == 'irt_1pl' else 'Deep baselines')")

    # Replace 'DeepKT' header
    content = content.replace("\\multicolumn{2}{c}{DeepKT}", "\\multicolumn{2}{c}{Deep baselines}")

    # Replace DeepKT in variable names extraction
    content = content.replace("row.get('DeepKT_auc_mean')", "row.get('Deep baselines_auc_mean')")
    content = content.replace("row.get('DeepKT_auc_std')", "row.get('Deep baselines_auc_std')")
    content = content.replace("row.get('DeepKT_ece_mean')", "row.get('Deep baselines_ece_mean')")
    content = content.replace("row.get('DeepKT_ece_std')", "row.get('Deep baselines_ece_std')")
    
    content = content.replace("['DeepKT_auc_mean']", "['Deep baselines_auc_mean']")
    content = content.replace("['DeepKT_ece_mean']", "['Deep baselines_ece_mean']")

    # Update caption
    old_cap = r"\caption{Sensitivity Analysis to KC-frequency Threshold Settings. Detailed results are separated by dataset and model group (DeepKT includes DKT and SimpleKT). Standard deviations reflect between-baseline variance.}"
    new_cap = r"\caption{Threshold sensitivity by dataset and model group. Deep baselines denote the mean over DKT and SimpleKT; standard deviations reflect between-baseline variation.}"
    content = content.replace(old_cap, new_cap)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_script('scripts/make_updated_latex_tables.py')
print("Updated scripts/make_updated_latex_tables.py")
