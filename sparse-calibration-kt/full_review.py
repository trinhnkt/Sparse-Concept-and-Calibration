import re
import glob
import os

jedm_dir = 'jedm_upload_folder'
tex_files = glob.glob(os.path.join(jedm_dir, '**/*.tex'), recursive=True)
tex_files.append(os.path.join(jedm_dir, 'main_jedm.tex'))

# 1. Collect all labels and refs
labels = set()
refs = []
cites = set()

for f in tex_files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'\\label\{([^}]+)\}', content):
        labels.add(m.group(1))
    for m in re.finditer(r'\\ref\{([^}]+)\}', content):
        refs.append((os.path.basename(f), m.group(1)))
    for m in re.finditer(r'\\cite\{([^}]+)\}', content):
        for key in m.group(1).split(','):
            cites.add(key.strip())

# 2. Check bbl
bbl_path = os.path.join(jedm_dir, 'references.bbl')
bib_keys = set()
with open(bbl_path, 'r', encoding='utf-8') as fh:
    bbl_content = fh.read()
for m in re.finditer(r'\\bibitem\{([^}]+)\}', bbl_content):
    bib_keys.add(m.group(1))

# 3. Check figures exist
fig_dir = os.path.join(jedm_dir, 'figures')
fig_files = set(os.listdir(fig_dir)) if os.path.isdir(fig_dir) else set()

fig_refs = []
for f in tex_files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'\\includegraphics.*?\{([^}]+)\}', content):
        fig_refs.append((os.path.basename(f), m.group(1)))

print("=" * 60)
print("JEDM MANUSCRIPT COMPREHENSIVE REVIEW")
print("=" * 60)

# Check 1: Labels
print("\n[1] CROSS-REFERENCES")
unresolved = [(f, r) for f, r in refs if r not in labels]
if unresolved:
    for f, r in unresolved:
        print(f"  FAIL: \\ref{{{r}}} in {f} -> NO MATCHING \\label")
else:
    print(f"  PASS: All {len(set(r for _,r in refs))} unique refs resolve to {len(labels)} labels")

# Check 2: Citations
print("\n[2] CITATIONS")
missing_cites = cites - bib_keys
if missing_cites:
    for c in missing_cites:
        print(f"  FAIL: \\cite{{{c}}} -> NOT IN .bbl")
else:
    print(f"  PASS: All {len(cites)} citations resolve to {len(bib_keys)} bibitem entries")

# Check 3: Figures
print("\n[3] FIGURE FILES")
for f, fig_path in fig_refs:
    fig_basename = os.path.basename(fig_path)
    if fig_basename in fig_files:
        print(f"  PASS: {fig_basename} (referenced in {f})")
    else:
        print(f"  FAIL: {fig_basename} MISSING (referenced in {f})")

# Check 4: Pelanek
print("\n[4] PELANEK ACCENT")
if "Pel{\\'a}nek" in bbl_content or "Pel{\\'{a}}nek" in bbl_content:
    print("  FAIL: Accented Pelanek still in .bbl")
else:
    print("  PASS: No accented Pelanek in .bbl")

# Check 5: Bad patterns
print("\n[5] BAD PATTERNS SCAN")
bad_patterns = {
    'Table ??': r'Table\s*\?\?',
    'Figure ??': r'Figure\s*\?\?',
    'Appendix ??': r'Appendix\s*\?\?',
    'DeepKT': r'DeepKT',
    'accurately isolates': r'accurately isolates',
    'never appeared in the test folds': r'never appeared in the test folds',
    'publicly available on the GitHub': r'publicly available on the GitHub',
    'Appendix Appendix': r'Appendix\s+Appendix',
}
for f in tex_files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for name, pat in bad_patterns.items():
        if re.search(pat, content, re.IGNORECASE):
            print(f"  FAIL: '{name}' found in {os.path.basename(f)}")

all_content = ''
for f in tex_files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fh:
        all_content += fh.read()

found_any = False
for name, pat in bad_patterns.items():
    if re.search(pat, all_content, re.IGNORECASE):
        found_any = True
if not found_any:
    print("  PASS: No bad patterns found")

# Check 6: Section structure of 04_experiments.tex
print("\n[6] 04_EXPERIMENTS.TEX STRUCTURE")
exp_path = os.path.join(jedm_dir, 'sections', '04_experiments.tex')
with open(exp_path, 'r', encoding='utf-8') as fh:
    exp_content = fh.read()

required_sections = [
    ('RQ1', r'\\subsection\{RQ1'),
    ('RQ2', r'\\subsection\{RQ2'),
    ('RQ3', r'\\subsection\{RQ3'),
    ('Figure 2 (strata_dist)', r'\\label\{fig:strata_dist\}'),
    ('Figure 3 (reliability)', r'\\label\{fig:reliability_junyi_temporal\}'),
    ('Table III input', r'\\input\{tables/table_iii'),
    ('Table IV input', r'\\input\{tables/table_iv'),
    ('Table VI input', r'\\input\{tables/table_vi'),
    ('DeLong table input', r'\\input\{tables/table_delong'),
    ('Baseline Implementations', r'\\subsection\{Baseline'),
    ('Threshold Sensitivity', r'\\subsection\{Threshold'),
]
for name, pat in required_sections:
    if re.search(pat, exp_content):
        print(f"  PASS: {name}")
    else:
        print(f"  FAIL: {name} MISSING")

exp_lines = exp_content.count('\n')
print(f"  File length: {exp_lines} lines")

# Check 7: Temporal single-run claim
print("\n[7] TEMPORAL SINGLE-RUN CLAIM")
if 'extending the temporal diagnostics to multiple seeds' in exp_content:
    print("  PASS: Softened temporal claim present")
else:
    print("  FAIL: Softened temporal claim missing")

# Check 8: Artifact availability
print("\n[8] ARTIFACT AVAILABILITY")
main_path = os.path.join(jedm_dir, 'main_jedm.tex')
with open(main_path, 'r', encoding='utf-8') as fh:
    main_content = fh.read()
if 'anonymized artifact repository will be provided during peer review' in main_content:
    print("  PASS: Proper anonymized statement")
elif 'publicly available on the GitHub' in main_content:
    print("  FAIL: Generic GitHub statement without URL")
else:
    print("  INFO: Check manually")

# Check 9: Table sizes
print("\n[9] TABLE FILE SIZES (empty check)")
table_dir = os.path.join(jedm_dir, 'tables')
for t in sorted(os.listdir(table_dir)):
    size = os.path.getsize(os.path.join(table_dir, t))
    status = 'WARN: TINY' if size < 600 else 'OK'
    print(f"  {status}: {t} ({size} bytes)")

# Check 10: Abstract/Conclusion overclaims
print("\n[10] ABSTRACT/CONCLUSION OVERCLAIM CHECK")
overclaim_patterns = [
    'very sparse calibration is good',
    'calibration always monotonically',
    'calibration monotonically worsens',
]
for pat in overclaim_patterns:
    if pat.lower() in main_content.lower():
        print(f"  FAIL: '{pat}' in main_jedm.tex")

conc_path = os.path.join(jedm_dir, 'sections', '06_conclusion.tex')
with open(conc_path, 'r', encoding='utf-8') as fh:
    conc_content = fh.read()
for pat in overclaim_patterns:
    if pat.lower() in conc_content.lower():
        print(f"  FAIL: '{pat}' in conclusion")

if 'Limited reliability flag' in conc_content or 'Limited reliability' in conc_content or 'caution' in conc_content.lower():
    print("  PASS: Conclusion has reliability caveat")
else:
    print("  WARN: No explicit reliability caveat in conclusion")

if '0.113' in conc_content and '0.158' in conc_content:
    print("  PASS: Dense->Medium gradient cited in conclusion")
else:
    print("  WARN: Check gradient numbers in conclusion")

print("\n" + "=" * 60)
print("REVIEW COMPLETE")
print("=" * 60)
