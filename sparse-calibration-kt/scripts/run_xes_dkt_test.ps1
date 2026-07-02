# run_xes_dkt_test.ps1
# Mini test chạy mô hình DKT trên GPU với bộ dữ liệu xes3g5m sample với 3 seed 42, 2024, 2025.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\xes_dkt_test.yaml
