/* Card explorer (docs/SITE_DESIGN.md). Vanilla JS, no dependencies. State lives in the URL hash so any view can be shared.
   Cards are verified claims; the evidence (quotations, warrants, open questions, relations) loads on demand per packet. */
(function () {
  "use strict";
  var app = document.getElementById("app");
  var BASE = app.getAttribute("data-base");
  var LS = "pico900.collection.v1";
  var cards = [], facets = null, byId = {}, detailCache = {}, colour = {}, partyName = {}, trName = {};
  var TIERS = ["primary", "secondary", "tertiary"];
  var EVL = { 5: "5 Pico's own words", 4: "4 scholar, warranted by Pico's text", 3: "3 scholar, warranted by scholarship", 2: "2 asserted, no stated warrant", 1: "1 speculative" };
  var TYPES = { doctrinal_content: "doctrine", source_identification: "source", interpretive_position: "interpretation", historical_event: "history", textual_crux: "textual crux", method: "method", reception: "reception" };
  var ATT = { scholar_claim: "scholar's claim", scholar_report: "scholar reports another", primary_text: "Pico's own words" };
  var FLAGS = { contested: "contested by another scholar", openq: "has open questions", primary: "Pico's own words" };
  var S = { q: "", where: "both", sort: "imp", colourBy: "trad", view: "grid", limit: 60, relParty: "", f: { topic: [], party: [], trad: [], who: [], work: [], typ: [], tier: [], ev: [], hg: [], flag: [] } };
  var coll = loadColl();
  var nodes = {};

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function loadColl() { try { return JSON.parse(localStorage.getItem(LS) || "[]"); } catch (e) { return []; } }
  function saveColl() { try { localStorage.setItem(LS, JSON.stringify(coll)); } catch (e) { /* storage may be blocked */ } }
  function get(url) { return fetch(url).then(function (r) { if (!r.ok) { throw new Error(url + " " + r.status); } return r.json(); }); }

  /* ---------- state <-> URL ---------- */
  function readHash() {
    var p = new URLSearchParams(location.hash.slice(1));
    S.q = p.get("q") || ""; S.sort = p.get("sort") || "imp"; S.colourBy = p.get("colour") || "trad"; S.view = p.get("view") || "grid";
    S.where = p.get("in") || "both"; S.relParty = p.get("rel") || ""; S.open = p.get("open") || "";
    Object.keys(S.f).forEach(function (k) { var v = p.get(k); S.f[k] = v ? v.split("~") : []; });
  }
  function writeHash() {
    var p = new URLSearchParams();
    if (S.q) { p.set("q", S.q); }
    if (S.sort !== "imp") { p.set("sort", S.sort); }
    if (S.colourBy !== "trad") { p.set("colour", S.colourBy); }
    if (S.view !== "grid") { p.set("view", S.view); }
    if (S.where !== "both") { p.set("in", S.where); }
    if (S.relParty) { p.set("rel", S.relParty); }
    Object.keys(S.f).forEach(function (k) { if (S.f[k].length) { p.set(k, S.f[k].join("~")); } });
    var h = p.toString();
    if (("#" + h) !== location.hash) { history.replaceState(null, "", h ? "#" + h : location.pathname + location.search); }
  }

  /* ---------- search and filters ---------- */
  function parseQuery(q) {
    var toks = [], re = /(\w+):"([^"]+)"|(\w+):(\S+)|"([^"]+)"|(\S+)/g, m;
    while ((m = re.exec(q))) {
      if (m[1]) { toks.push({ f: m[1].toLowerCase(), v: m[2].toLowerCase() }); }
      else if (m[3]) { toks.push({ f: m[3].toLowerCase(), v: m[4].toLowerCase() }); }
      else { toks.push({ f: "", v: (m[5] || m[6]).toLowerCase() }); }
    }
    return toks;
  }
  function hay(c) {
    if (c._hay) { return c._hay; }
    c._hay = { r: (c.text + " " + c.loc + " " + c.tp.join(" ")).toLowerCase(), q: (c.q + " " + c.who).toLowerCase() };
    return c._hay;
  }
  function tokOk(c, t) {
    var v = t.v;
    if (t.f === "claimant" || t.f === "who") { return c.who.toLowerCase().indexOf(v) >= 0; }
    if (t.f === "topic") { return c.tp.some(function (x) { return x.indexOf(v) >= 0; }); }
    if (t.f === "party") { return Object.keys(c.rel).some(function (x) { return x.indexOf(v) >= 0; }); }
    if (t.f === "work") { return c.w.toLowerCase().indexOf(v) >= 0; }
    if (t.f === "type") { return c.typ.indexOf(v) >= 0; }
    if (t.f === "tier") { return c.tier === v; }
    if (t.f === "thesis") { return c.th.indexOf(v) >= 0; }
    if (t.f === "locus") { return c.loc.toLowerCase().indexOf(v) >= 0; }
    var h = hay(c);
    return S.where === "restatement" ? h.r.indexOf(v) >= 0 : S.where === "quotation" ? h.q.indexOf(v) >= 0 : (h.r.indexOf(v) >= 0 || h.q.indexOf(v) >= 0);
  }
  var FACET = {
    topic: function (c) { return c.tp; }, party: function (c) { return Object.keys(c.rel); }, trad: function (c) { return [c.tr]; },
    who: function (c) { return [c.who]; }, work: function (c) { return [c.w]; }, typ: function (c) { return [c.typ]; },
    tier: function (c) { return [c.tier]; }, ev: function (c) { return [String(c.ev)]; }, hg: function (c) { return [c.hg]; },
    flag: function (c) { var o = []; if (c.cx) { o.push("contested"); } if (c.oq) { o.push("openq"); } if (c.att === "primary_text") { o.push("primary"); } return o; }
  };
  function passes(c, skip, toks) {
    for (var k in S.f) {
      if (k === skip || !S.f[k].length) { continue; }
      var vals = FACET[k](c);
      if (!S.f[k].some(function (x) { return vals.indexOf(x) >= 0; })) { return false; }
    }
    for (var i = 0; i < toks.length; i++) { if (!tokOk(c, toks[i])) { return false; } }
    return true;
  }
  function sorted(list) {
    var rp = S.relParty, s = S.sort;
    var key = {
      imp: function (c) { return -c.imp; }, ev: function (c) { return -c.ev * 1000 - c.imp; }, oq: function (c) { return -c.oq * 1000 - c.imp; },
      cx: function (c) { return (c.cx ? -1000 : 0) - c.imp; }, links: function (c) { return -c.nl * 1000 - c.imp; },
      rel: function (c) { return -((c.rel[rp] || 0) * 1000) - c.imp; }
    }[s === "rel" ? "rel" : s] || function (c) { return -c.imp; };
    if (s === "who") { return list.slice().sort(function (a, b) { return a.who.localeCompare(b.who) || (b.imp - a.imp); }); }
    return list.slice().sort(function (a, b) { return key(a) - key(b) || (a.id < b.id ? -1 : 1); });
  }

  /* ---------- rendering ---------- */
  function cardColour(c) {
    if (S.colourBy === "party") { var best = "", bs = 0; Object.keys(c.rel).forEach(function (p) { if (c.rel[p] > bs) { bs = c.rel[p]; best = p; } }); return best ? colour[best] : "#b0a99e"; }
    if (S.colourBy === "tier") { return { primary: "#7a2e1d", secondary: "#c08a5a", tertiary: "#d9cbb8" }[c.tier]; }
    if (S.colourBy === "ev") { return { 5: "#1b5e20", 4: "#2e7d32", 3: "#7cb342", 2: "#c0ca33", 1: "#e0d9a0" }[c.ev]; }
    return trName[c.tr] ? trName[c.tr].colour : "#b0a99e";
  }
  function pbars(c) {
    var ps = Object.keys(c.rel).sort(function (a, b) { return c.rel[b] - c.rel[a]; }).slice(0, 3);
    if (!ps.length) { return '<div class="meta" style="font:.72rem sans-serif">no evidence yet of bearing on a relationship</div>'; }
    return '<div class="pbars" aria-label="relevance to Pico\'s relationships">' + ps.map(function (p) {
      var pc = Math.round(c.rel[p] * 100);
      return '<div class="pbar" style="--pc:' + colour[p] + '" title="relevance to ' + esc(partyName[p]) + ': ' + pc + '%"><b>' + esc(partyName[p]) + '</b><span class="t"><i style="width:' + pc + '%"></i></span><em>' + pc + '</em></div>';
    }).join("") + "</div>";
  }
  function cardHtml(c) {
    var inC = coll.indexOf(c.id) >= 0;
    var chips = c.tp.slice(0, 3).map(function (t) { return '<button class="chip" data-facet="topic" data-val="' + esc(t) + '">' + esc(t) + "</button>"; }).join("");
    var trl = trName[c.tr] ? trName[c.tr].label : c.tr;
    return '<article class="pc-card ev' + c.ev + " tier-" + c.tier + '" style="--cc:' + cardColour(c) + '" data-id="' + esc(c.id) + '">' +
      '<header><span class="cid">' + esc(c.id) + '</span><span class="badge ok" title="quotation re-found in the source by a script">verified</span>' +
      (c.hg !== "assertive" ? '<span class="badge hedge" title="the source itself hedges">' + esc(c.hg) + "</span>" : "") +
      (c.cx ? '<span class="badge flag">contested</span>' : "") + '<span class="badge tier">' + esc(c.tier) + " " + Math.round(c.imp) + "</span>" +
      '<span title="' + esc(EVL[c.ev]) + '">evidence ' + c.ev + "/5</span></header>" +
      "<h3>" + esc(c.text) + "</h3>" +
      "<blockquote" + (c.q ? "" : ' class="withheld"') + ">" + (c.q ? esc(c.q) : "Quotation withheld in this public build (copyright); find it at the work and line below.") + "<cite>" + esc(c.who) + " (" + esc(ATT[c.att]) + "), " + esc(c.w) + ", l. " + c.ln + "</cite></blockquote>" +
      '<div class="chips"><button class="chip tr" data-facet="trad" data-val="' + esc(c.tr) + '">' + esc(trl) + "</button>" + chips +
      '<span class="chip" title="claim type">' + esc(TYPES[c.typ] || c.typ) + "</span></div>" + pbars(c) +
      '<footer><button data-act="open" aria-label="Open evidence for ' + esc(c.id) + '">Evidence</button>' +
      '<button data-act="coll" aria-pressed="' + inC + '">' + (inC ? "Collected" : "+ Collect") + "</button>" +
      '<button data-act="cite">Cite</button><button data-act="copy">Copy quote</button>' +
      '<span class="sp">' + (c.oq ? c.oq + " open question" + (c.oq > 1 ? "s" : "") + " · " : "") + c.nl + " link" + (c.nl === 1 ? "" : "s") + "</span></footer></article>";
  }
  function facetGroup(key, title, items, open) {
    var sel = S.f[key];
    var html = items.map(function (it) {
      return '<label><input type="checkbox" data-facet="' + key + '" value="' + esc(it.id) + '"' + (sel.indexOf(it.id) >= 0 ? " checked" : "") + (it.n === 0 && sel.indexOf(it.id) < 0 ? " disabled" : "") + ">" +
        (it.colour ? '<span class="sw" style="background:' + it.colour + '"></span>' : "") + "<span>" + esc(it.label) + '</span><span class="n">' + it.n + "</span></label>";
    }).join("");
    return "<details" + (open ? " open" : "") + "><summary>" + esc(title) + (sel.length ? " (" + sel.length + ")" : "") + "</summary>" + html + "</details>";
  }
  function counts(key, toks) {
    var m = {};
    cards.forEach(function (c) { if (passes(c, key, toks)) { FACET[key](c).forEach(function (v) { m[v] = (m[v] || 0) + 1; }); } });
    return m;
  }
  function renderSide(toks) {
    var g = function (k) { return counts(k, toks); };
    var tc = g("topic"), pc = g("party"), rc = g("trad"), wc = g("who"), kc = g("work"), yc = g("typ"), ic = g("tier"), ec = g("ev"), hc = g("hg"), fc = g("flag");
    var top = facets.topics.map(function (t) { return { id: t.id, label: t.id, n: tc[t.id] || 0 }; }).sort(function (a, b) { return b.n - a.n; });
    var topShown = S.showAllTopics ? top : top.slice(0, 14);
    var h = "";
    h += facetGroup("trad", "Tradition", facets.traditions.map(function (t) { return { id: t.id, label: t.label, colour: t.colour, n: rc[t.id] || 0 }; }).filter(function (t) { return t.n || S.f.trad.indexOf(t.id) >= 0; }), true);
    h += facetGroup("party", "Bears on (relationship)", facets.parties.map(function (p) { return { id: p.id, label: p.name, colour: p.colour, n: pc[p.id] || 0 }; }).filter(function (p) { return p.n || S.f.party.indexOf(p.id) >= 0; }).sort(function (a, b) { return b.n - a.n; }), true);
    h += facetGroup("topic", "Topic", topShown, true) + (top.length > 14 ? '<button class="more" data-act="alltopics">' + (S.showAllTopics ? "fewer topics" : "all " + top.length + " topics") + "</button>" : "");
    h += facetGroup("tier", "Importance tier", TIERS.map(function (t) { return { id: t, label: t, n: ic[t] || 0 }; }), true);
    h += facetGroup("ev", "Evidence level", [5, 4, 3, 2, 1].map(function (e) { return { id: String(e), label: EVL[e], n: ec[e] || 0 }; }), false);
    h += facetGroup("flag", "Flags", Object.keys(FLAGS).map(function (f) { return { id: f, label: FLAGS[f], n: fc[f] || 0 }; }), false);
    h += facetGroup("who", "Claimant", Object.keys(wc).sort(function (a, b) { return wc[b] - wc[a]; }).map(function (w) { return { id: w, label: w, n: wc[w] }; }), false);
    h += facetGroup("work", "Work", Object.keys(kc).sort(function (a, b) { return kc[b] - kc[a]; }).map(function (w) { return { id: w, label: w, n: kc[w] }; }), false);
    h += facetGroup("typ", "Kind of claim", Object.keys(yc).map(function (t) { return { id: t, label: TYPES[t] || t, n: yc[t] }; }), false);
    h += facetGroup("hg", "Source's own stance", ["assertive", "hedged", "speculative"].map(function (t) { return { id: t, label: t, n: hc[t] || 0 }; }), false);
    return h;
  }
  function chipsRow() {
    var out = [];
    Object.keys(S.f).forEach(function (k) { S.f[k].forEach(function (v) { out.push('<button data-rm="' + k + "~" + esc(v) + '" aria-label="Remove filter ' + esc(v) + '">' + esc(k + ": " + (k === "party" ? partyName[v] || v : k === "trad" ? (trName[v] || {}).label || v : v)) + " ×</button>"); }); });
    if (S.q) { out.push('<button data-rm="q~">search: ' + esc(S.q) + " ×</button>"); }
    return out.join("");
  }
  var view = [];
  function render() {
    var toks = parseQuery(S.q);
    view = sorted(cards.filter(function (c) { return passes(c, null, toks); }));
    var shown = view.slice(0, S.limit);
    nodes.side.innerHTML = renderSide(toks);
    nodes.chips.innerHTML = chipsRow();
    nodes.count.textContent = view.length + " of " + cards.length + " claims" + (S.sort === "rel" && S.relParty ? ", sorted by relevance to " + (partyName[S.relParty] || S.relParty) : "");
    nodes.grid.className = "pc-grid" + (S.view === "list" ? " list" : "");
    nodes.grid.innerHTML = shown.map(cardHtml).join("") || '<p class="meta">No claim matches. Remove a filter or a search word.</p>';
    nodes.more.hidden = view.length <= S.limit;
    nodes.more.textContent = "Show more (" + (view.length - S.limit) + " left)";
    nodes.tray.hidden = !coll.length;
    nodes.tray.querySelector(".n").textContent = coll.length + " collected";
    writeHash();
  }

  /* ---------- drawer ---------- */
  var openId = null, tab = "ev";
  function loadDetail(c) {
    if (detailCache[c.p]) { return Promise.resolve(detailCache[c.p][c.id]); }
    return get(BASE + "detail-" + c.p + ".json").then(function (d) { detailCache[c.p] = d; return d[c.id]; });
  }
  function relBtn(id) { var c = byId[id]; return c ? '<button data-open="' + esc(id) + '">' + esc(c.who) + ": " + esc(c.text.slice(0, 90)) + "…</button>" : esc(id); }
  function panel(c, d) {
    if (tab === "ev") {
      return "<h4>Quotations, re-found in the source</h4>" + d.quotes.map(function (q) { return "<blockquote>" + (q.t ? esc(q.t) : "<em>Withheld in this public build (copyright). Verified verbatim by script at:</em>") + '<span class="loc">' + esc(q.w) + ", l. " + q.ln + (q.pg ? ", p. " + esc(q.pg) : "") + "</span></blockquote>"; }).join("") +
        (d.hedge_words ? "<h4>The source's own hedge</h4><p>" + esc(d.hedge_words) + "</p>" : "") + "<h4>Restatement (a model paraphrase)</h4><p>" + esc(c.text) + "</p>" +
        (d.bears.length ? "<h4>Bears on</h4>" + d.bears.map(function (b) { return "<p><b>" + esc(partyName[b.party] || b.party) + "</b> (" + esc(b.kind) + "): " + esc(b.note) + "</p>"; }).join("") : "");
    }
    if (tab === "wa") {
      return "<h4>How the source supports it</h4>" + (d.warrants.length ? d.warrants.map(function (w) { return "<p><b>" + esc(w.k.replace("_", " ")) + ".</b> " + esc(w.t) + (w.q ? "<blockquote>" + esc(w.q) + '<span class="loc">' + esc(w.w) + ", l. " + w.ln + "</span></blockquote>" : "") + "</p>"; }).join("") : "<p>The source states no warrant for this claim (score: bare assertion).</p>") +
        (d.assumptions.length ? "<h4>Assumes</h4><ul>" + d.assumptions.map(function (a) { return "<li>" + esc(a) + "</li>"; }).join("") + "</ul>" : "");
    }
    if (tab === "oq") {
      return "<h4>What remains open</h4>" + (d.open.length ? d.open.map(function (o) { return "<p><b>" + esc(o.k.replace("_", " ")) + ".</b> " + esc(o.t) + "</p>"; }).join("") : "<p>No open question recorded for this claim.</p>");
    }
    if (tab === "re") {
      var h = "<h4>Linked claims</h4>";
      if (!d.rel.length) { h += "<p>No cross-scholar link recorded yet (linking is a later stage: see TICKETS.md T-CLAIMS-04).</p>"; }
      d.rel.forEach(function (r) { h += '<div class="rel"><b>' + esc(r.dir === "out" ? r.r.replace("_", " ") : "is " + r.r.replace("_", " ") + " by") + "</b> " + relBtn(r.id) + (r.basis ? "<br><small>" + esc(r.basis) + "</small>" : "") + "</div>"; });
      var sib = cards.filter(function (x) { return x.id !== c.id && x.tp[0] === c.tp[0]; }).slice(0, 5);
      h += "<h4>Same topic (" + esc(c.tp[0]) + ")</h4>" + sib.map(function (x) { return '<div class="rel">' + relBtn(x.id) + "</div>"; }).join("");
      return h;
    }
    var sc = d.score, row = function (n, v, max, fmt) { return '<div class="comp"><span>' + n + '</span><span class="t"><i style="width:' + Math.min(100, 100 * v / max) + '%"></i></span><b>' + (fmt || v) + "</b></div>"; };
    return "<h4>Importance components (published weights: data/claims/scoring.json)</h4>" + row("centrality", sc.centrality, 5) + row("corroboration", sc.corroboration, 4) + row("contestation", sc.contestation, 1) + row("warrant strength", sc.warrant_strength, 1) +
      row("reach", sc.reach, 1) + row("frame shift (judged)", sc.frame_shift, 1, sc.frame_shift.toFixed ? sc.frame_shift.toFixed(2) : sc.frame_shift) + "<p><b>Importance " + sc.importance + "</b>, rank " + sc.rank + " of " + cards.length + ". Evidence level " + sc.evidence_level + ". A triage score for editorial attention, not a measure of truth.</p>";
  }
  function openCard(id, push) {
    var c = byId[id]; if (!c) { return; }
    openId = id; tab = push ? tab : "ev";
    nodes.drawer.hidden = false; nodes.drawer.setAttribute("aria-label", "Evidence for " + id);
    nodes.drawer.innerHTML = '<button class="x" aria-label="Close">×</button><div class="cid loc">' + esc(id) + "</div><h3 style='margin:.3em 0'>" + esc(c.text) + "</h3><p class='meta'>Loading evidence…</p>";
    nodes.drawer.querySelector(".x").focus();
    loadDetail(c).then(function (d) {
      if (openId !== id) { return; }
      var tabs = [["ev", "Evidence"], ["wa", "Warrants"], ["oq", "Open questions (" + d.open.length + ")"], ["re", "Relations (" + d.rel.length + ")"], ["sc", "Scores"]];
      nodes.drawer.innerHTML = '<button class="x" aria-label="Close">×</button><div class="cid loc">' + esc(id) + " · " + esc(c.who) + " · " + esc(ATT[c.att]) + '</div><h3 style="margin:.3em 0">' + esc(c.text) + "</h3>" +
        '<div class="pc-tabs" role="tablist">' + tabs.map(function (t) { return '<button role="tab" data-tab="' + t[0] + '" aria-selected="' + (tab === t[0]) + '">' + t[1] + "</button>"; }).join("") + '</div><div class="pc-panel">' + panel(c, d) + "</div>";
      nodes.drawer.querySelector(".x").focus();
    })["catch"](function (e) { nodes.drawer.innerHTML += "<p>Could not load the evidence: " + esc(e.message) + "</p>"; });
  }
  function closeDrawer() { nodes.drawer.hidden = true; openId = null; }

  /* ---------- collection, citation ---------- */
  function cite(c) { return c.who + ", " + c.w + ", l. " + c.ln + " (claim " + c.id + ")"; }
  function copy(t) {
    if (navigator.clipboard && navigator.clipboard.writeText) { return navigator.clipboard.writeText(t)["catch"](function () { fallback(t); }); }
    fallback(t);
  }
  function fallback(t) { var a = document.createElement("textarea"); a.value = t; document.body.appendChild(a); a.select(); try { document.execCommand("copy"); } catch (e) { /* ignore */ } a.remove(); }
  function exportMd() {
    var out = "# My collection\n\n";
    coll.forEach(function (id, i) { var c = byId[id]; if (c) { out += (i + 1) + ". " + c.text + "\n" + (c.q ? "   > " + c.q + "\n" : "") + "   " + cite(c) + "\n\n"; } });
    return out;
  }
  function download(name, text) {
    var a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([text], { type: "text/plain" })); a.download = name; document.body.appendChild(a); a.click(); a.remove();
  }

  /* ---------- events ---------- */
  function dispatch(id, push) { return (window.PCApp ? window.PCApp.openCard : openCard)(id, push); }
  function toggle(list, v) { var i = list.indexOf(v); if (i >= 0) { list.splice(i, 1); } else { list.push(v); } }
  function onClick(e) {
    var t = e.target.closest("button, [data-open]"); if (!t) { return; }
    var card = t.closest(".pc-card"), id = card ? card.getAttribute("data-id") : null, act = t.getAttribute("data-act");
    if (t.getAttribute("data-open")) { dispatch(t.getAttribute("data-open"), false); return; }
    if (t.getAttribute("data-facet")) { toggle(S.f[t.getAttribute("data-facet")], t.getAttribute("data-val")); S.limit = 60; render(); return; }
    if (t.getAttribute("data-rm")) { var p = t.getAttribute("data-rm").split("~"); if (p[0] === "q") { S.q = ""; nodes.q.value = ""; } else { S.f[p[0]] = S.f[p[0]].filter(function (x) { return x !== p.slice(1).join("~"); }); } render(); return; }
    if (t.getAttribute("data-tab")) { tab = t.getAttribute("data-tab"); dispatch(openId, true); return; }
    if (t.classList.contains("x")) { closeDrawer(); return; }
    if (act === "open" && id) { dispatch(id, false); }
    else if (act === "coll" && id) { toggle(coll, id); saveColl(); render(); }
    else if (act === "cite" && id) { copy(cite(byId[id])); flash(t, "Copied"); }
    else if (act === "copy" && id) { copy((byId[id].q ? byId[id].q + " " : "") + "(" + cite(byId[id]) + ")"); flash(t, "Copied"); }
    else if (act === "alltopics") { S.showAllTopics = !S.showAllTopics; render(); }
    else if (act === "more") { S.limit += 60; render(); }
    else if (act === "export-md") { download("pico-collection.md", exportMd()); }
    else if (act === "export-json") { download("pico-collection.json", JSON.stringify({ cards: coll, exported: new Date().toISOString() }, null, 1)); }
    else if (act === "clear") { coll = []; saveColl(); render(); }
    else if (act === "view") { S.view = S.view === "grid" ? "list" : "grid"; render(); }
    else if (act === "reset") { S.q = ""; nodes.q.value = ""; Object.keys(S.f).forEach(function (k) { S.f[k] = []; }); S.sort = "imp"; nodes.sort.value = "imp"; render(); }
  }
  function flash(btn, msg) { var o = btn.textContent; btn.textContent = msg; setTimeout(function () { btn.textContent = o; }, 900); }
  function onChange(e) {
    var t = e.target;
    if (t.getAttribute("data-facet") && t.type === "checkbox") { toggle(S.f[t.getAttribute("data-facet")], t.value); S.limit = 60; render(); }
  }

  /* ---------- build the page ---------- */
  function build() {
    var partyOpts = facets.parties.filter(function (p) { return p.n; }).map(function (p) { return '<option value="' + esc(p.id) + '">' + esc(p.name) + "</option>"; }).join("");
    app.innerHTML = '<aside class="pc-side" aria-label="Filters" id="pc-side"></aside><section><div class="pc-bar" role="search">' +
      '<label class="sr" for="pc-q">Search claims</label><input id="pc-q" type="search" placeholder="Search: Anaxagoras, claimant:black, topic:de-ente, party:ficino, thesis:4&gt;13 …">' +
      '<label class="sr" for="pc-in">Search in</label><select id="pc-in"><option value="both">in restatements and quotations</option><option value="restatement">in restatements only</option><option value="quotation">in the scholars\' words only</option></select>' +
      '<label class="sr" for="pc-sort">Sort by</label><select id="pc-sort"><option value="imp">Sort: importance</option><option value="rel">Sort: relevance to …</option><option value="ev">Sort: evidence level</option><option value="cx">Sort: contested first</option><option value="oq">Sort: most open questions</option><option value="links">Sort: most linked</option><option value="who">Sort: claimant A-Z</option></select>' +
      '<label class="sr" for="pc-rel">Relevance to</label><select id="pc-rel"><option value="">party…</option>' + partyOpts + "</select>" +
      '<label class="sr" for="pc-col">Colour by</label><select id="pc-col"><option value="trad">Colour: tradition</option><option value="party">Colour: main relationship</option><option value="tier">Colour: importance tier</option><option value="ev">Colour: evidence level</option></select>' +
      '<button data-act="view" title="Switch between grid and list">Grid / list</button><button data-act="reset">Reset</button></div>' +
      '<div class="pc-chips" id="pc-chips"></div><p class="pc-count" id="pc-count" aria-live="polite"></p><div id="pc-grid" class="pc-grid"></div>' +
      '<button class="pc-more" data-act="more" id="pc-more">Show more</button></section>' +
      '<div class="pc-tray" id="pc-tray" hidden><span class="n"></span><button data-act="export-md">Export Markdown</button><button data-act="export-json">Export JSON</button><button data-act="clear">Clear</button></div>' +
      '<div class="pc-drawer" id="pc-drawer" role="dialog" aria-label="Evidence" hidden></div>';
    nodes = { side: document.getElementById("pc-side"), q: document.getElementById("pc-q"), sort: document.getElementById("pc-sort"), col: document.getElementById("pc-col"), rel: document.getElementById("pc-rel"),
      inn: document.getElementById("pc-in"), chips: document.getElementById("pc-chips"), count: document.getElementById("pc-count"), grid: document.getElementById("pc-grid"),
      more: document.getElementById("pc-more"), tray: document.getElementById("pc-tray"), drawer: document.getElementById("pc-drawer") };
    nodes.q.value = S.q; nodes.sort.value = S.sort; nodes.col.value = S.colourBy; nodes.rel.value = S.relParty; nodes.inn.value = S.where;
    var timer;
    nodes.q.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(function () { S.q = nodes.q.value; S.limit = 60; render(); }, 180); });
    nodes.sort.addEventListener("change", function () { S.sort = nodes.sort.value; if (S.sort === "rel" && !S.relParty) { S.relParty = "ficino"; nodes.rel.value = "ficino"; } render(); });
    nodes.rel.addEventListener("change", function () { S.relParty = nodes.rel.value; if (S.relParty) { S.sort = "rel"; nodes.sort.value = "rel"; } render(); });
    nodes.col.addEventListener("change", function () { S.colourBy = nodes.col.value; render(); });
    nodes.inn.addEventListener("change", function () { S.where = nodes.inn.value; render(); });
    app.addEventListener("click", onClick); app.addEventListener("change", onChange);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !nodes.drawer.hidden) { closeDrawer(); } });
    render();
  }
  Promise.all([get(BASE + "cards.json"), get(BASE + "facets.json")]).then(function (r) {
    cards = r[0]; facets = r[1];
    cards.forEach(function (c) { byId[c.id] = c; });
    facets.parties.forEach(function (p) { colour[p.id] = p.colour; partyName[p.id] = p.name; });
    facets.traditions.forEach(function (t) { trName[t.id] = t; });
    readHash(); build();
    if (S.open && byId[S.open]) { openCard(S.open, false); }
    window.PCApp = { openCard: openCard, closeDrawer: closeDrawer, S: S, byId: byId, coll: coll,
                     render: render, saveColl: saveColl, nodes: nodes, esc: esc, get: get,
                     BASE: BASE, partyName: partyName, cardHtml: cardHtml, detailCache: detailCache,
                     loadDetail: loadDetail, colour: colour };
    document.dispatchEvent(new CustomEvent("pcapp:ready"));
    window.addEventListener("hashchange", function () { readHash(); if (S.open && byId[S.open]) { openCard(S.open, false); } nodes.q.value = S.q; nodes.sort.value = S.sort; nodes.col.value = S.colourBy; nodes.rel.value = S.relParty; nodes.inn.value = S.where; render(); });
  })["catch"](function (e) { app.innerHTML = "<p class='notice'>Could not load the card data: " + esc(e.message) + "</p>"; });
})();
