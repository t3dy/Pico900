# Phase 1 Roadmap: Harvest All 900 Conclusions

**Status**: Ready to dispatch  
**Start Date**: 2026-09-25 (on user approval)  
**Scope**: Extract, translate, standardize all 900 conclusions from critical edition + megabase  
**Budget**: ~350k tokens (learning from Phase 0 efficiency)  

---

## Phase 1 Structure: Three Parallel Tracks

This phase runs three independent agent tracks simultaneously, each processing 8 sections of ~100 conclusions.

### Track A: RESEARCH (HARVESTER agents)
**Goal**: Extract Latin, collect translations, gather scholarship quotations  
**Agents**: H2, H3, H4 (three HARVESTER instances, section-assigned)  
**Output**: `data/staging/stage_[section].json` (parallel writes, no conflicts)  
**Token Budget**: 120k (40k per agent)  
**Success Criteria**: 
- All 900 Latin incipits extracted
- Each conclusion has 2–3 translation sources identified
- Scholar citations collected or marked [TO_SOURCE]

### Track B: BUILD (PORTER agents)
**Goal**: Standardize into Pico900 schema, assign IDs, validate structure  
**Agents**: P2, P3, P4 (three PORTER instances, section-assigned)  
**Input**: `data/staging/stage_[section].json`  
**Output**: `data/conclusions/[section]/*.json` (13 files per section × 8 sections = 104 files)  
**Token Budget**: 80k (26k per agent)  
**Concurrency**: Waits for corresponding HARVESTER to complete, then processes immediately  
**Success Criteria**:
- All conclusions in proper JSON schema
- IDs assigned: S[1-8].C[1-100]
- No schema violations

### Track C: VERIFY (REVIEWER agents + RETROSPECTIVE)
**Goal**: Validate entries against STYLE_GUIDE, flag gaps, generate reports  
**Agents**: R2, R3, R4 (three REVIEWER instances) + RETROSPECTIVE  
**Input**: `data/conclusions/[section]/*.json` (completed entries from POARTs)  
**Output**: `docs/PHASE_1_SECTION_REPORTS.md` (per-section validation report)  
**Token Budget**: 150k (50k per reviewer + 50k retrospective)  
**Concurrency**: Runs after each section's PORTER completes  
**Success Criteria**:
- All entries validated against STYLE_GUIDE
- Gaps identified and logged (missing translations, incomplete scholarship)
- Final retrospective: learnings for Phase 2

---

## Sectioning Strategy (8 Sections × ~100 Conclusions Each)

From critical edition taxonomy + megabase organization:

| Section | Name | Count | Focus |
|---------|------|-------|-------|
| S1 | Secundum Platonicos | 95 | Platonic philosophy |
| S2 | Secundum Aristotelem | 110 | Aristotelian philosophy |
| S3 | Secundum Avicennam | 105 | Islamic philosophy (Avicenna) |
| S4 | Secundum Averroem | 120 | Islamic philosophy (Averroes) |
| S5 | Secundum Zoroastrem | 80 | Persian/Zoroastrian theses |
| S6 | Secundum Hebraeos | 115 | Kabbalah + Jewish philosophy |
| S7 | Secundum Aegyptios | 95 | Hermetic + Egyptian magic |
| S8 | Secundum Theologos | 185 | Christian theology |
| | **TOTAL** | **905** | |

*Note: Total is 905 to allow for editorial variants in critical edition; final count will be 900.*

---

## Parallelization & Concurrency Rules

**One writer per file, always**:
- Each HARVESTER writes to its own `stage_[section].json` (no conflicts)
- Each PORTER writes to its own `data/conclusions/[section]/` (no conflicts)
- ORCHESTRATOR (coordinator) updates manifest atomically at phase gate

**Gate progression**:
```
H2 done → P2 starts (H3, H4 continue in parallel)
P2 done → R2 starts (P3, P4, H3, H4 continue)
R2 done → next section reports compile
All sections done → R RETROSPECTIVE runs final analysis
```

**Manifest coordination**:
- Phase-level manifest updated once per section completion (ORCHESTRATOR writes)
- No agent writes to manifest directly (avoids race conditions)
- Checkpoint after each section completes (recovery point if agent fails)

---

## Quality Gates

### Gate 1: HARVESTER Output (before PORTER starts)
**ORCHESTRATOR validates**:
- All 13 conclusions in `stage_[section].json`
- Latin incipits present and match critical edition
- Translation sources identified (URLs, page numbers)
- [ ] If failed: HARVESTER reruns section only

### Gate 2: PORTER Output (before REVIEWER starts)
**ORCHESTRATOR validates**:
- All JSON files well-formed (parseable)
- All required fields present (latin_incipit, english_translation, status, etc.)
- IDs properly formatted (S[1-8].C[1-100])
- [ ] If failed: PORTER reruns section only

### Gate 3: REVIEWER Output (before next section)
**ORCHESTRATOR validates**:
- All entries checked against STYLE_GUIDE
- Gaps flagged and logged
- Citation count per entry meets threshold (2–3 minimum)
- [ ] If failed: REVIEWER identifies specific entries for revision, P reruns those only

---

## Agent Specializations & Context Isolation

### HARVESTER (H2, H3, H4)
**Context received**: `SOURCING_PROTOCOL.md` + `CRITICAL_EDITION_TAXONOMY.md` + their section incipit list  
**Token budget**: 40k per agent  
**Task**: Extract Latin, find translations in megabase, collect quotations  
**Output contract**: `data/staging/stage_[section].json` with charge + defense + quotations  

### PORTER (P2, P3, P4)
**Context received**: `STYLE_GUIDE.md` + `data/staging/stage_[section].json`  
**Token budget**: 26k per agent  
**Task**: Normalize to Pico900 schema, validate, assign IDs  
**Output contract**: 100 well-formed JSON files in `data/conclusions/[section]/`  

### REVIEWER (R2, R3, R4)
**Context received**: `STYLE_GUIDE.md` + `QUALITY_CHECKLIST.md` + their section's JSON entries  
**Token budget**: 50k per agent (3-agent team processes all sections)  
**Task**: Validate each entry, flag gaps, compile section report  
**Output contract**: `docs/PHASE_1_SECTION_REPORT_S[1-8].md`  

### RETROSPECTIVE
**Context received**: All section reports + dispatch log + token usage  
**Token budget**: 50k  
**Task**: Analyze pipeline efficiency, identify bottlenecks, recommend Phase 2 improvements  
**Output contract**: `docs/PHASE_1_RETROSPECTIVE.md` + updated `DECISIONS.md`  

---

## Timeline & Checkpoints

| Checkpoint | Trigger | Action |
|------------|---------|--------|
| **S1 Complete** | H2 + P2 + R2 done | Update manifest, archive section reports |
| **S1–S4 Complete** | Halfway point | Mid-project retrospective (optional) |
| **S5–S8 Complete** | All sections done | Final retrospective, assess Phase 2 readiness |
| **Phase 1 Done** | All agents signed off | Approval gate: ready for Phase 2? |

---

## Success Criteria for Phase 1

- [ ] All 900 conclusions extracted + translated
- [ ] All entries in proper Pico900 schema
- [ ] 2–3 scholarly citations per entry (minimum)
- [ ] Section reports compiled with gap analysis
- [ ] Retrospective identifies process improvements
- [ ] Phase 1 completes under 350k token budget (or within 10% overage justified)
- [ ] All section checkpoints archived in git

---

## Phase 2 Gates (Blocked Until Phase 1 Complete)

- [ ] Do all 900 conclusions meet quality threshold? If not, which sections need revision?
- [ ] Should we build the website UI before Phase 2, or is Phase 1 complete data enough?
- [ ] What process improvements from Phase 1 retrospective should we implement?
- [ ] Are there any source gaps critical to fix before public launch?

**Phase 2 scope** (after approval):
- Build website UI (facing-page HTML layout, search, heretical toggle)
- Integrate heretical essay into navigation
- Deploy to GitHub Pages
- Iterate on design/UX based on early feedback

---

## How to Trigger Phase 1

When ready, dispatch agents as:

```bash
# H2, H3, H4 dispatch (parallel)
claude agent --task "Extract 100 conclusions from section S1" --context=HARVESTER
claude agent --task "Extract 100 conclusions from section S2" --context=HARVESTER
claude agent --task "Extract 100 conclusions from section S3" --context=HARVESTER

# (H4–H8 follow in parallel during Phase 1)

# P2 dispatch (after H2 completes)
claude agent --task "Standardize S1 conclusions" --context=PORTER --input=data/staging/stage_S1.json

# R2 dispatch (after P2 completes)
claude agent --task "Validate S1 entries" --context=REVIEWER --input=data/conclusions/S1/*.json

# RETROSPECTIVE dispatch (after all sections complete)
claude agent --task "Retrospective analysis" --context=RETROSPECTIVE --input=docs/PHASE_1_SECTION_REPORTS.md
```

---

## Expected Outcomes

**By end of Phase 1**:
- All 900 conclusions extracted, translated, standardized
- Full citation map (2–3 sources per conclusion)
- Section-by-section quality reports
- Pipeline validated and optimized
- Ready for UI development + public launch (Phase 2)

**By end of Phase 2**:
- Live website at https://t3dy.github.io/Pico900
- Facing-page Latin/English layout
- Search + filter functionality
- Heretical essay integrated
- Ready for scholarly use
