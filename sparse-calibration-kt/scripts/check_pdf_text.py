import sys
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed yet")
    sys.exit(0)

pdf_path = "paper/figures/figure1_pipeline.pdf"
doc = fitz.open(pdf_path)
page = doc[0]

# Print all text instances
text_instances = page.get_text("blocks")
for inst in text_instances:
    print(inst[4])
