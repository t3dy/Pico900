# A2 Audit: Heretical essay outline, S1 research notes, methodology documents

Auditor: A2 (read-only). Date of audit: 2026-09-25. Scope: long-form scholarly prose and research notes on the thirteen condemned theses.

## Locator key

Corpus files are in `E:\pdf\renaissance magic\Pico\Markdown\`. Locators are `ALIAS line N` (Markdown line numbers, not printed page numbers, unless a printed page is stated).

| Alias | File |
|---|---|
| CT | `Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__..._753eb1fa.md` (OUP 2022; Introduction, five chapters, Conclusions; treats six of the thirteen Questions in depth, CT 249-250) |
| CM | `Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__..._f7f272e1.md` (Belknap/Harvard 2019, CM 42-47) |
| FA | `Stephen_A_Farmer_..._Syncretism_in_the_West__..._c99b971b.md` (MRTS 167, Tempe 1998; 2nd printing 2003, FA 30-100). Latin + English + commentary on all 900 theses; the notes to the condemned theses are at FA 21458-22121 |
| ED22 | `Amos_Edelheit_Maynooth_University_-_A_Philosopher_at_the_Crossroads_..._dd0f01e6.md` (Brill 2022) |
| HO | `Critical_Political_Theory_..._Sophia_Howlett_-_Re-evaluating_Pico_..._3c6c4fa3.md` (Palgrave/Springer 2021) |
| DO | `M_V_Dougherty_Pico_della_Mirandola__New_Essays_pdf_78172345.md` (CUP 2008) |
| BL | `Studies_in_Medieval_and_Reformation_Traditions_116_..._Black_Crofton_..._c20489cd.md` (Crofton Black, *Pico's Heptaplus and Biblical Hermeneutics*, Brill 2006) |
| WK | `Chaim_Wirszubski_..._li_pdf_cd8c112f.md` |

Repo files (all under `C:\Dev\Pico900\`): OUT = `docs\HERETICAL_ESSAY_DRAFT_OUTLINE.md`; NOTES = `data\conclusions\Heretical\S1_RESEARCH_NOTES.md`; S2R = `docs\S2_HERETICAL_ESSAY_METHODOLOGY_REPORT.md`; PLAN = `docs\HERETICAL_RESEARCH_PLAN.md`; STG = `data\staging\stage_heretical.json`; SG1 = `docs\PICO900_STYLE_GUIDE.md`; SG2 = `docs\STYLE_GUIDE.md`; HAND = `HANDOVER_NEXT_SESSION.md`; DISP = `PHASE_0_DISPATCH_LOG.md`.

Method for quotations: I extracted every quoted span of 45+ characters from OUT and NOTES and searched it, after normalising whitespace, hyphenation, ligatures, curly quotes, punctuation and case, across all 73 Markdown files. I then hand-read the nearest real passage for each miss. Script and word lists are in the session scratchpad only; nothing else was written.

---

## 1. Verdict

1. Neither document is publishable or safe to build on. The outline and notes fail on accuracy, on verifiability of every scholar quotation, and on scholarly depth.
2. **P0: none of the 25 passages the outline puts in quotation marks under Copenhaver's name is verbatim.** Eight are recognisable, altered paraphrases of real passages; seventeen are not in any of the 73 corpus files. Two of the seventeen are the planners' pre-reading hypotheses (PLAN 81-85, 117) re-issued as quotations (OUT 14, 348); several others match prose in PicoDB's own encyclopedia pages, not Copenhaver.
3. Every page number the notes give for the Q1 and Q4 quotations is wrong (they land in the wrong chapter or inside Pico's own translated text). The `[VERIFIED]` tag means "checked against a megabase summary" (STG `source`), not against the book, which is in the corpus.
4. The chronology is wrong. The commission was created in February 1487 and met on 2 March 1487; the bull is dated 4 August 1487. OUT 12 says "March 1486", and all 13 `entry_H.1.*.json` files say "Condemned by papal bull (1486)".
5. Only 2 of the 13 theses (Q1 English, Q5) are stated correctly. Q4, Q6, Q9, Q10 and Q13 are stated incorrectly or replaced with invented wording; Q2 is misidentified ("original sin"); Q3, Q7, Q8, Q11, Q12 have no text although the corpus supplies most of them. The Q4 charge (Nestorianism) does not exist in the record.
6. The essay's central argument, that the commission misread *de possibili* claims as *de sic esse*, is refuted by its own authority: "twelve of the thirteen theses make no appeal to possibility" (CT 8574-8577). Its "coherent program" thesis is contradicted by CT 879-884, and its "vindication" reading by CT 1385-1387.
7. Claims that survive: thirteen theses; Cabrol supplies about half of Q6 (with caveats); the outcome was fixed; Q5's disjunctive defence is "sophistry"; the Pecock context; the Ockham *Dialogus*; the Gloss on Gratian in Q10; the *Fasciculus* episode in Q7.
8. Bibliographic defects: gender errors for Dougherty and Howlett; at least four citations to works that cannot be confirmed to exist; Farmer's title truncated and mis-subtitled in 331 files.
9. Prose: the file is called an outline but is written as argument, then over-uses a single figure ("not X but institutional Y", seven times), speculates in place of research (12 "would/likely address" attributions to scholars not read), and closes every section with a summary.
10. Depth: absent. None of the scholastic apparatus, commission personnel, procedure, verdict formulae, primary Latin, or historiographical dispute is present, though the corpus supplies all of it. Section 5 gives a model section on Q4.

---

## 2. Claim audit

Status: SUPPORTED / CONTRADICTED / UNVERIFIED.

| # | Claim (repo location) | Status | Locator and comment |
|---|---|---|---|
| 1 | Pope convened the commission "in March 1486"; trial "of 1486" (OUT 1, 5, 9, 12, 405; SG2 92, 105; 14 `entry_H.1.*.json` `charge` fields; `scripts/fill_charges_and_defenses.py` 87: "Condemned by papal bull (1486)") | **CONTRADICTED** | *Conclusions* printed December 1486 (CM 16681-16682). Pope indicted them and created the commission in February 1487 (CT 514, 543). First meeting Wednesday 2 March 1487, 12 of 16 present (CT 545-546). Q1 verdict recorded 5 March 1487 (CT 1281); others by the third week of March (CT 544; HO 1104-1107). The 13 were censured by the commission, not by a bull. The **bull** (*Et si ex iniuncto*) condemned the whole book, signed 4 August 1487 (HO 1137-1139; FA 1326-1327), or 8 August (BL 601), published four months later, in December (HO 1139-1143; BL 601-602). No 1486 papal act on the theses is in the corpus. |
| 2 | Thirteen theses were condemned (all files) | SUPPORTED | CT 246-250, 841-851; DO 591-593. Verdicts were graded, not uniform (see the verdict table in section 5). |
| 3 | Identity of the thirteen (topic labels, OUT/NOTES) | SUPPORTED for labels only | CT 846-850: Q1 Hell, Q2 Sin, Q3 Worship, Q4 Incarnation, Q5 Kabbalah, Q6/Q9/Q10 Eucharist, Q7 Origen, Q8 Belief, Q11 Miracle, Q12 God, Q13 Soul. Thesis texts: see rows 4-9. |
| 4 | Q4 thesis "Christ did not take on human nature, but rather assumed a man"; charged as Nestorian; defended by material/formal supposition (OUT 66-80; NOTES 109-132; STG Q4) | **CONTRADICTED** | The thesis is "I do not assent to the usual statement by theologians who say that God can make any nature whatever the supposit, granting this instead only for a nature able to reason" (CT 2140-2142, 6953-6958; Latin CT 6908-6909; Farmer's variant Latin FA 21767-21768, with note FA 21789-21797). Verdict: it "detracts from divine omnipotence and thereby suggests heresy" (CT 6845-6853; FA 21793). "Nestorian" occurs in CT only in a list of ancient heresies (CT 5163) and the index. Q4's *suppositare* is metaphysical, not the semantic supposition of Q9/Q10 (CT 2146-2149). |
| 5 | Q6 thesis "...even if the bread is not converted... **provided that breadness is taken away**" (OUT 105-107; STG Q6) | **CONTRADICTED** | Real thesis (Copenhaver): "without the substance of bread changing (conversio) into Christ's body or without annihilating the breadness (paneitatis annihilatio), it can happen... that Christ's body is on the altar", a statement "about possibility (de possibili), not about being so (de sic esse)" (CT 8612-8618; Latin CT 8651-8654). Farmer: "without the conversion of the bread into the body of Christ, or the annihilation of the breadness... This is said speaking of what is possible, however, not of what is so" (FA 21503-21512). The repo's proviso reverses the sense: breadness is *not* eliminated (*sustentatio paneitatis*, CT 751-753). |
| 6 | Q9 thesis "An accident can exist without a substance, just as a substance can exist without an accident" (OUT 128-130) | **CONTRADICTED** | Real: "Someone who says that an accident cannot exist without existing-in will be able to hold to the sacrament of the eucharist even while holding that the substance of bread does not remain" (CT 9919-9921; CT 1017-1019; FA 21498-21500). It is a divided modal; the repo's version is a different, unqualified claim. |
| 7 | Q10 Latin *"Hoc est enim corpus meum, propositio vera est, sumendo illud materialiter, non significative"* (OUT 149; STG Q10) | **CONTRADICTED** (Latin invented; sense close) | Real: *Illa verba (hoc est corpus, etc.), quae in consecratione dicuntur, materialiter tenentur non significative* (FA 21666-21667; English FA 21723-21725; CT 967-968). Verdict "scandalous and contrary to the usual view" is SUPPORTED (CT 1015-1017). |
| 8 | Q1 Latin *"...secundum existentiam realem descendit ad infernum, sicut communis via docet et Thomas..."* (OUT 37; NOTES 14) | **CONTRADICTED** (Latin invented; English SUPPORTED) | Real Latin: *Christus non ueraciter et quantum ad realem presentiam descendit ad inferos ut ponit Thommas et communis uia, sed solum quo ad effectum* (FA 21657-21658). English as OUT 39 matches CT 1342-1344. |
| 9 | Q2 = "Original sin: nature of the will and human capacity" (OUT 307-314; NOTES 58-79; STG Q2) | **CONTRADICTED** | Q2 "Sin" (CT 847) is Farmer's 4>19-20: a mortal sin is a finite evil, and a finite sin deserves only a finite penalty (FA 21923-21931); verdict "false, erroneous, and heretical", Pico's reply "added error to error" (FA 21937-21943). The agent expanded the label "Sin" into "original sin". |
| 10 | Q3 = "worship of images **or demons**" (OUT 316-323; NOTES 83-102) | **CONTRADICTED** in part | Thesis: "Neither the cross of Christ nor any image should be adored with the adoration of *latria*, even in the way Thomas proposes" (FA 21771-21772, 21818-21819). Nothing on demons. Verdict "scandalous, offensive to pious ears, and against the usage of the universal church" (FA 21838-21839). Pico's defence is in ED22 8183-8230. |
| 11 | Q13 = soul's mystical union with God; commission read it as "a denial of the distinction between the soul and the divine intellect" (OUT 206-217; NOTES 442-461) | **CONTRADICTED** | Q13: "The soul understands nothing actually and distinctly except itself" (CT 5825; FA 21301, Farmer 3>60; note FA 21289). Nothing in the corpus supports the quoted "denial" gloss (not found in any file). |
| 12 | Q11 "continues" the miracles thesis T2M8 (OUT 202-204; NOTES 407) | **CONTRADICTED / UNVERIFIED** | T2M8 (Christ's miracles) is a neighbour of Q5, not Q11. The commission judged it "true and tolerable" (FA 7078-7084), and CM 17652-17654 says the riskier magic theses were "not among the thirteen initially condemned". The text of Q11 itself is UNVERIFIED (CT gives only the label "Miracle", CT 848). |
| 13 | "The commission was staffed with Dominicans and Augustinians... invested in orthodoxy" (OUT 14, in quotation marks as Copenhaver; PLAN 117) | **CONTRADICTED** | CT 545-554: sixteen appointed, twelve at the first meeting; Bishop Jean Monissart of Tournai presiding; five other bishops, including Ardicino della Porta; Pedro Garcia, a Dominican Thomist; three theologians, one lawyer, four court officials; "Dominicans... but also Augustinians, Franciscans, and Servites". HO 1095-1104 adds Marco de Miroldo and Jean Cordier of Paris, who "defended all the conclusions considered". OUT 12 calls them "scholastic professors". |
| 14 | "The trial was rigged" (HAND 39; NOTES 495) | **SUPPORTED** (with qualifications) | "not neutral judges but prosecutors pursuing a guilty verdict" (CT 517-518); "indications that the trial's outcome was fixed" (CT 541); "they ignored what he said and found him guilty as charged" (CT 563-564). Qualifications: Cordier reportedly defended all theses (HO 1100-1101); the commission conceded T2M8 was "true and tolerable" (FA 7081-7084); Farmer calls the judgment "advisory" (FA 1324); the case moved to the Inquisition within a week of the Apology (HO 1124-1125). **OUT 12-13 and OUT 348 assert the opposite** ("not an inquisitorial spectacle"; "not persecution; it was a serious theological examination", the latter in quotation marks). Sentence 3 of OUT 348 comes verbatim from PLAN 83-84 and is contradicted by CT 517-518, 541-564. |
| 15 | Jean Cabrol "ghost author" of half of Q6 (HAND 36, 200; DISP 20; NOTES 218, 491) | **SUPPORTED** as fact; overstated in interpretation and novelty | CT 786-788: "Half of the lengthy Q6 came straight (more or less) from Cabrol's Defenses"; CT 1779-1781: "often verbatim... without acknowledgment"; Q6 never names him (CT 792-793). Caveats: "verbatim" (HAND 200) vs "more or less"; Copenhaver calls it "normal scholastic practice" (CT 1790-1794), so NOTES 491 ("raises questions about Pico's intellectual honesty") is the agent's gloss. **Not Copenhaver's discovery:** Caroti (2005) had shown Capreolus as Pico's direct source (ED22 1029-1034; CT 1802-1803), and Robiglio 2017 is cited at CT 812-813. "1483-4" is the first printed edition, not the date of composition (CT 1804-1806; Cabrol finished 1432, CT 1789). OUT 115 says Pico cited Cabrol for precedent; he did not name him. |
| 16 | "Q8 (doxastic bondage) is the deepest thesis" (HAND 37; OUT 257, 438; NOTES 283) | **CONTRADICTED / UNSUPPORTED** | Copenhaver: "both sides cared more about metaphysics than epistemic ethics. The Q8 thesis... is one of the shorter parts of the Apology" (CT 1420-1423); Pico's Q8 defence is "more expedient than principled... more pliable and pragmatic than theory-driven" and the court "had better grounds to condemn" if his beliefs were freely willed (CT 11477-11483). "Doxastic bondage" is Copenhaver's label for the *Q1* epistemic section (CT 1393-1444, section 1.5), not a Q8 concept ("Pico claimed to be adrift in doxastic bondage", CT 1431-1432). Q8T is qualified: no one believes "exactly because he wants to" (CT 11495-11497); Pico grants that the will is the exact cause once the terms are grasped (CT 10940-10946, 11566-11570). |
| 17 | "11 of 13 cluster around divine embodiment" (HAND 38, 206; DISP 22) | **CONTRADICTED** as stated | Divine embodiment links **five**: Q1, Q4, Q6, Q9, Q10 (CT 888-889). Copenhaver's "all but two" (Q5, Q7) is about "tensions between dogmatic necessity and metaphysical possibility" (CT 911-915), not embodiment. He also calls the set a "theological miscellany" that "was not Pico's invention" (CT 879-884). Blum (in DO) reads the thirteen as an apparently random collection (DO 596-598). Nine of the thirteen come from one section of the *Conclusions* (FA 21461-21464). OUT 388 ("not a miscellaneous collection... but a coherent program") is contradicted. |
| 18 | Central thesis: the commission read *de possibili* claims as *de sic esse* (OUT 5, 71, 93, 113, 353; NOTES 23) | **CONTRADICTED** | The *de possibili* device belongs to Q6 (CT 730-731, 8559-8567). "The case fails on prima facie evidence: twelve of the thirteen theses make no appeal to possibility" (CT 8574-8577). Copenhaver also finds Q6's modal defence "a modal tangle" (CT 8633). |
| 19 | Q1: Pico cited Ockham's *Summa Logicae* on the "coupled extreme" (OUT 48; NOTES 34) | **CONTRADICTED** | "Pico did not refer to Ockham's Logic" (CT 2080-2081); the coupled-extreme doctrine is Ockham's (CT 2023-2030), but Copenhaver says Pico "could have found the relevant notion... elsewhere" (CT 2080-2081). He did cite Ockham's *Dialogus* (CT 2081-2089; SUPPORTED) for the point that false belief is not heresy and that a pope who misuses heresy charges is an arch-heretic. The "repletive" mode (OUT 59; NOTES 30) does not appear in CT (searched). |
| 20 | Q5 defence: disjunctive hypothetical; Copenhaver calls it "sophistry" (OUT 283; NOTES 170) | SUPPORTED | CM 16702-16709: "Pico turned to sophistry... Clever and correct but evasive." **Omitted:** Pico clarified the comparison class as natural philosophy, "not revealed theology" (CM 17650-17657); Q5's defence leaned on scriptural numerology (CT 2290-2292); verdict "false, erroneous, superstitious, and heretical" (FA 7024-7027). OUT 285-289 instead invents a defence from the sefirot and Trinity: NOT FOUND. |
| 21 | "T2M9 (Farmer's critical edition)" (NOTES 196) | **CONTRADICTED** (attribution) | T2M9 is Copenhaver's own numbering (CM 16695). Farmer's is 9>9 (FA 25246); Latin FA 25208-25209. |
| 22 | Commission "had no access to Hebrew sources... no knowledge of Kabbalistic terminology" (OUT 280, 294) | UNVERIFIED (partial) | Real: Q5 was "utterly unintelligible to his judges" (CT 912-914); the Apology "mocked the Roman prelates for understanding nothing at all about Kabbalah, not even the word" (CM 16716-16718). The Hebrew-sources detail is not found. |
| 23 | "Judges trained only in Thomistic simplicity" (OUT 25, 162, 399) | **CONTRADICTED** | Mixed orders (CT 552-554); Cordier from Paris (HO 1097-1099). |
| 24 | Pecock precedent: "politically motivated" attack on Q1 (OUT 51, 364; NOTES 40) | **OVERSTATED** | Pecock facts are sound (formal proceedings 1457, CT 1182; the only pre-Reformation bishop to lose his see as a heretic, CT 1170-1172; descent clause, CT 1186-1192). Copenhaver's inference is hedged: "The facts are lost in time, but the circumstances are telling" (CT 1167-1168); "the Pecock debacle had politicized the underworld" (CT 1237-1238). "Politically motivated" and "a threat that had already cost them a bishop" (OUT 364) are the agents' additions. |
| 25 | Copenhaver "argues that Pico was not heretical but condemned by institutional intolerance"; later scholarship "vindicated" him; supposition theory "anticipated early modern philosophy" (OUT 346-350, 374) | **CONTRADICTED** | "All the antagonists were half-right" (CT 1385-1387); Pico's arrogance (CT 676, 1093); his way of doing philosophy "retrograde" (CT 2128); "the metaphysics of supposition was dying in disgrace and the semantics of supposition had fallen out of the curriculum" (CT 2151-2153); More's mockery of the "little logicals" (CT 1075-1081). Farmer warns that the Apology's evidence "must be approached with greater caution" because Pico "backtracked" (FA 21464-21470, 21794). |
| 26 | Copenhaver's book has "chapters 6-9" that cover Q2, Q3, Q7, Q11-Q13 (S2R 77-79, 149; NOTES 534; OUT 445; HAND 199) | **CONTRADICTED** | Five chapters plus "Conclusions" (CT 100-155). It concentrates on six Questions (CT 249-250). The recommended remedy ("obtain chapters 6-9") is impossible; the gap must be filled from FA (21458-22121), ED22 chs. 5, 14, 15, Crouzel 1977 and Fornaciari 2010. |
| 27 | Q7: Pico mocked a commissioner's use of the *Fasciculus Temporum*, with "scatological puns on witnesses"; "foreshadows Erasmian philology" (OUT 192, 190) | SUPPORTED with corrections | Episode: CT 597-618. The pun is *testis*/*testes* ("balls"), sexual, not scatological (CT 632, 706-707). The Erasmus remark is conditional: "If the whole Apology were like Q7, scholars would now see Pico's book as foreshadowing... Erasmus" (CT 920-923). Q7 thesis and verdict were available: "It is more rational to believe that Origen is saved, than to believe that he is damned" (FA 22099-22100); "rash and savoring of heresy" (FA 22112-22114). |
| 28 | Apologia date; print run | Date SUPPORTED elsewhere; print run UNVERIFIED | Apology dictated in "twenty long nights" (CT 1751-1753), published 31 May 1487 (HO 2068, quoting Borghesi 2012), "late May" (HO 1115). No corpus file gives a print run for either book (searched "print run", "copies" in CT, CM, FA, HO, ED22, BL). OUT and NOTES assert none. SG1 138-146 says the Apology is "unpublished in modern critical edition" (**CONTRADICTED**: Fornaciari 2010, CT 12895-12896, CT 257-258) and that manuscripts and "16th-century printed editions" verify it (**CONTRADICTED**: printed 1487, CT 497-498). |
| 29 | "Q5 is Pico's claim to have been 'the first among the Latins'... Wirszubski & Kristeller" (NOTES 188) | UNVERIFIED (misattributed) | Phrase found only in Farmer ("Pico boasts that he was 'first among the Latins' to mention Cabala", FA 6731-6732), not in WK. "Elia del Medico" is Elia del Medigo (CT 830-832). |
| 30 | Ficino "and later Christian Hebraists would develop" Pico's Kabbalah (OUT 374) | UNVERIFIED | No support found. Ficino and Poliziano "will have known what their friend was up to, more or less, even without making much sense of it" (CM 16685-16688). |

**Where the notes went wrong structurally.** STG's `source` field is "Copenhaver *Pico on Trial* (2025-07-05 megabase summary) + PicoDB condemned_theses.md". The book is in the corpus (847 KB) and was not read. STG records Q8's Latin and Q9's charge as "TO BE VERIFIED", yet NOTES 471 and 479 call Q8 and Q9 "complete". S2R 149-158 reports success.

### Bibliographic audit (details checked against front matter)

| Repo citation | Finding |
|---|---|
| Farmer, *Syncretism in the West: Pico's Platform* (331 JSON/MD files; once "...of Islamic Philosophy") | **Wrong title.** Actual: *Syncretism in the West: Pico's 900 Theses (1486): The Evolution of Traditional Religious and Philosophical Systems, with Text, Translation, and Commentary*, Medieval & Renaissance Texts & Studies 167, Tempe: Arizona, 1998, "Second Printing" 2003 (FA 30-100). Both "(1998)" and "(2003)" appear in the repo; 2003 is a reprint. |
| Deborah L. Black, *Logic and Intellect in Averroes* (234 `entry_S2.*.json` files) | **Cannot be confirmed.** No corpus file contains the phrase. The only "Black" in the corpus is Crofton Black, *Pico's Heptaplus and Biblical Hermeneutics* (Brill, 2006; BL 74, 102). Treat as a probable hallucinated title, and note the author-first-name is also unsupported. |
| Michael J. B. Allen, *Neoplatonism and the Platonic Tradition* (192 `entry_S1.*.json` files) | **Cannot be confirmed.** The corpus Allen is *Studies in the Platonism of Marsilio Ficino and Giovanni Pico* (Routledge, 2017, AL 89-98). |
| Howlett, *Pico's Three Paths to the Absolute* (SG2 196) and *Life and Works* (2019) (SG1 146) | **Cannot be confirmed / wrong.** Actual: Sophia Howlett, *Re-evaluating Pico: Aristotelianism, Kabbalism, and Platonism in the Philosophy of Giovanni Pico della Mirandola*, Palgrave Macmillan (Springer Nature), 2021 (HO 96-99). "Life and Works" is chapter 2 of that book (running head "2 LIFE AND WORKS", HO 774, 864, 954, 1044, 1132). |
| Dougherty, "she" (PLAN 88, 90, 109; S2R 87); "Dougherty anthology essays on eucharistic theology, free will, mysticism, logic" (NOTES 232, 300, 344, 388, 456) | **Wrong.** M. V. Dougherty is male ("His research in the history of philosophy...", DO 48), and is the editor, not the author. The book has no chapter on those topics: contents are Kraye, Blum, Sudduth, Allen, Dougherty, Rabin, Still, Borghesi (DO 100-120). Only Blum, "Pico, Theology, and the Church" (DO 591-611), treats the thirteen theses. |
| Howlett, "he" (PLAN 94-95, 148) | **Wrong.** Sophia Howlett. |
| Edelheit, *A Philosopher at the Crossroads* | Exists: Brill, Brill's Studies in Intellectual History 338, 2022 (ED22 50, 88-107). *Ficino, Pico and Savonarola* (Brill, 2008) also exists. NOTES 542 ("likely contains detailed analysis of the scholastic sources") is a guess; the scholastic material is in the 2022 book (chs. 5-11, 14-15, ED22 contents 132-190). |
| "Fornaciari critical edition of the *Apology* (Florence, 2010)" (NOTES 536) | SUPPORTED: Fornaciari, *Apologia: L'Autodifesa di Pico di fronte al tribunale dell'Inquisizione*, Florence: Galluzzo, 2010 (CT 12895-12896). The corpus holds only its index pages (pp. 375ff), so the Latin of Q2, Q3, Q7, Q11, Q12 is not obtainable from it here. |
| Copenhaver 2022 and 2019 | SUPPORTED (OUP 2022, CT 48; Belknap 2019, CM 42-47). |
| Wirszubski and Kristeller (1989) | SUPPORTED: Harvard UP 1989 (WK 46-52); Wirszubski d. 1977, Kristeller "brought this volume to completion" (WK 131). |

---

## 3. Quotation audit

Definitions: VERBATIM = found in the cited scholar's file after normalisation; ALTERED = a real passage says something similar but the quoted wording is not there; NOT FOUND = no passage in any corpus file says it, or the closest passage says something different. **Every NOT FOUND scholar-attributed quotation below is a P0 defect: it is text presented as Copenhaver's that Copenhaver did not write.**

### 3a. Passages put in Copenhaver's mouth in OUT (25 passages)

| OUT line | Quoted opening words | Status | Nearest real passage / provenance |
|---|---|---|---|
| 14 | "staffed with Dominicans and Augustinians... invested in orthodoxy" | NOT FOUND | Planners' phrase, PLAN 117 (plan, not book). Real: CT 552-554. |
| 23 | "Pico's defense was scholastic, technical, mostly orthodox (even if novel)" | NOT FOUND | PLAN 85 ("Copenhaver emphasizes: ..."), a pre-reading expectation. Contradicted by CT 1385-1387. |
| 42 | "The commission condemned this thesis as suggesting heresy about the incarnation... violate the Apostles' Creed" | NOT FOUND | Real verdict: CT 1276-1279. |
| 51 | "The Q1 thesis concerns the metaphysical problem of how Christ... politically motivated by Reginald Pecock's heresy trial" | ALTERED | CT 285-286 ("How could Christ, without a body, be in a place") and CT 1237-1238; "politically motivated" not in source. |
| 53 | "Pico was defending orthodoxy through metaphysical precision, not denying any article of the Creed... judges trained only in Thomistic simplicity" | NOT FOUND | CT 1271-1272 gives only "no one should understand me to say..." |
| 83 | "Q4 is the most metaphysically ambitious of the condemned propositions..." | NOT FOUND | First sentence matches PicoDB `apology.md`, an LLM-written encyclopedia page, not Copenhaver. |
| 85 | "The condemned thesis reveals Pico's dependence on late medieval metaphysical innovation... Scotist rather than Thomist categories" | NOT FOUND | CT 5556-5605: Q4's authority is Henry of Ghent, not Scotus. |
| 121 | "Q6 is the most technically demanding of the eucharistic theses..." | NOT FOUND | Closest real: Q6 is a "modal tangle" (CT 8633). |
| 123 | "Pico's exploration of the logical possibility space... institutional intolerance" | NOT FOUND | Contradicted by CT 8574-8577. |
| 144 | "Q9 is the middle of three eucharistic theses..." | NOT FOUND | Neither the sentence nor its "middle" framing is in CT. |
| 162 | "Q10 represents Pico's most audacious application of supposition theory..." | NOT FOUND | CT 977-986 describes the hoc/material supposition without such wording. |
| 164 | "The commission's reaction reveals the deep tension between scholastic logic and sacramental theology..." | NOT FOUND | No counterpart. |
| 187 | "Q7 takes the form of philological polemic rather than metaphysical argumentation" | ALTERED | CT 918-923: Q7's "format is more like a polemic by Eusebius than a summa by Aquinas, and the content of Q7 is philological." |
| 192 | "mocking one commissioner's reliance on the Fasciculus Temporum... scatological puns on witnesses" | ALTERED | Description in quote marks; real: CT 597-618, 632. |
| 195 | "Q7 is anomalous among the thirteen Questions..." | ALTERED | CT 911-924. Wording is not Copenhaver's. |
| 211 | "a denial of the distinction between the soul and the divine intellect" (Q13) | NOT FOUND | Contradicted by Q13's actual text (CT 5825). |
| 252 | "Q8 addresses a fundamental question in medieval moral and epistemological theology... Pico radicalized this by denying that will could control belief" | NOT FOUND | Contradicted by Q8T (CT 11495-11497, 10940-10946). |
| 254 | "Copenhaver further notes: 'Copenhaver notes that Q8 received little attention... anticipates modern epistemology'" | ALTERED | The quote contains the words "Copenhaver notes", so it cannot be his sentence. "Little attention" is real (CT 1421-1423); "anticipates modern epistemology" is not found anywhere. |
| 292 | "Q5 stands apart from the other condemned theses both in form and in philosophical register..." | NOT FOUND | Verbatim in PicoDB `condemned_theses.md`; not in CT or CM. |
| 294 | "The commission's response was driven by incomprehension as much as orthodoxy: the commissioners had no access to Hebrew sources..." | ALTERED | CT 912-914; CM 16716-16718. Hebrew-sources clause not found. |
| 297 | "From Pico's perspective, Q5 is not a threat to Christian theology but a supplement to it..." | ALTERED | The T2M6-T2M9 passage paraphrases CM 17640-17660; the framing sentence is not in the source. |
| 348 | "Pico was not a proto-modern humanist but a scholastic metaphysician. He walked into dangerous theological territory deliberately. The trial was not persecution; it was a serious theological examination..." | NOT FOUND | Lifted from PLAN 81-85, where it is the planners' summary before reading. Sentence 3 is contradicted by CT 517-518, 541-564. |
| 350 | "Far from undermining orthodoxy, Pico attempted to defend Christian doctrine through enhanced philosophical precision..." | NOT FOUND | No counterpart. |
| 364 | "politically motivated by Reginald Pecock's heresy trial (1457)..." | ALTERED | CT 1237-1238; see claim 24. |
| 399 | "Pico's greatest challenge was the logical apparatus... judges trained only in Thomistic simplicity" | NOT FOUND | No counterpart; contradicted by CT 552-554. |

Totals for the outline: 0 VERBATIM, 8 ALTERED (lines 51, 187, 192, 195, 254, 294, 297, 364), 17 NOT FOUND.

### 3b. What is genuinely verbatim

| Text | Where in repo | Source |
|---|---|---|
| "no one should understand me to say that Christ's soul did not descend into Hell" | OUT 46; NOTES 21 | CT 1271-1272 (Pico via Copenhaver) |
| Q1 thesis, English | OUT 39 | CT 1342-1344 |
| "False, erroneous, heretical and contrary to the truth of sacred scripture, notwithstanding any explanation..." | NOTES 52 | CT 1276-1279 (drops the qualifiers *secundum rigorem sermonis* and *ex vi verborum*) |
| T2M9 (English), T2M8 | OUT 202, 275; NOTES 163, 407 | CM 16695; CM 17628-17629 |
| Q5 Latin | OUT 273; NOTES 196 | FA 25208-25209 |
| "your little packet can go straight to Hell since no one trusts it" | NOTES 272 | CT 600-602 (page cite p. 8-10 is correct) |

### 3c. S1 notes

NOTES repeats about 26 distinct "Copenhaver" passages, several two or three times (for example Q4 at 136, 146; Q5 at 182, 192; Q6 at 228, 238; Q10 at 382, 392; Q8 at 296, 306; Q9 at 340, 350). The same classification applies: none verbatim; the rest NOT FOUND or ALTERED as in 3a. Two further features:

- **Page numbers fail.** "p. 44" and "p. 28" for Q1 land on the end of the list of Pico's medieval authorities (printed pp. 43-44, CT 2324-2379) and on Pico's attack on his judges' competence (printed p. 28, CT 1558-1606); "p. 142" for Q4 is inside Pico's own translated Q4 (printed pp. 135-144, CT 6949 onward); "p. 97" is in chapter 2 (§2.10), though NOTES 138 places it in chapter 3 (which begins p. 99); "p. 70-96" for Q6 is chapter 2 (Chapter 4 begins p. 145); "Ch. 5, p. 24-25" for Q8 is chapter 1 §1.5. Only pp. 8-10, 11-12, 13, 15, 16-18 are in the right region.
- **Quotations inside quotations.** NOTES 384 and 394 put "However, Copenhaver shows that Pico was..." in quotation marks under Copenhaver's name. NOTES 74-76, 99, 232, 266, 300, 344, 388, 433-435, 456 assign views to Dougherty, Howlett, Edelheit, Black and Copenhaver in the conditional ("would address", "likely addresses"). None is a quotation, but each sits in the position of a citation.

### 3d. Style-guide "model voice" quotations

| Quotation | Location | Status |
|---|---|---|
| Copenhaver, "Pico's engagement with Averroism was not incidental but constitutive..." | SG1 22 | NOT FOUND |
| Copenhaver, "Pico's reading of Plotinus was not incidental but structural..." | SG1 265 | NOT FOUND |
| Howlett, "Pico's Aristotelianism is not a departure from his Platonism but rather a deliberate synthesis..." | SG1 270 | NOT FOUND |
| Edelheit, "The essence-existence distinction that Pico inherits from Avicenna through Aquinas..." | SG1 275 | NOT FOUND |
| Howlett p. 18, "Pico accepts the Aristotelian hylomorphism..." [CITED] | SG2 196 | NOT FOUND; the cited title does not exist |
| Edelheit p. 156, "The doctrine of the soul as substantial form was scholastically orthodox..." [CITED] | SG2 199 | NOT FOUND |

These are pastiches. The guide labels them "Live Examples" of the authors' voices, so any contributor who lifts one as a quotation commits the same P0 defect. Label them "invented exemplars" or delete them.

---

## 4. Prose audit

Counts are regex matches followed by manual pruning (approximate, but each is a lower bound of what a reader would notice). OUT is 5,837 words in 454 lines, with 56 headings and 46 bullets; NOTES is 7,691 words in 565 lines, with 73 headings and 148 bullets.

| Trope | OUT | NOTES | Three worst verbatim examples (file line) |
|---|---|---|---|
| "not X but Y" / "rather than" | about 20 sentences (25 lines match the pattern; 5 are false positives) | about 19 | (i) "The commission's error was not theological but hermeneutical" (OUT 93), repeated as "The commission's fundamental error was not theological but hermeneutical" (OUT 353); (ii) "The commission's condemnation was not a theological refutation but an institutional refusal" (OUT 399), with variants at 173, 381, 402; (iii) "The 13 condemned theses are not a miscellaneous collection of heresies but a coherent metaphysical and theological program" (OUT 388), a false claim in the trope's form (see claim 17). The same antithesis appears at least seven times (OUT 93, 123, 173, 353, 381, 399, 402). |
| "It is important to note" and its cousins | 2 ("Critically," 280; "It is ironic-and instructive-" 402) | 2 | "It is ironic-and instructive-that the only 13 theses Pico chose to defend in his *Apology* were those condemned" (OUT 402). Also false: the Pope's condemnation forced the defence (CT 879-884). "Copenhaver further notes/observes/emphasizes" introduces five quotations (OUT 53, 85, 164, 254, 294). |
| Hedging in place of research | 8 lines | 27 lines | (i) "It likely connects to the immediately preceding proposition... Q11 likely continues this discussion" (OUT 202-204); (ii) "Q13 concerns the soul, likely in the context of its mystical union with God" (OUT 211); (iii) "This thesis likely represents Pico's engagement with late medieval metaphysics on divine simplicity" (OUT 330). Outline-appropriate as TODO placeholders; not appropriate as text that then feeds an argument (see 'Thematic Integration' at OUT 334-336). |
| Phantom scholars | 2 | 12 | (i) "Dougherty (essays on eucharistic theology): Would address Q9 alongside Q6 and Q10..." (NOTES 344; no such essay exists in DO 100-120); (ii) "Howlett and Edelheit: Likely address Q2 in broader context of human nature and divine grace" (NOTES 76); (iii) "Later scholarship has vindicated much of Pico's approach" (OUT 374), with no name, and "the modern scholarly consensus" (NOTES 479-480). |
| List-as-analysis and bullet fragments | 6 "Thematic Integration/Significance" blocks (OUT 87, 166, 219, 259, 299, 334) plus 3-5-item bullet lists standing in for argument at OUT 88-91, 168-171, 221-224, 358-361, 367-372, 390-393 | 148 bullets; each Question has a numbered "Defense" list of 3-5 moves | (i) OUT 367-372, "Vindication and Legacy" as five numbered claims with no evidence; (ii) OUT 358-361, three bullets naming "philosophical innovation", "textual authority", "institutional boundaries"; (iii) NOTES 19-34, five moves in a list where the relation between the moves is the argument. |
| Announce-then-deliver | 4 | 2 | (i) "This essay examines the 13 theses... The essay integrates scholarship from..." (OUT 5); (ii) "This essay outline organizes Pico's 13 condemned conclusions..." (OUT 453); (iii) the rhetorical question that opens §2 and §3 (OUT 32, 100). |
| Summary-paragraph closers | "Together, they..." at OUT 93, 173, 226, and a fourth in the Q5 block (297); a closing "Summary" (OUT 451-453) that restates the introduction; "Conclusion" (OUT 385-407) that restates §2-§8 | "Conclusion" (NOTES 552-564) | "Together, they demonstrate Pico's commitment to defending orthodoxy through metaphysical sophistication" (OUT 93). Also OUT 405-407, the last two paragraphs, which restate OUT 396-403. |
| Vague intensifiers | about 31 | about 31 | (i) "Q8 is the most philosophically profound of the condemned theses" (OUT 257); (ii) "Pico's most audacious application of supposition theory" (OUT 162); (iii) "a monument to Pico's ambition" (OUT 407). Add "profound", "sophisticated", "deeply", "fundamental", "systematic". |
| Placeholder as prose | 7 "to be verified" markers left in text | 6 "TO BE VERIFIED" plus 18 "INCOMPLETE" | "**The Thesis**: [To be verified from fuller sources]" (OUT 199, 309, 318, 327) directly above "Thematic Context" paragraphs that assert what the thesis concerns. |

**Outline versus argument.** The file is titled an outline yet contains complete argumentative paragraphs and block quotations. Its terseness is appropriate only for the headings and the "Charge / Defense / Copenhaver's Account" skeleton. The text within each cell, for example OUT 74-80 (Q4 defence) or 283-289 (Q5 defence), is written as finished prose and needs to be argued, not listed, in a real essay. The template fault is in SG2: its instruction "State the theses / The charge / Copenhaver's reading / Pico's defense / Scholarly debate / Conclusion" for each cluster (SG2 138-144) produces exactly this repetitive structure.

### Style-guide conflicts (SG1 vs SG2)

SG1 (`PICO900_STYLE_GUIDE.md`, "Authoritative", last updated 2026-09-25 18:00) and SG2 (`STYLE_GUIDE.md`, saved 16:45) are both live and neither supersedes the other.

1. **Citation form.** SG2: "**Scholar** (*Work*, p. X): 'quotation'" plus `[VERIFIED]`/`[CITED]`/`[INFERRED]` tags (SG2 61-88). SG1: author-date (Copenhaver 2019, 156-158), Chicago 17th, BibTeX (SG1 186-201).
2. **Quotation versus assertion.** SG2: "Citation > Summary", "Avoid paraphrases", "Every scholarly claim has a quotation backing it" (SG2 11, 77, 155). SG1: "Direct assertion backed by implicit scholarly weight" (SG1 25), which is exactly what produced the invented quotations.
3. **Uncertainty.** SG2 requires marking uncertainty and confidence levels. SG1 bans hedging ("Just argue it", SG1 32-34).
4. **Structure.** SG2 mandates per-cluster templates and entry headings; SG1 forbids "Listmaking disguised as analysis", restricts subheadings to sections of 200+ words, and forbids summary paragraphs (SG1 47, 235-243). The outline follows SG2 and so violates SG1.
5. **Q-clusters disagree.** SG2 lists Incarnation (Q1, Q2, Q3), Soul/Intellect (Q4, Q7, Q11), Other (Q8, Q12, Q13) (SG2 132-135). OUT uses (Q1, Q4), (Q6, Q9, Q10), (Q7, Q11, Q13), Q8, Q5, (Q2, Q3, Q12). PLAN 20-41 uses a third grouping. None matches the sources: Q2 is mortal sin, Q3 is images, Q4 is God's power to assume natures, Q7 is Origen, Q11 is miracles.
6. **Both contain factual errors.** SG2 92, 105 date the condemnation to 1486; SG1 138-146's model timeline entry says the Apology is unpublished in critical edition (false), verified by "16th-century" manuscripts (false), and that Copenhaver and Howlett read the Apology as Pico's "most mature philosophical work, not a defensive tract". Copenhaver describes it as rushed under pressure, its theories "not his own" (CT 392-394, 1751-1753, 2352-2354).
7. **SG1 breaches its own rule.** Its three model exemplars (SG1 22, 265, 270) use "not X but Y" ("not incidental but constitutive", "not incidental but structural", "not a departure... but rather a deliberate synthesis").

Recommendation: one guide. Keep SG1's voice rules, SG2's provenance discipline ([VERIFIED] means "matched to the book, line/page recorded"), and delete SG2's cluster template.

---

## 5. Depth audit and exemplar

### 5a. What a PhD reader would expect that is missing

All items below have sources in the corpus.

1. **A correct textual base for each thesis.** Latin and English for all 13 from FA (4>8 Q1, 4>19-20 Q2, 4>14 Q3, 4>13 Q4, 9>9 Q5, 4>2 Q6, 4>29 Q7, 4>18 Q8, 4>1 Q9, 4>10 Q10, 3>49 Q12, 3>60 Q13; FA 21657-22100, 25208) and from CT's printed translations (Q4 CT 6953 onward; Q9/Q10 CT 9916 onward; Q8 CT 11491 onward). Also the transmission history: two theological theses cut from the press (FA 21458-21460), Pico's punctuation switches exploited in defence (FA 10115-10118, 21657-21700), and the corrupted printed text of the Apology (CT 5613-5693).
2. **The verdict formulae and the procedure.** The graded verdicts below; the two-stage process (cardinals' commission, then the magisterial commission of February; seven censured in early March, six more in later March, HO 1093-1107; BL 590-593); the mission statement *ex vi verborum* and Pico's counter-appeal to *de virtute sermonis* (CT 559-560, 1286-1291; Courtenay 1984 cited CT 1304); the move to the Inquisition, the abjuration in late July, the bull and its four-month delay, Pico's arrest, Vincennes, Lorenzo de' Medici's intercession, and absolution by Alexander VI on 18 June 1493 (HO 1124-1180).

   | Q | Verdict recorded (Farmer/Copenhaver) | Locator |
   |---|---|---|
   | 1 | "false, erroneous, heretical, and against the truth of Sacred Scriptures" (unanimous) | CT 1276-1279; FA 21696-21698 |
   | 2 | "false, erroneous, and heretical"; Pico's reply "added error to error" | FA 21940-21943 |
   | 3 | "scandalous, offensive to pious ears, and against the usage of the universal church" | FA 21838-21839 |
   | 4 | "detracts from divine omnipotence and thereby suggests heresy" | CT 6851-6853; FA 21793 |
   | 5 | "false, erroneous, superstitious, and heretical" | FA 7024-7027 |
   | 6 | "erroneous" | CT 8641-8642 |
   | 7 | "rash and savoring of heresy, since it is opposed to the determination of the universal church" | FA 22112-22114 |
   | 8 | "erroneous and savoring of heresy" | FA 21895-21897; CT 11515-11516 |
   | 9 | "erroneous" (no reasons given) | CT 1017-1019, 9922-9925 |
   | 10 | "scandalous and contrary to the usual view" | CT 1015-1017 |
   | 11 | not located in corpus | (none) |
   | 12 | "false and can be taken to a heretical sense" | FA 21055-21059 |
   | 13 | among the thirteen; verdict not located | FA 21289 |

3. **The scholastic apparatus as argument, not name-dropping.** Two senses of "supposit": metaphysical (Q4, Q6) versus semantic (Q9, Q10), which the repo conflates (CT 2146-2149; ch. 2 §§2.6-2.9). *Suppositio materialis* and the *hoc* puzzle (CT 969-993; ch. 4.4-4.5). Ampliation and divided modals in Q9 (CT 1066-1081, 9957-9960). The α/β/γ-theories of the Eucharist: annihilation, change, remaining, with Quidort as the source of the remaining-theory (CT 8574-8686; ch. 4.2-4.3). Henry of Ghent's metaphysics of X/E/S being and the intellectual-nature restriction (CT ch. 3.3-3.5). Assent versus assertion (CT 5696-5757). All are in CT chs. 2-4.
4. **Q1 in its actual field: the location of separated substances.** Lombard's *Sentences* I.37 on circumscriptive/definitive presence (CT 1918-1926); Tempier 1277 and Godfrey of Fontaines (CT 1795-1850); Scotus's "an angel is often nowhere" (CT 1933-1935); Aquinas ST 3.52.2 (CT 1350); Guido Terrena's *Summa* as the source of Q1's paragraphs (CT 1144-1146); Pecock and the descent clause (CT 1113-1238).
5. **Q2, Q3, Q7 doctrinal backgrounds.** Mortal sin as finite evil and the proportion of punishment (FA 21873-21943, citing Aquinas *Sent.* 4 d. 46); *latria*, *dulia*, *hyperdulia* and the veneration of images (FA 21798-21806; ED22 8183-8230, Capreolus's defence of Thomas); Origen, posthumous condemnation, canon law and Crouzel 1977 (FA 22110-22121; CT 612-613, 944).
6. **Q8 within the medieval ethics of belief.** Holcot, d'Ailly, Henry of Oyta, Henry of Hesse, Aquinas on faith and assent (CT ch. 5, esp. 10940-11488); Farmer's contrast of intellectualism and voluntarism, and his note that Q8 "erroneous and savoring of heresy" was judged precisely because it made dogma pass intellectual tests (FA 5972-5978, 6134-6138, 21889-21900); Pico's Q1 "doxastic bondage" passage as the actual locus of the concept (CT 1393-1444).
7. **Q5 and concord.** T2M6-T2M9 as a set and the disjunctive-hypothetical defence (CM 16695-16709, 17619-17660); Q5's "true and tolerable" neighbour (FA 7078-7084); Flavius Mithridates and Kabbalah sources (CM 16689-16690; WK); the Apology's scriptural numerology (CT 2290-2292); Pico's boast to be "first among the Latins" (FA 6731-6732).
8. **The people.** Monissart, della Porta, Garcia (whose 1489 *Determinationes magistrales* rebuts the Apology, CT 12629-12631; ED22 ch. 14, contents line 181), Cordier, de Miroldo, Caroli (ED22 ch. 15); the layman-versus-theologian objection (a "twenty-three-year-old layman", FA 21462-21464). None is named in OUT.
9. **Pico's method and honesty, evidence-first.** Excerpting without naming (CT 1790-1794, 8547-8549), Caroti 2005, Robiglio 2017; Farmer's warning against trusting the Apology (FA 21464-21470); the haste (CT 5765-5766, 1751-1753).
10. **Historiography with names.** The Burckhardt-Gentile-Cassirer-Garin "progressive Pico" (FA 660-666); Copenhaver's programme (CT 224-244, 2233-2236; CM); **Edelheit's dissent: Pico was not a "scholastic philosopher", "at least as this term has been commonly understood. He most definitely was not"** (ED22 217-222), against Copenhaver's footnote 16, which disagrees with Edelheit on whether the Apology questions the basis of scholastic theology (CT 944-953); Howlett's critical turn (HO 165-170); Blum on the commission policing the boundary between natural philosophy and theology (DO 591-611); Farmer on "much sterile discussion" over orthodoxy (FA 1322-1330). The outline's premise that Copenhaver's Pico-as-scholastic is the field's view (OUT 348) is contested in the corpus itself.

Also missing: any footnote, bibliography or edition sigla, any primary Latin from the Apology, and any engagement with Garcia's reply.

### 5b. Exemplar section: Q4

The fourth condemned thesis is the best documented in the corpus: Copenhaver gives the Latin, the verdict and a full chapter (CT ch. 3, printed pp. 99-144); Farmer gives the Latin variant and the record of Pico's oral reply; Edelheit gives Pico's own Latin from the Apology. It is also the thesis the repo gets most wrong.

> **Q4: Withholding assent from the donkey**
>
> The fourth condemned thesis reads, in the Latin Copenhaver prints: *Non assentior communi sententiae theologorum dicentium posse Deum quamlibet naturam suppositare, sed de rationabili tantum hoc concedo*, "I do not assent to the usual statement by theologians who say that God can make any nature whatever the supposit, granting this instead only for a nature able to reason."[1] The stake is how far divine assumption extends. Christ's human nature is the paradigm of a nature made a supposit by the Word; the usual view added that omnipotence extends the possibility to any creature at all. Aquinas's *Sentences* commentary says "God can take on any creature he chooses", and Jean Cabrol argued early in the fifteenth century that a stone could be taken on.[2] Pico's minority view came from Henry of Ghent, who had reversed an earlier position, in the Quodlibet 13.5 that supplies most of Pico's Question: a nature is assumed in order to be improved, and only an intellectual nature can be raised to the vision of God.[3]
>
> The commission ruled that "by the import of its language" the thesis "detracts from divine omnipotence and thereby suggests heresy", a lighter formula than the "heretical" pronounced on Q1. Farmer's translation of the same record reads "derogates from divine omnipotence, and this savors of heresy."[4] The verdict recorded in the transcript speaks only of omnipotence.
>
> Pico's defence has three layers. The first is grammatical: he wrote *non assentior*, not *non credo*, and refusing assent to a proposition does not assert its contradiction, so his judges had confused the two.[5] The second is *illi quoque*: Henry held the position, seven named masters repeated Henry's account, and none called it heresy, so condemning Pico would make Henry a heretic.[6] Edelheit adds that Henry's stance was the more extreme, since Henry denied a possibility that Pico only declined to affirm.[7] The third is pastoral: the usual view licenses sentences such as "God is a donkey", which Pico argued would scandalize the uneducated more than his refusal.[8] School logic did entertain such sentences; the *Centiloquium*, widely attributed to Ockham, says "God can take on a stone, a stick of wood and so on."[9]
>
> Q4 is the only condemned thesis phrased as a refusal of assent, so the device that protected it could not do much for the other twelve.[10] Farmer, reading the notarial record, judges that Pico "prudently backtracked" in the Apology and warns that its evidence must be read with caution.[11] The Apology's text of Henry is itself corrupt, with more than two dozen errors in a few pages, and the whole work was dictated in about twenty nights.[12]

**Footnotes** (file + Markdown line; every quotation was checked verbatim):

1. Thesis English: CT 6953-6958 (also CT 2140-2142); Latin: CT 6908-6909. "The Q4 thesis is identical in both versions" (Conclusions and Apology): CT 5888-5889. Farmer prints a variant, *de rationali tamen* (FA 21767-21768); Copenhaver notes his own emendations (CT 5731-5734).
2. "God can take on any creature he chooses": CT 6750-6751 (Aquinas, *Sent.*); Aquinas's answers varied: CT 5443-5445. Cabrol: CT 5449-5458 (asked whether God could take on a stone; answer yes).
3. Henry's reversal: CT 6879-6883, 5772-5775; Quodlibet 13.5 fills most of Q4 (about 1,900 of 3,500 words): CT 5606-5607, 5815-5816. Improvement and the intellectual-nature restriction: CT 6483-6489, 6684-6685.
4. Verdict: CT 6845-6853 ("Having considered... the aforesaid conclusion detracts from divine omnipotence and thereby suggests heresy"). Q1 verdict "heretical": CT 1276-1279. Farmer: FA 21793.
5. *Non assentior* versus *non credo*: CT 6935-6939; "refusing to accept a proposition doesn't entail its contradiction": CT 5757; *de virtute sermonis*: CT 6894-6899.
6. Seven masters: CT 6504-6505, 6560-6562 (Bernard de Gannat, Durand, Godfrey, Scotus, and probably Ware, Orford, Sutton); Pico's own Latin list and "Henry a heretic" inference: ED22 7783-7790; Copenhaver on the tactic: CT 5804-5809, 6884-6886.
7. "Henry holds here a more radical and extreme position than Pico": ED22 7747-7753.
8. "more scandalous for the uneducated and more hurtful to pious ears": CT 6736; "God is a donkey", "God is a stick": CT 6743-6744.
9. *Centiloquium*: CT 2133-2134, 2179-2181. Copenhaver notes it is uncertain whether Pico read it (CT 2187-2188).
10. "no other condemned thesis makes a first-person, non assentior statement": CT 5819-5820; the distinction "could not help him much with the rest of the Apology": CT 5850-5852.
11. "prudently backtracked": FA 21794; "must be approached with greater caution": FA 21469-21470 (with FA 21464-21468).
12. Corrupt text, "more than two dozen within a few pages": CT 5677-5679. "The work of twenty long nights" (Pico's own words, quoted by Copenhaver): CT 1751-1753; also "within three weeks", CT 5766.

The section is 420 words. It asserts nothing about the *de possibili* device, Nestorianism, or Scotist categories, because none applies to Q4.

---

## 6. What I could not verify, and why

- **Q11's thesis and verdict.** CT lists the label "Miracle" (CT 848) and no thesis text. FA's notes flag three of the remaining theses as among the thirteen (Q5, Q12, Q13) and give verdicts for most, but I did not locate Q11 in Farmer (searched "thirteen", "commission", "miracle", 4>x and 9>x notes). I could not test the repo's assumption that Q11 is a "miracles" claim.
- **Q13's verdict.** FA 21289 names the thesis among the thirteen but gives no verdict; the trial minutes (Dorez and Thuasne 1897) are cited in CT/FA but are not in the corpus.
- **Q10's Latin in the *Apology* (as opposed to the *Conclusions*).** I used FA's Latin from the *Conclusions*; CT prints only English for Q9 and Q10 (in translation) and notes that Apology wording "differs slightly but not importantly" for Q6 (CT 8585-8586). Q10's Apology wording may differ in detail.
- **PicoDB quotations.** NOTES cite PicoDB pages (`apology.md`, `condemned_theses.md`, `ch05_is_heresy_willful.md`). I traced only whether phrases from OUT/NOTES appear in PicoDB: "Q4 is the most metaphysically ambitious" is in `apology.md`; "Q5 stands apart... both in form and in philosophical register" is in `condemned_theses.md`; "little attention in the trial record" is in the PicoDB chapter-1 summary; "politically motivated by Reginald", "doxastic constraints that anticipates", "institutional intolerance", "seeming dissolution", "judges trained only in Thomistic", "no access to Hebrew" occur in no PicoDB file I searched. Those PicoDB pages are LLM-authored summaries and are not primary evidence. I did not audit PicoDB itself.
- **"Repletive" presence.** The three modes of spatial presence (circumscriptive, definitive, repletive) are standard scholastic doctrine, but "repletive" appears in no corpus file. I mark the claim UNVERIFIED (in corpus), not false.
- **Fourth Lateran (1215)** in NOTES 244 is historically correct and CT discusses it (CT 7745-7770, index 152-4); I did not verify the specific PicoDB citation.
- **Bull date.** HO and FA say 4 August 1487; BL says 8 August. I cannot resolve the discrepancy from the corpus; Garin (cited by Farmer, FA 727) reprints the bull, but Garin's book is not in the corpus.
- **Whether Cordier "defended all the conclusions".** HO 1100-1101 says so; CT 561-562 and FA 21694 say every recorded vote was unanimous. Both may be true (a defence in debate, then a unanimous vote), but the corpus does not decide.
- **Printed page numbers.** Locators are Markdown lines. Where I state printed pages for CT (99-144, 135-144, 145) they come from the running heads and contents (CT 100-155 and page markers), not from the print edition.
- **Wirszubski's account of Pico's Kabbalah sources.** I did not search WK beyond checking that the "first among the Latins" phrase is absent.
- **Farmer's reliability on the trial record.** His notes cite Dorez and Thuasne (1897) for commission page numbers and quote verdicts in English translation; I could not check them against the minutes.

No file other than this one was created or modified.
