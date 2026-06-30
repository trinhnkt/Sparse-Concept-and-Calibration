import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

# 1. Find all cited keys in .tex files
tex_files = []
for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            tex_files.append(os.path.join(root, file))

cited_keys = set()
for fpath in tex_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for match in re.finditer(r'\\cite(?:[ptw])?\{([^}]+)\}', content):
        keys = [k.strip() for k in match.group(1).split(',')]
        for k in keys:
            cited_keys.add(k)

# 2. Parse references.bib
bib_file = os.path.join(folder, "references.bib")
with open(bib_file, 'r', encoding='utf-8') as f:
    bib_text = f.read()

pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}', re.DOTALL)
entries = []
gikt_year_old = ""

for match in pattern.finditer(bib_text):
    etype = match.group(1).lower()
    key = match.group(2).strip()
    content = match.group(3)
    
    # ONLY KEEP CITED KEYS!
    if key not in cited_keys:
        continue
        
    fields = {}
    field_pattern = re.compile(r'(\w+)\s*=\s*(?:\{([^}]*)\}|"([^"]*)")')
    for f_match in field_pattern.finditer(content):
        fname = f_match.group(1).lower()
        fval = f_match.group(2) if f_match.group(2) else f_match.group(3)
        if fval:
            val = fval.strip().replace('\n', ' ')
            fields[fname] = val
            
    # Metadata Check for GIKT
    if key == 'yang2021gikt':
        gikt_year_old = fields.get('year', '')
        # Conference was ECML PKDD 2020, but Proceedings published in 2021.
        # Let's standardize it: Year 2021, Booktitle: Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2020
        fields['year'] = '2021'
        fields['booktitle'] = 'Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2020'
        
    entries.append((key, fields))

# Formatting helpers
def format_author(author_str):
    if not author_str:
        return "Unknown"
    authors = author_str.split(' and ')
    formatted = []
    for a in authors:
        parts = a.split(',')
        if len(parts) == 2:
            last = parts[0].strip()
            first = parts[1].strip()
            initials = "".join([n[0] for n in first.split() if n])
            formatted.append(f"{last} {initials}")
        else:
            names = a.split()
            if len(names) > 1:
                last = names[-1]
                first = " ".join(names[:-1])
                initials = "".join([n[0] for n in first.split() if n])
                formatted.append(f"{last} {initials}")
            else:
                formatted.append(a.strip())
    return ", ".join(formatted)

bbl_file = os.path.join(folder, "references.bbl")
with open(bbl_file, 'w', encoding='utf-8') as f:
    f.write("\\begin{thebibliography}{99}\n")
    f.write("\\providecommand{\\doi}[1]{\\url{https://doi.org/#1}}\n\n")
    
    for key, fields in entries:
        author = format_author(fields.get('author', ''))
        title = fields.get('title', '').replace('{', '').replace('}', '')
        year = fields.get('year', '')
        
        journal = fields.get('journal', fields.get('booktitle', ''))
        volume = fields.get('volume', '')
        number = fields.get('number', '')
        pages = fields.get('pages', '').replace('--', '-')
        doi = fields.get('doi', '')
        
        citation = f"{author} ({year}) {title}."
        if journal:
            citation += f" \\textit{{{journal}}}"
            if volume:
                citation += f" {volume}"
                if number:
                    citation += f"({number})"
            if pages:
                citation += f":{pages}."
            else:
                citation += "."
        
        if doi:
            citation += f" \\doi{{{doi}}}"
            
        citation = citation.replace("Dem\\v{s", "Dem{\\v{s}}ar")
        citation = citation.replace("Pel\\'a", "Pel{\\'a}nek")
        citation = citation.replace("Beno\\^\\i", "Beno{\\^\\i}t")
        
        f.write(f"\\bibitem{{{key}}}\n{citation}\n\n")
        
    f.write("\\end{thebibliography}\n")

print(f"Generated EXACTLY {len(entries)} cited entries in references.bbl.")
print(f"GIKT year was: {gikt_year_old}, now forced to 2021 with ECML PKDD 2020 note.")
