# Rerun Environment Report

- **Python version**: 3.9+ (Windows environment)
- **PyTorch version**: 1.12.0+ (used during model inference and baseline runs)
- **GPU Acceleration**: CUDA was utilized where available for loading cached neural model predictions. Training for IRT baselines was executed on CPU (fast).
- **Reproducibility**: Seeds (42, 2024, 2025, 2026, 2027) were controlled using Python `random`, `numpy.random`, and `torch.manual_seed` to ensure consistency.

