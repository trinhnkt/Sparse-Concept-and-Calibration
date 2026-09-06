#!/usr/bin/env python3
"""P0: keep IV.D as secondary evidence; move Table 8 sparsification to SI S2."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_secondary"
WD_FORMAT_XML = 16
WD_SAVE = -1
WD_ALIGN_JUSTIFY = 3
WD_COLLAPSE_END = 0
FIRST = 10.1

REPLACEMENTS = [
    (
        "Learner exposure (distinct training learners per KC) enters the regressions below; it is not an E1–E2 estimability criterion. This subsection reports two distinct estimands. Neither is a causal claim.",
        "Learner exposure (distinct training learners per KC) enters the regressions below; it is not an E1–E2 estimability criterion. The regression and sparsification checks are not causal claims.",
    ),
    (
        "Table 7 separates two questions.",
        "The following checks are secondary evidence for why and when a sparse-calibration contrast is estimable; they do not replace the per-stratum ECE and Brier results. Table 7 separates two questions.",
    ),
    (
        "Within-KC controlled sparsification holds KC identity, the test set, labels, and all other KCs' training rows fixed, and reduces training rows for 30 originally dense KCs (ftrain≥500; seed 42, fold 0) to 500 or 50 rows. The selection rule was fixed and recorded before reduced-evidence ECE was inspected. Table 8 reports protocol endpoints (500 and 50 rows) for DKT and T-KT on all three datasets. Complete results for all models, datasets, and reduction levels are reported in Supplementary Table S2. Reducing training evidence for the same KC does not universally worsen calibration: several CIs lie below 0 or include 0. XES3G5M T-KT shows a positive ΔECE at 50 rows (+0.110 [+0.071, +0.156]); DKT at 500 rows is also positive (Table 8; Supplementary Table S2). The observational ASSISTments T-KT dense-to-sparse ECE gradient (0.114→0.228) is not reproduced by sparsifying originally dense ASSISTments KCs (T-KT, 50 rows: +0.002 [−0.021, +0.025]). Frequency alone is therefore not a universal causal explanation. Junyi T-KT at 50 rows does show a large positive ΔECE; that cell shows a within-KC increase is possible, not that it is a law.",
        "Controlled sparsification does not reproduce a universal monotonic frequency effect; complete dataset-model results are in Supplementary Table S2.",
    ),
    (
        "Within-KC sparsification (Table 8) does not reproduce the observational ASSISTments T-KT ECE gradient.",
        "Within-KC sparsification (Supplementary Table S2) does not reproduce the observational ASSISTments T-KT ECE gradient.",
    ),
    (
        "The next Table 9 slice is the protocol very-sparse bucket",
        "The next Table 8 slice is the protocol very-sparse bucket",
    ),
    (
        "Table 9 reports feasibility, not a production claim.",
        "Table 8 reports feasibility, not a production claim.",
    ),
    (
        "Table 9. Cold-start concept feasibility",
        "Table 8. Cold-start concept feasibility",
    ),
]

ESTIMANDS = (
    "The three analyses target different estimands: stratum ECE is an event-weighted "
    "coarse-bucket contrast, the regression estimates an adjusted between-KC association, "
    "and controlled sparsification evaluates an artificial within-KC reduction of training "
    "evidence. Their signs and magnitudes therefore need not coincide."
)


def para_text(para) -> str:
    return para.Range.Text.replace("\r", "").replace("\x07", "")


def apply_pairs(doc, pairs, log) -> None:
    for old, new in pairs:
        n = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text
            if old in text:
                inner.Text = text.replace(old, new)
                n += 1
        log.append(f"repl {old[:42]!r} n={n}")
        if n < 1:
            raise SystemExit(f"missing replacement {old[:60]!r}")


def insert_estimands(doc, log) -> None:
    for i in range(1, doc.Paragraphs.Count + 1):
        para = doc.Paragraphs(i)
        t = para_text(para)
        if not t.startswith("Controlled sparsification does not reproduce"):
            continue
        rng = para.Range
        rng.Collapse(WD_COLLAPSE_END)
        rng.InsertParagraphAfter()
        newp = para.Next()
        inner = doc.Range(newp.Range.Start, newp.Range.End - 1)
        inner.Text = ESTIMANDS
        try:
            newp.Style = "Text"
        except Exception:
            pass
        newp.Format.Alignment = WD_ALIGN_JUSTIFY
        newp.Format.FirstLineIndent = FIRST
        log.append(f"inserted estimands after p{i}")
        return
    raise SystemExit("sparsification sentence not found for insert")


def delete_table8(doc, log) -> None:
    for t in range(doc.Tables.Count, 0, -1):
        tbl = doc.Tables(t)
        if tbl.Rows.Count != 13 or tbl.Columns.Count != 6:
            continue
        h = tbl.Cell(1, 1).Range.Text.replace("\r", "").replace("\x07", "").strip()
        if h != "Dataset":
            continue
        cap = doc.Range(tbl.Range.Start - 1, tbl.Range.Start).Paragraphs(1)
        cap_t = para_text(cap)
        if "Within-KC controlled sparsification" not in cap_t and "Table 8." not in cap_t:
            continue
        tbl.Delete()
        if "Within-KC" in cap_t or "Table 8." in cap_t:
            cap.Range.Delete()
        log.append(f"deleted Table 8 cap={cap_t[:70]!r}")
        return
    raise SystemExit("main-text Table 8 sparsification not found")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["secondary_explain"]
    try:
        apply_pairs(doc, REPLACEMENTS, log)
        insert_estimands(doc, log)
        delete_table8(doc, log)
        body = doc.Content.Text or ""
        if "Table 8. Within-KC" in body:
            raise SystemExit("Table 8 sparsification caption remains")
        if ESTIMANDS not in body.replace("\r", " ").replace("\x07", " "):
            # Word may break lines; check a distinctive fragment
            if "Their signs and magnitudes therefore need not coincide" not in body:
                raise SystemExit("estimands sentence missing")
        if "Controlled sparsification does not reproduce a universal monotonic" not in body:
            raise SystemExit("short sparsification sentence missing")
        if "secondary evidence for why and when" not in body:
            raise SystemExit("secondary-evidence frame missing")
        if "Table 8. Cold-start" not in body:
            raise SystemExit("cold-start not Table 8")
        if "Table 9. Cold-start" in body:
            raise SystemExit("cold-start still Table 9")
        if "Table 7. Empirical conditions" not in body:
            raise SystemExit("Table 7 missing")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        if "0.196" not in body or "0.268" not in body:
            raise SystemExit("FAR locks missing")
        if "two distinct estimands" in body:
            raise SystemExit("old two-estimands sentence remains")
        if "+0.110 [+0.071, +0.156]" in body and "Table 8 reports protocol" in body:
            raise SystemExit("long Table 8 prose remains")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        print("\n".join(log))
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
