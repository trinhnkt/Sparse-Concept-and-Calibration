import sys

with open('src/recalculate_diagnostics.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix strata_map creation
old_strata = "key = (row['dataset'], row['split'], str(row['kc_id']))"
new_strata = "key = (row['dataset'], row['split'], str(row['kc_id']).replace('.0', ''))"
content = content.replace(old_strata, new_strata)

# Fix kc_ids extraction
old_kc = "kc_ids = df['kc_id'].astype(str).values"
new_kc = "kc_ids = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True).values"
content = content.replace(old_kc, new_kc)

# Ensure fallback for temporal goes to strict_cold_start if not in mapping! Wait, what if it's learner based?
# If learner based, missing KCs could be from test, but the kc_strata has all KCs in train.
# If a KC is not in train, it has 0 train freq, so it IS strict_cold_start!
old_fallback = """            else:
                # If a KC is completely missing from strata_df, it had 0 freq in training
                buckets.append('strict_cold_start')
                train_freqs.append(0)"""
# If the fallback is already strict_cold_start, that's fine.

with open('src/recalculate_diagnostics.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated src/recalculate_diagnostics.py")
