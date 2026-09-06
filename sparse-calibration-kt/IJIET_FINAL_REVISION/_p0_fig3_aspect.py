#!/usr/bin/env python3
"""Force Fig. 3 to 501.8 pt width with previous 480x445.5 aspect."""
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
H = 501.8 * 445.5 / 480.0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    try:
        fig3 = doc.InlineShapes(3)
        fig3.LockAspectRatio = False
        fig3.Width = W
        fig3.Height = H
        fig3.LockAspectRatio = True
        try:
            fig3.Range.Paragraphs(1).Alignment = WD_ALIGN_CENTER
        except Exception:
            pass
        if abs(fig3.Width - W) > 1 or fig3.Height < 450:
            raise SystemExit(f"fig3 {fig3.Width:.1f}x{fig3.Height:.1f}")
        print(f"fig3 {fig3.Width:.1f}x{fig3.Height:.1f}")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
