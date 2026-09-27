#!/usr/bin/env python3
"""entry_gate.py: mechanical gate for entry drafts (docs/ENTRY_FORMAT.md, rules 1-6). It certifies locators and
quotations against the source files; it does not judge prose. A failing draft goes back to its WRITER.

    python scripts/entry_gate.py [entries/*.draft.json]      (default: every *.draft.json under entries/)
Writes data/verification/entry_gate_report.json. Exit 1 if any draft fails.
"""
import difflib, glob, io, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
INV = {t["thesis_id"]: t for t in json.load(io.open(os.path.join(ROOT, "data", "inventory", "theses.json"), encoding="utf-8"))["theses"]}
LOC = re.compile(r"\b([a-z][a-z0-9_]{2,40}):(\d{2,6})(?:\s?-\s?(\d{2,6}))?\b")
COMMENTARY = ("doctrine", "context", "reception", "historiography", "commission_verdict")  # every sentence needs a locator
NOTES = ("attribution", "latin_note", "translation_note")  # short editorial notes: scholars named must be anchored, locators optional
PROSE = COMMENTARY + NOTES
SURNAMES = ["Copenhaver", "Farmer", "Wirszubski", "Edelheit", "Howlett", "Black", "Allen", "Akopyan", "Busi", "Dougherty", "Idel",
            "Scholem", "Kristeller", "Garin", "Yates", "Craven", "Di Napoli", "Kieszkowski", "Biondi", "Fornaciari", "Caroti",
            "Robiglio", "Mahoney", "Nardi", "Corazzol", "Ogren", "Novak", "Cassirer", "Walker", "Trinkaus", "Bausi", "Valcke"]
TIER_D_FIELDS = {"thesis_id", "tier", "latin", "latin_source", "latin_note", "translation", "translation_note", "translator",
                 "pico_stance", "attribution", "writer", "verifier", "verified_date", "not_established", "connections"}
_files, _lines = {}, {}


def lines_of(key):
    if key not in _files:
        p = REG[key]["path"]
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            _files[key] = fh.read().split("\n")
    return _files[key]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ı", "i").replace("v", "u").replace("j", "i").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9 ]+", " ", re.sub(r"-\s+", "", s)).split()


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def check(path):
    d = json.load(io.open(path, encoding="utf-8"))
    fails, notes = [], []
    tid = d.get("thesis_id")
    if tid not in INV:
        fails.append(f"unknown thesis_id {tid!r}")
        return {"file": path, "thesis_id": tid, "pass": False, "fails": fails, "notes": notes}
    # 1 locators
    n_loc = 0
    for s in strings({k: v for k, v in d.items() if k != "quotations"}):
        for m in LOC.finditer(s):
            key, a = m.group(1), int(m.group(2))
            if key not in REG:
                fails.append(f"locator work-key not in registry: {m.group(0)}"); continue
            n_loc += 1
            if a > len(lines_of(key)):
                fails.append(f"locator line beyond end of file: {m.group(0)} ({len(lines_of(key))} lines)")
    # 2 quotations
    for q in d.get("quotations", []) or []:
        key, ln, text = q.get("work"), q.get("line"), q.get("text", "")
        if key not in REG or not isinstance(ln, int):
            fails.append(f"quotation without a valid work/line: {q}"); continue
        L = lines_of(key)
        window = " ".join(L[max(0, ln - 4):ln + 3])
        qs, ws = norm(text), norm(window)
        if len(qs) < 3:
            fails.append(f"quotation too short to verify: {text!r}"); continue
        hay = " ".join(ws)
        found = " ".join(qs) in hay
        if not found:
            # tolerate one OCR-broken word: try the longest 60% span
            k = max(3, int(len(qs) * 0.6))
            found = any(" ".join(qs[i:i + k]) in hay for i in range(0, len(qs) - k + 1))
            if found:
                notes.append(f"quotation matched only in part (OCR?) at {key}:{ln}: {text[:60]!r}")
        if not found:
            fails.append(f"quotation not found within 3 lines of {key}:{ln}: {text[:80]!r}")
    # 3 translation vs Farmer's English
    fe = INV[tid].get("farmer_english_line")
    tr = d.get("translation") or ""
    if tr and fe:
        fk = next(k for k, w in REG.items() if w.get("role") == "edition_farmer")
        block = " ".join(lines_of(fk)[fe - 1:fe + 3])
        block = re.sub(r"^\s*\S+\s+", "", block, count=1)
        r = difflib.SequenceMatcher(None, " ".join(norm(tr)), " ".join(norm(block)[:len(norm(tr)) + 5]), autojunk=False).ratio()
        if r > 0.85:
            fails.append(f"translation is near-identical to Farmer's English (similarity {r:.2f}); write an original rendering")
        notes.append(f"translation/Farmer similarity {r:.2f}")
    # 4 commentary sentences carry locators
    for f in COMMENTARY:
        txt = d.get(f) or ""
        if not txt:
            continue
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", txt):
            if len(sent.split()) <= 4:
                continue
            if not LOC.search(sent):
                fails.append(f"{f}: sentence without locator: {sent[:90]!r}")
    # 5 scholar names must be anchored
    for f in PROSE:
        txt = d.get(f) or ""
        for sent in re.split(r"(?<=[.!?])\s+", txt):
            for sn in SURNAMES:
                if re.search(r"\b" + re.escape(sn) + r"\b", sent) and not LOC.search(sent):
                    fails.append(f"{f}: scholar named without locator in the sentence: {sn}: {sent[:80]!r}")
    # 6 tier D restriction
    if d.get("tier") == "D":
        extra = [k for k, v in d.items() if k not in TIER_D_FIELDS and v]
        if extra:
            fails.append(f"tier D entry carries fields it may not: {extra}")
    if n_loc == 0 and d.get("tier") != "D":
        fails.append("no locators at all in a tier A/B/C entry")
    return {"file": path, "thesis_id": tid, "pass": not fails, "fails": fails, "notes": notes, "locators": n_loc}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "entries", "*.draft.json")))
    results = [check(p) for p in paths]
    os.makedirs(os.path.join(ROOT, "data", "verification"), exist_ok=True)
    with io.open(os.path.join(ROOT, "data", "verification", "entry_gate_report.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    npass = sum(r["pass"] for r in results)
    for r in results:
        print(("PASS " if r["pass"] else "FAIL ") + f"{r['thesis_id']:8} {os.path.basename(r['file'])}")
        for f in r["fails"][:8]:
            print("      - " + f)
    print(f"{npass}/{len(results)} drafts pass the entry gate")
    return 0 if npass == len(results) and results else 1


if __name__ == "__main__":
    sys.exit(main())
