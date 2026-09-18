#!/usr/bin/env python3
"""Re-export named + blind PDFs from living Word. No 6.1 / venue text."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import win32com.client as win32

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from apply_a19_word import PAPER_TITLE, stamp_pdf_metadata  # noqa: E402
from apply_p0_b1_b13 import patch_blind_data  # noqa: E402
from build_a16_double_blind import (  # noqa: E402
    AUTHORS_META,
    BLIND_DOC,
    BLIND_DOCX,
    BLIND_PDF,
    FULL_DOC,
    FULL_DOCX,
    FULL_PDF,
    anonymize_blind,
    compact,
    export_pdf,
    lock_checks,
    pdf_text,
    set_word_props,
)
from fix_empty_page_break import copy_ojs_safe  # noqa: E402

LOG = HERE / "audit" / "export_pdfs_16sep_log.txt"
WD_FORMAT_XML = 16
WD_FORMAT_DOC = 0
WD_SAVE = -1


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log: list[str] = ["export 16sep"]
    LOG.write_text("start\n", encoding="utf-8")
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    full_doc = None
    blind_doc = None
    try:
        full_doc = word.Documents.Open(str(FULL_DOCX))
        try:
            full_doc.BuiltInDocumentProperties("Title").Value = PAPER_TITLE
        except Exception:
            pass
        full_doc.SaveAs2(str(FULL_DOCX), WD_FORMAT_XML)
        export_pdf(full_doc, FULL_PDF, include_props=True)
        full_doc.SaveAs2(str(FULL_DOC), WD_FORMAT_DOC)
        log.append("named pdf")
        LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
        full_doc.Close(WD_SAVE)
        full_doc = None

        shutil.copy2(FULL_DOCX, BLIND_DOCX)
        blind_doc = word.Documents.Open(str(BLIND_DOCX))
        anonymize_blind(blind_doc, log)
        patch_blind_data(blind_doc, log)
        set_word_props(blind_doc, "", "")
        try:
            blind_doc.BuiltInDocumentProperties("Title").Value = PAPER_TITLE
        except Exception:
            pass
        try:
            blind_doc.RemoveDocumentInformation(1)
        except Exception:
            pass
        if "Khanh-Trinh" in (blind_doc.Content.Text or ""):
            raise SystemExit("blind identified")
        blind_doc.SaveAs2(str(BLIND_DOCX), WD_FORMAT_XML)
        blind_doc.SaveAs2(str(BLIND_DOC), WD_FORMAT_DOC)
        export_pdf(blind_doc, BLIND_PDF, include_props=False)
        log.append("blind pdf")
        blind_doc.Close(WD_SAVE)
        blind_doc = None
    finally:
        if full_doc is not None:
            try:
                full_doc.Close(0)
            except Exception:
                pass
        if blind_doc is not None:
            try:
                blind_doc.Close(0)
            except Exception:
                pass
        word.Quit()

    stamp_pdf_metadata(FULL_PDF, AUTHORS_META)
    stamp_pdf_metadata(BLIND_PDF, "")
    copy_ojs_safe(log)
    full_t, full_pages = pdf_text(FULL_PDF)
    blind_t, blind_pages = pdf_text(BLIND_PDF)
    c = compact(full_t)
    locks = lock_checks(full_t, full_pages)
    checks = {
        "pages": 8 <= full_pages <= 14 and 8 <= blind_pages <= 14,
        "locks": all(locks.values()),
        "a6": "Table A6" in full_t,
        "b2": "0.114to0.228" in c and "0.020to0.088" in c,
        "b13": "exemptfromprospective" in c,
        "no_si": "Supplementary Table S" not in full_t,
        "no_jedm": "JEDM" not in full_t.upper().replace(" ", ""),
        "blind_clean": "Khanh-Trinh" not in blind_t,
    }
    log.append(f"pages {full_pages}/{blind_pages}")
    log.append(str(locks))
    log.append(str(checks))
    LOG.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log[-12:]))
    if not all(checks.values()):
        raise SystemExit(f"fail {checks}")


if __name__ == "__main__":
    main()
