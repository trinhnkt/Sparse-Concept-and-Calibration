import os
import glob
import re

def fix_table_notes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find \multicolumn{...}{p{\textwidth}}{...} and extract the note
    # It usually looks like: \multicolumn{7}{p{\textwidth}}{\textit{Note: ...}} \\
    
    # We will look for \multicolumn{.*?}{p{\textwidth}}{(.*?)} \\
    # and remove it from tabular, then insert it after \end{adjustbox}
    
    pattern = r'\\multicolumn\{[^\}]+\}\{p\{\\textwidth\}\}\{(.*?)\}\s*\\\\'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        note_content = match.group(1)
        # Remove the multicolumn line from the content
        content = re.sub(pattern, '', content)
        
        # Insert the note after \end{adjustbox}
        if '\\end{adjustbox}' in content and note_content not in content:
            replacement = f"\\end{{adjustbox}}\n\n\\vspace{{1ex}}\n\\noindent\\footnotesize {note_content}\n"
            content = content.replace('\\end{adjustbox}', replacement)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
            
    return False

if __name__ == "__main__":
    tables_dir = os.path.join(os.path.dirname(__file__), 'tables')
    tex_files = glob.glob(os.path.join(tables_dir, '*.tex'))
    
    count = 0
    for file in tex_files:
        if fix_table_notes(file):
            print(f"Fixed notes in: {os.path.basename(file)}")
            count += 1
            
    print(f"Total fixed files: {count}")
