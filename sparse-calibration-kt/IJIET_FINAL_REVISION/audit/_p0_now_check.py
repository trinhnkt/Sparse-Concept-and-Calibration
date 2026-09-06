#!/usr/bin/env python3
from __future__ import annotations
import re, sys, zipfile
from pathlib import Path
import fitz

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

def load(rel):
    d = fitz.open(str(HERE / rel))
    pages = [p.get_text("text") for p in d]
    return "\n".join(pages), d.page_count, pages

full, fp, fpages = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf")
blind, bp, _ = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf")
si, sp, _ = load("output/supplementary.pdf")
body = full.split("REFERENCES")[0]
heads = re.findall(r"\n([A-F]\. [A-Za-z][^\n]{8,70})", body)
print(f"pages {fp}/{bp}/{sp}")
print("IV heads", heads)
print("table first", [int(x) for x in dict.fromkeys(re.findall(r"Table (\d+)", body))])
checks = {
    "9/9": fp == 9 and bp == 9,
    "ECE": "0.1136" in full and "0.2280" in full,
    "FAR": "0.196" in full and "0.268" in full and "0.056" in full,
    "T7 cold-start": "Table 7. Cold-start" in full,
    "T8 conditions": "Table 8. Empirical conditions" in full,
    "IV.C cold": "C. Cold-start" in full,
    "IV.F FAR": "F. Secondary decision-error" in full,
    "no TSCDA": "TSCDA" not in full,
    "no JEDM body": "JEDM" not in body,
    "no mastery outcome": "mastery outcome" not in full.lower(),
    "estimands": "need not coincide" in full,
    "S2": "Supplementary Table S2" in full,
    "S7": "Supplementary Table S7" in full,
    "blind anon": "Anonymous Authors" in blind and "Khanh-Trinh" not in blind,
}
for k, v in checks.items():
    print(("PASS" if v else "FAIL"), k)

z = HERE / "output/OJS_UPLOAD/code_for_review_anonymous.zip"
with zipfile.ZipFile(z) as zh:
    txt = "\n".join(
        zh.read(n).decode("utf-8", "replace")
        for n in zh.namelist()
        if n.lower().endswith((".txt", ".md"))
    )
print("zip JEDM", "JEDM" in txt)
print("zip 8-page", "8-page" in txt)
print("--- page starts ---")
for i, p in enumerate(fpages, 1):
    print(f"p{i}:", " ".join(p.split()[:16]))
