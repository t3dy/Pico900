#!/usr/bin/env python3
"""integrity_gate.py: the truth check the schema validators never made.

Prior validators (validate_review.py, validate_phase_1_alpha.py) confirm that a field
EXISTS and has the right SHAPE. They cannot notice that 775 "translations" are five canned
sentences cycled per section, or that 283 "verified" citations are three quotations pasted
across 118 entries. This script grades every field of every entry by PROVENANCE, writes a
machine-readable coverage ledger, and refuses to pass content that only looks finished.

    python scripts/integrity_gate.py                   # report + write ledger and COVERAGE.md
    python scripts/integrity_gate.py --strict          # exit 1 if anything template-grade is renderable
    python scripts/integrity_gate.py --verify-quotes   # also search source Markdown for each quotation
    python scripts/integrity_gate.py --list-ready      # ids whose every public field is sourced

Grades (per field):
    misfiled     text in the wrong field (English in the Latin slot; Latin copied to English)
    quarantined  proven wrong by audit (data/quarantine.json); never rendered
    restricted   real text we may not publish (in-copyright translation)
    sourced      traceable: real text plus a locator (page, line, or edition reference)
    unverified   real-looking text, but no locator or not found in the source corpus
    template     generated filler: cycled sentence, boilerplate, or identical across entries
    placeholder  visibly empty ("TBD", "[CITATION TO BE FILLED]", "TO BE VERIFIED")
    missing      absent

Only `sourced` may be rendered as Pico's text or as a scholar's words. The build must show
everything else as an explicit "not yet edited" state, never as edition text.
"""
import argparse, collections, glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCL = os.path.join(ROOT, "data", "conclusions")
LEDGER = os.path.join(ROOT, "data", "coverage_ledger.json")
REPORT = os.path.join(ROOT, "COVERAGE.md")
SOURCES_MD = os.environ.get("PICO_SOURCES_MD", r"E:\pdf\renaissance magic\Pico\Markdown")

PLACEHOLDER = re.compile(r"TO BE (SOURCED|VERIFIED|FILLED)|TO_SOURCE|TO_TRANSLATE|NEEDS_TRANSLATION|\bTBD\b|CITATION TO BE|FROM CRITICAL EDITION|PAGE TO BE|pending", re.I)
TEMPLATE_SRC = re.compile(r"template|pending", re.I)
# Farmer's English (MRTS 167, (c) 1998) is in copyright; Pico's Latin is not. Never render it as ours.
RESTRICTED_SRC = re.compile(r"farmer", re.I)
BOILER_EXEG = re.compile(r"^Pico's conclusion on .+ within the .+ tradition\.?$")
REUSE_THRESHOLD = 3  # identical prose in more than this many entries is filler, not scholarship


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(CONCL, "*", "entry_*.json"))):
        with io.open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        d["_file"] = os.path.relpath(f, ROOT)
        rows.append(d)
    return rows


def section_of(d):
    # The `section` field is free text in older entries ("Secundum Avicennam"); the directory is canonical.
    return os.path.basename(os.path.dirname(d["_file"]))


def translation_of(d):
    t = d.get("english_translation")
    if isinstance(t, dict):
        return t.get("text") or "", t.get("source") or "", t.get("translator") or ""
    return t or "", d.get("translation_source") or "", ""


ENGLISH_HINT = re.compile(r"\b(?:the|and|of|is|that|which|are|with|not|from)\b", re.I)


def looks_english(t):
    """True when text reads as English (used to catch English filed in the Latin field)."""
    return len(ENGLISH_HINT.findall(t)) >= 2


def load_quarantine():
    p = os.path.join(ROOT, "data", "quarantine.json")
    if not os.path.exists(p):
        return set()
    with io.open(p, encoding="utf-8") as fh:
        return {(i["id"], i["field"]) for i in json.load(fh)["items"]}


def load_corpus():
    corpus = {}
    for f in glob.glob(os.path.join(SOURCES_MD, "*.md")):
        with io.open(f, encoding="utf-8", errors="ignore") as fh:
            corpus[os.path.basename(f)] = norm(fh.read())
    return corpus


def quote_status(q, corpus):
    """VERBATIM / PARTIAL / NOT_FOUND against the whole source corpus (ellipses split fragments)."""
    frags = [p for p in re.split(r"\.\.\.|…|\[[^\]]*\]", q) if len(norm(p)) >= 30]
    if not frags:
        return "TOO_SHORT"
    hits = [any(norm(p) in t for t in corpus.values()) for p in frags]
    return "VERBATIM" if all(hits) else "PARTIAL" if any(hits) else "NOT_FOUND"


def grade(rows, corpus):
    tr_count = collections.Counter(translation_of(d)[0].strip() for d in rows)
    ch_count = collections.Counter(d.get("charge") for d in rows)
    de_count = collections.Counter(d.get("defense") for d in rows)
    ex_count = collections.Counter(d.get("exegesis") for d in rows)
    q_count = collections.Counter(norm(c.get("quotation")) for d in rows for c in d.get("scholar_citations", []))
    quarantine = load_quarantine()
    out = []
    for d in rows:
        g = {}
        lat = d.get("latin_incipit") or ""
        g["latin"] = ("missing" if not lat else "placeholder" if PLACEHOLDER.search(lat)
                      else "sourced" if (d.get("latin_verified") or d.get("incipit_verified")) else "unverified")
        if looks_english(lat) and g["latin"] not in ("placeholder", "missing"):
            g["latin"] = "misfiled"  # English text sitting in the Latin field
        t, src, who = translation_of(d)
        g["translation"] = ("missing" if not t.strip() else "placeholder" if PLACEHOLDER.search(t) or t.strip() == "TO BE VERIFIED"
                            else "restricted" if RESTRICTED_SRC.search(src) or RESTRICTED_SRC.search(who)
                            else "template" if TEMPLATE_SRC.search(src) or TEMPLATE_SRC.search(who) or tr_count[t.strip()] > REUSE_THRESHOLD
                            else "unverified")
        if g["translation"] in ("unverified",) and lat and norm(t) == norm(lat):
            g["translation"] = "misfiled"  # Latin copied into the English field
        for f in ("charge", "defense"):
            v = d.get(f) or ""
            g[f] = ("missing" if not v else "placeholder" if PLACEHOLDER.search(v)
                    else "template" if (ch_count if f == "charge" else de_count)[v] > REUSE_THRESHOLD else "unverified")
        ex = d.get("exegesis") or ""
        g["exegesis"] = ("missing" if not ex else "template" if BOILER_EXEG.match(ex) or ex_count[ex] > REUSE_THRESHOLD else "unverified")
        cites = d.get("scholar_citations", [])
        cg = []
        for c in cites:
            q = str(c.get("quotation", ""))
            page = str(c.get("pages") or c.get("page") or "").strip()
            if not q.strip() or PLACEHOLDER.search(q):
                cg.append("placeholder")
            elif q_count[norm(q)] > REUSE_THRESHOLD:
                cg.append("template")
            elif corpus:
                st = quote_status(q, corpus)
                cg.append("sourced" if st == "VERBATIM" and page not in ("", "None") and not PLACEHOLDER.search(page) else
                          "unverified" if st in ("VERBATIM", "PARTIAL", "TOO_SHORT") else "template")
            else:
                cg.append("unverified")
        g["citations"] = "missing" if not cites else ("sourced" if all(x == "sourced" for x in cg) else
                                                      "placeholder" if all(x == "placeholder" for x in cg) else
                                                      "template" if any(x == "template" for x in cg) else "unverified")
        for f in list(g):
            if (d["conclusion_id"], f) in quarantine:
                g[f] = "quarantined"
        out.append({"id": d["conclusion_id"], "section": section_of(d), "file": d["_file"], "grade": g, "citation_grades": cg})
    return out


def grade_all(verify_quotes=True):
    """Public entry point for the build: [{id, grade{field: level}, citation_grades[...]}], in file order."""
    rows = load()
    return rows, grade(rows, load_corpus() if verify_quotes else {})


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verify-quotes", action="store_true")
    ap.add_argument("--list-ready", action="store_true")
    a = ap.parse_args()
    rows = load()
    corpus = load_corpus() if a.verify_quotes else {}
    if a.verify_quotes and not corpus:
        print("warning: no source Markdown found at", SOURCES_MD, file=sys.stderr)
    graded = grade(rows, corpus)
    fields = ["latin", "translation", "charge", "defense", "exegesis", "citations"]
    levels = ["sourced", "unverified", "template", "restricted", "misfiled", "quarantined", "placeholder", "missing"]
    by = collections.defaultdict(list)
    for e in graded:
        by[e["section"]].append(e)

    ready = [e["id"] for e in graded if all(e["grade"][f] == "sourced" for f in fields)]
    if a.list_ready:
        print("\n".join(ready) or "(none)")
        return 0

    lines = ["# COVERAGE: what the edition has, graded by provenance\n",
             "*Generated by `scripts/integrity_gate.py`. Do not hand-edit. Re-run after any data change.*\n",
             f"Entries: **{len(graded)}**. Fully sourced (every field): **{len(ready)}**. "
             f"Quotations checked against source corpus: **{'yes' if corpus else 'no (run with --verify-quotes)'}**.\n",
             "Grades: **sourced** (traceable) / unverified / **template** (filler) / placeholder / missing.\n"]
    for f in fields:
        lines += [f"\n## {f}\n", "| section | n | " + " | ".join(levels) + " |", "|---|---|" + "---|" * len(levels)]
        for s in sorted(by):
            c = collections.Counter(e["grade"][f] for e in by[s])
            lines.append(f"| {s} | {len(by[s])} | " + " | ".join(str(c[l]) for l in levels) + " |")
    with io.open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    with io.open(LEDGER, "w", encoding="utf-8") as fh:
        json.dump({"fields": fields, "entries": graded}, fh, indent=1)

    print("\n".join(lines))
    # a public-facing field that is template/placeholder must not be rendered as edition text
    bad = [e for e in graded if any(e["grade"][f] not in ("sourced", "unverified") for f in fields)]
    print(f"\nGATE: {len(bad)} of {len(graded)} entries carry template or placeholder content.")
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
