# Experimental Consistency Check Report

- **Methodology:** A strict regex assertion script was run against all LaTeX tables to verify that the core numerical results were neither manually altered nor unintentionally corrupted.
- **Results:**
  - **Table 3:** ALL target metrics PASSED (e.g., ASSISTments DKT 0.6980, Junyi DKT 0.7317, XES3G5M DKT 0.8170).
  - **Table 5:** ALL target metrics PASSED (e.g., XES3G5M dense/sparse/very sparse exactly match constraints).
  - **Table 6:** ALL target metrics PASSED (e.g., warm temporal AUCs for ASSISTments, Junyi, and XES3G5M match constraints).
  - **Figure 3/Table C5:** ALL target metrics PASSED (e.g., Junyi SimpleKT dense ECE 0.0889 N=3072767, very sparse ECE 0.0841 N=2545).
- **Conclusion:** Perfect numerical consistency. Zero data drift.
