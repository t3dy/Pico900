# Pico900 System Architecture Summary

**Project**: Digital edition of Pico's 900 Conclusions with facing-page Latin/English, scholarship citations, and "Heretical" essay

**Status**: Phase 0 (Heretical Essay Research) **ACTIVE**; Phase 1-Alpha (Four-Text Editions + Angelology) **READY FOR DISPATCH** 2026-09-25

**Live Site** (when built): https://t3dy.github.io/Pico900  
**Repository**: https://github.com/t3dy/Pico900

---

## What We've Built

### 1. Agentic Architecture
A deterministic, checkpointed multi-agent system for scholarly research at scale.

**Key Principles**:
- **Deterministic chunking**: Work is pre-assigned by section (no chaos, no race conditions)
- **Progressive context isolation**: Each agent gets ONLY their role context + task data (~2–15k tokens, not 50k bloat)
- **Phase gates with validation**: Output reviewed before next phase touches it
- **One-writer-per-file always**: ORCHESTRATOR manages all manifest writes atomically
- **Section-level checkpointing**: Recover from agent failure without restarting entire phase
- **Token budgeting**: Measured spend per phase; retrospectives after each phase to improve

**Agent Roles**:
- **HARVESTER**: Extract sources (megabase, PicoDB) → JSON
- **PORTER**: Standardize format → Pico900 entries
- **SYNTHESIZER**: Research, write, enhance → exegeses + citations
- **REVIEWER**: Validate against STYLE_GUIDE
- **ORCHESTRATOR**: Coordinate, validate, dispatch, update manifest

### 2. System Documentation
**Files Created**:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project bootloader: purpose, phases, constraints, status |
| `DECISIONS.md` | All architectural decisions logged with rationale |
| `DEPLOY_STATE.md` | GitHub Pages deployment config + base-path gotchas |
| `docs/ORCHESTRATION.md` | Agent lifecycle, phase structure, concurrency rules, handover protocol |
| `docs/CONTEXT_ARCHITECTURE.md` | What each agent receives; progressive revelation strategy |
| `docs/STYLE_GUIDE.md` | Entry template, citation format, quality checklist, heretical notes |
| `docs/SOURCING_PROTOCOL.md` | Where to find translations (megabase, PicoDB, critical edition) |
| `docs/AGENT_SWARM_PATTERNS.md` | Role definitions, handover protocols, parallel execution |
| `docs/HERETICAL_RESEARCH_PLAN.md` | Phase 0 specifics: 13 condemned conclusions, four pillars framework |
| `PHASE_0_RESEARCH_QUEUE.json` | Work tickets for heretical essay (6 tasks with prerequisites) |
| `PHASE_0_DISPATCH_LOG.md` | Live dispatch log (updated as agents complete) |
| `scripts/bootstrap_project.py` | Infrastructure generator (creates manifest, schema, queues) |

### 3. Research Foundation
**Existing Work Harvested**:
- ~100 translated conclusions in megabase (2025-07-04 file)
- Copenhaver *Pico on Trial* summary + analysis (megabase 2025-07-05)
- 15+ PicoDB study passes on Kabbalah, astrology, angelology, biography
- 73 Renaissance Magic corpus sources (Wirszubski, Edelheit, Howlett, Dougherty, Black, Akopyan, Allen)
- Critical edition (free): https://cds.lib.brown.edu/cds-project/picos-900-theses

### 4. Quality Standards
**Scholarly Rigor**:
- No unsourced assertions
- Verbatim quotations required (not paraphrase)
- Confidence levels marked: [VERIFIED], [CITED], [INFERRED]
- Provenance on every entry (source + translator)
- Heretical conclusions have extended "charge, defense, debate" sections

**Process Quality**:
- Schema validation (all entries match allowed fields)
- Citation linting (checks every [VERIFIED] has a quotation)
- Phase gates (output validated before next phase)
- Retrospectives (learn from each phase before scaling)

---

## Phase 0: Heretical Essay Research (Current)

**Objective**: Research the 13 condemned conclusions from the 1486 papal trial. Output: essay outline + citation map. Use this as a learning ground to validate pipeline methodology before scaling to 900.

**Duration**: 1–2 sessions, 150k tokens max

**Why Start Here?**
- Heretical essay is high-value + focused scope (13 conclusions, deep scholarship)
- Copenhaver + Dougherty + Edelheit + Howlett = bounded research surface
- Learn pipeline efficiency on a real output before scaling
- Proof-of-concept for the entire system

**Workflow**:

```
H1-HARVESTER (Extract 13 condemned theses from Copenhaver + PicoDB)
    ↓ [validate JSON structure]
P1-PORTER (Standardize into Pico900 format, IDs H.1.1–H.1.13)
    ↓ [validate schema]
S1-HERETICAL (Research charge, defense, debate for each conclusion)
    ↓ [collect findings]
S2-HERETICAL-ESSAY (Draft essay outline organized by theme)
    ↓ [collect essay skeleton]
R1-REVIEWER (Validate entries + essay against STYLE_GUIDE)
    ↓ [approve or request revision]
RETROSPECTIVE (Analyze results, report improvements for Phase 1)
```

**Current Status**:
- ✓ H1-HARVESTER dispatched (running in background)
- ⏳ P1-PORTER queued (awaiting H1 output)
- ⏳ S1 + S2 queued (awaiting P1 output)
- ⏳ R1 queued (awaiting S1 + S2 output)
- ⏳ RETROSPECTIVE queued (awaiting R1 approval)

**Deliverables**:
1. `data/conclusions/Heretical/entry_H.1.1–H.1.13.json` (13 enhanced entries with charge + defense + debate)
2. `docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md` (essay skeleton organized by theme: Incarnation, Eucharist, Soul/Intellect, Kabbalah/Magic, Other)
3. `docs/PHASE_0_REPORT.md` (retrospective: what worked, what's slow, improvements for Phase 1)

**Success Criteria** (all must pass):
- ✓ All 13 condemned conclusions identified
- ✓ Heretical entries have "charge, defense, debate" sections
- ✓ All scholarly citations verified or marked [CITED]
- ✓ Essay outline coherent and well-sourced
- ✓ Retrospective identifies concrete pipeline improvements

---

## Phase 1-Alpha: Four-Text Digital Editions + Angelology (NEW 2026-09-25)

**Objective**: Create parallel digital editions for *Oration*, *Commento*, *Heptaplus*, and *On Being and Unity* with angelology-focused commentary. Extract 97 angelology passages across four texts, synthesize cross-text exegeses, build shared scholarship database.

**Why Angelology Now?**
- Heretical conclusions Q1, Q6, Q8 cluster around divine embodiment—incomprehensible without angelology
- Four texts are philosophically unified via Pico's angelic synthesis (Pseudo-Dionysius + Aquinas + Kabbalah + Plotinus)
- 900 Conclusions contain entire sections on celestial magic + Kabbalah (angelic invocations)
- Parallel execution doesn't block main 900 pipeline

**Infrastructure Created**:
- **ANGELICRESEARCH.md** (7,000 words): Comprehensive angelology research guide
  - Four philosophical lineages with texts + scholarly consensus
  - Theme cross-text mapping table
  - Specific HARVESTER tasks (12-50 passages per text)
  - Scholarly debate log (Wirszubski vs. Allen, Howlett vs. Black, etc.)
  
- **data/texts/TEXTS_SCHEMA.json**: Entry templates + Phase 1-Alpha task descriptions
- **data/texts/EDITION_MANIFESTS.json**: Detailed work queues (H2-A–R1-A)
- **HANDOVER_PHASE_1_ALPHA.md**: Dispatch guide

**Workflow**:
```
HARVESTER H2-A, H3-A, H4-A, H5-A (extract angelology from 4 texts, parallel)
    ↓ [validate JSON structure]
PORTER P1-A, P2-A, P3-A, P4-A (standardize into conclusion entries, parallel)
    ↓ [validate schema]
SYNTHESIZER S1-A, S2-A (write cross-text exegeses + shared scholarship DB, parallel)
    ↓ [collect findings]
REVIEWER R1-A (validate against ANGELICRESEARCH.md + STYLE_GUIDE.md)
    ↓ [approve]
[APPROVED] → Four digital editions ready for deployment
```

**Current Status**:
- ✓ ANGELICRESEARCH.md written
- ✓ Infrastructure complete (schemas, manifests, handover)
- ⏳ H2-A–H5-A queued for dispatch
- ⏳ P1-A–P4-A awaiting HARVESTER output
- ⏳ S1-A, S2-A awaiting PORTER output
- ⏳ R1-A awaiting SYNTHESIZER output

**Deliverables**:
1. `data/texts/[oration|commento|heptaplus|being_unity]/entries/` (12-50 angelology entries per text)
2. `data/texts/[text]/exegeses/` (cross-text synthesis exegeses)
3. `data/scholarships/angels/` (shared angelology database: lineage tags + scholar debate log)
4. Four standalone digital editions (or integrated into Pico900) with facing-page Latin/English + angelology commentary

**Budget**: 80-90k tokens | **Wall-clock**: 8-12 hours (parallel execution) | **Priority**: HIGH

**Synergy with Phase 0**: As Phase 1-A agents work, they provide angelology context for heretical conclusions Q1, Q6, Q8. Phase 0 retrospective will note enrichment.

---

## Future Phases (Post-Phase 0)

### Phase 1: Harvest All 900 Conclusions
- 4 parallel HARVESTER agents extract translations from megabase + critical edition
- Input: ~100 already translated + ~800 new
- Output: ~95 staged JSON files (by section)
- Budget: 100k tokens

### Phase 2: Port All Conclusions
- 8 parallel PORTER agents standardize into Pico900 format
- Output: ~900 entry files
- Budget: 80k tokens

### Phase 3: Synthesize & Enhance
- 4 parallel SYNTHESIZER agents by research track (Heretical, Kabbalah, Astrology, Metaphysics)
- Output: Enhanced entries + full heretical essay + synthesis essays
- Budget: 200k tokens

### Phase 4: Review & Approve
- 2 REVIEWER agents validate all entries
- Output: Approved manifest
- Budget: 50k tokens

### Phase 5: Build & Deploy
- Generate static HTML, deploy to GitHub Pages
- Budget: 30k tokens

**Total estimated cost for 900 conclusions**: ~500k tokens (vs. ~1.5M if done serially or manually)

---

## Key Architectural Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Agent dispatch | Deterministic chunking | Reproducible, auditable, zero race conditions |
| Context size | Isolated (~5k per agent) | Token efficiency, reduce hallucination |
| Validation | Phase gates | Catch errors early, prevent cascading failures |
| Checkpointing | Section-level | Granular recovery without restarting entire phase |
| Writing | One-writer-per-file | Prevent manifest corruption, atomic updates |
| Communication | JSON + Markdown | Machine-readable work state, human-readable learnings |
| Learning | Retrospectives | Iterate methodology before scaling |
| Scholarship | Verbatim quotations | Maintain rigor, avoid synthesis drift |
| Translation | Harvest existing | Use megabase work first, supplement as needed |

---

## Next Steps (You, the User)

### Immediate (While H1-HARVESTER runs)
- Nothing; let it run. You'll be notified when it completes.

### After H1 Completes
- I'll validate the 13 conclusions were extracted correctly
- Dispatch P1-PORTER automatically
- Continue through the rest of Phase 0

### After Phase 0 Completes
- Review heretical essay outline + 13 entries
- Approve or request revision
- I'll generate Phase 0 retrospective with pipeline learnings
- Decide: iterate Phase 0 or proceed to Phase 1 (all 900)?

### Your Role Throughout
- **Review**: Read heretical essay outline when it's ready; approve or comment
- **Guide**: If you spot gaps or want to add your own commentary, flag it
- **Iterate**: If Phase 0 reveals pipeline problems, we fix before scaling
- **Write**: Add your own commentary to entries as you review them

---

## Token Economy

**Phase 0**: 150k tokens for learning ground
- Expensive on research (S1, S2) to maximize learning
- Generous on validation (R1) to catch quality issues early
- Rigorous retrospective (10k tokens) to identify improvements

**Scaling**: Once Phase 0 passes, Phase 1–5 estimated ~500k tokens total (efficient, learned methodology)

**Total project**: ~650k tokens (vs. ~1.5M if built serially or without agent infrastructure)

---

## Files You Can Read Anytime

- **`CLAUDE.md`** — Full project overview
- **`DECISIONS.md`** — Rationale behind all architectural choices
- **`docs/HERETICAL_RESEARCH_PLAN.md`** — What the heretical essay is researching
- **`PHASE_0_RESEARCH_QUEUE.json`** — Current work tickets and their status
- **`PHASE_0_DISPATCH_LOG.md`** — Live dispatch log (updated as agents complete)

---

## The Learning Loop

This system is built to iterate:

1. **Phase 0**: Research heretical essay (13 conclusions, bounded scope)
2. **Retrospective**: What worked? What's slow? (No point scaling broken methodology)
3. **Phase 1–5**: Apply learnings to all 900 conclusions
4. **Final retrospective**: What would we do differently on version 2?

The heretical essay itself becomes the proof-of-concept that the pipeline works.

---

**Status**: H1-HARVESTER running. Will notify on completion. Standing by.
