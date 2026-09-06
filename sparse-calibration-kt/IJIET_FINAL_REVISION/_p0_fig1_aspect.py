#!/usr/bin/env python3
"""Force Fig. 1 to 501.8 pt width with PNG aspect (809x156)."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
WD_FORMAT_XML = 16
WD_SAVE = -1
WD_ALIGN_CENTER = 1
W = 501.8
H = 501.8 * 156 / 809


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    try:
        fig1 = doc.InlineShapes(1)
        fig1.LockAspectRatio = False
        fig1.Width = W
        fig1.Height = H
        fig1.LockAspectRatio = True
        try:
            fig1.Range.Paragraphs(1).Alignment = WD_ALIGN_CENTER
        except Exception:
            pass
        if abs(fig1.Width - W) > 1 or fig1.Height < 90:
            raise SystemExit(f"fig1 {fig1.Width:.1f}x{fig1.Height:.1f}")
        print(f"fig1 {fig1.Width:.1f}x{fig1.Height:.1f}")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
