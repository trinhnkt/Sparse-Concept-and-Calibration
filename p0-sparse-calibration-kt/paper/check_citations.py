import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"
bib_file = os.path.join(folder, "references.bib")

with open(bib_file, 'r', encoding='utf-8') as f:
    bib_content = f.read()

# Extract all bib keys
bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_content))

print(f"Found {len(bib_keys)} keys in references.bib")

# Extract all cite commands
all_cited_keys = set()
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                cites = re.findall(r'\\cite[p|t]*\{([^\}]+)\}', content)
                for cite_group in cites:
                    for key in cite_group.split(','):
                        all_cited_keys.add(key.strip())

print(f"Found {len(all_cited_keys)} unique cited keys in .tex files.")

missing_keys = all_cited_keys - bib_keys
if missing_keys:
    print(f"MISSING KEYS: {missing_keys}")
else:
    print("ALL CITED KEYS ARE PRESENT IN REFERENCES.BIB")
