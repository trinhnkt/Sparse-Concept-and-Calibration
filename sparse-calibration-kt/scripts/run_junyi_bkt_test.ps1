# run_junyi_bkt_test.ps1
# Mini test chạy mô hình BKT với bộ dữ liệu Junyi sample với 3 seed 42, 2024, 2025.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\junyi_bkt_test.yaml
