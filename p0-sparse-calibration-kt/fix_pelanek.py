import glob

bib_files = glob.glob('**/*.bib', recursive=True)

for f in bib_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if "Pel{\\'a}nek, Radek" in content:
        content = content.replace("Pel{\\'a}nek, Radek", "Pelanek, Radek")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed Pelanek in {f}")
