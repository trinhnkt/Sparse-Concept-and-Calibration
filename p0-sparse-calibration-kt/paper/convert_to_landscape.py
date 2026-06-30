import os

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
        
    # Convert to sidewaystable
    content = content.replace("\\begin{table}[htbp]", "\\begin{sidewaystable}[htbp]")
    content = content.replace("\\begin{table}[H]", "\\begin{sidewaystable}[htbp]")
    content = content.replace("\\end{table}", "\\end{sidewaystable}")
    
    # Restore font and padding for better aesthetics since landscape has plenty of room
    content = content.replace("\\scriptsize", "\\footnotesize")
    content = content.replace("\\setlength{\\tabcolsep}{1pt}", "\\setlength{\\tabcolsep}{3pt}")
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Converted {tfile} to sidewaystable")
