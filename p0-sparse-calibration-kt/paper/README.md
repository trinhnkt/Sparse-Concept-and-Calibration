
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
- Table I: Leakage & Predictive Sanity Audit Checklist (L1--L8)
- Table II: Dataset statistics
- Table III: Overall baseline results
- Table IV: Performance by KC stratum (Learner-based)
- Table V: Calibration by KC stratum (Learner-based)
- Table VI: Limited cold-start KC diagnostics
- Table X: Detailed calibration results (Learner-based)
- Table XI: Calibration breakdown by stratum (Temporal)
- Table XII: Diagnostic Interpretation Guide
- Figure 1: Diagnostic pipeline
- Figure 2/3: Reliability diagrams and KC bucket distribution

## Data preparation
The learner-based and temporal splits provide 5-fold cross-validation or 5 seeds (seeds 42, 2024, 2025, 2026, 2027). You can run the script to regenerate splits if needed:
```
python scripts/create_new_folds.py
```

## Notes for submission
- Use cautious language: “under our experimental conditions”, “may differ”, “to our knowledge”.
- Do not write “we propose a new KT model” or “we solve cold-start KT”.
- Verify all 2024--2026 related work before final submission.
