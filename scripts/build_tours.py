#!/usr/bin/env python3
"""build_tours.py: render essays written from verified claims as guided, relationally browsable pages (T-SITE-04).

    python scripts/build_tours.py            public build: quotations cut to 40 words with work and line
    python scripts/build_tours.py --local    full quotations (<=120 words); local reading only, never deployed

For each essay in ESSAYS: (1) run scripts/commentary_check.py and REFUSE to build if it fails (no page may show
a citation that is dangling, unverified or unjudged by a second reader); (2) split at `## ` headings into stops;
(3) turn each [[claim-id]] into a numbered link to that claim's evidence card in the explorer (cards/#open=ID);
(4) give each stop a list of the sources it cites (claimant, kind of claim, work, line, the quotation, tier and
importance, hedge); (5) mark the editor's own sentences `(ed.)` so the three voices stay distinguishable
(docs/EDITORIAL_STANDARD.md s2). Output: site/essays/<slug>/index.html, site/essays/index.html, essay.css, tour.js.
Nothing on a page is typed by hand: the prose is the essay file, everything else is derived.
"""
import argparse, glob, html, io, json, os, re, shutil, subprocess, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpuslib as C
import commentary_check as K

BASE = os.environ.get("PICO_BASE_PATH", "/Pico900").rstrip("/")
OUT = os.path.join(ROOT, "site", "essays")
ESSAYS = [
    {"slug": "ficino-pico", "file": "docs/essays/ficino_pico_dispute.md", "kind": "Guided tour"},
    {"slug": "angelic-material", "file": "docs/angelology/COMMENTARY.md", "kind": "Commentary"},
    {"slug": "angels-location-trial", "file": "docs/essays/angels_location_trial.md", "kind": "Guided tour"},
    {"slug": "angelic-orders-sources", "file": "docs/essays/angelic_orders_sources.md", "kind": "Guided tour"},
]
REF = K.REF
ATT = {"scholar_claim": "scholar's own claim", "scholar_report": "scholar reporting another", "primary_text": "Pico's own words"}
TYPES = {"doctrinal_content": "doctrine", "source_identification": "source", "interpretive_position": "interpretation",
         "historical_event": "history", "textual_crux": "textual crux", "method": "method", "reception": "reception"}


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def cut(s, n):
    w = s.split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")


def work_short(work):
    w = C.registry().get(work, {})
    au = w.get("author", work)
    last = au.split(",")[0].split()[-1] if au else work
    return "%s %s" % (last, w.get("year", ""))


def shell(title, body, extra_head="", depth=1):
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(t)s - Pico, 900 Conclusions</title>
<link rel="stylesheet" href="%(b)s/css/style.css"><link rel="stylesheet" href="%(b)s/essays/essay.css">%(h)s</head>
<body><header class="top"><a class="brand" href="%(b)s/">Pico della Mirandola, <em>Conclusiones</em> (1486)</a>
<a href="%(b)s/sections/">Sections</a><a href="%(b)s/condemned/">The thirteen condemned</a><a href="%(b)s/scholarship/">Scholarship</a>
<a href="%(b)s/essays/">Essays</a><a href="%(b)s/cards/">Cards</a><a href="%(b)s/about/">Method</a></header>
%(body)s
<footer>Every numbered citation opens a claim whose quotation a script re-found in its source and whose restatement a second reader checked.
Sentences marked <span class="ed">(ed.)</span> are the editor's own inference, not a scholar's claim.</footer>
<script src="%(b)s/essays/tour.js"></script></body></html>
""" % {"t": esc(title), "b": BASE, "h": extra_head, "body": body}


def build_essay(spec, claims, status, scores, qmax, local):
    path = os.path.join(ROOT, spec["file"])
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "commentary_check.py"), path], capture_output=True, text=True,
                       encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if r.returncode != 0:
        errs = [l for l in r.stdout.splitlines() if l.startswith("ERROR")]
        print("REFUSED %s: the citation gate fails (%s)" % (spec["file"], "; ".join(e[:120] for e in errs)))
        return None
    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    title = re.match(r"# (.+)", text).group(1).strip()
    parts = re.split(r"(?m)^## ", text)
    pre, stops = parts[0], parts[1:]
    order, num = [], {}

    def number(cid):
        if cid not in num:
            num[cid] = len(num) + 1
            order.append(cid)
        return num[cid]

    def render_body(body, sid, cited):
        def sub(m):
            outs = []
            for i in [x.strip() for x in m.group(1).split("|") if x.strip()]:
                if i not in claims:
                    raise SystemExit("unknown claim %s in %s" % (i, spec["file"]))
                n = number(i)
                if i not in cited:
                    cited.append(i)
                outs.append('<sup class="fn"><a href="#fn-%s-%d" title="%s">%d</a></sup>' % (sid, n, esc(cut(claims[i]["text"], 22)), n))
            return "".join(outs)
        body = REF.sub(sub, body)
        body = body.replace("(ed.)", '<span class="ed" title="The editor\'s own inference or connective, not a scholar\'s claim">(ed.)</span>')
        return markdown.markdown(body)

    def sources(sid, cited):
        items = []
        for cid in cited:
            c = claims[cid]
            q = c["quotes"][0]
            sc = scores.get(cid, {})
            badges = ['<span class="b tier">%s %d</span>' % (esc(sc.get("tier", "")), round(sc.get("importance", 0)))]
            if c["hedge"] != "assertive":
                badges.append('<span class="b hedge">%s</span>' % esc(c["hedge"]))
            badges.append('<span class="b ok" title="restatement checked by a second reader; quotation re-found by a script">checked</span>')
            items.append(
                '<li id="fn-%s-%d" value="%d"><span class="who">%s</span> <span class="kind">(%s; %s)</span> <span class="loc">%s, l. %s</span>'
                ' <q>%s</q> %s <a class="open" href="%s/cards/#open=%s">open the claim card</a></li>' % (
                    sid, num[cid], num[cid], esc(c["claimant"]), esc(ATT.get(c["attribution"], c["attribution"])), esc(TYPES.get(c["claim_type"], c["claim_type"])),
                    esc(work_short(q["work"])), q["line"], esc(cut(q["text"], qmax)), " ".join(badges), BASE, esc(cid)))
        return '<aside class="evidence" aria-label="Sources cited in this stop"><h3>Sources cited here</h3><ol>%s</ol></aside>' % "".join(items) if items else ""

    sections, rail = [], []
    cited0 = []
    intro_html = render_body(re.sub(r"(?m)^# .+\n", "", pre, count=1), "intro", cited0)
    intro_src = sources("intro", cited0)
    for k, s in enumerate(stops, 1):
        head, _, body = s.partition("\n")
        head = head.strip()
        sid = "stop-%d" % k
        cited = []
        bh = render_body(body, sid, cited)
        prev = '<a class="prev" href="#stop-%d">&larr; Stop %d</a>' % (k - 1, k - 1) if k > 1 else '<a class="prev" href="#top">&uarr; Start</a>'
        nxt = '<a class="next" href="#stop-%d">Stop %d &rarr;</a>' % (k + 1, k + 1) if k < len(stops) else '<a class="next" href="%s/cards/">Explore all the cards &rarr;</a>' % BASE
        sections.append('<section id="%s" class="stop" data-n="%d"><h2>%s</h2>%s%s<nav class="stopnav">%s%s</nav></section>' % (
            sid, k, markdown.markdown(head)[3:-4], bh, sources(sid, cited), prev, nxt))
        rail.append('<li><a href="#%s" data-stop="%s">%s</a></li>' % (sid, sid, markdown.markdown(head)[3:-4]))
    words = len(re.sub(r"\[\[[^\]]*\]\]", "", text).split())
    body = ('<main class="essay" id="top"><nav class="rail" aria-label="Stops"><p class="railhead">%s</p><ol>%s</ol><p class="progress" id="progress"></p>'
            '<p class="railfoot"><a href="%s/cards/">Cards</a> &middot; <a href="%s/essays/">All essays</a></p></nav>'
            '<article data-slug="%s"><h1>%s</h1><p class="meta">%s. About %d words, %d cited claims. %s</p><div class="intro">%s%s</div>%s</article></main>' % (
                esc(spec["kind"]), "".join(rail), BASE, BASE, esc(spec["slug"]), esc(title), esc(spec["kind"]), words, len(num),
                "Local build: full quotations." if local else "Quotations are cut to %d words; each carries its work and line." % qmax,
                intro_html, intro_src, "".join(sections)))
    d = os.path.join(OUT, spec["slug"])
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(shell(title, body))
    print("built %s: %d stops, %d words, %d cited claims" % (spec["slug"], len(stops), words, len(num)))
    return {"slug": spec["slug"], "title": title, "kind": spec["kind"], "stops": len(stops), "words": words, "claims": len(num)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    qmax = 120 if a.local else 40
    claims, status = K.load_claims()
    with io.open(os.path.join(ROOT, "data", "claims", "angelology", "scores.json"), encoding="utf-8") as fh:
        scores = json.load(fh)["claims"]
    os.makedirs(OUT, exist_ok=True)
    for src, dst in (("src/css/essay.css", "essay.css"), ("src/js/tour.js", "tour.js")):
        shutil.copyfile(os.path.join(ROOT, src), os.path.join(OUT, dst))
    built, refused = [], 0
    for spec in ESSAYS:
        if not os.path.exists(os.path.join(ROOT, spec["file"])):
            continue
        b = build_essay(spec, claims, status, scores, qmax, a.local)
        if b:
            built.append(b)
        else:
            refused += 1
    rows = "".join('<li><a href="%s/essays/%s/">%s</a><br><span class="meta">%s &middot; %d stops &middot; %d words &middot; %d cited claims</span></li>' % (
        BASE, b["slug"], esc(b["title"]), esc(b["kind"]), b["stops"], b["words"], b["claims"]) for b in built)
    with io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(shell("Essays", '<main><h1>Essays and guided tours</h1><p class="meta">Written only from claims that a script re-found in their sources '
                       'and a second reader checked. Each numbered citation opens the claim\'s evidence.</p><ul class="essays">%s</ul></main>' % rows))
    return 1 if refused else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
