#!/usr/bin/env python3
"""harvest_prompts.py: keep PROMPTS.md complete.

PROMPTS.md is the project's source of truth for what Ted has asked for. This script reads the Claude Code
session transcripts for this project (JSONL), extracts every prompt a human typed, and rewrites the block of
PROMPTS.md between the GENERATED markers. Everything outside the markers (the distillation, status notes) is
hand-maintained and never touched.

What counts as a prompt:
  * a `user` record whose origin.kind == "human" (string content), and
  * a `queue-operation` `enqueue` record: messages typed while an agent was mid-turn appear ONLY here.
What does not: tool results, task notifications, local-command caveats, stop-hook notices.
Duplicates (the same text as enqueue and as user record) are merged. Text is stored verbatim; pasted blocks
(`<pasted_content ...>`) are kept only as a head and a size, because they are long handovers pasted from
elsewhere and the transcript still holds them.

    python scripts/harvest_prompts.py                # rewrite the generated block
    python scripts/harvest_prompts.py --check        # exit 1 if PROMPTS.md is stale (CI / session start)
    python scripts/harvest_prompts.py --list         # print ids and first lines only

Run it at the start of every session and before any handover.
"""
import argparse, glob, io, json, os, re, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "PROMPTS.md")
DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--Dev-Pico900")
BEGIN = "<!-- BEGIN GENERATED PROMPTS (scripts/harvest_prompts.py rewrites everything to END) -->"
END = "<!-- END GENERATED PROMPTS -->"
PASTE = re.compile(r"<pasted_content id=\"[^\"]*\">(.*?)</pasted_content>", re.S)
SKIP_HEAD = ("<task-notification", "<local-command", "<command-name>", "<system-reminder", "A session-scoped Stop hook")


def key(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def clean(text):
    """Verbatim, except pasted blocks are reduced to a head and a size."""
    def repl(m):
        body = m.group(1).strip()
        head = re.sub(r"\s+", " ", body)[:240]
        return "[pasted block, %d chars, begins: %s ...]" % (len(body), head)
    return PASTE.sub(repl, text).strip()


def harvest(pdir):
    found = {}
    for f in sorted(glob.glob(os.path.join(pdir, "*.jsonl"))):
        with io.open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                t = o.get("type")
                text = None
                if t == "user" and (o.get("origin") or {}).get("kind") == "human" and isinstance(o["message"]["content"], str):
                    text = o["message"]["content"]
                elif t == "queue-operation" and o.get("operation") == "enqueue" and isinstance(o.get("content"), str):
                    text = o["content"]
                if not text or text.lstrip().startswith(SKIP_HEAD):
                    continue
                text = clean(text)
                if not text:
                    continue
                ts = o.get("timestamp") or ""
                sess = (o.get("sessionId") or os.path.basename(f))[:8]
                k = (sess, key(text))
                # keep the earliest timestamp (the moment it was typed)
                if k not in found or ts < found[k]["ts"]:
                    found[k] = {"ts": ts, "session": sess, "text": text}
    rows = sorted(found.values(), key=lambda r: (r["ts"], r["session"]))
    seen = {}
    for r in rows:
        base = "P" + re.sub(r"\D", "", r["ts"])[:14]
        n = seen.get(base, 0)
        seen[base] = n + 1
        r["id"] = base + ("" if n == 0 else "-%d" % n)
    return rows


def render(rows):
    out = [BEGIN, "",
           "Generated %s from %d prompts. Timestamps are UTC. IDs are stable (timestamp of typing)." % (
               datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), len(rows)), ""]
    for r in rows:
        out.append("### %s  (%s, session %s)" % (r["id"], r["ts"][:16].replace("T", " "), r["session"]))
        out.append("")
        for ln in r["text"].split("\n"):
            out.append(("> " + ln).rstrip())
        out.append("")
    out.append(END)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=DEFAULT_DIR)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    rows = harvest(a.dir)
    if a.list:
        for r in rows:
            print(r["id"], r["session"], r["text"][:90].replace("\n", " "))
        return 0
    block = render(rows)
    cur = io.open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if BEGIN in cur and END in cur:
        pre, rest = cur.split(BEGIN, 1)
        post = rest.split(END, 1)[1]
        new = pre + block + post
    else:
        new = cur.rstrip() + "\n\n" + block + "\n"
    def body(s):  # ignore the generated-at line when checking staleness
        return re.sub(r"Generated [^\n]* from", "Generated from", s)
    if a.check:
        stale = body(new) != body(cur)
        print("PROMPTS.md is %s (%d prompts)" % ("STALE" if stale else "current", len(rows)))
        return 1 if stale else 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    print("wrote %s: %d prompts" % (OUT, len(rows)))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
