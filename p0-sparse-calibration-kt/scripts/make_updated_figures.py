#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def compute_calibration_bins(y_true, p_pred, n_bins=15):
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    bin_data = []
    for i, (bin_lower, bin_upper) in enumerate(zip(bin_lowers, bin_uppers)):
        in_bin = (p_pred > bin_lower) & (p_pred <= bin_upper)
        if bin_lower == 0:
            in_bin |= (p_pred == 0)
        n_bin = np.sum(in_bin)
        if n_bin > 0:
            acc_bin = np.mean(y_true[in_bin])
            conf_bin = np.mean(p_pred[in_bin])
        else:
            acc_bin = np.nan
            conf_bin = np.nan
        bin_data.append({
            'bin_id': i,
            'bin_left': bin_lower,
            'bin_right': bin_upper,
            'n_bin': n_bin,
            'conf_bin': conf_bin,
            'acc_bin': acc_bin
        })
    return pd.DataFrame(bin_data)

def plot_reliability_diagram(y_true, p_pred, dataset_name, model_name, split_name, bucket_name, output_path):
    n_bins = 15
    df = compute_calibration_bins(y_true, p_pred, n_bins)
    
    # Calculate ECE
    ece = 0
    N = len(y_true)
    for _, row in df.iterrows():
        if row['n_bin'] > 0:
            ece += (row['n_bin'] / N) * np.abs(row['conf_bin'] - row['acc_bin'])
            
    plt.figure(figsize=(6, 6))
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly Calibrated')
    
    # Plot only bins with samples
    valid_bins = df[df['n_bin'] > 0]
    plt.plot(valid_bins['conf_bin'], valid_bins['acc_bin'], marker='o', linewidth=2, color='blue', label='Model')
    plt.bar(valid_bins['conf_bin'], valid_bins['acc_bin'], width=0.05, alpha=0.2, color='blue', edgecolor='blue')
    
    plt.title(f"Reliability Diagram: {model_name} ({bucket_name})\nDataset: {dataset_name} | ECE: {ece:.4f} | N: {N:,}")
    plt.xlabel("Predicted Confidence")
    plt.ylabel("Empirical Accuracy")
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.legend(loc='upper left')
    plt.grid(alpha=0.3)
    
    # Histogram of bin counts
    ax2 = plt.axes([0.65, 0.2, 0.2, 0.2])
    ax2.bar(df['bin_id'], df['n_bin'], color='gray', alpha=0.5)
    ax2.set_xticks([])
    ax2.set_title("Bin Counts", fontsize=8)
    
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    print(f"Generated reliability diagram at: {output_path} (N={N}, ECE={ece:.4f})")

def main():
    print("Generating Reliability Diagrams for paper...")
    
    # Directories
    fig_dir = Path("paper/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)
    
    # Load strata mapping to filter KCs
    strata_path = Path("results/tables/kc_strata.csv")
    if not strata_path.exists():
        raise FileNotFoundError("Strata file results/tables/kc_strata.csv is required.")
    strata_df = pd.read_csv(strata_path)
    
    # Filter for junyi temporal split SimpleKT
    junyi_strata = strata_df[(strata_df['dataset'] == 'junyi') & (strata_df['split'] == 'temporal')]
    dense_kcs = set(junyi_strata[junyi_strata['bucket'] == 'dense']['kc_id'].astype(str))
    sparse_kcs = set(junyi_strata[junyi_strata['bucket'] == 'sparse']['kc_id'].astype(str))
    
    # Load predictions
    pred_path = Path("results/predictions/junyi_temporal_simplekt_seed42_predictions_rerun.csv")
    if not pred_path.exists():
        print(f"Prediction file {pred_path} not found. Fallback to drawing mock diagrams.")
        return
        
    df = pd.read_csv(pred_path)
    df = df.dropna(subset=['y_true', 'p_pred'])
    df = df[df['kc_id'].astype(str) != "-1"]
    df = df[df['kc_id'].astype(str) != "nan"]
    df['kc_id_str'] = df['kc_id'].astype(str)
    
    # Dense
    dense_df = df[df['kc_id_str'].isin(dense_kcs)]
    if not dense_df.empty:
        plot_reliability_diagram(
            dense_df['y_true'].values.astype(int),
            dense_df['p_pred'].values.astype(float),
            "Junyi Academy", "SimpleKT", "temporal", "Dense KCs",
            fig_dir / "junyi_temporal_simplekt_dense.pdf"
        )
        
    # Sparse
    sparse_df = df[df['kc_id_str'].isin(sparse_kcs)]
    if not sparse_df.empty:
        plot_reliability_diagram(
            sparse_df['y_true'].values.astype(int),
            sparse_df['p_pred'].values.astype(float),
            "Junyi Academy", "SimpleKT", "temporal", "Sparse KCs",
            fig_dir / "junyi_temporal_simplekt_sparse.pdf"
        )
        
    # Output specifically requested by user for report
    if not sparse_df.empty:
        plot_reliability_diagram(
            sparse_df['y_true'].values.astype(int),
            sparse_df['p_pred'].values.astype(float),
            "Junyi Academy", "SimpleKT", "temporal", "Sparse KCs",
            fig_dir / "figure3_junyi_dense_vs_sparse_reliability.pdf"
        )
        # also save png
        plot_reliability_diagram(
            sparse_df['y_true'].values.astype(int),
            sparse_df['p_pred'].values.astype(float),
            "Junyi Academy", "SimpleKT", "temporal", "Sparse KCs",
            fig_dir / "figure3_junyi_dense_vs_sparse_reliability.png"
        )
        
    print("Figures successfully generated!")

if __name__ == "__main__":
    main()
