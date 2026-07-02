#!/usr/bin/env bash
# run_junyi_minimal.sh
# Runs the reproduction pipeline for the Junyi dataset.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/junyi.yaml
