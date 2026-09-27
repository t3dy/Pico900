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

## The claims layer and swarm recipes (v2.2, 2026-09-26)

Added in response to `PROMPTS.md` P20260926041129, P20260926041326 and P20260926041711. **`PROMPTS.md` is the source of
intent; `TICKETS.md` (`python scripts/tickets.py`) is the board; `docs/CLAIMS_MODEL.md` is the scholarship layer.**
Ted's working mode is in `CLAUDE.md` ("Do not ask Ted questions"): the orchestrator decides, records, and continues.

**Start of every session (2 minutes).** `git status` (who else is writing); `python scripts/harvest_prompts.py` (new
prompts); `python scripts/tickets.py ready` and `check` (what can start, and that no two `doing` tickets own one file);
read the newest `HANDOVER.md`. Move the ticket you take to `doing` with your file list; move it to `done` only with the
gate output in `--note`.

**Roles added by the claims layer** (each has a cold-start brief in `docs/briefs/`):

| role | contract | owns | brief |
|---|---|---|---|
| RESEARCHER (claims) | reads one range of one scholar; writes claims with verbatim quotations, warrants, open questions, hedges, relationship tags | `data/claims/_work/<packet>.*`, `<domain>/<packet>.claims.json` | `claims_researcher.md` |
| VERIFIER (mechanical) | `scripts/claims_verify.py`: re-finds every quotation, warrant and locator; tickets carry the nearest real text; repairs wrong line numbers | `data/verification/claims/*.verdicts.json`, `data/claims/tickets/` | (script) |
| VERIFIER (semantic) | a different agent judges a 20% sample: does the restatement overreach its quotations? verdicts bind by content hash | `<packet>.semantic.json` | `claims_semantic_verifier.md` |
| LINKER | links claims across scholars (same, supports, contradicts, qualifies, depends on, cites), each with a stated basis; lists disputes | `<domain>/links.json` | `claims_linker.md` |
| SCORER | `scripts/claims_score.py`: importance, tiers, relevance to Pico's relationships, open questions, graph | `scores.json`, `relevance.json`, `open_questions.json`, `graph.json` | (script) |
| WRITER (from claims) | composes commentary and essays only from verified claims; `[[id]]` citations; `commentary_check.py` gate | its one output file | `commentary_writer.md` |

**Gates for the claims layer** (quote the output): C1 `python scripts/claims_verify.py` prints `TOTAL needs_fix: 0`;
C2 semantic reading: no `overreaches`/`wrong` outstanding, edited claims re-judged (bump `revision`), and every claim a writer cites has a current `supported` verdict (measured overreach rate 7-15%, so a random sample is not enough for cited claims: use `claims_sheet.py --from-commentary`); C3 `python scripts/claims_score.py`
prints links rejected 0; C4 `python scripts/commentary_check.py FILE` exits 0; C5 for anything rendered: the page loaded and read.

**Swarm recipe: the claims sweep (used 2026-09-26 for angelology and the Ficino dispute; 14 researchers, ~1,400 claims).**
1. Write the manifest first (`data/claims/manifest.json`: item, owner, scope, status). One packet per researcher: ranges
   of a big book split by line, chapters of an edited volume by essay, and never two agents on one packet.
2. Give each agent its **assignment** (work key, line range, topics, leads *to be verified*, output path) and the shared
   brief; nothing else. State leads as leads: the audit's line numbers were right, its characterisations sometimes not.
3. Launch all in parallel (they share no file). Agents write JSONL incrementally and run `claims_pack.py` themselves; the
   script, not the agent, decides whether a quotation is real.
4. When all packets show `needs_fix 0`: launch the semantic VERIFIERs (group 3-4 packets per agent, different agents
   from the researchers), then apply `suggested_text` through the packet owners, re-run `claims_verify.py`, re-sample edited claims.
5. Launch the LINKER (one agent, or one per topic group writing separate `*.links.json` files), then `claims_score.py`.
6. Only now launch WRITERs, one per output file, each with the commentary brief and a topic list. A second agent samples
   each written section against its claims. Update the manifest and tickets after each stage.
7. What a swarm of this size showed: agents given a verifier they cannot argue with produce 99% verbatim quotations; the residual
   risk is semantic (restatements that add a name the quotation lacks), which is why stage 4 exists and why
   `ungrounded_entity` warnings are leads for it.

**Swarm recipe: thesis entries** (as in the pipeline above): TRANSLATOR blocks and WRITERs by thesis block, one entry file each,
VERIFIER after; use `research-packets/` as input and `scripts/entry_gate.py` as the gate. **Swarm recipe: site and cards:** DESIGNER
(`docs/SITE_DESIGN.md`) -> BUILDER per file owner -> VERIFIER drives the built page at the real base path -> DEPLOYER.

**Relationship data.** Claims that bear on a relationship (`bears_on`) are the evidence for the network system
(`docs/INTELLECTUAL_NETWORK_DESIGN.md`); person ids come from `data/network/persons.json` once it exists (ticket T-REL-01);
`data/claims/parties.json` is the seed. Relevance of every card to every party is computed (`docs/CLAIMS_MODEL.md` s7-8), never typed.
