#!/usr/bin/env python3
"""Extract living-blind needles for GO/NO-GO audit. Read-only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "audit" / "_p0_gng_extract.txt"


def main() -> None:
    pdf = HERE / "output" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf"
    d = fitz.open(str(pdf))
    pages = [p.get_text("text") for p in d]
    t = "\n".join(pages)
    body = t.split("REFERENCES")[0]
    lines = [f"pages={d.page_count} file={pdf}"]
    needles = [
        "Three alternative",
        "two alternative",
        "A. E. Secondary",
        "E. Secondary explanatory",
        "F. Secondary decision-error",
        "competitive AUC",
        "Success claims require",
        "sparse mass",
        "k5/k10",
        "rebuild_locked_tables",
        "one-command",
        "NOT RECOVERED",
        "Month date, 2026",
        "Grok 4.6",
        "GPT-5.6",
        "ChatGPT",
        "TSCDA",
        "GKT",
        "CL4KT",
        "self-supervised",
        "distillation",
        "RQ3",
        "contribution (ii)",
        "ucid",
        "N=114",
        "865",
        "6,413,353",
        "0.1136",
        "0.2280",
        "Fig. 3.",
        "Table 6.",
        "Table 7.",
        "Table 8.",
    ]
    for n in needles:
        lines.append(f"HIT {n!r} {t.count(n)}")
    # dump contexts
    for key in [
        "Three alternative",
        "two alternative",
        "A. E. Secondary",
        "competitive AUC",
        "Success claims require",
        "sparse mass",
        "k5/k10",
        "rebuild_locked",
        "one-command",
        "NOT RECOVERED",
        "Month date",
        "Grok 4.6",
        "RQ3",
        "very-sparse",
        "N=114",
    ]:
        i = 0
        c = 0
        tl = t
        while c < 3:
            j = tl.find(key, i)
            if j < 0:
                break
            lines.append(f"--- {key} @{j} ---")
            lines.append(" ".join(tl[max(0, j - 80) : j + 180].split()))
            i = j + len(key)
            c += 1
    # IV heads
    heads = re.findall(r"\n([A-F]\. [A-Za-z][^\n]{8,80})", body)
    lines.append("HEADS " + " | ".join(heads))
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:80]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
