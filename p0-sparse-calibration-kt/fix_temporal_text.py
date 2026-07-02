import glob

old_text = "Because the dataset partition is strictly fixed, reporting multiple seeds would only capture neural network initialization variance rather than the generalization variance of interest. Thus, a single deterministic run accurately isolates the temporal generalization behavior."

new_text = "Because the temporal partition is fixed, the reported temporal results focus on fixed-cutoff temporal stress testing rather than estimating variance across temporal cut-points or neural initializations. We do not claim that neural initialization variance is absent; extending the temporal diagnostics to multiple seeds or multiple temporal cut-points is left for future work."

files_to_check = glob.glob('**/*.tex', recursive=True)
count = 0

for f in files_to_check:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
            count += 1
    except Exception as e:
        print(f"Error reading {f}: {e}")

print(f"Total files updated: {count}")
