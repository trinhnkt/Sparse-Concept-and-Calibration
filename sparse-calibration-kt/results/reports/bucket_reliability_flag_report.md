# Bucket Reliability Flag Report

**Date:** 2026-06-13  
**Status:** ✅ Completed

---

## 1. Reliability Flag Definition
The Reliability flag was added to all bucket-level tables based on the number of events (N) according to the strict pre-registered rule:
- **Reliable (R):** $N \ge 1000$
- **Limited (L):** $100 \le N < 1000$
- **Insufficient (I):** $N < 100$

## 2. Table IV Updates
- The `Rel.` column was added next to `Bucket`.
- Any bucket with $N < 100$ (e.g., ASSISTments 2012 BKT/DKT/SimpleKT very sparse, XES3G5M BKT sparse and very sparse) was marked as `I` (Insufficient). 
- Footnote updated to explain the abbreviation and interpretation rule.

## 3. Table V Updates
- The `Rel.` column was added next to `Bucket`.
- The same logic applies. Footnote updated to explain the abbreviations and add the specific BKT warning.

## 4. Specific Flags per Dataset (Table IV Learner-based)
- **ASSISTments 2012:**
  - BKT/DKT/SimpleKT Dense: R
  - BKT/DKT/SimpleKT Medium: R
  - BKT/DKT/SimpleKT Sparse: I / L / L
  - BKT/DKT/SimpleKT Very Sparse: I
- **Junyi Academy:**
  - BKT/DKT/SimpleKT Dense: R
  - BKT/DKT/SimpleKT Medium: R
- **XES3G5M:**
  - BKT/DKT/SimpleKT Dense: R
  - BKT/DKT/SimpleKT Medium: R
  - BKT Sparse: I
  - BKT Very Sparse: I
  - DKT/SimpleKT Sparse: R
  - DKT/SimpleKT Very Sparse: L

## 5. Changes to Figures & Text
- **Reliability Diagram (Figure 3):** Since there is no automated script to replot the PDF figure dynamically, the text and caption describing Figure 3 (Junyi temporal very sparse) were updated. The text now explicitly states: *"However, due to the Insufficient number of test events ($N < 100$) in the very sparse bucket, this diagram should be interpreted as a descriptive example rather than stable evidence."*
- **Main Text (Section IV.A & IV.C):**
  - Inserted the principle definition in Section IV.A: *"Following design principle P3, we annotate each bucket-level result with a reliability flag based on its sample size. Results from Insufficient buckets ($N < 100$) are reported for completeness but should be interpreted as descriptive, not as evidence of model behavior."*
  - Modified the strong claim in Section IV.C regarding DKT's high AUC on very sparse buckets to explicitly mention it is based on an Insufficient sample size and should be interpreted descriptively.

## 6. Constraints Confirmed
- **Có thay đổi threshold không?** Không.
- **Có thay đổi số liệu thực nghiệm gốc không?** Không.
- **Bold text trong Insufficient buckets:** Bảng gốc vốn không tô đậm (bold) kết quả, do đó không cần xoá bỏ `\textbf{}`.

*(Note: The local environment does not have a working LaTeX compiler, so `P0_bucket_reliability_flags_added.pdf` could not be built. However, all source files and CSVs have been fully and safely updated.)*
