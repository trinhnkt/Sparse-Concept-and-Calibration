import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.finditer(r'.{0,30}Appendix.{0,30}', content)
                for m in matches:
                    print(f"[{file}] {m.group(0)}")
