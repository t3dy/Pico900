#!/usr/bin/env python3
"""build_cards.py: the card explorer (T-SITE-01/02): verified claims as browsable, sortable, searchable cards.

    python scripts/build_cards.py                 public build: quotations cut to 40 words with their locator
    python scripts/build_cards.py --local         full quotations (up to 120 words); for local reading only, never deploy
    PICO_BASE_PATH="" python scripts/build_cards.py --local     root-served, for a quick local test

Reads   data/claims/<domain>/*.claims.json + verdicts (VERIFIED claims only), scores.json, relevance.json, graph.json,
        parties.json, topics.json, traditions.json, data/corpus/registry.json
Writes  site/cards/index.html, cards.css, cards.js, data/cards.json (compact cards), data/detail-<packet>.json (evidence,
        warrants, open questions, relations, score components), data/facets.json
Every card is derived; nothing is typed by hand. A claim that is not verified never appears (docs/CLAIMS_MODEL.md).
Design: docs/SITE_DESIGN.md. Copyright: scholarly quotations are shown at 40 words in public builds, with work and line, so a
reader can check the book; full quotations only with --local.
"""
import argparse, glob, html, io, json, os, shutil, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get("PICO_BASE_PATH", "/Pico900").rstrip("/")
OUT = os.path.join(ROOT, "site", "cards")
PARTY_COLOURS = ["#c0392b", "#2c7fb8", "#7b3294", "#1b9e77", "#d95f02", "#66a61e", "#a6761d", "#e7298a", "#1f78b4", "#666666",
                 "#b15928", "#008080", "#8c6bb1", "#ef6548", "#3690c0", "#41ab5d", "#807dba", "#cc4c02", "#737373", "#fb6a4a"]


def load(p):
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def words(s, n):
    w = s.split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="angelology")
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--quotes", choices=["cited", "all", "none"], default="cited",
                    help="public builds: which claims carry quotation text (cited = only claims cited in a published essay; D-43)")
    a = ap.parse_args()
    qmax = 120 if a.local else 40
    quotes_mode = "all" if a.local else a.quotes
    cited_ids = set()
    if quotes_mode == "cited":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import build_tours as T
        for spec in T.ESSAYS:
            fp = os.path.join(ROOT, spec["file"])
            if os.path.exists(fp):
                with io.open(fp, encoding="utf-8") as fh:
                    for m in T.REF.finditer(fh.read()):
                        cited_ids.update(x.strip() for x in m.group(1).split("|") if x.strip())

    def show_q(cid):
        return quotes_mode == "all" or (quotes_mode == "cited" and cid in cited_ids)
    reg = load(os.path.join(ROOT, "data", "corpus", "registry.json"))["works"]
    topics = {t["id"]: t for t in load(os.path.join(ROOT, "data", "claims", "topics.json"))["topics"]}
    parties = load(os.path.join(ROOT, "data", "claims", "parties.json"))["parties"]
    trad = load(os.path.join(ROOT, "data", "claims", "traditions.json"))
    ddir = os.path.join(ROOT, "data", "claims", a.domain)
    scores = load(os.path.join(ddir, "scores.json"))["claims"]
    tpr_path = os.path.join(ROOT, "data", "network", "thesis_person_relevance.json")
    tpr = load(tpr_path) if os.path.exists(tpr_path) else None
    rel = None if tpr else load(os.path.join(ddir, "relevance.json"))["parties"]
    gp = os.path.join(ddir, "graph.json")
    edges = load(gp)["edges"] if os.path.exists(gp) else []
    for i, p in enumerate(parties):
        p["colour"] = PARTY_COLOURS[i % len(PARTY_COLOURS)]
    pname = {p["id"]: p["name"] for p in parties}

    def wl(work):
        w = reg.get(work, {})
        au = w.get("author", work)
        last = au.split(",")[0].split()[-1] if au else work
        return "%s %s" % (last, w.get("year", ""))

    cards, detail = [], {}
    inb = {}
    for e in edges:
        inb.setdefault(e["to"], []).append(e)
    for f in sorted(glob.glob(os.path.join(ddir, "*.claims.json"))):
        pk = load(f)
        vf = os.path.join(ROOT, "data", "verification", "claims", pk["packet"] + ".verdicts.json")
        st = {c["id"]: c["status"] for c in load(vf)["claims"]} if os.path.exists(vf) else {}
        det = {}
        for c in pk["claims"]:
            cid = c["id"]
            if st.get(cid) != "verified" or cid not in scores:
                continue
            sc = scores[cid]
            tps = [t for t in c.get("topics", []) if t in topics] or ["other"]
            tr = next((trad["topic_tradition"][t] for t in tps if t in trad["topic_tradition"]), "unclassified")
            rv = {}
            if tpr:
                for tid in (c.get("theses") or []):
                    for pe in tpr.get(tid, {}).get("persons", []):
                        pid = pe["person_id"]
                        rv[pid] = max(rv.get(pid, 0), pe["relevance_score"])
            else:
                for p, bytype in rel.items():
                    s = bytype.get("claim", {}).get(cid)
                    if s:
                        rv[p] = s["score"]
            links = [e for e in edges if e["from"] == cid or e["to"] == cid]
            contested = any(e["relation"] in ("contradicts", "qualifies") for e in links)
            q0 = c["quotes"][0]
            loc = c.get("pico_locus") or {}
            cards.append({"id": cid, "p": pk["packet"], "who": c["claimant"], "att": c["attribution"], "typ": c["claim_type"],
                          "text": c["text"], "q": words(q0["text"], qmax) if show_q(cid) else "", "w": wl(q0["work"]), "ln": q0["line"],
                          "tp": tps, "tr": tr, "loc": ("%s | %s" % (loc.get("text"), loc.get("ref"))) if loc else "",
                          "hg": c["hedge"], "tier": sc["tier"], "imp": sc["importance"], "ev": sc["evidence_level"],
                          "cx": contested, "oq": len(c.get("open_questions") or []), "rel": rv,
                          "th": c.get("theses") or [], "nl": len(links)})
            det[cid] = {
                "quotes": [{"t": words(q["text"], qmax) if show_q(cid) else "", "w": wl(q["work"]), "work": q["work"], "ln": q["line"], "pg": q.get("page")} for q in c["quotes"]],
                "warrants": [{"k": w["kind"], "t": w["text"], "q": (words(w["quote"]["text"], qmax) if show_q(cid) else "") if w.get("quote") else None,
                              "w": wl(w["quote"]["work"]) if w.get("quote") else None, "ln": w["quote"]["line"] if w.get("quote") else None}
                             for w in c.get("warrants") or []],
                "assumptions": c.get("assumptions") or [],
                "open": [{"k": o["kind"], "t": o["text"]} for o in c.get("open_questions") or []],
                "bears": [{"party": b["party"], "kind": b["kind"], "note": b["note"]} for b in c.get("bears_on") or []],
                "rel": [{"id": e["to"] if e["from"] == cid else e["from"], "r": e["relation"], "dir": "out" if e["from"] == cid else "in", "basis": e.get("basis")} for e in links],
                "hedge_words": c.get("hedge_words") or "", "judged": c.get("judged"),
                "score": {k: sc[k] for k in ("centrality", "corroboration", "contestation", "warrant_strength", "reach", "frame_shift", "importance", "evidence_level", "rank")},
            }
        if det:
            detail[pk["packet"]] = det
    tcount = Counter(t for c in cards for t in c["tp"])
    facets = {
        "topics": [{"id": t, "label": topics[t]["label"], "n": n} for t, n in tcount.most_common()],
        "parties": [{"id": p["id"], "name": p["name"], "colour": p["colour"], "n": sum(1 for c in cards if p["id"] in c["rel"])} for p in parties],
        "traditions": [{"id": k, "label": v["label"], "colour": v["colour"]} for k, v in trad["traditions"].items()],
        "generated_local": a.local, "quote_words": qmax, "quotes_mode": quotes_mode, "quoted_claims": sum(1 for c in cards if c["q"]), "n": len(cards),
    }
    for d in ("data",):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    def dump(p, o):
        with io.open(os.path.join(OUT, p), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(o, fh, ensure_ascii=False, separators=(",", ":"))
    dump("data/cards.json", cards)
    dump("data/facets.json", facets)
    for pk, det in detail.items():
        dump("data/detail-%s.json" % pk, det)
    for src, dst in (("src/css/cards.css", "cards.css"), ("src/js/cards.js", "cards.js"),
                      ("src/js/relations.js", "relations.js"), ("src/js/workbench.js", "workbench.js")):
        shutil.copyfile(os.path.join(ROOT, src), os.path.join(OUT, dst))
    tpr_src = os.path.join(ROOT, "data", "network", "thesis_person_relevance.json")
    if os.path.exists(tpr_src):
        shutil.copyfile(tpr_src, os.path.join(OUT, "data", "thesis_person_relevance.json"))
    banner = ("Local build: full quotations. Do not deploy." if a.local else
              "Scholarly quotations are shown, cut to %d words, only for the %d claims cited in the essays; every claim carries its work and line so it can be checked in the book." % (qmax, sum(1 for c in cards if c["q"])))
    page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scholarship cards - Pico, 900 Conclusions</title>
<link rel="stylesheet" href="%(b)s/css/style.css"><link rel="stylesheet" href="%(b)s/cards/cards.css"></head>
<body><header class="top"><a class="brand" href="%(b)s/">Pico della Mirandola, <em>Conclusiones</em> (1486)</a>
<a href="%(b)s/sections/">Sections</a><a href="%(b)s/condemned/">The thirteen condemned</a><a href="%(b)s/scholarship/">Scholarship</a><a href="%(b)s/essays/">Essays</a><a href="%(b)s/cards/" aria-current="page">Cards</a><a href="%(b)s/about/">Method</a></header>
<main class="wide"><h1>What the scholars say: verified claims as cards</h1>
<p class="meta">%(n)d claims from %(k)d works on Pico's angelology and the One. Every card is a claim whose quotation was re-found in its source by a script; restatements are model paraphrases, sampled by a second reader. %(banner)s</p>
<div id="app" data-base="%(b)s/cards/data/"><noscript>This page needs JavaScript to filter and sort the cards.</noscript></div></main>
<footer>Scores are triage instruments with published weights (docs/CLAIMS_MODEL.md), not measures of truth.</footer>
<script src="%(b)s/cards/cards.js"></script><script src="%(b)s/cards/relations.js"></script><script src="%(b)s/cards/workbench.js"></script></body></html>
""" % {"b": BASE, "n": len(cards), "k": len({c["p"] for c in cards}), "banner": html.escape(banner)}
    with io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print("cards: %d (packets %d); local=%s; wrote %s" % (len(cards), len(detail), a.local, os.path.relpath(OUT, ROOT)))
    print("size cards.json: %.0f KB" % (os.path.getsize(os.path.join(OUT, "data", "cards.json")) / 1024))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
