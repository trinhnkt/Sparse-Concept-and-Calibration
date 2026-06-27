import os

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if "??" in content:
                    print(f"FOUND literal '??' in {file}")
                    
                if "[?" in content:
                    print(f"FOUND literal '[?' in {file}")
                    
                if "Table ??" in content:
                    print(f"FOUND literal 'Table ??' in {file}")
