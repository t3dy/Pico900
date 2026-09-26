# Intellectual Network System: Design & Integration

**Scope**: Extend Pico900's existing data ontology to model Pico's intellectual network as first-class scholarly metadata, materially informing the interpretation and scoring of individual theses and texts.

**Status**: Specification (design phase before implementation). This document establishes the architecture that will guide orchestration in Phase 1-Alpha and beyond.

**Authority**: Derived from user requirement in pasted spec 2026-09-26; grounded in existing `DATA_ONTOLOGY.md`, `RESEARCH_PROTOCOL.md`, `claims_verify.py`, `build_dossiers.py`, and corpus/claims model.

---

## Part 1: Existing Strengths (Do Not Break)

### What works and must not change:

1. **Corpus registry and location system** (`data/corpus/registry.json`, `corpuslib.py`)
   - 82 works, 73 Markdown conversions + 9 plain-text, 3.9M words
   - Locator: `work:line` (1-based, ±2 tolerance for OCR)
   - Quotation gate: `claims_verify.py` re-finds every quotation; no claim without verification
   - Status: Production-ready

2. **Thesis structure** (`data/inventory/farmer_structure.json`, `condemned_thirteen.json`)
   - All 900 theses from Farmer 1998, mapped to Apology Q1-Q13 (the 13 condemned)
   - Farmer line numbers as canonical locator for thesis Latin and commentary
   - Status: Ground truth

3. **Claims model** (`scripts/claims_verify.py`, `data/claims/`, `docs/CLAIMS_MODEL.md`)
   - Atomic facts with provenance: `source`, `claim_type`, `confidence` (5=primary, 4=strong doc, 3=strong inference, 2=plausible, 1=speculative, 0=unsupported)
   - Verification loop: RESEARCHER → claims packet → verify script → tickets → fix → verify again
   - Claims are never scored/linked/cited until verified
   - Status: In use, working

4. **Data ontology and mention extraction** (`docs/DATA_ONTOLOGY.md`, `docs/RESEARCH_PROTOCOL.md`)
   - Historiographical importance grades per thesis (primary / secondary / tertiary / unexamined)
   - Scholar mentions indexed by thesis and work
   - Gazetteer for persons/concepts (in `build_dossiers.py`)
   - Status: Populated for some theses (angelology), framework in place

5. **Research packets and tier system** (`research-packets/`, `build_dossiers.py`)
   - Per-thesis dossiers with Latin, apparatus, scholar mentions, cross-refs, connections
   - Tier suggestion (A: condemned + >=3 works; B: >=1; C: Farmer only; D: Latin only)
   - Status: Framework operational; packets exist

---

## Part 2: The Gap — What Network System Must Provide

### What does not yet exist:

1. **Person entities** with rich metadata (canonical names, dates, alternate names, institutions, traditions)
   - Currently: bare strings in gazetteer regexes (e.g., "Henry of Ghent" → regex)
   - Needed: a `PERSON` table with normalized identity, authority links, relationships to works
   - Why: Same person has multiple name forms (Henry of Ghent / Henricus Gandavensis / Henri de Gand); aliases drift across sources; an agent needs to know who "Albertus" means in a 1486 context

2. **Relationship model** with typed, directed, evidence-grounded edges
   - Currently: connections are person→thesis, not person→person with richness
   - Needed: Pico↔Ficino can have multiple relationships (correspondence, philosophical_disagreement, patron relationship, intellectual exchange) recorded separately, each with evidence level
   - Why: A single "influence" boolean crushes nuance. Pico and Ficino disagreed vehemently on some questions and agreed on others. That distinction matters.

3. **Relationship-to-text** precision
   - Currently: a mention links a thesis to a scholar; the scholar may discuss multiple people in that mention
   - Needed: explicit edges: Thesis 4>2 + Jean Quidort with evidence from Copenhaver page 150, not just "Quidort appears in a Copenhaver mention of 4>2"
   - Why: A WRITER needs to know not just that Quidort is mentioned but exactly which passage in which source links Quidort to that thesis, and what kind of link (source, critique, contextual parallel)

4. **Scored relevance dimensions** replacing a single influence score
   - Currently: if a person is connected to a thesis, scoring could naively add points
   - Needed: Separate scores for textual_centrality, source_relation, network_relevance, controversy, historical_significance, evidence_quality, tradition_significance, reception
   - Why: Ficino's philosophical disagreement with Pico on One/Intellect (score: high controversy) is different from del Medigo's transmission of Averroist terminology (score: high source_relation, moderate evidence), which is different from Savonarola's later spiritual influence (score: low-to-moderate, speculative, but reception-important for understanding trial aftermath)

5. **Evidence provenance** for every relationship claim
   - Currently: claims have provenance; relationships do not
   - Needed: Who says Ficino was Pico's teacher? A documentary source? A scholarly inference? A later interpretation?
   - Why: The system must distinguish "Ficino's letters show they corresponded" (level 5) from "Copenhaver infers influence from doctrinal similarity" (level 3) from "tradition held they were rivals" (level 1)

6. **Text-specific relationship relevance**
   - Currently: a relationship applies uniformly to all theses (if it appears at all)
   - Needed: Ficino is highly relevant to De ente et uno, moderately relevant to some Neoplatonic theses, minimally relevant to angelology
   - Why: When a WRITER composes an entry on a thesis about the Trinity, knowing that Ficino is relevant to it is different from knowing that Ficino wrote extensively on the Trinity but the particular thesis does not engage him. Both are true; both have different weight.

---

## Part 3: Schema Extension (Entity-Relationship Diagram)

### New core entities:

```
PERSON
├─ id (surrogate: pico_ficino_1)
├─ canonical_name
├─ sort_name
├─ alternate_names[] {form: string, language: string, period: string}
├─ birth_year (int, nullable)
├─ death_year (int, nullable)
├─ locations[] (institutions, patronage, study, trouble, exile)
├─ occupations[] (teacher, translator, patron, judge, theologian, philosopher)
├─ languages[] (Latin, Greek, Hebrew, Italian, Chaldean)
├─ intellectual_traditions[] (Platonism, Aristotelianism, Scholasticism, Kabbalah, Hermeticism)
├─ major_works[] {title, date, type}
├─ authoritative_sources[] (biographical dictionaries, critical editions)
├─ evidence_status (primary_source | strong_doc | scholarly_inference | speculative)
├─ notes

RELATIONSHIP (directed edge Pico → Other or Other → Pico, but bidirectional)
├─ id (surrogate: rel_pico_ficino_correspondence_1)
├─ person_a (Pico)
├─ person_b (other agent)
├─ relationship_type enum (correspondence, friendship, patronage, teacher, student, collaborator, translator, source, intermediary, intellectual_influence, philosophical_interlocutor, philosophical_disagreement, polemical_opponent, theological_opponent, trial_participant, institutional_relationship, acquaintance, intellectual_circle, studied_work, cited_work, work_known_indirectly, posthumous_editor, reception_figure)
├─ relationship_subtype (refinements: e.g., patronage → Medici political patronage vs intellectual support)
├─ start_date (year, nullable; when did this relationship begin?)
├─ end_date (year, nullable; when did it end?)
├─ location (where was it most active?)
├─ directionality enum (bidirectional, a_to_b, b_to_a)
├─ is_documentary (true if grounded in correspondence, records, etc.; false if scholarly inference)
├─ confidence_level enum (5=primary_source, 4=strong_doc, 3=strong_inference, 2=plausible, 1=speculative, 0=unsupported)
├─ description (prose summary: why this relationship, what it meant)
├─ evidence[] (array of Evidence IDs; see below)
├─ created_by (agent name or user)
├─ created_date
├─ notes

RELATIONSHIP_EVIDENCE
├─ id (surrogate: ev_pico_ficino_corr_1)
├─ relationship_id (what relationship does this support?)
├─ evidence_type enum (primary_source, scholarly_argument, editorial_metadata, database_inference)
├─ source (WORK reference: work_id, line range, or passage)
├─ claim_text (what does the source say?)
├─ interpretation (how does this source support the relationship claim?)
├─ evidence_level (confidence in this piece of evidence)
├─ verified (true if quotation_gate passed)
├─ created_by
├─ notes

TEXT_PERSON_RELATIONSHIP (the key new entity: thesis + person + relationship)
├─ id (surrogate)
├─ text_id (which thesis, section, or work? Farmer ID for theses, or a more general work:section notation)
├─ person_id (which person?)
├─ relationship_type enum (directly_cites, quotes, paraphrases, argues_against, defends, uses_argument_from, uses_terminology_from, responds_to, contrasts_with, agrees_with, possible_influence, documented_influence, historical_context, later_interpreter)
├─ relationship_direction enum (forward: text→person, backward: person→text, mutual)
├─ relevance_level enum (high, moderate, low, tangential)
├─ confidence_level (5-0 scale)
├─ evidence[] (array of RELATIONSHIP_EVIDENCE IDs)
├─ notes

RELATIONSHIP_SCORING
├─ id
├─ text_id
├─ person_id
├─ score_textual_centrality (0-10: how central is the person's contribution to the text's argument?)
├─ score_source_relation (0-10: how directly does the text cite/quote/build on the person's work?)
├─ score_network_relevance (0-10: how strong is the documented relationship between Pico and the person?)
├─ score_controversy (0-10: was the person involved in a philosophical/theological disagreement on this topic?)
├─ score_historical_significance (0-10: did this person/topic play a role in the 1487 trial or later reception?)
├─ score_evidence_quality (0-10: how strong is the documentary evidence?)
├─ score_tradition_significance (0-10: does this connect to a major philosophical school or tradition?)
├─ score_reception (0-10: how important was this person to later interpreters of the text?)
├─ score_total (sum or weighted average)
├─ reasoning (prose explanation of why these dimensions matter for this thesis)
├─ created_by
├─ created_date
```

### Modified existing entities:

**THESIS** (add fields to existing structure):
```
├─ persons_connected[] (array of person_ids with TEXT_PERSON_RELATIONSHIP.relevance_level)
├─ intellectual_traditions[] (Platonism, Aristotelianism, Kabbalah, etc.)
├─ relationship_network_description (prose: how does this thesis sit in Pico's intellectual landscape?)
```

**MENTION** (extend existing entity):
```
├─ persons_mentioned[] {person_id, context_window_start, context_window_end, mention_type} 
├─ concepts_mentioned[]
├─ implied_relationships[] {person_a, person_b, relationship_type, evidence_level}
   (extracted by agent, verified before scoring)
```

---

## Part 4: Implementation Strategy

### Phase 0 (immediate): Bootstrap person directory

**Task**: Populate the `PERSON` table from gazetteer + audit findings + Farmer notes.

**Source material**:
- `build_dossiers.py` gazetteer (existing)
- Farmer's notes and cross-references (F:10566 ff.)
- Edelheit Part 3 (contemporary opponents)
- Copenhaver 2022 biographical appendices
- Wirszubski 1989 Kabbalistic figures
- PicoDB `scholars` table (26 seeded)

**Deliverables**:
- `data/network/persons.json` (structured, one record per person, with authority pointers)
- `data/network/persons_manifest.json` (metadata: when populated, by whom, status: draft/verified)
- Updated `data/claims/parties.json` (now linked to person IDs)

**Gate**: Every person must have ≥1 locator (Farmer page, Copenhaver reference, or corpus line). Names without evidence are marked speculative, not removed.

### Phase 1-Alpha (2-3 weeks): Relationship extraction and evidence grounding

**Agents** (parallel swarm):
- **RELATIONSHIP-HARVESTER-FICINO**: Read Copenhaver 2019+2022, Allen 2017, Farmer notes; extract all Pico-Ficino relationships with evidence
- **RELATIONSHIP-HARVESTER-KABBALAH**: Wirszubski, Idel, Busi; extract relationships for del Medigo, Mithridates, Alemanno
- **RELATIONSHIP-HARVESTER-SCHOLASTIC**: Edelheit Part 3, audit A2; extract 13 condemned theses, trial participants
- **RELATIONSHIP-HARVESTER-CONTEMPORARIES**: All works; cross-check Pico mentions vs. correspondence, deduplicate
- **RELATIONSHIP-LINKER**: Consolidate relationships; mark duplicates; assign relationship_ids; link evidence

**Output**:
- `data/network/relationships.json` (all directed edges with evidence, confidence, description)
- `data/network/relationships_manifest.json` (audit trail)
- `data/network/relationship_evidence.json` (indexed by relationship_id, with source locators)

**Gate**: No relationship without ≥1 evidence entry. Every evidence entry must pass `claims_verify.py` (locator checked, quote verbatim). Confidence levels must be justified in notes.

### Phase 1-Beta (parallel): Text-person scoring

**Task**: For each thesis (or text section), identify which people are relevant and in what way.

**Method**: 
- RESEARCHER reads the thesis packet (existing structure in `research-packets/`)
- Identifies people mentioned in Farmer's Latin or commentary
- Cross-references scholar mentions (existing data/ontology/mentions/)
- Creates `TEXT_PERSON_RELATIONSHIP` entries linking the thesis to persons with relationship_type
- Records evidence (Farmer line, scholar mention, conceptual connection)

**Output**:
- `data/network/text_person_relationships.json` (keyed by thesis_id, then person_id)
- Separate from `RELATIONSHIP` (which is Pico-other person); this is text-centric

**Gate**: Every entry must have a text locator (Farmer line) and a source locator (scholar mention or claim ID). "Possible influence" entries must be marked speculative and justified.

### Phase 2 (3-4 weeks): Relationship-to-text scoring

**Task**: For each thesis, compute the scoring dimensions for each associated person.

**Method**:
1. WRITER reads the thesis + the associated persons/relationships
2. Scores each dimension (1-10 scale):
   - **textual_centrality**: Does the thesis text explicitly engage this person's work?
   - **source_relation**: Does the Latin quote or paraphrase the person's writing?
   - **network_relevance**: How strong is the relationship (from RELATIONSHIP table)?
   - **controversy**: Is this person a named opponent/defender in this debate?
   - **historical_significance**: Trial material? Reception history?
   - **evidence_quality**: How well documented is the relationship?
   - **tradition_significance**: Does this person represent a major school relevant to this thesis?
   - **reception**: How important is this person to interpreting the thesis later?
3. Writes reasoning (prose) explaining why these scores matter
4. Stores in `RELATIONSHIP_SCORING` table

**Output**:
- `data/network/relationship_scores.json` (thesis_id → person_id → [dimension scores])
- `data/network/relationship_reasoning.json` (thesis_id → person_id → prose)

**Verification** (by VERIFIER):
- Spot-check reasoning against source material
- Ensure scores correlate with evidence level (high scores need strong evidence)
- Flag outliers (e.g., high score with level-1 evidence)

---

## Part 5: Integration with Existing Systems

### How the network informs thesis entries:

**Before WRITER begins**:
```
WRITER receives dossier containing:
├─ Farmer Latin + 1486 apparatus
├─ Thesis index and tier (existing)
├─ Historiographical importance grade (existing)
├─ Scholar mentions (existing)
├─ TEXT_PERSON_RELATIONSHIP entries (NEW)
│  └─ For each associated person:
│     ├─ Relationship type (e.g., "Ficino: philosophical_disagreement")
│     ├─ Relevance level (high/moderate/low)
│     ├─ Evidence (Copenhaver p. 150, Farmer note, etc.)
│     └─ Reasoning from RELATIONSHIP_SCORING
├─ RELATIONSHIP entries for context (NEW)
│  └─ What was the nature of Pico-Ficino relationship generally?
│     Correspondence: documented. Philosophical disagreement: Q4. Patron relationship: no.
└─ Suggestions (NEW)
   └─ "High network relevance: Ficino actively engaged this question. Moderate evidence for direct Pico-Ficino debate on this particular thesis. Do not assume agreement just because both are Platonists."
```

**WRITER then**:
- Uses TEXT_PERSON_RELATIONSHIP entries to mention people with precision (not vague "influenced by")
- Cites RELATIONSHIP entries to contextualize disputes (e.g., "Unlike Ficino, Pico...")
- Draws on RELATIONSHIP_SCORING reasoning to calibrate how much space to give to a person in the commentary
- Flags potential misinterpretations (e.g., "Pico cites Henry of Ghent here, but not as a target; Pico uses Henry's framework to argue against a different objection")

### How scoring appears in the UI:

**Thesis card** (browsing):
```
4>2 [Eucharist]
Related: Ficino (philosophical_disagreement, network_relevance: 7/10)
         Quidort (source_relation: 8/10)
         Del Medigo (network_relevance: 4/10, marginal to this thesis)
```

**Thesis detail page**:
```
Intellectual Network
==================
Marsilio Ficino
  Relationship: Philosophical disagreement on the nature of substantial change
  Evidence: De ente et uno vs. Ficino's Theologia Platonica
  Network relevance: 8/10 (strong contemporary debate)
  Evidence quality: 9/10 (both primary sources engaged)
  Controversy: 9/10 (this is one of Pico's major points against Ficino)
  [More →] [Historical context] [Primary texts]

Jean Quidort
  Relationship: Pico uses Quidort's impanation model as a framework
  Evidence: Copenhaver 2022, ch. 4; Farmer note, l. 21500
  Source relation: 8/10 (thesis quotes/adapts Quidort)
  Evidence quality: 8/10 (Copenhaver traces the genealogy)
  Tradition significance: 7/10 (connects to 13th-c. eucharistic debates)
```

**Research view** (for scholars):
```
Filter by relationship type: [source] [influence] [disagreement] [context]
Filter by evidence level: [5: primary] [4: strong doc] [3: inference] [2-1: speculative]
Sort by: network_relevance | evidence_quality | tradition_significance
[Show reasoning] [Show all evidence]
```

---

## Part 6: Non-Negotiable Rules (from CLAUDE.md, carried into this system)

1. **No relationship is created without evidence.** A person is not "connected" to a thesis unless:
   - The thesis Latin explicitly names or quotes them, OR
   - A scholar explicitly links them in a passage we can point to, OR
   - The relationship is marked speculative with level 1 confidence and a clear justification

2. **Every confidence level must be justified.** A "level 5 = primary source" edge requires:
   - The primary source (Pico text, letter, Ficino response)
   - The exact passage (work:line)
   - A quotation or paraphrase that the quotation gate verified

3. **Relationships are not symmetric by default.** Pico → Ficino (correspondence) is different from Ficino → Pico (correspondence). The direction matters for some questions and should be explicit.

4. **Distinction between direct evidence and inference is mandatory.** Record separately:
   - "We have Ficino's letter to Pico dated 1485" (level 5)
   - "Copenhaver infers that Pico read Ficino's Theologia Platonica" (level 3)
   - These are different relationships or aspects of the same relationship, not collapsed into one score

5. **A relationship can have multiple pieces of evidence.** Pico-Ficino correspondence is grounded in:
   - Surviving letters (primary source, level 5)
   - Ficino's later response to De ente et uno (primary source, level 5)
   - Doctrinal parallels (scholarly inference, level 3)
   - Each is a separate evidence entry, not one aggregate claim.

6. **Do not retroactively infer influence.** Just because Pico and Ficino both wrote about the Intellect does not mean one influenced the other. The influence claim is a separate, testable claim that must be evidenced separately.

7. **A person's later reception is distinct from their influence on Pico.** Gianfrancesco Pico (nephew, posthumous editor) is NOT "an influence on Pico" in the normal sense; he reshaped Pico's reputation *after* Pico died. This is a different relationship type: `posthumous_editor` / `reception_figure`.

---

## Part 7: Relationship Type Vocabulary (Controlled Vocabulary)

These are mutually exclusive classifications for a relationship. One RELATIONSHIP entry has one primary type, but can have subtypes or notes for nuance.

### Documentary/Epistolary:
- **correspondence**: Surviving letters, documented exchange
- **friendship**: Described or implied by contemporaries; testimony of warmth/respect

### Intellectual/Pedagogical:
- **teacher** / **student**: Explicit instruction (del Medigo for Kabbalah/Aristotle)
- **collaborator**: Joint projects or active consultation (Mithridates + Pico on Kabbalistic texts)
- **translator**: One person translated the other's work or mediated translation (Mithridates, Alemanno)
- **source**: One person's work is a direct source for the other's thinking (Quidort → Pico on impanation)
- **intermediary**: Transmitted ideas indirectly (Mithridates, Alemanno as intermediaries for Kabbalistic material)

### Philosophical/Theological:
- **intellectual_interlocutor**: Engaged in a debate (Ficino, Henry of Ghent as intellectual opponents/partners)
- **philosophical_disagreement**: Explicit dispute on a question (Pico vs. Ficino on the One)
- **philosophical_agreement**: Both argue for the same position (Pico agrees with Aquinas on angel location in some respects)

### Institutional/Social:
- **patron** / **patronage**: Financial or institutional support (Lorenzo de' Medici)
- **institutional_relationship**: Both hold positions in the same institution (Neoplatonic Academy, papal court)
- **acquaintance**: Known but no major relationship attested

### Oppositional:
- **polemical_opponent**: Explicitly named as wrong or heretical (Pedro Garsia, trial opponents)
- **theological_opponent**: Disagrees on theological grounds without personal polemic (some scholastics)

### Historical/Circumstantial:
- **trial_participant**: Involved in the 1487 investigation (commissioners, defendants, inquisitors)
- **contemporary**: Lived in same era and milieu but no documented relationship
- **member_of_same_intellectual_circle**: Both part of Florentine Neoplatonic movement

### Reception:
- **posthumous_editor**: Edited or published after the author's death (Gianfrancesco)
- **later_respondent**: Engaged with the author's work after their death (Savonarola, 17th-century Jesuits)
- **reception_figure**: Important to how the author's work was interpreted (Copenhaver, modern Pico scholars)

---

## Part 8: Evidence Level Grading Rubric

**Level 5: Primary Source Documentary**
- Surviving letter, manuscript, printed edition from Pico's time or nearby
- The relationship is explicit and unambiguous
- Example: Ficino's letter dated 1485, thanking Pico for engagement with his work
- Verdict: verbatim, documentary

**Level 4: Strong Contemporary or Near-Contemporary Documentation**
- Account by someone who knew Pico or was reporting on contemporaries
- Credible testimony, not later invention
- Example: Gianfrancesco Pico's biography saying Giovanni studied with del Medigo
- Verdict: strong_doc

**Level 3: Strong Scholarly Inference from Primary Sources**
- Multiple primary sources point to a relationship, but the relationship word is not explicit
- The inference is grounded in textual analysis or archival cross-reference
- Example: Copenhaver's analysis showing Pico's use of Ficino's Theologia Platonica language patterns
- Verdict: strong_inference

**Level 2: Plausible Scholarly Inference**
- Plausible given the context, but based on fewer primary sources or more speculative reasoning
- Respectable scholars disagree about it
- Example: "Pico probably knew X's work because it was widely read" (but no direct evidence)
- Verdict: possible

**Level 1: Speculative / Traditional**
- Based on later tradition, conjecture, or guesswork
- Useful context but not scholarly evidence
- Example: "Renaissance tradition says Pico was influenced by Kabbalah" (true, but distinguish from documentary evidence)
- Verdict: speculative

**Level 0: Unsupported**
- No credible evidence; do not store as a relationship
- Flag if found and mark as requiring evidence before acceptance

---

## Part 9: Scope: The 25+ Core Figures in Pico's Intellectual Network

**Immediate priority** (Phase 1-Alpha): The 32-person core network drawn from Copenhaver, Howlett, Edelheit, and direct archival evidence.

### Tier 1: Central relationships (documented correspondence, collaboration, philosophical controversy)

**1. Marsilio Ficino (1433–1499)** — Mentor, friend, intellectual competitor, correspondent, and foil
- Relationship types: correspondence, friendship, intellectual_interlocutor, philosophical_disagreement
- Why central: Documented correspondence; intellectual partnership with underlying contest (Commento on Benivieni vs. De amore; De ente et uno vs. Theologia Platonica)
- Key evidence: Ficino's letters; Pico's Commento and De ente et uno; Copenhaver 2022; Howlett; Edelheit
- Network function: Hub for Florentine Platonism; simultaneously critic of Pico's philosophy
- Historiographical note: Gianfrancesco's posthumous presentation of harmony obscures the actual intellectual tensions

**2. Angelo Poliziano (1454–1494)** — Friend, correspondent, early critic, literary interlocutor
- Relationship types: correspondence, friendship, intellectual_interlocutor, collaborator
- Why central: Close Florentine intellectual friend; Pico asked his critique of poetry; critique prompted Pico's turn toward philosophy
- Key evidence: Howlett; Ficino correspondence mentions Poliziano; Pico's literary development
- Network function: Bridge between Pico's literary and philosophical projects; represents humanist philological method
- Historiographical note: Shows Pico's engagement with both humanist and scholastic traditions

**3. Ermolao Barbaro (1454–1493)** — Philosophical correspondent, linguistic/stylistic disputant
- Relationship types: correspondence, intellectual_interlocutor, philosophical_disagreement
- Why central: 1485 letter to Barbaro is one of Pico's earliest explicit philosophical controversies; defends scholastic philosophical language against humanist criticism
- Key evidence: Pico's 1485 letter to Barbaro; Copenhaver 2022; direct primary source engagement
- Network function: Marks Pico's negotiation between humanism and scholasticism; defends technical vocabulary
- Historiographical note: This dispute is foundational to understanding Pico's method and his later scholastic apparatus

**4. Elia del Medigo / Elijah of Candia (c. 1458–1493)** — Teacher in Padua; intermediary for Averroism, Hebrew, Kabbalah
- Relationship types: teacher, source, intermediary, intellectual_interlocutor
- Why central: Major influence on Pico's Aristotelian/Averroist and Hebrew education; not a Kabbalist himself but gateway to Jewish intellectual traditions
- Key evidence: Howlett; Mahoney essay on Pico & Del Medigo; Pico's later use of Averroist terminology
- Network function: Represents scholastic Aristotelianism side of Pico's education; transmits Jewish/Arabic intellectual networks
- Historiographical note: Del Medigo provides access to living Jewish intellectual traditions, not isolated occultism

**5. Flavius Mithridates** — Hebrew/Aramaic/Chaldean teacher, translator, collaborator
- Relationship types: teacher, translator, collaborator, intermediary
- Why central: Most important technical intermediary between Pico and Hebrew/Kabbalistic materials; Pico employed him; relationship was intellectually productive but interpersonally contentious
- Key evidence: Howlett; sarcastic marginal comments by Mithridates; 1489 arrest in Viterbo with Pico's books
- Network function: Pico's research laboratory for languages and translations; shows network functioning as applied research
- Historiographical note: Mithridates is rehabilitated by Howlett/modern scholarship from older dismissive accounts

**6. Yohanan Alemanno** — Hebrew scholar, Kabbalist, collaborator, possible teacher
- Relationship types: teacher, collaborator, intellectual_interlocutor, source
- Why central: Alemanno's *Commentary on the Song of Songs* was written at Pico's suggestion; embedded Pico in living Jewish Kabbalistic networks; Alemanno's own testimony is unusual primary source
- Key evidence: Howlett; Fanger *Invoking Angels*; Alemanno's own writings
- Network function: Key for understanding Kabbalah as embedded in Jewish intellectual networks, not merely Christian appropriation
- Historiographical note: Shows Pico's project as intercultural and relational, not appropriative

**7. Girolamo Benivieni (1453–1542)** — Friend, literary collaborator, student
- Relationship types: friendship, collaborator, intellectual_interlocutor
- Why central: Co-author of Commento on Song of Benivieni; Pico's test case for challenging Ficino's interpretation of Platonic love; both moved toward Savonarola
- Key evidence: Howlett; Edelheit; literary manuscripts
- Network function: Shows Pico's contests played out through specific texts and collaborators
- Historiographical note: Demonstrates that "Savonarola's circle" and "Ficino's circle" were not cleanly divided

### Tier 2: Major intellectual relationships (documented but less intensive correspondence)

**8. Nicoletto Vernia (c. 1420–1499)** — Paduan Aristotelian teacher
- Relationship types: teacher, intellectual_interlocutor, source
- Why central: Leading Paduan Aristotelian of Pico's generation; represents scholastic Aristotelian infrastructure Pico never abandoned
- Key evidence: Howlett; Mahoney essay; Pico's continued use of Aristotelian apparatus
- Network function: Anchors Pico's Aristotelianism; essential for understanding concordia with Platonism

**9. Agostino Nifo (c. 1473–1538)** — Paduan Aristotelian, peer/slightly younger
- Relationship types: intellectual_interlocutor, source, contemporary
- Why central: Part of Pico's Paduan circle; represents developing Renaissance Aristotelianism
- Key evidence: Howlett; Mahoney essay; Paduan university records
- Network function: Shows Pico's engagement with working Aristotelians, not just texts

**10. Lorenzo de' Medici (1449–1492)** — Patron, protector, literary correspondent
- Relationship types: patron, patronage, institutional_relationship, correspondent
- Why central: Political protector during trial; helped Pico return to Florence; member of intellectual network rather than philosophical teacher
- Key evidence: Pico's 1484 letter on poetry; Copenhaver 2022; Ficino correspondence
- Network function: Hub for Florentine intellectual patronage; essential for understanding material conditions of Pico's work

**11. Girolamo Savonarola (1452–1498)** — Late-life intellectual and religious interlocutor
- Relationship types: intellectual_interlocutor, later_respondent, philosophical_disagreement
- Why central: Pico and Savonarola reportedly discussed ancient pagan theology and Christianity; relationship developed over time; not a simple "conversion" narrative
- Key evidence: Edelheit; Copenhaver 2022; Benivieni's attendance at Savonarola's sermons with Pico
- Network function: Shows Pico's movement toward Savonarola; complicated by Savonarola's posthumous construction of Pico
- Historiographical note: Savonarola's account of Pico is reception history, not necessarily accurate to Pico's actual thought

**12. Gianfrancesco Pico della Mirandola (1469–1533)** — Nephew, posthumous editor, intellectual interpreter
- Relationship types: posthumous_editor, reception_figure, later_respondent
- Why central: Published 1496 edition; wrote *Vita*; shaped posthumous Pico image; suppressed and reframed materials
- Key evidence: Copenhaver 2022; Howlett; Gianfrancesco's editorial decisions
- Network function: **Reception history**: constructed "Christian saint Pico" that obscures earlier philosophical tensions
- Historiographical note: Gianfrancesco is both primary witness and active constructor of Pico tradition; must be read critically

### Tier 3: Paduan circle and educational formation

**13. Girolamo Donato** — Paduan intellectual companion
- Network function: Reconstructs actual social environment at Padua
- Key evidence: Howlett

**14. Girolamo Ramusio** — Paduan companion, later Orientalist
- Relationship types: intellectual_interlocutor, contemporary
- Network function: Shows knowledge network for languages and texts
- Key evidence: Howlett

**15. Battista Guarini (1435–1503)** — Ferrara teacher in rhetoric and humanities
- Relationship types: teacher, intellectual_interlocutor
- Network function: Literary and rhetorical formation before mature philosophy
- Key evidence: Howlett; Treccani

### Tier 4: Trial commission and institutional opposition (1487)

The commission examining Pico's Conclusions was internally divided. These individuals represent the institutional mechanism rather than personal philosophical relationships.

**16. Pedro Garcia, Bishop of Ussel** — Most important philosophical opponent
- Relationship types: polemical_opponent, theological_opponent, trial_participant
- Why important: Published *Determinationes magistralis contra conclusiones apologeticas* (1489) in response to Pico's *Apology*
- Key evidence: Copenhaver 2022; direct engagement with magic and Kabbalah
- Network function: Shows "Pico versus the theologians" in its most substantive form

**17. Jean Cordier** — Parisian theologian, commission member, Pico's defender
- Relationship types: correspondent, intellectual_interlocutor, trial_participant
- Why important: Defended theses; refused to sign final condemnation; links Pico's Parisian education to trial
- Key evidence: Edelheit; Howlett
- Network function: Shows commission was divided; Pico had support even among inquisitors

**18. Jean Monissart, Bishop of Tournai** — Commission presiding officer
- Relationship types: institutional_relationship, trial_participant
- Key evidence: Howlett; Copenhaver

**19. Marco de Miroldo** — Dominican, Master of Sacred Palace
- Relationship types: institutional_relationship, trial_participant
- Note: Did not participate fully due to illness; represents internal division

**20. Giovanni de Myrle** — Roman theologian, pro-Pico
- Relationship types: institutional_relationship, trial_participant
- Network function: Part of Pico's support network during trial

**21. Bonfrancesco Arlotti, Bishop of Reggio Emilia** — Favorable toward Pico, outside formal commission
- Network function: Shows "Church's response" was diverse

**22. Cardinal Giorgio da Costa, Bishop of Lisbon** — Favorable toward Pico
- Network function: Demonstrates disagreement among Roman theologians

**23. Gioacchino da Vinci** — Dominican superior general
- Relationship types: institutional_relationship, trial_participant

**24. Antonio Flores** — Legal expert on commission
- Relationship types: institutional_relationship, trial_participant

**25. Luca Borsiani da Foligno** — Papal confessor
- Relationship types: institutional_relationship, trial_participant

**26. Francesco da Murcia** — Papal-court theologian
- Relationship types: institutional_relationship, trial_participant

**27. Battista Signori da Genova** — Augustinian, trial participant
- Network function: Shows commission included multiple religious orders

**28. Cristoforo da Castronuovo** — Professor of theology
- Relationship types: institutional_relationship, trial_participant

### Tier 5: Ancient/Medieval philosophical sources (non-personal relationships)

These are sources Pico studied, quoted, or engaged with textually rather than through personal correspondence. They are relational in the sense that Pico's theses demonstrate engagement with their work.

**29. Thomas Aquinas** — Scholastic source, especially on theology
- Relationship types: source
- Why important: Extensive quotation and engagement in scholastic sections (1-6)
- Key evidence: Pico's theses; Edelheit 2022 Part 1

**30. Henry of Ghent** — Scholastic source on metaphysics and theology
- Relationship types: source
- Evidence: Farmer's notes; Copenhaver's analysis

**31. Plotinus** — Neoplatonic source, especially for Ficino dispute
- Relationship types: source, contested_interpretation
- Why important: Pico positions himself as alternative interpreter to Ficino
- Key evidence: Howlett; Commento on Benivieni

**32. Proclus** — Neoplatonic source, theological influence
- Relationship types: source

**Later expansion**: Hermes Trismegistus, Corpus Hermeticum, Gersonides, Recanati, Abulafia, Maimonides, Zoroaster, Orpheus, etc.

### Others mentioned in theses (sample):

**Antonio Cittadini** — Post-Pico controversy with Gianfrancesco; reception
- Relationship types: later_respondent, reception_figure
- When to add: After Pico's own lifetime, debates interpretation

**Paolo Cortesi** — Later defender of Pico
- Relationship types: reception_figure, later_respondent

---

## Part 10: Known Challenges and Mitigations

### Challenge 1: Same person, multiple names
**Problem**: "Henry of Ghent" = "Henricus Gandavensis" = "Henri de Gand" = "Heinrich von Gent"
**Mitigation**: `PERSON.alternate_names` with language/period tags; gazetteer updated to use `person_id`, not string names

### Challenge 2: Retroactive inference of influence
**Problem**: Both Pico and Ficino write on the Intellect; scholars infer influence without documentary evidence
**Mitigation**: `RELATIONSHIP.is_documentary` flag; separate level-5 "documented" from level-3 "inferred"; WRITER told to distinguish

### Challenge 3: Directionality ambiguity
**Problem**: "Pico and Ficino corresponded" is true, but did Pico ask Ficino's advice? Did Ficino initiate?
**Mitigation**: `RELATIONSHIP.directionality` enum; record the direction of influence/request explicitly; notes clarify if known

### Challenge 4: Reception distortion
**Problem**: Gianfrancesco's editorial decisions or Savonarola's later theology may not reflect Giovanni's own thought
**Mitigation**: Separate relationship types for posthumous_editor / later_respondent; mark as reception-important but not influence

### Challenge 5: Overcounting evidence
**Problem**: Same fact appears in multiple scholars (Copenhaver cites Farmer; both cite the Farmer line); avoid double-scoring
**Mitigation**: Evidence deduplicated by source locator; if two scholars cite the same passage, one evidence record with `scholars_citing[]` list

### Challenge 6: Speculative vs. speculativeness
**Problem**: A relationship marked level-1 speculative is still indexed; risk of treating it as fact
**Mitigation**: UI clearly labels confidence level; filtering on evidence_level ≥3 removes speculation; scores for speculative relationships are separate or suppress entirely

---

## Part 11: Integration with Existing DECISIONS.md and CLAUDE.md Rules

### From CLAUDE.md (non-negotiable):
1. **Never invent text.** → Every relationship text is cited from a source.
2. **No script writes prose.** → WRITER writes reasoning; scripts carry it forward only.
3. **No self-approval.** → RELATIONSHIP extracted by one agent, verified by another.
4. **Quote gate.** → RELATIONSHIP_EVIDENCE entries pass claims_verify.py before storage.
5. **Verify before "done".** → No relationship_scores published until spot-checked.

### Integration with existing workflows:
- **HARVESTER** (existing in RESEARCH_PROTOCOL.md) → Outputs TEXT_PERSON_RELATIONSHIP and RELATIONSHIP_EVIDENCE entries (new output format)
- **EXTRACTOR** (existing) → Also extracts implied relationships from mentions; flags for LINKER
- **LINKER** (existing) → Now handles relationship deduplication and evidence consolidation
- **WRITER** (existing) → Receives RELATIONSHIP_SCORING suggestions; writes reasoning; entries auto-cite people with precision
- **VERIFIER** (claims_verify.py) → Also spot-checks RELATIONSHIP_EVIDENCE entries

---

## Part 12: Success Metrics & Gating

### Phase 0 (Person bootstrap):
- [ ] 40+ persons in `data/network/persons.json`, each with ≥1 locator, authority source, alternate names
- [ ] Every person in gazetteer mapped to person_id
- [ ] Manifest written with status (draft/verified)

### Phase 1-Alpha (Relationship extraction):
- [ ] 200+ relationships extracted across Pico-other figures
- [ ] Every relationship has ≥1 evidence entry with verified locator
- [ ] Evidence level distribution: ≥20% level 5, ≥40% level 4, rest 3+
- [ ] No level-0 unsupported relationships in final set

### Phase 1-Beta (Text-person scoring):
- [ ] 100% of 900 theses have TEXT_PERSON_RELATIONSHIP entries where applicable
- [ ] No text-person entry without evidence (Farmer line or scholar mention)
- [ ] Relationships marked speculative are ≤10% of total per thesis

### Phase 2 (Scoring & reasoning):
- [ ] RELATIONSHIP_SCORING entries for top 50 theses (A-tier)
- [ ] Each score has prose reasoning ≥50 words
- [ ] Spot-check: high scores correlate with high evidence levels
- [ ] WRITER entries cite people with precision (name + relationship type + passage)

### Ongoing:
- [ ] New theses onboarded with TEXT_PERSON_RELATIONSHIP entries
- [ ] Network graph updated as new scholarship ingested
- [ ] Contradictions in scholarly interpretations recorded (historiographical disputes)

---

## Part 13: Files to Create / Modify

### New files:
- `data/network/persons.json`
- `data/network/persons_manifest.json`
- `data/network/relationships.json`
- `data/network/relationships_manifest.json`
- `data/network/relationship_evidence.json`
- `data/network/text_person_relationships.json`
- `data/network/relationship_scores.json`
- `data/network/relationship_reasoning.json`
- `docs/INTELLECTUAL_NETWORK_SYSTEM.md` (operational guide)
- `scripts/network_bootstrap.py` (populate persons from gazetteer + audit)
- `scripts/network_harvest.py` (extract relationships from claims + mentions)
- `scripts/network_verify.py` (spot-check relationships against source)
- `scripts/network_score.py` (compute relationship_scores from gathered dimensions)

### Modified files:
- `data/claims/parties.json` (add person_id foreign key)
- `data/ontology/mentions/by_thesis/` (add implied_relationships[] extraction)
- `research-packets/INDEX.md` (document new TEXT_PERSON_RELATIONSHIP field in packets)
- `scripts/build_dossiers.py` (include TEXT_PERSON_RELATIONSHIP in packet output)
- `docs/ORCHESTRATION.md` (add Phase 1-Alpha, Phase 1-Beta, Phase 2 tasks)
- `HANDOVER.md` (updated with network system rollout plan)
- `DECISIONS.md` (record design decisions and why)

---

## Part 14: Relationship to Scoring Algorithm (Future)

The existing thesis scoring algorithm (if any) should be extended, not replaced. The RELATIONSHIP_SCORING dimensions feed into the final thesis metadata but do not become a single number.

**Proposal** (for later decision, not now):
- Thesis entry displays: `score_historiographical_importance` (existing, from DATA_ONTOLOGY)
- Thesis entry displays: `network_metadata` with per-person dimensions (NEW)
- UI allows filtering/sorting by individual dimensions
- Research view allows "show me theses with high Ficino relevance" or "show me theses grounded in primary Aristotelian sources"

This preserves the existing importance grading while adding relational depth without collapsing nuance.

---

## Timeline & Next Steps

1. **This session**: Specification document (DONE — you're reading it)
2. **Next session (Phase 0, 1-2 days)**:
   - Run `bootstrap_persons.py` (gazetteer → persons.json, with draft confidence)
   - Hand-add high-priority figures from Edelheit, Copenhaver, Wirszubski
   - Write `persons_manifest.json` with provenance
3. **Following 2-3 weeks (Phase 1-Alpha)**:
   - Deploy RELATIONSHIP-HARVESTER agents (parallel by figure/work)
   - Output to `relationships.json`, `relationship_evidence.json`
   - Run verification loop via claims_verify.py
4. **Following 1-2 weeks (Phase 1-Beta)**:
   - RESEARCHER + build_dossiers.py produce TEXT_PERSON_RELATIONSHIP entries
   - Populate `text_person_relationships.json` (all 900 theses)
5. **Following 3-4 weeks (Phase 2)**:
   - WRITER scores each thesis-person pair
   - Populate `relationship_scores.json` with reasoning
   - Site rendering updated to display network metadata

**Total**: ~6-8 weeks from specification to full deployment. Can parallelize Phases 1-Alpha and 1-Beta.

---

## Appendix A: Example Relationship Records

### Pico ↔ Ficino: Correspondence

```json
{
  "id": "rel_pico_ficino_correspondence_1",
  "person_a_id": "pico_giovanni_1",
  "person_b_id": "ficino_marsilio_1",
  "relationship_type": "correspondence",
  "directionality": "bidirectional",
  "start_date": 1480,
  "end_date": 1494,
  "location": "Florence",
  "is_documentary": true,
  "confidence_level": 5,
  "description": "Documented exchange of letters between Ficino and Pico, discussing philosophical questions, with Ficino in the role of elder Platonist mentor.",
  "evidence": ["ev_ficino_letter_1485", "ev_pico_response_1485"],
  "notes": "Surviving letters in Ficino Opera; Kristeller edition. Relationship existed for the last ~15 years of Pico's life."
}
```

### Pico ↔ Ficino: Philosophical Disagreement

```json
{
  "id": "rel_pico_ficino_disagreement_1",
  "person_a_id": "pico_giovanni_1",
  "person_b_id": "ficino_marsilio_1",
  "relationship_type": "philosophical_disagreement",
  "relationship_subtype": "neoplatonic_metaphysics_one_intellect",
  "directionality": "bidirectional",
  "start_date": 1492,
  "end_date": 1494,
  "location": "Florence",
  "is_documentary": true,
  "confidence_level": 5,
  "description": "Pico's De ente et uno directly critiques Ficino's Theologia Platonica on the procession of the Intellect from the One. Ficino appears to have been aware of Pico's objections.",
  "evidence": ["ev_de_ente_pico_latin", "ev_theologia_ficino_latin", "ev_copenhaver_analysis"],
  "notes": "This is one of the most documented Pico-Ficino interactions. Both works are primary source documents. Copenhaver 2022 ch. 5 provides the scholarly synthesis."
}
```

### Pico → del Medigo: Teacher/Interlocutor

```json
{
  "id": "rel_pico_delmedigo_teacher_1",
  "person_a_id": "pico_giovanni_1",
  "person_b_id": "delmedigo_elia_1",
  "relationship_type": "teacher",
  "relationship_subtype": "hebrew_kabbalah_aristotelian",
  "directionality": "b_to_a",
  "start_date": 1485,
  "end_date": 1494,
  "location": "Florence",
  "is_documentary": true,
  "confidence_level": 4,
  "description": "Del Medigo instructed Pico in Hebrew language, Kabbalistic texts, and Averroist Aristotelian philosophy during Pico's years in Florence (evidence from Pico's later writings and Gianfrancesco's biography).",
  "evidence": ["ev_gianfrancesco_biography", "ev_pico_kabbalistic_theses", "ev_wirszubski_analysis"],
  "notes": "Gianfrancesco's account is contemporaneous (early 16th c.). Pico's Kabbalistic conclusions (section 10) show del Medigo's influence. Wirszubski 1989 is the authoritative study."
}
```

### Pico → Aquinas: Source (not teacher, not personal)

```json
{
  "id": "rel_pico_aquinas_source_1",
  "person_a_id": "pico_giovanni_1",
  "person_b_id": "aquinas_thomas_1",
  "relationship_type": "source",
  "directionality": "b_to_a",
  "start_date": 1450,
  "end_date": 1494,
  "location": null,
  "is_documentary": false,
  "confidence_level": 4,
  "description": "Pico cites and engages Aquinas extensively in the scholastic Conclusions (sections 1-6). Aquinas is a major source for Pico's theological method.",
  "evidence": ["ev_pico_latin_thesis_1_1", "ev_pico_latin_thesis_2_3", "ev_edelheit_analysis"],
  "notes": "This is not a personal relationship (Aquinas died 1274). It is a intellectual relationship grounded in textual engagement. Edelheit 2022 part 1 catalogs Pico's use of Aquinas."
}
```

### Pico ↔ Savonarola: Later Reception

```json
{
  "id": "rel_pico_savonarola_reception_1",
  "person_a_id": "pico_giovanni_1",
  "person_b_id": "savonarola_girolamo_1",
  "relationship_type": "later_respondent",
  "directionality": "b_to_a",
  "start_date": 1495,
  "end_date": 1498,
  "location": "Florence",
  "is_documentary": true,
  "confidence_level": 3,
  "description": "Savonarola (who knew Pico personally in the early 1490s) engaged with Pico's Neoplatonic theology and may have influenced Pico's later turn toward religious devotion. Savonarola later became a dominant figure in interpreting Pico's legacy.",
  "evidence": ["ev_gianfrancesco_pico_biography", "ev_copenhaver_savonarola_section", "ev_savonarola_sermons"],
  "notes": "This is a reception relationship, not an influence on Pico's Conclusions. Savonarola's role in Pico's later intellectual life is disputed; evidence is circumstantial (both in Florence, both religious). Later tradition made Savonarola a key interpreter of Pico."
}
```

---

**Document Status**: Specification, ready for Phase 0 bootstrap. Next: implementation scripts and manifest structure.
