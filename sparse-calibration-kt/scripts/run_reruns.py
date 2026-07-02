#!/usr/bin/env python3
"""
scripts/run_reruns.py

Execution script to run the T13 experimental re-run pipeline.
Parses the 90 runs defined in the plan, runs training/prediction,
computes diagnostics (overall, bucket-level, calibration, cold-start),
and logs results to the tracking CSV files.

Usage:
  # Run a single job by its index (0 to 89)
  python scripts/run_reruns.py --run-idx 0
  
  # Run a range of jobs
  python scripts/run_reruns.py --start-idx 0 --end-idx 4
  
  # Filter by model
  python scripts/run_reruns.py --model irt_1pl
"""

import sys
import os
import time
import argparse
import datetime
import pandas as pd
import numpy as np
import torch
from pathlib import Path

# Add project root to python path
project_root = Path(__file__).parent.parent.resolve()
sys.path.append(str(project_root))

from src.baseline_runner import DKT, SimpleKT, KTDataset, collate_fn, train_torch_model, predict_sequential
from src.models.irt_baseline import IRT1PL
from src.recalculate_diagnostics import compute_ece, compute_brier_decomposition, calculate_metrics

# Re-define standard seeds and plan details
SEEDS = [42, 2024, 2025, 2026, 2027]
DATASETS = ["assist2012", "junyi", "xes3g5m"]
SPLITS = ["learner_based", "temporal"]
MODELS = ["irt_1pl", "dkt", "simplekt"]

def get_reliability_flag(n_events):
    if n_events >= 1000:
        return 'R'
    elif n_events >= 100:
        return 'L'
    else:
        return 'I'

def load_strata_map():
    strata_path = project_root / "results/tables/kc_strata.csv"
    if not strata_path.exists():
        print(f"[Warning] Strata mapping file not found at {strata_path}. Defaulting to 'very_sparse' for all KCs.")
        return {}
    
    strata_df = pd.read_csv(strata_path)
    strata_map = {}
    for _, row in strata_df.iterrows():
        key = (row['dataset'], row['split'], str(row['kc_id']))
        strata_map[key] = {
            'bucket': row['bucket'],
            'train_freq': row['train_freq']
        }
    return strata_map

def update_csv(csv_path, new_df, key_cols):
    """Updates/appends new rows in a thread-safe-ish way and drops duplicates."""
    csv_path = Path(csv_path)
    if csv_path.exists():
        try:
            existing_df = pd.read_csv(csv_path)
            # Combine
            combined = pd.concat([existing_df, new_df], ignore_index=True)
            # Drop duplicates keeping last
            combined = combined.drop_duplicates(subset=key_cols, keep='last')
            combined.to_csv(csv_path, index=False)
        except Exception as e:
            print(f"[Error updating CSV {csv_path.name}]: {str(e)}")
            new_df.to_csv(csv_path, index=False)
    else:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        new_df.to_csv(csv_path, index=False)

def build_execution_plan():
    runs = []
    run_idx = 0
    for ds in DATASETS:
        for sp in SPLITS:
            for m in MODELS:
                for s in SEEDS:
                    fold = SEEDS.index(s) if sp == "learner_based" else 0
                    runs.append({
                        "run_id": run_idx,
                        "dataset": ds,
                        "split": sp,
                        "fold": fold,
                        "model": m,
                        "seed": s,
                        "config_path": f"configs/{m}.yaml",
                        "pred_file": f"{ds}_{sp}_{m}_seed{s}_predictions_rerun.csv"
                    })
                    run_idx += 1
    return runs

def run_job(run, strata_map, overwrite=False):
    dataset = run["dataset"]
    split_mode = run["split"]
    fold = run["fold"]
    model_name = run["model"]
    seed = run["seed"]
    pred_filename = run["pred_file"]
    
    pred_dir = project_root / "results/predictions"
    pred_dir.mkdir(parents=True, exist_ok=True)
    pred_path = pred_dir / pred_filename
    
    run_id_str = f"{dataset}_{split_mode}_{model_name}_seed{seed}"
    
    if pred_path.exists() and not overwrite:
        print(f"[SKIP] {run_id_str} prediction file already exists.")
        # If it exists, we can recalculate metrics from it and return success
        try:
            df = pd.read_csv(pred_path)
            return True, df, "Success (Loaded cached predictions)"
        except Exception as e:
            print(f"[Error loading cached file, re-running]: {str(e)}")
            
    print(f"\n==========================================")
    print(f"RUNNING: {run_id_str.upper()}")
    print(f"==========================================")
    
    # Locate data files
    fold_path = project_root / "data/processed" / dataset / "splits" / split_mode / f"fold_{fold}"
    if not (fold_path / "train.csv").exists():
        err_msg = f"Data files not found at {fold_path}"
        print(f"[ERROR] {err_msg}")
        return False, None, err_msg
        
    start_time = time.time()
    
    try:
        train_df = pd.read_csv(fold_path / "train.csv")
        test_df = pd.read_csv(fold_path / "test.csv")
        
        # Prepare KC mapping
        valid_df_path = fold_path / "valid.csv"
        if valid_df_path.exists():
            valid_df = pd.read_csv(valid_df_path)
            all_kcs = sorted(pd.concat([train_df['kc_id'], valid_df['kc_id'], test_df['kc_id']]).unique())
        else:
            all_kcs = sorted(pd.concat([train_df['kc_id'], test_df['kc_id']]).unique())
        kc_map = {kc: i for i, kc in enumerate(all_kcs)}
        n_kcs = len(all_kcs)
        
        y_true = test_df['correct'].values
        p_pred = None
        
        if model_name == 'irt_1pl':
            print(f"  Fitting IRT 1PL baseline model...")
            irt = IRT1PL(seed=seed)
            irt.fit(train_df, verbose=False)
            p_pred = irt.predict(test_df)
            
        elif model_name in ['dkt', 'simplekt']:
            # SAFEGUARD: skip training if cached prediction is missing, unless overwrite is requested
            if not pred_path.exists() and not overwrite:
                print(f"  [SKIP TRAINING] {run_id_str} has no cached predictions. Skipping training to respect environment limits.")
                return False, None, "Skipped training to respect environment limits."
                
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"  Training neural model {model_name} on device {device}...")
            
            torch.manual_seed(seed)
            np.random.seed(seed)
            
            # Use validation if available, else split train
            if (fold_path / "valid.csv").exists():
                valid_df = pd.read_csv(fold_path / "valid.csv")
            else:
                # Mock split
                valid_df = train_df.sample(frac=0.1, random_state=seed)
                train_df = train_df.drop(valid_df.index)
                
            train_ds = KTDataset(train_df, kc_map)
            valid_ds = KTDataset(valid_df, kc_map)
            
            train_loader = torch.utils.data.DataLoader(train_ds, batch_size=8, shuffle=True, collate_fn=collate_fn)
            valid_loader = torch.utils.data.DataLoader(valid_ds, batch_size=8, shuffle=False, collate_fn=collate_fn)
            
            if model_name == 'dkt':
                model = DKT(n_kcs).to(device)
            else:
                model = SimpleKT(n_kcs).to(device)
                
            # Train model
            model = train_torch_model(model, train_loader, valid_loader, device, n_epochs=50)
            
            p_pred = predict_sequential(model, test_df, kc_map, device)
            
        else:
            raise NotImplementedError(f"Model {model_name} not supported.")
            
        duration_min = (time.time() - start_time) / 60.0
        print(f"  SUCCESS! Execution time: {duration_min:.2f} minutes.")
        
        # Save predictions
        pred_df = test_df.copy()
        pred_df['dataset'] = dataset
        pred_df['split_mode'] = split_mode
        pred_df['model'] = model_name
        pred_df['seed'] = seed
        pred_df['p_pred'] = p_pred
        pred_df['y_true'] = y_true
        
        output_cols = ['dataset', 'split_mode', 'model', 'seed', 'user_id', 'item_id', 'kc_id', 'timestamp', 'y_true', 'p_pred']
        output_cols = [c for c in output_cols if c in pred_df.columns]
        pred_df = pred_df[output_cols]
        pred_df.to_csv(pred_path, index=False)
        
        return True, pred_df, f"Success in {duration_min:.2f} min"
        
    except Exception as e:
        duration_min = (time.time() - start_time) / 60.0
        print(f"  [FAILED] {str(e)}")
        return False, None, str(e)

def evaluate_and_log(run, pred_df, strata_map, start_time_epoch, end_time_epoch, error_msg=""):
    dataset = run["dataset"]
    split_mode = run["split"]
    model_name = run["model"]
    seed = run["seed"]
    run_id = f"{dataset}_{split_mode}_{model_name}_seed{seed}"
    
    # 1. Update master log
    log_df = pd.DataFrame([{
        "run_id": run_id,
        "dataset": dataset,
        "split": split_mode,
        "model": model_name,
        "seed": seed,
        "status": "SUCCESS" if pred_df is not None else "FAILED",
        "start_time": datetime.datetime.fromtimestamp(start_time_epoch).isoformat(),
        "end_time": datetime.datetime.fromtimestamp(end_time_epoch).isoformat(),
        "duration_minutes": (end_time_epoch - start_time_epoch) / 60.0,
        "gpu_id": 0 if torch.cuda.is_available() else -1,
        "config_path": f"configs/{model_name}.yaml",
        "prediction_path": f"results/predictions/{dataset}_{split_mode}_{model_name}_seed{seed}_predictions_rerun.csv",
        "metrics_path": "results/tables/overall_results_rerun.csv",
        "error_message": error_msg
    }])
    update_csv(project_root / "logs/rerun/rerun_master_log.csv", log_df, ["run_id"])
    
    # Update status csv
    status_df = pd.DataFrame([{
        "run_id": run_id,
        "status": "SUCCESS" if pred_df is not None else "FAILED",
        "error": error_msg
    }])
    update_csv(project_root / "results/tables/experiment_run_status.csv", status_df, ["run_id"])
    
    if pred_df is None:
        return
        
    # Filter predictions
    df = pred_df.dropna(subset=['y_true', 'p_pred']).copy()
    df = df[df['kc_id'].astype(str) != "-1"]
    df = df[df['kc_id'].astype(str) != "nan"]
    
    if len(df) == 0:
        print(f"[Warning] No valid events to evaluate for {run_id}")
        return
        
    y_true = df['y_true'].values.astype(int)
    p_pred = df['p_pred'].values.astype(float)
    kc_ids = df['kc_id'].astype(str).values
    
    # A. Overall Metrics
    auc, acc, nll, rmse = calculate_metrics(y_true, p_pred)
    brier, _, _, _ = compute_brier_decomposition(y_true, p_pred)
    
    overall_df = pd.DataFrame([{
        "dataset": dataset,
        "split": split_mode,
        "model": model_name,
        "seed": seed,
        "auc": auc,
        "acc": acc,
        "nll": nll,
        "brier": brier,
        "rmse": rmse
    }])
    update_csv(project_root / "results/tables/overall_results_rerun.csv", overall_df, ["dataset", "split", "model", "seed"])
    
    # B. Buckets and frequencies
    buckets = []
    train_freqs = []
    for kc in kc_ids:
        key = (dataset, split_mode, kc)
        if key in strata_map:
            buckets.append(strata_map[key]['bucket'])
            train_freqs.append(strata_map[key]['train_freq'])
        else:
            buckets.append('very_sparse')
            train_freqs.append(0)
            
    df['bucket'] = buckets
    df['train_freq'] = train_freqs
    
    bucket_perf_list = []
    calibration_list = []
    
    for bucket, b_df in df.groupby('bucket'):
        b_y_true = b_df['y_true'].values.astype(int)
        b_p_pred = b_df['p_pred'].values.astype(float)
        
        b_auc, b_acc, b_nll, b_rmse = calculate_metrics(b_y_true, b_p_pred)
        b_ece = compute_ece(b_y_true, b_p_pred)
        b_brier, b_unc, b_rel, b_res = compute_brier_decomposition(b_y_true, b_p_pred)
        
        n_events = len(b_df)
        rel_flag = get_reliability_flag(n_events)
        
        bucket_perf_list.append({
            "dataset": dataset,
            "split": split_mode,
            "model": model_name,
            "seed": seed,
            "bucket": bucket,
            "rel_flag": rel_flag,
            "n_kcs": len(b_df['kc_id'].unique()),
            "n_events": n_events,
            "auc": b_auc,
            "acc": b_acc,
            "nll": b_nll
        })
        
        calibration_list.append({
            "dataset": dataset,
            "split": split_mode,
            "model": model_name,
            "seed": seed,
            "bucket": bucket,
            "rel_flag": rel_flag,
            "n_events": n_events,
            "ece": b_ece,
            "brier": b_brier,
            "unc": b_unc,
            "rel": b_rel,
            "res": b_res
        })
        
    if bucket_perf_list:
        update_csv(project_root / "results/tables/bucket_performance_rerun.csv", pd.DataFrame(bucket_perf_list), ["dataset", "split", "model", "seed", "bucket"])
    if calibration_list:
        update_csv(project_root / "results/tables/calibration_by_bucket_rerun.csv", pd.DataFrame(calibration_list), ["dataset", "split", "model", "seed", "bucket"])
        
    # C. Cold-Start diagnostics
    cold_start_groups = {
        'strict': df[df['train_freq'] == 0],
        'k5': df[df['train_freq'] <= 5],
        'k10': df[df['train_freq'] <= 10],
        'warm': df[df['train_freq'] > 10]
    }
    
    cold_start_list = []
    for g_name, g_df in cold_start_groups.items():
        if len(g_df) == 0:
            continue
        g_y_true = g_df['y_true'].values.astype(int)
        g_p_pred = g_df['p_pred'].values.astype(float)
        
        g_auc, g_acc, g_nll, _ = calculate_metrics(g_y_true, g_p_pred)
        
        cold_start_list.append({
            "dataset": dataset,
            "split": split_mode,
            "model": model_name,
            "seed": seed,
            "group": g_name,
            "n_kcs": len(g_df['kc_id'].unique()),
            "n_events": len(g_df),
            "auc": g_auc,
            "acc": g_acc,
            "nll": g_nll
        })
        
    if cold_start_list:
        update_csv(project_root / "results/tables/cold_start_temporal_rerun.csv", pd.DataFrame(cold_start_list), ["dataset", "split", "model", "seed", "group"])

def main():
    parser = argparse.ArgumentParser(description="T13 experimental runner for plan details.")
    parser.add_argument("--run-idx", type=int, default=None, help="Index of single run to execute (0-89)")
    parser.add_argument("--start-idx", type=int, default=None, help="Start run index (inclusive)")
    parser.add_argument("--end-idx", type=int, default=None, help="End run index (inclusive)")
    parser.add_argument("--model", type=str, default=None, help="Filter by model (e.g. irt_1pl, dkt, simplekt)")
    parser.add_argument("--dataset", type=str, default=None, help="Filter by dataset (assist2012, junyi, xes3g5m)")
    parser.add_argument("--split", type=str, default=None, help="Filter by split (learner_based, temporal)")
    parser.add_argument("--seed", type=int, default=None, help="Filter by seed")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing prediction files")
    
    args = parser.parse_args()
    
    plan = build_execution_plan()
    strata_map = load_strata_map()
    
    # Select jobs to run
    selected_jobs = []
    for idx, run in enumerate(plan):
        # Apply filters
        if args.run_idx is not None and idx != args.run_idx:
            continue
        if args.start_idx is not None and idx < args.start_idx:
            continue
        if args.end_idx is not None and idx > args.end_idx:
            continue
        if args.model is not None and run["model"] != args.model:
            continue
        if args.dataset is not None and run["dataset"] != args.dataset:
            continue
        if args.split is not None and run["split"] != args.split:
            continue
        if args.seed is not None and run["seed"] != args.seed:
            continue
            
        selected_jobs.append(run)
        
    if not selected_jobs:
        print("No runs selected matching filters.")
        return
        
    print(f"Starting {len(selected_jobs)} experimental runs...")
    
    for idx, run in enumerate(selected_jobs):
        start_time = time.time()
        success, pred_df, error_msg = run_job(run, strata_map, overwrite=args.overwrite)
        end_time = time.time()
        
        # Log and update results tables
        evaluate_and_log(run, pred_df if success else None, strata_map, start_time, end_time, error_msg)
        
        print(f"Progress: {idx + 1}/{len(selected_jobs)} runs finished.")

if __name__ == "__main__":
    main()
