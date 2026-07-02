#!/usr/bin/env bash
# run_junyi_bkt_test.sh
# Mini test chạy mô hình BKT với bộ dữ liệu Junyi sample với 3 seed 42, 2024, 2025.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/junyi_bkt_test.yaml
