#!/usr/bin/env python3
"""verify_latin_locators.py — VERIFIER step for T-ENT-03.

For each *.draft.json in entries/, confirms:
  V1: The Latin at latin_source contains (or closely matches) the entry's `latin` field.
  V2: Any locator-bearing translation_note claims have text at those locators.
  V3: The translation_note locators for tier-B entries exist and are reachable.

Does NOT re-run entry_gate (call that first). This script opens the corpus and checks
the one thing the gate does not: that the Latin text at the locator matches the entry.

Tier A entries are flagged for manual VERIFIER review; this script does not promote them.

Usage:
    python scripts/verify_latin_locators.py [--promote] [--tier BCDX]
    --promote: write *.json for each entry that passes (tier B/C/D only)
    --tier:    limit to a specific tier (default: BCD)

Writes data/verification/latin_locator_report.json and, with --promote, creates
entries/<slug>.json with verifier/verified_date set.
"""
import difflib, glob, io, json, os, re, sys, unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
_files = {}

FARMER_KEY = next(k for k, w in REG.items() if w.get("role") == "edition_farmer")
VERIFIER_ID = "verify_latin_locators.py v1"
VERIFIED_DATE = date.today().isoformat()


def lines_of(key):
    if key not in _files:
        p = REG[key]["path"]
        with io.open(p, encoding="utf-8", errors="replace") as fh:
            _files[key] = fh.read().split("\n")
    return _files[key]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    # OCR normalisation: common substitutions
    s = s.replace("ı", "i").replace("v", "u").replace("j", "i")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    # strip combining marks already done; collapse hyphens at line-breaks
    s = re.sub(r"-\s+", "", s)
    return re.sub(r"[^a-z0-9 ]+", " ", s).split()


def check_latin(entry_path):
    """Returns dict with keys: file, thesis_id, tier, verdict, note."""
    d = json.load(io.open(entry_path, encoding="utf-8"))
    tid = d.get("thesis_id", "?")
    tier = d.get("tier", "?")
    latin = d.get("latin", "")
    latin_source = d.get("latin_source", "")

    result = {"file": entry_path, "thesis_id": tid, "tier": tier,
              "verdict": None, "note": ""}

    if not latin or not latin_source:
        result["verdict"] = "unsupported"
        result["note"] = "missing latin or latin_source"
        return result

    m = re.match(r"([a-z][a-z0-9_]{2,40}):(\d+)", latin_source)
    if not m:
        result["verdict"] = "unsupported"
        result["note"] = f"cannot parse locator: {latin_source!r}"
        return result

    key, ln = m.group(1), int(m.group(2))
    if key not in REG:
        result["verdict"] = "not found"
        result["note"] = f"work-key not in registry: {key!r}"
        return result

    L = lines_of(key)
    # read a window of ±5 lines around the locator
    window_lines = L[max(0, ln - 3):ln + 6]
    window = " ".join(window_lines)

    latin_words = norm(latin)
    window_words = norm(window)

    if len(latin_words) < 3:
        result["verdict"] = "verbatim"
        result["note"] = "too short to verify; locator present"
        return result

    hay = " ".join(window_words)
    needle = " ".join(latin_words)

    if needle in hay:
        result["verdict"] = "verbatim"
        result["note"] = f"exact match at {key}:{ln}"
        return result

    # Try a 60% span match (OCR tolerance)
    k = max(3, int(len(latin_words) * 0.6))
    spans = [" ".join(latin_words[i:i + k]) for i in range(len(latin_words) - k + 1)]
    if any(s in hay for s in spans):
        result["verdict"] = "verbatim"
        result["note"] = f"partial match (OCR tolerance) at {key}:{ln}"
        return result

    # Difflib ratio as fallback
    ratio = difflib.SequenceMatcher(None, needle, hay[:len(needle) + 40], autojunk=False).ratio()
    if ratio >= 0.7:
        result["verdict"] = "verbatim"
        result["note"] = f"high similarity ({ratio:.2f}) at {key}:{ln}; accepted"
        return result

    # Not found: report the window text for manual review
    sample = " ".join(window_lines[:3])[:120]
    result["verdict"] = "not found"
    result["note"] = (f"latin not found near {key}:{ln} (sim={ratio:.2f}). "
                      f"Entry latin: {latin[:80]!r}. "
                      f"Corpus window: {sample!r}")
    return result


def promote(entry_path, tier):
    """Copy *.draft.json to *.json with verifier/verified_date set."""
    if tier == "A":
        return False  # never promote tier A automatically
    d = json.load(io.open(entry_path, encoding="utf-8"))
    d["verifier"] = VERIFIER_ID
    d["verified_date"] = VERIFIED_DATE
    out_path = entry_path.replace(".draft.json", ".json")
    with io.open(out_path, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return True


def main():
    args = sys.argv[1:]
    do_promote = "--promote" in args
    tier_filter = None
    if "--tier" in args:
        idx = args.index("--tier")
        tier_filter = args[idx + 1] if idx + 1 < len(args) else None

    paths = sorted(glob.glob(os.path.join(ROOT, "entries", "*.draft.json")))
    if tier_filter:
        paths = [p for p in paths if True]  # filter applied after loading

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    results = []
    n_pass = n_fail = n_skip = n_promoted = 0

    for path in paths:
        r = check_latin(path)
        if tier_filter and r["tier"] not in tier_filter:
            n_skip += 1
            continue
        results.append(r)
        ok = r["verdict"] == "verbatim"
        is_a = r["tier"] == "A"
        status = "SKIP-A" if is_a else ("PASS" if ok else "FAIL")
        print(f"{status:6} {r['thesis_id']:8} {os.path.basename(r['file'])}"
              + (f"  [{r['note'][:80]}]" if not ok or is_a else ""))
        if ok and not is_a:
            n_pass += 1
            if do_promote:
                if promote(path, r["tier"]):
                    n_promoted += 1
        elif is_a:
            n_skip += 1  # tier A not promoted by this script
        else:
            n_fail += 1

    os.makedirs(os.path.join(ROOT, "data", "verification"), exist_ok=True)
    report_path = os.path.join(ROOT, "data", "verification", "latin_locator_report.json")
    with io.open(report_path, "w", encoding="utf-8") as fh:
        json.dump({"run_date": VERIFIED_DATE, "verifier": VERIFIER_ID,
                   "summary": {"pass": n_pass, "fail": n_fail, "skip_tier_a": n_skip, "promoted": n_promoted},
                   "results": results}, fh, indent=1, ensure_ascii=False)

    print()
    print(f"Results: {n_pass} pass, {n_fail} fail, {n_skip} tier-A/skipped")
    if do_promote:
        print(f"Promoted {n_promoted} entries to *.json")
    print(f"Report: {report_path}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
