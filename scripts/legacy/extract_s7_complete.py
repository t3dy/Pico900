#!/usr/bin/env python3
"""
Extract complete S7 (Secundum Hebraeos) conclusions from Farmer's critical edition.
Includes both:
1. Section 28: Historical Kabbalist conclusions (48 theses)
2. Section 11>: Pico's own magical and Kabbalistic conclusions (72 theses)
Output to data/staging/stage_S7.json for HARVESTER H8.
"""

import json
import re
from pathlib import Path

# Path to Farmer edition text
FARMER_TEXT = Path(r"C:\Dev\AUDIOBOOKMAKERSCHOLARLY\books\medieval-renaissance-texts-studies-167-stephen-a\source\cleaned") / "Medieval Renaissance Texts Studies 167 Stephen A Farmer Giovanni Pico Della Mirandola Syncretism in the West_ Pico s 900 Theses The Evolution of Traditional Religious and Philosophical Systems 2003.txt"

def extract_raw_by_pattern(text, pattern_prefix, stop_pattern=None):
    """Extract theses matching pattern_prefix until stop_pattern or end."""
    conclusions = []

    if pattern_prefix == "28":
        # For 28.N format
        thesis_pattern = rf"^({re.escape(pattern_prefix)}\.\d+)\. ([A-Z][^\n]*(?:\n(?![0-9]+\.)(?![A-Z][^.:]*:\s)(?!\s{{28}}).)*)+"
    else:
        # For 11>N format
        thesis_pattern = rf"^({re.escape(pattern_prefix)}>?\d+)\. ([A-Z][^\n]*(?:\n(?![0-9>]+\.)(?![A-Z][^.:]*:\s)(?!\s{{28}}).)*)+"

    for match in re.finditer(thesis_pattern, text, re.MULTILINE):
        thesis_id = match.group(1)
        content = match.group(2).strip()

        # Extract up to about 200 chars as incipit
        incipit = content[:120].strip()
        if len(content) > 120:
            incipit += "..." if not incipit.endswith('...') else ""

        conclusions.append({
            "thesis_id": thesis_id,
            "incipit": incipit,
            "full_text": content[:500]  # Store first 500 chars
        })

    return conclusions

def extract_section_28(text):
    """Extract section 28 conclusions (historical Kabbalist doctrine)."""
    # Find section 28
    match = re.search(r"^THE HEBREW CABALIST WISEMEN", text, re.MULTILINE)
    if not match:
        match = re.search(r"^28\.1\. ", text, re.MULTILINE)

    if not match:
        print("ERROR: Could not find section 28")
        return []

    start = match.start()

    # Find end (start of next major section or "THESES ACCORDING TO PICO")
    end_match = re.search(r"^CONCLUSIONES NUMERO|^THESES ACCORDING TO PICO|^11\.",
                          text[start+100:], re.MULTILINE)
    if end_match:
        end = start + 100 + end_match.start()
    else:
        end = len(text)

    section_text = text[start:end]

    # Extract theses numbered 28.N
    conclusions = []
    thesis_pattern = r"^28\.(\d+)\. ([A-Z][^\n]*(?:\n[^\n]*)*?)(?=\n28\.\d+\.|$|\n\n[A-Z][A-Z ])"

    for match in re.finditer(thesis_pattern, section_text, re.MULTILINE):
        num = match.group(1)
        full_text = match.group(2).strip()

        # Take first 150 chars as incipit
        incipit = full_text[:150]

        conclusions.append({
            "conclusion_id": f"28.{num}",
            "section": "S7",
            "section_name": "Secundum Hebraeos",
            "subsection": "Historical Kabbalist Theses",
            "latin_incipit": incipit,
            "translation_status": "TO_SOURCE",
            "heretical_flag": False,
            "source": "Farmer 1998, Section 28 (Secundum secretam doctrinam Hebraeorum)"
        })

    return conclusions

def extract_section_11_kabbala(text):
    """Extract section 11> conclusions (Pico's own magical & Kabbalistic conclusions)."""
    # Find section 11>1
    match = re.search(r"^11>1\. Quicquid dicant", text, re.MULTILINE)
    if not match:
        print("WARNING: Could not find section 11>1")
        return []

    start = match.start()

    # Find end (next major section or end of 11> numbering)
    end_match = re.search(r"^[0-9]+\. (?!Quicquid|Vbi|Per|Cum|Nisi|Omnes|Rectius|Nunqua|Similis|Ex|Quam|Non|Quia|Si|Deus|Qui|Nemo)",
                          text[start+100:], re.MULTILINE)
    if end_match:
        end = start + 100 + end_match.start()
    else:
        end = len(text)

    section_text = text[start:end]

    # Extract theses numbered 11>N
    conclusions = []
    thesis_pattern = r"^11>(\d+)\. ([A-Z][^\n]*(?:\n[^\n]*)*?)(?=\n11>\d+\.|$|\n\n[A-Z][A-Z ])"

    for match in re.finditer(thesis_pattern, section_text, re.MULTILINE):
        num = match.group(1)
        full_text = match.group(2).strip()

        # Take first 150 chars as incipit
        incipit = full_text[:150]

        conclusions.append({
            "conclusion_id": f"11>{num}",
            "section": "S7",
            "section_name": "Secundum Hebraeos (Pico's own opinions)",
            "subsection": "Magical & Kabbalistic Conclusions",
            "latin_incipit": incipit,
            "translation_status": "TO_SOURCE",
            "heretical_flag": False,
            "source": "Farmer 1998, Section 11> (Conclusiones secundum opinionem propriam: Magia & Cabala)"
        })

    return conclusions

def load_scholar_citations():
    """Load known scholar citations from PicoDB."""
    return {
        "Wirszubski": {
            "scholar": "Chaim Wirszubski",
            "work": "Pico della Mirandola's Encounter with Jewish Mysticism",
            "year": 1989,
            "type": "monograph"
        },
        "Copenhaver": {
            "scholar": "Brian P. Copenhaver",
            "work": "Magic and the Dignity of Man",
            "work_full": "Magic and the Dignity of Man: De-Kanting Pico's Oration (2002)",
            "type": "chapter"
        },
        "Scholem": {
            "scholar": "Gershom Scholem",
            "work": "Major Trends in Jewish Mysticism",
            "year": 1941,
            "type": "monograph"
        },
        "Busi": {
            "scholar": "Giulio Busi",
            "work": "Giovanni Pico della Mirandola: Mito, magia, Qabbalah",
            "year": 2014,
            "type": "volume"
        }
    }

if __name__ == "__main__":
    print("Extracting complete S7 (Secundum Hebraeos)...")

    with open(FARMER_TEXT, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Extract both sections
    section_28 = extract_section_28(full_text)
    section_11 = extract_section_11_kabbala(full_text)

    print(f"Section 28 (historical): {len(section_28)} conclusions")
    print(f"Section 11> (own opinions): {len(section_11)} conclusions")
    print(f"Total S7: {len(section_28) + len(section_11)} conclusions")

    # Combine and add metadata
    all_conclusions = section_28 + section_11

    # Add scholar citations
    scholars = load_scholar_citations()
    for conclusion in all_conclusions:
        conclusion["scholar_citations"] = [
            {
                "scholar": scholars["Wirszubski"]["scholar"],
                "work": scholars["Wirszubski"]["work"],
                "quotation": "[TO_SOURCE]",
                "verified": False
            },
            {
                "scholar": scholars["Copenhaver"]["scholar"],
                "work": scholars["Copenhaver"]["work_full"],
                "quotation": "[TO_SOURCE]",
                "verified": False
            },
            {
                "scholar": scholars["Scholem"]["scholar"],
                "work": scholars["Scholem"]["work"],
                "quotation": "[TO_SOURCE]",
                "verified": False
            }
        ]

    # Create output structure
    output = {
        "section": "S7",
        "section_name": "Secundum Hebraeos (Kabbalah & Jewish Philosophy)",
        "count": len(all_conclusions),
        "incipit_range": "T606–T720",
        "status": "HARVESTER_H8_EXTRACTION",
        "metadata": {
            "source": "Farmer 1998, Syncretism in the West: Pico's 900 Theses",
            "subsections": [
                {
                    "name": "Historical Kabbalist Theses",
                    "pattern": "28.N",
                    "count": len(section_28),
                    "description": "Secundum secretam doctrinam sapientum Hebraeorum Cabalistarum"
                },
                {
                    "name": "Pico's Own Magical & Kabbalistic Conclusions",
                    "pattern": "11>N",
                    "count": len(section_11),
                    "description": "Conclusiones secundum opinionem propriam (Magic & Kabbalah)"
                }
            ],
            "critical_note": "S7 is essential for understanding Q5 (magic & Kabbalah as proof of Christ's divinity). Hebrew primary sources limited; English translations require supplementary research in megabase and PicoDB.",
            "phase": "Phase 1 Extraction",
            "agent": "HARVESTER H8 (Strongest Agent)"
        },
        "conclusions": all_conclusions
    }

    # Save to JSON
    output_path = Path(r"C:\Dev\Pico900\data\staging")
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / "stage_S7.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nOutput saved to {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")

    # Show sample
    print("\nSample conclusions:")
    for c in all_conclusions[:3]:
        print(f"  {c['conclusion_id']}: {c['latin_incipit'][:80]}...")
    print("  ...")
    for c in all_conclusions[-2:]:
        print(f"  {c['conclusion_id']}: {c['latin_incipit'][:80]}...")
