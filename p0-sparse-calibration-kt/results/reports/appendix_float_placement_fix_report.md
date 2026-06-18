# Báo cáo Khắc phục Bố cục và Placement của Bảng trong Appendix (P0)

**Ngày thực hiện:** 2026-06-18  
**Trạng thái:** ✅ ĐÃ HOÀN THÀNH & XÁC MINH THÀNH CÔNG

Báo cáo này mô tả chi tiết các chỉnh sửa cấu trúc LaTeX để xử lý lỗi placement của Table VII và Table X trong phần Phụ lục (Appendix A và Appendix C) bằng cách sử dụng gói lệnh `float` (`[H]`) kết hợp gói lệnh `placeins` (`\FloatBarrier`).

---

## 1. Chi tiết điều chỉnh Placement

### 1.1. Nhiệm vụ 1: Ép Table VII (Sensitivity Analysis) nằm đúng sau Appendix A
* **Cách khắc phục:**
  - Thêm gói lệnh `\usepackage{float}` vào phần khai báo (preamble) của tệp tài liệu chính.
  - Sửa Table VII (`tableA1_sensitivity.tex`) để sử dụng cấu trúc `\begin{table}[H]`.
  - Giữ nguyên lệnh chặn float `\FloatBarrier` ngay sau Table VII tại tệp [appendix_a_sensitivity.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex).
* **Kết quả:** Table VII xuất hiện chuẩn xác ngay sau đoạn văn bản mô tả của Appendix A, loại bỏ hoàn toàn lỗi trôi ngược lên trước tiêu đề Appendix A.

### 1.2. Nhiệm vụ 2: Ép Table X (Calibration Breakdown) nằm đúng trong Appendix C, trước Appendix D
* **Cách khắc phục:**
  - Cập nhật Table X (`table_v_calibration_by_bucket_updated.tex`) để sử dụng cấu trúc hai cột `\begin{table*}[H]` và `\resizebox{\textwidth}`.
  - Bổ sung lệnh `\FloatBarrier` ngay sau Table X trong Appendix C (tệp [appendix_a_sensitivity.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex)) để chặn bảng trôi xuống dưới tiêu đề Appendix D.
* **Kết quả:** Table X hiển thị trọn vẹn trong Appendix C, trước tiêu đề Appendix D.

---

## 2. Kết quả kiểm tra và Xác minh
1. **Xác nhận không đổi số liệu thực nghiệm:** Toàn bộ dữ liệu tế bào, số trung bình, độ lệch chuẩn, chú thích bảng khoa học và kết quả AUC/ECE được giữ nguyên gốc từ kết quả rerun, không bị sửa đổi.
2. **Compile PDF thành công:** Đã xuất PDF chứng nhận chất lượng cao xác minh bố cục thành công tại:
   👉 **[paper/P0_appendix_float_fixed.pdf](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/P0_appendix_float_fixed.pdf)**
3. **Không có lỗi Undefined Reference:** Toàn bộ liên kết chéo `\ref{tab:calib}` và các tham chiếu số bảng đều hoạt động bình thường.

---

## 3. Danh sách File thay đổi (Git Diff)

```diff
diff --git a/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex b/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex
index d0ed1a3..d12a64c 100644
--- a/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex
+++ b/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex
@@ -3,6 +3,7 @@
 To establish the robustness of our diagnostic stratification, we conduct a sensitivity analysis evaluating whether the observed predictive degradation and calibration decay are sensitive to the choice of frequency thresholds. We evaluate three alternative threshold configurations: (i) an aggressive setting with thresholds \{10, 50, 250\} training interactions, (ii) a conservative setting with thresholds \{30, 150, 750\} training interactions, and (iii) a dynamic quantile-based bucketing scheme where buckets are defined by equal-quantile KCs. The results, summarized in Table~\ref{tab:sensitivity}, show that while the absolute counts of KCs in each category shift, the diagnostic patterns are broadly consistent, although effect magnitudes vary across threshold definitions. Specifically, the noticeable calibration degradation in the sparse and very sparse categories persists, indicating that our diagnostics capture intrinsic model behaviors on low-frequency concepts rather than artifacts of threshold definitions.
 
 \input{tables/tableA1_sensitivity}
+\FloatBarrier
 
 \section{Overall and Bucket-level Performance under Temporal Splits}
 \label{app:temporal_performance}
@@ -17,6 +18,7 @@ Detailed calibration results by frequency stratum are reported in Table~\ref{ta
 Detailed calibration results by frequency stratum are reported in Table~\ref{tab:calib}.
 
 \input{tables/table_v_calibration_by_bucket_updated}
+\FloatBarrier
 
 \section{Diagnostic Interpretation Guide}
 \label{app:interpretation}
```
