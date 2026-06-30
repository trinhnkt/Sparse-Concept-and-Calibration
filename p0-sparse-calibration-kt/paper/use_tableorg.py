import os
import glob
import re

def convert_to_tableorg(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We only apply this to tables that use \resizebox
    if '\\resizebox' not in content:
        return False

    # Replace \begin{table}[anything] with \begin{tableorg}[anything]
    new_content = re.sub(r'\\begin\{table\}\[([^\]]*)\]', r'\\begin{tableorg}[\1]', content)
    # Also handle \begin{table} without options
    new_content = re.sub(r'\\begin\{table\}(?!org)', r'\\begin{tableorg}', new_content)
    
    # Replace \end{table} with \end{tableorg}
    new_content = re.sub(r'\\end\{table\}', r'\\end{tableorg}', new_content)

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
            if convert_to_tableorg(file):
                print(f"Converted to tableorg: {file}")
                count += 1
                
    print(f"Total updated files: {count}")
