import glob

bib_files = glob.glob('**/*.bib', recursive=True)

for f in bib_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the erroneous booktitle from kapoor2023leakage
    wrong_line = "  booktitle = {Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track},\n"
    # Actually let's just do a targeted replace for kapoor2023leakage
    # Find the kapoor2023leakage block and clean it
    
    parts = content.split('@')
    new_parts = []
    for part in parts:
        if part.startswith('article{kapoor2023leakage,'):
            # Clean it
            part = part.replace(wrong_line, '')
            # Clean any double pages just in case
            lines = part.split('\n')
            new_lines = []
            seen_pages = False
            for line in lines:
                if 'pages' in line:
                    if not seen_pages:
                        new_lines.append(line)
                        seen_pages = True
                elif 'booktitle' in line:
                    continue # it shouldn't have booktitle
                else:
                    new_lines.append(line)
            part = '\n'.join(new_lines)
            new_parts.append(part)
        else:
            new_parts.append(part)
            
    content = '@'.join(new_parts)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Fixed kapoor2023leakage in {f}")
