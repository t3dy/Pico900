# Brief: RESEARCHER for a claim packet

You are a RESEARCHER in the Pico900 edition (roles: `C:\Dev\AGENTS.md`, `docs/ORCHESTRATION.md`). You read a
scholarly source and deconstruct it into **claims, warrants and open questions**, each tied to a verbatim quotation
that a script will re-find in the source. You write one packet. You write nothing else. You do not write commentary,
prose for the site, or code.

Read first, in this order: `docs/CLAIMS_MODEL.md` (the model and the ten packet rules; it is your contract), then this
brief. The audit (`audit/A3_angelology_neoplatonism.md`) shows what happened when an agent wrote from memory: invented
quotations, invented debates, wrong page numbers. Do not repeat it. **Everything you write comes from the text you have
open on the screen, not from what you know about the topic.** If you "know" that a scholar says something, find the
sentence or leave it out.

## Tools (run from `C:\Dev\Pico900`)

```
python scripts/corpus_tool.py works FILTER               # registry keys -> which file
python scripts/corpus_tool.py grep WORK "regex" -n 60    # find lines; cite as WORK:LINE
python scripts/corpus_tool.py show WORK 8400 8520        # read numbered lines (read in chunks of ~120-200 lines)
python scripts/corpus_tool.py check WORK LINE "quote"    # would this quotation pass the gate?
python scripts/corpus_tool.py page WORK LINE             # PDF page and nearest printed bracket marker
python scripts/claims_pack.py YOUR-PACKET                # assemble + verify + print tickets
```

The files are OCR Markdown: double spaces, hyphenated line breaks, footnote numerals run into the text, `## Page N` PDF
markers, sometimes a printed page in brackets like `[199]`. The gate ignores spacing, hyphens and punctuation, so copy
the text as it stands (drop footnote numerals if you like); do not "correct" a word.

## How to work

1. Work in the range you were given. Read it **all**, in chunks, in order. Do not sample. If a chapter is outside your range,
   leave it.
2. After each chunk, append the claims it gave you to `data/claims/_work/<packet>.jsonl`, **one claim per line**, in the
   format of `docs/CLAIMS_MODEL.md` section 4. Omit `id` (the pack tool numbers them). Append from the shell with a
   heredoc, or write the file with your file tool; never leave a claim only in your head. (JSON on one line: escape
   inner double quotes as `\"`.)
3. Every few chunks run `python scripts/claims_pack.py <packet>`. Fix every ticket it prints: it shows the nearest real
   text in the source. A quotation the source does not contain is deleted or replaced, never argued with.
4. When the range is done, write `data/claims/_work/<packet>.meta.json` (researcher name, scope, `not_mined`,
   `proposed_topics`, `proposed_parties`, `notes` including cruxes and OCR trouble), run `claims_pack.py` until it prints
   `needs_fix 0`, then run `python scripts/claims_verify.py data/claims/angelology/<packet>.claims.json` and read the
   warnings (`ungrounded_entity`: a name or year in your restatement that no quotation contains; remove it or add the
   quotation).
5. You may not edit any other packet, `links`, `scores`, `parties.json`, `topics.json`, or any file outside your packet
   and its `_work` files. If you need a new topic or party, propose it in `meta.json`.

## What a good claim is

- **Atomic:** one assertion. A sentence of Black or Allen usually holds one; a paragraph holds several.
- **Restated neutrally** in `text`, in one sentence, with no name, date or number that is not in a quotation.
- **Quoted tightly:** the sentence(s) that carry the assertion, 4 to 120 words, verbatim. Use `...` to skip; `[...]` for
  anything you insert. Where the assertion needs two places, give two quotes.
- **Attributed correctly:** `scholar_claim` is the author's own argument; `scholar_report` is the author reporting a
  view held by someone else (name them in `text`; `claimant` is still the author of the file); `primary_text` is
  Pico's own words, quoted from an edition of Pico.
- **Hedged as the source hedges:** if the author writes "it seems to me", "perhaps", "the likeliest hypothesis", set
  `hedge` and copy those words into `hedge_words`. Do not upgrade a guess into a finding.
- **Warranted honestly:** say how the author supports it (`primary_text` with the quotation of Pico; `scholar_evidence`
  with the quotation of another scholar the author relies on; `argument`; `authority`; or `inference`). If the author
  gives none, write no warrant.
- **Open where the source leaves it open:** unresolved cruxes, disputed readings, "we do not know", gaps in the
  evidence, with the author's own words as `basis_quote` when they say so. Do not invent questions to look thorough.
- **Bearing on relationships:** where a claim illuminates Pico's dealings with a named person
  (`data/claims/parties.json`) say how in `bears_on`, with the kind (quarrel, correspondence, teaching, patronage,
  friendship, source, reception, trial). Only if the quotation supports it.
- **Judged for frame shift** (0-3) with a one-sentence reason if above 0. Most claims are 0 or 1.

Aim for coverage and precision, not a target count: a dense 40 pages can give 60 good claims, a thin 40 pages ten.
Prefer the claims that a commentary on Pico's angelology, or on his dispute with Ficino over the One, would need.

## Report back (under 200 words)

Packet path, claims written, verified/needs_fix from the last `claims_pack.py`, what you did not mine and why, and any
crux or surprise. Do not paste claims into the report. Say plainly what is unfinished.
