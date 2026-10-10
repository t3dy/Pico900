#!/usr/bin/env python3
"""essay_sheet.py: the sentence-fidelity sheet for prose written from claims.

    python scripts/essay_sheet.py docs/essays/ficino_pico_dispute.md            writes data/verification/essays/<slug>.sheet.md
    python scripts/essay_sheet.py FILE --only 1-40                              sentence range (for splitting a long essay across readers)

commentary_check.py proves each citation exists, is verified and judged supported, and that quoted strings are verbatim. It cannot
prove that a SENTENCE says no more than the claims it cites: a writer can strengthen a hedge, merge two scholars, or state a
scholar's report as fact, and every gate still passes. Worse, claims are corrected after an essay is drafted (verifier rewrites), so a
sentence written from an old restatement can now overstate. This sheet puts each cited sentence beside the CURRENT restatement
(and the first quotation) of every claim it cites, for a second reader to judge. Verdicts go to
data/verification/essays/<slug>.fidelity.json (see docs/briefs/essay_fidelity_verifier.md). The sheet embeds quotations, so it is local only (.gitignore).
"""
import argparse, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_check as K
import claims_verify as V

ROOT = K.ROOT
OUT = os.path.join(ROOT, "data", "verification", "essays")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--only")
    a = ap.parse_args()
    lo, hi = (1, 10 ** 6)
    if a.only:
        lo, hi = [int(x) for x in a.only.split("-")]
    claims, status = K.load_claims()
    with io.open(a.file, encoding="utf-8") as fh:
        text = fh.read()
    slug = os.path.splitext(os.path.basename(a.file))[0]
    lines = ["# Essay fidelity sheet: %s" % os.path.relpath(a.file, ROOT), "",
             "For each sentence below: does it say NO MORE than the current restatements and quotations of the claims it cites? "
             "Verdict faithful / overreaches / misattributed, one-line reason, `suggested_sentence` if it needs rewording. "
             "Judge hedges (kept?), voice (a scholar's report never as the essay's own fact; Aquinas, Scotus, Dionysius only through the scholar), "
             "merging of two scholars or two doctrines, and any name, date or number not in the cited claims. Sentences marked (ed.) are the editor's "
             "own inference: judge only that they do not smuggle in an uncited fact.", ""]
    n, uncited = 0, []
    for pi, par in enumerate(K.paragraphs(text), 1):
        if not K.counted(par):
            continue
        body = par.replace("\n", " ")
        for s in K.SENT.split(body):
            s = s.strip()
            if len(s.split()) < 4:
                continue
            ids = []
            for m in K.REF.finditer(s):
                ids += [x.strip() for x in m.group(1).split("|") if x.strip()]
            n += 1
            if n < lo or n > hi:
                continue
            clean = K.REF.sub(lambda m: "[" + m.group(1) + "]", s)
            if not ids:
                uncited.append((n, pi, clean))
                continue
            lines.append("## S%03d  (paragraph %d)" % (n, pi))
            lines.append("")
            lines.append("**Sentence:** " + clean)
            lines.append("")
            for i in dict.fromkeys(ids):
                c = claims.get(i)
                if c is None:
                    lines.append("- **%s**: NOT FOUND" % i)
                    continue
                q = c["quotes"][0]
                lines.append("- **%s** (%s; %s; %s): %s" % (i, c["claimant"], c["attribution"], c["hedge"], c["text"]))
                lines.append("  > %s  (%s:%s)" % (" ".join(q["text"].split()[:50]) + (" ..." if len(q["text"].split()) > 50 else ""), q["work"], q["line"]))
            lines.append("")
    if uncited:
        lines.append("## Sentences with no citation (connective or editorial; flag any that assert a fact)")
        lines.append("")
        for n_, pi, t in uncited:
            lines.append("- S%03d (paragraph %d): %s" % (n_, pi, t))
        lines.append("")
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, slug + (".sheet.md" if not a.only else ".sheet.%s.md" % a.only))
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("wrote %s: %d sentences in the essay, %d listed with citations, %d uncited" % (os.path.relpath(path, ROOT), n, sum(1 for l in lines if l.startswith("## S")), len(uncited)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
