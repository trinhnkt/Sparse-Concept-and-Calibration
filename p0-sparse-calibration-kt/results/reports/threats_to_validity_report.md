# Threats to Validity Report

**Date:** May 17, 2026  
**Section Revised:** `paper/sections/05_discussion_limitations.tex` (Threats to Validity)  
**Authorship/Review Standard:** Professor in Educational Data Mining, Knowledge Tracing, and IEEE Formatting  

---

## 1. Revision Objective
The objective was to restructure and expand the standard `Limitations` subsection into a structured, formal **"Threats to Validity"** subsection (Section V.C) following standard software engineering and data mining review frameworks.

---

## 2. Threats to Validity Dimensions Integrated
We categorized the scope and experimental constraints into four key threats:

1. **Internal Validity:**
   - *Risk:* Preprocessing bugs, split leakage, sequence alignment errors, baseline-specific configurations.
   - *Mitigation:* Unified data schema, early stopping on validation folds, automated seven-channel checklist L1--L7.

2. **Construct Validity:**
   - *Risk:* Do metrics represent real student masteries?
   - *Detail:* Relies on KC annotation quality, Q-matrix provenance, and multi-skill item strategies. Varying granularity of concepts in Junyi or ASSISTments acts as a direct confounder.

3. **External Validity:**
   - *Risk:* Generalization of findings to other educational datasets.
   - *Detail:* While ASSISTments 2012, Junyi, and XES3G5M are massive and diverse, empirical rankings under specific configurations must not be treated as universal truths without localized replication.

4. **Statistical Conclusion Validity:**
   - *Risk:* Precision and stability of strata-specific estimates.
   - *Detail:* Link very sparse strata metrics with standard deviations and exact sample counts to account for high volatility (small-sample constraint).
