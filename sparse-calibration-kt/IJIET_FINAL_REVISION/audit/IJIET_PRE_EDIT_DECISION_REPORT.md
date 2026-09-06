# IJIET pre-edit decision report

**Date:** 6 September 2026  
**Mode:** AUDIT ONLY. No manuscript edits. No retrain. No new models.  
**Compiled source audited:** `IJIET_FINAL_REVISION/output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf` (9 pp, 760 669 bytes, 6 Sep 2026 15:49). Same bytes as `output/OJS_UPLOAD/` and `IJIET_SUBMISSION/output/`.  
**Note:** No file named `main_ijiet_blind(2).pdf` is on disk. Windows “(2)” is treated as this living blind PDF. Freeze `IJIET_FINAL_v3/manuscript/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf` (12:10, 735 693 bytes) was **not** used.  
**Word source:** `manuscript/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx` / `Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.docx`.

---

## Decision table

| ID | Proposed issue | Decision | Evidence | Risk if unchanged | Scientific result changes? | Rerun? | Exact action | Confidence |
|----|----------------|----------|----------|-------------------|----------------------------|--------|--------------|------------|
| P01 | Heading “A. E. Secondary explanatory analysis” | **REQUIRED_FIX** | Word Heading 2 is already `E. Secondary explanatory analysis` (full ¶86; blind ¶83). Next is `F. Secondary decision-error probe`. Compiled PDF **page 7** prints one italic heading line `A. E. Secondary explanatory analysis` (clip `audit/_p13_heading_clip.png`; y≈408, mixed Arial-Italic + Times-Italic). Table 8 leftover `A.` is glued onto heading E. | Reviewer reads a broken subsection label. | No | No | **Do not change the Word heading string.** Separate Table 8 from IV.E (paragraph/keep-with-next / table wrap) and rebuild named+blind PDFs so the printed heading is only `E. Secondary explanatory analysis`. Keep `F. Secondary decision-error probe`. | HIGH |
| P02 | Generative AI versions | **AUTHOR_DECISION_REQUIRED** | Blind PDF lists ChatGPT GPT-6 Astra, Claude Sonnet 5, Antigravity 2.12.0, Cursor Grok 4.6. `audit/AI_TOOL_VERSION_AUDIT.md` says **account logs do not retain ChatGPT/Claude/Antigravity build IDs**; those three versions are **public product IDs as of 6 Sep 2026**, filled at author request. Cursor Grok 4.6 is this revision session. Usage text is polish/format/consistency/repro-prompts; “not used to fabricate or alter experimental results.” | If a tool/version cannot be defended, IJIET §6.3 is the exposure. Inventing a “safer” version is worse. | No | No | Author confirms (A) keep public IDs as printed, or (B) log-only: Cursor Grok 4.6 only. See proposed statements below. **Do not invent versions.** | HIGH |
| P03 | Add limited cold-start k5/k10 | **CURRENT_TREATMENT_ACCEPTABLE** (OPTIONAL SI) | Paper already: strict `f=0`; very-sparse `0<f<20`; “not a limited cold-start (k5/k10) group.” Table 7 feasibility. **Registered code** (`src/recalculate_diagnostics.py`, `scripts/audit_temporal_split.py`): `k5: train_freq<=5`, `k10: train_freq<=10` (**includes** `f=0`), `warm: >10`. **Not** `1<=f<=5`. CSVs exist (`clean_cold_start_results_summary.csv`). Junyi temporal k5/k10 **coincide with strict** (0 KCs with `1<=f<=10`; `cold_start_group_audit_report.md`). Roadmap/P0 changelog phase 27 kept k5/k10 out of main Table 7. | Reviewer may ask for k5/k10; paper already disclaims. | No unless SI added | No | Keep Table 7. If SI is added later, use **registered** `f<=5` / `f<=10` and the Junyi coincidence note. **Do not** use the proposed `1<=f_train<=5` sentence as written. Do not redefine very-sparse. | HIGH |
| P04 | Reproducibility level / title | **NO_CHANGE** (title **DEFENSIBLE_WITH_WORDING_LIMIT**) | Claimed artifact: frozen zip + `scripts/rebuild_locked_tables.sh` from frozen summaries; Table 2 `NOT RECOVERED`; Limitations name that script. `docs/how_to_reproduce.md`: Track B = LEVEL A (CSV → S8–S9, verifies 0.1136/0.2280). Track A `reproduce_one_dataset.sh` exists (preprocess→train→metrics) but **does not reproduce locked ECE/FAR**. No Makefile/Docker. `requirements.txt` yes. Predictions exist under `results/predictions/` (92 files). | Over-reading “reproducible” as LEVEL C. Current wording already limits to frozen rebuild. | No | No | **REPRO_LEVEL = A** (review-facing). LEVEL B/C scripts exist but locked numbers are Track B only. Keep “one-command rebuild … from frozen summaries.” Do **not** strengthen to end-to-end. Title is defensible **with that limit**. | HIGH |
| P05 | Baselines vs Roadmap | **ACCEPT_CURRENT_BASELINES** | Scored: IRT, DKT, T-KT × 3 logs; official SimpleKT `[4]` Assist AUC/ECE only. BKT not scored; S9 + Limitations: pyBKT 1.4.1 degenerated Assist seed 42 (`docs/how_to_reproduce.md`). T-KT labeled local, not `[4]`. Official Junyi/XES **JSON+prediction paths exist** (`p0_simplekt_official_junyi_*.json`, `xes3g5m_*.json`) but XES seed-42 `n=1,589,145` matches **obsolete padded** test, not Table 1 `1,282,422`. No AKT exports. Roadmap S9: simpleKT **or** AKT; fallback two stable + documented classical. | Methods reviewer may want BKT or official SimpleKT on 3 logs. That is a new-experiment request. Adding unaligned XES official ECE would **conflict** with a2b locks. | No if unchanged | No | Do not train. Do not add Junyi/XES official cells until XES predictions are a2b-aligned. Deviation note below. | HIGH |
| P06 | Regression KC exclusions | **OPTIONAL** | IV.E: Assist 261 unique / Junyi 1,326 / XES 829. Table 1 totals 265 / 1,326 / 865. Code-traced (`a4_confounding_analysis.py`; `a2b/evaluate.py` inner+dropna): Assist **4** `test_freq=0` (kc 38, 178, 209, 291); Junyi **0**; XES **25** no test preds + **11** missing train covariates (strict `f=0`; 8 also `test_freq=0`). Padding `-1` not in a2b strata. | Reviewer asks 261/265 and 829/865. Reasons are complete-case, not a 866-KC bug. | No | No | Preferred **B**: 3-row SI reason table + one sentence. **C** (no change) is scientifically acceptable. Suggested wording in P06 below. | HIGH |
| P07 | Temporal evidence | **RECOMMENDED_FIX** → **ADD_SUPPLEMENTARY_TEMPORAL_TABLE** *or* **REDUCE_TEMPORAL_CLAIM** | Abstract/contribution (i): “learner-based primary reporting with a complementary temporal split.” Methods: gate **not** from temporal. Limitations: one corrected cutoff, seed 42. SI S10 = temporal **L1–L7 only**, no temporal ECE/AUC table. CSVs exist: `clean_calibration_by_bucket_temporal.csv`, cold-start temporal, `a2b/analysis/temporal_seed42.csv`. `temporal_prediction_alignment_audit.md` is **historical**; Assist/Junyi alignment of those CSVs is **not re-certified in this audit**. | Reviewer: promised temporal, Results are learner-based. | No (reporting) | No | Prefer one SI temporal table from **post-alignment** exports only. If Assist/Junyi alignment cannot be certified, **narrow** contribution (i) instead of inventing numbers. Do not new temporal training. | MEDIUM |
| P08 | “Month date, 2026” + CC BY | **KEEP_TEMPLATE_PLACEHOLDER** | Official template in-repo: `IJIET_SUBMISSION/source/template/IJIET_template.doc` (same 102 400 bytes as `_archive/.../IJIET_template.doc`). Template review 31/08: placeholders `Manuscript received Month date` and CC BY 4.0 are **in the template**. Blind PDF still has them. | None at submission. Inventing dates/DOI/volume is the real policy risk. | No | No | Keep placeholders. Never invent received/accepted/DOI/volume/pages. | HIGH |
| P09 | Fig. 1 print quality | **MINOR_REFORMAT** | Scientific workflow matches the brief (logs→…→reliability). Source PNG `figures/fig1_pipeline.png` is **809×497** (two rows). PDF display box page 3 is **501.7×166.6 pt** (aspect ≈3.01 vs PNG ≈1.63). Figure is **vertically crushed** at print size. Content readable in the PNG; print size is the issue. | Small/squashed labels at IJIET column width. | No | No | Keep workflow. Set Word/PDF frame aspect to 809:497 (e.g. width 501.7 pt → height ≈ **308 pt**) or shrink type, then rebuild. Optional unless editor flags it. | HIGH |
| P10 | Reliability fig: Junyi vs XES | **KEEP_ASSIST_JUNYI** | Fig. 3: Assist dense vs sparse; Junyi dense vs medium (empty sparse). Table 5/8 already give XES flat 0.1176–0.1254. Junyi is the estimability case. Switching costs a new 15-bin figure; little new information. | Low. A reviewer can still ask for an XES panel. | No | No | Keep. Optional extra XES panel in SI only if desired later. | HIGH |
| P11 | Keep Table 6 in main | **KEEP_MAIN** | Table 6 is the only main Murphy extract (Assist DKT/T-KT dense–sparse; Junyi DKT/T-KT dense–medium). S1 is the full grid. Calibration decomposition is contribution (ii). Caption mentions XES 0.1176/0.1129/0.1254 but **body has no XES rows** (caption-only). | Caption/body mismatch is a nit, not a reason to drop the table. | No | No | Keep Table 6. Optional caption trim: delete the XES “Brier rows below” clause (point to S1). Do not move the whole table to SI. | HIGH |
| P12.1 | XES 865 real KCs | **NO_CHANGE** | Table 1 / methods: 865 KCs; official paper 865; padding excluded. | — | No | No | Do not reopen 866. | HIGH |
| P12.2 | XES padding excluded | **NO_CHANGE** | Methods: flatten unmasked positions; padding dropped; 6,413,353 valid KC-level rows. | — | No | No | — | HIGH |
| P12.3 | XES very-sparse N≈114 flag L | **NO_CHANGE** | Table 7: N=114 L; T-KT 0.184; DKT 0.173; same masked series as Table 5. | — | No | No | — | HIGH |
| P12.4 | Junyi ucid exercise-level | **NO_CHANGE** | Methods + V.C: ucid = unique content/exercise ID, not a skill tag. | — | No | No | — | HIGH |
| P12.5 | Junyi = estimability case | **NO_CHANGE** | V.C: granularity-and-estimability, not pedagogical KC sparsity. | — | No | No | — | HIGH |
| P12.6 | FAR secondary, not RQ3 | **NO_CHANGE** | Intro + IV.F: locked gate is a probe, “not RQ3”; S3–S6. | — | No | No | — | HIGH |
| P12.7 | FAR ≠ latent mastery | **NO_CHANGE** | III.H / V.D: y=0 is next-response error, not latent-skill diagnosis. | — | No | No | — | HIGH |
| P12.8 | GKT/CL4KT/GNN/SSL not scored | **NO_CHANGE** | Related-only; Limitations: not trained. 0 experimental GKT/CL4KT cells. | — | No | No | Do not reintroduce. | HIGH |
| P12.9 | RQ3 = conditions + cut robustness | **NO_CHANGE** | Intro RQ3 + IV.D + S7 two alternative grids. FAR not RQ3. | — | No | No | — | HIGH |
| P12.10 | “low-frequency tail mass” | **NO_CHANGE** | Table 8 / IV.D: `f_train<100`; not “sparse mass.” | — | No | No | — | HIGH |
| P12.11 | Limited-support wording | **NO_CHANGE** | III.E: “Substantive stratum-level interpretations require at least Limited support.” | — | No | No | — | HIGH |
| P12.12 | T-KT never called SimpleKT | **NO_CHANGE** | Repeated “not SimpleKT [4]”; Table 4/5 “SimpleKT” rows are **official** `[4]` only. | — | No | No | — | HIGH |
| P12.13 | No universal sparse-AUC fail | **NO_CHANGE** | Intro + IV.A: XES sparse AUC higher (DKT 0.858 vs 0.818; T-KT 0.847 vs 0.752). | — | No | No | — | HIGH |
| P12.14 | No universal sparse-ECE fail | **NO_CHANGE** | Junyi empty; XES essentially flat. | — | No | No | — | HIGH |
| P12.15 | XES flat as counter-pattern | **NO_CHANGE** | IV.B / V.A: “counter-pattern,” “essentially flat.” | — | No | No | — | HIGH |
| P12.16 | Sparsification secondary | **NO_CHANGE** | IV.E + S2; “does not reproduce a universal monotonic frequency effect.” | — | No | No | — | HIGH |
| P12.17 | Regression = association | **NO_CHANGE** | IV.E: “not causal”; “between-KC association.” | — | No | No | — | HIGH |

---

## P02 — proposed AI statements (do not insert yet)

**If the author confirms public product IDs (current PDF):**

> During manuscript preparation, the authors used ChatGPT GPT-6 Astra, Claude Sonnet 5, Google Antigravity 2.12.0, and Cursor Grok 4.6 for language polishing, formatting, consistency checking, and reproducibility-prompt preparation. Those version strings are the public product identifiers as of 6 September 2026; interactive account logs did not retain build IDs. AI was not used to fabricate or alter experimental results. After using these tools, the authors reviewed and edited the content. The authors remain responsible for all content. Generative AI is not listed as a co-author.

**If the author wants only log-verified tools:**

> During manuscript preparation, the authors used Cursor Grok 4.6 for language polishing, formatting, consistency checking, and reproducibility-prompt preparation. AI was not used to fabricate or alter experimental results. After using this tool, the authors reviewed and edited the content. The authors remain responsible for all content. Generative AI is not listed as a co-author.

Do not invent a third set of versions.

---

## P03 extra return

**ADD_K5_K10** — no (not in main).  
**CURRENT_TREATMENT_ACCEPTABLE** — yes.  
**AUTHOR_DECISION_REQUIRED** — only if the supervisor wants a SI k5/k10 table.

Registered convention is `f<=5` / `f<=10` (includes strict). The suggested main-text sentence with `1<=f_train<=5` is **incorrect** for this repo.

---

## P04 extra return

**REPRO_LEVEL = A** (what the paper actually promises and what `rebuild_locked_tables.sh` does).  
Track A is a separate retrain path and is **not** the source of locked Table 5/FAR cells.

**TITLE_REPRODUCIBILITY = DEFENSIBLE_WITH_WORDING_LIMIT**

---

## P05 extra return

**ACCEPT_CURRENT_BASELINES**

Deviation note for supervisor:

> P0 instantiates the diagnostic protocol with local IRT, DKT, and T-KT on three logs after pyBKT 1.4.1 degenerated on ASSISTments seed 42 (IRT is the documented classical fallback). The Roadmap strong slot is filled by official SimpleKT `[4]` on ASSISTments learner-based AUC/ECE only. T-KT is a local Transformer baseline and is not `[4]`. Official SimpleKT prediction files for Junyi/XES exist but XES event counts match the obsolete padded series; they are not added until aligned with the a2b mask. AKT / GKT / CL4KT / GNN / SSL are out of P0 and are not scored.

---

## P06 extra — exclusion table (code-traced)

| Dataset | Total_KCs | Included_KCs | Excluded_KCs | Reason | Count |
|---------|----------:|-------------:|-------------:|--------|------:|
| ASSISTments 2012 | 265 | 261 | 4 | No evaluable test predictions (`test_freq=0`); kc_id 38, 178, 209, 291 | 4 |
| Junyi Academy | 1326 | 1326 | 0 | — | 0 |
| XES3G5M | 865 (padding excluded) | 829 | 36 | 25 no evaluable test predictions; 11 missing train-only covariates (strict `f=0`; 8 of these also `test_freq=0`) | 36 |

Suggested wording **if** SI is added:

> Regression inclusion requires evaluable test predictions and complete train-only covariates; dataset-specific inclusion and exclusion counts are reported in Supplementary Table Sx.

---

## P07 extra return

**TEMPORAL_EVIDENCE_SUFFICIENT** — no (S10 is leakage-only).  
**ADD_SUPPLEMENTARY_TEMPORAL_TABLE** — preferred **if** Assist/Junyi temporal CSVs are certified post-alignment.  
**REDUCE_TEMPORAL_CLAIM** — required alternative if they are not.  
**AUTHOR_DECISION_REQUIRED** — which of those two, after one alignment check.

---

## P08 extra return

**KEEP_TEMPLATE_PLACEHOLDER**

**REMOVE_FOR_SUBMISSION** — no (would deviate from official template).  
**AUTHOR_EDITORIAL_CONFIRMATION_REQUIRED** — only if IJIET OJS later asks to delete placeholders.

---

## P09 / P10 / P11 extra returns

**P09:** MINOR_REFORMAT (aspect), not REDRAW. Workflow unchanged.  
**P10:** KEEP_ASSIST_JUNYI  
**P11:** KEEP_MAIN (optional caption trim only)

---

## Summary

### A. REQUIRED BEFORE SUBMISSION

1. **P01** — Fix compiled heading so page 7 reads `E. Secondary explanatory analysis` (layout/export). Word heading text is already correct.

### B. RECOMMENDED

1. **P07** — Either a certified SI temporal performance table, or a narrower contribution-(i) sentence.  
2. **P09** — Match Fig. 1 frame aspect to PNG 809×497.  
3. **P11 caption** — Drop XES “Brier rows below” from Table 6 caption (S1 already holds XES Brier).

### C. OPTIONAL

1. **P03** — SI-only registered k5/k10 (`f<=5`/`f<=10`), not main Table 7.  
2. **P06** — 3-row SI exclusion table.  
3. **P10** — SI XES reliability panel (not a main-fig swap).

### D. AUTHOR / SUPERVISOR DECISION

1. **P02** — Public AI version IDs vs Grok-only.  
2. **P07** — Add SI temporal table vs reduce claim (depends on alignment certification).  
3. **P05** — Supervisor sign-off on the baseline deviation note (no new training implied).

### E. DO NOT CHANGE

- All **P12.1–P12.17** items.  
- **P04** title and LEVEL A wording.  
- **P05** scored model set (do not add unaligned official Junyi/XES ECE; do not score BKT/GKT/CL4KT).  
- **P08** Month-date / CC BY placeholders.  
- **P10** Assist+Junyi reliability figure.  
- **P11** Table 6 location.  
- Locked numbers: Assist T-KT ECE 0.1136/0.2280; FAR 0.196/0.268; XES 0.1176/0.1129/0.1254; Table 7 XES N=114.  
- No GKT, CL4KT, GNN, SSL, path recommendation, or distillation.

---

## Files that would be touched **if** a later edit pass is approved

| Item | Files | Numbers change? | Retrain? | CPU-only? |
|------|-------|-----------------|----------|-----------|
| P01 | `manuscript/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx` (layout only), rebuild blind/named PDF | No | No | N/A (Word/PDF) |
| P02 | Word Generative AI + cover letter | No | No | N/A |
| P07 reduce-claim | Word Abstract / contribution (i) | No | No | N/A |
| P07 add SI | new SI tex + `supplementary.tex` + pointer | No new experiments | No | Yes, from certified CSVs only |
| P09 | Word Fig. 1 frame size; rebuild PDF | No | No | N/A |
| P11 caption | Word Table 6 caption | No | No | N/A |
| P06 SI | `supplementary/Table_S_regression.tex` or new S-table | No | No | No |

---

**OVERALL_STATUS = READY_FOR_FINAL_FORMAT_AUDIT** (applied 6 Sep 2026, changelog P0 phase 36)

Applied without touching locks: P01 (heading E), P07 (temporal → S10 leakage only), P09 (Fig. 1 809×497 aspect), P11 (Table 6 caption). Not applied: P02 author AI versions, P03/P06 optional SI, P05 supervisor note.
