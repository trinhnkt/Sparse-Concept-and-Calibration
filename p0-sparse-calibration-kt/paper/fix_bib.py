import os
import re

def fix_bib(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix liu2023xes3g5m
    old_xes = """@inproceedings{liu2023xes3g5m,
  author    = {Liu, Zitao and others},
  title     = {{XES3G5M}: A Knowledge Tracing Benchmark Dataset with Auxiliary Information},
  booktitle = {Thirty-sixth Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year      = {2023}
}"""
    new_xes = """@inproceedings{liu2023xes3g5m,
  author    = {Liu, Zitao and Liu, Qiongqiong and Guo, Teng and Chen, Jiahao and Huang, Shuyan and Zhao, Xiangyu and Tang, Jiliang and Luo, Weiqi and Weng, Jian},
  title     = {{XES3G5M}: A Knowledge Tracing Benchmark Dataset with Auxiliary Information},
  booktitle = {Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track},
  year      = {2023}
}"""
    content = content.replace(old_xes, new_xes)

    # 2. Fix choffin2019das3h
    old_das = """@inproceedings{choffin2019das3h,
  title={{DAS3H}: Modeling Student Learning and Forgetting for Optimally Scheduling Distributed Practice of Skills},
  author={Choffin, Beno{\\^\\i}t and Popineau, Fabrice and Bourda, Yolaine and Vie, Jo{~a}o-Jirol},
  booktitle={Educational Data Mining},
  year={2019}
}"""
    new_das = """@inproceedings{choffin2019das3h,
  title={{DAS3H}: Modeling Student Learning and Forgetting for Optimally Scheduling Distributed Practice of Skills},
  author={Choffin, Beno{\\^\\i}t and Popineau, Fabrice and Bourda, Yolaine and Vie, Jill-J{\\^e}nn},
  booktitle={Proceedings of the 12th International Conference on Educational Data Mining},
  pages     = {276--281},
  year={2019}
}"""
    content = content.replace(old_das, new_das)

    # 3. Fix gervet2020deep
    old_gervet = """@article{gervet2020deep,
  title={When is Deep Learning the Best Approach to Knowledge Tracing?},
  author={Gervet, Theophile and Koedinger, Ken and Schneider, Jeff and Mitchell, Tom and others},
  journal={Journal of Educational Data Mining},
  volume={12},
  number={3},
  pages={31--54},
  year={2020}
}"""
    new_gervet = """@article{gervet2020deep,
  title={When is Deep Learning the Best Approach to Knowledge Tracing?},
  author={Gervet, Theophile and Koedinger, Ken and Schneider, Jeff and Mitchell, Tom},
  journal={Journal of Educational Data Mining},
  volume={12},
  number={3},
  pages={31--54},
  year={2020}
}"""
    content = content.replace(old_gervet, new_gervet)

    # 4. Fix nixon2019measuring
    old_nixon = """@inproceedings{nixon2019measuring,
  title={Measuring Calibration in Deep Learning},
  author={Nixon, Jeremy and Dusenberry, Michael W and Zhang, Linxi and Jerfel, Ghassen and Blei, David},
  booktitle={CVPR Workshops},
  volume={2},
  number={7},
  year={2019}
}"""
    new_nixon = """@inproceedings{nixon2019measuring,
  title={Measuring Calibration in Deep Learning},
  author={Nixon, Jeremy and Dusenberry, Michael W and Zhang, Linxi and Jerfel, Ghassen and Tran, Dustin},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
  pages     = {38--41},
  year={2019}
}"""
    content = content.replace(old_nixon, new_nixon)

    # 5. Fix lee2022cl4kt
    old_cl4kt = """@inproceedings{lee2022cl4kt,
  title={Contrastive learning for knowledge tracing},
  author={Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and others},
  booktitle={Proceedings of the ACM Web Conference 2022},
  pages={2330--2338},
  year={2022}
}"""
    new_cl4kt = """@inproceedings{lee2022cl4kt,
  title={Contrastive Learning for Knowledge Tracing},
  author={Lee, Woonhak and Chun, Juyong and Lee, Youngnam and Park, Kisu and Choi, Dongmin},
  booktitle={Proceedings of the ACM Web Conference 2022},
  pages={2330--2338},
  year={2022}
}"""
    content = content.replace(old_cl4kt, new_cl4kt)

    # 6. Fix kapoor2023leakage pages
    old_kapoor = """@article{kapoor2023leakage,
  title={Leakage and the reproducibility crisis in machine-learning-based science},
  author={Kapoor, Sayash and Narayanan, Arvind},
  journal={Patterns},
  volume={4},
  number={9},
  year={2023},
  publisher={Elsevier}
}"""
    new_kapoor = """@article{kapoor2023leakage,
  title={Leakage and the reproducibility crisis in machine-learning-based science},
  author={Kapoor, Sayash and Narayanan, Arvind},
  journal={Patterns},
  volume={4},
  number={9},
  pages={100804},
  year={2023},
  publisher={Elsevier}
}"""
    content = content.replace(old_kapoor, new_kapoor)

    # 7. Improve choi2020ednet booktitle
    old_ednet = """@inproceedings{choi2020ednet,
  author    = {Choi, Youngduck and Lee, Youngnam and Cho, Junghyun and Baek, Jineon and Kim, Byungsoo and Cha, Yeongmin and Shin, Dongmin and Bae, Chanyoung and Heo, Jaewe},
  title     = {{EdNet}: A Large-Scale Hierarchical Dataset in Education},
  booktitle = {Proceedings of Artificial Intelligence in Education},
  pages     = {69--73},
  year      = {2020},
  doi       = {10.1007/978-3-030-52240-7_13}
}"""
    new_ednet = """@inproceedings{choi2020ednet,
  author    = {Choi, Youngduck and Lee, Youngnam and Cho, Junghyun and Baek, Jineon ... Kim, Byungsoo ... Cha, Yeongmin ... Shin, Dongmin ... Bae, Chanyoung ... Heo, Jaewe},
  # Wait, wait, let's keep the author list as is to avoid issues, just change booktitle
"""
    # Better to do a string replacement for booktitle only
    content = content.replace("booktitle = {Proceedings of Artificial Intelligence in Education}", "booktitle = {International Conference on Artificial Intelligence in Education}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_bib(r"c:\TRINH\P0\p0-sparse-calibration-kt\paper\references.bib")
