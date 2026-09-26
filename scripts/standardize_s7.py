#!/usr/bin/env python3
"""
PORTER P8: Standardize S7 staging JSON into individual Pico900 schema entries.

Input: data/staging/stage_S7.json
Output: data/conclusions/S7/entry_S7.C001.json through entry_S7.C118.json
"""

import json
import os
from pathlib import Path

def standardize_conclusion(staging_entry, new_id):
    """
    Convert a staging entry into Pico900 standardized schema.

    Required fields:
    - conclusion_id
    - section
    - latin_incipit
    - english_translation
    - charge
    - defense
    - scholar_citations
    - heretical_flag
    - tags
    - status
    """

    # Map old fields to new schema
    scholar_citations = []
    if staging_entry.get("scholar_citations"):
        for sc in staging_entry["scholar_citations"]:
            scholar_citations.append({
                "scholar": sc.get("scholar", ""),
                "work": sc.get("work", ""),
                "year": sc.get("year"),
                "quotation": "",  # Will be populated later during citation phase
                "status": sc.get("status", "[TO_SOURCE]"),
                "verified": sc.get("verified", False)
            })

    # Build standardized entry
    standardized = {
        "conclusion_id": new_id,
        "section": "S7",
        "section_name": "Secundum Hebraeos - Kabbalah & Jewish Philosophy",
        "subsection": staging_entry.get("subsection", ""),
        "type": staging_entry.get("type", ""),
        "latin_incipit": staging_entry.get("latin_incipit", ""),
        "latin_full": staging_entry.get("latin_full", ""),
        "english_translation": staging_entry.get("english_translation", ""),
        "english_full": staging_entry.get("english_full", ""),
        "translation_source": staging_entry.get("translation_source", ""),
        "charge": staging_entry.get("charge", ""),
        "defense": staging_entry.get("pico_defense", ""),
        "scholar_citations": scholar_citations,
        "heretical_flag": staging_entry.get("heretical_flag", False),
        "is_condemned": staging_entry.get("is_condemned", False),
        "tags": staging_entry.get("tags", []),
        "status": "standardized"
    }

    return standardized


def main():
    # Read staging file
    staging_file = Path("C:/Dev/Pico900/data/staging/stage_S7.json")

    if not staging_file.exists():
        print(f"ERROR: Staging file not found at {staging_file}")
        return False

    with open(staging_file, 'r', encoding='utf-8') as f:
        staging_data = json.load(f)

    conclusions = staging_data.get("conclusions", [])
    actual_count = len(conclusions)

    print(f"Processing {actual_count} conclusions from S7 staging...")

    # Create output directory
    output_dir = Path("C:/Dev/Pico900/data/conclusions/S7")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Standardize and write each conclusion
    success_count = 0
    error_count = 0

    for idx, staging_entry in enumerate(conclusions, start=1):
        new_id = f"S7.C{idx:03d}"

        try:
            standardized = standardize_conclusion(staging_entry, new_id)

            # Validate required fields
            required_fields = [
                "conclusion_id", "section", "latin_incipit",
                "english_translation", "scholar_citations",
                "heretical_flag", "tags", "status"
            ]

            missing_fields = [f for f in required_fields if f not in standardized]
            if missing_fields:
                print(f"  WARNING [{new_id}]: Missing fields: {missing_fields}")

            # Write individual JSON file
            output_file = output_dir / f"entry_{new_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(standardized, f, indent=2, ensure_ascii=False)

            success_count += 1
            if idx % 20 == 0:
                print(f"  OK: Processed {idx}/{actual_count}...")

        except Exception as e:
            print(f"  ERROR [{new_id}]: {str(e)}")
            error_count += 1

    # Print summary
    print("\n" + "="*60)
    print("STANDARDIZATION COMPLETE")
    print("="*60)
    print(f"Total conclusions: {actual_count}")
    print(f"Successfully standardized: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Output directory: {output_dir}")

    # List sample files
    if success_count > 0:
        files = sorted(output_dir.glob("entry_S7.C*.json"))
        print(f"\nSample output files:")
        for f in files[:3]:
            print(f"  - {f.name}")
        if len(files) > 3:
            print(f"  ... and {len(files) - 3} more")

    return error_count == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
