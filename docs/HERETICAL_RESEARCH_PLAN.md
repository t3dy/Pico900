<!-- QUARANTINE-BANNER -->
> **QUARANTINED 2026-09-25: do not cite, quote or build on this file.**  
> audit/A2 found pre-reading hypotheses here later re-issued as quotations (lines 84-85, 117) and misnamed bibliography. Treat every claim as a lead, not a finding.  
> Rewrite from the sources under `docs/ORCHESTRATION.md` (RESEARCHER -> WRITER -> VERIFIER). Evidence in `audit/`.

# Phase 0 Research Plan: Heretical Essay on Condemned Propositions

**Objective**: Research the 13 conclusions condemned by Pope Innocent VIII (1486). Output: essay outline + citation map. Use this as a learning ground to refine the pipeline before scaling to all 900 conclusions.

**Duration**: 1–2 sessions, 150k tokens max.

**Deliverables**:
1. `data/conclusions/Heretical/entry_H.*.json` (13 entries with charge, defense, debate sections)
2. `docs/HERETICAL_ESSAY_OUTLINE.md` (essay organized by theme, with integrated quotations)
3. `docs/PHASE_0_REPORT.md` (retrospective: what worked, what was slow, what to improve)

---

## The 13 Condemned Conclusions

From Copenhaver *Pico on Trial* and papal records. **HARVESTER to extract exactly these**:

The papal commission (1486) condemned 13 theses from the 900 Conclusions. They grouped into themes:

### Incarnation & Divine Embodiment (Q1–Q4)
1. **Q1**: Christ's descent into Hell (bodiless spatiality problem)
2. **Q2**: Related incarnational claim
3. **Q3**: Related incarnational claim  
4. **Q4**: Related (exact theses TBD from Copenhaver source)

### Eucharist & Transubstantiation (Q6, Q9–Q10)
5. **Q6**: Christ's body on altar without annihilation of bread
6. **Q9**: Eucharistic consecration  
7. **Q10**: Eucharistic claim (exact thesis TBD)

### Soul/Intellect/Immortality (Q7, Q11)
8. **Q7**: Soul and immortality (likely touching unity-of-intellect controversy)
9. **Q11**: Related soul claim

### Kabbalah/Magic (Q5)
10. **Q5**: Claim about Kabbalah or magic (Pico's syncretism flagged as heterodox)

### Other Theological Issues (Q8, Q12–Q13)
11. **Q8**: Belief, will, heresy (doxastic voluntarism)
12. **Q12**: Related claim
13. **Q13**: Related claim

**HARVESTER to confirm exact numbers and Latin from Copenhaver's account.**

---

## Research Framework: The Four Pillars

### Pillar 1: The Charge (Papal Commission)
**What Copenhaver shows**: The commission didn't condemn Pico for being a "modernist" or proto-Enlightenment thinker. They condemned him for:
- Proposing metaphysical novelties that contradicted established doctrine
- Using Kabbalah and Arabic philosophy in ways that blurred Christian orthodoxy
- Suggesting alternative epistemologies (prophecy, dream revelation) that bypassed sacramental channels

**How to research**:
- Read Copenhaver *Pico on Trial*, Introduction + Chapter 1
- Extract the exact charge for each conclusion
- Quote the papal commission's reasoning (when available)
- Note: Did they cite precedent (Wyclif, Hus)? Did they invoke specific scholastic authorities?

**Quotations to find**:
- Copenhaver on each Q1–Q13: What was the theological problem?
- Papal documents (if cited in Copenhaver): Direct charge language

### Pillar 2: Pico's Defense (Apology)
**What Copenhaver shows**: Pico's Apology is a scholastic defense, not a humanist retreat. He fights back—technically, textually, with authority-citations.

**How to research**:
- For each condemned conclusion, does Pico offer a defense in the Apology?
- If yes: extract Pico's exact rebuttal language (Latin + English)
- If no: note it (some conclusions Pico may have abandoned)
- Copenhaver's interpretation: Does he think Pico's defense was successful? Evasive? Heretical even by his own admission?

**Quotations to find**:
- Pico's own words from Apology (Questions Q1–Q13)
- Copenhaver's account of Pico's reasoning

### Pillar 3: Modern Historiographical Debate
**What modern scholars say**:

**Copenhaver** (*Pico on Trial*):
- Pico was not a proto-modern humanist but a scholastic metaphysician
- He walked into dangerous theological territory deliberately
- The trial was not persecution; it was a serious theological examination
- Copenhaver emphasizes: Pico's defense was scholastic, technical, mostly orthodox (even if novel)

**Dougherty** (ed., *Pico della Mirandola*):
- Essays on specific works; what does she say about the condemned conclusions?
- Likely: Dougherty contextualizes Pico within Renaissance Platonism and Christian Kabbalah
- Look for: Does she defend Pico's Kabbalah use? Critique it?

**Howlett**:
- Emphasizes concordism and Pico's effort to reconcile traditions
- How does he read the condemned propositions? As concordist moves? As heterodox?
- Does he think Pico overstepped? Or that the commission was wrong to condemn?

**Edelheit**:
- Scholastic sources for Pico; how did medieval theology shape his thinking?
- For heretical conclusions: Where did the problematic ideas come from? Scotus? Ockham? Arabic philosophy?
- Does Edelheit think the heresies were genuine or exaggerated?

**How to research**:
- Read relevant sections of Copenhaver, Dougherty, Howlett, Edelheit
- For each of 13 conclusions: Extract 3–4 quotations showing scholarly debate
- Organize debate: Is there consensus? Or disagreement on interpretation?

**Quotations to find**:
- Copenhaver: How does he frame the charge and defense?
- Dougherty: Does she defend Pico's approach?
- Howlett: How does concordism explain the conclusions?
- Edelheit: What scholastic precedent underlies Pico's thinking?

### Pillar 4: Contextualization (Inquisition, Theology, Politics)
**The larger picture**:
- The 1486 Rome trial happened in a context of theological policing
- Precedents: Wyclif condemned, Hus burned, mysticism under scrutiny
- The papal commission was staffed with Dominicans, Augustinians (orders invested in orthodoxy)
- Gianfrancesco (Pico's nephew) later tampered with Pico's texts; what did he change?

**How to research**:
- Copenhaver on the historical context: What was at stake in 1486?
- PicoDB's MISSING_WRITINGS_ACQUISITION_LOG: Any textual transmission risk on the condemned conclusions?
- How did reception of Pico change after the trial? Was he vindicated or stigmatized?

**Quotations to find**:
- Copenhaver on the inquisitorial context
- PicoDB on Gianfrancesco's edits (did he soften heretical conclusions?)

---

## Source Materials

### Primary Sources
- **Copenhaver *Pico on Trial*** (megabase 2025-07-05 file has Chapter 1 summary; full book in corpus)
  - Read: Introduction, Chapters 1–3 (covers Q1–Q4, Q6–Q10)
  - Extract: Charge + Pico's defense for each Q

- **Pico's *Apology*** (Questions Q1–Q13)
  - Reference in PicoDB if available
  - Copenhaver cites it extensively

### Secondary Sources
- **Dougherty** (ed., *Pico della Mirandola*)
  - Essays on Pico's works; look for heretical-conclusions context
  
- **Howlett** ("Pico's Three Paths to the Absolute" or similar)
  - Concordism + Oration + 900 Conclusions
  - How does he read the condemned theses?

- **Edelheit** (*A Philosopher at the Crossroads* or *Ficino Pico and Savonarola*)
  - Scholastic sources + Pico's formation
  - Why did Pico arrive at these conclusions?

- **PicoDB Study Passes**
  - Study Pass 001–005: General Pico research + Copenhaver notes
  - Study Pass 013–014: Commento (related to heretical trial context)

---

## Phase 0 Workflow

### Step 1: HARVESTER (Extract Condemned Conclusions)
**Agent task**: Extract the 13 condemned conclusions from Copenhaver + PicoDB.

**Input**:
- Copenhaver *Pico on Trial* (megabase 2025-07-05 file)
- PicoDB artifacts on heresy/trial
- Papal records (if available in corpus)

**Output**: `data/staging/stage_heretical.json`
```json
{
  "conclusions": [
    {
      "conclusion_number": "Q1",
      "theme": "Incarnation & Divine Embodiment",
      "latin_incipit": "[Latin from 900 Conclusions or Apology]",
      "english_translation": "[English]",
      "papal_charge": "[Exact charge from commission]",
      "picos_defense": "[Pico's response from Apology if available]",
      "copenhaver_account": "[Copenhaver's interpretation of charge + defense]",
      "source_references": ["Copenhaver p. X", "PicoDB artifact Y"]
    },
    ...
  ]
}
```

**Methodology notes**: Extract verbatim. Don't synthesize or interpret. SYNTHESIZER will do that.

---

### Step 2: PORTER (Standardize Entries)
**Agent task**: Convert to Pico900 format.

**Input**: `data/staging/stage_heretical.json`

**Output**: 13 JSON files in `data/conclusions/Heretical/`
- IDs: `H.1.1` through `H.1.13`
- Status: "sourced" (translations exist; citations TBD)
- Empty fields: `exegesis`, `scholar_citations`, `heretical_notes` (SYNTHESIZER will fill)

---

### Step 3: SYNTHESIZER – Two parallel agents

#### S1: Heretical Conclusions Research
**Agent task**: For each of 13 conclusions, write the "charge, defense, debate" section.

**Input**:
- 13 ported entries
- Copenhaver *Pico on Trial* (full text or key chapters)
- Dougherty + Howlett + Edelheit excerpts
- `docs/HERETICAL_RESEARCH_PLAN.md` (this file)

**Output**: Enhanced entries with:
```json
{
  "heretical_flag": true,
  "heretical_notes": {
    "charge": "Papal commission condemned as [specific heresy] because [reasoning].",
    "defense": "Pico responded: [Apology quote or Copenhaver's account of defense].",
    "modern_debate": {
      "copenhaver": "[Copenhaver's interpretation of charge + whether defense was credible]",
      "dougherty": "[Dougherty's view: was Pico right? Wrong?]",
      "howlett": "[Howlett's concordist reading]",
      "edelheit": "[Edelheit's scholastic context]"
    }
  },
  "scholar_citations": [
    {
      "scholar": "Copenhaver",
      "work": "Pico on Trial",
      "pages": "45-67",
      "quotation": "...",
      "confidence": "VERIFIED or CITED",
      "relevance": "Explains the papal commission's charge and Pico's scholastic defense"
    },
    ...
  ]
}
```

**Confidence levels**:
- `[VERIFIED]`: Checked against Copenhaver's text
- `[CITED]`: Taken from Copenhaver, not independently verified against source
- Mark all clearly

**Heretical_notes sections must include**:
- The exact charge (theological problem)
- Pico's defense (if available)
- Modern scholars' disagreement on whether it was heretical

**Methodology to record**:
- Which sources were most useful?
- Any surprises in the scholarship?
- Did the four pillars (charge, defense, debate, context) work as a framework?

---

#### S2: Heretical Essay Outline
**Agent task**: Draft essay outline organized by theme.

**Input**:
- Enhanced entries from S1
- Research notes from S1 (what scholars said about each conclusion)
- `docs/HERETICAL_RESEARCH_PLAN.md`

**Output**: `docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md`

**Structure** (recommended):
1. **Introduction** (§1): Historical context (1486 trial, Pope Innocent VIII, precedents)
2. **Incarnation & Divine Embodiment** (§2): Q1–Q4, organized by theme
   - Charge: What was the metaphysical problem?
   - Debate: Copenhaver vs. Howlett vs. Edelheit — was Pico heretical or sophisticated?
   - Integrated quotations
3. **Eucharist & Transubstantiation** (§3): Q6, Q9–Q10
4. **Soul/Intellect/Immortality** (§4): Q7, Q11 (likely touches unity-of-intellect controversy)
5. **Kabbalah/Magic** (§5): Q5 (Pico's syncretism; does Dougherty defend it?)
6. **Other Theological Issues** (§6): Q8, Q12–Q13
7. **Historiographical Reflection** (§7): What does the trial reveal about late medieval theology? Was Pico condemned for being too radical or for being misunderstood?

**Methodology to record**:
- How did organizing by theme vs. by order of condemnation change our understanding?
- Did the essay argument emerge from the sources, or did we impose it?
- What's the strongest section? Weakest?

---

### Step 4: REVIEWER (Validate)
**Agent task**: Check entries + essay against STYLE_GUIDE.

**Validation checklist**:
- Every scholarly claim has a **verbatim quotation**
- Confidence levels marked: `[VERIFIED]` or `[CITED]` only
- Heretical conclusions have "charge, defense, debate" sections
- Tags valid
- Exegesis explains WHY the conclusion matters (or note if exegesis is blank awaiting SYNTHESIZER)
- Essay outline is coherent and well-sourced

**Output**: Approval list or revision requests

---

### Step 5: Retrospective & Learning
**What to measure**:
1. **Completeness**: Did we find all 13 condemned conclusions? Any we missed?
2. **Citation accuracy**: Did SYNTHESIZER's quotations check out against sources?
3. **Scholarship coverage**: Did Copenhaver + Dougherty + Howlett + Edelheit provide sufficient debate?
4. **Token efficiency**: Did we stay under 150k? What was expensive?
5. **Methodology**: Did the "charge, defense, debate" framework work? Any refinements?

**Retrospective document** (`docs/PHASE_0_REPORT.md`):
- What worked
- What was slow (which agents/tasks?)
- Surprises (did scholarship agree or disagree?)
- Recommendations for Phase 1 (all 900 conclusions)

---

## Success Criteria

Phase 0 is complete when:
- ✓ All 13 condemned conclusions are identified and extracted
- ✓ Heretical entries have charge + defense + modern debate sections
- ✓ All scholarly citations are verified or clearly marked [CITED]
- ✓ Essay outline is coherent, well-sourced, and ready for Ted to review
- ✓ Retrospective identifies pipeline efficiency gains for Phase 1

If any criterion fails, halt and iterate before scaling to all 900.

