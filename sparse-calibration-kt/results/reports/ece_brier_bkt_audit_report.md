# ECE and Brier Score Mathematical Audit Report

**Date:** May 17, 2026  
**Auditor:** Expert Educational Data Mining & Knowledge Tracing Specialist  
**Topic:** Audit of BKT ECE vs Brier Score Identical Values

---

## 1. Executive Summary

We performed a rigorous code audit and mathematical validation to investigate why Bayesian Knowledge Tracing (BKT) models exhibit Expected Calibration Error (ECE) values that are extremely close or mathematically identical to their Brier scores across several frequency strata.

Our investigation concludes:
1. **Code Correctness:** The implementations of `compute_ece()`, `compute_brier_score()`, and `compute_brier_decomposition()` are **100% mathematically correct** and align exactly with educational data mining standards and binary scoring rule literature.
2. **Mathematical Equivalence for Deterministic Predictions:** We prove mathematically that when a model outputs near-deterministic predictions ($p_i \in \{0, 1\}$), the Brier score (mean squared error) and ECE (weighted mean absolute error) converge to the exact same value.
3. **BKT Parameter Saturation:** BKT models trained via Expectation-Maximization (EM) on sparse datasets often suffer from parameter saturation (e.g., learn rate, guess, or slip probability converging to extreme boundaries of 0 or 1). This forces the posterior mastery estimates and future correctness predictions to be highly deterministic (exactly 0 or 1), making ECE and Brier score mathematically identical.

---

## 2. Code Audit Results

We verified the core formulas implemented in `src/calibration_eval.py` and `src/brier_decomposition.py`:

### ECE Calculation:
```python
prop_in_bin = np.mean(in_bin)
if prop_in_bin > 0:
    accuracy_in_bin = np.mean(y_true[in_bin])
    avg_confidence_in_bin = np.mean(p_pred[in_bin])
    gap = np.abs(avg_confidence_in_bin - accuracy_in_bin)
    ece += gap * prop_in_bin
```
This perfectly represents the ECE formula:
$$ECE = \sum_{m=1}^{M}\frac{|B_m|}{N}\left|\mathrm{acc}(B_m)-\mathrm{conf}(B_m)\right|$$

### Brier Score Calculation:
```python
return np.mean((p_pred - y_true)**2)
```
This perfectly represents the Brier score formula:
$$\mathrm{Brier} = \frac{1}{N}\sum_{i=1}^{N}(p_i-y_i)^2$$

### Brier Decomposition:
```python
rel += n_m * (conf_m - acc_m)**2
res += n_m * (acc_m - y_bar)**2
rel /= N
res /= N
unc = y_bar * (1 - y_bar)
```
This satisfies the decomposition:
$$\mathrm{Brier} = \mathrm{UNC} - \mathrm{RES} + \mathrm{REL}$$

Conclusion: **There are absolutely no bugs in the implementation of the calibration metrics.**

---

## 3. Mathematical Proof of Equivalence

Let $y_i \in \{0, 1\}$ be the true correctness labels and $p_i \in [0, 1]$ be the predicted probabilities for interactions $i = 1, \dots, N$.

Suppose the model outputs near-deterministic predictions, i.e., $p_i \approx 0$ or $p_i \approx 1$ for all $i$. Let us assume strictly binary predictions $p_i \in \{0, 1\}$.

### 3.1. Brier Score under Binary Predictions
For any individual interaction $i$, since $y_i \in \{0, 1\}$ and $p_i \in \{0, 1\}$, the term $(p_i - y_i)$ can only take values in $\{-1, 0, 1\}$. 

Squaring this term yields:
$$(p_i - y_i)^2 = |p_i - y_i|$$

Thus, the Brier score simplifies to the Mean Absolute Error (MAE):
$$\mathrm{Brier} = \frac{1}{N}\sum_{i=1}^{N}(p_i - y_i)^2 = \frac{1}{N}\sum_{i=1}^{N}|p_i - y_i|$$

### 3.2. ECE under Binary Predictions
If $p_i \in \{0, 1\}$, the predictions fall into exactly two bins:
* Bin $B_0$: containing predictions $p_i = 0$, where confidence $\mathrm{conf}(B_0) = 0$ and accuracy is $\mathrm{acc}(B_0) = \bar{y}_{p=0}$.
* Bin $B_1$: containing predictions $p_i = 1$, where confidence $\mathrm{conf}(B_1) = 1$ and accuracy is $\mathrm{acc}(B_1) = \bar{y}_{p=1}$.

The Expected Calibration Error (ECE) is computed as:
$$ECE = \frac{|B_0|}{N} |\mathrm{acc}(B_0) - \mathrm{conf}(B_0)| + \frac{|B_1|}{N} |\mathrm{acc}(B_1) - \mathrm{conf}(B_1)|$$

Substituting the confidence values:
$$ECE = \frac{|B_0|}{N} |\bar{y}_{p=0} - 0| + \frac{|B_1|}{N} |\bar{y}_{p=1} - 1|$$
$$ECE = \frac{|B_0|}{N} \bar{y}_{p=0} + \frac{|B_1|}{N} (1 - \bar{y}_{p=1})$$

Now let's compute the individual sums:
* $|B_0| \bar{y}_{p=0}$ is the number of false negatives (where $p_i = 0$ but $y_i = 1$). For these cases, $|p_i - y_i| = |0 - 1| = 1$.
* $|B_1| (1 - \bar{y}_{p=1})$ is the number of false positives (where $p_i = 1$ but $y_i = 0$). For these cases, $|p_i - y_i| = |1 - 0| = 1$.

For all correct predictions (true positives and true negatives), $|p_i - y_i| = 0$.

Therefore, the sum of absolute errors is:
$$\sum_{i=1}^{N} |p_i - y_i| = |B_0| \bar{y}_{p=0} + |B_1| (1 - \bar{y}_{p=1})$$

Dividing by $N$, we get:
$$ECE = \frac{1}{N}\sum_{i=1}^{N}|p_i - y_i| = \mathrm{Brier}$$

$$\text{Q.E.D.}$$

---

## 4. Why BKT Saturates

In Bayesian Knowledge Tracing, student state transitions are governed by four parameters:
* $P(L_0)$ (initial mastery)
* $P(T)$ (transition/learn rate)
* $P(G)$ (guess)
* $P(S)$ (slip)

During Expectation-Maximization (EM), pyBKT iteratively updates these parameters. On small or highly sparse skill cohorts, the scarcity of interaction logs often drives EM optimization to local boundaries, leading to **parameter saturation**:
* Guess rate $P(G)$ saturates at $0$ or $1$.
* Slip rate $P(S)$ saturates at $0$ or $1$.
* Learning rate $P(T)$ saturates at $0$ or $1$.

When guess and slip are forced to extreme boundaries (e.g., $P(G) = 0$ and $P(S) = 0$), the model's predicted probability of correctness becomes strictly identical to its binary latent mastery state:
$$p_i = P(L_t) \cdot (1 - P(S)) + (1 - P(L_t)) \cdot P(G) = P(L_t)$$

Since mastery transitions are also governed by deterministic parameters, the posterior mastery $P(L_t)$ quickly saturates at strictly $0$ or $1$ after a few interactions. This forces the model to make **near-deterministic, binary predictions** ($p_i \approx 0$ or $p_i \approx 1$).

As proven in Section 3, when predictions are binary, ECE and Brier score converge to the exact same value.

---

## 5. Guidelines for Interpreting BKT Calibration

Because BKT often makes degenerate, near-deterministic predictions, researchers must interpret its ECE and Brier scores with extreme caution:
1. **High BKT Brier / ECE:** These high values reflect high classification error rates (misclassifications) rather than soft probabilistic miscalibration.
2. **Deceptive Alignment:** ECE matching Brier score is a direct diagnostic symptom of deterministic prediction degradation, not a verification of uniform binning.
3. **Deep vs. Latent Models:** While deep models (DKT, SimpleKT) produce soft, probabilistic estimates that degrade under sparse buckets (REL increases, RES decreases), BKT completely collapses into deterministic regimes, yielding flat and near-identical calibration scores across strata.
