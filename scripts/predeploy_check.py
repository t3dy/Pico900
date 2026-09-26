#!/usr/bin/env python3
"""predeploy_check.py: the DEPLOYER's gate for the built site (site/). Exit 0 only if all pass.

Encodes the defects found by audit/A4_site_and_governance.md, each of which shipped in a "ready to
deploy" build: CSS that parsed as empty (doubled braces), internal links that 404 under the Pages
subpath, and generated filler shown as Pico's text. Run after `python scripts/build_html_site.py`.

    python scripts/predeploy_check.py

Checks:
  1. every root-absolute src/href starts with the base path (/Pico900/)
  2. every internal link resolves to a file in site/ once the base path is stripped
  3. style.css has no doubled braces and defines real rules
  4. no filler marker appears on any page (template names, placeholder strings)
  5. every page has exactly one <h1> and a lang attribute on <html>
This does not replace loading the live URL afterwards, which the workspace rules still require.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = os.environ.get("PICO_BASE_PATH", "/Pico900").rstrip("/")
FILLER = re.compile(r"template_based|template_S\d|CITATION TO BE FILLED|TO BE SOURCED|TO_SOURCE|TO_TRANSLATE|"
                    r"NEEDS_TRANSLATION|pending_translation|TO BE VERIFIED|\[Latin text pending\]|\[Charge pending\]", re.I)
LINK = re.compile(r'(?:src|href)="([^"#?]+)')


def pages():
    for dp, _, fs in os.walk(SITE):
        for f in fs:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


def main():
    if not os.path.isdir(SITE):
        print("no site/ directory: build first")
        return 2
    problems = []
    n = 0
    for p in pages():
        n += 1
        rel = os.path.relpath(p, SITE).replace("\\", "/")
        with io.open(p, encoding="utf-8") as fh:
            h = fh.read()
        if len(re.findall(r"<h1[ >]", h)) != 1:
            problems.append(f"{rel}: expected exactly one <h1>")
        if not re.search(r"<html[^>]*\blang=", h):
            problems.append(f"{rel}: <html> has no lang")
        m = FILLER.search(h)
        if m:
            problems.append(f"{rel}: filler marker shown: {m.group(0)!r}")
        for link in LINK.findall(h):
            if link.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if link.startswith("/"):
                if BASE and not (link == BASE or link.startswith(BASE + "/")):
                    problems.append(f"{rel}: root-absolute link outside base path: {link}")
                    continue
                target = link[len(BASE):] if BASE else link
                target = target.lstrip("/")
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(rel), link)).replace("\\", "/")
            path = os.path.join(SITE, target)
            if os.path.isdir(path):
                path = os.path.join(path, "index.html")
            if not os.path.exists(path):
                problems.append(f"{rel}: link does not resolve: {link}")
    css = os.path.join(SITE, "css", "style.css")
    if not os.path.exists(css):
        problems.append("css/style.css missing")
    else:
        with io.open(css, encoding="utf-8") as fh:
            c = fh.read()
        if "{{" in c or re.search(r"\w\s*}}\s*\w", c):
            problems.append("css/style.css contains doubled braces (rules parse as empty)")
        if len(re.findall(r"\{[^{}]*:[^{}]*\}", c)) < 10:
            problems.append("css/style.css defines fewer than 10 rules")
    seen = {}
    for pr in problems:
        seen.setdefault(re.sub(r"^[^:]+: ", "", pr), []).append(pr)
    print(f"checked {n} pages; {len(problems)} problems in {len(seen)} kinds")
    for kind, ps in list(seen.items())[:15]:
        print(f"  {len(ps):5d}x  {kind}   e.g. {ps[0].split(':')[0]}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
