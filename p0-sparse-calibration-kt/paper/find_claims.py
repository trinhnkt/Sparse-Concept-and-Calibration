import os

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if "artifactual" in content.lower():
                    print(f"FOUND 'artifactual' in {file}")
                if "perfectly illustrates" in content.lower():
                    print(f"FOUND 'perfectly illustrates' in {file}")
                if "this pattern suggests" in content.lower():
                    print(f"FOUND 'this pattern suggests' in {file}")
