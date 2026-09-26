#!/usr/bin/env python3
"""harvest_mentions.py: HARVESTER. Find every place in the scholarly corpus where a specific thesis of the
900 is cited or quoted, and write mention records with file:line locators and context windows.

Deterministic; no model in the loop. Four detectors, each recorded as `method`:
  farmer_id        explicit Farmer-style ids in other scholars (4>13, 7.2 only when marked as a thesis)
  q_number         Copenhaver's Q1..Q13 (Pico on Trial), mapped through data/inventory/condemned_thirteen.json
  edelheit_chapter "thesis N [according to X]" in Edelheit 2022, resolved by chapter (one chapter per scholastic author)
  latin_quote      a verbatim quotation of the thesis's Latin: >=2 distinct normalised 4-word shingles
                   (u/v, i/j, OCR spacing and hyphenation normalised) within a 25-line window
  wirszubski_conclusio  "Conclusio <roman>" headings in Wirszubski, confirmed by a latin_quote hit nearby
Also: Farmer's own cross-references in his notes to each thesis (connections/farmer_crossrefs.json).

Inputs : data/inventory/theses.json, data/corpus/registry.json (built by build_corpus_registry.py)
Outputs: data/ontology/mentions/by_thesis/*.json, by_scholar/*.json, stats.json, MENTION_STATS.md,
         data/ontology/connections/farmer_crossrefs.json
Context windows are short research excerpts kept inside the repo for WRITER/VERIFIER use; the site never renders them.
"""
import io, json, os, re, sys, unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "data", "inventory")
ONT = os.path.join(ROOT, "data", "ontology")
WINDOW = 25
CTX_LINES = 3
CTX_CHARS = 700

EDELHEIT_CHAPTER_SECTIONS = {  # (first pdf page, last pdf page) -> historical section id
    (197, 224): "1", (225, 284): "2", (285, 298): "3", (299, 330): "4", (331, 344): "5", (345, 371): "6"}
NAME_TO_SECTION = [
    ("albert", "1"), ("thomas", "2"), ("aquinas", "2"), ("francis", "3"), ("mayronnes", "3"), ("meyronnes", "3"),
    ("scotus", "4"), ("henry", "5"), ("giles", "6"), ("averro", "7"), ("avicenna", "8"), ("farabi", "9"),
    ("isaac", "10"), ("abumaron", "11"), ("avenzoar", "11"), ("moses", "12"), ("maimonides", "12"),
    ("mohammed", "13"), ("avempace", "14"), ("theophrastus", "15"), ("ammonius", "16"), ("simplicius", "17"),
    ("alexander", "18"), ("themistius", "19"), ("plotinus", "20"), ("adeland", "21"), ("porphyry", "22"),
    ("iamblichus", "23"), ("proclus", "24"), ("pythagor", "25"), ("chaldean", "26"), ("hermes", "27"),
    ("mercur", "27"), ("cabalist", "28"), ("kabbalist", "28")]
ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}


def roman_to_int(s):
    s = s.lower(); total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN.get(ch, 0)
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def norm_word(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    w = w.replace("ı", "i").replace("ſ", "s").replace("v", "u").replace("j", "i").replace("ae", "e").replace("oe", "e")
    return re.sub(r"[^a-z]", "", w)


def tokenize_lines(lines):
    """Yield (norm_word, line_no); glue words hyphenated across a line break."""
    carry = None
    for i, ln in enumerate(lines, 1):
        ws = re.findall(r"[A-Za-zÀ-ɏıſ]+(?:-(?=\s*$))?", ln)
        for k, w in enumerate(ws):
            hy = w.endswith("-")
            w = w.rstrip("-")
            if carry:
                w, carry = carry[0] + w, None
                nw = norm_word(w)
                if nw:
                    yield nw, i
                continue
            if hy and k == len(ws) - 1:
                carry = (w, i)
                continue
            nw = norm_word(w)
            if nw:
                yield nw, i
    if carry:
        nw = norm_word(carry[0])
        if nw:
            yield nw, carry[1]


def shingles(words, k):
    return [tuple(words[i:i + k]) for i in range(len(words) - k + 1)]


def read(path):
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def context(lines, ln):
    a, b = max(0, ln - 1 - CTX_LINES), min(len(lines), ln + CTX_LINES)
    return re.sub(r"\s+", " ", " ".join(lines[a:b])).strip()[:CTX_CHARS]


def thesis_slug(tid):
    if ">" in tid:
        sec, n = tid.split(">")
        return f"own_{sec}_{int(n):03d}"
    sec, n = tid.split(".")
    return f"hist_{int(sec):02d}_{int(n):03d}"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    inv = json.load(io.open(os.path.join(INV, "theses.json"), encoding="utf-8"))["theses"]
    reg = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
    cond = json.load(io.open(os.path.join(INV, "condemned_thirteen.json"), encoding="utf-8"))["theses"]
    q_to_id = {f"Q{c['q']}": c["farmer_id"].split(" ")[0] for c in cond}
    by_id = {t["thesis_id"]: t for t in inv}
    sec_count = defaultdict(int)
    for t in inv:
        sec_count[t["section"]] = max(sec_count[t["section"]], t["n"])

    # shingle index: only shingles unique to one thesis
    sh_map, sh_owner = {}, defaultdict(set)
    th_words = {}
    for t in inv:
        ws = [norm_word(w) for w in re.findall(r"[A-Za-zÀ-ɏıſ]+", t["latin"])]
        ws = [w for w in ws if len(w) >= 2]
        th_words[t["thesis_id"]] = ws
        if len(ws) < 3:
            continue  # too short to identify by quotation; found by explicit id only
        k = 4 if len(ws) >= 6 else max(2, min(3, len(ws)))
        for s in shingles(ws, k):
            sh_owner[s].add(t["thesis_id"])
    for s, owners in sh_owner.items():
        if len(owners) == 1:
            sh_map[s] = next(iter(owners))
    need = {tid: (2 if len(ws) >= 6 else 1) for tid, ws in th_words.items()}
    print(f"theses {len(inv)}; unique shingles {len(sh_map)}")

    mentions = defaultdict(list)          # thesis_id -> [mention]
    crossrefs = defaultdict(set)          # thesis_id -> set(thesis_id)
    farmer_key = next(k for k, w in reg.items() if w.get("role") == "edition_farmer")

    for key, w in reg.items():
        if w.get("skip"):
            continue
        path = w["path"]
        if not os.path.exists(path):
            print("missing", key, path); continue
        lines = read(path)
        n_hits = 0

        # --- latin_quote: stream shingles of 2,3,4 words
        toks = list(tokenize_lines(lines))
        words = [x[0] for x in toks]
        hits = defaultdict(list)  # thesis -> [(line, shingle)]
        for k in (2, 3, 4):
            for i in range(len(words) - k + 1):
                s = tuple(words[i:i + k])
                tid = sh_map.get(s)
                if tid:
                    hits[tid].append((toks[i][1], s))
        for tid, hs in hits.items():
            if key == farmer_key:
                # Farmer's own text: only record occurrences away from the thesis's own Latin/English lines
                own = {by_id[tid]["latin_line"], by_id[tid].get("farmer_english_line") or -1}
                hs = [(l, s) for l, s in hs if all(abs(l - o) > 6 for o in own)]
            hs.sort()
            i = 0
            while i < len(hs):
                j = i
                while j + 1 < len(hs) and hs[j + 1][0] - hs[i][0] <= WINDOW:
                    j += 1
                distinct = {s for _, s in hs[i:j + 1]}
                if len(distinct) >= need[tid]:
                    ln = hs[i][0]
                    mentions[tid].append({"work": key, "line": ln, "method": "latin_quote",
                                          "evidence": [" ".join(s) for s in list(distinct)[:4]],
                                          "context": context(lines, ln)})
                    n_hits += 1
                i = j + 1

        # --- farmer_id in other scholars (and Farmer's cross-references from his notes)
        if key != farmer_key:
            for i, ln in enumerate(lines, 1):
                for m in re.finditer(r"(?<![\d.>])(\d{1,2}a?)>(\d{1,3})(?:\s?[-–]\s?(\d{1,3}))?(?![\d>])", ln):
                    sec = m.group(1) + ">"
                    if sec not in sec_count:
                        continue
                    a, b = int(m.group(2)), int(m.group(3) or m.group(2))
                    if b < a or b - a > 12:
                        b = a
                    for n in range(a, b + 1):
                        tid = f"{sec}{n}"
                        if tid in by_id:
                            mentions[tid].append({"work": key, "line": i, "method": "farmer_id", "evidence": [m.group(0)],
                                                  "context": context(lines, i)}); n_hits += 1
                for m in re.finditer(r"\bthes(?:is|es)\s+(\d{1,2})\.(\d{1,3})\b", ln, re.I):
                    tid = f"{int(m.group(1))}.{int(m.group(2))}"
                    if tid in by_id:
                        mentions[tid].append({"work": key, "line": i, "method": "farmer_id", "evidence": [m.group(0)],
                                              "context": context(lines, i)}); n_hits += 1
        else:
            for t in inv:
                for nl in t["farmer_note_lines"]:
                    block = " ".join(lines[nl - 1:nl + 12])
                    block = block.split("\n## Page")[0]
                    for m in re.finditer(r"(?<![\d.>])(\d{1,2}a?)>(\d{1,3})(?:\s?[-–—]\s?(\d{1,3}))?(?![\d>])", block):
                        sec = m.group(1) + ">"; a, b = int(m.group(2)), int(m.group(3) or m.group(2))
                        if sec in sec_count and b >= a and b - a <= 12:
                            for n in range(a, b + 1):
                                if f"{sec}{n}" in by_id and f"{sec}{n}" != t["thesis_id"]:
                                    crossrefs[t["thesis_id"]].add(f"{sec}{n}")
                    for m in re.finditer(r"(?<![\d.>])(\d{1,2})\.(\d{1,3})(?:\s?[-–—]\s?(\d{1,3}))?(?![\d.])", block):
                        sec = m.group(1); a, b = int(m.group(2)), int(m.group(3) or m.group(2))
                        if sec in sec_count and b >= a and b - a <= 12:
                            for n in range(a, b + 1):
                                if f"{sec}.{n}" in by_id and f"{sec}.{n}" != t["thesis_id"]:
                                    crossrefs[t["thesis_id"]].add(f"{sec}.{n}")
                    # own-opinion ids whose '>' the OCR printed as '2' (4213 = 4>13); accepted only when unambiguous
                    for m in re.finditer(r"(?<![\d.>])(\d{3,5})(?![\d.>])", block):
                        s = m.group(1)
                        parses = []
                        for k in (1, 2):
                            if len(s) > k + 1 and s[k] == "2":
                                sec, n = s[:k] + ">", s[k + 1:]
                                if sec in sec_count and n.isdigit() and 1 <= int(n) <= sec_count[sec]:
                                    parses.append(f"{sec}{int(n)}")
                        if len(parses) == 1 and parses[0] != t["thesis_id"] and parses[0] in by_id:
                            crossrefs[t["thesis_id"]].add(parses[0])

        # --- q_number (Copenhaver 2022 only)
        if w.get("role") == "trial_copenhaver":
            for i, ln in enumerate(lines, 1):
                for m in re.finditer(r"\bQ(1[0-3]|[1-9])\b", ln):
                    tid = q_to_id.get("Q" + m.group(1))
                    if tid in by_id:
                        mentions[tid].append({"work": key, "line": i, "method": "q_number", "evidence": [m.group(0)],
                                              "context": context(lines, i)}); n_hits += 1

        # --- edelheit_chapter (Edelheit 2022 only)
        if w.get("role") == "scholastic_edelheit":
            page = 0
            for i, ln in enumerate(lines, 1):
                pm = re.match(r"^## Page (\d+)", ln)
                if pm:
                    page = int(pm.group(1)); continue
                for m in re.finditer(r"\bthes(?:is|es)\s+(\d{1,3})(?:\s*(?:,|and|to|–|-)\s*(\d{1,3}))?", ln, re.I):
                    tail = " ".join(lines[i - 1:i + 2])[m.start():m.start() + 220].lower()
                    sec = None
                    am = re.search(r"according to (the )?([a-zà-ÿ]+(?: (?:of|the|de) [a-zà-ÿ]+)?)", tail)
                    if am:
                        for frag, s in NAME_TO_SECTION:
                            if frag in am.group(2):
                                sec = s; break
                    if sec is None:
                        for (a, b), s in EDELHEIT_CHAPTER_SECTIONS.items():
                            if a <= page <= b:
                                sec = s; break
                    if sec is None:
                        continue
                    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
                    if b < a or b - a > 6:
                        b = a
                    for n in range(a, b + 1):
                        tid = f"{sec}.{n}"
                        if tid in by_id:
                            mentions[tid].append({"work": key, "line": i, "method": "edelheit_chapter", "evidence": [m.group(0)],
                                                  "context": context(lines, i)}); n_hits += 1

        # --- wirszubski_conclusio (confirmed by a latin_quote within 15 lines)
        if w.get("role") == "kabbalah_wirszubski":
            lq = defaultdict(list)
            for tid, ms in mentions.items():
                for mm in ms:
                    if mm["work"] == key and mm["method"] == "latin_quote":
                        lq[tid].append(mm["line"])
            for i, ln in enumerate(lines, 1):
                m = re.search(r"\bconclusio(?:nes)?\s+([xivlc]+)\b", ln, re.I)
                if not m:
                    continue
                n = roman_to_int(m.group(1))
                cands = [c for c in (f"28.{n}", f"11>{n}") if c in by_id]
                conf = [c for c in cands if any(abs(l - i) <= 15 for l in lq.get(c, []))]
                for c in (conf or cands):
                    mentions[c].append({"work": key, "line": i, "method": "wirszubski_conclusio",
                                        "evidence": [m.group(0)], "resolved": bool(conf), "context": context(lines, i)})
                    n_hits += 1
        print(f"{key:28} hits {n_hits}")

    # de-duplicate: same work, same method, lines within 3
    for tid, ms in mentions.items():
        ms.sort(key=lambda m: (m["work"], m["method"], m["line"]))
        out, last = [], None
        for m in ms:
            if last and last["work"] == m["work"] and last["method"] == m["method"] and m["line"] - last["line"] <= 3:
                continue
            out.append(m); last = m
        mentions[tid] = out

    os.makedirs(os.path.join(ONT, "mentions", "by_thesis"), exist_ok=True)
    os.makedirs(os.path.join(ONT, "mentions", "by_scholar"), exist_ok=True)
    os.makedirs(os.path.join(ONT, "connections"), exist_ok=True)
    by_work = defaultdict(list)
    stats = {"theses": {}, "works": {}, "_note": "Counts are of mention records (deduplicated within 3 lines); "
             "n_works counts distinct works other than Farmer's own edition."}
    for t in inv:
        tid = t["thesis_id"]
        ms = mentions.get(tid, [])
        with io.open(os.path.join(ONT, "mentions", "by_thesis", thesis_slug(tid) + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"thesis_id": tid, "latin": t["latin"], "farmer_latin_line": t["latin_line"], "mentions": ms,
                       "farmer_crossrefs": sorted(crossrefs.get(tid, []))}, fh, indent=1, ensure_ascii=False)
        works = {m["work"] for m in ms if m["work"] != farmer_key}
        meth = defaultdict(int)
        for m in ms:
            meth[m["method"]] += 1
        stats["theses"][tid] = {"n_mentions": len(ms), "n_works": len(works), "works": sorted(works),
                                "by_method": dict(meth), "n_crossrefs": len(crossrefs.get(tid, [])),
                                "condemned": tid in q_to_id.values()}
        for m in ms:
            by_work[m["work"]].append(dict(m, thesis_id=tid))
    for key, ms in by_work.items():
        with io.open(os.path.join(ONT, "mentions", "by_scholar", key + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"work": key, "meta": reg[key], "n_mentions": len(ms),
                       "n_theses": len({m["thesis_id"] for m in ms}), "mentions": sorted(ms, key=lambda m: m["line"])},
                      fh, indent=1, ensure_ascii=False)
        stats["works"][key] = {"n_mentions": len(ms), "n_theses": len({m["thesis_id"] for m in ms})}
    with io.open(os.path.join(ONT, "connections", "farmer_crossrefs.json"), "w", encoding="utf-8") as fh:
        json.dump({"_note": "Theses that Farmer's note on the key thesis refers to (his 'Cf.' network); undirected use is fine.",
                   "crossrefs": {k: sorted(v) for k, v in crossrefs.items()}}, fh, indent=1, ensure_ascii=False)
    with io.open(os.path.join(ONT, "stats.json"), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=1, ensure_ascii=False)

    # Markdown summary
    th = stats["theses"]
    n0 = sum(1 for v in th.values() if v["n_works"] == 0)
    n1 = sum(1 for v in th.values() if v["n_works"] == 1)
    n2 = sum(1 for v in th.values() if v["n_works"] >= 2)
    n3 = sum(1 for v in th.values() if v["n_works"] >= 3)
    top = sorted(th.items(), key=lambda kv: (-kv[1]["n_works"], -kv[1]["n_mentions"]))[:40]
    sec_rows = defaultdict(lambda: [0, 0, 0])
    for t in inv:
        v = th[t["thesis_id"]]; r = sec_rows[t["section"]]
        r[0] += 1; r[1] += v["n_works"] > 0; r[2] += v["n_mentions"]
    md = ["# Mention statistics (generated by scripts/harvest_mentions.py)", "",
          f"Theses: {len(th)}. Discussed by no scholar outside Farmer: **{n0}**; by exactly one: {n1}; by two or more: {n2}; by three or more: {n3}.",
          "", "## Coverage by section", "", "| section | theses | with any scholar mention | mention records |", "|---|---|---|---|"]
    for t in inv:
        pass
    seen = set()
    for t in inv:
        s = t["section"]
        if s in seen:
            continue
        seen.add(s); r = sec_rows[s]
        md.append(f"| {s} {t['section_name']} | {r[0]} | {r[1]} | {r[2]} |")
    md += ["", "## Most-discussed theses", "", "| thesis | works | mentions | condemned | works |", "|---|---|---|---|---|"]
    for tid, v in top:
        md.append(f"| {tid} | {v['n_works']} | {v['n_mentions']} | {'yes' if v['condemned'] else ''} | {', '.join(v['works'])} |")
    md += ["", "## Works", "", "| work | mention records | distinct theses |", "|---|---|---|"]
    for key, v in sorted(stats["works"].items(), key=lambda kv: -kv[1]["n_theses"]):
        md.append(f"| {key} | {v['n_mentions']} | {v['n_theses']} |")
    with io.open(os.path.join(ONT, "MENTION_STATS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print(f"no-scholar {n0}; one {n1}; two+ {n2}; three+ {n3}; crossref theses {len(crossrefs)}")


if __name__ == "__main__":
    main()
