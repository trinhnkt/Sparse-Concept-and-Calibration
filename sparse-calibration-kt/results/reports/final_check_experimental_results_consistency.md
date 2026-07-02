# Global Experimental Results Consistency Check

## 1. Old Numbers Verification
A regex search across `paper/sections/04_experiments.tex` confirmed that the following outdated numbers have been successfully removed:
- `0.6987`
- `0.6825`
- `0.9117`
- `0.0794`
- `0.8630`
- `0.8508`
- `0.8708`
- `0.8593`
- `0.8186`
- `0.7554`
(Note: Some of these numbers correctly remain within the Table IV output files, as they correspond to Dense strata values, but all references in the text interpreting these values have been updated to the current post-correction values).

## 2. Table VIII Verification
References to Table VIII now accurately use the overall temporal values:
- ASSISTments temporal IRT: `0.5917`
- DKT: `0.6609`
- SimpleKT: `0.6739`

## 3. Table VI Warm Cohort Verification
The text references warm-cohort values explicitly separated from the overall temporal values, properly matching Table VI:
- ASSISTments warm: IRT 0.5923, DKT 0.6610, SimpleKT 0.6741
- Junyi warm: IRT 0.6527, DKT 0.6949, SimpleKT 0.7129
- XES3G5M warm: IRT 0.6563, DKT 0.6573, SimpleKT 0.6613

## 4. Figure 1 Verification
- The pipeline figure explicitly displays `Leakage & Predictive Sanity Audit (L1--L8)`.
- The pipeline figure natively includes `≤ 5 or ≤ 10` for the k-shot definition.
- The `03_protocol.tex` caption has been adjusted to cleanly reflect the natively generated image text.

## 5. Figure 3 Verification
- See `final_check_figure3_regeneration_status.md` for full provenance. The image was successfully regenerated directly from the post-T9 prediction CSV file, resulting in identical ECE/N values.

## 6. Appendix D Verification
- The L8 predictive sanity check warning has been added into `table_interpretation_guide.tex` for the near-random diagnostic pattern.

## 7. IRT Temporal Std Verification
- The clarification sentence for deterministic model variance (IRT) under the 5-fold evaluation loop has been properly added to `04_experiments.tex`.
