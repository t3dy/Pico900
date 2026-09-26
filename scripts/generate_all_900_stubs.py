#!/usr/bin/env python3
"""
Generate stubs for all 900 Pico conclusions.

This script creates a complete set of stub JSON entries for all sections of the
900 Conclusions, based on the critical edition taxonomy. Stubs include:
- conclusion_id (e.g., S1.C001)
- section and order
- latin_incipit (placeholder to be filled from critical edition)
- Basic metadata (status: unstarted, translation source: null, etc.)

Existing entries are preserved; missing ones are created.

Usage:
    python scripts/generate_all_900_stubs.py
        Generate all stubs and report status

    python scripts/generate_all_900_stubs.py --overwrite
        Regenerate all stubs (overwrites existing)

    python scripts/generate_all_900_stubs.py --section S1
        Generate stubs for section S1 only
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Critical edition section structure (from CRITICAL_EDITION_TAXONOMY.md)
SECTIONS = {
    "S1": {
        "name": "Secundum Platonicos",
        "count": 95,
        "topic": "Neoplatonic Philosophy",
    },
    "S2": {
        "name": "Secundum Aristotelem",
        "count": 110,
        "topic": "Aristotelian Philosophy",
    },
    "S3": {
        "name": "Secundum Averroem",
        "count": 120,
        "topic": "Aristotelian Islamic Philosophy (Averroes)",
    },
    "S4": {
        "name": "Secundum Avicennam",
        "count": 105,
        "topic": "Aristotelian Islamic Philosophy (Avicenna)",
    },
    "S5": {
        "name": "Secundum Zoroastrem",
        "count": 80,
        "topic": "Persian & Magian Philosophy",
    },
    "S6": {
        "name": "Secundum Moysem Aegyptium",
        "count": 95,
        "topic": "Egyptian & Hermetic Magic",
    },
    "S7": {
        "name": "Secundum Hebraeos",
        "count": 115,
        "topic": "Kabbalah & Jewish Philosophy",
    },
    "S8": {
        "name": "Secundum Isaac Narbonensem et Abumaron",
        "count": 8,
        "topic": "Medieval Jewish Philosophers",
    },
    "S9": {
        "name": "Secundum Theologos",
        "count": 185,
        "topic": "Christian Theology & Church Fathers",
    },
}

STUB_TEMPLATE = {
    "conclusion_id": "",  # e.g., S1.C001
    "section": "",  # e.g., S1
    "order": None,  # Numeric order within section
    "section_name": "",  # Full name of section
    "topic": "",  # Topic descriptor
    "latin_incipit": "[TO BE SOURCED FROM CRITICAL EDITION]",
    "incipit_verified": False,
    "english_translation": "[TO BE SOURCED]",
    "translation_source": None,
    "translation_translator": None,
    "exegesis": "",
    "commentary_status": "unstarted",
    "charge": None,
    "defense": None,
    "scholar_citations": [],
    "heretical_flag": False,
    "heretical_notes": None,
    "tags": [],
    "status": "unstarted",
    "notes": "",
    "created_date": datetime.utcnow().isoformat(),
    "updated_date": datetime.utcnow().isoformat(),
}


def create_stub(section_id, order, section_info):
    """Create a stub entry for a conclusion."""
    stub = STUB_TEMPLATE.copy()
    stub["conclusion_id"] = f"{section_id}.C{order:03d}"
    stub["section"] = section_id
    stub["order"] = order
    stub["section_name"] = section_info["name"]
    stub["topic"] = section_info["topic"]
    return stub


def load_existing_entry(file_path):
    """Load an existing entry to preserve data."""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    return None


def generate_stubs(sections_filter=None, overwrite=False):
    """Generate stub entries for all sections."""
    data_dir = Path("data/conclusions")
    created_count = 0
    preserved_count = 0
    total_count = 0

    for section_id, section_info in sorted(SECTIONS.items()):
        if sections_filter and section_id not in sections_filter:
            continue

        section_dir = data_dir / section_id
        section_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{section_id}: {section_info['name']} ({section_info['count']} conclusions)")
        print("=" * 70)

        for order in range(1, section_info["count"] + 1):
            conclusion_id = f"{section_id}.C{order:03d}"
            file_path = section_dir / f"entry_{conclusion_id}.json"
            total_count += 1

            # Check if file exists and we should preserve it
            existing = load_existing_entry(file_path)
            if existing and not overwrite:
                # Preserve existing entry
                preserved_count += 1
                # Update timestamp
                existing["updated_date"] = datetime.utcnow().isoformat()
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
                continue

            # Create new stub
            stub = create_stub(section_id, order, section_info)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(stub, f, indent=2, ensure_ascii=False)
            created_count += 1

            # Progress indicator
            if order % 20 == 0 or order == section_info["count"]:
                print(f"  Created/processed {order}/{section_info['count']}")

    print("\n" + "=" * 70)
    print(f"Summary:")
    print(f"  Created new stubs: {created_count}")
    print(f"  Preserved existing: {preserved_count}")
    print(f"  Total entries: {total_count}")
    return created_count, preserved_count, total_count


def update_manifest(total_count):
    """Update the manifest with stub generation status."""
    manifest_path = Path("data/conclusions_manifest.json")

    # Load or create manifest
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        manifest = {
            "phase": "1",
            "phase_start": datetime.utcnow().isoformat(),
            "status": "in_progress",
            "stub_generation_complete": False,
            "sections": {},
        }

    # Mark stub generation complete
    manifest["stub_generation_complete"] = True
    manifest["stub_generation_timestamp"] = datetime.utcnow().isoformat()
    manifest["total_stubs_generated"] = total_count

    # Save manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest updated: {manifest_path}")


def main():
    sections_filter = None
    overwrite = False

    if "--overwrite" in sys.argv:
        overwrite = True
        print("WARNING: Will overwrite existing entries (except preserved fields)")

    if "--section" in sys.argv:
        idx = sys.argv.index("--section")
        if idx + 1 < len(sys.argv):
            sections_filter = [sys.argv[idx + 1]]

    print("Generating stubs for all 900 Pico Conclusions")
    print("=" * 70)

    created, preserved, total = generate_stubs(sections_filter, overwrite)
    update_manifest(total)

    print(f"\n✓ Complete. {created} stubs created, {preserved} preserved.")
    print(f"✓ All {total} conclusion entries now have stubs.")


if __name__ == "__main__":
    main()
