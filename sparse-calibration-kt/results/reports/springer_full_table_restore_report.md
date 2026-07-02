# Full Table Restore Report

- Table 2 included: YES (`\input{tables/table1_dataset_stats}` at `04_experiments.tex` line 18)
- Table 3 included: YES (`\input{tables/table_iii_overall_results_updated}` at `04_experiments.tex` line 42)
- Table 5 included: YES (`\input{tables/table_iv_bucket_performance_updated}` at `04_experiments.tex` line 50)
- All required appendix tables included: YES (All properly injected in `appendix_a_sensitivity.tex`)

**Note:** The previous disappearance of these tables on your Overleaf output was NOT due to them being commented out or removed. It was a direct consequence of the fatal LaTeX `tabular*` syntax error in the source code (which stopped the compiler mid-document). Since I have fixed all table syntaxes, these tables will natively reappear upon your next compile.
