# run_junyi_minimal.ps1
# Runs reproduction pipeline for Junyi natively in PowerShell.

$env:PYTHONPATH="."
.\scripts\reproduce_one_dataset.ps1 configs\junyi.yaml
