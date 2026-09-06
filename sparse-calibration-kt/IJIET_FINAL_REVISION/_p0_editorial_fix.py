#!/usr/bin/env python3
"""P0 editorial: locked C2, Table 7 E1–E3, cite [8][9], keywords, L6."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BACKUP = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_editorial"

WD_FORMAT_XML = 16
WD_SAVE = -1
EN = "\u2013"

PAIRS = [
    (
        " (locked C2)",
        "",
    ),
    (
        "evaluation instrument, mastery threshold",
        "evaluation protocol, leakage audit",
    ),
    (
        "Graph-based and contrastive KT models are related literature only;",
        "Graph-based Knowledge Tracing [8] and contrastive learning for KT [9] "
        "are related literature only;",
    ),
    (f"C1{EN}C2", f"E1{EN}E2"),
    ("C1-C2", "E1-E2"),
    ("C1 is a non-empty", "E1 is a non-empty"),
    ("C2 is enough sparse", "E2 is enough sparse"),
    ("C3 and other structural", "E3 and other structural"),
    ("C3 (frequency", "E3 (frequency"),
    ("C3 is not necessary", "E3 is not necessary"),
    ("Sparse mass (C1)", "Sparse mass (E1)"),
    ("Sparse test support (C2)", "Sparse test support (E2)"),
    ("Difficulty coupling (C3)", "Difficulty coupling (E3)"),
    ("Valid-only selection", "Final checkpoint"),
]


def apply_pairs(text: str) -> tuple[str, list[str]]:
    hits: list[str] = []
    out = text
    for old, new in PAIRS:
        if old and old in out:
            n = out.count(old)
            out = out.replace(old, new)
            hits.append(f"{old[:40]!r} x{n}")
    return out, hits


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.copy2(FULL, BACKUP)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["editorial"]
    try:
        n_para = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            try:
                if para.Range.Tables.Count:
                    continue
            except Exception:
                pass
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text
            new, hits = apply_pairs(text)
            if hits:
                inner.Text = new
                n_para += 1
                log.append(f"p{i}: {'; '.join(hits)}")
        n_cell = 0
        for t in range(1, doc.Tables.Count + 1):
            table = doc.Tables(t)
            for r in range(1, table.Rows.Count + 1):
                for c in range(1, table.Columns.Count + 1):
                    try:
                        cell = table.Cell(r, c)
                    except Exception:
                        continue
                    inner = doc.Range(cell.Range.Start, cell.Range.End - 1)
                    text = inner.Text
                    new, hits = apply_pairs(text)
                    if hits:
                        inner.Text = new
                        n_cell += 1
                        log.append(f"t{t}r{r}c{c}: {'; '.join(hits)}")
        body = doc.Content.Text or ""
        if "(locked C2)" in body or "locked C2" in body:
            raise SystemExit("locked C2 still present")
        if "evaluation instrument" in body.lower():
            raise SystemExit("keywords still evaluation instrument")
        if "[8]" not in body or "[9]" not in body:
            raise SystemExit("missing [8] or [9] in body")
        if f"C1{EN}C2" in body or "C1-C2" in body:
            raise SystemExit("C1–C2 estimability label still present")
        if "Sparse mass (C1)" in body:
            raise SystemExit("Table 7 still uses C1")
        if "Valid-only selection" in body:
            raise SystemExit("L6 still Valid-only selection")
        if f"E1{EN}E2" not in body and "E1-E2" not in body:
            raise SystemExit("E1–E2 not inserted")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        log.append(f"paras={n_para} cells={n_cell}")
        print("\n".join(log))
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
