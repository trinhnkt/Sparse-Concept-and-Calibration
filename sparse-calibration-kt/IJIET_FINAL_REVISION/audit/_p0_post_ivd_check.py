#!/usr/bin/env python3
"""Post-IV.D living-PDF checklist. No edits."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def load(rel: str):
    d = fitz.open(str(HERE / rel))
    pages = [p.get_text("text") for p in d]
    return "\n".join(pages), d.page_count, d.metadata, pages


def first_ids(text: str, pat: str) -> list[int]:
    order: list[int] = []
    for m in re.finditer(pat, text):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    return order


def main() -> None:
    full, fp, fm, fpages = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf")
    blind, bp, bm, _ = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf")
    si, sp, _, _ = load("output/supplementary.pdf")
    body = full.split("REFERENCES")[0]
    print(f"pages named/blind/si {fp}/{bp}/{sp}")
    print("table first-appear", first_ids(body, r"Table (\d+)"))
    print("fig first-appear", first_ids(body, r"Fig\. (\d+)"))
    checks = {
        "9 pages": fp == 9 and bp == 9,
        "ECE 0.1136/0.2280": "0.1136" in full and "0.2280" in full,
        "FAR 0.196/0.268": "0.196" in full and "0.268" in full,
        "no TSCDA": "TSCDA" not in full,
        "no JEDM in article": "JEDM" not in body,
        "secondary evidence": "secondary evidence for why and when" in full,
        "short sparsif": "universal monotonic frequency effect" in full,
        "estimands": "need not coincide" in full,
        "no 12-row Table 8 caption": "Table 8. Within-KC" not in full,
        "Table 7 conditions": "Table 7. Empirical conditions" in full,
        "Table 8 cold-start": "Table 8. Cold-start" in full,
        "S2 pointer": "Supplementary Table S2" in full,
        "regression -0.068": "0.068" in full,
        "no github blind": "trinhnkt" not in blind.lower(),
        "Anonymous blind": "Anonymous Authors" in blind,
        "no Khanh blind": "Khanh-Trinh" not in blind,
    }
    for k, v in checks.items():
        print(("PASS" if v else "FAIL"), k)

    idx = full.find("Table 6.")
    chunk = full[idx : idx + 2800] if idx >= 0 else ""
    print("Table6 has XES body row", "XES3G5M" in chunk.split("Fig.")[0] if "Fig." in chunk else "XES3G5M" in chunk)

    z = HERE / "output" / "OJS_UPLOAD" / "code_for_review_anonymous.zip"
    with zipfile.ZipFile(z) as zh:
        readme = zh.read("README_CODE_FOR_REVIEW.txt").decode("utf-8", "replace")
        living = ""
        if "IJIET_FINAL_REVISION/README.md" in zh.namelist():
            living = zh.read("IJIET_FINAL_REVISION/README.md").decode("utf-8", "replace")
    print("zip names JEDM", "JEDM" in readme or "JEDM" in living)
    print("zip says 8-page", "8-page" in readme)
    print("--- leftover Table 9 in body ---", "Table 9." in body)


if __name__ == "__main__":
    main()
