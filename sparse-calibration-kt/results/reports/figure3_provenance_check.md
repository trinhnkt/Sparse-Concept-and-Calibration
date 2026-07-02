# Figure 3 Provenance Check

- **Script Tạo Hình:** `scripts/make_updated_figures.py`
- **Prediction CSV:** `results/predictions/junyi_temporal_simplekt_seed42.csv`
- **Label-alignment correction:** CÓ. Dữ liệu prediction CSV được sinh ra từ pipeline T9 rerun, sau khi temporal split đã được fix label-alignment.
- **Tạo sau T9 re-run:** CÓ. Figure đã được regenerate hoàn toàn tự động từ luồng prediction mới nhất.
- **ECE/N khớp không:** CÓ. Output script trả về `Dense ECE = 0.2267, N = 3,072,767` và `Very Sparse ECE = 0.3084, N = 2,545` khớp tuyệt đối với số hiện hữu trong PDF.

Do Figure 3 được tái tạo trực tiếp từ prediction post-T9 và cho kết quả giống hệt, chúng ta có thể khẳng định Provenance = CONFIRMED POST-T9.
