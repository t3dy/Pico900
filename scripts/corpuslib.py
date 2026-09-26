#!/usr/bin/env python3
"""corpuslib.py: find text in the Markdown corpus, tolerating OCR.

One implementation, shared by corpus_tool.py (agents looking things up), claims_verify.py (the quotation
gate) and commentary_check.py. The audit found that quotations "verified" by agents were not in the sources;
the remedy is that nothing is stored as a quotation until this library has located it.

Matching model
  * Both quote and source are reduced to their letters and digits (lower-cased, accents and ligatures folded).
    Spacing, hyphenation at line ends, punctuation, curly quotes and footnote-mark spacing therefore cannot
    cause a miss. The price is that the match is insensitive to punctuation, which is acceptable for a
    quotation gate and is stated in every verdict (`basis`).
  * `[...]`, `...` and `[editorial text]` in a quote split it into fragments; fragments must occur in order.
  * verdicts: verbatim | verbatim_modulo_marks (equal once digits are ignored: footnote numerals inside the
    text) | altered (>= 0.85 of the fragment is present, in order, but not all: a reworded quotation) |
    not_found | untestable.
  * Lines are 1-based and reliable to about +/- 2 (OCR joins lines). Cite `work:line`.
"""
import bisect, difflib, io, json, os, re, sys, unicodedata
from functools import lru_cache

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "data", "corpus", "registry.json")
LIG = {"æ": "ae", "œ": "oe", "ß": "ss", "ſ": "s"}
ELLIPSIS = re.compile(r"\s*(?:\[\s*(?:\.\s*){2,}\s*\]|(?:\.\s*){3,}|…)\s*")
BRACKET = re.compile(r"\[[^\]]*\]")
SPLIT = "\u0001"
MIN_FRAG = 12          # normalised characters; shorter fragments are ignored (too generic to test)
MAX_GAP = 4000         # normalised characters allowed between consecutive fragments


def norm(s, digits=True):
    out = []
    for ch in unicodedata.normalize("NFKD", s):
        if unicodedata.combining(ch):
            continue
        for c in LIG.get(ch.lower(), ch.lower()):
            if c.isalpha() or (digits and c.isdigit()):
                out.append(c)
    return "".join(out)


@lru_cache(maxsize=None)
def registry():
    with io.open(REGISTRY, encoding="utf-8") as fh:
        return json.load(fh)["works"]


def path_of(work):
    w = registry().get(work)
    if not w:
        raise KeyError("unknown work key %r (see data/corpus/registry.json)" % work)
    if not os.path.exists(w["path"]):
        raise FileNotFoundError(w["path"])
    return w["path"]


@lru_cache(maxsize=None)
def lines_of(work):
    with io.open(path_of(work), encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


class Index:
    """Normalised streams of one work, with position -> line maps."""

    def __init__(self, work):
        self.work = work
        self.lines = lines_of(work)
        strict, loose, ss, sl = [], [], [], []
        ps = pl = 0
        for ln in self.lines:
            n = norm(ln)
            m = "".join(c for c in n if not c.isdigit())
            ss.append(ps); sl.append(pl)
            strict.append(n); loose.append(m)
            ps += len(n); pl += len(m)
        self.strict, self.loose = "".join(strict), "".join(loose)
        self.starts = {"strict": ss, "loose": sl}

    def line_of(self, pos, mode):
        return bisect.bisect_right(self.starts[mode], pos) - 1 + 1  # 0-based index -> 1-based line

    def stream(self, mode):
        return self.strict if mode == "strict" else self.loose


@lru_cache(maxsize=None)
def index(work):
    return Index(work)


def fragments(quote):
    q = BRACKET.sub(SPLIT, ELLIPSIS.sub(SPLIT, quote))
    return [f for f in q.split(SPLIT) if f.strip()]


def _occurrences(s, sub, limit=60):
    i = s.find(sub)
    n = 0
    while i >= 0 and n < limit:
        yield i
        n += 1
        i = s.find(sub, i + 1)


def _chain(s, frags, start):
    """Fragments in order beginning at `start`; returns (end, max_gap) or None."""
    pos, gap = start, 0
    for k, f in enumerate(frags):
        i = s.find(f, pos) if k else (start if s.startswith(f, start) else -1)
        if i < 0:
            return None
        if k:
            gap = max(gap, i - pos)
        pos = i + len(f)
    return pos, gap


def locate(work, quote, near=None):
    """Verdict for `quote` in `work`. `near` (a line number) disambiguates repeated phrases."""
    ix = index(work)
    raw = [(f, norm(f)) for f in fragments(quote)]
    frs = [(f, n) for f, n in raw if len(n) >= MIN_FRAG] or [(f, n) for f, n in raw if n]
    if not frs:
        return {"verdict": "untestable", "reason": "no letters to match", "basis": "letters and digits only"}
    for mode in ("strict", "loose"):
        s = ix.stream(mode)
        fr = [n if mode == "strict" else "".join(c for c in n if not c.isdigit()) for _, n in frs]
        fr = [f for f in fr if f]
        if not fr:
            continue
        cands = list(_occurrences(s, fr[0]))
        if near is not None:
            cands.sort(key=lambda p: abs(ix.line_of(p, mode) - near))
        for p in cands:
            r = _chain(s, fr, p)
            if r:
                end, gap = r
                out = {"verdict": "verbatim" if mode == "strict" else "verbatim_modulo_marks",
                       "line_start": ix.line_of(p, mode), "line_end": ix.line_of(max(end - 1, p), mode),
                       "occurrences": len(cands), "basis": "letters and digits only; punctuation ignored"}
                if gap > MAX_GAP:
                    out["warning"] = "fragments are %d characters apart; check they belong to one passage" % gap
                return out
    return fuzzy(ix, frs)


def fuzzy(ix, frs):
    """Best approximate location of the longest fragment, by k-gram voting then SequenceMatcher."""
    f = max((n for _, n in frs), key=len)
    s, mode = ix.loose, "loose"
    f = "".join(c for c in f if not c.isdigit())
    if len(f) < 20:
        return {"verdict": "not_found", "basis": "fragment too short for approximate search"}
    k, votes = 10, {}
    for o in range(0, len(f) - k, max(3, len(f) // 40)):
        for p in _occurrences(s, f[o:o + k], 30):
            b = (p - o) // 40
            votes[b] = votes.get(b, 0) + 1
    if not votes:
        return {"verdict": "not_found", "basis": "no 10-character run of the quotation occurs in the source"}
    b = max(votes, key=votes.get)
    lo = max(0, b * 40 - 60)
    win = s[lo: lo + len(f) + 140]
    sm = difflib.SequenceMatcher(None, f, win, autojunk=False)
    blocks = [m for m in sm.get_matching_blocks() if m.size]
    cov = sum(m.size for m in blocks) / len(f)
    if not blocks:
        return {"verdict": "not_found", "basis": "no overlap"}
    a = lo + min(m.b for m in blocks)
    z = lo + max(m.b + m.size for m in blocks)
    l1, l2 = ix.line_of(a, mode), ix.line_of(z - 1, mode)
    excerpt = " ".join(x.strip() for x in ix.lines[l1 - 1: l2] if x.strip())
    out = {"verdict": "altered" if cov >= 0.85 else "not_found", "coverage": round(cov, 3),
           "best_match": {"line_start": l1, "line_end": l2, "excerpt": excerpt[:900]},
           "basis": "approximate: share of the longest fragment found near this location"}
    if out["verdict"] == "altered":
        out["line_start"], out["line_end"] = l1, l2
    return out


def show(work, a, b):
    L = lines_of(work)
    a = max(1, a); b = min(len(L), b)
    return "\n".join("%6d  %s" % (i, L[i - 1]) for i in range(a, b + 1))


def grep(work, pattern, flags=re.I, width=200):
    rx = re.compile(pattern, flags)
    return [(i, l.strip()[:width]) for i, l in enumerate(lines_of(work), 1) if rx.search(l)]


def page_of(work, line):
    """Nearest preceding PDF page marker ('## Page N') and printed page bracket like '[199]', if the OCR kept them."""
    L = lines_of(work)
    pdf = printed = None
    for i in range(min(line, len(L)) - 1, max(0, line - 400), -1):
        t = L[i].strip()
        if pdf is None:
            m = re.match(r"^#+\s*Page\s+(\d+)", t, re.I)
            if m:
                pdf = int(m.group(1))
        if printed is None:
            m = re.match(r"^\[(\d{1,4})\]$", t)
            if m:
                printed = int(m.group(1))
        if pdf and printed:
            break
    return {"pdf_page": pdf, "printed_bracket": printed}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(locate(sys.argv[1], sys.argv[2]), indent=1, ensure_ascii=False))
