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
`research-packets/` holds one packet per thesis, the WRITER's sole input (local only — see rule 10 below; regenerate
with `scripts/harvest_mentions.py` + `scripts/build_dossiers.py` if missing). New entries go to `entries/` in the
Farmer-keyed format of `docs/ENTRY_FORMAT.md` and pass `scripts/entry_gate.py`. Session notes:
`RESEARCHNOTES_2026-09-25.md`.

**As of 2026-09-27, `entries/` covers 856 of 900 theses** (833 pass `scripts/entry_gate.py`), with 18 verified
(second-agent-checked and promoted to `entries/<slug>.json`) — all thirteen condemned theses have full commentary,
ten of them verified. Missing: Proclus 24.16-24.55 and nine tier-A commentaries; see `HANDOVER.md` "2026-09-27" for
the exact list and the next steps. `main` is pushed to GitHub as of this date (rule 10: without the corpus text).

## Working mode (Ted's standing instruction; `PROMPTS.md`)

**Do not ask Ted questions.** He is not an engineer and does not want to make engineering calls. Use judgement, record the
decision and its reason in `DECISIONS.md`, and keep going. Do as much work per prompt as is appropriate; proceed through
phases without waiting for "go"; end with a handover a next window can run as a `/goal`. Several windows work on this project
at once: run `git status` first, name the files you own (`scripts/tickets.py`), prefer new files to edits of shared ones,
and never edit a file another window is changing. If something a document promises has not been built, build it. Report
what was verified by running it and what was not; a shape check is not verification.

## Agentic Onboarding: How to Work with Our System Files

Incoming agents (Claude Code, Antigravity, etc.) must operate by this protocol:

1. **Hierarchy of Truth**:
   - **`PROMPTS.md`** is the ultimate authority for user intent. Always run `python scripts/harvest_prompts.py --check` first.
   - **`TICKETS.md`** (`data/tickets/board.json`) is the agile board. Run `python scripts/tickets.py ready` to see what can be worked on. Run `python scripts/tickets.py check` to ensure no conflicting file ownership among active tickets.
   - **`DECISIONS.md`** records all architectural decisions (D-1 through D-23). Review it to understand established principles.
   - **`HANDOVER.md`** is the operational state. Read it to know what the previous session accomplished and where work stopped.
   - **`docs/ORCHESTRATION.md`** defines role contracts (RESEARCHER, WRITER, VERIFIER, LINKER, AUDITOR) and swarm recipes.
   - **`docs/CLAIMS_MODEL.md`** defines the verified claims system for all scholarship.

2. **The 4 Active Development Streams (Interrupted Work Triage)**:
   - **Stream 1: Thesis Entries (`T-ENT-01`, `T-ENT-02`, `T-ENT-03`)**: 118 draft entries in `entries/`. 20 pass `scripts/entry_gate.py`; 98 fail primarily due to translation similarity (>0.85 against Farmer's English; D-13) or missing sentence locators. Next: Remediate the 98 drafts, then launch VERIFIER agents on the 20 passing drafts.
   - **Stream 2: Claims Layer (`T-CLAIMS-02`, `T-CLAIMS-03`, `T-CLAIMS-04`)**: 1,665 claims verified across 14 packets. 13 packets 100% verified. Only 2 claims in `edelheit2022.claims.json` need quote fix. Next: Fix the 2 claims, run semantic verifier (`T-CLAIMS-03`), run LINKER (`T-CLAIMS-04`), run `claims_score.py`.
   - **Stream 3: Intellectual Network (`T-REL-01`)**: Spec and Phase 0 plan ready (`docs/INTELLECTUAL_NETWORK_DESIGN.md`). Next: Implement `scripts/network_bootstrap.py` to generate `data/network/persons.json` from `build_dossiers.py` gazetteer + `data/claims/parties.json`.
   - **Stream 4: Research Companion / PicoDB Integration (`T-SITE-05`)**: 7-tab companion site planned from `C:\dev\PicoDB`. Next: Curate `data/sources.json` with 30–100 word blurbs sortable by tradition.

3. **Deterministic Gates (Quote the Output)**:
   - `python scripts/entry_gate.py` — exits 0 only when translations are original and every sentence has a locator.
   - `python scripts/claims_verify.py` — exits 0 only when every quotation is located verbatim in the OCR corpus.
   - `python scripts/commentary_check.py <file>` — exits 0 only when every claim cited in prose is verified.


## Read first, by task

| task | read |
|---|---|
| **know what Ted has asked for** | **`PROMPTS.md`** (every prompt, verbatim; the source of truth for intent; `python scripts/harvest_prompts.py` keeps it current) |
| see who is doing what, and what is next | `TICKETS.md` (`python scripts/tickets.py ready`) |
| write or review any prose | `docs/EDITORIAL_STANDARD.md`, then `docs/briefs/commentary_writer.md` |
| run agents (roles, gates, swarm recipes) | `docs/ORCHESTRATION.md` (roles, gates, prohibitions, "Swarm recipes") |
| read a scholar, or use what scholars say | `docs/CLAIMS_MODEL.md`; `docs/briefs/claims_researcher.md`; `python scripts/claims_query.py` |
| people and relationships, relevance to Ficino and others | `docs/INTELLECTUAL_NETWORK_DESIGN.md`, `docs/CLAIMS_MODEL.md` s7-8 |
| design or build the website, cards, tours, the Workbench | `docs/SITE_DESIGN.md`, `DEPLOY_STATE.md` |
| angels and the One (commentary, finding aid, Ficino essay) | `docs/angelology/`, `docs/essays/`, `data/claims/` |
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
8. **What a scholar says goes through a verified claim** (`docs/CLAIMS_MODEL.md`). Prose, cards and scores cite claims;
   a claim exists only after `scripts/claims_verify.py` re-found its quotation in the source and a second agent sampled
   its restatement. Never write "Black argues" or "Allen notes" from memory of the book; `scripts/commentary_check.py`
   refuses prose whose citations are dangling, unverified or unquoted.
9. **A gate that a script can pass without opening a source is not a gate.** When you write a check, test it on a
   deliberately wrong input and show it fails. (Shell warning: heredocs in this environment halve backslashes, so a
   regex `\b` becomes a backspace and fails silently; write scripts with the Write tool, not shell heredocs.)
10. **Never commit copyrighted material.** Ted, 2026-09-27, in chat: "don't commit anything copyrighted to the github
    just our digital edition and project and website etc we've been building." `github.com/t3dy/Pico900` is PUBLIC.
    Never `git add` full-text book conversions (`data/corpus/markdown|text|neoplatonism|picodb/`), a generated Latin
    dump derived from them (`data/texts/conclusiones_900_latin.*`), copied external reference pages (`docs/resources/`),
    or the harvester's dossiers that embed hundreds of verbatim scholar excerpts (`research-packets/`,
    `data/ontology/mentions/`) — all are `.gitignore`d; regenerate locally, never restore them to git. A commit that
    slipped 73 MB of this into `main`'s history was found and removed with `git rebase --onto`, not a revert — a
    revert leaves the blobs in history (D-25, D-28/D-41, D-29/D-42). If you ever find a commit like that again, do
    the same: rebase it out before anyone pushes, don't just add a `.gitignore` entry going forward. A short,
    individually attributed quotation inside `entries/*.json` or `data/claims/*.claims.json` is fine (ordinary
    scholarly citation); a directory whose job is to cache hundreds of large excerpts is not.

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
scripts/build_site_v2.py     builds site/ from entries/ (verified as edition text, drafts badged); legacy builder in scripts/legacy/
scripts/seed_inventory.py    writes farmer_structure.json, condemned_thirteen.json, quarantine.json from the audit
scripts/build_corpus_registry.py  data/corpus/registry.json (78 works; locator files; roles)
scripts/extract_farmer_theses.py  data/inventory/theses.json (the 900; gate G0)
scripts/harvest_mentions.py       data/ontology/mentions/**, stats.json, MENTION_STATS.md, connections/farmer_crossrefs.json
scripts/build_dossiers.py         research-packets/*.md, INDEX.md, translation-sheets/, data/ontology/theses.json
scripts/entry_gate.py             gate for entries/*.draft.json (docs/ENTRY_FORMAT.md rules 1-6)
research-packets/            one research packet per thesis (WRITER input); translation-sheets/ for TRANSLATORs
                             .gitignore'd (rule 10): local only, embeds scholar excerpts; regenerate, don't restore
entries/                     Farmer-keyed entries: <slug>.draft.json (WRITER) -> <slug>.json (after VERIFIER); pushed
docs/ENTRY_FORMAT.md  docs/DATA_ONTOLOGY.md  docs/RESEARCH_PROTOCOL.md  docs/exemplars/

PROMPTS.md                   every prompt Ted has typed, verbatim (scripts/harvest_prompts.py); source of truth for intent
TICKETS.md  data/tickets/    the agile board (scripts/tickets.py: one writer per file enforced; `ready` lists what can start)
docs/CLAIMS_MODEL.md         claims, warrants, open questions, importance, relevance to Pico's relationships, the correction loop
docs/SITE_DESIGN.md          cards, frames, colour, sort/filter/search, relational browsing, tours, the Workbench (logins, collections)
docs/briefs/                 cold-start briefs: claims_researcher, claims_semantic_verifier, claims_linker, commentary_writer
data/claims/                 parties.json, topics.json, scoring.json, manifest.json; <domain>/<packet>.claims.json (one owner each),
                             links.json, scores.json, relevance.json, open_questions.json, graph.json; tickets/ (what to fix)
data/verification/claims/    verdicts (script) and semantic verdicts (second agent) per packet
scripts/corpuslib.py corpus_tool.py   find and check text in the OCR corpus (cite work:line)
scripts/claims_verify.py claims_pack.py claims_score.py claims_query.py commentary_check.py   the claims layer
docs/angelology/  docs/essays/       commentary on the angelic material; the Ficino-Pico essay (written from verified claims only)
```

## Related

`C:\Dev\PicoDB` (research portal), `C:\Dev\megabase` (LLM archive), `E:\pdf\renaissance magic\Pico\` (sources),
`C:\Dev\wiki` (workspace knowledge base).
