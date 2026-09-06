# Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing

Manuscript for the *International Journal of Information and Education Technology* (IJIET, [www.ijiet.org](https://www.ijiet.org)). **DOI: pending.**

A reproducible protocol and calibration diagnostic for sparse knowledge components: train-only strata, occupancy-aware reporting, ECE/Brier, reliability diagrams, L1–L7 leakage control, and a frozen one-command table rebuild. It is not a new Knowledge Tracing architecture and not a classroom trial.

**T-KT** in the paper is a local Transformer KT baseline, not published SimpleKT.

## Paper

Named and double-blind PDFs (9 pages; IJIET allows 8–10) live in [`sparse-calibration-kt/IJIET_FINAL_REVISION/output/OJS_UPLOAD/`](sparse-calibration-kt/IJIET_FINAL_REVISION/output/OJS_UPLOAD/).

- [Named PDF](sparse-calibration-kt/IJIET_FINAL_REVISION/output/OJS_UPLOAD/Reproducible%20Sparse-Concept%20and%20Calibration%20Diagnostics%20for%20Knowledge%20Tracing.pdf)
- [Blind PDF](sparse-calibration-kt/IJIET_FINAL_REVISION/output/OJS_UPLOAD/Reproducible%20Sparse-Concept%20and%20Calibration%20Diagnostics%20for%20Knowledge%20Tracing_blind.pdf)
- Supplementary Tables S1–S10: `supplementary.pdf` in the same folder
- Locked numbers: [`sparse-calibration-kt/IJIET_FINAL_REVISION/audit/SCIENTIFIC_LOCKS.md`](sparse-calibration-kt/IJIET_FINAL_REVISION/audit/SCIENTIFIC_LOCKS.md)

## Datasets

Raw interaction logs are **not** in this repository. Obtain them from the original providers and place dumps under `sparse-calibration-kt/data/`:

1. [ASSISTments 2012](https://sites.google.com/site/assistmentsdata/)
2. [Junyi Academy](https://pslcdatashop.web.cmu.edu/)
3. [XES3G5M](https://github.com/pykt-team/pykt-toolkit)

## Reproduce

**LEVEL A** (review-facing): rebuild locked tables from frozen CSVs. This does **not** retrain models and does **not** change ASSISTments T-KT ECE `0.1136` / `0.2280` or FAR `0.196` / `0.268`.

```bash
cd sparse-calibration-kt
bash scripts/rebuild_locked_tables.sh
# Windows: scripts/rebuild_locked_tables.ps1
```

**Track A** retrains local IRT / DKT / T-KT. It does **not** recreate those locked cells. Details: [`sparse-calibration-kt/IJIET_FINAL_REVISION/docs/how_to_reproduce.md`](sparse-calibration-kt/IJIET_FINAL_REVISION/docs/how_to_reproduce.md).

```bash
conda create -n sparse_kt python=3.9 -y
conda activate sparse_kt
pip install -r sparse-calibration-kt/requirements.txt
```

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

- Code: [MIT](LICENSE)
- Manuscript text, figures, and supplementary tables: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
