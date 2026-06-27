import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

adjustments = {
    "table1_dataset_stats.tex": (r"\small", r"4pt"),
    "table_iii_overall_results_updated.tex": (r"\small", r"4pt"),
    "table_iv_bucket_performance_updated.tex": (r"\footnotesize", r"3pt"),
    "tableA1_sensitivity.tex": (r"\small", r"4pt"),
    "tableA_overall_full.tex": (r"\small", r"4pt"),
    "table_v_calibration_by_bucket_updated.tex": (r"\footnotesize", r"3pt")
}

for filename, (font_size, tabcolsep) in adjustments.items():
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Escape backslash for replacement string
    repl_font_size = font_size.replace('\\', '\\\\')
    
    content = re.sub(r'\\scriptsize|\\footnotesize|\\small', repl_font_size, content)
    
    content = re.sub(r'\\setlength\{\\tabcolsep\}\{[^\}]+\}', f'\\\\setlength{{\\\\tabcolsep}}{{{tabcolsep}}}', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename} with {font_size} and {tabcolsep}")
