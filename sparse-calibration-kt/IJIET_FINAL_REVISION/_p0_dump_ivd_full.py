#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
from docx import Document

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
OUT = HERE / "audit" / "_p0_ivd_full.txt"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = Document(str(FULL))
    lines = []
    for i in [88, 89, 90, 91, 92, 93, 94, 96, 99, 100, 101, 108]:
        lines.append(f"===== p{i} =====")
        lines.append(d.paragraphs[i].text)
    OUT.write_text("\n\n".join(lines), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
