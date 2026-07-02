import glob

old_text = "More broadly, our temporal-split audit demonstrates that the protocol's built-in leakage and sanity checks successfully catch subtle evaluation pipeline bugs, ensuring that researchers can distinguish genuine concept-level cold-start failure from alignment artifacts."
new_text = "Furthermore, the observed heterogeneity in performance and calibration trends across different datasets underscores the necessity of a standardized diagnostic protocol. More broadly, our temporal-split audit demonstrates that the protocol's built-in leakage and sanity checks successfully catch subtle evaluation pipeline bugs, ensuring that researchers can distinguish genuine concept-level cold-start failure from alignment artifacts."

files = glob.glob('**/06_conclusion.tex', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
