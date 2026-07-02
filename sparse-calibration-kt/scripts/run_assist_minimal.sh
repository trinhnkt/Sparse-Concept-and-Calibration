#!/usr/bin/env bash
# run_assist_minimal.sh
# Runs the reproduction pipeline for the ASSISTments 2012 dataset.

set -e

export PYTHONPATH="."
./scripts/reproduce_one_dataset.sh configs/assist2012.yaml
