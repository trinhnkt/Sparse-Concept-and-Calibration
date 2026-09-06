# CHANGELOG_P0 — Align main text with GS Hậu roadmap v3.0

**Date:** 2026-09-03  
**Pages:** 8–10 allowed. **Retrain:** no. **Locks:** ASSISTments ECE `0.1136`/`0.2280`; FAR `0.196`/`0.268` remain as a simulated probe.

| Phase | Change |
|---|---|
| 1 | Removed TSCDA name; GKT/CL4KT not scored; II.B → evaluation rigor/leakage |
| 2 | Contributions C1 protocol+L1–L7, C2 ECE/Brier/reliability, C3 artefact |
| 3 | Table 9 leakage; Table 10 Brier U-R-R; Table 11 cold-start feasibility; Fig. 2 reliability |
| 4 | `analysis/leakage_audit_log.csv`; `docs/how_to_reproduce.md` |
| 5 | Named+blind PDF 9/9 pages; OJS pack synced 2026-09-03 |
| 6 | Editorial 2026-09-04: drop leftover “locked C2”; Table 7 estimability labels E1–E3; cite GKT/CL4KT [8][9] as related literature only; keywords protocol/leakage; L6 = final checkpoint |
| 7 | Grammar/caption: “an E1–E2”; Table 9 PASS includes fixed schedule (L6 final checkpoint) |
| 8 | FAR Tables 5–6 → SI S5–S6; main tables renumbered 1–9; Table 9 cold-start Autofit |

| 9 | SI Table S7 three-cut (20/100/500 lock; Alt-1 10/50/250; Alt-2 30/150/750) on frozen T-KT CSVs; `how_to_reproduce.md` points to `reproduce_one_dataset.sh` and states it does not recreate locked ECE/FAR |

| 10 | Official SimpleKT [4] on ASSISTments 4 partitions: AUC `0.7700±0.0013`, ACC `0.7522±0.0014`; ECE dense `0.0203±0.0035` / medium `0.0262±0.0025` / sparse `0.0884±0.0187` (N=415 L). ΔECE +0.068; added Table 4 row + Table 5 three rows. T-KT ECE `0.1136`/`0.2280` unchanged. BKT still not scored. Junyi/XES official ECE not added. |

| 11 | IV.B pointer to SI Table S7 (3-cut does not flip T-KT dense→sparse ECE). IV.C: seed-42 ΔFAR CI `[0.006, 0.138]` called wide; sparse ECE Limited N=415. Table 9 Small Caps off. T-KT ECE/FAR locks unchanged. |

| 12 | V.B: EdTech skip/advance gates consume *p*, not AUC; protocol is evaluation, not a production threshold. T-KT ECE/FAR locks unchanged. |
| 13 | Restore justify + Text style on 9 leftover Normal paragraphs (IV.D, IV.E, V.A–D, VI). No numeric edits. |
| 14 | Close GS v3.0 items 6/7/10 without BKT or lock edits: SI S8 bucket AUC/ACC; SI S9 baseline inventory (IRT fallback; no 2–3% pyKT Assist2012 claim); `scripts/rebuild_locked_tables.sh` verifies ECE 0.1136/0.2280 from frozen CSVs. IV.A / Limitations pointers. |
| 15 | Table 9 XES very-sparse → masked a2b: N 112→114, T-KT ECE 0.183→0.184, DKT ECE 0.184→0.173; prose N≈112→N≈114. Assist 0.245/0.178 unchanged. T-KT ECE/FAR locks unchanged. |
| 16 | Table 9 caption: XES very-sparse = same masked series as Table 5 (N=114). Locks file records 0.184/0.173. |

Official `pykt.models.simplekt.simpleKT` ASSISTments AUC/ECE is now in the manuscript. BKT remains un-scored (pyBKT 1.4.1 degenerate on ASSISTments fold 0 seed 42).
