#!/usr/bin/env python3
"""
Clean up stage_S7.json: remove duplicates, keep only unique conclusions.
Target: 47 (28.N) + 72 (11>N) = 119 unique conclusions
"""

import json
from pathlib import Path
from collections import OrderedDict

output_path = Path(r"C:\Dev\Pico900\data\staging\stage_S7.json")

with open(output_path, encoding='utf-8') as f:
    data = json.load(f)

# Deduplicate by conclusion_id, keeping first occurrence
seen = set()
unique_conclusions = []

for conclusion in data['conclusions']:
    cid = conclusion['conclusion_id']
    if cid not in seen:
        seen.add(cid)
        unique_conclusions.append(conclusion)

# Sort by conclusion_id (28.1-28.47 first, then 11>1-11>72)
def sort_key(c):
    cid = c['conclusion_id']
    if cid.startswith('28.'):
        num = int(cid.split('.')[1])
        return (0, num)
    else:  # 11>N
        num = int(cid.split('>')[1])
        return (1, num)

unique_conclusions.sort(key=sort_key)

# Count
hist_count = sum(1 for c in unique_conclusions if c['type'] == 'historical')
own_count = sum(1 for c in unique_conclusions if c['type'] == 'personal')

print(f"Original: {len(data['conclusions'])} entries")
print(f"After deduplication: {len(unique_conclusions)} unique conclusions")
print(f"  Historical (28.N): {hist_count}")
print(f"  Pico's Own (11>N): {own_count}")
print(f"  Total: {len(unique_conclusions)}")

# Update data
data['conclusions'] = unique_conclusions
data['actual_count'] = len(unique_conclusions)
data['metadata']['subsections']['historical_kabbalist_theses']['count'] = hist_count
data['metadata']['subsections']['picos_own_conclusions']['count'] = own_count

# Save cleaned version
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nCleaned JSON saved to {output_path}")
print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

# Verify
print("\nVerification:")
print(f"  First: {unique_conclusions[0]['conclusion_id']}")
print(f"  Last: {unique_conclusions[-1]['conclusion_id']}")

EOF
python3 C:\Dev\Pico900\deduplicate_s7.py
