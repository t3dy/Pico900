# Intellectual Network System: Summary

**Date**: 2026-09-26

**Status**: Specification complete. Ready for Phase 0 implementation.

**Deliverables**: Two guidance documents + design specification

---

## What Was Built

### 1. `docs/INTELLECTUAL_NETWORK_DESIGN.md` (4500+ words)

Complete specification for modeling Pico's intellectual relationships as first-class scholarly metadata.

**Includes**:
- Rationale (the gap in the existing system)
- Complete schema (PERSON, RELATIONSHIP, RELATIONSHIP_EVIDENCE, TEXT_PERSON_RELATIONSHIP, RELATIONSHIP_SCORING)
- Implementation strategy (Phase 0, 1-Alpha, 1-Beta, Phase 2)
- 32-person core network with relationship types and tier structure
- Relationship type vocabulary (17 types)
- Evidence level grading rubric (5-0 scale)
- Example relationship records (Ficino, del Medigo, Aquinas, trial commission, Savonarola, Alemanno)
- Known challenges and mitigations
- Success metrics

### 2. `docs/NETWORK_SYSTEM_HANDOVER.md` (3000+ words)

Operational guide for implementing the system.

**Includes**:
- Phase 0 bootstrap instructions (persons.json, manifests, controlled vocabularies)
- Phase 1-Alpha relationship extraction (5-person harvester swarm)
- Phase 1-Beta text-person scoring (900 theses)
- Phase 2 dimension scoring and reasoning
- Integration with existing workflows
- Timeline and milestones (10-12 weeks total)
- Known challenges and mitigations
- Success criteria and definition of done

### 3. Network Design Specification Details

**Core insight**: Pico's intellectual world is a dense network connecting:
- Florentine humanism (Ficino, Poliziano, Benivieni)
- Paduan Aristotelianism/Averroism (del Medigo, Vernia, Nifo)
- Parisian scholasticism (Jean Cordier and others)
- Jewish philosophy and Kabbalah (Mithridates, Alemanno)
- Papal theology and trial (Pedro Garcia, trial commission)
- Later reception (Gianfrancesco, Savonarola, later interpreters)

**The key distinction**: Pico uses people from **mutually incompatible intellectual communities** to construct his concordist project. The network captures this complexity.

---

## Why This Matters

### Before:
- A thesis might have a mention of "Ficino" in scholar notes, but no structured representation
- Scoring was opaque: "Ficino influence +5 points" (undefined)
- Direction was lost: Is Pico learning from Ficino, disagreeing with him, or both?
- Medieval sources (Aquinas, Henry of Ghent) mixed with living contemporaries as if equivalent
- Reception figures (Gianfrancesco, later commentators) treated as if they influenced Pico's original thought

### After:
- Every thesis has explicit relationships to Pico's network figures
- Scoring is transparent: 8 separate dimensions, each 1-10, each with prose reasoning
- Direction is explicit: correspondence ≠ philosophical_disagreement ≠ source
- Medieval sources are labeled as such (textual, not personal relationships)
- Reception figures are separate (posthumous_editor, later_respondent)
- Evidence is always documented with source locator (work:line)
- Confidence levels are graded (5=primary, 4=strong doc, 3=strong inference, 2=plausible, 1=speculative)

---

## The 32-Person Core Network

### Tier 1 (Central relationships, documented):
1. Marsilio Ficino — mentor, friend, intellectual competitor, correspondent
2. Angelo Poliziano — friend, literary critic, intellectual interlocutor
3. Ermolao Barbaro — correspondent, linguistic/philosophical disputant
4. Elia del Medigo — teacher in Padua, Averroism, Hebrew, Kabbalah intermediary
5. Flavius Mithridates — Hebrew/Aramaic teacher, translator, collaborator
6. Yohanan Alemanno — Hebrew scholar, Kabbalist, collaborator
7. Girolamo Benivieni — friend, literary collaborator, test case for Ficino critique
8. Nicoletto Vernia — Paduan Aristotelian teacher
9. Agostino Nifo — Paduan Aristotelian, peer
10. Lorenzo de' Medici — patron, protector, intellectual network hub
11. Girolamo Savonarola — late-life intellectual/religious interlocutor
12. Gianfrancesco Pico — nephew, posthumous editor, reception figure

### Tier 2 (Important educational/network figures):
13-17. Paduan circle: Donato, Ramusio, Guarini, etc.

### Tier 4 (Trial commission, institutional opposition):
18-27. Pedro Garcia (main opponent), Jean Cordier (defender), Jean Monissart, Marco de Miroldo, Giovanni de Myrle, Bonfrancesco Arlotti, Cardinal Giorgio da Costa, and others

### Tier 5 (Medieval/ancient textual sources):
28-32. Thomas Aquinas, Henry of Ghent, Plotinus, Proclus, etc. (textual sources, not personal relationships)

---

## Key Technical Decisions

### 1. Relationship type vocabulary
17 distinct types (correspondence, friendship, patronage, teacher, student, collaborator, translator, source, intermediary, intellectual_interlocutor, philosophical_disagreement, polemical_opponent, theological_opponent, trial_participant, institutional_relationship, acquaintance, posthumous_editor). Not a single "influence" boolean.

### 2. Directionality
Explicit: Ficino → Pico (teaching) is different from Pico → Ficino (studying with). Both may be true; both recorded separately.

### 3. Evidence grading
5-level scale:
- Level 5: Primary source documentary (Ficino's letter)
- Level 4: Strong contemporary/near-contemporary documentation
- Level 3: Strong scholarly inference from primary sources
- Level 2: Plausible scholarly inference
- Level 1: Speculative / traditional
- Level 0: Unsupported (not stored)

### 4. Text-specific relevance
Same relationship (Ficino-Pico) has different relevance to different theses:
- High relevance: De ente et uno, Commento on Benivieni, some Neoplatonic theses
- Moderate: some astrological material
- Low: angelology theses

### 5. Multi-dimensional scoring (not opaque)
Instead of a single score, 7 dimensions:
- textual_centrality (how central is the person to the thesis's argument?)
- source_relation (does the thesis quote/adapt the person's work?)
- network_relevance (how strong is the Pico-person relationship?)
- controversy (was the person involved in philosophical/theological disagreement on this topic?)
- historical_significance (trial, reception, major debate?)
- evidence_quality (how well documented is the relationship?)
- tradition_significance (does this connect to a major philosophical school?)

Each dimension scored 1-10 with reasoning.

---

## Implementation Roadmap

### Phase 0 (1-2 days, next session):
- Create `data/network/persons.json` with 24 persons (Tier 1+4)
- Bootstrap from gazetteer + Copenhaver/Howlett
- Write `persons_manifest.json` with sourcing metadata
- Create controlled vocabularies (relationship types, evidence levels)

### Phase 1-Alpha (2-3 weeks):
- Deploy 5-agent harvester swarm (Ficino, Padua, Kabbalah, trial, reception)
- Extract 30+ relationships from sources with evidence
- Verify all evidence via claims_verify.py
- Output: `relationships.json`, `relationship_evidence.json`

### Phase 1-Beta (1-2 weeks):
- Create TEXT_PERSON_RELATIONSHIP entries for all 900 theses
- Link each entry to evidence (Farmer line or scholar mention)
- Output: `text_person_relationships.json`

### Phase 2 (3-4 weeks):
- Score each thesis-person pair on 7 dimensions
- Write prose reasoning (100-200 words minimum)
- Output: `relationship_scores.json`, `relationship_reasoning.json`

### Integration (2-3 weeks):
- Update build_dossiers.py to include network metadata in packets
- Update thesis entry template to auto-populate with people suggestions
- Update site HTML to display network metadata
- Deploy live

**Total**: ~10-12 weeks from specification to live system.

---

## Authority & Sources

### Design grounded in:
1. **User specification** (2026-09-26) — Core requirements for intellectual network modeling
2. **Copenhaver 2022** — *Pico della Mirandola on Trial* (most comprehensive source on relationships + trial)
3. **Copenhaver 2019** — *Magic and the Dignity of Man* (correspondence, reception, Savonarola)
4. **Howlett 2021** — *Re-evaluating Pico* (network reconstruction, education itinerary, Kabbalah)
5. **Edelheit 2022** — *Ficino, Pico and Savonarola* (trial, theology, relationship evolution)
6. **Fanger 2012** — *Invoking Angels* (Jewish networks, Alemanno, theurgy)
7. **Farmer 1998** — *Syncretism in the West* (Farmer's own notes, context, sources)

### Grounded in existing Pico900 structure:
- Data ontology (mentions, historiographical importance, gazetteer)
- Claims model (evidence levels, verification, sourcing)
- Thesis inventory (Farmer IDs, structure)
- Research protocols (harvesting, extraction, linking)

---

## Not Included (Out of Scope)

This document specifies the **data system**, not:
- UI/UX design (how network is displayed on site)
- Algorithmic ranking (how to rank theses by network relevance for browsing)
- NLP extraction (automated relationship mining)
- Graph visualization (rendering the network visually)

These are follow-on work, specified elsewhere.

---

## File Structure (as of 2026-09-26)

```
Pico900/
├── docs/
│   ├── INTELLECTUAL_NETWORK_DESIGN.md        ← Specification (this session)
│   ├── NETWORK_SYSTEM_HANDOVER.md            ← Implementation plan (this session)
│   ├── DATA_ONTOLOGY.md                       (existing; unchanged)
│   ├── RESEARCH_PROTOCOL.md                   (existing; unchanged)
│   └── ...
├── data/
│   ├── network/                               ← NEW FOLDER
│   │   ├── persons.json                       (Phase 0)
│   │   ├── persons_manifest.json              (Phase 0)
│   │   ├── relationships.json                 (Phase 1-Alpha)
│   │   ├── relationship_evidence.json         (Phase 1-Alpha)
│   │   ├── text_person_relationships.json     (Phase 1-Beta)
│   │   ├── relationship_scores.json           (Phase 2)
│   │   ├── relationship_reasoning.json        (Phase 2)
│   │   ├── relationship_types.json            (Phase 0, vocab)
│   │   └── evidence_levels.json               (Phase 0, vocab)
│   ├── claims/
│   │   ├── parties.json                       (modified to add person_id foreign key)
│   │   └── ...
│   └── ...
├── scripts/
│   ├── network_bootstrap.py                   (Phase 0, new)
│   ├── network_harvest.py                     (Phase 1-Alpha, new)
│   ├── network_verify.py                      (Phase 1-Alpha, new)
│   ├── network_score.py                       (Phase 2, new)
│   ├── build_dossiers.py                      (modified to include network metadata)
│   └── ...
└── ...
```

---

## Success Criteria

### Phase 0 Gate:
- 24 persons (Tier 1+4) in persons.json
- Each with ≥1 locator (book/page, authority record, Stanford SEP, etc.)
- No null canonical fields
- Manifest shows sourcing + verification status

### Phase 1-Alpha Gate:
- 30+ relationships with evidence
- All evidence entries verified (locator found, quote verbatim)
- Confidence levels: ≥20% level 5, ≥40% level 4, rest ≥3
- relationships.json + relationship_evidence.json consistent

### Phase 1-Beta Gate:
- 900 theses have TEXT_PERSON_RELATIONSHIP entries
- No entry without evidence
- Speculative entries ≤10% per thesis
- Distribution report complete

### Phase 2 Gate:
- 100+ theses scored
- Each score has reasoning ≥100 words
- Spot-checks pass
- High scores correlate with high evidence levels

### Ongoing:
- New theses onboarded with network metadata
- Contradictions documented
- Network updated as new sources discovered

---

## Next Action

Deploy `network_bootstrap.py` script to auto-generate persons.json from:
1. Gazetteer in build_dossiers.py
2. Copenhaver 2022 bibliography + appendices
3. Howlett 2021 bibliography
4. PicoDB existing persons table

Then hand-verify Tier 1+4 figures and flesh out with:
- Alternate names (Latin, Italian, Hebrew, etc.)
- Birth/death dates
- Occupations and institutions
- Languages and intellectual traditions
- Authority identifiers

**Estimated time**: 1-2 days.

---

**Document Status**: Summary of specification and implementation plan. Reference for all phases. Commit this alongside the two detailed documents.
