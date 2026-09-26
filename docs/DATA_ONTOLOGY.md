# Data ontology: what the research layer records, and where

Written 2026-09-25 to match the code (`scripts/harvest_mentions.py`, `scripts/build_dossiers.py`). Sections
marked *planned* are not implemented; do not cite them as if they existed.

## Principle

Every record is a fact about a text at a location. The unit of location is `work-key:line`, where the key names
an entry in `data/corpus/registry.json` and the line is a line of that entry's file. A record without a locator
does not exist for the edition. Counts and rankings are computed from records; they are never written by hand
or by a model.

## Entities (implemented)

| entity | file | fields |
|---|---|---|
| **Work** | `data/corpus/registry.json` | key, author, title, year, kind, role (`edition_farmer`, `trial_copenhaver`, `scholastic_edelheit`, `kabbalah_wirszubski`), path, locator_unit, plain_text_twin, source_file. 78 works after de-duplication; hand-labelled entries are bibliographically reliable, `(from file name)` entries are not yet |
| **Thesis** | `data/inventory/theses.json` | thesis_id (Farmer: `7.2`, `4>13`), section, section_name, n, latin, latin_line, apparatus_1486 [{line,text}], folio_1486, farmer_english_line (pointer only), farmer_english_words, farmer_note_lines, cumulative_number, tier, pico_stance |
| **Mention** | `data/ontology/mentions/by_thesis/<slug>.json`, `by_scholar/<key>.json` | work, line, method (`farmer_id`, `q_number`, `edelheit_chapter`, `latin_quote`, `wirszubski_conclusio`), evidence (the matched string(s)), context (about 700 characters around the line), resolved (Wirszubski only) |
| **Cross-reference** | `data/ontology/connections/farmer_crossrefs.json` | thesis -> theses Farmer's note on it refers to (his "Cf." network; 731 theses, 3,306 edges) |
| **Thesis aggregate** | `data/ontology/theses.json` | per thesis: n_works, n_mentions, works, by_method, farmer_crossrefs, n_farmer_notes, entities (gazetteer counts of persons/concepts in notes and contexts), suggested_tier, condemned, q, packet path |
| **Statistics** | `data/ontology/stats.json`, `MENTION_STATS.md` | per thesis and per work; coverage by section; most-discussed theses |
| **Condemned thesis** | `data/inventory/condemned_thirteen.json` | q, topic, farmer_id, farmer_line, Latin incipit (Farmer OCR), audit result, dates |
| **Research packet** | `research-packets/<slug>.md` | the human-readable join of all the above for one thesis, plus WRITER instructions; `translation-sheets/T*.md` are the tier-D subset by block |
| **Entry** | `entries/<slug>.draft.json` -> `<slug>.json` | `docs/ENTRY_FORMAT.md`; the only place prose lives |

Slugs: `hist_07_002` for 7.2, `own_04_013` for 4>13, `own_7a_003` for 7a>3.

## Derived measures (implemented)

- `n_works`: distinct works other than Farmer's edition with at least one mention record.
- `suggested_tier`: A if condemned or n_works >= 3; B if n_works >= 1; C if Farmer has a note or a cross-reference; D otherwise.
- Gazetteer `entities`: counts of ~100 named persons and concepts (regexes in `build_dossiers.py`) in the thesis's
  Farmer notes and mention contexts. They rank what a packet is about; they are not claims.

## Relations (implemented as data, not as a graph store)

`cites` (Work -> Thesis, via Mention), `quotes_latin` (Mention.method = latin_quote), `refers_to`
(Thesis -> Thesis, Farmer cross-reference), `condemned_as` (Thesis -> Q number), `belongs_to` (Thesis -> section).

## Planned (not implemented)

- Claims: atomic, typed statements extracted from mentions (doctrinal_content, historical_event,
  interpretive_position, source_identification) with counter-claims. Today the claim lives in the entry prose
  with its locator; a claim store would let disputes be queried across entries.
- Historiographical disputes: pairs of claims from different works about one thesis.
- Person and concept authority records (`data/authorities/`) for the site's people and concept pages.
- Topic-based harvesting (English keywords), needed for the ~480 theses no scholar cites by id or Latin; it will
  produce leads with lower confidence and must be marked as such.
- A SQLite view over the JSON for the site build (the PicoDB FTS index at `E:\pdf\...\Pico\db\pico.db` can serve as
  a search backend meanwhile).

## How the site will use it

Each thesis page: Latin with folio and apparatus; original translation; commentary by tier; "cited by" list from
mentions (work, page where known); Farmer's cross-references as links; persons/concepts as links to authority pages
once those exist. Nothing renders from a packet directly; only from a verified entry.
