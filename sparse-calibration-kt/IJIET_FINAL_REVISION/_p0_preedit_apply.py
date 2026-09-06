#!/usr/bin/env python3
"""Apply pre-edit recommended fixes. No numeric lock edits. No retrain."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_preedit"

WD_FORMAT_XML = 16
WD_SAVE = -1
WD_ALIGN_CENTER = 1
FIG_W = 501.8
FIG_H = 501.8 * 589 / 1650

PAIRS = [
    (
        "evaluation protocol that combines learner-based primary reporting "
        "with a complementary temporal split,",
        "evaluation protocol that uses learner-based primary reporting "
        "(the complementary temporal split is leakage-audited in "
        "Supplementary Table S10),",
    ),
    (
        "evaluation protocol with learner-based primary reporting and a "
        "complementary temporal split,",
        "evaluation protocol with learner-based primary reporting "
        "(temporal split: leakage audit only, Supplementary Table S10),",
    ),
    (
        "XES3G5M T-KT ECE cells in the main text use the masked series "
        "0.1176 / 0.1129 / 0.1254; Brier rows below are the same "
        "four-partition aggregation as Supplementary Table S1.",
        "Full Brier, UNC, REL, and RES grids, including XES3G5M, are in "
        "Supplementary Table S1.",
    ),
]


def cell_text(cell) -> str:
    return " ".join(
        (cell.Range.Text or "").replace("\r", " ").replace("\x07", " ").split()
    )


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    log: list[str] = ["preedit"]
    try:
        # P01: strip auto list label from IV.E heading (prints as "A. E.")
        p01 = 0
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            try:
                if para.Range.Tables.Count:
                    continue
            except Exception:
                pass
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = (inner.Text or "").strip()
            if text != "E. Secondary explanatory analysis":
                continue
            try:
                lf = para.Range.ListFormat
                log.append(
                    f"p01_before list={lf.ListType} lev={lf.ListLevelNumber} "
                    f"str={lf.ListString!r}"
                )
                lf.RemoveNumbers()
            except Exception as exc:
                log.append(f"p01_list_err {exc}")
            # keep typed "E." only
            inner.Text = "E. Secondary explanatory analysis"
            try:
                para.Style = "Heading 2"
            except Exception:
                pass
            p01 += 1
        log.append(f"p01_headings={p01}")
        if p01 != 1:
            raise SystemExit(f"P01 heading hits={p01}")

        # P07 + P11 text replacements (skip table body cells except captions)
        counts = {old: 0 for old, _ in PAIRS}
        for i in range(1, doc.Paragraphs.Count + 1):
            para = doc.Paragraphs(i)
            inner = doc.Range(para.Range.Start, para.Range.End - 1)
            text = inner.Text or ""
            changed = False
            for old, new in PAIRS:
                if old in text:
                    text = text.replace(old, new, 1)
                    counts[old] += 1
                    changed = True
            if changed:
                inner.Text = text
                log.append(f"p{i}")
        missing = [old[:48] for old, n in counts.items() if n != 1]
        if missing:
            raise SystemExit(f"pair counts {counts}")

        # P09 Fig. 1 native PNG aspect 809x497
        fig1 = doc.InlineShapes(1)
        fig1.LockAspectRatio = False
        fig1.Width = FIG_W
        fig1.Height = FIG_H
        fig1.LockAspectRatio = True
        try:
            fig1.Range.Paragraphs(1).Alignment = WD_ALIGN_CENTER
        except Exception:
            pass
        log.append(f"fig1 {fig1.Width:.1f}x{fig1.Height:.1f}")
        if abs(fig1.Width - FIG_W) > 1.5 or abs(fig1.Height - FIG_H) > 3:
            raise SystemExit(f"fig1 size {fig1.Width:.1f}x{fig1.Height:.1f}")

        body = doc.Content.Text or ""
        if "with a complementary temporal split" in body:
            raise SystemExit("P07 old temporal clause remains")
        if "Supplementary Table S10" not in body:
            raise SystemExit("P07 S10 pointer missing")
        if "Brier rows below are the same" in body:
            raise SystemExit("P11 old Table 6 XES clause remains")
        if "0.1136" not in body or "0.2280" not in body:
            raise SystemExit("ECE locks missing")
        if "0.1176" not in body or "0.1254" not in body:
            raise SystemExit("XES ECE locks missing")
        if "0.196" not in body or "0.268" not in body:
            raise SystemExit("FAR locks missing")
        if "E. Secondary explanatory analysis" not in body:
            raise SystemExit("IV.E heading missing")
        if "F. Secondary decision-error probe" not in body:
            raise SystemExit("IV.F heading missing")
        doc.SaveAs2(str(FULL), WD_FORMAT_XML)
        print("\n".join(log))
        print("counts=" + str({k[:36]: n for k, n in counts.items()}))
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
