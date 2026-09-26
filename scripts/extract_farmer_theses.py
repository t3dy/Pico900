#!/usr/bin/env python3
"""extract_farmer_theses.py: RESEARCHER phase 0. Derive the inventory of the 900 theses from Farmer's
edition (Markdown OCR) and write data/inventory/theses.json + data/inventory/extract_report.json.

Farmer prints, per section: a Latin page, then the facing English page, with notes at the foot; the OCR
interleaves them. Every thesis id therefore occurs up to four times: Latin, an optional `1486` apparatus
line, English (Farmer's translation, in copyright: only its line number is stored), and notes.

OCR damage to the id token is the main hazard: the `>` of own-opinion ids becomes a digit (`4>1` -> `421.`),
a section digit is misread (`3>62` -> `5762.`), the thesis digits themselves are misread (`3>63` -> `3765.`),
the period becomes a comma or colon, `/` stands for a digit. Resolution therefore works inside the known
line span of each section and distinguishes a *clean* token (separator preserved: `4>13`, `7.2`, `9-8`),
which is trusted even across a one- or two-step gap, from a *garbled* token, for which the sequence is
trusted instead: a Latin line within ten lines of the previous Latin thesis is the next thesis. Every
inference of that kind is logged in extract_report.json for a VERIFIER.

Gate G0: the Latin count per section equals Farmer's printed count and the total is 900.
"""
import io, json, os, re, sys

FARMER = r"E:\pdf\renaissance magic\Pico\Markdown\Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_in_the_West__Pico_s_900_Theses_The_Evo_pdf_c99b971b.md"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
END_LINE = 28040  # colophon "Impressum Romae ..."

# (id, name, start line of the Latin section heading, printed count). 7>/7a> are split as Farmer prints them.
SECTIONS = [
    ("1", "Albert the Great", 10920, 16), ("2", "Thomas Aquinas", 11238, 45), ("3", "Francis of Meyronnes", 11969, 8),
    ("4", "Scotus", 12135, 22), ("5", "Henry of Ghent", 12477, 13), ("6", "Giles of Rome", 12666, 11),
    ("7", "Averroes", 12859, 41), ("8", "Avicenna", 13561, 12), ("9", "al-Farabi", 13767, 11),
    ("10", "Isaac of Narbonne", 13964, 4), ("11", "Abumaron", 14049, 4), ("12", "Moses of Egypt", 14134, 3),
    ("13", "Mohammed of Toledo", 14209, 5), ("14", "Avempace", 14297, 2), ("15", "Theophrastus", 14362, 4),
    ("16", "Ammonius", 14469, 3), ("17", "Simplicius", 14541, 9), ("18", "Alexander of Aphrodisias", 14710, 8),
    ("19", "Themistius", 14876, 5), ("20", "Plotinus", 14987, 15), ("21", "Adeland the Arab", 15274, 8),
    ("22", "Porphyry", 15433, 12), ("23", "Iamblichus", 15632, 9), ("24", "Proclus", 15838, 55),
    ("25", "Pythagorean mathematics", 16886, 14), ("26", "Chaldean theologians", 17119, 6),
    ("27", "Mercury Trismegistus", 17236, 10), ("28", "Hebrew Cabalists", 17420, 47),
    ("1>", "Paradoxical reconciliations", 18494, 17), ("2>", "Philosophical, against the common view", 18858, 80),
    ("3>", "Paradoxical, new doctrines", 20258, 71), ("4>", "Theological, against the common mode", 21432, 29),
    ("5>", "Plato", 22132, 62), ("6>", "Book of Causes", 23348, 10), ("7>", "Mathematics", 23606, 11),
    ("7a>", "Questions to be answered by numbers", 23812, 74), ("8>", "Zoroaster and Chaldeans", 24715, 15),
    ("9>", "Magic", 25106, 26), ("10>", "Orphic Hymns", 25560, 31),
    ("11>", "Cabalistic, confirming the Christian religion", 26227, 72),
]
assert sum(c for _, _, _, c in SECTIONS) == 900

HEAD = re.compile(r"^\s*(?P<tok>\d[\d a>/.,:\-\u2013]{0,8}?)[.,:]\s+(?P<text>\S.*)$")
RANGE = re.compile(r"^\s*(\d{1,2}a?)[.>](\d{1,3})\s?[-\u2013\u2014]\s?(\d{1,3})\.\s+(\S.*)$")
PAGE = re.compile(r"^## Page \d+")
ENG_STRONG = set("the of and that which are to this with from by there be as it its or one any if so but what who "
                 "all than can does should whether when how their not was were has have".split())
ENG_WEAK = {"is": 0.6, "his": 0.5, "a": 0.3}
LAT_WORDS = set("est et non sit sunt esse ut ad cum quod qui quae sed nec uel ab ex si omnis nihil deus dei anima "
                "intellectus quam ipsa ipse ipsum hoc illud tamen ita aut atque enim potest possibile secundum natura "
                "naturam rerum res dico dicitur habet habere unum ens omnia nulla nullus prima primum idem esset posse "
                "diuina uirtus corpus forma materia intelligere intelligit utrum vtrum sicut propter super animam suam "
                "quo qua quia ergo ideo omne omnes per de in sint an quomodo quid quis cur num sic tam iam uero vero "
                "autem igitur nisi sine inter contra apud ante post sub pro".split())
LAT_SUFFIX = (("ibus", 1), ("orum", 1), ("arum", 1), ("ntur", 1), ("tur", 1), ("que", 0.8), ("um", 1), ("us", 1), ("ae", 1),
              ("em", 0.6), ("am", 0.5), ("os", 0.5), ("is", 0.5), ("it", 0.3))
ENG_SUFFIX = (("tion", 1), ("ness", 1), ("ing", 1), ("ed", 1), ("ly", 1), ("ity", 1), ("ies", 0.6), ("s", 0.1))
NOTE_MARK = re.compile(r"\bCf\.|\bcf\.|\bSee\b|\bsee\b|\bpp?\.\s?\d|\b[Nn]ote\b|\bSeries\b|\bstarts at\b|\babove\b|\bbelow\b|"
                       r"\(\d{4}[:)]|\b(Farmer|Kristeller|Garin|Wirszubski|Copenhaver|Allen|Nardi|Mahoney|Scholem|Opera)\b|\s=\s|"
                       r"\b[dqn]\.\s?\d|\bfol\.|\bibid|\bch\.\s?\d|\bbk\.|\bSentences\b")
NOTE_LIGHT = re.compile(r"\bCf\.|\bcf\.|\bSee\b|\(\d{4}[:)]|\bnote\b|\bpp?\.\s?\d|\s=\s|\bibid|\bfol\.")
APPARATUS = re.compile(r"^\s*1[45]\d\d\b|^\s*\d{4}\b")


def words(t):
    return re.findall(r"[a-zà-ÿ]+", t.lower())


def scores(t):
    ws = words(t)
    eng = lat = 0.0
    for w in ws:
        if w in ENG_STRONG:
            eng += 1
        elif w in ENG_WEAK:
            eng += ENG_WEAK[w]
        else:
            for suf, v in ENG_SUFFIX:
                if len(w) > len(suf) + 2 and w.endswith(suf):
                    eng += v; break
        if w in LAT_WORDS:
            lat += 1
        else:
            for suf, v in LAT_SUFFIX:
                if len(w) > len(suf) + 1 and w.endswith(suf):
                    lat += v; break
    return eng, lat, len(ws)


def is_latin(t):
    """Latin outscores English on function words and morphology (OCR soup with no evidence either way counts as Latin)."""
    eng, lat, n = scores(t)
    return eng < 1 if lat == 0 else lat >= eng


def has_latin_evidence(t):
    eng, lat, n = scores(t)
    return lat > 0 and lat > eng


def join_block(lines, i):
    """Join a thesis line with its continuation lines up to a blank line or the next heading/page marker."""
    out, k = [lines[i]], i + 1
    while k < len(lines):
        ln = lines[k]
        if not ln.strip() or PAGE.match(ln) or HEAD.match(ln) or RANGE.match(ln):
            break
        out.append(ln)
        k += 1
    txt = ""
    for ln in out:
        s = ln.strip()
        if txt.endswith("-") and not txt.endswith(" -"):
            txt = txt[:-1] + s
        else:
            txt = (txt + " " + s).strip()
    return re.sub(r"\s+", " ", txt), k


def token_info(tok, own):
    """Return (clean, section_digits_as_read, candidate_numbers)."""
    t = tok.replace(" ", "")
    if own:
        if re.search(r"[>\-\u2013]", t):
            tail = re.split(r"[>\-\u2013]", t)[-1]
            return True, re.split(r"[>\-\u2013]", t)[0], ([int(tail)] if tail.isdigit() else [])
        digits = re.sub(r"[^0-9]", "", t)
        return False, None, [int(digits[k:]) for k in range(1, len(digits)) if digits[k:]]
    groups = re.findall(r"\d+", t)
    if len(groups) >= 2 and re.search(r"[./,]", t):
        return True, groups[0], [int(groups[-1])]
    if len(groups) == 1:
        return False, None, [int(groups[0])]
    return False, None, [int(g) for g in groups]


def parse():
    with io.open(FARMER, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    theses, report = [], {"sections": [], "unresolved": [], "inferred": []}
    for si, (sid, name, start, printed) in enumerate(SECTIONS):
        end = SECTIONS[si + 1][2] if si + 1 < len(SECTIONS) else END_LINE
        own = sid.endswith(">")
        sec_digits = sid.rstrip(">")
        by_n = {}
        latin_next, eng_next, last_latin_line = 1, 1, None
        i = start
        while i < end:
            ln = lines[i]
            mr = RANGE.match(ln)
            if mr and mr.group(1) == sec_digits:
                a, b = int(mr.group(2)), int(mr.group(3))
                if 1 <= a < b <= printed + 2:
                    text, k = join_block(lines, i)
                    for x in range(a, b + 1):
                        by_n.setdefault(x, {}).setdefault("note_lines", []).append(i + 1)
                    i = k
                    continue
            m = HEAD.match(ln)
            if not m:
                i += 1
                continue
            clean, sec_read, cands = token_info(m.group("tok"), own)
            text, k = join_block(lines, i)
            tok_rx = r"\s*".join(map(re.escape, m.group("tok").split()))
            body = re.sub(r"^" + tok_rx + r"\s*[.,:]\s*", "", text, count=1)
            folio = re.findall(r"<\d+[rv]/\d+[rv]>", body)
            body = re.sub(r"\s*<\d+[rv]/\d+[rv]>", "", body).strip()
            # strip a leading stray number from the body ("74:   62. Vtrum ...")
            body = re.sub(r"^\d{1,3}\.\s+", "", body)
            latin_like = is_latin(body)
            apparatus = bool(APPARATUS.match(body)) or bool(
                re.search(r"\b148[67]\b|Emendationes|\bcorrige\b", body) and (" |" in body or len(body) < 100))
            n = None
            if apparatus:
                n = next((c for c in cands if c in by_n), None)
                if n is None:
                    report.setdefault("apparatus_unplaced", []).append({"section": sid, "line": i + 1, "token": m.group("tok"), "text": body[:80]})
                    i = k
                    continue
            elif latin_next in cands and latin_like and latin_next <= printed and (has_latin_evidence(body) or not NOTE_MARK.search(body)):
                n = latin_next
            elif not latin_like and not NOTE_LIGHT.search(body) and any(
                    c in by_n and "latin_line" in by_n[c] and "english_line" not in by_n[c] for c in cands):
                n = next(c for c in cands if c in by_n and "latin_line" in by_n[c] and "english_line" not in by_n[c])
                eng_next = n
            elif has_latin_evidence(body) and not NOTE_MARK.search(body) and " |" not in body and latin_next <= printed and last_latin_line is not None and (i + 1 - last_latin_line) <= 10:
                # in the Latin block: sequence beats a damaged token
                if clean and any(latin_next < c <= min(printed, latin_next + 2) for c in cands):
                    n = min(c for c in cands if latin_next < c <= min(printed, latin_next + 2))
                    report["inferred"].append({"section": sid, "line": i + 1, "assigned": n, "token": m.group("tok"), "why": f"clean token after gap; expected {latin_next}"})
                else:
                    n = latin_next
                    if latin_next not in cands:
                        report["inferred"].append({"section": sid, "line": i + 1, "assigned": n, "token": m.group("tok"), "why": "garbled token; assigned by sequence"})
            elif latin_like and latin_next <= printed and clean and (sec_read == sec_digits) and any(latin_next < c <= min(printed, latin_next + 2) for c in cands):
                n = min(c for c in cands if latin_next < c <= min(printed, latin_next + 2))
                report["inferred"].append({"section": sid, "line": i + 1, "assigned": n, "token": m.group("tok"), "why": f"clean token after gap; expected {latin_next}"})
            else:
                # a note or an unresolvable line
                nn = [c for c in cands if 1 <= c <= printed and c in by_n]
                if nn and not latin_like:
                    by_n.setdefault(nn[0], {}).setdefault("note_lines", []).append(i + 1)
                elif latin_like and cands:
                    report["unresolved"].append({"section": sid, "line": i + 1, "token": m.group("tok"), "text": body[:80]})
                i = k
                continue
            rec = by_n.setdefault(n, {})
            if apparatus:
                rec.setdefault("apparatus", []).append({"line": i + 1, "text": body})
            elif n == latin_next and "latin_line" not in rec and latin_like:
                rec.update(latin=body, latin_line=i + 1, folio=folio)
                latin_next, last_latin_line = n + 1, i + 1
            elif latin_like and "latin_line" not in rec and n > latin_next:
                rec.update(latin=body, latin_line=i + 1, folio=folio)
                latin_next, last_latin_line = n + 1, i + 1
            elif not latin_like and "english_line" not in rec and n >= eng_next and not NOTE_MARK.search(body):
                cum = re.search(r"\((\d{3})\)\s*$", body)
                rec.update(english_line=i + 1, english_words=len(words(body)))
                if cum:
                    rec["cumulative_number"] = int(cum.group(1))
                eng_next = n + 1
            else:
                rec.setdefault("note_lines", []).append(i + 1)
            i = k
        got = sorted(n for n, r in by_n.items() if "latin_line" in r)
        report["sections"].append({"section": sid, "name": name, "printed": printed, "latin_found": len(got),
                                   "missing": [n for n in range(1, printed + 1) if n not in got],
                                   "extra": [n for n in got if n > printed],
                                   "english_found": sum("english_line" in r for r in by_n.values())})
        for n in sorted(by_n):
            r = by_n[n]
            if "latin_line" not in r or n > printed:
                continue
            key = f"{sid}{n}" if own else f"{sid}.{n}"
            theses.append({"thesis_id": key, "section": sid, "section_name": name, "n": n,
                           "latin": r["latin"], "latin_line": r["latin_line"], "latin_source": "Farmer 1998 (OCR; collate)",
                           "apparatus_1486": r.get("apparatus", []), "folio_1486": r.get("folio", []),
                           "farmer_english_line": r.get("english_line"), "farmer_english_words": r.get("english_words"),
                           "farmer_note_lines": sorted(set(r.get("note_lines", []))), "cumulative_number": r.get("cumulative_number"),
                           "tier": "D", "pico_stance": "reports" if not own else "endorses"})
    return theses, report


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    theses, report = parse()
    out = os.path.join(ROOT, "data", "inventory")
    os.makedirs(out, exist_ok=True)
    with io.open(os.path.join(out, "theses.json"), "w", encoding="utf-8") as fh:
        json.dump({"_provenance": "Derived from Farmer 1998 OCR by scripts/extract_farmer_theses.py; latin_line etc. are "
                   "line numbers in that Markdown. Farmer's English is not stored (copyright); its line is. "
                   "Ids inferred from sequence are listed in extract_report.json['inferred'] and must be checked.",
                   "count": len(theses), "theses": theses}, fh, indent=1, ensure_ascii=False)
    with io.open(os.path.join(out, "extract_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    bad = 0
    cum_bad = [(t["thesis_id"], t["cumulative_number"], k + 1) for k, t in enumerate(theses)
               if t.get("cumulative_number") and t["cumulative_number"] != k + 1]
    report["cumulative_mismatches"] = cum_bad
    with io.open(os.path.join(out, "extract_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    for s in report["sections"]:
        flag = "" if s["latin_found"] == s["printed"] and not s["extra"] else "  <-- CHECK"
        bad += bool(flag)
        print(f"{s['section']:>4} {s['name'][:30]:30} printed {s['printed']:3} latin {s['latin_found']:3} english {s['english_found']:3}"
              f" missing {s['missing']} extra {s['extra']}{flag}")
    print(f"total latin theses: {len(theses)} (printed 900); unresolved: {len(report['unresolved'])}; inferred ids: {len(report['inferred'])}")
    n_cum = sum(1 for t in theses if t.get("cumulative_number"))
    print(f"cumulative numbers printed by Farmer: {n_cum}; mismatching the derived order: {len(cum_bad)} {cum_bad[:8]}")
    ok = len(theses) == 900 and bad == 0 and not cum_bad
    print("GATE G0", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
