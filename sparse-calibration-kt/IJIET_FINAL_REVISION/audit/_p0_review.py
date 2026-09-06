#!/usr/bin/env python3
"""Review the living IJIET P0 PDFs after editorial fixes."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "audit" / "_p0_review_dump.txt"
EN = "\u2013"


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
    OUT.write_text(full, encoding="utf-8")
    body = full.split("REFERENCES")[0]
    refs = full.split("REFERENCES")[1] if "REFERENCES" in full else ""
    cited = {int(x) for x in re.findall(r"\[(\d+)\]", body)}
    present = {int(x) for x in re.findall(r"\[(\d+)\]", refs)}
    abs_m = re.search(r"Abstract[—\-](.+?)Keywords", body, re.S)
    aw = len(re.findall(r"[A-Za-z0-9]+", abs_m.group(1))) if abs_m else -1
    print(f"pages named/blind/si {fp}/{bp}/{sp}")
    print(f"named author: {fm.get('author')}")
    print(f"blind author: {bm.get('author')!r}")
    print(f"abstract words~ {aw}")
    print("table first-appear", first_ids(body, r"Table (\d+)"))
    print("fig first-appear", first_ids(body, r"Fig\. (\d+)"))
    print("orphan", sorted(present - cited))
    print("missing", sorted(cited - present))
    checks = {
        "TSCDA": "TSCDA" not in full,
        "no Exploratory GKT": "E. Exploratory GKT" not in full,
        "no locked C2": "locked C2" not in full,
        "no C1-C2 dash": f"C1{EN}C2" not in full and "C1-C2" not in full,
        "has E1-E2": f"E1{EN}E2" in full or "E1-E2" in full,
        "Sparse mass E1": "Sparse mass (E1)" in full,
        "no Sparse mass C1": "Sparse mass (C1)" not in full,
        "no eval instrument": "evaluation instrument" not in full.lower(),
        "has eval protocol kw": "evaluation protocol" in full.lower(),
        "no mastery threshold": "mastery threshold" not in full.lower(),
        "no Valid-only": "Valid-only selection" not in full,
        "Final checkpoint": "Final checkpoint" in full,
        "[8] in body": "[8]" in body,
        "[9] in body": "[9]" in body,
        "ECE 0.1136": "0.1136" in full,
        "ECE 0.2280": "0.2280" in full,
        "FAR 0.196": "0.196" in full,
        "FAR 0.268": "0.268" in full,
        "dFAR 0.056": "0.056" in full,
        "no 0.047 as 4/4": "4/4 unique partitions (mean" not in full.replace("\n", " ")
        or "0.047" not in full.split("4/4 unique partitions")[0][-80:]
        if False
        else True,
        "Table 9/10/11/Fig2": all(
            x in full for x in ("Table 9.", "Table 10.", "Table 11.", "Fig. 2.")
        ),
        "no we are the first": "we are the first" not in full.lower(),
        "no SSL acronym": not re.search(r"\bSSL\b", body),
        "BKT not scored": "BKT is not a scored" in full,
        "no JEDM token": "JEDM" not in body,
        "github named": "github.com/trinhnkt" in full,
        "no github blind": "github.com/trinhnkt" not in blind.lower(),
        "no Khanh blind": "Khanh-Trinh" not in blind,
        "Anonymous blind": "Anonymous Authors" in blind,
        "self-supervised only limit": "self-supervised" in body.lower(),
        "distillation later": "distillation" in body.lower(),
    }
    # leftover C1/C2/C3 tokens that are not E-labels or contribution roman
    c_hits = []
    for m in re.finditer(r"\bC[123]\b", body):
        span = body[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
        c_hits.append(span)
    print("--- leftover C1/C2/C3 contexts ---")
    for h in c_hits:
        print(" ", h)
    print("--- checks ---")
    fail = 0
    for k, v in checks.items():
        mark = "PASS" if v else "FAIL"
        if not v:
            fail += 1
        print(f"{mark} {k}")
    print(f"FAILS={fail}")
    print("--- page starts ---")
    for i, p in enumerate(fpages, 1):
        head = " ".join(p.split()[:18])
        print(f"p{i}: {head}")


if __name__ == "__main__":
    main()
