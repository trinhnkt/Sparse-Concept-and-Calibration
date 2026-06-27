import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

labels = set()
refs = set()

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                found_labels = re.findall(r'\\label\{([^\}]+)\}', content)
                for label in found_labels:
                    labels.add(label)
                
                found_refs = re.findall(r'\\(?:auto)?ref\*?\{([^\}]+)\}', content)
                for ref in found_refs:
                    refs.add(ref)

missing_labels = refs - labels
print(f"Missing labels (Refs that don't exist): {missing_labels}")
