# S1 Harvester Protocol — Secundum Platonicos Extraction (H2)

**Date**: 2026-09-25  
**Harvester**: H2  
**Target**: Extract 95 Neoplatonic conclusions (T1–T95)  
**Output**: `data/staging/stage_S1.json`  
**Status**: SEEDED — Template and metadata complete; Latin incipits + translations + citations pending

---

## Quick Start

1. **Open**: `data/staging/stage_S1.json`
2. **Reference**: 
   - Latin incipits → https://cds.lib.brown.edu/cds-project/picos-900-theses
   - Translations → Megabase 2025-07-04 "Pico 900 Conclusions Exegesis.md"
   - Scholarship → E:\pdf\renaissance magic\Pico\ (PDF corpus)

3. **Workflow**: 
   - For each conclusion T1–T95:
     1. Fetch Latin incipit from critical edition
     2. Search megabase for English translation (by Neoplatonic keyword)
     3. Extract 3–4 scholar quotations (page-specific)
     4. Mark incipit_verified: true, heretical_flag (if applicable)
     5. Update status → "translation_sourced" or "commentary_ready"

4. **Commit**: Every 10 conclusions with message: "S1 conclusions T[N]–T[N+10]: Latin + translations + scholar citations"

---

## Latin Incipits: Where to Find Them

### Primary Source: Brown Critical Edition
- URL: https://cds.lib.brown.edu/cds-project/picos-900-theses
- Structure: Browse by section ("Secundum Platonicos"), click each conclusion to view Latin
- Verification: Cross-check against Farmer's critical edition (1998)

### Secondary Source: Farmer's Critical Edition (1998)
- Title: *Giovanni Pico della Mirandola: Conclusiones nongentae* (critical edition)
- Available: Check C:\Dev\megabase\ or PDFs in E:\pdf\renaissance magic\Pico\

---

## Translations: Megabase Sources

### Main Translation Pass: 2025-07-04
File: C:\Dev\megabase\chats_2025\2025-07-04_Pico 900 Conclusions Exegesis.md

Search for Neoplatonic keywords: "Plotinus", "emanation", "henosis", "soul", "intellect", "One", "Beauty", "daemons", "henads", "mysticism"

Extract translations that match S1 theme/number. Cite as: "Megabase 2025-07-04_Pico 900 Conclusions Exegesis.md"

### Original Translation (If Needed)
If no megabase translation found, translate from Latin yourself. Mark as: "translator": "Ted Hand 2026" and "translation_source": "original_2026"

---

## Scholar Quotations: PDF Corpus Strategy

### The Four Essential Sources

#### 1. Michael J B Allen — Neoplatonism and the Platonic Tradition
- File: E:\pdf\renaissance magic\Pico\(Variorum Collected Studies 1063) Allen...pdf
- Chapters: Look for chapters on Pico's Neoplatonism, Plotinus, Proclus, henads
- Citation: "Allen, Neoplatonism and the Platonic Tradition (Routledge 2017), p. [PAGE]"

#### 2. Brian P Copenhaver — Pico on Trial (2022)
- File: E:\pdf\renaissance magic\Pico\Brian P Copenhaver Pico della Mirandola on Trial...pdf
- Key Chapter: Ch. 5 — Mystical Theology and the Soul
- Focus: Copenhaver analyzes Q13 (condemned) in context of Neoplatonic mysticism
- Citation: "Copenhaver, Pico on Trial (Harvard UP 2022), p. [PAGE]"

#### 3. Amos Howlett — Concordism and 900 Structure
- Focus: Reconciles Aristotelian causality with Platonic emanation
- Check E:\pdf\renaissance magic\Pico\ or megabase

#### 4. Wirszubski & Kristeller — Pico's Encounter with Jewish Mysticism
- File: E:\pdf\renaissance magic\Pico\Chaim Wirszubski Paul Oskar Kristeller...pdf
- Chapters: henads ↔ sefirot parallel; Neoplatonism + Kabbalah synthesis
- Citation: "Wirszubski & Kristeller, Pico's Encounter with Jewish Mysticism (Harvard UP 1989), p. [PAGE]"

### Extraction Workflow

For each conclusion (or cluster):

1. Identify Neoplatonic theme (e.g., "The One", "Soul", "Daemons")
2. Search Allen's index or TOC for chapter on that theme
3. Read that chapter and find passage discussing Pico's treatment
4. Extract exact quotation (include enough context)
5. Record: Scholar name, work, page number, quotation text, verified: true
6. Repeat for Copenhaver, Howlett, Wirszubski

---

## Heretical Flagging: Checklist

Mark heretical_flag: true if:

- Thesis mentions theurgy or "divine working" (theurgic innovation = condemned Q5)
- Thesis addresses daemon magic or daemon invocation (condemned Q5)
- Thesis uses "divine names" (Kabbalistic/theurgic signature; Q5)
- Thesis discusses soul's union with God or henosis in mystical/ecstatic terms (Q13 condemned)
- Thesis on angel magic or angel invocation (Q5 neighbor)
- Copenhaver marks it as controversial in Pico on Trial Ch. 5

Reference: S1_RESEARCH_NOTES.md (Heretical conclusions synthesis) for Q5, Q13 exact charges.

---

## Status Levels

| Status | Meaning |
|--------|---------|
| incipit_pending | Latin incipit not yet sourced |
| incipit_sourced | Latin found, verified |
| translation_pending | No translation found |
| translation_sourced | Translation found, sourced |
| citations_partial | 1–2 citations found |
| commentary_ready | All 3–4 citations + heretical flag set |
| cluster_templated | Template for cluster; individuals pending |

---

## Commit Messages (Every 10 Conclusions)

Example:
```
git commit -m "S1 conclusions T[N]–T[N+10]: Latin + translations + scholar citations

- T[N]: [THEME] — Latin sourced, [SOURCE], [COUNT] citations
- Status: [X]/95 commentary-ready
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Checkpoints

After each 10 conclusions:
1. Update completion_status fields in stage_S1.json
2. Commit with message above
3. Log in DECISIONS.md

After all 95:
1. Verify all status fields are commentary_ready
2. Final commit: "✅ S1 HARVESTER H2 COMPLETE"
3. Update PHASE_1_RESEARCH_QUEUE.json
4. Handoff to PORTER for standardization

---

## Support Files

- docs/NEOPLATONISM_SOURCING_PROTOCOL.md — Full sourcing protocol
- docs/NEOPLATONISM_WORKFLOW.md — Workflow phases
- data/neoplatonism/philosophers_index.json — Philosopher metadata
- S1_RESEARCH_NOTES.md — Heretical conclusions context
- CRITICAL_EDITION_TAXONOMY.md — Section structure

---

**Estimated time**: ~90 minutes for all 95 conclusions  
**Token budget**: 40,000 tokens  

**Go. Extract S1 now.**
