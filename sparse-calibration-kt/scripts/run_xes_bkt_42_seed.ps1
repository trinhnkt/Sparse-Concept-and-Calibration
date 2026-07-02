# run_xes_bkt_one_seed.ps1
# Huấn luyện mô hình BKT trên TOÀN BỘ bộ dữ liệu xes3g5m lớn trên CPU với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\xes_bkt_one_seed.yaml
