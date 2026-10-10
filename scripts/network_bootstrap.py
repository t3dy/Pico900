#!/usr/bin/env python3
"""network_bootstrap.py: Create data/network/persons.json from parties.json

    python scripts/network_bootstrap.py --source parties.json --merge
        Converts data/claims/parties.json into data/network/persons.json;
        person IDs replace party slugs; alternate names from aliases.

    python scripts/network_bootstrap.py --status
        Report: count of persons, proposed, speculative, verified.

Phase 0 bootstrap: 40+ persons with >=1 locator, authority source, alternate names.
Later phases link these to relationships, text-person scoring, and evidence.
"""
import argparse, io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NET = os.path.join(ROOT, "data", "network")
PARTIES_PATH = os.path.join(ROOT, "data", "claims", "parties.json")
PERSONS_PATH = os.path.join(NET, "persons.json")
MANIFEST_PATH = os.path.join(NET, "persons_manifest.json")


def ensure_network_dir():
    os.makedirs(NET, exist_ok=True)


def load_parties():
    with io.open(PARTIES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def parties_to_persons(parties_doc):
    """Convert parties.json structure to persons.json."""
    persons = []
    for party in parties_doc.get("parties", []):
        person = {
            "person_id": party["id"],  # surrogate key
            "canonical_name": party["name"],
            "sort_name": party["name"].split()[-1] if " " in party["name"] else party["name"],
            "alternate_names": [],
            "birth_year": None,
            "death_year": None,
            "occupations": [],
            "intellectual_traditions": [],
            "languages": [],
            "authoritative_sources": [],
            "locators": [],  # will be populated in Phase 1 from Farmer + corpus
            "evidence_status": "draft",  # will be verified in Phase 1
            "notes": "",
        }

        # Aliases become alternate_names
        if "aliases" in party:
            for alias in party["aliases"]:
                person["alternate_names"].append({
                    "form": alias,
                    "language": "Latin|English",
                    "period": "c. 1480–1500",
                })

        # Mark proposed parties
        if party.get("proposed"):
            person["evidence_status"] = "speculative"

        persons.append(person)

    return persons


def write_persons(persons):
    """Write persons.json and manifest."""
    ensure_network_dir()

    # Write persons
    with io.open(PERSONS_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(persons, fh, indent=2, ensure_ascii=False)

    # Write manifest
    manifest = {
        "created": "2026-09-28",
        "source": "data/claims/parties.json",
        "count": len(persons),
        "status": "Phase 0 bootstrap",
        "note": "Person IDs from party slugs; alternate names from aliases. Locators (Farmer page, authority source) to be added in Phase 1. Every person marked draft or speculative pending verification.",
    }
    with io.open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    print(f"wrote {os.path.relpath(PERSONS_PATH, ROOT)}: {len(persons)} persons")
    print(f"wrote {os.path.relpath(MANIFEST_PATH, ROOT)}")


def report_status():
    """Print current status."""
    if not os.path.exists(PERSONS_PATH):
        print("data/network/persons.json: NOT FOUND (run --source to create)")
        return

    with io.open(PERSONS_PATH, encoding="utf-8") as fh:
        persons = json.load(fh)

    total = len(persons)
    speculative = sum(1 for p in persons if p.get("evidence_status") == "speculative")
    verified = sum(1 for p in persons if p.get("evidence_status") == "verified")

    print(f"persons.json: {total} total, {speculative} speculative, {verified} verified")
    print("Phase 0 deliverables:")
    print("  - Person records: " + ("✓" if total >= 40 else "✗ need " + str(40 - total)))
    print("  - Manifest: ✓" if os.path.exists(MANIFEST_PATH) else "✗")
    print("Pending:")
    print("  - Locators (Farmer page, authority source): Phase 1")
    print("  - Relationship extraction: Phase 1-Alpha")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="source vocab (parties.json)")
    ap.add_argument("--merge", action="store_true", help="merge into persons.json")
    ap.add_argument("--status", action="store_true", help="report status")
    a = ap.parse_args()

    if a.status:
        report_status()
    elif a.source and a.merge:
        parties_doc = load_parties()
        persons = parties_to_persons(parties_doc)
        write_persons(persons)
    else:
        ap.print_help()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
