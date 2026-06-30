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

for root, dirs, files in os.walk(folder):
    for tfile in files:
        if tfile.endswith('.tex'):
            fpath = os.path.join(root, tfile)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove resizebox
            content = re.sub(r'\\resizebox\{\\linewidth\}\{!\}\{\s*', '', content)
            
            # Remove closing brace of resizebox
            content = re.sub(r'\\end\{tabular\}\s*\}\%?', r'\\end{tabular}', content)
            
            if tfile in wide_tables:
                # Force tiny and 1pt padding
                content = content.replace("\\scriptsize", "\\tiny")
                content = content.replace("\\setlength{\\tabcolsep}{3pt}", "\\setlength{\\tabcolsep}{1.5pt}")
                
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Processed {tfile}")

