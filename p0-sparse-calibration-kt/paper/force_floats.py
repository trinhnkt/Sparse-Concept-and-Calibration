import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

# 1. Add \usepackage{float} to main_springer_traditional.tex
main_file = os.path.join(folder, "main_springer_traditional.tex")
with open(main_file, 'r', encoding='utf-8') as f:
    content = f.read()

if "\\usepackage{float}" not in content:
    content = content.replace("\\usepackage{graphicx}", "\\usepackage{graphicx}\n\\usepackage{float}")
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added float package to main.")

# 2. Force [H] for all tables and figures
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # replace \begin{table}[something] with \begin{table}[H]
            new_content = re.sub(r'\\begin\{table\}\[[a-zA-Z!]*\]', r'\\begin{table}[H]', content)
            # if no bracket was present, add [H]
            new_content = re.sub(r'\\begin\{table\}(?!\s*\[)', r'\\begin{table}[H]', new_content)
            
            # replace \begin{figure}[something] with \begin{figure}[H]
            new_content = re.sub(r'\\begin\{figure\}\[[a-zA-Z!]*\]', r'\\begin{figure}[H]', new_content)
            # if no bracket was present, add [H]
            new_content = re.sub(r'\\begin\{figure\}(?!\s*\[)', r'\\begin{figure}[H]', new_content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Forced [H] in {file}")
