# Claude Code Instructions: Pico900

A scholarly digital edition of Giovanni Pico della Mirandola's *Conclusiones* (the *900 Theses*, Rome,
7 December 1486): Latin and English, with commentary at the standard of a good monograph, that lets a
reader recover the historical context and the philosophical depth of each thesis, and the trial that
condemned thirteen of them. Inherits `C:\Dev\CLAUDE.md`, `C:\Dev\AGENTS.md` and `C:\Dev\ORCHESTRATION.md`.

## State, 2026-09-25 (read this before believing any other status file)

An audit (`audit/A1`-`A4`) found that the earlier reports of "929 entries, 100% translated, 98% cited,
approved, ready to deploy" were false. **0 of 929 entries are fully sourced.** About 143 rows hold any
real text; the other ~775 are generated filler that has been withdrawn from the site. The site is
**not live** (`DEPLOY_STATE.md`). What is solid: the source corpus, the true structure of the work
(`data/inventory/farmer_structure.json`), the reconciliation of the thirteen condemned theses
(`data/inventory/condemned_thirteen.json`), the audit reports, and the tooling below.

Run `python scripts/integrity_gate.py --verify-quotes` for the live picture of the legacy entries (`COVERAGE.md`).

**Since the evening of 2026-09-25 the research layer exists** (`docs/ORCHESTRATION.md`, "The pipeline"):
`data/inventory/theses.json` holds all 900 theses from Farmer with line locators (validated against Farmer's own
running count); `data/ontology/` holds every scholarly mention of every thesis, harvested deterministically from 78
works, with statistics (`MENTION_STATS.md`: 421 theses cited by at least one scholar, 63 by three or more); and
`research-packets/` holds one packet per thesis, the WRITER's sole input. New entries go to `entries/` in the
Farmer-keyed format of `docs/ENTRY_FORMAT.md` and pass `scripts/entry_gate.py`. Session notes:
`RESEARCHNOTES_2026-09-25.md`.

## Read first, by task

| task | read |
|---|---|
| write or review any prose | `docs/EDITORIAL_STANDARD.md` |
| run agents | `docs/ORCHESTRATION.md` (roles, gates, prohibitions) |
| touch data | `data/inventory/`, `data/quarantine.json`, `COVERAGE.md` |
| build or publish | `DEPLOY_STATE.md`, then `scripts/predeploy_check.py` |
| know what is wrong and why | `audit/` |
| current handover | `HANDOVER.md` |

Older status, handover and phase files are in `docs/archive/`. They are history, not instructions.

## Ground truth and where it is

- **Structure and Latin/English of all 900 theses**: Farmer, *Syncretism in the West: Pico's 900 Theses
  (1486)* (Tempe: MRTS 167, 1998), Markdown at `E:\pdf\renaissance magic\Pico\Markdown\Stephen_A_Farmer_*c99b971b.md`
  (~30k lines; cite by line, e.g. `F:21444`). Its English is in copyright: do not reproduce it.
- **The trial**: Copenhaver, *Pico della Mirandola on Trial: Heresy, Freedom, and Philosophy* (Oxford UP, 2022);
  Fornaciari's edition of the *Apologia* (2010; only front matter and contents survive in the corpus).
- Also in the corpus (73 Markdown files): Copenhaver, *Magic and the Dignity of Man* (Harvard UP, 2019);
  Wirszubski, *Pico's Encounter with Jewish Mysticism*; Edelheit, *A Philosopher at the Crossroads* (Brill, 2022);
  Sophia Howlett, *Re-evaluating Pico* (Palgrave Macmillan, 2021); M. V. Dougherty (ed.), *Pico della Mirandola:
  New Essays* (CUP, 2008); Crofton Black, *Pico's Heptaplus and Biblical Hermeneutics* (Brill, 2006); Allen, Akopyan, Busi and others.
- PicoDB (`C:\Dev\PicoDB`) and megabase (`C:\Dev\megabase`) are *leads*, never evidence: a megabase summary is
  an LLM's memory of a book. Open the book. The Markdown is OCR: search with short fragments and tolerate
  hyphenation and double spaces.

## Non-negotiable rules (each is a scar)

1. **Never invent text.** No translation, Latin, charge, defense, exegesis, quotation, page number or
   bibliographic detail is written unless it comes from a source you opened. Say "not established by the
   sources consulted" instead. Prior agents filled fields to hit a count; that is the failure to avoid.
2. **No script writes prose.** Generators carry sourced text forward; they contain no template sentences.
3. **No self-approval.** The agent that wrote a field never verifies it. Verification means re-finding the quotation
   or fact in the source, not re-running a schema validator.
4. **Quote gate.** No quotation is stored until located verbatim; record file and line. An introduction is not by the
   author of the volume it introduces.
5. **Dates.** Published 7 Dec 1486 (colophon, F:28040); commission Feb-Mar 1487; bull of 4 Aug 1487. "Condemned by
   papal bull (1486)" is wrong wherever it appears.
6. **Verify before "done"** (workspace rule): quote gate output, load the built page, state what is unverified.
7. **Never publish from `docs/`**, and never deploy without `DEPLOY_STATE.md` and `predeploy_check.py`.

## Files known to contain unverified or invented material; do not cite or imitate

`docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md` and `data/conclusions/Heretical/S1_RESEARCH_NOTES.md` (none of the
scholar quotations in them is verbatim), the S7 `scholar_citations` (3 strings reused), the `S4` "Farmer"
quotations, all `template_*`/`pending_*` fields, and the archived v1 style guides' "model voice" paragraphs.
Consult `audit/` before reusing anything from the pre-audit pipeline.

## Layout

```
CLAUDE.md  HANDOVER.md  DECISIONS.md  DEPLOY_STATE.md  README.md  COVERAGE.md (generated)
audit/                       A1-A4 audit reports (the evidence for everything above)
data/inventory/              farmer_structure.json, condemned_thirteen.json (the real 900)
data/quarantine.json         fields proven wrong; never rendered
data/conclusions/<S#|Heretical>/entry_*.json   legacy entries (mostly filler; being replaced by Farmer-keyed entries)
data/coverage_ledger.json    generated by integrity_gate.py
docs/EDITORIAL_STANDARD.md  docs/ORCHESTRATION.md  docs/archive/
scripts/integrity_gate.py    provenance grades, coverage ledger, quote verification (legacy entries)
scripts/style_lint.py        mechanical AI-prose markers
scripts/predeploy_check.py   DEPLOYER's gate for site/
scripts/build_html_site.py   builds site/ from the legacy entries (to be re-pointed at entries/)
scripts/seed_inventory.py    writes farmer_structure.json, condemned_thirteen.json, quarantine.json from the audit
scripts/build_corpus_registry.py  data/corpus/registry.json (78 works; locator files; roles)
scripts/extract_farmer_theses.py  data/inventory/theses.json (the 900; gate G0)
scripts/harvest_mentions.py       data/ontology/mentions/**, stats.json, MENTION_STATS.md, connections/farmer_crossrefs.json
scripts/build_dossiers.py         research-packets/*.md, INDEX.md, translation-sheets/, data/ontology/theses.json
scripts/entry_gate.py             gate for entries/*.draft.json (docs/ENTRY_FORMAT.md rules 1-6)
research-packets/            one research packet per thesis (WRITER input); translation-sheets/ for TRANSLATORs
entries/                     Farmer-keyed entries: <slug>.draft.json (WRITER) -> <slug>.json (after VERIFIER)
docs/ENTRY_FORMAT.md  docs/DATA_ONTOLOGY.md  docs/RESEARCH_PROTOCOL.md  docs/exemplars/
```

## Related

`C:\Dev\PicoDB` (research portal), `C:\Dev\megabase` (LLM archive), `E:\pdf\renaissance magic\Pico\` (sources),
`C:\Dev\wiki` (workspace knowledge base).
