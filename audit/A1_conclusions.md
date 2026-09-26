# A1 Audit: the 929 conclusion entries

Auditor: read-only qualitative and factual pass. Date of audit: 2026-09-25.
Files inspected: `data/conclusions/{S1..S9,Heretical}`, `data/schema.json`, `docs/STYLE_GUIDE.md`, `docs/PICO900_STYLE_GUIDE.md`, `data/conclusions/Heretical/S1_RESEARCH_NOTES.md`.

Locator convention. Line numbers refer to the Markdown conversions in `E:\pdf\renaissance magic\Pico\Markdown\`.
`F:` = Farmer, *Syncretism in the West* (`Stephen_A_Farmer_...c99b971b.md`).
`C:` = Copenhaver, *Pico della Mirandola on Trial* (`Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial...753eb1fa.md`).
`W:` = Wirszubski, *Pico's Encounter with Jewish Mysticism* (`Chaim_Wirszubski...cd8c112f.md`, the file ending `_Ha_pdf_`).
`A:` = Fornaciari, *Apologia* (`Giovanni_Pico_della_Mirandola_Apologia...7cec82e9.md`; only front matter and contents survive, 1103 lines).
`CM:` = Copenhaver, *Magic and the Dignity of Man* (`...f7f272e1.md`).
Farmer's English translation and Copenhaver's English are paraphrased below, never quoted at length. Latin theses of 1486 are quoted freely.

---

## Verdict (10 lines)

1. **Real content is about 143 of 900 theses (16%).** S7 (118, the two Cabalistic sections), S3 (11 of Averroes' 41) and S4 (all 12 of Avicenna's) carry text from Farmer's edition; two Heretical entries (H.1.1, H.1.5) are substantively right.
2. **775 of the 929 rows are template filler**: a canned English sentence, "[TO BE SOURCED...]" for Latin, and one charge/defense pair shared by a whole section (S1 95, S2 110, S3 109, S4 93, S5 80, S6 95, S8 8, S9 185). The sentences I searched for ("Being is predicated primarily of substance", "The Church is the mystical body of Christ", "Evil arises from matter's resistance to form") occur nowhere in Farmer's text.
3. **The S1-S9 scheme matches the work only in patches.** S3, S4, S7 and S8 name real sections (S8 even has the right count, 4+4), S1 corresponds loosely to the Platonists; S2 ("Aristotle"), S5 (80), S6 (95) and S9 ("Theologians", 185) have no counterpart. The own-opinion half of the work (498 theses) has no home except the Cabalistic section 11> (S7) and, nominally, the Zoroaster section 8> (S5, filler) (Section 1).
4. **929 is indefensible.** Farmer prints 402 historical + 498 own-opinion = 900 (F:10761-10762). The repo is 900 + 29: 13 Heretical duplicates plus scaffold overshoot, and one real thesis (11>66) is missing.
5. **The Latin that exists is faithful but truncated**: 108 of 118 S7 `latin_full` fields stop at the first OCR line-break ("irratio-", "peti-", "expo-"). 44 S7 entries repeat the Latin in the English field; 23 read "[TO_TRANSLATE]" although Farmer prints English for every one; 23 have English text in the Latin field. Only 32 of 118 have a distinct English rendering, and those copy Farmer's published translation.
6. **The 13 condemned theses are mostly wrong or empty**: 2 correct, 1 inverted (H.1.6), 2 invented or reversed (H.1.4, H.1.9), 1 with invented Latin and a distorted English (H.1.10), 7 unfilled. Each is dated "Condemned by papal bull (1486)"; the commission judged in March 1487 and the bull is of 4 August 1487 (Section 3).
7. **"283 verified citations" in S7 are 3 distinct strings** repeated 118, 118 and 47 times. One is misattributed (it is from the editors' Introduction, not Wirszubski), one appears in no file of the corpus, one is a paraphrase of Copenhaver dressed as a quotation. Further fabricated quotations: S4.C001 (Farmer, "Pico's Platform"), S1_RESEARCH_NOTES.md (Copenhaver pp. 28, 44), and the "zigging and zagging" model quote in PICO900_STYLE_GUIDE.
8. **charge/defense/exegesis are boilerplate almost everywhere**: 1 charge string per section for S2, S5, S6, S8, S9; 4-5 exegesis stubs ("Pico's conclusion on Sefirot within the Kabbalah tradition") per section. The only specific ones (S3.C001-11, S4.C001-12) are accurate about the thesis but overstate Pico's own position and invent sources.
9. **The two style guides conflict** (quotation-first vs assertive synthesis; two citation systems; 1486 vs 1487) and both contain factual errors (Section 2c).
10. **Treat the repo as a scaffold.** Rebuild the spine from Farmer's numbered 900 (section.thesis ids), hold the 13 condemned theses as flags on their 4>/9>/3> parents, and quarantine the template rows so they cannot render as content.

---

## 1. True structure of the 900 versus the repo scheme

Farmer prints the historical part ("according to the doctrine/opinions of others", nominally 400) and the own-opinion part ("according to my own opinion", nominally 500). His chart: F:10566-10667 (historical) and F:10677-10762 (own opinion). Printed counts are 402 and 498, total 900 (F:10667, F:10761-10762). Farmer notes the nominal totals were altered by late revisions (F:10613-10616, 10716-10719).

### 1a. Farmer's structure

| Part | Section (Farmer no.) | Printed count | Latin heading line | Repo home |
|---|---|---|---|---|
| Latins, 115 (F:10595) | 1 Albert | 16 | F:10920 | none |
| | 2 Thomas | 45 | F:11238 | none |
| | 3 Francis of Meyronnes | 8 | F:11969 | none |
| | 4 Scotus | 22 | F:12135 | none |
| | 5 Henry of Ghent | 13 | F:12477 | none |
| | 6 Giles of Rome | 11 | F:12666 | none |
| Arabs, 82 (F:10609) | 7 Averroes | 41 | F:12859 | S3 (11 real + 109 filler) |
| | 8 Avicenna | 12 | F:13561 | S4 (12 real + 93 filler) |
| | 9 al-Farabi | 11 | F:13767 | none |
| | 10 Isaac of Narbonne | 4 | F:13964 | S8 (filler) |
| | 11 Abumaron (= Avenzoar, F:14071-14074) | 4 | F:14049 | S8 (filler) |
| | 12 Moses of Egypt (= Maimonides, F:14153-14154) | 3 | F:14134 | S6 (95 filler, mislabelled) |
| | 13 Mohammed of Toledo | 5 | F:14209 | none |
| | 14 Avempace | 2 | F:14297 | none |
| Greek Peripatetics, 29 (F:10634) | 15 Theophrastus (heading says III, chart says 4: F:14363 vs F:10627) | 4 | F:14362 | none |
| | 16 Ammonius | 3 | F:14469 | none |
| | 17 Simplicius | 9 | F:14541 | none |
| | 18 Alexander of Aphrodisias | 8 | F:14710 | none |
| | 19 Themistius | 5 | F:14876 | none |
| Platonists, 99 (F:10647) | 20 Plotinus | 15 | F:14987 | S1 (loose) |
| | 21 "Adeland the Arab" | 8 | F:15274 | S1 |
| | 22 Porphyry | 12 | F:15433 | S1 |
| | 23 Iamblichus | 9 | F:15632 | S1 |
| | 24 Proclus | 55 | F:15838 | S1 |
| Ancient sages, 77 (F:10665) | 25 Pythagorean mathematics (heading XIII, chart 14) | 14 | F:16886 | none |
| | 26 Chaldean theologians | 6 | F:17119 | S5 (filler) |
| | 27 Mercury Trismegistus | 10 | F:17236 | none (S6 title mislabels Moses as Hermetic) |
| | 28 Hebrew Cabalists | 47 | F:17420 | S7 C001-C047 |
| **Historical total** | | **402** | | |
| Own opinion | 1> Paradoxical reconciliations | 17 | F:18494 | none |
| | 2> Philosophical, against the common view | 80 | F:18858 | none |
| | 3> Paradoxical, new doctrines | 71 | F:20258 | none |
| | 4> Theological, against the common mode (title says 31; text has 29) | 29 | F:21432, 21490 | none (S9 is unrelated) |
| | 5> Plato | 62 | F:22132 | none |
| | 6> Book of Causes | 10 | F:23348 | none |
| | 7> / 7a> Mathematics | 11 + 74 = 85 | F:23606 | none |
| | 8> Zoroaster and Chaldeans | 15 | F:24715 | S5 (filler) |
| | 9> Magic | 26 | F:25106 | none |
| | 10> Orphic Hymns | 31 | F:25560 | none |
| | 11> Cabalistic, confirming the Christian religion (title says 71 at F:26276; text runs to 72, ends "(900)" at F:28088) | 72 | F:26227 | S7 C048-C118 (71 of 72) |
| **Own-opinion total** | | **498** | | |
| **Grand total** | | **900** | F:10762 | |

Arithmetic check (mine): 115+82+29+99+77 = 402; 17+80+71+29+62+10+85+15+26+31+72 = 498.

### 1b. Repo sections against the work

| Repo section (count) | Corresponds to something real? | Verdict |
|---|---|---|
| S1 (95) | Platonists as a group (99 theses, F:10647); content is "T1..T95" cluster themes, not theses. Plotinus alone has 15 (F:14987). | Loose match, zero real theses. Latin empty or "[FROM CRITICAL EDITION: T1 ...]". |
| S2 "Secundum Aristotelem" (110) | No. Pico has no Aristotle section; the nearest are the Greek Peripatetics (29) and the Latins (115). | Invented section. |
| S3 "Secundum Averroem" (120) | Yes, section 7, but 41 theses, not 120 (F:12860). | 11 real (7.1-7.11), 109 filler. |
| S4 "Secundum Avicennam" (105) | Yes, section 8, 12 theses (F:13562). | 12 real, 93 filler. Count exact for the real part. |
| S5 "Secundum Zoroastrem" (80) | Zoroaster and Chaldeans: 15 own-opinion (8>, F:24715) plus 6 Chaldean theologians (F:17119) = 21. | 80 has no basis. |
| S6 "Secundum Moysem Aegyptium" (95) | Section 12 is Moses of Egypt = Maimonides, 3 theses on metaphysics from the *Guide* (F:14153-14158, 14179-14198). | Count wrong; topic "Egyptian & Hermetic Magic" wrong (Hermes is section 27, 10 theses). |
| S7 "Secundum Hebraeos" (118) | Yes: section 28 (47) + 11> (72). Repo has 47 + 71. | Best-grounded section. Thesis 11>66 missing (Section 2). |
| S8 "Isaac Narbonensem et Abumaron" (8) | Yes, 4 + 4 = 8. | Count right. Topic "Medieval Jewish Philosophers" wrong: Abumaron is the Arab physician Avenzoar (F:14071-14074). |
| S9 "Secundum Theologos" (185) | No such section. Pico's own theology section has 29 (F:21490); the "Latin philosophers and theologians" heading (F:10915) covers 115. | Invented section. |
| Heretical (13) | Not a section of the work. The 13 come from 4> (9 of them: F:21461), 3> (2) and 9> (2). | Should be a flag, not a section. |

**Is 929 defensible?** No. Farmer's own total is 900 (F:10762). The repo has 775 filler rows, 141 real distinct theses (S7 118, S3 11, S4 12) and 13 Heretical rows: 775 + 141 + 13 = 929. The two Farmer sections whose titles disagree with their contents (4>: 31 vs 29, F:21490; 11>: 71 vs 72, F:26276) show that even the nominal count is contested; the repo should adopt Farmer's numbering (F:10761-10762) and record such discrepancies in a field.

---

## 2. Sample audit (28 entries)

Severity scale: **Critical** = invented, inverted or fabricated content; **High** = wrong gloss, missing translation or fabricated citation; **Medium** = truncation or overstatement; **Low** = correct but thin.

### 2a. Per-entry table

| id | Latin ok? | English real? | charge/defense specific? | section right? | severity | note |
|---|---|---|---|---|---|---|
| S7.C001 | Yes = 28.1 (F:17532-17533), cut at "irratio-" | Copy of Farmer's published translation (F:17586); cut at 150 characters mid-sentence; `english_full` swallows 28.2-28.5 | No: "[TO_SOURCE]". Exegesis "Divine Names" mismatches (28.1 is a priestly-sacrifice thesis; Farmer says Pico points to a mystical reading at 11>11, F:17563-17565) | Yes (F:17430) | Medium | Wirszubski quote in `scholar_citations` is not Wirszubski (2b-3). |
| S7.C010 | Yes = 28.10 (F:17728-17729), truncated; `latin_full` = incipit | Farmer verbatim (F:17787-17788) with stray "//" | No placeholders. Exegesis "Sefirot" fits (F:17752), by chance of a 5-label draw | Yes | Low | |
| S7.C040 | Yes = 28.40 (F:18298-18299), cut at "peti-" | Farmer verbatim (F:18349-18350) | Placeholders. "Sefirot" fits ("lord of the nose" = fifth sefirah, F:18326-18327) | Yes | Low | Wirszubski pp. 48-49 (W:2777-2799) gives Zohar III 130v and Recanati fol. 65ra as sources; unused. |
| S7.C070 | Yes = 11>23 (F:26904-26906), cut at "expo-" | **No**: English field is the Latin; Farmer's English exists (F:26962-26964) | Placeholders. Exegesis "Sefirot" and tags "gematria, letter combination" do not fit: thesis is Christological (F:26939-26941; W:8273-8277) | Yes; subsection label "Magia & Cabala" imprecise, Farmer's title is "Cabalistic conclusions confirming the Christian religion" (F:26276-26280) | High | Exemplar 3 below. |
| S7.C100 | Yes = 11>53 (F:27524-27526), truncated | **No**: Latin copy; Farmer English at F:27579-27582 | Placeholders. "Sefirot" acceptable (shining mirror / mirror not shining = 6th and 10th sefirot, F:27555-27558) | Yes | Medium | |
| S7.C118 | Yes = 11>72, complete (F:28032-28033) | **No**: Latin copy; Farmer English at F:28087-28088 | Placeholders. Exegesis "Gematria" is wrong; note F:28065-28071 reads book of God / book of the Law = nature / Torah, and the closing plan to convert the Jews | Yes | Medium | This is the 900th thesis (F:28088) but the repo indexes it as the 71st of the set; thesis 11>66 is absent (2b-2). |
| H.1.1 | **Reconstructed**, not Farmer's: repo "vere et secundum existentiam realem ... infernum, sicut communis via docet et Thomas" vs Farmer 4>8 "ueraciter et quantum ad realem presentiam descendit ad inferos ut ponit Thommas et communis uia" (F:21657-21658). Identical to the string at `S1_RESEARCH_NOTES.md` line 14, where it is labelled "Original Latin". | Real rendering of Q1; matches Copenhaver's wording (C:1991-1993) and Farmer (F:21714-21715) closely | Boilerplate (identical across 13). Exegesis reads "Pico's conclusion on Kabbalah" for a Christology thesis | Right thesis (Q1 = 4>8) | High | `latin_verified` false, correctly. |
| H.1.2 | "TO BE VERIFIED" | same | boilerplate; tags say `original_sin` | Q2 is punishment for mortal sin (A:1034), 4>19-20 (F:21879-21880) | High | Unfilled; research notes title Q2 "Original Sin", which is wrong. |
| H.1.3 | "TO BE VERIFIED" | same | boilerplate; tags "magic, idolatry" unsupported | Q3 = 4>14 cross and images (F:21771-21772; A:1035) | High | Unfilled. |
| H.1.4 | **Invented**: "Christus non accepit naturam humanam, sed hominem accepit" occurs nowhere in the 900 | invented; asserts a Nestorian-sounding claim Pico never made | boilerplate | Real Q4 = 4>13, on God's assuming irrational nature (F:21767-21768; C:6908-6909; A:1036) | **Critical** | Exemplar 2. |
| H.1.5 | Yes = 9>9 (F:25208-25209), orthography normalised | Real; acceptable | boilerplate; exegesis "Magic" for a Kabbalah thesis | Right (Q5) | Low | Only fully correct heretical entry. |
| H.1.6 | **Inverted**: repo "dummodo paneitas tollatur" ("provided breadness is taken away"); Farmer 4>2 "sine conuersione panis in corpus Christi uel paneitatis anihilatione" (F:21444-21446) means without annihilation of breadness | Inverted and drops the "de possibili, non de sic esse" clause (F:21447-21448) | boilerplate | Right (Q6 = 4>2) | **Critical** | Exemplar 1. |
| H.1.7 | "TO BE VERIFIED" | same | boilerplate | Q7 = 4>29 Origen (F:22051-22053) | High | Unfilled. |
| H.1.8 | "TO BE VERIFIED" | same | boilerplate | Q8 = 4>18 belief (F:21862-21870) | High | Unfilled. |
| H.1.9 | **Not a thesis of the 900**; states the opposite of the real Q9 premise: Farmer 4>1 "accidens existere non posse nisi inexistat" (F:21439-21441) | invented ("An accident can exist without a substance") | boilerplate | Real Q9 = 4>1 (C:8922-8931) | **Critical** | Hard error. |
| H.1.10 | Invented ("Hoc est enim corpus meum, propositio vera est, sumendo illud materialiter, non significative"); Farmer 4>10 "Illa uerba (hoc est corpus, etc.) quae in consecratione dicuntur materialiter tenentur non significatiue" (F:21666-21667) | Distorted: adds "is true"; the thesis says the words are taken materially, i.e. as quoted matter (F:21745-21750) | boilerplate | Right (Q10 = 4>10) | High | |
| H.1.11 | "TO BE VERIFIED" | same | boilerplate | Q11 miracles; probably 9>8 (F:25204-25205), unconfirmed (Section 5) | High | Unfilled. |
| H.1.12 | "TO BE VERIFIED" | same | boilerplate | Q12 = 3>49 (F:20990-20991) | High | Unfilled. |
| H.1.13 | "TO BE VERIFIED" | same | boilerplate | Q13 = 3>60 (F:21254; C:5825) | High | Unfilled. |
| S1.C001 | Placeholder "[FROM CRITICAL EDITION: T1 The One]" | Template sentence "The One transcends being and all predicates" (`template_S1`); no such thesis | Invented cluster note ("check whether Pico invokes Pseudo-Dionysius"); Farmer's first Plotinus thesis 20.1 says the first intelligible does not exist beyond the first intellect (F:15049), drawn from Enneads 5.5.1ff (F:15071-15072); repo cites Enneads 5.1.1, 6.9.3 | Loose (Platonists) | **Critical** | |
| S1.C050 | Empty | Template "Individual souls possess immortality through theosis" | Boilerplate charge about "hierarchy denying divine sovereignty" attached to a "soul faculties" cluster; the real immortality thesis is 20.3 "All life is immortal" (F:15055) and Plotinus has only 15 theses (F:14987) | No Plotinus no. 50 exists | **Critical** | |
| S2.C001 | Placeholder | Template "Being is predicated primarily of substance"; no hit in Farmer | One charge string for all 110 ("Challenges Platonic forms or Christian metaphysics") | No Aristotle section exists | **Critical** | S2.C060 identical pattern. |
| S3.C001 | Near: "Possibilis est ... " vs Farmer "Possibile est prophetia in somnis per illustrationem intellectus agentis super animam nostram" (F:12864-12865); grammar slip | Paraphrase of Farmer's English (F:12906-12907), reworded | Charge fine. Defense wrong in kind: "Pico accepts this ... not demonic deception". Section 7 is headed "according to the opinions of others"; Farmer's note says only that it stems from commentary on *De divinatione per somnum* and that a study is needed (F:12923-12925). "Influenced by Avicenna" unsupported | Yes (F:12859) | Medium | |
| S3.C002 | Yes = 7.2 (F:12937), "Vna" normalised | Real: F:12991 | Charge accurate and specific (unity of intellect). Defense cross-refers to 7.4 correctly (F:13001-13002) but "explicitly rejects" overstates | Yes | Low | Best entry in the sample; Exemplar 4. |
| S4.C001 | Yes = 8.1 (F:13566-13567), orthography normalised | Paraphrase; adds "a third kind" not in the source (F:13620-13621) | Commentary ("tools for metaphysician and magician") unsupported; Farmer ties 8.1-2 to the Prior Analytics series drawn from del Medigo's translation of Averroes (F:13362-13366, 13604). Exegesis "Divine Attributes" wrong (it is logic) | Yes | High | Fabricated Farmer quotation (2b-4). |
| S4.C002 | Yes = 8.2 (F:13570-13572) | Close paraphrase of Farmer (F:13624-13627) | Charge true and specific. Defense ("modal necessities ... prophetic knowledge") unsupported. Exegesis "Causation" wrong | Yes | Medium | |
| S5.C040 | Placeholder | Template "Evil arises from matter's resistance to form"; no hit | Boilerplate "Persian dualism" charge. Keyword search finds no dualist Zoroaster theses in Farmer (no hit for Ahriman/Ahura outside the bibliography); the section's own note treats the "Chaldean" oracles (F:24735-24740) | Section real only at 21 theses | **Critical** | |
| S9.C100 | Placeholder | Template "The Church is the mystical body of Christ"; no hit | One charge string for all 185 | No such section | **Critical** | |

### 2b. Hard errors register (separate from prose weakness)

1. **Inverted or invented condemned theses**: H.1.4 (invented), H.1.6 (inverted), H.1.9 (opposite of the real premise), H.1.10 (Latin invented, "is true" added). Sources: rows above.
2. **One real thesis missing from S7.** S7 holds 71 own-opinion Cabalistic entries. Mapping every entry to Farmer's numbers (by incipit search) shows C048-C065 = 11>1-11>18 (offset 47) through C112 = 11>65, then C113 = 11>67 (Farmer's 11>66 "Ego animam nostram sic decem sephirot adapto..." at F:27834 has no entry), then C114 = 11>68, C118 = 11>72. Farmer's own title says 71 while the text has 72 (F:26276, 28032).
3. **Citations that cannot stand.**
   - S7 Wirszubski #1 ("Christian Kabbalism of the Renaissance... Pico's role was especially important because he used the Jewish Kabbala for the confirmation of Christian theology"): spliced with an ellipsis from two separate spots of the book's Introduction (W:240-241 and 248-250, page [ix]); the Introduction speaks about Wirszubski in the third person (W:225-228), so it is not by him (the editorial author is not named in the lines I read). No page given.
   - S7 Wirszubski #3 ("Pico's Kabbalistic thought synthesized multiple Jewish mystical traditions through the work of Mithridates' translations"): no match in any of the 73 Markdown files (regex search, tolerant of OCR spacing).
   - S7 Copenhaver ("Abulafia's letter explains why the futility of attempting to get at the divine through the sefirotic Kabbalah..."): paraphrase, not a quotation, of CM:14366-14371; shown 47 times, once per historical entry, none of which is about Abulafia.
   - Counts: the citation manifest's "283 verified" = 118 + 118 + 47 uses of these 3 strings.
4. **S4.C001**: the "Farmer" quotation ("The twelve theses secundum Avicennam ... between Averroes's forty-one and al-Farabi's eleven", page 264) and the work title "Syncretism in the West: Pico's Platform (1998)" exist nowhere; the real title is "... Pico's 900 Theses (1486)". The second Farmer quote in S4.C002 ("Pico's reception of Avicennan logic reflects...") has no match either. "Deborah Black, *Logic and Intellect in Averroes* (2006)" is not in the corpus; the only Black (2006) the corpus cites on Pico is Crofton Black on the *Heptaplus* (C:2216-2218), so this looks like a conflation (inference).
5. **S1_RESEARCH_NOTES.md** attributes to Copenhaver (pp. 28, 44) the sentences beginning "The Q1 thesis reveals Pico at his most scholastically sophisticated" and "The metaphysical problem of how a bodiless spirit can be 'in' a place was technically demanding". Neither string, nor "defending orthodoxy through metaphysical precision", occurs in Copenhaver (regex search on `753eb1fa.md`). The verdict formula the notes quote is real (C:1276-1279).
6. **English field misuse in S7**: of 118, 44 hold a copy of the Latin, 23 read "[TO_TRANSLATE]" (C006-C009, C011-C014, C016-C019, C021-C024, C036-C037, C041-C043, C046-C047), 19 hold English text in both fields, 32 have a distinct English string. Farmer prints English for all (for example 28.47 at F:18456-18457).
7. **Latin field misuse in S7**: 23 entries put English in `latin_incipit` (C044, C057-C060, C064, C071, C076, C081-C083, C087-C088, C091-C094, C096-C098, C102-C103, C113). Most are OCR page-order collisions; C044 is an English translation of 28.44 (F:18443-18445) sitting in the Latin field.
8. **Rights**: where S7 has an English rendering (C001-C005, C010, C020, C025-C035, C038-C040 ...), it reproduces Farmer's published translation verbatim (checked at F:17586, 17787, 18349-18350) under `translation_source: "Farmer 1998"`. Whether reuse is licensed is a decision for the project owner; the data does not record one. S3/S4 English is a close rewording of Farmer's.
9. **Scholar attribution drift**: S7's first subsection label credits "sapientum Hebraeorum Cabalistarum" correctly (F:17430), but S6 attaches Moses of Egypt (Maimonides) to "Hermeticism" (F:14153-14158).
10. **Schema drift**: `schema.json` demands `conclusion_id` like "I.1.1" and `english_translation` as an object, status in {unstarted, draft, sourced, complete, reviewed}, and lowercase tags with a typo ("aristotlelianism"). Data uses S7.C001 ids, `english_translation` as string or object, status "standardized", tags "Kabbalah, divine names, gematria", `page` vs `pages`, and un-schema'd `charge`/`defense`/`latin_full` fields. Nothing validates.

### 2c. Prose weakness and style-guide problems

- **Exegesis**: every S1-S9 exegesis is a one-line stub of the form "Pico's conclusion on *X* within the *Y* tradition", with X drawn from 3-5 labels per section (S7: 5 stubs across 118 entries; S9: 5 across 185). The label frequently misdescribes the thesis (H.1.1 "Kabbalah"; S4.C001 "Divine Attributes"; S7.C070 "Sefirot"; S7.C118 "Gematria").
- **charge/defense**: 1 distinct charge and 1 distinct defense per section in S2, S5, S6, S8, S9; the Heretical set has one charge ("Condemned by papal bull (1486)") and one defense ("Contains profound theological truth requiring proper interpretation") for all 13.
- **Status inflation**: Heretical entries carry `status: sourced` with zero citations and 7 of 13 unfilled; S7 carries `status: standardized` with placeholders in charge/defense and 67 of 118 lacking an English rendering (44 Latin copies, 23 "[TO_TRANSLATE]").
- **Tags**: the 71 own-opinion Cabalistic entries share one tag list, ["Kabbalah", "magic", "divine names", "gematria", "letter combination"].

**Where the two style guides conflict**

| Point | `STYLE_GUIDE.md` | `PICO900_STYLE_GUIDE.md` |
|---|---|---|
| Method | quotation first, "avoid paraphrases", every scholarly claim backed by a quotation (Core principles 3; Quality checklist) | assertive synthesis in a scholar's voice; "just argue it"; hedging is a failure (Voice 1) |
| Citation form | **Scholar** (*Work*, p. X) with [VERIFIED]/[CITED]/[INFERRED] tags | author-date in text, Chicago bibliography, evidence status Verified/Likely/Probable/Uncertain/Placeholder |
| Heresy vocabulary | "condemned", "attacked" | prefer "heresy indictment / heresy charge" over "persecution" or "attacks" |
| Date of the affair | "condemned by Pope Innocent VIII in 1486" and "papal commission, 1486" (lines 92, 105) | timeline example says February 1487 (correct, C:514) |
| Heretical clusters | Q1-Q3 "Incarnation", Q4/Q7/Q11 "Soul, Intellect & Immortality", Q8/Q12/Q13 "belief, unity, miracle" | not addressed |

**Factual errors in the guides** (both checked against the corpus):
- `STYLE_GUIDE.md` clusters (lines 133-137) mislabel the Questions: Q2 is punishment for mortal sin, Q3 worship of the cross, Q4 the assumption of natures, Q7 Origen, Q11 Christ's miracles (C:846-850; A:1033-1045). Its heretical-entry example on unity of intellect is not among the thirteen (that material is Averroes 7.2-7.4, F:12991-13002). Its worked example "Conclusion I.1.2, *Anima est forma substantialis corporis*" is not a thesis of the 900 (no hit in Farmer).
- `PICO900_STYLE_GUIDE.md` line 22 gives a "Copenhaver" model quotation ("zigging and zagging") found in no corpus file. Line 138 says the *Apologia* "remains unpublished in modern critical edition": Fornaciari's edition (2010) is in the corpus and cited by Copenhaver (C:525-527). "Howlett, *Life and Works* (2019)" and "Howlett, three chapters" have no counterpart in the corpus: the only Howlett file is a short article by Sophia Howlett (`Critical_Political_Theory_..._Howlett_-_Re-evaluating_Pico...`), and Copenhaver's *Pico on Trial* does not cite Howlett at all (grep). Both guides use "Howlett" as if a major authority.

---

## 3. The 13 condemned theses

Source of the list. Copenhaver names the thirteen by topic in the order of the *Apology* (C:846-850): Q1 Hell, Q2 Sin, Q3 Worship, Q4 Incarnation, Q5 Kabbalah, Q6 Eucharist, Q7 Origen, Q8 Belief, Q9 Eucharist, Q10 Eucharist, Q11 Miracle, Q12 God, Q13 Soul. The Fornaciari contents give the Latin headings (A:1033-1045). Farmer identifies which section-4 theses the commission attacked and says nine of the thirteen come from that section (F:21461-21462); my mapping yields exactly 9 in 4>, 2 in 3>, 2 in 9>. Copenhaver's printed order of the theses in the *Conclusions*, Q12, Q13, Q9, Q6, Q1 (C:1252-1253), agrees with the positions 3>49, 3>60, 4>1, 4>2, 4>8.

| Q | Topic | Real thesis (Farmer id, line) | Latin incipit (Farmer) | Commission's finding (source) | Repo entry | Result |
|---|---|---|---|---|---|---|
| Q1 | Descent into Hell | 4>8 (F:21657) | Christus non ueraciter et quantum ad realem presentiam descendit ad inferos ut ponit Thommas et communis uia, sed solum quo ad effectum | false, erroneous, heretical, against Scripture (F:21696-21697; C:1276-1279) | H.1.1 | **Matches in substance**; Latin reconstructed, differs from Farmer |
| Q2 | Punishment of mortal sin | 4>19-20 (F:21873-21880) | Secunda est quod peccato mortali finiti temporis non debetur poena infinita secundum tempus, sed finita tantum | false, erroneous, heretical (F:21940-21942) | H.1.2 | **Unfilled**; tags and notes title it "original sin" (wrong) |
| Q3 | Adoration of the cross and images | 4>14 (F:21771) | Nec crux Christi nec ulla imago adoranda est adoratione latriae, etiam eo modo quo ponit Thommas | scandalous, offensive to pious ears, against the usage of the church (F:21837-21839) | H.1.3 | **Unfilled** |
| Q4 | Assumption of natures by God | 4>13 (F:21767) | Non assentior communi sententiae theologorum dicentium posse deum quamlibet naturam suppositare, sed de rationali tamen hoc concedo | derogates from divine omnipotence, savors of heresy (F:21792-21793) | H.1.4 | **Wrong** (invented thesis) |
| Q5 | Magic and Kabbalah prove Christ's divinity | 9>9 (F:25208-25209) | Nulla est scientia quae nos magis certificet de diuinitate Christi quam magia et cabala | verdict wording not located; Copenhaver says the judges could not follow it (C:912-915) | H.1.5 | **Matches** |
| Q6 | Eucharist: presence without conversion | 4>2 (F:21444) | Si teneatur communis uia de possibilitate suppositationis ... sine conuersione panis in corpus Christi uel paneitatis anihilatione, potest fieri ut in altari sit corpus Christi ... | erroneous (C:8641-8642; C:8901-8903) | H.1.6 | **Inverted** |
| Q7 | Salvation of Origen | 4>29 (F:22051-22053) | Rationabilius est credere Origenem esse saluum, quam credere ipsum esse damnatum | rash and savoring of heresy (F:22113-22114) | H.1.7 | **Unfilled** |
| Q8 | Freedom to believe | 4>18 (F:21862-21870) | Dico probabiliter, et nisi esset communis modus dicendi theologorum in oppositum, firmiter assererem ... nullus credit aliquid esse uerum praecise quia uult credere id esse uerum | erroneous, savoring of heresy (F:21895-21896) | H.1.8 | **Unfilled** |
| Q9 | Eucharist: accidents | 4>1 (F:21439-21441) | Qui dixerit accidens existere non posse nisi inexistat, Eucharistiae poterit sacramentum tenere etiam tenendo panis substantiam non remanere ut tenet communis uia | erroneous (C:8901-8902) | H.1.9 | **Wrong** (states the opposite) |
| Q10 | Eucharist: words of consecration | 4>10 (F:21666-21667) | Illa uerba (hoc est corpus, etc.), quae in consecratione dicuntur, materialiter tenentur non significatiue | scandalous, contrary to the common opinion of holy doctors (F:21750-21752; C:8902-8903) | H.1.10 | **Latin invented, English distorted** |
| Q11 | Christ's miracles | probably 9>8 (F:25204-25205), unconfirmed | Miracula Christi non ratione rei factae, sed ratione modi faciendi, suae diuinitatis argumentum certissimum sunt | not located | H.1.11 | **Unfilled**; identification unverified (Section 5) |
| Q12 | Whether God understands | 3>49 (F:20990-20991) | Magis improprie dicitur de deo quod sit intellectus uel intelligens, quam de anima rationali quod sit angelus | "false and can be taken in a heretical sense" (F:21058-21059) | H.1.12 | **Unfilled** |
| Q13 | The hidden understanding of the soul | 3>60 (F:21254; C:5825) | Nihil intelligit actu et distincte anima, nisi se ipsam | attacked by the commission (F:21289); wording of verdict not located | H.1.13 | **Unfilled** |

Tally: matches 2 (H.1.1 in substance, H.1.5); inverted or invented 3 (H.1.4, H.1.6, H.1.9); distorted 1 (H.1.10); unfilled 7 (H.1.2, .3, .7, .8, .11, .12, .13). All 13 carry zero citations, `heretical_notes: null` and the same charge/defense strings. `S1_RESEARCH_NOTES.md` repeats the errors: it lists Q2 as "Original Sin" and gives H.1.4, H.1.6 and H.1.9 as "Original Latin" (lines 111, 207, 321).

### Dates: correction to "Condemned by papal bull (1486)"

| Event | Correct date | Source |
|---|---|---|
| *Conclusiones* printed, Rome (Eucharius Silber), colophon | 7 December 1486 | F:28040-28042, 28095-28098 |
| Debate announced for after the Epiphany | after 6 January 1487 (the text says "post Epiphaniam"; the date is my inference) | F:28046, 28102 |
| Pope creates the commission | February 1487 | C:514, 543 |
| Commission's first meeting; verdicts recorded | first meeting Wednesday 2 March; Q1 verdict recorded 5 March; verdicts in "before the third week of March" | C:545-546, 1281, 543-544 |
| *Apologia* written after the verdicts | spring 1487 (Copenhaver dates it after March 5; the exact publication date was not located) | C:1281-1282 |
| Bull condemning the work as a whole | signed 4 August 1487, published four months later | F:1326-1327 |
| Bull's penalties | all copies burned within three days; excommunication for reading, copying, printing or hearing it read | F:1360-1365 |

Correction. The thirteen theses were **censured by a papal commission in March 1487** (Farmer: "advisory judgment", F:1323-1325); **no condemnation existed in 1486**, the year of publication. The **bull of 4 August 1487** condemned the whole book, not the thirteen (F:1325-1332). The field `charge` should read: "Censured by the papal commission of 1487 (verdict: ...); the whole work condemned by Innocent VIII's bull of 4 August 1487." Copenhaver himself speaks of the Pope having "condemned" thirteen propositions "within weeks" of publication (C:247-248), which describes the commission stage, not the bull.

---

## 4. Rewrite exemplars (exegesis field, PICO900 style guide voice)

Each text carries locators; nothing here quotes Farmer's or Copenhaver's English. Latin of the 1486 theses is quoted. Where I could not verify a claim I have said so in the text.

### Exemplar 1 (worst): H.1.6, thesis Q6 = 4>2

> Thesis 4>2 reads: "Si teneatur communis uia de possibilitate suppositationis in respectu ad quamcunque creaturam, dico quod sine conuersione panis in corpus Christi uel paneitatis anihilatione, potest fieri ut in altari sit corpus Christi secundum ueritatem sacramenti Eucharistiae; quod sit dictum loquendo de possibili, non de sic esse" (Farmer, l. 21444-21448). Given the common opinion that a divine supposit can take on any creature, Christ's body could stand on the altar while the bread's substance stays unconverted and its breadness (*paneitas*) stays unannihilated. The closing clause confines the claim to possibility and asserts nothing about the sacrament as instituted (Farmer, l. 21524-21528). The earlier entry's Latin ("dummodo paneitas tollatur") reverses the printed text, which excludes the annihilation of breadness. The model descends from Jean Quidort's impanation theory, in which the Word assumes the bread's nature; Pico took it second-hand from Jean Cabrol (Copenhaver, l. 786-788, 8050-8078). Copenhaver treats Q6 as the one condemned thesis whose wording appeals to possibility, and records that the commission judged it erroneous all the same (l. 8574-8577, 8641-8642).

(About 175 words. Unverified: the exact verdict wording for Q6; my sources give only "erroneous".)

### Exemplar 2 (worst): H.1.4, thesis Q4 = 4>13

> Thesis 4>13 reads: "Non assentior communi sententiae theologorum dicentium posse deum quamlibet naturam suppositare, sed de rationali tamen hoc concedo" (Farmer, l. 21767-21768; Copenhaver, l. 6908-6909). Pico withholds assent from the common opinion that God can assume any nature and grants assumption of a rational nature. The Latin previously carried under H.1.4 ("Christus non accepit naturam humanam, sed hominem accepit") occurs nowhere in the 900. This is the only condemned thesis phrased in the first person, and Pico chose *non assentior* over *non credo* to reduce his exposure (Copenhaver, l. 5818-5821, 6932-6939). The commission ruled that the thesis derogates from divine omnipotence and savors of heresy (Farmer, l. 21792-21793). Pico answered orally, on the authority of Henry of Ghent, that natures below the rational are not assumable, whatever God's power; in the *Apology* he retreated to a quarrel with the way the common opinion argues (Farmer, l. 21789-21796). Copenhaver adds that Henry himself abandoned the common opinion (l. 6880-6883).

(About 165 words.)

### Exemplar 3 (worst): S7.C070, thesis 11>23

> Thesis 11>23 reads: "Per illud dictum Hieremiae: Lacerauit uerbum suum, secundum expositionem Cabalistarum, habemus intelligere quod deum sanctum et benedictum lacerauit deus pro peccatoribus" (Farmer, l. 26904-26906). Wirszubski identifies the verse as Lam. 2:17 and shows two strands fused in Pico's reading: the midrashic "God rent his purple" (Wayyikra Rabba, Lamentations Rabba, Zohar I 61v) and the Kabbalistic equation of "word" (*verbum*) with the tenth sefirah (W:8273-8277, 8322-8330; 1989, 162-63). Farmer confirms the tenth-sefirah reading and adds that the Word of John 1:1 enters the sense (l. 26939-26941). Wirszubski groups theses 21-24 of the set under one pattern: an existing rabbinic or Kabbalistic exposition receives a Christian meaning, the method of Raymundus Martini's *Pugio fidei* (W:8298-8308). Thesis 11>23 presents the divine self-laceration for sinners as the Cabalists' own doctrine, and 11>24 continues to the claim that the death of Christ satisfies for human sin (Farmer, l. 26909-26914). The tags "gematria" and "letter combination" and the label "Sefirot" in the earlier entry do not describe this thesis.

(About 170 words. Unverified: which of the two strands Pico intended as primary; Wirszubski says the verse "can only be" Lam. 2:17 and does not rank the strands.)

### Exemplar 4 (best): S3.C002, thesis 7.2

> Thesis 7.2, "Vna est anima intellectiua in omnibus hominibus" (Farmer, l. 12937), opens the Averroes series on the unity of the intellect. Farmer traces 7.2-4 to commentary on *De anima* 3.5 and ties them to Simplicius 17.9, Alexander 18.1, Plotinus 20.7 and Pico's own 3>67-69 (l. 12967-12971, 12978-12979); thesis 3>69 gives as a probability the view that each series of souls is beatified in its own intellect (l. 21396-21398). The section stands under the heading "according to the opinions of others": 7.2 reports Averroes and commits Pico to nothing. Thesis 7.3 defends Averroes' account of the conjunction of agent and possible intellect against John of Jandun (l. 12940-12944). Thesis 7.4 keeps the unity of the intellect and allows that my soul, so particularly mine that it is shared with no one, remains after death (l. 13001-13002). The earlier entry's claim that Pico "explicitly rejects" 7.2 in 7.4 overstates: 7.4 leaves 7.2 standing and adds a harmonizing clause. Farmer notes that Nifo later credited Pico with a resolution tied to Albert the Great and finds it only loosely related to the theses (l. 12975-12979).

(About 175 words.)

---

## 5. What I could not verify, and why

1. **Q11's thesis.** The Copenhaver table and the Apologia contents give the topic ("Miracle", "de miraculis Christi": C:848, A:1043), and Farmer's count (9 of 13 in 4>, F:21461-21462) leaves 9> as the only remaining place. I did not find a passage naming the exact thesis. 9>7 ("opera Christi ... per uiam magiae uel per uiam cabalae", F:25200-25201) and 9>8 (F:25204-25205) are the candidates; I chose 9>8 from memory of the *Apology* and mark it unconfirmed.
2. **Commission wording for Q5, Q11, Q13.** Farmer quotes the commission for Q1-Q4, Q7, Q8, Q10 and Q12, Copenhaver for Q1, Q6, Q9 and Q10. My searches did not surface verdicts for Q5, Q11, Q13. The Fornaciari file in the corpus holds only front matter and contents (1103 lines), so the *Apologia* text itself was not available to me.
3. **Farmer's full count.** I verified totals against Farmer's chart (F:10566-10762) and each section heading line, not by counting all 900 theses. Farmer's headings and chart disagree by one in a few places (Theophrastus, Pythagorean mathematics, sections 4> and 11>, F:14363, 16887, 21490, 26276); I report both.
4. **Missing S7 thesis.** The 11>66 result comes from an incipit-matching script on the repo JSON against Farmer's OCR; three S7 entries (C015, C075, C081) did not match on my first-pass search because of OCR variance, and I resolved the offset from their neighbours, not from a direct hit.
5. **Verbatim reuse of Farmer's English.** Checked in three S7 entries only (C001, C010, C040). I did not compare all 32 entries with a distinct English rendering, nor test the S3/S4 English beyond the first two entries of each.
6. **Citation searches.** I searched by regex across the 73 Markdown files with tolerance for double spaces. OCR hyphenation or a different edition (for example the Cambridge or Harvard pagination of Wirszubski) could hide a valid source for the two "not found" quotations. The result is "no match in the corpus", not proof that no such sentence exists in print. The S1_RESEARCH_NOTES quotes and the style-guide quote get the same caveat.
7. **Wirszubski Introduction authorship.** The lines I read (W:225-256) show that the Introduction is not by Wirszubski; I did not locate the signature, so I cannot name its author.
8. **"Deborah Black" versus "Crofton Black."** My statement that the repo conflates the two is an inference from the corpus containing only Crofton Black (2006) on Pico.
9. **Brown critical edition.** I audited the repo's Latin against Farmer's edition, not against the Brown edition named in `CLAUDE.md` (no network access) and not against the 1486 editio princeps. Farmer's Latin normalises u/v and punctuation, so orthographic differences reported here are of that kind unless marked as a wording difference.
10. **Rows I did not read.** I sampled 28 of 929 entries and computed structural statistics (placeholder counts, distinct-string counts) over all of them. Claims about S2, S5, S6, S8, S9 rest on 1 to 2 entries each plus those statistics. I did not read the megabase or PicoDB files cited as translation sources.
11. **Copyright judgement.** I state what the data shows (verbatim reuse of a published translation, with no licence recorded); I make no legal determination.
