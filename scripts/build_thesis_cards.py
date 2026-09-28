#!/usr/bin/env python3
"""
T-SITE-06: Build thesis cards for all 900 conclusions with person relevance bars.

Generates data/thesis_cards_data.json with all thesis metadata and person relevance.
Site templates (site/conclusions/index.html and detail pages) use this data.

Reads from:
- data/inventory/theses.json (all 900 theses)
- data/network/thesis_person_relevance.json (person relevance scores)
- data/network/persons.json (person metadata for colors/names)

Usage:
    python scripts/build_thesis_cards.py
"""

import json
import os
from pathlib import Path

def load_json(path):
    """Load JSON file safely."""
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Building thesis cards with person relevance...")

    # Load all data
    theses_data = load_json('data/inventory/theses.json')
    relevance_data = load_json('data/network/thesis_person_relevance.json') or {}
    persons_data = load_json('data/network/persons.json') or []

    if not theses_data:
        print("ERROR: data/inventory/theses.json not found")
        return

    # Build person lookup
    persons_by_id = {p['person_id']: p for p in persons_data}

    # Color scheme for persons
    person_colors = {
        'ficino': '#8B4513',
        'delmedigo': '#DC143C',
        'mithridates': '#4169E1',
        'barbaro': '#FFD700',
        'alemanno': '#9370DB',
        'poliziano': '#20B2AA',
        'benivieni': '#FF6347',
        'savonarola': '#2F4F4F',
        'gianfrancesco-pico': '#DAA520',
        'lorenzo-de-medici': '#FF4500',
    }

    # Build thesis summary data structure
    thesis_summary = []
    thesis_count = 0
    with_relevance = 0

    for thesis in theses_data.get('theses', []):
        thesis_id = thesis.get('thesis_id', '')
        if not thesis_id:
            continue

        thesis_count += 1

        # Get relevance data for this thesis
        rel_entry = relevance_data.get(thesis_id, {})
        persons = rel_entry.get('persons', [])

        # Build entry for explorer data
        entry = {
            'thesis_id': thesis_id,
            'section': thesis.get('section', ''),
            'section_name': thesis.get('section_name', ''),
            'latin': thesis.get('latin', '')[:150],
            'person_relevance': [
                {
                    'person_id': p['person_id'],
                    'name': persons_by_id.get(p['person_id'], {}).get('canonical_name', p['person_id']),
                    'score': p['relevance_score'],
                }
                for p in persons[:5]
            ] if persons else []
        }

        if persons:
            with_relevance += 1

        thesis_summary.append(entry)

    # Write explorer data file
    explorer_data = {
        'total_theses': thesis_count,
        'theses_with_relevance': with_relevance,
        'theses': thesis_summary,
        'person_colors': person_colors,
    }

    with open('data/thesis_cards_data.json', 'w', encoding='utf-8') as f:
        json.dump(explorer_data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Thesis cards data built!")
    print(f"  - Total theses: {thesis_count}")
    print(f"  - Theses with person relevance: {with_relevance}")
    print(f"  - Output: data/thesis_cards_data.json")
    print(f"  - Data structure: thesis_id -> persons (sorted by relevance)")
    print(f"  - Relevance scores integrate mention harvest + verified claims")
    print(f"  - Next: site templates use this data to render explorer and detail pages")

if __name__ == '__main__':
    main()
