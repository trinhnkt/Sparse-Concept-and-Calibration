# Báo cáo Chỉnh sửa Bố cục và Tính Nhất quán (P0 - T17 - Final Layout Consistency)

**Ngày thực hiện:** 2026-06-18  
**Trạng thái:** ✅ ĐÃ HOÀN THÀNH (100% PASS)  

Báo cáo này tóm tắt kết quả giải quyết các lỗi trình bày và tính nhất quán trên bản thảo LaTeX và các bảng biểu đi kèm của bài báo P0(17) trước khi gửi GS Hậu xem xét lại.

---

## 1. Kết quả thực hiện 6 nhiệm vụ chi tiết

### 1.1. Nhiệm vụ 1: Xử lý hiển thị Table VI (Table V trong code LaTeX)
*   **Nguyên nhân lỗi:** Tabular format specification của bảng calibration được khai báo là `lllrccccc` (9 cột) trong khi tiêu đề và hàng dữ liệu thực tế chứa tới 10 cột (Dataset, Model, Bucket, Rel, #Events, ECE, Brier, UNC, REL, RES). Mâu thuẫn này dẫn đến việc cột cuối cùng `RES` bị cắt bỏ hoặc lỗi căn chỉnh trong tài liệu PDF.
*   **Phương án xử lý:** Khôi phục hiển thị đầy đủ ngay trong main text bằng cách điều chỉnh định dạng tabular trong script sinh bảng thành `lllrcccccc` (10 cột) để hiển thị đầy đủ.
*   **Các file cập nhật:**
    - [make_updated_latex_tables.py](file:///c:/TRINH/P0/p0-sparse-calibration-kt/scripts/make_updated_latex_tables.py) (Dòng 496).
    - Đã chạy lại script để tái tạo hoàn chỉnh các tệp:
      - [table_v_calibration_by_bucket_updated.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/tables/table_v_calibration_by_bucket_updated.tex)
      - [table_v_calibration_with_reliability.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/tables/table_v_calibration_with_reliability.tex)
      - [table5_calibration_per_bucket.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/tables/table5_calibration_per_bucket.tex)
      - [tableA_calibration_by_bucket_full.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/tables/tableA_calibration_by_bucket_full.tex)
    - Đồng thời, sửa lỗi tương tự của Table IV và Table IX (từ `lllcrcccc` thành `lllcrccccc`) giúp hiển thị đầy đủ 10 cột.

### 1.2. Nhiệm vụ 2: Sửa cross-reference Appendix A thành Appendix B cho temporal split
*   **File chỉnh sửa:** [04_experiments.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 14).
*   **Nội dung thay đổi:** Đổi tham chiếu từ `Appendix~\ref{app:sensitivity}` (Appendix A) sang `Appendix~\ref{app:temporal_performance}` (Appendix B - Nơi lưu trữ thực tế của temporal split).
*   **Văn bản mới:**
    > *"Temporal splits are used as a complementary stress-test for future-oriented and limited cold-start diagnostics, reported in Table~\ref{tab:cold_start} and Appendix~\ref{app:temporal_performance}."*

### 1.3. Nhiệm vụ 3: Sửa định dạng số “N = 2, 545” thành “N = 2,545”
*   **File chỉnh sửa:** [04_experiments.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 67 và 84).
*   **Nội dung thay đổi:** Đóng gói dấu phẩy trong dấu ngoặc nhọn `{}` dạng `$N = 2{,}545$` trong chế độ toán học để ngăn cản LaTeX tự động chèn khoảng trắng sau dấu phẩy.
*   **Kết quả:** Sau khi biên dịch, số lượng sự kiện hiển thị chuẩn xác là **N = 2,545**.

### 1.4. Nhiệm vụ 4: Làm mềm câu diễn giải calibration trong RQ2
*   **File chỉnh sửa:** [04_experiments.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 61).
*   **Văn bản mới (Hedging):**
    > *"Our results suggest that, on datasets where sparse learner-based strata are present, calibration errors tend to increase as concept frequency decreases under our experimental conditions:"*
*   **Ý nghĩa:** Tránh việc khẳng định như một quy luật tuyệt đối đối với tất cả các tập dữ liệu (vì Junyi không có sparse strata, còn XES3G5M có counter-pattern).

### 1.5. Nhiệm vụ 5: Thêm câu giải thích việc chuyển BKT sang IRT trong Section IV.B
*   **File chỉnh sửa:** [04_experiments.tex](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/sections/04_experiments.tex) (Dòng 30).
*   **Nội dung thay đổi:** Thêm câu dẫn giải thích ngắn gọn và lịch sự khoa học, chỉ sang Appendix D để xem chi tiết:
    > *"We initially evaluated BKT but replaced it with IRT after observing numerical instability in EM-based \texttt{pyBKT} estimation; details are provided in Appendix~\ref{app:bkt_instability}."*

### 1.6. Nhiệm vụ 6: Cân nhắc vị trí Table VII (Table VIII trong file TeX thực tế)
*   **Quyết định:** Giữ Table VII (Threshold Sensitivity) trong main text.
*   **Lý do:** Bảng này có chiều ngang gọn trong 1 cột (`\resizebox{\columnwidth}`) và chỉ dài 33 dòng, không ảnh hưởng đến độ dài hay luồng đọc của Section IV.E. Bố cục trang hiện tại hoàn toàn cân đối.

---

## 2. Xác nhận Tính Toàn vẹn và Thẩm định PDF

1.  **Không thay đổi kết quả thực nghiệm:** Không có bất kỳ số liệu thực nghiệm nào từ rerun T13 bị thay đổi.
2.  **Compile PDF thành công:** Đã xuất bản vẽ PDF candidate kiểm tra chất lượng cao định dạng vector tại:
    👉 **[paper/P0_17_final_layout_consistency_fixed.pdf](file:///c:/TRINH/P0/p0-sparse-calibration-kt/paper/P0_17_final_layout_consistency_fixed.pdf)**
3.  **Không có lỗi layout hay cross-reference:** Tất cả các bảng biểu hiển thị đầy đủ, không bị cut-off thông tin.

---

## 3. Danh sách File thay đổi (Git Diff Summary)

```text
Staged changes:
  - modified: paper/main.tex (author block columns)
  - modified: paper/main_submit_candidate.tex (author block columns)
  - modified: paper/sections/04_experiments.tex (cross-ref, softened RQ2 text, BKT->IRT sentence, N={,} formatting)
  - modified: paper/tables/table_iv_bucket_performance_updated.tex (10-column spec)
  - modified: paper/tables/table_v_calibration_by_bucket_updated.tex (10-column spec)
  - modified: paper/tables/table_ix_updated.tex (10-column spec)
  - modified: scripts/make_updated_latex_tables.py (tabular spec fix)
  - modified: src/generate_pdf_presubmission_check.py (output candidate path, Rel. column added)
  - new file: paper/P0_17_final_layout_consistency_fixed.pdf
  - new file: results/reports/p0_17_final_layout_consistency_report.md
```
