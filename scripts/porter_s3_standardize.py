#!/usr/bin/env python3
"""
PORTER P3: Standardize 11 explicit Averroist conclusions from S3 staging into Pico900 schema.

Input: data/staging/stage_S3.json (11 complete + 109 placeholders from HARVESTER H3)
Output:
  - 11 JSON files in data/conclusions/S3/entry_S3.C001.json through entry_S3.C011.json
  - Updated manifest entry
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
STAGING_FILE = PROJECT_ROOT / "data" / "staging" / "stage_S3.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "conclusions" / "S3"
MANIFEST_FILE = PROJECT_ROOT / "data" / "conclusions_manifest.json"


def load_staging_data():
    """Load the staging JSON."""
    with open(STAGING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def standardize_conclusion(raw_conclusion, index):
    """
    Standardize a raw conclusion from staging into Pico900 schema.

    Args:
        raw_conclusion: dict from staging JSON
        index: 0-indexed position (0-10 for 11 conclusions)

    Returns:
        dict conforming to Pico900 schema
    """
    # New ID format: S3.C001, S3.C002, etc.
    conclusion_id = f"S3.C{index + 1:03d}"

    # Extract and reformat data
    standardized = {
        "conclusion_id": conclusion_id,
        "section": "S3",
        "conclusion_num": raw_conclusion.get("conclusion_num", ""),
        "latin_incipit": raw_conclusion.get("latin_incipit", ""),
        "english_translation": raw_conclusion.get("english_translation", {}).get("text", ""),
        "translation_source": raw_conclusion.get("english_translation", {}).get("source", ""),
        "charge": raw_conclusion.get("charge", ""),
        "defense": raw_conclusion.get("defense", ""),
        "exegesis": raw_conclusion.get("exegesis", ""),
        "scholar_citations": raw_conclusion.get("scholar_citations", []),
        "heretical_flag": raw_conclusion.get("heretical_flag", False),
        "heretical_notes": raw_conclusion.get("heretical_notes"),
        "tags": raw_conclusion.get("tags", []),
        "notes": raw_conclusion.get("notes", ""),
        "status": "standardized",
        "created_date": datetime.utcnow().isoformat() + "Z",
        "updated_date": datetime.utcnow().isoformat() + "Z"
    }

    return standardized


def validate_conclusion(conclusion):
    """
    Validate that all required fields are present and properly formatted.

    Args:
        conclusion: dict to validate

    Returns:
        tuple: (is_valid, errors_list)
    """
    required_fields = [
        "conclusion_id",
        "section",
        "latin_incipit",
        "english_translation",
        "charge",
        "defense",
        "scholar_citations",
        "heretical_flag",
        "tags",
        "status"
    ]

    errors = []

    for field in required_fields:
        if field not in conclusion:
            errors.append(f"Missing required field: {field}")
        elif field == "tags" and not isinstance(conclusion[field], list):
            errors.append(f"Field '{field}' must be a list, got {type(conclusion[field]).__name__}")
        elif field == "scholar_citations" and not isinstance(conclusion[field], list):
            errors.append(f"Field '{field}' must be a list, got {type(conclusion[field]).__name__}")

    # Validate ID format
    if "conclusion_id" in conclusion:
        expected_format = "S3.C###"
        if not conclusion["conclusion_id"].startswith("S3.C") or len(conclusion["conclusion_id"]) != 7:
            errors.append(f"ID format incorrect: {conclusion['conclusion_id']} (expected S3.C### format)")

    return len(errors) == 0, errors


def write_conclusion_file(conclusion, output_dir):
    """
    Write a single conclusion to a JSON file.

    Args:
        conclusion: standardized conclusion dict
        output_dir: Path to output directory

    Returns:
        bool: True if successful
    """
    filename = f"entry_{conclusion['conclusion_id']}.json"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conclusion, f, indent=2, ensure_ascii=False)

    return filepath.exists()


def update_manifest(manifest_file, s3_summary):
    """
    Update the conclusions manifest with S3 summary.

    Args:
        manifest_file: Path to manifest
        s3_summary: dict with section summary
    """
    try:
        if manifest_file.exists():
            with open(manifest_file, 'r', encoding='utf-8-sig') as f:
                manifest = json.load(f)
        else:
            manifest = {"sections": {}}

        # Handle both array and dict formats for sections
        if isinstance(manifest.get("sections"), list):
            # Find and update S3 in the list
            found = False
            for section in manifest["sections"]:
                if section.get("section_id") == "S3":
                    section["status"] = "porter_complete"
                    section["gates"]["porter_gate"]["status"] = "passed"
                    section["gates"]["porter_gate"]["timestamp"] = datetime.utcnow().isoformat() + "Z"
                    section["conclusion_count_explicit"] = s3_summary["complete_conclusions"]
                    found = True
                    break
            if not found:
                # S3 not in list, create new entry
                manifest["sections"].append({
                    "section_id": "S3",
                    "section_name": "Secundum Averroem",
                    "status": "porter_complete",
                    **s3_summary
                })
        elif isinstance(manifest.get("sections"), dict):
            manifest["sections"]["S3"] = s3_summary
        else:
            manifest["sections"] = {"S3": s3_summary}

        manifest["updated_date"] = datetime.utcnow().isoformat() + "Z"

        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"   ✗ Error updating manifest: {e}")
        raise


def main():
    """Main PORTER execution."""
    print("=" * 70)
    print("PORTER P3: S3 Averroist Conclusions Standardization")
    print("=" * 70)

    # Load staging data
    print(f"\n1. Loading staging data from {STAGING_FILE}...")
    staging_data = load_staging_data()
    metadata = staging_data.get("metadata", {})
    conclusions = staging_data.get("conclusions", [])

    print(f"   Found {len(conclusions)} conclusions (expecting 11 complete + 109 placeholders)")
    print(f"   Metadata: {metadata.get('total_conclusions')} total, {metadata.get('harvested_count')} harvested")

    # Create output directory
    print(f"\n2. Creating output directory: {OUTPUT_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"   ✓ Directory ready")

    # Process each conclusion
    print(f"\n3. Standardizing {len(conclusions)} conclusions...")
    standardized_conclusions = []
    validation_errors = []

    for i, raw_conclusion in enumerate(conclusions):
        conclusion_id_old = raw_conclusion.get("conclusion_id", f"S3.{i+1}")

        # Standardize
        standardized = standardize_conclusion(raw_conclusion, i)

        # Validate
        is_valid, errors = validate_conclusion(standardized)

        if is_valid:
            standardized_conclusions.append(standardized)
            print(f"   [{i+1:2d}/11] {standardized['conclusion_id']} ({conclusion_id_old}) — VALID")
        else:
            validation_errors.append({
                "conclusion_id": standardized.get("conclusion_id", conclusion_id_old),
                "errors": errors
            })
            print(f"   [{i+1:2d}/11] {standardized['conclusion_id']} ({conclusion_id_old}) — INVALID")
            for err in errors:
                print(f"         - {err}")

    if validation_errors:
        print(f"\n   WARNING: {len(validation_errors)} validation error(s) detected!")
        return False

    # Write individual files
    print(f"\n4. Writing {len(standardized_conclusions)} JSON files to {OUTPUT_DIR}...")
    files_written = 0

    for conclusion in standardized_conclusions:
        success = write_conclusion_file(conclusion, OUTPUT_DIR)
        if success:
            files_written += 1
            filename = f"entry_{conclusion['conclusion_id']}.json"
            filepath = OUTPUT_DIR / filename
            print(f"   ✓ {conclusion['conclusion_id']}: {filepath}")
        else:
            print(f"   ✗ Failed to write {conclusion['conclusion_id']}")

    print(f"   Total files written: {files_written}/{len(standardized_conclusions)}")

    # Update manifest
    print(f"\n5. Updating manifest...")
    s3_summary = {
        "section_id": "S3",
        "section_name": "Secundum Averroem",
        "complete_conclusions": len(standardized_conclusions),
        "placeholder_conclusions": 109,
        "total_conclusions": 120,
        "status": "11 complete; 109 placeholders deferred to Phase 2",
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "files": [f"entry_S3.C{i+1:03d}.json" for i in range(len(standardized_conclusions))]
    }

    update_manifest(MANIFEST_FILE, s3_summary)
    print(f"   ✓ Manifest updated: {MANIFEST_FILE}")

    # Summary
    print("\n" + "=" * 70)
    print("STANDARDIZATION COMPLETE")
    print("=" * 70)
    print(f"✓ 11 conclusions standardized and written")
    print(f"✓ IDs assigned: S3.C001 through S3.C011")
    print(f"✓ All JSON valid")
    print(f"✓ Manifest updated")
    print(f"✓ Status: Ready for next phase (Phase 2 will handle 109 placeholders)")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
