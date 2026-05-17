# run_assist_gpu_test.ps1
# Mini test chạy mô hình BKT, DKT, SimpleKT trên GPU với bộ dữ liệu ASSISTments 2012 sample với 3 seed 42, 2024, 2025.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\assist_gpu_test.yaml
