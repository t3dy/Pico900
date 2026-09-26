# Handover: Pico900 (2026-09-25, evening: research layer built, swarms launched)

Read `CLAUDE.md` first, then `docs/ORCHESTRATION.md` ("The pipeline"). This replaces the morning handover
(state after the audit) and the pre-audit one in `docs/archive/status/`.

## State

- **Inventory**: `data/inventory/theses.json`, all 900 theses from Farmer's edition with line locators, 1486/1487
  apparatus (139), folio marks (58), a pointer to Farmer's English (864) and to his notes (801). Validated: every
  section's count equals Farmer's printed count and all 149 marginal cumulative numbers agree with the derived
  order. Two ids rest on sequence inference (3>63 at F:21264, 7a>63 at F:24505; both checked by eye).
- **Harvest**: `data/ontology/` — mentions of theses in 78 works (explicit ids, Copenhaver's Q-numbers, Edelheit's
  chapter references, Wirszubski's *Conclusio* headings, verbatim Latin), with statistics. 421 theses are cited by at
  least one scholar, 63 by three or more, 479 by none (sections 7-27: the Arabs, Greeks and Platonists are
  the desert). Farmer's cross-reference network: 731 theses, 3,306 edges.
- **Packets**: `research-packets/` (900) and `translation-sheets/` (10 blocks). Tiers suggested: A 63, B 358, C 416, D 63.
- **Entries**: `entries/` is being filled by the swarms launched at the end of this session (see below). Legacy
  `data/conclusions/` entries remain quarantined/withdrawn; the site build still reads them and must be re-pointed.
- **Not live** (`DEPLOY_STATE.md`).

## Swarms launched (background agents; results arrive as `entries/*.draft.json`)

| agent | scope | output |
|---|---|---|
| WRITER-A1..A3 | the thirteen condemned theses (14 ids: Q2 is 4>19-20), tier A, full entries | `entries/own_04_*.draft.json`, `own_09_008/009`, `own_03_049/060` |
| WRITER-B1..B4 | the other 49 tier-A theses (28.x, 3>55, 5>19, 7>5-6, 8>6-7, 9>1-26, 10>2, 10>15, 11>x) | `entries/*.draft.json` |
| TRANSLATOR-T01..T10 | original translations + attribution for every non-tier-A thesis, one block per agent | `entries/*.draft.json` (tier-D fields) |

One writer per file: the lists are disjoint. Each agent runs `python scripts/entry_gate.py <its files>` before
finishing and reports what it could not establish.

## Do next

1. When the swarms report: run `python scripts/entry_gate.py` over `entries/`; read the report; send failures back.
2. Launch VERIFIERs (different agents from the writers): tier A first. A VERIFIER re-finds every quotation and
   dated claim at its locator, checks each translation's sense against Farmer's English line without copying it,
   and promotes `<slug>.draft.json` to `<slug>.json` only on a clean pass; verdicts to `data/verification/`.
3. Have Ted read five tier-A entries cold before scaling the commentary to tier B.
4. Re-point `scripts/build_html_site.py` at `entries/` (Farmer-keyed; render only verified fields; "cited by" from
   `data/ontology/mentions`; cross-references as links), then `predeploy_check.py`, then `DEPLOY_STATE.md`.
5. Topic harvesting for the 479 uncited theses (planned in `docs/DATA_ONTOLOGY.md`); Edelheit's Part 3 and the
   Platonism literature (Allen) are the likely sources.
6. Bibliographic confirmation of the `(from file name)` registry entries before any of them is cited.

## Known defects and cautions

- Farmer's Latin is OCR: `ı` for `i`, `_` for spaces, `<}N00)9>` for Hebrew; the WRITER normalises obvious OCR and
  records anything doubtful in `latin_note`. Collation against the 1486 print and the Brown edition remains undone.
- Farmer's English line pointers are 96% complete; where absent, the VERIFIER finds the English on the facing page.
- The gazetteer and the registry labels are first drafts; `(from file name)` works are not citable yet.
- `harvest_mentions.py` explicit-id detection in works other than Farmer covers `d>d` and "thesis d.d" forms only;
  Italian/German works citing "conclusione 23" are found only when they quote the Latin.
- Cost: a tier-A packet can exceed 50 KB (4>2 has 80 Copenhaver mentions); writers are told to open sources at the
  cited lines, not to read books.

## Commands

```bash
python scripts/build_corpus_registry.py && python scripts/extract_farmer_theses.py && python scripts/harvest_mentions.py && python scripts/build_dossiers.py
python scripts/entry_gate.py                      # all drafts
python scripts/integrity_gate.py --verify-quotes  # legacy entries only
```

## Coordination with the other windows (added late 2026-09-25)

This window (`window-8857d983`) owns: `scripts/{build_corpus_registry,extract_farmer_theses,harvest_mentions,build_dossiers,entry_gate,build_site_v2}.py`,
`data/inventory/`, `data/corpus/`, `data/ontology/`, `research-packets/`, `entries/` (through its writer and translator
agents), `docs/{ENTRY_FORMAT,DATA_ONTOLOGY,RESEARCH_PROTOCOL}.md`, `RESEARCHNOTES_2026-09-25.md`. The claims layer
(`data/claims/`, `docs/CLAIMS_MODEL.md`, `scripts/claims_*.py`), the ticket board and `PROMPTS.md` belong to
`window-3bc261ff`; the intellectual network to `window-a08fd9b0`. Tickets for this window's work are on the board
(`python scripts/tickets.py list`). Commits 7f8bd73 and ae9a4bf accidentally snapshotted the claims layer's
uncommitted files (D-17); nothing was lost.
