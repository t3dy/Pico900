# Site design: cards, relational browsing, tours and the Workbench

Status: v1 specification, 2026-09-26. Answers P20260926004626 (Sources tab), P20260926005522 / P20260926005916 (People tab,
PicoDB merge), P20260926041418, P20260926041446, P20260926041502 (dense, colour-coded, sortable, searchable cards),
P20260926041711 (logins and personal collections; best-practice relational browsing; relevance of every thesis to Pico's
relationships), P20260926041806 (the guided essay on Ficino and Pico). Data comes from `docs/CLAIMS_MODEL.md`,
`docs/DATA_ONTOLOGY.md` and `docs/INTELLECTUAL_NETWORK_DESIGN.md`; hosting rules from `DEPLOY_STATE.md` and the workspace
hosting policy. Nothing here is built until a ticket in `data/tickets/` says so.

## 1. Principles

1. **Overview first, zoom and filter, details on demand** (Shneiderman). A card is the overview; expanding it is the detail;
   nothing on a card is decoration, every mark encodes a datum.
2. **The evidence is on the card.** A reader who meets a claim sees its quotation, its source and line, and its verification
   state without leaving the page. This is the edition's answer to the audit: no assertion without visible evidence.
3. **Every card is a node.** Every named thing on a card (a person, a work, a topic, a thesis) is a link to that thing's card,
   and every card lists what links to it (backlinks). Browsing is following relations; search and filters are the way in.
4. **Never colour alone.** Every colour channel is doubled by a shape, label or pattern (colour-blind safe palette, e.g.
   Okabe-Ito; WCAG AA contrast; full keyboard operation; screen-reader labels on badges and bars).
5. **Honest empties.** A missing field renders "not yet edited" or "no evidence yet", never a blank that looks like zero and never
   filler. Scores show their components on demand.
6. **Static first.** The public edition is a static site on GitHub Pages (workspace policy). Anything dynamic is either client-side
   over pre-built JSON or lives in the Workbench (section 8), which is a separate application.

## 2. Vocabulary (what the pieces are called)

| term | plain meaning | here |
|---|---|---|
| **card** | a small, self-contained summary of one thing, clickable | thesis card, claim card, person card ... |
| **frame** | the card's layout and chrome: header, body, footer, badges | three sizes: compact, standard, expanded |
| **badge / chip** | a small labelled tag | tradition chip, evidence badge, "condemned" badge |
| **facet** | a property you can filter or group by | tradition, topic, person, evidence level |
| **facet panel** | the sidebar of filters with counts | left column of every list page |
| **sort menu** | choose the ordering | importance, Farmer order, relevance to Ficino |
| **lens** | a saved combination of filters, sort and colour-by | "Ficino dispute", "condemned theses" |
| **detail drawer** | a panel that slides in beside the list to show a card in full without losing your place | opens on click |
| **backlinks** | "what points here" | footer of every card |
| **trail** | the path of cards you followed, as breadcrumbs, with back and forward | top bar |
| **tour** | a guided essay: prose with cards inset at each stop, previous and next | the Ficino essay |
| **collection / board** | a set of cards a reader keeps for a research or writing project | Workbench |
| **note** | the reader's own text attached to a card | Workbench |
| **relation strip** | a row of related cards under a card | "same claim", "contradicted by" |
| **ego graph** | the network around one node | People and Topic pages |
| **provenance state** | how well founded the card's content is | verified, sampled, unverified, not yet edited |

## 3. Card types

| type | source data | headline | what the body shows |
|---|---|---|---|
| **Thesis** | `data/inventory/theses.json`, `data/ontology/`, claims with `theses` | Farmer id, Latin incipit, English gloss | attribution and Pico's stance; historiographical importance; mention count and which scholars; condemned mark and Apology question; relevance bars per party; open questions count |
| **Claim** | `data/claims/**` + `scores.json` | the restatement | the verbatim quotation(s) with work and line; warrants; hedge; open questions; links (supports, contradicts); evidence level; importance components |
| **Passage** | claims with `attribution: primary_text` | Pico's words, locus (e.g. Oration section 35) | quotation, translation source, who comments on it (claims about it), textual cruxes |
| **Person** | `data/network/persons.json` (network system) | name, dates, role | relationship list by type and evidence level; theses and passages that concern them; relevance ranking; ego graph |
| **Relationship** | `data/network/relationships.json` | "Pico and Ficino: disagreement over the One" | type, dates, evidence list (claims), the cards it touches |
| **Source** | `data/sources.json` (being rebuilt), corpus registry | title, author, tradition | the 30-100 word blurb (P20260926004626), sortable by tradition; which theses cite it; "read in the corpus" |
| **Scholar / Work** | corpus registry, `data/ontology/mentions/` | author, book | what it argues, chapters mined, claims count, mention statistics |
| **Topic** | `data/claims/topics.json` + `scores.json` | topic label | top claims, who says what, disagreements, open questions, Pico loci |
| **Question** | `open_questions.json` | the open question | the claim it arises from, the source's own words, which topic, importance of the parent claim |

## 4. Card frames

Three sizes, one grammar. The same fields, disclosed progressively.

```
COMPACT (list rows and dense grids)
+--[kind icon] 4>13  "Quod nulli ..."                     [condemned Q4] [primary]     [+] [cite]
|  ▮▮▮▮▯ Ficino   ▮▯▯▯▯ Savonarola      3 scholars · 2 open questions · evidence 5

STANDARD (default grid card)
+---------------------------------------------------------------------------------+
| header:  [icon] TYPE   id / locus                        badges: tier · evidence  |
| title:   the claim or thesis in one line                                        |
| body:    2-3 lines: restatement, or Latin incipit + gloss                       |
|          "verbatim quotation ..." (Black, l. 8408)                [show more]     |
| strip:   tradition chip · topic chips · claimant                                 |
| bars:    relevance to parties (colour per party, length = score)                |
| footer:  [expand] [open page] [+ collect] [copy quote] [cite]   links: 5 · backlinks: 3 |
+---------------------------------------------------------------------------------+

EXPANDED (detail drawer / card page)
 tabs:  Evidence | Warrants | Open questions | Relations | Scores | Sources
   Evidence:   every quotation with work, line, page (if evidenced) and verification verdict
   Warrants:   how the source supports the claim; kind and strength
   Open:       what is unsettled, in the source's own words where it says so
   Relations:  supports / contradicts / qualifies / depends on, each with its basis, as clickable cards
   Scores:     importance components as bars (centrality, corroboration, contestation, warrant, reach, frame shift [judged])
   Sources:    the passage in the source with context (+/- 10 lines), link to the corpus location
```

Card state is always visible in the header: `verified` (quotation located and restatement sampled), `unverified`,
`sampled-flagged` (the second verifier said the restatement overreaches), `not yet edited`. An unverified claim never
renders as a claim; it renders in a "leads" list with that label.

## 5. Colour and shape encoding (one channel per meaning)

| meaning | channel | values |
|---|---|---|
| Tradition of a source or person | hue of the left border and chip | scholastic, Platonic/Neoplatonic, Aristotelian, Arabic, Kabbalistic/Hebrew, Hermetic/Chaldean, Patristic/Dionysian, humanist/contemporary |
| Party (relationship) | hue of the relevance bar and chip, distinct from tradition hues | one fixed colour per party (Ficino, Poliziano, Savonarola ...) |
| Evidence level (5-0) | border style | solid heavy 5, solid 4, dashed 3, dotted 2, hollow 1 |
| Importance tier | ribbon and card size | primary (ribbon, wider in grids), secondary, tertiary |
| Contested | corner mark | two opposed arrows |
| Condemned thesis | dark red seal icon | with Apology question number |
| Hedge (source's own stance) | word on the card | "hedged", "speculative", never colour only |
| Provenance state | icon plus word | verified tick, unverified question, flagged exclamation |

A `colour by` control on every list lets the reader switch which channel drives colour (tradition, party, evidence, tier),
so the density of a page is the reader's choice. Palette and contrast are checked in `docs/SITE_DESIGN.md` s10 tests.

## 6. Controls: sorting, filtering, searching

**Sort menu** (every list): importance (default for claims), Farmer order (theses), relevance to a chosen party, evidence
level, date of source, contested first, most open questions, alphabetical, recently added. A `relevance to` picker chooses
the party; the list then sorts by that party's score and shows its bar first.

**Facet panel** with live counts: kind of card, tradition, topic, person/party, work or scholar, claim type, evidence level,
importance tier, hedge, has open questions, contested, condemned, Pico text (Oration, Heptaplus, Commento, De ente, 900),
verified only (default on for claims). Facets combine with AND across facets, OR within a facet. Active filters show as
removable chips above the results; the URL carries all state (`?f=topic:de-ente&sort=rel:ficino`) so any view can be shared,
bookmarked and cited.

**Search.** Client-side full-text over pre-built JSON (a small index such as MiniSearch or Lunr generated at build time, sharded
by card type so a page loads only what it needs). Fielded queries: `claimant:black`, `topic:three-worlds`, `work:allen2017`,
`party:ficino`, `"exact phrase"`, `thesis:4>13`. Results are cards with the matching quotation highlighted. Search over
quotations and search over restatements are separate toggles: the reader should know whether they are searching a
scholar's words or our paraphrase.

**Click boxes and buttons** on every card: expand, open page, copy quotation with citation, copy citation (Chicago, plus BibTeX
for the work), collect (+), compare (select two cards, see them side by side: same topic, different claimants), "why is this
card here?" (shows the query, filters or relation that produced it), report an error (opens a prefilled issue).

## 7. Relational browsing

- **Everything named is a link.** People, works, theses, topics, Pico loci. Links carry a hover preview (the target's compact card).
- **Relation strips** under each card: *same claim in other scholars*, *contradicted by*, *qualified by*, *depends on*, *cited
  by*, *bears on Ficino / Poliziano / ...*, *concerns theses ...*.
- **Ego graph** on Person and Topic pages: nodes coloured by tradition, edge style by relationship type (solid documentary,
  dashed inferred), edge weight by evidence level; click a node to open its card; a slider hides evidence below a level.
  A list view of the same data is always offered (accessibility, and graphs mislead when dense).
- **Matrix view** for relevance: theses (rows) by parties (columns), cell shading = relevance; click a cell for its evidence.
  This is the "relevance of every thesis to his relationships" view (P20260926041711 and the clarification that it applies to
  anyone he corresponded or quarrelled with).
- **Timeline** of Pico's life and works with relationships overlaid: 1486 Rome print, the commission of 1487, the bull of 4 August
  1487, the Heptaplus (1489), De ente et uno (1491), Ficino's and Poliziano's letters. Dates come only from verified claims.
- **Trail and back-forward** keep the reader oriented; **compare** puts two cards side by side; **lenses** save a whole
  configuration under a name and a URL.
- **Neighbours of a thesis:** Farmer's own cross-references (`data/ontology/connections/farmer_crossrefs.json`) as a strip on
  every thesis card; they are already evidence-grade data.

## 8. Tours (the guided essay)

A **tour** is an essay page whose paragraphs carry stops. Each stop pulls in cards (claims, passages, persons) inline, in the
essay's own order, with previous/next, a progress rail, and "leave the tour here" links that open the free browser at the
card's page with the trail intact. The first tour is the Ficino-Pico essay (P20260926041806):

1. Ficino's position on the One and Being (claims from Allen, Edelheit 2008, Howlett).
2. Dionysius and the Latin West; Aquinas's encounter with Dionysius (claims from Edelheit 2022, Howlett, Copenhaver).
3. *De ente et uno*, chapter by chapter (passages from the Miller translation; each step of the argument a stop).
4. Pico's moves against Ficino, and the contemporary reaction (Cittadini; Poliziano's role; the letters).
5. What is still open (the tour's last stop is an "open questions" card set).

Tour data is a JSON list of stops: `{id, title, prose (with [[claim-ids]]), cards: [ids], next}`. The prose passes
`scripts/commentary_check.py`; the cards are pulled by id, so a tour can never show something unverified.

## 9. Data contract for the front end

The builder writes JSON shards; the pages are vanilla JS (workspace idiom; no framework needed for the static edition).

```
site/data/cards/<type>.json          array of cards (compact fields) for lists and search
site/data/card/<id>.json             one card in full (expanded fields), fetched on open
site/data/facets.json                facet definitions and value counts
site/data/relevance.json             party -> card -> score and evidence ids
site/data/graph.json                 nodes and edges (from claims graph and network relationships)
site/data/index/<type>.idx.json      pre-built search index shard
site/data/tours/<slug>.json          tour stops
```

A card (compact):

```json
{ "id": "black2006-b:014", "type": "claim", "title": "...restatement...", "claimant": "Crofton Black",
  "topics": ["three-worlds"], "tradition": "platonic", "evidence": 4, "tier": "primary", "importance": 71.5,
  "state": "verified", "hedge": "assertive", "contested": true, "open_questions": 2,
  "quote": {"text": "...", "work": "black2006", "line": 8408}, "links": {"contradicts": ["allen2017-venus:031"]},
  "relevance": {"ficino": 0.62}, "pico_locus": "heptaplus | second proem", "theses": [] }
```

Everything on a card is derived from `scores.json`, `relevance.json`, the packets and the network files by one script; nothing on
a card is typed by hand. Rebuilding is idempotent. The builder refuses to emit a claim card whose claim is not verified.

## 10. Verification of the interface (before anyone calls it done)

Workspace rule: load the built page, drive it, read what it shows. For this interface: serve at the real base path
(`/Pico900/`), open a list page, apply two facets and a sort, confirm counts and order against the JSON; search a phrase from a
quotation and confirm the highlight is verbatim; open a card, follow a relation, use back; collect a card and reload (state
persists); tab through the page with the keyboard; check the colour channels under a greyscale filter; check narrow-screen layout.
Record what was driven in `VERIFIED.md`, with what remained unconfirmed.

## 11. The Workbench: logins and personal collections (full-stack)

Reader accounts, collections, notes and saved lenses need a server. That is the stated reason the workspace hosting policy
asks for before using Vercel (P20260926041711); the public edition stays on Pages.

**Stage 1, no server (build first).** Collections in the browser (`localStorage`/IndexedDB), on the static site: collect
cards, group them into named boards, add notes, save lenses, export. The data model below is the same one Stage 2 uses, so
nothing is migrated by hand. Export formats: Markdown outline with footnoted quotations (feeds writing), CSL JSON/BibTeX for the
works, JSON of the board for re-import.

**Stage 2, full stack.** A separate app (the Workbench) on a host that can run a server, reading the same static JSON for
content and storing only user data.

| entity | fields |
|---|---|
| User | id, email or provider id, display name, created |
| Project | id, user, title, question (the research question), created, updated, visibility (private, link, public) |
| Collection | id, project, title, order |
| CollectionItem | id, collection, card id, added, position, colour label |
| Note | id, user, target (card id, collection item, or project), body (Markdown, may cite `[[claim-id]]`), created, updated |
| SavedLens | id, user, name, filter and sort state (the URL query), created |
| ShareLink | id, project, token, expires |

Rules: cards are referenced by id only (content is never copied into user data, so a corrected claim corrects every collection); if
a card id disappears or is demoted from verified, the item shows "this card has changed" and keeps the reader's note; a note that cites
a claim is checked with the same `[[id]]` syntax and shows the claim's quotation on hover; export always includes the quotation
and locator. Authentication by a managed provider (email link or OAuth); no passwords stored by us; the app holds no secrets in
the repository (workspace rule: secrets never pass through chat, they go into the host's secret manager). Data export and
deletion for every user from day one. The choice of host and auth provider is recorded in `DECISIONS.md` when Stage 2 starts.

Writing support: a **draft view** where the reader writes with `[[...]]` citations against their collection and the Workbench
runs the same `commentary_check` logic client-side, so a user's own essay gets the same discipline as the edition's.

## 12. Build order (tickets in `data/tickets/`)

| ticket | deliverable |
|---|---|
| T-SITE-01 | `scripts/build_cards.py`: cards, facets, search index and card pages from claims, scores, relevance (prototype for the angelology and Ficino topics) |
| T-SITE-02 | card frames, colour and control CSS/JS; sort, facets, search, expand, collect (localStorage) |
| T-SITE-03 | relation strips, backlinks, trail, compare; ego graph and matrix view |
| T-SITE-04 | tour template and the Ficino-Pico tour |
| T-SITE-05 | Sources tab and People tab from `data/sources.json` (rebuilt) and `data/network/` |
| T-SITE-06 | thesis cards for all 900 with relevance bars (needs T-REL-02) |
| T-SITE-07 | Workbench Stage 1 (browser collections and export) |
| T-SITE-08 | Workbench Stage 2 (accounts, server storage, sharing) |
| T-SITE-09 | interface verification pass (s10), then DEPLOYER steps in `DEPLOY_STATE.md` |
