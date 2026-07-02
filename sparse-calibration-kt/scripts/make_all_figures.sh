#!/usr/bin/env bash
# make_all_figures.sh
# Generates all reliability diagrams and visualization figures.

set -e

export PYTHONPATH="."
python src/reliability_diagram_plotter.py
