#!/usr/bin/env python3
"""Balance layout: fill page holes by floating Fig. 2/3; keep Table 5 with caption."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from manuscript_paths import FULL_DOCX  # noqa: E402

LOG = HERE / "audit" / "balance_layout_log.txt"


def ptext(el) -> str:
    return "".join(el.itertext()).strip()


def has_pict(el) -> bool:
    return bool(el.xpath(".//*[local-name()='pict' or local-name()='drawing']"))


def keep_next(el, on: bool = True) -> None:
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        pPr = etree.SubElement(el, qn("w:pPr"))
    kn = pPr.find(qn("w:keepNext"))
    if on:
        if kn is None:
            kn = etree.SubElement(pPr, qn("w:keepNext"))
        kn.set(qn("w:val"), "true")
    elif kn is not None:
        pPr.remove(kn)


def set_caption_spacing(el) -> None:
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        pPr = etree.SubElement(el, qn("w:pPr"))
    sp = pPr.find(qn("w:spacing"))
    if sp is None:
        sp = etree.SubElement(pPr, qn("w:spacing"))
    sp.set(qn("w:before"), "80")
    sp.set(qn("w:after"), "40")


def find_p(body, pred):
    for el in body:
        if el.tag == qn("w:p") and pred(el):
            return el
    raise SystemExit("paragraph not found")


def find_tbl_after(body, caption_el):
    seen = False
    for el in body:
        if el is caption_el:
            seen = True
            continue
        if seen and el.tag == qn("w:tbl"):
            return el
    raise SystemExit("table after caption not found")


def move_block_before(anchor, *els) -> None:
    for el in reversed(els):
        anchor.addprevious(el)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log: list[str] = []
    d = Document(str(FULL_DOCX))
    body = d.element.body

    fig2_cap = find_p(body, lambda e: ptext(e).startswith("Fig. 2."))
    fig2_pict = fig2_cap.getprevious()
    if fig2_pict is None or not has_pict(fig2_pict):
        raise SystemExit("Fig. 2 pict not before caption")
    f_head = find_p(body, lambda e: ptext(e).startswith("F. Calibration"))
    if fig2_cap.getnext() is not f_head and f_head.getprevious() is not fig2_cap:
        move_block_before(f_head, fig2_pict, fig2_cap)
        log.append("moved Fig. 2 to after E. Reliability, before F. Calibration")
    else:
        log.append("Fig. 2 already before F")

    fig3_cap = find_p(body, lambda e: ptext(e).startswith("Fig. 3."))
    fig3_pict = fig3_cap.getprevious()
    if fig3_pict is None or not has_pict(fig3_pict):
        raise SystemExit("Fig. 3 pict not before caption")
    d_head = find_p(body, lambda e: ptext(e).startswith("D. Diagnostic conditions"))
    if fig3_cap.getnext() is not d_head:
        move_block_before(d_head, fig3_pict, fig3_cap)
        log.append("moved Fig. 3 to after Table 7, before IV.D")
    else:
        log.append("Fig. 3 already before IV.D")

    keep_next(fig2_pict, True)
    keep_next(fig3_pict, True)
    keep_next(fig2_cap, False)
    keep_next(fig3_cap, False)
    set_caption_spacing(fig2_cap)
    set_caption_spacing(fig3_cap)
    log.append("KeepNext on Fig. 2/3 images only")

    t5_cap = find_p(body, lambda e: ptext(e).startswith("Table 5."))
    keep_next(t5_cap, True)
    set_caption_spacing(t5_cap)
    log.append("Table 5 caption KeepWithNext")

    t6_cap = find_p(body, lambda e: ptext(e).startswith("Table 6."))
    keep_next(t6_cap, True)

    blob = "\n".join(ptext(el) for el in body if el.tag == qn("w:p"))
    for lock in ("0.1136", "0.2280", "0.196", "0.268", "Fig. 2.", "Fig. 3.", "Table 5.", "Table 7."):
        if lock not in blob:
            raise SystemExit(f"missing {lock}")

    d.save(str(FULL_DOCX))
    LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
