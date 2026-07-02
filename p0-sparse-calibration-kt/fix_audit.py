import sys

with open('scripts/audit_temporal_split.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix strata_map creation
old_strata = "key = (row['dataset'], row['split'], str(row['kc_id']))"
new_strata = "key = (row['dataset'], row['split'], str(row['kc_id']).replace('.0', ''))"
if old_strata in content:
    content = content.replace(old_strata, new_strata)
else:
    # try another format
    content = content.replace("str(row['kc_id'])", "str(row['kc_id']).replace('.0', '')")

# Fix kc_ids extraction
old_kc = "kc_ids = df['kc_id'].astype(str).values"
new_kc = "kc_ids = df['kc_id'].astype(str).str.replace(r'\.0$', '', regex=True).values"
content = content.replace(old_kc, new_kc)

with open('scripts/audit_temporal_split.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scripts/audit_temporal_split.py")
