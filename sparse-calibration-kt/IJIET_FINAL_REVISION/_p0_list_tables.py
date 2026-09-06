#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import win32com.client as win32

FULL = Path(__file__).resolve().parent / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL), ReadOnly=True)
    try:
        print("tables", doc.Tables.Count)
        for t in range(1, doc.Tables.Count + 1):
            tbl = doc.Tables(t)
            prev = doc.Range(max(0, tbl.Range.Start - 250), tbl.Range.Start)
            cap = " ".join(prev.Text.replace("\r", " ").replace("\x07", " ").split())[-180:]
            h = tbl.Cell(1, 1).Range.Text.replace("\r", " ").replace("\x07", "").strip()
            print(f"t{t} rows={tbl.Rows.Count} cols={tbl.Columns.Count} h={h!r}")
            print(f"  cap... {cap}")
        body = doc.Content.Text or ""
        for s in ["Table 5. Simulated", "Table 6. Gate", "Table 3. Seven", "IVC probe", "A locked gate"]:
            print("hit", s, s in body)
        print("locked gate", "A locked gate at" in body)
        print("table5 sim", "Table 5 is a simulated" in body)
    finally:
        doc.Close(0)
        word.Quit()


if __name__ == "__main__":
    main()
