import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

table_files = [
    "table1_leakage_audit.tex",
    "table1_dataset_stats.tex",
    "table_iii_overall_results_updated.tex",
    "table_delong_overall_auc.tex",
    "table_iv_bucket_performance_updated.tex",
    "table_vi_cold_start_temporal_updated.tex",
    "tableA1_sensitivity.tex",
    "tableA_overall_full.tex",
    "tableA_performance_by_bucket_full.tex",
    "table_v_calibration_by_bucket_updated.tex",
    "table_xi_temporal_calibration_breakdown.tex",
    "table_interpretation_guide.tex"
]

print("Scanning tables in order of inclusion:")
for tf in table_files:
    filepath = os.path.join(folder, tf)
    if not os.path.exists(filepath):
        print(f"MISSING: {tf}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Extract begin table placement
        placement = re.search(r'\\begin\{table\}\[([^\]]+)\]', content)
        place_str = placement.group(1) if placement else "NONE"
        
        # Check tabular environment
        tabular = re.search(r'\\begin\{(tabular[x\*]?)\}', content)
        tab_str = tabular.group(1) if tabular else "NONE"
        
        # Check resizebox
        has_resize = "resizebox" in content
        
        print(f"\n{tf}")
        print(f"  Placement: [{place_str}]")
        print(f"  Tabular: {tab_str}")
        print(f"  Has Resizebox: {has_resize}")
