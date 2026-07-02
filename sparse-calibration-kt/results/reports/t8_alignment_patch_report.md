# T8.3 Alignment Patch Report

## 1. Files Modified

| File Path | Line Numbers | Summary of Change |
| :--- | :---: | :--- |
| [src/baseline_runner.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/src/baseline_runner.py) | ~156-186, ~237 | Định nghĩa hàm helper `predict_sequential` và thay thế logic dự đoán tuần tự bị trùng lặp. |
| [src/full_baseline_runner.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/src/full_baseline_runner.py) | ~13, ~138 | Import và gọi hàm `predict_sequential` thay cho khối logic trùng lặp. |
| [scripts/run_reruns.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/scripts/run_reruns.py) | ~35, ~201 | Import và gọi hàm `predict_sequential` thay cho khối logic trùng lặp. |

## 2. Alignment Logic After Patch

### Pseudocode
```python
def predict_sequential(model, test_df, kc_map, device):
    model.eval()
    test_preds_dict = {}
    
    # Sắp xếp để đảm bảo causal correctness (theo user và thời gian)
    test_df_sorted = test_df.sort_values(['user_id', 'timestamp'])
    
    for user_id, group in test_df_sorted.groupby('user_id', sort=True):
        state_feats = []
        for i in range(len(group)):
            if i == 0:
                pred_val = 0.5  # Cold start
            else:
                pred_val = model(state_feats) # Dự đoán dựa trên history
            
            # Ghi nhận kết quả dự đoán tương ứng với index dòng gốc trong test_df
            test_preds_dict[group.index[i]] = pred_val
            state_feats.append(kc * 2 + correct)
            
    # Dựng lại mảng dự đoán đúng theo thứ tự dòng ban đầu của test_df
    p_pred = np.array([test_preds_dict[idx] for idx in test_df.index])
    return p_pred
```

### Key Elements:
- **Keys used for alignment:** Original row index of `test_df` (RangeIndex `idx`).
- **Sort order:** Stable sort by `['user_id', 'timestamp']` for user sequential simulation, but mapped back to the original index order.
- **Pairing:** `p_pred` is aligned positionally with `test_df` index, so `p_pred[idx]` is paired exactly with `test_df.loc[idx, 'correct']`.

## 3. Dataset Coverage

- **ASSISTments:** Covered / Not changed (same logic used, verified working).
- **Junyi:** Fixed (uses the unified `predict_sequential` logic).
- **XES3G5M:** Fixed (uses the unified `predict_sequential` logic).

## 4. Risk Assessment

- **Multi-skill/Multi-KC rows (XES3G5M):** XES3G5M có một số dòng có cùng `user_id` và `timestamp` do multi-skill expansion. Pandas `sort_values` thực hiện sắp xếp mặc định ổn định (stable sort) giữ nguyên thứ tự xuất hiện ban đầu, do đó index gốc được giữ vững và gán đúng. Không có nguy cơ gán nhầm.
- **Dữ liệu lớn:** Hàm `predict_sequential` được tối ưu hóa chạy trực tiếp trên GPU và lưu dict thông qua list index lookup, hoạt động hiệu quả trên cả bộ dữ liệu lớn.
