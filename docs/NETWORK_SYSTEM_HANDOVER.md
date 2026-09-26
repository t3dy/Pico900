# Handover: Intellectual Network System Implementation

**Status**: Specification and Phase 0 planning complete. Ready for implementation.

**Date**: 2026-09-26

**Authority**: User spec + INTELLECTUAL_NETWORK_DESIGN.md + core scholar readings (Copenhaver, Howlett, Edelheit)

---

## What this System Does

The intellectual network system models Pico's relationships with 32+ key figures as first-class scholarly metadata. Every thesis can now be understood in the context of:

- **Who influenced its thinking** (with evidence level)
- **What philosophical disputes it engages**
- **How it fits Pico's broader intellectual project**

Rather than:
- A single "influence" boolean (too crude)
- Or vague network diagrams (no evidence)

---

## Immediate Next Steps (Phase 0: Bootstrap)

### 1. Create person directory and index files

**Files to create**:
- `data/network/persons.json` — Structured person records (40+ figures)
- `data/network/persons_manifest.json` — Metadata: who populated it, when, status
- `data/network/relationship_types.json` — Controlled vocabulary (17 relationship types)
- `data/network/evidence_levels.json` — Confidence grading rubric (5-0 scale)

**Implementation**:
- Start with Tier 1 (12 central figures) + Tier 4 (12 trial commission members)
- Extract alternate names from Markdown corpus (gazetteer in build_dossiers.py)
- Add birth/death dates from Copenhaver/Howlett appendices
- Record authority pointers (VIAF, LCNAF, Treccani, Stanford SEP, etc.)
- Mark confidence level for each person record (how well documented is the person?)

**Responsibility**: One agent (ORCHESTRATOR or BOOTSTRAP agent) writes these files atomically. One writer per file always (CLAUDE.md).

**Gate**: Every person has ≥1 locator (book reference, line number, or URL). No null fields in canonical records. Manifest shows who sourced what.

### 2. Script: network_bootstrap.py

**Task**: Automate person-record generation from existing sources.

**Inputs**:
- `build_dossiers.py` gazetteer (current person name + regex)
- `data/claims/parties.json` (seeded party list)
- Copenhaver 2022 bibliography and appendices
- Howlett bibliography

**Outputs**:
- `data/network/persons.json` (structured records)
- `data/network/bootstrap_report.json` (what was found, what's missing, what's ambiguous)

**Logic**:
1. For each gazetteer entry, create a PERSON record
2. Extract alternate names (Latin, Italian, Hebrew, etc.) from contexts where they appear
3. Look up dates in Copenhaver/Howlett indices
4. Assign authority identifiers where available
5. Mark fields as draft/verified based on source authority

**Run**: Next session, Phase 0
```bash
python scripts/network_bootstrap.py --source gazetteer --output persons.json --verbose
python scripts/network_bootstrap.py --source parties.json --merge
```

### 3. Hand-verification pass

**Task**: Review bootstrap output; hand-add missing figures and refine records.

**Scope**:
- Tier 1 figures (12 central): flesh out with full Copenhaver/Howlett/Edelheit data
- Tier 4 trial commission figures (12): verify names and dates; resolve OCR issues in commission records
- Check for duplicates (same person, different name forms)
- Add occupations, institutions, languages

**Responsibility**: ORCHESTRATOR or dedicated VERIFIER agent. Work directly in persons.json (one writer).

**Output**: Fully populated Tier 1 + Tier 4 persons (24 records) + bootstrap report.

---

## Phase 0 Outputs (Deliverables)

### 1. `data/network/persons.json`
```json
{
  "persons": [
    {
      "id": "pico_giovanni_1",
      "canonical_name": "Giovanni Pico della Mirandola",
      "sort_name": "Pico, Giovanni della Mirandola",
      "alternate_names": [
        {"form": "Giovanni Pico", "language": "Italian", "period": "1460s"},
        {"form": "Ioannes Picus", "language": "Latin", "period": "1480s"},
        {"form": "Jean Pic", "language": "French", "period": "1480s"}
      ],
      "birth_year": 1463,
      "death_year": 1494,
      "locations": [
        {"place": "Mirandola", "role": "birthplace/lordship", "dates": "1463-1494"}
      ],
      "occupations": ["philosopher", "theologian", "nobleman"],
      "languages": ["Italian", "Latin", "Greek", "Hebrew"],
      "intellectual_traditions": ["Platonism", "Aristotelianism", "Scholasticism", "Kabbalah", "Hermeticism"],
      "major_works": [
        {"title": "900 Conclusions", "date": 1486, "type": "thesis_collection"},
        {"title": "Oration on the Dignity of Man", "date": 1486, "type": "oration"}
      ],
      "authoritative_sources": ["Copenhaver 2022", "Howlett 2021", "Edelheit 2022"],
      "evidence_status": "primary_source",
      "notes": "Subject of this research database. Died age 31."
    },
    {
      "id": "ficino_marsilio_1",
      "canonical_name": "Marsilio Ficino",
      "sort_name": "Ficino, Marsilio",
      "birth_year": 1433,
      "death_year": 1499,
      "locations": [
        {"place": "Florence", "role": "residence", "dates": "1433-1499"}
      ],
      "occupations": ["philosopher", "theologian", "translator", "priest"],
      "languages": ["Latin", "Greek", "Italian"],
      "intellectual_traditions": ["Platonism", "Neoplatonism", "Scholasticism"],
      "major_works": [
        {"title": "Theologia Platonica", "date": 1482, "type": "philosophical_treatise"},
        {"title": "Commentary on the Symposium", "date": 1469, "type": "commentary"}
      ],
      "authoritative_sources": ["Copenhaver 2022", "Howlett 2021", "Kristeller (Ficino Opera)"],
      "evidence_status": "primary_source",
      "notes": "Elder mentor, intellectual competitor, correspondent. Central to Pico's philosophical development."
    }
  ],
  "metadata": {
    "created": "2026-09-26T00:00:00Z",
    "created_by": "bootstrap + hand-verification",
    "total_count": 24,
    "status": "draft",
    "next_action": "Phase 1-Alpha relationship extraction"
  }
}
```

### 2. `data/network/persons_manifest.json`
```json
{
  "manifest": [
    {"person_id": "pico_giovanni_1", "sourced_from": "primary", "verified": true, "added": "2026-09-26"},
    {"person_id": "ficino_marsilio_1", "sourced_from": "bootstrap + Copenhaver", "verified": true, "added": "2026-09-26"},
    ...
  ],
  "summary": {
    "total_persons": 24,
    "verified": 24,
    "draft": 0,
    "missing_birth_date": 2,
    "missing_death_date": 1,
    "alternate_names_added": 18,
    "authority_identifiers": 16
  }
}
```

### 3. `data/network/relationship_types.json` (controlled vocab)
```json
{
  "relationship_types": [
    {
      "id": "correspondence",
      "label": "Correspondence",
      "description": "Surviving letters, documented exchange",
      "directionality": "bidirectional",
      "is_documentary": true
    },
    {
      "id": "friendship",
      "label": "Friendship",
      "description": "Described or implied by contemporaries; testimony of warmth/respect",
      "directionality": "bidirectional",
      "is_documentary": false
    },
    ...
  ]
}
```

### 4. Updated `data/claims/parties.json`
- Each party now has a `person_id` foreign key
- Points to the canonical person record in persons.json

### 5. Phase 0 Completion Report
- Count of persons bootstrapped: 24 (Tier 1 + Tier 4)
- Count of alternate names added: ~30
- Authority identifiers resolved: ~16
- Outstanding questions: Listed by person (e.g., "Jean Monissart exact dates unclear")
- Next actions: What Tier 2 figures to add before Phase 1-Alpha

---

## Phase 1-Alpha: Relationship Extraction (2-3 weeks, parallel agents)

### Overview
Extract all relationships between Pico and the 32-person core network from scholarly sources. Each relationship must be grounded in evidence with verified locator.

### Agent swarm (parallel by figure/work):

**RELATIONSHIP-HARVESTER agents** (5 parallel):
1. **Ficino harvester** — Copenhaver 2019+2022, Allen 2017, Farmer notes
   - Extract: correspondence, philosophical_disagreement, intellectual_interlocutor, friendship
   - Output: 4-5 relationships with 10+ evidence entries

2. **Paduan circle harvester** — Howlett ch. 2-3 (Del Medigo, Vernia, Nifo, Donato, Ramusio, Guarini)
   - Extract: teacher, intellectual_interlocutor, source, contemporary
   - Output: 5-6 relationships with evidence

3. **Kabbalah/Hebrew harvester** — Wirszubski, Idel, Busi, Fanger *Invoking Angels*
   - Extract: teacher, translator, collaborator, source for Mithridates, Alemanno
   - Output: 3 relationships with evidence

4. **Trial commission harvester** — Copenhaver 2022 ch. 6-7, Edelheit, audit A2
   - Extract: trial_participant, polemical_opponent, institutional_relationship
   - Output: 12 relationships (Garcia, Cordier, Monissart, etc.) with evidence
   - Note: Some are pro-Pico (Cordier, Giovanni de Myrle) — capture that

5. **Florentine/reception harvester** — Benivieni, Poliziano, Savonarola, Gianfrancesco
   - Extract: friendship, correspondence, intellectual_interlocutor, collaborator, later_respondent, posthumous_editor
   - Output: 6 relationships with evidence

**RELATIONSHIP-LINKER agent** (serial, after harvesters):
- Consolidate relationships; mark duplicates; assign relationship_ids; cross-reference evidence
- Output: `data/network/relationships.json`, `data/network/relationship_evidence.json`

### Outputs:

**`data/network/relationships.json`**
```json
{
  "relationships": [
    {
      "id": "rel_pico_ficino_correspondence_1",
      "person_a_id": "pico_giovanni_1",
      "person_b_id": "ficino_marsilio_1",
      "relationship_type": "correspondence",
      "confidence_level": 5,
      "evidence": ["ev_ficino_letter_1485", "ev_pico_response_sketch"],
      "description": "Documented exchange of letters, 1485-1494"
    },
    {
      "id": "rel_pico_ficino_disagreement_one_intellect",
      "person_a_id": "pico_giovanni_1",
      "person_b_id": "ficino_marsilio_1",
      "relationship_type": "philosophical_disagreement",
      "relationship_subtype": "neoplatonic_metaphysics",
      "confidence_level": 5,
      "evidence": ["ev_de_ente_pico_latin", "ev_theologia_ficino_latin", "ev_copenhaver_ch5"],
      "description": "Pico's De ente et uno critiques Ficino's procession of Intellect from One"
    }
  ],
  "metadata": {
    "total_relationships": 32,
    "by_type": {
      "correspondence": 5,
      "philosophical_disagreement": 4,
      "teacher": 4,
      "trial_participant": 12,
      "source": 3
    }
  }
}
```

**`data/network/relationship_evidence.json`**
```json
{
  "evidence": [
    {
      "id": "ev_ficino_letter_1485",
      "relationship_id": "rel_pico_ficino_correspondence_1",
      "evidence_type": "primary_source",
      "source": {
        "work_id": "ficino_opera",
        "line_start": 12345,
        "line_end": 12367
      },
      "claim_text": "[Letter text or quotation]",
      "interpretation": "Shows Ficino in role of elder mentor discussing philosophy with Pico",
      "evidence_level": 5,
      "verified": true,
      "verified_by": "claims_verify.py",
      "notes": "Kristeller edition; confirmed verbatim in Ficino Opera"
    }
  ]
}
```

**Gate**: 
- No relationship without ≥1 evidence entry
- Every evidence entry passes `claims_verify.py` (locator checked, quote verbatim if quoted)
- Confidence levels justified in notes
- Evidence level distribution: ≥20% level 5, ≥40% level 4, rest ≥3

### Timeline:
- **Week 1**: Harvester swarm (parallel)
- **Week 2**: LINKER consolidation + verification loop
- **Week 3**: Polish and gate review

---

## Phase 1-Beta: Text-Person Scoring (1-2 weeks, parallel by thesis)

### Overview
For each thesis (or text section), identify which people are relevant and assign relationship type (from TEXT_PERSON_RELATIONSHIP vocab).

### Inputs:
- `research-packets/hist_0N_NNN.md` (thesis packet from build_dossiers.py)
- `data/network/relationships.json` (Phase 1-Alpha output)
- `data/ontology/mentions/by_thesis/` (scholar mentions, existing)

### Task:
1. RESEARCHER reads the thesis packet
2. Identifies people mentioned in Farmer Latin or commentary
3. Cross-references scholar mentions (existing data)
4. Creates TEXT_PERSON_RELATIONSHIP entries with relationship_type, evidence locator
5. Marks "speculative" relationships and justifies them

### Output:
**`data/network/text_person_relationships.json`**
```json
{
  "text_person_relationships": [
    {
      "text_id": "hist_01_001",
      "person_id": "ficino_marsilio_1",
      "relationship_type": "philosophical_disagreement",
      "relationship_direction": "forward",
      "relevance_level": "high",
      "confidence_level": 3,
      "evidence": [
        {
          "source_type": "farmer_note",
          "source_locator": "F:12345",
          "claim": "Farmer commentary notes Ficino disagrees on this point"
        },
        {
          "source_type": "scholar_mention",
          "source_locator": "copenhaver2022:ch5:p150",
          "claim": "Copenhaver traces this thesis to Pico's response to Ficino"
        }
      ],
      "notes": "Not explicitly named in thesis text, but Farmer notes and Copenhaver establish connection"
    }
  ],
  "metadata": {
    "total_entries": 900,
    "percent_with_people": 75,
    "avg_people_per_thesis": 2.3
  }
}
```

**Gate**:
- 100% of 900 theses have entries (even if "no relevant people")
- No entry without evidence (Farmer line or scholar mention or claim_id)
- Speculative relationships ≤10% per thesis
- Distribution tracked in manifest

---

## Phase 2: Relationship Scoring & Reasoning (3-4 weeks)

### Overview
For each thesis, score each associated person on 7 dimensions (1-10 scale). Write prose reasoning.

### Outputs:

**`data/network/relationship_scores.json`**
```json
{
  "scores": [
    {
      "text_id": "hist_04_002",
      "person_id": "quidort_jean_1",
      "score_textual_centrality": 8,
      "score_source_relation": 9,
      "score_network_relevance": 6,
      "score_controversy": 5,
      "score_historical_significance": 4,
      "score_evidence_quality": 8,
      "score_tradition_significance": 7,
      "score_reception": 4,
      "score_total": 51,
      "reasoning": "This thesis quotes Quidort's impanation model almost directly. Farmer and Copenhaver both trace the genealogy. Quidort (13th-c.) is not a contemporary, but his work is the textual source. Network relevance is moderate because Quidort is a medieval source, not part of Pico's living circle. Evidence is strong."
    }
  ]
}
```

**`data/network/relationship_reasoning.json`**
```json
{
  "reasoning": [
    {
      "text_id": "hist_04_002",
      "person_id": "ficino_marsilio_1",
      "reasoning": "Unlike Ficino (who argues for Transubstantiation), Pico uses the impanation model. This thesis is one of the points of philosophical disagreement between them. Copenhaver notes that Q6 was condemned partly because of its heterodox eucharistic doctrine. Ficino's disagreement is not explicit in this thesis but is central to understanding what Pico is opposing.",
      "length": 112,
      "includes_citations": true
    }
  ]
}
```

### Process:
- WRITER reads thesis + person + relationships + evidence
- Scores each dimension (1-10) with explicit rubric
- Writes reasoning (100-200 words minimum)
- VERIFIER spot-checks against source material

---

## Integration with Existing Workflows

### How it flows into thesis entries:

1. **Build script** (`build_dossiers.py`):
   - Already builds research packets with Farmer Latin + mentions
   - Now adds: `TEXT_PERSON_RELATIONSHIP` entries + `RELATIONSHIP_SCORING` suggestions

2. **WRITER template**:
   - Entry template auto-populated with:
     - People connected to this thesis (with relevance level)
     - Suggested focus areas (high-scoring people)
     - Evidence locators (Farmer line, scholar mention, etc.)
   - WRITER cites people with precision: "Ficino disagreed on this point (De ente et uno); Pico adapts Quidort's framework (Farmer:12345)"

3. **Site rendering**:
   - Thesis cards show related people with relevance badges
   - Detail page shows scoring dimensions
   - Research view allows filtering by person, relationship type, evidence level

### Files that change:
- `scripts/build_dossiers.py` — add TEXT_PERSON_RELATIONSHIP to packet output
- `research-packets/` — packets now include people suggestions
- Entry templates — populated with network metadata
- Site HTML — new "Intellectual Network" section on thesis pages

---

## Known Challenges & Mitigations

### 1. Same person, multiple name forms
**Problem**: "Henry of Ghent" = "Henricus Gandavensis" = "Henri de Gand"
**Mitigation**: persons.json has alternate_names with language/period tags; gazetteer uses person_id, not string matching

### 2. Retroactive inference of influence
**Problem**: Both Pico and Ficino write on the Intellect; scholars infer influence without documentary evidence
**Mitigation**: `is_documentary` flag; separate level-5 "documented" from level-3 "inferred"; WRITER told to distinguish

### 3. Medieval sources (Aquinas, Henry of Ghent, Quidort)
**Problem**: These are textual sources, not personal relationships
**Mitigation**: Keep them in the network but mark relationship_type as "source" with is_documentary=false (textual, not personal); note that they are medieval, not Pico's contemporaries

### 4. Gianfrancesco's editorial distortion
**Problem**: Gianfrancesco reshaped Pico's legacy; his account is reception history, not biography
**Mitigation**: Mark Gianfrancesco relationships separately as `posthumous_editor` / `reception_figure`; use Copenhaver and Howlett to correct the record

### 5. Overcounting evidence
**Problem**: Same fact appears in multiple scholars; risk of double-scoring
**Mitigation**: Evidence deduplicated by source locator; if multiple scholars cite same passage, one evidence record with scholars_citing[] list

---

## Non-Negotiable Rules

1. **No relationship without evidence** — Must be able to point to a passage in a source
2. **Every confidence level justified** — "Level 5 = primary source" requires the actual document and locator
3. **Direction matters** — Pico → Ficino (studying) ≠ Ficino → Pico (patronizing)
4. **Inference vs. documentation separate** — Record both but distinguish clearly
5. **No double-counting** — Same evidence doesn't inflate score if used in multiple relationships
6. **Verifier ≠ Writer** — Person who writes relationship scoring does not verify it
7. **Quote gate** — Every quotation must pass claims_verify.py before storage

---

## Timeline & Milestones

| When | What | Gate |
|------|------|------|
| Next session (1-2 days) | Phase 0: Bootstrap persons.json + verify Tier 1+4 | 24 persons, each with ≥1 locator |
| Following 2-3 weeks | Phase 1-Alpha: Extract relationships | 30+ relationships, all evidenced, levels 3+ |
| Following 1-2 weeks | Phase 1-Beta: Text-person scoring prep | 900 theses have TEXT_PERSON entries |
| Following 3-4 weeks | Phase 2: Score relationships & write reasoning | 100+ top theses scored with reasoning |
| Following 2-3 weeks | Integration: Update site, templates, workflows | Live network metadata in thesis entries |

**Total elapsed**: ~10-12 weeks from specification to full deployment. Phases 1-Alpha and 1-Beta can run partially in parallel.

---

## Key Files to Create/Modify

### New files:
- `data/network/persons.json` — Person directory
- `data/network/persons_manifest.json` — Metadata
- `data/network/relationships.json` — All directed edges
- `data/network/relationship_evidence.json` — Evidence entries
- `data/network/text_person_relationships.json` — Thesis-person entries
- `data/network/relationship_scores.json` — Scored dimensions
- `data/network/relationship_reasoning.json` — Prose explanations
- `docs/INTELLECTUAL_NETWORK_SYSTEM.md` — Operational guide (to be written)
- `scripts/network_bootstrap.py` — Automate person record creation
- `scripts/network_harvest.py` — Extract relationships from sources (Phase 1-Alpha)
- `scripts/network_verify.py` — Spot-check relationships (verification layer)
- `scripts/network_score.py` — Compute relationship_scores (Phase 2)

### Modified files:
- `data/claims/parties.json` — add person_id foreign key
- `scripts/build_dossiers.py` — output TEXT_PERSON_RELATIONSHIP in packets
- `docs/ORCHESTRATION.md` — document Phase 0, 1-Alpha, 1-Beta, Phase 2
- `DECISIONS.md` — record design decisions
- `HANDOVER.md` — updated with network rollout

---

## Success Criteria & Definition of Done

### Phase 0:
- [ ] 24 persons (Tier 1 + Tier 4) in persons.json, each with canonical_name, birth/death, occupations, traditions
- [ ] Every person has ≥1 locator (book/page, Stanford SEP entry, Treccani, etc.)
- [ ] persons_manifest.json shows sourcing and verification status
- [ ] No null canonical fields (allow null alternate_names, dates if not known)

### Phase 1-Alpha:
- [ ] 30+ relationships extracted, each with ≥1 evidence entry
- [ ] All evidence entries verified via claims_verify.py (locator found, quote verbatim if quoted)
- [ ] Confidence levels: ≥20% level 5, ≥40% level 4, rest ≥3
- [ ] relationships.json and relationship_evidence.json complete and consistent

### Phase 1-Beta:
- [ ] 900 theses have TEXT_PERSON_RELATIONSHIP entries (even if empty)
- [ ] No entry without evidence (Farmer line or scholar mention)
- [ ] Speculative entries ≤10% per thesis average
- [ ] Distribution report: % of theses with 0, 1-3, 4+ people

### Phase 2:
- [ ] 100+ top theses have scored relationships
- [ ] Each score has prose reasoning ≥100 words
- [ ] Spot-check: high scores correlate with high evidence levels
- [ ] WRITER entries cite people with relationship type + passage

### Ongoing:
- [ ] New theses onboarded with network metadata
- [ ] Contradictions in scholarship documented (historiographical disputes)
- [ ] Network graph updated as new sources discovered

---

## Appendix: Authority Sources Used in Phase 0

### Primary sources on Pico's network:
- Copenhaver, *Pico della Mirandola on Trial* (2022) — comprehensive; appendix of figures
- Copenhaver, *Magic and the Dignity of Man* (2019) — correspondence, reception
- Howlett, *Re-evaluating Pico* (2021) — network reconstruction; education itinerary
- Edelheit, *Ficino, Pico and Savonarola* (2022) — trial, theology, relationships
- Fanger, *Invoking Angels* (2012) — Alemanno, magic, theurgy
- Farmer, *Syncretism in the West* (1998) — Farmer's own notes on sources and context

### Reference materials:
- Stanford Encyclopedia of Philosophy — Pico (2012), Gianfrancesco (2017)
- Treccani — Pico della Mirandola entry
- Kristeller — Ficino Opera (full text edition)
- PicoDB — existing persons/scholars table (not authority but useful list)

---

**Document Status**: Handover, ready for Phase 0 implementation.
**Next**: Deploy `network_bootstrap.py` script and begin person directory population.
