# Handover: Pico900 (2026-09-25, after the audit)

Read `CLAUDE.md` first. This file is the current state and the next steps. It replaces the earlier
`HANDOVER.md` (archived as `docs/archive/status/HANDOVER_2026-09-26_superseded.md`), whose claims of
"929 conclusions, 100% translated, 98.6% cited, no further technical work required" were false.

## The state, plainly

- **Nothing is fully sourced.** `python scripts/integrity_gate.py --verify-quotes` grades every field of all 929
  legacy entries; 0 pass. About 143 rows hold any real text (S7's 118 Cabalistic theses, 11 Averroes theses, 12
  Avicenna theses, and two condemned theses stated correctly). ~775 rows were generated filler.
- **The site is not live** (`DEPLOY_STATE.md`). The build was repaired (styles, base-path links, no filler) and passes
  `scripts/predeploy_check.py`, but with 0 sourced entries it would publish a Latin-and-badges skeleton.
- **What is solid**: the source corpus (Farmer's edition of all 900 theses is in it, plus Copenhaver, Wirszubski, Edelheit,
  Howlett, Dougherty, Black), the true structure of the work (`data/inventory/farmer_structure.json`: 402 + 498 = 900), the
  reconciliation of the thirteen condemned theses (`data/inventory/condemned_thirteen.json`), the audit
  (`audit/A1`-`A4`), and the tooling.

## What this session did

Audited every category of writing against the sources (four parallel read-only auditors, one output file each; findings
in `audit/`), then:

- Built `scripts/integrity_gate.py` (provenance grades, coverage ledger, quotation check), `scripts/style_lint.py`,
  `scripts/predeploy_check.py`, `scripts/seed_inventory.py`, `scripts/quarantine_banner.py`.
- Rewrote `docs/ORCHESTRATION.md` (v2), wrote `docs/EDITORIAL_STANDARD.md` (one standard), rewrote `CLAUDE.md`,
  `README.md`, `DEPLOY_STATE.md`; logged decisions in `DECISIONS.md`.
- Fixed `scripts/build_html_site.py`: it now renders only `sourced`/`unverified` fields, withholds in-copyright English,
  prefixes links with `/Pico900/`, and un-doubles the CSS. Verified by serving at the real subpath and loading pages.
- Quarantined (banner, not deletion) the pre-audit heretical essay and notes, the angelology and Neoplatonism docs and
  the S7 citation protocol. Archived ~35 contradictory status files to `docs/archive/`.
- Ran the first VERIFIER pass over five candidate model entries (`audit/V1_exemplar_verification.md`).

## Do next, in this order

1. **Decide Q-1 to Q-4 in `DECISIONS.md`** (translation policy, depth tiers, whether to publish a skeleton, Latin base
   text). Everything below assumes the proposed defaults.
2. **Derive the real inventory** (RESEARCHER): a script that reads Farmer's Markdown and emits one record per thesis,
   keyed `7.2` / `4>8`, with Latin and the Farmer line number, and checks the count against `farmer_structure.json` (900;
   Farmer's headings and chart disagree by one in four places, noted there). The OCR is spaced and hyphenated; expect to
   collate by hand at section boundaries. Output `data/inventory/theses.json`; gate G0 = the count matches.
3. **Pilot block: the thirteen condemned theses (Tier A)**, through RESEARCHER, WRITER, VERIFIER, AUDITOR. Everything needed
   is mapped: Farmer ids and lines and the commission's verdicts (`condemned_thirteen.json`, A1 s3, A2 s5a), scholastic
   apparatus and locators (A2 s5a), model sections for Q4 (A2 s5b) and theses 4>2, 4>13, 11>23, 7.2 (A1 s4; see V1 for
   which passed verification). Have Ted read five entries cold before scaling. Measure minutes per verified thesis.
4. **Rebuild the heretical essay** from the pilot, not from `docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md` (quarantined). A2
   supplies the depth list and shows that the outline's central argument is contradicted by Copenhaver.
5. **Re-key the legacy entries** to Farmer's numbering; retire `S1..S9`. Section 7 (Averroes, 41) and section 28 (Cabalists,
   47) plus 11> (72) are the richest and already partly in the repo; S6/S9/S2/S5 contents are filler and should be dropped.
6. **Only then deploy**, per `DEPLOY_STATE.md` (never from `docs/`).

## Open defects (known, unfixed)

- 22 S7 entries have English in the Latin field; 23 have `[TO_TRANSLATE]`; 108 of 118 S7 Latin fields stop at the first OCR
  line break. The gate grades these; the fix is re-derivation from Farmer, not patching.
- S7 English reproduces Farmer's translation (in copyright): withheld from the site, still in the JSON.
- Thesis 11>66 is missing from S7. Q11's exact thesis is unconfirmed (9>8 or 9>7).
- The angelology and Neoplatonism modules (`data/texts/`, `data/scholarships/angels/`, `data/neoplatonism/`,
  `data/sources.json`) are mislabelled and partly wrong (`data/texts/QUARANTINE.md`; A3). Not rendered anywhere.
- `data/schema.json` matches neither the data nor the docs; nothing validates against it. Replace it when the Farmer-keyed
  entry format is fixed (fields: `EDITORIAL_STANDARD.md` s5).
- Latin has not been collated against the Brown critical edition or the 1486 print. Farmer's Latin is an edition; reuse
  terms are unconfirmed.
- The gate's page-locator and quotation checks depend on the source Markdown at `E:\pdf\...`; without it quotations grade
  `unverified` at best.

## What was not verified this session

- I did not read all 929 entries or all 946 pages; I measured them by script and sampled 28 entries plus 12 passage entries
  by auditor. Sections S2, S5, S6, S8, S9 rest on 1-2 entries each plus the statistics.
- Auditors' "not found" results are regex searches of OCR text; they show absence from the corpus, not from print.
- Q11's thesis, and the commission's wording for Q5, Q11, Q13, are unlocated in the corpus.
- No live URL was tested for content because there is no live site. The subpath serve-and-load test was done locally only.
- The exemplars' correctness is only as good as `audit/V1_exemplar_verification.md`; see that file.

## Commands

```bash
python scripts/integrity_gate.py --verify-quotes     # the truth about the data (writes COVERAGE.md, data/coverage_ledger.json)
python scripts/style_lint.py FILE...                 # AI-prose marker counts
python scripts/build_html_site.py && python scripts/predeploy_check.py   # build and gate the site
python -m http.server 8766 --directory <dir containing a Pico900/ copy of site/>   # test at the real subpath
```
