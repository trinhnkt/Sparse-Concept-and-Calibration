import os
import glob
import re

tables_dir = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"
tex_files = glob.glob(os.path.join(tables_dir, "*.tex"))

for file_path in tex_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    # Remove \begin{adjustbox}{max width=\textwidth} or similar
    content = re.sub(r'\\begin\{adjustbox\}\{[^\}]*\}', '', content)
    # Remove \end{adjustbox}
    content = re.sub(r'\\end\{adjustbox\}', '', content)
    # Remove \resizebox{\textwidth}{!}{
    content = re.sub(r'\\resizebox\{[^\}]*\}\{[^\}]*\}\{%?', '', content)
    
    # Fix the trailing } that was meant for resizebox or adjustbox
    # Usually it's after \end{tabular} or \end{tabular}%
    # It looks like \end{tabular} \n } or \end{tabular}% \n }
    content = re.sub(r'(\\end\{tabular\*?\}[^\n]*\n*)\}', r'\1', content)

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {os.path.basename(file_path)}")
