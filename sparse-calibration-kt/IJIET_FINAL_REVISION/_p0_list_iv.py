#!/usr/bin/env python3
from __future__ import annotations
import sys
from docx import Document

d = Document(r"IJIET_FINAL_REVISION/manuscript/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx")
sys.stdout.reconfigure(encoding="utf-8")
for i, p in enumerate(d.paragraphs):
    if i < 60 or i > 115:
        continue
    t = " ".join(p.text.split())
    mark = "HEAD" if t.startswith(("IV.", "A.", "B.", "C.", "D.", "E.", "F.", "V.")) else ""
    print(f"{i:3} {mark:4} {t[:120]}")
