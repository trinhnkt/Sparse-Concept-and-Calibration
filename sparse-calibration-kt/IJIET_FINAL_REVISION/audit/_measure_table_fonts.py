#!/usr/bin/env python3
"""Measure table/caption fonts in the living named Word + PDF."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import fitz
import win32com.client as win32

HERE = Path(__file__).resolve().parent.parent
DOCX = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
PDF = HERE / "output" / "OJS_UPLOAD" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf"


def font_of(rng) -> tuple[str, float]:
    f = rng.Font
    name = f.Name or ""
    sz = float(f.Size) if f.Size not in (None, 9999999) else -1
    return name, sz


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(DOCX), ReadOnly=True)
    try:
        print("=== CAPTIONS ===")
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs(i)
            t = doc.Range(p.Range.Start, p.Range.End - 1).Text.replace("\r", "").strip()
            if t.startswith("Table ") or t.startswith("Fig."):
                name, sz = font_of(doc.Range(p.Range.Start, p.Range.End - 1))
                print(f"{p.Style.NameLocal!r} {name} {sz}pt | {t[:88]}")

        print("=== TABLE CELLS (Word) ===")
        for ti in range(1, doc.Tables.Count + 1):
            tbl = doc.Tables(ti)
            sz_c: Counter[float] = Counter()
            font_c: Counter[str] = Counter()
            odd = []
            for r in range(1, tbl.Rows.Count + 1):
                for c in range(1, tbl.Columns.Count + 1):
                    try:
                        rng = tbl.Cell(r, c).Range
                    except Exception:
                        continue
                    name, sz = font_of(rng)
                    font_c[name or "(mixed)"] += 1
                    sz_c[sz] += 1
                    txt = rng.Text.replace("\r", " ").replace("\x07", "").strip()
                    if sz not in (7.0, 8.0):
                        odd.append(f"  r{r}c{c} {sz}pt {name} | {txt[:50]}")
            print(
                f"T{ti} {tbl.Rows.Count}x{tbl.Columns.Count} "
                f"fonts={dict(font_c)} sz={dict(sz_c)}"
            )
            for line in odd[:8]:
                print(line)
    finally:
        doc.Close(0)
        word.Quit()

    print("=== PDF SPANS near Table n. ===")
    d = fitz.open(str(PDF))
    for pi, pg in enumerate(d):
        blocks = pg.get_text("dict")["blocks"]
        capture = False
        leftover = 0
        for b in blocks:
            if b.get("type") != 0:
                continue
            for ln in b.get("lines", []):
                spans = ln.get("spans", [])
                line = "".join(s.get("text", "") for s in spans)
                if line.strip().startswith("Table ") or line.strip().startswith("Fig."):
                    capture = True
                    leftover = 18
                if leftover > 0:
                    sizes = sorted({round(s["size"], 1) for s in spans if s.get("text", "").strip()})
                    fonts = sorted({s.get("font", "") for s in spans if s.get("text", "").strip()})
                    print(f"p{pi+1} {sizes} {fonts} | {line.strip()[:90]}")
                    leftover -= 1
                    if leftover == 0:
                        capture = False
    d.close()


if __name__ == "__main__":
    main()
