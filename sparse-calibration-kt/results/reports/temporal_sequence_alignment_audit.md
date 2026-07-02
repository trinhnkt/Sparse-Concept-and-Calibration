# Sequence Alignment Audit
The previous bug 'Prediction-Label Misalignment' was caused by groupby operations not preserving the row order when evaluating on test sets. This misalignment led to temporal AUC dropping to ~0.50.
This bug has already been FIXED in the project.
