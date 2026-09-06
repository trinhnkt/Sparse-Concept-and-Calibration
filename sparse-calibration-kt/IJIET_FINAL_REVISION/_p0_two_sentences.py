#!/usr/bin/env python3
"""Fix 'an E1–E2' and Table 9 L6 caption. No numeric edits."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BACKUP = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_an"

WD_FORMAT_XML = 16
WD_SAVE = -1
EN = "\u2013"

PAIRS = [
    (
        f"it is not a E1{EN}E2 estimability criterion",
        f"it is not an E1{EN}E2 estimability criterion",
    ),
    (
        "it is not a E1-E2 estimability criterion",
        "it is not an E1-E2 estimability criterion",
    ),
    (
        "PASS means the decision is train-only or validation-only. "
        "Test is used only to report.",
        "PASS means the decision is train-only, validation-only, or a fixed "
        "training schedule (L6: final checkpoint). Test is used only to report.",
    ),
]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.copy2(FULL, BACKUP)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["an-e1e2-l6cap"]
    counts = {old: 0 for old, _ in PAIRS}
    try:
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            try:
                if para.Range.Tables.Count:
                    continue
            except Exception:
                pass
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text
            changed = False
            for old, new in PAIRS:
                if old in text:
                    text = text.replace(old, new, 1)
                    counts[old] += 1
                    changed = True
            if changed:
                inner.Text = text
                log.append(f"p{i}")
        body = doc.Content.Text or ""
        if "not a E1" in body:
            raise SystemExit("a E1 still present")
        if "train-only or validation-only" in body:
            raise SystemExit("old Table 9 caption still present")
        if "L6: final checkpoint" not in body:
            raise SystemExit("new L6 caption missing")
        if "not an E1" not in body.replace(EN, "-") and f"not an E1{EN}E2" not in body:
            raise SystemExit("an E1–E2 missing")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        log.append("counts=" + str({k[:36]: n for k, n in counts.items()}))
        if sum(counts.values()) < 2:
            raise SystemExit(f"too few hits {counts}")
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
