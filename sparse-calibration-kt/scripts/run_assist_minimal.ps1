# run_assist_minimal.ps1
# Runs reproduction pipeline for ASSISTments 2012 natively in PowerShell.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\assist2012.yaml
