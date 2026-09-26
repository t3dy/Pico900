#!/usr/bin/env python3
"""
Fix schema/formatting issues across 69 angelology entries.

Issues to fix:
1. JSON formatting: Missing commas after exegesis field
2. Lineage schema violations: Replace invalid values with allowed set
3. Tag schema violations: Replace invalid tags with allowed set
4. Missing heretical-adjacent tags: Add where discussing divine embodiment
5. Cross-reference errors: Fix malformed/non-existent references
"""

import json
import os
import re
from pathlib import Path

# Constants
ALLOWED_LINEAGES = {"pseudo-dionysius", "aquinas", "kabbalah", "plotinus", "synthesis"}
ALLOWED_TAGS = {
    "angels",
    "arabic_philosophy",
    "aristotlelianism",
    "astrology",
    "causality",
    "christian_theology",
    "epistemology",
    "essence_existence",
    "eucharist",
    "heretical",
    "heretical_adjacent",
    "incarnation",
    "intellect",
    "kabbalah",
    "logic",
    "magic",
    "metaphysics",
    "platonism",
    "prophecy",
    "soul",
    "theology",
    "angelology",
    "neoplatonism",
    "hierarchy",
    "dignity",
    "hypostases",
    "angelic_orders",
    "kabbalistic",
    "mysticism",
    "mystical_union",
    "participation",
    "emanation",
    "being",
    "unity",
    "ascent",
}

# Lineage mappings for invalid values
LINEAGE_MAPPINGS = {
    "iamblichus": "plotinus",
    "proclus": "plotinus",
    "ficino": "synthesis",
    "mysticism": "synthesis",
    "eriugena": "pseudo-dionysius",
    "zoroastrianism": "synthesis",
    "aristotle": "synthesis",  # From O.1.1.json
    "plato": "plotinus",  # From Heptaplus files
    "bonaventure": "aquinas",
    "scotus": "aquinas",
}

# Tag mappings for invalid values
TAG_MAPPINGS = {
    "philosophy": "metaphysics",
    "cosmology": ["metaphysics", "neoplatonism"],
    "contemplation": ["mysticism", "mystical_union"],
    "freedom": "heretical_adjacent",
}

# Keywords indicating heretical_adjacent relevance
HERETICAL_KEYWORDS = {
    "incarnation", "eucharist", "embodiment", "body", "matter", "substance",
    "essence", "intellect", "will", "doxastic", "divine presence", "presence",
    "transubstantiation", "form", "participation", "union", "mystical",
}

TEXTS_DIR = "data/texts"
ENTRIES_SUBDIRS = {
    "oration": "entries",
    "commento": "entries",
    "heptaplus": "entries",
    "being_unity": "entries",
}

ISSUES_LOG = {
    "json_formatting": [],
    "lineage_violations": [],
    "tag_violations": [],
    "heretical_adjacent_added": [],
    "cross_reference_errors": [],
    "files_fixed": 0,
    "total_fixes": 0,
}


def check_and_fix_json_formatting(file_path):
    """Check for and fix missing comma after exegesis field."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for missing comma after "exegesis": "..." field
    pattern = r'("exegesis":\s*"[^"]*(?:\\.[^"]*)*")\s*\n\s*("exegesis_status"|"lineage"|"key_concepts"|"tags"|"cross_references"|"scholar_citations"|"status"|"notes")'

    if re.search(pattern, content):
        # Fix: add comma
        content = re.sub(pattern, r'\1,\n  \2', content)
        return True, content
    return False, content


def parse_json_safe(file_path):
    """Safely parse JSON, handling missing commas."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            # Try fixing common issues
            content = f.read()

            # Fix missing comma after exegesis
            content_fixed, _ = check_and_fix_json_formatting(file_path)
            if content_fixed:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass

            raise e


def fix_lineage(lineage_value):
    """Fix lineage field to use only allowed values."""
    if not lineage_value:
        return lineage_value

    if isinstance(lineage_value, str):
        # Split by pipe or comma
        parts = re.split(r'[|,]\s*', lineage_value.strip())
        fixed_parts = []

        for part in parts:
            part = part.strip().lower()
            if not part:
                continue

            # Check if it's already valid
            if part in ALLOWED_LINEAGES:
                fixed_parts.append(part)
            # Check mapping
            elif part in LINEAGE_MAPPINGS:
                mapped = LINEAGE_MAPPINGS[part]
                if isinstance(mapped, list):
                    fixed_parts.extend(mapped)
                else:
                    fixed_parts.append(mapped)
            else:
                # Try to match partial names
                matched = False
                for allowed in ALLOWED_LINEAGES:
                    if part in allowed or allowed in part:
                        fixed_parts.append(allowed)
                        matched = True
                        break
                if not matched:
                    # Default to synthesis if we can't map
                    fixed_parts.append("synthesis")

        # Remove duplicates while preserving order
        seen = set()
        result = []
        for item in fixed_parts:
            if item not in seen:
                result.append(item)
                seen.add(item)

        return " | ".join(result) if result else "synthesis"

    return lineage_value


def fix_tags(tags_list, exegesis_text=""):
    """Fix tags to use only allowed values and add heretical_adjacent if needed."""
    if not tags_list:
        tags_list = []

    fixed_tags = []
    changes_made = False

    for tag in tags_list:
        tag_lower = tag.lower().replace("_", "_")

        # Check if it's valid
        if tag_lower in ALLOWED_TAGS:
            fixed_tags.append(tag_lower)
        # Check mapping
        elif tag_lower in TAG_MAPPINGS:
            mapped = TAG_MAPPINGS[tag_lower]
            if isinstance(mapped, list):
                fixed_tags.extend(mapped)
            else:
                fixed_tags.append(mapped)
            changes_made = True
        else:
            # Try fuzzy matching
            found = False
            for allowed in ALLOWED_TAGS:
                if tag_lower in allowed or allowed in tag_lower:
                    if allowed not in fixed_tags:
                        fixed_tags.append(allowed)
                    found = True
                    break
            if found:
                changes_made = True

    # Remove duplicates
    fixed_tags = list(dict.fromkeys(fixed_tags))

    # Check if heretical_adjacent should be added
    if exegesis_text:
        exegesis_lower = exegesis_text.lower()
        has_heretical_keywords = any(
            keyword in exegesis_lower for keyword in HERETICAL_KEYWORDS
        )

        if has_heretical_keywords and "heretical_adjacent" not in fixed_tags:
            fixed_tags.append("heretical_adjacent")
            changes_made = True

    return fixed_tags, changes_made


def fix_cross_references(cross_refs, text_entries_map):
    """Fix cross-reference errors."""
    fixed_refs = {}
    changes_made = False

    for key, value in cross_refs.items():
        if isinstance(value, list):
            fixed_list = []
            for ref in value:
                # Check if it's a range like "C.1.1-C.1.5"
                if isinstance(ref, str) and "-" in ref:
                    # Expand range
                    match = re.match(r'([A-Z]?)\.(\d+)\.(\d+)-[A-Z]?\.(\d+)\.(\d+)', ref)
                    if match:
                        prefix, book_start, subsec_start, book_end, subsec_end = match.groups()
                        if book_start == book_end:
                            for i in range(int(subsec_start), int(subsec_end) + 1):
                                expanded = f"{prefix}.{book_start}.{i}"
                                fixed_list.append(expanded)
                            changes_made = True
                        else:
                            # Complex range, leave as is
                            fixed_list.append(ref)
                    else:
                        fixed_list.append(ref)
                else:
                    fixed_list.append(ref)
            fixed_refs[key] = fixed_list
        else:
            fixed_refs[key] = value

    return fixed_refs, changes_made


def process_angelology_entries():
    """Process all 69 angelology entries."""
    pico900_root = Path(".")

    all_files = []
    for text_name in ENTRIES_SUBDIRS.keys():
        entries_dir = pico900_root / TEXTS_DIR / text_name / ENTRIES_SUBDIRS[text_name]
        if entries_dir.exists():
            json_files = list(entries_dir.glob("*.json"))
            all_files.extend(json_files)

    print(f"Found {len(all_files)} JSON files")

    # Build a map of all entry IDs for cross-reference validation
    entry_ids = set()
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Try fixing formatting first
                content = f.read()
                fixed_formatting, fixed_content = check_and_fix_json_formatting(file_path)

                data = json.loads(fixed_content) if fixed_formatting else json.loads(content)
                if "conclusion_id" in data:
                    entry_ids.add(data["conclusion_id"])
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")

    print(f"Found {len(entry_ids)} unique entry IDs")

    # Process each file
    for file_path in sorted(all_files):
        try:
            # Read and parse
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix JSON formatting first
            fixed_formatting, fixed_content = check_and_fix_json_formatting(file_path)
            if fixed_formatting:
                ISSUES_LOG["json_formatting"].append(str(file_path))

            # Parse JSON
            data = json.loads(fixed_content)
            original_data = json.loads(fixed_content)

            # Fix Issue #2: Lineage
            if "lineage" in data:
                old_lineage = data["lineage"]
                new_lineage = fix_lineage(old_lineage)
                if old_lineage != new_lineage:
                    data["lineage"] = new_lineage
                    ISSUES_LOG["lineage_violations"].append({
                        "id": data.get("conclusion_id"),
                        "old": old_lineage,
                        "new": new_lineage
                    })

            # Fix Issue #3: Tags and Issue #4: Heretical-adjacent
            if "tags" in data:
                exegesis_text = data.get("exegesis", "")
                old_tags = data["tags"].copy() if isinstance(data["tags"], list) else []
                new_tags, was_modified = fix_tags(data["tags"], exegesis_text)

                if new_tags != old_tags:
                    data["tags"] = new_tags
                    ISSUES_LOG["tag_violations"].append({
                        "id": data.get("conclusion_id"),
                        "old": old_tags,
                        "new": new_tags
                    })

                if was_modified and "heretical_adjacent" in new_tags and "heretical_adjacent" not in old_tags:
                    ISSUES_LOG["heretical_adjacent_added"].append(data.get("conclusion_id"))

            # Fix Issue #5: Cross-references
            if "cross_references" in data:
                old_refs = json.dumps(data["cross_references"], sort_keys=True)
                new_refs, was_modified = fix_cross_references(data["cross_references"], entry_ids)

                if json.dumps(new_refs, sort_keys=True) != old_refs:
                    data["cross_references"] = new_refs
                    ISSUES_LOG["cross_reference_errors"].append({
                        "id": data.get("conclusion_id"),
                        "changes": True
                    })

            # Write back if changes made
            if data != original_data or fixed_formatting:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                ISSUES_LOG["files_fixed"] += 1

                # Validate JSON was written correctly
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)

        except Exception as e:
            print(f"ERROR processing {file_path}: {e}")

    return ISSUES_LOG


def print_report(log):
    """Print summary report."""
    print("\n" + "="*80)
    print("REMEDIATION REPORT")
    print("="*80)

    print(f"\nFiles Fixed: {log['files_fixed']}")

    print(f"\n1. JSON FORMATTING ERRORS (missing commas): {len(log['json_formatting'])}")
    if log['json_formatting']:
        for f in log['json_formatting'][:5]:
            print(f"   - {f}")
        if len(log['json_formatting']) > 5:
            print(f"   ... and {len(log['json_formatting']) - 5} more")

    print(f"\n2. LINEAGE VIOLATIONS: {len(log['lineage_violations'])}")
    if log['lineage_violations']:
        for item in log['lineage_violations'][:5]:
            print(f"   - {item['id']}: {item['old']} -> {item['new']}")
        if len(log['lineage_violations']) > 5:
            print(f"   ... and {len(log['lineage_violations']) - 5} more")

    print(f"\n3. TAG VIOLATIONS: {len(log['tag_violations'])}")
    if log['tag_violations']:
        for item in log['tag_violations'][:3]:
            print(f"   - {item['id']}: {item['old']} → {item['new']}")
        if len(log['tag_violations']) > 3:
            print(f"   ... and {len(log['tag_violations']) - 3} more")

    print(f"\n4. HERETICAL-ADJACENT TAGS ADDED: {len(log['heretical_adjacent_added'])}")
    if log['heretical_adjacent_added']:
        for item in log['heretical_adjacent_added'][:5]:
            print(f"   - {item}")
        if len(log['heretical_adjacent_added']) > 5:
            print(f"   ... and {len(log['heretical_adjacent_added']) - 5} more")

    print(f"\n5. CROSS-REFERENCE ERRORS: {len(log['cross_reference_errors'])}")
    if log['cross_reference_errors']:
        for item in log['cross_reference_errors'][:5]:
            print(f"   - {item['id']}")
        if len(log['cross_reference_errors']) > 5:
            print(f"   ... and {len(log['cross_reference_errors']) - 5} more")

    total_issues = (len(log['json_formatting']) + len(log['lineage_violations']) +
                   len(log['tag_violations']) + len(log['heretical_adjacent_added']) +
                   len(log['cross_reference_errors']))

    print(f"\nTOTAL ISSUES FIXED: {total_issues}")
    print("="*80 + "\n")


if __name__ == "__main__":
    log = process_angelology_entries()
    print_report(log)
