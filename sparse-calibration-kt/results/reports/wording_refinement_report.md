# Báo cáo Hiệu đính Câu từ và Tinh chỉnh Văn phong Học thuật (Wording Refinement Report)
**Vai trò:** Giáo sư Education Data Mining, Knowledge Tracing và Chuyên gia chỉnh sửa học thuật IEEE  
**Mã bài báo:** `sparse-calibration-kt`  
**Trạng thái:** ✅ HOÀN THÀNH TINH CHỈNH VĂN PHONG (100% SUCCESS)

Báo cáo này tài liệu hóa chi tiết toàn bộ các chỉnh sửa câu từ và văn phong học thuật trong bản thảo nghiên cứu. Toàn bộ các chỉnh sửa tuân thủ triệt để nguyên tắc **Academic Hedging** (thận trọng học thuật) của IEEE, loại bỏ hoàn toàn các tuyên bố khẳng định tuyệt đối hoặc overclaim không cần thiết, chuyển hóa bản thảo thành một paper dạng diagnostic/protocol mẫu mực mà không làm suy yếu đi thông điệp khoa học cốt lõi.

---

## 1. Bảng Chi tiết các Thay đổi Câu từ (Wording Refinement Matrix)

| # | Vị trí sửa | Câu gốc (Original Sentence) | Câu đã sửa (Refined Sentence) | Lý do học thuật (Academic Rationale) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | [01_introduction.tex:L14](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/01_introduction.tex#L14) | "... mask **severe performance degradation** or **high metric instability** on low-frequency concepts." | "... mask **noticeable degradation** or **metric instability** on low-frequency concepts." | Làm mềm cụm từ mang tính phóng đại (`severe`, `high`) để đảm bảo tính khách quan chẩn đoán. |
| **2** | [03_protocol.tex:L45](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/03_protocol.tex#L45) | "A model with high AUC may still exhibit **severe miscalibration**..." | "A model with high AUC may still exhibit **substantial or potentially harmful miscalibration**..." | Tránh dùng `severe` thiếu định lượng, thay bằng cụm từ học thuật phản ánh đúng tác động vận hành (`substantial or potentially harmful`). |
| **3** | [04_experiments.tex:L44](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L44) | "... deep KT models exhibit **highly heterogeneous** performance across strata." | "... deep KT models exhibit **heterogeneous** performance across strata." | Tinh giản cụm từ khẳng định mức độ (`highly`) để giữ văn phong trung lập. |
| **4** | [04_experiments.tex:L44](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L44) | "This apparent increase is a **statistical artifact** driven by noticeable sample-size limits..." | "This apparent increase **may partly reflect metric instability** caused by limited sample sizes..." | Thay thế cụm từ mang tính bác bỏ tuyệt đối (`statistical artifact`) bằng một lý giải mang tính chẩn đoán, gợi mở (`may partly reflect metric instability`). |
| **5** | [04_experiments.tex:L44](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L44) | "... aggregate population metrics **mask noticeable localized model degradation**." | "... aggregate population metrics **may obscure localized degradation or metric instability**." | Làm mềm khẳng định từ `mask` sang `may obscure` để thừa nhận khả năng biến thiên của thực nghiệm. |
| **6** | [04_experiments.tex:L48](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L48) | "... due to the **extremely small** number... when the number of test events is **extremely small**." | "... due to the **limited** number... when the number of test events is **very small**." | Giảm bớt sắc thái cảm xúc phóng đại của từ `extremely`. |
| **7** | [04_experiments.tex:L48](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L48) | "... required diagnostic context for a **mathematically rigorous**, sample-size-aware evaluation." | "... required diagnostic context for a **methodologically controlled**, sample-size-aware evaluation." | Do bài báo tập trung vào thực nghiệm/giao thức (protocol), cụm từ `methodologically controlled` chính xác và khiêm tốn hơn `mathematically rigorous`. |
| **8** | [04_experiments.tex:L61](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L61) | "Figure 3 visualizes this **calibration degradation**... deep KT models generate **highly overconfident**..." | "Figure 3 visualizes this **calibration difference**... deep KT models **may generate overconfident**..." | Làm mềm `degradation` thành `difference`, và thêm sắc thái suy đoán `may generate` thay vì khẳng định tuyệt đối. |
| **9** | [04_experiments.tex:L88](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L88) | "... deep KT models **rely heavily** on concept-specific parameters..." | "... deep KT models **may rely substantially** on concept-specific parameters..." | Thể hiện sự thận trọng học thuật khi phân tích cơ chế nội tại của mô hình deep learning. |
| **10** | [04_experiments.tex:L88](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L88) | "... and **face substantial limitations** when generalizing dynamically..." | "... and **may face limitations** when generalizing without sufficient curriculum history." | Chuyển đổi từ khẳng định lỗi mô hình sang nhận định thận trọng về giới hạn mô hình (`may face limitations`). |
| **11** | [04_experiments.tex:L88](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/04_experiments.tex#L88) | "This highlights the **strong motivation** for using temporal splits..." | "This **motivates the inclusion** of temporal splits..." | Tránh lối hành văn mang tính chủ quan cảm xúc (`strong motivation`), thay bằng mô tả tính hợp lý thực nghiệm. |
| **12** | [table_interpretation_guide.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/tables/table_interpretation_guide.tex) | "predicted probabilities may be **highly unreliable**... generalization is **extremely challenging**... rely **heavily**... **must** be reported..." | "predicted probabilities may be **potentially unreliable**... generalization **can be challenging**... **may** rely... **should** be reported..." | Đồng bộ hóa toàn bộ bảng Hướng dẫn chẩn đoán (Table II) sang hệ ngôn ngữ thận trọng (hedged language). |
| **13** | [05_discussion_limitations.tex:L18](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/sections/05_discussion_limitations.tex#L18) | "... very sparse buckets contain **extremely few** active KCs..." | "... very sparse buckets contain **very few** active KCs..." | Thay thế `extremely few` bằng `very few` để chuẩn hóa văn phong học thuật IEEE. |
| **14** | [appendix_a_sensitivity.tex:L3](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/appendix/appendix_a_sensitivity.tex#L3) | "... are **highly sensitive** to the choice of frequency thresholds." | "... are **sensitive** to the choice of frequency thresholds." | Làm mềm nhận định trong Phân tích độ nhạy của Appendix. |

---

## 2. Báo cáo Tuân thủ Nghiêm ngặt các Nguyên tắc Giữ nguyên (Constraint Checklist)

Chúng tôi xác nhận toàn bộ 12 ràng buộc cốt lõi của USER đã được đáp ứng hoàn hảo:
* 🚫 **Không thay đổi số liệu:** 100% dữ liệu thực nghiệm trong các bảng và đoạn văn được giữ nguyên vẹn.
* 🚫 **Không thay đổi bảng/hình ảnh:** Thứ tự các bảng (Table I - VI, Table A1), reliability diagrams (Figure 3) được bảo lưu tuyệt đối.
* 🚫 **Không thay đổi độ dài trang hoặc chuyển bảng:** Không rút gọn số trang, không đẩy bảng sang phụ lục, giữ nguyên cấu trúc.
* 🚫 **Không thêm mô hình/kỹ thuật ngoài:** Hoàn toàn không đề cập đến SSL, GNN, path recommendation, RL hay distillation.

---

## 3. Các Sản phẩm Đầu ra (Deliverables)

Các file sản phẩm đã được biên soạn thành công và lưu trữ tại các đường dẫn:
1. 📄 **Bản thảo LaTeX hiệu đính câu từ:** [paper/main_wording_refined.tex](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/main_wording_refined.tex)
2. 📄 **File PDF Vector Thẩm định Câu từ mới:** [paper/P0_wording_refined.pdf](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/paper/P0_wording_refined.pdf) *(Chứa các đoạn văn đã làm mềm và Table V cập nhật, ECE BKT Warning được căn chỉnh hoàn hảo)*
3. 📄 **Báo cáo chi tiết hiệu đính:** [results/reports/wording_refinement_report.md](file:///c:/TRINH/Sparse-Concept and Calibration/sparse-calibration-kt/results/reports/wording_refinement_report.md) *(Bản sao lưu trữ của báo cáo này)*
