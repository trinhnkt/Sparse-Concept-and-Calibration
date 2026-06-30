import os

def remove_hyphens_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replacements
    replacements = {
        'Khanh-Trinh': 'Khanh Trinh',
        'Minh-Tuan': 'Minh Tuan',
        'Tien-Duong': 'Tien Duong',
        'Van-Hau': 'Van Hau',
        'Chi-Thanh': 'Chi Thanh'
    }
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        return True
    return False

if __name__ == "__main__":
    files = [
        r"c:\TRINH\P0\p0-sparse-calibration-kt\paper\main_springer_traditional.tex",
        r"c:\TRINH\P0\p0-sparse-calibration-kt\paper\main_springer_compact.tex",
        r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\main_springer_traditional.tex",
        r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\main_springer_compact.tex"
    ]
    
    count = 0
    for file in files:
        if remove_hyphens_in_file(file):
            count += 1
            
    print(f"Total files updated: {count}")
