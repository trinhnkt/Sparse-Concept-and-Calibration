import os

filepath = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\references.bib"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check for unbalanced braces
def check_braces(text):
    stack = []
    for i, char in enumerate(text):
        if char == '{':
            stack.append(i)
        elif char == '}':
            if not stack:
                return f"Unmatched }} at index {i}"
            stack.pop()
    if stack:
        return f"Unmatched {{ at index {stack[-1]}"
    return "Braces balanced"

print("Syntax Check:", check_braces(content))

# Look for common bibtex errors
lines = content.split('\n')
for i, line in enumerate(lines):
    if line.strip().startswith('@') and '{' not in line:
        print(f"Warning: line {i+1} starts with @ but has no {{: {line}")
    if line.count('{') != line.count('}'):
        # Just a heuristic, not always an error on a single line
        pass

print("Done.")
