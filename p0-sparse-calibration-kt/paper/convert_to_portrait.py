import os
import glob
import re

def process_table_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if it has sidewaystable
    if '\\begin{sidewaystable}' not in content:
        return False
    
    # 1. Replace \begin{sidewaystable} with \begin{table}
    content = content.replace('\\begin{sidewaystable}', '\\begin{table}')
    content = content.replace('\\end{sidewaystable}', '\\end{table}')
    
    # 2. Wrap \begin{tabular} ... \end{tabular} inside \begin{adjustbox}{max width=\textwidth} ... \end{adjustbox}
    if '\\begin{adjustbox}' not in content:
        pattern = r'(\\begin\{tabular\}.*?\\end\{tabular\})'
        def replacer(match):
            return '\\begin{adjustbox}{max width=\\textwidth}\n' + match.group(1) + '\n\\end{adjustbox}'
        content = re.sub(pattern, replacer, content, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return True

if __name__ == "__main__":
    tables_dir = os.path.join(os.path.dirname(__file__), 'tables')
    tex_files = glob.glob(os.path.join(tables_dir, '*.tex'))
    
    count = 0
    for file in tex_files:
        if process_table_file(file):
            print(f"Processed: {os.path.basename(file)}")
            count += 1
            
    print(f"Total processed files: {count}")
