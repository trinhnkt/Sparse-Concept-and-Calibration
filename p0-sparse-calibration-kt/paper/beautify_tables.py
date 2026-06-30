import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

short_wide = [
    "table1_dataset_stats.tex",
    "table_iii_overall_results_updated.tex",
    "tableA_overall_full.tex"
]

long_wide = [
    "table_iv_bucket_performance_updated.tex",
    "table_vi_cold_start_temporal_updated.tex",
    "tableA_performance_by_bucket_full.tex",
    "table_v_calibration_by_bucket_updated.tex",
    "table_xi_temporal_calibration_breakdown.tex"
]

for root, dirs, files in os.walk(folder):
    for tfile in files:
        if tfile.endswith('.tex'):
            fpath = os.path.join(root, tfile)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reset everything back to a clean state first
            # 1. Remove \tiny and \setlength{\tabcolsep}{1.5pt}
            content = content.replace("\\tiny", "\\scriptsize")
            content = content.replace("\\setlength{\\tabcolsep}{1.5pt}", "\\setlength{\\tabcolsep}{3pt}")
            
            # 2. If it's a short_wide table, we wrap in adjustbox safely
            if tfile in short_wide:
                if "\\begin{adjustbox}" not in content:
                    content = content.replace("\\begin{tabular}", "\\begin{adjustbox}{max width=\\linewidth}\n\\begin{tabular}")
                    content = content.replace("\\end{tabular}", "\\end{tabular}\n\\end{adjustbox}")
            
            # 3. If it's a long_wide table, we convert to sidewaystable
            if tfile in long_wide:
                # Remove adjustbox if present from previous attempts
                content = re.sub(r'\\begin\{adjustbox\}\{[^\}]*\}\s*', '', content)
                content = re.sub(r'\\end\{tabular\}\s*\\end\{adjustbox\}', r'\\end{tabular}', content)
                
                # Convert table to sidewaystable
                content = content.replace("\\begin{table}[htbp]", "\\begin{sidewaystable}[htbp]")
                content = content.replace("\\begin{table}[H]", "\\begin{sidewaystable}[htbp]")
                content = content.replace("\\end{table}", "\\end{sidewaystable}")
                
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Beautified {tfile}")

