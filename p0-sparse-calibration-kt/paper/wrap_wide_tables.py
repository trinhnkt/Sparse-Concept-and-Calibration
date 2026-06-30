import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

wide_tables = [
    "table1_dataset_stats.tex",
    "table_iii_overall_results_updated.tex",
    "table_iv_bucket_performance_updated.tex",
    "table_vi_cold_start_temporal_updated.tex",
    "tableA_overall_full.tex",
    "tableA_performance_by_bucket_full.tex",
    "table_v_calibration_by_bucket_updated.tex",
    "table_xi_temporal_calibration_breakdown.tex"
]

for tfile in wide_tables:
    fpath = os.path.join(folder, tfile)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "\\resizebox" not in content:
        # We need to wrap \begin{tabular} ... \end{tabular}
        # But wait! There might be multiple tabulars? No, just 1 usually.
        # Let's replace \begin{tabular} with \resizebox{\linewidth}{!}{ \begin{tabular}
        content = content.replace("\\begin{tabular}", "\\resizebox{\\linewidth}{!}{\n\\begin{tabular}")
        
        # And replace \end{tabular} with \end{tabular} }
        content = content.replace("\\end{tabular}", "\\end{tabular}\n}")
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Wrapped {tfile} with resizebox")

