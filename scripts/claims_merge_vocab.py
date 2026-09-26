#!/usr/bin/env python3
"""claims_merge_vocab.py: the orchestrator's merge of topics and parties (the researchers may only propose).

    python scripts/claims_merge_vocab.py [--domain angelology] [--write]

Collects (1) every topic id and party slug actually USED in claims, and (2) every `proposed_topics` / `proposed_parties`
in packets and their _work/*.meta.json, and reports which are missing from data/claims/topics.json and parties.json.
With --write it adds them (label from the proposal; otherwise "(used in packets: N claims)") and marks each `proposed: true`
so an editor can rename or fold them. Never removes or renames an existing entry. One writer per file: only this
script and the orchestrator touch topics.json and parties.json.
"""
import argparse, glob, io, json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="angelology")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    tp, pp = os.path.join(ROOT, "data", "claims", "topics.json"), os.path.join(ROOT, "data", "claims", "parties.json")
    topics, parties = load(tp), load(pp)
    have_t = {t["id"] for t in topics["topics"]}
    have_p = {p["id"] for p in parties["parties"]}
    used_t, used_p, prop_t, prop_p = Counter(), Counter(), {}, {}
    files = glob.glob(os.path.join(ROOT, "data", "claims", a.domain, "*.claims.json"))
    for f in files:
        p = load(f)
        for c in p["claims"]:
            used_t.update(c.get("topics") or [])
            used_p.update(b.get("party") for b in c.get("bears_on") or [])
        for t in p.get("proposed_topics") or []:
            prop_t.setdefault(t["id"], t.get("label", ""))
        for q in p.get("proposed_parties") or []:
            prop_p.setdefault(q["id"], q.get("name", ""))
    for f in glob.glob(os.path.join(ROOT, "data", "claims", "_work", "*.meta.json")):
        m = load(f)
        for t in m.get("proposed_topics") or []:
            prop_t.setdefault(t["id"], t.get("label", ""))
        for q in m.get("proposed_parties") or []:
            prop_p.setdefault(q["id"], q.get("name", ""))
    new_t = {k: n for k, n in used_t.items() if k not in have_t}
    new_p = {k: n for k, n in used_p.items() if k and k not in have_p}
    print("topics used but not in topics.json:", dict(new_t) or "none")
    print("parties used but not in parties.json:", dict(new_p) or "none")
    print("proposed topics not yet merged:", [k for k in prop_t if k not in have_t and k not in new_t] or "none")
    print("proposed parties not yet merged:", [k for k in prop_p if k not in have_p and k not in new_p] or "none")
    if a.write:
        for k in sorted(set(new_t) | {k for k in prop_t if k not in have_t}):
            topics["topics"].append({"id": k, "label": prop_t.get(k) or "(used in packets: %d claims)" % used_t.get(k, 0), "proposed": True})
        for k in sorted(set(new_p) | {k for k in prop_p if k not in have_p}):
            parties["parties"].append({"id": k, "name": prop_p.get(k) or k, "proposed": True})
        for path, obj in ((tp, topics), (pp, parties)):
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(obj, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        print("written: topics %d, parties %d" % (len(topics["topics"]), len(parties["parties"])))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
