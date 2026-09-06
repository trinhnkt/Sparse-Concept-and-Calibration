#!/usr/bin/env python3
"""Restore named Word, pull Fig. 1 out of Table 3, restyle Table 3."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_a16_double_blind import para_text  # noqa: E402
from manuscript_paths import FULL_DOCX  # noqa: E402

BAK = HERE / "manuscript" / (
    "Reproducible Sparse-Concept and Calibration Diagnostics "
    "for Knowledge Tracing.docx.bak_pre_p0_t3fix"
)
FIG = HERE / "figures" / "fig1_pipeline.png"
CAP1 = (
    "Fig. 1. Reproducible sparse-concept and calibration diagnostic pipeline. "
    "Tags L1–L7 match Table 3 (L5: no test-fit map; L6: final checkpoint; "
    "L7: f_train=0). Not a new KT architecture."
)

WD_FORMAT_XML = 16
WD_ALIGN_CENTER = 1
WD_ALIGN_LEFT = 0
WD_COLLAPSE_END = 0
WD_COLLAPSE_START = 1
WD_LINE_SINGLE = 1
WD_LINE_NONE = 0
WD_BORDER_TOP = 1
WD_BORDER_BOTTOM = 3
WD_WIDTH_075 = 6
WD_WIDTH_150 = 12
WD_PERCENT = 2
FIG_W = 501.8
LOCKS = ("0.1136", "0.2280", "0.1176", "0.1254", "0.196", "0.268")
ROW_LOCKS = (
    "L1 Split",
    "L2 Preprocess",
    "L3 Q-matrix",
    "L4 Bucket",
    "L5 Calibration",
    "L6 Hyperparam.",
    "L7 Cold-start",
)
HEADER = ("Channel", "Decision", "Assist.", "Junyi", "XES3G5M")


def cell_text(cell) -> str:
    return (cell.Range.Text or "").replace("\r", " ").replace("\x07", "").strip()


def set_cell(doc, cell, text: str) -> None:
    while cell.Range.InlineShapes.Count:
        cell.Range.InlineShapes(1).Delete()
    inner = doc.Range(cell.Range.Start, cell.Range.End - 1)
    inner.Text = text


def find_table3(doc):
    for ti in range(1, doc.Tables.Count + 1):
        tbl = doc.Tables(ti)
        if tbl.Rows.Count != 8 or tbl.Columns.Count != 5:
            continue
        blob = " ".join(cell_text(tbl.Cell(r, 1)) for r in range(1, 9))
        if "L1 Split" in blob and "L7 Cold-start" in blob:
            return tbl
    raise SystemExit("Table 3 not found")


def style_caption(rng) -> None:
    try:
        rng.Style = "figure caption"
    except Exception:
        pass
    rng.Font.Name = "Times New Roman"
    rng.Font.Size = 8
    rng.Font.Bold = False
    rng.Font.Italic = False
    pf = rng.ParagraphFormat
    pf.Alignment = WD_ALIGN_CENTER
    pf.SpaceBefore = 3
    pf.SpaceAfter = 8
    pf.KeepWithNext = False


def style_table(tbl) -> None:
    tbl.AllowAutoFit = False
    try:
        tbl.Rows.WrapAroundText = False
    except Exception:
        pass
    tbl.PreferredWidthType = WD_PERCENT
    tbl.PreferredWidth = 100
    for ci, w in enumerate((88, 128, 92, 104, 90), 1):
        tbl.Columns(ci).PreferredWidthType = 3
        tbl.Columns(ci).PreferredWidth = w
    for b in (1, 2, 3, 4, 8, 9):
        try:
            tbl.Borders(b).LineStyle = WD_LINE_NONE
        except Exception:
            pass
    tbl.Borders(WD_BORDER_TOP).LineStyle = WD_LINE_SINGLE
    tbl.Borders(WD_BORDER_TOP).LineWidth = WD_WIDTH_150
    tbl.Borders(WD_BORDER_TOP).Color = 0
    tbl.Borders(WD_BORDER_BOTTOM).LineStyle = WD_LINE_SINGLE
    tbl.Borders(WD_BORDER_BOTTOM).LineWidth = WD_WIDTH_150
    tbl.Borders(WD_BORDER_BOTTOM).Color = 0
    hdr = tbl.Rows(1)
    hdr.Borders(WD_BORDER_BOTTOM).LineStyle = WD_LINE_SINGLE
    hdr.Borders(WD_BORDER_BOTTOM).LineWidth = WD_WIDTH_075
    hdr.Borders(WD_BORDER_BOTTOM).Color = 0
    try:
        hdr.Shading.BackgroundPatternColor = 0xF2F2F2
    except Exception:
        pass
    for r in range(1, tbl.Rows.Count + 1):
        tbl.Rows(r).AllowBreakAcrossPages = False
        for c in range(1, tbl.Columns.Count + 1):
            cell = tbl.Cell(r, c)
            rng = cell.Range
            rng.Font.Name = "Times New Roman"
            rng.Font.Size = 7
            rng.Font.Italic = False
            rng.Font.Bold = r == 1
            cell.VerticalAlignment = 1
            pf = rng.ParagraphFormat
            pf.SpaceBefore = 1
            pf.SpaceAfter = 1
            pf.LineSpacingRule = 0
            pf.Alignment = WD_ALIGN_CENTER if c >= 3 else WD_ALIGN_LEFT
            try:
                cell.TopPadding = 1.4
                cell.BottomPadding = 1.4
                cell.LeftPadding = 3
                cell.RightPadding = 3
            except Exception:
                pass
    for c, name in enumerate(HEADER, 1):
        if cell_text(tbl.Cell(1, c)) != name:
            raise SystemExit(f"header c{c} {cell_text(tbl.Cell(1, c))!r}")
    for i, name in enumerate(ROW_LOCKS, 2):
        if cell_text(tbl.Cell(i, 1)) != name:
            raise SystemExit(f"row {i} {cell_text(tbl.Cell(i, 1))!r}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not FIG.is_file():
        raise SystemExit(f"missing {FIG}")
    if not BAK.is_file():
        raise SystemExit(f"missing {BAK}")
    shutil.copy2(BAK, FULL_DOCX)
    iw, ih = Image.open(FIG).size
    fig_h = FIG_W * ih / iw
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL_DOCX))
    saved = False
    try:
        tbl = find_table3(doc)
        for r in range(1, tbl.Rows.Count + 1):
            for c in range(1, tbl.Columns.Count + 1):
                cell = tbl.Cell(r, c)
                while cell.Range.InlineShapes.Count:
                    cell.Range.InlineShapes(1).Delete()
        set_cell(doc, tbl.Cell(1, 1), "Channel")
        cap3 = None
        for i in range(1, doc.Paragraphs.Count + 1):
            if para_text(doc.Paragraphs(i)).startswith("Table 3. Seven-channel"):
                cap3 = doc.Paragraphs(i)
                break
        if cap3 is None:
            raise SystemExit("Table 3 caption missing")
        rng = cap3.Range
        rng.Collapse(WD_COLLAPSE_START)
        rng.InsertParagraphBefore()
        pic_p = cap3.Previous()
        shp = pic_p.Range.InlineShapes.AddPicture(str(FIG))
        shp.LockAspectRatio = True
        shp.Width = FIG_W
        if abs(shp.Height - fig_h) > 8:
            shp.LockAspectRatio = False
            shp.Height = fig_h
            shp.LockAspectRatio = True
        pic_p.Alignment = WD_ALIGN_CENTER
        pic_p.Format.SpaceBefore = 6
        pic_p.Format.SpaceAfter = 2
        pic_p.Format.KeepWithNext = True
        rng = pic_p.Range
        rng.Collapse(WD_COLLAPSE_END)
        rng.InsertParagraphAfter()
        cap1 = pic_p.Next()
        inner = doc.Range(cap1.Range.Start, cap1.Range.End - 1)
        inner.Text = CAP1
        style_caption(cap1.Range)
        for i in range(doc.Paragraphs.Count, 0, -1):
            p = doc.Paragraphs(i)
            t = para_text(p)
            if (
                t.startswith("Fig. 1. Reproducible")
                and abs(p.Range.Start - cap1.Range.Start) > 2
                and p.Range.Tables.Count == 0
            ):
                p.Range.Delete()
        style_table(tbl)
        if tbl.Cell(1, 1).Range.InlineShapes.Count:
            raise SystemExit("figure still inside Table 3")
        body = doc.Content.Text or ""
        for lock in LOCKS:
            if lock not in body:
                raise SystemExit(f"missing lock {lock}")
        print(f"fig1 {shp.Width:.1f}x{shp.Height:.1f} png={iw}x{ih}")
        print("header", [cell_text(tbl.Cell(1, c)) for c in range(1, 6)])
        doc.SaveAs2(str(FULL_DOCX), WD_FORMAT_XML)
        saved = True
    finally:
        try:
            doc.Close(0)
        except Exception:
            pass
        word.Quit()
    if not saved:
        raise SystemExit("not saved")


if __name__ == "__main__":
    main()
