import os

filepath = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\sections\05_discussion_limitations.tex"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace "perfectly illustrates" with "illustrates" or "demonstrates"
new_content = content.replace("perfectly illustrates", "demonstrates")

if new_content != content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed perfectly illustrates in 05_discussion_limitations.tex")
else:
    print("Not found.")
