# Session state, 2026-09-26 (window 3bc261ff), left at a usage limit

Read `PROMPTS.md` first (Ted's prompts, verbatim), then `TICKETS.md`. This note says exactly where the claims work stopped.

## Built and run (evidence: commands below)

- `PROMPTS.md` + `scripts/harvest_prompts.py` (29 prompts harvested from six transcripts; `--check` for staleness).
- Claims layer: `scripts/corpuslib.py corpus_tool.py claims_verify.py claims_pack.py claims_score.py claims_query.py commentary_check.py claims_merge_vocab.py`; spec `docs/CLAIMS_MODEL.md`; briefs in `docs/briefs/`.
  The verifier was tested on planted defects (altered quote, fabricated quote, wrong line, scholar claim from Pico's text, invented names): it caught each.
- Sweep: 14 packets in `data/claims/angelology/`; last `python scripts/claims_verify.py` showed `TOTAL needs_fix: 0`, about 1,460 claims, every quotation verbatim.
- `TICKETS.md` / `scripts/tickets.py` (21 tickets), `docs/SITE_DESIGN.md` (cards, frames, colour, sort/filter/search, relational browsing, tours, Workbench with logins and collections), `CLAUDE.md` and `docs/ORCHESTRATION.md` updated (working mode: no questions; swarm recipes).

## Not done (in order)

1. **Packet `copenhaver2022-angels`** may still be finishing (agent R-COPENHAVER); Black A/B/C, Howlett, Edelheit x2, De ente, Wirszubski agents may also still be finalising their packets. Re-run `python scripts/claims_verify.py`; fix any `needs_fix` via `python scripts/claims_pack.py <packet>`.
2. **Known verifier gap:** R-HEPTAPLUS held nine translators' notes out of its packet because `wallis1965` is in `PRIMARY_WORKS`; scholar claims from editions now only warn (`scholar_from_edition`), so those notes (listed in `data/claims/_work/wallis1965-heptaplus.meta.json` notes) can be added.
3. `python scripts/claims_merge_vocab.py --write` (topics used but unlisted: `knowledge-felicity`; parties `alemanno`, `elijah-delmedigo`, `johanan-alemanno`; many proposed topics). Fold `elia-del-medigo`/`elijah-delmedigo`, `alemanno`/`johanan-alemanno` into the network system's person ids (T-REL-01).
4. **Semantic verification (T-CLAIMS-03):** launch ~5 agents with `docs/briefs/claims_semantic_verifier.md`, grouped: allen x2; black a,b; black c, wirszubski, copenhaver; howlett, edelheit x2; borghesi, wallis x2, dougherty. Sample sheets are already generated (`data/verification/claims/*.sample.md`). Watch `ungrounded_entity` warnings (name in restatement, absent from quotation) and `scholar_from_edition` (borghesi2012: 91).
5. **Linkers (T-CLAIMS-04)** with `docs/briefs/claims_linker.md`, three topic groups, separate files `links-a/b/c.links.json` with id prefixes A/B/C; then `python scripts/claims_score.py` (importance, tiers, relevance per party, open questions, graph). Dedupe duplicate edges across files if needed.
6. **Writers:** `docs/angelology/COMMENTARY.md` (Oration, Commento via Allen, Heptaplus via Black; T-ANG-01), `docs/angelology/FINDING_AID.md` and a rebuilt `docs/ANGELICRESEARCH.md` (T-ANG-02), and the Ficino-Pico essay with its tour through *De ente et uno* and Aquinas encountering Dionysius (T-FIC-01), all with `docs/briefs/commentary_writer.md`, gated by `commentary_check.py`. Note: Aquinas's and Dionysius's own texts are not in the corpus; that strand rests on Edelheit, Howlett, Copenhaver, Allen claims.
7. Site: `scripts/build_cards.py` (T-SITE-01), cards CSS/JS, integration with the other window's `scripts/build_site_v2.py`, then tours and the Workbench per `docs/SITE_DESIGN.md`.
8. Update `PROMPTS.md` requirement statuses (table says "see below"; fill from tickets), `DECISIONS.md` (decisions taken this session: claims layer and scoring weights; relevance model; parties as seed for the network system; static-first with a two-stage Workbench and the stated Vercel reason; commentary and essay only from verified claims), and `HANDOVER.md`. Run `python scripts/harvest_prompts.py` first.

## Environment traps

Shell heredocs here halve backslashes (`\b` became a backspace and silently broke a regex): write scripts with the Write tool. Another window has committed some of this window's files inside its commits; run `git status` before committing.
