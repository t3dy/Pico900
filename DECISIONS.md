# Decisions Log — Pico900

All directional decisions recorded here with date, decider (C=Claude based on system judgment, T=Ted explicit), rationale, and what it rules out.

## 2026-09-25 — Project Initiation (T)

**Decision**: Create Pico900 as a standalone static-site digital edition, separate from PicoDB research portal.

**Rationale**: 
- Pico900 is a specific deliverable (snazzy website with facing-page Latin/English + commentary)
- PicoDB is the underlying research infrastructure (full portal, 15+ study passes)
- Separating them allows iteration on the website without disrupting research
- Aligns with workspace precedent (Claudiens = website; RenMagDB = research)

**Rules out**: 
- Merging Pico900 back into PicoDB
- Building Pico900 as dynamic site or Next.js app (static on GitHub Pages only)
- Requiring visitors to understand PicoDB infrastructure

---

**Decision**: Prioritize existing translations over new work (T)

**Rationale**: 
- Megabase contains ~100 translation passes already
- Sourcing them first is efficient context engineering
- Supplement with new work as needed

**Rules out**: 
- Wholesale retranslation of the 900 before harvesting megabase

---

**Decision**: Commentary from verbatim scholarship quotations first, then LLM synthesis (T)

**Rationale**: 
- Maintains scholarly rigor and traceability
- Avoids synthesis drift
- Mirrors PicoDB's provenance model

**Rules out**: 
- Starting with LLM-generated commentary and adding citations after
- Paraphrasing scholarship without quotation

---

**Decision**: "Heretical" essay synthesizes Copenhaver, Dougherty, Howlett, Edelheit on condemned propositions (T)

**Rationale**: 
- Copenhaver's *Pico on Trial* is canonical on heresy charges
- Dougherty anthology covers specific conclusions
- Howlett + Edelheit discuss historiography and scholasticism
- Unified essay layer needed

**Rules out**: 
- Heretical conclusions scattered throughout site; need one synthesis

---

## 2026-09-25 — Agentic Architecture Decisions (C)

**Decision**: Deterministic chunking over dynamic task-stealing for agent work distribution.

**Rationale**: 
- Workspace principle: "deterministic before LLM"
- Pre-assign work by section/theme = reproducible, auditable, zero race conditions
- Parallel agents (4–8) working on independent sections simultaneously
- Simpler checkpointing: per-section, not per-task
- Rules out hermeticism: if an agent dies, we resume exactly where it left off

**Rules out**: 
- Dynamic task-stealing (agents pick next available task)
- Concurrent writes to same manifest section (serializes via ORCHESTRATOR)

---

**Decision**: Aggressive context isolation: agents receive ONLY their role context + specific task manifest entry.

**Rationale**: 
- HARVESTER doesn't need STYLE_GUIDE or heretical essay plan
- PORTER doesn't need megabase paths or critical edition URLs
- Token efficiency: ~5–10k tokens per agent instead of ~50k if they all carried full project context
- Reduces hallucination and scope creep
- Forces clear handover contracts between stages

**Rules out**: 
- Giving agents full CLAUDE.md + all documentation
- Assuming agents will read project context "for reference"

Implementation:
- HARVESTER: Receives `SOURCING_PROTOCOL.md` + `data/staging_queue.json` only
- PORTER: Receives `STYLE_GUIDE.md` + `data/staging/[section].json` only
- SYNTHESIZER: Receives `STYLE_GUIDE.md` + `data/conclusions/[section]/*.json` + relevant PicoDB excerpts only
- REVIEWER: Receives `STYLE_GUIDE.md` + citation linter schema + entries to review only

---

**Decision**: Phase gates with mandatory validation before stage progression.

**Rationale**: 
- Workspace rule: "verify before done" — output is only good if it's been checked
- Each phase produces an artifact; next phase receives only approved input
- Prevents cascading errors (garbage in → garbage out)
- Creates natural pause points for retrospectives and learnings

**Rules out**: 
- Continuous flow without validation
- Agents shipping unreviewed work

Flow:
```
HARVESTER → [output: stage_*.json]
            ↓ [ORCHESTRATOR validates structure]
         PORTER → [output: conclusions/[section]/*.json]
                  ↓ [ORCHESTRATOR validates schema]
               SYNTHESIZER → [output: enhanced conclusions + essay outline]
                             ↓ [REVIEWER validates against STYLE_GUIDE]
                          [APPROVED] → manifest update
```

---

**Decision**: Section-level (not conclusion-level) checkpointing.

**Rationale**: 
- 95 conclusions = 95 files would be excessive
- 8 sections = 8 checkpoint files, manageable and traceable
- Each section ~12 conclusions on average
- If agent fails mid-section, we restart that section only (~5k tokens to re-harvest)

**Rules out**: 
- Per-conclusion checkpoints (too granular)
- Per-phase checkpoints (too coarse; can't resume mid-phase)

Sections (from megabase + critical edition):
1. Secundum Adelandum Arabem (8)
2. Secundum Abucaten Avenan (10)
3. Secundum Averroem (41)
4. Secundum Avicennam (12)
5. Secundum Alfarabium (11)
6. Secundum Moysem Aegyptium (3)
7. Secundum Isaac Narbonensem + Abumaron Babylonium (8)
8. [Remaining sections to be catalogued from critical edition]

---

**Decision**: Token budgeting per phase; retrospective after each phase.

**Rationale**: 
- Heretical essay work = learning ground for pipeline efficiency
- Phase 1 (Heretical Essay Research): 150k tokens max (HARVESTER + SYNTHESIZER only)
- Measure: Do we hit quality? How fast? What's the bottleneck?
- Iterate before scaling to all 900 conclusions

**Rules out**: 
- Open-ended token spend
- Scaling to full 900 without learning from heretical work first

---

**Decision**: One-writer-per-file always; ORCHESTRATOR manages all manifest updates atomically.

**Rationale**: 
- Workspace rule: "one writer per file, always"
- JSON manifest is the source of truth; can't have concurrent writes
- ORCHESTRATOR collects output from all agents, batches manifest updates, writes once per phase
- Prevents corruption, race conditions, merge conflicts

**Rules out**: 
- Multiple agents editing manifest simultaneously
- Git-based merge of manifest (too complex for JSON state)

---

**Decision**: JSON manifest + Markdown phase reports for communication and retrospectives.

**Rationale**: 
- `data/conclusions_manifest.json`: machine-readable, queryable, version-able
- `docs/PHASE_[N]_REPORT.md`: human-readable learnings, methodology notes, bottlenecks
- Agents write `.md` summaries after each phase (what worked, what was slow, surprises)
- Enables iteration: next phase starts with lessons from previous

**Rules out**: 
- Stdout logging only (not searchable)
- Expecting agents to improve process without explicit retrospective

---

**Decision**: Start with heretical essay research (Phase 0) before main pipeline. Use it as iteration engine.

**Rationale** (T):
- Heretical essay is high-value + focused scope (13 conclusions, deep scholarship)
- Copenhaver + Dougherty + Edelheit + Howlett = bounded research surface
- Learn pipeline efficiency on a real, valuable output before scaling to 95 conclusions
- Heretical essay becomes the proof-of-concept for the whole system

**Rules out**: 
- Starting with broad harvesting of all 900
- Treating heretical essay as "just another section"

Phase 0 deliverable: **Heretical Essay Outline + Full Citation Map** (13 condemned conclusions with source quotations organized by theme)

---

## 2026-09-25 — System Documentation Structure (C)

**Decision**: Create modular system documentation with progressive context revelation.

**Files created**:
- `CLAUDE.md` (bootloader: purpose, phases, constraints)
- `DECISIONS.md` (this file: all architectural choices logged)
- `docs/SOURCING_PROTOCOL.md` (where to find translations)
- `docs/STYLE_GUIDE.md` (entry format + quality checklist)
- `docs/AGENT_SWARM_PATTERNS.md` (role definitions, handover protocols)
- `docs/ORCHESTRATION.md` (NEW: agent lifecycle, gates, concurrency rules, phase structure)
- `docs/CONTEXT_ARCHITECTURE.md` (NEW: what each agent receives; isolation boundaries)
- `docs/HERETICAL_RESEARCH_PLAN.md` (NEW: Phase 0 specifics — Copenhaver + Dougherty deep dive)
- `PHASE_0_RESEARCH_QUEUE.json` (NEW: work tickets for heretical essay research)

**Rationale**: 
- Each agent reads ONLY the docs relevant to their role
- HARVESTER doesn't read STYLE_GUIDE (doesn't write entries)
- PORTER doesn't read SOURCING_PROTOCOL (sources already found)
- Reduces cognitive load, token spend, hallucination

**Rules out**: 
- Single monolithic documentation
- Agents reading everything

---

## 2026-09-25 — Phase 0 Launch (C)

**Decision**: Initiate Phase 0 (Heretical Essay Research) immediately as proof-of-concept for pipeline.

**Agents Dispatched**:
1. HARVESTER H1-HERETICAL (a7f3b6eed4c0d4a14): Extract 13 condemned conclusions from Copenhaver
2. PORTER P1-HERETICAL (queued, awaiting H1 output)
3. SYNTHESIZER S1-HERETICAL + S2-HERETICAL-ESSAY (queued)
4. REVIEWER R1-HERETICAL (queued)
5. RETROSPECTIVE (queued)

**Phase Budget**: 150k tokens max

**Success Criteria** (Phase 0 must pass all):
- All 13 condemned conclusions identified
- Heretical entries have charge + defense + modern debate
- All citations verified or marked [CITED]
- Essay outline coherent and well-sourced
- Retrospective identifies pipeline improvements

**Rules out**:
- Starting Phase 1 (all 900) until Phase 0 passes all criteria
- Scaling the pipeline without learning from heretical essay work

---

## 2026-09-25 — Phase 1 Prioritization (T)

**Decision**: Prioritize Neoplatonic (S1) and Arabic philosopher sections (S3, S4) for Phase 1 Wave 1.

**Rationale**:
- Existing research in PicoDB covers these areas extensively (15+ study passes)
- Megabase has translation passes + essay fragments on these sections
- Fastest path to high-quality deliverables
- Copenhaver provides backbone for theological (S9) sections; can defer those

**Rules out**:
- Default left-to-right section ordering
- Starting with understudied sections (S8 on medieval Jewish philosophers)

**Dispatch order for Phase 1**:
1. Wave 1: S1 (Platonics), S3 (Averroes), S4 (Avicenna) — H2, H3, H4
2. Wave 2: S2 (Aristotle), S5 (Zoroastrianism), S6 (Hermeticism) — H5, H6, H7
3. Wave 3: S7 (Kabbalah) — H8 (strongest agent, due to source difficulty)
4. Wave 4: S8 (Medieval Jewish) — H9
5. Wave 5: S9 (Christian Theology) — H10

**Implementation**:
- Update PHASE_1_ROADMAP.md to reflect priority ordering
- Create CRITICAL_EDITION_TAXONOMY.md with section priority tiers + incipit ranges
- Dispatch log will track actual order (may differ from plan based on agent availability)

---

## Next Decision Gates

- **Phase 0 → GitHub**: Commit Phase 0 deliverables + push to GitHub Pages ✓ (DONE)
- **Phase 1 infrastructure**: Create PHASE_1_ROADMAP.md, ORCHESTRATION.md, TAXONOMY.md, RESEARCH_QUEUE.json ✓ (IN PROGRESS)
- **Phase 1 launch**: User approval to dispatch H2, H3, H4 for Wave 1 (awaiting)
- **Mid-Phase 1**: Retrospective checkpoint after S1–S4 complete (optional)
- **Phase 1 complete**: Evaluate all 900 conclusions against success criteria
- **Phase 2 gate**: Approve website UI + deployment plan before building

