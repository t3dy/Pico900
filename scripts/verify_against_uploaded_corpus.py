#!/usr/bin/env python3
"""verify_against_uploaded_corpus.py: REAL verification of entries/*.draft.json quotations
against actual uploaded source texts (scratchpad copies of Farmer, Copenhaver, Wirszubski,
Edelheit, Allen, Dougherty, etc.) - not the mechanical/structural checks of entry_gate_local.py.

Unlike the registry's E:\\pdf files (inaccessible here), these are real OCR'd texts the user
uploaded directly into this session. Line numbers in entries/*.draft.json locators do NOT
match these files' line numbers (different OCR extraction), so this script does NOT check
line-window proximity. Instead it checks: does the claimed quotation text actually appear,
verbatim (whitespace/OCR-normalized), ANYWHERE in the named source file? This is a real
content check that the sandbox previously could not do at all.

Usage: python scripts/verify_against_uploaded_corpus.py entries/*.draft.json
Writes a report to stdout and data/verification/uploaded_corpus_verification.json
"""
import glob, io, json, os, re, sys, unicodedata

CORPUS_DIR = "/tmp/claude-0/-home-user-Pico900/d31499eb-8d51-54ab-a15e-47b46fe33c11/scratchpad/farmer"
WORK_FILES = {
    "farmer1998": "farmer1998_uploaded.txt",
    "copenhaver2022": "copenhaver2022.txt",
    "copenhaver2019": "copenhaver2019.txt",
    "wirszubski1989": "wirszubski1989.txt",
    "edelheit2022": "edelheit2022.txt",
    "edelheit2008": "edelheit2008.txt",
    "edelheit2014": "edelheit2014.txt",
    "allen2017": "allen2017.txt",
    "dougherty2008": "dougherty2008_full.txt",
    "busi2014": "busi_ebgi_qabbalah.txt",
    "selfknowledge_notes": "selfknowledge_notes_full.txt",
}
_cache = {}


def norm(s):
    """Word-level normalization: lowercase, strip accents/punctuation, collapse whitespace."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    # rejoin hyphenated line-breaks ("substan-\ntial" -> "substantial") before anything else
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]+", " ", s)).strip()


def nospace(s):
    """Strip ALL whitespace/punctuation for substring matching. This source's OCR runs many
    words together with no spaces at all (column-join artifacts) and inconsistently hyphenates
    across line breaks, so word-boundary matching misses real quotes. Stripping everything to a
    bare letter/digit stream sidesteps both problems at the cost of only checking character
    sequence, not exact word boundaries - acceptable for a lead, not a substitute for a human
    or the real entry_gate.py checking the registry's own corpus copy."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s)


def load(key):
    if key not in _cache:
        fn = WORK_FILES.get(key)
        if not fn:
            _cache[key] = (None, None)
            return None, None
        p = os.path.join(CORPUS_DIR, fn)
        if not os.path.exists(p):
            _cache[key] = (None, None)
            return None, None
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        _cache[key] = (norm(raw), nospace(raw))
    return _cache[key]


def check_quote(key, text):
    hay_words, hay_ns = load(key)
    if hay_words is None:
        return "NO_CORPUS_FILE"
    q = norm(text)
    if len(q) < 8:
        return "TOO_SHORT"
    if q in hay_words:
        return "FOUND_EXACT"
    qns = nospace(text)
    if len(qns) >= 10 and qns in hay_ns:
        return "FOUND_EXACT"
    # tolerate minor OCR gaps: try a contiguous 70%-length span, both word- and char-level
    words = q.split()
    if len(words) >= 4:
        k = max(4, int(len(words) * 0.7))
        for i in range(0, len(words) - k + 1):
            if " ".join(words[i:i + k]) in hay_words:
                return "FOUND_PARTIAL"
    if len(qns) >= 15:
        k = max(15, int(len(qns) * 0.7))
        for i in range(0, len(qns) - k + 1, max(1, k // 3)):
            if qns[i:i + k] in hay_ns:
                return "FOUND_PARTIAL"
    return "NOT_FOUND"


def check_entry(path):
    d = json.load(io.open(path, encoding="utf-8"))
    results = []
    for q in d.get("quotations", []) or []:
        key, text = q.get("work"), q.get("text", "")
        status = check_quote(key, text)
        results.append({"work": key, "text": text[:100], "status": status})
    cv = d.get("commission_verdict")
    if cv:
        # extract quoted spans in commission_verdict for a spot check
        for m in re.finditer(r'["\u201c]([^"\u201d]{10,200})["\u201d]', cv):
            # try against every work mentioned nearby; just try all keys, report best
            best = "NOT_FOUND"
            for key in WORK_FILES:
                st = check_quote(key, m.group(1))
                if st in ("FOUND_EXACT", "FOUND_PARTIAL"):
                    best = st
                    results.append({"work": key, "text": m.group(1)[:100], "status": st, "field": "commission_verdict"})
                    break
            else:
                results.append({"work": "unknown", "text": m.group(1)[:100], "status": best, "field": "commission_verdict"})
    return {"file": path, "thesis_id": d.get("thesis_id"), "quotations_checked": results}


def main():
    paths = sys.argv[1:] or sorted(glob.glob("entries/*.draft.json"))
    all_results = [check_entry(p) for p in paths]
    total = sum(len(r["quotations_checked"]) for r in all_results)
    found = sum(1 for r in all_results for q in r["quotations_checked"] if q["status"] in ("FOUND_EXACT", "FOUND_PARTIAL"))
    no_corpus = sum(1 for r in all_results for q in r["quotations_checked"] if q["status"] == "NO_CORPUS_FILE")
    not_found = sum(1 for r in all_results for q in r["quotations_checked"] if q["status"] == "NOT_FOUND")
    for r in all_results:
        bad = [q for q in r["quotations_checked"] if q["status"] == "NOT_FOUND"]
        if bad:
            print(f"THESIS {r['thesis_id']} ({r['file']}): {len(bad)} quotation(s) NOT FOUND in corpus:")
            for q in bad:
                print(f"    [{q['work']}] {q['text']!r}")
    os.makedirs("data/verification", exist_ok=True)
    with io.open("data/verification/uploaded_corpus_verification.json", "w", encoding="utf-8") as fh:
        json.dump(all_results, fh, indent=1, ensure_ascii=False)
    print(f"\n{found}/{total} quotations verified present in uploaded corpus; {not_found} NOT FOUND; {no_corpus} had no corpus file for that work-key")


if __name__ == "__main__":
    main()
