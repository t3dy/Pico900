# Editorial Standard — Pico900

**Purpose**: One unified standard for every conclusion entry, at PhD level. This file is the source of truth for what "done" means. Any agent writing or reviewing entries must follow this.

## Core Rule: Provenance Over Volume

An entry with an honestly-marked gap is worth more than an entry with a fabricated quotation. **Never invent**:
- A Latin incipit you have not read in a source
- A scholar quotation with a page number you have not verified
- A translation attributed to a named source you did not consult

If content is synthesized from general/training knowledge rather than a specific consulted source, it MUST be marked `[SYNTHESIZED — needs verification against primary/secondary source]`. This is not a failure state; it is the honest default until sourcing work happens.

## Provenance Grades (apply to every field)

- **VERIFIED**: Directly read/quoted from a named source with a locator (page, section, line). Quotation is verbatim.
- **CITED**: A scholar or work is known to discuss this thesis (from training knowledge or secondary reference), but the exact quotation/page has not been pulled and confirmed.
- **SYNTHESIZED**: Original explanation or translation composed without a specific consulted source. Philosophically informed but not sourced.
- **UNSTARTED**: Placeholder only.

Every `scholar_citations` entry must carry one of these grades. An entry cannot claim `commentary_status: complete` while any citation is graded UNSTARTED, and cannot claim VERIFIED grade for a quotation that wasn't actually cross-checked in this session against a real text.

## Per-Entry Requirements

1. **Latin incipit**: sourced (critical edition/Farmer) or explicitly marked `[TO_SOURCE]`. Never fabricate Latin.
2. **Translation**: marked with translator + method (LLM-synthesized vs. sourced from megabase/scholar).
3. **Exegesis** (1–2 paragraphs): philosophical content — what the thesis claims and why it matters. May be SYNTHESIZED grade if no source consulted, but must be philosophically accurate, not generic filler ("this thesis reflects Pico's syncretic project...").
4. **Metadata** (required for every conclusion, not optional):
   - `philosophical_relevance`: what philosophical question/school this thesis engages
   - `historiographical_relevance`: why scholars have cared about this thesis (debate, trial, reception)
   - `relationships`: which other conclusions, philosophers, or Pico's other works (Oration, Heptaplus, Apologia) this connects to
   - `tags`: from the allowed tag set in schema.json
5. **Heretical flag**: true only for the 13 conclusions actually condemned in 1487 (see `data/conclusions/Heretical/`). Do not apply loosely.

## Banned Moves (style_lint targets)

- Generic AI-essay filler: "This conclusion demonstrates Pico's remarkable synthesis of..." with no specific content
- Quotations without a locator
- Invented scholar names or invented works
- Treating SYNTHESIZED content as if it were VERIFIED in downstream summaries/reports

## Status Field Definitions

- `unstarted`: stub only, no research done
- `draft`: exegesis written, citations not yet graded/verified
- `sourced`: at least one VERIFIED or CITED citation present
- `complete`: exegesis + metadata + 2+ citations at CITED or better grade
- `reviewed`: a second pass (different agent or human) has checked the above

## Applies To

- All 900 conclusion entries in `data/conclusions_manifest.json`
- The Heretical essay (`docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md` and successors)
- Any commentary or synthesis document

## Reporting Honesty

When an agent reports completion ("all 95 conclusions sourced"), the report must state the provenance grade breakdown (e.g., "12 VERIFIED, 40 CITED, 43 SYNTHESIZED"), not just a count. A completion report that doesn't break down grades should be treated as unverified.
