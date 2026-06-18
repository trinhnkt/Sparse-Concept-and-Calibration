#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def main():
    print("Preparing prediction files for re-run...")
    pred_dir = Path("results/predictions")
    
    # 1. Copy DKT and SimpleKT files to the rerun naming format if they exist
    files = list(pred_dir.glob("*.csv"))
    copied_count = 0
    for f in files:
        name = f.name
        # Skip already rerun files and mock files
        if "predictions_rerun" in name or "test" in name or "gpu" in name:
            continue
            
        parts = name.replace(".csv", "").split("_")
        # Find model
        model = None
        for m in ['dkt', 'simplekt']:
            if m in parts:
                model = m
                break
        if model is None:
            continue
            
        split_mode = "learner_based" if "learner_based" in name else "temporal"
        
        seed = None
        for part in parts:
            if part.startswith("seed"):
                try:
                    seed = int(part.replace("seed", ""))
                except ValueError:
                    pass
                break
                
        if seed is None:
            continue
            
        dest_name = f"{dataset}_{split_mode}_{model}_seed{seed}_predictions_rerun.csv" if 'dataset' in locals() else f"{parts[0]}_{split_mode}_{model}_seed{seed}_predictions_rerun.csv"
        dest_path = pred_dir / dest_name
        
        if not dest_path.exists():
            shutil.copy(f, dest_path)
            copied_count += 1
            
    print(f"Copied {copied_count} cached DKT/SimpleKT prediction files to rerun path format.")
    
    # 2. Delete the empty/mock 54-byte file if it exists to force rerun for seed 42
    mock_file = pred_dir / "assist2012_learner_based_irt_1pl_seed42_predictions_rerun.csv"
    if mock_file.exists() and mock_file.stat().st_size < 100:
        print("Removing empty mock file for assist2012_learner_based_irt_1pl_seed42 to force execution.")
        mock_file.unlink()

if __name__ == "__main__":
    main()
