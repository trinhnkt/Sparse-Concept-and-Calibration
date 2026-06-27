import os
import glob

replacements = {
    r"tab:datasets": r"tab:dataset_stats",
    r"tab:overall": r"tab:overall_learner",
    r"tab:delong_test": r"tab:delong",
    r"tab:bucket": r"tab:strata_learner",
    r"tab:cold_start": r"tab:cold_start_temporal",
    r"tab:overall_temporal": r"tab:temporal_overall",
    r"tab:bucket_temporal": r"tab:temporal_strata",
    r"tab:calib": r"tab:calibration_learner",
    r"tab:temporal_calibration_breakdown": r"tab:calibration_temporal",
    r"fig:reliability_comparison": r"fig:reliability_junyi_temporal"
}

files = glob.glob(r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\**\*.tex", recursive=True)

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    orig = content
    for old, new in replacements.items():
        content = content.replace(f"{{{old}}}", f"{{{new}}}")
        
    if content != orig:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated labels in {os.path.basename(file)}")
