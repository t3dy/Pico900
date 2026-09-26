# Pico900 Agile Ticketing & Multi-Agent Orchestration System

This document describes the sophisticated, deterministic multi-agent coordination system used for Phase 1 and beyond.

---

## System Overview

**Architecture**: Deterministic section-based work assignment with parallel agent tracks, atomic manifest updates, and phase gates.

**Why deterministic?**: 
- Work is pre-assigned by section, not dynamically stolen
- Zero race conditions (each agent writes to its own output location)
- Reproducible and auditable (same section always goes to same agent on retry)
- Simpler recovery (if H2 fails on S1, restart H2 on S1; no ambiguity)

**Why section-based?**:
- 900 conclusions is too large for one-agent passes
- 8 sections of ~100 conclusions each = good parallelization
- Checkpointing per-section = manageable and traceable

---

## Three Agent Roles

### HARVESTER (H[n])
**Job**: Extract Latin, find translations, collect scholarship quotations  
**Input**: Section assignment + SOURCING_PROTOCOL.md + CRITICAL_EDITION_TAXONOMY.md  
**Output**: `data/staging/stage_[section].json` with charge, defense, quotations  
**Token budget**: 40k per section  
**Concurrency**: 4–8 agents run in parallel (one per section)  

**Context isolation**:
- Does NOT receive STYLE_GUIDE (doesn't write entries)
- Does NOT receive full essay outline (doesn't need it)
- Receives ONLY section-specific incipit list + sourcing guidance

### PORTER (P[n])
**Job**: Standardize into Pico900 schema, assign IDs, validate structure  
**Input**: `data/staging/stage_[section].json` (from HARVESTER)  
**Output**: `data/conclusions/[section]/*.json` (100 JSON files)  
**Token budget**: 26k per section  
**Concurrency**: Waits for corresponding HARVESTER, then processes immediately  

**Context isolation**:
- Does NOT receive SOURCING_PROTOCOL (sources already found)
- Receives STYLE_GUIDE only (needs it for validation)
- Receives ONLY the staging JSON for their section

### REVIEWER (R[n])
**Job**: Validate entries against STYLE_GUIDE, flag gaps, generate section report  
**Input**: `data/conclusions/[section]/*.json` (completed entries from PORTER)  
**Output**: `docs/PHASE_1_SECTION_REPORT_[section].md` (validation report)  
**Token budget**: 50k (shared across 3 agents processing all sections)  
**Concurrency**: Starts after each section's PORTER completes  

**Context isolation**:
- Receives STYLE_GUIDE + QUALITY_CHECKLIST only
- Does NOT receive source materials (doesn't need to re-verify sources)
- Receives ONLY the JSON entries to review

---

## Orchestration Flow

### Gate 1: HARVESTER Output Validation
```
HARVESTER completes section → 
  writes data/staging/stage_[section].json → 
    ORCHESTRATOR validates:
      ✓ Valid JSON
      ✓ All fields present
      ✓ Count matches expected
      ✓ No duplicates
    → Manifest updated: harvest_gate = PASSED
    → PORTER dispatched (for this section only)
```

### Gate 2: PORTER Output Validation
```
PORTER completes section → 
  writes data/conclusions/[section]/*.json → 
    ORCHESTRATOR validates:
      ✓ All files present
      ✓ Valid JSON in each
      ✓ Schema correct
      ✓ IDs formatted correctly
    → Manifest updated: porter_gate = PASSED
    → REVIEWER dispatched (for this section only)
```

### Gate 3: REVIEWER Output Validation
```
REVIEWER completes section → 
  writes docs/PHASE_1_SECTION_REPORT_[section].md → 
    ORCHESTRATOR validates:
      ✓ Report is valid Markdown
      ✓ All entries assessed
      ✓ Quality threshold met (2–3 citations minimum)
      ✓ Gaps logged
    → Manifest updated: review_gate = PASSED
    → Next section begins H→P→R cycle
```

---

## Manifest as Source of Truth

**File**: `data/conclusions_manifest.json`

**Tracks**:
- Per-section status (queued → harvesting → porting → reviewing → approved)
- Agent assignments
- Gate completion timestamps
- Token usage per phase
- Quality metrics (gaps, missing citations)

**Updated by**: ORCHESTRATOR only (atomic writes; no race conditions)

**Read by**:
- Dispatch log (to decide what to dispatch next)
- REVIEWER (to assess quality)
- RETROSPECTIVE (to analyze bottlenecks)

**Example entry**:
```json
{
  "section_id": "S1",
  "section_name": "Secundum Platonicos",
  "status": "approved",
  "harvester_agent": "H2",
  "porter_agent": "P2",
  "reviewer_agent": "R2",
  "gates": {
    "harvest_gate": { "status": "passed", "timestamp": "2026-09-25T14:30:00Z" },
    "porter_gate": { "status": "passed", "timestamp": "2026-09-25T15:00:00Z" },
    "review_gate": { "status": "passed", "timestamp": "2026-09-25T15:45:00Z" }
  },
  "token_usage": { "harvester": 41200, "porter": 28000, "reviewer": 15000 },
  "gaps": { "missing_translations": 2, "incomplete_scholarship": 1 }
}
```

---

## Recovery Protocol

**If H[n] fails**:
1. Manifest shows harvest_gate = FAILED for section [n]
2. Checkpoint saved: `data/staging/stage_[section]_checkpoint.json`
3. H[n] reruns (picks up from checkpoint if partial work exists)
4. On success, ORCHESTRATOR validates and dispatches P[n]

**If P[n] fails**:
1. Manifest shows porter_gate = FAILED for section [n]
2. PORTER reruns (fast; only needs to re-standardize, ~15 min)
3. Writes to temp location first; renames on success (atomic write)
4. On success, ORCHESTRATOR validates and dispatches R[n]

**If R[n] fails**:
1. Manifest shows review_gate = FAILED for section [n]
2. REVIEWER reruns (generates fresh report)
3. On success, section marked APPROVED

**Key principle**: No cascading failures. If one section fails, only that section is restarted; other sections continue independently.

---

## Parallelization Strategy

### Ideal timeline:
```
T+0:00     H2 → S1 | H3 → S2 | H4 → S3
T+1:30     H2 done, P2 starts S1
           H5 → S4 | H6 → S5 | H7 → S6 (continue in parallel)
T+2:00     P2 done, R2 starts S1
           H3 done (S2), P3 starts S2
T+2:45     P3 done (S2), R2 starts S2 validation (while still on S1 if needed)
           H4 done (S3), P4 starts S3
...and so on
```

### Wall-clock time:
- **Sequential (one section at a time)**: 8 sections × 3 hours/section = 24 hours
- **Parallel (3 HAWest at once)**: 24 hours ÷ 3 + setup = ~8–10 hours

**Actual achieved**: Depends on agent speed (may be faster or slower than estimate)

---

## Quality Assurance

### STYLE_GUIDE
All entries must pass:
- [ ] Latin incipit present and verified against critical edition
- [ ] English translation sourced (megabase, scholarly translation, or marked original)
- [ ] Charge section complete (what was condemned + papal charge)
- [ ] Defense section complete (Pico's response + scholastic framework)
- [ ] Scholar citations: 2–3 minimum, verified or marked [TO_SOURCE]
- [ ] No spelling errors in Latin or English
- [ ] JSON schema valid
- [ ] Tags populated (heretical, section, themes)

### Per-Section Report
REVIEWER generates markdown report for each section containing:
1. Summary (count, completeness %)
2. Quality metrics (avg citations per entry, gaps)
3. Specific gaps (which entries are missing translations, incomplete)
4. Recommendations (additional sources to pursue, patterns observed)

### Final Retrospective
After all sections complete, RETROSPECTIVE agent analyzes:
1. Total token usage vs. budget
2. Which sections were slowest/fastest
3. Quality trends (did later sections improve in quality?)
4. Bottlenecks (was it HARVESTER, PORTER, or REVIEWER that slowed progress?)
5. Recommendations for Phase 2

---

## Dispatch Sequence

### Phase 1, Wave 1 (T+0)
```
# Dispatch H2, H3, H4 in parallel
claude dispatch H2 --section=S1 --context=HARVESTER
claude dispatch H3 --section=S3 --context=HARVESTER
claude dispatch H4 --section=S4 --context=HARVESTER
```

### Phase 1, Wave 2 (T+2h, or when first HAWest completes)
```
# Wait for H2 to complete
# Dispatch P2 (waits for stage_S1.json)
# Dispatch H5, H6, H7 (next sections)
claude dispatch P2 --section=S1 --context=PORTER --input=data/staging/stage_S1.json
claude dispatch H5 --section=S2 --context=HARVESTER
claude dispatch H6 --section=S5 --context=HARVESTER
claude dispatch H7 --section=S6 --context=HARVESTER
```

### Phase 1, Wave 3 (T+2.5h, or when first PORTER completes)
```
# Wait for P2 to complete
# Dispatch R2 (validates stage_S1)
# Dispatch P3 (waits for stage_S3.json from H3)
# Dispatch P4 (waits for stage_S4.json from H4)
claude dispatch R2 --section=S1 --context=REVIEWER --input=data/conclusions/S1/
claude dispatch P3 --section=S3 --context=PORTER --input=data/staging/stage_S3.json
claude dispatch P4 --section=S4 --context=PORTER --input=data/staging/stage_S4.json
```

(Pattern continues until all sections complete)

---

## Metrics Dashboard

**Tracked in manifest**:
- Sections completed
- Avg tokens per section
- Avg time per section
- Gate pass rate (should be 100%)
- Quality score (avg citations, gaps per section)

**Report generated by RETROSPECTIVE**:
- Phase 1 total token cost
- Wall-clock time (actual vs. estimated)
- Bottlenecks identified
- Specific improvements for Phase 2

**Updated live in**:
- `data/conclusions_manifest.json` (machine-readable)
- `PHASE_1_DISPATCH_LOG.md` (human-readable)
- Terminal output during dispatches

---

## Key Design Principles

1. **Deterministic**: Work assigned in advance, not dynamically stolen
2. **Atomic**: Manifest updated once per gate completion (no partial states)
3. **Auditable**: Every decision logged; every agent's output validated
4. **Recoverable**: If an agent fails, only that section is restarted
5. **Parallel**: Independent sections run in parallel; no artificial serialization
6. **Lean context**: Each agent receives only what it needs (30% token savings)

---

## Integration with Git

**After each section completes**:
1. Section report added to git
2. Checkpoint manifest committed
3. Dispatch log committed
4. Message: "Phase 1, S[n] complete: 95 conclusions, all gates passed"

**After Phase 1 complete**:
1. All sections merged
2. Final manifest committed
3. Retrospective report committed
4. Message: "Phase 1 complete: 900 conclusions, ready for Phase 2"

---

## How to Use This System

### To start Phase 1:
1. Run `PHASE_1_RESEARCH_QUEUE.json` to trigger Wave 1 agent dispatch
2. Monitor `PHASE_1_DISPATCH_LOG.md` for completion
3. ORCHESTRATOR handles gate validation automatically
4. When all sections complete, RETROSPECTIVE generates analysis

### To add a new section:
1. Add entry to `PHASE_1_RESEARCH_QUEUE.json`
2. Add entry to `docs/CRITICAL_EDITION_TAXONOMY.md`
3. Dispatcher will pick it up on next wave

### To pause mid-phase:
1. Don't dispatch new agents
2. Allow in-flight agents to complete
3. Manifest checkpoint saved; resume from there

### To restart after failure:
1. Check manifest for failed section
2. Dispatch replacement agent for that section only
3. Other sections unaffected

---

## Sophisticated Features

1. **Wave-based dispatch**: Tier 1 (high-priority sections) first; Tier 3 (large sections) last
2. **Section priority tracking**: CRITICAL_EDITION_TAXONOMY.md ranks sections by research coverage
3. **Adaptive token budgeting**: Budget per agent adjusts based on section size + difficulty
4. **Gap analysis per section**: REVIEWER reports exactly which entries are incomplete
5. **Retrospective analysis**: Identifies bottlenecks and suggests improvements
6. **Atomic manifest**: No race conditions, reliable source of truth
7. **Context isolation**: 30% token savings by not sending unnecessary data to agents

---

## Next Steps

1. User approves Phase 1 roadmap + orchestration plan
2. H2, H3, H4 dispatched for Wave 1 (S1, S3, S4)
3. Monitor dispatch log + manifest for progress
4. Sections complete in waves; RETROSPECTIVE runs after all sections done
5. Results reviewed; Phase 2 gates evaluated

**Phase 1 is ready to launch on user approval.**
