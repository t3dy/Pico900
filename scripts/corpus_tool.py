#!/usr/bin/env python3
"""corpus_tool.py: how a RESEARCHER finds things in the corpus without opening a 1 MB file.

    python scripts/corpus_tool.py works [FILTER]            list registry keys (author, title, lines)
    python scripts/corpus_tool.py grep WORK REGEX [-n 40]    matching lines: `line: text`
    python scripts/corpus_tool.py show WORK FROM TO          numbered lines FROM..TO
    python scripts/corpus_tool.py find WORK "a phrase"       OCR-tolerant location of a phrase (line, verdict)
    python scripts/corpus_tool.py check WORK LINE "quote"    would this quotation pass the gate at that line?
    python scripts/corpus_tool.py page WORK LINE             PDF page / printed page marker near a line

Cite as `work:line` (e.g. `black2006:8408`). `check` prints exactly the verdict claims_verify.py will give.
"""
import argparse, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpuslib as C


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("works"); s.add_argument("filter", nargs="?", default="")
    s = sub.add_parser("grep"); s.add_argument("work"); s.add_argument("regex"); s.add_argument("-n", type=int, default=40)
    s = sub.add_parser("show"); s.add_argument("work"); s.add_argument("a", type=int); s.add_argument("b", type=int)
    s = sub.add_parser("find"); s.add_argument("work"); s.add_argument("phrase")
    s = sub.add_parser("check"); s.add_argument("work"); s.add_argument("line", type=int); s.add_argument("quote")
    s = sub.add_parser("page"); s.add_argument("work"); s.add_argument("line", type=int)
    a = ap.parse_args()
    if a.cmd == "works":
        for k, v in C.registry().items():
            if a.filter.lower() in (k + v["author"] + v["title"]).lower():
                try:
                    n = len(C.lines_of(k))
                except Exception:
                    n = "missing"
                print("%-22s %-28s %-60s %s lines" % (k, v["author"][:28], v["title"][:60], n))
    elif a.cmd == "grep":
        hits = C.grep(a.work, a.regex)
        for ln, t in hits[: a.n]:
            print("%d: %s" % (ln, t))
        print("-- %d matching lines%s" % (len(hits), " (truncated)" if len(hits) > a.n else ""))
    elif a.cmd == "show":
        print(C.show(a.work, a.a, a.b))
    elif a.cmd == "find":
        print(json.dumps(C.locate(a.work, a.phrase), indent=1, ensure_ascii=False))
    elif a.cmd == "check":
        r = C.locate(a.work, a.quote, near=a.line)
        r["claimed_line"] = a.line
        if "line_start" in r:
            r["locator_ok"] = abs(r["line_start"] - a.line) <= 10
        print(json.dumps(r, indent=1, ensure_ascii=False))
    elif a.cmd == "page":
        print(json.dumps(C.page_of(a.work, a.line)))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
