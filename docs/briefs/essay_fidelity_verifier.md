# Brief: essay fidelity VERIFIER

You are a VERIFIER (`docs/ORCHESTRATION.md`), and you did not write the essay. The citation gate has already shown that every
`[claim-id]` in the essay exists, passed the quote gate and has a second reader's `supported` verdict, and that every quoted string is
verbatim. It cannot show that a **sentence** says no more than the claims it cites. That is your job.

Your input is a sheet from `python scripts/essay_sheet.py FILE` (`data/verification/essays/<slug>.sheet.md`): each cited sentence beside
the CURRENT restatement and first quotation of each claim it cites. Claims are corrected after an essay is drafted, so a sentence written
from an older, stronger restatement may now overstate. Open the source (`python scripts/corpus_tool.py show WORK FROM TO`) whenever the
restatement alone leaves a doubt.

## For each sentence, decide

- **faithful**: it says no more than the cited claims (with their hedges) support.
- **overreaches**: it adds anything the claims do not give: a stronger verb (concludes, proves, shows for suggests, argues, seems); a dropped hedge or
  conditional; a cause, motive, date, name or number not in a cited claim; a generalisation ("scholars agree", "always", "the whole tradition") from one scholar;
  two scholars or two doctrines merged into one position; an evaluation ("striking", "decisive") the sources do not make.
- **misattributed**: a scholar's report or inference is stated as the essay's own fact, or as Aquinas's, Scotus's, Dionysius's or Ficino's own position
  when the claim gives it only through the scholar (neither Aquinas nor Dionysius is in the corpus); or a claim by one scholar is credited to another; or the
  Dionysian orders, the Hebrew hierarchies and the sefirot are merged in the essay's own voice.

Sentences ending `(ed.)` are the editor's own inference: judge only that they assert no uncited fact. Sentences with no citation are listed at the end of the
sheet: flag any that assert a fact (a name, date, number, doctrine or attribution) rather than connect or frame.

## Output

`data/verification/essays/<slug>.fidelity.json`:

```json
{ "essay": "docs/essays/....md", "verifier": "EV-1", "date": "2026-09-28",
  "judged": [ {"sentence": "S014", "verdict": "faithful"},
              {"sentence": "S015", "verdict": "overreaches",
               "reason": "cited claim says Howlett 'suggests'; sentence says she 'shows'",
               "suggested_sentence": "Howlett suggests that ... [claim-id]"} ],
  "patterns": "one or two lines on recurring problems" }
```

Keep each `suggested_sentence` faithful to the essay's voice and keep its `[claim-id]` citations exactly as in the sheet. Judge EVERY sentence in your
range. You may not edit the essay. Report under 150 words: counts by verdict, the recurring pattern, and any sentence that puts a scholar's report of Aquinas, Scotus or
Dionysius in the essay's own voice.
