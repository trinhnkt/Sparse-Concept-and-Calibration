#!/usr/bin/env python3
"""P0: lock Contributions to protocol / calibration / artefact. No C1–C3 tokens."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_contrib3"
WD_FORMAT_XML = 16
WD_SAVE = -1

OLD = (
    "Contributions are conservative: (i) a reproducible evaluation protocol "
    "for KT under learner-based, temporal, and cold-start-concept views, "
    "with train-only KC-frequency strata (including a strict f=0 bin) and a "
    "seven-channel leakage checklist covering split, preprocessing, Q-matrix "
    "mapping, sparse-bucket assignment, calibration parameters, "
    "hyperparameter selection, and cold-start definition; (ii) calibration "
    "diagnostics per KC stratum using 15-bin ECE, Brier score, Murphy "
    "decomposition (UNC − RES + REL), and reliability diagrams—under our "
    "experimental conditions, dense and sparse calibration profiles differ "
    "on some logs, and overall-AUC rankings may differ from sparse-stratum "
    "calibration; (iii) review scripts and tables so the protocol can be "
    "re-run without redefining buckets. We do not propose a new KT "
    "architecture, a new calibration algorithm, or a classroom intervention. "
    "Graph and contrastive KT models are out of scope and are not scored."
)

NEW = (
    "Contributions are conservative: (i) a train-only sparse-concept "
    "evaluation protocol combining learner-based and temporal views, "
    "explicit cold-start definitions, occupancy-aware reporting, and L1–L7 "
    "leakage control; (ii) per-stratum calibration diagnostics using ECE, "
    "Brier decomposition, and reliability diagrams, showing "
    "dataset-dependent rather than universal sparse-calibration "
    "vulnerability; (iii) a reproducibility artifact with frozen scripts "
    "and configuration and a one-command rebuild of the diagnostic tables "
    "from frozen summaries. We do not propose a new KT architecture, a new "
    "calibration algorithm, or a classroom intervention. Graph and "
    "contrastive KT models are out of scope and are not scored."
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
        contrib = ""
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text or ""
            if NEW in text:
                n = 1
                contrib = text
                continue
            if OLD in text:
                inner.Text = text.replace(OLD, NEW)
                n += 1
                contrib = NEW
        if n != 1:
            raise SystemExit(f"contrib hits={n}")
        if "occupancy-aware reporting" not in contrib:
            raise SystemExit("C1 occupancy missing")
        if "dataset-dependent rather than universal" not in contrib:
            raise SystemExit("C2 dataset-dependent missing")
        if "reproducibility artifact" not in contrib:
            raise SystemExit("C3 artifact missing")
        if "FAR" in contrib or "regression" in contrib.lower() or "sparsification" in contrib:
            raise SystemExit("supporting analysis entered contributions")
        if "C1" in contrib or "C2" in contrib or "C3" in contrib:
            raise SystemExit("C1–C3 tokens in contributions")
        body = doc.Content.Text or ""
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        print("contrib3 n=1")
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
