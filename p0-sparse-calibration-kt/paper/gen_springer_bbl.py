import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"
bib_file = os.path.join(folder, "references.bib")
bbl_file = os.path.join(folder, "references.bbl")

with open(bib_file, 'r', encoding='utf-8') as f:
    bib_text = f.read()

# Match entries
pattern = re.compile(r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}', re.DOTALL)
entries = []

for match in pattern.finditer(bib_text):
    etype = match.group(1).lower()
    key = match.group(2).strip()
    content = match.group(3)
    
    fields = {}
    field_pattern = re.compile(r'(\w+)\s*=\s*(?:\{([^}]*)\}|"([^"]*)")')
    for f_match in field_pattern.finditer(content):
        fname = f_match.group(1).lower()
        fval = f_match.group(2) if f_match.group(2) else f_match.group(3)
        if fval:
            # clean up LaTeX specific escapes for Python processing
            val = fval.strip().replace('\n', ' ')
            fields[fname] = val
            
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
            # Get initials
            initials = "".join([n[0] for n in first.split() if n])
            formatted.append(f"{last} {initials}")
        else:
            # First Last
            names = a.split()
            if len(names) > 1:
                last = names[-1]
                first = " ".join(names[:-1])
                initials = "".join([n[0] for n in first.split() if n])
                formatted.append(f"{last} {initials}")
            else:
                formatted.append(a.strip())
    return ", ".join(formatted)

with open(bbl_file, 'w', encoding='utf-8') as f:
    f.write("\\begin{thebibliography}{99}\n")
    f.write("\\providecommand{\\doi}[1]{\\url{https://doi.org/#1}}\n\n")
    
    for key, fields in entries:
        author = format_author(fields.get('author', ''))
        title = fields.get('title', '')
        # Remove curly braces from title
        title = title.replace('{', '').replace('}', '')
        year = fields.get('year', '')
        
        journal = fields.get('journal', fields.get('booktitle', ''))
        volume = fields.get('volume', '')
        number = fields.get('number', '')
        pages = fields.get('pages', '').replace('--', '-')
        doi = fields.get('doi', '')
        
        # Build the citation string Springer style
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
            
        # Fix the weird brace error I saw earlier just in case
        citation = citation.replace("Dem\\v{s", "Dem{\\v{s}}ar")
        citation = citation.replace("Pel\\'a", "Pel{\\'a}nek")
        citation = citation.replace("Beno\\^\\i", "Beno{\\^\\i}t")
        
        f.write(f"\\bibitem{{{key}}}\n{citation}\n\n")
        
    f.write("\\end{thebibliography}\n")

print(f"Generated Springer-style {bbl_file} with {len(entries)} entries.")
