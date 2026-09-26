#!/usr/bin/env python3
"""seed_inventory.py: writes data/inventory/{farmer_structure,condemned_thirteen}.json and data/quarantine.json.

These are transcribed from audit/A1_conclusions.md (sections 1a, 2a, 3), which read Farmer's edition
line by line. They are the *inventory* the edition should be built from: the work's real structure,
not the retired S1..S9 scheme. Provenance is recorded in each file. Re-running overwrites them, so
edit this script (or replace it with a re-derivation straight from Farmer) rather than the JSON.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "E:\\pdf\\renaissance magic\\Pico\\Markdown\\Stephen_A_Farmer_..._c99b971b.md"


def dump(rel, obj):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)


hist = [
    ("Latins", 1, "Albert (the Great)", 16, 10920, None),
    ("Latins", 2, "Thomas Aquinas", 45, 11238, None),
    ("Latins", 3, "Francis of Meyronnes", 8, 11969, None),
    ("Latins", 4, "Scotus", 22, 12135, None),
    ("Latins", 5, "Henry of Ghent", 13, 12477, None),
    ("Latins", 6, "Giles of Rome", 11, 12666, None),
    ("Arabs", 7, "Averroes", 41, 12859, "S3 (11 real + 109 filler)"),
    ("Arabs", 8, "Avicenna", 12, 13561, "S4 (12 real + 93 filler)"),
    ("Arabs", 9, "al-Farabi", 11, 13767, None),
    ("Arabs", 10, "Isaac of Narbonne", 4, 13964, "S8 (filler)"),
    ("Arabs", 11, "Abumaron (= Avenzoar, F:14071-14074)", 4, 14049, "S8 (filler)"),
    ("Arabs", 12, "Moses of Egypt (= Maimonides, F:14153-14154)", 3, 14134, "S6 (95 filler, mislabelled)"),
    ("Arabs", 13, "Mohammed of Toledo", 5, 14209, None),
    ("Arabs", 14, "Avempace", 2, 14297, None),
    ("Greek Peripatetics", 15, "Theophrastus (heading says III, chart says 4: F:14363 vs F:10627)", 4, 14362, None),
    ("Greek Peripatetics", 16, "Ammonius", 3, 14469, None),
    ("Greek Peripatetics", 17, "Simplicius", 9, 14541, None),
    ("Greek Peripatetics", 18, "Alexander of Aphrodisias", 8, 14710, None),
    ("Greek Peripatetics", 19, "Themistius", 5, 14876, None),
    ("Platonists", 20, "Plotinus", 15, 14987, "S1 (loose)"),
    ("Platonists", 21, "'Adeland the Arab'", 8, 15274, "S1"),
    ("Platonists", 22, "Porphyry", 12, 15433, "S1"),
    ("Platonists", 23, "Iamblichus", 9, 15632, "S1"),
    ("Platonists", 24, "Proclus", 55, 15838, "S1"),
    ("Ancient sages", 25, "Pythagorean mathematics (heading XIII, chart 14)", 14, 16886, None),
    ("Ancient sages", 26, "Chaldean theologians", 6, 17119, "S5 (filler)"),
    ("Ancient sages", 27, "Mercury Trismegistus", 10, 17236, None),
    ("Ancient sages", 28, "Hebrew Cabalists", 47, 17420, "S7 C001-C047"),
]
own = [
    ("1>", "Paradoxical reconciliations", 17, 18494, None),
    ("2>", "Philosophical, against the common view", 80, 18858, None),
    ("3>", "Paradoxical, new doctrines", 71, 20258, None),
    ("4>", "Theological, against the common mode (title says 31; text has 29)", 29, 21432, None),
    ("5>", "Plato", 62, 22132, None),
    ("6>", "Book of Causes", 10, 23348, None),
    ("7>/7a>", "Mathematics (11 + 74)", 85, 23606, None),
    ("8>", "Zoroaster and Chaldeans", 15, 24715, "S5 (filler)"),
    ("9>", "Magic", 26, 25106, None),
    ("10>", "Orphic Hymns", 31, 25560, None),
    ("11>", "Cabalistic, confirming the Christian religion (title says 71 at F:26276; text runs to 72, ends '(900)' at F:28088)",
     72, 26227, "S7 C048-C118 (71 of 72; 11>66 missing)"),
]
ht, ot = sum(x[3] for x in hist), sum(x[2] for x in own)
assert (ht, ot) == (402, 498), (ht, ot)
dump("data/inventory/farmer_structure.json", {
    "_provenance": "Transcribed from audit/A1_conclusions.md s1a, which read Farmer's edition (Syncretism in the West, MRTS 167, Tempe 1998). Line numbers (F:) are into " + F + ". Counts are Farmer's printed counts; headings and chart disagree by one in four places (noted in the names). Not yet re-derived by a second agent.",
    "printed_total": 900, "historical_total": ht, "own_opinion_total": ot,
    "historical": [dict(group=g, section=n, name=nm, count=c, heading_line=l, repo_home=r) for g, n, nm, c, l, r in hist],
    "own_opinion": [dict(section=n, name=nm, count=c, heading_line=l, repo_home=r) for n, nm, c, l, r in own],
    "id_scheme": "Cite as Farmer's section.thesis: '7.2' for historical, '4>8' for own-opinion. The repo's S1..S9 ids are retired.",
    "repo_sections_with_no_counterpart": ["S2 Aristotle", "S9 Theologians"],
    "note": "The thirteen condemned theses are flags on 4>, 3> and 9> theses, not a section; see condemned_thirteen.json",
})

thirteen = [
    (1, "Descent into Hell", "4>8", 21657, "Christus non ueraciter et quantum ad realem presentiam descendit ad inferos ut ponit Thommas et communis uia, sed solum quo ad effectum", "H.1.1", "matches in substance; repo Latin reconstructed, differs from Farmer"),
    (2, "Punishment of mortal sin", "4>19-20", 21873, "Secunda est quod peccato mortali finiti temporis non debetur poena infinita secundum tempus, sed finita tantum", "H.1.2", "unfilled; repo tags wrongly say original sin"),
    (3, "Adoration of the cross and images", "4>14", 21771, "Nec crux Christi nec ulla imago adoranda est adoratione latriae, etiam eo modo quo ponit Thommas", "H.1.3", "unfilled"),
    (4, "Assumption of natures by God", "4>13", 21767, "Non assentior communi sententiae theologorum dicentium posse deum quamlibet naturam suppositare, sed de rationali tamen hoc concedo", "H.1.4", "WRONG: repo Latin invented"),
    (5, "Magic and Kabbalah and Christ's divinity", "9>9", 25208, "Nulla est scientia quae nos magis certificet de diuinitate Christi quam magia et cabala", "H.1.5", "matches"),
    (6, "Eucharist: presence without conversion", "4>2", 21444, "Si teneatur communis uia de possibilitate suppositationis in respectu ad quamcunque creaturam, dico quod sine conuersione panis in corpus Christi uel paneitatis anihilatione, potest fieri ut in altari sit corpus Christi ...", "H.1.6", "INVERTED in repo"),
    (7, "Salvation of Origen", "4>29", 22051, "Rationabilius est credere Origenem esse saluum, quam credere ipsum esse damnatum", "H.1.7", "unfilled"),
    (8, "Freedom to believe", "4>18", 21862, "Dico probabiliter, et nisi esset communis modus dicendi theologorum in oppositum, firmiter assererem ... nullus credit aliquid esse uerum praecise quia uult credere id esse uerum", "H.1.8", "unfilled"),
    (9, "Eucharist: accidents", "4>1", 21439, "Qui dixerit accidens existere non posse nisi inexistat, Eucharistiae poterit sacramentum tenere etiam tenendo panis substantiam non remanere ut tenet communis uia", "H.1.9", "WRONG: repo states the opposite"),
    (10, "Eucharist: words of consecration", "4>10", 21666, "Illa uerba (hoc est corpus, etc.), quae in consecratione dicuntur, materialiter tenentur non significatiue", "H.1.10", "repo Latin invented, English distorted"),
    (11, "Christ's miracles", "9>8 (UNCONFIRMED; 9>7 is the alternative)", 25204, "Miracula Christi non ratione rei factae, sed ratione modi faciendi, suae diuinitatis argumentum certissimum sunt", "H.1.11", "unfilled; identification unconfirmed"),
    (12, "Whether God understands", "3>49", 20990, "Magis improprie dicitur de deo quod sit intellectus uel intelligens, quam de anima rationali quod sit angelus", "H.1.12", "unfilled"),
    (13, "The hidden understanding of the soul", "3>60", 21254, "Nihil intelligit actu et distincte anima, nisi se ipsam", "H.1.13", "unfilled"),
]
dump("data/inventory/condemned_thirteen.json", {
    "_provenance": "Transcribed from audit/A1_conclusions.md s3. Copenhaver, Pico on Trial (C:846-850) names the thirteen by topic in the Apologia's order. Latin incipits are the auditor's transcription of Farmer's OCR (u/v and punctuation are Farmer's, not Pico's 1486 print): COLLATE against the Brown edition and the editio princeps before publication. Farmer's Latin is an edition; confirm reuse terms.",
    "dates": {
        "printed_Rome_Silber": "7 December 1486 (F:28040-28042)",
        "commission_created": "February 1487 (C:514, 543)",
        "commission_verdicts": "March 1487; first meeting 2 March, Q1 verdict 5 March (C:545-546, 1281)",
        "bull_Etsi_ex_iniuncto": "4 August 1487 (Black gives 8 August; A2); published in December; condemned the whole work, not only the thirteen (F:1325-1332)",
        "correction": "No condemnation existed in 1486. The repo's 'Condemned by papal bull (1486)' is wrong.",
    },
    "theses": [dict(q=q, topic=t, farmer_id=i, farmer_line=l, latin_incipit_farmer_ocr=lat, repo_entry=e, audit_result=r)
               for q, t, i, l, lat, e, r in thirteen],
})

items = []
for eid, fields, why in [
    ("H.1.1", ["latin"], "Latin reconstructed, differs from Farmer 4>8 (A1 s2a)"),
    ("H.1.4", ["latin", "translation"], "Invented thesis; not in the 900 (A1 s2a, s3)"),
    ("H.1.6", ["latin", "translation"], "Inverted: reverses 'sine ... paneitatis anihilatione' (A1 s2a, s3)"),
    ("H.1.9", ["latin", "translation"], "Not a thesis of the 900; states the opposite of 4>1 (A1 s2a, s3)"),
    ("H.1.10", ["latin", "translation"], "Latin invented; English adds 'is true' (A1 s2a, s3)"),
    ("S4.C001", ["citations"], "Fabricated 'Farmer' quotation and title (A1 s2b-4)"),
    ("S4.C002", ["citations"], "Fabricated 'Farmer' quotation (A1 s2b-4)"),
]:
    for f in fields:
        items.append({"id": eid, "field": f, "reason": why, "audit": "A1_conclusions.md"})
dump("data/quarantine.json", {
    "_note": "Fields proven wrong by audit. integrity_gate.py grades them 'quarantined' and the build never renders them. Remove an item only when a verified replacement exists.",
    "items": items,
})
print("wrote inventory (402 + 498 = 900), condemned_thirteen, quarantine:", len(items), "items")
