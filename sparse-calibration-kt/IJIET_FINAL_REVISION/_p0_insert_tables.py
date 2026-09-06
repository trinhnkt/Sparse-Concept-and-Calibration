#!/usr/bin/env python3
"""Insert Table 9 leakage, Table 10 Brier, Table 11 cold-start, Fig. 2 after named anchors."""
from __future__ import annotations

import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
FIG2 = HERE / "figures" / "fig2_reliability_p0.png"

WD_ALIGN_CENTER = 1
WD_BREAK_SECTION = 2
WD_STORY = 6


def find_para(doc, startswith: str):
    for i in range(1, doc.Paragraphs.Count + 1):
        t = doc.Paragraphs(i).Range.Text.replace("\r", "").replace("\x07", "")
        if t.startswith(startswith):
            return i
    raise SystemExit(f"anchor not found: {startswith[:50]!r}")


def style_caption(rng) -> None:
    try:
        rng.Style = "figure caption"
    except Exception:
        pass
    rng.Font.Name = "Times New Roman"
    rng.Font.Size = 8
    rng.Font.Bold = False
    rng.ParagraphFormat.Alignment = WD_ALIGN_CENTER


def style_table(tbl) -> None:
    for r in range(1, tbl.Rows.Count + 1):
        for c in range(1, tbl.Columns.Count + 1):
            cell = tbl.Cell(r, c)
            cell.Range.Font.Name = "Times New Roman"
            cell.Range.Font.Size = 7
            cell.Range.Font.Bold = r == 1
            pf = cell.Range.ParagraphFormat
            pf.SpaceBefore = 0
            pf.SpaceAfter = 0


def insert_after(doc, i: int, caption: str, rows: list[list[str]]) -> None:
    rng = doc.Paragraphs(i).Range
    rng.Collapse(0)
    rng.InsertParagraphAfter()
    cap = doc.Paragraphs(i + 1).Range
    cap.Text = caption + "\r"
    style_caption(cap)
    rng = doc.Paragraphs(i + 1).Range
    rng.Collapse(0)
    tbl = doc.Tables.Add(rng, len(rows), len(rows[0]))
    for ri, row in enumerate(rows, 1):
        for ci, val in enumerate(row, 1):
            tbl.Cell(ri, ci).Range.Text = val
    style_table(tbl)


def insert_fig2(doc, i: int) -> None:
    rng = doc.Paragraphs(i).Range
    rng.Collapse(0)
    rng.InsertParagraphAfter()
    cap_i = i + 1
    doc.Paragraphs(cap_i).Range.Text = (
        "Fig. 2. Reliability diagrams (15 equal-width bins; seed 42). "
        "Rows: ASSISTments 2012 and Junyi Academy. Columns: DKT and T-KT. "
        "ASSISTments panels show dense vs sparse; Junyi panels show dense vs medium "
        "(learner-based sparse is empty). Not a classroom trial.\r"
    )
    style_caption(doc.Paragraphs(cap_i).Range)
    rng = doc.Paragraphs(cap_i).Range
    rng.Collapse(0)
    rng.InsertParagraphAfter()
    pic_i = cap_i + 1
    shp = doc.Paragraphs(pic_i).Range.InlineShapes.AddPicture(str(FIG2))
    shp.LockAspectRatio = True
    shp.Width = 480


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not FIG2.is_file():
        raise SystemExit(f"missing {FIG2}")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(FULL))
    try:
        # avoid double insert
        whole = doc.Content.Text
        if "Table 9. Seven-channel leakage" in whole:
            print("tables already present")
            doc.Close(0)
            word.Quit()
            return

        t4 = find_para(doc, "C. Threshold-based decision error")
        insert_after(
            doc,
            t4 - 1,
            "Table 10. Four-partition Brier score and Murphy decomposition (UNC − RES + REL) "
            "by train-only stratum. N is the mean test-event count. Junyi sparse is empty. "
            "XES3G5M T-KT ECE cells in the main text use the masked series 0.1176 / 0.1129 / "
            "0.1254; Brier rows below are the same four-partition aggregation as Supplementary Table S1.",
            [
                ["Dataset", "Model", "Stratum", "N", "ECE", "Brier", "UNC", "REL", "RES"],
                ["ASSISTments", "DKT", "dense", "523,971", "0.0602", "0.1931", "0.2103", "0.0053", "0.0223"],
                ["ASSISTments", "DKT", "sparse", "415", "0.2333", "0.2502", "0.2337", "0.0624", "0.0451"],
                ["ASSISTments", "T-KT", "dense", "523,971", "0.1136", "0.2116", "0.2103", "0.0201", "0.0186"],
                ["ASSISTments", "T-KT", "sparse", "415", "0.2280", "0.2525", "0.2337", "0.0594", "0.0392"],
                ["Junyi", "DKT", "dense", "3,226,541", "0.0389", "0.1804", "0.2078", "0.0022", "0.0294"],
                ["Junyi", "DKT", "medium", "3,706", "0.2513", "0.3077", "0.2432", "0.0741", "0.0091"],
                ["Junyi", "T-KT", "dense", "3,232,614", "0.0792", "0.1884", "0.2079", "0.0084", "0.0279"],
                ["Junyi", "T-KT", "medium", "3,836", "0.1073", "0.2307", "0.2417", "0.0149", "0.0260"],
            ],
        )
        insert_fig2(doc, find_para(doc, "C. Threshold-based decision error") - 1)

        t2 = find_para(doc, "Graph-based and contrastive KT models are not trained")
        insert_after(
            doc,
            t2,
            "Table 9. Seven-channel leakage checklist for the evaluation pipeline (learner-based fold 0). "
            "PASS means the decision is train-only, validation-only, or a fixed training schedule (L6: final checkpoint). Test is used only to report.",
            [
                ["Channel", "Decision", "Assist.", "Junyi", "XES3G5M"],
                ["L1 Split", "Learner-disjoint users", "PASS", "PASS", "PASS"],
                ["L2 Preprocess", "Train-only transforms", "PASS", "PASS", "PASS"],
                ["L3 Q-matrix", "Static platform tag", "PASS", "PASS (ucid)", "PASS"],
                ["L4 Bucket", "f_train cuts only", "PASS", "PASS (empty sparse)", "PASS"],
                ["L5 Calibration", "No test-fit map", "PASS", "PASS", "PASS"],
                ["L6 Hyperparam.", "Final checkpoint", "PASS", "PASS", "PASS"],
                ["L7 Cold-start", "f_train=0 documented", "PASS (I)", "PASS (empty)", "PASS (I)"],
            ],
        )

        e = find_para(doc, "E. Cold-start concept feasibility")
        insert_after(
            doc,
            e + 1,
            "Table 11. Cold-start concept feasibility (four-partition means). Strict: f_train=0. "
            "Limited/very-sparse: 0<f_train<20. I = Insufficient (N<100). Not a recommender user/item split.",
            [
                ["Dataset", "Slice", "Mean N", "Flag", "T-KT ECE", "DKT ECE"],
                ["ASSISTments", "strict f=0", "4", "I", "descriptive", "descriptive"],
                ["ASSISTments", "very-sparse", "17", "I", "0.245", "0.178"],
                ["Junyi", "strict / sparse", "0", "empty", "—", "—"],
                ["XES3G5M", "very-sparse", "114", "I/L", "0.184", "0.173"],
            ],
        )
        doc.Save()
        print("inserted tables 9–11 and Fig. 2")
    finally:
        try:
            doc.Close(0)
        except Exception:
            pass
        word.Quit()


if __name__ == "__main__":
    main()
