import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

# 1. Parse references.bib for all keys
bib_file = os.path.join(folder, "references.bib")
with open(bib_file, 'r', encoding='utf-8') as f:
    bib_content = f.read()

# Extract keys: @type{key,
bib_keys = set()
for match in re.finditer(r'@\w+\s*\{\s*([^,\s]+)\s*,', bib_content):
    bib_keys.add(match.group(1))

print(f"Found {len(bib_keys)} entries in references.bib")

# 2. Parse all .tex files for \cite{...}
tex_files = []
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            tex_files.append(os.path.join(root, file))

cited_keys = set()
for fpath in tex_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find \cite{key1,key2}
    for match in re.finditer(r'\\cite(?:[ptw])?\{([^}]+)\}', content):
        keys_str = match.group(1)
        # split by comma
        keys = [k.strip() for k in keys_str.split(',')]
        for k in keys:
            cited_keys.add(k)

print(f"Found {len(cited_keys)} unique cited keys in .tex files")

# 3. Cross check
missing_in_bib = cited_keys - bib_keys
if missing_in_bib:
    print("\n[ERROR] The following keys are cited in .tex but MISSING from references.bib:")
    for k in sorted(missing_in_bib):
        print(f"  - {k}")
else:
    print("\n[OK] All cited keys exist in references.bib.")

missing_in_tex = bib_keys - cited_keys
if missing_in_tex:
    print("\n[WARNING] The following keys are in references.bib but NEVER cited in .tex:")
    for k in sorted(missing_in_tex):
        print(f"  - {k}")
else:
    print("\n[OK] All entries in references.bib are cited in the text.")

