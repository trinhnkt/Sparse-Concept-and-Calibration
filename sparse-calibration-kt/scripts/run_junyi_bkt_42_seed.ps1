# run_junyi_bkt_one_seed.ps1
# Huấn luyện mô hình BKT trên TOÀN BỘ bộ dữ liệu Junyi lớn (3GB) với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\junyi_bkt_one_seed.yaml
