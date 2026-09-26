# Research Protocol: Mining scholar knowledge to build historiographical dossiers

**Objective**: Extract what our scholars know about each thesis (mentions, claims, connections, interpretations) and structure it as historiographical context for WRITER entries.

**Sources**: 73 Markdown files of OCR'd scholarship + audiobookmaker text versions + critical editions.

**Output**: Structured JSON in `data/ontology/` keyed by thesis_id, scholar name, and entity type (person/concept).

---

## Phase 1: Identify thesis mentions in scholar texts

**Task**: For each scholar work, find every passage that discusses a Pico thesis.

**Method**: 

1. **Keyword-driven search** (HARVESTER-SEARCH agent)
   - Search for thesis incipits (opening words in Latin)
   - Search for thesis numbers (if scholars use Farmer's numbering or the Apologia's Q1-Q13)
   - Search for doctrinal keywords (e.g., "unity of intellect", "divine assumption", "Kabbalah", "magic")
   - Search for key people mentioned in thesis sources (e.g., "Henry of Ghent", "Averroes", "Jean Quidort")

2. **Context window** (HARVESTER-EXTRACT agent)
   - For each hit, extract a 200-500 word context window around the mention
   - Preserve the page/line number or file:line locator for verification

3. **Deduplication** (HARVESTER-DEDUPE agent)
   - If the same passage appears in multiple scholar works (e.g., Farmer and Copenhaver both quote the same Pico Latin), keep only one canonical version with pointers to where else it appears

**Output**: `data/ontology/mentions/by_thesis/{thesis_id}.json`
```json
{
  "thesis_id": "4>2",
  "mentions": [
    {
      "scholar": "Copenhaver",
      "work": "Pico on Trial",
      "locator": "l. 8050-8078",
      "context_window": "...Jean Quidort's impanation theory... [200-500 words]",
      "confidence": "to_be_verified"
    }
  ]
}
```

---

## Phase 2: Extract atomic claims (EXTRACTOR agents)

**Task**: For each mention, identify the factual claims being made.

**Claim types**:
- `doctrinal_content`: What does Pico say in this thesis? (primary source)
- `historical_event`: What happened in Pico's life or times relevant to this thesis?
- `interpretive_position`: What does this scholar argue about the thesis?
- `source_identification`: Where did Pico get this idea? (e.g., "from Henry of Ghent")
- `biography`: A biographical detail explaining the thesis

**Example**:
Mention: "Jean Quidort argued that a stone could be made a supposit by God."

Claims extracted:
1. `source_identification`: "Jean Quidort held that stones can be assumed by God" (Copenhaver, source)
2. `doctrinal_content`: "Q6 (4>2) descends from Quidort's impanation model" (Copenhaver, interpretation)
3. `source_identification`: "Pico took this model second-hand from Jean Cabrol" (Copenhaver, source)

**Output**: `data/ontology/claims/{thesis_id}.json`
```json
{
  "thesis_id": "4>2",
  "claims": [
    {
      "id": "claim_4>2_001",
      "text": "Jean Quidort argued that a stone could be made a supposit by God",
      "claim_type": "source_identification",
      "source": {
        "scholar": "Copenhaver",
        "work": "Pico on Trial",
        "locator": "l. 6750-6751"
      },
      "confidence": "verbatim_quotation",
      "entities": ["Jean Quidort", "divine assumption", "stones"]
    }
  ]
}
```

---

## Phase 3: Extract connections (LINKER agents)

**Task**: For each thesis, identify people and concepts linked to it.

**Connection types**:
- `source`: A prior thinker whose work Pico reworked (e.g., "Henry of Ghent → Q4")
- `critique`: A thinker who criticized or disagreed with Pico's position
- `inspiration`: A work that inspired Pico (e.g., "Book of Causes → doctrinal parallelism")
- `biographical_moment`: An event in Pico's life that shaped this thesis (e.g., "trial → Q6 defense")
- `doctrinal_parallel`: Another thesis that relies on the same principle

**Extraction logic**:
- For each Claim of type `source_identification`, create a Connection
- For each person named in a mention of a thesis, create a Connection (if the scholar explicitly links them)
- For each doctrinal keyword (e.g., "assumption", "intellect"), create a Connection

**Output**: `data/ontology/connections/{thesis_id}.json`
```json
{
  "thesis_id": "4>2",
  "connections": [
    {
      "entity_type": "person",
      "entity_name": "Jean Quidort",
      "relation_type": "source",
      "scholars_who_note_this": ["Copenhaver", "Farmer"],
      "mention_count": 2,
      "primary_locator": {
        "scholar": "Copenhaver",
        "work": "Pico on Trial",
        "locator": "l. 8050-8078"
      }
    },
    {
      "entity_type": "person",
      "entity_name": "Jean Cabrol",
      "relation_type": "source",
      "scholars_who_note_this": ["Copenhaver"],
      "mention_count": 1
    },
    {
      "entity_type": "concept",
      "entity_name": "divine assumption",
      "relation_type": "doctrinal_framework",
      "scholars_who_note_this": ["Copenhaver", "Farmer", "Edelheit"],
      "mention_count": 5
    }
  ]
}
```

---

## Phase 4: Identify historiographical disputes (SYNTHESIZER agents)

**Task**: Find places where scholars disagree about a thesis.

**Method**:
- For each thesis, compare interpretations across scholars
- Identify pairs of Claims that contradict each other
- Mark which scholars align and which dissent

**Example**:
- Copenhaver: "Q4 is Pico's attempt to reconcile divine omnipotence with human freedom"
- Edelheit: "Q4 is a scholastic exercise with no real philosophical commitment by Pico"
- → Create a Historiographical_Dispute: {scholar_A: Copenhaver, scholar_B: Edelheit, thesis: 4>13, topic: "Pico's philosophical commitment"}

**Output**: `data/ontology/historiographical_disputes/{thesis_id}.json`
```json
{
  "thesis_id": "4>13",
  "disputes": [
    {
      "topic": "Is Pico philosophically committed to this thesis?",
      "position_A": {
        "scholar": "Copenhaver",
        "text": "Pico is attempting a genuine philosophical reconciliation",
        "locator": "On Trial, l. 5753-5757"
      },
      "position_B": {
        "scholar": "Edelheit",
        "text": "Pico is playing with scholastic forms without real commitment",
        "locator": "A Philosopher at the Crossroads, l. 7747-7753"
      }
    }
  ]
}
```

---

## Phase 5: Aggregate and grade historiographical importance (AUDITOR agents)

**Task**: For each thesis, compute a summary score of how central it is to the scholarship.

**Metrics**:
- `historian_mentions`: count of distinct scholars who discuss it
- `mention_density`: average number of mentions per scholar (mentions / scholars)
- `historiographical_importance`: enum (primary / secondary / tertiary / unexamined)
- `importance_justification`: text explaining why (e.g., "condemned thesis; chapter-length treatment by Copenhaver; doctrinal hinge in Thomas-Henry concord debate")
- `disputed_interpretations_count`: how many historiographical disagreements exist?

**Output**: `data/ontology/theses.json`
```json
{
  "theses": [
    {
      "thesis_id": "4>2",
      "historian_mentions": 3,
      "mention_density": 1.5,
      "historiographical_importance": "primary",
      "importance_justification": "Condemned Q6; unique impanation model; Copenhaver ch. 4; extensively annotated by Farmer; source-traced to Quidort and Cabrol",
      "disputed_interpretations_count": 1,
      "connections_count": 8,
      "claims_count": 12
    }
  ]
}
```

---

## Agent swarm structure

```
PHASE 1: HARVESTER SWARM (parallel by scholar)
├─ HARVESTER-SEARCH    [Copenhaver, Wirszubski, Edelheit, ...]  → finds mentions
├─ HARVESTER-EXTRACT   [Copenhaver, Wirszubski, ...]            → context windows
└─ HARVESTER-DEDUPE    [all scholars]                            → de-duplicate

                        ↓ (checkpoints at data/ontology/mentions/by_thesis/)

PHASE 2: EXTRACTOR SWARM (parallel by thesis)
├─ EXTRACTOR-CLAIMS    [4>2, 4>13, 7.2, 11>23, ...]            → atomic facts
└─ CLAIM-LINKER        [all theses]                             → cross-reference claims

                        ↓ (checkpoints at data/ontology/claims/)

PHASE 3: LINKER SWARM (parallel by thesis)
├─ LINKER-PERSONS      [4>2, 4>13, ...]                         → people connections
└─ LINKER-CONCEPTS     [4>2, 4>13, ...]                         → doctrinal concepts

                        ↓ (checkpoints at data/ontology/connections/)

PHASE 4: SYNTHESIZER SWARM (parallel by thesis)
└─ SYNTHESIZER-DISPUTES [4>2, 4>13, ...]                        → historiographical disagreements

                        ↓ (checkpoints at data/ontology/historiographical_disputes/)

PHASE 5: AUDITOR SWARM (serial, one-shot)
└─ AUDITOR-AGGREGATE   [aggregate all phases]                   → theses.json with importance grades

                        ↓ (final output: data/ontology/theses.json)

PHASE 6: WRITER TEMPLATES
└─ WRITER uses ontology fields to auto-populate entry templates with
   - historiographical_context (from disputes + interpretations)
   - importance_grade (from histogram_importance)
   - people/concept connections (from connections list)
   - source-traced claims (from claims list, with locators)
```

---

## Verification gates

**G1-HARVEST**: Every mention has a locator; context windows are 200-500 words; no null fields.

**G2-EXTRACT**: Every claim is linked to a source mention; confidence grades match quotation verbatim-ness.

**G3-LINKER**: Every connection has at least one scholar noting it; connections are grounded in Claims.

**G4-SYNTHESIZER**: Every dispute has two or more scholars; positions are quoted or paraphrased from sources.

**G5-AUDITOR**: Historiographical_importance grades correlate with mention_density (no "primary" theses with <1 mention).

---

## Timeline and checkpoints

- **Week 1**: HARVESTER swarm on 10 scholars (Copenhaver, Wirszubski, Edelheit, Howlett, Black, Allen, Akopyan, Busi, Farmer notes, Dougherty)
  - Output: `data/ontology/mentions/` populated for all 900 theses
  - Gate G1 pass
  
- **Week 2**: EXTRACTOR + LINKER swarms (parallel)
  - Output: `data/ontology/claims/`, `data/ontology/connections/`
  - Gate G2, G3 pass

- **Week 3**: SYNTHESIZER swarm
  - Output: `data/ontology/historiographical_disputes/`
  - Gate G4 pass

- **Week 4**: AUDITOR + WRITER integration
  - Output: `data/ontology/theses.json`, updated entry templates
  - Gate G5 pass
  - WRITER entries auto-populated with historiographical dossiers

---

## Success metrics

- 100% of theses have ≥1 mention (no unexamined theses)
- Average mention_density ≥ 1.5 (each thesis discussed in 1.5+ scholars' works on average)
- ≥50 historiographical disputes identified across 900 theses
- Entry template fields for historiographical_context, connections, importance_grade auto-populate from ontology
- WRITER can cite specific scholar claims with line locators immediately
