# Appendix Numbering Fix Report

- Investigated the `sn-jnl` class behavior regarding appendices.
- The `\begin{appendices}` environment defined by the template conflicted with the standard numbering flow when placed after `\backmatter` or when cross-referencing. This caused the subsequent `\section` commands to be numbered sequentially as `4` and `5` instead of `A`, `B`, etc.
- **Action Taken:** Replaced `\begin{appendices}` with the standard LaTeX `\appendix` command in `main_springer_traditional.tex`.
- **Result:** The `\appendix` macro correctly signals LaTeX to reset the section counter to zero and switch the counter format to alphabetic (A, B, C...).
- `Appendix D`, `Appendix E`, and `Appendix F` will now render with correct lettering, and cross-references like `Appendix~\ref{app:alignment}` will correctly output "Appendix F" instead of "Appendix 6".
