# Context Architecture: Progressive Revelation & Isolation

How information flows to agents. What each role receives, what they don't, and why.

## Principle: Progressive Revelation on Need-to-Know Basis

Agents receive ONLY:
1. **Role-specific documentation** (template, format, validation rules)
2. **Assigned work** (queue entry + input data for that task)
3. **Direct dependencies** (source files, reference materials needed to complete the task)

Agents do NOT receive:
- Full project context (CLAUDE.md, all documentation)
- Other agents' work (HARVESTER doesn't see STYLE_GUIDE; PORTER doesn't read source PDFs)
- Historical decisions or project rationale (unless directly relevant to their task)

**Why**: Token efficiency. A HARVESTER who receives STYLE_GUIDE.md + schema.json + full CLAUDE.md wastes ~20k tokens on irrelevant context. Focused context = faster, cheaper, less hallucination.

---

## HARVESTER: What They Receive

**Files**:
- `docs/SOURCING_PROTOCOL.md` (where translations live in megabase/PicoDB)
- `PHASE_[N]_RESEARCH_QUEUE.json` (their assigned ticket only)
- Source file paths (exact URLs/paths to megabase files, PicoDB excerpts, PDF corpus)

**NOT received**:
- STYLE_GUIDE.md (they don't write entries)
- DECISIONS.md (why decisions were made)
- Full CLAUDE.md (project narrative)
- Other sections' work

**Total context**: ~2–3k tokens

**Example ticket**:
```json
{
  "task_id": "H1",
  "role": "HARVESTER",
  "section": "Heretical conclusions (13 theses)",
  "sources": [
    "C:\\Dev\\megabase\\chats_2025\\2025-07-05_Pico della Mirandola Summary.md (lines 1–150)",
    "C:\\Dev\\PicoDB\\artifacts\\essays\\pico_kabbalah_synthesis_longform_draft.md"
  ],
  "target_output": "data/staging/stage_heretical.json",
  "instructions": "Extract verbatim: (1) the 13 condemned conclusions (Latin incipit + English translation), (2) the papal commission's charge for each, (3) Pico's defense if available in the Apology, (4) any modern scholarly debate. Output JSON structure: { conclusion_id, latin_incipit, english_translation, charge, defense, scholarly_debate, sources }",
  "output_schema": "data/staging_schema.json"
}
```

The agent gets SOURCES + INSTRUCTIONS. That's it. No STYLE_GUIDE.

---

## PORTER: What They Receive

**Files**:
- `docs/STYLE_GUIDE.md` (entry template only, NOT the full guide; just the template section)
- `data/schema.json` (allowed fields, tags, status values)
- `data/staging/stage_[section].json` (output from HARVESTER for their section)
- `PHASE_[N]_RESEARCH_QUEUE.json` (their ticket)

**NOT received**:
- SOURCING_PROTOCOL.md (sources are already found)
- DECISIONS.md
- Full project context
- Other sections' staged JSON

**Total context**: ~3–4k tokens

**What STYLE_GUIDE section looks like for PORTER**:
```markdown
# Entry Template (PORTER Use Only)

## JSON Structure

```json
{
  "conclusion_id": "H.1.1",
  "section": "Heretical conclusions",
  "latin_incipit": "...",
  "latin_source": "megabase",
  "latin_verified": false,
  "english_translation": {
    "text": "...",
    "source": "2025-07-05_Pico della Mirandola Summary.md",
    "translator": "LLM"
  },
  "exegesis": null,
  "commentary_status": "draft",
  "scholar_citations": [],
  "heretical_flag": true,
  "heretical_notes": null,
  "tags": ["heretical"],
  "status": "sourced",
  "created_date": "[ISO 8601]",
  "updated_date": "[ISO 8601]"
}
```

## Rules

- `conclusion_id`: Assign sequentially. Format: `[SECTION_PREFIX].[NUMBER]`. Example: `H.1.1` = Heretical, first, first.
- `status`: Always "sourced" (work from HARVESTER is complete).
- `commentary_status`: "draft" (exegesis field is null; SYNTHESIZER will fill it).
- All other fields: Copy from harvested JSON verbatim.
```

PORTER doesn't get the full STYLE_GUIDE (which includes heretical notes section, quality checklist, etc.). They get just the template.

---

## SYNTHESIZER: What They Receive

**Files**:
- `docs/STYLE_GUIDE.md` (full version: entry template + citation format + quality checklist)
- `docs/HERETICAL_RESEARCH_PLAN.md` (for heretical specialty only; specific to their research task)
- Relevant research protocol (e.g., `docs/KABBALAH_READING_PROTOCOL.md` if they're doing Kabbalah)
- `data/conclusions/[section]/*.json` (ported entries for their section)
- PicoDB excerpts (scholar profiles, source packets relevant to their specialty)
- Research source access (e.g., paths to Copenhaver, Howlett books in the corpus)

**NOT received**:
- Full CLAUDE.md (project narrative)
- ORCHESTRATION.md (they don't manage orchestration)
- Other sections' entries
- SOURCING_PROTOCOL.md (sources are found; they synthesize)

**Total context**: ~10–15k tokens (varies by specialty)

**Specialty Examples**:

### Heretical Essay Synthesizer
Receives:
- `docs/HERETICAL_RESEARCH_PLAN.md` (full scope: Copenhaver, Dougherty, Howlett, Edelheit framework)
- Excerpt from Copenhaver *Pico on Trial* (the 13 condemned theses section)
- Excerpts from PicoDB: Copenhaver source packet, Dougherty notes
- PicoDB's `docs/MISSING_WRITINGS_ACQUISITION_LOG.md` (for transmission risk notes)
- 13 ported heretical conclusion entries

Instructions:
```
For each of the 13 conclusions:
1. State the papal commission's charge (cite Copenhaver)
2. Cite Pico's defense from the Apology if available
3. Synthesize modern scholarly debate (Copenhaver, Dougherty, Howlett, Edelheit)
4. Find 3–4 verbatim quotations total across all sources
5. Mark confidence: [VERIFIED] if checked against source, [CITED] if taken from Scholar
6. Write heretical_notes section with these three parts

Then draft an essay outline organized by theme:
- Incarnation & Embodiment (Q1, Q2, Q3)
- Eucharist & Transubstantiation (Q6, Q9, Q10)
- Soul/Intellect/Immortality (Q4, Q7, Q11)
- Kabbalah/Magic (Q5, others)
- Other theological (Q8, Q12, Q13)

Integrate quotations as you organize.
```

### Kabbalah Synthesizer
Receives:
- `docs/KABBALAH_READING_PROTOCOL.md` (how to read Kabbalah theses; Wirszubski, Busi frameworks)
- PicoDB's `docs/KABBALAH_READING_PROTOCOL.md` + related essay drafts
- Excerpts from Wirszubski *Pico's Encounter with Jewish Mysticism*
- 12 (or more) Kabbalah-related conclusions across all sections (scattered, they need to ID them)
- `docs/LIANA_SAIF_RESEARCH_GUIDE.md` (NEW: for Arabic Neoplatonic background on Kabbalah)

Instructions:
```
Find all conclusions related to Kabbalah (they're scattered across sections).
For each:
1. Explain the Kabbalistic concept Pico is invoking
2. Cite Wirszubski on Pico's use of Hebrew/Kabbalah
3. Cite Busi on the praxis/correspondence dimension
4. Find 2–3 quotations (Wirszubski or Busi preferred; Copenhaver OK)
5. Tag: ["kabbalah", "hebrew", "mysticism", "jewish_philosophy", plus others]
6. Note: Any connection to Arabic Neoplatonism? (Saif's research)

After researching all Kabbalah conclusions, draft a synthesis essay:
- Pico's Kabbalah as translational project
- Mithridates' role
- Christianization vs. fidelity to source
- Modern historiographical debate
```

### Astrology Synthesizer
Receives:
- `docs/ASTROLOGY_READING_PROTOCOL.md`
- PicoDB's astrology essay draft + Akopyan source packet
- Excerpt from Akopyan *Debating the Stars*
- Astrology-related conclusions from the 900
- `docs/LIANA_SAIF_RESEARCH_GUIDE.md` (for Arabic astrological influences)

---

## REVIEWER: What They Receive

**Files**:
- `docs/STYLE_GUIDE.md` (full version: entry template + citation format + quality checklist)
- `data/schema.json`
- `data/[role]_LINTER_OUTPUT.json` (output from citation validation script; which entries have missing quotations, invalid tags, etc.)
- All entries for the section they're reviewing (from SYNTHESIZER)
- Essays/outlines to review

**NOT received**:
- SOURCING_PROTOCOL.md
- HERETICAL_RESEARCH_PLAN.md
- PicoDB excerpts (they're validating against STYLE_GUIDE, not researching)

**Total context**: ~5k tokens per batch

**Validation checklist** (from STYLE_GUIDE):
- Every scholarly claim has a **verbatim quotation**
- Confidence levels marked: `[VERIFIED]` or `[CITED]` only
- No unsourced paraphrase
- Heretical conclusions have "charge, defense, debate" sections
- Tags are valid (from schema)
- Entry schema matches allowed fields
- Exegesis explains WHY the conclusion matters

---

## ORCHESTRATOR: Full Context

ORCHESTRATOR receives everything:
- Full CLAUDE.md, DECISIONS.md, all docs
- All phases' research queues
- All agents' outputs + session notes
- Manifest (reading + writing)

**Why**: ORCHESTRATOR coordinates across all phases and roles. They need to understand the whole system.

**Token budget**: ~30–50k per cycle (reading outputs + validating + dispatching)

---

## Context Flow Diagram

```
User Request
    ↓
ORCHESTRATOR (reads: CLAUDE.md, DECISIONS.md, all phase specs)
    ├─→ HARVESTER (reads: SOURCING_PROTOCOL.md + queue ticket)
    │                ↓ [outputs: staged JSON]
    │                ↓ [ORCHESTRATOR validates]
    │
    ├─→ PORTER (reads: STYLE_GUIDE template + schema + staged JSON)
    │            ↓ [outputs: entry files]
    │            ↓ [ORCHESTRATOR validates schema]
    │
    ├─→ SYNTHESIZER (reads: STYLE_GUIDE full + protocol + entry files + PicoDB excerpts)
    │                 ↓ [outputs: enhanced entries + essay sections]
    │                 ↓ [ORCHESTRATOR collects]
    │
    ├─→ REVIEWER (reads: STYLE_GUIDE full + schema + linter output + entries)
    │              ↓ [outputs: approval or revision requests]
    │              ↓ [ORCHESTRATOR batches approvals]
    │
    └─→ [ORCHESTRATOR updates manifest atomically]
            ↓
        [Phase complete, retrospective written]
            ↓
        [Next phase triggered]
```

---

## Special Case: Liana Saif Research Integration

For any SYNTHESIZER working on:
- **Arabic philosophers** (Averroes, Avicenna, al-Farabi conclusions)
- **Kabbalah conclusions** (medieval Kabbalah's Arabic Neoplatonic background)
- **Astrology/Magic conclusions** (Arabic astrological and magical traditions)

Agent also receives:
- `docs/LIANA_SAIF_RESEARCH_GUIDE.md` (excerpt from her *Arabic Influences on Early Modern Occult Philosophy*)
- Path to Saif's book in corpus: `E:\pdf\renaissance magic\Pico\Liana_Saif_Arabic_Influences_Early_Modern_Occult_Philosophy.pdf`

Instructions in their ticket:
```
When researching [TOPIC], consult Liana Saif's framework:
- [specific chapter/section reference]
- Look for: How did Arabic philosophers (al-Kindi, al-Farabi, Avicenna, Averroes) theorize [TOPIC]?
- How did Pico adapt or critique them?
- Quote Saif on Pico's use of Arabic sources.

Example: "Saif argues that Pico's adoption of Averroes on [X] represents a creative reconfiguration of Islamic philosophy to suit Christian esotericism."
```

---

## Summary Table

| Role | Context Size | Key Documents | Focus |
|------|--------------|----------------|-------|
| HARVESTER | ~2k tokens | SOURCING_PROTOCOL.md + queue ticket | Finding sources |
| PORTER | ~3k tokens | STYLE_GUIDE template + schema + staged JSON | Formatting |
| SYNTHESIZER | ~12k tokens | STYLE_GUIDE full + protocol + PicoDB excerpts + research sources | Research + writing |
| REVIEWER | ~5k tokens | STYLE_GUIDE full + schema + linter output | Validation |
| ORCHESTRATOR | ~50k tokens | All documentation + all phases | Coordination |

