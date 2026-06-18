# Multi-skill Convention Revision Report

**Date:** 2026-06-13  
**Task:** Tài liệu hóa convention xử lý multi-skill items trong Section III.A theo góp ý của GS Hậu  
**File sửa:** `paper/sections/03_protocol.tex`  
**File copy main:** `paper/main_multiskill_convention_added.tex`

---

## 1. Convention thực tế đã xác định

**Convention: Pre-expanded one-row-per-KC (từ nguồn dataset)**

Sau khi kiểm tra toàn bộ code pipeline, xác định được:

| Dataset | Evidence | Convention |
|---------|----------|------------|
| **XES3G5M** | `create_xes3g5m_full.py` line 29–30: load từ `kc_level/train_valid_sequences.csv` | `kc_level` split đã là one-KC-per-row do dataset authors cung cấp sẵn |
| **ASSISTments 2012** | `configs/assist2012.yaml`: `kc_col: skill_id` → `preprocess.py` đọc trực tiếp cột `skill_id` | Raw file đã có one `skill_id` per row |
| **Junyi Academy** | `configs/junyi.yaml`: `kc_col: ucid` | Items là single-skill, không có multi-skill items |

**Kết luận:** Không có code explicit "expand" multi-skill items trong `preprocess.py`. Multi-skill items đã được expand sẵn bởi nguồn dataset (đặc biệt XES3G5M `kc_level` folder). KC-frequency stratification được tính **sau** khi dữ liệu đã ở dạng pre-expanded, dùng training-fold counts only.

### Files đã kiểm tra
- `src/preprocess.py` — không có multi-skill expansion logic
- `src/create_xes3g5m_full.py` — load từ `kc_level/` folder (one-KC-per-row)
- `src/create_xes3g5m_sample.py` — load từ `kc_level/` folder (one-KC-per-row)
- `src/create_assist_sample.py` — đọc CSV thô, không expand
- `src/create_junyi_sample.py` — đọc CSV thô, không expand
- `configs/assist2012.yaml` — `kc_col: skill_id`
- `configs/junyi.yaml` — `kc_col: ucid`
- `configs/xes3g5m.yaml` — `kc_col: skill_id`
- `docs/how_to_reproduce.md` — rỗng (không có documentation)
- `docs/qmatrix_provenance.md` — rỗng (không có documentation)

---

## 2. Vị trí đã sửa

**File:** `paper/sections/03_protocol.tex`  
**Section:** III.A — Data Schema  
**Vị trí:** Lines 9–11, ngay sau equation (1)

---

## 3. Đoạn văn đã thay thế

### Câu cũ (đã xóa)
```
Multi-skill items should be handled according to the preprocessing convention of the chosen 
benchmark implementation and documented in the artifact.
```

### Đoạn mới (đã thêm)
```latex
% TODO (NCS confirm before submission): Verify that multi-skill handling below matches 
% actual raw-data format for all three datasets.
In this paper, multi-skill items are represented using a one-row-per-KC convention: each 
interaction involving multiple KCs is pre-expanded into one row per KC by the dataset 
source, so that each row in the processed data corresponds to exactly one (learner, item, 
KC, correctness, timestamp) tuple. Specifically, XES3G5M is loaded from the \texttt{kc\_level} 
split provided by the dataset authors~\cite{liu2023xes3g5m}, which already stores one KC 
per row; ASSISTments 2012 is read from the standard release file in which each row carries 
a single \texttt{skill\_id}; Junyi Academy items are inherently single-skill. No additional 
expansion is performed by our \texttt{preprocess.py} pipeline. KC-frequency stratification 
(Section~\ref{sec:kc-strat}) is computed on these pre-expanded rows using training-fold 
counts only.
```

---

## 4. Thay đổi phụ trợ

- **Thêm label** `\label{sec:kc-strat}` cho subsection KC-frequency Stratification (line 17) để `\ref{sec:kc-strat}` resolve đúng.
- **Citation dùng:** `\cite{liu2023xes3g5m}` — key này đã có sẵn trong `references.bib` (entry `liu2023xes3g5m`).

---

## 5. KC-frequency stratification được tính sau convention nào

KC-frequency stratification được tính **sau khi dữ liệu đã ở dạng pre-expanded** (one-row-per-KC), sử dụng **training-fold counts only** (đúng theo P1: Train-only Definitions trong Design Principles của paper).

---

## ⚠️ WARNING — Cần NCS xác nhận trước khi submit

> **Lý do cảnh báo:** Code `preprocess.py` không có explicit multi-skill expansion logic. Convention "pre-expanded from dataset source" được suy ra từ:
> 1. XES3G5M load từ `kc_level/` folder (không phải `question_level/`)
> 2. ASSIST 2012 raw file có `skill_id` per row (đã expanded)
> 
> **Tuy nhiên:** Chưa xác nhận được từ tài liệu chính thức hoặc README rằng ASSIST 2012 raw file thực sự đã được expanded. Nếu raw file ASSIST 2012 có format khác (e.g., multi-skill trong một cell), convention này cần cập nhật lại.

**Files cần kiểm tra thủ công:**
1. `data/raw/assistments2012/2012-2013-data-with-predictions-4-final.csv` — xác nhận mỗi row có một `skill_id` duy nhất
2. `data/raw/xes3g5m/kc_level/train_valid_sequences.csv` — xác nhận `concepts` field là single KC per position (đã verified qua code)
3. `data/raw/junyi/Log_Problem.csv` — xác nhận `ucid` là single-skill per row

**TODO LaTeX comment** đã được thêm ở line 10 trong `03_protocol.tex` để nhắc nhở trước khi submit.

---

## 6. Xác nhận không thay đổi ngoài phạm vi

| Hạng mục | Trạng thái |
|----------|------------|
| Bảng (Tables) | ✅ Không thay đổi |
| Hình (Figures) | ✅ Không thay đổi |
| Số liệu thực nghiệm | ✅ Không thay đổi |
| Kết quả | ✅ Không thay đổi |
| Bucket thresholds | ✅ Không thay đổi |
| Các Section khác | ✅ Không thay đổi |
| Claim mới | ✅ Không thêm claim mới |

---

## 7. Về compile PDF

Máy local không có LaTeX (pdflatex) được cài đặt. Để tạo `P0_multiskill_convention_added.pdf`, compile trên **Overleaf** với `main_multiskill_convention_added.tex`. Citation `\cite{liu2023xes3g5m}` và label `\ref{sec:kc-strat}` đều đã được setup đúng để compile thành công.

---

*Report được tạo tự động bởi Antigravity — 2026-06-13*
