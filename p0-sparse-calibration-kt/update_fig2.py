import glob
import re

files = glob.glob('**/03_methodology.tex', recursive=True) + glob.glob('**/04_experiments.tex', recursive=True)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    if "fig:strata_dist" in content:
        # Find the caption for fig:strata_dist
        # It looks like: \caption{KC-frequency strata distribution ... Dense: \mathrm{train\_freq} \ge 500.}
        # Let's just string replace the end of it
        old_cap = "Dense: \mathrm{train\_freq} \ge 500.}"
        new_cap = "Dense: \mathrm{train\_freq} \ge 500. Strict cold-start KCs are analyzed separately in the cold-start diagnostics and are not plotted as a separate bar in this figure.}"
        if "Strict cold-start KCs are analyzed separately" not in content:
            content = content.replace(old_cap, new_cap)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated Figure 2 caption in {f}")
