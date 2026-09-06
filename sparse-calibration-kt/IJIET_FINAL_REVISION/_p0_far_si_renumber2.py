#!/usr/bin/env python3
"""Finish FAR-to-SI: delete leftover robustness table, renumber, fix cold-start."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
WD_FORMAT_XML = 16
WD_SAVE = -1
WD_AUTOFIT_WINDOW = 2

RENUMBER = [
    ("Table 11. Cold-start", "Table 9. Cold-start"),
    ("Table 11 reports feasibility", "Table 9 reports feasibility"),
    ("Table 10. Four-partition Brier", "Table 6. Four-partition Brier"),
    (
        "Table 9. Seven-channel leakage checklist",
        "Table 3. Seven-channel leakage checklist",
    ),
    ("Table 9 records a seven-channel leakage audit", "Table 3 records a seven-channel leakage audit"),
    ("Table 3. Overall learner-based", "Table 4. Overall learner-based"),
    ("Table 3 reports overall learner-based", "Table 4 reports overall learner-based"),
    ("Table 3 may suffice", "Table 4 may suffice"),
    ("Table 3 is an insufficient evaluation", "Table 4 is an insufficient evaluation"),
    ("Table 4 reports event-level expected", "Table 5 reports event-level expected"),
    (
        "Table 4. T-KT event-level expected calibration error",
        "Table 5. T-KT event-level expected calibration error",
    ),
    ("Table 4, N=415", "Table 5, N=415"),
]


def para_text(para) -> str:
    return para.Range.Text.replace("\r", "").replace("\x07", "")


def apply_pairs(doc, pairs, log) -> None:
    for old, new in pairs:
        n = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text
            if old in text:
                inner.Text = text.replace(old, new)
                n += 1
        log.append(f"renum {old[:42]!r} n={n}")


def delete_robustness(doc, log) -> None:
    for t in range(doc.Tables.Count, 0, -1):
        tbl = doc.Tables(t)
        if tbl.Rows.Count != 3 or tbl.Columns.Count != 7:
            continue
        h = tbl.Cell(1, 1).Range.Text.replace("\r", "").replace("\x07", "").strip()
        if h != "Model":
            continue
        # delete long caption paragraph(s) immediately before
        cap = doc.Range(tbl.Range.Start - 1, tbl.Range.Start).Paragraphs(1)
        cap_t = para_text(cap)
        tbl.Delete()
        if "Gate robustness" in cap_t or "Mean N, Nadvance" in cap_t or "four unique learner" in cap_t:
            cap.Range.Delete()
        log.append(f"deleted robustness table cap={cap_t[:60]!r}")
        return
    raise SystemExit("robustness 3x7 table not found")


def delete_para_startswith(doc, start: str, log: list[str]) -> None:
    for i in range(doc.Paragraphs.Count, 0, -1):
        if para_text(doc.Paragraphs(i)).startswith(start):
            doc.Paragraphs(i).Range.Delete()
            log.append(f"deleted para {start[:40]!r}")


def fix_coldstart_table(doc, log: list[str]) -> None:
    for t in range(1, doc.Tables.Count + 1):
        tbl = doc.Tables(t)
        try:
            h = tbl.Cell(1, 1).Range.Text.replace("\r", " ").replace("\x07", " ")
        except Exception:
            continue
        if tbl.Columns.Count != 6 or tbl.Rows.Count < 4:
            continue
        # last table-ish: Dataset + Slice style
        c2 = tbl.Cell(1, 2).Range.Text.replace("\r", "").replace("\x07", "").lower()
        if "slice" not in c2 and "SLICE" not in tbl.Cell(1, 2).Range.Text:
            continue
        headers = ["Dataset", "Slice", "Mean N", "Flag", "T-KT ECE", "DKT ECE"]
        for c, val in enumerate(headers, 1):
            cell = tbl.Cell(1, c)
            cell.Range.Text = val
            cell.Range.Font.AllCaps = False
            cell.Range.Font.Name = "Times New Roman"
            cell.Range.Font.Size = 7
            cell.Range.Font.Bold = True
        for r in range(2, tbl.Rows.Count + 1):
            for c in range(1, tbl.Columns.Count + 1):
                cell = tbl.Cell(r, c)
                raw = cell.Range.Text.replace("\r", " ").replace("\x07", " ").strip()
                low = raw.lower()
                if "descripti" in low:
                    raw = "descr."
                elif "assistme" in low:
                    raw = "ASSISTments"
                elif "very-spar" in low or "very spar" in low:
                    raw = "very-sparse"
                elif "strict" in low and "sparse" in low:
                    raw = "strict / sparse"
                elif "strict" in low:
                    raw = "strict f=0"
                cell.Range.Text = raw
                cell.Range.Font.AllCaps = False
                cell.Range.Font.Name = "Times New Roman"
                cell.Range.Font.Size = 7
                cell.Range.Font.Bold = False
        try:
            tbl.AutoFitBehavior(WD_AUTOFIT_WINDOW)
        except Exception:
            pass
        log.append(f"coldstart t={t}")
        return
    raise SystemExit("cold-start table not found")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["renumber2"]
    try:
        delete_para_startswith(doc, "Table 6 checks whether", log)
        delete_para_startswith(doc, "Seed-42 ΔFAR 95% CI", log)
        delete_robustness(doc, log)
        apply_pairs(doc, RENUMBER, log)
        fix_coldstart_table(doc, log)
        body = doc.Content.Text or ""
        if "Table 6. Gate robustness" in body:
            raise SystemExit("robustness caption remains")
        if "Table 5. Simulated gate" in body:
            raise SystemExit("seed42 FAR table remains")
        if "Table 9. Seven-channel" in body:
            raise SystemExit("leakage still Table 9")
        if "Table 3. Seven-channel" not in body:
            raise SystemExit("leakage Table 3 missing")
        if "Table 9. Cold-start" not in body:
            raise SystemExit("cold-start Table 9 missing")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        if "0.196" not in body or "0.268" not in body:
            raise SystemExit("FAR locks missing")
        if "0.056" not in body:
            raise SystemExit("0.056 missing")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        print("\n".join(log))
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
