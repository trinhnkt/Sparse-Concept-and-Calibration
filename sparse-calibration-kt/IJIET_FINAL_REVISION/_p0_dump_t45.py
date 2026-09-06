#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import win32com.client as win32

FULL = Path(__file__).resolve().parent / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"


def cell(tbl, r, c):
    return tbl.Cell(r, c).Range.Text.replace("\r", " ").replace("\x07", "").strip()


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL), ReadOnly=True)
    try:
        for t in range(1, doc.Tables.Count + 1):
            tbl = doc.Tables(t)
            prev = doc.Range(max(0, tbl.Range.Start - 200), tbl.Range.Start)
            cap = " ".join(prev.Text.replace("\r", " ").replace("\x07", " ").split())
            if True:
                print(f"\n==== t{t} {tbl.Rows.Count}x{tbl.Columns.Count} ====")
                print(cap[-240:])
                for r in range(1, tbl.Rows.Count + 1):
                    vals = [cell(tbl, r, c) for c in range(1, tbl.Columns.Count + 1)]
                    print(r, vals)
    finally:
        doc.Close(0)
        word.Quit()


if __name__ == "__main__":
    main()
