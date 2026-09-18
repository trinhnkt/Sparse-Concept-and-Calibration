#!/usr/bin/env python3
"""Center tables, compact cell padding, cap over-tall figures. No cell-text edits."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_a16_double_blind import para_text  # noqa: E402
from manuscript_paths import FULL_DOCX  # noqa: E402

WD_SAVE = -1
WD_ALIGN_ROW_CENTER = 1
WD_CELL_ALIGN_CENTER = 1
WD_LINE_STYLE_SINGLE = 1
WD_LINE_WIDTH_075PT = 6  # 0.75 pt; template tables used 1pt=8
MAX_FIG_HEIGHT_PT = 268.0  # ~9.4 cm so a 1-col figure leaves room for caption+text
LOG = HERE / "audit" / "polish_layout_com_log.txt"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log: list[str] = []
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL_DOCX))
    try:
        for ti in range(1, doc.Tables.Count + 1):
            tbl = doc.Tables(ti)
            try:
                tbl.Rows.Alignment = WD_ALIGN_ROW_CENTER
            except Exception:
                pass
            tbl.TopPadding = 1.5
            tbl.BottomPadding = 1.5
            tbl.LeftPadding = 4.0
            tbl.RightPadding = 4.0
            try:
                tbl.Range.Cells.VerticalAlignment = WD_CELL_ALIGN_CENTER
            except Exception:
                pass
            for r in range(1, tbl.Rows.Count + 1):
                pf = tbl.Rows(r).Range.ParagraphFormat
                pf.KeepWithNext = False
                pf.SpaceBefore = 0
                pf.SpaceAfter = 0
            log.append(f"T{ti} centered {tbl.Rows.Count}x{tbl.Columns.Count}")

        n_fig = 0
        for i in range(1, doc.InlineShapes.Count + 1):
            sh = doc.InlineShapes(i)
            h = float(sh.Height)
            w = float(sh.Width)
            if h > MAX_FIG_HEIGHT_PT:
                scale = MAX_FIG_HEIGHT_PT / h
                sh.Height = MAX_FIG_HEIGHT_PT
                sh.Width = w * scale
                log.append(f"fig{i} {h:.1f}->{MAX_FIG_HEIGHT_PT:.1f}pt w={sh.Width:.1f}")
                n_fig += 1
            else:
                log.append(f"fig{i} keep h={h:.1f} w={w:.1f}")
        log.append(f"scaled={n_fig}")

        for i in range(1, doc.Paragraphs.Count + 1):
            t = para_text(doc.Paragraphs(i)).strip()
            if t.startswith("Table ") or t.startswith("Fig. "):
                p = doc.Paragraphs(i)
                p.Alignment = 1
                p.Format.FirstLineIndent = 0
                p.Format.SpaceBefore = 4
                p.Format.SpaceAfter = 2
                if t.startswith("Table 5.") or t.startswith("Table 6."):
                    p.KeepWithNext = True

        pages = doc.ComputeStatistics(2)
        log.append(f"pages_word={pages}")
        if not (8 <= pages <= 14):
            raise SystemExit(f"page count {pages}")
        doc.Save()
        log.append("saved")
    finally:
        doc.Close(WD_SAVE)
        word.Quit()
    LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
