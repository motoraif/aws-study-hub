/* AWS Study Hub - Flashcards with SM-2 spaced repetition
   Loads data/flashcards.json, filters by cert, schedules reviews with a
   simplified SM-2 algorithm, and persists per-card scheduling in
   localStorage. No backend required. */
(function () {
  var root = document.getElementById('flash-app');
  if (!root) return;

  var DATA_URL = '../data/flashcards.json';
  var LS_KEY = 'flash_sm2_v1';

  var state = { all: [], cert: 'ALL', queue: [], idx: 0, showBack: false, sessionStats: { reviewed: 0, again: 0 } };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  function loadSched() { try { return JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch (e) { return {}; } }
  function saveSched(s) { try { localStorage.setItem(LS_KEY, JSON.stringify(s)); } catch (e) {} }

  // Simplified SM-2. quality: 0 = Again, 3 = Hard, 4 = Good, 5 = Easy
  function schedule(card, quality) {
    var sched = loadSched();
    var s = sched[card.id] || { ef: 2.5, reps: 0, interval: 0, due: 0 };
    if (quality < 3) {
      s.reps = 0; s.interval = 1; // relearn tomorrow
    } else {
      s.reps += 1;
      if (s.reps === 1) s.interval = 1;
      else if (s.reps === 2) s.interval = 6;
      else s.interval = Math.round(s.interval * s.ef);
      s.ef = Math.max(1.3, s.ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)));
    }
    s.due = Date.now() + s.interval * 86400000; // days -> ms
    s.last = Date.now();
    sched[card.id] = s;
    saveSched(sched);
  }

  function isDue(card) {
    var sched = loadSched();
    var s = sched[card.id];
    return !s || !s.due || s.due <= Date.now();
  }

  function certList() {
    return ['ALL'].concat(
      state.all.map(function (c) { return c.cert; })
        .filter(function (v, i, a) { return a.indexOf(v) === i; })
        .sort(function (a, b) { return a === 'GENERAL' ? -1 : b === 'GENERAL' ? 1 : a.localeCompare(b); })
    );
  }

  function renderStart() {
    var sched = loadSched();
    var opts = certList().map(function (c) {
      var pool = c === 'ALL' ? state.all : state.all.filter(function (x) { return x.cert === c; });
      var due = pool.filter(isDue).length;
      var label = c === 'ALL' ? 'All topics' : (c === 'GENERAL' ? 'General (ports, CIDR, IAM...)' : c);
      return '<option value="' + esc(c) + '">' + esc(label) + ' - ' + pool.length + ' cards, ' + due + ' due</option>';
    }).join('');

    var learned = Object.keys(sched).filter(function (id) { return (sched[id].reps || 0) >= 3; }).length;

    root.innerHTML =
      '<div class="card quiz-panel">' +
        '<h2 style="margin-top:0">Flashcards</h2>' +
        '<p style="color:var(--text-muted)">Spaced-repetition flashcards. Rate how well you knew each card and the app schedules its next review. Progress is saved in your browser.</p>' +
        '<div class="quiz-controls">' +
          '<label>Deck<br><select id="flash-cert">' + opts + '</select></label>' +
          '<label>Mode<br><select id="flash-mode">' +
            '<option value="due">Due for review</option>' +
            '<option value="all">All cards (shuffled)</option>' +
          '</select></label>' +
        '</div>' +
        '<button class="btn btn-primary" id="flash-start">Start Reviewing &rarr;</button>' +
        '<p style="color:var(--text-muted);font-size:0.85rem;margin-top:1rem">Cards learned (3+ correct reps): <strong>' + learned + '</strong>' +
        (learned ? ' &middot; <button class="linklike" id="flash-reset">reset progress</button>' : '') + '</p>' +
      '</div>';

    document.getElementById('flash-start').addEventListener('click', function () {
      startSession(document.getElementById('flash-cert').value, document.getElementById('flash-mode').value);
    });
    var reset = document.getElementById('flash-reset');
    if (reset) reset.addEventListener('click', function () {
      if (confirm('Reset all flashcard scheduling?')) { localStorage.removeItem(LS_KEY); renderStart(); }
    });
  }

  function startSession(cert, mode) {
    state.cert = cert;
    var pool = cert === 'ALL' ? state.all : state.all.filter(function (c) { return c.cert === cert; });
    if (mode === 'due') pool = pool.filter(isDue);
    if (!pool.length) { pool = cert === 'ALL' ? state.all : state.all.filter(function (c) { return c.cert === cert; }); }
    state.queue = shuffle(pool);
    state.idx = 0; state.showBack = false;
    state.sessionStats = { reviewed: 0, again: 0 };
    renderCard();
  }

  function renderCard() {
    if (state.idx >= state.queue.length) return renderDone();
    var c = state.queue[state.idx];
    var n = state.queue.length;

    root.innerHTML =
      '<div class="card quiz-panel">' +
        '<div class="quiz-meta">' +
          '<span class="badge badge-blue">' + esc(c.cert === 'GENERAL' ? 'General' : c.cert) + '</span>' +
          '<span class="badge">' + esc(c.topic) + '</span>' +
          '<span class="quiz-progress-text">Card ' + (state.idx + 1) + ' of ' + n + '</span>' +
        '</div>' +
        '<div class="progress-bar" style="margin:0.75rem 0"><div class="progress-fill" style="width:' + Math.round(state.idx / n * 100) + '%"></div></div>' +
        '<div class="flashcard" id="flashcard" tabindex="0" role="button" aria-label="Flashcard, click to reveal answer">' +
          '<div class="flashcard-label">' + (state.showBack ? 'Answer' : 'Question') + '</div>' +
          '<div class="flashcard-text">' + esc(state.showBack ? c.back : c.front) + '</div>' +
          (state.showBack ? '' : '<div class="flashcard-hint">Click or press Space to flip</div>') +
        '</div>' +
        (state.showBack ?
          '<div class="flash-rate">' +
            '<button class="btn flash-again" data-q="0">Again</button>' +
            '<button class="btn flash-hard" data-q="3">Hard</button>' +
            '<button class="btn flash-good" data-q="4">Good</button>' +
            '<button class="btn flash-easy" data-q="5">Easy</button>' +
          '</div>'
          : '<div class="quiz-nav" style="margin-top:1.25rem"><span></span><button class="btn btn-primary" id="flash-flip">Show Answer</button></div>') +
      '</div>';

    var fc = document.getElementById('flashcard');
    function flip() { if (!state.showBack) { state.showBack = true; renderCard(); } }
    fc.addEventListener('click', flip);
    fc.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); } });
    var flipBtn = document.getElementById('flash-flip');
    if (flipBtn) flipBtn.addEventListener('click', flip);

    root.querySelectorAll('.flash-rate .btn').forEach(function (b) {
      b.addEventListener('click', function () {
        var q = parseInt(b.dataset.q, 10);
        schedule(c, q);
        state.sessionStats.reviewed++;
        if (q < 3) state.sessionStats.again++;
        state.idx++; state.showBack = false;
        renderCard();
      });
    });
  }

  function renderDone() {
    var s = state.sessionStats;
    root.innerHTML =
      '<div class="card quiz-panel quiz-result pass">' +
        '<div style="font-size:2.5rem">&#127881;</div>' +
        '<h2 style="margin:0.5rem 0 0">Session complete!</h2>' +
        '<p class="quiz-score-sub">Reviewed ' + s.reviewed + ' cards' + (s.again ? ' &middot; ' + s.again + ' marked "Again" (will repeat sooner)' : '') + '</p>' +
        '<div class="quiz-nav" style="margin-top:1rem">' +
          '<button class="btn btn-primary" id="flash-more">Review More</button>' +
          '<button class="btn btn-outline" id="flash-home">Back to Start</button>' +
        '</div>' +
      '</div>';
    document.getElementById('flash-more').addEventListener('click', function () { startSession(state.cert, 'due'); });
    document.getElementById('flash-home').addEventListener('click', renderStart);
  }

  root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Loading flashcards&hellip;</p></div>';
  fetch(DATA_URL, { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (data) {
      state.all = (data && data.cards) || [];
      if (!state.all.length) { root.innerHTML = '<div class="card quiz-panel"><p>No flashcards available yet.</p></div>'; return; }
      renderStart();
    })
    .catch(function () {
      root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Could not load flashcards. Please refresh the page.</p></div>';
    });
})();
