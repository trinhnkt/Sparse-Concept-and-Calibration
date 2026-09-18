#!/usr/bin/env python3
"""Fill leftover whitespace: 2-col body before oversized 1-col figures. No cell edits."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from manuscript_paths import FULL_DOCX  # noqa: E402

LOG = HERE / "audit" / "fill_page_holes_log.txt"


def ptext(el) -> str:
    return "".join(el.itertext()).strip()


def has_pict(el) -> bool:
    return bool(el.xpath(".//*[local-name()='pict' or local-name()='drawing']"))


def has_sect(el) -> bool:
    pPr = el.find(qn("w:pPr"))
    if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
        return True
    return el.find(qn("w:sectPr")) is not None


def find_p(body, pred):
    for el in body:
        if el.tag == qn("w:p") and pred(el):
            return el
    raise SystemExit("paragraph not found")


def block_until(start, stop) -> list:
    out = []
    el = start
    while el is not None and el is not stop:
        nxt = el.getnext()
        if has_sect(el) and not ptext(el) and not has_pict(el):
            el = nxt
            continue
        out.append(el)
        el = nxt
    if not out:
        raise SystemExit("empty block")
    return out


def move_before(anchor, els: list) -> None:
    for el in reversed(els):
        if el is anchor:
            continue
        anchor.addprevious(el)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log: list[str] = []
    d = Document(str(FULL_DOCX))
    body = d.element.body

    cap2 = find_p(body, lambda e: ptext(e).startswith("Fig. 2."))
    pict2 = cap2.getprevious()
    if pict2 is None or not has_pict(pict2):
        raise SystemExit("Fig. 2 pict missing")
    e_head = find_p(body, lambda e: ptext(e).startswith("E. Reliability flags"))
    f_head = find_p(body, lambda e: ptext(e).startswith("F. Calibration"))
    e_block = block_until(e_head, f_head)
    move_before(pict2, e_block)
    log.append(f"E. Reliability ({len(e_block)} els) before Fig. 2")

    cap3 = find_p(body, lambda e: ptext(e).startswith("Fig. 3."))
    pict3 = cap3.getprevious()
    if pict3 is None or not has_pict(pict3):
        raise SystemExit("Fig. 3 pict missing")
    d_head = find_p(body, lambda e: ptext(e).startswith("D. Diagnostic conditions"))
    t8 = find_p(body, lambda e: ptext(e).startswith("Table 8."))
    d_block = block_until(d_head, t8)
    move_before(pict3, d_block)
    log.append(f"IV.D ({len(d_block)} els) before Fig. 3")

    blob = "\n".join(ptext(el) for el in body if el.tag == qn("w:p"))
    for lock in ("0.1136", "0.2280", "0.196", "0.268", "Fig. 2.", "Fig. 3.", "E. Reliability", "D. Diagnostic"):
        if lock not in blob:
            raise SystemExit(f"missing {lock}")
    d.save(str(FULL_DOCX))
    LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
