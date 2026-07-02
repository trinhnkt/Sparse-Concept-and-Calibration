import sys, re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update text
    pattern_text = re.compile(
        r'Because temporal splits stress future-concept generalization.*?misinterpreted as good calibration\.', 
        re.DOTALL
    )
    new_text = r'''Because temporal splits stress future-concept generalization, we use the Junyi temporal split in Fig.~\ref{fig:reliability_junyi_temporal} to visualize calibration behavior under a more challenging evaluation setting. Figure~\ref{fig:reliability_junyi_temporal} visualizes this calibration difference by plotting reliability diagrams for SimpleKT on Junyi under temporal splitting. While the dense stratum (ECE = .0889$) is smoother and supported by substantially more test events ( = 3,072,767$), it is still imperfectly calibrated. In contrast, the sparse stratum (ECE = .1624$,  = 16,206$) has noticeably lower calibration quality than the dense stratum, while still retaining meaningful discrimination (AUC = .6529$). This illustrates that calibration degradation and discrimination should be interpreted jointly.'''
    
    content = pattern_text.sub(new_text, content)

    # 2. Update graphic include
    content = content.replace('junyi_temporal_simplekt_very_sparse.pdf', 'junyi_temporal_simplekt_sparse.pdf')

    # 3. Update subfigure caption
    content = content.replace('Reliability diagram of SimpleKT on Junyi temporal split for Strict Cold-start KCs.', 'Reliability diagram of SimpleKT on Junyi temporal split for Sparse KCs.')

    # 4. Update main figure caption
    pattern_caption = re.compile(
        r'\\caption\{Comparison of reliability curves between Dense and Strict Cold-start KCs.*?despite the curve\'s appearance\.\}', 
        re.DOTALL
    )
    new_caption = r'''\caption{Comparison of reliability curves between Dense and Sparse KCs for SimpleKT on the Junyi temporal split after the label-alignment correction. The diagonal dashed line represents perfect calibration. \ifdefined\iscompact Source calibration values are reported in Supplementary Table S3.\else Source calibration values are reported in Table~\ref{tab:calibration_temporal}.\fi\ The sparse stratum has lower calibration quality than the dense stratum while still retaining meaningful discrimination (AUC = 0.6529), illustrating that calibration degradation and discrimination should be interpreted jointly.}'''
    
    content = pattern_caption.sub(new_caption, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
fix_file('paper/sections/04_experiments.tex')
fix_file('springer_upload_folder/sections/04_experiments.tex')
fix_file('jedm_upload_folder/sections/04_experiments.tex')
print('Updated 04_experiments.tex in all folders')
