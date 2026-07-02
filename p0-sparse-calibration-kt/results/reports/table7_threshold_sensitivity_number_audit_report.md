# Table 7 Threshold Sensitivity Audit Report
- Source CSV/log for Table 7: results/tables/sensitivity_analysis.csv
- Split mode used: learner_based
- Whether XES3G5M dense AUC is consistent with Table 5: YES (Both now use the leak-free _rerun predictions. The previous discrepancy occurred because sensitivity analysis grouped an older leak-affected file (seed 42, AUC ~ 0.91) while Table 5 used the rerun file. This is now fully synchronized.)
- Whether XES3G5M IRT dense ECE is consistent with Table 10: YES
- Corrections applied: Re-ran sensitivity analysis specifically mapping out old leak-affected files and prioritizing the newest _rerun predictions across all folds.
- Remaining numbers to verify: None.
