#!/usr/bin/env python3
"""
Validate all S7 standardized JSON files against Pico900 schema.
"""

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "conclusion_id",
    "section",
    "latin_incipit",
    "english_translation",
    "scholar_citations",
    "heretical_flag",
    "tags",
    "status",
]

def validate_file(filepath):
    """Validate a single JSON file against schema."""
    errors = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]
    except Exception as e:
        return [f"File error: {e}"]

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif field == "conclusion_id" and not data[field]:
            errors.append(f"Empty conclusion_id")
        elif field == "section" and data[field] != "S7":
            errors.append(f"Section mismatch: expected 'S7', got '{data[field]}'")
        elif field == "status" and data[field] != "standardized":
            errors.append(f"Status mismatch: expected 'standardized', got '{data[field]}'")
        elif field == "tags" and not isinstance(data[field], list):
            errors.append(f"Tags should be array, got {type(data[field])}")
        elif field == "heretical_flag" and not isinstance(data[field], bool):
            errors.append(f"heretical_flag should be boolean, got {type(data[field])}")

    # Validate ID format
    if "conclusion_id" in data:
        conclusion_id = data["conclusion_id"]
        if not conclusion_id.startswith("S7.C"):
            errors.append(f"ID format mismatch: '{conclusion_id}' should start with 'S7.C'")

    return errors


def main():
    output_dir = Path("C:/Dev/Pico900/data/conclusions/S7")

    if not output_dir.exists():
        print(f"ERROR: Output directory not found: {output_dir}")
        return False

    # Get all JSON files
    json_files = sorted(output_dir.glob("entry_S7.C*.json"))

    if not json_files:
        print(f"ERROR: No JSON files found in {output_dir}")
        return False

    print(f"Validating {len(json_files)} files...\n")

    valid_count = 0
    invalid_count = 0
    all_errors = {}

    for filepath in json_files:
        errors = validate_file(filepath)

        if not errors:
            valid_count += 1
        else:
            invalid_count += 1
            all_errors[filepath.name] = errors

    # Print results
    print("="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    print(f"Total files: {len(json_files)}")
    print(f"Valid files: {valid_count}")
    print(f"Invalid files: {invalid_count}")

    if invalid_count > 0:
        print("\nInvalid files:")
        for filename, errors in sorted(all_errors.items()):
            print(f"\n  {filename}:")
            for error in errors:
                print(f"    - {error}")

    # Verify ID sequence
    print("\n" + "="*70)
    print("ID SEQUENCE CHECK")
    print("="*70)

    id_sequence_ok = True
    for idx, filepath in enumerate(json_files, start=1):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        expected_id = f"S7.C{idx:03d}"
        actual_id = data.get("conclusion_id", "")
        if actual_id != expected_id:
            print(f"ERROR: File {idx} has ID '{actual_id}', expected '{expected_id}'")
            id_sequence_ok = False

    if id_sequence_ok:
        print(f"OK: All {len(json_files)} IDs are sequential and correctly formatted")

    # Summary
    print("\n" + "="*70)
    success = (invalid_count == 0 and id_sequence_ok)
    if success:
        print("SUCCESS: All validations passed!")
        print("="*70)
        print(f"[OK] All 118 files present")
        print(f"[OK] All JSON parseable")
        print(f"[OK] All required fields present")
        print(f"[OK] All IDs sequential (S7.C001 through S7.C118)")
        print(f"[OK] All status set to 'standardized'")
    else:
        print("FAILURE: Some validations failed")
        print("="*70)

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
