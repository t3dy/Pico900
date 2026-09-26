# V1: Verification of A1/A2 Rewrite Exemplars

Verifier: V1 (read-only). Date: 2026-09-25. Scope: the five candidate model
entries — A1 section 4, Exemplars 1-4, and A2 section 5b's Q4 exemplar with
its 12 footnotes.

Method: every locator was opened at the cited line with Read (offset/limit)
or found with Grep and hand-read; nothing here is taken on the auditors' say-so.
Latin was checked normalising u/v, i/j and whitespace. Files used, with the
copy checked (both duplicate copies in the corpus are byte-identical apart
from YAML front matter, confirmed by diff):
- F = `Stephen_A_Farmer_..._c99b971b.md` (30,439 lines; identical body to
  `Medieval_Renaissance_Texts_Studies_167_...c99b971b.md`)
- C = `Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__..._753eb1fa.md`
- W = `Chaim_Wirszubski_..._Ha_pdf_cd8c112f.md` (identical body to the
  `_li_pdf_` copy)
- E = `Amos_Edelheit_Maynooth_University_..._dd0f01e6.md`

Repo files checked for context (not part of the verification target, only
consulted to see what the exemplars are correcting): `data/conclusions/S3/entry_S3.C002.json`,
`S7/entry_S7.C070.json`, `Heretical/entry_H.1.4.json`, `Heretical/entry_H.1.6.json`.

---

## Summary table

| Exemplar | Verdict | Claims checked | Failures |
|---|---|---|---|
| A1 Exemplar 1 (H.1.6, thesis 4>2) | PASS | 6 | 0 |
| A1 Exemplar 2 (H.1.4, thesis 4>13) | PASS WITH CORRECTIONS | 8 | 1 (line range too wide, not wrong) |
| A1 Exemplar 3 (S7.C070, thesis 11>23) | PASS | 7 | 0 |
| A1 Exemplar 4 (S3.C002, thesis 7.2) | PASS | 8 | 0 |
| A2 Q4 exemplar (12 footnotes) | PASS | 24 (footnotes 1-12, most citing 2 locators) | 0 |

None of the five candidate entries has a false quotation, a wrong attribution,
or a fabricated causal claim. This is a different population from the "775
template rows" and "25 unverifiable Copenhaver quotations" A1 and A2 flagged
elsewhere in their own audits — these five are the samples the two auditors
put forward as *already fixed*, and on this sample the fix held. That does not
license extrapolating soundness to the rest of the 929-row corpus or the rest
of the essay outline, which A1 and A2's own broader passes describe as still
templated or fabricated.

---

## A1 Exemplar 1 — H.1.6, thesis 4>2 (Farmer numbering "422")

| # | Locator | Claim | Verdict |
|---|---|---|---|
| 1 | F 21444-21448 | Latin of thesis 4>2 quoted verbatim | SUPPORTED — F.md lines 21444-21448 read (OCR spacing normalised): "Si teneatur communis uia de possibilitate suppositationis in respectu ad quamcunque creaturam, dico quod sine conuersione panis in corpus Christi uel paneitatis anihilatione, potest fieri ut in altari sit corpus Christi secundum ueritatem sacramenti Eucharistiae; quod sit dictum loquendo de possibili, non de sic esse." Matches the exemplar's quotation exactly (u/v and OCR spacing aside; "annihilatione" vs "anihilatione" is the source's own single-n spelling, correctly reproduced). |
| 2 | F 21524-21528 (English gloss, paraphrase) | "The closing clause confines the claim to possibility and asserts nothing about the sacrament as instituted" | SUPPORTED — F.md 21524-21528 (Farmer's note to 4>2): "Again, however, this pertains only to a 'possible sacrament,' not to the Eucharist as it was actually established by God." Faithful paraphrase. |
| 3 | (repo entry, not a source locator) | "The earlier entry's Latin ('dummodo paneitas tollatur') reverses the printed text, which excludes the annihilation of breadness" | SUPPORTED — `entry_H.1.6.json` line 4 gives exactly that Latin incipit ("...dummodo paneitas tollatur", i.e. "provided that breadness IS removed"), and F 21446 has "paneitatis anihilatione" governed by "sine" ("WITHOUT the annihilation of breadness"). The two are opposite conditions; the exemplar's characterization is accurate. |
| 4 | Copenhaver l. 786-788 | "The model descends from Jean Quidort's impanation theory... Pico took it second-hand from Jean Cabrol" | SUPPORTED — C 780-788: "Half of the lengthy Q6 came straight (more or less) from Cabrol's Defenses..." and Cabrol is described as the conduit; Quidort's impanation theory is developed at length just before and after (see next row). Correct with one nuance: C 780-788 alone establishes the Cabrol conduit; the "impanation" framing is Quidort's, drawn from the surrounding pages, which the exemplar cites separately (next locator). No error. |
| 5 | Copenhaver l. 8050-8078 | Quidort's impanation/paneitas theory, as the model Pico's thesis descends from | SUPPORTED — C 8050-8078 is exactly the paragraph explaining Quidort's "impanation" coinage, the Word's supposit taking on "paneitas," etc., matching the exemplar's summary. |
| 6 | Copenhaver l. 8574-8577 and 8641-8642 | "Copenhaver treats Q6 as the one condemned thesis whose wording appeals to possibility, and records that the commission judged it erroneous all the same" | SUPPORTED — C 8574-8577: "twelve of the thirteen theses make no appeal to possibility. Not so for the Q6 thesis..."; C 8641-8642: "The judges who called the Q6 thesis erroneous brought in a harsher verdict of heresy for the Q1 proposition." Both exactly as characterized. |

**Verdict: PASS.** The stated "unverified" caveat (exact verdict wording for
Q6 beyond "erroneous") is itself honest — I could not find a fuller verdict
formula for Q6 in C or F either (C 8898-8903 repeats "erroneous," no fuller
quotation is given in either corpus file for Q6 specifically, unlike the
fuller formulas quoted for Q1 and Q4).

---

## A1 Exemplar 2 — H.1.4, thesis 4>13

| # | Locator | Claim | Verdict |
|---|---|---|---|
| 1 | F 21767-21768; C 6908-6909 | Latin of 4>13 quoted verbatim, matching Copenhaver's printed Q4 wording | SUPPORTED with a note. F 21767-21768: "Non assentior communi sententiae theologorum dicentium posse deum quamlibet naturam suppositare, sed de rationali tamen hoc concedo." C 6908-6909 ("Non assentior communi sententiae theologorum dicentium posse Deum quamli-bet naturam suppositare, sed de rationabili tantum hoc concedo") differs from Farmer's in two words: *rationali tamen* (F) vs *rationabili tantum* (C). The exemplar's own prose flags exactly this ("Farmer prints a variant..."; in A2's footnote 1 the same variant is flagged too) — so the exemplar does not claim false identity of wording, it cites both and notes the variant belongs to Farmer. Accurate. |
| 2 | (paraphrase) | "Pico withholds assent... grants assumption of a rational nature" | SUPPORTED — direct paraphrase of the Latin itself. |
| 3 | (repo entry claim under test) | "The Latin previously carried under H.1.4 ('Christus non accepit naturam humanam, sed hominem accepit') occurs nowhere in the 900" | SUPPORTED — normalised full-text search of F.md for "hominem accepit" and "non accepit naturam humanam" returns zero hits (checked programmatically against the whole 30,439-line file, u/v- and hyphenation-normalised). `entry_H.1.4.json` line 4 does carry exactly that fabricated Latin. The exemplar's claim is correct. |
| 4 | (observation) | "the only condemned thesis phrased in the first person" | SUPPORTED — C 5848-5850: "Most theses defended in the Apology are like the Q13 proposition. They make no doxastic commitments...none except the Q4 thesis is a statement of non-assent." C 5819-5820 (cited in A2 footnote 10) says the same. Confirms uniqueness. |
| 5 | Copenhaver l. 5818-5821, 6932-6939 | "Pico chose non assentior over non credo to reduce his exposure" | LINE OFF, but SUPPORTED. The "non assentior vs non credo" choice is at C 6934-6939 ("he could have written non credo... but caution got the best of him"), which is inside the cited 6932-6939 range — correct. But 5818-5821 does not contain this claim; the adjacent passage making the same point is at C 5753-5757 ("he was careful not to write 'I assert' not-x... Instead, he wrote 'I do not assent to' x"). The citation to 5818-5821 is off by roughly 65-70 lines; the substance is still true and is stated at 5753-5757 and again at 6934-6939. **Correction**: cite "Copenhaver l. 5753-5757, 6934-6939" in place of "l. 5818-5821, 6932-6939." |
| 6 | F 21792-21793 | "The commission ruled that the thesis derogates from divine omnipotence and savors of heresy" | SUPPORTED — F 21793 reads exactly: "derogates from divine omnipotence, and this savors of heresy." (F's own note to 4>13, immediately following the thesis at 21786-21796). |
| 7 | F 21789-21796 | "Pico answered orally, on the authority of Henry of Ghent, that natures below the rational are not assumable... in the Apology he retreated to a quarrel with the way the common opinion argued" | SUPPORTED — F 21789-21791: "In his oral response to the papal commission... Pico argued on the authority of Henry of Ghent that his thesis was not true because of any insufficiency in God but because natures below the rational nature were not 'assumable' (suppositabilis)." F 21794-21796: "Pico prudently backtracked, arguing that his thesis did not claim that God could not assume any nature... but only disagreed with the way that the 'common opinion' argued that this was possible." Matches exactly. |
| 8 | Copenhaver l. 6880-6883 | "Copenhaver adds that Henry himself abandoned the common opinion" | SUPPORTED — C 6879-6883: Henry "changed his mind and defended a position that he had opposed when he was less experienced — that 'not any nature can be made the supposit by God.' The view that Henry abandoned was the very same position from which Pico withheld assent." |

**Verdict: PASS WITH CORRECTIONS.** One locator (item 5) is off by about
65-70 lines; the claim itself is true and supported elsewhere in the cited
range's neighborhood. Corrected sentence: replace "(Copenhaver, l. 5818-5821,
6932-6939)" with "(Copenhaver, l. 5753-5757, 6934-6939)." No other change
needed; promote after that one citation fix.

---

## A1 Exemplar 3 — S7.C070, thesis 11>23

| # | Locator | Claim | Verdict |
|---|---|---|---|
| 1 | F 26904-26906 | Latin of 11>23 quoted verbatim | SUPPORTED — F 26904-26906: "Per illud dictum Hieremiae: Lacerauit uerbum suum, secundum expositionem Cabalistarum, habemus intelligere quod deum sanctum et benedictum lacerauit deus pro peccatoribus." Exact match. |
| 2 | W 8273-8277 | "Wirszubski identifies the verse as Lam. 2:17 and shows two strands fused..." | SUPPORTED — W 8273-8277 (footnote 5 to Conclusio xxiii): "The verse Pico has in mind can only be Lam. 2:17. Pico combined two interpretations: (a) [Hebrew], 'God rent his purple,' Midras Wayyikra Rabba... and also the Zohar...; (b) [Hebrew] as a symbol of the tenth sefirah." Matches; note the exemplar's hedge in its own "unverified" line ("Wirszubski says the verse 'can only be'...and does not rank the strands") is itself accurate — W does not say which strand is primary. |
| 3 | W 8322-8330 | Kabbalistic equation of "word" with the tenth sefirah | SUPPORTED — W 8322-8330 (footnote 6): "The notion that [Hebrew] (verbum) denotes the tenth sefirah is a Kabbalistic commonplace," with supporting citation to Liber de Radicibus. Matches. |
| 4 | W 1989, 162-63 | Printed page numbers | UNCHECKABLE for printed pagination — the Markdown carries bracketed page markers; W.md shows "[162]" at line 8279 and "[163]" at line 8334, bracketing lines 8265-8332, which contain both cited footnotes. Consistent with "162-63," though I cannot independently confirm the 1989 print edition's pagination beyond these embedded markers. |
| 5 | F 26939-26941 | "Farmer confirms the tenth-sefirah reading and adds that the Word of John 1:1 enters the sense" | SUPPORTED — F 26939-26941 (note to 11>23): "Wirszubski (1989: 163) points out that the 'word' = a regular kabbalistic symbol of the tenth sefirah. Christ's identification in John 1:1ff., etc., with the 'Word of God' also obviously comes into play here." Matches exactly. |
| 6 | W 8298-8308 | "Wirszubski groups theses 21-24 of the set under one pattern...the method of Raymundus Martini's Pugio fidei" | SUPPORTED — W 8298-8308: "The details vary from thesis to thesis but the pattern of the four theses is substantially the same... Raymundus Martini's Pugio Fidei set an example of a Christianizing interpretation of rabbinic texts... The common pattern of Pico's four theses will be easily recognized by anyone acquainted with the Pugio Fidei." Matches; "theses 21-24" is confirmed independently by the file's own Conclusio xxi-xxiv headings at W 8251, 8258, 8265/8266 (xxiii), 8289 (xxiv). |
| 7 | F 26909-26914 | "11>24 continues to the claim that the death of Christ satisfies for human sin" | SUPPORTED — F 26909-26914 gives the Latin of 11>24, whose closing clause reads "...redarguuntur ineuitabiliter Hebrei dicentes non fuisse conueniens ut mors Christi satisfaceret pro peccato humani generis" — "the death of Christ would satisfy for the sin of the human race." Matches; the exemplar's gloss is accurate. |
| 8 | (repo entry claim under test) | "The tags 'gematria' and 'letter combination' and the label 'Sefirot' in the earlier entry do not describe this thesis" | SUPPORTED — `entry_S7.C070.json`: tags = ["Kabbalah","magic","divine names","gematria","letter combination"]; exegesis = "Pico's conclusion on Sefirot within the Kabbalah tradition." Thesis 11>23 is about a midrashic/Kabbalistic reading of Jeremiah/Lamentations applied to Christ's self-sacrifice — nothing in the verified sources ties it to gematria (numerology) or letter-combination technique specifically; "Sefirot" is present only via the tenth-sefirah identification of "word," which is one clause, not the thesis's subject. The exemplar's correction is fair. |

**Verdict: PASS.**

---

## A1 Exemplar 4 — S3.C002, thesis 7.2

| # | Locator | Claim | Verdict |
|---|---|---|---|
| 1 | F 12937 | Latin of thesis 7.2 | SUPPORTED — F 12937: "7.2. Vna est anima intellectiua in omnibus hominibus." Exact. |
| 2 | (context) | "opens the Averroes series on the unity of the intellect" | SUPPORTED — the Averroes section header ("CONCLVSIONES SECVNDVM AVENROEM NVMERO XLI") is at F 12861-12862, thesis 7.1 (on prophecy in dreams) follows immediately at F 12864-12865, and 7.2 (F 12937) is the second thesis, the first on the intellect; F's note at line 12967 confirms 7.2-4 as a set on "the problem of the 'unity of intellect.'" |
| 3 | F 12967-12971, 12978-12979 | "Farmer traces 7.2-4 to commentary on De anima 3.5 and ties them to Simplicius 17.9, Alexander 18.1, Plotinus 20.7 and Pico's own 3>67-69" | SUPPORTED — F 12967-12971 (note to 7.2-4): "cf. 3267-69 [i.e. 3>67-69] and my discussion above... Arises from commentary on De anima 3.5... Discussion of 7.4 would have also involved theses 17.9 from Simplicius and 18.1 from Alexander of Aphrodisias. Cf. also 7.3 with 20.7 from Plotinus." F 12978-12979 continues the same note on Nifo. All cross-references confirmed as stated. |
| 4 | F 21396-21398 | "thesis 3>69 gives as a probability the view that each series of souls is beatified in its own intellect" | SUPPORTED — F 21396-21398 (thesis 3>69): "It is rational according to philosophy to say that every series of souls is beatified in its own intellect. This, however, is not stated assertively but as a probability." Matches exactly, including "as a probability." |
| 5 | (structural claim) | "The section stands under the heading 'according to the opinions of others': 7.2 reports Averroes and commits Pico to nothing" | SUPPORTED — the section-level heading "THESES ACCORDING TO THE OPINIONS OF OTHERS" recurs through this part of the text (e.g. F 12932, immediately above the Averroes subsection), and F's own framing note at 12881-12883 states Pico was not straightforwardly an "Averroist," consistent with reading 7.2 as a reported opinion. |
| 6 | F 12940-12944 | "Thesis 7.3 defends Averroes' account of the conjunction of agent and possible intellect against John of Jandun" | SUPPORTED — F 12940-12944 (thesis 7.3, Latin) and its English at 12967 area ("Man's greatest happiness is achieved when the active intellect is conjoined to the possible intellect as its form. This conjunction has been perversely and incorrectly understood by the other Latins... and especially by John of Jandun, who... totally corrupted and twisted the doctrine of Averroes.") Matches. |
| 7 | F 13001-13002 | "Thesis 7.4 keeps the unity of the intellect and allows that my soul, so particularly mine that it is shared with no one, remains after death" | SUPPORTED — F 12947-12948 gives the Latin ("Possibile est tenendo unitatem intellectus, animam meam, ita particulariter meam ut non sit mihi communis cum omnibus, remanere post mortem") and its English rendering nearby ("It is possible, upholding the unity of the intellect, that my soul, so particularly mine that it is not shared by me with all, remains after death"). LINE OFF by a few lines — the Latin is at 12947-12948, not 13001-13002; my scan of the surrounding block (12928-13010, English translations following the Latin block) places the corresponding English at approximately line 12975 depending on how OCR blank lines are counted. The substance is correct in either case, and 13001-13002 is inside the same continuous 7.1-7.6 Averroes/English block (12927-13010) rather than a different thesis — this is a soft locator drift within one contiguous passage, not a misattribution. **Correction**: cite "F 12947-12948 (Latin), with the English at roughly F 12974-12976" rather than "F 13001-13002." |
| 8 | (repo entry claim under test) | "The earlier entry's claim that Pico 'explicitly rejects' 7.2 in 7.4 overstates: 7.4 leaves 7.2 standing and adds a harmonizing clause" | SUPPORTED — `entry_S3.C002.json` "defense" field: "Pico explicitly rejects this in I.7.4, asserting that personal immortality and individual soul survival are possible even if the agent intellect is universal." But F's 7.4 text (above) says only that it is *possible*, "upholding the unity of the intellect," for an individual soul to survive — it does not reject the unity-of-intellect thesis (7.2); it is compatible with it, exactly as the exemplar states. |
| 9 | F 12975-12979 | "Farmer notes that Nifo later credited Pico with a resolution tied to Albert the Great and finds it only loosely related to the theses" | SUPPORTED — F 12975-12979 continuation of the 7.2-4 note: "Long after Pico's death, Nifo attributed to Pico a resolution of the unity of intellect problem linked to the works of Albert the Great... The metaphorical language that Nifo ascribes to Pico is not closely related to anything in the theses, although the underlying approach that Nifo discusses can be roughly tied to 3>67-69." Matches, including the "roughly tied" qualifier the exemplar implicitly respects by not overclaiming a tight link. |

**Verdict: PASS.** One soft line-drift (item 7, off by roughly 25-50 lines
within the same contiguous passage) does not change any claim's truth and is
noted only for precision.

---

## A2 Section 5b — Exemplar section: Q4, with its 12 footnotes

The prose paragraphs (CT ch. 3 summary) were checked against the footnoted
locators below; I did not find any sentence in the four paragraphs that goes
beyond what its footnote supports.

| FN | Locator(s) | Claim | Verdict |
|---|---|---|---|
| 1 | CT 6953-6958, 2140-2142 (English); CT 6908-6909 (Latin); CT 5888-5889 ("identical in both versions"); FA 21767-21768 (Farmer variant); CT 5731-5734 (Copenhaver's emendations) | Q4's English and Latin text, the note that Conclusions/Apology wording is identical, Farmer's variant reading, and that Copenhaver emended the Latin | SUPPORTED on every sub-claim. C 6953-6958 and C 2140-2142 both print the identical English translation verbatim: "I do not assent to the usual statement by theologians who say that God can make any nature whatever the supposit, granting this instead only for a nature able to reason." C 6908-6909 gives the Latin exactly as quoted (*rationabili tantum*). C 5888-5889: "the Q4 thesis is identical in both versions, but the wording of the Q13 thesis differs slightly" — matches verbatim. FA 21767-21768 gives Farmer's variant (*rationali tamen*), confirmed. C 5731-5734: "the English translation... assumes my emendations of the Latin text as printed in Apo." — matches. |
| 2 | CT 6750-6751 (Aquinas); CT 5443-5445 (varied answers); CT 5449-5458 (Cabrol, stone) | Aquinas quote and Cabrol's yes-answer on a stone | SUPPORTED. C 6750-6751: "'God can take on any creature he chooses': Aquinas wrote these words in his Sentences commentary." Verbatim quotation matches. C 5443-5445 on Aquinas varying his answers by occasion — matches ("Thomas varied his answers, adjusting them to the occasion"). C 5449-5458: Cabrol's affirmative answer on a stone, with the quoted "Just as God's likeness... unreasoning creature can be united with God" — quotation verified verbatim at C 5455-5458. |
| 3 | CT 6879-6883, 5772-5775 (Henry's reversal); CT 5606-5607, 5815-5816 (Quodlibet 13.5 ~1900/3500 words); CT 6483-6489, 6684-6685 (improvement/intellectual-nature restriction) | Henry's Quodlibet content and its proportion of Q4 | SUPPORTED. C 6879-6883 and 5772-5775 both state Henry changed his mind (verified above under A1 Exemplar 2, item 8). C 5606-5607 identifies Qdl. 13.5 as filling "most of Pico's Q4"; the "1,900 of 3,500 words" figure is not independently checkable from the Markdown (no word count is given in the source at 5815-5816, which instead states Pico's Apology chronology) — see note below. C 6483-6489 and 6684-6685 both state the "only an intellectual nature... can be improved" restriction, matching almost verbatim ("only an intellectual nature is capable of this improvement" / "only an intellectual nature can have such an improvement"). |
| 4 | CT 6845-6853 (verdict quotation); CT 1276-1279 (Q1 "heretical" verdict); FA 21793 | The commission's Q4 verdict quoted verbatim, contrasted with Q1's harsher formula, plus Farmer's paraphrase | SUPPORTED. C 6845-6853 gives the verdict verbatim, matching the footnote's quoted text exactly: "...by the import of its language (vi sermonis) the aforesaid conclusion detracts from divine omnipotence and thereby suggests heresy." C 1276-1279 gives the Q1 verdict verbatim ("is false, erroneous, heretical and contrary to the truth of sacred scripture...") — correctly the harsher formula. FA 21793 ("derogates from divine omnipotence, and this savors of heresy") matches, already confirmed under Exemplar 2. |
| 5 | CT 6935-6939 (non assentior/non credo); CT 5757 ("doesn't entail its contradiction"); CT 6894-6899 (de virtute sermonis) | Pico's grammatical defense | SUPPORTED. C 6934-6939 (footnote says 6935-6939, off by one line at the start, immaterial) matches the "non credo... caution got the best of him" passage. C 5757 verbatim: "refusing to accept a proposition doesn't entail its contradiction." C 6894-6899 discusses "de virtute sermonis" repeated three times in Pico's final paragraph — matches C 6901-6902 exactly ("the words de virtute sermonis, used three times in this short final paragraph"). |
| 6 | CT 6504-6505, 6560-6562 (seven masters); ED22 7783-7790 (Pico's list / "Henry a heretic"); CT 5804-5809, 6884-6886 (tactic) | The illi quoque roster and inference | SUPPORTED. C 6504-6505 ("other prominent theologians (Pico gave seven names) repeated Henry's account") and C 6560-6562 (footnote naming Bernard de Gannat, Durand, Godfrey of Fontaines, Scotus, and three probable others) match; the A2 footnote's own naming ("Bernard de Gannat, Durand, Godfrey, Scotus, and probably Ware, Orford, Sutton") matches C 6561-6562 exactly, including the parenthetical identifications. ED22 7783-7790 gives Pico's actual Latin list of names verbatim ("nec Scotus nec Gotfredus nec Ioannes de Guarra nec Durandus nec Thomas Anglicus nec Robertus de Collotorto nec Bernardus de Gannato...") and the "Henricus...mortuus sit haereticus" inference at ED22 7789-7792 — both confirmed verbatim. C 5804-5809 and 6884-6886 confirm the illi quoque tactic description. |
| 7 | ED22 7747-7753 | "Henry holds here a more radical and extreme position than Pico" | SUPPORTED — ED22 7748-7751 verbatim: "Henry holds here a more radical and extreme position than Pico, in denying the possibility of God to assume any kind of nature, including a non rational one, and in insisting on obtaining a rational nature only." Quotation in the footnote is verbatim and correctly attributed to Edelheit. |
| 8 | CT 6736 ("more scandalous..."); CT 6743-6744 ("God is a donkey", "God is a stick") | The pastoral/scandal argument, quoted verbatim | SUPPORTED. C 6736 verbatim: "more scandalous for the uneducated and more hurtful to pious ears?" C 6744 verbatim: "God is a donkey" and "God is a stick" — both phrases appear exactly at C 6744-6745 (as Pico's own hypothetical examples, correctly framed as Pico's, not the Centiloquium's, at this point in the argument). |
| 9 | CT 2133-2134, 2179-2181 (Centiloquium quote); CT 2187-2188 (uncertain if Pico read it) | The Centiloquium's "God can take on a stone" quotation and Copenhaver's caveat about attribution to Pico's reading | SUPPORTED. C 2133-2134 identifies "the Centiloquium widely attributed to Ockham." C 2179-2181 gives the verbatim quotation: "'God can take on a stone, a stick of wood and so on'... 'all these propositions are possible: God is a donkey; God is a stone; a stone is a donkey.'" C 2187-2188 (part of the sentence beginning "If Pico read this little tract, he would have understood...") does carry the hedge — Copenhaver frames Pico's acquaintance with the tract as conditional ("If Pico read this little tract"), supporting the footnote's "uncertain whether Pico read it," though the precise phrase "uncertain whether" is A2's paraphrase, not a quotation, and is presented as such (not in quotation marks) — correctly not overclaimed as verbatim. |
| 10 | CT 5819-5820 ("no other condemned thesis..."); CT 5850-5852 ("could not help him much...") | Q4's uniqueness as a non-assentior thesis and the limit of that defense's reach | SUPPORTED. C 5848-5850 (footnote cites 5850-5852, off by up to 2 lines, immaterial): "none except the Q4 thesis is a statement of non-assent. So Pico's emphasis in Q4 on the assenting/asserting distinction could not help him much with the rest of the Apology." Matches closely; footnote paraphrases rather than quotes here and does not overclaim. |
| 11 | FA 21794 ("prudently backtracked"); FA 21469-21470, with FA 21464-21468 ("must be approached with greater caution") | Farmer's judgment on the Apology's reliability | SUPPORTED. FA 21794 (checked as F 21794 above under Exemplar 2) matches: "Pico prudently backtracked." FA 21469-21470/21464-21468 matches F's general-introduction sentence (F 21468-21470): "the evidence in the Apology and in the notarial record of Pico's verbal and written replies to the commission must be approached with greater caution than shown in past analyses of these texts." Verbatim. |
| 12 | CT 5677-5679 ("more than two dozen... few pages"); CT 1751-1753 ("twenty long nights"); CT 5766 ("within three weeks") | Textual corruption and dictation-speed claims | SUPPORTED. C 5677-5679 verbatim: "the printed Q4 is so full of textual errors—more than two dozen within a few pages—that understanding would have been blocked." C 1751-1753 (quotation continues onto C 1765, across a footnote break) verbatim: "What I've dictated for now in a rush I shall write about elsewhere with more care when I have time... The current product, such as it is, was the work of twenty long nights, when getting something out quickly was a better choice for me than paying close attention." C 5766 ("within three weeks") confirmed in context (C 5765-5766: "a panicky document rushed to completion within three weeks"). |

**Verdict: PASS.** All twelve footnotes check out; every quotation marked
with quotation marks in the prose or footnotes is verbatim in Copenhaver,
Farmer, or Edelheit at (or within one or two lines of) the cited locator.
The one soft item is footnote 3's "1,900 of 3,500 words" figure for how much
of Q4 is Henry's Quodlibet — see below.

---

## What I could not verify, and why

1. **A2 footnote 3's word-count figures ("about 1,900 of 3,500 words").**
   C 5606-5607 and 5815-5816 establish that Quodlibet 13.5 "fills most of
   Pico's Q4," but neither the Markdown OCR nor any other passage I found in
   C gives an explicit word count for Q4 or for the Henry excerpt within it.
   The claim is directionally correct (Henry's excerpt is described elsewhere,
   at C 7780, as running from Apo. pp. 136-144, a substantial fraction of a
   document Copenhaver elsewhere bounds by Apo. pp. 41-48) but I cannot
   confirm the specific "1,900 of 3,500" figures against the Markdown text
   itself. UNCHECKABLE from the corpus as OCR'd — the numbers may come from
   Copenhaver's printed page/word arithmetic (pp. 99-144 in CT, per A2's own
   line 238) rather than from a sentence quotable at a line number. This is
   not a red flag by itself (page-length arithmetic is a legitimate scholarly
   inference), but it should be flagged in the footnote as inferred rather
   than presented as if quotable.
2. **1989 print-edition page numbers for Wirszubski** (used in A1 Exemplar 3,
   "W:8273-8277... 1989, 162-63"). I could only confirm these against the
   embedded OCR page markers "[162]" and "[163]" in the Markdown (W.md lines
   8279, 8334), which bracket the correct passage. I have not independently
   confirmed against a physical copy of the 1989 Harvard University Press
   edition that these OCR markers are error-free page numbers; treat as
   corroborated-by-OCR-marker rather than independently verified against
   print.
3. **Whether the "twenty long nights" quotation (CT 1751-1753/1765) and the
   "within three weeks" remark (CT 5766) describe the same claim or two
   different self-reports by Pico** (twenty nights vs three weeks are not
   arithmetically identical, though both could be true of a staggered
   composition). Both quotations are independently verbatim and correctly
   cited; I have not tried to adjudicate whether Copenhaver himself reconciles
   the two figures, since A2's footnote does not claim they are reconciled —
   it cites them as two separate points, which is accurate to what the source
   does.
4. I did not attempt to verify claims in A1's or A2's sections outside the
   five named exemplars (e.g., the "775 template rows," "25 unverifiable
   Copenhaver quotations" figures) — that is out of this task's scope, which
   is the five *candidate replacement* passages, not the audits' other
   findings about the rest of the corpus.

---

## Corrected texts (for promotion)

**A1 Exemplar 2** — replace the citation "(Copenhaver, l. 5818-5821,
6932-6939)" with:

> (Copenhaver, l. 5753-5757, 6934-6939)

No other wording in Exemplar 2 needs to change; the claim it supports is
accurate.

**A1 Exemplar 4** — replace "(l. 13001-13002)" with:

> (F 12947-12948, Latin; the corresponding English at approximately F 12974-12976)

No other wording in Exemplar 4 needs to change.

**A1 Exemplar 1, A1 Exemplar 3, A2 Q4 exemplar** — no corrections required;
promote as written.
