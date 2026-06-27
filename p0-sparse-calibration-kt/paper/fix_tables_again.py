import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

def apply_resizebox(filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any manual font sizing and tabcolsep
    content = re.sub(r'\\scriptsize|\\footnotesize|\\small|\\normalsize', '', content)
    content = re.sub(r'\\setlength\{\\tabcolsep\}\{[^\}]+\}', '', content)
    
    # Check if already wrapped in resizebox
    if r'\resizebox' not in content:
        # Wrap tabular in resizebox
        content = re.sub(r'(\\begin\{tabular\}[^\n]*\n)(.*?)(\\end\{tabular\})', 
                         r'\\resizebox{\\linewidth}{!}{\n\1\2\3\n}', 
                         content, flags=re.DOTALL)
        
    # Clean up multiple blank lines left by removals
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied resizebox to {filename}")

def apply_tabular_star(filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any manual font sizing and tabcolsep, replace with normalsize
    content = re.sub(r'\\scriptsize|\\footnotesize|\\small|\\normalsize', r'\\normalsize', content)
    content = re.sub(r'\\setlength\{\\tabcolsep\}\{[^\}]+\}', '', content)

    # Change tabular to tabular*
    if r'\begin{tabular}' in content:
        # Replace \begin{tabular}{...} with \begin{tabular*}{\linewidth}{@{\extracolsep{\fill}}...}
        content = re.sub(r'\\begin\{tabular\}\{([^\}]+)\}', 
                         r'\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}\\1}', 
                         content)
        content = re.sub(r'\\end\{tabular\}', r'\\end{tabular*}', content)

    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Applied tabular* to {filename}")

# Overflowing tables
apply_resizebox("table1_dataset_stats.tex")
apply_resizebox("table_iii_overall_results_updated.tex")
apply_resizebox("table_iv_bucket_performance_updated.tex")
apply_resizebox("table_v_calibration_by_bucket_updated.tex") # C4 is identical width to Table 5

# Too small tables
apply_tabular_star("tableA1_sensitivity.tex")
apply_tabular_star("tableA_overall_full.tex")

