# Báo cáo Khắc phục Bố cục và Placement của Bảng trong Appendix (P0) - Chỉ sửa Table VII

**Ngày thực hiện:** 2026-06-18  
**Trạng thái:** ✅ ĐÃ HOÀN THÀNH & XÁC MINH THÀNH CÔNG

Báo cáo này mô tả chi tiết các chỉnh sửa cấu trúc LaTeX để xử lý lỗi placement của Table VII trong phần Phụ lục (Appendix A), đồng thời xác nhận giữ nguyên cấu trúc mặc định của Table X theo yêu cầu.

---

## 1. Chi tiết điều chỉnh Placement

### 1.1. Nhiệm vụ 1: Ép Table VII (Sensitivity Analysis) nằm đúng sau Appendix A
* **Cách khắc phục:**
  - Định vị đoạn lệnh chèn bảng `\input{tables/tableA1_sensitivity}` ngay bên dưới đoạn văn bản mô tả của Appendix A.
  - Sử dụng lệnh chặn float `\FloatBarrier` từ gói lệnh `placeins` ngay phía sau Table VII. Việc này ép LaTeX phải xả toàn bộ float của bảng Table VII trước khi bước sang tiêu đề Appendix B (`\section{Overall and Bucket-level Performance under Temporal Splits}`).
* **Kết quả:** Table VII xuất hiện chuẩn xác bên dưới tiêu đề Appendix A và đoạn mô tả tương ứng, loại bỏ lỗi trôi ngược lên trước tiêu đề.

### 1.2. Nhiệm vụ 2: Giữ nguyên cấu trúc Table X
* **Trạng thái:** Không can thiệp vào floating hay placement của Table X (chi tiết calibration) nữa. Table X được trả về chế độ floating mặc định ban đầu của tài liệu, không sử dụng `\FloatBarrier` hay `\clearpage` trong Appendix C.

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
index d0ed1a3..1f4f5f8 100644
--- a/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex
+++ b/p0-sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex
@@ -3,6 +3,7 @@
 To establish the robustness of our diagnostic stratification, we conduct a sensitivity analysis evaluating whether the observed predictive degradation and calibration decay are sensitive to the choice of frequency thresholds. We evaluate three alternative threshold configurations: (i) an aggressive setting with thresholds \{10, 50, 250\} training interactions, (ii) a conservative setting with thresholds \{30, 150, 750\} training interactions, and (iii) a dynamic quantile-based bucketing scheme where buckets are defined by equal-quantile KCs. The results, summarized in Table~\ref{tab:sensitivity}, show that while the absolute counts of KCs in each category shift, the diagnostic patterns are broadly consistent, although effect magnitudes vary across threshold definitions. Specifically, the noticeable calibration degradation in the sparse and very sparse categories persists, indicating that our diagnostics capture intrinsic model behaviors on low-frequency concepts rather than artifacts of threshold definitions.
 
 \input{tables/tableA1_sensitivity}
+\FloatBarrier
 
 \section{Overall and Bucket-level Performance under Temporal Splits}
 \label{app:temporal_performance}
```
