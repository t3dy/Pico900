#!/usr/bin/env python3
"""
Extract S7 (Secundum Hebraeos) conclusions from Farmer's critical edition.
Output to data/staging/stage_S7.json for HARVESTER H8.
"""

import json
import re
from pathlib import Path

# Path to Farmer edition text
FARMER_TEXT = Path(r"C:\Dev\AUDIOBOOKMAKERSCHOLARLY\books\medieval-renaissance-texts-studies-167-stephen-a\source\cleaned") / "Medieval Renaissance Texts Studies 167 Stephen A Farmer Giovanni Pico Della Mirandola Syncretism in the West_ Pico s 900 Theses The Evolution of Traditional Religious and Philosophical Systems 2003.txt"

def extract_section_28():
    """Extract all conclusions from section 28 (Secundum Hebraeos)."""

    with open(FARMER_TEXT, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find section 28 start
    section_28_match = re.search(r"^28\.1\. Sicut homo", text, re.MULTILINE)
    if not section_28_match:
        print("ERROR: Could not find section 28")
        return []

    # Extract section 28 (from 28.1 onwards)
    section_28_start = section_28_match.start()

    # Find where section 28 ends (look for start of next section or end of file)
    # Section 29 would start with "^29\." but based on the structure, section 28 is likely the last
    # or we can look for "THESES ACCORDING TO PICO'S OWN OPINION" or similar
    section_end_match = re.search(r"^(?:29\.|CONCLUSIONES SECUNDUM|THESES ACCORDING TO PICO)",
                                  text[section_28_start:], re.MULTILINE)
    if section_end_match:
        section_28_end = section_28_start + section_end_match.start()
    else:
        section_28_end = len(text)

    section_28_text = text[section_28_start:section_28_end]

    # Extract all conclusions with pattern: "28.N. Latin text"
    # The pattern is: thesis number, followed by Latin (uppercase first word)
    # Then on next line or after, English translation

    conclusions = []

    # Split by thesis number
    thesis_pattern = r"^(\d+\.\d+)\. ([A-Z][^.\n]*(?:\n[a-z][^\n]*)*)(?:\n|$)"

    for match in re.finditer(thesis_pattern, section_28_text, re.MULTILINE):
        thesis_id = match.group(1)
        full_text = match.group(2).strip()

        # Split Latin from English (Latin is all caps or mixed case, English starts after \n)
        lines = full_text.split('\n')

        # Latin is typically the first part (before a blank line or before lowercase English start)
        latin_lines = []
        english_start_idx = 0

        for i, line in enumerate(lines):
            # English translations typically start with numbers (e.g., "(360)") or after capitalized opening
            if (line and line[0].islower() and not line.startswith('id est') and
                not line.startswith('et ') and i > 0):
                english_start_idx = i
                break
            latin_lines.append(line)

        latin = ' '.join(latin_lines).strip()
        english = ' '.join(lines[english_start_idx:]).strip() if english_start_idx < len(lines) else ""

        # Remove trailing notes/references in English
        english = re.sub(r'\s+\([0-9]{3}\).*$', '', english)

        if latin:
            conclusions.append({
                "conclusion_id": thesis_id,
                "section": "S7",
                "section_name": "Secundum Hebraeos",
                "latin_incipit": latin[:100] if len(latin) > 100 else latin,  # Store incipit only
                "latin_full": latin,
                "english_translation": english[:150] if len(english) > 150 else english,
                "english_full": english,
                "source": "Farmer 1998 (Syncretism in the West)",
                "topics": ["Kabbalah", "sefirot", "Hebrew", "mysticism", "divine names"],
                "charge": "[TO_SOURCE]",
                "defense": "[TO_SOURCE]",
                "scholar_citations": [
                    {
                        "scholar": "Wirszubski",
                        "work": "Pico della Mirandola's Encounter with Jewish Mysticism",
                        "quotation": "[TO_SOURCE]"
                    },
                    {
                        "scholar": "Copenhaver",
                        "work": "Magic and the Dignity of Man",
                        "quotation": "[TO_SOURCE]"
                    }
                ]
            })

    return conclusions

if __name__ == "__main__":
    print("Extracting S7 conclusions...")
    conclusions = extract_section_28()

    print(f"Extracted {len(conclusions)} conclusions")

    # Sample output
    if conclusions:
        print("\nFirst 3 conclusions:")
        for c in conclusions[:3]:
            print(f"  {c['conclusion_id']}: {c['latin_incipit']}")

    # Save to JSON
    output = {
        "section": "S7",
        "section_name": "Secundum Hebraeos",
        "count": len(conclusions),
        "incipit_range": "T606–T720",
        "conclusions": conclusions
    }

    output_path = Path(r"C:\Dev\Pico900\data\staging\stage_S7.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to {output_path}")
