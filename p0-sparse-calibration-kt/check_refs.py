import re
import glob
import os

jedm_dir = 'jedm_upload_folder'
tex_files = glob.glob(os.path.join(jedm_dir, '**/*.tex'), recursive=True)

# Collect all labels
labels = set()
refs = []

for f in tex_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find all \label{...}
    for m in re.finditer(r'\\label\{([^}]+)\}', content):
        labels.add(m.group(1))
    
    # Find all \ref{...}
    for m in re.finditer(r'\\ref\{([^}]+)\}', content):
        refs.append((f, m.group(1)))

print("=== DEFINED LABELS ===")
for l in sorted(labels):
    print(f"  {l}")

print(f"\n=== TOTAL: {len(labels)} labels ===")

print("\n=== UNRESOLVED REFERENCES ===")
unresolved = 0
for f, r in refs:
    if r not in labels:
        print(f"  !! {r} referenced in {os.path.basename(f)} but NEVER DEFINED")
        unresolved += 1

if unresolved == 0:
    print("  None! All references resolve.")
else:
    print(f"\n  TOTAL UNRESOLVED: {unresolved}")
