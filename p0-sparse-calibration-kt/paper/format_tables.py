import os
import glob
import re

tables_dir = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"
tex_files = glob.glob(os.path.join(tables_dir, "*.tex"))

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    
    # Remove existing sizing commands
    content = re.sub(r'\\small\s*', '', content)
    content = re.sub(r'\\footnotesize\s*', '', content)
    content = re.sub(r'\\scriptsize\s*', '', content)
    content = re.sub(r'\\setlength\{\\tabcolsep\}\{[^\}]*\}\s*', '', content)

    # Insert \scriptsize and \setlength{\tabcolsep}{3pt} right before \begin{tabular...
    # We want to do this inside the table environment so it is locally scoped.
    # We match \begin{tabular} or \begin{tabularx}
    
    # Check if the table has more than 5 columns (rough heuristic by counting & in a row or looking at column spec)
    # Actually, let's just apply \scriptsize and \setlength{\tabcolsep}{3pt} to ALL tables except maybe very small ones,
    # or just all of them to be safe against overflows. The user requested no overflows.
    # Let's apply \footnotesize and \setlength{\tabcolsep}{3pt} for better readability, and \scriptsize for the very wide ones.
    
    is_wide = "table_iv_bucket_performance" in file_path or "table_v_calibration_by_bucket" in file_path or "tableA_performance_by_bucket" in file_path or "table_xi_temporal" in file_path
    
    size_cmd = r'\\scriptsize' if is_wide else r'\\footnotesize'
    tabcol_cmd = r'\\setlength{\\tabcolsep}{2.5pt}' if is_wide else r'\\setlength{\\tabcolsep}{4pt}'
    
    replacement = f"{size_cmd}\n{tabcol_cmd}\n\\begin{{tabular"
    content = re.sub(r'\\begin\{tabular', replacement, content)
    
    # tabularx handling
    replacement_x = f"{size_cmd}\n{tabcol_cmd}\n\\begin{{tabularx"
    content = re.sub(r'\\begin\{tabularx', replacement_x, content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Formatted {os.path.basename(file_path)}")
