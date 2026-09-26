# Claude Code Instructions — Pico900

Digital edition of Giovanni Pico della Mirandola's *900 Conclusions* (*Conclusiones 900*) with facing-page Latin (from the critical edition) and English, scholarly commentary from verbatim quotations, and an in-depth "Heretical" essay synthesizing research on the condemned propositions.

## Project Summary

**Live site**: https://t3dy.github.io/Pico900  
**Repository**: https://github.com/t3dy/Pico900  
**Type**: Static digital edition + research portal  
**Status**: Bootstrapping from existing research  

This project is **not** a replacement for `C:\Dev\PicoDB` (the full research portal) or `C:\Dev\megabase` (the LLM conversation archive). Pico900 is a **specific deliverable**: a snazzy, hyperlinked website presenting all 900 conclusions with scholarly apparatus, sourced entirely from existing research, PicoDB infrastructure, and megabase LLM conversations.

## Context Engineering Strategy

The 900 Conclusions are the densest Pico text (895 propositions + editorial material). To work at this scale without exploding context costs:

1. **Source the Latin programmatically.** The critical edition is free at https://cds.lib.brown.edu/cds-project/picos-900-theses. We fetch/parse the full text once, store as JSON.

2. **Find existing translations first.** Megabase contains multiple translation passes (LLM-assisted, scholarly notes). Search before doing new work: grep megabase for "900", "conclusiones", "conclusions", "theses" and harvest all translation artifacts.

3. **Leverage PicoDB's study passes.** PicoDB has 15+ study passes (Kabbalah, astrology, biography, angelology, astrology, etc.). Those study passes created source packets, scholar profiles, and section summaries. Port relevant material into Pico900's commentary and "Heretical" essay.

4. **Commentary is *cited* before *generated*.** For each conclusion, prefer verbatim quotations from scholarship (Wirszubski, Copenhaver, Howlett, Edelheit, Dougherty, Busi, Allen, Akopyan, Black, etc.) over LLM synthesis. Only synthesize after we've exhausted direct quotation.

5. **"Heretical" essay is a synthesis project.** Copenhaver's *Pico on Trial*, the Dougherty anthology, Howlett, Edelheit chapters, and footnotes on the 1486 Rome trial all discuss specific condemned conclusions. Collect those discussions, organize by conclusion number, and write a unified essay pulling them together.

6. **Checkpoint the corpus.** Create `data/conclusions_manifest.json` tracking: conclusion_id, Latin, English, translation_source, commentary_status, scholar_citations_count, heretical_flag. Use this to know what's done and what's not.

## File Structure

```
Pico900/
├── CLAUDE.md                          (this file)
├── DECISIONS.md                       (decisions log)
├── DEPLOY_STATE.md                    (GitHub Pages + repo config)
├── README.md                          (public-facing)
├── data/
│   ├── conclusions_raw.json           (fetched Latin + metadata from critical ed.)
│   ├── conclusions_manifest.json      (checkpoint: ID, source status, commentary status)
│   ├── translations/
│   │   ├── translated_conclusions.json (merged translations from megabase passes)
│   │   └── translation_sources.md     (which megabase convos contributed)
│   └── scholarship/
│       ├── heretical_conclusions.json (conclusions flagged as condemned; sources)
│       ├── scholar_index.json         (Wirszubski, Copenhaver, etc.; their IDs + works)
│       └── citations.json             (conclusion_id → list of source quotations)
├── docs/
│   ├── SOURCING_PROTOCOL.md           (how to find translations in megabase)
│   ├── COMMENTARY_PROTOCOL.md         (when to quote vs synthesize)
│   ├── HERETICAL_ESSAY_PLAN.md        (structure for the condemned-propositions essay)
│   └── PICOLATINDECLARATIONS.md       (reference: text/critical edition notes)
├── scripts/
│   ├── fetch_critical_edition.py      (scrape/parse Latin from Brown)
│   ├── merge_translations.py          (consolidate megabase translation passes)
│   ├── build_site.py                  (generate static HTML from JSON)
│   └── checkpoint_manifest.py         (track progress)
├── src/
│   ├── css/
│   │   └── edition.css                (facing-page layout, scholar highlighting)
│   ├── js/
│   │   └── edition.js                 (vanilla JS for nav, filtering, heretical toggle)
│   └── templates/
│       ├── index.html                 (landing page)
│       ├── conclusion.html            (single-conclusion page with facing text)
│       ├── heretical_essay.html       (long-form essay on condemned propositions)
│       └── about.html                 (documentation)
├── site/                              (generated static HTML, gitignored)
└── .gitignore
```

## Workflow Phases

### Phase 1: Foundation (CURRENT)
- Create folder + CLAUDE.md + DEPLOY_STATE.md ✓
- Search megabase for 900 Conclusions work + translations
- Create `data/conclusions_manifest.json` as checkpoint
- Document sourcing protocol for translations
- Begin collecting scholar citations for ~first 100 conclusions

### Phase 2: Fetch + Merge
- `fetch_critical_edition.py`: grab Latin from Brown critical edition
- `merge_translations.py`: consolidate megabase translations into JSON
- Populate `data/conclusions_raw.json` and `data/translations/translated_conclusions.json`
- Hand-verify first 20 for accuracy

### Phase 3: Commentary + Heretical
- For each conclusion: find 2-3 relevant scholar quotations (Copenhaver, Wirszubski, etc.)
- Populate `data/scholarship/citations.json`
- Extract heretical flags from `data/scholarship/heretical_conclusions.json`
- Begin drafting "Heretical" essay

### Phase 4: Build + Deploy
- `build_site.py`: generate static HTML from JSON
- Test facing-page layout, search, heretical toggle
- Deploy to GitHub Pages

## Research Sources

### Megabase
`C:\Dev\megabase` contains LLM conversation artifacts. Search for:
- "900 conclusions" / "900 theses" / "conclusiones"
- "pico translation"
- "pico heretical" / "pico condemned"
- "pico propositions"

### PicoDB
`C:\Dev\PicoDB` has 15+ study passes with sections on:
- 900 Conclusions structure (Farmer's reading in `docs/PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md`)
- Heretical conclusions (embedded in `artifacts/essays/`)
- Kabbalah, astrology, angelology theses
- Scholar profiles (Copenhaver, Howlett, Wirszubski, etc.)

### Scholarship Library
- **Wirszubski & Kristeller**: *Pico della Mirandola's Encounter with Jewish Mysticism* — Kabbalah theses, 900 structure
- **Copenhaver**: *Pico della Mirandola on Trial* — Heretical conclusions, Rome trial, condemned propositions
- **Dougherty** (ed.): *Pico della Mirandola* anthology — essays on individual works, some on 900
- **Howlett**: Three chapters on concordism, Oration, and 900 structure
- **Edelheit**: Scholastic sources for the 900
- **Black**: Heptaplus hermeneutics (overlaps 900's exegetical theses)
- **Akopyan**: Astrology in the 900 and *Disputationes*
- **Farmer**: The 900 as debate database; oral-disputational logic

### Critical Edition
Free Latin text: https://cds.lib.brown.edu/cds-project/picos-900-theses

### PDF Research Materials
`E:\pdf\renaissance magic\Pico\` contains 73 processed sources (73 Markdown conversions in `E:\pdf\renaissance magic\Pico\Markdown`).

## Key Decisions (log to DECISIONS.md immediately)

- **Latin source**: Brown critical edition (free, reliable)
- **Translation**: Existing megabase work first, supplement as needed
- **Commentary**: Verbatim quotations from scholarship, then LLM synthesis
- **Deployment**: GitHub Pages, static site, vanilla JS
- **Scope**: All 900 eventually; start with highest-research-coverage conclusions

## Operating Constraints

1. **Never commit copyrighted PDFs or full-text scholarly books** to the repo. Use quotations only.
2. **All translations must be sourced** — either cite megabase conversation ID or mark as "original translation by Ted Hand 2026"
3. **"Heretical" essay must cite scholarship directly.** No synthesis without backing quotation.
4. **Commentary status is tracked in `conclusions_manifest.json`.** Update the checkpoint after every major change.
5. **Context engineering**: If a session gets large, split work by conclusion clusters (e.g., 1-100, 101-200, etc.) and checkpoint.

## Related Projects

- `C:\Dev\PicoDB` — Full Pico research portal (15+ study passes, SQLite, 73 sources)
- `C:\Dev\megabase` — LLM conversation archive (translation passes, conceptual work)
- `E:\pdf\renaissance magic\Pico\` — 73 research materials in Markdown

## Links

- Public site: https://t3dy.github.io/Pico900
- Repo: https://github.com/t3dy/Pico900
- Critical edition: https://cds.lib.brown.edu/cds-project/picos-900-theses
