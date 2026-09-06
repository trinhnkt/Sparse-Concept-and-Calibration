#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
OUT = HERE / "audit" / "_p0_results_dump.txt"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = Document(str(FULL))
    lines = []
    in_res = False
    for i, p in enumerate(d.paragraphs):
        t = p.text.strip()
        if t.startswith("IV. RESULTS") or t.startswith("IV. R"):
            in_res = True
        if t.startswith("V. DISCUSSION") or t.startswith("V. D"):
            lines.append(f"===== p{i} =====")
            lines.append(t)
            break
        if not in_res:
            continue
        if not t:
            continue
        head = t.startswith(("IV.", "A.", "B.", "C.", "D.", "E.", "F.", "Table ", "Fig."))
        if head or len(t) < 80:
            lines.append(f"===== p{i} =====")
            lines.append(t[:700])
            lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT, "n", len(lines))


if __name__ == "__main__":
    main()
