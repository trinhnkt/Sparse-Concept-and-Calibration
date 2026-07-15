# Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper](https://img.shields.io/badge/Paper-JEDM-green.svg)](#) <!-- Thêm link bài báo sau khi Accept -->

This repository contains the official PyTorch implementation and diagnostic evaluation protocol for the paper **"Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing"** (submitted to *Journal of Educational Data Mining - JEDM*).

## 📌 Overview
Current Knowledge Tracing (KT) evaluations often rely on aggregate predictive metrics (e.g., global AUC) that mask severe performance degradation on **sparse and cold-start knowledge components (KCs)**. This repository provides a dataset-agnostic diagnostic protocol that extends standard KT evaluation with:
- KC-frequency stratification (Dense, Medium, Sparse, Very Sparse).
- Per-stratum calibration diagnostics (Expected Calibration Error - ECE, Brier Score, NLL).
- An **eight-channel leakage and predictive-sanity audit** to prevent data contamination (especially in temporal splits).

## 🚀 1. Installation & Clean Environment Setup

We highly recommend using a clean virtual environment (Conda or venv) to ensure strict reproducibility.

```bash
# 1. Clone the repository
git clone https://github.com/anonymous-researcher-2026/sparse-calibration-kt.git
cd sparse-calibration-kt

# 2. Create and activate a virtual environment
conda create -n sparse_kt python=3.9 -y
conda activate sparse_kt

# 3. Install dependencies
pip install -r requirements.txt
```
*(All random seeds are strictly fixed across the codebase (e.g., `seed=42`) to guarantee identical outputs).*

## 📊 2. Datasets & Preprocessing
The experiments are conducted on three large-scale educational datasets (totalling ~26.8M interactions):
1. **ASSISTments 2012**
2. **Junyi Academy**
3. **XES3G5M**

**Data Setup:**
Download the raw datasets from their official sources and place them in the `data/raw/` directory. Then, run the preprocessing pipeline to filter sequence lengths and build KC vocabularies without data leakage:
```bash
bash scripts/run_preprocessing.sh
```

## ⚙️ 3. Training & Reproducing Results
We provide out-of-the-box scripts to train and evaluate the baseline models (IRT, DKT, SimpleKT) under our rigorous diagnostic protocol.

To reproduce the **Learner-based Split** (Zero-shot unseen learner evaluation) and the **Temporal Split**:
```bash
# Run Item Response Theory (IRT)
bash scripts/run_irt.sh

# Run Deep Knowledge Tracing (DKT)
bash scripts/run_dkt.sh

# Run SimpleKT
bash scripts/run_simplekt.sh
```

To reproduce the **Eight-Channel Leakage Audit** and generate the calibration reliability diagrams:
```bash
bash scripts/run_8_channel_audit.sh
```
*Note: The evaluation logs containing Mean ± Std (over 5 random seeds) will be saved in the `results/` folder, which exactly matches the tables reported in the paper.*

## 📖 Citation
If you find this protocol or codebase useful for your research, please cite our paper:

```bibtex
@article{sparse_calibration_kt,
  title={Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing},
  author={Anonymous Authors},
  journal={Journal of Educational Data Mining},
  year={2026}
}
```

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
