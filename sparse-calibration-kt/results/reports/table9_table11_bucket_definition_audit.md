# Table 9 & Table 11 Bucket Definition Audit

## 1. Bucket Distribution on Junyi Temporal Split
- **Junyi temporal strict group**: 4 KCs / 2,545 Events.
- **Junyi temporal very sparse group after excluding strict**: 0 KCs / 0 Events.

## 2. Table Renderings
- **Whether Table 9 uses “strict cold-start” or recomputed “very sparse”**: Table 9 uses the recomputed "very sparse" (which explicitly excludes req_train = 0). For Junyi Temporal, the "very sparse" row is completely omitted because it contains 0 KCs/Events after this exclusion. "Strict cold-start" is NOT included in Table 9.
- **Whether Table 11 uses “strict cold-start” or recomputed “very sparse”**: Similarly, Table 11 uses the recomputed "very sparse" and explicitly excludes "strict cold-start". For Junyi Temporal, Table 11 only shows dense, medium, and sparse rows.

## 3. Duplication Check
- **No bucket duplication**: PASS. The groups are strictly disjoint. The 4 zero-frequency KCs in Junyi Temporal are reported **only** in Table 6 (Cold-Start Diagnostics) under the strict (and effectively k5, k10) cohorts, and are completely removed from the general strata reporting in Tables 9 and 11.
