
# Overleaf Template: P0 Sparse-Concept and Calibration Diagnostics for KT

## Paper title
**Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing**

## Recommended use
1. Go to Overleaf → New Project → Upload Project.
2. Upload this ZIP file.
3. Set compiler to **pdfLaTeX**.
4. Compile `main.tex`.
5. Replace all `[TODO: ...]` placeholders with real experimental results.

## Scope
This template is designed for a **protocol / diagnostic / resource paper**. It intentionally avoids claiming a new KT model. Do not add SSL, GNN, graph augmentation, learning path recommendation, or distillation into the main contribution of P0.

## Main result objects expected
- Table 1: dataset statistics
- Table 2: leakage audit L1--L7
- Table 3: overall baseline results
- Table 4: performance by KC stratum
- Table 5: calibration by KC stratum
- Table 6: limited cold-start KC diagnostics
- Figure 1: diagnostic pipeline
- Figure 2/3: reliability diagrams and KC bucket distribution

## Data preparation
The original learner-based splits only contain 3 folds (seeds 42, 2024, 2025). To perform the full 5-fold cross-validation, run the script to generate the missing folds (seeds 2026, 2027):
```
python scripts/create_new_folds.py
```

## Notes for submission
- Use cautious language: “under our experimental conditions”, “may differ”, “to our knowledge”.
- Do not write “we propose a new KT model” or “we solve cold-start KT”.
- Verify all 2024--2026 related work before final submission.
