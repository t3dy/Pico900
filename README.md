# Pico900: a digital edition of Pico's 900 Conclusions (in preparation)

A scholarly edition of Giovanni Pico della Mirandola's *Conclusiones* (Rome, 7 December 1486): the Latin,
an English translation, and commentary that gives a reader the historical context and philosophical depth of
each thesis, with a study of the thirteen theses censured in 1487.

**Status.** Work in progress and not yet published. An audit on 2026-09-25 found that earlier drafts had filled
empty fields with generated placeholder text; that text has been withdrawn, and the edition is being rebuilt
from Farmer's edition (the source of the 900) with every claim traced to a source. See `HANDOVER.md`,
`COVERAGE.md` and `audit/`.

## Principles

- Every Latin word, translation, quotation and date carries a source. A field without one is shown as
  *not yet edited*, never filled.
- Scholarly quotations are shown only after they have been found, verbatim, in the cited work.
- Translations are original and are checked against, not copied from, Farmer's (in copyright).
- Depth is tiered and stated openly (`docs/EDITORIAL_STANDARD.md`).

## Where things are

| | |
|---|---|
| `docs/EDITORIAL_STANDARD.md` | how entries and essays are written |
| `docs/ORCHESTRATION.md` | how agents work on this project, and the gates |
| `data/inventory/` | the true structure of the 900 and the thirteen condemned theses |
| `COVERAGE.md` | generated: what is sourced, by field, by section |
| `audit/` | the audit reports |
| `DEPLOY_STATE.md` | publishing (currently: not live) |
| `CLAUDE.md` | instructions for agents |

## Building

```bash
python scripts/build_corpus_registry.py            # the works and their locator files
python scripts/extract_farmer_theses.py            # the 900 theses from Farmer's edition (gate G0)
python scripts/harvest_mentions.py                 # every scholarly mention of every thesis, with statistics
python scripts/build_dossiers.py                   # one research packet per thesis (the writer's input)
python scripts/entry_gate.py                       # check entry drafts: locators, verbatim quotations, original translation
python scripts/build_site_v2.py                    # build site/ from entries/ (verified as text; drafts badged)
python scripts/predeploy_check.py                  # gate before any publish
```

## Licence

Pico's *Conclusiones* are in the public domain. The edition's original apparatus and translations are offered
under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Farmer's translation and other modern
scholarship are cited, not reproduced.

## Related

`C:\Dev\PicoDB` (research portal), `C:\Dev\megabase` (LLM archive), `E:\pdf\renaissance magic\Pico\` (sources).
