import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

print("Checking label positions...")
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check order of caption and label
                cap_idx = content.find(r'\caption')
                lab_idx = content.find(r'\label')
                
                if cap_idx != -1 and lab_idx != -1:
                    if lab_idx < cap_idx:
                        print(f"WARNING: Label before caption in {file}")
                    else:
                        pass
                elif lab_idx != -1 and cap_idx == -1:
                    print(f"WARNING: Label without caption in {file}")
print("Done.")
