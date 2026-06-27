import re

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
                return False, f"Unmatched }} at index {i}"
            stack.pop()
    if stack:
        return False, f"Unmatched {{ at index {stack[-1]}"
    return True, "Balanced"

ok, msg = check_braces(content)
print(f"Brace check: {ok}, {msg}")

# Check entries format
entries = re.findall(r'@\w+\{([^,]+),', content)
print(f"Found {len(entries)} entries")

# Check for missing commas after title, author etc
lines = content.split('\n')
for i, line in enumerate(lines):
    line = line.strip()
    if '=' in line and not line.endswith(',') and not line.endswith('}') and not line.endswith('"{') and not line.endswith('",'):
        print(f"Warning: Line {i+1} might be missing a comma: {line}")
