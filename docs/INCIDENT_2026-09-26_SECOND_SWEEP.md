# Incident Report: Second Sweep of Fabricated/Misattributed Quotations (2026-09-26)

## Summary

After reaching 900/900 draft coverage (D-24), `scripts/verify_against_uploaded_corpus.py` was run against
the full `entries/` corpus a second time, checking every `quotations[]` entry against this session's real
uploaded copies of Farmer 1998, Copenhaver 2019/2022, Wirszubski 1989, Edelheit 2008/2014/2022, Allen 2017,
Dougherty 2008, and Busi & Ebgi 2014. This flagged roughly 30 additional NOT_FOUND quotations beyond the
5 fabrications and 3 misattributions already fixed and documented in
`docs/INCIDENT_2026-09-26_DOUGHERTY_VERDICT_FABRICATION.md`. Four batches (A-D) of investigation and
remediation followed, each committed separately:

- **Batch A** (`74a4e22`): `own_4_010`, `own_4_018`, `own_4_019`, `own_4_020`, `own_4_029` (condemned-thesis
  entries).
- **Batch B** (`fd3a50b`, part of `425acd8`): `own_9_001`, `own_9_003`, `own_9_004`, `own_9_006`, `own_9_013`,
  `own_9_015`, `own_9_018` (magic-section entries).
- **Batch C** (`425acd8`, `3b5f8e8`): `own_3_049`, `own_4_001`, `own_10_005` (in progress alongside batch B).
- **Batch D** (`d4114c1`): `own_10_006`, `own_11_018`, `hist_02_040`, `hist_03_001`, `hist_21_006`,
  `hist_28_024`, completing the investigation of `own_4_001`/`own_3_049`/`own_10_005` from batch C and nine
  entries in total.

## What was confirmed fabricated (removed, not repaired)

Consistent with the pattern already documented in the Dougherty/Porter incidents: a plausible-sounding
quotation, correctly styled for its claimed source, that does not occur anywhere in that source.

- `own_4_010`: a Farmer "hostility" claim about the judges.
- `own_4_019`, `own_4_020`: Farmer verdict-tag paraphrases ("false, erroneous, and heretical" / "error to
  error") -- the genuine, independently-verified Dougherty verdict-tags for the same theses were retained.
- `own_9_001`: a claim that medieval magical treatises "regularly began by protesting" their magic was
  natural, attributed to Farmer.
- `own_9_003`: an anecdote that Pico sent Ermolao Barbaro a plague antidote "concocted from the oil of
  scorpions and the tongues of asps," attributed to a "Petrus Crinitus" report in Farmer -- neither
  "Crinitus" nor any of "scorpion(s)"/"asps"/"antidote"/"plague" occurs anywhere in the corpus.
- `own_9_006`: an Italian sentence attributed to Busi & Ebgi that is in fact a back-translation of the
  thesis's own Latin dressed up as a scholar's quotation (the same pattern as the `own_10_004` Busi
  fabrication in the first incident); a genuine footnote making a related point was found and substituted.
- `own_3_049`: "false and can be taken to a heretical sense" and "mode of speaking of Dionysius," both
  attributed to Farmer -- the first is a paraphrase-with-alteration of the thesis's genuine, independently-
  verified Dougherty verdict-tag ("Wrong and can be twisted to a heretical meaning"), which was retained.
- `own_4_001`: a fabricated Dougherty verdict-tag ("Erroneous," already caught and removed in the first
  incident) -- confirmed still absent on this second check.
- `own_10_005`: "most Renaissance manuscripts held eighty-six Orphic hymns... how many Pico recognized is
  anyone's guess," attributed to Farmer.
- `own_10_006`: "Pico's extreme correlative system," attributed to Farmer, describing this thesis and 10>7 --
  Farmer's introduction discusses "correlative systems" at length in general, but never applies the phrase
  to this thesis, which this uploaded copy gives no interpretive note for at all.
- `own_11_018`: "it is possible to generate several plausible readings of the thesis," attributed to Farmer.
- `hist_02_040`: an English translation of Aristotle's bat/sun image (Metaphysics 2), attributed as a
  Farmer's-note translation -- the passage does not occur in farmer1998 at all, but a very close match
  (Aquinas's Latin quoting Aristotle, and Aristotle's own Greek, Metaphysics 993b7-9) was found genuinely
  present in edelheit2022 and substituted, correctly cited.
- `hist_03_001`: Edelheit "observing" that the thesis's opening word `ideo` implies continuation from
  "thesis 45"; and, separately, a Farmer note tying the thesis to the Kabbalistic Ein-Sof, cited to
  farmer1998:12005 -- that line in this uploaded copy is unrelated content (thesis 4>8-4>12, on Christ's
  descent into Hell).
- `hist_21_006`: an Italian sentence attributed to Busi & Ebgi ("Per quanto noto, nessuna fonte attribuisce
  però...") plus a claim that they identify "Abdala" with "Abdallah ibn Salam" and Qur'an 46:10 -- neither
  the sentence nor the identification is in the uploaded text, though the book's index does point to an
  introduction page range (roman numerals xxviii-xxxi) discussing the same figure; the text actually present
  in that range (about the Oration's "Abdalla," not this thesis's dream-saying) was used instead.
- `hist_28_024`: "common symbols of the fourth and fifth sefirot" and a further claim that the fifth
  sefirah "was regularly associated with Satan and the origins of evil," both attributed to Farmer -- only
  the plainer, genuinely-confirmed fact (Farmer's note to the neighbouring thesis 28.6: "north" is a regular
  symbol of the fifth sefirah) survives.

## What was misattributed (genuine quotation, wrong work or wrong line -- re-tagged, not removed)

- `own_4_029`: Latin quotations re-tagged from an unrelated work to edelheit2014.
- `own_4_018`: "tyrannical command" re-tagged to copenhaver2022 (Apology Q8).
- `own_9_004`, `own_9_013`, `own_9_018`: substitute genuine quotations found by direct corpus search in
  place of unverifiable ones.
- `hist_28_024`: "Empedocles becomes relevant as an interpreter of Job," cited to edelheit2008 (which never
  discusses Empedocles or Job at all) -- genuine in edelheit2022, discussing the same Oration passage.

## A further, distinct problem found in batch D: wrong locators on quotations that are otherwise genuine

Several entries also carried real, verbatim quotations tagged with a line number that does not match this
session's uploaded OCR copy (a different extraction from the project's registered ~30,000-line corpus copy
at `E:\pdf\...`, so line numbers are not expected to agree -- see the Dougherty incident's "misattribution
pattern" section for the first instance of this). Batch D corrected several of these on discovery
(`own_3_049`'s cross-references to theses 7a>5/7a>6 and to the Apology's question order; `hist_02_040` and
`hist_03_001`'s other Edelheit citations; `hist_21_006`'s Averroes/Timaeus source locators), documenting
each correction in the entry's `not_established`. This was not exhaustive: several other locators in these
same entries were left uncorrected where the task's scope did not require touching them, with a note added
that a full line-by-line reconciliation against the registered corpus copy is still pending.

## Tooling

No new tooling was added in this sweep; `scripts/verify_against_uploaded_corpus.py` (from the first
incident) and `scripts/entry_gate_local.py` were both re-run after each batch. `data/verification/
uploaded_corpus_verification.json` should always be regenerated by running the verify script with **no**
arguments (`python scripts/verify_against_uploaded_corpus.py`) so it covers the full 900-entry corpus; a
scoped run against a handful of files during batch D briefly truncated this report to 9 entries before
being caught and regenerated in the same commit.

## Residual scope

This pass covered only the entries citing the eleven works this session has uploaded copies of, and within
those, only the quotations the verify script's fuzzy matcher actually flags (a small number of false
positives from its 70%-length partial-match tolerance were caught by direct grep during batch D's
investigation of `own_3_049`, e.g. "mode of speaking of Dionysius" reads as `FOUND_PARTIAL` on pure
character overlap despite not existing in the source). A further run after batch D found 2 new NOT_FOUND
quotations in `own_4_019` (edelheit2008): the two Latin lines from Pico's Apology preamble ("Nisi essent
dicta sanctorum..." and "propter reverentiam sanctorum..."). These were resolved directly: both are
genuine and verbatim, but in `edelheit2014.txt` (same footnote, line 8510 in the uploaded copy), not
`edelheit2008`. Re-tagged; `own_4_019` now passes both the local gate and the corpus verifier. As of
this fix, a corpus-wide re-run of `verify_against_uploaded_corpus.py` reports **0 quotations NOT_FOUND**
across all 900 entries (412/466 checkable quotations confirmed genuine; 54 remain unverifiable only
because the corresponding work was never uploaded this session).

## Standing lesson (reaffirmed a third time)

Same as the first incident: an agent given a specific, plausible-sounding fact to produce, when it cannot
find the exact source, will sometimes invent a stylistically-consistent quotation, page number, or
attribution rather than report the gap -- and will occasionally alter a real quotation's wording just
enough to misattribute it. The only reliable defense is checking every claim against the actually-opened
source text, including quotations the mechanical verifier's fuzzy matching marks as found.
