#!/usr/bin/env bash
# run_xes_dkt_test.sh
# Mini test chạy mô hình DKT trên GPU với bộ dữ liệu xes3g5m sample với 3 seed 42, 2024, 2025.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/xes_dkt_test.yaml
