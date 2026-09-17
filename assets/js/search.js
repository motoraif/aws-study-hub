/* AWS Study Hub - Client-side search
   Loads data/search-index.json and provides an instant search overlay.
   No external dependencies. Triggered by the navbar search button or "/". */
(function () {
  var inDocs = location.pathname.split('/').filter(Boolean).indexOf('docs') !== -1;
  var rootPath = inDocs ? '../' : './';
  var INDEX_URL = rootPath + 'data/search-index.json';

  var docs = null;
  var loading = false;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Build the overlay DOM once
  var overlay = document.createElement('div');
  overlay.id = 'search-overlay';
  overlay.className = 'search-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Site search');
  overlay.hidden = true;
  overlay.innerHTML =
    '<div class="search-box">' +
      '<input type="search" id="search-input" placeholder="Search pages, topics, services..." aria-label="Search" autocomplete="off">' +
      '<div id="search-results" class="search-results"></div>' +
      '<div class="search-hint">Press <kbd>Esc</kbd> to close &middot; <kbd>&uarr;</kbd><kbd>&darr;</kbd> to navigate &middot; <kbd>Enter</kbd> to open</div>' +
    '</div>';
  document.addEventListener('DOMContentLoaded', function () { document.body.appendChild(overlay); });

  var input, resultsEl, activeIdx = -1, currentResults = [];

  function ensureRefs() {
    input = document.getElementById('search-input');
    resultsEl = document.getElementById('search-results');
  }

  function loadIndex() {
    if (docs || loading) return Promise.resolve();
    loading = true;
    return fetch(INDEX_URL, { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : { docs: [] }; })
      .then(function (data) { docs = (data && data.docs) || []; })
      .catch(function () { docs = []; })
      .then(function () { loading = false; });
  }

  function score(doc, terms) {
    var hay = (doc.title + ' ' + doc.desc + ' ' + (doc.headings || []).join(' ')).toLowerCase();
    var titleLc = doc.title.toLowerCase();
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (!t) continue;
      if (titleLc.indexOf(t) !== -1) s += 10;
      var idx = hay.indexOf(t);
      if (idx === -1) return 0; // every term must appear somewhere
      s += 3;
      (doc.headings || []).forEach(function (h) { if (h.toLowerCase().indexOf(t) !== -1) s += 2; });
    }
    return s;
  }

  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return (docs || []).map(function (d) { return { d: d, s: score(d, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 12)
      .map(function (x) { return x.d; });
  }

  function matchedHeadings(doc, q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    return (doc.headings || []).filter(function (h) {
      var hl = h.toLowerCase();
      return terms.some(function (t) { return hl.indexOf(t) !== -1; });
    }).slice(0, 2);
  }

  function renderResults(q) {
    currentResults = search(q);
    activeIdx = currentResults.length ? 0 : -1;
    if (!q) { resultsEl.innerHTML = '<div class="search-empty">Start typing to search across all pages.</div>'; return; }
    if (!currentResults.length) { resultsEl.innerHTML = '<div class="search-empty">No results for "' + esc(q) + '".</div>'; return; }
    resultsEl.innerHTML = currentResults.map(function (d, i) {
      var subs = matchedHeadings(d, q);
      return '<a class="search-result' + (i === 0 ? ' active' : '') + '" href="' + rootPath + esc(d.url) + '" data-i="' + i + '">' +
        '<div class="search-result-title">' + esc(d.title) + '</div>' +
        '<div class="search-result-desc">' + esc(d.desc) + '</div>' +
        (subs.length ? '<div class="search-result-sub">' + subs.map(esc).join(' &middot; ') + '</div>' : '') +
        '</a>';
    }).join('');
  }

  function setActive(i) {
    var items = resultsEl.querySelectorAll('.search-result');
    if (!items.length) return;
    activeIdx = (i + items.length) % items.length;
    items.forEach(function (el, idx) { el.classList.toggle('active', idx === activeIdx); });
    items[activeIdx].scrollIntoView({ block: 'nearest' });
  }

  function open() {
    ensureRefs();
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    loadIndex().then(function () { renderResults(input.value.trim()); });
    input.focus();
  }
  function close() {
    overlay.hidden = true;
    document.body.style.overflow = '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    ensureRefs();

    // Trigger: navbar button (added by components.js) or "/" key
    document.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('#search-toggle');
      if (t) { e.preventDefault(); open(); }
    });
    document.addEventListener('keydown', function (e) {
      if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && overlay.hidden) {
        var tag = (document.activeElement && document.activeElement.tagName) || '';
        if (tag === 'INPUT' || tag === 'TEXTAREA') return;
        e.preventDefault(); open();
      }
    });

    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    input.addEventListener('input', function () { renderResults(input.value.trim()); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { close(); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); setActive(activeIdx + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(activeIdx - 1); }
      else if (e.key === 'Enter') {
        var items = resultsEl.querySelectorAll('.search-result');
        if (items[activeIdx]) { window.location.href = items[activeIdx].getAttribute('href'); }
      }
    });
  });
})();
