import glob

# Replace "Table ??" in 04_experiments.tex
exp_files = glob.glob('**/04_experiments.tex', recursive=True)
for f in exp_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace literal "Table ??" with "Table~\ref{tab:cold_start_temporal}"
    # But wait, there might be Table ?? for Appendix B or Table 6.
    # We should specifically target the ones mentioned:
    # "reported in Table ?? and Appendix B" -> "reported in Table~\ref{tab:cold_start_temporal} and Appendix B"
    # "under time-partitioned (temporal) splitting in Table ??." -> "... splitting in Table~\ref{tab:cold_start_temporal}."
    
    content = content.replace("reported in Table ?? and Appendix B", "reported in Table~\\ref{tab:cold_start_temporal} and Appendix B")
    content = content.replace("splitting in Table ??.", "splitting in Table~\\ref{tab:cold_start_temporal}.")
    # Replace any remaining literal Table ?? with Table~\ref{tab:cold_start_temporal} if it refers to it
    content = content.replace("Table ??", "Table~\\ref{tab:cold_start_temporal}")

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Fixed Table ?? in {f}")

# Update label in table_vi_cold_start_temporal_updated.tex
tab_files = glob.glob('**/table_vi_cold_start_temporal_updated.tex', recursive=True)
for f in tab_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace("\\label{tab:cold_start}", "\\label{tab:cold_start_temporal}")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated label in {f}")

