import os

def fix_bbl(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix liu2023xes3g5m
    old_xes = r"""\bibitem{liu2023xes3g5m}
Liu Z, Teng Q, Chen J, Huang S, Fang J, Gao M, Tang J, Luo W (2023) XES3G5M: A Knowledge Tracing Benchmark Dataset with Auxiliary Information. \textit{Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track}."""
    
    new_xes = r"""\bibitem{liu2023xes3g5m}
Liu Z, Liu Q, Guo T, Chen J, Huang S, Zhao X, Tang J, Luo W, Weng J (2023) XES3G5M: A Knowledge Tracing Benchmark Dataset with Auxiliary Information. \textit{Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track}."""
    
    content = content.replace(old_xes, new_xes)

    # 2. Fix choffin2019das3h
    old_das = r"""\bibitem{choffin2019das3h}
Choffin B, Popineau F, Bourda Y, Vie J (2019) DAS3H: Modeling Student Learning and Forgetting for Optimally Scheduling Distributed Practice of Skills. \textit{Proceedings of the 12th International Conference on Educational Data Mining}."""
    
    new_das = r"""\bibitem{choffin2019das3h}
Choffin B, Popineau F, Bourda Y, Vie JJ (2019) DAS3H: Modeling Student Learning and Forgetting for Optimally Scheduling Distributed Practice of Skills. \textit{Proceedings of the 12th International Conference on Educational Data Mining}:276-281."""
    
    content = content.replace(old_das, new_das)

    # 3. Fix kapoor2023leakage
    old_kapoor = r"""\bibitem{kapoor2023leakage}
Kapoor S, Narayanan A (2023) Leakage and the reproducibility crisis in machine-learning-based science. \textit{Patterns} 4(9)."""
    
    new_kapoor = r"""\bibitem{kapoor2023leakage}
Kapoor S, Narayanan A (2023) Leakage and the reproducibility crisis in machine-learning-based science. \textit{Patterns} 4(9):100804."""
    
    content = content.replace(old_kapoor, new_kapoor)

    # 4. Fix choi2020ednet
    old_ednet = r"""\bibitem{choi2020ednet}
Choi Y, Lee Y, Cho J, Baek J, Kim B, Cha Y, Shin D, Bae C, Heo J (2020) EdNet. \textit{Proceedings of Artificial Intelligence in Education}:69-73. \doi{10.1007/978-3-030-52240-7_13}"""
    
    new_ednet = r"""\bibitem{choi2020ednet}
Choi Y, Lee Y, Cho J, Baek J, Kim B, Cha Y, Shin D, Bae C, Heo J (2020) EdNet: A Large-Scale Hierarchical Dataset in Education. \textit{International Conference on Artificial Intelligence in Education}:69-73. \doi{10.1007/978-3-030-52240-7_13}"""
    
    content = content.replace(old_ednet, new_ednet)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed: {filepath}")

if __name__ == "__main__":
    fix_bbl(r"c:\TRINH\P0\p0-sparse-calibration-kt\paper\references.bbl")
    fix_bbl(r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\references.bbl")
