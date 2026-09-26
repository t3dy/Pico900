#!/usr/bin/env python3
"""build_dossiers.py: turn the inventory + harvested mentions into one research packet per thesis, the
WRITER's sole input (docs/ORCHESTRATION.md). Also writes data/ontology/theses.json (per-thesis aggregate:
statistics, suggested tier, connections) and research-packets/INDEX.md.

A packet contains only material with a locator: the Latin (Farmer line), the 1486 apparatus, short excerpts
of Farmer's notes (his commentary is in copyright: excerpts are for the WRITER to paraphrase with the
locator, never to reproduce), Farmer's cross-references with the Latin of the referenced theses, every
scholar mention with its context window, and the persons/concepts named in those windows (gazetteer counts).
Farmer's English translation is pointed to by line number only.
"""
import io, json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV, ONT = os.path.join(ROOT, "data", "inventory"), os.path.join(ROOT, "data", "ontology")
PK = os.path.join(ROOT, "research-packets")
NOTE_WORDS = 120

GAZETTEER = {  # display name -> regex (case-insensitive) over context windows and Farmer notes
    "Henry of Ghent": r"\bHenry of Ghent\b|\bHenricus\b|\bGandav", "Thomas Aquinas": r"\bAquinas\b|\bThomas\b(?! Anglicus)",
    "Duns Scotus": r"\bScotus\b", "Albert the Great": r"\bAlbert(us)?\b", "Giles of Rome": r"\bGiles\b|\bAegidius\b",
    "Francis of Meyronnes": r"\bMeyronnes\b|\bMayronnes\b|\bMeyronis\b", "Averroes": r"\bAverro", "Avicenna": r"\bAvicenna\b",
    "al-Farabi": r"\bFarabi\b", "Maimonides": r"\bMaimonides\b|\bMoses of Egypt\b", "Avempace": r"\bAvempace\b",
    "John of Jandun": r"\bJandun\b|\bGandavo\b", "Elia del Medigo": r"\bdel Medigo\b|\bElia\b", "Flavius Mithridates": r"\bMithridates\b|\bMithndates\b",
    "Marsilio Ficino": r"\bFicino\b", "Savonarola": r"\bSavonarola\b", "Lorenzo de' Medici": r"\bLorenzo\b", "Poliziano": r"\bPoliziano\b|\bPolitian\b",
    "Innocent VIII": r"\bInnocent\b", "Pedro Garsia": r"\bGarsia\b|\bGarcia\b", "Giovanni Caroli": r"\bCaroli\b", "Bernardo Torni": r"\bTorni\b",
    "Galgani da Siena": r"\bGalgani\b", "Antonio Cittadini": r"\bCittadini\b", "Pomponazzi": r"\bPomponazzi\b", "Agostino Nifo": r"\bNifo\b",
    "Menahem Recanati": r"\bRecanati\b", "Abraham Abulafia": r"\bAbulafia\b", "Yohanan Alemanno": r"\bAlemanno\b", "Gersonides": r"\bGersonides\b|\bLevi ben Gerson\b",
    "Proclus": r"\bProclus\b", "Plotinus": r"\bPlotinus\b", "Iamblichus": r"\bIamblichus\b", "Porphyry": r"\bPorphyry\b", "Simplicius": r"\bSimplicius\b",
    "Themistius": r"\bThemistius\b", "Alexander of Aphrodisias": r"\bAlexander\b", "Theophrastus": r"\bTheophrastus\b", "Ammonius": r"\bAmmonius\b",
    "Zoroaster": r"\bZoroaster\b", "Hermes Trismegistus": r"\bHermes\b|\bTrismegist|\bMercury\b", "Orpheus": r"\bOrph(eus|ic)\b", "Pythagoras": r"\bPythagor",
    "Plato": r"\bPlato\b", "Aristotle": r"\bAristot", "Joachim of Fiore": r"\bJoachim\b", "Jean Cabrol": r"\bCabrol\b|\bCapreolus\b", "Jean Quidort": r"\bQuidort\b|\bJohn of Paris\b",
    "Peter Lombard": r"\bLombard\b|\bSentences\b", "Ockham": r"\bOckham\b", "Robert Holcot": r"\bHolcot\b", "Pierre d'Ailly": r"\bAilly\b", "Guido Terrena": r"\bTerrena\b",
    "Godfrey of Fontaines": r"\bGodfrey\b", "Durandus": r"\bDurand", "Reginald Pecock": r"\bPecock\b", "Nicholas of Cusa": r"\bCusa", "Ramon Llull": r"\bLlull\b|\bLull\b",
    "Bessarion": r"\bBessarion\b", "Benivieni": r"\bBenivieni\b", "Gianfrancesco Pico": r"\bGianfrancesco\b", "Origen": r"\bOrigen\b", "Augustine": r"\bAugustin",
    "Dionysius the Areopagite": r"\bDionysius\b|\bAreopagit", "Kristeller": r"\bKristeller\b", "Garin": r"\bGarin\b", "Scholem": r"\bScholem\b", "Idel": r"\bIdel\b",
    "Yates": r"\bYates\b", "Cassirer": r"\bCassirer\b", "Burckhardt": r"\bBurckhardt\b", "Di Napoli": r"\bDi Napoli\b", "Dulles": r"\bDulles\b",
    # concepts
    "unity of the intellect": r"unity of (the )?intellect|unitatem intellectus", "agent intellect": r"agent intellect|intellectus agens|active intellect",
    "supposit / assumption": r"\bsupposit", "Eucharist": r"\bEucharist|\btransubstant|\bimpanat", "Incarnation": r"\bIncarnation\b",
    "sefirot": r"\bsefir|\bsephir", "Metatron": r"\bMetatron\b", "gematria": r"\bgematria\b", "divine names": r"divine name|nomina dei|seventy-two",
    "natural magic": r"natural magic|magia naturalis", "theurgy": r"\btheurg", "emanation": r"\bemanat", "Book of Causes": r"Liber de causis|Book of Causes",
    "Orphic hymns": r"Orphic hymn", "Chaldean Oracles": r"Chaldean Oracle", "astrology": r"\bastrolog", "prophecy": r"\bprophe", "beatitude / happiness": r"\bbeatitud|\bfelicit|\bhappiness",
    "formal numbers": r"formal number|formal arithmetic|numeri formales", "haecceity": r"\bhaecceit", "essence and existence": r"essence and existence|esse et essentia|actus essendi",
    "condemnation / trial": r"\bcondemn|\bcommission\b|\bheres|\bheretic|\bApolog",
}
GAZ = {k: re.compile(v, re.I) for k, v in GAZETTEER.items()}


def read(path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def slug(tid):
    if ">" in tid:
        sec, n = tid.split(">"); return f"own_{sec}_{int(n):03d}"
    sec, n = tid.split("."); return f"hist_{int(sec):02d}_{int(n):03d}"


def excerpt(lines, ln, max_words=NOTE_WORDS):
    out, k = [], ln - 1
    while k < len(lines) and lines[k].strip() and not lines[k].startswith("## Page") and (k == ln - 1 or not re.match(r"^\s*\d", lines[k])):
        out.append(lines[k].strip()); k += 1
    txt = re.sub(r"\s+", " ", " ".join(out))
    ws = txt.split(" ")
    return " ".join(ws[:max_words]) + (" [...]" if len(ws) > max_words else "")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    inv = json.load(io.open(os.path.join(INV, "theses.json"), encoding="utf-8"))["theses"]
    by_id = {t["thesis_id"]: t for t in inv}
    reg = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
    cond = {c["farmer_id"].split(" ")[0]: c for c in json.load(io.open(os.path.join(INV, "condemned_thirteen.json"), encoding="utf-8"))["theses"]}
    stats = json.load(io.open(os.path.join(ONT, "stats.json"), encoding="utf-8"))["theses"]
    xr = json.load(io.open(os.path.join(ONT, "connections", "farmer_crossrefs.json"), encoding="utf-8"))["crossrefs"]
    farmer_key = next(k for k, w in reg.items() if w.get("role") == "edition_farmer")
    F = read(reg[farmer_key]["path"])
    os.makedirs(PK, exist_ok=True)
    agg, index_rows = [], []
    for t in inv:
        tid = t["thesis_id"]
        m = json.load(io.open(os.path.join(ONT, "mentions", "by_thesis", slug(tid) + ".json"), encoding="utf-8"))
        st = stats[tid]
        notes = [(ln, excerpt(F, ln)) for ln in t["farmer_note_lines"]]
        # gazetteer over Farmer notes + mention contexts
        bag = " ".join(x for _, x in notes) + " " + " ".join(mm["context"] for mm in m["mentions"])
        ents = Counter()
        for name, rx in GAZ.items():
            c = len(rx.findall(bag))
            if c:
                ents[name] = c
        n_works = st["n_works"]
        is_cond = tid in cond
        tier = "A" if is_cond or n_works >= 3 else "B" if n_works >= 1 else "C" if (notes or xr.get(tid)) else "D"
        agg.append({"thesis_id": tid, "section": t["section"], "section_name": t["section_name"], "latin": t["latin"],
                    "farmer_latin_line": t["latin_line"], "condemned": is_cond, "q": cond[tid]["q"] if is_cond else None,
                    "n_works": n_works, "n_mentions": st["n_mentions"], "works": st["works"], "by_method": st["by_method"],
                    "farmer_crossrefs": xr.get(tid, []), "n_farmer_notes": len(notes), "entities": ents.most_common(12),
                    "suggested_tier": tier, "packet": f"research-packets/{slug(tid)}.md"})
        index_rows.append((tid, tier, n_works, st["n_mentions"], len(xr.get(tid, [])), is_cond))
        # packet
        L = [f"# Research packet: thesis {tid} ({t['section_name']})", "",
             f"Suggested tier: **{tier}** (condemned: {'Q' + str(cond[tid]['q']) if is_cond else 'no'}; scholarly works citing it: {n_works}; mention records: {st['n_mentions']}; Farmer cross-references: {len(xr.get(tid, []))})", "",
             "Locators are `work-key:line` into the files named in `data/corpus/registry.json`. Nothing here may be asserted in an entry without its locator. Farmer's English translation is copyright: its line is given so a VERIFIER can check a new translation's sense against it; it is not to be copied. In the OCR of Farmer's notes the `>` of own-opinion ids is printed as a digit: `4213` = 4>13, `422` = 4>2, `11250` = 11>50; historical ids keep their form (`7.2`).", "",
             "## Text", "", f"**Latin (Farmer 1998, {farmer_key}:{t['latin_line']}):** {t['latin']}", ""]
        if t.get("apparatus_1486"):
            L += ["**1486 apparatus (Farmer):** " + "; ".join(f"{a['text']} ({farmer_key}:{a['line']})" for a in t["apparatus_1486"]), ""]
        L += [f"**Farmer's English:** {farmer_key}:{t['farmer_english_line']}" + (f" (cumulative thesis number {t['cumulative_number']})" if t.get("cumulative_number") else ""), ""]
        if is_cond:
            c = cond[tid]
            L += ["## Condemned thesis", "", f"Q{c['q']} in Copenhaver's numbering: {c['topic']}. Audit note: {c['audit_result']}. See `data/inventory/condemned_thirteen.json` for the verdict formulae collected by A2.", ""]
        L += ["## Farmer's notes (excerpts to paraphrase, not reproduce)", ""]
        L += [f"- {farmer_key}:{ln}: {x}" for ln, x in notes] or ["- (Farmer has no note on this thesis.)"]
        L += ["", "## Farmer's cross-references (his 'Cf.' network; Latin is public domain)", ""]
        L += [f"- **{r}** ({by_id[r]['section_name']}, {farmer_key}:{by_id[r]['latin_line']}): {by_id[r]['latin'][:220]}" for r in xr.get(tid, []) if r in by_id] or ["- (none)"]
        L += ["", f"## Scholar mentions ({st['n_mentions']} records in {n_works} works)", ""]
        byw = defaultdict(list)
        for mm in m["mentions"]:
            byw[mm["work"]].append(mm)
        for wk in sorted(byw, key=lambda k: (k == farmer_key, k)):
            w = reg.get(wk, {})
            L += [f"### {wk}: {w.get('author', '?')}, *{w.get('title', '?')}* ({w.get('year', '?')})", ""]
            for mm in sorted(byw[wk], key=lambda z: z["line"]):
                res = "" if mm.get("resolved", True) else " [UNRESOLVED: could be 28.n or 11>n]"
                L += [f"- `{wk}:{mm['line']}` ({mm['method']}; evidence: {', '.join(mm['evidence'])}){res}", f"  > {mm['context']}", ""]
        if not byw:
            L += ["(No scholar in the corpus cites or quotes this thesis by a detectable method. Search the corpus by topic before writing; if nothing is found, the entry says so.)", ""]
        L += ["## Persons and concepts named in the material above (gazetteer counts)", "",
              ", ".join(f"{k} ({v})" for k, v in ents.most_common(20)) or "(none)", "",
              "## WRITER instructions", "",
              "Fields (docs/EDITORIAL_STANDARD.md s5): translation (original, from the Latin), translation_note, attribution and pico_stance, sources, doctrine, context, reception, historiography, connections. Depth by tier. Every factual sentence ends in a locator from this packet or from a source you opened yourself (record file and line). Where the packet is silent, write 'not established by the sources consulted'. Do not name a scholar, title, page or date that is not in a source you read. Output: `entries/" + slug(tid) + ".draft.json`.", ""]
        with io.open(os.path.join(PK, slug(tid) + ".md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
    with io.open(os.path.join(ONT, "theses.json"), "w", encoding="utf-8") as fh:
        json.dump({"_note": "Per-thesis aggregate from inventory + harvested mentions. suggested_tier: A condemned or >=3 works; B >=1 work; C Farmer note/crossref only; D nothing beyond the Latin.",
                   "theses": agg}, fh, indent=1, ensure_ascii=False)
    tiers = Counter(r[1] for r in index_rows)
    md = ["# Research packets index", "", f"Generated by scripts/build_dossiers.py. Tiers: A {tiers['A']}, B {tiers['B']}, C {tiers['C']}, D {tiers['D']}.", "",
          "| thesis | tier | works | mentions | crossrefs | condemned | packet |", "|---|---|---|---|---|---|---|"]
    for tid, tier, nw, nm, nx, ic in index_rows:
        md.append(f"| {tid} | {tier} | {nw} | {nm} | {nx} | {'Q' + str(cond[tid]['q']) if ic else ''} | [{slug(tid)}]({slug(tid)}.md) |")
    with io.open(os.path.join(PK, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    # compact translation sheets, one per block, for TRANSLATOR agents (Latin, apparatus, Farmer's English line, first note words)
    BLOCKS = [("T01_latins_1-6", ["1", "2", "3", "4", "5", "6"]), ("T02_arabs_7-14", ["7", "8", "9", "10", "11", "12", "13", "14"]),
              ("T03_greeks_platonists_15-24", ["15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]),
              ("T04_ancients_25-28", ["25", "26", "27", "28"]), ("T05_own_1-2", ["1>", "2>"]), ("T06_own_3-4", ["3>", "4>"]),
              ("T07_own_5-6", ["5>", "6>"]), ("T08_own_7-7a", ["7>", "7a>"]), ("T09_own_8-10", ["8>", "9>", "10>"]), ("T10_own_11", ["11>"])]
    os.makedirs(os.path.join(PK, "translation-sheets"), exist_ok=True)
    tier_of = {a["thesis_id"]: a["suggested_tier"] for a in agg}
    for name, secs in BLOCKS:
        rows = [t for t in inv if t["section"] in secs]
        L = [f"# Translation sheet {name}", "", f"{len(rows)} theses. For each: write an original English translation from the Latin; check its sense against Farmer's English at the line given (do not copy it); note any crux. Output one JSON object per thesis as specified in docs/ENTRY_FORMAT.md (tier-D fields only unless the thesis is yours to write in full). Tier A theses are marked; they belong to a WRITER, not to this sheet.", ""]
        for t in rows:
            L += [f"## {t['thesis_id']} ({t['section_name']}; tier {tier_of[t['thesis_id']]}{'; TIER A, SKIP' if tier_of[t['thesis_id']] == 'A' else ''})",
                  f"- Latin ({farmer_key}:{t['latin_line']}): {t['latin']}"]
            if t.get("apparatus_1486"):
                L.append("- 1486/1487 apparatus: " + "; ".join(a["text"] for a in t["apparatus_1486"]))
            L.append(f"- Farmer's English: {farmer_key}:{t['farmer_english_line']}")
            if t["farmer_note_lines"]:
                L.append(f"- Farmer's first note ({farmer_key}:{t['farmer_note_lines'][0]}): {excerpt(F, t['farmer_note_lines'][0], 40)}")
            L.append("")
        with io.open(os.path.join(PK, "translation-sheets", name + ".md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
    print("packets:", len(index_rows), dict(tiers), "| translation sheets:", len(BLOCKS))


if __name__ == "__main__":
    main()
