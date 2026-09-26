#!/usr/bin/env python3
"""
Bootstrap Pico900: Initialize project structure, create conclusion stubs, validate schema.

Usage:
    python scripts/bootstrap_project.py
        Create manifest template and data structures

    python scripts/bootstrap_project.py --harvest megabase
        Harvest translated conclusions from megabase 2025-07-04 file

    python scripts/bootstrap_project.py --stub [section] [count]
        Create [count] stub conclusions for a given section
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Define conclusion sections and rough counts (to be refined)
SECTIONS = {
    "Conclusiones secundum Avicennam": 12,
    "Conclusiones secundum Averroem": 41,
    "Conclusiones secundum Alfarabium": 11,
    "Conclusiones secundum Adelandum Arabem": 8,
    "Conclusiones secundum Abucaten Avenan": 10,
    "Conclusiones secundum Avempacem Arabem": 2,
    "Conclusiones secundum Isaac Narbonensem": 4,
    "Conclusiones secundum Abumaron Babylonium": 4,
    "Conclusiones secundum Moysem Aegyptium": 3,
    # More sections to be catalogued...
}

SCHEMA = {
    "conclusion_id": "str (e.g., 'I.1.1')",
    "section": "str (one of SECTIONS keys)",
    "latin_incipit": "str (opening words of Latin text)",
    "latin_source": "str enum: 'critical_edition' | 'megabase' | 'picodb'",
    "latin_verified": "bool",
    "english_translation": {
        "text": "str",
        "source": "str (megabase file or 'original_2026')",
        "translator": "str enum: 'LLM' | 'Ted Hand'",
    },
    "exegesis": "str (1-2 paragraphs of philosophical context)",
    "commentary_status": "str enum: 'unstarted' | 'draft' | 'sourced_quotations' | 'complete'",
    "scholar_citations": [
        {
            "scholar": "str (author name)",
            "work": "str (title)",
            "pages": "str or int (page or page range)",
            "quotation": "str (exact quotation)",
            "confidence": "str enum: 'VERIFIED' | 'CITED' | 'INFERRED'",
            "relevance": "str (how this quotation illuminates the conclusion)",
        }
    ],
    "heretical_flag": "bool",
    "heretical_notes": "str (if flagged: charge, defense, debate summary)",
    "tags": ["str (from allowed tag set)"],
    "notes": "str (editorial notes, uncertainties, revisions)",
    "status": "str enum: 'unstarted' | 'draft' | 'sourced' | 'complete' | 'reviewed'",
    "created_date": "ISO 8601 date",
    "updated_date": "ISO 8601 date",
    "assigned_to": "str (LLM agent ID or 'Ted Hand' or None)",
}

ALLOWED_TAGS = {
    "heretical",
    "kabbalah",
    "astrology",
    "magic",
    "metaphysics",
    "logic",
    "theology",
    "soul",
    "intellect",
    "incarnation",
    "eucharist",
    "arabic_philosophy",
    "platonism",
    "aristotlelianism",
    "christian_theology",
    "epistemology",
    "causality",
    "essence_existence",
    "angels",
    "prophecy",
}


def create_conclusion_stub(conclusion_id: str, section: str, latin_incipit: str) -> dict:
    """Create a single conclusion stub."""
    now = datetime.now().isoformat()
    return {
        "conclusion_id": conclusion_id,
        "section": section,
        "latin_incipit": latin_incipit,
        "latin_source": None,
        "latin_verified": False,
        "english_translation": {
            "text": None,
            "source": None,
            "translator": None,
        },
        "exegesis": None,
        "commentary_status": "unstarted",
        "scholar_citations": [],
        "heretical_flag": False,
        "heretical_notes": None,
        "tags": [],
        "notes": None,
        "status": "unstarted",
        "created_date": now,
        "updated_date": now,
        "assigned_to": None,
    }


def create_manifest(sections: dict) -> dict:
    """Create a master manifest with all conclusion stubs."""
    manifest = {
        "project": "Pico900",
        "title": "Digital Edition of Pico's 900 Conclusions",
        "version": "0.1.0",
        "created": datetime.now().isoformat(),
        "sections": {},
        "total_conclusions": 0,
    }

    conclusion_counter = 0

    for section_name, count in sections.items():
        manifest["sections"][section_name] = {
            "count": count,
            "conclusions": [],
        }

        for i in range(1, count + 1):
            conclusion_counter += 1
            section_num = chr(65 + (conclusion_counter // 100))  # A, B, C...
            local_num = (conclusion_counter % 100) or 100
            conclusion_id = f"{section_num}.{i}"

            stub = create_conclusion_stub(
                conclusion_id=conclusion_id,
                section=section_name,
                latin_incipit="[TO BE FILLED]",
            )
            manifest["sections"][section_name]["conclusions"].append(stub)

    manifest["total_conclusions"] = conclusion_counter
    return manifest


def save_manifest(manifest: dict, output_path: Path = None):
    """Save manifest to JSON file."""
    if output_path is None:
        output_path = Path("data") / "conclusions_manifest.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"[OK] Manifest saved to {output_path}")
    print(f"  Total conclusions: {manifest['total_conclusions']}")


def save_schema(output_path: Path = None):
    """Save schema and allowed values to JSON."""
    if output_path is None:
        output_path = Path("data") / "schema.json"

    schema_doc = {
        "title": "Conclusion Entry Schema",
        "version": "1.0",
        "fields": SCHEMA,
        "allowed_tags": sorted(list(ALLOWED_TAGS)),
        "status_values": ["unstarted", "draft", "sourced", "complete", "reviewed"],
        "confidence_values": ["VERIFIED", "CITED", "INFERRED"],
        "sources": ["critical_edition", "megabase", "picodb"],
        "translators": ["LLM", "Ted Hand"],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema_doc, f, indent=2)

    print(f"[OK] Schema saved to {output_path}")


def harvest_megabase_conclusion(
    conclusion_id: str, section: str, latin_text: str, translation: str, exegesis: str
) -> dict:
    """Create a conclusion entry from harvested megabase data."""
    stub = create_conclusion_stub(conclusion_id, section, latin_text[:50])

    stub["latin_incipit"] = latin_text
    stub["latin_source"] = "megabase"
    stub["latin_verified"] = False  # Will be verified against critical edition

    stub["english_translation"]["text"] = translation
    stub["english_translation"]["source"] = "2025-07-04_Pico 900 Conclusions Exegesis.md"
    stub["english_translation"]["translator"] = "LLM"

    stub["exegesis"] = exegesis
    stub["commentary_status"] = "draft"
    stub["status"] = "sourced"

    return stub


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--bootstrap":
            print("Creating project bootstrap...")
            manifest = create_manifest(SECTIONS)
            save_manifest(manifest)
            save_schema()
            print("[OK] Project bootstrap complete")

        elif sys.argv[1] == "--create-heretical-queue":
            print("Creating heretical conclusions queue...")
            heretical_queue = {
                "title": "Heretical Conclusions Processing Queue",
                "description": "Conclusions flagged as condemned or heretical; prioritized for essay synthesis",
                "created": datetime.now().isoformat(),
                "conclusions": [],
                # To be populated by research agents
            }
            output_path = Path("data") / "heretical_queue.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(heretical_queue, f, indent=2)
            print(f"[OK] Heretical queue created at {output_path}")

        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print(__doc__)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
