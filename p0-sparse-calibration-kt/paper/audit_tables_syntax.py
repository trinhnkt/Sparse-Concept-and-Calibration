import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

table_files = [f for f in os.listdir(folder) if f.endswith('.tex')]
print(f"Found {len(table_files)} tables.")

for tfile in table_files:
    fpath = os.path.join(folder, tfile)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for table environment
    if "\\begin{table}" not in content:
        issues.append("Missing \\begin{table}")
    if "\\end{table}" not in content:
        issues.append("Missing \\end{table}")
        
    # Check for resizebox / maxsizebox
    if "resizebox" in content:
        issues.append("Still contains resizebox")
    if "maxsizebox" in content:
        issues.append("Still contains maxsizebox")
        
    # Check for stray closing braces that might belong to removed resizebox
    # A bit tricky, but let's check if the number of { matches }
    # Ignore escaped \{ and \}
    content_clean = re.sub(r'\\.', '', content)
    open_b = content_clean.count('{')
    close_b = content_clean.count('}')
    if open_b != close_b:
        issues.append(f"Unbalanced braces! {open_b} open vs {close_b} close.")
        
    if issues:
        print(f"[FAIL] {tfile}: {', '.join(issues)}")
    else:
        print(f"[OK] {tfile}")

