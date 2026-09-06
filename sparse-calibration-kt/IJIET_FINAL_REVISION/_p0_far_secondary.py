#!/usr/bin/env python3
"""P0: shrink IV.C FAR to one secondary-probe paragraph. No lock edits."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_far_sec"
WD_FORMAT_XML = 16
WD_SAVE = -1

OLD_IVC = (
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
    "ΔFAR. That interval is wide, and the sparse ECE cell is Limited "
    "(N=415); neither is a high-N finding. DKT ΔFAR is positive on only "
    "three of five runs. On XES3G5M, T-KT ΔFAR is negative on all five "
    "runs (mean −0.017). Graph and contrastive models are not scored."
)

NEW_IVC = (
    "A locked gate at τ=0.7 is a simulated next-response decision-error "
    "probe, not RQ3. On ASSISTments 2012, T-KT FAR is 0.196 on dense KCs "
    "and 0.268 on sparse KCs (ΔFAR=+0.072; seed 42) and is positive in "
    "4/4 unique learner partitions. On XES3G5M the same probe is negative. "
    "The τ-grid, occupancy-policy counterfactual, denominators, and seed "
    "tables are Supplementary Tables S3–S6."
)

OLD_VA = (
    "Third, threshold behavior can differ by frequency stratum. The "
    "simulated ASSISTments gate (Supplementary Tables S5–S6) can raise "
    "T-KT FAR on sparse KCs relative to dense KCs, with ΔFAR positive in "
    "4/4 unique learner partitions (and in 5/5 training runs, two of which "
    "share a split); on XES3G5M, T-KT ΔFAR and ΔMiss are both negative "
    "after padding is excluded, so a flat ECE is not by itself a "
    "decision-error result."
)

NEW_VA = (
    "Third, a simulated next-response decision-error probe can differ by "
    "frequency stratum: ASSISTments T-KT ΔFAR is positive in 4/4 unique "
    "partitions, and the XES3G5M probe is negative (Supplementary Tables "
    "S5–S6)."
)


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
        log.append(f"repl {old[:40]!r} n={n}")
        if n != 1:
            raise SystemExit(f"expected 1 hit for {old[:50]!r}, got {n}")


def delete_efar(doc, log) -> None:
    for i in range(doc.Paragraphs.Count, 0, -1):
        t = para_text(doc.Paragraphs(i))
        if t.startswith("T-KT dense E[FAR]"):
            doc.Paragraphs(i).Range.Delete()
            log.append("deleted E[FAR] vs ECE sentence")
            return
    raise SystemExit("E[FAR] sentence not found")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["far_secondary"]
    try:
        apply_pairs(doc, [(OLD_IVC, NEW_IVC), (OLD_VA, NEW_VA)], log)
        delete_efar(doc, log)
        body = doc.Content.Text or ""
        if "Nadvance=284,326" in body:
            raise SystemExit("seed-42 denominator dump remains")
        if "next-response decision-error probe" not in body:
            raise SystemExit("probe wording missing")
        if "mastery outcome" in body.lower():
            raise SystemExit("mastery outcome appeared")
        if "0.196" not in body or "0.268" not in body:
            raise SystemExit("FAR locks missing")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        if "ΔFAR=+0.072" not in body and "ΔFAR=+0.072" not in body.replace("\u0394", "Δ"):
            if "+0.072" not in body:
                raise SystemExit("ΔFAR=+0.072 missing")
        if "not RQ3" not in body:
            raise SystemExit("not RQ3 missing")
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
