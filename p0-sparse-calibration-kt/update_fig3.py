import glob
import re

exp_files = glob.glob('**/04_experiments.tex', recursive=True)

new_fig3 = r"""\begin{figure}[htbp]
  \centering
  \includegraphics[width=\linewidth]{figures/figure3_junyi_dense_vs_sparse_reliability.pdf}
  \caption{Comparison of reliability curves between Dense and Sparse KCs for SimpleKT on the Junyi temporal split after the label-alignment correction. The diagonal dashed line represents perfect calibration. \ifdefined\iscompact Source calibration values are reported in Supplementary Table S3.\else Source calibration values are reported in Table~\ref{tab:calibration_temporal}.\fi\ The sparse stratum has higher calibration error than the dense stratum while still retaining meaningful discrimination (AUC = 0.6529), illustrating that calibration degradation and discrimination should be interpreted jointly.}
  \label{fig:reliability_junyi_temporal}
\end{figure}"""

new_text = "Because temporal splits stress future-concept generalization, we use the Junyi temporal split in Figure 3 to visualize calibration behavior under a more challenging evaluation setting. Figure 3 compares SimpleKT reliability diagrams between dense and sparse KCs. The dense stratum is supported by substantially more test events and has lower ECE (0.0889), whereas the sparse stratum shows higher ECE (0.1624) while retaining meaningful discrimination (AUC = 0.6529). This comparison highlights why calibration and discrimination must be interpreted jointly at the stratum level."

for f in exp_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Use replace on match group 0
    pattern = re.compile(r'\\begin\{figure\}.*?\\label\{fig:reliability_junyi_temporal\}\s*\\end\{figure\}', re.DOTALL)
    match = pattern.search(content)
    if match:
        content = content.replace(match.group(0), new_fig3)
    else:
        print(f"Could not find Figure 3 block in {f}")
        continue
        
    content = re.sub(r'Because temporal splits stress future-concept generalization[^\n]+', new_text, content)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated Figure 3 in {f}")
