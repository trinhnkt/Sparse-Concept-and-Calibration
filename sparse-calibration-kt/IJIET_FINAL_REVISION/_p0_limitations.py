#!/usr/bin/env python3
"""P0: clean Limitations; drop NOT RECOVERED; keep listed caveats."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_limitations"
WD_FORMAT_XML = 16
WD_SAVE = -1

NEW = (
    "Next-response correctness is not latent mastery: y=0 is an incorrect "
    "next attempt, not a latent-skill diagnosis. The threshold gate is a "
    "simulated probe, not a classroom policy. There is no classroom RCT. "
    "We do not train graph, contrastive, or self-supervised KT models. "
    "BKT is not a scored baseline; IRT is the classical reference "
    "(pyBKT 1.4.1 degenerated on ASSISTments seed 42; Supplementary "
    "Table S9). T-KT is a local Transformer implementation, not published "
    "SimpleKT [4]; official SimpleKT is scored on ASSISTments AUC/ECE "
    "only. Temporal evaluation uses a single corrected cutoff (seed 42). "
    "Seeds 2025 and 2026 share a split. R/L/I are descriptive support "
    "flags. ECE depends on binning. Three datasets cannot establish a "
    "universal diagnostic law. The reported diagnostics are reproduced "
    "from the frozen review artifact (code_for_review_anonymous.zip) and "
    "configuration; locked tables rebuild from frozen summaries "
    "(scripts/rebuild_locked_tables.sh)."
)


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
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text or ""
            if text.startswith("Next-response correctness is not latent mastery"):
                if NEW in text:
                    n = 1
                else:
                    inner.Text = NEW
                    n += 1
        if n != 1:
            raise SystemExit(f"limitations hits={n}")
        body = doc.Content.Text or ""
        lim = ""
        for i in range(1, doc.Paragraphs.Count + 1):
            t = doc.Range(
                doc.Paragraphs(i).Range.Start, doc.Paragraphs(i).Range.End - 1
            ).Text or ""
            if t.startswith("Next-response correctness is not latent mastery"):
                lim = t
                break
        must = [
            "not latent mastery",
            "Three datasets",
            "ECE depends on binning",
            "descriptive support flags",
            "single corrected cutoff",
            "2025 and 2026 share a split",
            "pyBKT 1.4.1 degenerated",
            "local Transformer implementation",
            "code_for_review_anonymous.zip",
        ]
        missing = [m for m in must if m not in lim]
        if missing:
            raise SystemExit(f"limitations missing {missing}")
        if "NOT RECOVERED" in lim:
            raise SystemExit("NOT RECOVERED still in Limitations")
        if "not byte-identical to a recovered pyKT" in lim:
            raise SystemExit("unrecovered-image sentence still in Limitations")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        print("limitations n=1")
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
