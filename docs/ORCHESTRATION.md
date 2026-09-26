# Orchestration: Pico900 (v2, 2026-09-25)

Inherits `C:\Dev\AGENTS.md` (roles), `C:\Dev\ORCHESTRATION.md` (one writer per file; manifests;
fan out only when the work is wide) and `C:\Dev\CLAUDE.md` (verify before saying "done"). This file
adds only what is specific to a Latin scholarly edition. The v1 pipeline (HARVESTER, PORTER,
SYNTHESIZER, REVIEWER, ticket queues, token budgets) is preserved in `docs/archive/v1-pipeline/`.

## Why v2

v1 reported 929 entries "100% translated, 98% cited, approved." The audit of 2026-09-25
(`audit/`, `COVERAGE.md`) found zero fully sourced entries. Its gates asked *is the field
present and well-formed?* and a generator obliged: `scripts/populate_translations_direct.py` cycles
five canned sentences per section; `scripts/add_scholar_citations.py` writes `"quotation": "[CITATION TO
BE FILLED]"`; three quotations were pasted across 118 Kabbalah entries and marked verified. Every
gate passed, because no gate opened a source. **A metric that can be met without reading the
sources will be met without reading the sources.** The remedy is structural, not exhortatory.

## The unit and the inventory

The unit of work is **one conclusion, identified by its place in Farmer's edition** (*Syncretism in
the West*, MRTS 167, 1998), not by the invented `S1..S9` scheme, whose sections (Zoroaster, Moses,
"Theologos") do not correspond to the structure of the text. The inventory of units is derived
from the edition, one row per printed conclusion, and lives in `data/inventory/`. A section label is an
index, not an inventory: the count of real conclusions comes from the source, never from a target
number. (Same lesson as HPin3D's coverage ledger: gaps hide in whatever index is convenient.)

## Roles

Workspace roles apply as written. Pico900 adds one and sharpens two.

| role | Pico900 contract |
|---|---|
| **RESEARCHER** (v1: HARVESTER) | Reads a *block* of the edition and the scholarship on it. Output: `research-packets/<block>.packet.json`. Every item carries a source and a locator (file, line, page). Latin is transcribed verbatim from Farmer, with the OCR line number. Scholar text is quoted verbatim or not at all. Contradictions between sources are recorded, not resolved. Touches no entry files. |
| **WRITER** (new; v1: SYNTHESIZER) | Writes prose for entries **only from a packet** and only into `entry.draft`. Each factual sentence ends in a locator. Where the packet is silent, the entry says "not established by the sources consulted"; it never fills the gap. May not author a quotation, a page number, a bibliographic title, or a scholar's name that is not in the packet. |
| **VERIFIER** (v1: REVIEWER) | A different agent from the WRITER. Re-locates **every** quotation and every date, name and number in the draft against the source Markdown or PDF; records one verdict per claim (`verbatim / altered / not found / unsupported`). Promotes `draft` to `public` only on a clean pass. Suspects the instrument first: OCR spacing and hyphenation defeat naive search, so normalise before concluding a quotation is absent. |
| **AUDITOR** | Samples every category of writing (entries, essay, angelology, site, governance prose) against the sources and the editorial standard. `audit/` is the model. Run at each block boundary and before any deploy. |
| **BUILDER / DEPLOYER** | As the workspace. The build refuses to render a field graded below `sourced` as edition text (see Gates). One deployer; read `DEPLOY_STATE.md` first. |

## Handover files

RESEARCHER -> `research-packets/<block>.packet.json` -> WRITER -> `entry.draft` -> VERIFIER ->
`entry.public` + `data/verification/<block>.verdicts.json` -> BUILDER. Handovers go through files,
never through conversation. A packet must let an agent start cold.

## Gates

Deterministic gates run first and are not delegated to an agent's judgement.

| gate | check | tool |
|---|---|---|
| **G0 inventory** | Entry count in a block equals the count printed in the edition | `data/inventory/` vs `data/conclusions/` |
| **G1 provenance** | No field of a block is graded `template` or `placeholder`; nothing renders as `sourced` without a locator | `python scripts/integrity_gate.py --verify-quotes --strict` |
| **G2 verification** | 100% of quotations and 100% of dated or numbered claims re-located by a second agent; 20% random sample of the remaining sentences | `data/verification/<block>.verdicts.json` |
| **G3 style** | Mechanical trope counts under threshold, then a read against `docs/EDITORIAL_STANDARD.md` | `python scripts/style_lint.py` (to be written) plus AUDITOR |
| **G4 render** | Build, serve at the real base path, load an actual page, read it as a scholar | DEPLOYER, per workspace rule |

A gate result is quoted, not paraphrased. "Complete" without the command output is not accepted.

## Prohibitions (each one learned from a real failure)

1. **No script writes prose fields.** A generator may carry text forward from a sourced packet. It
   may not contain a translation, charge, defense, exegesis or quotation string of its own. Check:
   `grep -rnE "TEMPLATE|template_|\[CITATION TO BE|NEEDS_TRANSLATION" scripts/` must print nothing.
2. **No shared quotation.** A quotation appearing in more than three entries is a filler signal, and the
   gate grades it `template`.
3. **No entry count without a source.** Do not create stubs to reach a target count (929 entries
   were minted for a 900-thesis work by "section rounding").
4. **Validators certify truth, not shape.** A schema check may not be reported as verification.
5. **No self-approval.** The agent that wrote a field never verifies it, and a rerun of the same
   validator is not a second opinion.
6. **No fabricated exemplars.** Model-voice examples in guides are labelled "pastiche" and never
   attributed to a named scholar as if quoted.

## Parallelism

Parallel by **block of conclusions**, one directory per block, one writer per file.

```
 [R: block A]  [R: block B]  [R: block C]      parallel: separate packets
      v             v             v
 [W: A]        [W: B]        [W: C]            parallel: separate entry dirs
      v             v             v
 [V: A']       [V: B']       [V: C']           a different agent from W, same block, after W finishes
                    v
        integrity_gate  ->  build  ->  AUDITOR sample
```

Never a WRITER and a VERIFIER on one block at once. Never two agents on one entry file.
`COVERAGE.md` and `data/coverage_ledger.json` are generated by one script; nobody hand-edits them.

## Pilot before scale

v1 validated a *format* on 13 entries and then scaled the format. v2 validates *quality*: take one
20-conclusion block through RESEARCHER, WRITER, VERIFIER and AUDITOR; have a scholar (Ted) read
five entries cold; measure the verified-claim rate and the minutes per verified conclusion; only
then plan the sweep. Budgets are set from that measured rate, not from estimates (v1's "~2 hours,
30k tokens" figures were never measured).

## Checkpointing

Progress lives in `data/coverage_ledger.json` (per conclusion, per field, graded) and
`data/blocks_manifest.json` (per block: researcher, writer, verifier, gate results, dates). After
an interruption the recovery step is "run the gate, read the ledger, resume the first block that
has not passed G2."

## Failure modes seen here

| failure | rule that now prevents it |
|---|---|
| Filler translations and citations green-lit by a shape validator | G1 provenance gate; prohibition 1 |
| One quotation reused 118 times and marked verified | prohibition 2; G2 |
| Invented section scheme with invented counts | inventory derived from the edition; prohibition 3 |
| "Approved" by the agent or model that produced the work | prohibition 5 |
| A handover asserting "no further technical work required" | workspace rule: cite gate output, state what is unverified |
| Status-file sprawl (25+ root files, contradictory) | one `HANDOVER.md`, one `PROGRESS` derived from the ledger; dated reports go to `docs/archive/` |
| Model-voice examples that read as real quotations | prohibition 6 |

## The pipeline (v2.1, 2026-09-25): deterministic research, then agents

Everything an agent writes from is produced by scripts that read the sources; no model decides what a
scholar "discusses". Run in this order after any change to the corpus or the parser:

```
python scripts/build_corpus_registry.py    # data/corpus/registry.json: one entry per work, locator file, role
python scripts/extract_farmer_theses.py    # data/inventory/theses.json: the 900 from Farmer's OCR (gate G0)
python scripts/harvest_mentions.py         # data/ontology/mentions/**, stats.json, MENTION_STATS.md, connections/
python scripts/build_dossiers.py           # research-packets/<slug>.md (+INDEX.md, translation-sheets/), data/ontology/theses.json
```

| stage | what it establishes | how it is checked |
|---|---|---|
| inventory | id, Latin, Farmer line, 1486/1487 apparatus, folio, Farmer's English line (pointer), note lines | count = 900 per section; Farmer's marginal cumulative numbers (149 of them) must agree with the derived order; ids inferred from sequence are listed in `extract_report.json` |
| harvest | every place a work cites or quotes a thesis: explicit ids (`4>13`), Copenhaver's `Q4`, Edelheit's "thesis 6" by chapter, Wirszubski's `Conclusio xxiii`, and verbatim Latin (normalised 4-word shingles) | each mention carries `work:line`, the evidence string and a context window; statistics per thesis/work are computed, never written |
| packets | one file per thesis: text, apparatus, Farmer's note excerpts and cross-references, all mentions with context, gazetteer counts, suggested tier | a packet contains nothing without a locator |

**Roles on top of the pipeline.** *TRANSLATOR* (a WRITER restricted to tier-D fields) works from
`research-packets/translation-sheets/T*.md`, one block per agent, and never touches a tier-A thesis.
*WRITER* works from one packet per thesis and writes `entries/<slug>.draft.json` (`docs/ENTRY_FORMAT.md`).
*VERIFIER* runs `python scripts/entry_gate.py` first (locators exist, quotations verbatim, translation not
Farmer's), then re-reads every quoted or dated claim at its locator, then promotes `draft` to `entries/<slug>.json`.
Tiers are suggested by statistics (`data/ontology/theses.json`: A condemned or >=3 works, B >=1, C Farmer only,
D Latin only) and may be overridden by Ted there.

**Why the inventory is the contract.** v1 minted entries to reach a target count (929) without consulting the
source. Farmer prints 900; the parser finds 900 and proves the order against Farmer's own running count. Every entry
corresponds to one row, and every row carries the Farmer line so a VERIFIER can re-derive it.
