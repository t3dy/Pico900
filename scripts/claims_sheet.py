#!/usr/bin/env python3
"""claims_sheet.py: a semantic-verification sheet for SPECIFIC claims (targeted verification).

    python scripts/claims_sheet.py --from-commentary docs/angelology/COMMENTARY.md --out data/verification/claims/targeted-commentary.md
    python scripts/claims_sheet.py --ids black2006-b:014 allen2017-venus:031 --out sheet.md
    python scripts/claims_sheet.py --from-commentary FILE --missing-only     only claims with no current `supported` verdict

Why: a commentary may cite only claims that a second reader judged `supported` at their current wording
(commentary_check.py, error `unsampled_ref`). A writer's claims are rarely in the random 20% sample, so the writer's cited
claims are verified as a targeted batch. The verifier writes one file per packet:
    data/verification/claims/<packet>.semantic.<tag>.json     (same format as the sample verdicts; copy each hash)
claims_verify.py merges every `<packet>.semantic*.json`. The sheet lists the claim id, hash, restatement, quotations
(with work:line), warrants and bears_on, grouped by packet so a verifier can write the per-packet files.
"""
import argparse, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_verify as V
import commentary_check as K

ROOT = V.ROOT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--from-commentary")
    ap.add_argument("--out")
    ap.add_argument("--missing-only", action="store_true")
    ap.add_argument("--party", help="every verified claim with a bears_on entry for this party (e.g. ficino)")
    ap.add_argument("--ungrounded-only", action="store_true", help="with --party: only claims whose quotations do not name the party")
    a = ap.parse_args()
    claims, status = K.load_claims()
    ids = list(a.ids)
    if a.from_commentary:
        with io.open(a.from_commentary, encoding="utf-8") as fh:
            for m in K.REF.finditer(fh.read()):
                ids += [x.strip() for x in m.group(1).split("|") if x.strip()]
    if a.party:
        for cid, c in claims.items():
            if status.get(cid) != "verified":
                continue
            if any(b.get("party") == a.party for b in c.get("bears_on") or []):
                ground = V.gn(" ".join(q["text"] for q in c["quotes"]))
                if a.ungrounded_only and V.party_grounded(a.party, ground):
                    continue
                ids.append(cid)
    ids = sorted(set(ids))
    sems = {}
    by_packet = {}
    for i in ids:
        c = claims.get(i)
        if c is None or status.get(i) != "verified":
            print("skip %s: not a verified claim" % i)
            continue
        pk = i.split(":")[0]
        if pk not in sems:
            sems[pk] = V.semantic_verdicts(pk)
        j = sems[pk].get(i)
        ok = bool(j and j.get("hash") == V.chash(c) and j.get("verdict") == "supported")
        if a.missing_only and ok:
            continue
        by_packet.setdefault(pk, []).append(c)
    lines = ["# Targeted semantic verification sheet", "",
             "For each claim: does `text` say no more than the quotations support (read them in context: `python scripts/corpus_tool.py show WORK FROM TO`)? "
             "Verdict supported / overreaches / wrong, one-line reason, `suggested_text` if it overreaches. Judge attribution, hedge and bears_on too. "
             "Write one file per packet: data/verification/claims/<packet>.semantic.<tag>.json (format: docs/briefs/claims_semantic_verifier.md), copying each hash.", ""]
    n = 0
    for pk in sorted(by_packet):
        lines.append("# Packet %s (%d claims)" % (pk, len(by_packet[pk])))
        lines.append("")
        for c in by_packet[pk]:
            n += 1
            lines.append("## %s  hash: %s  (%s, %s, %s)" % (c["id"], V.chash(c), c["claimant"], c["attribution"], c["hedge"]))
            lines.append("")
            lines.append("**Restatement:** " + c["text"])
            lines.append("")
            for q in c["quotes"]:
                lines.append("> %s\n> (%s:%s)\n" % (q["text"], q["work"], q["line"]))
            for w in c.get("warrants") or []:
                lines.append("- warrant [%s]: %s" % (w["kind"], w["text"]))
            for b in c.get("bears_on") or []:
                lines.append("- bears on %s (%s): %s" % (b["party"], b["kind"], b["note"]))
            lines.append("")
    text = "\n".join(lines)
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote %s: %d claims in %d packets" % (a.out, n, len(by_packet)))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
