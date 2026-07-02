# Báo cáo Chỉnh sửa Tính Nhất quán Bài báo P0 (T16 - Final Polish)

**Ngày thực hiện:** 2026-06-18  
**Trạng thái:** ✅ ĐÃ HOÀN THÀNH (100% PASS)  

Báo cáo này tóm tắt kết quả giải quyết 8 điểm không nhất quán (consistency issues) cuối cùng trên bản thảo LaTeX và hình vẽ của bài báo P0 trước khi gửi lại GS Hậu thẩm định.

---

## 1. Tóm tắt Chi tiết 8 Sửa đổi Polish

### 1.1. Sửa Abstract claim về ranking-divergence
* **File chỉnh sửa:** [paper/main.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/main.tex) và [paper/main_submit_candidate.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/main_submit_candidate.tex) (Dòng 70–73).
* **Nội dung thay đổi:** Thay thế câu khẳng định mạnh về ranking divergence bằng câu thận trọng hơn:
  > *"Under our experimental conditions, calibration error varies substantially across KC-frequency strata, and aggregate AUC may obscure stratum-level reliability differences."*
* **Lý do:** Đảm bảo ngôn ngữ khoa học khách quan, không đưa ra các khẳng định quá mức chưa được chứng minh toàn diện trong mọi điều kiện.

### 1.2. Chỉnh sửa Figure 1 Pipeline Diagram
* **File chỉnh sửa:** [src/generate_pipeline_diagram.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/src/generate_pipeline_diagram.py) (Dòng 39).
* **Nội dung thay đổi:** Sửa nhãn `"Model Training (BKT, DKT, SimpleKT)"` thành `"Model Training (IRT, DKT, SimpleKT)"`.
* **Kết quả:** Đã chạy lại script nguồn để tái tạo hình ảnh PDF vector chuẩn hóa tại [paper/figures/figure1_pipeline.pdf](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/figures/figure1_pipeline.pdf). Biểu đồ mới đã hiển thị chính xác tên baseline `IRT` thay cho `BKT`.

### 1.3. Chỉnh sửa Note/Caption của Figure 3
* **File chỉnh sửa:** [paper/sections/04_experiments.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 67 và Dòng 84).
* **Nội dung thay đổi:** Loại bỏ khẳng định sai về việc nhóm `very sparse` của Junyi (N = 2,545) là "Insufficient" (vì N > 1000 thuộc nhóm Reliable). Thay bằng note chuẩn xác:
  > *"The very sparse stratum contains fewer KCs but sufficient test events (N = 2,545); thus, the curve is reported as a stratum-level calibration diagnostic rather than as an insufficient-sample estimate."*

### 1.4. Chỉnh sửa Diễn giải Temporal Split ở Table VI và RQ3
* **File chỉnh sửa:** 
  - [paper/sections/04_experiments.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 94).
  - [scripts/make_updated_latex_tables.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/scripts/make_updated_latex_tables.py) (Dòng 723 - Note của Table VI).
* **Nội dung thay đổi:** Thay vì tuyên bố chung chung là tất cả các mô hình đã phục hồi tín hiệu dự đoán trên temporal split, văn bản mới chỉ rõ:
  > *"After label-alignment correction, ASSISTments 2012 shows recovered temporal predictive signal on the warm cohort. However, Junyi Academy and XES3G5M still show near-random AUC for deep KT baselines under temporal splits, suggesting dataset-specific temporal generalization challenges that require further analysis."*

### 1.5. Sửa Số liệu đoạn XES3G5M Anomaly khớp với Table IV & V
* **File chỉnh sửa:** [paper/sections/04_experiments.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 54).
* **Nội dung thay đổi:** Đồng bộ hóa các giá trị AUC trong phần biện giải counter-pattern của XES3G5M chính xác với số liệu thực tế trong Table IV (Bản cập nhật):
  - Số cũ: *sparse (0.857, 0.850)* và *very sparse (0.874, 0.849)* so với *dense (0.819, 0.755)*.
  - Số mới: **sparse (0.8630, 0.8508)** và **very sparse (0.8708, 0.8593)** so với **dense (0.8186, 0.7554)** (cặp số lần lượt đại diện cho DKT và SimpleKT).

### 1.6. Thêm Giải thích việc Junyi Learner-based không có Sparse Bucket
* **File chỉnh sửa:** [paper/sections/04_experiments.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 57–58, ngay trước Table V).
* **Nội dung thay đổi:** Thêm đoạn giải thích:
  > *"On Junyi Academy under the learner-based split, the sparse and very sparse buckets are empty because all KCs have training-fold frequency at least 100. This absence is itself a diagnostic observation: Junyi does not exhibit learner-based sparse-KC concerns under the pre-registered thresholds."*

### 1.7. Làm rõ Caption của Table VIII (Sensitivity Analysis)
* **File chỉnh sửa:** [scripts/make_updated_latex_tables.py](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/scripts/make_updated_latex_tables.py) (Dòng 744).
* **Nội dung thay đổi:** Thêm câu làm rõ tính chất tổng hợp (aggregation) vào caption của bảng phân tích độ nhạy:
  > *"...Values are averaged across datasets and baselines for each threshold setting; standard deviations reflect between-dataset and between-baseline variation."*
* **Kết quả:** Đã chạy lại script sinh bảng LaTeX để cập nhật trực tiếp vào file [table_vii_threshold_sensitivity_updated.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/tables/table_vii_threshold_sensitivity_updated.tex) and [tableA1_sensitivity.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/tables/tableA1_sensitivity.tex).

### 1.8. Thêm Câu phối hợp với Công trình của NCS Tuấn vào Section V.B
* **File chỉnh sửa:** [paper/sections/05_discussion_limitations.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/05_discussion_limitations.tex) (Dòng 9).
* **Nội dung thay đổi:** Bổ sung vào cuối mục Scope Boundaries đoạn văn sau:
  > *"This paper focuses on downstream evaluation diagnostics for KT. A complementary line of work in our group addresses leakage control in concept-graph construction for graph-augmented KT. These two protocols are designed to be composable in future structure-aware KT studies."*

### 1.9. Giải thích sự chênh lệch AUC và ACC của mô hình IRT
* **File chỉnh sửa:** [paper/sections/04_experiments.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 40).
* **Nội dung thay đổi:** Bổ sung câu phân tích nguyên nhân tại sao mô hình IRT đạt độ chính xác (ACC) cao (~0.70–0.80) nhưng giá trị AUC lại ở mức ngẫu nhiên (0.5000) dưới learner-based splits để giải đáp thắc mắc của Reviewer:
  > *"IRT’s learner-based AUC remains at 0.50 because unseen learners do not have estimated ability parameters; however, its ACC reflects majority-class and item/concept difficulty effects rather than discriminative ranking ability."*

---

## 2. Xác nhận Tính Toàn vẹn và Thẩm định PDF

1. **Không thay đổi kết quả thực nghiệm:** Toàn bộ các giá trị trung bình, độ lệch chuẩn và số lượng sự kiện (`#Events`) của 56 cấu hình rerun thực tế không bị tác động dưới bất kỳ hình thức nào.
2. **Compile PDF thành công:** Tệp preview PDF vector chất lượng cao đã được cập nhật và biên dịch thành công tại:
   👉 **[paper/P0_16_consistency_fixed.pdf](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/P0_16_consistency_fixed.pdf)**
3. **Mã nguồn đồng bộ:** Tất cả các sửa đổi ở trên đều được thực hiện trực tiếp trên các tệp `.tex` nguồn tương ứng trong thư mục `paper/`.

---

## 3. Danh sách File thay đổi (Git Diff Summary)

```text
Changes not staged for commit:
  - modified: paper/appendix/appendix_a_sensitivity.tex
  - modified: paper/figures/figure1_pipeline.pdf
  - modified: paper/main.tex
  - modified: paper/main_submit_candidate.tex
  - modified: paper/sections/04_experiments.tex
  - modified: paper/sections/05_discussion_limitations.tex
  - modified: paper/tables/table6_cold_start_results.tex
  - modified: paper/tables/tableA1_sensitivity.tex
  - modified: paper/tables/table_vi_cold_start_temporal_updated.tex
  - modified: paper/tables/table_vii_threshold_sensitivity_updated.tex
  - modified: scripts/make_updated_latex_tables.py
  - modified: src/generate_pdf_presubmission_check.py
  - modified: src/generate_pipeline_diagram.py

Untracked files:
  - new file: paper/P0_16_consistency_fixed.pdf
```
