# Orchestration: Agent Lifecycle, Gates & Concurrency

How agents work, when they work, what they receive, and when they hand off.

## Agent Roles & Lifecycle

### ORCHESTRATOR
**Who**: Central coordinator (Claude session or dedicated agent).

**Responsibilities**:
- Reads work from queue (JSON manifests)
- Assigns work to agents by role + section
- Monitors agent status (started / in_progress / complete / failed)
- Collects outputs from agents
- **Performs all manifest writes** (atomic, one-at-a-time, no races)
- Validates output structure before gate passage
- Triggers phase transitions
- Writes phase reports

**Context received**: Full project context (CLAUDE.md, DECISIONS.md, all phase specs)

**Token budget**: ~20k per cycle (reading outputs + updating manifest + dispatch)

---

### HARVESTER (Role)
**Task**: Extract translations + data from megabase/PicoDB. Output: structured JSON.

**Lifecycle**:
1. ORCHESTRATOR assigns `PHASE_0_RESEARCH_QUEUE.json` entry to a HARVESTER agent
2. Agent receives:
   - Entry: `{ "task_id": "H1", "section": "Heretical conclusions", "sources": [...], "target_output": "stage_heretical.json" }`
   - `docs/SOURCING_PROTOCOL.md` (where to find stuff)
   - Relevant source file paths (megabase, PicoDB, PDF corpus)
3. Agent reads sources, extracts verbatim text, produces `data/staging/[section].json`
4. Agent reports status: "Complete. 13 conclusions harvested. Output: data/staging/stage_heretical.json"
5. ORCHESTRATOR validates structure, archives agent's session notes

**Concurrency**: Up to 4 HARVESTER agents in parallel (one per major source section, no file conflicts)

**Context received**: SOURCING_PROTOCOL.md + assigned queue entry only (~2k tokens)

**Token budget**: ~30k per agent (reading source files + extracting + JSON structuring)

---

### PORTER (Role)
**Task**: Convert harvested JSON into Pico900 standard format. Output: validated conclusion entries.

**Lifecycle**:
1. ORCHESTRATOR (after HARVESTER phase validation) assigns PORTER a section
2. Agent receives:
   - `data/staging/stage_[section].json` (output from HARVESTER)
   - `docs/STYLE_GUIDE.md` (entry template + format)
   - `data/schema.json` (allowed fields, tags, status values)
3. Agent converts harvested data into Pico900 entries, assigns IDs, validates schema
4. Agent produces `data/conclusions/[section]/entry_[id].json` (one per conclusion)
5. Agent reports: "Converted 13 heretical conclusions. Produced 13 entries. Status: sourced."
6. ORCHESTRATOR batch-validates all entries against schema

**Concurrency**: Up to 8 PORTER agents in parallel (one per section, separate output directories = no conflicts)

**Context received**: STYLE_GUIDE.md + schema.json + staging JSON for their section only (~3k tokens)

**Token budget**: ~25k per agent (parsing + reformatting + ID assignment + validation)

---

### SYNTHESIZER (Role)
**Task**: Enhance entries with exegeses, find scholarship citations, write essay outlines. Output: enriched conclusions + essay plans.

**Lifecycle**:
1. ORCHESTRATOR (after PORTER validation) assigns SYNTHESIZER a section + specialty
2. Agent receives:
   - `data/conclusions/[section]/` (ported entries)
   - `docs/STYLE_GUIDE.md` (citation format, confidence levels, heretical notes)
   - Relevant PicoDB excerpts (scholar profiles, source packets for their specialty)
   - For heretical work: `docs/HERETICAL_RESEARCH_PLAN.md` + Copenhaver/Dougherty excerpts
3. Agent writes exegeses, finds scholarship quotations (2–3 per conclusion), fills metadata
4. For heretical conclusions: agent writes "charge, defense, debate" sections
5. Agent produces:
   - Enhanced `data/conclusions/[section]/entry_[id].json` (with exegesis + citations)
   - `data/essays/heretical_outline_[subsection].md` (partial essay, if heretical)
6. Agent reports methodology: "Found citations in: Copenhaver p. 45–67, Dougherty ch. 3, Howlett p. 89. Confidence levels: 2 VERIFIED, 1 CITED."
7. ORCHESTRATOR collects outputs

**Concurrency**: Up to 4 SYNTHESIZER agents (one per major research track: Kabbalah, Astrology, Metaphysics, Heretical)

**Context received**: STYLE_GUIDE.md + assigned section entries + relevant PicoDB excerpts + research plan (~10k tokens)

**Token budget**: ~40k per agent (research + writing + citation work)

---

### REVIEWER (Role)
**Task**: Validate entries against STYLE_GUIDE.md. Approve or request revision.

**Lifecycle**:
1. ORCHESTRATOR assigns REVIEWER a batch of enhanced entries
2. Agent receives:
   - `docs/STYLE_GUIDE.md` (quality checklist)
   - `data/schema.json` (validation rules)
   - All enhanced entries for the section
   - Citation linter output (from `scripts/validate_citations.py`)
3. Agent checks:
   - Every scholarly claim has a verbatim quotation
   - Confidence levels are marked
   - Heretical conclusions have extended notes
   - Tags are valid
   - Entry structure matches schema
4. Agent produces:
   - Approval list: "Entries 1–13: APPROVED"
   - Revision requests: "Entry 5: Missing [VERIFIED] tag on Copenhaver citation. Entry 7: Exegesis too brief."
5. ORCHESTRATOR batches approved entries for manifest update

**Concurrency**: Up to 2 REVIEWER agents (validation doesn't benefit from parallelism; keep focused)

**Context received**: STYLE_GUIDE.md + schema.json + entries to review (~5k tokens per batch)

**Token budget**: ~15k per agent (validation is mostly checking, not generating)

---

## Phase Structure

### Phase 0: Heretical Essay Research (Learning Ground)
**Objective**: Research 13 condemned conclusions. Output: essay outline + citation map.

**Duration**: 1–2 sessions, 150k tokens max.

**Sequence**:
1. **HARVESTER** (1 agent, ~2 hours):
   - Extract heretical conclusions from Copenhaver *Pico on Trial* (megabase 2025-07-05)
   - Extract condemned theses from PicoDB
   - Output: `data/staging/stage_heretical.json` (13 conclusions + source passages)

2. **PORTER** (1 agent, ~1 hour):
   - Convert to Pico900 format
   - Output: `data/conclusions/Heretical/*.json` (13 entries, status="sourced")

3. **SYNTHESIZER** (2 agents, ~4 hours, parallel):
   - **S1-HERETICAL**: Research charge, defense, debate for each conclusion. Find 3–4 quotations per conclusion (Copenhaver, Dougherty, Howlett, Edelheit).
   - **S1-ESSAY**: Draft essay outline organized by theme (Incarnation, Eucharist, Soul/Intellect, Kabbalah, Other). Integrate quotations.
   - Output: Enhanced entries + `docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md`

4. **REVIEWER** (1 agent, ~1 hour):
   - Validate citations (all [VERIFIED] or [CITED] tags have quotations)
   - Check heretical notes completeness
   - Output: Approval list or revision requests

5. **RETROSPECTIVE** (Claude, ~30 min):
   - Write `docs/PHASE_0_REPORT.md`
   - Questions: Did we find all condemned conclusions? Were citations accurate? What was slow?
   - Learnings: Refine SYNTHESIZER workflow before scaling to 900

**Gate**: Phase 0 complete when heretical essay outline is approved and citations are verified.

---

### Phase 1: Harvest All 900 Conclusions
**Objective**: Extract translations from megabase + critical edition. Output: staged JSON for all 95+ known conclusions.

**Duration**: 1 session, 100k tokens max.

**Sequence**: Same as Phase 0, but with 4 parallel HARVESTER agents (one per major source section)

---

### Phase 2: Port All Conclusions
**Objective**: Standardize into Pico900 format. Output: schema-valid entry files.

**Duration**: 1 session, 80k tokens.

**Sequence**: 8 parallel PORTER agents (one per section)

---

### Phase 3: Synthesize & Enhance
**Objective**: Add exegeses, scholarship citations, tags. Output: enriched entries.

**Duration**: 2 sessions, 200k tokens.

**Sequence**: 4 parallel SYNTHESIZER agents (Heretical, Kabbalah, Astrology, Metaphysics/Logic)

---

### Phase 4: Review & Approve
**Objective**: Validate all entries. Output: approved manifest.

**Duration**: 1 session, 50k tokens.

**Sequence**: Batch review (2 agents, concurrent on different sections)

---

### Phase 5: Build & Deploy
**Objective**: Generate static HTML, deploy to GitHub Pages.

**Duration**: 1 session, 30k tokens.

**Sequence**: Single agent (build process is deterministic, not parallelizable)

---

## Work Queues & Tickets

**File**: `PHASE_[N]_RESEARCH_QUEUE.json`

Example (Phase 0):
```json
{
  "phase": 0,
  "phase_name": "Heretical Essay Research",
  "status": "active",
  "total_token_budget": 150000,
  "phase_start": "2026-09-25T18:00:00Z",
  "tickets": [
    {
      "task_id": "H1",
      "role": "HARVESTER",
      "section": "Heretical conclusions (13 theses)",
      "sources": [
        "C:\\Dev\\megabase\\chats_2025\\2025-07-05_Pico della Mirandola Summary.md",
        "C:\\Dev\\PicoDB\\artifacts\\essays\\pico_kabbalah_synthesis_longform_draft.md"
      ],
      "target_output": "data/staging/stage_heretical.json",
      "status": "queued",
      "assigned_to": null,
      "started_at": null,
      "completed_at": null,
      "token_budget": 30000,
      "notes": "Extract the 13 condemned conclusions from Copenhaver's account. Look for papal commission charge, Pico's defense, modern scholarship debate."
    },
    {
      "task_id": "P1",
      "role": "PORTER",
      "section": "Heretical conclusions",
      "input": "data/staging/stage_heretical.json",
      "target_output": "data/conclusions/Heretical/",
      "status": "queued",
      "assigned_to": null,
      "started_at": null,
      "completed_at": null,
      "token_budget": 25000,
      "prerequisites": ["H1"],
      "notes": "Assign IDs (H.1.1 through H.1.13). Mark status='sourced'."
    },
    {
      "task_id": "S1-HERETICAL",
      "role": "SYNTHESIZER",
      "specialty": "heretical_conclusions",
      "section": "Heretical conclusions",
      "input": "data/conclusions/Heretical/",
      "target_output": "data/conclusions/Heretical/ (enhanced) + data/essays/heretical_charge_defense_debate.md",
      "status": "queued",
      "assigned_to": null,
      "started_at": null,
      "completed_at": null,
      "token_budget": 50000,
      "prerequisites": ["P1"],
      "research_scope": "Copenhaver, Dougherty, Howlett, Edelheit. For each of 13 conclusions: (1) state the charge, (2) cite Pico's defense from Apology if available, (3) synthesize modern debate. Minimum 3 quotations per conclusion.",
      "notes": "This is the learning ground. Record methodology in output: what sources were most useful? What patterns emerged?"
    },
    {
      "task_id": "S2-ESSAY",
      "role": "SYNTHESIZER",
      "specialty": "heretical_essay_outline",
      "section": "Heretical conclusions",
      "input": "data/conclusions/Heretical/*.json (enhanced from S1) + docs/HERETICAL_RESEARCH_PLAN.md",
      "target_output": "docs/HERETICAL_ESSAY_OUTLINE.md",
      "status": "queued",
      "assigned_to": null,
      "started_at": null,
      "completed_at": null,
      "token_budget": 30000,
      "prerequisites": ["S1-HERETICAL"],
      "research_scope": "Organize 13 conclusions by theme: (1) Incarnation & Embodiment, (2) Eucharist & Transubstantiation, (3) Soul/Intellect/Immortality, (4) Kabbalah/Magic, (5) Other. Write essay outline with integrated quotations from scholarship.",
      "notes": "Outputs become the skeleton of the final heretical essay."
    },
    {
      "task_id": "R1",
      "role": "REVIEWER",
      "section": "Heretical conclusions",
      "input": "data/conclusions/Heretical/*.json (enhanced) + docs/HERETICAL_ESSAY_OUTLINE.md",
      "target_output": "data/review_approval_HERETICAL.json",
      "status": "queued",
      "assigned_to": null,
      "started_at": null,
      "completed_at": null,
      "token_budget": 15000,
      "prerequisites": ["S1-HERETICAL", "S2-ESSAY"],
      "validation_rules": [
        "Every scholarly claim has a verbatim quotation",
        "Confidence levels marked: [VERIFIED] or [CITED] only",
        "Heretical conclusions have 'charge, defense, debate' sections",
        "Tags valid: ['heretical', 'theology', 'scholasticism', 'humanistic']",
        "Entry schema matches docs/schema.json"
      ],
      "notes": "Approve or request revision. If approved, entries move to manifest."
    }
  ]
}
```

---

## Handover Protocol

When one agent completes, it hands off to the next via:

1. **Output file** (JSON or `.md`)
2. **Status update** to queue ticket (marked "complete")
3. **Session notes** (Markdown summary of methodology, surprises, bottlenecks)
4. **ORCHESTRATOR validation** (checks output structure)
5. **Prerequisite gate** (next agent's tickets stay "queued" until prerequisites are "complete")

Example flow:
```
H1: HARVESTER produces stage_heretical.json
    ↓ (ORCHESTRATOR validates JSON structure)
    ↓ (ORCHESTRATOR marks H1 ticket "complete")
    ↓ (P1 ticket prerequisite satisfied, status changes to "ready")
    ↓ (ORCHESTRATOR assigns P1 to PORTER agent)
P1: PORTER consumes stage_heretical.json, produces 13 entry files
    ↓ (ORCHESTRATOR validates schema)
    ↓ (marks P1 "complete")
    ↓ (S1 and S2 prerequisites satisfied, status change to "ready")
S1 + S2: Two SYNTHESIZER agents work in parallel
    ↓
R1: REVIEWER validates, approves
    ↓
ORCHESTRATOR: Batch-updates manifest with approved entries
```

---

## Concurrency Constraints

**Hard rules**:
- Only ONE agent writes to `data/conclusions_manifest.json` (ORCHESTRATOR)
- Only ONE agent writes to each section's output directory (e.g., only one PORTER agent writes to `data/conclusions/Heretical/`)
- Read-only access is shared (all PORTER agents can read from `data/staging/`)

**Soft constraints** (performance, not safety):
- Max 4 HARVESTER agents in parallel (diminishing returns beyond that)
- Max 8 PORTER agents (one per section)
- Max 4 SYNTHESIZER agents (one per research track)
- Max 2 REVIEWER agents (validation is IO-heavy, benefit from parallelism is low)

---

## Checkpointing & Recovery

If an agent fails mid-task:

1. ORCHESTRATOR detects timeout or error
2. Agent's output file is archived to `data/archives/[task_id]_partial.json`
3. Ticket is marked "failed"
4. ORCHESTRATOR can:
   - **Retry**: Assign to a fresh agent (all work is deterministic, safe to repeat)
   - **Resume**: If output is partial and resumable, agent re-reads checkpoint + continues from line N

Example: SYNTHESIZER-1 crashes after researching 8/13 conclusions.
- Output `data/conclusions/Heretical/entry_H.1.1-8.json` is archived
- Ticket noted: "S1 failed at conclusion 9/13"
- New SYNTHESIZER agent resumes: reads archived output, continues from conclusion 9

---

## Retrospectives & Learning

After each phase:

1. **Phase Report**: ORCHESTRATOR (or dedicated agent) writes `docs/PHASE_[N]_REPORT.md`
   - What was completed
   - Token spend vs. budget
   - Bottlenecks (which agents were slow?)
   - Surprises (what did we learn?)
   - Recommendations for next phase

2. **Methodology Review** (after Phase 0):
   - Did HARVESTER find all conclusions?
   - Did PORTER format correctly?
   - Was SYNTHESIZER research complete?
   - Were citations accurate?
   - **Decision**: Refine workflow before scaling, or proceed to Phase 1?

3. **Iteration**: Phase 0 learnings feed into Phase 1–5 planning

