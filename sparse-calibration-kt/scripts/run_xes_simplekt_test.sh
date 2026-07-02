#!/usr/bin/env bash
# run_xes_simplekt_test.sh
# Mini test chạy mô hình SimpleKT trên GPU với bộ dữ liệu xes3g5m sample với 3 seed 42, 2024, 2025.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/xes_simplekt_test.yaml
