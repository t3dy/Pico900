#!/usr/bin/env python3
"""claims_apply_semantic.py: apply the semantic verifier's suggested rewrites (docs/CLAIMS_MODEL.md s6).

    python scripts/claims_apply_semantic.py [--dry-run]

For every `overreaches` verdict in data/verification/claims/*.semantic.json whose hash still matches the claim as it stands and
which carries a `suggested_text`, replace the claim's `text` in the packet's _work JSONL with the suggestion, then re-pack and
re-verify the packet. The changed claim has a new hash, so it is no longer covered by the old verdict and is sampled again
first (claims_verify.py puts edited claims at the head of the next sample sheet). The rewrite is the VERIFIER's words, not
the researcher's and not mine.

Not applied, and listed for a human or fixer agent: verdicts `wrong`; overreaches without `suggested_text`; overreaches whose
reason concerns `bears_on`, `attribution`, `hedge`, `warrant` or `frame_shift` fields (those need a different edit than the
restatement).
"""
import argparse, glob, io, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import claims_verify as V

ROOT = V.ROOT
FIELDS = re.compile(r"bears_on|attribution|hedge field|warrant|frame_shift|claimant", re.I)


def usable_rewrite(row, new):
    """A verifier's `suggested_text` must be a RESTATEMENT. Some verifiers put an editing instruction there ("Text unchanged. Drop or
    re-anchor the bears_on."): writing that into the claim wrecks it (happened 2026-09-28: 17 claims). Refuse anything that is not a
    plausible standalone sentence about the source, is (nearly) the current text, or talks about fields."""
    n = (new or "").strip()
    if len(n) < 40 or n == (row.get("text") or "").strip():
        return False
    if re.match(r"(?i)^(text|no change|unchanged|keep|drop|remove|delete|re-?anchor|fix|change|replace|see |n/a|none)", n):
        return False
    if re.search(r"(?i)bears_on|re-?anchor|quote_index|the hedge|this claim|verdict|suggested", n):
        return False
    return len(n.split()) >= 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    applied, manual, touched, dropped_tags = 0, [], set(), 0
    for sf in sorted(glob.glob(os.path.join(V.VERDICTS, "*.semantic*.json"))):
        sem = V.load(sf)
        packet = sem["packet"]
        jp = os.path.join(ROOT, "data", "claims", "_work", packet + ".jsonl")
        if not os.path.exists(jp):
            continue
        rows = [json.loads(l) for l in io.open(jp, encoding="utf-8") if l.strip()]
        pk = V.load(os.path.join(ROOT, "data", "claims", "angelology", packet + ".claims.json"))
        byid = {c["id"]: c for c in pk["claims"]}
        idx = {r.get("id"): r for r in rows if r.get("id")}
        for j in sem.get("judged", []):
            if j.get("verdict") not in ("overreaches", "wrong"):
                continue
            c = byid.get(j["id"])
            if c is None or V.chash(c) != j.get("hash"):
                continue                                    # already edited since the verdict
            r = idx.get(j["id"])
            if j["verdict"] == "wrong" or r is None:
                manual.append((j["id"], j["verdict"], j.get("reason", "")[:160]))
                continue
            reason = j.get("reason", "")
            done = False
            # 1. restatement rewrite: the verifier's own words. Applied even when the reason also mentions other fields.
            if j.get("suggested_text") and not usable_rewrite(r, j["suggested_text"]):
                manual.append((j["id"], j["verdict"], "[suggested_text is not a restatement: %r] %s" % (j["suggested_text"][:60], reason[:90])))
            elif j.get("suggested_text"):
                if not a.dry_run:
                    r["text"] = j["suggested_text"]
                done = True
            # 2. relationship tags: when the reason mentions bears_on, drop exactly the tags whose party no quotation names
            #    (the deterministic grounding test the scorer uses). Never invents or rewrites a tag.
            if re.search(r"bears_on", reason, re.I) and r.get("bears_on"):
                ground = V.gn(" ".join(q.get("text", "") for q in r.get("quotes", []) if isinstance(q, dict)))
                keep = [b for b in r["bears_on"] if V.party_grounded(b.get("party", ""), ground)]
                if len(keep) != len(r["bears_on"]):
                    if not a.dry_run:
                        r["bears_on"] = keep
                        r["revision"] = int(r.get("revision", 0)) + 1
                    done = True
                    dropped_tags += len(r["bears_on"]) - len(keep) if a.dry_run else 0
            # 3. anything else the reason names (attribution, hedge, warrant, frame_shift, claimant, locus) needs a person
            other = re.search(r"attribution|hedge field|hedge wrong|`hedge`|warrant|frame_shift|claimant|pico_locus", reason, re.I)
            if other or not done:
                manual.append((j["id"], j["verdict"], ("[partly applied] " if done else "") + reason[:150]))
            if done and not a.dry_run:
                touched.add(packet)
            applied += 1 if done else 0
        if not a.dry_run and packet in touched:
            with io.open(jp, "w", encoding="utf-8", newline="\n") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("rewrites %s: %d" % ("found" if a.dry_run else "applied", applied))
    for m in manual:
        print("MANUAL %s [%s] %s" % m)
    if not a.dry_run:
        for packet in sorted(touched):
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "claims_pack.py"), packet], capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr.strip()[:200])
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
