# IJIET_FINAL_REVISION

Living IJIET manuscript (named + blind, 9 pages; allowed 8–10). Edit Word in `manuscript/`, then pack `output/OJS_UPLOAD/`.

| Path | Role |
|------|------|
| `manuscript/` | Named and blind Word |
| `output/OJS_UPLOAD/` | Files to upload to IJIET OJS |
| `analysis/` | Locked numeric artifacts |
| `audit/SCIENTIFIC_LOCKS.md` | Frozen ECE/FAR/XES cells |
| `docs/how_to_reproduce.md` | LEVEL A vs Track A |
| `supplementary/` | Tables S1–S10 sources |
| `figures/` | Fig. 1–3 |
| `tables/` | Numeric table copies |
| `a2b/` | Masked XES3G5M series (source of truth for XES ECE) |

Target: named and blind files use the paper title (`manuscript_paths.py`). Rebuild both with `build_a16_double_blind.py` after named edits.

## Submit here

OJS files: `output/OJS_UPLOAD/` (see `README_SUBMIT.md` there).
