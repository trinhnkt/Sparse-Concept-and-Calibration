#!/usr/bin/env bash
# run_junyi_bkt_one_seed.sh
# Huấn luyện mô hình BKT trên TOÀN BỘ bộ dữ liệu Junyi lớn (3GB) với duy nhất 1 seed 42.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/junyi_bkt_one_seed.yaml
