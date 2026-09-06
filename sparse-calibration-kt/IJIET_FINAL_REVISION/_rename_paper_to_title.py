#!/usr/bin/env python3
"""Rename living paper Word/PDF to the manuscript title and retarget scripts."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from manuscript_paths import BLIND_STEM, NAMED_STEM  # noqa: E402

ROOT = HERE.parent
OLD_NEW = [
    ("main_ijiet_full.docx", f"{NAMED_STEM}.docx"),
    ("main_ijiet_full.doc", f"{NAMED_STEM}.doc"),
    ("main_ijiet_full.pdf", f"{NAMED_STEM}.pdf"),
    ("main_ijiet_blind.docx", f"{BLIND_STEM}.docx"),
    ("main_ijiet_blind.doc", f"{BLIND_STEM}.doc"),
    ("main_ijiet_blind.pdf", f"{BLIND_STEM}.pdf"),
]
RENAME_DIRS = [
    HERE / "manuscript",
    HERE / "output",
    HERE / "output" / "OJS_UPLOAD",
    ROOT / "IJIET_SUBMISSION" / "source",
    ROOT / "IJIET_SUBMISSION" / "output",
]
# Do not rewrite historical audit notes; only active scripts + submit docs.
TEXT_ROOTS = [
    HERE,
    ROOT / "Check list",
    ROOT / "IJIET_SUBMISSION",
]
TEXT_SUFFIXES = {".py", ".md", ".txt"}
SKIP_PARTS = {
    "_archive",
    ".git",
    "snapshots",
    "_export_tmp",
    "CHANGELOG_",
    "_rename_paper_to_title.py",
    "manuscript_paths.py",
}


def rename_files() -> list[str]:
    log = []
    for folder in RENAME_DIRS:
        if not folder.is_dir():
            continue
        for old_name, new_name in OLD_NEW:
            src = folder / old_name
            dst = folder / new_name
            if not src.is_file():
                continue
            if dst.exists() and dst.resolve() != src.resolve():
                dst.unlink()
            src.rename(dst)
            log.append(f"rename {src.relative_to(ROOT.parent)} -> {new_name}")
    return log


def rewrite_texts() -> list[str]:
    log = []
    for root in TEXT_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            s = str(path)
            if any(part in s for part in SKIP_PARTS):
                continue
            if path.name.startswith("CHANGELOG_"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            new = text
            for old_name, new_name in OLD_NEW:
                new = new.replace(old_name, new_name)
            if new != text:
                path.write_text(new, encoding="utf-8")
                log.append(f"edit {path.relative_to(ROOT)}")
    return log


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    log = rename_files() + rewrite_texts()
    print("\n".join(log) if log else "no changes")
    print(f"named={NAMED_STEM}")
    print(f"blind={BLIND_STEM}")


if __name__ == "__main__":
    main()
