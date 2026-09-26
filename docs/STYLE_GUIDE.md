# Style Guide — Pico900

Scholarly standards for all entries: conclusions, commentary, citations, and essays.

Based on Ted Hand's scholarly values and frameworks from `C:\Dev\wiki`, `PicoDB`, and `IslamicateOccultPortal`.

## Core Principles

1. **Provenance First**: Every fact, quotation, interpretation carries explicit source attribution.
2. **No Drift**: Commentary is sourced directly from scholarship or marked as LLM-synthesized with confidence level.
3. **Citation > Summary**: Prefer verbatim quotations over paraphrase; use quotations to build argument.
4. **Accuracy Over Elegance**: Choose clarity and precision over rhetorical flourish.
5. **Transparency**: Mark editorial decisions, uncertainties, and revisions.

## Conclusion Entry Template

```
## Conclusion [ID] — [Latin Incipit]

### Latin Text
[Latin from critical edition, with apparatus if relevant]

### English Translation
[Translation — cite source: existing megabase translation, PicoDB, or "original translation 2026"]

### Exegesis
[1-2 paragraphs of philosophical context and meaning]

### Scholarship & Citations

**Primary Source(s)**:
- [Arabic/Greek/medieval philosopher Pico quotes or references]
  - Source: [Edition/standard reference]

**Scholarly Quotations**:
- **Wirszubski** (*Pico's Encounter with Jewish Mysticism*, p. X): "[quotation]"
  - Relevance: [How this quotation illuminates the conclusion]

- **Copenhaver** (*Pico on Trial*, p. Y): "[quotation]"
  - Relevance: [If heretical, note connection; if scholastic, explain]

- **[Scholar Name]** (*[Work]*, p. Z): "[quotation]"
  - Relevance: [One-sentence connection]

### Commentary [Optional — Ted's Own Notes]
[If Ted provides original commentary, format as:]
- **Ted Hand (2026)**: [Observation or argument]
  - Source: [Session date or reference]

### Tags
[heretical | kabbalah | astrology | magic | metaphysics | logic | theology | soul | intellect | etc.]

### Status
[unstarted | draft | sourced | complete | reviewed]

---
```

## Citation Format

### Direct Quotations

**Scholar** (*Work*, p. X): "[exact quotation, including sic if errors present]"

### Page Ranges

If a quotation spans pages: **Scholar** (*Work*, pp. X–Y): "[quotation]"

### Secondary References

If citing a scholar's citation of another work:
- **Scholar A** citing **Scholar B** (*Work B*): "[quotation]"
  - Original source: [Full citation of Work B if available, or "not consulted"]

### Paraphrases

Avoid paraphrases. If unavoidable, preface with "As Scholar argues:" and cite page.

## Confidence Levels for Scholarship Quotations

Mark each citation with confidence:

- **[VERIFIED]**: Quotation checked against primary source document
- **[CITED]**: Taken from Scholar, not verified against original
- **[INFERRED]**: Synthesized from multiple passages; Scholar not directly quoted

Example:
> **Wirszubski** (*Encounter*, p. 45): "[quotation]" [VERIFIED — checked against PicoDB's Wirszubski scans]

## Heretical Conclusions — Extended Notes

For conclusions flagged as heretical (condemned by Pope Innocent VIII in 1486):

1. **State the charge explicitly**: "Condemned by papal commission as [specific heresy]"
2. **Cite Copenhaver's account**: Quote his analysis of why it was deemed heretical
3. **Note Pico's defense**: If available in *Apology*, cite his rebuttal
4. **Historiographical context**: How do modern scholars view it? (Edelheit, Howlett, Akopyan, etc.)

### Example: Heretical Conclusion Entry

```
## Conclusion [X] — [Heretical Thesis on Unity of Intellect]

### Charge
Condemned by papal commission, 1486, as potentially implying **impersonal immortality** or **denial of individual soul**.

### Pico's Defense (from *Apology*, Q3)
**Pico's own words** [if available]: "[quotation from Apology]"

### Scholarly Analysis

**Copenhaver** (*Pico on Trial*, p. Y): "[quotation explaining why the charge was made]"
- Interpretation: Copenhaver reads this as Pico's syncretism overstepping into dangerous territory.

**Howlett** (*[Work]*, p. Z): "[quotation offering alternative interpretation]"
- Interpretation: Howlett suggests Pico was working within scholastic bounds; the condemnation was political.

### Modern Consensus
[Does modern scholarship view this as truly heretical? As misunderstood? As bold but defensible?]
```

## The "Heretical" Essay — Structure & Standards

Main essay on condemned propositions. Organize by:

1. **Historical Context** (§1)
   - The 1486 trial, Pope Innocent VIII's commission
   - 13 condemned theses
   - Stakes: potential excommunication, exile

2. **Clustered Analysis by Theme** (§2–5)
   - **Incarnation & Divine Embodiment** (Q1, Q2, Q3): metaphysics of God's presence
   - **Eucharist & Transubstantiation** (Q6, Q9, Q10): substance, form, presence
   - **Soul, Intellect & Immortality** (Q4, Q7, Q11): person vs. universal
   - **Kabbalah & Magic** (Q5, others): heterodox knowledge claims
   - **Other Theological Issues** (Q8, Q12, Q13): belief, unity, miracle

3. **For Each Cluster** (§X.1–X.N):
   - **State the theses** (Latin incipit + English)
   - **The charge**: What was theologically suspect?
   - **Copenhaver's reading**: His account of the papal commission's reasoning
   - **Pico's defense** (from *Apology* if available)
   - **Scholarly debate**: What do Howlett, Edelheit, Wirszubski, etc. argue about this?
   - **Conclusion**: Was it heretical? By what standard?

4. **Historiographical Reflection** (Conclusion, §6)
   - The trial as a window into late medieval theology
   - Pico's intellectual ambition vs. doctrinal boundaries
   - How different eras (Renaissance, Enlightenment, 20th century) have *interpreted* Pico

## Quality Checklist for Entries

- [ ] **Latin text is accurate** (compare against critical edition)
- [ ] **Translation is clear and defensible** (cite source)
- [ ] **Every scholarly claim has a quotation backing it** (no unsourced assertions)
- [ ] **Exegesis explains WHY the conclusion matters** (not just what it says)
- [ ] **Tags are consistent** with schema (see `data/schema.json`)
- [ ] **Status field is up-to-date** (draft → sourced → complete → reviewed)
- [ ] **Confidence levels are marked** for all citations
- [ ] **Heretical conclusions have extended notes** (charge, defense, debate)
- [ ] **No unsourced paraphrase** — every secondary idea cites its scholar

## Markdown Formatting

- **Bold**: scholar names, work titles, key concepts
- *Italics*: Latin phrases, foreign words
- `Code`: JSON field names, technical database terms
- > Blockquote: longer quotations (3+ lines)
- [VERIFIED], [CITED], [INFERRED]: confidence tags

## Example Conclusion (Complete)

---

## Conclusion I.1.2 — Anima est forma substantialis corporis

### Latin Text
*Anima est forma substantialis corporis* — commonly attributed to **Conclusiones secundum Aristotelem**, representing Pico's alignment with peripatetic hylomorphism.

### English Translation
"The soul is the substantial form of the body."

Source: Standard scholastic translation; compare Copenhaver *Pico on Trial* p. 103.

### Exegesis
This conclusion affirms the Aristotelian doctrine that the soul is not a separate substance inhabiting the body (Platonism), but rather the *actualization* of matter into a living whole. It is foundational to Pico's metaphysics and his defense against charges of immaterialism or dualism.

### Scholarship & Citations

**Primary Context**: 
- Aristotle, *De Anima II.1*
- Thomas Aquinas, *Summa Theologiae* I, Q75–76

**Scholarly Quotations**:

- **Howlett** (*Pico's Three Paths to the Absolute*, p. 18): "Pico accepts the Aristotelian hylomorphism as the basis for his Platonizing synthesis; the soul animates matter, but retains its capacity for ascent beyond embodiment." [CITED]
  - Relevance: Establishes how Pico uses Aristotle as foundation for Platonic ascent.

- **Edelheit** (*A Philosopher at the Crossroads*, p. 156): "The doctrine of the soul as substantial form was scholastically orthodox, making Pico's broader use of Kabbalah and magic harder to charge as radical materialism." [CITED]
  - Relevance: Historical context—this conclusion is relatively safe, unlike his heretical theses.

### Commentary
None (yet—Ted may add)

### Tags
metaphysics | soul | aristotle | scholasticism

### Status
sourced

---

## Tools for Maintaining Quality

1. **Manifest checkpoint** (`data/conclusions_manifest.json`): Track sourcing status per conclusion
2. **Citation linter** (`scripts/check_citations.py`): Verify every `[VERIFIED]` or `[CITED]` tag has a corresponding quotation
3. **Schema validation** (`scripts/validate_schema.py`): Ensure all tags, status values, confidence levels match allowed values
4. **Heretical essay outline** (`docs/HERETICAL_ESSAY_OUTLINE.md`): Template for organizing condemned propositions

