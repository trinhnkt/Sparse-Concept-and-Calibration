#!/usr/bin/env python3
"""Compile supplementary.tex twice; copy PDF to output/."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUP_TEX = HERE / "supplementary" / "supplementary.tex"
SUP_PDF = HERE / "output" / "supplementary.pdf"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = shutil.which("pdflatex")
    if not cmd:
        raise SystemExit("pdflatex missing")
    for _ in range(2):
        proc = subprocess.run(
            [cmd, "-interaction=nonstopmode", "-halt-on-error", SUP_TEX.name],
            cwd=str(SUP_TEX.parent),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode != 0:
            print(proc.stdout[-2000:])
            print(proc.stderr[-500:])
            raise SystemExit("pdflatex supplementary failed")
    built = SUP_TEX.with_suffix(".pdf")
    shutil.copy2(built, SUP_PDF)
    print(f"supplementary={SUP_PDF}")


if __name__ == "__main__":
    main()
