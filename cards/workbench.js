/* workbench.js — T-SITE-07: notes, lenses, enhanced collection tray. Loads after cards.js. */
(function () {
  "use strict";
  var P;
  var NOTES_KEY = "pico900.notes.v1";
  var LENSES_KEY = "pico900.lenses.v1";

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* ---------- notes ---------- */
  function loadNotes() { try { return JSON.parse(localStorage.getItem(NOTES_KEY) || "{}"); } catch (e) { return {}; } }
  function saveNote(id, text) { var n = loadNotes(); if (text.trim()) { n[id] = text; } else { delete n[id]; } try { localStorage.setItem(NOTES_KEY, JSON.stringify(n)); } catch (e) {} }

  function injectNoteArea(id) {
    var drawer = P.nodes.drawer;
    if (!drawer || drawer.hidden) { return; }
    if (drawer.querySelector(".wb-note")) { return; }
    var notes = loadNotes();
    var area = document.createElement("div");
    area.className = "wb-note";
    area.innerHTML = "<h4>Note</h4>" +
      '<textarea placeholder="Your notes on this claim…" aria-label="Note for ' + esc(id) + '">' +
      esc(notes[id] || "") + "</textarea>";
    var ta = area.querySelector("textarea");
    var timer;
    ta.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { saveNote(id, ta.value); }, 400);
    });
    drawer.appendChild(area);
  }

  /* ---------- lenses ---------- */
  function loadLenses() { try { return JSON.parse(localStorage.getItem(LENSES_KEY) || "{}"); } catch (e) { return {}; } }
  function saveLens(name) {
    var lenses = loadLenses();
    lenses[name] = { q: P.S.q, sort: P.S.sort, colourBy: P.S.colourBy, relParty: P.S.relParty, f: JSON.parse(JSON.stringify(P.S.f)) };
    try { localStorage.setItem(LENSES_KEY, JSON.stringify(lenses)); } catch (e) {}
  }
  function applyLens(name) {
    var lenses = loadLenses();
    var l = lenses[name]; if (!l) { return; }
    P.S.q = l.q || ""; P.S.sort = l.sort || "imp"; P.S.colourBy = l.colourBy || "trad"; P.S.relParty = l.relParty || "";
    Object.keys(P.S.f).forEach(function (k) { P.S.f[k] = (l.f && l.f[k]) ? l.f[k] : []; });
    P.nodes.q.value = P.S.q; P.nodes.sort.value = P.S.sort; P.nodes.col.value = P.S.colourBy; P.nodes.rel.value = P.S.relParty;
    P.render();
  }
  function deleteLens(name) { var lenses = loadLenses(); delete lenses[name]; try { localStorage.setItem(LENSES_KEY, JSON.stringify(lenses)); } catch (e) {} }

  function renderLensPanel() {
    var panel = document.getElementById("wb-lenses"); if (!panel) { return; }
    var lenses = loadLenses();
    var names = Object.keys(lenses);
    if (!names.length) { panel.innerHTML = "<p class='meta'>No saved lenses.</p>"; return; }
    panel.innerHTML = names.map(function (n) {
      return '<div class="wb-lens"><button data-apply-lens="' + esc(n) + '">' + esc(n) + '</button>' +
        '<button data-del-lens="' + esc(n) + '" aria-label="Delete lens ' + esc(n) + '">×</button></div>';
    }).join("");
  }

  /* ---------- enhanced tray ---------- */
  function buildCollPanel() {
    var tray = P.nodes.tray; if (!tray) { return; }
    var existingList = tray.querySelector(".wb-coll-list");
    if (!existingList) {
      existingList = document.createElement("div");
      existingList.className = "wb-coll-list";
      tray.appendChild(existingList);
    }
    existingList.innerHTML = P.coll.map(function (id) {
      var c = P.byId[id];
      if (!c) { return '<div class="wb-coll-item">' + esc(id) + "</div>"; }
      var notes = loadNotes();
      return '<div class="wb-coll-item"><button data-open-coll="' + esc(id) + '">' + esc(id) + " — " +
        esc(c.text.slice(0, 60)) + (c.text.length > 60 ? "…" : "") + "</button>" +
        (notes[id] ? '<p class="meta" style="margin:.2em 0 0 .5em">' + esc(notes[id].slice(0, 60)) + "…</p>" : "") + "</div>";
    }).join("") || "<p class='meta'>No cards collected yet.</p>";
  }

  /* ---------- toolbar injection ---------- */
  function injectToolbar() {
    var toolbar = document.querySelector(".pc-bar"); if (!toolbar) { return; }

    var saveBtn = document.createElement("button");
    saveBtn.setAttribute("data-act", "save-lens");
    saveBtn.title = "Save current filters as a named lens";
    saveBtn.textContent = "Save lens";
    toolbar.appendChild(saveBtn);

    var side = P.nodes.side;
    var lensSection = document.createElement("details");
    lensSection.innerHTML = '<summary>Lenses <span class="n" id="wb-lens-count"></span></summary><div id="wb-lenses"></div>';
    if (side) { side.insertAdjacentElement("afterbegin", lensSection); }
    renderLensPanel();
    document.getElementById("wb-lens-count").textContent = Object.keys(loadLenses()).length || "";
  }

  /* ---------- events ---------- */
  function init() {
    P = window.PCApp;
    injectToolbar();

    var origOpen = P.openCard;
    P.openCard = function (id, push) {
      origOpen(id, push);
      setTimeout(function () { injectNoteArea(id); buildCollPanel(); }, 120);
    };

    var origRender = P.render;
    P.render = function () { origRender(); setTimeout(buildCollPanel, 0); };

    document.getElementById("app").addEventListener("click", function (e) {
      var t = e.target.closest("[data-act=save-lens], [data-apply-lens], [data-del-lens], [data-open-coll]");
      if (!t) { return; }
      if (t.getAttribute("data-act") === "save-lens") {
        var name = prompt("Name this lens:");
        if (name && name.trim()) { saveLens(name.trim()); renderLensPanel(); document.getElementById("wb-lens-count").textContent = Object.keys(loadLenses()).length; }
        return;
      }
      var al = t.getAttribute("data-apply-lens"); if (al) { applyLens(al); return; }
      var dl = t.getAttribute("data-del-lens"); if (dl) { deleteLens(dl); renderLensPanel(); document.getElementById("wb-lens-count").textContent = Object.keys(loadLenses()).length || ""; return; }
      var oc = t.getAttribute("data-open-coll"); if (oc) { P.openCard(oc, false); }
    });
  }

  document.addEventListener("pcapp:ready", function () {
    setTimeout(init, 0);
  });
})();
