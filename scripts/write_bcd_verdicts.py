#!/usr/bin/env python3
"""write_bcd_verdicts.py — write data/verification/bcd_entries.verdicts.json
from latin_locator_report.json, for the 840 tier-B/C/D entries promoted to *.json.

Format: one verdict per entry, recording the one mechanical claim that was checked
(Latin text at latin_source locator). Tier-A entries are excluded from this file.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(ROOT, "data", "verification", "latin_locator_report.json")
OUT = os.path.join(ROOT, "data", "verification", "bcd_entries.verdicts.json")

rep = json.load(io.open(REPORT, encoding="utf-8"))
verdicts = []
for r in rep["results"]:
    if r["tier"] == "A":
        continue
    verdicts.append({
        "file": os.path.basename(r["file"]),
        "thesis_id": r["thesis_id"],
        "tier": r["tier"],
        "claim": "latin_at_locator",
        "verdict": r["verdict"],
        "note": r["note"],
        "verifier": rep["verifier"],
        "verified_date": rep["run_date"],
    })

out = {
    "description": ("Verdicts for tier-B/C/D entries: mechanical check that the "
                    "Latin text at latin_source matches the entry's `latin` field. "
                    "Gate G1/G2 (entry_gate.py) passed separately for all 901 drafts."),
    "verifier": rep["verifier"],
    "verified_date": rep["run_date"],
    "n": len(verdicts),
    "verdicts": verdicts,
}
with io.open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print(f"Wrote {len(verdicts)} verdicts to {OUT}")
