# Incident Report: Fabricated Dougherty Verdict-Tags and a False Busi Quotation (2026-09-26)

## Summary

The user uploaded real source texts directly into this session (Farmer 1998, Copenhaver 2019/2022,
Wirszubski 1989, Edelheit 2008/2014/2022, Allen 2017, Dougherty 2008, Busi & Ebgi 2014, and others),
copied to this session's scratchpad (not committed to git — most are in-copyright scholarship). This
made REAL quotation verification possible for the first time this session, via a new script,
`scripts/verify_against_uploaded_corpus.py`. Running it against the 85 WRITER-swarm entries and then
against all 203 entries found:

- **188-239 quotations checked; the large majority (188, later 91/109 after fixes on the 85-entry
  subset) verified genuinely present**, word-for-word, in the actual source text.
- **5 confirmed fabrications**, all following the same pattern (see below).
- **3 citations misattributed to the wrong book** (real quotations, wrong Edelheit title).
- A residue of ~5-6 flagged items that are most likely genuine content from Farmer's extensive
  notes apparatus, which this particular uploaded copy of Farmer does not include (it has only the
  bare thesis text and short English glosses, not the annotation layer many entries cite) — these
  are documented as unverifiable-with-available-corpus, not confirmed fabrications.

## The fabrication pattern found

Dougherty (2008) prints a numbered table of the thirteen condemned theses with the commission's
verdict tag for each (e.g. "Wrong, erroneous, heretical.", "Outrageous, offensive to pious ears,
and unaccustomed in the universal Church."). In the source text as extracted, this table's visible
items run 1, 2, 3, 4, 5, 6, then jumps directly to 11, 12, 13 — items 7-10 are not present in the
consulted text. Those four items correspond to theses Q5 (9>9), Q6 (4>2), Q9 (4>1), and Q10 (4>10).

For all four of those theses, a WRITER agent had confidently quoted a Dougherty verdict-tag, with a
specific line number, that does **not appear anywhere in the source text**:

- `own_9_009` (Q5): "Wrong, erroneous, superstitious, heretical" — fabricated (the real Farmer/
  Wirszubski verdict quotations for this thesis, already in the entry, ARE genuine).
- `own_4_002` (Q6): "Wrong and in matters of faith erroneous" — fabricated.
- `own_4_001` (Q9): "Erroneous" — fabricated.
- `own_4_010` (Q10): "Outrageous, contrary to the opinion of the Church Fathers" — fabricated.

Each invented tag was stylistically consistent with Dougherty's real tags for neighboring items —
plausible-sounding, not random — which is exactly why a mechanical gate cannot catch this: the
fabrication is confident, well-formed prose with a specific (invented) locator. Only checking it
against the actual source text catches it.

The other nine condemned-thesis verdict-tags (Q1, Q2 x2, Q3, Q4, Q7, Q8, Q11, Q12, Q13) were all
independently verified as genuine, word-for-word matches.

## The false Busi & Ebgi quotation

`own_10_004` (thesis 10>4, "as the hymns of David serve Cabala, so the hymns of Orpheus serve
magic") claimed that Busi & Ebgi (2014) give "their own Italian translation" of this thesis at a
specific line, citing an Italian sentence as a verbatim quotation. On verification: that line
number contains completely unrelated Latin text (about the tripartite structure of the human
soul, apparently from a different Pico work). The "quotation" was, in fact, simply the writer's
own back-translation of the thesis's Latin into Italian, dressed up as a verbatim citation from
Busi's book. Fixed by removing the false claim; the entry's independently-verified Wirszubski
citation for the same thesis was retained.

## The misattribution pattern (less serious, also fixed)

Three genuine Latin quotations were correctly transcribed but tagged with the wrong work-key —
`edelheit2008` ("Scholastic Florence: Moral Psychology in the Quattrocento", a book about
unrelated topics: Alamanno Donati, Lorenzo Pisano, theories of love) instead of `edelheit2022`
("A Philosopher at the Crossroads: Giovanni Pico della Mirandola's Encounter with Scholastic
Philosophy", which is actually about Pico and does discuss the Apology in detail). All three were
confirmed present, verbatim, in `edelheit2022` and re-tagged accordingly:

- `own_9_009`: "fuisse perfidum quendam hominem et diabolicum..."
- `own_4_002`: "loquendo de possibili non de sic esse"
- `own_4_018`: "sine rationis persuasione aut motivo"

Their line numbers are now cited per this session's uploaded copy of `edelheit2022`, flagged in
each entry's `not_established` as pending reconciliation with the project's registered corpus copy
(different OCR extraction, different line numbers — same caveat as the Farmer file; see
`docs/INCIDENT_2026-09-26_PORTER_FABRICATION.md` for the earlier instance of this issue).

## What this means for the rest of the corpus

This session's uploaded texts only let me verify entries that cite these specific eleven works.
Entries citing other corpus works (Akopyan, Busi's specific other claims, Howlett, Novak, Ogren,
etc. — the "NO_CORPUS_FILE" results in the verification report) remain unverified by this pass.
The fabrication rate found here (5 confirmed among the higher-stakes condemned-thesis and Q-tag
claims specifically) should not be extrapolated as a global rate across all 203 entries, but it
does confirm that mechanical gates (`entry_gate.py`, `entry_gate_local.py`) cannot catch
confidently-worded, plausible fabrication — only source-text verification can.

## Tooling added

`scripts/verify_against_uploaded_corpus.py` — checks every `quotations[]` entry (and quoted spans
inside `commission_verdict`) against the uploaded source texts, using a whitespace-stripped
substring match to tolerate this OCR corpus's frequent word-run-together and cross-line-hyphenation
artifacts (a naive word-boundary match produced many false negatives before this was added). Writes
`data/verification/uploaded_corpus_verification.json`. The uploaded source texts themselves are
NOT committed to the repository (most are in-copyright scholarly monographs); they live only in
this session's scratchpad and will not persist past the session.

## Standing lesson

Confirmed twice now in this project's history (the original PORTER incident, `audit/A1-A4`, and
this one): an agent given a specific, plausible-sounding fact to produce, when it cannot find the
exact source, will sometimes produce a stylistically-consistent invention rather than reporting
the gap. The only reliable defense is checking claims against the actual source text — never trust
a quotation because it "sounds right" for the source.
