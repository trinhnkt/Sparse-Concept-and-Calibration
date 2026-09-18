#!/usr/bin/env python3
"""Tighten space above tables/figures: drop empty spacer paras, shrink caption before."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from manuscript_paths import FULL_DOCX  # noqa: E402

LOG = HERE / "audit" / "tighten_float_gaps_log.txt"
BEFORE = "60"  # 3 pt
AFTER = "40"  # 2 pt


def text_of(el) -> str:
    return "".join(el.itertext()).strip()


def has_pict(el) -> bool:
    return bool(el.xpath(".//*[local-name()='pict' or local-name()='drawing']"))


def is_caption_start(s: str) -> bool:
    return s.startswith("Table ") or s.startswith("Fig. ")


def set_spacing(p_el, before: str | None, after: str | None) -> None:
    pPr = p_el.find(qn("w:pPr"))
    if pPr is None:
        pPr = etree.SubElement(p_el, qn("w:pPr"))
    sp = pPr.find(qn("w:spacing"))
    if sp is None:
        sp = etree.SubElement(pPr, qn("w:spacing"))
    if before is not None:
        sp.set(qn("w:before"), before)
    if after is not None:
        sp.set(qn("w:after"), after)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    d = Document(str(FULL_DOCX))
    body = d.element.body
    kids = list(body)
    ns_p = qn("w:p")
    ns_tbl = qn("w:tbl")

    def neighbor(idx: int, step: int):
        j = idx + step
        while 0 <= j < len(kids):
            e = kids[j]
            if e.tag == ns_p and not text_of(e) and not has_pict(e):
                j += step
                continue
            return e
        return None

    removed = 0
    to_drop = []
    for i, el in enumerate(kids):
        if el.tag != ns_p or has_pict(el) or text_of(el):
            continue
        prev = neighbor(i, -1)
        nxt = neighbor(i, 1)
        prev_tbl = prev is not None and prev.tag == ns_tbl
        nxt_cap = nxt is not None and is_caption_start(text_of(nxt))
        nxt_tbl = nxt is not None and nxt.tag == ns_tbl
        prev_cap = prev is not None and is_caption_start(text_of(prev))
        if (prev_tbl and (nxt_cap or nxt_tbl)) or (prev_cap and nxt_tbl):
            to_drop.append(el)
    for el in to_drop:
        body.remove(el)
        removed += 1

    n_cap = 0
    n_pict = 0
    for el in body:
        if el.tag != qn("w:p"):
            continue
        t = text_of(el)
        if is_caption_start(t):
            set_spacing(el, BEFORE, AFTER)
            n_cap += 1
        if has_pict(el):
            set_spacing(el, "40", AFTER)
            n_pict += 1

    d.save(str(FULL_DOCX))
    msg = f"removed_empty={removed} captions={n_cap} pict={n_pict}"
    LOG.write_text(msg + "\n", encoding="utf-8")
    print(msg)


if __name__ == "__main__":
    main()
