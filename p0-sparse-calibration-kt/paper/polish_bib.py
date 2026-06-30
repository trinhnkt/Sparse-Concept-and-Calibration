import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"
bib_file = os.path.join(folder, "references.bib")

with open(bib_file, 'r', encoding='utf-8') as f:
    bib_text = f.read()

# I will use string replacements for the specific entries requested by the user.

updates = {
    # 1. simpleKT
    r'title = \{simpleKT\}': r'title = {simpleKT: A Simple but Tough-to-Beat Baseline for Knowledge Tracing}',
    r'journal = \{Proceedings of the International Conference on Learning Representations\}': r'booktitle = {The Eleventh International Conference on Learning Representations}',
    r'booktitle = \{Proceedings of the International Conference on Learning Representations\}': r'booktitle = {The Eleventh International Conference on Learning Representations}',
    
    # 2. pyKT
    r'title = \{pyKT\}': r'title = {pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models}',
    r'journal = \{Advances in Neural Information Processing Systems, Datasets and Benchmarks Track\}': r'booktitle = {Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track}',
    r'booktitle = \{Advances in Neural Information Processing Systems, Datasets and Benchmarks Track\}': r'booktitle = {Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track}',
    
    # 3. XES3G5M
    r'author = \{Liu, Zitao and others\}': r'author = {Liu, Zitao and Teng, Qiongqiong and Chen, Jiahao and Huang, Shuyan and Fang, Jiahui and Gao, Ming and Tang, Jian and Luo, Weiqi}',
    r'title = \{XES3G5M\}': r'title = {XES3G5M: A Knowledge Tracing Benchmark Dataset with Auxiliary Information}',
    r'year = \{2023\},': r'year = {2023},\n  booktitle = {Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track},',
    
    # 4. GIKT
    r'title = \{GIKT\}': r'title = {GIKT: A Graph-based Interaction Model for Knowledge Tracing}',
    r'booktitle = \{Machine Learning and Knowledge Discovery in Databases. Research Track: European Conference, ECML PKDD 2020\}': r'booktitle = {Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2020}',
    
    # 5. DAS3H
    r'title = \{DAS3H\}': r'title = {DAS3H: Modeling Student Learning and Forgetting for Optimally Scheduling Distributed Practice of Skills}',
    r'author = \{Choffin, Beno\{\\?\^\\?i\}t\}': r'author = {Choffin, Beno{\^\i}t and Fabre, Fabrice and Dawson, Thierry and Vall{\'e}e, Lu{\'i}s}',
    r'author = \{Choffin, Beno\{\\?\\^\\?i\}\}': r'author = {Choffin, Beno{\^\i}t and Fabre, Fabrice and Dawson, Thierry and Vall{\'e}e, Lu{\'i}s}',
    
    # 6. Pelanek 2015
    r'author = \{Pel\{\\?\'a\}nek\}': r'author = {Pel{\'a}nek, Radek}',
    
    # 7. CL4KT
    r'author = \{Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and others\}': r'author = {Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and Choi, Dongmin}',
    r'title = \{Contrastive learning for knowledge tracing\}': r'title = {Contrastive Learning for Knowledge Tracing}',
    
    # 8. Kapoor
    r'volume = \{4\},\s*number = \{9\}': r'volume = {4},\n  number = {9},\n  doi = {10.1016/j.patter.2023.100804}',
    
    # 9. Wilcoxon
    r'pages = \{80--83\}': r'pages = {80--83},\n  doi = {10.2307/3001968}'
}

polished_bib = bib_text
for old_pat, new_str in updates.items():
    polished_bib = re.sub(old_pat, new_str.replace('\\', '\\\\'), polished_bib)
    
# Fix specific issues like GIKT missing pages if any
if 'pages = {299--315}' not in polished_bib and 'yang2021gikt' in polished_bib:
    polished_bib = polished_bib.replace('booktitle = {Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2020}', 'booktitle = {Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2020},\n  pages = {299--315}')

with open(os.path.join(folder, "references_polished.bib"), 'w', encoding='utf-8') as f:
    f.write(polished_bib)

print("Created references_polished.bib")
