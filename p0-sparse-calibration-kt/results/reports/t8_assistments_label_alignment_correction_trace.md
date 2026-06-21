# T8.1 ASSISTments Label-alignment Correction Trace

## 1. Summary

- **ASSISTments temporal issue trước correction:** DKT và SimpleKT đạt AUC xấp xỉ 0.50 (ngẫu nhiên) dưới temporal split ngay cả trên warm cohort. Logic BKT và IRT vẫn đạt AUC cao hơn (~0.65). Điều này cho thấy có sự lệch pha nghiêm trọng giữa predictions và labels.
- **Sau correction:** AUC trên warm cohort phục hồi về mức hợp lý:
  - DKT warm AUC đạt **0.6606** (seed 42).
  - SimpleKT warm AUC đạt **0.6734** (seed 42).

## 2. Commit / Diff Evidence

- **Commit hash:** `78998842fe23b4b6b332f998e2fda5525957fb36`
- **Commit message:** `Resolve final layout and consistency issues in P0(17)`
- **File path:** [src/baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py)
- **Line numbers:** ~246-276 in `baseline_runner.py` (before modifications).
- **Diff trước/sau:**

```diff
@@ -246,31 +246,40 @@ def run_experiments(config_path):
                     # For predictions in the required CSV format, we need to align with original test_df rows
                     # This is tricky with sequence models. A simpler way is to re-run prediction per user.
                     
-                    # To match the requested CSV exactly, let's predict for every interaction
-                    test_preds_list = []
+                    # BUG FIX (T11): Build predictions indexed by original DataFrame row index
+                    # to avoid prediction-label misalignment caused by groupby reordering.
+                    # test_df.groupby('user_id') iterates users in sorted user_id order,
+                    # but test_df rows may be in a different order (e.g., sorted by timestamp).
+                    # Assigning test_preds_list directly to pred_df['p_pred'] would misalign
+                    # predictions with labels. Fix: use a dict keyed by row index.
+                    test_preds_dict = {}  # {original_row_idx: pred_val}
+                    # Sort within each user's group by timestamp for causal correctness
+                    test_df_sorted = test_df.sort_values(['user_id', 'timestamp']) if 'timestamp' in test_df.columns else test_df.sort_values('user_id')
                     with torch.no_grad():
-                        for user_id, group in test_df.groupby('user_id'):
+                        for user_id, group in test_df_sorted.groupby('user_id', sort=True):
                             kcs = [kc_map[k] for k in group['kc_id'].values]
                             labels = group['correct'].values
+                            row_indices = group.index.tolist()
                             
-                            # Sequential prediction
+                            # Sequential prediction (causal: predict step i from history 0..i-1)
                             state_feats = []
                             for i in range(len(group)):
                                 current_kc = kcs[i]
                                 if i == 0:
-                                    # Cold start for this user, use global average or 0.5
-                                    pred_val = 0.5 
+                                    # Cold start for this user, use 0.5
+                                    pred_val = 0.5
                                 else:
                                     # Predict using previous interactions
                                     inp = torch.tensor([state_feats], dtype=torch.long).to(device)
-                                    out = model(inp) # (1, seq, n_kcs)
+                                    out = model(inp)  # (1, seq, n_kcs)
                                     pred_val = out[0, -1, current_kc].item()
                                 
-                                test_preds_list.append(pred_val)
+                                test_preds_dict[row_indices[i]] = pred_val
                                 # Update state for next step: kc * 2 + label
                                 state_feats.append(current_kc * 2 + labels[i])
-                                
-                    p_pred = np.array(test_preds_list)
+                    
+                    # Reconstruct p_pred aligned with test_df original row order
+                    p_pred = np.array([test_preds_dict[idx] for idx in test_df.index])
```

## 3. Root Cause

- **Mô tả bug alignment cụ thể:** 
  Khi thực hiện dự đoán tuần tự cho từng user trong test set, code cũ dùng vòng lặp `for user_id, group in test_df.groupby('user_id')`. Vòng lặp `groupby` này của pandas tự động duyệt qua các user theo thứ tự tăng dần của `user_id`. Kế đó, các dự đoán được gom vào một danh sách phẳng `test_preds_list` và gán trực tiếp lại vào `pred_df = test_df.copy()` thông qua `pred_df['p_pred'] = test_preds_list`.
  Tuy nhiên, trong `temporal` split, `test_df` được sắp xếp theo thời gian toàn cục (`timestamp`), hoàn toàn không theo thứ tự tăng dần của `user_id`. Việc gán trực tiếp một danh sách phẳng (được sinh ra theo thứ tự user_id) vào dataframe ban đầu (sắp xếp theo timestamp) đã phá vỡ hoàn toàn sự liên kết giữa nhãn thực tế (`y_true`) và giá trị dự đoán (`p_pred`) của từng dòng tương tác → AUC bị kéo về ngẫu nhiên (~0.50).
- **Dataset/split/model bị ảnh hưởng:**
  Tất cả các datasets (assist2012, junyi, xes3g5m) dưới split `temporal` khi chạy các mô hình tuần tự (DKT, SimpleKT) đều bị ảnh hưởng bởi lỗi này.

## 4. Correction Logic

- **Logic sửa chính xác:** 
  Thay vì lưu các dự đoán vào danh sách phẳng theo thứ tự duyệt của `groupby`, chúng ta khởi tạo một dictionary `test_preds_dict` có key là index gốc của tương tác đó trong dataframe `test_df` (`row_indices[i]`). Sau khi đã dự đoán xong cho tất cả các user, ta dựng lại mảng `p_pred` bằng cách lấy các giá trị dự đoán từ dict tương ứng với thứ tự index nguyên bản của `test_df`:
  `p_pred = np.array([test_preds_dict[idx] for idx in test_df.index])`

## 5. Evidence of Recovery on ASSISTments

- **AUC trước correction:** 
  - DKT temporal AUC: **0.4991**
  - SimpleKT temporal AUC: **0.5014**
- **AUC sau correction:** 
  - DKT temporal AUC: **0.6605** (Overall) / **0.6606** (Warm Cohort)
  - SimpleKT temporal AUC: **0.6730** (Overall) / **0.6734** (Warm Cohort)
