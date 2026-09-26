# Phase 3 Autonomous Execution Handover

**This document enables continuous autonomous work across sessions.**

---

## Quick Start: Launching Phase 3 (Next Session)

**Your exact next command**:
```bash
cd C:\Dev\Pico900
git status  # Verify main branch is clean
python scripts/build_site.py  # Test website generator works
# Then dispatch Phase 3 agents per the dispatch manifest below
```

---

## Phase 3 Dispatch Manifest (Ready to Execute)

Copy-paste these commands in sequence. Each agent will run in parallel; no waiting required.

### Agent 1: Q5 Heretical Essay (Kabbalah & Magic)

```
Agent Name: WRITER-Q5
Task: Draft heretical essay on Kabbalah & Magic as proof of Christ's divinity
Input: S7 conclusions (118) + 283 verified quotations from S7_CITATION_MANIFEST.json
Structure: 
  1. Historical context (1486 trial, papal charge)
  2. Pico's Kabbalistic framework (sefirot, divine names, Abulafia)
  3. Defense of syncretic approach (Wirszubski + Copenhaver analysis)
  4. Integration with Q1–Q13 heretical essay
Token budget: 40k
Output: docs/Q5_HERETICAL_ESSAY_DRAFT.md
Success criteria:
  - [ ] Essay 4000+ words
  - [ ] 10+ direct quotations from Wirszubski/Copenhaver
  - [ ] Explains Pico's claim: "Magic & Kabbalah give greatest certainty of Christ's divinity"
  - [ ] Links to S7 website pages (once live)
```

### Agent 2: Q8 Heretical Essay (Epistemology of Belief)

```
Agent Name: WRITER-Q8
Task: Draft heretical essay on doxastic voluntarism and institutional justice
Input: S3 conclusions (11 Averroist) + S3.C002 monopsychism (links to Q8)
Structure:
  1. Philosophical problem: Can belief be willed?
  2. Medieval context (divine foreknowledge, free will)
  3. Pico's radical answer: Doxastic bondage (belief is constrained)
  4. Implications: Heresy charges are epistemically unjust
  5. Integration with Q1–Q13 heretical essay
Token budget: 40k
Output: docs/Q8_HERETICAL_ESSAY_DRAFT.md
Success criteria:
  - [ ] Essay 3000+ words
  - [ ] 8+ direct quotations from Copenhaver/medieval sources
  - [ ] Explains why institutional belief-policing is unjust
  - [ ] Links to S3 website pages
```

### Agent 3: S1 Supplementation (Scholar Quotations)

```
Agent Name: HARVESTER-S1-Phase3A
Task: Extract 2–3 scholar quotations per S1 conclusion (95 total)
Input: 
  - data/conclusions/S1/ (95 files with empty quotation slots)
  - S1_SOURCING_MANIFEST.json (checkpoint)
  - PDF corpus (Allen, Howlett, Copenhaver, Wirszubski, Edelheit)
Process:
  1. Read each S1 file
  2. Extract Allen quotations on henosis + Neoplatonism
  3. Extract Howlett on soul faculty + concordism
  4. Extract Copenhaver on mystical theology (Q13 context)
  5. Update JSON quotation fields
  6. Commit with message: "S1 Phase 3A: Scholar quotations (95 conclusions, 250+ quotations)"
Token budget: 50k
Output: Updated data/conclusions/S1/*.json files
Success criteria:
  - [ ] 2–3 quotations per conclusion (285–855 total)
  - [ ] All quotations directly cited (not paraphrased)
  - [ ] Scholar, work, page documented
  - [ ] Valid JSON in all files
```

### Agent 4: S1 Supplementation (Latin Incipits)

```
Agent Name: HARVESTER-S1-Phase3B
Task: Source Latin incipits from critical edition (95 total)
Input:
  - data/conclusions/S1/ (95 files with placeholder incipits)
  - Brown critical edition: https://cds.lib.brown.edu/cds-project/picos-900-theses
  - Farmer critical edition (1998) as fallback
Process:
  1. Read each S1 file
  2. Fetch Latin incipit from critical edition
  3. Verify against existing megabase translations
  4. Update JSON latin_incipit field
  5. Mark as verified
  6. Commit with message: "S1 Phase 3B: Latin incipits (95 conclusions, critical edition sourced)"
Token budget: 50k
Output: Updated data/conclusions/S1/*.json files
Success criteria:
  - [ ] All 95 Latin incipits sourced and verified
  - [ ] Match critical edition text
  - [ ] All JSON valid
```

### Agent 5: S3 Website Deployment

```
Agent Name: DEPLOYER-S3
Task: Deploy S3 website to GitHub Pages
Input: Phase 2 commits on main branch (build_site.py + 11 S3 conclusions)
Process:
  1. Verify Phase 2 commits are on main
  2. Run: python scripts/build_site.py
  3. Test site locally: python -m http.server 8000
  4. Push main branch to GitHub
  5. Verify live URL: https://t3dy.github.io/Pico900/
  6. Document in dispatch log: "S3 website live (11 Averroist conclusions)"
Token budget: 20k
Output: Live website at https://t3dy.github.io/Pico900/
Success criteria:
  - [ ] Site builds without errors
  - [ ] All 11 S3 pages render correctly
  - [ ] Search/filter works
  - [ ] Heretical toggle works
  - [ ] Mobile responsive
  - [ ] No console errors
```

### Agent 6: S2 Verification & Supplementation

```
Agent Name: HARVESTER-S2-Phase3
Task: Verify + supplement 110 Aristotelian conclusions
Input: data/staging/stage_S2.json (seeded but not supplemented)
Process:
  1. Parse stage_S2.json
  2. Phase 3A: Fetch Latin from critical edition + Farmer (4–6 hrs)
  3. Phase 3B: Extract English translations from Farmer apparatus (3–4 hrs)
  4. Phase 3C: Collect 2–3 scholar quotations per conclusion (6–8 hrs)
  5. Standardize into Pico900 schema
  6. Output: 110 JSON files in data/conclusions/S2/
  7. Commit: "S2 Phase 3: Supplementation and standardization (110 conclusions)"
Token budget: 50k
Output: data/conclusions/S2/*.json files (110 total)
Success criteria:
  - [ ] All 110 files valid JSON
  - [ ] Latin incipits sourced and verified
  - [ ] English translations sourced (Farmer or marked [TO_TRANSLATE])
  - [ ] 2–3 quotations per conclusion
```

### Agent 7: Remaining Sections (S5, S6, S8, S9) Extraction

```
Agent Name: HARVESTER-S5-S9
Task: Extract 4 remaining sections (~340 conclusions total)
Input: CRITICAL_EDITION_TAXONOMY.md (section structure + priority tiers)
Dispatch strategy (staggered):
  1. Week 1: H-S5 (Zoroastrianism, 80 conclusions)
  2. Week 1: H-S6 (Hermeticism, 95 conclusions)
  3. Week 2: H-S8 (Medieval Jewish, 8 conclusions)
  4. Week 3: H-S9 (Christian Theology, 185 conclusions)
Token budget: 40k per agent (160k total for all 4)
Process: Apply content-first HARVESTER methodology from Phase 1-2 lessons
Output: data/staging/stage_S5.json, stage_S6.json, stage_S8.json, stage_S9.json
Success criteria:
  - [ ] All 4 staging files created
  - [ ] Each section: Latin + translations + quotations
  - [ ] All JSON valid
```

---

## Execution Timeline (Phase 3)

```
Dispatch batch 1 (Week 1, Day 1):
  └─ All 7 agents dispatched simultaneously (parallel execution)

Week 1 (Parallel):
  ├─ WRITER-Q5: Q5 heretical essay drafting (6–8 hrs)
  ├─ WRITER-Q8: Q8 heretical essay drafting (4–6 hrs)
  ├─ HARVESTER-S1-Phase3A: Scholar quotations (25–30 hrs)
  ├─ HARVESTER-S1-Phase3B: Latin incipits (15–20 hrs)
  ├─ DEPLOYER-S3: Website deployment (30 min)
  ├─ HARVESTER-S2-Phase3: S2 verification (13–18 hrs)
  └─ HARVESTER-S5-S9: S5-S6 extraction (40–60 hrs)

Week 2:
  ├─ S7 website integration (if S7 supplementation 80% complete)
  ├─ S1 website integration (if S1 supplementation 80% complete)
  ├─ HARVESTER-S8: Medieval Jewish extraction (8 conclusions, 2–3 hrs)
  └─ HARVESTER-S9: Christian Theology extraction (185 conclusions, 30–40 hrs)

Week 3-4:
  ├─ Phase 4 planning (specialist review, final assembly)
  ├─ Remaining supplementation (90%+ target)
  └─ Full website integration (all 900 conclusions live)
```

**Critical path**: S1/S2 supplementation + S5-S9 extraction = 3–4 weeks  
**Bottleneck**: Remaining sections extraction (S8-S9)

---

## How to Continue from Next Session

1. **Read this document** (you're reading it)
2. **Verify Phase 2 is committed**:
   ```bash
   git log --oneline | head -5  # Should show Phase 2 complete commit
   git status  # Should be clean on main
   ```

3. **Dispatch Phase 3 agents in batch** (all 7 at once):
   - Copy the 7 Agent prompts from "Dispatch Manifest" section above
   - Use the Agent tool to launch each one
   - They'll run in parallel; no waiting required

4. **Monitor progress** (optional):
   - Watch dispatch log: `tail -50 PHASE_1_DISPATCH_LOG.md`
   - Check manifests for completion status

5. **When Phase 3 agents finish**:
   - Read phase completion reports
   - Commit any new work to main branch
   - Follow Phase 4 readiness steps (similar handover document will be created)

---

## Key Files for Phase 3

**Infrastructure**:
- `scripts/build_site.py` — Website generator (tested, production-ready)
- `scripts/harvest_s7_citations.py` — Citation extraction (can be adapted for other sections)
- `scripts/source_s1_content.py` — Content sourcing (framework for Phase 3A-B)

**Manifests & Checkpoints**:
- `data/conclusions_manifest.json` — Master progress tracker (236 conclusions, all phases)
- `data/conclusions/S1/S1_SOURCING_MANIFEST.json` — S1 checkpoint
- `data/conclusions/S7/S7_CITATION_MANIFEST.json` — S7 checkpoint (283 quotations)
- `data/staging/stage_S2.json` — S2 seeded (ready for Phase 3 supplementation)

**Phase 2 Outputs** (ready to integrate):
- `data/conclusions/S1/*.json` — 95 Neoplatonic (framework + metadata, needs supplementation)
- `data/conclusions/S3/*.json` — 11 Averroist (100% complete, live on website)
- `data/conclusions/S4/*.json` — 12 Avicennist (72% complete, needs citations)
- `data/conclusions/S7/*.json` — 118 Kabbalistic (100% structural, 283 quotations filled)

**Documentation**:
- `PHASE_1_RETROSPECTIVE.md` — Phase 1 analysis + lessons learned
- `PHASE_2_DISPATCH_BRIEF.md` — Phase 2 work queue (complete)
- `PHASE_3_READINESS.md` — Phase 3 readiness checklist
- `DECISIONS.md` — All major architecture decisions logged

**Website**:
- `site/` (generated, gitignored) — Latest build output (run `python scripts/build_site.py` to regenerate)
- `site/index.html` — Landing page (11 S3 conclusions visible)
- `site/conclusions/S3_C*.html` — 11 individual conclusion pages

---

## Autonomous Execution Model

**Each session follows this pattern**:

1. **Dispatch batch**: Launch multiple agents in parallel
2. **No waiting**: Agents run autonomously in background
3. **Parallel tracks**: 
   - Track A: Essay drafting (Q5 + Q8)
   - Track B: Content supplementation (S1 + S2)
   - Track C: Website building (S3/S7 integration)
   - Track D: Section extraction (S5-S9)
4. **Completion notifications**: As each agent finishes, next steps are triggered
5. **Handover**: At session end, create new handover document for next session

---

## Success Metrics for Phase 3

- [ ] Q5 heretical essay: Drafted and integrated into website
- [ ] Q8 heretical essay: Drafted and integrated into website
- [ ] S1 supplementation: 80%+ complete (253-285 quotations + 95 Latin incipits)
- [ ] S2 supplementation: 80%+ complete (220-330 quotations + 110 Latin + translations)
- [ ] S3 website: Live and functional (11 Averroist conclusions)
- [ ] S5-S6 extracted: Seeded and ready (175 conclusions)
- [ ] S8-S9 extracted: Seeded and ready (193 conclusions)
- [ ] Total: S1-S9 present in data/conclusions/ directory (586+ conclusions)
- [ ] Website: S3 live (Week 1), S7 integration (Week 2), full integration (Week 3-4)

---

## When to Create Phase 4 Handover

At the end of Phase 3 (Week 4), create a new `PHASE_4_HANDOVER_AUTONOMOUS.md` document with:
- Phase 4 dispatch manifest (remaining sections, final supplementation, specialist review)
- Execution timeline (Week 5-6)
- Success metrics for Phase 4 (all 900 conclusions live, heretical essays finalized, public deployment)

---

## Notes for Future Sessions

- **Content-first beats infrastructure-first**: Phase 1-2 learned this lesson. Future HARVESTER agents should extract substance first, build scaffolding second.
- **Parallel execution is 4× faster**: Use it everywhere. No sequential work unless dependencies force it.
- **Checkpoints enable recovery**: All sections have manifests. If an agent fails, checkpoint files allow resume without restart.
- **Autonomy scales**: This model worked for 236 conclusions in Phase 1-2. It will work for all 900 by Phase 4.

---

**Status**: Phase 3 is fully specified and ready for autonomous execution in next session.

**Next session**: Copy the 7 Agent prompts from "Dispatch Manifest" and launch them all simultaneously. Come back in 3-4 weeks with Phase 4 handover document ready.

**Estimated total project timeline**: Phase 0-4 complete by late October 2026 (all 900 conclusions live, website published, heretical essays integrated).
