import os
import glob
import re

tables_dir = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"
tex_files = glob.glob(os.path.join(tables_dir, "*.tex"))

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    
    # Replace fixed cm widths with \textwidth in multicolumn
    content = re.sub(r'(\\multicolumn\{[0-9]+\})\{p\{[0-9\.]+cm\}\}', r'\1{p{\\textwidth}}', content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed multicolumn width in {os.path.basename(file_path)}")
