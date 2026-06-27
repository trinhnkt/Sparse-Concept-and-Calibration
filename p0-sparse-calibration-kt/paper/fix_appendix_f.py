import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"

files_to_fix = [
    r"appendix\appendix_a_sensitivity.tex",
    r"sections\04_experiments.tex",
    r"tables\table_xi_temporal_calibration_breakdown.tex"
]

for filename in files_to_fix:
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace hardcoded 'Appendix F' with 'Appendix~\ref{app:alignment}'
    new_content = re.sub(r'Appendix F', r'Appendix~\\ref{app:alignment}', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed Appendix F in {filename}")
