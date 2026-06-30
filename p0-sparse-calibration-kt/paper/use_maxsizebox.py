import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

# Add adjustbox to main
main_file = os.path.join(folder, "main_springer_traditional.tex")
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()

if "\\usepackage{adjustbox}" not in content:
    content = content.replace("\\usepackage{graphicx}", "\\usepackage{graphicx}\n\\usepackage{adjustbox}")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added adjustbox to main_springer_traditional.tex")

main_compact = os.path.join(folder, "main_springer_compact.tex")
with open(main_compact, 'r', encoding='utf-8') as f:
    content = f.read()

if "\\usepackage{adjustbox}" not in content:
    content = content.replace("\\usepackage{graphicx}", "\\usepackage{graphicx}\n\\usepackage{adjustbox}")
    with open(main_compact, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added adjustbox to main_springer_compact.tex")

# Replace resizebox with maxsizebox
for root, dirs, files in os.walk(os.path.join(folder, "tables")):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # replace \resizebox{\linewidth}{!}{ with \maxsizebox{\linewidth}{0.9\textheight}{
            new_content = content.replace(r'\resizebox{\linewidth}{!}{', r'\maxsizebox{\linewidth}{0.9\textheight}{')
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Replaced resizebox with maxsizebox in {file}")
