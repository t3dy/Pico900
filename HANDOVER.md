# Handover: Pico900 (Updated 2026-09-26 — Multi-Window State & Agentic Recovery Guide)

Read `CLAUDE.md` first, then `PROMPTS.md` (source of truth for Ted's intent) and `TICKETS.md`.
This handover synthesizes the state across all Claude Code windows (`window-8857d983`, `window-3bc261ff`, `window-a08fd9b0`, `window-2f4b7fcd`) following session limit interruptions, and provides an immediate operational guide for incoming agentic coding assistants.

---

## 1. Executive Summary & Repository State

- **Copy-text & Inventory**: 900 theses extracted deterministically from Farmer's 1998 critical edition OCR (`data/inventory/theses.json`). Validated against Farmer's 149 marginal cumulative counts.
- **Deterministic Harvest**: Mentions harvested from 78 scholarly works across 421 theses (`data/ontology/mentions/`). Cross-reference graph: 731 theses, 3,306 edges.
- **Research Packets**: 900 standalone research packets in `research-packets/` providing the only authorized input for thesis writers.
- **Verified Claims Layer**: 1,665 atomic scholarly claims extracted and verbatim-verified against the OCR corpus across 14 packets in `data/claims/angelology/`. 13 of 14 packets are 100% verified.
- **Draft Entries**: 118 draft entries in `entries/`. 20 pass `entry_gate.py`; 98 are in remediation due to translation similarity or missing locators.
- **Intellectual Network System**: Full specification (`docs/INTELLECTUAL_NETWORK_DESIGN.md`) for modeling Pico's 32+ key relationships as first-class metadata. Ready for Phase 0 bootstrap.
- **Deployment Status**: NOT LIVE (`DEPLOY_STATE.md`). No public deployment until tier-A pilot entries pass second-agent verification.

---

## 2. Unfinished Work from Claude Code Worktrees (Triage & Status)

Three major agent swarms and one architecture session were active in Claude Code before hitting session limits:

### Stream A: Thesis Writer & Translator Swarms (`T-ENT-01`, `T-ENT-02`)
- **What happened**: 17 background agents were dispatched (7 WRITERs for tier A, 10 TRANSLATORs for non-tier-A). WRITER-A2 finished 4 clean tier-A drafts. The other 16 agents were interrupted mid-run by session limits.
- **Current Gate State (`python scripts/entry_gate.py`)**:
  - **20 PASS**: `own_4_001`, `own_4_002`, `own_4_008`, `own_4_010`, `own_4_014`, `own_4_018`, `own_4_019`, `own_4_020`, `own_4_029`, `own_9_001`..`own_9_004`, `own_9_009`, `own_9_013`, `own_9_015`, etc.
  - **98 FAIL**: Primarily in `entries/own_2_*.draft.json` and partial blocks. Two failure modes flagged by the gate:
    1. *Translation similarity > 0.85* against Farmer's English (violates D-13 requiring original translations from the Latin copy-text).
    2. *Sentences without locators* in `attribution` and `translation_note`.
- **Immediate Next Step**:
  1. Remediate the 98 failing drafts by generating original English translations directly from the Latin text and ensuring every sentence ends in a locator.
  2. Launch a VERIFIER agent on the 20 passing drafts (`T-ENT-03`) to re-verify against source locators and promote to `entries/<slug>.json`.

### Stream B: Claims Layer & Angelology Sweep (`T-CLAIMS-02`, `T-CLAIMS-03`, `T-CLAIMS-04`)
- **What happened**: 14 researcher agents extracted claims across Allen, Black, Borghesi, Copenhaver, Dougherty, Edelheit, Howlett, Wallis, and Wirszubski.
- **Current Gate State (`python scripts/claims_verify.py`)**:
  - 1,665 claims verified verbatim against the text corpus.
  - 13 packets show `needs_fix: 0`.
  - Only `edelheit2022.claims.json` has 2 claims needing fix:
    - Claim `edelheit2022:118`: Quote interrupted by footnote 42 in the copy-text at line 19549.
    - Claim `edelheit2022:133`: Quote includes footnote 79 citation marker in copy-text at line 20090.
- **Immediate Next Step**:
  1. Fix the two quote strings in `data/claims/angelology/edelheit2022.claims.json` so `claims_verify.py` exits with `TOTAL needs_fix: 0`.
  2. Run semantic verification (`T-CLAIMS-03`) using `docs/briefs/claims_semantic_verifier.md` against `data/verification/claims/*.sample.md`.
  3. Run LINKER (`T-CLAIMS-04`) using `docs/briefs/claims_linker.md` to link cross-scholar claims.
  4. Run `python scripts/claims_score.py` to generate `scores.json`, `relevance.json`, `open_questions.json`, and `graph.json`.
  5. Unblocks writing of `docs/angelology/COMMENTARY.md` (T-ANG-01), rebuilt `docs/ANGELICRESEARCH.md` (T-ANG-02), and the Ficino-Pico dispute essay (T-FIC-01).

### Stream C: Intellectual Network System (`T-REL-01`)
- **What happened**: Comprehensive specification completed in `docs/INTELLECTUAL_NETWORK_DESIGN.md` and `docs/NETWORK_SYSTEM_HANDOVER.md`. Controlled vocabulary seeded and merged into `data/claims/parties.json` and `topics.json` via `scripts/claims_merge_vocab.py`.
- **Current State**: Ticket `T-REL-01` is marked `READY` on the board.
- **Immediate Next Step**:
  - Write `scripts/network_bootstrap.py` to generate `data/network/persons.json` from `scripts/build_dossiers.py` gazetteer + `data/claims/parties.json`.
  - Resolve canonical person IDs for key figures (Ficino, Del Medigo, Mithridates, Alemanno, Barbaro, Savonarola, trial commissioners).

### Stream D: Research Companion & PicoDB Integration (`T-SITE-05`)
- **What happened**: Architectural plan created in Claude memory (`pico900_picodb_integration_plan.md`) to integrate assets from `C:\dev\PicoDB` (SQLite `pico.db`, `sources.json`, `pico_life_timeline.json`, 94 documents).
- **Current State**: Ticket `T-SITE-05` is marked `READY` on the board.
- **Immediate Next Step**:
  - Curate `data/sources.json` (30–100 word blurbs sortable by tradition: Scholastic, Platonic, Aristotelian, Arabic, Kabbalistic, Hermetic).
  - Draft initial templates for Scholars, Bibliography, and Biography tabs.

---

## 3. How to Work with System Files (Onboarding Guide for Agents)

When an agentic system starts a turn in this repository, follow this exact sequence:

1. **Check Git Status**: Run `git status` to see what files exist and prevent concurrent collisions.
2. **Check Prompts (`PROMPTS.md`)**: Run `python scripts/harvest_prompts.py --check`. This file contains Ted's verbatim prompts and is the ultimate authority on user intent.
3. **Check the Agile Board (`TICKETS.md`)**: Run `python scripts/tickets.py ready` to see unblocked tickets with dependencies satisfied. Run `python scripts/tickets.py check` to ensure no two tickets own overlapping paths.
4. **Follow Ted's Standing Rule**: **DO NOT ASK QUESTIONS.** Ted is not an engineer and does not want to make architectural calls. Make the decision, record it in `DECISIONS.md` with the rationale, and keep executing.
5. **Enforce Deterministic Gates**: Never report something is "done" without running and quoting the gate command output:
   - `python scripts/entry_gate.py [files]` — for thesis entries.
   - `python scripts/claims_verify.py [packet]` — for scholarly claims.
   - `python scripts/commentary_check.py [file]` — for prose / commentary citing claims.
6. **End Session with Handover**: Update `HANDOVER.md` and record new prompts/tickets before closing a window.

---

## 4. Key Verification & Build Commands

```bash
# Check prompt freshness and agile tickets
python scripts/harvest_prompts.py --check
python scripts/tickets.py ready
python scripts/tickets.py check

# Thesis entries pipeline and gate
python scripts/entry_gate.py                           # Check all draft entries
python scripts/entry_gate.py entries/own_04_001.draft.json # Check single entry

# Claims layer verification
python scripts/claims_verify.py                        # Verify all 14 scholar packets
python scripts/claims_merge_vocab.py --write           # Merge new vocabulary into topics/parties
python scripts/claims_score.py                         # Generate multidimensional scores & graph

# Build and integrity gates
python scripts/build_site_v2.py                        # Rebuild static site from entries/
python scripts/integrity_gate.py --verify-quotes       # Check legacy entries
python scripts/predeploy_check.py                      # Pre-deployment validation gate
```
---

## 5. What does NOT go to GitHub (read before adding any file)

`github.com/t3dy/Pico900` is PUBLIC. Per Ted, 2026-09-27: "don't commit anything copyrighted to the github just our
digital edition and project and website etc we've been building." (D-28, D-29). Never `git add`:

- `data/corpus/` — full-text Markdown/plain-text conversions of in-copyright scholarly books (libgen-sourced). A
  commit that added 73 MB of this was found and removed from `main`'s history entirely (D-28), not just reverted.
- `data/texts/` — a generated complete-Latin file derived from that same corpus staging; regenerate locally if needed.
- `docs/resources/` — copied SEP entries and similar external reference material.
- `research-packets/` and `data/ontology/mentions/` — the harvester's per-thesis dossiers, each embedding hundreds
  of ~700-character verbatim excerpts from in-copyright scholarship (D-29). Reproducible locally at any time via
  `python scripts/harvest_mentions.py && python scripts/build_dossiers.py` against the local corpus (which itself
  lives outside git, under `E:\pdf\renaissance magic\Pico\Markdown\` or wherever this machine's copy is).

All four are listed in `.gitignore`. What *is* the edition, and does get pushed: `entries/` (our prose, with short
attributed quotations), `data/inventory/` (Pico's own public-domain Latin, the primary text), `data/ontology/theses.json`
and `MENTION_STATS.md`/`stats.json` (aggregate counts, not excerpt text), `data/corpus/registry.json` (metadata: which
work has which key, not its content), `docs/`, `scripts/`, `site/` when built, and every project-management file
(`DECISIONS.md`, `HANDOVER.md`, `PROMPTS.md`, `TICKETS.md`, `README.md`).

A cloud session that needs the actual corpus text gets it from Ted out of band (a private mount, a zip he supplies),
never from `git` on this public repo.

## 2026-09-26 morning (window-8857d983): relaunch after the session limit

- Gate rule 4 narrowed to the commentary fields (D-26): 89/118 drafts pass; the 29 left are 22 renderings too close
  to Farmer's wording and 7 notes naming him without a locator, assigned to a TRANSLATOR-FIX agent.
- Relaunched what the limit killed, with incremental writes (D-27): 6 WRITERs for the 45 missing tier-A entries,
  9 TRANSLATORs for the blocks that produced nothing (T01-T04, T06-T10), 1 fix agent for 1>/2>.
- VERIFIER-V1 (the nine condemned drafts + Q9-Q10) and VERIFIER-V2 (the other ten tier-A drafts) launched; verdicts to
  `data/verification/entries/`, promoted entries written as `entries/<slug>.json`.

## 2026-09-27 (window-8857d983): copyrighted material removed from history; main pushed

The commit behind D-24 (73 MB of in-copyright corpus text) was dropped from `main`'s history with
`git rebase --onto` (verified clean: nothing later depended on its files). `research-packets/` and
`data/ontology/mentions/` were untracked (`git rm --cached`, kept on disk) for the same reason (D-29).
`.gitignore` now excludes all four paths. `main` was pushed to `origin/main` after this cleanup; `gh-pages`
already carries a live built site (see `DEPLOY_STATE.md`) and was not touched here.
