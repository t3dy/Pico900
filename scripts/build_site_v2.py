#!/usr/bin/env python3
"""build_site_v2.py: static site from the Farmer-keyed entries (entries/*.json verified, entries/*.draft.json
unverified) plus the research layer (inventory, mentions, cross-references). Output: site/.

Rendering rules (docs/EDITORIAL_STANDARD.md s3, s10): a verified entry renders as edition text; a draft renders
with a visible "unverified draft" badge on every field; a thesis with no entry shows its Latin (public domain,
from the inventory) and "translation and commentary not yet prepared". Farmer's English and his notes are never
rendered; his cross-references are rendered as links (public-domain Latin). Base path: PICO_BASE_PATH (default /Pico900).
Run scripts/predeploy_check.py afterwards.
"""
import glob, html, io, json, os, re, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = os.environ.get("PICO_BASE_PATH", "/Pico900").rstrip("/")
PROSE = [("doctrine", "Doctrine"), ("context", "Context"), ("reception", "Reception"), ("historiography", "Historiography")]
esc = lambda s: html.escape(str(s), quote=True)


def slug(tid):
    if ">" in tid:
        sec, n = tid.split(">"); return f"own_{sec}_{int(n):03d}"
    sec, n = tid.split("."); return f"hist_{int(sec):02d}_{int(n):03d}"


def sec_slug(sec):
    return "own_" + sec.rstrip(">") if sec.endswith(">") else "hist_" + sec


CSS = """
:root{--ink:#1e1a16;--paper:#faf7f1;--rule:#d8cfc0;--accent:#7a2e1d;--muted:#6b625a;--badge:#b7791f;--ok:#2e6b3f}
*{box-sizing:border-box}body{margin:0;font-family:Georgia,'Times New Roman',serif;background:var(--paper);color:var(--ink);line-height:1.5}
header.top{border-bottom:1px solid var(--rule);padding:14px 24px;display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
header.top a{color:var(--accent);text-decoration:none}header.top .brand{font-size:1.15rem;font-weight:bold}
main{max-width:980px;margin:0 auto;padding:24px}h1{font-weight:normal;font-size:1.7rem;margin:.2em 0}
h2{font-size:1.05rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:1.6em 0 .4em;border-bottom:1px solid var(--rule)}
.latin{font-size:1.15rem;line-height:1.55}[lang=la]{font-style:italic}.translation{font-size:1.08rem}
.badge{display:inline-block;font:.72rem sans-serif;letter-spacing:.03em;padding:1px 6px;border-radius:3px;background:#f3e6c9;color:var(--badge);border:1px solid #e3cf9a;vertical-align:middle}
.badge.ok{background:#e3efe6;color:var(--ok);border-color:#bcd7c3}.badge.cond{background:#f6dcd6;color:var(--accent);border-color:#e6b8ad}
.meta{color:var(--muted);font-size:.92rem}.notice{background:#fff8e6;border:1px solid #e9d9a8;padding:10px 14px;margin:14px 0;font-size:.95rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}.card{border:1px solid var(--rule);padding:10px 12px;background:#fff;border-radius:4px}
.card a{color:var(--accent);text-decoration:none}table{border-collapse:collapse;width:100%;font-size:.95rem}td,th{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:left;vertical-align:top}
.loc{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.82rem;color:var(--muted)}ul.cites li{margin:.25em 0}
nav.pn{display:flex;justify-content:space-between;margin-top:28px;border-top:1px solid var(--rule);padding-top:10px}nav.pn a{color:var(--accent);text-decoration:none}
footer{border-top:1px solid var(--rule);color:var(--muted);font-size:.85rem;padding:16px 24px;margin-top:40px}
@media (max-width:600px){main{padding:16px}header.top{padding:10px 16px}}
"""


def page(title, body, depth_desc=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} - Pico, 900 Conclusions</title><link rel="stylesheet" href="{BASE}/css/style.css"></head>
<body><header class="top"><a class="brand" href="{BASE}/">Pico della Mirandola, <em>Conclusiones</em> (1486)</a>
<a href="{BASE}/sections/">Sections</a><a href="{BASE}/condemned/">The thirteen condemned</a><a href="{BASE}/scholarship/">Scholarship</a><a href="{BASE}/about/">Method</a></header>
<main>{body}</main>
<footer>A digital edition in preparation. Latin from Farmer's edition (1998), collation pending; translations original; every claim carries a locator. Work in progress: fields marked <span class="badge">unverified draft</span> have not yet passed verification.</footer></body></html>"""


def render_prose(txt):
    # turn (work:line) locators into spans; keep paragraphs
    t = esc(txt)
    t = re.sub(r"\(([a-z][a-z0-9_]+):(\d+(?:\s?-\s?\d+)?)\)", r'<span class="loc">(\1:\2)</span>', t)
    return "".join(f"<p>{p.strip()}</p>" for p in t.split("\n") if p.strip())


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    inv = json.load(io.open(os.path.join(ROOT, "data", "inventory", "theses.json"), encoding="utf-8"))["theses"]
    reg = json.load(io.open(os.path.join(ROOT, "data", "corpus", "registry.json"), encoding="utf-8"))["works"]
    cond = {c["farmer_id"].split(" ")[0]: c for c in json.load(io.open(os.path.join(ROOT, "data", "inventory", "condemned_thirteen.json"), encoding="utf-8"))["theses"]}
    xr = json.load(io.open(os.path.join(ROOT, "data", "ontology", "connections", "farmer_crossrefs.json"), encoding="utf-8"))["crossrefs"]
    agg = {a["thesis_id"]: a for a in json.load(io.open(os.path.join(ROOT, "data", "ontology", "theses.json"), encoding="utf-8"))["theses"]}
    entries, bad = {}, []
    for p in glob.glob(os.path.join(ROOT, "entries", "*.json")):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except Exception as e:
            bad.append(os.path.basename(p)); continue
        tid = d.get("thesis_id")
        if not tid:
            continue
        verified = not p.endswith(".draft.json")
        if tid not in entries or verified:
            entries[tid] = (d, verified)
    by_id = {t["thesis_id"]: t for t in inv}
    order = [t["thesis_id"] for t in inv]
    os.makedirs(os.path.join(SITE, "css"), exist_ok=True)
    with io.open(os.path.join(SITE, "css", "style.css"), "w", encoding="utf-8") as fh:
        fh.write(CSS)

    def link(tid, text=None):
        return f'<a href="{BASE}/theses/{slug(tid)}.html">{esc(text or tid)}</a>'

    # thesis pages
    os.makedirs(os.path.join(SITE, "theses"), exist_ok=True)
    for i, t in enumerate(inv):
        tid = t["thesis_id"]
        e, verified = entries.get(tid, (None, False))
        badge = "" if verified else '<span class="badge">unverified draft</span>' if e else ""
        B = [f'<p class="meta">{esc(t["section_name"])} &middot; thesis {esc(tid)}' + (f' &middot; <span class="badge cond">condemned, Q{cond[tid]["q"]}</span>' if tid in cond else "") + "</p>",
             f"<h1>Thesis {esc(tid)}</h1>"]
        if not verified:
            B.append('<div class="notice">Work in progress. ' + ("This entry is a draft awaiting verification: every claim carries a locator, but no second reader has yet re-found each one." if e else "No entry has been prepared for this thesis yet; the Latin below is from Farmer's edition and awaits collation.") + "</div>")
        latin = (e or {}).get("latin") or t["latin"]
        B += ["<h2>Latin</h2>", f'<p class="latin" lang="la">{esc(latin)}</p>',
              f'<p class="meta">Copy-text: Farmer 1998, line {t["latin_line"]}' + (f'; 1486 print folio {esc(", ".join(t["folio_1486"]))}' if t.get("folio_1486") else "") + "</p>"]
        if t.get("apparatus_1486"):
            B.append('<p class="meta">Apparatus (Farmer): ' + "; ".join(esc(a["text"]) for a in t["apparatus_1486"]) + "</p>")
        if e and e.get("latin_note"):
            B.append(f'<p class="meta">{render_prose(e["latin_note"])}</p>')
        B.append("<h2>English</h2>")
        if e and e.get("translation"):
            B.append(f'<p class="translation" lang="en">{esc(e["translation"])} {badge}</p>')
            if e.get("translation_note"):
                B.append(f'<p class="meta">{render_prose(e["translation_note"])}</p>')
            B.append(f'<p class="meta">Translation: {esc(e.get("translator", "unstated"))}</p>')
        else:
            B.append('<p class="meta">Translation not yet prepared.</p>')
        if e and (e.get("attribution") or e.get("pico_stance")):
            B.append(f'<p class="meta">Attribution: {esc(e.get("attribution", ""))} &middot; Pico\'s stance: {esc(e.get("pico_stance", "unstated"))}</p>')
        if tid in cond:
            c = cond[tid]
            B += ["<h2>Condemnation</h2>", f"<p>Q{c['q']} in the order of the Apology: {esc(c['topic'])}. Printed 7 December 1486; censured by the papal commission in February-March 1487; the work as a whole condemned by the bull of 4 August 1487.</p>"]
            if e and e.get("commission_verdict"):
                B.append(f"<p>{render_prose(e['commission_verdict'])} {badge}</p>")
        if e:
            for f, label in PROSE:
                if e.get(f):
                    B += [f"<h2>{label}</h2>", render_prose(e[f]) + (f"<p>{badge}</p>" if badge else "")]
            if e.get("sources"):
                B += ["<h2>Pico's sources</h2>", "<ul>" + "".join(f"<li>{esc(s.get('text', ''))}: {esc(s.get('pico_relation', ''))} <span class='loc'>({esc(s.get('locator', ''))})</span></li>" for s in e["sources"]) + "</ul>"]
            if e.get("quotations"):
                B += ["<h2>Quotations cited</h2>", "<ul class='cites'>" + "".join(
                    f"<li>&ldquo;{esc(q.get('text', ''))}&rdquo; &mdash; {esc(reg.get(q.get('work', ''), {}).get('author', q.get('work', '')))}, <em>{esc(reg.get(q.get('work', ''), {}).get('title', ''))}</em> <span class='loc'>({esc(q.get('work', ''))}:{esc(q.get('line', ''))})</span></li>" for q in e["quotations"]) + "</ul>"]
            if e.get("not_established"):
                B += ["<h2>Not established</h2>", "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in e["not_established"]) + "</ul>"]
        else:
            B += ["<h2>Commentary</h2>", "<p class='meta'>Commentary forthcoming.</p>"]
        # research layer: cited by, cross-references
        a = agg.get(tid, {})
        if a.get("works"):
            B += ["<h2>Discussed in</h2>", "<ul class='cites'>" + "".join(f"<li>{esc(reg.get(w, {}).get('author', w))}, <em>{esc(reg.get(w, {}).get('title', ''))}</em> ({esc(reg.get(w, {}).get('year') or 'n.d.')})</li>" for w in a["works"] if w in reg) + "</ul>",
                  f"<p class='meta'>Mention records in the corpus: {a.get('n_mentions', 0)} (deterministic harvest; see Method).</p>"]
        refs = xr.get(tid, [])
        if refs:
            B += ["<h2>Farmer's cross-references</h2>", "<ul>" + "".join(f"<li>{link(r)} <span lang='la'>{esc(by_id[r]['latin'][:140])}</span></li>" for r in refs if r in by_id) + "</ul>"]
        if e and e.get("connections"):
            B += ["<h2>Related theses</h2>", "<p>" + ", ".join(link(r) for r in e["connections"] if r in by_id) + "</p>"]
        prev_l = f'<a href="{BASE}/theses/{slug(order[i - 1])}.html">&larr; {esc(order[i - 1])}</a>' if i > 0 else ""
        next_l = f'<a href="{BASE}/theses/{slug(order[i + 1])}.html">{esc(order[i + 1])} &rarr;</a>' if i + 1 < len(order) else ""
        B.append(f'<nav class="pn"><span>{prev_l}</span><span>{next_l}</span></nav>')
        with io.open(os.path.join(SITE, "theses", slug(tid) + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page(f"Thesis {tid}", "\n".join(B)))

    # sections
    secs = []
    for t in inv:
        if not secs or secs[-1][0] != t["section"]:
            secs.append((t["section"], t["section_name"], []))
        secs[-1][2].append(t["thesis_id"])
    os.makedirs(os.path.join(SITE, "sections"), exist_ok=True)
    rows = []
    for sec, name, ids in secs:
        nv = sum(1 for x in ids if entries.get(x, (None, False))[1]); nd = sum(1 for x in ids if x in entries and not entries[x][1])
        rows.append(f"<tr><td><a href='{BASE}/sections/{sec_slug(sec)}.html'>{esc(sec)} {esc(name)}</a></td><td>{len(ids)}</td><td>{nv}</td><td>{nd}</td></tr>")
        L = [f"<h1>{esc(sec)} {esc(name)}</h1>", f"<p class='meta'>{len(ids)} theses; {nv} verified, {nd} in draft.</p>", "<table><tr><th>thesis</th><th>Latin</th><th>status</th></tr>"]
        for x in ids:
            e, v = entries.get(x, (None, False))
            st = "<span class='badge ok'>verified</span>" if v else "<span class='badge'>draft</span>" if e else "<span class='meta'>Latin only</span>"
            L.append(f"<tr><td>{link(x)}</td><td lang='la'>{esc(by_id[x]['latin'][:160])}</td><td>{st}</td></tr>")
        L.append("</table>")
        with io.open(os.path.join(SITE, "sections", sec_slug(sec) + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page(f"Section {sec}", "\n".join(L)))
    with io.open(os.path.join(SITE, "sections", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("Sections", "<h1>The forty sections</h1><p>402 theses according to the opinions of others, then 498 according to Pico's own opinion (Farmer's numbering).</p><table><tr><th>section</th><th>theses</th><th>verified</th><th>draft</th></tr>" + "".join(rows) + "</table>"))

    # condemned
    os.makedirs(os.path.join(SITE, "condemned"), exist_ok=True)
    L = ["<h1>The thirteen condemned theses</h1>", "<p>Numbered Q1-Q13 in the order of Pico's <em>Apology</em>, following Copenhaver. Q2 spans two theses.</p><table><tr><th>Q</th><th>topic</th><th>thesis</th><th>status</th></tr>"]
    for c in sorted(cond.values(), key=lambda c: c["q"]):
        ids = [x for x in re.findall(r"\d+>\d+", c["farmer_id"])]
        fid = c["farmer_id"].split(" ")[0]
        if "-" in c["farmer_id"]:
            sec, rng = c["farmer_id"].split(">"); a, b = rng.split("-"); ids = [f"{sec}>{a}", f"{sec}>{b}"]
        else:
            ids = [fid]
        st = ", ".join(("verified" if entries.get(x, (None, False))[1] else "draft" if x in entries else "Latin only") for x in ids)
        L.append(f"<tr><td>Q{c['q']}</td><td>{esc(c['topic'])}</td><td>{', '.join(link(x) for x in ids if x in by_id)}</td><td>{esc(st)}</td></tr>")
    L.append("</table>")
    with io.open(os.path.join(SITE, "condemned", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("The thirteen condemned", "\n".join(L)))

    # scholarship
    os.makedirs(os.path.join(SITE, "scholarship"), exist_ok=True)
    st = json.load(io.open(os.path.join(ROOT, "data", "ontology", "stats.json"), encoding="utf-8"))["works"]
    L = ["<h1>Scholarship in the corpus</h1>", "<p>Works read for this edition, with the number of theses each cites or quotes (found by a deterministic harvest of explicit references and verbatim Latin; see Method). Entries labelled from a file name await bibliographic confirmation and are not cited.</p>",
         "<table><tr><th>author</th><th>title</th><th>year</th><th>theses cited</th></tr>"]
    for k, w in sorted(reg.items(), key=lambda kv: -(st.get(kv[0], {}).get("n_theses", 0))):
        if w.get("author") == "(from file name)":
            continue
        L.append(f"<tr><td>{esc(w['author'])}</td><td><em>{esc(w['title'])}</em></td><td>{esc(w.get('year') or '')}</td><td>{st.get(k, {}).get('n_theses', 0)}</td></tr>")
    L.append("</table>")
    with io.open(os.path.join(SITE, "scholarship", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("Scholarship", "\n".join(L)))

    # about
    os.makedirs(os.path.join(SITE, "about"), exist_ok=True)
    nv = sum(1 for v in entries.values() if v[1]); nd = len(entries) - nv
    about = f"""<h1>Method</h1>
<p>This edition presents the 900 <em>Conclusiones</em> that Giovanni Pico della Mirandola had printed at Rome on 7 December 1486 for a disputation that never took place, with the thirteen theses censured by a papal commission in 1487 marked as such. The text follows Stephen Farmer's edition (<em>Syncretism in the West</em>, 1998), whose numbering is used throughout (7.2 = second thesis according to Averroes; 4&gt;13 = thirteenth theological thesis according to Pico's own opinion); collation against the 1486 print is pending.</p>
<p>Translations are original and are checked for sense against Farmer's, which is in copyright and is not reproduced. Commentary is written from research packets assembled by a deterministic harvest of the scholarly corpus ({len(reg)} works): every place a scholar cites a thesis by number or quotes its Latin is recorded with a file-and-line locator, and every sentence of commentary ends with such a locator. A second reader re-finds each quotation and each dated claim before an entry is marked verified.</p>
<p>State at build: {nv} verified entries, {nd} drafts awaiting verification, {900 - len(entries)} theses with Latin only. Depth is tiered: the condemned theses and those most discussed in the scholarship receive full commentary first.</p>
<p>Source code and data: <a href="https://github.com/t3dy/Pico900">github.com/t3dy/Pico900</a>.</p>"""
    with io.open(os.path.join(SITE, "about", "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("Method", about))

    # index
    cards = "".join(f"<div class='card'><a href='{BASE}/sections/{sec_slug(sec)}.html'>{esc(sec)} {esc(name)}</a><br><span class='meta'>{len(ids)} theses</span></div>" for sec, name, ids in secs)
    body = f"""<h1>Giovanni Pico della Mirandola, <em>Conclusiones nongentae</em></h1>
<p class="meta">Rome, 7 December 1486. A digital edition in preparation: Latin, original English, and commentary at the standard of the scholarship, every claim located in its source.</p>
<div class="notice">Work in progress: {nv} verified entries, {nd} drafts, {900 - len(entries)} theses with Latin only. Read <a href="{BASE}/about/">Method</a> before citing.</div>
<h2>Start here</h2><p><a href="{BASE}/condemned/">The thirteen condemned theses</a> &middot; <a href="{BASE}/sections/">All forty sections</a> &middot; <a href="{BASE}/scholarship/">The scholarship</a></p>
<h2>Sections</h2><div class="grid">{cards}</div>"""
    with io.open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("Pico, 900 Conclusions", body))
    print(f"built site/: 900 thesis pages; entries {len(entries)} ({nv} verified, {nd} drafts); unreadable entry files skipped: {len(bad)} {bad[:5]}")


if __name__ == "__main__":
    main()
