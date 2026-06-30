import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"
files_to_fix = [
    "table1_dataset_stats.tex",
    "table_iii_overall_results_updated.tex",
    "tableA_overall_full.tex"
]

for tfile in files_to_fix:
    fpath = os.path.join(folder, tfile)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove adjustbox
    content = re.sub(r'\\begin\{adjustbox\}\{[^\}]*\}\s*', '', content)
    content = re.sub(r'\\end\{tabular\}\s*\\end\{adjustbox\}', r'\\end{tabular}', content)
    
    # Tighten padding slightly to prevent overflow
    content = content.replace("\\setlength{\\tabcolsep}{3pt}", "\\setlength{\\tabcolsep}{1pt}")
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {tfile}")
