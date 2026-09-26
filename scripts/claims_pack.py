#!/usr/bin/env python3
"""claims_pack.py: the RESEARCHER's write-and-check loop for one packet.

A researcher appends ONE claim per line (JSON) to      data/claims/_work/<packet>.jsonl
and, when useful, keeps packet-level notes in           data/claims/_work/<packet>.meta.json
    {"researcher": "...", "scope": {"work": "...", "line_start": 1, "line_end": 900},
     "not_mined": ["..."], "proposed_topics": [], "proposed_parties": [], "notes": "..."}

    python scripts/claims_pack.py PACKET [--domain angelology]

It (1) parses every line and reports JSON errors by line number, (2) numbers claims that lack an id
(`<packet>:<nnn>`), (3) repairs wrong line numbers in place (the only edit it ever makes to your claims),
(4) writes data/claims/<domain>/<packet>.claims.json, (5) runs claims_verify on it and prints the tickets:
what failed, and the nearest real text in the source. Repeat until it prints `needs_fix 0`.
Append-only JSONL means an interrupted session loses nothing: recovery is "run claims_pack again".
"""
import argparse, io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_verify as V
import corpuslib as C

ROOT = C.ROOT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packet")
    ap.add_argument("--domain", default="angelology")
    a = ap.parse_args()
    work = os.path.join(ROOT, "data", "claims", "_work")
    src = os.path.join(work, a.packet + ".jsonl")
    if not os.path.exists(src):
        print("no such file: %s (append claims there, one JSON object per line)" % src)
        return 2
    claims, bad = [], 0
    with io.open(src, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                claims.append(json.loads(line))
            except ValueError as e:
                bad += 1
                print("JSON ERROR line %d of %s: %s" % (n, os.path.basename(src), e))
    if bad:
        print("fix the %d unparseable line(s) first; nothing written" % bad)
        return 2
    used = {c.get("id") for c in claims if c.get("id")}
    k = 0
    for c in claims:
        if not c.get("id"):
            k += 1
            while "%s:%03d" % (a.packet, k) in used:
                k += 1
            c["id"] = "%s:%03d" % (a.packet, k)
            used.add(c["id"])
    meta = {}
    mp = os.path.join(work, a.packet + ".meta.json")
    if os.path.exists(mp):
        with io.open(mp, encoding="utf-8") as fh:
            meta = json.load(fh)
    # repair locators in place (mechanical); rewrite the jsonl only if something moved
    moved = 0
    for c in claims:
        before = json.dumps(c, sort_keys=True)
        V.check_claim(c, a.packet, True, False)
        if json.dumps(c, sort_keys=True) != before:
            moved += 1
    with io.open(src, "w", encoding="utf-8", newline="\n") as fh:
        for c in claims:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    packet = {"packet": a.packet, "researcher": meta.get("researcher", ""), "created": meta.get("created", ""),
              "scope": meta.get("scope"), "claims": claims, "not_mined": meta.get("not_mined", []),
              "proposed_topics": meta.get("proposed_topics", []), "proposed_parties": meta.get("proposed_parties", []),
              "notes": meta.get("notes", "")}
    outdir = os.path.join(ROOT, "data", "claims", a.domain)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, a.packet + ".claims.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(packet, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    res, _, _ = V.verify_packet(out, False, False)
    V.os.makedirs(V.VERDICTS, exist_ok=True)
    with io.open(os.path.join(V.VERDICTS, a.packet + ".verdicts.json"), "w", encoding="utf-8", newline="\n") as fh:
        res["summary"] = {}
        json.dump(res, fh, indent=1, ensure_ascii=False)
    nv = sum(1 for c in res["claims"] if c["status"] == "verified")
    print("packet %s: %d claims, verified %d, needs_fix %d (locators repaired in %d)" % (a.packet, len(claims), nv, len(claims) - nv, moved))
    shown = 0
    for c in res["claims"]:
        for i in c["issues"]:
            if i["severity"] == "error" and shown < 40:
                shown += 1
                print("  %s  %s  [%s]  %s" % (c["id"], i["code"], i["where"], i["detail"]))
                if i.get("suggested_excerpt"):
                    print("      nearest real text (line %s): %s" % (i.get("suggested_line"), i["suggested_excerpt"][:400]))
    warn = sum(1 for c in res["claims"] for i in c["issues"] if i["severity"] == "warn")
    if warn:
        print("  (%d warnings: run `python scripts/claims_verify.py %s` for the list)" % (warn, os.path.relpath(out, ROOT)))
    return 0 if nv == len(claims) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
