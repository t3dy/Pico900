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

## Lessons from the first semantic verification (2026-09-26): what a second reader kept finding

Across seven verifiers and about 400 judged claims, 85-93% were `supported`, 7-15% `overreach`, and about 1% were `wrong`
(the Oration packet, judged in full, was worst at 15%). The failures repeat; avoid them:

1. **Hedges and conditionals must survive in `text`, not only in `hedge`.** "Black says it is likely that ..." stays "likely";
   "if the thesis contained nothing new" stays a conditional; "I have proposed" stays a proposal. "Surely" is emphasis, not a hedge.
2. **Quote through the end of the clause your restatement uses.** Many quotations stopped at a page break one sentence short of
   the word the restatement then used (a name, "empyrean", "Hierotheus"). If the subject is a pronoun, include the sentence that
   names it.
3. **Two-layer reports.** When Ficino reports the Averroists, or Black translates Dionysius, or Edelheit reports Garsia, the
   restatement names who holds the view. Do not restate the reported view as the reporter's, or the reporter's translation as the
   author's words.
4. **Do not upgrade a parallel to a source.** "Cf.", "See", "echoed by", "evidently connected" are parallels, not sources, causes or
   influence. `bears_on` kind `source` only where the text says the person or work was a source; otherwise `other`.
5. **`bears_on` needs a quotation that names the party.** `quote_index` must point to a quotation that contains them; a note that
   Pico inherited, used or answered something needs a quotation saying so. De ente never names Ficino: anything about Ficino there
   comes from Miller's report or a scholar's inference, and says so.
6. **Pico's disclaimers stay disclaimers.** "Let no one expect from us ..." is not a positive assertion of the thing disclaimed.
7. **Do not give Pico's gloss to the authority he cites**, or pad an endnote pointer with neighbouring notes.
8. **`frame_shift` 2 or 3 is rare.** Plain exposition of a text, however important, is 0 or 1. Do not justify a 2 by cross-text links.
9. **Check `pico_locus.ref` against the section you quoted** (Oration section numbers are in the edition).
10a. **`bears_on` needs its own check, separate from the main text.** A claim's restatement can be fully supported while its
    `bears_on` still overreaches: verify that the named party actually appears in the specific quote its `quote_index` points to,
    not just that the claim in general is about the right topic. A tag naming a shared tradition ("the Ancient Theology of the
    Gentiles") is not a tag naming a specific person unless that person is named too.
10b. **An unquoted clause tacked onto an otherwise well-quoted claim is still an overreach**, even when most of the sentence is
    fine — a fact from a different, unquoted sentence, or from a source note that was never quoted at all, must be cut or given
    its own quotation.
10. **Editing a claim after a verifier judged it:** increase its integer `revision` by 1 (add `"revision": 1` if absent); the
    verdict is bound to the claim's content plus `revision`, and only a bump makes the verifier look again.

## Report back (under 200 words)

Packet path, claims written, verified/needs_fix from the last `claims_pack.py`, what you did not mine and why, and any
crux or surprise. Do not paste claims into the report. Say plainly what is unfinished.
