#!/usr/bin/env python3
"""Rebuild anonymous review zip and copy README/zip into OJS slots. No numeric edits."""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from apply_a19_word import REVIEW_README_TEXT, REVIEW_ZIP, pack_review_zip  # noqa: E402

OJS = HERE / "output" / "OJS_UPLOAD"
SUB_OUT = HERE.parent / "IJIET_SUBMISSION" / "output"
README_REVIEW = HERE / "output" / "README_CODE_FOR_REVIEW.txt"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    README_REVIEW.write_text(REVIEW_README_TEXT, encoding="utf-8")
    log: list[str] = ["repack_zip"]
    pack_review_zip(log)
    with zipfile.ZipFile(REVIEW_ZIP) as zf:
        names = zf.namelist()
        texts = []
        for n in names:
            if n.lower().endswith((".txt", ".md", ".tex")):
                texts.append(zf.read(n).decode("utf-8", "replace"))
        blob = "\n".join(texts)
        if "JEDM" in blob or "jedm" in blob.lower():
            raise SystemExit("zip text still names JEDM")
        if "8-page" in blob:
            raise SystemExit("zip text still says 8-page")
        if "_archive/" in " ".join(names).lower():
            raise SystemExit("zip contains _archive")
    shutil.copy2(REVIEW_ZIP, OJS / "code_for_review_anonymous.zip")
    shutil.copy2(README_REVIEW, OJS / "README_CODE_FOR_REVIEW.txt")
    if SUB_OUT.is_dir():
        shutil.copy2(REVIEW_ZIP, SUB_OUT / "code_for_review_anonymous.zip")
    print("\n".join(log))
    print("zip_ok")


if __name__ == "__main__":
    main()
