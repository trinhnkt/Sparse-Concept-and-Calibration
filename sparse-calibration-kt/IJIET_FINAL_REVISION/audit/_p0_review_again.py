#!/usr/bin/env python3
"""Living-pack review dump for 6 Sep P0 after phases 28–30."""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import fitz
from docx import Document

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "audit" / "_p0_review_again.txt"


def pdf(rel: str):
    d = fitz.open(str(HERE / rel))
    pages = [p.get_text("text") for p in d]
    return d, "\n".join(pages), d.page_count, dict(d.metadata or {}), pages


def main() -> None:
    lines: list[str] = []
    full_doc, full, fp, fm, fpages = pdf("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf")
    _, blind, bp, bm, _ = pdf("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf")
    _, si, sp, _, _ = pdf("output/supplementary.pdf")
    body = full.split("REFERENCES")[0]
    wd = Document(str(HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"))

    def p(*a):
        lines.append(" ".join(str(x) for x in a))

    p("pages", fp, bp, sp)
    p("named author", fm.get("author"))
    p("blind author", repr(bm.get("author")))

    # key paragraphs
    for para in wd.paragraphs:
        t = para.text.strip()
        if t.startswith("Contributions are conservative"):
            p("CONTRIB", t)
        if t.startswith("Next-response correctness"):
            p("LIMIT", t)
        if t.startswith("Manuscript received"):
            p("DATE", t)
        if t.startswith("This study is a secondary"):
            p("ETHICS", t)
        if t.startswith("During manuscript preparation"):
            p("AI", t)

    needles = {
        "ECE 0.1136": "0.1136" in full,
        "ECE 0.2280": "0.2280" in full,
        "FAR 0.196": "0.196" in full,
        "FAR 0.268": "0.268" in full,
        "dFAR 0.056": "0.056" in full,
        "XES 0.1176": "0.1176" in full,
        "XES 0.1129": "0.1129" in full,
        "XES 0.1254": "0.1254" in full,
        "T7 N=114": "N=114" in full or "N≈114" in full or "N=114" in body,
        "official SimpleKT 0.7700": "0.7700" in full,
        "official ECE 0.0203": "0.0203" in full,
        "official ECE 0.0884": "0.0884" in full,
        "occupancy-aware": "occupancy-aware" in full,
        "dataset-dependent rather": "dataset-dependent rather" in full,
        "reproducibility artifact": "reproducibility artifact" in full,
        "NOT RECOVERED in Lim": "NOT RECOVERED" in full[full.find("D. Limitations"):full.find("VI. CONCLUSION")] if "D. Limitations" in full else True,
        "NOT RECOVERED count": full.count("NOT RECOVERED"),
        "TSCDA": "TSCDA" in full,
        "JEDM body": "JEDM" in body,
        "mastery outcome": "mastery outcome" in full.lower(),
        "k5/k10 in body": "k5" in body and "k10" in body,
        "C1 token": "C1–C3" in full or "C1-C2" in full,
        "not under consideration": "not under consideration" in full,
        "Month date": "Month date, 2026" in full,
        "September 1": "September 1" in full,
        "10.18178": "10.18178" in full,
        "GPT-5.6": "GPT-5.6" in full,
        "Grok 4.6": "Grok 4.6" in full,
        "zip in Lim": "code_for_review_anonymous.zip" in full,
        "Fig. 1 pipeline": "Fig. 1. Reproducible" in full,
        "Fig. 3 reliability": "Fig. 3. Reliability" in full,
        "Table 8 conditions": "Table 8. Empirical conditions" in full,
        "Table 8 sparsif": "Table 8. Within-KC" in full,
        "S5-S6": "S5–S6" in full or "S5-S6" in full,
    }
    for k, v in needles.items():
        p(("PASS" if v else "FAIL") if isinstance(v, bool) else v, k)

    # Limitations should NOT contain NOT RECOVERED
    lim = full[full.find("D. Limitations"):full.find("VI. CONCLUSION")] if "D. Limitations" in full else ""
    p("LIM_NOT_RECOVERED", "NOT RECOVERED" in lim)
    p("LIM_zip", "code_for_review_anonymous.zip" in lim)

    contrib_i = full.find("Contributions")
    p("CONTRIB_PDF", " ".join(full[contrib_i:contrib_i+700].split())[:500])

    z = HERE / "output" / "OJS_UPLOAD" / "code_for_review_anonymous.zip"
    with zipfile.ZipFile(z) as zh:
        txt = "\n".join(
            zh.read(n).decode("utf-8", "replace")
            for n in zh.namelist()
            if n.lower().endswith((".txt", ".md"))
        )
        names = zh.namelist()
    p("zip files", len(names))
    p("zip JEDM", "JEDM" in txt)
    p("zip 8-page", "8-page" in txt)
    p("zip Khanh", "Khanh" in txt)
    p("zip trinhnkt", "trinhnkt" in txt.lower())

    p("blind Khanh", "Khanh-Trinh" in blind)
    p("blind github", "github.com" in blind.lower())
    p("blind Anonymous", "Anonymous Authors" in blind)

    # page 3/6 figure sizes
    for i, page in enumerate(full_doc, 1):
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") == 1:
                b = block["bbox"]
                p(f"img p{i}", round(b[2]-b[0],1), "x", round(b[3]-b[1],1))

    full_doc.close()
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
