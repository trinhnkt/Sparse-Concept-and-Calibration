import glob

bib_files = glob.glob('**/*.bib', recursive=True)

for f in bib_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix literal \n
    content = content.replace(r'\n', '\n')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Cleaned {f}")
