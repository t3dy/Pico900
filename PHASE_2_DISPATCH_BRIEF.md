# Phase 2 Dispatch Brief — HARVESTER & SYNTHESIZER Agents
**Date**: 2026-09-25  
**Sender**: R2 (REVIEWER Agent)  
**Status**: Ready for dispatch after Phase 1 R2 review completion  

---

## Overview

Phase 1 REVIEWER (R2) has validated 107 standardized conclusions (S1 Neoplatonic + S4 Avicennist) and identified critical blockers for Phase 2. This brief outlines the work queue for Phase 2 HARVESTER and SYNTHESIZER agents.

**Full Review Details**: See `PHASE_1_REVIEW_SUMMARY.md`

---

## Phase 2 Work Queue

### Critical Blockers (S1 Section)

S1 Neoplatonic conclusions cannot proceed to final REVIEWER until these blockers are resolved:

1. **Latin Incipit Fetch** (91/95 entries missing)
2. **English Translation Sourcing** (94/95 entries missing)
3. **Scholar Citation Harvesting** (94/95 entries need 2–3 quotations)

### Secondary Work (S4 + S1 Heretical)

- S4 Avicennist: Add citations to 11 entries (non-blocking but recommended)
- S1 Heretical: Cross-reference to Phase 0 essay (depends on Phase 0 completion)

---

## Dispatch Sequence

### Tier 1: Critical Path (Deploy Immediately)

#### Agent: H1-S1 — Fetch Latin Critical Edition
**Role**: HARVESTER  
**Scope**: S1.C001–C095 (91 entries needing Latin incipit)  
**Task**:
1. Fetch full text from https://cds.lib.brown.edu/cds-project/picos-900-theses
2. Parse and identify Latin incipits for each S1 conclusion (cross-reference with order numbers T1, T2, etc.)
3. For each S1 entry: Populate `latin_incipit` field with verified text from critical edition
4. Set `incipit_verified: true` for all entries
5. Output: Updated `data/conclusions/S1/*.json` files

**Difficulty**: Medium  
**Estimated Duration**: 4–6 hours  
**Dependencies**: None  
**Deliverable**: S1 entries with populated `latin_incipit` + `incipit_verified=true`  

**Blocking Until Complete**: YES — Cannot proceed to translation sourcing without Latin.

---

#### Agent: H2-S1 — Source English Translations
**Role**: HARVESTER  
**Scope**: S1.C001–C095 (94 entries needing translations)  
**Task**:
1. Search megabase conversations for translation work on 900 Conclusions:
   - Keywords: "900 conclusions", "900 theses", "conclusiones", "pico translation", "neoplatonic conclusions"
   - Look for `megabase/` directories with Pico work (e.g., "2025-07-04_Pico 900 Conclusions Exegesis.md" or similar)
2. Search PicoDB study passes for translation artifacts (e.g., "PICOLATINDECLARATIONS.md" in `C:\Dev\PicoDB`)
3. For each S1 conclusion:
   - If existing translation found in megabase/PicoDB: Extract and cite source
   - If no translation available: Generate original translation (mark as "original translation 2026")
4. For each entry: Populate:
   - `english_translation` (as string or dict with `text` + `source` + `translator`)
   - `translation_source` (e.g., "Megabase 2025-07-04", "PicoDB Neoplatonic Study Pass", "Original 2026")
   - `translation_translator` (scholar name or "Ted Hand 2026")
5. Output: Updated `data/conclusions/S1/*.json` files

**Difficulty**: High (literature search + curation)  
**Estimated Duration**: 8–12 hours  
**Dependencies**: H1-S1 should complete first (but can run in parallel)  
**Deliverable**: S1 entries with `english_translation` + `translation_source` + `translation_translator`  

**Blocking Until Complete**: YES — Cannot write exegeses without translations.

---

#### Agent: H3-S1 — Harvest Scholar Citations
**Role**: HARVESTER  
**Scope**: S1.C001–C095 (94 entries needing 2–3 quotations each)  
**Task**:
1. For each S1 entry, identify 2–3 relevant scholars:
   - Primary targets: Copenhaver, Wirszubski, Howlett, Allen, Edelheit, Black, Busi, Akopyan
   - Secondary targets: Farmer, Farmer anthology, other Pico specialists in PicoDB (73 sources)

2. Extract quotations from sources:
   - **Copenhaver**: *Pico on Trial* (especially chapters on heretical conclusions, metaphysics, Kabbalah)
   - **Wirszubski**: *Pico della Mirandola's Encounter with Jewish Mysticism* (especially Neoplatonic-Kabbalistic synthesis)
   - **Howlett**: *Pico's Three Paths to the Absolute* or similar work on Neoplatonic metaphysics
   - **Allen**: *Neoplatonism and the Platonic Tradition* (Plotinian parallels)
   - **Other sources**: PicoDB Markdown conversions (73 files in `C:\Dev\PicoDB`); megabase Pico work

3. For each quotation collected:
   - Verify page number and context
   - Set confidence level:
     - [VERIFIED]: Quotation checked against source document
     - [CITED]: Taken from scholar; source trusted but not personally verified
     - [INFERRED]: Synthesized from multiple passages (avoid if possible)
   - Tag accordingly in JSON

4. Populate `scholar_citations` array with 2–3 complete entries (format: scholar, work, page, quotation, confidence_level)

5. Output: Updated `data/conclusions/S1/*.json` files

**Difficulty**: Very High (requires reading multiple scholars, verifying quotations)  
**Estimated Duration**: 12–16 hours  
**Dependencies**: H1-S1, H2-S1 (or can run in parallel; doesn't depend on them)  
**Deliverable**: S1 entries with `scholar_citations` (2–3 per entry, min 1 verified)  

**Blocking Until Complete**: YES — STYLE_GUIDE requires minimum 2 citations; Phase 2 cannot be marked complete without this.

---

### Tier 2: Secondary Priority (Run After Tier 1)

#### Agent: H4-S4 — Complete Avicennian Logic Citations
**Role**: HARVESTER  
**Scope**: S4 (12 entries, 11 needing additional citations)  
**Task**:
1. Current state: S4 entries have 0–3 citations; target is 2–3 minimum per STYLE_GUIDE
   - S4.C001: 3 citations (complete) ✓
   - S4.C002–C004, C006, C008, C012: 1–2 citations (need 1+ more)
   - S4.C005, C007, C009, C010, C011: 0–1 citations (need 1–2 more)

2. Find additional Avicennian logic scholarship:
   - Deborah Black (*Logic and Intellect in Averroes*, 2006)
   - Wirszubski (if he covers Avicenna + Pico)
   - Farmer, Syncretism sections on Arab logic
   - PicoDB S4-related sources

3. Add 1–2 quotations per entry to reach 2–3 minimum

4. Output: Updated `data/conclusions/S4/*.json` files

**Difficulty**: Medium  
**Estimated Duration**: 4–6 hours  
**Dependencies**: None (independent of S1 work)  
**Deliverable**: S4 entries with complete citations (2–3 minimum per entry)  

**Non-Blocking**: This work improves S4 quality but does not block Phase 2 completion.

---

### Tier 3: Heretical Integration (Run After Phase 0 Completion)

#### Agent: S1-HERETICAL — Cross-Reference S1 + Phase 0 Heretical Essay
**Role**: SYNTHESIZER  
**Scope**: S1 entries flagged as heretical (35 of 95)  
**Task**:
1. Wait for Phase 0 heretical essay completion (being written by S1-HERETICAL + S2-HERETICAL-ESSAY agents)

2. Once Phase 0 essay is complete, identify mapping between S1 heretical flags and Q1–Q13 condemned propositions:
   - Example: S1.C001 (The One beyond being) → Q1 (Incarnation & Divine Embodiment)
   - Example: S1.C004 (Soul's individuation) → Q4 (Soul, Intellect & Immortality)

3. For each S1 heretical entry:
   - Add field `heretical_mapping` with Q number (e.g., `"heretical_mapping": "Q1"`)
   - Add field `heretical_essay_section` with reference (e.g., `"heretical_essay_section": "§2.1 Incarnation & Divine Embodiment"`)

4. Output: Updated `data/conclusions/S1/*.json` files with heretical mappings

**Difficulty**: Medium (editorial synthesis)  
**Estimated Duration**: 2–4 hours  
**Dependencies**: Phase 0 heretical essay must complete first  
**Deliverable**: S1 heretical entries with `heretical_mapping` + `heretical_essay_section`  

**When to Dispatch**: After Phase 0 REVIEWER (R1-REVIEWER) validates heretical essay.

---

#### Agent: S2-CHARGE-DEFENSE — Populate Charge/Defense for Heretical S1
**Role**: SYNTHESIZER  
**Scope**: S1 entries flagged as heretical (35 of 95)  
**Task**:
1. Depends on: H3-S1 (citations) + Phase 0 heretical essay completion

2. For each S1 heretical entry:
   - Examine Phase 0 heretical essay section (linked by S1-HERETICAL agent)
   - Extract charge statement (what papal commission objected to)
   - Extract Pico's defense (from *Apology*, *Disputationes*, or scholarly reconstruction)
   - Extract scholarly debate summary (Copenhaver vs. Howlett? Wirszubski vs. Allen?)

3. Populate:
   - `charge`: Explicit theological charge (2–3 sentences)
   - `defense`: Pico's scholastic response (2–3 sentences)
   - Add commentary field with debate context (optional)

4. Output: Updated `data/conclusions/S1/*.json` files with populated charge/defense

**Difficulty**: Medium (editorial synthesis)  
**Estimated Duration**: 4–6 hours  
**Dependencies**: H3-S1 + S1-HERETICAL + Phase 0 essay  
**Deliverable**: S1 heretical entries with complete `charge` + `defense`  

**When to Dispatch**: After S1-HERETICAL mapping completes.

---

## Summary: Phase 2 Timeline

### Week 1 (Tier 1: Critical Blockers)
- **Day 1**: Dispatch H1-S1 (Latin), H2-S1 (translations), H3-S1 (citations) in parallel
- **Day 2–3**: Agents work in background; ~20–30 hours combined effort
- **Day 4**: H1-S1, H2-S1, H3-S1 complete; S1 entries fully populated

### Week 2 (Tier 2: Secondary)
- **Day 1**: Dispatch H4-S4 (Avicennian citations)
- **Day 2**: H4-S4 completes (~6 hours)

### Week 3 (Tier 3: Heretical Integration) — Depends on Phase 0
- **When**: After Phase 0 heretical essay completes + R1-REVIEWER validates
- **Day 1**: Dispatch S1-HERETICAL (mapping), then S2-CHARGE-DEFENSE (populate charge/defense)
- **Day 2**: Synthesis agents complete (~6 hours combined)

### Total Estimated Duration
- **Critical path**: 3 weeks wall-clock (but parallel execution compresses to ~5 days)
- **Agent effort**: ~35–45 hours combined across 5 HARVESTER + 2 SYNTHESIZER agents

---

## Quality Checkpoints

### Before Dispatching Agents
- ✓ Review `PHASE_1_REVIEW_SUMMARY.md` (this review's findings)
- ✓ Confirm blockers are understood
- ✓ Verify PicoDB + megabase search paths are accessible
- ✓ Notify orchestrator of parallel vs. sequential scheduling

### After Phase 2 Agents Complete
- [ ] PORTER re-standardizes S1 + S4 entries with new content
- [ ] REVIEWER (R2 again) validates Phase 2 output against STYLE_GUIDE
- [ ] All entries must have:
  - Verified Latin incipit
  - Sourced English translation
  - 2–3 scholar citations (min 1 verified)
  - Heretical entries: charge, defense, Phase 0 mapping
- [ ] Before Phase 3, generate new manifest checkpoint: `data/conclusions_manifest.json` (update progress tracking)

---

## Files Referenced

- **Source Data**: `data/conclusions/S1/*.json` (95 entries), `data/conclusions/S4/*.json` (12 entries)
- **Reference Docs**:
  - `docs/STYLE_GUIDE.md` (validation criteria)
  - `docs/ANGELICRESEARCH.md` (angelology context for heretical entries)
  - `PHASE_1_REVIEW_SUMMARY.md` (this review's detailed findings)
  - `HANDOVER_PHASE_1_ALPHA.md` (context on Phase 0 + Phase 1-Alpha)
- **Resource Locations**:
  - PicoDB: `C:\Dev\PicoDB` (15+ study passes, 73 Markdown sources)
  - Megabase: `C:\Dev\megabase` (LLM conversations, translations)
  - Brown Critical Edition: https://cds.lib.brown.edu/cds-project/picos-900-theses
  - Wiki: `C:\Dev\wiki` (cross-project references)

---

## Standing Instructions for Agents

### HARVESTER Agents (H1-S1, H2-S1, H3-S1, H4-S4)

1. **Read STYLE_GUIDE.md** before starting work (understand citation format, confidence levels, heretical section structure)
2. **Check conclusion_manifest.json** (if it exists) to see which entries are already sourced
3. **For each quotation**:
   - Verify exact page number
   - Copy verbatim (including [sic] if original has errors)
   - Set confidence level: [VERIFIED] if checked against source, [CITED] if from scholar, [INFERRED] if synthesized
4. **No unsourced paraphrases** — Every secondary-source claim must cite a scholar
5. **Prefer direct quotation over summary** (STYLE_GUIDE principle #3)
6. **Mark work completed** by updating `status` field to "sourced" before passing to PORTER

### SYNTHESIZER Agents (S1-HERETICAL, S2-CHARGE-DEFENSE)

1. **Read Phase 0 heretical essay** (output by S1-HERETICAL + S2-HERETICAL-ESSAY, validated by R1-REVIEWER)
2. **Cross-reference methodology**: How does Phase 0 essay organize Q1–Q13? Use same organization for S1 mapping.
3. **Maintain chain of evidence**: Every charge/defense claim must reference Phase 0 essay or original scholarship (Copenhaver, *Apology*, etc.)
4. **Flag uncertainties**: If Q-number mapping is ambiguous, note it explicitly (e.g., "S1.C009 may relate to Q5 or Q8; see Phase 0 §3.2 for debate")
5. **Mark work completed** by updating `status` field to "sourced" before passing to PORTER

---

## Escalation Path

If agents encounter blockers:

1. **Missing Latin from Brown critical edition**: Try Farmer critical edition (1998) as fallback
2. **Missing translation in megabase**: Generate original translation, mark as "[Original 2026]"
3. **Missing scholar quotations**: If work is out of print/unavailable, note "[Source unavailable; synthesized from secondary references]"
4. **Ambiguous heretical mapping**: Flag to ORCHESTRATOR; do not guess Q-number correspondence

---

**Ready for Dispatch**  
**Generated**: 2026-09-25 16:50 UTC  
**Gate**: Orchestrator approval required before launching Tier 1 agents
