#!/usr/bin/env python3
"""claims_verify.py: the mechanical VERIFIER for claim packets. Opens the sources; never trusts the writer.

    python scripts/claims_verify.py                       # verify every data/claims/**/*.claims.json
    python scripts/claims_verify.py PACKET.claims.json    # one packet
    python scripts/claims_verify.py --fix-locators        # rewrite wrong line numbers to the true line (only that)
    python scripts/claims_verify.py --strict              # ungrounded names/years count as errors
    python scripts/claims_verify.py --quiet               # summary only

Writes   data/verification/claims/<packet>.verdicts.json   (one verdict per claim, per quote, per warrant)
         data/claims/tickets/<packet>.tickets.json         (what to fix, with the nearest real text from the source)
Exit 1 if any claim needs a fix. A schema check is not verification: this opens the source and re-finds every
quotation (`corpuslib.locate`). What it cannot judge (does the restatement fairly summarise the quotation?) is
sampled by a second agent from `data/verification/claims/<packet>.sample.md`.

Self-correction loop (docs/CLAIMS_MODEL.md s6): RESEARCHER writes packet -> this script -> tickets ->
RESEARCHER (or a fixer) applies the tickets -> this script again, until clean. A claim with an error is never scored,
linked or cited.
"""
import argparse, glob, io, json, os, re, sys, random
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpuslib as C

ROOT = C.ROOT
CLAIM_GLOB = os.path.join(ROOT, "data", "claims", "**", "*.claims.json")
VERDICTS = os.path.join(ROOT, "data", "verification", "claims")
TICKETS = os.path.join(ROOT, "data", "claims", "tickets")
PRIMARY_WORKS = {"borghesi2012", "wallis1965", "heptaplus_it", "lettere", "farmer1998"}
ATTRIBUTION = {"scholar_claim", "scholar_report", "primary_text"}
CLAIM_TYPE = {"doctrinal_content", "source_identification", "interpretive_position", "historical_event",
              "textual_crux", "method", "reception"}
HEDGE = {"assertive", "hedged", "speculative"}
WARRANT_KIND = {"primary_text", "scholar_evidence", "argument", "authority", "inference"}
OQ_KIND = {"evidence_gap", "interpretive", "textual", "chronological", "scope"}
REL_KIND = {"quarrel", "correspondence", "patronage", "teaching", "source", "reception", "friendship", "trial", "other"}
STOP = set("""The This That These Those There Their They Then Thus Here When Where While What Which Whose Who Because
Although However Both Each Such Some Many Most Other Another After Before During Between Against Within Without
Pico Pico's God Heptaplus Oration Commento Conclusiones Apologia Book Chapter Exposition Proem Genesis Bible
Latin Greek Hebrew Italian Christian Platonic Platonist Neoplatonic Aristotelian Kabbalistic Dionysian Thomist
Renaissance Florence Florentine Rome Roman""".split())
YEAR = re.compile(r"\b1[0-9]{3}\b")
NAME = re.compile(r"\b[A-Z][A-Za-zÀ-ſ'’-]{3,}\b")


def load(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def chash(c):
    """Identity of what a semantic reader judged: the restatement plus its quotations."""
    import hashlib
    body = c.get("text", "") + "|" + "|".join(q.get("text", "") for q in c.get("quotes", []) if isinstance(q, dict))
    if c.get("revision"):
        body += "|rev%s" % c["revision"]   # bump `revision` whenever any field of a judged claim is edited (bears_on, hedge, ...)
    return hashlib.sha1(body.encode("utf-8")).hexdigest()[:10]


def semantic_verdicts(packet):
    """data/verification/claims/<packet>.semantic.json, written by the second (semantic) verifier:
    {"packet": ..., "verifier": ..., "judged": [{"id", "hash", "verdict": supported|overreaches|wrong, "reason", "suggested_text"}]}"""
    out = {}
    # <packet>.semantic.json (the random sample) and <packet>.semantic.<tag>.json (targeted verification of cited
    # claims). Files are applied oldest-mtime-first so the most RECENTLY WRITTEN verdict wins for a given claim id,
    # regardless of filename (a plain ".semantic.json" sorts after ".semantic.confirm.json" alphabetically, which
    # would silently resurrect a stale overreach verdict the confirm file was meant to supersede -- caught 2026-09-27
    # when a fixed, re-judged claim kept failing commentary_check.py because the old sample file's verdict still won).
    files = sorted(glob.glob(os.path.join(VERDICTS, packet + ".semantic*.json")), key=lambda p: os.path.getmtime(p))
    for p in files:
        for j in load(p).get("judged", []):
            out[j["id"]] = j
    return out


def gn(s):
    return C.norm(s, digits=True)


PARTY_TOKENS = None


def party_tokens(party):
    """Name tokens by which a party would be recognised in a quotation (from data/claims/parties.json)."""
    global PARTY_TOKENS
    if PARTY_TOKENS is None:
        PARTY_TOKENS = {}
        pp = os.path.join(ROOT, "data", "claims", "parties.json")
        skip = {"papal", "pope", "the", "1487", "della", "medici"}
        for q in load(pp)["parties"]:
            toks = [gn(t) for t in q["name"].replace("'", " ").split()]
            PARTY_TOKENS[q["id"]] = [t for t in toks if len(t) >= 5 and t not in skip] or toks
            PARTY_TOKENS[q["id"]] += [gn(x) for x in q.get("aliases", [])]
    return PARTY_TOKENS.get(party, [gn(party)])


def party_grounded(party, ground):
    return any(t and t in ground for t in party_tokens(party))


def grounded(n, ground):
    """Is the normalised name/number present in the evidence, allowing derived forms (Neoplatonism/Neoplatonic,
    Oratio/Oration, plurals)? Numbers must match exactly."""
    if n in ground:
        return True
    if n.isdigit():
        return False
    stem = n[: max(5, len(n) - 3)]
    return len(n) >= 6 and stem in ground


def check_quote(q, where, issues, attribution, claimant, fix):
    """Verify one quote object {text, work, line}. Returns the verdict dict."""
    if not isinstance(q, dict) or not q.get("text") or not q.get("work"):
        issues.append({"code": "schema", "severity": "error", "where": where, "detail": "quote needs text, work, line"})
        return {"verdict": "invalid"}
    work, line = q["work"], q.get("line")
    try:
        v = C.locate(work, q["text"], near=line if isinstance(line, int) else None)
    except (KeyError, FileNotFoundError) as e:
        issues.append({"code": "unknown_work", "severity": "error", "where": where, "detail": str(e)})
        return {"verdict": "invalid"}
    words = len(q["text"].split())
    if v["verdict"] in ("altered", "not_found", "untestable"):
        iss = {"code": "quote_" + v["verdict"], "severity": "error", "where": where,
               "detail": "the quotation is %s in %s" % (v["verdict"].replace("_", " "), work), "verdict": v}
        if v.get("best_match"):
            iss["suggested_line"] = v["best_match"]["line_start"]
            iss["suggested_excerpt"] = v["best_match"]["excerpt"]
        issues.append(iss)
    else:
        if not isinstance(line, int):
            issues.append({"code": "schema", "severity": "error", "where": where, "detail": "quote.line must be an integer"})
        elif abs(v["line_start"] - line) > 10:
            issues.append({"code": "quote_locator_wrong", "severity": "error" if not fix else "info", "where": where,
                           "detail": "cited line %s, quotation found at %s" % (line, v["line_start"]),
                           "suggested_line": v["line_start"], "fixable": True})
            if fix:
                q["locator_corrected_from"] = line
                q["line"] = v["line_start"]
        if v.get("warning"):
            issues.append({"code": "quote_fragments_far", "severity": "warn", "where": where, "detail": v["warning"]})
        if v.get("occurrences", 1) > 1 and words < 12:
            issues.append({"code": "quote_ambiguous", "severity": "warn", "where": where,
                           "detail": "short phrase occurs %d times; the locator disambiguates" % v["occurrences"]})
    if words > 120:
        issues.append({"code": "quote_too_long", "severity": "warn", "where": where, "detail": "%d words; quote what the claim needs" % words})
    if words < 4:
        issues.append({"code": "quote_too_short", "severity": "warn", "where": where, "detail": "%d words is too little to test" % words})
    is_primary = work in PRIMARY_WORKS
    if attribution == "primary_text" and not is_primary:
        issues.append({"code": "primary_from_scholar", "severity": "error", "where": where,
                       "detail": "attribution primary_text but %s is a scholarly work, not an edition of Pico" % work})
    if attribution in ("scholar_claim", "scholar_report") and is_primary:
        issues.append({"code": "scholar_from_edition", "severity": "warn", "where": where,
                       "detail": "scholar claim quoted from an edition of Pico (%s): allowed only for the editors' or translators' NOTES, never Pico's own text; the semantic verifier checks the quotation is in the notes" % work})
    if attribution in ("scholar_claim", "scholar_report") and not is_primary and claimant:
        author = C.registry().get(work, {}).get("author", "")
        if re.search(r"\(eds?\.?\)|\beds\b|from file name", author.lower()):
            author = claimant  # edited volume or unlabelled work: the essay's author is the claimant; the packet says which essay
        last = re.sub(r"[^A-Za-z]", "", claimant.split()[-1]).lower()
        if last and last not in re.sub(r"[^a-z ]", "", author.lower()):
            issues.append({"code": "claimant_mismatch", "severity": "warn", "where": where,
                           "detail": "claimant %r is not the author of %s (%s); if the scholar is quoting another, use attribution scholar_report and name the reporter" % (claimant, work, author)})
    return v


def check_claim(c, packet, fix, strict):
    issues, qv, wv = [], [], []
    for k in ("id", "claimant", "attribution", "claim_type", "topics", "text", "quotes", "hedge"):
        if k not in c or c[k] in (None, "", []):
            issues.append({"code": "schema", "severity": "error", "where": k, "detail": "missing %s" % k})
    if issues:
        return issues, qv, wv
    if not str(c["id"]).startswith(packet + ":"):
        issues.append({"code": "bad_id", "severity": "error", "where": "id", "detail": "id must start with %r" % (packet + ":")})
    for k, allowed in (("attribution", ATTRIBUTION), ("claim_type", CLAIM_TYPE), ("hedge", HEDGE)):
        if c[k] not in allowed:
            issues.append({"code": "schema", "severity": "error", "where": k, "detail": "%r not in %s" % (c[k], sorted(allowed))})
    for i, q in enumerate(c["quotes"]):
        qv.append(check_quote(q, "quotes[%d]" % i, issues, c["attribution"], c["claimant"], fix))
    for w in c.get("warrants") or []:
        wid = w.get("id", "?")
        if w.get("kind") not in WARRANT_KIND or not w.get("text"):
            issues.append({"code": "schema", "severity": "error", "where": "warrant " + wid, "detail": "needs kind in %s and text" % sorted(WARRANT_KIND)})
            continue
        if w["kind"] in ("primary_text", "scholar_evidence"):
            if not w.get("quote"):
                issues.append({"code": "warrant_unevidenced", "severity": "error", "where": "warrant " + wid,
                               "detail": "a %s warrant must carry the quotation that is the evidence" % w["kind"]})
            else:
                att = "primary_text" if w["kind"] == "primary_text" else "scholar_report"
                wv.append(check_quote(w["quote"], "warrant %s" % wid, issues, att, None, fix))
        elif w["kind"] == "inference" and not w.get("basis"):
            issues.append({"code": "warrant_unevidenced", "severity": "error", "where": "warrant " + wid,
                           "detail": "an inference warrant must list `basis` (claim ids or quote indexes)"})
    for o in c.get("open_questions") or []:
        if o.get("kind") not in OQ_KIND or not o.get("text"):
            issues.append({"code": "schema", "severity": "error", "where": "open_question", "detail": "needs kind in %s and text" % sorted(OQ_KIND)})
        elif o.get("basis_quote"):
            check_quote(o["basis_quote"], "open_question %s" % o.get("id", "?"), issues, "scholar_report", None, fix)
    for b in c.get("bears_on") or []:
        if not b.get("party") or b.get("kind") not in REL_KIND or not b.get("note"):
            issues.append({"code": "schema", "severity": "error", "where": "bears_on", "detail": "needs party, kind in %s, note" % sorted(REL_KIND)})
    j = c.get("judged")
    if j is not None and (j.get("frame_shift") not in (0, 1, 2, 3) or (j.get("frame_shift") and not j.get("justification"))):
        issues.append({"code": "schema", "severity": "error", "where": "judged", "detail": "frame_shift 0-3, with a justification when > 0"})
    # hedging must be evidenced in the source's own words
    ground = gn(" ".join(q.get("text", "") for q in c["quotes"] if isinstance(q, dict)))
    if c["hedge"] != "assertive":
        hw = c.get("hedge_words")
        if not hw or gn(hw) not in ground:
            issues.append({"code": "hedge_ungrounded", "severity": "warn", "where": "hedge",
                           "detail": "a hedged/speculative claim needs `hedge_words` that occur in a quote"})
    # entity grounding: names and years in the restatement must occur in the evidence
    claimant_tokens = {gn(t) for t in c["claimant"].split()}
    seen = set()
    for tok in NAME.findall(re.sub(r"[’']s\b", "", c["text"])) + YEAR.findall(c["text"]):
        n = gn(tok)
        if tok in STOP or n in claimant_tokens or n in seen:
            continue
        seen.add(n)
        if not grounded(n, ground):
            issues.append({"code": "ungrounded_entity", "severity": "error" if strict else "warn", "where": "text",
                           "detail": "%r occurs in the restatement but in none of the quotations" % tok})
    for b in c.get("bears_on") or []:
        if b.get("party") and not party_grounded(b["party"], ground):
            issues.append({"code": "bears_on_ungrounded", "severity": "warn", "where": "bears_on",
                           "detail": "party %r is named in no quotation of this claim: the relationship tag is an inference, not evidence" % b["party"]})
    for e in c.get("entities") or []:
        if not grounded(gn(e.split()[-1]), ground) and gn(e) not in ground:
            issues.append({"code": "ungrounded_entity", "severity": "error" if strict else "warn", "where": "entities",
                           "detail": "entity %r is in no quotation of this claim" % e})
    return issues, qv, wv


def verify_packet(path, fix, strict):
    p = load(path)
    packet = p.get("packet")
    claims = p.get("claims") or []
    out = {"packet": packet, "file": os.path.relpath(path, ROOT), "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "claims": []}
    if not packet:
        out["fatal"] = "packet has no `packet` id"
        return out, p, False
    ids = set()
    changed = False
    sem = semantic_verdicts(packet)
    for c in claims:
        before = json.dumps(c, sort_keys=True)
        issues, qv, wv = check_claim(c, packet, fix, strict)
        j = sem.get(c.get("id"))
        if j and j.get("hash") == chash(c) and j.get("verdict") in ("overreaches", "wrong"):
            issues.append({"code": "semantic_" + j["verdict"], "severity": "error", "where": "text",
                           "detail": "second verifier: %s" % j.get("reason", ""), "suggested_text": j.get("suggested_text")})
        if c.get("id") in ids:
            issues.append({"code": "dup_id", "severity": "error", "where": "id", "detail": "duplicate id"})
        ids.add(c.get("id"))
        if json.dumps(c, sort_keys=True) != before:
            changed = True
        err = [i for i in issues if i["severity"] == "error"]
        out["claims"].append({"id": c.get("id"), "status": "needs_fix" if err else "verified",
                              "quotes": [{k: v for k, v in x.items() if k != "best_match"} for x in qv],
                              "warrants": [x.get("verdict") for x in wv], "issues": issues})
    return out, p, changed


def reuse_check(packets):
    """Prohibition 2: a quotation that appears in more than three claims is filler."""
    seen = {}
    for out, p, _ in packets:
        for c in p.get("claims", []):
            for q in c.get("quotes", []):
                if isinstance(q, dict) and q.get("text"):
                    seen.setdefault(gn(q["text"])[:200], []).append(c.get("id"))
    return {k: v for k, v in seen.items() if len(set(v)) > 3}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("packets", nargs="*")
    ap.add_argument("--fix-locators", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    paths = a.packets or sorted(glob.glob(CLAIM_GLOB, recursive=True))
    os.makedirs(VERDICTS, exist_ok=True)
    os.makedirs(TICKETS, exist_ok=True)
    results, bad = [], 0
    for path in paths:
        out, p, changed = verify_packet(path, a.fix_locators, a.strict)
        results.append((out, p, changed))
        if changed and a.fix_locators:
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(p, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
    reused = reuse_check(results)
    all_ids = {}
    for out, p, _ in results:
        for c in out["claims"]:
            all_ids.setdefault(c["id"], []).append(out["packet"])
    for out, p, _ in results:
        tickets = []
        for c in out["claims"]:
            if c["id"] in all_ids and len(all_ids[c["id"]]) > 1:
                c["issues"].append({"code": "dup_id", "severity": "error", "where": "id", "detail": "id also used in another packet"})
                c["status"] = "needs_fix"
            for i in c["issues"]:
                if i["severity"] == "error":
                    tickets.append({"claim_id": c["id"], **{k: i[k] for k in i if k != "verdict"}, "verdict": (i.get("verdict") or {}).get("verdict")})
        n = len(out["claims"])
        nv = sum(1 for c in out["claims"] if c["status"] == "verified")
        nq = sum(len(c["quotes"]) for c in out["claims"])
        vq = sum(1 for c in out["claims"] for q in c["quotes"] if q.get("verdict") in ("verbatim", "verbatim_modulo_marks"))
        warns = sum(1 for c in out["claims"] for i in c["issues"] if i["severity"] == "warn")
        out["summary"] = {"claims": n, "verified": nv, "needs_fix": n - nv, "quotes": nq, "quotes_verbatim": vq,
                          "warnings": warns, "verified_rate": round(nv / n, 3) if n else None}
        base = out["packet"] or os.path.basename(out["file"])
        with io.open(os.path.join(VERDICTS, base + ".verdicts.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False)
        with io.open(os.path.join(TICKETS, base + ".tickets.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"packet": base, "open": len(tickets), "tickets": tickets}, fh, indent=1, ensure_ascii=False)
        # a sample sheet for the second (semantic) verifier: 20% of verified claims, at least 5
        vc = [c for c in out["claims"] if c["status"] == "verified"]
        byid = {c["id"]: c for c in p.get("claims", [])}
        sem = semantic_verdicts(base)
        unjudged = [c for c in vc if not (sem.get(c["id"]) and sem[c["id"]].get("hash") == chash(byid[c["id"]]))]
        edited = [c for c in unjudged if c["id"] in sem]          # was flagged, has since been changed: re-judge first
        rest = [c for c in unjudged if c["id"] not in sem]
        random.Random(base).shuffle(rest)
        want = max(5, len(vc) // 5) - (len(vc) - len(unjudged))    # judged claims already count toward the 20%
        take = {c["id"] for c in edited} | {c["id"] for c in rest[: max(0, want)]}
        with io.open(os.path.join(VERDICTS, base + ".sample.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Semantic sample for %s\n\nFor each claim: does `text` say no more than the quotations support? Answer supported / overreaches / wrong, with one line of reason.\n\n" % base)
            for cid in sorted(take):
                c = byid[cid]
                fh.write("## %s (%s, %s)\n\n**Restatement:** %s\n\n" % (cid, c["claimant"], c["hedge"], c["text"]))
                for q in c["quotes"]:
                    fh.write("> %s\n> (%s:%s)\n\n" % (q["text"], q["work"], q["line"]))
                for w in c.get("warrants") or []:
                    fh.write("- warrant [%s]: %s\n" % (w["kind"], w["text"]))
                fh.write("\n")
        bad += n - nv
        if not a.quiet or out["summary"]["needs_fix"]:
            s = out["summary"]
            print("%-24s claims %3d  verified %3d  needs_fix %3d  quotes verbatim %3d/%3d  warnings %3d" % (
                base, s["claims"], s["verified"], s["needs_fix"], s["quotes_verbatim"], s["quotes"], s["warnings"]))
    for k, v in reused.items():
        print("REUSED QUOTATION (%d claims): %s ..." % (len(set(v)), k[:60]))
        bad += 1
    print("TOTAL needs_fix: %d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
