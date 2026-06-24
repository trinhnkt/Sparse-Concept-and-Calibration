# Báo cáo chuyển đổi định dạng JEDM (Journal of Educational Data Mining)

## Những file đã chỉnh sửa
- **`main_jedm.tex`**: File chính được tạo mới với cấu hình `article`, margin, font chữ và title/author block chuẩn hóa theo JEDM.
- **`main_jedm_anonymous.tex`**: Phiên bản ẩn danh (ẩn tên tác giả, thông tin liên lạc, ORCID, tên viện, repo GitHub).
- **`tables/table1_dataset_stats.tex`**: Đổi từ `table*` thành `table` và thêm `\resizebox{\linewidth}{!}{}` để tránh tràn lề ở chế độ một cột.
- **`tables/table1_leakage_audit.tex`**: Đổi từ `table*` thành `table` và thêm `\resizebox{\linewidth}{!}{}` để tránh tràn lề.
- Đã sao lưu bản gốc vào `backup_before_jedm_format/`.

## Những yêu cầu JEDM đã đáp ứng
- Khổ giấy A4, lề trái/phải 2.75 cm, trên/dưới 2.25 cm.
- Chế độ 1 cột.
- Font nội dung chính là Times Roman (`mathptmx`).
- Font tiêu đề và tác giả là Helvetica (sans-serif) (`helvet`, `titlesec`).
- Table caption nằm phía TRÊN bảng (`\captionsetup[table]{position=top}`).
- Figure caption nằm phía DƯỚI hình (`\captionsetup[figure]{position=bottom}`).
- Cấu trúc thứ tự (Abstract -> Keywords -> Sections -> Appendix -> Acknowledgements -> References).
- Tài liệu tham khảo theo chuẩn `acm`.

## Những lỗi LaTeX đã sửa
- Sửa lỗi tràn bảng ở các bảng 2 cột (`table*`) khi chuyển sang 1 cột bằng cách bọc nội dung trong `\resizebox` theo tỉ lệ chiều ngang của trang giấy (`\linewidth`).

## Cảnh báo còn lại
- Môi trường hiện tại không có sẵn `pdflatex` / `bibtex` trong hệ thống (PATH), do đó bước biên dịch tạo file PDF tự động chưa thể thực hiện. Tuy nhiên, mã nguồn `.tex` đã được chuẩn hóa để sẵn sàng biên dịch thủ công (bằng cách mở trên Overleaf, TeXstudio, v.v.).

## Những điểm cần tác giả kiểm tra thủ công
- Mở `main_jedm.tex` bằng Overleaf hoặc một trình biên dịch LaTeX cục bộ và chạy thử nghiệm.
- Kiểm tra lại kích thước và sự rõ ràng của các bảng số liệu, do việc ép vào một cột có thể làm kích thước chữ nhỏ lại nếu dùng `\resizebox`. Trong một số trường hợp, nếu quá nhỏ, tác giả có thể cần phải thay `\resizebox` bằng cấu trúc ngắt dòng (word-wrap) trong `tabularx` hoặc chuyển bảng thành chế độ nằm ngang (`pdflscape`).
- Đọc lướt qua một lượt các công thức toán xem có công thức nào vô tình bị dài quá không (mặc dù cấu hình căn lề có thể bao bọc, nhưng có thể cần thủ công dùng `split`).
- Nếu muốn Submit lên Overleaf, dùng các file `main_jedm.tex` làm file gốc (Main document).
