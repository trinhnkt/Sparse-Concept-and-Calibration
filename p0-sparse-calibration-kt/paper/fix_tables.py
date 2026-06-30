import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

# 1. Remove FloatBarriers
for fname in ["sections/04_experiments.tex", "appendix/appendix_a_sensitivity.tex"]:
    fpath = os.path.join(folder, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("\\FloatBarrier\n", "")
    content = content.replace("\\FloatBarrier", "")
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Removed FloatBarriers from {fname}")

# 2. Fix Tables: Remove maxsizebox/resizebox and use scriptsize/tabcolsep
tables_dir = os.path.join(folder, "tables")
for root, dirs, files in os.walk(tables_dir):
    for file in files:
        if file.endswith('.tex'):
            fpath = os.path.join(root, file)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove \maxsizebox{\linewidth}{0.9\textheight}{
            content = re.sub(r'\\maxsizebox\{\\linewidth\}\{0\.9\\textheight\}\{', '', content)
            # Remove \resizebox{\linewidth}{!}{
            content = re.sub(r'\\resizebox\{\\linewidth\}\{!\}\{', '', content)
            
            # Remove the closing brace of the box: it is usually right before \end{table}
            # We look for \end{tabular}\n}% or \end{tabular}\n}
            content = re.sub(r'\\end\{tabular\}\s*\}\%?', r'\\end{tabular}', content)
            
            # Insert \scriptsize and \setlength{\tabcolsep}{3pt} right after \centering
            if "\\centering" in content and "\\scriptsize" not in content and "\\small" not in content:
                content = content.replace("\\centering", "\\centering\n\\scriptsize\n\\setlength{\\tabcolsep}{3pt}")
            elif "\\centering" in content and "\\small" in content:
                # If it already has small, upgrade to scriptsize
                content = content.replace("\\small", "\\scriptsize\n\\setlength{\\tabcolsep}{3pt}")
                
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed table: {file}")

print("Done fixing tables and floats.")
