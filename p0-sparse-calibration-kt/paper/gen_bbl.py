import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"
bib_file = os.path.join(folder, "references.bib")
bbl_file = os.path.join(folder, "references.bbl")

with open(bib_file, 'r', encoding='utf-8') as f:
    bib_text = f.read()

# Very basic parser
entries = []
# Match @type{key, ... }
pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}', re.DOTALL)

for match in pattern.finditer(bib_text):
    etype = match.group(1).lower()
    key = match.group(2).strip()
    content = match.group(3)
    
    # Extract fields
    fields = {}
    field_pattern = re.compile(r'(\w+)\s*=\s*(?:\{([^}]*)\}|"([^"]*)")')
    for f_match in field_pattern.finditer(content):
        fname = f_match.group(1).lower()
        fval = f_match.group(2) if f_match.group(2) else f_match.group(3)
        fields[fname] = fval.strip() if fval else ""
        
    entries.append((key, fields))

# Generate bbl
with open(bbl_file, 'w', encoding='utf-8') as f:
    f.write("\\begin{thebibliography}{99}\n\n")
    for key, fields in entries:
        author = fields.get('author', 'Unknown Author').replace('\n', ' ')
        title = fields.get('title', 'Unknown Title').replace('\n', ' ')
        year = fields.get('year', '')
        journal = fields.get('journal', fields.get('booktitle', ''))
        
        # Simple formatting
        f.write(f"\\bibitem{{{key}}}\n")
        f.write(f"{author} ({year}). {title}. \\textit{{{journal}}}.\n\n")
    f.write("\\end{thebibliography}\n")

print(f"Generated {bbl_file} with {len(entries)} entries.")
