#!/usr/bin/env python3
"""P0 polish: Fig. 3 → 501.8 pt; Table 8 section rows as one compact span."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_fig3_t8"
WD_FORMAT_XML = 16
WD_SAVE = -1
WD_ALIGN_CENTER = 1
WD_ALIGN_LEFT = 0
FIG_W = 501.8

LOCKS = ("0.1136", "0.2280", "0.1176", "0.1254", "18.9%", "1,969")


def cell_text(cell) -> str:
    return " ".join((cell.Range.Text or "").replace("\r", " ").replace("\x07", " ").split())


def find_t8(doc):
    for i in range(1, doc.Tables.Count + 1):
        tbl = doc.Tables(i)
        if tbl.Rows.Count < 8 or tbl.Columns.Count < 4:
            continue
        if cell_text(tbl.Cell(1, 1)) == "Condition" and "ASSISTments" in cell_text(tbl.Cell(1, 2)):
            return tbl
    raise SystemExit("Table 8 not found")


def compact_section_row(tbl, r: int, label: str) -> None:
    try:
        tbl.Cell(r, 1).Merge(tbl.Cell(r, tbl.Columns.Count))
    except Exception:
        pass
    rng = tbl.Cell(r, 1).Range
    rng.Text = label + "\r"
    rng.Font.Name = "Times New Roman"
    rng.Font.Size = 7
    rng.Font.Bold = True
    rng.Font.Italic = True
    pf = rng.ParagraphFormat
    pf.Alignment = WD_ALIGN_LEFT
    pf.SpaceBefore = 0
    pf.SpaceAfter = 0
    try:
        tbl.Rows(r).HeightRule = 0
    except Exception:
        pass


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    try:
        if doc.InlineShapes.Count < 3:
            raise SystemExit(f"figs={doc.InlineShapes.Count}")
        fig3 = doc.InlineShapes(3)
        old_w, old_h = float(fig3.Width), float(fig3.Height)
        fig3.LockAspectRatio = True
        fig3.Width = FIG_W
        try:
            fig3.Range.Paragraphs(1).Alignment = WD_ALIGN_CENTER
        except Exception:
            pass
        if fig3.Width < 500:
            raise SystemExit(f"fig3 still narrow {fig3.Width}")
        print(f"fig3 {old_w:.1f}x{old_h:.1f} -> {fig3.Width:.1f}x{fig3.Height:.1f}")

        tbl = find_t8(doc)
        compact_section_row(tbl, 2, "A. Estimability")
        compact_section_row(tbl, 5, "B. Observed pattern/context")
        body = doc.Content.Text or ""
        for tok in LOCKS:
            if tok not in body:
                raise SystemExit(f"lock missing {tok}")
        if "18.9%" not in cell_text(tbl.Cell(3, 2)):
            raise SystemExit("E1 Assist cell changed")
        if "0.114" not in cell_text(tbl.Cell(9, 2)) or "0.228" not in cell_text(tbl.Cell(9, 2)):
            raise SystemExit("T-KT ECE Assist cell changed")
        if "0.1176" not in cell_text(tbl.Cell(9, 4)):
            raise SystemExit("XES ECE cell changed")
        print("t8 section rows compacted")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
