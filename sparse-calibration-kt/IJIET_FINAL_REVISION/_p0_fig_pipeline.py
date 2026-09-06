#!/usr/bin/env python3
"""Insert compact pipeline as Fig. 1; renumber distribution→2, reliability→3."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_a16_double_blind import para_text, set_para_text  # noqa: E402

FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_fig1"
FIG = HERE / "figures" / "fig1_pipeline.png"

WD_ALIGN_CENTER = 1
WD_SAVE = -1
COL_W = 243.65

CAP1 = (
    "Fig. 1. Reproducible sparse-concept and calibration diagnostic pipeline. "
    "Tags L1–L7 match Table 3 (L5: no test-fit map; L6: final checkpoint; "
    "L7: f_train=0). Not a new KT architecture."
)


def find_para(doc, pred) -> int:
    for i in range(1, doc.Paragraphs.Count + 1):
        if pred(para_text(doc.Paragraphs(i))):
            return i
    raise SystemExit("anchor not found")


def style_caption(rng) -> None:
    try:
        rng.Style = "figure caption"
    except Exception:
        pass
    rng.Font.Name = "Times New Roman"
    rng.Font.Size = 8
    rng.Font.Bold = False
    rng.ParagraphFormat.Alignment = WD_ALIGN_CENTER


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not FIG.is_file():
        raise SystemExit(f"missing {FIG}")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    try:
        whole = doc.Content.Text
        if "diagnostic pipeline. Tags L1" in whole:
            print("pipeline already inserted")
            return
        i_top = find_para(doc, lambda t: "Fig. 1 (top) shows" in t)
        set_para_text(
            doc.Paragraphs(i_top),
            para_text(doc.Paragraphs(i_top)).replace("Fig. 1 (top)", "Fig. 2 (top)", 1),
        )
        i_dist = find_para(doc, lambda t: t.startswith("Fig. 1. Distribution"))
        set_para_text(
            doc.Paragraphs(i_dist),
            para_text(doc.Paragraphs(i_dist)).replace("Fig. 1.", "Fig. 2.", 1),
        )
        style_caption(doc.Paragraphs(i_dist).Range)
        i_rel = find_para(doc, lambda t: t.startswith("Fig. 2. Reliability"))
        set_para_text(
            doc.Paragraphs(i_rel),
            para_text(doc.Paragraphs(i_rel)).replace("Fig. 2.", "Fig. 3.", 1),
        )
        style_caption(doc.Paragraphs(i_rel).Range)
        i_t3 = find_para(doc, lambda t: "Table 3 records a seven-channel" in t)
        set_para_text(
            doc.Paragraphs(i_t3),
            para_text(doc.Paragraphs(i_t3)).replace(
                "Table 3 records a seven-channel leakage audit (L1–L7) "
                "for the evaluation pipeline on each dataset.",
                "Table 3 records a seven-channel leakage audit (L1–L7) "
                "for the evaluation pipeline on each dataset. Fig. 1 "
                "summarizes that pipeline.",
                1,
            ),
        )
        i_cap3 = find_para(doc, lambda t: t.startswith("Table 3. Seven-channel"))
        rng = doc.Paragraphs(i_cap3).Range
        rng.Collapse(0)
        rng.InsertParagraphAfter()
        pic_i = i_cap3 + 1
        shp = doc.Paragraphs(pic_i).Range.InlineShapes.AddPicture(str(FIG))
        shp.LockAspectRatio = True
        shp.Width = COL_W
        try:
            doc.Paragraphs(pic_i).Range.ParagraphFormat.Alignment = WD_ALIGN_CENTER
        except Exception:
            pass
        rng = doc.Paragraphs(pic_i).Range
        rng.Collapse(0)
        rng.InsertParagraphAfter()
        cap_i = pic_i + 1
        set_para_text(doc.Paragraphs(cap_i), CAP1)
        style_caption(doc.Paragraphs(cap_i).Range)
        text = doc.Content.Text
        if "Fig. 1. Distribution" in text:
            raise SystemExit("old Fig. 1 distribution caption remains")
        if "Fig. 2. Reliability" in text:
            raise SystemExit("old Fig. 2 reliability caption remains")
        if "Fig. 3. Reliability" not in text:
            raise SystemExit("Fig. 3 caption missing")
        if "Fig. 2 (top)" not in text:
            raise SystemExit("Fig. 2 (top) missing")
        if "0.1136" not in text or "0.2280" not in text:
            raise SystemExit("ECE lock missing")
        doc.Save()
        print("fig pipeline inserted")
    finally:
        try:
            doc.Close(WD_SAVE)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
