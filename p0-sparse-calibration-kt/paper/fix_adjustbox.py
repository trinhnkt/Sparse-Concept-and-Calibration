import os
import glob
import re

def fix_adjustbox(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace \begin{adjustbox}{max width=\textwidth} with \resizebox{\textwidth}{!}{%
    new_content = content.replace('\\begin{adjustbox}{max width=\\textwidth}', '\\resizebox{\\textwidth}{!}{%')
    
    # Replace \end{adjustbox} with }
    new_content = new_content.replace('\\end{adjustbox}', '}')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    dirs_to_check = [
        os.path.join(os.path.dirname(__file__), 'tables'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'springer_upload_folder', 'tables')
    ]
    
    count = 0
    for d in dirs_to_check:
        tex_files = glob.glob(os.path.join(d, '*.tex'))
        for file in tex_files:
            if fix_adjustbox(file):
                print(f"Fixed adjustbox in: {file}")
                count += 1
                
    print(f"Total fixed files: {count}")
