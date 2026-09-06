# Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing

Manuscript for the *International Journal of Information and Education Technology* (IJIET, [www.ijiet.org](https://www.ijiet.org)). Diagnostic evaluation of Knowledge Tracing calibration on sparse concepts and a simulated mastery gate. Not a new KT architecture and not a classroom trial.

**T-KT** in the paper is a local Transformer KT baseline, not published SimpleKT.

The repository landing page is the parent [`README.md`](../README.md).

## IJIET OJS upload

Use **`IJIET_FINAL_REVISION/output/OJS_UPLOAD/`**.

| File | Role |
|------|------|
| Title-named `.doc` / `.docx` / `.pdf` | Named manuscript (editor) |
| Title-named `_blind.pdf` (optional `.doc`) | Double-blind review |
| `supplementary.pdf` | Tables S1–S10 |
| `code_for_review_anonymous.zip` | Anonymous code |
| `cover_letter_ijiet.txt` | Editor only |

Do not send reviewers the named PDF/Word.

## Repository layout

| Path | Role |
|------|------|
| `IJIET_FINAL_REVISION/` | Living Word/PDF (9 pages; allowed 8–10), figures, supplementary, locked analysis |
| `src/` `scripts/` `configs/` `tests/` | Training and evaluation code |
| `analysis/` `results/` | Numeric artifacts for reproduction |
| `data/` | Place official ASSISTments 2012, Junyi Academy, XES3G5M dumps here |

## Reproduce experiments

**LEVEL A** (no retrain): `bash scripts/rebuild_locked_tables.sh`

```bash
conda create -n sparse_kt python=3.9 -y
conda activate sparse_kt
pip install -r requirements.txt
```

See `IJIET_FINAL_REVISION/docs/how_to_reproduce.md`. Track A retrains local models and does **not** recreate locked ECE/FAR.

## License

Code: MIT. Manuscript text and figures: CC BY 4.0. See the parent `LICENSE`.
