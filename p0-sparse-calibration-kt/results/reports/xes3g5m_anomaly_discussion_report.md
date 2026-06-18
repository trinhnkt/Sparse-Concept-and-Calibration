# XES3G5M Anomaly Discussion Report

**Date:** 2026-06-13  
**Status:** ✅ Completed

---

## 1. Vị trí thêm đoạn thảo luận
Đoạn thảo luận về pattern bất thường của XES3G5M đã được thêm vào cuối **Section IV.C** (RQ1: Strata Performance Analysis), ngay sau khi Bảng IV được phân tích và ngay trước khi bắt đầu **Section IV.D** (RQ2: Calibration and Reliability Profiles) trong file `paper/sections/04_experiments.tex`.

## 2. Nguồn số liệu AUC sử dụng
Các số liệu AUC được sử dụng trong đoạn thảo luận được lấy chính xác từ file `paper/tables/table4_metric_per_bucket.tex` (Bảng IV hiện tại của bài P0):
*   DKT sparse: $0.8572 \approx 0.857$
*   SimpleKT sparse: $0.8495 \approx 0.850$
*   DKT very sparse: $0.8742 \approx 0.874$
*   SimpleKT very sparse: $0.8492 \approx 0.849$
*   DKT dense: $0.8185 \approx 0.819$
*   SimpleKT dense: $0.7551 \approx 0.755$

Số liệu trong đoạn văn bản hoàn toàn khớp với bảng thực tế của dự án.

## 3. Xác nhận không thay đổi bảng/hình/số liệu
*   ✅ Hoàn toàn **không** thay đổi bất kỳ số liệu thực nghiệm nào.
*   ✅ Hoàn toàn **không** sửa đổi Bảng IV, Hình, Caption hay kết quả của paper. 
*   ✅ Không có reference mới nào được thêm (vì không yêu cầu và không cần thiết).

## 4. Xác nhận văn phong (Hedging language)
Đoạn văn mới được viết theo đúng yêu cầu về phong cách học thuật thận trọng:
*   Đưa ra các cách giải thích dưới dạng "khả năng" (*"Several non-exclusive explanations are plausible"*).
*   Sử dụng từ ngữ giảm nhẹ như *"may mean"*, *"partially decoupling"*.
*   Thừa nhận giới hạn của bài báo bằng câu *"beyond the scope of this protocol paper"*.
*   Nhấn mạnh kết luận cốt lõi mà không đưa ra claim mới quá mạnh: hiện tượng này *"reinforces our point that bucket-level diagnostics reveal phenomena that overall AUC alone cannot."*

---
*Lưu ý: Môi trường hiện tại không có sẵn `pdflatex` hay `latexmk` trong đường dẫn (PATH), do đó hệ thống không thể tự động build file PDF `P0_xes3g5m_anomaly_discussion_added.pdf` ngay tại đây. Tuy nhiên, file `.tex` đã được cập nhật thành công và sẵn sàng để compile.*
