#!/usr/bin/env bash
# run_assist_gpu_test.sh
# Mini test chạy mô hình BKT, DKT, SimpleKT trên GPU với bộ dữ liệu ASSISTments 2012 sample với 3 seed 42, 2024, 2025.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/assist_gpu_test.yaml
