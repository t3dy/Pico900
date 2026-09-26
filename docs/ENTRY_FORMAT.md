# Entry format (Farmer-keyed), v2

One JSON file per thesis in `entries/<slug>.draft.json` (WRITER output) and `entries/<slug>.json` (after a
VERIFIER promotes it). `<slug>` is `hist_07_002` for 7.2 and `own_04_013` for 4>13 (see
`research-packets/INDEX.md`). Field meanings: `docs/EDITORIAL_STANDARD.md` s5; provenance rules:
`docs/ORCHESTRATION.md`. The build renders only fields that carry locators.

## Locators

A locator is `work-key:line` into the file named for that key in `data/corpus/registry.json`
(e.g. `farmer1998:21767`, `copenhaver2022:6908`). A locator names the line where the claim's evidence
begins. Line numbers are those of the Markdown/plain-text file, not printed pages; add the printed page in
`page` when the file shows it (`## Page N` markers give the PDF page).

## Fields

```json
{
  "thesis_id": "4>13",
  "tier": "A",
  "latin": "Non assentior communi sententiae theologorum dicentium posse deum quamlibet naturam suppositare, sed de rationali tamen hoc concedo.",
  "latin_source": "farmer1998:21767",
  "latin_note": "Copenhaver prints the Apology's reading 'rationabili tantum' (copenhaver2022:6908); Farmer 'rationali tamen'.",
  "translation": "I do not assent to the common opinion of the theologians who say that God can make any nature whatever a supposit; I grant this only of a rational nature.",
  "translation_note": "'suppositare': to make a nature the supposit of a divine Person, as the Word assumed a human nature; not 'suppose'.",
  "translator": "machine-drafted 2026-09-25 (agent WRITER-A1), checked against Farmer's sense at farmer1998:21814; awaiting human check",
  "pico_stance": "endorses",
  "attribution": "Pico's own opinion (section 4>, theological conclusions against the common mode of the theologians)",
  "sources": [
    {"text": "Henry of Ghent, Quodlibet 13.5", "locator": "copenhaver2022:5606", "pico_relation": "supplies most of Pico's defence of Q4 in the Apology"}
  ],
  "doctrine": "Prose. Each factual sentence ends with a locator in parentheses.",
  "context": "Prose with locators.",
  "reception": "Prose with locators; for a condemned thesis, the commission's verdict formula quoted with its locator.",
  "historiography": "Prose with locators; named scholars, positions, disagreements.",
  "connections": ["4>2", "4>8", "3>49"],
  "condemned_flag": true,
  "commission_verdict": "\"derogates from divine omnipotence, and this savors of heresy\" (farmer1998:21793); Copenhaver's rendering copenhaver2022:6845-6853",
  "quotations": [
    {"text": "Henry holds here a more radical and extreme position than Pico", "work": "edelheit2022", "line": 7748, "verbatim": true}
  ],
  "not_established": ["Whether Pico read the Centiloquium (copenhaver2022:2187 leaves it open)."],
  "writer": "WRITER-A1 (agent), 2026-09-25",
  "verifier": null,
  "verified_date": null
}
```

## Rules the gate enforces (`scripts/entry_gate.py`)

1. Every locator's work-key exists in the registry and its line number lies inside that file.
2. Every item in `quotations` is found verbatim (whitespace- and OCR-normalised) within 3 lines of its locator.
3. `translation` is not identical, nor near-identical, to the text at Farmer's English line (copyright).
4. Prose fields contain no sentence without a locator, except sentences inside `not_established`.
5. No scholar surname appears in prose that does not appear in the registry or in `quotations`.
6. `tier` D entries have only `latin*`, `translation*`, `translator`, `pico_stance`, `attribution`.

A draft that fails is returned to the WRITER with the failing rule; it is never patched by the gate.
