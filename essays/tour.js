/* Tour behaviour: highlight the stop being read, show "Stop n of N", remember the reader's place. No dependencies. */
(function () {
  "use strict";
  var article = document.querySelector("article[data-slug]");
  if (!article) { return; }
  var key = "pico900.tour." + article.getAttribute("data-slug");
  var stops = [].slice.call(document.querySelectorAll("section.stop"));
  var links = {};
  [].forEach.call(document.querySelectorAll(".rail a[data-stop]"), function (a) { links[a.getAttribute("data-stop")] = a; });
  var progress = document.getElementById("progress");

  function mark(id) {
    Object.keys(links).forEach(function (k) { links[k].classList.toggle("active", k === id); });
    var n = stops.findIndex(function (s) { return s.id === id; }) + 1;
    if (progress && n) { progress.textContent = "Stop " + n + " of " + stops.length; }
    try { localStorage.setItem(key, id); } catch (e) { /* storage may be blocked */ }
  }
  // Which stop is being read: the last one whose top has passed 30% of the viewport height. A scroll listener (not
  // IntersectionObserver) so it is deterministic and testable; passive, so it never blocks scrolling.
  var current = null;
  function update() {
    var line = window.innerHeight * 0.3, id = stops.length ? stops[0].id : null;
    for (var i = 0; i < stops.length; i++) {
      if (stops[i].getBoundingClientRect().top <= line) { id = stops[i].id; }
    }
    if (id && id !== current) { current = id; mark(id); }
  }
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  var saved = null;
  try { saved = localStorage.getItem(key); } catch (e) { saved = null; }
  if (progress && saved && !location.hash) {
    var a = document.createElement("a");
    a.href = "#" + saved; a.textContent = "Resume at " + (links[saved] ? links[saved].textContent.split(" ")[0] + " " + links[saved].textContent.split(" ")[1] : "your last stop");
    progress.parentNode.insertBefore(a, progress.nextSibling);
  }
  update();
})();
