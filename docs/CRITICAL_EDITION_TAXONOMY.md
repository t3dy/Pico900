# Critical Edition Taxonomy: Conclusions Organization

**Source**: Farmer's critical edition of *Conclusiones 900* (1998) + Brown critical edition (free online)  
**Purpose**: Map conclusion positions to sections; used by HARVESTER agents for systematic extraction

---

## Section Hierarchy & Priority

### PRIORITY TIER 1: Existing Research (START HERE)

#### S1: Secundum Platonicos (Neoplatonic Philosophy)
- **Count**: 95 conclusions
- **Focus**: Neoplatonic metaphysics, emanationism, the One, the soul's ascent
- **Existing Research**: PicoDB has extensive study pass on Neoplatonism (15+ chapters)
- **Megabase**: Multiple translation passes + essay fragments on Pico's Plotinus synthesis
- **Copenhaver**: *Pico on Trial* chapters on mystical theology (Q13 on soul's union)
- **Priority**: **HIGHEST** — harvest first; rich existing materials to integrate
- **Estimated difficulty**: Medium (good source coverage)

#### S3: Secundum Averroem (Aristotelian Islamic Philosophy — Averroes)
- **Count**: 120 conclusions
- **Focus**: Aristotelian physics, intellect theory, the eternity of the world
- **Existing Research**: PicoDB study pass on Islamic Aristotelianism; megabase translations
- **Copenhaver**: References to Averroist theses condemned in medieval theology
- **Priority**: **HIGH** — substantial existing work
- **Estimated difficulty**: High (technical Aristotelian vocabulary)

#### S4: Secundum Avicennam (Aristotelian Islamic Philosophy — Avicenna)
- **Count**: 105 conclusions
- **Focus**: Aristotelian metaphysics, essence/existence distinction, divine attributes
- **Existing Research**: PicoDB study pass on Avicennan metaphysics; megabase translations
- **Copenhaver**: Implicit in discussions of scholastic synthesis (Thomas drew on Avicenna)
- **Priority**: **HIGH** — parallels S3 but different metaphysical approach
- **Estimated difficulty**: High (essence/existence distinction is technically demanding)

---

### PRIORITY TIER 2: Moderate Research Coverage

#### S2: Secundum Aristotelem (Direct Aristotelian Philosophy)
- **Count**: 110 conclusions
- **Focus**: Aristotle's *Physics*, *Metaphysics*, *Organon* (direct, not mediated through Islamic philosophers)
- **Existing Research**: General Aristotelian background available; less specific Pico work
- **Priority**: **MEDIUM** — foundational but less specialized
- **Estimated difficulty**: Medium

#### S5: Secundum Zoroastrem (Persian & Magian Philosophy)
- **Count**: 80 conclusions
- **Focus**: Zoroastrian dualism, Persian cosmology, astrology, magic
- **Existing Research**: OCCULTIMGDB has Persian source materials; less direct coverage in PicoDB
- **Priority**: **MEDIUM** — specialized sources required
- **Estimated difficulty**: High (Persian sources may be in indirect translation)

#### S6: Secundum Moysem Aegyptium (Egyptian & Hermetic Magic)
- **Count**: 95 conclusions
- **Focus**: Hermeticism, Egyptian magic, divine names, talismanic theory
- **Existing Research**: PicoDB has Hermetic study pass; megabase has translation fragments
- **Priority**: **MEDIUM** — good research base but texts are fragmentary
- **Estimated difficulty**: Medium

---

### PRIORITY TIER 3: Sparse Research Coverage

#### S7: Secundum Hebraeos (Kabbalah & Jewish Philosophy)
- **Count**: 115 conclusions
- **Focus**: Kabbalah (sefirot, divine names), Jewish mysticism, Avraham Abulafia
- **Existing Research**: Wirszubski & Kristeller monograph *Pico's Encounter with Jewish Mysticism*; Copenhaver *Magic and the Dignity of Man*
- **Priority**: **HIGH** (despite sparse coverage) — essential for understanding Pico's syncretism and the "heretical" Q5
- **Estimated difficulty**: Very High (Hebrew sources; limited English translations)

#### S8: Secundum Isaac Narbonensem + Abumaron Babylonium (Medieval Jewish Philosophers)
- **Count**: 8 conclusions (smaller cluster)
- **Focus**: Medieval Jewish Neoplatonism, Kabbalistic philosophy
- **Existing Research**: Specialist secondary literature; limited megabase coverage
- **Priority**: **MEDIUM** — small section; specialized sources
- **Estimated difficulty**: Very High (medieval Hebrew + Arabic sources)

#### S9: Secundum Theologos (Christian Theology & Church Fathers)
- **Count**: 185 conclusions (largest section)
- **Focus**: Christian theology, trinitarian doctrine, Christology, ecclesiology, patristic sources
- **Existing Research**: Copenhaver *Pico on Trial* covers selected conclusions (Q1, Q4, Q6, Q9, Q10, Q13); Dougherty anthology
- **Priority**: **MEDIUM** — saves for later (largest section; can afford to be last)
- **Estimated difficulty**: Medium (well-documented sources)

---

## Phase 1 Dispatch Order (Revised for Priority)

**Recommended order for agent dispatch** (not chronological by section ID, but by research coverage):

| Dispatch Wave | Section | Agents | Priority | Rationale |
|---------------|---------|--------|----------|-----------|
| **Wave 1** (T+0) | S1 (Platonics) | H2 | 1 | Highest research coverage; Neoplatonism extensively documented in PicoDB |
| | S3 (Averroes) | H3 | 1 | Aristotelian Islamic philosophy; good megabase translations |
| | S4 (Avicenna) | H4 | 1 | Parallels S3; rich research base |
| **Wave 2** (T+2h) | S2 (Aristotle) | H5 | 2 | Foundational; can start after Wave 1 |
| | S5 (Zoroastres) | H6 | 2 | Moderate coverage; specialized |
| | S6 (Hermeticism) | H7 | 2 | Good Hermetic research; ready to process |
| **Wave 3** (T+4h) | S7 (Kabbalah) | H8 | 1 (special) | Despite sparse coverage, essential for Pico's syncretism; assign strongest agent |
| **Wave 4** (T+6h) | S8 (Medieval Jewish) | H9 | 3 | Small section; specialized sources; can follow Kabbalah |
| **Wave 5** (T+8h) | S9 (Theology) | H10 | 2 | Largest section; saves for last; Copenhaver provides backbone |

**Note**: Dispatch order prioritizes **by research coverage**, not by section ID. This maximizes efficiency: agents working on well-researched sections finish faster and move to validation sooner.

---

## Incipit Ranges (for Agent Work Tickets)

### S1: Secundum Platonicos (95 conclusions)
**Incipits range**: T1–T95 (or "Secundum Platonicos 1"–"Secundum Platonicos 95")  
**Topics**: Being, Unity, Good, Emanation, Intellect, Soul, Beauty, Providence, Knowledge, Resurrection of the body  
**Key Platonic authorities**: Plato, Plotinus, Porphyry, Pseudo-Dionysius, Macrobius

### S2: Secundum Aristotelem (110 conclusions)
**Incipits range**: T96–T205  
**Topics**: Categories, Substance, Quality, Action, Passion, Prime Mover, Intellect, God, Necessity, Generation  
**Key Aristotelian authorities**: Aristotle (all works), Averroes (as interpreter), Aquinas

### S3: Secundum Averroem (120 conclusions)
**Incipits range**: T206–T325  
**Topics**: Intellect (agent vs. possible), Eternity of the world, God's knowledge, Causation, Physics  
**Key Islamic authorities**: Averroes (Ibn Rushd), Al-Ghazali, Alfarabi  
**Connection to heretical conclusions**: Some S3 theses likely informed Q8 (epistemology of belief)

### S4: Secundum Avicennam (105 conclusions)
**Incipits range**: T326–T430  
**Topics**: Essence/Existence distinction, God's attributes, Divine knowledge, Causation, Metaphysics  
**Key Islamic authorities**: Avicenna (Ibn Sina), Al-Farabi, Ghazali  
**Connection to heretical conclusions**: Metaphysical framework for Q1, Q4 (divine embodiment)

### S5: Secundum Zoroastrem (80 conclusions)
**Incipits range**: T431–T510  
**Topics**: Dualism, Cosmology, Evil, Light/Darkness, Astrology, Magic  
**Key Persian authorities**: Zoroastrian cosmology (via secondary sources), Pseudepigrapha  
**Note**: Direct Persian sources rare; mostly Greco-Roman mediations (Plutarch, Porphyry)

### S6: Secundum Moysem Aegyptium (95 conclusions)
**Incipits range**: T511–T605  
**Topics**: Egyptian theology, Hermeticism, Divine names, Talismanic magic, Alchemy  
**Key Hermetic authorities**: *Corpus Hermeticum*, *Emerald Tablet*, Ficino translations  
**Connection to heretical conclusions**: Informs Q5 (Kabbalah & magic as proof of Christ)

### S7: Secundum Hebraeos (115 conclusions)
**Incipits range**: T606–T720  
**Topics**: Kabbalah, Sefirot, Divine names, Jewish mysticism, Abulafia, Bahir, Zohar traditions  
**Key Kabbalistic authorities**: Zohar, Sepher Bahir, Abulafia commentaries (via Pico's sources)  
**Connection to heretical conclusions**: **DIRECTLY INFORMS Q5** (magic & Kabbalah as proof of Christ)

### S8: Secundum Isaac Narbonensem + Abumaron Babylonium (8 conclusions)
**Incipits range**: T721–T728  
**Topics**: Medieval Jewish Neoplatonism, philosophical theology  
**Key authorities**: Isaac Israeli, Abraham ibn Daud  
**Note**: Small cluster; can follow S7 as natural extension

### S9: Secundum Theologos (185 conclusions)
**Incipits range**: T729–T900 (+ editorial variants)  
**Topics**: Christian theology, Christology, Mariology, Eschatology, Sacraments, Canon Law  
**Key Theological authorities**: Augustine, Thomas Aquinas, Bonaventure, Scotus, Ockham, Church Fathers  
**Connection to heretical conclusions**: **DIRECTLY INFORMS Q1, Q4, Q6, Q9, Q10, Q13** (incarnation, eucharist, soul)

---

## Sources by Section

### S1: Platonics
- [ ] PicoDB `study_neoplatonism.md` (15+ chapters)
- [ ] Megabase: "Pico Plotinus," "Pico emanation," "Pico mysticism"
- [ ] Copenhaver *Pico on Trial* Ch. 5 (Q13 on soul's union)
- [ ] Kristeller *Eight Philosophers of the Italian Renaissance* (Pico chapter on Platonism)

### S3–S4: Islamic Philosophers
- [ ] PicoDB `study_islamic_philosophy.md`
- [ ] Megabase: "Averroes," "Avicenna," "Pico Arabic," "Pico Aristotelianism"
- [ ] Farmer *Syncretism in the West* (Islamic philosophy in medieval Europe)
- [ ] Arnaldez *Islamic Philosophy* (reference)

### S5: Zoroastrianism
- [ ] PicoDB `study_zoroastrianism.md` (limited)
- [ ] OCCULTIMGDB: Persian cosmology manuscripts
- [ ] Plutarch *On Isis and Osiris* (Zoroastrian echoes)
- [ ] Boyce *Zoroastrianism* (reference)

### S6: Hermeticism
- [ ] PicoDB `study_hermeticism.md`
- [ ] Megabase: "Pico Hermes," "Pico Hermetic," "Pico talismans"
- [ ] Ficino *Liber de Sole* (Hermetic Neoplatonism)
- [ ] Copenhaver *Pico on Trial* Ch. 2 (Q5 on magic)

### S7: Kabbalah
- [ ] Wirszubski & Kristeller *Pico's Encounter with Jewish Mysticism* (canonical)
- [ ] Copenhaver *Magic and the Dignity of Man* (Ch. on Kabbalah)
- [ ] PicoDB `study_kabbalah.md`
- [ ] Megabase: "Pico Kabbalah," "Pico Sefirot," "Pico Abulafia"
- [ ] Zohar, Bahir (in English translation, as available)

### S9: Christian Theology
- [ ] Copenhaver *Pico on Trial* (full text; Q1, Q4, Q6, Q9, Q10 especially)
- [ ] Dougherty (ed.) *Pico della Mirandola* anthology
- [ ] Howlett, Edelheit (works on Pico's scholasticism)
- [ ] Medieval theological sources (Aquinas, Scotus, Ockham)

---

## HARVESTER Instructions (Use This)

When dispatching H[n], include this file + the relevant section's incipit range:

```
HARVESTER H[n]:
- Read: CRITICAL_EDITION_TAXONOMY.md (this file)
- Your section: [Section name] ([Incipit range])
- Extract: [Count] conclusions
- Priority sources: [Priority tier sources listed above]
- Output: data/staging/stage_[Section_ID].json

Task: Extract Latin incipits from critical edition. For each:
1. Find Latin in Farmer edition OR Brown edition (free online)
2. Identify 2–3 translations in megabase (search by incipit)
3. Collect 3–4 scholar quotations from PicoDB or provided sources
4. Verify each conclusion against at least one secondary source
5. Output to staging JSON with charge + defense + quotations
```

---

## Verification Checklist (ORCHESTRATOR + REVIEWER)

- [ ] All conclusions from section present in output
- [ ] Latin incipits match critical edition (Farmer or Brown)
- [ ] English translations sourced (megabase or noted as original)
- [ ] Scholar quotations verified or marked [TO_SOURCE]
- [ ] No duplicate entries
- [ ] Charge and defense sections populated
- [ ] Exegesis placeholder ready for next phase
