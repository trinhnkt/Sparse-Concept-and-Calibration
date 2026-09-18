#!/usr/bin/env python3
"""1-column continuous sections around Fig. 3 and Table 4."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_a16_double_blind import para_text  # noqa: E402
from manuscript_paths import FULL_DOCX  # noqa: E402

WD_SAVE = -1
WD_SECTION_CONTINUOUS = 3
WD_COLLAPSE_START = 1
WD_COLLAPSE_END = 0
LOG = HERE / "audit" / "wrap_fig3_onecol_log.txt"


def find_para(doc, prefix: str):
    for i in range(1, doc.Paragraphs.Count + 1):
        if para_text(doc.Paragraphs(i)).strip().startswith(prefix):
            return i, doc.Paragraphs(i)
    raise SystemExit(f"missing {prefix}")


def wrap_para_span(doc, start_i: int, end_i: int, restore_2col_prefix: str | None, log: list[str], label: str) -> None:
    start = doc.Paragraphs(start_i)
    if start.Range.Sections(1).PageSetup.TextColumns.Count == 1:
        end = doc.Paragraphs(end_i)
        if start.Range.Sections(1).Index == end.Range.Sections(1).Index:
            log.append(f"{label} already 1-col")
            return
    r0 = doc.Paragraphs(start_i).Range
    r0.Collapse(WD_COLLAPSE_START)
    r0.InsertBreak(WD_SECTION_CONTINUOUS)
    end_i += 1  # inserted para before start
    start_i += 1
    r1 = doc.Paragraphs(end_i).Range
    r1.Collapse(WD_COLLAPSE_END)
    r1.InsertBreak(WD_SECTION_CONTINUOUS)
    mid = doc.Paragraphs(start_i).Range.Sections(1)
    mid.PageSetup.TextColumns.SetCount(1)
    log.append(f"{label} sec{mid.Index} cols=1 w={mid.PageSetup.TextColumns(1).Width:.1f}")
    if restore_2col_prefix:
        j, p = find_para(doc, restore_2col_prefix)
        sec = p.Range.Sections(1)
        if sec.PageSetup.TextColumns.Count < 2:
            sec.PageSetup.TextColumns.SetCount(2)
            sec.PageSetup.TextColumns.Spacing = 14.4
            log.append(f"restore 2-col at {restore_2col_prefix!r} sec{sec.Index}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log: list[str] = []
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL_DOCX))
    try:
        cap_i, cap = find_para(doc, "Fig. 3.")
        pict_i = cap_i - 1
        wrap_para_span(doc, pict_i, cap_i, "D. Diagnostic conditions", log, "Fig. 3")

        t4_i, t4 = find_para(doc, "Table 4.")
        if t4.Range.Sections(1).PageSetup.TextColumns.Count != 1:
            tbl = None
            for ti in range(1, doc.Tables.Count + 1):
                t = doc.Tables(ti)
                if t.Range.Start >= t4.Range.Start:
                    tbl = t
                    break
            if tbl is None:
                raise SystemExit("Table 4 body missing")
            r0 = t4.Range
            r0.Collapse(WD_COLLAPSE_START)
            r0.InsertBreak(WD_SECTION_CONTINUOUS)
            t4_i, t4 = find_para(doc, "Table 4.")
            tbl = None
            for ti in range(1, doc.Tables.Count + 1):
                t = doc.Tables(ti)
                if t.Range.Start >= t4.Range.Start:
                    tbl = t
                    break
            r1 = tbl.Range
            r1.Collapse(WD_COLLAPSE_END)
            r1.InsertBreak(WD_SECTION_CONTINUOUS)
            t4_i, t4 = find_para(doc, "Table 4.")
            t4.Range.Sections(1).PageSetup.TextColumns.SetCount(1)
            _, bhead = find_para(doc, "B. Calibration across frequency")
            if bhead.Range.Sections(1).PageSetup.TextColumns.Count < 2:
                bhead.Range.Sections(1).PageSetup.TextColumns.SetCount(2)
                bhead.Range.Sections(1).PageSetup.TextColumns.Spacing = 14.4
            log.append("Table 4 1-col wrap")
        else:
            log.append("Table 4 already 1-col")

        _, cap = find_para(doc, "Fig. 3.")
        cap.Previous.KeepWithNext = True
        cap.KeepWithNext = False
        pages = doc.ComputeStatistics(2)
        log.append(f"pages={pages}")
        if not (8 <= pages <= 14):
            raise SystemExit(f"pages {pages}")
        doc.Save()
    finally:
        doc.Close(WD_SAVE)
        word.Quit()
    LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
