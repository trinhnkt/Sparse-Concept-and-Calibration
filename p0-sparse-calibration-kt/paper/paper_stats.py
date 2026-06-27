import os
import re

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\sections"
sections = ["01_introduction.tex", "02_related_work.tex", "03_protocol.tex", "04_experiments.tex", "05_discussion_limitations.tex", "06_conclusion.tex"]

print("=== PAPER REVIEW STATISTICS ===")

total_words = 0
for sec in sections:
    filepath = os.path.join(folder, sec)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # remove latex commands roughly
            text = re.sub(r'\\[a-zA-Z]+\{.*?\}', '', content)
            text = re.sub(r'\\[a-zA-Z]+', '', text)
            words = len(text.split())
            total_words += words
            
            # find long sentences
            sentences = re.split(r'[.!?]\s+', text)
            long_sentences = [s for s in sentences if len(s.split()) > 45]
            
            print(f"- {sec}: {words} words, {len(long_sentences)} long sentences (>45 words)")

print(f"\nTotal estimated word count (excluding commands/preamble): {total_words}")
