#!/usr/bin/env python3
"""P0: reorder Results to A–F roadmap. No numeric lock edits. No k5/k10."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_reorder"
WD_FORMAT_XML = 16
WD_SAVE = -1
WD_COLLAPSE_START = 1

REPLACEMENTS = [
    (
        "The main ASSISTments calibration ordering remains qualitatively unchanged under two alternative train-only frequency cut grids (Supplementary Table S7). ",
        "",
    ),
    (
        "C. Threshold-based decision error",
        "F. Secondary decision-error probe",
    ),
    (
        "D. Dataset-dependent explanatory analysis",
        "D. Diagnostic conditions and threshold sensitivity",
    ),
    (
        "E. Cold-start concept feasibility",
        "C. Cold-start concept feasibility",
    ),
    (
        "Table 7. Empirical conditions",
        "Table 8. Empirical conditions",
    ),
    (
        "Table 7 separates two questions.",
        "Table 8 separates two questions.",
    ),
    (
        "Limited sparse support, Table 7)",
        "Limited sparse support, Table 8)",
    ),
    (
        "structural context (Table 7)",
        "structural context (Table 8)",
    ),
    (
        "The next Table 8 slice",
        "The next Table 7 slice",
    ),
    (
        "Table 8 reports feasibility",
        "Table 7 reports feasibility",
    ),
    (
        "Table 8. Cold-start concept feasibility",
        "Table 7. Cold-start concept feasibility",
    ),
    (
        "they do not replace the per-stratum ECE and Brier results. Table 8 separates two questions.",
        "they do not replace the per-stratum ECE and Brier results. "
        "Supplementary Table S7 checks the same ASSISTments T-KT dense-to-sparse ECE rise "
        "under two alternative train-only cut grids; the sign does not flip. "
        "Table 8 separates two questions.",
    ),
]


def para_text(para) -> str:
    return para.Range.Text.replace("\r", "").replace("\x07", "")


def find_para(doc, start: str) -> int:
    for i in range(1, doc.Paragraphs.Count + 1):
        if para_text(doc.Paragraphs(i)).startswith(start):
            return i
    raise SystemExit(f"not found: {start!r}")


def apply_pairs(doc, pairs, log) -> None:
    for old, new in pairs:
        n = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            if old in inner.Text:
                inner.Text = inner.Text.replace(old, new)
                n += 1
        log.append(f"repl {old[:36]!r} n={n}")
        if n < 1:
            raise SystemExit(f"missing {old[:60]!r}")


def cut_to_before(doc, start: str, end: str, paste_before: str, log: str) -> None:
    s = find_para(doc, start)
    e = find_para(doc, end)
    rng = doc.Range(doc.Paragraphs(s).Range.Start, doc.Paragraphs(e).Range.Start)
    rng.Cut()
    dest = find_para(doc, paste_before)
    ins = doc.Paragraphs(dest).Range
    ins.Collapse(WD_COLLAPSE_START)
    ins.Paste()
    print(f"moved {start!r} -> before {paste_before!r}")


def insert_e_heading(doc, log) -> None:
    i = find_para(doc, "Learner exposure")
    style = doc.Paragraphs(find_para(doc, "D. Diagnostic conditions")).Style
    rng = doc.Paragraphs(i).Range
    rng.Collapse(WD_COLLAPSE_START)
    rng.InsertParagraphBefore()
    newp = doc.Paragraphs(i)
    newp.Style = style
    inner = doc.Range(newp.Range.Start, newp.Range.End - 1)
    inner.Text = "E. Secondary explanatory analysis"
    log.append(f"inserted E heading at p{i}")


def heading_order(doc) -> list[str]:
    out = []
    in_iv = False
    for i in range(1, doc.Paragraphs.Count + 1):
        t = para_text(doc.Paragraphs(i)).strip()
        if t.startswith("IV. RESULTS"):
            in_iv = True
        if t.startswith("V. DISCUSSION"):
            break
        if in_iv and t[:2] in ("A.", "B.", "C.", "D.", "E.", "F."):
            out.append(t)
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["reorder_results"]
    try:
        cut_to_before(
            doc,
            "E. Cold-start concept feasibility",
            "V. DISCUSSION",
            "C. Threshold-based decision error",
            log,
        )
        cut_to_before(
            doc,
            "C. Threshold-based decision error",
            "D. Dataset-dependent explanatory analysis",
            "V. DISCUSSION",
            log,
        )
        apply_pairs(doc, REPLACEMENTS, log)
        insert_e_heading(doc, log)
        heads = heading_order(doc)
        log.append("HEADS " + " | ".join(heads))
        want = [
            "A. Aggregate discrimination",
            "B. Calibration across frequency strata",
            "C. Cold-start concept feasibility",
            "D. Diagnostic conditions and threshold sensitivity",
            "E. Secondary explanatory analysis",
            "F. Secondary decision-error probe",
        ]
        if heads != want:
            raise SystemExit(f"heading order {heads}")
        body = doc.Content.Text or ""
        if "Table 7. Cold-start" not in body:
            raise SystemExit("cold-start not Table 7")
        if "Table 8. Empirical conditions" not in body:
            raise SystemExit("conditions not Table 8")
        if "Table 7. Empirical conditions" in body:
            raise SystemExit("old Table 7 conditions remains")
        if "k5/k10" not in body:
            raise SystemExit("lost k5/k10 disclaimer")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        if "0.196" not in body or "0.268" not in body:
            raise SystemExit("FAR locks missing")
        if "0.056" not in body:
            raise SystemExit("0.056 missing")
        if "Supplementary Table S7" not in body:
            raise SystemExit("S7 pointer missing")
        if "mastery outcome" in body.lower():
            raise SystemExit("mastery outcome")
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
