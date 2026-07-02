import sys, re, os

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern 1 (Springer)
        pattern1 = re.compile(r'The code, protocol checklist, and reporting templates are publicly available on the \\href\{https://github\.com/trinhnkt/P0\}\{GitHub repository\}\.')
        
        # Pattern 2 (JEDM/Old)
        pattern2 = re.compile(r'We will release the complete reproducibility package upon acceptance at \\url\{https://github\.com/trinhnkt/P0\}\.')

        new_text = r'The anonymized artifact repository will be provided during peer review. The public repository will be released upon acceptance.'
        
        original_content = content
        content = pattern1.sub(new_text, content)
        content = pattern2.sub(new_text, content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Apply to all tex files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.tex'):
            fix_file(os.path.join(root, file))

