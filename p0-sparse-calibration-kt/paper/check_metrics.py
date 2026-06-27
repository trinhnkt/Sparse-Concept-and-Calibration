import os

def check_content(file_path, expected_strings):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nChecking {os.path.basename(file_path)}:")
    for s in expected_strings:
        if s in content:
            print(f"  [PASS] Found '{s}'")
        else:
            print(f"  [FAIL] Missing '{s}'")

tables_dir = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

# 1. Table 3 ASSISTments learner-based
check_content(os.path.join(tables_dir, "table_iii_overall_results_updated.tex"), [
    r"0.6980 \pm 0.0013",
    r"0.6840 \pm 0.0025"
])

# 2. Table 4 DeLong Bonferroni alpha = 0.0056
check_content(os.path.join(tables_dir, "table_delong_overall_auc.tex"), [
    r"0.0056"
])

# 3. Table 5 XES3G5M counter-pattern (sparse 0.8590, 0.8509 etc)
check_content(os.path.join(tables_dir, "table_iv_bucket_performance_updated.tex"), [
    r"0.8590 \pm", r"0.8509 \pm",  # sparse
    r"0.8413 \pm", r"0.8379 \pm",  # very sparse
    r"0.8168 \pm", r"0.7547 \pm"   # dense
])

# 4. Table 6 warm temporal
check_content(os.path.join(tables_dir, "table_vi_cold_start_temporal_updated.tex"), [
    r"0.6606", r"0.6734", # ASSISTments
    r"0.6949", r"0.7167", # Junyi
    r"0.6626", r"0.6615"  # XES3G5M
])

# 5. Table C5 / Figure 3 values in table_xi_temporal_calibration_breakdown.tex
check_content(os.path.join(tables_dir, "table_xi_temporal_calibration_breakdown.tex"), [
    r"0.0889", r"3,072,767", # Junyi Dense
    r"0.0841", r"2,545"      # Junyi Very Sparse
])
