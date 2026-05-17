# run_xes_simplekt_one_seed.ps1
# Huấn luyện mô hình SimpleKT trên TOÀN BỘ bộ dữ liệu xes3g5m lớn trên GPU với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\xes_simplekt_one_seed.yaml
