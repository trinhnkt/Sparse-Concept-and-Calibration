#!/usr/bin/env python3
"""Snapshot living IJIET pack into IJIET_FINAL_v3/. Does not edit the living paper."""
from __future__ import annotations

import hashlib
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REV = ROOT / "IJIET_FINAL_REVISION"
DEST = ROOT / "IJIET_FINAL_v3"
TODAY = date(2026, 9, 6).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_file(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise SystemExit(f"missing {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree_files(src: Path, dst: Path, suffixes: tuple[str, ...] | None = None) -> int:
    n = 0
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if suffixes and p.suffix.lower() not in suffixes:
            continue
        if p.name.startswith(".") or p.suffix.lower() in {".aux", ".log", ".pyc"}:
            continue
        rel = p.relative_to(src)
        if any(part in {"__pycache__", "a9"} for part in rel.parts):
            continue
        copy_file(p, dst / rel)
        n += 1
    return n


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if DEST.exists():
        raise SystemExit(f"{DEST} already exists — refuse to overwrite a freeze")

    blind = REV / "output" / "main_ijiet_blind.pdf"
    full = REV / "output" / "main_ijiet_full.pdf"
    si_pdf = REV / "output" / "supplementary.pdf"
    for p in (blind, full, si_pdf):
        if not p.is_file():
            raise SystemExit(f"missing baseline {p}")

    # manuscript — baseline PDF is the living blind file, unchanged
    for name in (
        "main_ijiet_blind.docx",
        "main_ijiet_blind.doc",
        "main_ijiet_full.docx",
        "main_ijiet_full.doc",
    ):
        copy_file(REV / "manuscript" / name, DEST / "manuscript" / name)
    copy_file(blind, DEST / "manuscript" / "main_ijiet_blind.pdf")
    copy_file(full, DEST / "manuscript" / "main_ijiet_full.pdf")
    copy_file(si_pdf, DEST / "manuscript" / "supplementary.pdf")
    copy_file(blind, DEST / "manuscript" / "BASELINE_main_ijiet_blind.pdf")

    # scripts — result / freeze rebuild only (no historical apply_a* mutators)
    script_files = [
        ROOT / "scripts" / "rebuild_locked_tables.sh",
        ROOT / "scripts" / "rebuild_locked_tables.ps1",
        ROOT / "scripts" / "p0_rebuild_locked_tables.py",
        ROOT / "scripts" / "p0_si_threecut.py",
        ROOT / "scripts" / "p0_official_simplekt_ece.py",
        ROOT / "scripts" / "reproduce_one_dataset.sh",
        ROOT / "scripts" / "reproduce_one_dataset.ps1",
        REV / "_p0_compile_si.py",
        REV / "_p0_rebuild_blind.py",
        REV / "_export_a31_pdfs.py",
    ]
    for src in script_files:
        copy_file(src, DEST / "scripts" / src.name)

    # results — table-backing CSVs / JSON only
    analysis_ok = {".csv", ".txt", ".md", ".json"}
    copy_tree_files(REV / "analysis", DEST / "results" / "analysis", tuple(analysis_ok))
    copy_tree_files(
        REV / "a2b" / "analysis",
        DEST / "results" / "a2b_analysis",
        (".csv", ".txt", ".md"),
    )
    copy_file(
        ROOT / "analysis" / "four_partition" / "summary_4part_overall.csv",
        DEST / "results" / "four_partition" / "summary_4part_overall.csv",
    )
    for name in (
        "p0_official_simplekt_assist_ece.json",
        "p0_si_threecut.json",
    ):
        copy_file(ROOT / "results" / "reports" / name, DEST / "results" / "reports" / name)
    for p in (ROOT / "results" / "reports").glob("p0_simplekt_official_assist2012_*.json"):
        copy_file(p, DEST / "results" / "reports" / p.name)
    copy_tree_files(ROOT / "results" / "tables", DEST / "results" / "tables")
    copy_tree_files(REV / "tables", DEST / "results" / "printed_tables", (".csv", ".tex", ".md"))

    # supplementary + figures
    copy_tree_files(REV / "supplementary", DEST / "supplementary", (".tex", ".md", ".pdf"))
    copy_tree_files(REV / "figures", DEST / "figures", (".png", ".py"))

    # audit
    copy_file(REV / "audit" / "SCIENTIFIC_LOCKS.md", DEST / "audit" / "SCIENTIFIC_LOCKS.md")
    copy_file(REV / "audit" / "CHANGELOG_P0.md", DEST / "audit" / "CHANGELOG_P0.md")

    # reproducibility
    copy_file(REV / "docs" / "how_to_reproduce.md", DEST / "reproducibility" / "how_to_reproduce.md")
    copy_file(ROOT / "requirements.txt", DEST / "reproducibility" / "requirements.txt")
    copy_file(REV / "output" / "README_CODE_FOR_REVIEW.txt", DEST / "reproducibility" / "README_CODE_FOR_REVIEW.txt")
    copy_file(REV / "analysis" / "leakage_audit_log.csv", DEST / "reproducibility" / "leakage_audit_log.csv")

    blind_hash = sha256(DEST / "manuscript" / "main_ijiet_blind.pdf")
    full_hash = sha256(DEST / "manuscript" / "main_ijiet_full.pdf")
    si_hash = sha256(DEST / "manuscript" / "supplementary.pdf")
    (DEST / "reproducibility" / "BASELINE_MANIFEST.txt").write_text(
        "\n".join(
            [
                f"freeze_date={TODAY}",
                "source=IJIET_FINAL_REVISION (living pack at freeze)",
                "baseline_pdf=manuscript/main_ijiet_blind.pdf",
                "also_copied_as=manuscript/BASELINE_main_ijiet_blind.pdf",
                "pages_named_blind=9/9",
                f"sha256_main_ijiet_blind.pdf={blind_hash}",
                f"sha256_main_ijiet_full.pdf={full_hash}",
                f"sha256_supplementary.pdf={si_hash}",
                "do_not_overwrite_baseline_pdf",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"froze {DEST}")
    print(f"blind sha256 {blind_hash}")


if __name__ == "__main__":
    main()
