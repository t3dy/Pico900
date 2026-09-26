# Archive

History, kept because it explains how the project got here. **Nothing in this directory is an instruction,
a specification, or evidence.** Several files certify work that the audit of 2026-09-25 (`audit/`) found to
be filler or unverified, and their success claims are wrong.

| directory | contents | why archived |
|---|---|---|
| `status/` | root-level handovers, phase reports, progress and readiness files, the false deployment guide, and a stray path-mangled copy of it | contradicted each other and the data; superseded by `HANDOVER.md`, `DEPLOY_STATE.md`, `COVERAGE.md` |
| `v1-pipeline/` | HARVESTER/PORTER/SYNTHESIZER/REVIEWER orchestration, agile ticketing, context architecture, phase review reports | replaced by `docs/ORCHESTRATION.md` (v2); its gates checked field presence, so filler passed |
| `v1-style/` | `PICO900_STYLE_GUIDE.md`, `STYLE_GUIDE.md` | replaced by `docs/EDITORIAL_STANDARD.md`; their model-voice passages and worked examples are invented or wrong |

Legacy validators and one-off extractors are in `scripts/legacy/` for the same reason: they certified shape,
not truth.
