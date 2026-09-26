# Agent Swarm Patterns — Pico900

How to use parallel agents to harvest, port, and synthesize content from megabase and PicoDB efficiently.

Reference: `C:\Dev\ORCHESTRATION.md` and `C:\Dev\AGENTS.md` for workspace-wide agent roles and patterns.

## The Four Roles

**HARVESTER agents**: Extract translations, quotations, and structured data from megabase and PicoDB. Output: JSON files, staged for merging.

**PORTER agents**: Convert harvested data into Pico900 format. Reconcile conflicts, fill gaps, maintain provenance. Output: conclusion entries matching STYLE_GUIDE.md.

**SYNTHESIZER agents**: Combine porter output, create coherent entries, write exegeses and commentary. Output: complete conclusion entries ready for review.

**REVIEWER agents**: Validate against STYLE_GUIDE.md, check citations, ensure quality. Output: approval or revision requests.

## The Harvesting Pipeline

```
megabase/
PicoDB/
  ↓
[HARVESTER agents work in parallel on independent sections]
  ├─ H1: Adelandum Arabem (8 conclusions) → stage_adelandum.json
  ├─ H2: Averroem (41 conclusions) → stage_averroem.json [split into 5-conclusion chunks]
  ├─ H3: Avicennam (12 conclusions) → stage_avicenna.json
  └─ H4: Heretical theses (from Copenhaver) → stage_heretical.json
  ↓
[Merge staged files]
  → data/translations/translated_conclusions.json
  → data/scholarship/heretical_conclusions.json
  ↓
[PORTER agents work in parallel on independent sections]
  ├─ P1: Convert Adelandum → conclusion entries
  ├─ P2: Convert Averroem (chunked) → conclusion entries
  ├─ P3: Convert Avicennam → conclusion entries
  └─ P4: Convert heretical → conclusion entries
  ↓
[Merge ported entries]
  → data/conclusions_manifest.json (updated)
  ↓
[SYNTHESIZER agents work on exegesis + commentary]
  ├─ S1: Write exegeses for Adelandum
  ├─ S2: Write commentary + citations for Averroem (select conclusions)
  ├─ S3: Kabbalah synthesis (from PicoDB)
  └─ S4: Begin heretical essay (from Copenhaver + Howlett)
  ↓
[REVIEWER agents validate + approve]
  ├─ R1: Check Adelandum entries against STYLE_GUIDE
  ├─ R2: Verify all citations (linter)
  └─ R3: Approve heretical essay outline
  ↓
Ready for web build
```

## Agent Instructions by Role

### HARVESTER Template

**Task**: Extract translations and data from [SOURCE] for [SECTION]. Output structured JSON.

**Input**:
- Source file(s) (e.g., `C:\Dev\megabase\chats_2025\2025-07-04_Pico 900 Conclusions Exegesis.md`)
- Section to extract (e.g., "Conclusiones secundum Adelandum Arabem")
- Output template (see below)

**Output Format**:
```json
{
  "section": "Conclusiones secundum Adelandum Arabem",
  "source": "2025-07-04_Pico 900 Conclusions Exegesis.md",
  "harvested_conclusions": [
    {
      "conclusion_id": "[to_be_assigned]",
      "latin_incipit": "Intellectus agens nihil est...",
      "english_translation": "[full translation from megabase]",
      "exegesis": "[full exegesis from megabase]",
      "notes": "Exact text from lines X-Y of source file"
    },
    ...
  ],
  "metadata": {
    "harvested_date": "ISO 8601",
    "harvested_by": "[agent_id]",
    "section_count": 8,
    "completeness": "complete | partial"
  }
}
```

**Key Guidelines**:
- Extract text **verbatim** from source files
- Preserve line numbers and source references
- Do NOT synthesize or paraphrase
- If a section is partial, mark `completeness: partial`
- Output to `data/staging/stage_[section_name].json`

### PORTER Template

**Task**: Convert harvested JSON into Pico900 conclusion entries. Reconcile translations, assign IDs, maintain provenance.

**Input**:
- Staged JSON from HARVESTER (e.g., `data/staging/stage_adelandum.json`)
- Critical edition Latin text (for verification)
- STYLE_GUIDE.md (for entry format)

**Output**: `data/conclusions/[section_name]/conclusion_[id].json` files, each matching STYLE_GUIDE.md template

**Key Guidelines**:
- Assign unique `conclusion_id` (e.g., "I.1.1" for first conclusion, Adelandum section)
- Mark `latin_source: "megabase"` (to be verified later against critical edition)
- Set `commentary_status: "draft"` (translations exist; exegesis may need enhancement)
- Set `status: "sourced"` (harvested from known source)
- All `scholar_citations` start empty; SYNTHESIZER will populate
- If megabase included exegesis, use it as `exegesis` field

### SYNTHESIZER Template

**Task**: Enhance entries with scholarship citations, write exegeses, draft commentary.

**Input**:
- Ported conclusion entries from PORTER
- PicoDB source packets and scholar profiles
- Pico scholarship documents (Wirszubski, Copenhaver, etc.)
- STYLE_GUIDE.md (citation format, quality standards)

**Output**: Complete conclusion entries with:
- Verified exegeses (1-2 paragraphs)
- 2-3 `scholar_citations` for each conclusion (verbatim quotations)
- Heretical flags + notes for condemned propositions
- `status: "complete"` or `"reviewed"`

**Key Guidelines** (from STYLE_GUIDE.md):
- Every `scholar_citations` entry must include a **verbatim quotation**
- Mark confidence: `[VERIFIED]` (checked against source), `[CITED]` (taken from Scholar, not verified), `[INFERRED]` (synthesized)
- No unsourced assertions — every scholarly claim must cite a scholar
- For heretical conclusions: research the charge, Pico's defense (if in *Apology*), and modern debate
- Write exegesis to explain **why** the conclusion matters, not just what it says

### REVIEWER Template

**Task**: Validate entries against STYLE_GUIDE.md, check citations, approve or request revision.

**Input**:
- Complete conclusion entries from SYNTHESIZER
- STYLE_GUIDE.md (quality checklist)
- Citation validation script output (from `scripts/validate_citations.py`)

**Output**: Approval ("merged to manifest") or revision requests

**Checklist**:
- [ ] Latin text is accurate (compare against critical edition)
- [ ] English translation is clear and defensible (cite source)
- [ ] Every scholarly claim has a **verbatim quotation** backing it
- [ ] Exegesis explains WHY the conclusion matters
- [ ] Tags are consistent with schema
- [ ] Confidence levels marked for all citations
- [ ] Heretical conclusions have extended notes
- [ ] No unsourced paraphrase
- [ ] Markdown formatting is consistent

## Parallel Execution: The Orchestration Pattern

Reference: `C:\Dev\ORCHESTRATION.md` — "one writer per file, always"

### Working Queue

Create a manifest tracking agent assignments:

```json
{
  "harvesting_queue": [
    {
      "agent": "HARVESTER-1",
      "task": "Extract Adelandum Arabem from 2025-07-04 megabase file",
      "status": "in_progress",
      "output": "data/staging/stage_adelandum.json"
    },
    {
      "agent": "HARVESTER-2",
      "task": "Extract Averroem (conclusions 1-10)",
      "status": "in_progress",
      "output": "data/staging/stage_averroem_chunk1.json"
    },
    ...
  ],
  "porting_queue": [...],
  "synthesis_queue": [...],
  "review_queue": [...]
}
```

### Checkpoints

After each phase, merge outputs:

**After Harvesting**: `python scripts/merge_staged_files.py`
- Merges all `data/staging/stage_*.json` files into `data/translations/translated_conclusions.json`
- Validates no duplicates, no orphan conclusions

**After Porting**: `python scripts/merge_ported_entries.py`
- Merges all `data/conclusions/[section]/*.json` into `data/conclusions_manifest.json`
- Updates manifest with sourcing status
- Checkpoints progress

**After Synthesis**: `python scripts/validate_citations.py`
- Lints all entries: checks `[VERIFIED]` tags have quotations, tags are valid, etc.
- Reports issues to reviewer queue

**After Review**: `python scripts/merge_approved_entries.py`
- Moves approved entries to final manifest
- Generates build manifest for HTML generation

## Phase 1: Harvest From Megabase (Example)

**Objective**: Extract the ~100 conclusions already translated in 2025-07-04 file.

**Agents Assigned**:

1. **HARVESTER-1: Adelandum Arabem**
   - **Prompt**: Extract all conclusions from the "Conclusiones secundum Adelandum Arabem" section of `C:\Dev\megabase\chats_2025\2025-07-04_Pico 900 Conclusions Exegesis.md`. Output JSON with: conclusion_id (placeholder), latin_incipit, english_translation, exegesis. Be verbatim; do not paraphrase.
   - **Output**: `data/staging/stage_adelandum.json`

2. **HARVESTER-2: Averroem Part 1 (Conclusions 1-20)**
   - **Prompt**: Extract conclusions I.7.1 through I.7.20 from Averroes section. Output JSON. Mark completeness: full or partial.
   - **Output**: `data/staging/stage_averroem_chunk1.json`

3. **HARVESTER-3: Averroem Part 2 (Conclusions 21-41)**
   - **Prompt**: Extract conclusions I.7.21 through I.7.41. Output JSON.
   - **Output**: `data/staging/stage_averroem_chunk2.json`

4. **HARVESTER-4: Other Sections (Avicenna, Alfarabius, Heretical)**
   - **Prompt**: Extract remaining sections (Avicenna 12 conclusions, Alfarabius 11, etc.). Output separate JSON files.
   - **Output**: `data/staging/stage_*.json` (multiple files)

**Execution**: All four agents run in parallel. After ~1 hour, merge their outputs.

## Phase 2: Port & Standardize (Example)

**Objective**: Convert harvested JSON into standardized Pico900 entries.

**Agents Assigned**:

1. **PORTER-1: Adelandum Arabem → Conclusion Entries**
   - **Prompt**: Convert `data/staging/stage_adelandum.json` into 8 conclusion entry JSON files following STYLE_GUIDE.md template. Assign IDs (I.1.1 through I.1.8). Mark all with `status: "sourced"`, `commentary_status: "draft"`.
   - **Output**: `data/conclusions/Adelandum/*.json`

2. **PORTER-2: Averroem Chunk 1 → Conclusion Entries**
   - **Prompt**: Convert chunk 1 (conclusions 1-20) into entries. IDs: I.2.1 through I.2.20.
   - **Output**: `data/conclusions/Averroem/chunk1/*.json`

3. **PORTER-3: Averroem Chunk 2 → Conclusion Entries**
   - **Prompt**: Convert chunk 2 (conclusions 21-41) into entries. IDs: I.2.21 through I.2.41.
   - **Output**: `data/conclusions/Averroem/chunk2/*.json`

4. **PORTER-4: Remaining Sections**
   - **Prompt**: Port Avicenna, Alfarabius, Moysem Aegyptium sections into entries.
   - **Output**: `data/conclusions/[section]/*.json` (multiple directories)

## Phase 3: Synthesize & Enhance (Example)

**Objective**: Write exegeses, find scholarship citations, flag heretical conclusions.

**Agents Assigned**:

1. **SYNTHESIZER-1: Kabbalah Conclusions (Cross-Section)**
   - **Prompt**: Identify all conclusions related to Kabbalah (likely scattered across sections). For each, synthesize exegesis + find 2-3 Wirszubski/Busi/Copenhaver quotations. Reference PicoDB's Kabbalah reading protocol. Mark `tags: ["kabbalah", ...]`.
   - **Input**: Completed conclusion entries (from PORTER)
   - **Output**: Enhanced conclusion entries (updated JSON files)

2. **SYNTHESIZER-2: Heretical Essay Outline**
   - **Prompt**: From Copenhaver's *Pico on Trial* (2025-07-05 megabase file), identify and organize all 13 condemned conclusions. Outline the heretical essay by theme (incarnation, eucharist, soul/intellect, Kabbalah). Draft 3-4 sections. Cite scholarly debate.
   - **Output**: `docs/HERETICAL_ESSAY_OUTLINE.md` + `data/heretical_queue.json` (annotated)

3. **SYNTHESIZER-3: Astrology Conclusions (Cross-Section)**
   - **Prompt**: Identify astrology-related conclusions. Synthesize exegesis using PicoDB's astrology protocol + Akopyan. Find citations. Mark `tags: ["astrology", ...]`.
   - **Output**: Enhanced conclusion entries

4. **SYNTHESIZER-4: Metaphysics & Being (Averroem + Avicenna)**
   - **Prompt**: Conclusions on substance, essence, being, causality. Write exegeses explaining their philosophical centrality. Find Allen, Edelheit, Howlett citations.
   - **Output**: Enhanced conclusion entries

## Checkpointing & Recovery

If an agent task is interrupted or fails:

1. **Agent saves partial work** to `data/staging/[task_id]_partial.json`
2. **Manifest notes task status** (in_progress → paused)
3. **Next agent resumes** from that checkpoint
4. **Upon completion**, partial file is merged with others

Example checkpoint:
```json
{
  "task_id": "HARVESTER-2",
  "status": "paused_after_conclusion_15",
  "resumed_by": "HARVESTER-2 (resumed)",
  "work_file": "data/staging/stage_averroem_chunk1_partial.json",
  "last_conclusion_id": "I.7.15",
  "notes": "Continue from I.7.16"
}
```

## Key Tools & Scripts

**`scripts/merge_staged_files.py`**: Merge all `data/staging/stage_*.json` into consolidated file. Check for conflicts.

**`scripts/validate_citations.py`**: Lint all entries. Check:
- Every `[VERIFIED]` citation has a quotation
- All `tags` are in allowed set
- All status/confidence values are valid
- No orphan conclusions

**`scripts/checkpoint_progress.py`**: Update manifest, track sourcing status, generate progress report.

**`scripts/build_site.py`**: Generate static HTML from manifest (final step).

## Cost & Efficiency Notes

Using agent swarms to harvest + port avoids:
- Context explosion from reading 900+ conclusions manually
- Transcript bloat from verbose agent outputs
- Repetitive prompt writing

Advantages:
- Parallel execution (4 agents = 4x speed)
- Checkpointing + recovery (no restart from scratch)
- Delegation to specialized roles (HARVESTER ≠ SYNTHESIZER)
- Auditable: every entry has source + agent ID

**Estimated cost**: ~200k tokens total (harvesting + porting + synthesis + review) vs. ~1M tokens if done serially or manually.

