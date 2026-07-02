# run_assist_simplekt_one_seed.ps1
# Huấn luyện mô hình SimpleKT trên TOÀN BỘ bộ dữ liệu ASSISTments 2012 lớn trên GPU với duy nhất 1 seed 42.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\assist_simplekt_one_seed.yaml
