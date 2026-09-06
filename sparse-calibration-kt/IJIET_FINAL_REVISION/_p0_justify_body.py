#!/usr/bin/env python3
"""Restore IJIET body justify on leftover Normal paragraphs. No numeric edits."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_justify"
WD_ALIGN_JUSTIFY = 3
WD_SAVE = -1
FIRST = 10.1


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    n = 0
    try:
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs(i)
            if p.Range.Tables.Count:
                continue
            if p.Style.NameLocal != "Normal":
                continue
            t = p.Range.Text.replace("\r", "").replace("\x07", "").strip()
            if len(t) < 40:
                continue
            if int(p.Format.Alignment) == WD_ALIGN_JUSTIFY:
                continue
            p.Style = "Text"
            p.Format.Alignment = WD_ALIGN_JUSTIFY
            p.Format.FirstLineIndent = FIRST
            n += 1
            print(f"justified p{i} {t[:48]!r}")
        body = doc.Content.Text or ""
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE lock missing")
        if n < 1:
            raise SystemExit("no paragraphs changed")
        doc.Save()
        print(f"saved n={n}")
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
