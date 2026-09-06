#!/usr/bin/env python3
"""RQ3 → estimability/robustness; FAR is a probe, not an RQ. No numeric locks."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from docx import Document

HERE = Path(__file__).resolve().parent
FULL = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
BAK = HERE / "manuscript" / "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx.bak_pre_p0_rq3"

OLD_RQ = (
    "RQ2: How does calibration vary across KC-frequency strata and datasets? "
    "RQ3: When a fixed probability threshold is applied, does decision-error "
    "behavior differ between sparse and dense KCs?"
)
NEW_RQ = (
    "RQ2: How does probability calibration vary across train-only "
    "KC-frequency strata and datasets? RQ3: Under what dataset and concept "
    "conditions are sparse-concept calibration diagnostics estimable and "
    "informative, and are the conclusions robust to alternative train-only "
    "frequency cuts?"
)

OLD_ANS = (
    "On ASSISTments 2012, T-KT expected calibration error (ECE) increases "
    "from dense to sparse KCs, and a locked gate at τ=0.7 yields a higher "
    "FAR on sparse than on dense advances. The same ECE gradient is absent "
    "on Junyi, where the learner-based sparse stratum is empty, and is "
    "essentially absent for T-KT on XES3G5M."
)
NEW_ANS = (
    "On ASSISTments 2012, T-KT expected calibration error (ECE) increases "
    "from dense to sparse KCs (Limited sparse support, Table 7). The same "
    "ECE gradient is absent on Junyi, where the learner-based sparse "
    "stratum is empty, and is essentially absent for T-KT on XES3G5M. "
    "Three alternative train-only frequency cuts leave that ASSISTments "
    "T-KT rise positive (Supplementary Table S7). A locked gate at τ=0.7 "
    "is a simulated decision-error probe (Supplementary Tables S5–S6), "
    "not RQ3."
)


def set_para_text(p, new: str) -> None:
    if not p.runs:
        p.add_run(new)
        return
    p.runs[0].text = new
    for r in p.runs[1:]:
        r.text = ""


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if not BAK.exists():
        shutil.copy2(FULL, BAK)
    d = Document(str(FULL))
    hits = {"rq": 0, "ans": 0}
    for p in d.paragraphs:
        if OLD_RQ in p.text:
            set_para_text(p, p.text.replace(OLD_RQ, NEW_RQ, 1))
            hits["rq"] += 1
        elif OLD_ANS in p.text:
            set_para_text(p, p.text.replace(OLD_ANS, NEW_ANS, 1))
            hits["ans"] += 1
    if hits["rq"] != 1 or hits["ans"] != 1:
        raise SystemExit(f"hits={hits}")
    full = "\n".join(p.text for p in d.paragraphs)
    if "When a fixed probability threshold is applied" in full:
        raise SystemExit("old RQ3 remains")
    if "not RQ3" not in full or "Supplementary Table S7" not in full:
        raise SystemExit("new RQ3 answer missing")
    if "0.1136" not in full or "0.2280" not in full:
        raise SystemExit("ECE lock missing")
    if "TSCDA" in full:
        raise SystemExit("TSCDA reappeared")
    d.save(str(FULL))
    print("rq3 patched")


if __name__ == "__main__":
    main()
