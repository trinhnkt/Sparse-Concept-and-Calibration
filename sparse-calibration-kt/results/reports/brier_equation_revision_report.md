# Brier Equation Revision Report

**Date:** 2026-06-13  
**Task:** Bổ sung định nghĩa UNC, REL, RES vào Section III.D theo góp ý của GS Hậu  
**File sửa:** `paper/sections/03_protocol.tex`  
**File copy main:** `paper/main_brier_equations_added.tex`

---

## 1. Vị trí các thay đổi

### 1.1. Equation UNC

**File:** `paper/sections/03_protocol.tex`  
**Vị trí:** Lines 44–46, ngay sau equation Brier decomposition (`\brier = \unc - \res + \rel`)

```latex
\begin{equation}
\unc = \bar{y}(1-\bar{y}).
\end{equation}
```

### 1.2. Equation REL

**File:** `paper/sections/03_protocol.tex`  
**Vị trí:** Lines 47–50, ngay sau equation UNC

```latex
\begin{equation}
\rel = \frac{1}{N}\sum_{m=1}^{M} n_m
\left(\mathrm{conf}_m - \mathrm{acc}_m\right)^2.
\end{equation}
```

### 1.3. Equation RES

**File:** `paper/sections/03_protocol.tex`  
**Vị trí:** Lines 51–54, ngay sau equation REL

```latex
\begin{equation}
\res = \frac{1}{N}\sum_{m=1}^{M} n_m
\left(\mathrm{acc}_m - \bar{y}\right)^2.
\end{equation}
```

---

## 2. Đoạn diễn giải ý nghĩa các thành phần

**Vị trí:** Line 55, ngay sau ba equation UNC/REL/RES

> "$\unc$ measures the intrinsic uncertainty of the prediction task and is independent of the model; $\rel$ measures the deviation between predicted probabilities and observed frequencies, where lower values indicate better reliability; $\res$ measures how well the model separates events with different outcome rates from the global mean, where higher values indicate better resolution."

---

## 3. Ký hiệu bổ sung (giới thiệu trước 3 equation, line 43)

Đoạn giới thiệu ký hiệu được thêm sau equation decomposition:

> "where the three components are defined as follows. Let $\bar{y}$ denote the global correctness rate, $M=15$ the number of calibration bins, $n_m$ the number of samples in bin $m$, $\mathrm{acc}_m$ the empirical accuracy in bin $m$, $\mathrm{conf}_m$ the average predicted confidence in bin $m$, and $N$ the total number of samples."

---

## 4. Logic sau chỉnh sửa của Section III.D

Sau khi chỉnh sửa, Section III.D có cấu trúc logic hoàn chỉnh:

| Bước | Nội dung |
|------|----------|
| 1 | Định nghĩa ECE (M=15 bins) |
| 2 | Định nghĩa Brier score |
| 3 | Định nghĩa Brier decomposition: `Brier = UNC − RES + REL` |
| 4 | Giới thiệu ký hiệu: $\bar{y}$, $M$, $n_m$, $\mathrm{acc}_m$, $\mathrm{conf}_m$, $N$ |
| 5 | Equation UNC = $\bar{y}(1-\bar{y})$ |
| 6 | Equation REL = $\frac{1}{N}\sum n_m(\mathrm{conf}_m - \mathrm{acc}_m)^2$ |
| 7 | Equation RES = $\frac{1}{N}\sum n_m(\mathrm{acc}_m - \bar{y})^2$ |
| 8 | Diễn giải ý nghĩa UNC, REL, RES |

---

## 5. Xác nhận không thay đổi ngoài phạm vi

| Hạng mục | Trạng thái |
|----------|------------|
| Bảng (Tables) | ✅ Không thay đổi |
| Hình (Figures) | ✅ Không thay đổi |
| Số liệu thực nghiệm | ✅ Không thay đổi |
| Kết quả | ✅ Không thay đổi |
| Các Section khác | ✅ Không thay đổi |
| Numbering equations | ✅ Dùng `\begin{equation}` tự động, không hard-code |
| Claim mới | ✅ Không thêm claim mới |

---

## 6. Về compile PDF

Máy local không có LaTeX (pdflatex) được cài đặt. Để tạo `P0_brier_equations_added.pdf`, cần thực hiện một trong các cách sau:

- **Overleaf:** Upload/sync `paper/` folder lên Overleaf, compile với `main_brier_equations_added.tex` (hoặc `main.tex` vì sections đã được cập nhật).
- **Cài MiKTeX/TeX Live:** Sau khi cài, chạy: `pdflatex -interaction=nonstopmode main_brier_equations_added.tex` từ thư mục `paper/`.

Các macro cần thiết (`\unc`, `\rel`, `\res`, `\brier`, `\ece`) đã được định nghĩa sẵn trong `main.tex` (lines 40–44), nên compile sẽ thành công mà không cần thay đổi gì thêm.

---

*Report được tạo tự động bởi Antigravity — 2026-06-13*
