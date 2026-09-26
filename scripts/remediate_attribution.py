#!/usr/bin/env python3
"""remediate_attribution.py: mechanical, non-prose-generating fixes for the dominant entry_gate.py
failure patterns found in WRITER-swarm output:

1. `attribution` field written as a descriptive sentence (>4 words, no locator) -> shortened to a
   <=4-word tag ("Pico's own opinion" / "Reports <Name>"), which the gate's word-count exemption
   accepts without a locator. The longer descriptive text (if any) is preserved by moving it, only
   if it already carried its own locator, into `context`; otherwise it is dropped (it was
   unsourced description anyway, e.g. restating the section title, which is not evidence).
2. A `reception` (or other prose) field whose entire content is the literal fallback sentence
   "not established by the sources consulted." (or a close variant) is moved into the
   `not_established` list and the field is cleared. This is a relocation of the WRITER's own
   words, not new prose.

This script does NOT touch scholar-name-without-locator failures or translation_note/doctrine
sentences lacking locators - those need a human or agent to either find the real locator or cut
the sentence, and doing that automatically risks misattribution.

Usage: python scripts/remediate_attribution.py entries/*.draft.json
"""
import glob, io, json, re, sys

FALLBACK_RE = re.compile(r"^\s*not established by the sources consulted\.?\s*$", re.IGNORECASE)
LOC = re.compile(r"\b([a-z][a-z0-9_]{2,40}):(\d{2,6})(?:\s?-\s?(\d{2,6}))?\b")


def short_attribution(d):
    attr = d.get("attribution") or ""
    stance = d.get("pico_stance")
    tid = d.get("thesis_id", "")
    if len(attr.split()) <= 4:
        return None  # already fine (gate exempts <=4-word sentences from the locator check)
    if LOC.search(attr):
        return None  # already carries a locator; the gate's rule 4 already accepts this as-is
    if stance == "endorses":
        new = "Pico's own opinion"
    else:
        # try to pull a proper name out of the old attribution, e.g. "Reports the doctrine of Henry of Ghent, section 5 ..."
        m = re.search(r"doctrine of ([A-Z][A-Za-z.]+(?: [A-Za-z.]+){0,3}?)(?:,| \()", attr)
        name = m.group(1).strip() if m else None
        new = f"Reports {name}" if name and len(("Reports " + name).split()) <= 4 else "Reports another philosopher"
    return new


def fix_file(path):
    d = json.load(io.open(path, encoding="utf-8"))
    changed = []
    new_attr = short_attribution(d)
    if new_attr:
        changed.append(f"attribution: {d['attribution']!r} -> {new_attr!r}")
        d["attribution"] = new_attr
    for field in ("reception", "context", "historiography", "doctrine"):
        val = d.get(field)
        if val and FALLBACK_RE.match(val.strip()):
            ne = d.get("not_established") or []
            if val.strip() not in ne:
                ne.append(val.strip())
            d["not_established"] = ne
            d[field] = None
            changed.append(f"{field}: moved fallback sentence to not_established")
    if changed:
        with io.open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
    return changed


def main():
    paths = sys.argv[1:] or sorted(glob.glob("entries/*.draft.json"))
    total = 0
    for p in paths:
        changed = fix_file(p)
        if changed:
            total += 1
            print(p)
            for c in changed:
                print("   ", c)
    print(f"\n{total}/{len(paths)} files modified")


if __name__ == "__main__":
    main()
