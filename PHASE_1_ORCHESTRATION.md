# Phase 1 Orchestration: Sophisticated Multi-Agent Pipeline

**Framework**: Deterministic, section-based work assignment with parallel tracks and atomic manifest updates.

---

## System Architecture

```
┌─ HARVESTER H2 ──→ stage_S1.json ─┐
├─ HARVESTER H3 ──→ stage_S2.json ─┼─→ ORCHESTRATOR ──→ manifest update (gate 1)
├─ HARVESTER H4 ──→ stage_S3.json ─┤                     ↓
│  (H5–H8 follow)                   │             ┌─ PORTER P2 ──→ conclusions/S1/*.json
│                                   └─────────────┼─ PORTER P3 ──→ conclusions/S2/*.json
│                                                 ├─ PORTER P4 ──→ conclusions/S3/*.json
│                                                 │  (P5–P8 follow)
│                                                 │
│                                                 └─→ ORCHESTRATOR ──→ manifest update (gate 2)
│                                                      ↓
│                                   ┌─ REVIEWER R2 ──→ PHASE_1_SECTION_REPORT_S1.md
│                                   ├─ REVIEWER R3 ──→ PHASE_1_SECTION_REPORT_S2.md
│                                   ├─ REVIEWER R4 ──→ PHASE_1_SECTION_REPORT_S3.md
│                                   │  (R2–R4 cycle through sections)
│                                   │
│                                   └─→ ORCHESTRATOR ──→ manifest update (gate 3)
│                                                 ↓
│                                        RETROSPECTIVE ──→ PHASE_1_RETROSPECTIVE.md
└────────────────────────────────────────────────────────→ Final manifest + commit
```

---

## Agent Lifecycle & Dispatch Order

### Batch 1: Initial Parallel Dispatch (T+0)
**Agents**: H2, H3, H4  
**Task**: Extract first 3 sections (S1, S2, S3 = 300 conclusions)  
**Duration**: ~2 hours (parallel)  
**Output**: 3 `stage_*.json` files  

### Batch 2: First PORTER Wave (T+2h, or when H2 completes)
**Agent**: P2  
**Task**: Standardize S1 conclusions (wait for H2 to complete)  
**Duration**: ~30 min  
**Output**: `data/conclusions/S1/*.json`  

**In parallel (T+0, still running)**:
- H3 continues (S2)
- H4 continues (S3)
- H5 starts (S4)
- H6 starts (S5)
- (etc.)

### Batch 3: First REVIEWER Wave (T+2.5h, or when P2 completes)
**Agent**: R2  
**Task**: Validate S1 entries  
**Duration**: ~45 min  
**Output**: `docs/PHASE_1_SECTION_REPORT_S1.md`  

**In parallel (T+2h)**:
- P3 starts (S2, waits for H3)
- P4 starts (S3, waits for H4)

### Cascading Pattern
Each subsequent section follows the H→P→R pattern with no gaps. When R2 finishes S1, it immediately picks up S2 validation while P5 standardizes S4, and H7 extracts S5.

---

## Concurrency Rules

### Rule 1: One Writer Per File
- H2 writes only to `data/staging/stage_S1.json` (no conflicts with H3, H4, etc.)
- P2 writes only to `data/conclusions/S1/` (no conflicts with P3, P4)
- PORTER output files are per-section, per-agent (no merge conflicts)

### Rule 2: Atomic Manifest Updates
- Only ORCHESTRATOR writes to `data/conclusions_manifest.json`
- Manifest updated once per gate (not per agent)
- Update includes: section status, token usage, timestamp, approval status

### Rule 3: Sequential Gates (Per Section)
```
H[n] completes S[n] → ORCHESTRATOR validates output → 
P[n] starts S[n]   → ORCHESTRATOR validates output → 
R[n] starts S[n]   → ORCHESTRATOR validates output → 
Manifest updated   → Next section begins
```

No agent waits for another section's completion; only for its own predecessor in the H→P→R chain.

### Rule 4: No Agent Context Overlap
- HARVESTER doesn't receive STYLE_GUIDE (unnecessary)
- PORTER doesn't receive SOURCING_PROTOCOL (already executed)
- REVIEWER doesn't receive CRITICAL_EDITION_TAXONOMY (doesn't need source info)

Each agent receives **only** what it needs. ~30% token savings vs. full-context approach.

---

## Quality Gates & Validation

### Gate 1: HARVESTER Output Validation
**Trigger**: H[n] completes, writes `data/staging/stage_[section].json`  
**Validator**: ORCHESTRATOR (automated check)  
**Checks**:
- [ ] File is valid JSON
- [ ] All fields present (latin_incipit, english_translation, charge, defense, etc.)
- [ ] Count = expected conclusions for section (100±5 for variance)
- [ ] No duplicate entries

**Action if failed**:
- Flag error in manifest
- Do NOT dispatch P[n]
- Notify user: "H[n] output validation failed for section [section]; awaiting review"

---

### Gate 2: PORTER Output Validation
**Trigger**: P[n] completes, writes 100 JSON files to `data/conclusions/[section]/`  
**Validator**: ORCHESTRATOR (automated check)  
**Checks**:
- [ ] All 100 files present
- [ ] Each file is valid JSON
- [ ] ID formatting correct: `S[1-8].C[1-100]`
- [ ] All required schema fields populated
- [ ] No parse errors

**Action if failed**:
- Flag specific file(s) that failed
- Do NOT dispatch R[n] for this section
- Notify user: "P[n] schema validation failed for [file]; awaiting revision"

---

### Gate 3: REVIEWER Output Validation
**Trigger**: R[n] completes, writes `docs/PHASE_1_SECTION_REPORT_[section].md`  
**Validator**: ORCHESTRATOR + final user review  
**Checks**:
- [ ] Report is well-formed Markdown
- [ ] All entries assessed against STYLE_GUIDE
- [ ] Gap count recorded (missing translations, incomplete scholarship)
- [ ] Quality threshold achieved (2–3 citations per entry minimum)

**Action if passed**:
- Mark section as APPROVED in manifest
- Proceed to next section

**Action if failed**:
- Flag specific entries for revision
- Requeue P[n] to fix those entries only
- Requeue R[n] to re-validate

---

## Manifest Tracking

**File**: `data/conclusions_manifest.json`  
**Structure**:
```json
{
  "phase": "1",
  "total_sections": 8,
  "sections": [
    {
      "section_id": "S1",
      "section_name": "Secundum Platonicos",
      "conclusion_count": 95,
      "status": "approved",
      "harvester_agent": "H2",
      "porter_agent": "P2",
      "reviewer_agent": "R2",
      "gates": {
        "harvest_gate": { "status": "passed", "timestamp": "2026-09-25T14:30:00Z" },
        "porter_gate": { "status": "passed", "timestamp": "2026-09-25T15:00:00Z" },
        "review_gate": { "status": "passed", "timestamp": "2026-09-25T15:45:00Z" }
      },
      "token_usage": {
        "harvester": 42000,
        "porter": 28000,
        "reviewer": 15000
      },
      "gaps": {
        "missing_translations": 3,
        "incomplete_scholarship": 2
      }
    },
    ...
  ],
  "retrospective": {
    "timestamp": "2026-09-26T12:00:00Z",
    "total_tokens_used": 348000,
    "bottlenecks": [...],
    "improvements_for_phase_2": [...]
  }
}
```

---

## Token Budgeting

| Agent Type | Per Section | Sections | Total |
|------------|------------|----------|-------|
| HARVESTER | 40k | 8 | 320k |
| PORTER | 26k | 8 | 208k |
| REVIEWER | 50k (shared across 3 agents) | 8 | 150k |
| **Subtotal** | | | **678k** |
| RETROSPECTIVE | — | — | 50k |
| **TOTAL** | | | **728k** |

*Note: This is higher than the 350k estimate in ROADMAP because I'm tracking three REVIEWER agents. Actual parallelization will reduce wall-clock time. Budget revised upward to ensure quality.*

---

## Recovery Protocol (If Agent Fails)

**If H[n] fails mid-section**:
- Manifest marks status as FAILED
- Checkpoint saved: `data/staging/stage_[section]_checkpoint.json`
- H[n] reruns from checkpoint (no re-work)

**If P[n] fails mid-section**:
- Manifest marks status as FAILED
- PORTER restarts (fast: only needs to re-standardize, ~10 min)
- P[n] writes to temp location first, then renames to final on success

**If R[n] fails mid-section**:
- Report is incomplete; R[n] reruns from start (agents generate fresh reports each time)
- Previous partial report archived with timestamp

---

## How ORCHESTRATOR Works

**Role**: Automated coordinator (not an agent; part of the system)

**Responsibilities**:
1. Monitor agent completion (via dispatch log)
2. Validate output at each gate
3. Update manifest atomically
4. Determine which agent to dispatch next
5. Log all decisions to `PHASE_1_DISPATCH_LOG.md`

**Execution** (runs between agent dispatches):
- Read latest dispatch log
- Check for completed agents
- Validate their output
- Update manifest + dispatch next agent

**Not responsible for**:
- Writing agent context (that's done at dispatch)
- Writing final entries (agents do that)
- Approving quality (REVIEWER does that)

---

## Phase 1 Completion Criteria

**All of the following must be true**:
- [ ] All 8 sections processed through H→P→R gates
- [ ] Manifest shows all sections = APPROVED
- [ ] Section reports filed for all 8 sections
- [ ] Token usage ≤ 350k (or within justified overage)
- [ ] Retrospective identifies 3+ concrete improvements for Phase 2
- [ ] Zero critical gaps remaining (missing translations, incomplete scholarship)

**If any criterion fails**:
- Fix identified issues before marking Phase 1 COMPLETE
- Do not proceed to Phase 2 until all criteria pass

---

## Phase 1 Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Conclusions extracted | 900 | TBD |
| Schema compliance | 100% | TBD |
| Avg citations per entry | 2.5 | TBD |
| Gate 1 pass rate | 100% | TBD |
| Gate 2 pass rate | 100% | TBD |
| Gate 3 pass rate | 95%+ | TBD |
| Token efficiency | ≤350k | TBD |
| Wall-clock time | ≤8 hours | TBD |

---

## Example: Section S1 Execution

**T+0:00 — H2 dispatched**
- Task: Extract 95 Platonic conclusions
- Context: `SOURCING_PROTOCOL.md` + S1 incipit list
- Budget: 40k tokens
- Output: `data/staging/stage_S1.json`

**T+1:30 — H2 completes, ORCHESTRATOR validates**
- Checks: 95 entries, valid JSON, all fields present ✓
- Manifest updated: S1 harvest_gate = PASSED
- Logs: `PHASE_1_DISPATCH_LOG.md` records completion

**T+1:35 — P2 dispatched**
- Task: Standardize S1 conclusions
- Context: `STYLE_GUIDE.md` + `data/staging/stage_S1.json`
- Budget: 26k tokens
- Output: `data/conclusions/S1/*.json` (95 files)

**T+2:05 — P2 completes, ORCHESTRATOR validates**
- Checks: 95 files, valid schema, IDs formatted correctly ✓
- Manifest updated: S1 porter_gate = PASSED
- Logs: `PHASE_1_DISPATCH_LOG.md` records completion

**T+2:15 — R2 dispatched**
- Task: Validate S1 entries
- Context: `STYLE_GUIDE.md` + `data/conclusions/S1/*.json`
- Budget: 50k tokens (R2 handles S1–S3, then S4–S6, then S7–S8)
- Output: `docs/PHASE_1_SECTION_REPORT_S1.md`

**T+3:00 — R2 completes, ORCHESTRATOR validates**
- Report present ✓
- Gaps logged: 2 missing translations, 1 incomplete scholarship citation
- Manifest updated: S1 review_gate = PASSED (with notes)
- Logs: `PHASE_1_DISPATCH_LOG.md` records completion + gap count

**T+3:05 — Next section (S2) ready**
- If H3 is done: P3 dispatches immediately
- If H3 not yet done: P3 waits (no idle time; H3 is still running in parallel)

---

## Dispatch Log Template

**File**: `PHASE_1_DISPATCH_LOG.md`

```markdown
# Phase 1 Dispatch Log

| Timestamp | Agent | Task | Status | Output | Tokens | Notes |
|-----------|-------|------|--------|--------|--------|-------|
| 2026-09-25 14:00 | H2 | Extract S1 | Running | — | — | Parallel dispatch: H3, H4 also started |
| 2026-09-25 15:30 | H2 | Extract S1 | Complete | stage_S1.json | 41.2k | 95 entries, gate 1 passed |
| 2026-09-25 15:35 | P2 | Standardize S1 | Running | — | — | Waits for H2: done ✓ |
| ... | ... | ... | ... | ... | ... | ... |
```

---

## Next: Trigger Phase 1

When ready:
1. Update this file's success metrics table (leave TBD for now)
2. Create `data/PHASE_1_RESEARCH_QUEUE.json` with H2–H8 work tickets
3. Dispatch H2, H3, H4 with CRITICAL_EDITION_TAXONOMY.md context
4. Monitor dispatch log; ORCHESTRATOR handles gate validation

Phase 1 launches when you say "go."
