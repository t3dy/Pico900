# A4 — Built site, deployment hazard, governance prose

Auditor: A4 (read-only). Observed 2026-09-25/26 against the working tree at `C:\Dev\Pico900` (HEAD `5948858`, 35 commits ahead of `origin/main`).
Method: served a copy of `site/` under a `/Pico900/` subpath (scratchpad, port 8766) and the raw `site/` at root (port 8765) to emulate GitHub Pages and the handover's local test; read HTML and the browser DOM; fact-checked guide passages by grep against `E:\pdf\renaissance magic\Pico\Markdown\` (73 files). Both servers stopped. Nothing else in the repo was touched.
Note: another session was editing the tree while I worked (staged renames of four `docs/*.md` into `docs/archive/v1-pipeline/`; new untracked `COVERAGE.md`, `data/coverage_ledger.json`, `scripts/integrity_gate.py`, `scripts/style_lint.py`, `docs/ORCHESTRATION.md`). Counts below are as I saw them.

---

## Verdict

1. **The site is not publishable and the handover's "ready, 15 minutes" is wrong.** Nothing is live: `https://t3dy.github.io/Pico900/` returns GitHub's "There isn't a GitHub Pages site here" (404). `DEPLOYMENT_GUIDE.md`'s "S3 proof-of-concept is live" is false.
2. **The stylesheet is dead.** `site/css/style.css` was written with Python f-string double braces (`:root {{ … }}`); the browser parses every rule as empty. All 931 pages render as unstyled default HTML: no facing-page columns, no header, no responsive rules.
3. **3,716 root-absolute links lack the `/Pico900/` prefix** (index → conclusion links, prev/next, footer "About"). On Pages, no conclusion is reachable from the index. The `Sources` nav link (931 pages) points at a directory that does not exist.
4. **The handover's deploy command publishes the wrong thing.** `Copy-Item -Recurse site docs -Force` with `docs\` already present nests the site at `docs\site\` (tested). The Pages root would 404, all assets would 404, and 22 internal working documents would be served raw beside it.
5. **Roughly 73% of pages (680/929) present machine-generated template sentences as Pico's English**, under a Latin panel that says `[TO BE SOURCED FROM CRITICAL EDITION]`. The data says `template_based`; the page says nothing. The same 5 sentences repeat across whole sections (e.g. "The Trinity preserves strict monotheism." on 37 pages).
6. **Placeholders are visible to readers** on 777 of 929 pages (`[CITATION TO BE FILLED]`, `(TBD)`, `[TO_SOURCE]`, `TO BE VERIFIED`, `[TO BE EXTRACTED]`, `[WORK TITLE]`). Only 23 pages contain no placeholder string, and 7 of those have real Latin plus non-template English.
7. **Provenance and confidence are never shown.** The builder does not render translator, source, exegesis, confidence, verified flags, or page locators, even where the JSON has them.
8. **Citations are the most dangerous content**: 1,467 of 1,835 entries are placeholders; the three "real" quotations on `S7.C010` are one misattributed (Kristeller, not Wirszubski), one paraphrase in quotation styling, one not found in the source; several bibliographic identities are wrong (Deborah "Black", "John M Dougherty", "Oren Edelheit", Farmer's title).
9. **The style guides are partly invented.** The "model voice" paragraphs attributed to Copenhaver, Howlett and Edelheit appear nowhere in the corpus; the Apology timeline example contradicts Copenhaver and Howlett on five points, one of them directly ("most mature" vs "derivative and reactive"). The guide bans "not X but Y" and uses it in 5 of its 8 exemplars.
10. **None of the guide's genres (scholar profile, bibliography, timeline, people) exists** in site or data, and the guides omit every editorial convention a Latin critical edition needs.

---

## Part A — What a reader sees

### A0. Pages examined
Index `/Pico900/`, About `/Pico900/about/`, `S7.C010` (the "full-quality" tier), `H.1.1` (real text), `H.1.2` (unfilled), `S2.C005`, `S5.C005`, `S9.C050`, plus `S1.C001`, `S3.C001/C002`, `S4.C001`, `H.1.10`. Whole-site counts come from parsing all 929 conclusion pages.

### A1. BLOCKER — stylesheet does not apply
- `site/css/style.css` line 2: `:root {{`; every rule and the `@media (max-width: 768px) {{` block use doubled braces. In the browser: `document.styleSheets[0].cssRules` = 43 rules, all empty (`":root { }"`, `"* { }"`, `".header { }"`). Computed: body font Times New Roman, header background transparent, `.facing-page` `display: block`, header `position: static`.
- Cause: `scripts/build_html_site.py` line 114 `CSS = """…"""` is written verbatim (line 616–620) but was authored as a `.format()` template.
- Effect: no side-by-side Latin/English, no sticky header, no mobile breakpoint, no heretical-section colouring. The screenshot of `S7.C010` is a plain black-on-white document. The "responsive / mobile-friendly / print-friendly" claims in `DEPLOY_STATE.md` are untrue of this build.

### A2. BLOCKER — links that 404 under `/Pico900/`
Grep over `site\` (lines with `href="/…"`/`src="/…"`):

| pattern | count | resolves on Pages? |
|---|---|---|
| `/Pico900/` (home, ×2 per page) | 1,862 | yes |
| `/Pico900/css/style.css` | 931 | yes (but empty rules, A1) |
| `/Pico900/js/search.js` | 931 | yes |
| `/Pico900/about/` | 931 | yes |
| `/Pico900/sources/` | 931 | **no — directory does not exist** |
| bare `/conclusions/<id>.html` (index: 929, prev/next: 1,856) | 2,785 | **no** — resolves to `t3dy.github.io/conclusions/…`, a different site root |
| bare `/about/` (footer, every page) | 931 | **no** |

Bare total = 3,716. Fetch tests through the emulated subpath: `/Pico900/conclusions/H.1.1.html` 200; `/conclusions/H.1.1.html` 404; `/about/` 404; `/Pico900/sources/` 404.
Source: `build_html_site.py` lines 51, 463, 467, 542 hard-code root-absolute paths while the header nav uses `{base_path}`. `DEPLOY_STATE.md` says "All paths use /Pico900/"; that is false.
The handover's local test (`cd site; python -m http.server 8000`) hides this: at server root the bare links work (200) but `/Pico900/css/style.css` and `/Pico900/js/search.js` 404. Neither environment shows a working site, and the check-box "previous/next links work" cannot have been observed on the deployed path. The `AGENTS.md` DEPLOYER gate (`grep -rn 'src="/\|href="/'` must print nothing) is stricter than needed (it also flags `/Pico900/` prefixed links); read as "no bare root-absolute paths" it fails with 3,716 hits.

### A3. BLOCKER — template content presented as Pico
Data (`data/conclusions/*/entry_*.json`): 680 records have `english_translation.translator = "template_based"`, `source = "template_S1…S9"` (S1 95, S2 110, S3 109, S4 93, S5 80, S6 95, S8 8, S9 185), `status: unstarted/pending_sourcing` for most. The page shows none of this.
- English is one of 5 sentences per section: S2 5 unique of 110 pages, S5 5/80, S6 5/95, S8 5/8, S9 5/185, S3 16/120 (11 real + 5 templates). "The Trinity preserves strict monotheism.", "Christ's incarnation perfects human nature.", "The Eucharist effects real transubstantiation." each appear on 37 pages.
- Charge/Defense: 38 distinct strings across 929 pages; 13 strings cover 901 pages. One charge ("May risk heresy through syncretistic integration of pagan sources") is on 185 pages.
- Volume is invented: `S3` has 120 pages but its own data (S4.C001 citation text) speaks of "Averroes's forty-one"; `S4` has 105 pages but the same text says twelve theses secundum Avicennam. Both sections are padded to a target count, not to Pico's.
- Reader experience (`S2.C005`): Latin panel = `[TO BE SOURCED FROM CRITICAL EDITION]`; English panel = "Generation and corruption occur in the sublunar realm."; citations = "Stephen A Farmer — Syncretism in the West: Pico's Platform (TBD) [CITATION TO BE FILLED]". A first-time scholar would reasonably read the English as Pico's thesis. Nothing distinguishes it from `S3.C001`.

### A4. HIGH — Latin state across the site
Of 929 pages: 680 `[TO BE SOURCED FROM CRITICAL EDITION]`; 90 empty Latin panel (S1); 7 `TO BE VERIFIED` (H); 1 `[FROM CRITICAL EDITION: T1 — The One]`; **151 with Latin text**. Of those 151, 118 (all S7) are a single PDF line: no terminal punctuation, 22 end in a hyphen ("…animalium irratio-"). `S7.C010` Latin ends "…quam quod sit"; the English beside it runs on "…than that it is the tenth; and in its middle is set the great Adam, who is Tiferet", with a stray blank line inside the sentence. The source line in Wirszubski (md line 1720) reads "…quam quod sit decima;". 70 pages (63 S7, 7 H) show the **Latin string in the English panel** (e.g. `S7.C100`: English = "Cum fieri lucem nihil sit aliud quam participare lucem, conueniens est").
No `lang="la"` anywhere; orthography is inconsistent within the site (`conueniens`, `aedificium`).

### A5. HIGH — the "full-quality" S7 page (`S7.C010`)
Reader sees: `Conclusion S7.C010` / `Secundum Hebraeos - Kabbalah & Jewish Philosophy • Thesis ` (thesis number blank on all 118), truncated Latin, English with a hard break, **Charge `[TO_SOURCE]` / Defense `[TO_SOURCE]`** (all 118 S7 pages), three "Scholar Citations" with no page, year, or confidence; navigation links that 404 on Pages. The record's `exegesis` ("Pico's conclusion on Sefirot within the Kabbalah tradition.") and `translation_source` ("Farmer 1998") are not rendered. Historical context and philosophical depth: none. The page conveys labels ("Charge", "Defense", "Philosophical Context") without content.
Citation spot-check (S7.C010), against the source files:
1. Wirszubski, "Christian Kabbalism of the Renaissance... Pico's role was especially important because he used the Jewish Kabbala for the confirmation of Christian theology": both fragments exist, but they are two separate sentences in **Kristeller's Introduction** (md ~lines 230–250, "Introduction / Paul Oskar Kristeller"), joined by an ellipsis and credited to Wirszubski. The record marks it `"status":"verified","verified":true`.
2. Copenhaver, "Abulafia's letter explains why the futility of attempting to get at the divine…": not verbatim. The passage (Dignity, ~line 14366) begins "The futility of this approach, according to Abulafia, was trying to get at God's essence through his attributes." The page presents a paraphrase as a quotation.
3. Wirszubski, "Pico's Kabbalistic thought synthesized multiple Jewish mystical traditions through the work of Mithridates' translations": 0 matches in the Wirszubski file for "Kabbalistic thought synthesi"; not found.

### A6. HIGH — citation layer overall
1,835 citation entries in 929 pages: 368 carry text, **1,467 (80%) are placeholders**; 141 pages have at least one text citation. Where text exists the page shows author, title and quotation only. Identity problems (checked against the shelf, `E:\pdf\renaissance magic\Pico\Markdown`):

| on site | count | shelf says |
|---|---|---|
| "Deborah L Black — Logic and Intellect in Averroes" | ~233 | shelf holds *Crofton* Black, *Pico's Heptaplus and Biblical Hermeneutics* (Brill 2006); `CLAUDE.md` lists only "Black: Heptaplus hermeneutics". I did not verify whether D. Black wrote a book of the site's title; nothing on the shelf supports it. |
| "John M Dougherty — The Philosophy of Pico della Mirandola" | 185 | shelf: M. V. Dougherty (ed.), *Pico della Mirandola: New Essays* |
| "Stephen A Farmer — Syncretism in the West: Pico's Platform" | ~328 | Farmer, *Syncretism in the West: Pico's 900 Theses (1486): The Evolution of Traditional Religious and Philosophic Systems* (Tempe: MRTS, 1998; © 1998 in front matter) |
| "Edelheit, Oren — Scholasticism and Mysticism in Medieval Intellectual Culture (2008)" | 2 | shelf has Amos Edelheit, *Ficino, Pico and Savonarola* (2008), *A Philosopher at the Crossroads* (Brill 2022) |
| "Copenhaver — Pico on Trial, Ch. 5" as source for S1 Neoplatonic theses | 17 | Ch. 5 = "Is Heresy Willful? Pico's Q8" |
| "PicoDB avicenna.md — Avicenna concept page" | 4 | an internal file, not a scholarly source |
| "Howlett — [WORK TITLE]" | 1 | placeholder |

Root cause: `CLAUDE.md`'s scholar roster is surname-only with no titles; agents filled in first names and titles.

### A7. HIGH — heretical pages
- `H.1.1` (Q1 Hell, Copenhaver's numbering): shows Latin "Christus non vere et secundum existentiam realem descendit ad infernum…" and an English rendering. The record says `latin_source: "megabase"`, `latin_verified: false`, translator `"LLM"`, source "2025-07-05 Pico della Mirandola Summary.md". The page presents it as edition text. I could not find the Latin in the corpus (0 hits for "Christus non vere et secundum"); this is inconclusive, not a refutation.
- Charge on all 13 pages: "Condemned by papal bull (1486)". The bull *Et si ex iniuncto* is 4 August 1487 (Edelheit 2008 note on the Roman affair; Howlett ch. 2, p. 21). Defense on all 13: "Contains profound theological truth requiring proper interpretation" (identical; it is not Pico's Apology).
- All 13 show **"Heretical Status: None"** (null rendered as text) on pages flagged heretical.
- No citations block at all on any H page. No Apology question number, no commission finding, no link to the numbered conclusion in the 900 (the 13 are a subset of the 900, so H pages also inflate the 929 count).
- `H.1.2`: Latin "TO BE VERIFIED", English "TO BE VERIFIED", plus the generic charge/defense. 7 of 13 H pages are like this.

### A8. MEDIUM — agent working notes published as reader copy
- 20 S1 pages (S1.C061…): "Daemon and angel theses likely connected to heretical Q5 (magic/theurgy). … Check whether Iamblichan theurgy (ritual invocation of daemons) appears here; if so, mark for heretical essay."
- 15 S1 pages (S1.C081…): "Q13: Soul's union with God. Condemned as apparent denial of creature-creator distinction. See *Apology* Q13."
- `S3.C002`: "It relates to Q8 (epistemology of belief) in the heretical essay." No essay page exists.
- `S1.C001`: Charge/Defense "TO BE FILLED"; citations "[TO BE EXTRACTED]".

### A9. MEDIUM — search and navigation
- `search.js` (565 bytes) filters the index's `.conclusion-item` text: ID, section name, and the English snippet cut at ~100 characters. Measured: "Christus" 0 hits, "quam quod sit" 0, "heretical" 0, "condemned" 0, "descend" 2, "trinity" 37, "secundum" 798. Latin, charge, citations, tags are unsearchable.
- No filter by section, tier, or heretical flag (`DEPLOY_STATE.md` claims a heretical filter). The index is one 292 KB page of 929 anchors, sorted lexicographically (H first), each labelled `ID — Section` with a truncated English snippet; 131 rows show no section (all S1, all H, and the 12 real S4 and 11 real S3 records, i.e. exactly the records with the best data).
- `Sources` nav (931 pages) 404s. No essay, scholars, bibliography or timeline page. `src/templates/sources.html` and `scripts/build_sources.py` exist but `build_html_site.py` does not call them.

### A10. MEDIUM — accessibility and mobile (checked in the DOM)
- `<html lang="en">` on all 931 pages; **0 uses of `lang="la"`**; Latin inherits English.
- Two `<h1>` per page (site title in the nav plus the page title); no skip link; no `<header>` landmark (a `nav.header`); search `<input>` has no label or `aria-label` (placeholder only); no `:focus` rules.
- Contrast: moot at present because the CSS is dead; the intended palette (`#333` on white, `#e0e1dd` on `#1a1a2e`) would pass. `<title>` is "Conclusion S7.C010 - Pico900" (no incipit, no Farmer/Biondi number).
- Mobile (375 px emulation): viewport meta present, no horizontal overflow, single column (because nothing is styled). The intended `@media` breakpoint is dead (A1).
- No `robots`/`noindex`: placeholder-filled pages would be indexed.

### A11. MEDIUM — About page and index claims vs reality
About: "presents all 900 conclusions" (index says 929); "Facing-page Latin (from the critical edition)" (151 pages have any Latin; the data records `latin_source: megabase`, never `critical_edition`); "Philosophical charge and defense for each conclusion" (38 strings); "Scholar citations from leading Pico researchers" (see A6). No statement of edition base, translation source, method, status ("work in progress"), authorship, or corrections policy. Licence: "Pico's Conclusions are in the public domain" is true of the Latin only; the same page releases the apparatus under CC BY-SA 4.0 while the S7 English is credited in data to Farmer 1998 (copyright 1998 in the shelf copy) and appears verbatim in another copyrighted volume (Abravanel/Alemanno/Ogren, Supplements to the *Journal of Jewish Thought and Philosophy* 27, md line 6082). That is a licence and copyright problem the page does not disclose.

---

## Part B — Deployment hazard

### B1. What the documents say
| document | source | build | state claim |
|---|---|---|---|
| `DEPLOY_STATE.md` | branch `main`, **`/` root** | `scripts/build_site.py` | "S3 proof-of-concept … 11 Averroist conclusions"; "All paths use /Pico900/" |
| `DEPLOYMENT_GUIDE.md` (tracked) | `/` root | `build_site.py`; URLs `S3_C001.html` | "S3 proof-of-concept is live" |
| `HANDOVER.md` | **`main /docs`** | `build_html_site.py` | 929 pages, "ready", 946 HTML files |
| `C:DevPico900DEPLOYMENT_GUIDE.md` (untracked stray) | `/docs` | `build_html_site.py` | "Ready to Deploy … Just copy to docs/ and push" |

The stray file is a Windows path-mangling artifact (git prints the name as `C\357\200\272DevPico900DEPLOYMENT_GUIDE.md`; the colon became a private-use character). It is a shorter, later variant of the handover's plan and contradicts the tracked `DEPLOYMENT_GUIDE.md`. It is untracked; `git add .` would add it. It should be reviewed, then removed by the owner.

### B2. Does DEPLOY_STATE.md match reality? No.
- Live: **404, no Pages site** (single browser read of `https://t3dy.github.io/Pico900/`). Repo is public; `origin/main` (local ref, may be stale) holds 49 files and none of the 929 pages.
- "Source `/` root" vs handover `/docs`: unresolved conflict; no `.github/workflows` exists although DEPLOY_STATE says "GitHub Actions will deploy automatically".
- "S3, 11 conclusions" vs built site 929 pages (933 files: 931 html, 1 css, 1 js; 4.5 MB). Handover says "946 HTML files"; actual 931.
- `build_site.py` names pages `S3_C001.html`; the built site uses `S3.C001.html`. The guide's verification URLs do not exist.
- "All paths use /Pico900/": false (A2).

### B3. What `Copy-Item -Recurse site docs -Force` then push would do
Tested in scratchpad with PowerShell 5.1 (same tree shape):
- `docs\` exists → the site is copied **inside** it as `docs\site\…` (`docs\site\index.html`, `docs\site\conclusions\…`, `docs\site\css\…`). Re-running merges into `docs\site\`. If `docs\` did not exist, the copy would produce `docs\index.html` (the intended layout).

**Would publish:** with Pages source `main /docs` on a public repo, the site at `https://t3dy.github.io/Pico900/site/`, plus every file in `docs\` as a raw static file: at HEAD 22 `.md` and 1 `.txt` at the top level (`PICO900_STYLE_GUIDE.md`, `STYLE_GUIDE.md`, `HERETICAL_RESEARCH_PLAN.md`, `PHASE_1_RETROSPECTIVE.md`, four `PHASE_1_S*_REVIEW_REPORT.md`, `REVIEWER_R3_BRIEFING.txt`, `S1_HARVESTER_PROTOCOL.md`, `SOURCING_PROTOCOL.md`, …) and 4 more in `docs\archive\v1-pipeline\` (staged), plus untracked `docs\ORCHESTRATION.md`. These are internal handovers, agent retrospectives and review reports; they contain local paths (`E:\pdf\…`). A keyword scan for credentials found none (only prose uses of "secret"/"token"); the scan was not exhaustive. Jekyll is on (no `.nojekyll`); I expect the `.md` files without front matter to pass through as static files, but did not test because Pages is off.
**Would break:**
- `https://t3dy.github.io/Pico900/` → 404 (no `docs/index.html`; no README in `docs/`).
- At `/Pico900/site/`, every page requests `/Pico900/css/style.css` and `/Pico900/js/search.js`, which now live at `/Pico900/site/css/…` → 404. Header "Pico900/Conclusions" link → `/Pico900/` → 404. All 3,716 bare links go to `t3dy.github.io/conclusions/…` or `/about/` (a different site root) → 404.
- Best case (docs emptied first so `docs\index.html` is correct): root loads, CSS empty (A1), JS works, header About works, but no conclusion page is reachable by click, `Sources` 404s, prev/next 404. The 26 working documents would be overwritten or merged alongside (`-Force` deletes nothing), so they would still be published. The repo's own working docs need a home other than `docs/` if `docs/` is the Pages folder.
- The push itself also publishes to the repo: 35 local commits, ~1,100 tracked files including `data/` with 680 template records and the internal docs, to a public repository.

### B4. Workspace rules the plan must satisfy (`AGENTS.md` DEPLOYER, `CLAUDE.md` Hosting policy)
| rule | status |
|---|---|
| GitHub Pages default host | met (no Vercel) |
| read `DEPLOY_STATE.md` first; keep it true, "including saying not live yet" | **fails**: it describes a different build and a different source folder |
| no root-absolute paths | **fails** (3,716) |
| `VERIFIED.md` handover from VERIFIER to DEPLOYER | **absent** |
| "load the live URL afterwards and play the thing" | not possible until deployed; nothing to compare against |
| Pages base-path gotcha documented | documented but violated by the builder |
| `CLAUDE.md` working discipline ("deployed/done" only after checking the live artifact) | `DEPLOYMENT_GUIDE.md` says "live" while the URL is 404; `HANDOVER.md` ticks "Website tested locally" though the local test would show unstyled pages and 404 JS |

---

## Part C — Governance prose

### C1. Fact-check of the guides' own examples
Locators: `P9` = `docs/PICO900_STYLE_GUIDE.md`, `SG` = `docs/STYLE_GUIDE.md`. Corpus locators are md line numbers in the named file; "0 hits" = grep across all 73 files.

| claim | source finding | locator |
|---|---|---|
| P9 L22 Copenhaver model quote: "Pico's engagement with Averroism was not incidental but constitutive… zigging and zagging…" | **Not found.** 0 hits for "zigging", "zagging", "not incidental", "conceptual tools for reconciling". Presented under a real name as "Copenhaver's style (the model)". Pastiche | corpus-wide grep |
| P9 L265 "Copenhaver": "Pico's reading of Plotinus was not incidental but structural… Enneadic" | **Not found** (0 hits "Enneadic", "not incidental"). Substance doubtful: the Oration is 1486; the corpus has passages pairing 1492 and Plotinus (Allen files) that I did not read, so the chronology should be checked before anyone asserts it | corpus-wide |
| P9 L270 "Howlett": "Pico's Aristotelianism is not a departure… deliberate synthesis… reads Aristotle through Aquinas's reconciliation of Aristotle and Augustine" | **Not found** (0 hits "deliberate synthesis", "reads Aristotle through") | Howlett `…3c6c4fa3.md` and corpus |
| P9 L275 "Edelheit": "essence-existence distinction… hinge… ens necessarium… participated dependence… actus essendi" | **Not found** in Edelheit (0 hits "ens necessarium", "participated dependence", "metaphysical edifice"). "actus essendi" occurs in Copenhaver *On Trial* and a *Thomist* article; "hinge on which" only in a Corazzol article | corpus-wide |
| P9 L74 "Brian P. Copenhaver (b. 1940) is Harvard's leading historian" | Copenhaver's acknowledgments place his chair and sabbatical at **UCLA**; Harvard is only the publisher. Birth year not verifiable in the corpus | Dignity md ~L246–248; Trial md ~L443, 466 |
| P9 L74–76 Copenhaver "defense of Kabbalistic ascent… ritual theurgy… Pico's own marginalia" | Broadly supported by Del Soldato's *Speculum* review ("a mystical text… kabbalistic knowledge plays a major part"; book reconstructs how the Oration was misread). "Ritual theurgy" and "Pico's own marginalia" unsupported ("marginal" hits are unrelated) | Speculum md ~L37–55; Dignity md L9244, 13869 |
| P9 L103 *Magic and the Dignity of Man*, Harvard UP, 2019 | **Correct** (Belknap Press of Harvard UP, © 2019, ISBN 9780674238268) | Dignity md L42–66 |
| P9 L146 *Pico on Trial* (2022) | **Correct**: Oxford University Press, © 2022, "First Edition published in 2022" | Trial md L36–48 |
| P9 L99 "Wallis's 1965 Dover translation" | **Wrong publisher**: © 1965 Bobbs-Merrill; now Hackett | Heptaplus/Wallis md L71–79 |
| P9 L138 "Following his heresy indictment by the papal commission in Rome (February 1487), Pico composed his Apologia" | **Sequence wrong.** Commission appointed 20 Feb 1487; commission denounced 13 theses on 13 Mar 1487; Apologia published 31 May 1487; inquisition announced 6 Jun; Pico's submission 31 Jul; bull 4 Aug 1487 | Edelheit *Ficino, Pico and Savonarola* md L14672–14684; Howlett md L1113–1132 |
| P9 L150 "Pope Innocent VIII (indicted Pico)" | Howlett: the bull condemned "the whole book, but not the author"; an arrest warrant followed in December | Howlett md L1131–1138 |
| P9 L148 "Departure from Rome (1488)" | Howlett: fled Rome "in November" [1487], before the December warrant; caught between Grenoble and Lyon | Howlett md ~L1138–1145 |
| P9 L138 "unpublished in modern critical edition" | **Contradicted for the present**: Copenhaver (2022) cites "the very useful editions and translations of the Apology (Afr.) by Paolo Fornaciari" (Fornaciari 2010). Edelheit (2008) said none existed | Trial md L257, 526–527; Edelheit md L14700 |
| P9 L138 "Copenhaver and Howlett read the Apology as Pico's most mature philosophical work, not a defensive tract" | **Contradicted by both.** Copenhaver's theses list: "both his other published works, especially the Apology, were more derivative and reactive than creative". Howlett: the Apology "was largely a defence of the 13" | Trial md ~L2350–2358; Howlett md L1115–1116 |
| P9 L146 "Copenhaver, Pico on Trial (2022), ch. 3" | Ch. 3 is "What Can Be Taken On? Pico's Q4" (Incarnation, Henry of Ghent); the Roman affair and the thirteen are ch. 1 | Trial md L95–140 (contents) |
| P9 L146 "Howlett, *Life and Works* (2019), ch. 5" | Howlett's book is *Re-evaluating Pico: Aristotelianism, Kabbalism, and Platonism…* (Palgrave Macmillan, 2021); "Life and Works" is its **ch. 2** (p. 11), trial on pp. 20–21 | Howlett md L205–222 |
| P9 L144 "Evidence status: text exists in 16th-century manuscripts and printed editions" | The Apology was printed in 1487 (first edition used by Copenhaver) | Trial md L526–527 |
| P9 L178 Savonarola "likely first encountered… Bologna in the late 1470s… (see Walden, *Savonarola*, 2011)" | Supported in part: Walden says the relationship "probably began in the late 1470s" at Bologna, "definite encounter… around 1480" at the Reggio Emilia Dominican chapter. But the source is Justine Walden (Yale), "An Anatomy of Influence: Savonarola and Pico" (file metadata `SavPicoPresentRSA2012`, a 2012 conference paper), not "Savonarola, 2011" | Walden md L96–100, 12, 22 |
| P9 L176 Savonarola "trained at Ferrara… compendium (1495)" | Ferrara and *Compendium of Revelations* 1495: **confirmed** | Walden md L88–98 |
| P9 L176 "active as a preacher from the late 1470s… San Marco 1482 where he developed a following" | Edelheit: first sermons 1482–1487 **failed**; he left and returned in 1490, then became popular | Edelheit md L18910–18922 |
| P9 L178 "During Pico's heresy crisis (1487), Savonarola was among his defenders, and the two corresponded" | **No support found** in Walden or Edelheit. Walden's sequence: flight and imprisonment (1487–88), Lorenzo's harbour, then Pico persuades Lorenzo to summon Savonarola (1490) | Walden md L108–113 |
| P9 L178 "Savonarola delivered a funeral oration praising Pico's holiness" | **Not found.** Walden: Pico was buried at San Marco in the Dominican habit "by the hands of Savonarola himself". Edelheit refers to Savonarola's "famous words on Giovanni Pico… after his death" (Burckhardt attacked them). A sermon or remark, not a documented oration | Walden md L148–151; Edelheit md L19373–19376 |
| P9 L180 "Howlett argues Savonarola's theology… shaped Pico's final turn" | Not tested (Howlett mentions Savonarola 63 times); unverified | — |
| SG L92 heretical conclusions "condemned by Pope Innocent VIII in 1486" | 1486 = publication of the theses (6 Dec 1486). The bull is **4 August 1487** | Edelheit md L14672–14684 |
| SG L132–136 essay clusters by Question number | Copenhaver's table: Q1 Hell, Q2 Sin, Q3 Worship, Q4 Incarnation, Q5 Kabbalah, Q6/Q9/Q10 Eucharist, Q7 Origen, Q8 Belief, Q11 Miracle, Q12 God, Q13 Soul. The guide's clusters get **7 of 13 wrong** (Q1–3 as "Incarnation", Q4/Q7/Q11 as "Soul", Q13 as "miracle"); Q5, Q6, Q8, Q9, Q10, Q12 fit | Trial md L845–849 |
| SG L175 example "Conclusion I.1.2 — Anima est forma substantialis corporis" | Not found in the corpus; ID scheme `I.1.2` matches neither the repo (`S1.C042`, `H.1.1`) nor Farmer/Biondi numbering; the incipit is not an attested Pico conclusion | corpus-wide |
| SG L196 Howlett, *Pico's Three Paths to the Absolute*, p. 18, quotation | **No such title** (0 hits) and quotation not found; Howlett's book is *Re-evaluating Pico* (2021). Tagged `[CITED]` | corpus-wide |
| SG L199 Edelheit, *A Philosopher at the Crossroads*, p. 156, quotation | Real book (Brill 2022) but the quotation is **not found** (0 hits "scholastically orthodox", "radical materialism"). Tagged `[CITED]` | corpus-wide |
| SG L183 "compare Copenhaver *Pico on Trial* p. 103" | p. 103 falls in ch. 3 (Incarnation), not hylomorphism | Trial md L95–140 |
| README "condemned propositions" dated 1486; site H pages "papal bull (1486)" | 4 Aug 1487 | as above |

Pattern: the examples that carry real names, titles and page numbers are wrong or invented, and agents are told to imitate them. The two guide examples that are checkable and right are the two publisher/year facts (Harvard 2019, OUP 2022).

### C2. Internal contradictions
**"not X but Y".** `P9` L42 bans "It's not X, but rather Y". Exemplar blockquotes in `P9`: 8. Five contain the exact form: L22 (twice: "not incidental but constitutive… not as a monolithic… but as a dialectical"), L180 ("not isolated humanism but embeddedness"), L265, L270 ("not a departure… but rather a deliberate synthesis"), L275 ("not merely a logical tool but the hinge"). The other three use the same contrast by negation ("rather than recanting, Pico…", "not a defensive tract" L138; "rather than humanist philosophy" L74; "not on human autonomy" L107). So 8/8 exemplars rely on it, 5/8 in the banned form. L240 (Do These Things) quotes the L22 sentence as the model opening; L272 explicitly defends a "not X but Y" as acceptable when qualified; L285 closes "The goal is not… The goal is to…". `SG` has one instance (L186 "not a separate substance… but rather"). Other banned items in the exemplars: "remarkable document" (L138), "definitive", "must-read" (L107, L113); L219 bans "genius".
A `scripts/style_lint.py` (untracked, from another session) has a `not_x_but_y` marker but skips blockquotes, so the exemplars would be exempt; it cites `docs/EDITORIAL_STANDARD.md`, which does not exist in `docs/` as of my read. Not audited.

**Guide vs guide vs data.**
| dimension | `PICO900_STYLE_GUIDE` | `STYLE_GUIDE` | data/schema |
|---|---|---|---|
| register | assertive, no hedging, no "often/sometimes", name-or-omit | provenance first, "Avoid paraphrases", mark uncertainty | — |
| unit of prose | 100–300-word synthesised blocks | quotation-led, 1–2-paragraph exegesis | exegesis is a one-line stub on all records seen |
| confidence | Evidence Status: Verified/Likely/Probable/Uncertain/Placeholder | `[VERIFIED]`/`[CITED]`/`[INFERRED]` | citation `confidence` VERIFIED/CITED/INFERRED (schema); S7 uses `status:"verified"`, `verified:true`; templates use `confidence:"CITED"` on a placeholder |
| status enum | — | unstarted/draft/sourced/complete/reviewed | schema same; data uses **`standardized`** (236 records), `pending_sourcing`; translators enum `LLM`/`Ted Hand`, data has `template_based` |
| citation format | Chicago 17th, author-date in text `(Copenhaver 2019, 156–158)`, BibTeX for each | `**Scholar** (*Work*, p. X): "…"` | site shows name — title — quotation, no year or page |
| conclusion ID | — | `I.1.2` | schema example `I.1.1`; data `S1.C001`, `H.1.1` |
| condemnation date | Feb 1487 (commission) | 1486 | site 1486 |
| authority | "Authoritative for all contributor writing" | no status line | — |
Also: neither guide says which governs; `SG` names `scripts/check_citations.py`, `scripts/validate_schema.py` and `docs/HERETICAL_ESSAY_OUTLINE.md` (file is `HERETICAL_ESSAY_DRAFT_OUTLINE.md`; scripts absent). `README.md` names `docs/COMMENTARY_PROTOCOL.md`, `docs/HERETICAL_ESSAY_PLAN.md`, `scripts/fetch_critical_edition.py`, `scripts/merge_translations.py` (none present) and features (filter by theme/scholar, cross-references, essay) the site lacks. `CLAUDE.md`'s file tree (`conclusions_raw.json`, `data/scholarship/citations.json`, `src/templates/conclusion.html`) is not the real layout (`data/conclusions/<sec>/entry_*.json`; `data/scholarship/` is empty).

### C3. Are the genre specs implemented?
No. Scholar profile, bibliography entry, biography timeline and people/figures: no page, no data file, no template. `data/scholarship/` is empty; `data/scholarships/` holds only `angels`; `data/sources.json` and `src/templates/sources*.html` exist but the build does not use them; the nav link to `/sources/` 404s. The Savonarola, Apology and Copenhaver examples are the only instances of those genres anywhere, and they are the defective ones tested above.

### C4. What the guides lack for a PhD-level edition of a Latin text
1. **Edition base and witnesses**: which text (1486 Rome princeps; Kieszkowski 1973; Biondi 1995; Farmer 1998; the Kabbalistic conclusions' separate edition), the copy-text rule, and where Brown's edition sits. The data says `latin_source: megabase` or Farmer, never `critical_edition`.
2. **Latin editorial conventions**: orthography (u/v, i/j, æ/e, `conueniens`), abbreviation expansion and its marking, punctuation, capitalisation, hyphenation across lines (22 S7 records end mid-word), lacunae and conjectures, an apparatus criticus (or a decision not to have one), how variants are shown.
3. **Translation policy and copyright basis**: Latin is public domain; Farmer's English (© 1998) is not, nor any modern translation. The guides say "cite source" and allow "original translation by Ted Hand 2026", yet data carries `LLM` and `template_based`. Missing: whose translation is displayed, permission or fair-use limits on quotation length, disclosure of machine translation, a rule that a template sentence may never appear in the English slot.
4. **How to cite a conclusion**: Farmer/Biondi numbering versus the repo's `S1.C042`/`H.1.1`; whether the 13 condemned are cross-references to numbered conclusions or separate entries (currently 929 = 916 + 13, not 900); persistent URLs and edition-version citation.
5. **Editorial voice versus source voice**: how to mark Pico's words, the commission's charge, a scholar's quotation, an LLM-synthesised charge/defense, and the editor's comment. `SG` marks only "Ted Hand (2026)" commentary; the site prints synthesised text under "Charge/Defense" with no label.
6. **Quotation fidelity rules**: ellipses across sentences, bracketed insertions, page locators mandatory, no paraphrase in quotation styling, who wrote a quoted introduction (the Kristeller/Wirszubski error).
7. **A verification standard** tying `[VERIFIED]` to an independent check with locator and checker, and a required record when a claim fails verification.
8. **Status and provenance display**: what a reader must see on every page (translator, source, verified flags, draft banner, hide-or-badge rule for unfilled fields).
9. **Bibliographic authority list**: full author names, titles, publishers, years for each cited scholar (the `CLAUDE.md` roster is surname-only and produced the A6 errors).
10. **Historical conventions**: dates (1486 publication, 1487 condemnation), place names, personal names (Pico/Giovanni), Hebrew/Arabic/Greek transliteration, Q-number scheme for the Apology, and how Copenhaver's numbering relates to the commission's.
11. **Accessibility and language tagging** (`lang="la"`, headings, keyboard use) and a corrections/versioning policy.

---

## What I could not verify, and why
- **Live site beyond one read.** I loaded `https://t3dy.github.io/Pico900/` once (404). I did not check `t3dy.github.io/` (user site) nor GitHub Pages settings, so which source folder is configured, and what a bare `/conclusions/…` would resolve to, is inferred from URL structure.
- **Jekyll behaviour** for the `.md` files in `docs/`: expected to serve as static files; untested because Pages is off.
- **The Latin and English of `H.1.1`** and of other pages against a critical edition: the Brown edition, Farmer's Latin and Biondi were not fetched or opened as text; only corpus greps were possible, and OCR/line-break variance can hide matches (my "not found" results rest on short distinctive phrases, several of which are ordinary words such as "zigging").
- **Copenhaver's birth year**, **Howlett on Savonarola's influence**, **Deborah Black's bibliography**, and **whether Copenhaver's Q4 chapter assigns a different scope than I read** from the contents page and table only.
- **Plotinus chronology** for the Oration (flagged, not resolved).
- **Section taxonomy** (S1–S9 vs Pico's actual divisions and counts): I saw internal contradictions (S3 120 vs "forty-one", S4 105 vs "twelve") but did not audit the taxonomy; `docs/CRITICAL_EDITION_TAXONOMY.md` was not read.
- **Screen-reader behaviour**: DOM inspection only; no assistive technology. Keyboard and contrast were inferred from CSS and markup, and contrast is moot until A1 is fixed.
- **Mobile**: one emulated width (375 px), one page, unstyled.
- **Secrets**: keyword scan of `docs/`, top-level `.md` and `scripts/` only; not a full secret scan of `data/` or history.
- The tree was changing under me (another session's staged renames and new files); if `docs/` has since changed, B3's file list will differ.
