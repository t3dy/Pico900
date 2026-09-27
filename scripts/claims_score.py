#!/usr/bin/env python3
"""claims_score.py: verify links, score claims, aggregate to topics and loci, compute relevance to Pico's relationships.

    python scripts/claims_score.py [--domain angelology]

Reads    data/claims/<domain>/*.claims.json   and   data/verification/claims/*.verdicts.json (verified claims only)
         data/claims/<domain>/*.links.json    (cross-claim relations; each link must state its basis)
         data/claims/scoring.json, parties.json, topics.json
Writes   data/claims/<domain>/scores.json        per claim: components and importance, tier; per topic; per locus
         data/claims/<domain>/relevance.json     per party: card type -> card id -> {score, evidence, basis}
         data/claims/<domain>/open_questions.json  every open question of every verified claim, ranked by parent importance
         data/claims/<domain>/graph.json         nodes and edges of the claim graph (for the site's relational views)

The formulas are in docs/CLAIMS_MODEL.md s5 and s7. Only VERIFIED claims are scored; a claim that needs a fix is listed
under `excluded` and never appears in a score, a link or a card. Every output records the weights it used.
"""
import argparse, glob, io, json, os, sys
from datetime import datetime, timezone
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpuslib as C
import claims_verify as V

UNGROUNDED = 0.4   # weight of a relationship tag whose party is named in no quotation of the claim (an inference)
RELATIONS = {"supports", "contradicts", "qualifies", "depends_on", "same_claim", "cites"}


def load(p):
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dump(p, o):
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(o, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def norm01(vals):
    m = max(vals.values()) if vals else 0
    return {k: (v / m if m else 0.0) for k, v in vals.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="angelology")
    a = ap.parse_args()
    cfg = load(os.path.join(ROOT, "data", "claims", "scoring.json"))
    W, WW, KW = cfg["importance_weights"], cfg["warrant_weights"], cfg["relevance_kind_weights"]
    ddir = os.path.join(ROOT, "data", "claims", a.domain)
    claims, excluded, packets = {}, [], {}
    for f in sorted(glob.glob(os.path.join(ddir, "*.claims.json"))):
        p = load(f)
        packets[p["packet"]] = p
        vf = os.path.join(ROOT, "data", "verification", "claims", p["packet"] + ".verdicts.json")
        status = {}
        if os.path.exists(vf):
            status = {c["id"]: c["status"] for c in load(vf)["claims"]}
        for c in p["claims"]:
            if status.get(c["id"]) == "verified":
                claims[c["id"]] = c
            else:
                excluded.append({"id": c["id"], "reason": status.get(c["id"], "no verdict: run claims_verify.py")})
    edges, bad_links = [], []
    for c in claims.values():
        for r in c.get("relations_local") or []:
            edges.append({"from": c["id"], "to": r.get("to"), "relation": r.get("relation"), "basis": r.get("basis"), "src": "local"})
    for f in sorted(glob.glob(os.path.join(ddir, "*.links.json"))):
        for l in load(f).get("links", []):
            edges.append({"from": l.get("from"), "to": l.get("to"), "relation": l.get("relation"), "basis": l.get("basis"), "src": os.path.basename(f), "id": l.get("id")})
    good = []
    for e in edges:
        why = None
        if e["from"] not in claims or e["to"] not in claims:
            why = "endpoint missing or not verified"
        elif e["relation"] not in RELATIONS:
            why = "unknown relation"
        elif not e.get("basis"):
            why = "no basis stated"
        elif e["from"] == e["to"]:
            why = "self link"
        if why:
            bad_links.append({**e, "problem": why})
        else:
            good.append(e)
    deg, corr, contest = defaultdict(int), defaultdict(set), defaultdict(float)
    for e in good:
        a_, b_ = claims[e["from"]], claims[e["to"]]
        deg[e["from"]] += 1; deg[e["to"]] += 1
        if e["relation"] in ("same_claim", "supports"):
            corr[e["from"]].update([a_["claimant"], b_["claimant"]]); corr[e["to"]].update([a_["claimant"], b_["claimant"]])
        if e["relation"] in ("contradicts", "qualifies") and a_["claimant"] != b_["claimant"]:
            v = 1.0 if e["relation"] == "contradicts" else 0.5
            contest[e["from"]] = max(contest[e["from"]], v); contest[e["to"]] = max(contest[e["to"]], v)
    comp = {}
    for cid, c in claims.items():
        if c["attribution"] == "primary_text":
            ws = 1.0
        else:
            ws_list = [WW.get(w["kind"], 0) for w in c.get("warrants") or []]
            ws = sum(ws_list) / len(ws_list) if ws_list else WW["none"]
        # evidence level on the network system's scale (docs/INTELLECTUAL_NETWORK_DESIGN.md Part 8):
        # 5 Pico's own verified words; 4 a scholar's claim warranted by Pico's text; 3 warranted by other scholarship;
        # 2 an assertion without stated warrant; 1 anything the source itself hedges as speculative. A hedge caps at 2.
        kinds = {w["kind"] for w in c.get("warrants") or []}
        if c["attribution"] == "primary_text":
            ev = 5
        elif "primary_text" in kinds:
            ev = 4
        elif "scholar_evidence" in kinds:
            ev = 3
        else:
            ev = 2
        if c["hedge"] == "hedged":
            ev = min(ev, 2)
        elif c["hedge"] == "speculative":
            ev = 1
        comp[cid] = {
            "evidence_level": ev,
            "centrality": deg[cid],
            "corroboration": max(1, len(corr[cid] | {c["claimant"]})),
            "contestation": contest[cid],
            "warrant_strength": round(ws, 3),
            "reach": min(1.0, (len(c.get("topics") or []) + len(c.get("bears_on") or [])) / cfg["reach_cap"]),
            "frame_shift": (c.get("judged") or {}).get("frame_shift", 0) / 3.0,
            "frame_shift_is_judged": True,
            "open_question_load": len(c.get("open_questions") or []),
        }
    ncent = norm01({k: v["centrality"] for k, v in comp.items()})
    ncorr = norm01({k: v["corroboration"] - 1 for k, v in comp.items()})
    for cid, m in comp.items():
        m["importance"] = round(100 * (W["centrality"] * ncent[cid] + W["corroboration"] * ncorr[cid] + W["contestation"] * m["contestation"] +
                                       W["warrant_strength"] * m["warrant_strength"] + W["reach"] * m["reach"] + W["frame_shift"] * m["frame_shift"]), 1)
    order = sorted(comp, key=lambda k: (-comp[k]["importance"], k))
    n = len(order)
    cut1, cut2 = int(round(n * cfg["tiers"]["primary"])), int(round(n * (cfg["tiers"]["primary"] + cfg["tiers"]["secondary"])))
    for i, cid in enumerate(order):
        comp[cid]["tier"] = "primary" if i < cut1 else "secondary" if i < cut2 else "tertiary"
        comp[cid]["rank"] = i + 1

    def aggregate(keyf):
        groups = defaultdict(list)
        for cid, c in claims.items():
            for k in keyf(c):
                groups[k].append(cid)
        out = {}
        for k, ids in groups.items():
            top = sorted((comp[i]["importance"] for i in ids), reverse=True)[:3]
            out[k] = {"claims": len(ids), "importance": round(sum(top) / len(top), 1), "top_claims": sorted(ids, key=lambda i: -comp[i]["importance"])[:5],
                      "claimants": sorted({claims[i]["claimant"] for i in ids}), "primary_claims": sum(1 for i in ids if comp[i]["tier"] == "primary")}
        return out
    topics = aggregate(lambda c: c.get("topics") or [])
    loci = aggregate(lambda c: ["%s | %s" % ((c.get("pico_locus") or {}).get("text"), (c.get("pico_locus") or {}).get("ref"))] if c.get("pico_locus") else [])
    theses = aggregate(lambda c: c.get("theses") or [])
    # relevance to Pico's relationships: earned by verified claims that bear on the party
    parties = {p["id"]: p for p in load(os.path.join(ROOT, "data", "claims", "parties.json"))["parties"]}
    unknown_parties = set()
    raw = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"sum": 0.0, "evidence": []})))
    for cid, c in claims.items():
        for b in c.get("bears_on") or []:
            if b["party"] not in parties:
                unknown_parties.add(b["party"])
            ground = V.gn(" ".join(q["text"] for q in c["quotes"]))
            gr = V.party_grounded(b["party"], ground)
            w = KW.get(b["kind"], 0.4) * comp[cid]["importance"] / 100.0 * (1.0 if gr else UNGROUNDED)
            cards = [("claim", cid)]
            cards += [("topic", t) for t in c.get("topics") or []]
            cards += [("thesis", t) for t in c.get("theses") or []]
            if c.get("pico_locus"):
                cards.append(("locus", "%s | %s" % (c["pico_locus"].get("text"), c["pico_locus"].get("ref"))))
            for ctype, key in cards:
                r = raw[b["party"]][ctype][key]
                r["sum"] += w
                r["evidence"].append({"claim": cid, "kind": b["kind"], "note": b["note"], "grounded": gr})
    relevance = {}
    for party, bytype in raw.items():
        relevance[party] = {}
        for ctype, cards in bytype.items():
            m = max(v["sum"] for v in cards.values())
            relevance[party][ctype] = {k: {"score": round(v["sum"] / m, 3), "n_claims": len(v["evidence"]), "evidence": v["evidence"],
                                          "basis": "sum of kind_weight x importance over verified claims bearing on this party, scaled to the party's maximum for this card type"}
                                       for k, v in sorted(cards.items(), key=lambda kv: -kv[1]["sum"])}
    oq = []
    for cid, c in claims.items():
        for o in c.get("open_questions") or []:
            oq.append({"claim": cid, "id": o.get("id"), "kind": o["kind"], "text": o["text"], "basis_quote": o.get("basis_quote"),
                       "topics": c.get("topics"), "parent_importance": comp[cid]["importance"], "claimant": c["claimant"]})
    oq.sort(key=lambda o: -o["parent_importance"])
    stamp = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "weights": cfg}
    dump(os.path.join(ddir, "scores.json"), {**stamp, "claims": comp, "topics": topics, "loci": loci, "theses": theses, "excluded": excluded,
                                             "rejected_links": bad_links})
    dump(os.path.join(ddir, "relevance.json"), {**stamp, "parties": relevance, "unknown_parties": sorted(unknown_parties)})
    dump(os.path.join(ddir, "open_questions.json"), {**stamp, "open_questions": oq})
    dump(os.path.join(ddir, "graph.json"), {**stamp, "nodes": [{"id": k, "claimant": c["claimant"], "topics": c.get("topics"), "tier": comp[k]["tier"], "importance": comp[k]["importance"]} for k, c in claims.items()], "edges": good})
    print("verified claims %d, excluded %d, links ok %d rejected %d, open questions %d" % (len(claims), len(excluded), len(good), len(bad_links), len(oq)))
    for cid in order[:12]:
        print("  %5.1f %-9s %s  %s" % (comp[cid]["importance"], comp[cid]["tier"], cid, claims[cid]["text"][:90]))
    for party, bytype in sorted(relevance.items()):
        print("  relevance[%s]: %s" % (party, {t: len(v) for t, v in bytype.items()}))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
