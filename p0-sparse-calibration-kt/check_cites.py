import re
import glob
import os

jedm_dir = 'jedm_upload_folder'
tex_files = glob.glob(os.path.join(jedm_dir, 'sections/*.tex'), recursive=True)
tex_files.append(os.path.join(jedm_dir, 'main_jedm.tex'))
tex_files += glob.glob(os.path.join(jedm_dir, 'appendix/*.tex'), recursive=True)

# Collect all \cite{...} keys
cite_keys = set()
for f in tex_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'\\cite\{([^}]+)\}', content):
        for key in m.group(1).split(','):
            cite_keys.add(key.strip())

# Collect all \bibitem{...} keys from bbl
bbl_path = os.path.join(jedm_dir, 'references.bbl')
bib_keys = set()
with open(bbl_path, 'r', encoding='utf-8') as fh:
    content = fh.read()
for m in re.finditer(r'\\bibitem\{([^}]+)\}', content):
    bib_keys.add(m.group(1))

print('=== CITED KEYS ===')
for k in sorted(cite_keys):
    status = 'OK' if k in bib_keys else 'MISSING FROM BBL!'
    print(f'  {k}: {status}')

print(f'\nTotal cited: {len(cite_keys)}')
print(f'Total in bbl: {len(bib_keys)}')

missing = cite_keys - bib_keys
if missing:
    print(f'\n!! MISSING CITATIONS: {missing}')
else:
    print('\nAll citations resolved!')

unused = bib_keys - cite_keys
if unused:
    print(f'Unused bib entries (not cited): {unused}')
