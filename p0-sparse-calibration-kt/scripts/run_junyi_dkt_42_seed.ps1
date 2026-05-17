# run_junyi_dkt_one_seed.ps1
# Huấn luyện mô hình DKT trên TOÀN BỘ bộ dữ liệu Junyi lớn (3GB) trên GPU với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\junyi_dkt_one_seed.yaml
