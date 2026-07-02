import glob
import re

def fix_all_bibs():
    bib_files = glob.glob('**/*.bib', recursive=True)
    
    # We will use regex to find the start of pelanek2015metrics and the start of the next entry to replace the whole corrupted block
    
    for f in bib_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 1. Fix the pelanek2015metrics corruption
        # It looks like: @article{pelanek2015metrics, ... } ... }
        # Let's just find everything from @article{pelanek2015metrics, to the end of the file or the next @
        
        # Split by '@' and reconstruct
        entries = content.split('@')
        new_entries = []
        for entry in entries:
            if entry.startswith('article{pelanek2015metrics,'):
                # replace this whole entry
                new_entry = """article{pelanek2015metrics,
  author  = {Pel{\\'a}nek, Radek},
  title   = {Metrics for Evaluation of Student Models},
  journal = {Journal of Educational Data Mining},
  volume  = {7},
  number  = {2},
  pages   = {1--19},
  year    = {2015},
  doi     = {10.5281/zenodo.3554665}
}\n"""
                new_entries.append(new_entry)
            else:
                new_entries.append(entry)
                
        content = '@'.join(new_entries)
        
        # 2. Apply other fixes (from fix_bib.py)
        
        # liu2023xes3g5m
        content = re.sub(
            r'author\s*=\s*\{Liu, Zitao and others\}',
            'author    = {Liu, Zitao and Liu, Qiongqiong and Guo, Teng and Chen, Jiahao and Huang, Shuyan and Zhao, Xiangyu and Tang, Jiliang and Luo, Weiqi and Weng, Jian}',
            content
        )
        content = content.replace("booktitle = {Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track}", "booktitle = {Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track}")

        # choffin2019das3h
        content = content.replace("author={Choffin, Beno{\\^\\i}t and Popineau, Fabrice and Bourda, Yolaine and Vie, Jo{\\~a}o-Jirol}", "author={Choffin, Beno{\\^\\i}t and Popineau, Fabrice and Bourda, Yolaine and Vie, Jill-J{\\^e}nn}")
        content = content.replace("booktitle={Educational Data Mining}", "booktitle={Proceedings of the 12th International Conference on Educational Data Mining}")

        # gervet2020deep
        content = content.replace("author={Gervet, Theophile and Koedinger, Ken and Schneider, Jeff and Mitchell, Tom and others}", "author={Gervet, Theophile and Koedinger, Ken and Schneider, Jeff and Mitchell, Tom}")

        # nixon2019measuring
        content = content.replace("author={Nixon, Jeremy and Dusenberry, Michael W and Zhang, Linxi and Jerfel, Ghassen and Blei, David}", "author={Nixon, Jeremy and Dusenberry, Michael W and Zhang, Linxi and Jerfel, Ghassen and Tran, Dustin}")
        content = content.replace("booktitle={CVPR Workshops}", "booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops}")

        # lee2022cl4kt
        content = content.replace("author={Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and others}", "author={Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and Choi, Dongmin}")

        # kapoor2023leakage missing pages
        if "pages={100804}" not in content and "pages   = {100804}" not in content:
            content = content.replace("year={2023},\n  publisher={Elsevier}", "pages={100804},\n  year={2023},\n  publisher={Elsevier}")

        # choi2020ednet
        content = content.replace("booktitle = {Proceedings of Artificial Intelligence in Education}", "booktitle = {International Conference on Artificial Intelligence in Education}")
        
        # Fix title casing/acronyms for consistency
        content = content.replace("title={Contrastive learning for knowledge tracing}", "title={Contrastive Learning for Knowledge Tracing}")
        content = content.replace("title={Graph-based knowledge tracing: modeling student proficiency using graph neural network}", "title={Graph-based Knowledge Tracing: Modeling Student Proficiency using Graph Neural Network}")
        content = content.replace("title={{GIKT}: A graph-based interaction model for knowledge tracing}", "title={{GIKT}: A Graph-based Interaction Model for Knowledge Tracing}")
        content = content.replace("title={How deep is knowledge tracing?}", "title={How Deep is Knowledge Tracing?}")
        content = content.replace("title={Leakage and the reproducibility crisis in machine-learning-based science}", "title={Leakage and the Reproducibility Crisis in Machine-Learning-based Science}")
        content = content.replace("title={Modeling students' memory for application in adaptive educational systems}", "title={Modeling Students' Memory for Application in Adaptive Educational Systems}")
        content = content.replace("title={Item response theory for psychologists}", "title={Item Response Theory for Psychologists}")
        content = content.replace("title={Probabilistic models for some intelligence and attainment tests}", "title={Probabilistic Models for Some Intelligence and Attainment Tests}")
        content = content.replace("title={Transforming classifier scores into accurate multiclass probability estimates}", "title={Transforming Classifier Scores into Accurate Multiclass Probability Estimates}")
        content = content.replace("title={Individual comparisons by ranking methods}", "title={Individual Comparisons by Ranking Methods}")
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Repaired and formatted {f}")

if __name__ == "__main__":
    fix_all_bibs()
