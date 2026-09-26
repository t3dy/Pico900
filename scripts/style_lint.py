#!/usr/bin/env python3
"""style_lint.py: mechanical pass over prose for the AI-writing markers named in
docs/EDITORIAL_STANDARD.md. It counts; it does not judge. A clean lint is necessary, never
sufficient: the AUDITOR still reads. Use it on essays, entry prose fields, and site copy.

    python scripts/style_lint.py docs/HERETICAL_ESSAY_DRAFT_OUTLINE.md
    python scripts/style_lint.py --entries data/conclusions        # exegesis fields of all entries
    python scripts/style_lint.py --max-per-1k 3 FILE...            # exit 1 if any marker density exceeds

Density is hits per 1,000 words. Markdown code fences and blockquotes are skipped, so a
quoted scholar is not charged with the style of the quotation.
"""
import argparse, collections, glob, io, json, os, re, sys

MARKERS = {
    # corrective contrast used as a reflex rather than against a named position
    "not_x_but_y": r"\bnot (?:merely |simply |just |only |incidental|a |an |the )?[^.;:\n]{1,60}?,? (?:but|rather)\b",
    "announce": r"\b(?:it is|it's) (?:important|worth|useful) (?:to )?(?:note|noting|stress|emphasi[sz]e|remember)|\bnote that\b|\bit should be noted\b",
    "filler_adverb": r"\b(?:importantly|interestingly|essentially|basically|fundamentally|crucially|notably|remarkably|arguably|ultimately)\b",
    "hedge": r"\b(?:it could be argued|one might (?:say|argue)|may (?:well )?suggest|seems? to (?:suggest|imply)|in a sense|to some extent|somewhat)\b",
    "phantom_scholar": r"\b(?:scholars|historians|critics|commentators|some (?:have|see)|many (?:have|see)) (?:have )?(?:argued|suggested|noted|shown|claimed|long held|often)\b|\bvarious scholars\b",
    "vague_frequency": r"\b(?:often|sometimes|frequently|many|several|numerous|various)\b",
    "list_frame": r"\bon (?:the )?one hand\b|\bon the other hand\b|\bfirst(?:ly)?,.{0,80}\bsecond(?:ly)?,",
    "signpost": r"\bas (?:mentioned|noted|discussed) (?:earlier|above|previously)\b|\bthis (?:section|essay|article|entry) (?:will|discusses|examines)\b|\bin (?:this|the following) (?:section|entry)\b",
    "puffery": r"\b(?:profound|rich|deeply|tapestry|landscape|realm|delve|testament|pivotal|seminal|groundbreaking|fascinating|vibrant)\b",
    "banned_term": r"\b(?:renaissance man|ahead of his time|genius|magical thinking|superstition)\b",
}
COMPILED = {k: re.compile(v, re.I) for k, v in MARKERS.items()}


def prose(text):
    out, fence = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence or line.lstrip().startswith(">") or line.lstrip().startswith("|"):
            continue
        out.append(line)
    return "\n".join(out)


def lint(text, label):
    p = prose(text)
    words = max(1, len(re.findall(r"\w+", p)))
    counts, examples = collections.Counter(), collections.defaultdict(list)
    for k, rx in COMPILED.items():
        for m in rx.finditer(p):
            counts[k] += 1
            if len(examples[k]) < 2:
                s = p[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                examples[k].append(s)
    return {"label": label, "words": words, "counts": counts, "examples": examples}


def report(r, max_per_1k):
    bad = False
    print(f"\n{r['label']}  ({r['words']} words)")
    for k in MARKERS:
        n = r["counts"][k]
        if not n:
            continue
        d = 1000.0 * n / r["words"]
        flag = ""
        if max_per_1k is not None and d > max_per_1k:
            flag, bad = "  <-- over threshold", True
        print(f"  {k:16s} {n:4d}  ({d:4.1f}/1k){flag}")
        for e in r["examples"][k]:
            print(f"      ...{e}...")
    if not r["counts"]:
        print("  no markers")
    return bad


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--entries", help="directory of entry_*.json; lints the exegesis field")
    ap.add_argument("--max-per-1k", type=float, default=None)
    a = ap.parse_args()
    results = []
    for f in a.files:
        with io.open(f, encoding="utf-8", errors="ignore") as fh:
            results.append(lint(fh.read(), f))
    if a.entries:
        buf = []
        for f in sorted(glob.glob(os.path.join(a.entries, "*", "entry_*.json"))):
            with io.open(f, encoding="utf-8") as fh:
                d = json.load(fh)
            ex = d.get("exegesis") or ""
            if ex:
                buf.append(ex)
        results.append(lint("\n\n".join(buf), a.entries + " [exegesis fields]"))
    bad = False
    for r in results:
        bad |= report(r, a.max_per_1k)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
