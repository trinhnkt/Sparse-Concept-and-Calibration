# Appendix Heading Format Check Report
Appendix sections use the standard \section{...} syntax inside an ppendix environment block.
In standard LaTeX and JEDM class templates, the ppendix command automatically swaps section numbering to alphabetic characters (Appendix A, Appendix B, etc.). Manually hardcoding \section*{Appendix A. ...} risks breaking the ef{app:sensitivity} cross-references elsewhere in the document.
Therefore, the headings are kept clean and structurally sound.
