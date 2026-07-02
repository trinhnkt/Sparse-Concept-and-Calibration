# 📝 TABLE IV & RQ1 CONSISTENCY REPORT

## 1. Context and Problem Statement
During peer review, a critical discrepancy was identified in the interpretation of **Research Question 1 (RQ1)**. Specifically:
*   The manuscript text claimed that for **DKT** on the **ASSISTments 2012** dataset, the AUC decreases from the dense stratum to the very sparse stratum.
*   However, the actual empirical results in **Table IV** showed:
    *   **DKT Dense Stratum AUC:** $0.6974 \pm 0.0011$
    *   **DKT Very Sparse Stratum AUC:** $0.9259 \pm 0.1283$
*   This represents a substantial contradiction (0.9259 is much higher than 0.6974), which severely undermines the credibility of the manuscript's empirical claims.

---

## 2. Empirical Verification
An empirical check of all deep baseline models (DKT and SimpleKT) on the very sparse stratum shows that their AUC values are indeed higher than or comparable to those of the dense stratum:
1.  **ASSISTments 2012 (Learner-based)**:
    *   DKT: Dense $0.6974$ vs. Very Sparse $0.9259$
    *   SimpleKT: Dense $0.6813$ vs. Very Sparse $0.9222$
2.  **XES3G5M (Learner-based)**:
    *   DKT: Dense $0.8190$ vs. Very Sparse $0.8801$
    *   SimpleKT: Dense $0.7553$ vs. Very Sparse $0.8515$

### Why is very sparse AUC so high?
The very sparse stratum contains concepts that appear extremely rarely in the training dataset ($f_{train} \le 5$ times). In a random learner-based split, the number of test events for these concepts is extremely small (for ASSISTments 2012, there are only 11 KCs in this bucket with a handful of test events). When evaluating AUC on very few test events, the metric suffers from severe **sample-size instability**:
*   A single student who answers a sequence of very sparse KCs correctly or incorrectly can artificially inflate the ROC curve to a near-perfect area under the curve ($>0.90$).
*   This high AUC is statistically unreliable, as indicated by the very large standard deviation of the very sparse AUC values (e.g., $\pm 0.1283$ for DKT).

---

## 3. Resolution and Text Revision
To resolve this contradiction and ensure a highly rigorous, academically cautious interpretation, we have made the following updates:
1.  **Corrected Manuscript Interpretation**: We removed the erroneous claim that AUC falls from dense to very sparse.
2.  **Added Scientific Caveat**: We rewrote the interpretation to explain the high AUC of very sparse strata as an artifact of small-sample instability rather than genuine model superiority on rare concepts. We emphasized that aggregate AUC in sparse concepts can be misleadingly high, which highlights the crucial importance of our **calibration-aware diagnostics (ECE and Brier score decomposition)**.
3.  **Added Footnote / Table Note**: We added a clear warning to Table IV: *"Note: Very sparse AUC should be interpreted cautiously due to limited test events."*

### Revised Manuscript Text in Section IV-C (RQ1):
> *"Bucket-level results reveal heterogeneous behavior across strata. In some very sparse cells, AUC can be unstable because of limited sample sizes; therefore, calibration and sample-size-aware diagnostics are necessary. Specifically, while the apparent AUC of DKT on ASSISTments 2012 very sparse stratum reaches $0.9259 \pm 0.1283$, this is driven by the small size of the evaluation cohort and should be interpreted cautiously, as the high standard deviation indicates high instability."*
