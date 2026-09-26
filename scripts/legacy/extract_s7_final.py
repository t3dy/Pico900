#!/usr/bin/env python3
"""
Final extraction of S7 (Secundum Hebraeos) conclusions.
Properly extracts only Latin incipits (avoids notes and English translations).
Output: data/staging/stage_S7.json
"""

import json
import re
from pathlib import Path

FARMER_TEXT = Path(r"C:\Dev\AUDIOBOOKMAKERSCHOLARLY\books\medieval-renaissance-texts-studies-167-stephen-a\source\cleaned") / "Medieval Renaissance Texts Studies 167 Stephen A Farmer Giovanni Pico Della Mirandola Syncretism in the West_ Pico s 900 Theses The Evolution of Traditional Religious and Philosophical Systems 2003.txt"

def extract_conclusions():
    """Extract S7 conclusions with Latin incipits and English translations."""

    with open(FARMER_TEXT, 'r', encoding='utf-8') as f:
        text = f.read()

    conclusions = []

    # Pattern 1: Extract 28.N theses (Latin only, no notes or English)
    # Latin appears first, then blank line, then notes, then English
    # Capture only the first occurrence of "28.N. "
    section_28_pattern = r"^28\.(\d+)\. ([A-Z][^\n]*(?:\n[a-z][^\n]*)*?)(?=\n\n28\.\d|^28\.\d|\n[A-Z][A-Z ]{10,}|$)"

    for match in re.finditer(section_28_pattern, text, re.MULTILINE):
        thesis_num = match.group(1)
        latin_text = match.group(2).strip()

        # Find corresponding English translation
        # English version appears as "28.N. [English]... (page#)"
        english_pattern = rf"^28\.{re.escape(thesis_num)}\. ((?:[A-Z][^(]*?))\s*\([0-9]+\)"
        english_match = re.search(english_pattern, text, re.MULTILINE)
        english_text = english_match.group(1).strip() if english_match else "[TO_TRANSLATE]"

        conclusions.append({
            "conclusion_id": f"28.{thesis_num}",
            "section": "S7",
            "section_name": "Secundum Hebraeos (Historical Kabbalist Doctrine)",
            "subsection": "Secundum secretam doctrinam sapientum Hebraeorum Cabalistarum",
            "type": "historical",
            "latin_incipit": latin_text[:120],
            "latin_full": latin_text[:500],
            "english_translation": english_text[:150] if english_text != "[TO_TRANSLATE]" else "[TO_TRANSLATE]",
            "english_full": english_text[:500] if english_text != "[TO_TRANSLATE]" else "[TO_TRANSLATE]",
            "translation_source": "Farmer 1998" if english_text != "[TO_TRANSLATE]" else "TO_SOURCE",
            "heretical_flag": False,
            "is_condemned": False,
            "tags": ["Kabbalah", "sefirot", "mysticism", "Hebrew", "theurgy"]
        })

    # Pattern 2: Extract 11>N theses (Pico's own conclusions)
    # Same pattern as above
    section_11_pattern = r"^11>(\d+)\. ([A-Z][^\n]*(?:\n[a-z][^\n]*)*?)(?=\n\n11>\d|^11>\d|\n[A-Z][A-Z ]{10,}|$)"

    for match in re.finditer(section_11_pattern, text, re.MULTILINE):
        thesis_num = match.group(1)
        latin_text = match.group(2).strip()

        # Find corresponding English translation
        english_pattern = rf"^11>{re.escape(thesis_num)}\. ((?:[A-Z][^(]*?))\s*(?:\([0-9]+\)|$)"
        english_match = re.search(english_pattern, text, re.MULTILINE)
        english_text = english_match.group(1).strip() if english_match else "[TO_TRANSLATE]"

        conclusions.append({
            "conclusion_id": f"11>{thesis_num}",
            "section": "S7",
            "section_name": "Secundum Hebraeos (Pico's Own Magical & Kabbalistic Conclusions)",
            "subsection": "Conclusiones secundum opinionem propriam: Magia & Cabala",
            "type": "personal",
            "latin_incipit": latin_text[:120],
            "latin_full": latin_text[:500],
            "english_translation": english_text[:150] if english_text != "[TO_TRANSLATE]" else "[TO_TRANSLATE]",
            "english_full": english_text[:500] if english_text != "[TO_TRANSLATE]" else "[TO_TRANSLATE]",
            "translation_source": "Farmer 1998" if english_text != "[TO_TRANSLATE]" else "TO_SOURCE",
            "heretical_flag": False,
            "is_condemned": False,
            "tags": ["Kabbalah", "magic", "divine names", "gematria", "letter combination"]
        })

    return conclusions

def add_scholar_citations(conclusions):
    """Add standard scholar citations to all conclusions."""

    base_citations = [
        {
            "scholar": "Chaim Wirszubski",
            "work": "Pico della Mirandola's Encounter with Jewish Mysticism",
            "year": 1989,
            "status": "[TO_SOURCE]",
            "verified": False
        },
        {
            "scholar": "Brian P. Copenhaver",
            "work": "Magic and the Dignity of Man (in: The Italian Renaissance in the Twentieth Century)",
            "year": 2002,
            "status": "[TO_SOURCE]",
            "verified": False
        },
        {
            "scholar": "Gershom Scholem",
            "work": "Major Trends in Jewish Mysticism",
            "year": 1941,
            "status": "[TO_SOURCE]",
            "verified": False
        }
    ]

    for conclusion in conclusions:
        conclusion["scholar_citations"] = base_citations.copy()
        conclusion["charge"] = "[TO_SOURCE]"
        conclusion["pico_defense"] = "[TO_SOURCE]"

    return conclusions

if __name__ == "__main__":
    print("Extracting S7 conclusions (final)...")

    conclusions = extract_conclusions()
    conclusions = add_scholar_citations(conclusions)

    # Count by type
    hist_count = sum(1 for c in conclusions if c['type'] == 'historical')
    own_count = sum(1 for c in conclusions if c['type'] == 'personal')

    print(f"\nExtraction Summary:")
    print(f"  Historical (28.N): {hist_count}")
    print(f"  Pico's Own (11>N): {own_count}")
    print(f"  Total: {len(conclusions)}")

    # Create output
    output = {
        "section": "S7",
        "section_name": "Secundum Hebraeos - Kabbalah & Jewish Philosophy",
        "description": "115 conclusions on Kabbalistic doctrine, sefirot, divine names, and mystical union. Spans Pico's engagement with Hebrew mysticism through Flavius Mithridates' translations. Essential for understanding Q5 (Heretical Conclusion: Magic & Kabbalah demonstrate Christ's divinity).",
        "incipit_range": "T606–T720",
        "estimated_count": 115,
        "actual_count": len(conclusions),
        "status": "HARVESTER_H8_EXTRACTION_COMPLETE",
        "metadata": {
            "agent": "HARVESTER H8 (Strongest Agent)",
            "phase": "Phase 1 Foundation",
            "priority": "TIER 1 (Special: despite sparse direct coverage, essential for Pico's syncretic project)",
            "source_text": "Farmer, S.A. (1998). Syncretism in the West: Pico's 900 Theses. Medieval & Renaissance Texts & Studies 167.",
            "subsections": {
                "historical_kabbalist_theses": {
                    "label": "Secundum secretam doctrinam sapientum Hebraeorum Cabalistarum",
                    "count": hist_count,
                    "pattern": "28.N",
                    "description": "Conclusions attributed to Kabbalist doctrine; Pico here reports rather than endorses"
                },
                "picos_own_conclusions": {
                    "label": "Conclusiones secundum opinionem propriam",
                    "count": own_count,
                    "pattern": "11>N",
                    "description": "Pico's personal magical & Kabbalistic conclusions; he fully endorses these"
                }
            },
            "critical_notes": [
                "Hebrew primary sources extremely limited in English translation",
                "Translations depend on Mithridates' Latin versions (Codex Vaticanus Ebr. 190)",
                "Mithridates' versions contain interpolated Christianizing glosses",
                "This section directly feeds Q5 (Heretical) defense: Pico's proof that magic & Kabbalah demonstrate Christ",
                "Sefirot system: correlates with Neoplatonic henads, angels, and Christian Trinity",
                "Letter combination (gematria): Hebrew alphabet as key to hidden meanings in Scripture"
            ]
        },
        "conclusions": conclusions
    }

    # Save JSON
    output_path = Path(r"C:\Dev\Pico900\data\staging\stage_S7.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nJSON saved to {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

    # Sample output
    print("\nFirst 3 conclusions:")
    for c in conclusions[:3]:
        print(f"  {c['conclusion_id']}: {c['latin_incipit']}")

    print("\n... (conclusions 4-" + str(len(conclusions)-2) + ") ...")

    print(f"\nLast 2 conclusions:")
    for c in conclusions[-2:]:
        print(f"  {c['conclusion_id']}: {c['latin_incipit']}")

