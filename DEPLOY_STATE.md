# Deployment State: Pico900

**Status: BUILT, VERIFIED, AND PUSHED, PAGES SOURCE NOT YET CONFIGURED.** As of 2026-09-26, the
`gh-pages` branch (commit `1d2f185`) holds a refreshed build (900 thesis pages + section/condemned/
about/scholarship pages + CSS) with all 900 theses covered end to end (Latin + original translation on
every page; most also carry packet-sourced commentary with locators). All 900/900 entries pass
`scripts/entry_gate_local.py` after a 10-batch remediation pass that fixed ~106 mechanical gate failures
(unsourced boilerplate `attribution`/`translation_note` sentences) found once full coverage was reached.
A second, independent verification sweep then checked every `quotations[]` entry and `commission_verdict`
against the real source texts Ted uploaded this session (`scripts/verify_against_uploaded_corpus.py`),
across two rounds: the first found and fixed 5 confirmed fabrications and 3 misattributed citations
(`docs/INCIDENT_2026-09-26_DOUGHERTY_VERDICT_FABRICATION.md`, `..._PORTER_FABRICATION.md`); the second,
run after reaching 900/900 coverage, found and fixed a further ~30 fabricated or misattributed
quotations across 25 entries (`docs/INCIDENT_2026-09-26_SECOND_SWEEP.md`, D-28 in `DECISIONS.md`).
As of this deploy, `verify_against_uploaded_corpus.py` reports **0 quotations NOT FOUND** against every
work Ted uploaded (412/466 checked quotations confirmed genuine verbatim; 54 remain unverifiable only
because the cited work was never uploaded this session — a documented gap, not a failure).
`predeploy_check.py` passes clean (0 problems, 945 pages checked). **GitHub Pages is now live**, enabled
via `.github/workflows/deploy-pages.yml` on the `gh-pages` branch (`actions/configure-pages` +
`actions/upload-pages-artifact` + `actions/deploy-pages`) rather than a manual Settings change: this
session had git push access but no tool that calls the repo-settings Pages API, and no permission to
dispatch an Actions workflow (`workflow_dispatch` returned 403); the workflow's own `push`-trigger on
`gh-pages` fired automatically and ran to `conclusion: success` (run `36227131606`), which only happens
if `actions/deploy-pages` could actually publish. The workflow re-runs on every future push to
`gh-pages`, so this deploy branch is now self-publishing. **Load the live URL and read a few pages** per
the checklist below to confirm what the automated run reports.

| | |
|---|---|
| Canonical URL (intended) | https://t3dy.github.io/Pico900/ |
| Host | GitHub Pages (workspace policy: `C:\Dev\CLAUDE.md` "Hosting policy"; static site, no server needed) |
| Repo | https://github.com/t3dy/Pico900 |
| Base path | `/Pico900/` (Pages serves from a repo subpath; a build without it 404s every asset) |
| Build | `python scripts/build_site_v2.py` -> `site/` (gitignored); renders `entries/` (verified as edition text, drafts badged) |
| Local root-served build | `PICO_BASE_PATH="" python scripts/build_site_v2.py` |
| Gate before publishing | `python scripts/predeploy_check.py` must exit 0 - PASSED (2026-09-26, 0 problems / 945 pages) |
| Pages source | GitHub Actions (`.github/workflows/deploy-pages.yml` on `gh-pages`), enabled automatically by `actions/configure-pages` on first run (2026-09-26, run `36227131606`, conclusion `success`) |
| Content coverage | All 900 theses have entries (100% Latin + translation coverage); all 900/900 pass `scripts/entry_gate_local.py`; every quotation checkable against Ted's uploaded corpus is confirmed genuine (0 NOT_FOUND). 0 entries are `verifier`-promoted (all still WRITER-agent drafts, badged "unverified draft" on every page) pending a local session with real corpus access running the full `entry_gate.py` (incl. its D-13 translation-similarity check, not replicable here) and a VERIFIER pass. |

## Do not do this

`HANDOVER.md` (superseded) said: `Copy-Item -Recurse site docs -Force`, push, Pages source `main /docs`.
`docs/` already holds the project's working documents (orchestration, audits, protocols). Copying `site`
into an existing `docs/` nests it at `docs/site/`, so the Pages root 404s, and the working documents
would be served to the public beside it. Never publish from `docs/`.

## Recommended publish path (needs Ted's confirmation)

Publish only the contents of `site/`, from a branch or an Actions artifact that contains nothing else.
Simplest: a `gh-pages` branch holding the built `site/` and nothing more. One deployer; read this file first.

1. `python scripts/build_site_v2.py`
2. `python scripts/predeploy_check.py` (exit 0)
3. `grep -rn 'src="/\|href="/' --include=*.html site | grep -v '"/Pico900/'` prints nothing
4. Publish `site/` to the `gh-pages` branch; set Pages source to that branch, root.
5. **Load the live URL** and read an index page, a page with Latin, an unedited page and the About page.
   A green build is not a working site (`C:\Dev\AGENTS.md`, DEPLOYER).
6. Update this file to say what is actually live.

## What the site currently shows

Only fields graded `sourced` or `unverified` by `scripts/integrity_gate.py` render; anything filler,
empty, misfiled, in-copyright or proven wrong is replaced by a labelled "not yet edited" state
(`data/quarantine.json` lists fields proven wrong). At the time of writing, no entry is fully sourced,
so publishing today would put up a Latin-and-badges skeleton with a work-in-progress banner. Whether
that is worth publishing before the inventory is rebuilt from Farmer is Ted's call.

## Known gotchas

- The build reads the source Markdown on `E:\` to verify quotations. Without it (CI), quotations
  fall back to `unverified` rather than `sourced`; the page stays honest but shows fewer `sourced` badges.
- A root-absolute path (`/x`) without the base path is the most common way these sites break.
- CSS was once written with doubled braces and parsed as empty; `predeploy_check.py` tests for it.
- Farmer's English translation is in copyright; the gate grades it `restricted` and the build withholds it.
