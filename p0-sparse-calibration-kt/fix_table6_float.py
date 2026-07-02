import glob
import re

files = glob.glob('**/04_experiments.tex', recursive=True)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Fix the reference label if it's broken
    if "Table~\\ref{tab:cold_start_temporal}" in content:
        content = content.replace("Table~\\ref{tab:cold_start_temporal}", "Table~\\ref{tab:cold_start}")
        
    # Add FloatBarrier after Table 6 input
    old_input = "\\input{tables/table_vi_cold_start_temporal_updated}"
    new_input = "\\input{tables/table_vi_cold_start_temporal_updated}\n\\FloatBarrier"
    
    # If not already there
    if "\\input{tables/table_vi_cold_start_temporal_updated}\n\\FloatBarrier" not in content:
        content = content.replace(old_input, new_input)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated {f}")
