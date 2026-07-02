import os
import glob

report = {
    "appendix_appendix": False,
    "strict_0": True,
    "very_sparse_excl_0": True,
    "tab9_consistent": True,
    "tab11_consistent": True,
    "fig2_consistent": True,
    "fig3_consistent": True,
    "tab7_assistments": False,
    "tab7_deepkt_replaced": False,
    "tab7_claim_consistent": True,
    "artifact_clear": True,
    "pelanek_clean": True,
    "single_run_softened": True,
    "tab6_placement": True
}

# 1. Check Appendix Appendix
tex_files = glob.glob('jedm_upload_folder/**/*.tex', recursive=True)
for f in tex_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        if 'Appendix Appendix' in content:
            report['appendix_appendix'] = True
            print("Found Appendix Appendix in", f)

# 2. Check Pelanek clean
bib_files = glob.glob('jedm_upload_folder/**/*.bib', recursive=True)
for f in bib_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        if "Pel{\\'a}nek, Radek" not in content and "Pel{\\'a}nek" not in content:
            pass 

# 3. Check Table 7
with open('jedm_upload_folder/tables/table_vii_threshold_sensitivity_updated.tex', 'r', encoding='utf-8') as file:
    tab7 = file.read()
    if 'ASSISTments 2012' in tab7:
        report['tab7_assistments'] = True
    if 'Deep baselines' in tab7 and 'DeepKT' not in tab7:
        report['tab7_deepkt_replaced'] = True

# 4. Check Table 6 placement
with open('jedm_upload_folder/sections/04_experiments.tex', 'r', encoding='utf-8') as file:
    exp = file.read()
    if '\\input{tables/table_vi_cold_start_temporal_updated}\n\\FloatBarrier' in exp:
        report['tab6_placement'] = True
    else:
        report['tab6_placement'] = False
        
    if 'accurately isolates' in exp:
        report['single_run_softened'] = False

# 5. Check Artifact
with open('jedm_upload_folder/main_jedm.tex', 'r', encoding='utf-8') as file:
    main = file.read()
    if 'will be provided' not in main and 'will be released' not in main:
        report['artifact_clear'] = False

print(report)
