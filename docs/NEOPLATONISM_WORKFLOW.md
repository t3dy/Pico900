# Neoplatonism Research Workflow for Pico900

End-to-end workflow for researching and commenting on Pico's Neoplatonist theses.

## Phase 1: Discovery — Which Conclusions Are Neoplatonic?

### 1.1 Read the 900 Conclusions with Neoplatonism in Mind

Scan the critical edition (or `data/conclusions_raw.json` once it's populated) for language suggesting Neoplatonism:

- **Emanation**: "emanatio", "procedere", "profluxus" → Plotinus ontology
- **The One**: "Unum", "primum", "fonte", "causa" → henology (Proclus, Plotinus)
- **Intellect/Nous**: "intellectus", "noeticus", "intelligibile" → hypostasis triad
- **Soul**: "anima", "psyche" → Plotinian trichotomy
- **Daemons**: "daemones", "daimones", "mediating spirits" → Porphyry, Apuleius
- **Theurgy**: "theourgia", "theurgic", "sacred operations" → Iamblichus, Chaldean Oracles
- **Divine Names**: "nomina", "divine attributes" → Chaldean Oracles, henads
- **Henads**: "henades", "divine ones" → Proclus, medieval Platonism
- **Triadic structure**: "trias", "proceeding-remaining-returning" → Proclus
- **Mystical Union**: "henosis", "unio mystica" → Plotinus contemplation

### 1.2 Use Existing Resources

Check for existing research:
- **PicoDB**: Read `PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md` for structure and existing annotations
- **Megabase**: Search for "Plotinus", "Porphyry", "Iamblichus", "henads", "theurgy", "emanation"
- **Michael J B Allen's works**: He has written extensively on Pico's Neoplatonism; check bibliography

### 1.3 Mark Candidates

Use the research CLI:
```bash
python scripts/neoplatonism_research.py --status
```

This shows how many conclusions are already mapped. Add a candidate:
```python
from scripts.neoplatonism_research import NeoplatonismResearch

research = NeoplatonismResearch()
research.add_thesis_mapping(
    conclusion_id=123,
    philosophers=["plotinus", "porphyry"],
    status="candidate",
    notes="Language on emanation and soul-matter division"
)
```

## Phase 2: Primary Sourcing — Find the Neoplatonist Text

### 2.1 Identify Which Philosopher(s) Are Relevant

Use the philosophers index:
```bash
python scripts/neoplatonism_research.py --philosopher plotinus
python scripts/neoplatonism_research.py --list-philosophers
```

### 2.2 Locate Key Works in the Archive

For each philosopher, check their archive locations:

| Philosopher | Start Here | Then Check |
|---|---|---|
| **Plotinus** | Michael J B Allen/ | Beierwaltes/ |
| **Porphyry** | Christian Platonism/ | Michael J B Allen/ |
| **Iamblichus** | Iamblichus/ | Chaldean Oracles/ |
| **Proclus** | Michael J B Allen/ | Beierwaltes/ |
| **Chaldean Oracles** | Chaldean Oracles/ | Iamblichus/ |
| **Nicomachus** | Nicomachus/ | Beierwaltes/ |
| **Apuleius** | Apuleis/ | Christian Platonism/ |

### 2.3 Extract the Relevant Passage

**Process**:
1. Open the folder / file
2. Search for key terms (name, concept, work title)
3. If Markdown exists, use it; otherwise extract from PDF with page number
4. Record: philosopher, work, edition/translator, pages, quote snippet

**Example**:
```
Found: Plotinus, Enneads 5.1.1 (Armstrong trans., p. 234-245)
Context: Discussion of the three hypostases (One, Intellect, Soul)
Snippet: "The divine principle remains above... the Intellect proceeds from it..."
```

### 2.4 Update the Thesis Mapping

```python
research.add_primary_source(
    conclusion_id=123,
    philosopher="plotinus",
    work="Enneads 5.1.1 (The Three Hypostases)",
    edition="Armstrong",
    pages="234-245"
)
```

Update status to "primary_sourced".

## Phase 3: Secondary Sourcing — Find Pico Scholarship

### 3.1 Search Michael J B Allen FIRST

Michael J B Allen is *the* expert on Pico and Neoplatonism. Locate his works in:
- `e:\pdf\Neoplatonism\Michael J B Allen\`
- His books: *Neoplatonism and the Platonic Tradition*, *Plato's Third Eye*, etc.

Search for:
- The philosopher you're studying (Plotinus, Porphyry, etc.)
- Your conclusion number (if Pico-focused)
- The concept (henads, emanation, daemons, etc.)

### 3.2 Check Other Key Scholars

- **Copenhaver** (*Pico on Trial*) — especially on condemned propositions
- **Howlett** — concordism and Platonic structure
- **Edelheit** — Scholastic sources
- **Farmer** — oral disputation, 900 as debate
- **Beierwaltes** — medieval transmission

### 3.3 Extract Quotations

Find passages where the scholar discusses Pico's use of the Neoplatonist source. Example:

> "Pico's emissio intelligibilis follows Plotinus's doctrine of emanation from the One, mediated through the Platonic Intellect. This appears explicitly in Conclusions II.i.1-14, where Pico asserts that all procession derives from a single principle." — Michael J B Allen, *Neoplatonism and the Platonic Tradition*, p. 78.

Record:
- Author, work, page
- Whether the scholar explicitly connects it to Pico's conclusion number
- The quotation (short phrase or sentence, not full paragraphs)

### 3.4 Update the Thesis Mapping

```python
research.add_scholarship(
    conclusion_id=123,
    author="Michael J B Allen",
    work="Neoplatonism and the Platonic Tradition",
    chapter="Pico's Plotinus",
    pages="45-78"
)
```

Update status to "scholarship_added" or "commentary_ready" if complete.

## Phase 4: Commentary Writing

### 4.1 Structure

Each thesis commentary should include:

1. **Neoplatonist Source(s)**: 
   - "Pico relies here on Plotinus's doctrine of emanation..." 
   - Citation: Plotinus, *Enneads* 5.1.1 (Armstrong trans., p. 234).

2. **Historical Context**:
   - When/where this idea appears in Neoplatonism
   - How it evolved (Porphyry vs. Iamblichus vs. Proclus)

3. **Pico's Synthesis**:
   - How Pico adapts it (if at all)
   - Whether it's harmonized with other traditions (Kabbalah, Aquinas, etc.)
   - Scholar citation: Michael J B Allen argues that...

4. **Heretical Flag** (if applicable):
   - Was this conclusion condemned?
   - Is the Neoplatonic source itself controversial?

### 4.2 Citation Format

**Primary Neoplatonist source**:
```
Plotinus. *Enneads* 5.1.1. Trans. Armstrong, vol. 3, p. 234.
```

**Secondary scholarship**:
```
Michael J B Allen, *Neoplatonism and the Platonic Tradition* (Cambridge: Harvard University Press, 1994), p. 78.
```

**Pico's conclusion**:
```
Pico, *Conclusions*, II.i.1.
```

## Phase 5: Checkpoint & Progress Tracking

### 5.1 Update the Manifest

After each cluster of conclusions (e.g., 1-50, 51-100), run:

```bash
python scripts/neoplatonism_research.py --status
```

This shows:
- How many conclusions mapped to each philosopher
- Progress across status levels
- Research gaps

### 5.2 Log Decisions

In `DECISIONS.md`, record:
- Which conclusions you've prioritized for Neoplatonism research
- Any new insights about Pico's Neoplatonism synthesis
- Archive resources that proved most valuable
- Scholar recommendations for future researchers

## Tips & Gotchas

### Tip 1: Emanation vs. Creation
Pico often merges Neoplatonic emanation with Aquinas's Christian creation ex nihilo. When you see "emanatio" or similar, check whether Pico explicitly reconciles the two or treats them as compatible. Allen writes extensively on this.

### Tip 2: Henads as Divine Names
In later Neoplatonism (Iamblichus, Proclus), the henads are individual divine manifestations. This maps to Kabbalah's Sephiroth and to the divine names in the *Chaldean Oracles*. When you see a thesis on divine names, it's likely invoking both traditions.

### Tip 3: Theurgy is Controversial
Several of Pico's theurgic theses were condemned by Rome (1486). If you're researching theurgy, check `data/staging/stage_heretical.json` and `HERETICAL_RESEARCH_PLAN.md` for overlap.

### Tip 4: Proclus Dominates Medieval Reception
Proclus's *Elements of Theology* was THE systematic Neoplatonic text for medieval scholasticism (often in Latin translation). When a Pico thesis echoes Neoplatonic structure but arrives via Aquinas, Proclus is usually the common ancestor.

### Tip 5: Check Ficino
Ficino (*Theologia Platonica*) translated and commented on Plotinus. Pico likely knew Ficino's work. When you find a Plotinian reference in Pico, check whether Ficino mediated it or whether Pico went directly to the source.

## Workflow Checklist

For each cluster of conclusions:

- [ ] **Discovery**: Read conclusions, mark Neoplatonism candidates
- [ ] **Archive**: Identify relevant philosophers from candidates
- [ ] **Primary**: Extract primary Neoplatonist sources from archive
- [ ] **Secondary**: Find Michael J B Allen and other scholars on Pico
- [ ] **Commentary**: Draft commentary with citations
- [ ] **Heretical**: Check if any are condemned propositions
- [ ] **Checkpoint**: Update manifest, log decisions
- [ ] **Report**: Run `neoplatonism_research.py --status`

## Related Documents

- `NEOPLATONISM_SOURCING_PROTOCOL.md` — Full sourcing rules
- `data/neoplatonism/philosophers_index.json` — Metadata on philosophers
- `data/neoplatonism/archive_inventory.json` — Archive structure
- `HERETICAL_RESEARCH_PLAN.md` — For conclusions flagged as condemned
- `DECISIONS.md` — Log major decisions here
