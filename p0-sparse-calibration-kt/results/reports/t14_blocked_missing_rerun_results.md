# T14 Blocked: Missing Rerun Results

This report documents why the manuscript tables, figures, and results interpretation cannot be updated yet.

## 1. Blocking Criteria Status

As per the protocol, updating the paper is blocked due to incomplete re-run results:
- **`overall_results_rerun.csv`**: Template only (49 bytes, headers initialized but no data).
- **`bucket_performance_rerun.csv`**: Template only (69 bytes, headers initialized but no data).
- **`calibration_by_bucket_rerun.csv`**: Template only (73 bytes, headers initialized but no data).
- **`cold_start_temporal_rerun.csv`**: Template only (59 bytes, headers initialized but no data).
- **`experiment_run_status.csv`**: Template only (21 bytes, headers initialized but no data).

## 2. Audit of Rerun Summary (`rerun_summary_report.md`)

We have inspected the rerun manager report to determine the project status:
- **Completeness**: 0 of 90 runs have been executed. The execution loop is pending cluster resources due to massive hardware requirements (~360 GPU hours total).
- **Classical Baseline Chosen**: `irt_1pl` (IRT 1-Parameter Logistic).
- **Temporal Split Debug**: The prediction-label misalignment bug has been fixed in the pipeline code, but actual metrics have not been re-computed.
- **Failures/Pending Jobs**: All 90 runs are marked as pending/needs retry.
- **Manual Review Needed**: Yes, once the cluster completes the 90 runs, overall and stratum-level calibration metrics must be checked.

## 3. Resolution Plan
The paper updates (Tables III-IX, Figures 2-3, and Section IV texts) are deferred until the re-run jobs are successfully executed and the CSVs in `results/tables/` are populated with actual data.

- **Status**: **BLOCKED_BY_INCOMPLETE_RERUN_RESULTS**
- **Action Required**: Run the pipeline execution scripts on a GPU cluster to populate the rerun tables.
