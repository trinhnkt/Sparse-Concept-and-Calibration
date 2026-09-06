#!/usr/bin/env python3
"""Inspect Word sections and inline figures."""
from __future__ import annotations

import sys

import win32com.client as win32

from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL), ReadOnly=True)
    try:
        print("sections", doc.Sections.Count)
        for i in range(1, doc.Sections.Count + 1):
            ps = doc.Sections(i).PageSetup
            cols = ps.TextColumns.Count
            start = doc.Sections(i).Range.Start
            print(f"sec{i} cols={cols} start={start}")
        print("figs", doc.InlineShapes.Count)
        for i in range(1, doc.InlineShapes.Count + 1):
            sh = doc.InlineShapes(i)
            t = sh.Range.Paragraphs(1).Range.Text[:40].replace("\r", " ")
            cols = sh.Range.Sections(1).PageSetup.TextColumns.Count
            print(f"fig{i} w={sh.Width:.1f} h={sh.Height:.1f} cols={cols} para={t!r}")
        for i in range(1, doc.Paragraphs.Count + 1):
            t = doc.Paragraphs(i).Range.Text.replace("\r", "").replace("\x07", "")
            if t.startswith("Fig. 1.") or t.startswith("Fig. 2.") or t.startswith("Fig. 3."):
                print(f"cap i={i}", t[:80])
                if doc.Paragraphs(i).Range.InlineShapes.Count:
                    print("  has shape")
            if doc.Paragraphs(i).Range.InlineShapes.Count:
                print(f"shape-para i={i}", t[:40])
    finally:
        doc.Close(0)
        word.Quit()


if __name__ == "__main__":
    main()
