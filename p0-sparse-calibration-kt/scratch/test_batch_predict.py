import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from pathlib import Path

# Reuse models from baseline_runner
from src.baseline_runner import DKT, SimpleKT, predict_sequential

def predict_sequential_batched(model, test_df, kc_map, device, batch_size=2048):
    model.eval()
    test_df_sorted = test_df.sort_values(['user_id', 'timestamp']) if 'timestamp' in test_df.columns else test_df.sort_values('user_id')
    
    user_groups = test_df_sorted.groupby('user_id', sort=True)
    
    users_data = []
    for user_id, group in user_groups:
        kcs = [kc_map[k] for k in group['kc_id'].values]
        labels = group['correct'].values
        row_indices = group.index.tolist()
        state_feats = [kcs[i] * 2 + int(labels[i]) for i in range(len(group))]
        users_data.append({
            'kcs': kcs,
            'labels': labels,
            'row_indices': row_indices,
            'state_feats': state_feats,
            'len': len(group)
        })
        
    max_len = max(u['len'] for u in users_data)
    test_preds_dict = {}
    
    # Initialize all step 0 predictions to 0.5
    for u in users_data:
        test_preds_dict[u['row_indices'][0]] = 0.5
        
    with torch.no_grad():
        for step_idx in range(1, max_len):
            active_users = [u for u in users_data if u['len'] > step_idx]
            if not active_users:
                break
                
            for start_u in range(0, len(active_users), batch_size):
                sub_batch = active_users[start_u:start_u + batch_size]
                
                inp_list = [u['state_feats'][:step_idx] for u in sub_batch]
                inp_tensor = torch.tensor(inp_list, dtype=torch.long, device=device)
                
                target_kcs = [u['kcs'][step_idx] for u in sub_batch]
                
                out = model(inp_tensor) # (sub_batch_size, step_idx, n_kcs)
                
                preds = out[torch.arange(len(sub_batch)), -1, target_kcs].cpu().numpy()
                
                for idx, u in enumerate(sub_batch):
                    row_idx = u['row_indices'][step_idx]
                    test_preds_dict[row_idx] = float(preds[idx])
                    
    p_pred = np.array([test_preds_dict[idx] for idx in test_df.index])
    return p_pred

def test_equivalence():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Testing on device: {device}")
    
    # Load a small dataset
    dataset_name = "xes_gpu_test"
    base_path = Path(f"data/processed/{dataset_name}/splits/temporal/fold_0")
    if not base_path.exists():
        print("Dataset xes_gpu_test splits not found. Please run preprocessing first.")
        return
        
    train_df = pd.read_csv(base_path / "train.csv")
    valid_df = pd.read_csv(base_path / "valid.csv")
    test_df = pd.read_csv(base_path / "test.csv")
    
    all_kcs = sorted(pd.concat([train_df['kc_id'], valid_df['kc_id'], test_df['kc_id']]).unique())
    kc_map = {kc: i for i, kc in enumerate(all_kcs)}
    n_kcs = len(all_kcs)
    
    print(f"Loaded {dataset_name} with {n_kcs} KCs, test set rows: {len(test_df)}")
    
    # Initialize random models
    dkt_model = DKT(n_kcs).to(device)
    simplekt_model = SimpleKT(n_kcs).to(device)
    
    # Run predictions on DKT
    print("Running DKT predictions...")
    import time
    t0 = time.time()
    preds_seq_dkt = predict_sequential(dkt_model, test_df, kc_map, device)
    t1 = time.time()
    preds_batch_dkt = predict_sequential_batched(dkt_model, test_df, kc_map, device)
    t2 = time.time()
    
    print(f"DKT sequential: {t1 - t0:.4f}s, DKT batched: {t2 - t1:.4f}s")
    diff_dkt = np.max(np.abs(preds_seq_dkt - preds_batch_dkt))
    print(f"DKT Max Absolute Difference: {diff_dkt:.6e}")
    assert np.allclose(preds_seq_dkt, preds_batch_dkt, atol=1e-4), "DKT predictions do not match!"
    
    # Run predictions on SimpleKT
    print("Running SimpleKT predictions...")
    t0 = time.time()
    preds_seq_skt = predict_sequential(simplekt_model, test_df, kc_map, device)
    t1 = time.time()
    preds_batch_skt = predict_sequential_batched(simplekt_model, test_df, kc_map, device)
    t2 = time.time()
    
    print(f"SimpleKT sequential: {t1 - t0:.4f}s, SimpleKT batched: {t2 - t1:.4f}s")
    diff_skt = np.max(np.abs(preds_seq_skt - preds_batch_skt))
    print(f"SimpleKT Max Absolute Difference: {diff_skt:.6e}")
    assert np.allclose(preds_seq_skt, preds_batch_skt, atol=1e-4), "SimpleKT predictions do not match!"
    
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_equivalence()
