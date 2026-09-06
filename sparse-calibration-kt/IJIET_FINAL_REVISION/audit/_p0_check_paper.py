#!/usr/bin/env python3
"""One-shot audit of the living IJIET P0 PDFs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def load(name: str) -> tuple[str, int, dict]:
    d = fitz.open(str(HERE / name))
    text = "\n".join(p.get_text("text") for p in d)
    return text, d.page_count, d.metadata


def first_ids(text: str, pat: str) -> list[int]:
    order: list[int] = []
    for m in re.finditer(pat, text):
        n = int(m.group(1))
        if n not in order:
            order.append(n)
    return order


def main() -> None:
    full, fp, fm = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf")
    blind, bp, bm = load("output/Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf")
    body = full.split("REFERENCES")[0]
    refs = full.split("REFERENCES")[1] if "REFERENCES" in full else ""
    cited = {int(x) for x in re.findall(r"\[(\d+)\]", body)}
    present = {int(x) for x in re.findall(r"\[(\d+)\]", refs)}
    abs_m = re.search(r"Abstract[—\-](.+?)Keywords", body, re.S)
    aw = len(re.findall(r"[A-Za-z0-9]+", abs_m.group(1))) if abs_m else -1
    print(f"pages named/blind {fp}/{bp}")
    print(f"named author meta: {fm.get('author')}")
    print(f"blind author meta: {bm.get('author')!r}")
    print(f"abstract words~ {aw}")
    print("table first-appear", first_ids(body, r"Table (\d+)"))
    print("fig first-appear", first_ids(body, r"Fig\. (\d+)"))
    print("cited", sorted(cited))
    print("ref list", sorted(present))
    print("orphan refs", sorted(present - cited))
    print("missing refs", sorted(cited - present))
    needles = {
        "TSCDA": "TSCDA" in full,
        "Exploratory GKT": "E. Exploratory GKT" in full,
        "GKT scored": "CL4KT protocol adapter are scored" in full,
        "JEDM token": "JEDM" in body,
        "locked C2": "locked C2" in full,
        "github named": "github.com/trinhnkt" in full,
        "github blind": "github.com/trinhnkt" in blind.lower(),
        "Khanh blind": "Khanh-Trinh" in blind,
        "Anonymous blind": "Anonymous Authors" in blind,
        "ECE 0.1136": "0.1136" in full,
        "ECE 0.2280": "0.2280" in full,
        "FAR 0.196": "0.196" in full,
        "FAR 0.268": "0.268" in full,
        "dFAR 0.056": "0.056" in full,
        "dFAR 0.047 as 4/4": "4/4 unique partitions (mean ΔFAR 0.047" in full
        or "4/4 unique partitions (mean ΔFAR 0.047" in full.replace("\n", " "),
        "Table 9": "Table 9." in full,
        "Table 10": "Table 10." in full,
        "Table 11": "Table 11." in full,
        "Fig. 2": "Fig. 2." in full,
        "we are the first": "we are the first" in full.lower(),
        "new KT architecture proposed": "We propose a new KT" in full,
        "SSL word": "self-supervised" in body.lower(),
        "SSL acronym": bool(re.search(r"\bSSL\b", body)),
        "GNN word": "graph neural" in body.lower(),
        "distillation": "distillation" in body.lower(),
        "BKT scored": "BKT is not a scored" in full,
        "eval instrument kw": "evaluation instrument" in full,
    }
    for k, v in needles.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
