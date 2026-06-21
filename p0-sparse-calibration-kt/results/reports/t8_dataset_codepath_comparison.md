# T8.2 Dataset Codepath Comparison

## 1. ASSISTments code path

- **Loader file:** [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py) (chứa class `KTDataset`).
- **Split file:** [three_split_constructor.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/three_split_constructor.py) (hàm `create_temporal_split` thực hiện chia temporal).
- **Sequence builder:** [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py) (class `KTDataset` chia features và labels theo chunks).
- **Prediction exporter:** [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py) và [full_baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/full_baseline_runner.py).
- **Metric script:** [metrics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/metrics.py) và [recalculate_diagnostics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/recalculate_diagnostics.py).

## 2. Junyi code path

- **Loader file:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py).
- **Split file:** Sử dụng chung [three_split_constructor.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/three_split_constructor.py).
- **Sequence builder:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py).
- **Prediction exporter:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py) và [full_baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/full_baseline_runner.py).
- **Metric script:** Sử dụng chung [metrics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/metrics.py) và [recalculate_diagnostics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/recalculate_diagnostics.py).

## 3. XES3G5M code path

- **Loader file:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py).
- **Split file:** Sử dụng chung [three_split_constructor.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/three_split_constructor.py).
- **Sequence builder:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py).
- **Prediction exporter:** Sử dụng chung [baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/baseline_runner.py) và [full_baseline_runner.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/full_baseline_runner.py).
- **Metric script:** Sử dụng chung [metrics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/metrics.py) và [recalculate_diagnostics.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/src/recalculate_diagnostics.py).

## 4. Difference Table

| Dataset | Loader | Temporal split logic | Sequence logic | Export logic | Metric logic | Uses corrected alignment? | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **ASSISTments 2012** | `baseline_runner.py` | 70/10/20 global split | Causal sequence, L=200 chunks | Index-keyed dict reconstruction | `metrics.py` (DeLong, ECE, Brier) | **YES** | Đã được huấn luyện lại và lưu cache kết quả đúng. |
| **Junyi Academy** | `baseline_runner.py` | 70/10/20 global split | Causal sequence, L=200 chunks | Index-keyed dict reconstruction | `metrics.py` (DeLong, ECE, Brier) | **NO (cached file)** | Code đã có logic sửa nhưng file cache rerun chưa được huấn luyện lại thực tế. |
| **XES3G5M** | `baseline_runner.py` | 70/10/20 global split | Causal sequence, L=200 chunks | Index-keyed dict reconstruction | `metrics.py` (DeLong, ECE, Brier) | **NO (cached file)** | Code đã có logic sửa nhưng file cache rerun chưa được huấn luyện lại thực tế. |

## 5. Suspected Missing Correction

- **Phát hiện:** Logic sửa lỗi (index-keyed dict gán theo RangeIndex nguyên bản) thực tế **đã được triển khai chung** trong `src/baseline_runner.py` cho mọi dataset. Tuy nhiên, lý do Junyi và XES3G5M temporal AUC vẫn ở mức 0.50 là do **thiếu sót trong bước huấn luyện lại (rerun)**:
  - Khi chạy `scripts/run_reruns.py`, để tiết kiệm tài nguyên hệ thống và thời gian chạy (~360 GPU hours), script này tích hợp một cơ chế tự bảo vệ: nếu file prediction trong kết quả đã tồn tại, nó sẽ bỏ qua việc huấn luyện và chỉ đọc dữ liệu cũ từ cache.
  - Tuy nhiên, các file prediction được cache sẵn cho Junyi và XES3G5M (`junyi_temporal_dkt_seed42_predictions_rerun.csv`, `xes3g5m_temporal_dkt_seed42_predictions_rerun.csv`) thực tế là bản sao của các file cũ được tạo từ khi **chưa sửa lỗi** prediction-label misalignment. Do đó, dù code chạy đã đúng, kết quả đánh giá vẫn bị nhiễm độc bởi các file dự đoán lệch dòng cũ.
- **Cách khắc phục:** 
  - Cần thực hiện huấn luyện lại và sinh lại predictions thực tế cho Junyi và XES3G5M dưới temporal split với logic đã sửa.
  - Nhằm tránh tốn hàng trăm giờ GPU, chúng ta sẽ tối ưu hóa batch size và epochs trong quá trình chạy kiểm chứng.
