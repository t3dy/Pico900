/* relations.js — T-SITE-03: trail, backlinks, compare, matrix view. Loads after cards.js. */
(function () {
  "use strict";
  var app, P;
  var trail = [];
  var compareIds = [];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* ---------- trail ---------- */
  function pushTrail(id) {
    if (trail[trail.length - 1] === id) { return; }
    trail.push(id);
    if (trail.length > 12) { trail.shift(); }
  }

  function trailHtml() {
    if (trail.length < 2) { return ""; }
    var items = trail.slice(-5);
    return '<nav class="pc-trail" aria-label="Trail">' +
      items.map(function (id, i) {
        var c = P.byId[id];
        var label = c ? esc(id) + " <small>" + esc(c.text.slice(0, 40)) + "…</small>" : esc(id);
        if (i === items.length - 1) { return "<span>" + label + "</span>"; }
        return '<button data-trail="' + esc(id) + '">' + label + "</button> ›";
      }).join(" ") + "</nav>";
  }

  /* ---------- mini-card for drawer ---------- */
  function miniCard(id, relLabel) {
    var c = P.byId[id];
    if (!c) { return '<div class="pc-mini">' + esc(id) + "</div>"; }
    return '<div class="pc-mini" style="--cc:' + (P.colour[c.tr] || "#b0a99e") + '">' +
      '<b data-open-trail="' + esc(id) + '">' + esc(relLabel) + "</b>" +
      '<button data-open-trail="' + esc(id) + '">' + esc(id) + " — " + esc(c.text.slice(0, 80)) + (c.text.length > 80 ? "…" : "") + "</button>" +
      (c.q ? "<blockquote>" + esc(c.q.split(" ").slice(0, 20).join(" ") + (c.q.split(" ").length > 20 ? " …" : "")) + "<cite>" + esc(c.w) + " l." + c.ln + "</cite></blockquote>" : "") +
      "</div>";
  }

  /* ---------- enhanced Relations tab ---------- */
  function patchRelTab(d, c) {
    var drawer = P.nodes.drawer;
    var panel = drawer.querySelector(".pc-panel");
    if (!panel) { return; }
    var activeTab = drawer.querySelector("[role=tab][aria-selected=true]");
    if (!activeTab || activeTab.getAttribute("data-tab") !== "re") { return; }
    var h = "<h4>Linked claims</h4>";
    if (!d.rel.length) {
      h += "<p>No cross-scholar link recorded yet.</p>";
    } else {
      d.rel.forEach(function (r) {
        var label = r.dir === "out" ? r.r.replace(/_/g, " ") : "is " + r.r.replace(/_/g, " ") + " by";
        h += miniCard(r.id, label);
        if (r.basis) { h += "<p class='meta' style='margin-left:1em'>" + esc(r.basis) + "</p>"; }
      });
    }
    var sib = Object.values(P.byId).filter(function (x) { return x.id !== c.id && x.tp[0] === c.tp[0]; }).slice(0, 4);
    if (sib.length) { h += "<h4>Same topic (" + esc(c.tp[0]) + ")</h4>" + sib.map(function (x) { return miniCard(x.id, "same topic"); }).join(""); }
    panel.innerHTML = h;
  }

  /* ---------- compare ---------- */
  var compareEl = null;
  function addCompareButtons() {
    document.querySelectorAll(".pc-card").forEach(function (el) {
      if (el.querySelector("[data-act=cmp]")) { return; }
      var footer = el.querySelector("footer");
      if (!footer) { return; }
      var id = el.getAttribute("data-id");
      var btn = document.createElement("button");
      btn.setAttribute("data-act", "cmp");
      btn.setAttribute("data-id", id);
      btn.setAttribute("aria-pressed", compareIds.indexOf(id) >= 0 ? "true" : "false");
      btn.textContent = compareIds.indexOf(id) >= 0 ? "Comparing" : "Compare";
      footer.appendChild(btn);
    });
  }

  function renderCompare() {
    if (!compareEl) {
      compareEl = document.createElement("div");
      compareEl.id = "pc-compare";
      compareEl.setAttribute("role", "dialog");
      compareEl.setAttribute("aria-label", "Compare two cards");
      document.getElementById("app").appendChild(compareEl);
    }
    if (compareIds.length < 2) {
      compareEl.hidden = true;
      compareEl.innerHTML = "";
      return;
    }
    compareEl.hidden = false;
    compareEl.innerHTML = '<button class="x" id="pc-cmp-close" aria-label="Close compare">×</button>' +
      '<div class="pc-compare-body">' +
      compareIds.map(function (id) { return P.cardHtml(P.byId[id]); }).join('<div class="pc-compare-sep" aria-hidden="true">vs</div>') +
      "</div>";
    document.getElementById("pc-cmp-close").addEventListener("click", function () {
      compareIds = []; renderCompare(); addCompareButtons();
    });
  }

  function toggleCompare(id) {
    var i = compareIds.indexOf(id);
    if (i >= 0) { compareIds.splice(i, 1); }
    else {
      if (compareIds.length >= 2) { compareIds.shift(); }
      compareIds.push(id);
    }
    renderCompare();
    addCompareButtons();
  }

  /* ---------- matrix view ---------- */
  var matrixEl = null, tprData = null;

  function buildMatrix() {
    if (!matrixEl) {
      matrixEl = document.createElement("div");
      matrixEl.id = "pc-matrix";
      document.getElementById("app").appendChild(matrixEl);
    }
    matrixEl.hidden = false;
    matrixEl.innerHTML = "<p class='meta'>Loading relevance data…</p>";
    if (tprData) { renderMatrix(); return; }
    fetch(P.BASE + "thesis_person_relevance.json")
      .then(function (r) { return r.ok ? r.json() : null; })["catch"](function () { return null; })
      .then(function (d) {
        if (!d) { matrixEl.innerHTML = "<p class='meta'>Matrix data not available at this path.</p>"; return; }
        tprData = d; renderMatrix();
      });
  }

  function renderMatrix() {
    var theses = Object.keys(tprData).slice(0, 80);
    var persons = {};
    theses.forEach(function (tid) {
      (tprData[tid].persons || []).forEach(function (p) { persons[p.person_id] = p.person_id; });
    });
    var cols = Object.keys(persons);
    if (!cols.length) { matrixEl.innerHTML = "<p>No person relevance data.</p>"; return; }
    var head = "<tr><th>Thesis</th>" + cols.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") + "</tr>";
    var rows = theses.map(function (tid) {
      var pm = {};
      (tprData[tid].persons || []).forEach(function (p) { pm[p.person_id] = p.relevance_score; });
      var cells = cols.map(function (c) {
        var v = pm[c] || 0, pc = Math.min(100, Math.round(v * 100));
        var bg = pc > 0 ? "rgba(139,69,19," + (0.1 + 0.7 * pc / 100).toFixed(2) + ")" : "transparent";
        var title = pc > 0 ? tid + " × " + c + ": " + pc + "%" : "";
        return '<td style="background:' + bg + '" title="' + esc(title) + '">' + (pc > 0 ? pc : "") + "</td>";
      }).join("");
      var base = P.BASE.replace(/\/cards\/data\/$/, "/conclusions/");
      return "<tr><td><a href='" + esc(base + encodeURIComponent(tid) + "/") + "'>" + esc(tid) + "</a></td>" + cells + "</tr>";
    }).join("");
    matrixEl.innerHTML = '<button class="x" id="pc-mat-close" aria-label="Close matrix">×</button>' +
      "<h3>Thesis × Person relevance (first 80 theses with data)</h3>" +
      '<div class="pc-matrix-scroll"><table class="pc-matrix-tbl"><thead>' + head + "</thead><tbody>" + rows + "</tbody></table></div>" +
      "<p class='meta'>Shading: 0–100% relevance based on scholar mentions and verified claims. Click a thesis ID to open its detail page.</p>";
    document.getElementById("pc-mat-close").addEventListener("click", function () { matrixEl.hidden = true; });
  }

  /* ---------- init ---------- */
  function init() {
    P = window.PCApp;
    app = document.getElementById("app");

    var origOpen = P.openCard;
    P.openCard = function (id, push) {
      pushTrail(id);
      origOpen(id, push);
      setTimeout(function () {
        var drawer = P.nodes.drawer;
        if (!drawer || drawer.hidden) { return; }
        var h = trailHtml();
        var existing = drawer.querySelector(".pc-trail");
        if (existing) { existing.outerHTML = h || ""; }
        else if (h) { drawer.insertAdjacentHTML("afterbegin", h); }
        addCompareButtons();
        if (P.detailCache) {
          var c = P.byId[id];
          if (c && P.detailCache[c.p] && P.detailCache[c.p][id]) {
            patchRelTab(P.detailCache[c.p][id], c);
          } else if (c) {
            var orig2 = P.loadDetail;
            P.loadDetail(c).then(function (d) { if (d) { patchRelTab(d, c); } });
          }
        }
      }, 50);
    };

    var origRender = P.render;
    P.render = function () { origRender(); setTimeout(addCompareButtons, 0); };

    var toolbar = app.querySelector(".pc-bar");
    if (toolbar) {
      var matBtn = document.createElement("button");
      matBtn.setAttribute("data-act", "matrix");
      matBtn.title = "Thesis × Person relevance matrix";
      matBtn.textContent = "Matrix";
      toolbar.appendChild(matBtn);
      matBtn.addEventListener("click", function () {
        if (matrixEl && !matrixEl.hidden) { matrixEl.hidden = true; } else { buildMatrix(); }
      });
    }

    app.addEventListener("click", function (e) {
      var t = e.target.closest("[data-act=cmp], [data-trail], [data-open-trail]");
      if (!t) { return; }
      if (t.getAttribute("data-act") === "cmp") { toggleCompare(t.getAttribute("data-id")); return; }
      var id = t.getAttribute("data-trail") || t.getAttribute("data-open-trail");
      if (id) { P.openCard(id, false); }
    });
  }

  document.addEventListener("pcapp:ready", function () {
    setTimeout(init, 0);
  });
})();
