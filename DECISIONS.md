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

---

## 2026-09-25 — Scope Expansion: Four-Text Digital Editions (T)

**Decision**: Create parallel digital editions for *Oration*, *Commento*, *Heptaplus*, and *On Being and Unity* with facing-page Latin/English + angelology-focused commentary.

**Rationale**:
- Pico's angelology is the **structural backbone** of all four texts
- Angelology research is **prerequisite** for understanding heretical conclusions (Q1, Q6, Q8 cluster around divine embodiment via angels)
- Four texts are **philosophically unified** (Pseudo-Dionysius + Aquinas + Kabbalah + Plotinus synthesis)
- Facing-page editions provide **interpretive depth** that helps scholars navigate 900 Conclusions with proper context
- Edition infrastructure is **reusable** for all 900 conclusions later

**Angelology Focus**:
- Research four lineages: Pseudo-Dionysius, Aquinas, Kabbalah, Plotinus
- Map angelic correspondence across all texts (theme cross-reference table in ANGELICRESEARCH.md)
- Heretical conclusions Q1, Q6, Q8 are solved by understanding celestial metaphysics first
- Agent swarms can work on edges (angel-themed conclusions) while main pipeline continues

**Rules out**:
- Postponing angelology research to Phase 2 or later
- Treating four-text editions as "context only" rather than first-class deliverables
- Angelology as isolated sections in 900 Conclusions

**Implementation**:
- Create `data/texts/` directory with subdirs: `oration/`, `commento/`, `heptaplus/`, `being_unity/`
- Each text has: `passages_angelology.json`, `entries/`, `exegeses/`
- Shared scholarship database: `data/scholarships/angels/` (lineage tags + debate log)
- ANGELICRESEARCH.md is north star for all angel-related work (HARVESTER, SYNTHESIZER, REVIEWER receive excerpts only)

**Agent Workflow** (Parallel to Phase 0/1):
1. **HARVESTER**: Extract angelology passages from four texts (parallel execution, 4 agents)
2. **PORTER**: Standardize + cross-link angelology passages
3. **SYNTHESIZER**: Write exegeses for angelic concepts across all four texts
4. **REVIEWER**: Validate against ANGELICRESEARCH.md + STYLE_GUIDE.md

**Phase Sequencing**:
- **Phase 0** (Heretical Essay Research): Continue as planned, but note angelology will be needed for deep work
- **Phase 1-Alpha** (Four-Text Editions + Angelology): Parallel to Phase 1 main pipeline
  - Agents H2-A, H3-A, H4-A extract angelology from Oration, Commento, Heptaplus
  - Agents P2-A, P3-A, P4-A port angel-themed conclusions
  - Agents S1-A–S4-A synthesize angelology exegeses across texts
  - Result: Four high-quality digital editions ready for delivery as standalone sites (or integrated into Pico900)
- **Phase 1-B**: Main 900 Conclusions pipeline (continues with S1–S9 sections as originally planned)

**Token Budget**:
- Phase 1-Alpha (Four-Text Editions): ~80k tokens (parallel harvesting + porting + synthesis)
- Phase 1-B (900 Conclusions): ~100k tokens (now running parallel to 1-Alpha)
- Total Phase 1: ~180k tokens (vs. 100k sequential) — parallelism costs extra communication, but delivers more value

---

## 2026-09-25 — Angelology as Lens for Heretical Essay (C)

**Decision**: Reframe heretical conclusions research around angelology framework.

**Rationale**:
- Condemned conclusions Q1, Q6, Q8 are incomprehensible without angelology (divine embodiment, doxastic bondage, etc.)
- ANGELICRESEARCH.md provides **unified theological framework** for understanding heresy charges
- Copenhaver's trial analysis becomes clearer when read through angelic metaphysics
- Synergy: angelology research in four texts informs deeper heretical essay commentary

**Rules out**:
- Treating angelology as optional supplementary material
- Heretical essay research isolated from angelology research

**Implementation** (for continuing Phase 0):
- When S1-HERETICAL writes exegeses for Q1, Q6, Q8, they reference ANGELICRESEARCH.md for angelology context
- When R1-REVIEWER validates heretical entries, check: does exegesis explain the angelological charge?
- Phase 0 retrospective will note: "Angelology research in parallel editions deeply enriched heretical essay commentary"

---

## 2026-09-26 — Phase 1 Execution Decisions (C)

**Decision**: Adopt content-first extraction methodology for all future HARVESTER agents.

**Rationale**:
- H4 (Avicennist, 12 full conclusions) delivered publication-ready entries; H2 (Neoplatonic, 95 stubs) delivered empty infrastructure
- Content-first approach reduces Phase 2 remediation effort by ~50%
- Sparse, substantive content outweighs full-coverage empty scaffolding
- Manifests critical learning for all Phase 2+ sections

**Rules out**:
- Infrastructure-first methodology for future sections
- Creating JSON entries without substantive charge/defense pairs and 2+ citations

**Implementation**:
- Standardize HARVESTER briefing with explicit "content-first" directive
- Instruct: "Extract only conclusions you can substantiate. Do not create skeleton stubs."
- Track `conclusion_count_explicit` vs. `conclusion_count_implicit` in manifest
- For S2, S5, S6, S8, S9 dispatches, mandate content-first approach

---

**Decision**: Distinguish explicit vs. implicit conclusions in manifest schema.

**Rationale**:
- Critical edition contains ~141 explicit conclusions (full Pico text) + ~202 implicit conclusions (incipit-only placeholders)
- S3/S4 discovery: 91% and 89% deferred to implicit, respectively
- Distinct tracking enables accurate Phase 2 planning and prevents confusion about section completeness
- Reflects discovery that critical edition has two-tier structure: explicit (complete) and implicit (outline)

**Rules out**:
- Conflating explicit and implicit conclusion counts
- Treating all 900 as equally extractable in one pass

**Implementation**:
- Update manifest schema: add `conclusion_count_explicit` and `conclusion_count_implicit` fields
- Report both counts for every section
- Set extraction target = explicit conclusions only; defer implicit to Wave 2
- Communicate to all future HARVESTER agents: "Critical edition has explicit (full text) and implicit (outline) sections. Extract explicit to completion; mark implicit as placeholders."

---

**Decision**: S7 citation-filling will proceed in parallel with S3 site build, not sequentially.

**Rationale**:
- S7 quotation-filling is 50–80 hour effort; blocks Phase 3 heretical essay Q5 drafting if sequential
- Parallel execution (researcher + builder on independent tracks) avoids critical path blocking
- Phase 2 completion timeline: week 4–5 (parallel) vs. week 8+ (sequential)
- Aligns with workspace principle: deliver working product early, add features iteratively

**Rules out**:
- Sequential execution of S7 citation-filling after S3 site complete
- Deferring heretical essay Q5 drafting until after S7 completion

**Implementation**:
- Phase 2a (weeks 1–2): S3 site build (builder) + S7 Wirszubski citations (researcher, 20–30 hours)
- Phase 2b (weeks 3–4): S7 Scholem + specialist citations (researcher, 30–50 hours) **IN PARALLEL WITH** final site integration
- Phase 2c (week 4+): S1 content remediation (scholar, 50–60 hours) runs independently
- Phase 2d (weeks 1–3): S2 extraction (HARVESTER agents) runs independently
- Critical path: S7 citation-filling 100% → Phase 3 Q5 essay drafting can begin

---

**Decision**: Add intermediate HARV-CHECK gate between HARVESTER and PORTER dispatch.

**Rationale**:
- S1's empty scaffolds (95 entries with 0% content) were caught late (REVIEWER gate)
- HARV-CHECK gate (before PORTER) would flag methodology errors early
- Prevents wasting 25k PORTER tokens standardizing incomplete entries
- Catches: empty charge/defense sections, <1 avg citation per entry, unexpectedly low explicit conclusion count

**Rules out**:
- Relying solely on REVIEWER gate for methodology validation
- PORTER standardizing incomplete or poorly-researched entries

**Implementation**:
- HARV-CHECK validates after each HARVESTER completion:
  - `conclusion_count_explicit` ≥ 25% of estimated range
  - Average citations per entry ≥ 1
  - Charge/defense sections are substantive (not placeholder text)
  - No more than 20% deferred as implicit/placeholder
- If HARV-CHECK fails, alert and allow HARVESTER to revise before PORTER dispatch
- Add to manifest schema: `harv_check` gate (status, timestamp, validation notes)

---

**Decision**: Refine status field semantics with granular completion tracking.

**Rationale**:
- Current `status: "standardized"` masks wide variance: 1% complete (S1) vs. 100% complete (S3)
- Downstream processes (site builder, researcher) need to distinguish "ready to publish" from "structure ready, content blocked"
- Prevents erroneous decisions based on ambiguous status

**Rules out**:
- Relying solely on `status` field for completeness assessment

**Implementation**:
- Add `completion_tracker` object to manifest schema for each section:
  ```json
  "completion_tracker": {
    "latin_incipit_pct": 100,
    "english_translation_pct": 100,
    "charge_defense_pct": 25,
    "scholar_citations_pct": 10,
    "overall_pct": 33
  }
  ```
- Update completion_tracker at each gate (HARVESTER, HARV-CHECK, PORTER, REVIEWER)
- Use for Phase 2 scheduling: sections with ≥90% completion move to site build; <50% stay in remediation
- Implementation timing: Phase 2a (manifest schema update before S2 dispatch)

---

**Decision**: Phase 2 will execute four parallel independent tracks (no blocking dependencies).

**Rationale**:
- S3 site build (builder) doesn't depend on S7 citations (researcher)
- S1 content remediation (scholar) doesn't depend on S2 extraction (HARVESTERs)
- Parallel execution delivers Phase 2 completion by week 4–5 instead of week 8–10 (sequential)
- Maximizes throughput while avoiding work-in-progress bottlenecks

**Tracks**:
1. **S3 Site Build** (2 weeks, builder): HTML from 11 JSON entries + facing-page layout + search/filter + deployment
2. **S7 Citation-Filling** (3–4 weeks, researcher): Wirszubski + Scholem + specialists for 118 entries (~50–80 hours)
3. **S1 Content Remediation** (2–3 weeks, scholar): Latin/translation/charge-defense sourcing for 95 entries (~50–60 hours)
4. **S2 Extraction** (2–3 weeks, HARVESTERs): Peripatetic conclusions from critical edition (content-first methodology)

**Rules out**:
- Sequential execution of tracks
- S3 site gated on S7 citations

**Implementation**:
- Assign builder, researcher, scholar, and HARVESTER agents to non-overlapping tasks
- Weekly checkpoint meetings (Monday + Friday) to monitor progress
- Manifest updates per-track without cross-track blocking
- Phase 2 complete when all four tracks reach closure (staggered completion acceptable)

---

## Next Decision Gates

- **Phase 1 → Phase 2**: Retrospective complete; HARVESTER methodology refined (content-first + HARV-CHECK); Phase 2 parallel tracks approved
- **Phase 2a Start**: Dispatch builder (S3 site), researcher (S7 citations), HARVESTER H2 (S2 extraction) simultaneously (week 1, 2026-09-30)
- **Phase 2a Checkpoint**: Week 2 (2026-10-07) — S3 site rendering tests, S7 Wirszubski 50% complete, S2 extraction in progress
- **Phase 2b Integration**: Week 3–4 (2026-10-14 to 2026-10-21) — S3 site deployed, S7 citations ≥80%, S1 remediation ramping
- **Phase 2 Complete**: Week 5 (2026-10-28) — All four tracks closed; manifest shows ≥90% overall completion
- **Phase 3 Gate**: Heretical essay Q5/Q8 drafting approved once S7 citations 100% + S3 site live
- **Angelology Research**: Continue in parallel (four-text editions); integrate findings into Pico900 Q1/Q6/Q8 sections as they become ready

