import os
import glob
import re

tables_dir = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"
tex_files = glob.glob(os.path.join(tables_dir, "*.tex"))

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix the \begin issue first
    content = content.replace("\x08egin{tabular", "\\begin{tabular")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
