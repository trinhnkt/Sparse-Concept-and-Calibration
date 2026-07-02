import glob
import re

new_bib = """@article{pelanek2015metrics,
  author  = {Pel{\\'a}nek, Radek},
  title   = {Metrics for Evaluation of Student Models},
  journal = {Journal of Educational Data Mining},
  volume  = {7},
  number  = {2},
  pages   = {1--19},
  year    = {2015},
  doi     = {10.5281/zenodo.3554665}
}"""

bib_files = glob.glob('**/*.bib', recursive=True)

for f in bib_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to find the pelanek2015metrics block
    pattern = re.compile(r'@article\{pelanek2015metrics,[^}]+?\}', re.IGNORECASE)
    
    if pattern.search(content):
        new_content = pattern.sub(new_bib, content)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {f}")
    else:
        # maybe just append if not found, though we know it's there from grep
        pass
