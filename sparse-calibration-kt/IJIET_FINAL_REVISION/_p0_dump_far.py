#!/usr/bin/env python3
"""Dump RQ / FAR / mastery wording from the living named Word."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
OUT = HERE / "audit" / "_p0_far_dump.txt"

NEEDLES = (
    "RQ1",
    "RQ2",
    "RQ3",
    "FAR",
    "false-advance",
    "mastery",
    "decision-error",
    "Nadvance",
    "ΔFAR",
    "Delta FAR",
    "0.072",
    "0.056",
    "S5",
    "S6",
    "Threshold-based",
    "simulated",
)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = Document(str(FULL))
    lines: list[str] = []
    for i, p in enumerate(d.paragraphs):
        t = p.text.strip()
        if not t:
            continue
        if any(n.lower() in t.lower() for n in NEEDLES):
            lines.append(f"===== p{i} =====")
            lines.append(t)
            lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT, "hits", len(lines) // 3)


if __name__ == "__main__":
    main()
