Write-Host "Starting temporal diagnostics for Junyi and XES3G5M..."
# Run DKT on Junyi
python scripts\run_reruns.py --config configs\junyi_dkt_test.yaml
# Run SimpleKT on Junyi
python scripts\run_reruns.py --config configs\junyi_simplekt_test.yaml
# Run DKT on XES3G5M
python scripts\run_reruns.py --config configs\xes_dkt_test.yaml
# Run SimpleKT on XES3G5M
python scripts\run_reruns.py --config configs\xes_simplekt_test.yaml
Write-Host "Temporal diagnostics completed."
