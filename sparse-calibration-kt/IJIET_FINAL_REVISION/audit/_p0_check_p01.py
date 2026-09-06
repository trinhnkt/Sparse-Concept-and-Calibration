import sys

sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

import fitz
from docx import Document

HERE = Path(__file__).resolve().parents[1]
for name in ("Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx", "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.docx"):
    d = Document(str(HERE / "manuscript" / name))
    for i, p in enumerate(d.paragraphs):
        if "Secondary explanatory" in (p.text or ""):
            print(name, i, p.style.name, repr(p.text))

pdf = fitz.open(str(HERE / "output" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf"))
for i, page in enumerate(pdf):
    if "Secondary explanatory" not in page.get_text("text"):
        continue
    print("PAGE", i + 1)
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for line in b.get("lines", []):
            s = "".join(sp["text"] for sp in line["spans"])
            if "Secondary" in s or s.strip().startswith("A.") or "Estimability" in s:
                fonts = sorted(
                    {(round(sp["size"], 1), sp["font"]) for sp in line["spans"]}
                )
                y = line["bbox"][1]
                print(f"  y={y:.1f} {fonts} | {s!r}")
