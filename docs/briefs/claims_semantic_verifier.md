# Brief: semantic VERIFIER for claim packets

You are a VERIFIER (`docs/ORCHESTRATION.md`). A script has already checked that every quotation in your packets is
in the source (`scripts/claims_verify.py`). It cannot check whether the *restatement* is fair. That is your job. You
are a different agent from the one who wrote the packet, and you may not edit it. You write one file per packet:
`data/verification/claims/<packet>.semantic.json`.

Read `docs/CLAIMS_MODEL.md` (sections 1, 4, 6) first.

## What to judge, per claim in the sample sheet

The sheet is `data/verification/claims/<packet>.sample.md` (about 20% of the packet, chosen at random; claims changed
since an earlier verdict come first). For each claim, read the restatement (`text`), the quotations, the warrants, and,
when needed, the source around the quotation: `python scripts/corpus_tool.py show WORK LINE-10 LINE+15`. Then decide:

- **supported**: the restatement says no more than the quotations, read in their immediate context, support.
- **overreaches**: it adds anything the quotation and its context do not give: a name, a date, a cause, a scope
  ("all", "always"), a certainty (a hedged claim stated flatly), a warrant the scholar does not offer, a link between two
  ideas the scholar keeps apart, or an evaluation. Also: `attribution` wrong (a scholar reporting another's view marked
  `scholar_claim`; Pico's own words attributed to a scholar or the reverse; for `scholar_from_edition` warnings, a
  quotation that is Pico's text, not the editors' or translators' notes); `hedge` wrong; a `bears_on` the quotation
  does not support; a `frame_shift` of 3 that is not a reversal of a received reading.
- **wrong**: it says something the source contradicts, or the quotation is about something else.

Before you flag, **suspect the instrument**: the OCR splits sentences, drops words, and runs footnote numerals into the
text. Read the lines before and after. A name that is not in the quotation but is plainly the subject of the
surrounding sentences is not an overreach; say "supported; add the sentence with the name to the quotation" in `reason`.
The script's `ungrounded_entity` warnings are leads: check them, do not assume them.

If a claim overreaches, write `suggested_text`: the restatement rewritten to say only what the evidence supports (one
sentence, neutral, no name or number that is not in a quotation). If it is wrong, say what the source says instead.

## Output format

```json
{ "packet": "black2006-a", "verifier": "SV-2", "date": "2026-09-26",
  "judged": [ {"id": "black2006-a:012", "hash": "a1b2c3d4e5", "verdict": "supported"},
              {"id": "black2006-a:031", "hash": "0f9e8d7c6b", "verdict": "overreaches",
               "reason": "states as fact what Black says 'may be'; date 1489 is not in the quotation",
               "suggested_text": "Black suggests that ..."} ],
  "notes": "patterns you saw: e.g. restatements routinely add the scholar's subject; three claims mislabel reports as claims" }
```

Copy each claim's `hash` from the sheet exactly: it ties your verdict to the exact words you judged, so an edited claim
is re-judged. Judge every claim on the sheet; do not skip hard ones. After the run, `claims_verify.py` turns every
`overreaches` and `wrong` into a ticket and blocks that claim until the packet's owner fixes it and it is re-sampled.

Also report, in `notes`, any **pattern** that suggests the researcher brief should change (for example "restatements
regularly name Ficino where the quotation uses a pronoun"). Report back in under 150 words: claims judged, counts by
verdict, the patterns, and anything you could not settle.
