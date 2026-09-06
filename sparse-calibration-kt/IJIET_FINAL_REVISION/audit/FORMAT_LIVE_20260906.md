# FORMAT LIVE — IJIET template vs living pack (6 Sep 2026)

**Authority:** `IJIET_SUBMISSION/source/template/IJIET_template.doc` (www.ijiet.org: “follow the Template Paper”).  
**Measured:** Word COM + PDF (`audit/_format_ijiet_live.py`).  
**Files:** title-named Word + named/blind PDF (9/9 pages after Table 3 / Fig. 1 fix).

## Verdict

**Fits the IJIET submission template.** Geometry, typeface, front matter, 2-column body, captions, references, empty header/footer, and 8–10 page band all match. Not a desk-reject format risk. Remaining items are known intentional deviations or nits.

## Mandatory checks

| # | Template rule | Living | Status |
|---|---|---|---|
| 1 | A4 595.35×841.95 pt | Word 595.35×841.95; PDF 595.32×841.92 | **OK** |
| 2 | Margins T/B 50.45, L/R 46.80 | All 22 sections identical | **OK** |
| 3 | Front 1-col 501.75; body 2-col 243.65 + gutter 14.40 | sec1 1-col; 2-col sections exact; 1-col bands for wide tables/figs (template also switches) | **OK** |
| 4 | Empty header/footer (no vol/DOI/running head) | All sections `header='' footer=''`; PDF top band empty; no `10.18178` | **OK** |
| 5 | Title 20 pt TNR, centered, not bold | 20.0 pt TNR center, SpaceAfter 20 | **OK** |
| 6 | Authors 11 pt TNR, centered | 11.0 pt (style name still “+ Asian MS Mincho”, same as template) | **OK** |
| 7 | Affiliation / email / corresponding 9 pt center | 9.0 pt; `*Corresponding author`; emails present | **OK** |
| 8 | Dates: template placeholders until production | `Month date, 2026` ×3 | **OK** |
| 9 | Abstract— / Keywords— 9 pt, indent 10.1, justify | Style `Abstract` / `IndexTerms` 9 pt | **OK** |
| 10 | Heading 1 10 pt TNR, centered | I–VI 10 pt center | **OK** |
| 11 | Body Text 10 pt TNR justify, first-line 10.1 | 48 body paras 10 pt justify; PDF body 10.0 | **OK** |
| 12 | Table/Fig caption style `figure caption` 8 pt | True captions 8 pt; “Table 4 reports…” is body 10 pt (not a caption) | **OK** |
| 13 | Tables TNR; template sample 8 pt | T2 **8 pt**; T1, T3–T8 **7 pt** (wide 2-col fit; prior audit) | **OK** (intentional) |
| 14 | Figs embedded, not linked | 3 inline shapes; Fig. 1 501.8×179.2; Fig. 2 501.8×352.5; Fig. 3 501.8×465.8 | **OK** |
| 15 | References 8 pt hanging | Style `References` 8 pt, hang −18 pt | **OK** |
| 16 | CC BY footer line | Present | **OK** |
| 17 | Length | Named 9 / blind 9 (allowed 8–10) | **OK** |
| 18 | Double-blind PDF | Blind meta author empty; no Hung Yen / github / trinhnkt | **OK** |

## Intentional deviations (do not change unless editor asks)

- Heading 1 typed as `I. INTRODUCTION` ALL CAPS (template sample heading is “Introduction”; published IJIET issues use the numbered form).
- `IV. RESULTS` and `V. DISCUSSION` split (template sample combines “Result and Discussion”).
- Affiliation omits Department/Faculty (university + city + country only).
- Extra end-matter: Conflict, Author contributions, Ethical, Data/code, Generative AI, Acknowledgment.
- Extra 1-col sections for Tables 1–3 / Figs 1–3 (template also inserts 1-col for wide objects).
- Table body 7 pt except Table 2 at 8 pt.

## Nits (not desk-reject)

| Nit | Detail |
|---|---|
| Author `SpaceAfter` | Template 6 pt; living 0 pt (block slightly tighter). |
| Table 7 cell styles | Header/body cells are **Heading 1** in Word (print 7 pt). Outline/navigation looks noisy; PDF is fine. |
| Caption scan false hits | PDF reports 3× 10 pt lines starting “Table …” — those are body sentences (`Table 4 reports`, `Table S7`). |
| Author style name | Still lists Asian MS Mincho (copied from template); rendered TNR 11. |
| Table 8 | 3 mixed-font symbol cells, still 7 pt. |

## What is not required at submission

Volume, issue, DOI `10.18178/ijiet`, production page numbers, or filled received/revised/accepted dates. Header must stay empty.

## Locks (unchanged by this audit)

ECE 0.1136 / 0.2280; FAR 0.196 / 0.268; XES 0.1176 / 0.1129 / 0.1254; Fig. 1 present; refs through [26].
