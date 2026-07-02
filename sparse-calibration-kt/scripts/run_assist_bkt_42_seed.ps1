# run_assist_bkt_one_seed.ps1
# Huấn luyện mô hình BKT trên TOÀN BỘ bộ dữ liệu ASSISTments 2012 lớn trên CPU với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\assist_bkt_42_seed.yaml
