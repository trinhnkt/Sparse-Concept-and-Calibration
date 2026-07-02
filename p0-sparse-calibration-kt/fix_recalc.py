import sys

with open('scripts/recalc_temporal_calibration.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: strata_map should stringify keys properly
old_strata = "key = (row['dataset'], str(row['kc_id']))"
new_strata = "key = (row['dataset'], str(row['kc_id']).replace('.0', ''))"
content = content.replace(old_strata, new_strata)

# Fix 2: matching kc_ids
old_kc = "kc_ids = df['kc_id'].astype(str).values"
new_kc = "kc_ids = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True).values"
content = content.replace(old_kc, new_kc)

# Fix 3: default bucket from very_sparse to strict_cold_start
old_get = "b = strata_map.get((dataset, kc), 'very_sparse')"
new_get = "b = strata_map.get((dataset, kc), 'strict_cold_start')"
content = content.replace(old_get, new_get)

with open('scripts/recalc_temporal_calibration.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scripts/recalc_temporal_calibration.py")
