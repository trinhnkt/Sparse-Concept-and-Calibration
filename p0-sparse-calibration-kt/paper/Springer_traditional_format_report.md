# Springer Nature Traditional Publishing Format Report

## Danh sách file đã chỉnh sửa
1. paper/main_springer_traditional.tex (Tạo mới từ main_jedm.tex)
2. paper/main_springer_traditional_anonymous.tex (Tạo mới bản giấu tên)
3. paper/sections/04_experiments.tex (Sửa môi trường igure* thành igure)
4. Các file trong paper/tables/*.tex (Sửa môi trường 	able* thành 	able)

## Template Springer Nature đã sử dụng
- Sử dụng document class chính thức của Springer Nature: \documentclass[sn-mathphys]{sn-jnl}.
- Định dạng kiểu 1 cột chuẩn theo hướng dẫn của Springer Nature (mặc định của sn-jnl).
- Đã cấu hình thêm các package cần thiết như 	abularx, djustbox để hỗ trợ bảng biểu.

## Những lỗi LaTeX đã sửa
- Chuyển đổi toàn bộ môi trường \begin{figure*} và \begin{table*} thành \begin{figure} và \begin{table} để tương thích với template 1 cột của Springer Nature, tránh cảnh báo/lỗi định dạng tràn lề.
- Đảm bảo cấu trúc Declarations đúng chuẩn Springer Nature với các mục (Funding, Competing interests, Ethics approval, Consent, Data availability, Code availability, Authors' contributions, Use of generative AI tools).
- Các bảng biểu đều có Caption ở trên, sử dụng \resizebox để ngăn tràn lề (giữ nguyên cấu trúc ooktabs cũ).

## Những cảnh báo còn lại
- Môi trường compile cục bộ trên máy không có sẵn pdflatex trong PATH, do đó chưa thể biên dịch trực tiếp ra PDF trên máy này. Tác giả có thể biên dịch file main_springer_traditional.tex trên hệ thống Overleaf hoặc TeX Studio.
- Các bảng sử dụng \resizebox{\columnwidth} có thể sẽ được co giãn tùy thuộc vào lề của file template Springer, tác giả cần kiểm tra lại độ dễ nhìn của font chữ trong bảng sau khi biên dịch.

## Những điểm tác giả cần kiểm tra thủ công
1. **Authors' contributions:** Trong file main_springer_traditional.tex hiện đang để placeholder \todo{Authors to explicitly define individual contributions.}. Tác giả cần bổ sung nội dung cụ thể (ai viết code, ai làm thực nghiệm, ai viết bản thảo).
2. **ORCID:** Các ORCID của nhóm tác giả đã được giữ nguyên và tích hợp, vui lòng kiểm tra lại sự hiển thị trên file PDF cuối cùng.
3. **References:** Template đang sử dụng \bibliography{references} (chế độ mặc định của Springer cho math/phys). Nếu Applied Intelligence yêu cầu một style trích dẫn cụ thể (như tên-năm thay vì số), tác giả có thể đổi option trong \documentclass (ví dụ sn-basic).
4. **Bảng và Hình:** Đảm bảo khi biên dịch không bị mờ và không bị đẩy xuống cuối quá xa do float.

## LƯU Ý QUAN TRỌNG KHI NỘP BÀI (SUBMISSION)
**Khi nộp bài trên hệ thống Editorial Manager của Springer (cho tạp chí Applied Intelligence), tác giả BẮT BUỘC PHẢI CHỌN "Traditional publishing" hoặc "Subscription publishing" nếu không muốn trả phí APC (Article Processing Charge) cho Open Access.** 
Bài báo hiện tại đã được cấu hình loại bỏ tất cả các tuyên bố liên quan đến Open Access và giấy phép CC-BY.
