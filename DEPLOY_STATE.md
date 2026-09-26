# Deployment State: Pico900

**Status: NOT LIVE.** `https://t3dy.github.io/Pico900/` returned GitHub's "There isn't a GitHub Pages
site here" (404) when checked on 2026-09-25. Nothing has been published. Any earlier document that says
"deployed", "ready to deploy" or "live" is wrong; see `audit/A4_site_and_governance.md` Part B.

| | |
|---|---|
| Canonical URL (intended) | https://t3dy.github.io/Pico900/ |
| Host | GitHub Pages (workspace policy: `C:\Dev\CLAUDE.md` "Hosting policy"; static site, no server needed) |
| Repo | https://github.com/t3dy/Pico900 |
| Base path | `/Pico900/` (Pages serves from a repo subpath; a build without it 404s every asset) |
| Build | `python scripts/build_site_v2.py` -> `site/` (gitignored); renders `entries/` (verified as edition text, drafts badged) |
| Local root-served build | `PICO_BASE_PATH="" python scripts/build_site_v2.py` |
| Gate before publishing | `python scripts/predeploy_check.py` must exit 0 |
| Pages source | **not yet configured.** Decision pending: see below |

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
