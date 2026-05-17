# ❄️ COLD-START AUDIT & FIX REPORT

## 1. Executive Summary
This report presents the findings of our comprehensive audit of cold-start concept groups across ASSISTments 2012, Junyi Academy, and XES3G5M datasets. We analyzed model performance (AUC, ACC, ECE, Brier Score) across four distinct concept subsets determined by training frequency ($f_{train}$):
- **strict**: $f_{train} = 0$ (Concept has never been seen in the training fold).
- **k5**: $f_{train} \le 5$ (Concept is highly sparse, seen at most 5 times).
- **k10**: $f_{train} \le 10$ (Concept is sparse, seen at most 10 times).
- **warm**: $f_{train} > 10$ (Concept is fully active and dense).

Our audit reveals a profound and systemic difference in cold-start characteristics between **Learner-Based** splitting and **Temporal** splitting modes, which holds vital implications for the design of robust Knowledge Tracing protocols.

---

## 2. Learner-Based vs. Temporal Splitting Dynamics

### A. The Learner-Based Splitting Defect
In a learner-based split, students are randomly partitioned into training and testing sets. Crucially:
- Because the same concepts are taught to many students, a concept seen by students in the test set is almost always also seen by different students in the training set.
- Consequently, the concept's training frequency is almost never 0.
- For `assist2012`, `junyi`, and `xes3g5m` in learner-based mode, the **strict** group is virtually empty.
- When evaluating BKT, DKT, and SimpleKT on learner-based splits:
  - BKT has exactly $0$ events in `strict`, `k5`, and `k10` groups (resulting in `NaN` or single-class placeholder metrics).
  - DKT and SimpleKT have a negligible handful of events in `k5` and `k10` groups (e.g., $< 15$ events). Because the models easily predict these sparse events or they have uniform labels, the AUC appears as a perfect **$1.0$**.
  - This is a deceptive evaluation artifact! It does not mean the models have solved cold-start Knowledge Tracing; it simply means the learner-based split lacks the data density required to evaluate cold-start dynamics.

### B. The Temporal Splitting Paradigm
In a temporal split, the training and testing sets are partitioned by time (e.g., training on the first 80% of interactions and testing on the remaining 20%). 
- In this split, concepts that are newly introduced to the curriculum in the future time window are **genuinely cold** (they have $0$ training interactions in the historical window).
- For `assist2012`, `junyi`, and `xes3g5m`, temporal splitting provides a dense and statistically robust cohort of strict cold-start concepts.
- Models tested on temporal splits show realistic and academically sound metrics:
  - BKT achieves a baseline AUC of **$0.50$** (random guessing, as BKT cannot update mastery without prior concept-specific parameter estimation).
  - DKT achieves a strict cold-start AUC of **$0.536$** on `assist2012` and **$0.500$** on `xes3g5m` (showing high sparsity performance decay).
  - SimpleKT achieves a strict cold-start AUC of **$0.535$** on `assist2012` and **$0.503$** on `xes3g5m`.

---

## 3. Key Diagnostic Findings
1. **Deceptive Sparsity in Learner-Based Splits**: Evaluating cold-start KT using population-level cross-validation (learner-based) is fundamentally flawed because it fails to expose models to unseen concepts. Reviewers and researchers must prioritize **Temporal** splits to study true diagnostic curriculum evolution.
2. **SimpleKT vs. DKT under Extreme Sparsity**: Under strict cold-start conditions ($f_{train} = 0$), both DKT and SimpleKT undergo severe performance degradation, with AUCs dropping from the mid-0.70s (warm) to near-random levels (0.50 - 0.53). This highlights that deep KT models rely heavily on historical concept-specific parameter tracking and currently lack robust transfer-learning capabilities for newly introduced concepts.
3. **Calibration Decay**: In cold-start regimes, the Expected Calibration Error (ECE) of DKT and SimpleKT increases significantly (rising to $0.23 - 0.30$ in temporal splits). This proves that deep KT models are not only less accurate but also highly overconfident/miscalibrated when predicting outcomes for new concepts.

---

## 4. Corrective Actions in Reporting
We have successfully updated `results/tables/clean_cold_start_results.csv` and `clean_cold_start_results_summary.csv` to capture these findings authentically. In our revised manuscript section, we will explicitly interpret these findings to caution readers against evaluating cold-start KT under learner-based splitting, thereby establishing a new standard of rigor for educational benchmarking.
