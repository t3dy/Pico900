#!/usr/bin/env python3
"""commentary_check.py: the gate on prose written from claims (commentaries, essays, card text).

    python scripts/commentary_check.py docs/angelology/COMMENTARY.md            # check
    python scripts/commentary_check.py FILE --render docs/angelology/COMMENTARY.rendered.md   # check, then render

Syntax in the source file
    [[allen2017-venus:012]]            cite a claim (several in a row are fine; `[[a:1|b:2]]` too)
    "a direct quotation of five or more words"   must occur in the quotations of the claims cited in that paragraph
    (ed.)                              ends a sentence that is the editor's own inference or connective
    Headings, lists of links and blockquoted epigraphs are not counted as sentences.

Errors (exit 1):  dangling_ref (no such claim) | unverified_ref (claim did not pass claims_verify) |
                  unsupported_quote (a quoted string not found in the cited claims' quotations or their sources) |
                  uncited_ratio (more than 15% of sentences carry neither a citation nor `(ed.)`) |
                  ed_ratio (more than 25% of sentences are `(ed.)`)
Warnings:         each uncited sentence; style_lint output if scripts/style_lint.py exists.
--render writes the file with [[ids]] replaced by numbered footnotes giving author, work, year, line (and page when the
claim records one) and the verbatim quotation, plus a `.refs.json` mapping each paragraph to its claim ids (for the site).
This checks that the writer's words are anchored. It cannot judge whether a sentence fairly summarises its claim: a
second agent samples that (docs/CLAIMS_MODEL.md s6).
"""
import argparse, glob, io, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpuslib as C

ROOT = C.ROOT
REF = re.compile(r"\[\[([^\]]+)\]\]")
QUOTE = re.compile(r"[“\"]([^“”\"]{20,}?)[”\"]")
SENT = re.compile(r"(?<=[.!?])[”\"')\]]*\s+(?=[A-Z“\"\[(])")


def load_claims():
    claims, status = {}, {}
    for f in glob.glob(os.path.join(ROOT, "data", "claims", "**", "*.claims.json"), recursive=True):
        with io.open(f, encoding="utf-8") as fh:
            p = json.load(fh)
        vf = os.path.join(ROOT, "data", "verification", "claims", p["packet"] + ".verdicts.json")
        st = {}
        if os.path.exists(vf):
            with io.open(vf, encoding="utf-8") as fh:
                st = {c["id"]: c["status"] for c in json.load(fh)["claims"]}
        for c in p["claims"]:
            claims[c["id"]] = c
            status[c["id"]] = st.get(c["id"], "unverified")
    return claims, status


def paragraphs(text):
    out, buf = [], []
    for ln in text.split("\n"):
        if ln.strip() == "":
            if buf:
                out.append("\n".join(buf)); buf = []
        else:
            buf.append(ln)
    if buf:
        out.append("\n".join(buf))
    return out


def counted(par):
    s = par.strip()
    return not (s.startswith("#") or s.startswith(">") or s.startswith("|") or s.startswith("- [") or s.startswith("<!--") or s.startswith("```"))


def ids_in(par):
    ids = []
    for m in REF.finditer(par):
        ids += [x.strip() for x in m.group(1).split("|") if x.strip()]
    return ids


def work_label(work):
    w = C.registry().get(work, {})
    return "%s, *%s* (%s)" % (w.get("author", work), w.get("title", work), w.get("year", "n.d."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--render")
    a = ap.parse_args()
    with io.open(a.file, encoding="utf-8") as fh:
        text = fh.read()
    claims, status = load_claims()
    errors, warns = [], []
    total = cited = eds = uncited = 0
    pars = paragraphs(text)
    refs_map = []
    for pi, par in enumerate(pars, 1):
        ids = ids_in(par)
        for i in ids:
            if i not in claims:
                errors.append(("dangling_ref", "paragraph %d: no claim %s" % (pi, i)))
            elif status[i] != "verified":
                errors.append(("unverified_ref", "paragraph %d: %s is %s" % (pi, i, status[i])))
        if ids:
            refs_map.append({"paragraph": pi, "claims": sorted(set(ids)), "head": par.strip()[:80]})
        # quotations must come from the cited claims' quotations (normalised containment), else be found in their works
        pool = " ".join(q["text"] for i in set(ids) if i in claims for q in claims[i].get("quotes", []))
        pool_n = C.norm(pool)
        works = {q["work"] for i in set(ids) if i in claims for q in claims[i].get("quotes", [])}
        for m in QUOTE.finditer(REF.sub("", par)):
            q = m.group(1)
            if len(q.split()) < 5:
                continue
            frs = [C.norm(f) for f in C.fragments(q) if len(C.norm(f)) >= C.MIN_FRAG] or [C.norm(q)]
            if all(f in pool_n for f in frs):
                continue
            ok = False
            for w in works:
                try:
                    if C.locate(w, q)["verdict"] in ("verbatim", "verbatim_modulo_marks"):
                        ok = True
                        break
                except Exception:
                    pass
            if not ok:
                errors.append(("unsupported_quote", "paragraph %d: %r is in no cited claim and not verbatim in their sources" % (pi, q[:90])))
        if not counted(par):
            continue
        body = REF.sub("\u0002", par.replace("\n", " "))
        for s in SENT.split(body):
            s = s.strip()
            if len(s.split()) < 4:
                continue
            total += 1
            if "\u0002" in s:
                cited += 1
            elif s.rstrip().endswith("(ed.)") or "(ed.)" in s[-12:]:
                eds += 1
            else:
                uncited += 1
                warns.append("uncited: " + s[:110])
    if total:
        if uncited / total > 0.15:
            errors.append(("uncited_ratio", "%d of %d sentences (%.0f%%) have neither a citation nor (ed.)" % (uncited, total, 100.0 * uncited / total)))
        if eds / total > 0.25:
            errors.append(("ed_ratio", "%d of %d sentences (%.0f%%) are editor's inference" % (eds, total, 100.0 * eds / total)))
    lint = os.path.join(ROOT, "scripts", "style_lint.py")
    if os.path.exists(lint):
        r = subprocess.run([sys.executable, lint, a.file], capture_output=True, text=True, encoding="utf-8")
        warns.append("style_lint:\n" + (r.stdout or r.stderr).strip())
    print("%s: %d sentences, %d cited, %d (ed.), %d uncited; %d claim references" % (a.file, total, cited, eds, uncited, len(set(sum([r["claims"] for r in refs_map], [])))))
    for code, msg in errors:
        print("ERROR %s: %s" % (code, msg))
    for w in warns[:40]:
        print("warn  " + w)
    if a.render and not errors:
        n, notes, order = 0, [], {}
        def sub(m):
            nonlocal n
            outs = []
            for i in [x.strip() for x in m.group(1).split("|") if x.strip()]:
                if i not in order:
                    n += 1
                    order[i] = n
                    c = claims[i]
                    q = c["quotes"][0]
                    words = q["text"].split()
                    qt = " ".join(words[:45]) + (" ..." if len(words) > 45 else "")
                    loc = "l. %s%s" % (q["line"], ", p. %s" % q["page"] if q.get("page") else "")
                    who = "" if c["attribution"] == "primary_text" else "%s, " % c["claimant"]
                    notes.append("[^%d]: %s%s, %s. “%s” (claim %s; %s)" % (n, who if False else "", work_label(q["work"]), loc, qt, i, c["attribution"].replace("_", " ")))
                outs.append("[^%d]" % order[i])
            return "".join(outs)
        rendered = REF.sub(sub, text).rstrip() + "\n\n" + "\n".join(notes) + "\n"
        with io.open(a.render, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(rendered)
        with io.open(os.path.splitext(a.render)[0] + ".refs.json", "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"source": os.path.relpath(a.file, ROOT), "paragraphs": refs_map}, fh, indent=1, ensure_ascii=False)
        print("rendered %s with %d footnotes" % (a.render, n))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
