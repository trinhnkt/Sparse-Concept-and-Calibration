import os

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder"
main_file = os.path.join(folder, "main_springer_traditional.tex")
compact_file = os.path.join(folder, "main_springer_compact.tex")
supp_file = os.path.join(folder, "supplementary_springer.tex")

with open(main_file, "r", encoding="utf-8") as f:
    content = f.read()

# For compact: Replace \begin{appendices} ... \end{appendices} with a reference statement
# Actually, the user wants me to say "Detailed calibration breakdowns are provided in Supplementary Tables Sx-Sy."
# Let's just find \begin{appendices} and \end{appendices}
import re

compact_content = re.sub(
    r"\\begin\{appendices\}.*?\\end\{appendices\}",
    r"Detailed calibration breakdowns are provided in the Supplementary Material.",
    content,
    flags=re.DOTALL
)

with open(compact_file, "w", encoding="utf-8") as f:
    f.write(compact_content)

# For supplementary: Extract the preamble and add the appendices
preamble = content.split(r"\begin{document}")[0]
supp_content = preamble + r"""\begin{document}

\title[Supplementary Material]{Supplementary Material for: Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing}
\maketitle

\begin{appendices}
\input{appendix/appendix_a_sensitivity}
\end{appendices}

\end{document}
"""

with open(supp_file, "w", encoding="utf-8") as f:
    f.write(supp_content)

print("Generated compact and supplementary files.")
