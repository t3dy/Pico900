#!/usr/bin/env python3
"""entry_gate_local.py: the subset of scripts/entry_gate.py's checks that do NOT require opening
the OCR corpus files under E:\\pdf\\... (which don't exist in this sandbox). Skips: quotation
verbatim-in-corpus check (rule 2), translation-vs-Farmer similarity (rule 3), and locator
line-bounds check (part of rule 1). Keeps: locator format/registry-key check, prose-sentence-
needs-locator check, scholar-name-anchored check, tier D restriction. A draft that passes this
still needs the real scripts/entry_gate.py run locally (with corpus access) before promotion.

    python scripts/entry_gate_local.py [entries/*.draft.json]
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
INV = {t["thesis_id"]: t for t in json.load(io.open(os.path.join(ROOT, "data", "inventory", "theses.json"), encoding="utf-8"))["theses"]}
LOC = re.compile(r"\b([a-z][a-z0-9_]{2,40}):(\d{2,6})(?:\s?-\s?(\d{2,6}))?\b")
PROSE = ("doctrine", "context", "reception", "historiography", "attribution", "latin_note", "translation_note", "commission_verdict")
SURNAMES = ["Copenhaver", "Farmer", "Wirszubski", "Edelheit", "Howlett", "Black", "Allen", "Akopyan", "Busi", "Dougherty", "Idel",
            "Scholem", "Kristeller", "Garin", "Yates", "Craven", "Di Napoli", "Kieszkowski", "Biondi", "Fornaciari", "Caroti",
            "Robiglio", "Mahoney", "Nardi", "Corazzol", "Ogren", "Novak", "Cassirer", "Walker", "Trinkaus", "Bausi", "Valcke"]
TIER_D_FIELDS = {"thesis_id", "tier", "latin", "latin_source", "latin_note", "translation", "translation_note", "translator",
                 "pico_stance", "attribution", "writer", "verifier", "verified_date", "not_established", "connections"}


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
    n_loc = 0
    for s in strings({k: v for k, v in d.items() if k != "quotations"}):
        for m in LOC.finditer(s):
            key = m.group(1)
            if key not in REG:
                fails.append(f"locator work-key not in registry: {m.group(0)}"); continue
            n_loc += 1
    for q in d.get("quotations", []) or []:
        key, ln, text = q.get("work"), q.get("line"), q.get("text", "")
        if key not in REG or not isinstance(ln, int):
            fails.append(f"quotation without a valid work/line: {q}"); continue
        if len(re.findall(r"\w+", text or "")) < 3:
            fails.append(f"quotation too short to verify: {text!r}")
        notes.append(f"quotation at {key}:{ln} NOT corpus-verified in this sandbox (no corpus access)")
    if d.get("translation"):
        notes.append("translation/Farmer similarity NOT checked in this sandbox (no corpus access) - run real entry_gate.py locally before promotion")
    for f in PROSE:
        txt = d.get(f) or ""
        if not txt:
            continue
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", txt):
            if len(sent.split()) <= 4:
                continue
            if not LOC.search(sent):
                fails.append(f"{f}: sentence without locator: {sent[:90]!r}")
    for f in PROSE:
        txt = d.get(f) or ""
        for sent in re.split(r"(?<=[.!?])\s+", txt):
            for sn in SURNAMES:
                if re.search(r"\b" + re.escape(sn) + r"\b", sent) and not LOC.search(sent):
                    fails.append(f"{f}: scholar named without locator in the sentence: {sn}: {sent[:80]!r}")
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
    npass = sum(r["pass"] for r in results)
    for r in results:
        print(("PASS " if r["pass"] else "FAIL ") + f"{r['thesis_id']:8} {os.path.basename(r['file'])}")
        for f in r["fails"][:8]:
            print("      - " + f)
    print(f"{npass}/{len(results)} drafts pass the LOCAL (partial) gate; full corpus verification still required locally")
    return 0 if npass == len(results) and results else 1


if __name__ == "__main__":
    sys.exit(main())
