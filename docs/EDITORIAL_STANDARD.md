# Editorial Standard: Pico900

**Status**: authoritative. Supersedes `docs/PICO900_STYLE_GUIDE.md` and `docs/STYLE_GUIDE.md`
(both moved to `docs/archive/v1-style/`). Written 2026-09-25 from the audit in `audit/`.

The edition addresses a reader with a doctoral training in the history of philosophy, who will
check a reference and be entitled to find it right. Every rule below serves that reader. The
standard for prose is a good monograph; the standard for the apparatus is a good critical edition.

## 1. The one rule

**Every proposition an entry asserts carries its evidence, or is marked as the editor's inference.**
A locator (work, page or line, edition) is evidence. "Scholars agree" is not. A field without
evidence is shown as *not yet edited*; it is never filled to look finished. The audit found that the
pipeline filled fields to satisfy a count. A blank labelled blank is scholarship; filler is not.

## 2. Three voices, always distinguishable

| voice | what it is | how it appears |
|---|---|---|
| **Pico** | the Latin text and the editor's translation of it | Latin panel and English panel, each with its source line |
| **The tradition** | what Farmer, Copenhaver, Wirszubski and others say | verbatim quotation with page locator, or a paraphrase that names the author and page |
| **The editor** | interpretation, connection, gloss | plain prose, unmarked by quotation, and never presented as a scholar's view |

An LLM-drafted sentence is editorial voice at best. It never carries a scholar's name, and it is
never shown as a quotation. Machine involvement in a translation is disclosed on the entry.

## 3. Evidence grades

The grades in `scripts/integrity_gate.py` are the vocabulary; they replace `[VERIFIED]/[CITED]/[INFERRED]`.

| grade | meaning | may render as edition text |
|---|---|---|
| `sourced` | text plus a locator, re-found in the source by a second agent | yes |
| `unverified` | plausible text, no locator or not yet re-found | yes, with a visible badge |
| `template`, `placeholder`, `misfiled`, `restricted`, `quarantined`, `missing` | filler, empty, wrong field, in copyright, proven wrong, absent | never |

Promotion to `sourced` is the VERIFIER's act (`docs/ORCHESTRATION.md`), not the writer's.

## 4. The text

**Numbering.** Cite a conclusion by Farmer's numbering: `7.2` for the second thesis of section 7
(Averroes) in the historical part, `4>8` for the eighth thesis of section 4 in Pico's own
opinions. The retired `S1..S9` ids are not used. Where Farmer's headings and his chart disagree by one
(sections 15, 25, 4>, 11>), record the discrepancy in a `numbering_note` field. Inventory:
`data/inventory/farmer_structure.json`.

**Whose thesis it is.** The first 402 theses report the doctrines of named authorities ("according to
Averroes"). Pico commits himself to none of them by stating it. Each entry records
`attribution` (Averroes, Proclus, Pico's own) and `pico_stance` (reports / endorses / revises /
reverses / unstated), with the evidence. Reading a section-7 thesis as Pico's own opinion is the
commonest error and the audit found it in the drafted commentary.

**Latin.** Pico's Latin is in the public domain. State the copy-text (Farmer 1998 unless changed;
the 1486 Rome print of Eucharius Silber is the witness of record, colophon dated 7 December 1486,
Farmer l. 28040-28042). Reproduce the whole thesis, never the first line. Normalise `u/v` and `i/j`
in one declared direction; record expansions of abbreviations in italics or brackets; keep punctuation
as the copy-text has it; mark a hyphenated line break as a repair, not a word. An OCR fragment
ending mid-word is a defect, not a text. Wrap all Latin in `lang="la"`.

**Translation.** English renderings are original, prepared from the Latin, and *checked against*
Farmer's translation, which is © 1998 MRTS and is not reproduced. No entry may carry Farmer's English
under the source `Farmer 1998`; the gate grades that `restricted`. Each translation records its
translator (person or "machine-drafted, human-checked by NAME"), date, and any crux. A Latin thesis
whose sense is disputed carries a `translation_note` naming the choices. No template sentence ever
occupies the English slot.

**Apparatus.** Give a short apparatus criticus only where witnesses differ and the difference
matters; otherwise say the entry follows the copy-text. Give Pico's sources with locators where
Farmer or the scholarship identifies them (Farmer's notes do so for most theses).

## 5. Anatomy of an entry

Fields in this order. A field with no evidence is omitted from the page, not filled.

1. **Text**: Latin, translation, `translation_note`.
2. **Attribution and stance**: whose thesis, and Pico's relation to it.
3. **Sources**: what Pico is reworking, with locators (the text he had, in whose translation).
4. **Doctrine**: the philosophical argument. Define each technical term at first use (supposition,
   *actus essendi*, agent intellect, sefirah). State the problem the thesis answers.
5. **Context**: the school debate, the Florentine and Roman setting, the reason a Quattrocento
   reader would care or object.
6. **Reception**: the commission's verdict where there is one, Pico's reply in the *Apologia*, later readers.
7. **Historiography**: named scholars, what each claims, with page locators; disagreements shown.
8. **Connections**: other theses (by Farmer id) and other works of Pico that bear on this one.
9. **Apparatus**: status grades, verifier, date, and open questions ("not established by the sources consulted").

**Tiers.** Uniform depth across 900 theses is a promise no pipeline keeps, and the audit shows what
happens when one is made. Depth is assigned in advance and recorded in the ledger:

| tier | entries | content | length |
|---|---|---|---|
| A | the thirteen condemned; theses the scholarship discusses at length | fields 1-9 in full | 500-1,000 words |
| B | theses with an identified source and some scholarship | fields 1-4 and 7 where available | 150-400 words |
| C | the rest | fields 1-3 and a one-sentence gloss | under 100 words |
| D | not yet researched | fields 1 only (Latin and translation) with the "commentary forthcoming" state | none |

## 6. Prose

**Register.** Assertive where the evidence permits, explicit where it does not. Calibrate with an
evidence term, not a soft verb: *attested* (a witness says so), *inferred* (the editor argues it,
and the argument is given), *conjectured* (no witness), *unknown*. "May suggest" and "arguably" are
not evidence terms.

**Corrective contrast.** The construction "not X but Y" is permitted when X is a named position and
Y is argued against it ("Burckhardt read the Oration as a manifesto; Copenhaver shows that its
audience was the Roman disputation, not Florentine humanism"). It is banned as a reflex, where X
is a strawman nobody holds ("not incidental but constitutive"). The previous guide banned the
construction in one section and used it in five of its eight exemplars; the rule is now stated so
that it can be followed.

**Also banned.** Announcing what is coming ("this entry will discuss"); recapping what was just said;
"it is important to note"; unnamed scholarship ("scholars have argued"); frequency words in place
of a number ("often", "several"); intensifiers and puff ("profound", "seminal", "rich"); the terms
in section 9. `scripts/style_lint.py` counts these. A clean lint is necessary and never sufficient.

**Close on significance.** End an entry on what the thesis shows about Pico, the tradition, or the
scholarship on it, not on a summary of the entry.

## 7. Quotation

Verbatim, in quotation marks, with author, work, edition and page. Ellipses mark every omission,
brackets every insertion, `[sic]` every reproduced error. Keep quotations short (a sentence or two).
A paraphrase is never set in quotation marks. Check who wrote what you quote: a volume's introduction
is not by the volume's principal author (the audit found one such misattribution). If a quotation is
taken from a scholar quoting another, cite both and say so. No quotation is accepted until a second
agent has found it in the source; `scripts/integrity_gate.py --verify-quotes` is the mechanical first pass.

## 8. Bibliographic and biographical apparatus

Genres beyond the entries (scholar profiles, bibliography, a chronology of Pico's life, people around
Pico) are specified here and built from **authority records** in `data/authorities/`, one JSON file
per person or work, each fact with a locator. The prose is composed from the records, not the other
way about. A record for a work takes its full author name, title, publisher, place and year from the
title page or copyright page of the copy consulted; a surname alone is never enough.

Established from the corpus (and to be reconfirmed when the records are made): Copenhaver, *Magic and
the Dignity of Man* (Harvard UP, Belknap, 2019); Copenhaver, *Pico della Mirandola on Trial* (Oxford
UP, 2022); Farmer, *Syncretism in the West: Pico's 900 Theses (1486)* (Tempe: MRTS 167, 1998);
Howlett, *Re-evaluating Pico* (Palgrave Macmillan, 2021); Fornaciari's edition of the *Apologia* (2010).
A chronology entry gives date, event, place, evidence status, and the source. The guide contains no
model paragraph about a real person: every earlier example of that kind, checked against the sources,
was wrong in some detail.

## 9. Vocabulary

Use *Kabbalah*, *conclusions* / *theses* consistently, *divine names*, *separate substances*, *theurgy*.
Avoid "Renaissance man", "ahead of his time", "genius", "magical thinking", "superstition", "merely",
"simply". Dates: 1486 is publication, March 1487 the commission's verdicts, 4 August 1487 the bull. Say
"censured by the commission" for the thirteen and "condemned by the bull" for the work as a whole.
Name Hebrew, Arabic and Greek terms in one declared transliteration.

## 10. What every page shows

The status of each field (badge for `unverified`), the translator and source of the English, the
copy-text of the Latin, the date the entry was last verified, and a link to the corrections log.
Unedited fields say so. Draft banner site-wide until the inventory (900 by Farmer's numbering) is
complete. Headings in order, one `h1`, `lang` on every foreign-language span, keyboard-reachable search.

## 11. Exemplars

Model entries live in `docs/exemplars/`, and only after a VERIFIER has re-found every locator in them.
Candidates written during the audit are in `audit/A1_conclusions.md` section 4 (theses `4>2`, `4>13`,
`11>23`, `7.2`). Until promoted they are candidates and are not to be imitated as if authoritative.
