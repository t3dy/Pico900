#!/usr/bin/env python3
"""quarantine_banner.py: prepend a warning banner to pre-audit documents whose quotations or claims
failed verification, so an agent that opens one cannot mistake it for evidence. Idempotent.
Text files are not deleted or rewritten; the history stays readable, clearly marked."""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- QUARANTINE-BANNER -->"

TARGETS = {
    "docs/ANGELICRESEARCH.md":
        "audit/A3 found its Heptaplus 'seven-layer' scheme is in neither Pico nor Black, its Kabbalistic layer rests on "
        "text where Pico declines to give the Hebrew angelology, and its scholar attributions are unfindable.",
    "docs/NEOPLATONISM_MODULE_SUMMARY.md":
        "audit/A3: the module's validation certified JSON shape only; claims of verified citations and resolved "
        "cross-references are untested (50 of 146 cross-references resolve to nothing).",
    "docs/NEOPLATONISM_WORKFLOW.md": "audit/A3: certified by shape-only validators. See audit/A3_angelology_neoplatonism.md.",
    "docs/NEOPLATONISM_QUICKREF.md": "audit/A3: certified by shape-only validators. See audit/A3_angelology_neoplatonism.md.",
    "docs/NEOPLATONISM_SOURCING_PROTOCOL.md": "audit/A3: certified by shape-only validators. See audit/A3_angelology_neoplatonism.md.",
    "docs/SOURCES_FEATURE.md":
        "audit/A3 found data/sources.json holds 46 of a claimed 87 sources, is a list of supposed influences and not a "
        "bibliography, and that at least eight of ten rows checked contain factual errors.",
    "docs/S7_KABBALISTIC_CITATION_PROTOCOL.md":
        "audit/A1 found the citations this protocol produced are three strings repeated across 118 entries, one of "
        "them absent from every source and one misattributed.",
    "data/scholarships/angels/README.md":
        "audit/A3: the lineage files' 'verified' status is untested; 46 of 129 passages still contain placeholders.",
    "docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md":
        "audit/A2_essay_and_notes.md found that none of the 25 passages attributed to Copenhaver here is verbatim "
        "(17 appear in no source; 8 are altered paraphrases), the chronology is wrong (the commission sat in 1487, not "
        "March 1486; the bull is 4 August 1487), and the central argument is contradicted by Copenhaver (CT 8574-8577).",
    "data/conclusions/Heretical/S1_RESEARCH_NOTES.md":
        "audit/A1 and A2 found the scholar quotations and page numbers here are not verbatim or are misplaced, and that "
        "it gives Latin for Q4, Q6 and Q9 that occurs nowhere in the 900 and misnames Q2 as 'original sin'.",
    "docs/S2_HERETICAL_ESSAY_METHODOLOGY_REPORT.md":
        "audit/A2 found factual and bibliographic errors here (mis-gendered scholars, unconfirmed titles, speculative "
        "attributions to works not read).",
    "docs/HERETICAL_RESEARCH_PLAN.md":
        "audit/A2 found pre-reading hypotheses here later re-issued as quotations (lines 84-85, 117) and misnamed "
        "bibliography. Treat every claim as a lead, not a finding.",
}

for rel, why in TARGETS.items():
    p = os.path.join(ROOT, rel)
    with io.open(p, encoding="utf-8") as fh:
        body = fh.read()
    if MARK in body:
        continue
    banner = (MARK + "\n> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  \n> " + why +
              "  \n> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.\n\n")
    with io.open(p, "w", encoding="utf-8") as fh:
        fh.write(banner + body)
    print("bannered", rel)
