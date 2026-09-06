#!/usr/bin/env python3
"""Move FAR Tables 5–6 to SI numbering; renumber main tables; fix cold-start layout."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BACKUP = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_far_si"

WD_FORMAT_XML = 16
WD_SAVE = -1
WD_AUTOFIT_WINDOW = 2

IVC_OLD = (
    "Table 5 is a simulated gate at τ=0.7 on ASSISTments 2012 fold 0 (seed 42), "
    "reported as a decision-error probe rather than contribution (ii)."
)
IVC_NEW = (
    "A locked gate at τ=0.7 is reported only as a decision-error probe, not "
    "contribution (ii). The full seed-42 FAR cells and the four-partition "
    "robustness table are Supplementary Tables S5–S6 (τ grid and occupancy "
    "policies: S3–S4). For T-KT on ASSISTments 2012 fold 0 (seed 42), FAR is "
    "0.196 [0.186, 0.208] on dense KCs (N=528,018; Nadvance=284,326; "
    "Nincorrect=158,623; E[FAR]=0.113; Excess FAR=0.083; Miss=0.352) and "
    "0.268 [0.202, 0.337] on sparse KCs (N=444, Limited; Nadvance=235; "
    "Nincorrect=197; E[FAR]=0.050; Excess FAR=0.218; Miss=0.320). "
    "ΔFAR=+0.072. DKT FAR is 0.200 [0.190, 0.211] dense and 0.296 [0.221, "
    "0.383] sparse. Sparse T-KT FAR uses Limited occupancy (Nadvance=235). "
    "ΔFAR is positive in 4/4 unique partition-level estimates "
    "(partition-level mean 0.056, range 0.015–0.087) and in 5/5 training "
    "runs (mean 0.047, sd 0.033; two runs share a split). Mean sparse "
    "denominators are N=413, Nadvance=227, Nincorrect=155. A KC-clustered "
    "bootstrap on seed 42 yields a 95% interval [0.006, 0.138] for T-KT "
    "ΔFAR. DKT ΔFAR is positive on only three of five runs. On XES3G5M, "
    "T-KT ΔFAR is negative on all five runs (mean −0.017). Graph and "
    "contrastive models are not scored."
)

PAIRS_EARLY = [
    (
        "Tables 5–6 use one locked global τ=0.7",
        "Supplementary Tables S5–S6 use one locked global τ=0.7",
    ),
    (
        "report FAR with its denominators (Tables 5–6; Supplementary Tables S3–S4)",
        "report FAR with its denominators (Supplementary Tables S3–S6)",
    ),
    (
        "The simulated ASSISTments gate (Tables 5–6) can raise",
        "The simulated ASSISTments gate (Supplementary Tables S5–S6) can raise",
    ),
    (
        "(Supplementary Tables S3–S4), not as the primary contribution",
        "(Supplementary Tables S3–S6), not as the primary contribution",
    ),
    (
        "empty (Table 7)",
        "empty under the pre-specified cuts",
    ),
    (
        "Table 9 records a seven-channel leakage audit",
        "Table 3 records a seven-channel leakage audit",
    ),
]

# After FAR tables are gone. Specific captions first.
RENUMBER = [
    ("Table 11. Cold-start", "Table 9. Cold-start"),
    ("Table 11 reports feasibility", "Table 9 reports feasibility"),
    ("Table 10. Four-partition Brier", "Table 6. Four-partition Brier"),
    (
        "Table 9. Seven-channel leakage checklist",
        "Table 3. Seven-channel leakage checklist",
    ),
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
    ("same aggregation and M = 15", "same aggregation and M = 15"),  # no-op guard
]


def para_text(para) -> str:
    return para.Range.Text.replace("\r", "").replace("\x07", "")


def set_inner(doc, para, text: str) -> None:
    inner = doc.Range(para.Range.Start, para.Range.End - 1)
    inner.Text = text


def apply_pairs(doc, pairs: list[tuple[str, str]], log: list[str], tag: str) -> None:
    for old, new in pairs:
        if old == new:
            continue
        n = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text
            if old in text:
                inner.Text = text.replace(old, new)
                n += 1
        log.append(f"{tag} {old[:40]!r} -> {n}")


def delete_caption_and_table(doc, caption_start: str, log: list[str]) -> None:
    found = False
    for t in range(doc.Tables.Count, 0, -1):
        tbl = doc.Tables(t)
        start = tbl.Range.Start
        if start < 2:
            continue
        prev = doc.Range(max(0, start - 400), start)
        ptxt = prev.Text.replace("\r", " ").replace("\x07", " ")
        if caption_start not in ptxt:
            continue
        # delete caption paragraph immediately before table
        cap = doc.Range(tbl.Range.Start - 1, tbl.Range.Start).Paragraphs(1)
        cap_t = para_text(cap)
        tbl.Delete()
        if caption_start[:20] in cap_t:
            cap.Range.Delete()
        found = True
        log.append(f"deleted table+cap {caption_start[:40]!r}")
        break
    if not found:
        raise SystemExit(f"table not found for {caption_start!r}")


def delete_para_startswith(doc, start: str, log: list[str]) -> None:
    for i in range(doc.Paragraphs.Count, 0, -1):
        if para_text(doc.Paragraphs(i)).startswith(start):
            doc.Paragraphs(i).Range.Delete()
            log.append(f"deleted para {start[:40]!r}")
            return


def fix_coldstart_table(doc, log: list[str]) -> None:
    for t in range(1, doc.Tables.Count + 1):
        tbl = doc.Tables(t)
        try:
            h = tbl.Cell(1, 1).Range.Text.replace("\r", " ").replace("\x07", " ")
        except Exception:
            continue
        if "Dataset" not in h and "DATASET" not in h.upper():
            continue
        if tbl.Columns.Count < 6:
            continue
        # header + short cells
        headers = ["Dataset", "Slice", "Mean N", "Flag", "T-KT ECE", "DKT ECE"]
        for c, val in enumerate(headers, 1):
            cell = tbl.Cell(1, c)
            cell.Range.Text = val
            cell.Range.Font.AllCaps = False
            cell.Range.Font.Name = "Times New Roman"
            cell.Range.Font.Size = 7
            cell.Range.Font.Bold = True
        # body: force sentence case labels already in cells
        for r in range(2, tbl.Rows.Count + 1):
            for c in range(1, tbl.Columns.Count + 1):
                cell = tbl.Cell(r, c)
                raw = cell.Range.Text.replace("\r", "").replace("\x07", "").strip()
                low = raw.lower().replace("\n", " ")
                if "descripti" in low:
                    raw = "descr."
                elif "assistme" in low:
                    raw = "ASSISTments"
                elif "very-spar" in low or "very spar" in low:
                    raw = "very-sparse"
                elif "strict" in low and "f=0" in low.replace(" ", ""):
                    raw = "strict f=0"
                elif "strict" in low and "sparse" in low:
                    raw = "strict / sparse"
                cell.Range.Text = raw
                cell.Range.Font.AllCaps = False
                cell.Range.Font.Name = "Times New Roman"
                cell.Range.Font.Size = 7
                cell.Range.Font.Bold = False
        try:
            tbl.AutoFitBehavior(WD_AUTOFIT_WINDOW)
        except Exception:
            pass
        log.append(f"coldstart table t={t} rows={tbl.Rows.Count}")
        return
    raise SystemExit("cold-start table not found")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.copy2(FULL, BACKUP)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["far_si_renumber"]
    try:
        apply_pairs(doc, PAIRS_EARLY, log, "early")
        # rewrite IV.C lead
        n = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            try:
                if para.Range.Tables.Count:
                    continue
            except Exception:
                pass
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            if IVC_OLD in inner.Text:
                inner.Text = IVC_NEW
                n += 1
                log.append(f"ivc i={i}")
        if n != 1:
            raise SystemExit(f"IV.C replacements={n}")

        delete_para_startswith(doc, "Table 6 checks whether", log)
        delete_para_startswith(doc, "Seed-42 ΔFAR 95% CI", log)
        delete_caption_and_table(doc, "Table 5. Simulated gate", log)
        delete_caption_and_table(doc, "Table 6. Gate robustness", log)

        apply_pairs(doc, RENUMBER, log, "renum")
        fix_coldstart_table(doc, log)

        body = doc.Content.Text or ""
        if "Table 5. Simulated gate" in body or "Table 6. Gate robustness" in body:
            raise SystemExit("FAR tables still in main")
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
            raise SystemExit("0.056 missing from main")
        if "TSCDA" in body:
            raise SystemExit("TSCDA returned")
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
