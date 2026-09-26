#!/usr/bin/env python3
"""
PORTER P2: Standardize S1 staging conclusions into Pico900 schema.

Input: data/staging/stage_S1.json (95 Neoplatonic conclusions from HARVESTER H2)
Output: data/conclusions/S1/entry_S1.C001.json through entry_S1.C095.json

Converts from staging schema -> Pico900 standardized schema.
IDs: S1.T001-095 (staging) -> S1.C001-095 (standardized)
"""

import json
import os
import sys
from pathlib import Path


def load_staging_file(filepath):
    """Load the staging JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def standardize_conclusion(staged_entry, conclusion_number):
    """
    Convert a staged entry to standardized Pico900 schema.

    Args:
        staged_entry: Dict from stage_S1.json['conclusions']
        conclusion_number: Int from 1 to 95

    Returns:
        Standardized conclusion dict
    """
    # Convert conclusion number to ID: 1 -> S1.C001
    conclusion_id = f"S1.C{conclusion_number:03d}"

    # Extract and normalize fields
    return {
        "conclusion_id": conclusion_id,
        "section": "S1",
        "order": conclusion_number,
        "latin_incipit": staged_entry.get("incipit") or "",
        "incipit_verified": staged_entry.get("incipit_verified", False),
        "english_translation": staged_entry.get("english_translation") or "",
        "translation_source": staged_entry.get("translation_source"),
        "translation_translator": staged_entry.get("translation_translator"),
        "philosophical_theme": staged_entry.get("philosophical_theme") or "",
        "key_concepts": staged_entry.get("key_concepts", []),
        "plotinian_parallel": staged_entry.get("plotinian_parallel"),
        "secondary_philosophers": staged_entry.get("secondary_philosophers", []),
        "charge": staged_entry.get("charge") or "",
        "defense": staged_entry.get("defense") or "",
        "scholar_citations": [
            {
                "scholar": cit.get("scholar", ""),
                "work": cit.get("work", ""),
                "page": cit.get("section"),
                "quotation": cit.get("quotation") or "",
                "verified": cit.get("verified", False),
                "confidence_level": "UNVERIFIED"
            }
            for cit in staged_entry.get("scholar_citations", [])
        ],
        "heretical_flag": staged_entry.get("heretical_flag", False),
        "heretical_notes": staged_entry.get("heretical_notes"),
        "tags": staged_entry.get("tags", []),
        "status": "standardized",
        "notes": staged_entry.get("notes"),
        "created_from_cluster": False
    }


def expand_cluster_entry(cluster_entry, start_num, end_num):
    """
    Expand a cluster placeholder into individual standardized entries.

    Args:
        cluster_entry: Dict from stage_S1.json['conclusions'] marked as cluster
        start_num: Starting conclusion number (1-indexed)
        end_num: Ending conclusion number (1-indexed, inclusive)

    Returns:
        List of standardized conclusion dicts
    """
    entries = []
    for num in range(start_num, end_num + 1):
        entry_copy = {
            "conclusion_id": f"S1.C{num:03d}",
            "section": "S1",
            "order": num,
            "latin_incipit": "",
            "incipit_verified": False,
            "english_translation": "",
            "translation_source": None,
            "translation_translator": None,
            "philosophical_theme": cluster_entry.get("philosophical_theme") or "",
            "key_concepts": cluster_entry.get("key_concepts", []),
            "plotinian_parallel": cluster_entry.get("plotinian_parallel"),
            "secondary_philosophers": cluster_entry.get("secondary_philosophers", []),
            "charge": "",
            "defense": "",
            "scholar_citations": [
                {
                    "scholar": cit.get("scholar", ""),
                    "work": cit.get("work", ""),
                    "page": None,
                    "quotation": "",
                    "verified": False,
                    "confidence_level": "UNVERIFIED"
                }
                for cit in cluster_entry.get("scholar_citations", [])
            ],
            "heretical_flag": cluster_entry.get("heretical_flag", False),
            "heretical_notes": cluster_entry.get("heretical_notes"),
            "tags": cluster_entry.get("tags", []),
            "status": "standardized",
            "notes": cluster_entry.get("notes"),
            "created_from_cluster": True
        }
        entries.append(entry_copy)
    return entries


def process_staging_file(staging_filepath, output_dir):
    """
    Process the entire staging file and write standardized JSON files.

    Args:
        staging_filepath: Path to stage_S1.json
        output_dir: Output directory for individual conclusion files

    Returns:
        Dict with success status and statistics
    """
    # Load staging data
    staging_data = load_staging_file(staging_filepath)

    # Create output directory if needed
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process conclusions
    all_conclusions = []

    # Map of staged conclusion_id to {type: 'individual' or 'cluster', range: (start, end) if cluster}
    staged_ids = {
        'S1.T1': ('individual', None),
        'S1.T2': ('individual', None),
        'S1.T3': ('individual', None),
        'S1.T4': ('individual', None),
        'S1.T5': ('individual', None),
        'S1.T6': ('cluster', (6, 20)),
        'S1.T21': ('cluster', (21, 40)),
        'S1.T41': ('cluster', (41, 60)),
        'S1.T61': ('cluster', (61, 80)),
        'S1.T81': ('cluster', (81, 95))
    }

    # Process each staged entry
    for staged_entry in staging_data.get('conclusions', []):
        cid = staged_entry.get('conclusion_id')

        if cid not in staged_ids:
            sys.stderr.write(f"Warning: Unknown conclusion ID {cid}, skipping\n")
            continue

        entry_type, range_info = staged_ids[cid]

        if entry_type == 'individual':
            num = int(cid.split('.T')[1])
            standardized = standardize_conclusion(staged_entry, num)
            all_conclusions.append(standardized)
        elif entry_type == 'cluster':
            start_num, end_num = range_info
            expanded = expand_cluster_entry(staged_entry, start_num, end_num)
            all_conclusions.extend(expanded)

    # Validate we have exactly 95 conclusions
    if len(all_conclusions) != 95:
        raise ValueError(
            f"Expected 95 conclusions, got {len(all_conclusions)}. "
            "Cluster expansion failed."
        )

    # Sort by order to ensure sequential
    all_conclusions.sort(key=lambda x: x['order'])

    # Write individual JSON files
    written_files = []
    for conclusion in all_conclusions:
        filename = f"entry_{conclusion['conclusion_id']}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conclusion, f, indent=2, ensure_ascii=False)

        written_files.append(filepath)

    # Generate summary statistics
    stats = {
        'total_conclusions': len(all_conclusions),
        'individual_entries': sum(1 for c in all_conclusions if not c['created_from_cluster']),
        'cluster_expanded_entries': sum(1 for c in all_conclusions if c['created_from_cluster']),
        'heretical_conclusions': sum(1 for c in all_conclusions if c['heretical_flag']),
        'files_written': len(written_files),
        'output_directory': output_dir,
        'all_files': sorted([os.path.basename(f) for f in written_files])
    }

    return {
        'success': True,
        'conclusions': all_conclusions,
        'stats': stats,
        'written_files': written_files
    }


def main():
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    staging_file = project_root / 'data' / 'staging' / 'stage_S1.json'
    output_dir = project_root / 'data' / 'conclusions' / 'S1'

    sys.stdout.write("PORTER P2: Standardizing S1 conclusions...\n")
    sys.stdout.write(f"Input: {staging_file}\n")
    sys.stdout.write(f"Output directory: {output_dir}\n")
    sys.stdout.write("\n")

    result = process_staging_file(str(staging_file), str(output_dir))

    if result['success']:
        stats = result['stats']
        sys.stdout.write("[OK] Standardization complete!\n")
        sys.stdout.write(f"  Total conclusions written: {stats['total_conclusions']}\n")
        sys.stdout.write(f"  Individual entries: {stats['individual_entries']}\n")
        sys.stdout.write(f"  Cluster-expanded entries: {stats['cluster_expanded_entries']}\n")
        sys.stdout.write(f"  Heretical conclusions flagged: {stats['heretical_conclusions']}\n")
        sys.stdout.write(f"  Files written to: {stats['output_directory']}\n")
        sys.stdout.write("\n")
        sys.stdout.write("First 5 files:\n")
        for fn in stats['all_files'][:5]:
            sys.stdout.write(f"  - {fn}\n")
        sys.stdout.write(f"  ... ({stats['total_conclusions'] - 5} more)\n")

        # Validate output
        sys.stdout.write("\n")
        sys.stdout.write("Validation:\n")
        expected_ids = [f"S1.C{i:03d}" for i in range(1, 96)]
        actual_ids = [c['conclusion_id'] for c in result['conclusions']]

        if actual_ids == expected_ids:
            sys.stdout.write("  [OK] All IDs correctly formatted and sequential (S1.C001-S1.C095)\n")
        else:
            sys.stdout.write("  [FAIL] ID validation failed!\n")
            missing = set(expected_ids) - set(actual_ids)
            if missing:
                sys.stdout.write(f"    Missing IDs: {sorted(missing)[:5]}...\n")
            extra = set(actual_ids) - set(expected_ids)
            if extra:
                sys.stdout.write(f"    Extra IDs: {sorted(extra)[:5]}...\n")

        # Check all required fields
        sys.stdout.write("\n")
        sys.stdout.write("Schema validation (first 5 entries):\n")
        required_fields = [
            'conclusion_id', 'section', 'latin_incipit', 'english_translation',
            'charge', 'defense', 'scholar_citations', 'heretical_flag', 'tags', 'status'
        ]

        all_valid = True
        for i, conclusion in enumerate(result['conclusions'][:5]):
            missing_fields = [f for f in required_fields if f not in conclusion]
            if missing_fields:
                sys.stdout.write(f"  [FAIL] {conclusion['conclusion_id']}: Missing {missing_fields}\n")
                all_valid = False
            else:
                sys.stdout.write(f"  [OK] {conclusion['conclusion_id']}: All required fields present\n")

        if all_valid:
            sys.stdout.write("\n")
            sys.stdout.write("[SUCCESS] All 95 files created with valid schema\n")
        else:
            sys.stdout.write("\n")
            sys.stdout.write("[WARNING] Some entries have missing fields\n")

        return 0
    else:
        sys.stdout.write("[FAIL] Standardization failed\n")
        return 1


if __name__ == '__main__':
    exit(main())
