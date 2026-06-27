import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

labels = set()
refs = set()

# Collect labels and refs
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find \label{...}
                found_labels = re.findall(r'\\label\{([^\}]+)\}', content)
                for label in found_labels:
                    labels.add(label)
                
                # Find \ref{...} and \autoref{...}
                found_refs = re.findall(r'\\(?:auto)?ref\{([^\}]+)\}', content)
                for ref in found_refs:
                    refs.add(ref)

print(f"Total labels: {len(labels)}")
print(f"Total refs: {len(refs)}")

missing_labels = refs - labels
if missing_labels:
    print(f"MISSING LABELS (these will show as ?? in PDF): {missing_labels}")
else:
    print("ALL REFERENCES HAVE MATCHING LABELS.")
