#!/usr/bin/env python3
"""
S1 Content Sourcing Script: Harvest Latin, English, Scholar Quotations for 95 Neoplatonism Conclusions

Usage:
    python scripts/source_s1_content.py --phase [1|2|3]
        Phase 1: Harvest megabase translations (2025-07-04 file)
        Phase 2: Extract scholar quotations from research materials
        Phase 3: Update JSON files with sourced content

    python scripts/source_s1_content.py --file entry_S1.C001.json
        Source a single file

Requirements:
    - Megabase translations: C:\Dev\megabase\chats_2025\2025-07-04_Pico 900 Conclusions Exegesis.md
    - Heretical research notes: C:\Dev\Pico900\data\conclusions\Heretical\S1_RESEARCH_NOTES.md
    - Scholar PDFs indexed in neoplatonism data
"""

import json
import re
from pathlib import Path
from datetime import datetime

# Sourcing metadata: Scholar citations and their key works
SCHOLAR_SOURCES = {
    "Copenhaver": {
        "works": [
            "Pico on Trial: Heresy, Freedom, and Philosophy",
            "Magic and the Dignity of Man"
        ],
        "availability": "megabase (2025-07-05 summary + full text online)",
        "key_pages": {
            "incarnation": [142, 97],
            "eucharist": [70, 96, 12, 11],
            "heresy_belief": [24, 25],
            "henosis": [44, 28],
            "kabbalah": [406, 410]
        }
    },
    "Michael J B Allen": {
        "works": [
            "Neoplatonism and the Platonic Tradition",
            "Synoptic Art"
        ],
        "availability": "cited in project data",
        "key_themes": ["henosis", "emanation", "intellect", "soul_ascent"]
    },
    "Howlett": {
        "works": [
            "On Concordism (chapters on Pico)",
            "Soul Studies"
        ],
        "availability": "cited in research notes",
        "key_themes": ["soul_faculties", "intellect", "virtue_hierarchy"]
    },
    "Wirszubski": {
        "works": [
            "Pico della Mirandola's Encounter with Jewish Mysticism"
        ],
        "availability": "cited in heretical research notes",
        "key_themes": ["kabbalah", "mysticism", "henosis"]
    },
    "Edelheit": {
        "works": [
            "Ficino, Pico and Savonarola",
            "Scholastic Sources (essays)"
        ],
        "availability": "cited in research notes",
        "key_themes": ["metaphysics", "soul", "christology"]
    }
}

# S1 Conclusions Clusters (from RESEARCH_NOTES context)
S1_CLUSTERS = {
    "T1": {"range": (1, 5), "theme": "The One and Emanation"},
    "T2-T5": {"range": (6, 20), "theme": "Henosis and Union with the Good"},
    "T6-T20": {"range": (21, 50), "theme": "Metaphysical Hierarchy, Being, Intellect"},
    "T21-T30": {"range": (51, 75), "theme": "Soul's Faculties and Descent"},
    "T31-T40": {"range": (76, 95), "theme": "Soul's Union with God, Mystical Ascent"},
}

# Heretical flags (from S1_RESEARCH_NOTES.md: Q13 on soul's union with God)
HERETICAL_CONCLUSIONS = list(range(81, 96))  # S1.C81-C95 correspond to Q13 cluster


def create_blank_sourcing_template(conclusion_id: str, order: int) -> dict:
    """Create a blank template for sourcing metadata."""
    return {
        "conclusion_id": conclusion_id,
        "order": order,
        "sourcing_status": {
            "latin_incipit": "unstarted",
            "english_translation": "unstarted",
            "charge": "unstarted",
            "defense": "unstarted",
            "scholar_citations": "unstarted"
        },
        "megabase_refs": [],
        "picodb_refs": [],
        "scholar_annotations": [],
        "confidence_flags": [],
        "last_updated": datetime.now().isoformat()
    }


def harvest_megabase_translations(megabase_path: str) -> dict:
    """
    Extract translations from megabase 2025-07-04 Pico Exegesis file.

    Returns: {conclusion_id: {latin, english, exegesis, source}}
    """
    translations = {}

    try:
        with open(megabase_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠ Megabase file not found: {megabase_path}")
        return translations

    # Pattern: Match conclusions like "I.21.1" with Latin and Translation blocks
    # This is a simplified extraction; full implementation would parse structured sections

    pattern = r'### (I\.\d+\.\d+|II\.\d+\.\d+|[A-Z]+\.\d+\.\d+)\s+\*\*Latin:\*\*(.*?)\*\*Translation:\*\*(.*?)(?:###|$)'

    matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)

    for match in matches:
        conclusion_key = match.group(1).strip()
        latin = match.group(2).strip()
        english = match.group(3).strip()

        # Clean up markdown formatting
        latin = re.sub(r'\*+|\*\*', '', latin).strip()
        english = re.sub(r'\*+|\*\*', '', english).strip()

        translations[conclusion_key] = {
            "latin": latin[:200],  # Incipit (first ~200 chars)
            "english": english[:500],
            "source": "megabase_2025-07-04_Pico_900_Conclusions_Exegesis",
            "translator": "LLM"
        }

    return translations


def get_heretical_flag(conclusion_order: int) -> bool:
    """Check if conclusion is in heretical cluster (Q13: soul's union with God)."""
    return conclusion_order in HERETICAL_CONCLUSIONS


def get_cluster_info(conclusion_order: int) -> dict:
    """Determine which thematic cluster a conclusion belongs to."""
    for cluster_name, cluster_info in S1_CLUSTERS.items():
        start, end = cluster_info["range"]
        if start <= conclusion_order <= end:
            return {
                "cluster": cluster_name,
                "theme": cluster_info["theme"]
            }
    return {"cluster": "unknown", "theme": ""}


def extract_scholar_quotations(conclusion_theme: str) -> list:
    """
    Template for extracting scholar quotations matching a conclusion theme.
    Full implementation would search PDF materials and PicoDB.
    """
    quotations = []

    # Placeholder: Example structure for Copenhaver citations
    if "henosis" in conclusion_theme.lower() or "union" in conclusion_theme.lower():
        quotations.append({
            "scholar": "Copenhaver",
            "work": "Pico on Trial: Heresy, Freedom, and Philosophy",
            "page": "[TO_VERIFY]",
            "quotation": "[EXTRACT FROM SOURCE]",
            "confidence": "UNVERIFIED"
        })

    if "metaphysics" in conclusion_theme.lower() or "hierarchy" in conclusion_theme.lower():
        quotations.append({
            "scholar": "Michael J B Allen",
            "work": "Neoplatonism and the Platonic Tradition",
            "page": "[TO_VERIFY]",
            "quotation": "[EXTRACT FROM SOURCE]",
            "confidence": "UNVERIFIED"
        })

    return quotations


def update_s1_file(file_path: str, sourcing_data: dict, megabase_translations: dict) -> bool:
    """
    Update a single S1 JSON file with sourced content.

    Returns: True if successful, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            entry = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"✗ Error reading {file_path}: {e}")
        return False

    conclusion_id = entry.get("conclusion_id", "")
    order = entry.get("order", 0)
    theme = entry.get("philosophical_theme", "")

    # Update with heretical flag
    if get_heretical_flag(order):
        entry["heretical_flag"] = True
        entry["heretical_notes"] = "Q13 cluster: Soul's union with God. See *Apology* Q13 and heretical research notes."

    # Update with cluster info
    cluster_info = get_cluster_info(order)
    entry["_sourcing"] = {
        "cluster": cluster_info["cluster"],
        "theme": cluster_info["theme"],
        "status": "standardized"
    }

    # Attempt to populate from megabase (if translations were harvested)
    if megabase_translations and conclusion_id in megabase_translations:
        trans = megabase_translations[conclusion_id]
        if not entry.get("latin_incipit"):
            entry["latin_incipit"] = trans.get("latin", "")
            entry["incipit_verified"] = False
        if not entry.get("english_translation"):
            entry["english_translation"] = trans.get("english", "")
            entry["translation_source"] = trans.get("source")
            entry["translation_translator"] = trans.get("translator")

    # Placeholder for charge/defense (would be populated from Copenhaver + trial docs)
    if not entry.get("charge") or entry.get("charge") == "":
        entry["charge"] = "[TO_SOURCE FROM COPENHAVER/TRIAL DOCS]"
    if not entry.get("defense") or entry.get("defense") == "":
        entry["defense"] = "[TO_SOURCE FROM APOLOGY + COPENHAVER]"

    # Add scholar quotations placeholder
    if not entry.get("scholar_citations") or len(entry.get("scholar_citations", [])) == 0:
        entry["scholar_citations"] = extract_scholar_quotations(theme)

    # Mark updated
    entry["updated_date"] = datetime.now().isoformat()

    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"✗ Error writing {file_path}: {e}")
        return False


def main():
    import sys

    project_root = Path(__file__).parent.parent
    s1_dir = project_root / "data" / "conclusions" / "S1"
    megabase_file = Path("C:\\Dev\\megabase\\chats_2025\\2025-07-04_Pico 900 Conclusions Exegesis.md")

    # Phase 1: Harvest megabase
    print("📚 Phase 1: Harvesting megabase translations...")
    megabase_translations = harvest_megabase_translations(str(megabase_file))
    print(f"✓ Extracted {len(megabase_translations)} translation entries from megabase")

    # Phase 2: Update all S1 files
    print("\n📝 Phase 2: Updating S1 JSON files...")
    updated_count = 0
    failed_count = 0

    for file_path in sorted(s1_dir.glob("entry_S1.C*.json")):
        if update_s1_file(str(file_path), {}, megabase_translations):
            updated_count += 1
        else:
            failed_count += 1

    print(f"✓ Updated {updated_count} files")
    if failed_count > 0:
        print(f"✗ Failed to update {failed_count} files")

    print(f"\n✅ S1 sourcing framework initialized.")
    print(f"   Next: Manually source Latin incipits from Brown critical edition")
    print(f"   Next: Extract scholar quotations from E:\\pdf\\renaissance magic\\Pico\\")
    print(f"   Next: Populate charge/defense from Copenhaver + trial documents")


if __name__ == "__main__":
    main()
