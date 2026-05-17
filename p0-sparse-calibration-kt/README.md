# p0-sparse-calibration-kt

**Paper title:** *Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing*  
**Paper type:** Protocol / diagnostic / resource paper  

## Primary Goal
Build a reproducible experimental project that evaluates Knowledge Tracing baselines under sparse-concept, calibration, limited cold-start concept, and leakage-audit settings.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run minimal reproduction: `bash scripts/reproduce_one_dataset.sh --dataset assist2012`

## Project Structure
- `configs/`: Configuration files for datasets and experiments.
- `src/`: Core source code for preprocessing, splitting, training, and evaluation.
- `scripts/`: Shell scripts for reproducing experiments.
- `results/`: Output predictions, tables, and figures.
- `logs/`: Audit logs and experiment tracking.
