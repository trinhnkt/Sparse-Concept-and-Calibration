#!/usr/bin/env bash
# make_all_tables.sh
# Generates all LaTeX tables and reports from the results.

set -e

export PYTHONPATH="."
python src/report_generator.py --project-root . --output results/reports/p0_diagnostic_report.md
