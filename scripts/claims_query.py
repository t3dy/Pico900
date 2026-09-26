#!/usr/bin/env python3
"""claims_query.py: read VERIFIED claims compactly (for LINKER, WRITER, cards, and you).

    python scripts/claims_query.py --topic three-worlds                 ids, claimant, hedge, restatement
    python scripts/claims_query.py --claimant Black --full              plus quotations, warrants, open questions
    python scripts/claims_query.py --locus "heptaplus" --text "Anaxagoras"
    python scripts/claims_query.py --party ficino --min-importance 20   claims bearing on a party
    python scripts/claims_query.py --id black2006-b:014 --full          one claim
    python scripts/claims_query.py --topics                             topic list with claim counts
    python scripts/claims_query.py --stats                              claims per packet and per claimant

Only claims that passed claims_verify.py are shown (verdict `verified` and no semantic error). Importance comes from
scores.json when it exists. Output is plain text so an agent can read it without opening 5,000-line JSON.
"""
import argparse, glob, io, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def verified_claims(domain="angelology"):
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "claims", domain, "*.claims.json"))):
        p = load(f)
        vf = os.path.join(ROOT, "data", "verification", "claims", p["packet"] + ".verdicts.json")
        st = {c["id"]: c["status"] for c in load(vf)["claims"]} if os.path.exists(vf) else {}
        for c in p["claims"]:
            if st.get(c["id"]) == "verified":
                c["_packet"] = p["packet"]
                out[c["id"]] = c
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="angelology")
    ap.add_argument("--topic"); ap.add_argument("--claimant"); ap.add_argument("--locus"); ap.add_argument("--party")
    ap.add_argument("--text"); ap.add_argument("--id"); ap.add_argument("--packet"); ap.add_argument("--attribution")
    ap.add_argument("--min-importance", type=float, default=0)
    ap.add_argument("--full", action="store_true"); ap.add_argument("--topics", action="store_true"); ap.add_argument("--stats", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    cl = verified_claims(a.domain)
    sc = {}
    sp = os.path.join(ROOT, "data", "claims", a.domain, "scores.json")
    if os.path.exists(sp):
        sc = load(sp)["claims"]
    if a.topics:
        cnt = Counter(t for c in cl.values() for t in c.get("topics", []))
        for t, n in cnt.most_common():
            print("%4d  %s" % (n, t))
        return 0
    if a.stats:
        print("verified claims:", len(cl))
        for k, n in Counter(c["_packet"] for c in cl.values()).most_common():
            print("%5d  %s" % (n, k))
        for k, n in Counter(c["claimant"] for c in cl.values()).most_common():
            print("%5d  claimant %s" % (n, k))
        return 0
    rx = re.compile(a.text, re.I) if a.text else None
    rows = []
    for cid, c in cl.items():
        if a.id and cid != a.id: continue
        if a.packet and c["_packet"] != a.packet: continue
        if a.topic and a.topic not in c.get("topics", []): continue
        if a.claimant and a.claimant.lower() not in c["claimant"].lower(): continue
        if a.attribution and c["attribution"] != a.attribution: continue
        if a.locus and a.locus.lower() not in json.dumps(c.get("pico_locus") or {}).lower(): continue
        if a.party and not any(b.get("party") == a.party for b in c.get("bears_on", [])): continue
        if rx and not (rx.search(c["text"]) or any(rx.search(q["text"]) for q in c["quotes"])): continue
        imp = sc.get(cid, {}).get("importance", 0)
        if imp < a.min_importance: continue
        rows.append((imp, cid, c))
    rows.sort(key=lambda r: (-r[0], r[1]))
    for imp, cid, c in rows[: a.limit or None]:
        pl = c.get("pico_locus") or {}
        print("%s | %s | %s | %s%s" % (cid, c["claimant"], c["hedge"], c["text"], ("  [imp %.0f]" % imp) if imp else ""))
        if a.full:
            print("    locus: %s %s | topics: %s | type: %s | attribution: %s" % (pl.get("text"), pl.get("ref"), ",".join(c.get("topics", [])), c["claim_type"], c["attribution"]))
            for q in c["quotes"]:
                print("    > %s  (%s:%s)" % (q["text"], q["work"], q["line"]))
            for w in c.get("warrants") or []:
                print("    warrant [%s] %s" % (w["kind"], w["text"]))
            for o in c.get("open_questions") or []:
                print("    open [%s] %s" % (o["kind"], o["text"]))
            for b in c.get("bears_on") or []:
                print("    bears on %s (%s): %s" % (b["party"], b["kind"], b["note"]))
            print()
    print("-- %d claims" % len(rows))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
