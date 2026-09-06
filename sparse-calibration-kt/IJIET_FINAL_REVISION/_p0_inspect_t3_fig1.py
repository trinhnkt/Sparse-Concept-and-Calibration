#!/usr/bin/env python3
"""Inspect Word order around Table 3 / Fig. 1."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from manuscript_paths import FULL_DOCX  # noqa: E402

WD_SAVE = 0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL_DOCX), ReadOnly=True)
    try:
        n = doc.Paragraphs.Count
        print("paras", n, "inlines", doc.InlineShapes.Count, "tables", doc.Tables.Count)
        for i in range(1, n + 1):
            p = doc.Paragraphs(i)
            t = (p.Range.Text or "").replace("\r", " ").replace("\x07", " ").strip()
            if not t and p.Range.InlineShapes.Count == 0:
                continue
            hit = (
                t.startswith("Table 3")
                or t.startswith("Fig. 1")
                or "seven-channel" in t.lower()
                or "summarizes that pipeline" in t
                or p.Range.InlineShapes.Count
                or t.startswith("Channel")
                or t.startswith("L1 ")
            )
            if hit or (30 <= i <= 55):
                nshp = p.Range.InlineShapes.Count
                extra = f"  shapes={nshp}" if nshp else ""
                print(f"{i:04d}{extra} {t[:140]}")
        print("--- tables ---")
        for ti in range(1, doc.Tables.Count + 1):
            tb = doc.Tables(ti)
            cap = (tb.Range.Paragraphs(1).Range.Text or "")[:80]
            wrap = tb.Rows.WrapAroundText if hasattr(tb.Rows, "WrapAroundText") else "?"
            print(f"T{ti} rows={tb.Rows.Count} cols={tb.Columns.Count} wrap={wrap} first={cap!r}")
        if doc.InlineShapes.Count:
            s = doc.InlineShapes(1)
            print(f"fig1 {s.Width:.1f}x{s.Height:.1f}")
    finally:
        doc.Close(WD_SAVE)
        word.Quit()


if __name__ == "__main__":
    main()
