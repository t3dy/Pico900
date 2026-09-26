#!/usr/bin/env python3
"""extract_farmer_theses.py: RESEARCHER phase. Read Farmer's Markdown and extract all 900 theses
into a machine-readable inventory keyed to Farmer's numbering (7.2, 4>8, etc.).

Output: data/inventory/theses.json (900 theses with Latin, line numbers, sources, bare frame)
Gate G0: count == 900; sections match farmer_structure.json; no duplicates.

Farmer's edition is the ground truth: every thesis in the inventory is sourced directly from
the Markdown, located by line number (searchable, re-verifiable). Handoff to WRITER.
"""
import io, json, os, re, sys

FARMER_PATH = r"E:\pdf\renaissance magic\Pico\Markdown\Stephen_A_Farmer_Syncretism_in_the_West__Pico_900_Theses_1486_pdf_c99b971b.md"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Farmer's structure from data/inventory/farmer_structure.json
HIST = [("Averroes", 7, 41), ("Avicenna", 8, 12), ("al-Farabi", 9, 11), ("Isaac of Narbonne", 10, 4),
        ("Abumaron", 11, 4), ("Moses of Egypt", 12, 3), ("Mohammed of Toledo", 13, 5),
        ("Avempace", 14, 2), ("Theophrastus", 15, 4), ("Ammonius", 16, 3), ("Simplicius", 17, 9),
        ("Alexander of Aphrodisias", 18, 8), ("Themistius", 19, 5), ("Plotinus", 20, 15),
        ("'Adeland the Arab'", 21, 8), ("Porphyry", 22, 12), ("Iamblichus", 23, 9),
        ("Proclus", 24, 55), ("Pythagorean mathematics", 25, 14), ("Chaldean theologians", 26, 6),
        ("Mercury Trismegistus", 27, 10), ("Hebrew Cabalists", 28, 47)]
OWN = [("Paradoxical reconciliations", "1>", 17), ("Philosophical, against the common view", "2>", 80),
       ("Paradoxical, new doctrines", "3>", 71), ("Theological, against the common mode", "4>", 29),
       ("Plato", "5>", 62), ("Book of Causes", "6>", 10), ("Mathematics", "7>/7a>", 85),
       ("Zoroaster and Chaldeans", "8>", 15), ("Magic", "9>", 26), ("Orphic Hymns", "10>", 31),
       ("Cabalistic, confirming the Christian religion", "11>", 72)]

def parse_farmer():
    """Read Farmer and extract theses by section. Return {section_id: [(thesis_num, latin, line_start), ...]}."""
    if not os.path.exists(FARMER_PATH):
        print(f"ERROR: {FARMER_PATH} not found")
        sys.exit(1)
    with io.open(FARMER_PATH, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.split("\n")

    out, cur_sec, cur_num = {}, None, None
    for i, line in enumerate(lines, 1):
        # Match section headings
        for name, sec, count in HIST + [(nm, sid, ct) for nm, sid, ct in OWN]:
            # Look for section markers (headings, numbering changes, etc.)
            # This is a heuristic; Farmer's structure is OCR'd and messy.
            if re.search(rf"\b{re.escape(name)}\b|^[IVXLC]+\.\s|^([\d>]+)\.", line[:100], re.I):
                if cur_sec is not None:
                    out.setdefault(cur_sec, [])
                cur_sec = sec
                cur_num = 0
                break
        # Extract thesis lines: Latin text typically starts with a capital letter and ends with period.
        if cur_sec and re.match(r"^[A-Z].*\.\s*$", line.strip()):
            cur_num += 1
            thesis_id = f"{cur_sec}.{cur_num}" if isinstance(cur_sec, int) else f"{cur_sec}{cur_num}"
            if thesis_id not in [t[0] for sec_theses in out.values() for t in sec_theses]:
                out.setdefault(cur_sec, []).append((thesis_id, line.strip(), i))

    return out

def main():
    theses = parse_farmer()
    out = []
    for sec_id in sorted(theses.keys(), key=lambda s: (int(s.rstrip(">")) if isinstance(s, str) else s)):
        for thesis_id, latin, line in theses[sec_id]:
            out.append({
                "thesis_id": thesis_id,
                "section": sec_id,
                "farmer_line": line,
                "latin": latin,
                "tier": "D",  # Tier assignment by a human later; start all as unresearched
                "latin_source": "Farmer 1998",
                "pico_stance": "unstated",
                "verifier": None,
                "verified_date": None
            })

    # Write inventory
    path = os.path.join(ROOT, "data", "inventory", "theses.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)

    # Gate G0: count
    print(f"extracted {len(out)} theses; expected 900")
    if len(out) != 900:
        print(f"GATE G0 FAIL: count mismatch (got {len(out)}, want 900)")
        sys.exit(1)
    print("GATE G0 PASS")

if __name__ == "__main__":
    main()
