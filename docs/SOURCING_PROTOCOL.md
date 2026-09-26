# Sourcing Protocol — Pico900

How to find translations, scholarship, and existing work for the 900 Conclusions.

## Megabase Translation Passes (Priority 1)

### Existing Work — FOUND

**File**: `C:\Dev\megabase\chats_2025\2025-07-04_Pico 900 Conclusions Exegesis.md`

Contains **detailed translations and philosophical exegeses** of multiple sections:

- **Conclusiones secundum Adelandum Arabem** (8 conclusions + exegesis)
- **Conclusiones secundum Abucaten Avenan** (10 conclusions + exegesis)  
- **Conclusiones secundum Averroem** (41 conclusions + exegesis)
- **Conclusiones secundum Avicennam** (12 conclusions + exegesis)
- **Conclusiones secundum Alfarabium** (11 conclusions + exegesis)
- **Conclusiones secundum Moysem Aegyptium** (3 conclusions + exegesis)
- **Conclusiones secundum Isaac Narbonensem** (4 conclusions)
- **Conclusiones secundum Abumaron Babylonium** (4 conclusions)

**Status**: HARVEST FOR PICO900

Each section includes:
- Annotated Latin text (from Pico's original)
- English translation
- Detailed philosophical exegesis
- Connection to Arabic sources (al-Farabi, Avicenna, Averroes, etc.)
- References to Liana Saif's work on Arabic influences

**File**: `C:\Dev\megabase\chats_2025\2025-07-05_Pico della Mirandola Summary.md`

Contains:
- **Chapter-by-chapter summary** of Brian P. Copenhaver's *Pico on Trial: Heresy, Freedom, and Philosophy*
- Introduction + Chapter 1 summaries (more chapters may follow in the file)
- Heavy focus on the 13 condemned theses and their theological/scholastic context
- Key for understanding the "Heretical" essay

**Status**: HARVEST FOR HERETICAL ESSAY

### How to Search Megabase

```bash
# Search for all Pico-related conversations
grep -r "pico\|900.*conclus\|conclus.*900" C:\Dev\megabase --include="*.md" -i

# Specific searches
grep -l "900 conclusions\|900 theses" C:\Dev\megabase/chats_2025/*.md
grep -l "heretical\|condemned" C:\Dev\megabase/chats_2025/*.md
```

## PicoDB Study Passes (Priority 2)

`C:\Dev\PicoDB` contains 15+ study passes with material relevant to 900 Conclusions:

### Key Resources

- **docs/PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md** — notes on 900 Conclusions structure, especially Farmer's reading
- **docs/KABBALAH_READING_PROTOCOL.md** — Kabbalah-related conclusions (Wirszubski, Busi guidance)
- **docs/ASTROLOGY_READING_PROTOCOL.md** — astrology conclusions (Akopyan guidance)
- **docs/ANGELOLOGY_READING_PROTOCOL.md** — angelology conclusions
- **artifacts/essays/** — Longform syntheses on specific topics (Kabbalah, astrology, biography, angelology)
- **artifacts/source_packets/** — Source packets for scholars (Copenhaver, Howlett, Wirszubski, etc.)

### For Heretical Essay

- **docs/MISSING_WRITINGS_ACQUISITION_LOG.md** — notes on textual transmission risk (Gianfrancesco tampering)
- **Study Pass 002** coverage of Copenhaver's *Pico on Trial*
- Cross-references in artifact essays on heresy, trial, scholasticism

## Renaissance Magic PDF Corpus (Priority 3)

**Location**: `E:\pdf\renaissance magic\Pico\`

73 research sources, all converted to Markdown:

- `E:\pdf\renaissance magic\Pico\Markdown\` — Full-text conversions
- `E:\pdf\renaissance magic\Pico\data\` — Manifest, ontology, corpus catalog
- `E:\pdf\renaissance magic\Pico\db\` — SQLite database

### Key Scholarship

From the corpus (check the file list in `E:\pdf\renaissance magic\Pico\`):

1. **Wirszubski & Kristeller** — *Pico della Mirandola's Encounter with Jewish Mysticism*
   - Essential for Kabbalah conclusions
   - Primary source control for 900 theses on Hebrew learning and Kabbalah

2. **Copenhaver** — *Pico della Mirandola on Trial* (also in megabase summary)
   - Essential for Heretical essay
   - 13 condemned conclusions with theological/scholastic context

3. **Howlett** — *Three chapters on concordism, Oration, and 900 structure*
   - Overall structure and argumentative logic of the 900

4. **Edelheit** — *Scholastic sources for the 900* (also in PicoDB)
   - Medieval philosophical background

5. **Dougherty** (ed.) — *Pico della Mirandola* anthology
   - Essays on individual works, some specific conclusions

6. **Akopyan** — *Astrology in the 900 and Disputationes*
   - Developmental chronology of Pico's views on astrology

7. **Allen** — *Studies in the Platonism of Ficino and Pico*
   - Pico-Ficino relation (especially in 900's metaphysics)

8. **Black** — *Heptaplus hermeneutics* (overlaps with 900's exegetical theses)
   - Biblical hermeneutics framework

## Critical Edition (Free Online)

**Source**: https://cds.lib.brown.edu/cds-project/picos-900-theses

- Full Latin text of the 900 Conclusions
- Apparatus criticus
- Digital humanities interface for browsing

**Workflow**:
1. Fetch the Latin text from Brown critical edition
2. Match against existing translations in megabase
3. Supplement with new translations as needed

## How to Track Sourcing

Create `data/conclusions_manifest.json` with this structure:

```json
{
  "conclusion_id": "I.1.1",
  "section": "Conclusiones secundum Avicennam",
  "latin_source": "critical_edition | megabase | picodb",
  "latin_verified": true,
  "english_translation": {
    "text": "...",
    "source": "2025-07-04_Pico 900 Conclusions Exegesis.md | original_2026",
    "translator": "LLM | Ted Hand"
  },
  "commentary_status": "unstarted | draft | sourced_quotations | complete",
  "scholar_citations": [
    {
      "scholar": "Wirszubski",
      "work": "Pico della Mirandola's Encounter with Jewish Mysticism",
      "pages": "45-47",
      "quotation": "...",
      "verified": false
    }
  ],
  "heretical_flag": false,
  "tags": ["kabbalah", "hebrew", "mysticism"],
  "notes": ""
}
```

## Workflow by Section

### Conclusiones secundum Adelandum Arabem (8 conclusions)

- ✓ Translations + exegesis in megabase (2025-07-04)
- [ ] Verify translations against critical edition
- [ ] Find scholar citations (Wirszubski, Akopyan, Copenhaver)
- [ ] Determine if any are heretical (check Copenhaver)

### Conclusiones secundum Averroem (41 conclusions)

- ✓ Extensive exegesis in megabase (2025-07-04)
- [ ] This is a large section — split into 5-conclusion chunks for context efficiency
- [ ] Priority: conclusions about intellect, soul, causality
- [ ] Heretical check: references to unified intellect

### Conclusiones secundum Avicennam (12 conclusions)

- ✓ Translations + exegesis in megabase (2025-07-04)
- [ ] This section deals with logic, essence, substance — less likely to be heretical
- [ ] Scholar citations: Edelheit (scholasticism), Allen (Ficino comparison)

### Conclusiones secundum Alfarabium (11 conclusions)

- ✓ Translations + exegesis in megabase (2025-07-04)
- [ ] Logic, demonstration, species — technical and philosophical
- [ ] Less heretical risk; focus on clarity and elegance of argument

### Conclusiones secundum Moysem Aegyptium (3 conclusions)

- ✓ Exegesis in megabase (2025-07-04)
- [ ] Hermetic-Platonic critique of Aristotle
- [ ] Likely heretical regarding causality and divine nature — check Copenhaver

## Search Strategy for Remaining Sections

Remaining sections of the 900 Conclusions (beyond the ~100 already exegeted in megabase):

1. **Christian Kabbalah conclusions** — search megabase for "kabbalah" + "900"
2. **Heretical conclusions** — search for "condemned" + "heretical" + Copenhaver references
3. **Magic and astrology conclusions** — search for "magic" + "astrology" + "900"
4. **Soul and intellect conclusions** — search for "intellect" + "agent intellect" + "soul"

### Megabase Search Command

```bash
find C:\Dev\megabase -name "*.md" -type f -exec grep -l "pico\|conclus" {} \; | xargs grep -l "900\|theses"
```

## External Resources

- **Scryfall bulk data** — MTG encyclopedia (not directly relevant to 900, but used in MTGSLIDER pattern)
- **Emerald Tablet DB** — Hermetic texts (adjacent to Pico's Hermeticism)
- **Witcher Portal** — DH pattern reference for provenance model

## Next Steps

1. **Month 1**: Harvest existing translations from megabase; verify against critical edition; document sourcing
2. **Month 2**: Extract heretical conclusions from Copenhaver; begin essay outline
3. **Month 3**: Research commentary for remaining sections; balance quotation + LLM synthesis
4. **Month 4**: Build website; deploy to GitHub Pages

