import os
import glob
import re

tex_files = glob.glob(r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\**\*.tex", recursive=True)
bib_file = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\references.bib"

with open(bib_file, 'r', encoding='utf-8') as f:
    bib_content = f.read()

# Find all bib keys
bib_keys = re.findall(r'@\w+\{([^,]+),', bib_content)
bib_keys_set = set(key.strip() for key in bib_keys)

all_citations = set()
for file in tex_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        cites = re.findall(r'\\cite\{([^\}]+)\}', content)
        for cite_group in cites:
            keys = [k.strip() for k in cite_group.split(',')]
            all_citations.update(keys)

missing = all_citations - bib_keys_set
print(f"Total citations used: {len(all_citations)}")
print(f"Total bib keys available: {len(bib_keys_set)}")
print(f"Missing citations: {missing}")

