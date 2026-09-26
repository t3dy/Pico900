# Research notes, 2026-09-25: building the knowledge pipeline for the 900 theses

Running notes from the session that built the harvest pipeline. Facts here were established by reading the
files named; anything not yet checked is marked so. Later agents: extend this file, do not rewrite it.

## What the corpus actually is

- 73 Markdown conversions in `E:\pdf\renaissance magic\Pico\Markdown\` (OCR; multiple spaces, hyphenated
  line breaks, `## Page N` markers giving the PDF page). Audits A1-A4 and V1 cite these by line, so they are the
  locator files. 92 plain-text drafts in `...\Pico\plain_text_drafts\` (audiobookmaker output: same OCR with
  whitespace collapsed; 19 works exist only there, e.g. Vanden Broecke *The Limits of Influence*, Rabin 2010,
  the HOPOS 2021 Ficino/Pico cosmology article, Cassirer 1942). Registry: `data/corpus/registry.json` (82 works
  after de-duplication).
- The pre-existing PicoDB portal under the same folder (`db/pico.db`, FTS5 over 10,538 pages; `data/pico_ontology.json`)
  is a usable full-text index but its summaries are LLM-authored: leads, not evidence (`CLAUDE.md`).

## How each scholar refers to a thesis (the citation resolver's basis)

| work | form | resolution |
|---|---|---|
| Farmer 1998 | `7.2` (historical), `4>13` (own opinion); in the *heading* lines of the Latin/English pages the OCR turns `>` into a digit (`421.` = 4>1, `2712.` = 2>12) and sometimes misreads section or thesis digits (`5762.` = 3>62, `3765.` = 3>63); in notes `4>13` survives | `scripts/extract_farmer_theses.py`: section span + expected-next-number; clean vs garbled tokens |
| Copenhaver 2022 | `Q1`..`Q13` (the Apology's order), 430 occurrences | `data/inventory/condemned_thirteen.json` maps Q -> Farmer id |
| Edelheit 2022 | "thesis 14 according to Albert the Great", or bare "thesis 6" inside a chapter devoted to one scholastic (ch. 6 Albert = section 1 ... ch. 11 Giles = section 6; printed page = PDF page - 11) | chapter page ranges in `harvest_mentions.py` |
| Wirszubski 1989 | `CONCLUSIO XXIII` headings; OCR drops trailing numerals (`CONCLUSIO X` for XIII-XVI); two runs (the 47 of section 28, the 72 of 11>) | roman numeral + confirmation by a Latin-quotation hit within 15 lines |
| Busi/Ebgi 2014, Dougherty 2008, Ogren 2009, the German Kabbalah study | Farmer-style `d>d` (88, 43, ...) and verbatim Latin | `farmer_id` detector; Latin shingles |
| everyone | verbatim Latin quotations | 4-word shingles, normalised u/v, i/j, ae/e, OCR spacing and hyphenation; >=2 distinct shingles in 25 lines |

## Findings while building (each with where to look)

- Farmer's colophon (F:28040-28042): printed at Rome by Eucharius Silber, 7 December 1486. The "1486 condemnation"
  wording in older repo files is wrong; commission Feb-Mar 1487, bull 4 Aug 1487 (A2; Black gives 8 Aug).
- Farmer's chart of the historical theses (F:10566 ff.) and his section headings disagree by one in four places
  (Theophrastus III/4, Pythagoras XIII/14, 4> XXXI/29, 11> LXXI/72); the parser uses the actual counts and records
  the discrepancy in `data/inventory/farmer_structure.json`.
- Farmer prints a running cumulative number in parentheses on some English lines, e.g. `(685)` at 7a>3, `(750)` at
  7a>68, `(755)` at 7a>73, `(900)` at 11>72: an independent check on the numbering.
- Sections 1-6 (the Latin scholastics, 115 theses) have no coverage in the repo at all; Edelheit 2022 discusses them
  thesis by thesis (ch. 6-11) and Edelheit's Part 3 reports the contemporary attacks (Torni, Galgani, Garsia, Caroli,
  Cittadini, Pomponazzi). That is where the historiography of the scholastic theses will come from.
- The 1486 apparatus lines (`421. 1486 inexistat. Eucharistiae`) are Farmer's record of the editio princeps readings:
  useful for the Latin editorial note field.

## Decisions taken in this session (recorded in DECISIONS.md)

- The inventory is derived from Farmer's OCR by script; ids inferred from sequence are logged for a VERIFIER.
- Mentions are harvested deterministically; an LLM never decides whether a scholar "discusses" a thesis. The packet
  is the WRITER's only input. Statistics (works per thesis, mentions per work) come from the harvest, so they cannot
  be inflated by a writer.
- Tiers are suggested from the statistics (A condemned or >=3 works; B >=1; C Farmer only; D Latin only), and Ted
  can override in `data/ontology/theses.json`.

## Open questions for later agents

- Q11: 9>8 ("Miracula Christi non ratione rei factae ...", F:25204) is the working identification; unconfirmed.
- Latin collation against the Brown edition and the 1486 print has not been done; Farmer's OCR is the copy-text.
- The gazetteer in `build_dossiers.py` is a first list; add persons as packets reveal them.

## Results of the first full run (evening)

- Inventory: 900/900; 149 cumulative numbers agree; 2 sequence-inferred ids (3>63, 7a>63) checked by eye.
- OCR lessons for the parser, all now handled: `>` printed as a digit in heading lines; section and thesis digits
  misread (`5762` = 3>62, `3765` = 3>63); comma or colon after the id; `/` for a digit (`2/.2` = 27.2); `-` for `>`;
  apparatus lines dated 1487 as well as 1486, some not beginning with the year ("colon retained from 1486 edition");
  folio marks `<14r/14v>` appended to the Latin; a stray leading number (`74:  62. Vtrum ...`).
- Harvest: 421 theses cited by at least one scholar, 479 by none; the uncited are almost all in sections 7-27.
  Edelheit 2022 alone accounts for the scholastic theses (137 distinct); Wirszubski for 136 Kabbalistic ones;
  Copenhaver 2022 for the 13 condemned (404 records). The German *Erkenntnistheorie und christliche Kabbalah* study
  (author still to be confirmed from its front matter) cites 95 theses and is worth a bibliographic check.
- A regex written into a script through a shell heredoc lost its `\b` as a backspace character twice today; write
  patches to a file and run the file (`scratchpad/fix_backspace.py` repairs the symptom; the cause is the heredoc).
