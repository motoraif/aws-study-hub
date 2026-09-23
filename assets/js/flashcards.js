/* AWS Study Hub - Flashcards with SM-2 Spaced Repetition
   Builds a flashcard deck from data/quiz-questions.json (front = question,
   back = correct answer + explanation). Scheduling uses a simplified SM-2
   algorithm; per-card state (ease, interval, due date, repetitions) is saved
   in localStorage. No backend, all data stays in the browser. */
(function () {
  var root = document.getElementById('flashcards-app');
  if (!root) return;

  var DATA_URL = '../data/quiz-questions.json';
  var LS_KEY = 'flashcards_sm2_v1';

  var state = { all: [], cert: 'ALL', queue: [], idx: 0, flipped: false, reviewedThisSession: 0 };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function today() { return new Date().toISOString().slice(0, 10); }
  function addDays(dateStr, n) {
    var d = new Date(dateStr + 'T00:00:00');
    d.setDate(d.getDate() + n);
    return d.toISOString().slice(0, 10);
  }

  function loadSched() {
    try { return JSON.parse(localStorage.getItem(LS_KEY)) || {}; } catch (e) { return {}; }
  }
  function saveSched(s) {
    try { localStorage.setItem(LS_KEY, JSON.stringify(s)); } catch (e) {}
  }

  // Default SM-2 card state
  function defaultCard() { return { ease: 2.5, interval: 0, reps: 0, due: today() }; }

  /* SM-2 update.
     quality: 0 = Again (forgot), 3 = Hard, 4 = Good, 5 = Easy.
     Ratings below 3 reset the repetition count and reschedule soon. */
  function sm2(card, quality) {
    var c = { ease: card.ease, interval: card.interval, reps: card.reps, due: card.due };
    if (quality < 3) {
      c.reps = 0;
      c.interval = 0; // review again this session / next day
      c.due = quality === 0 ? today() : addDays(today(), 1);
    } else {
      c.reps += 1;
      if (c.reps === 1) c.interval = 1;
      else if (c.reps === 2) c.interval = 6;
      else c.interval = Math.round(c.interval * c.ease);
      c.due = addDays(today(), c.interval);
    }
    // Update ease factor (bounded at 1.3)
    c.ease = c.ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    if (c.ease < 1.3) c.ease = 1.3;
    return c;
  }

  function certList() {
    return ['ALL'].concat(
      state.all.map(function (q) { return q.cert; })
        .filter(function (v, i, a) { return a.indexOf(v) === i; }).sort()
    );
  }

  // Build the study queue: due cards first (oldest due date), then unseen cards.
  function buildQueue(cert) {
    var sched = loadSched();
    var pool = cert === 'ALL' ? state.all : state.all.filter(function (q) { return q.cert === cert; });
    var t = today();
    var due = [], fresh = [];
    pool.forEach(function (q) {
      var c = sched[q.id];
      if (!c) fresh.push(q);
      else if (c.due <= t) due.push(q);
    });
    due.sort(function (a, b) { return (sched[a.id].due < sched[b.id].due) ? -1 : 1; });
    // shuffle fresh cards
    for (var i = fresh.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var tmp = fresh[i]; fresh[i] = fresh[j]; fresh[j] = tmp; }
    return due.concat(fresh);
  }

  function counts(cert) {
    var sched = loadSched();
    var pool = cert === 'ALL' ? state.all : state.all.filter(function (q) { return q.cert === cert; });
    var t = today(), due = 0, fresh = 0, learned = 0;
    pool.forEach(function (q) {
      var c = sched[q.id];
      if (!c) { fresh++; return; }
      if (c.due <= t) due++;
      // "Learned" = graduated out of the initial learning steps (SM-2 reps >= 2,
      // i.e. interval has reached 6+ days). This is reachable within normal use,
      // unlike the old reps>=3 which only ever counted after several days.
      if (c.reps >= 2) learned++;
    });
    return { total: pool.length, due: due, fresh: fresh, learned: learned };
  }

  // ---- Screens -------------------------------------------------------------

  function renderStart() {
    var certs = certList();
    var opts = certs.map(function (c) {
      var n = c === 'ALL' ? state.all.length : state.all.filter(function (q) { return q.cert === c; }).length;
      return '<option value="' + esc(c) + '">' + (c === 'ALL' ? 'All certifications' : esc(c)) + ' (' + n + ' cards)</option>';
    }).join('');

    var cur = counts(state.cert);

    root.innerHTML =
      '<div class="card quiz-panel">' +
        '<h2 style="margin-top:0">&#128218; Flashcards</h2>' +
        '<p style="color:var(--text-muted)">Study with spaced repetition. Rate how well you recalled each card and the scheduler shows it again at the right time. Progress is saved privately in your browser.</p>' +
        '<div class="quiz-controls">' +
          '<label>Certification<br><select id="fc-cert">' + opts + '</select></label>' +
        '</div>' +
        '<div class="fc-stats" role="group" aria-label="Deck status">' +
          '<div class="fc-stat"><div class="fc-stat-num" id="fc-due">' + cur.due + '</div><div class="fc-stat-lbl">due now</div></div>' +
          '<div class="fc-stat"><div class="fc-stat-num" id="fc-new">' + cur.fresh + '</div><div class="fc-stat-lbl">new</div></div>' +
          '<div class="fc-stat"><div class="fc-stat-num" id="fc-learned">' + cur.learned + '</div><div class="fc-stat-lbl">learned</div></div>' +
        '</div>' +
        '<button class="btn btn-primary" id="fc-start">Start Studying &rarr;</button>' +
        ' <button class="btn btn-outline" id="fc-reset" style="font-size:0.8rem">Reset progress</button>' +
      '</div>';

    var certSel = document.getElementById('fc-cert');
    certSel.value = state.cert;
    certSel.addEventListener('change', function () {
      state.cert = certSel.value;
      var c = counts(state.cert);
      document.getElementById('fc-due').textContent = c.due;
      document.getElementById('fc-new').textContent = c.fresh;
      document.getElementById('fc-learned').textContent = c.learned;
    });
    document.getElementById('fc-start').addEventListener('click', function () {
      state.cert = certSel.value;
      state.queue = buildQueue(state.cert);
      state.idx = 0; state.flipped = false; state.reviewedThisSession = 0;
      if (!state.queue.length) { renderDone(true); return; }
      renderCard();
    });
    document.getElementById('fc-reset').addEventListener('click', function () {
      if (confirm('Reset all flashcard progress? This clears your spaced-repetition schedule.')) {
        localStorage.removeItem(LS_KEY); renderStart();
      }
    });
  }

  // Render the full card shell once per question. The flip is then a pure
  // CSS transition (toggling .flipped on the existing element) so the 3D
  // animation actually plays instead of the DOM being rebuilt each time.
  function renderCard() {
    if (state.idx >= state.queue.length) { renderDone(false); return; }
    var q = state.queue[state.idx];
    var correct = q.options[q.answer];
    var total = state.queue.length;
    var remaining = total - state.idx;
    var progressPct = Math.round((state.idx) / total * 100);

    root.innerHTML =
      '<div class="fc-topbar">' +
        '<div class="fc-meta">' +
          '<span class="badge badge-orange">' + esc(q.cert) + '</span>' +
          '<span class="badge">' + esc(q.domain) + '</span>' +
        '</div>' +
        '<span class="fc-remaining">' + remaining + ' / ' + total + '</span>' +
      '</div>' +
      '<div class="fc-progress"><div class="fc-progress-fill" style="width:' + progressPct + '%"></div></div>' +
      '<div class="flashcard' + (state.flipped ? ' flipped' : '') + '" id="fc-card" tabindex="0" role="button" ' +
        'aria-label="Flashcard. Press Space or Enter to flip.">' +
        '<div class="flashcard-inner">' +
          '<div class="flashcard-face flashcard-front">' +
            '<span class="fc-face-label">&#10067; Question</span>' +
            '<p class="fc-q">' + esc(q.question) + '</p>' +
            '<span class="fc-hint">Tap card or press <kbd>Space</kbd> to flip</span>' +
          '</div>' +
          '<div class="flashcard-face flashcard-back">' +
            '<span class="fc-face-label">&#9989; Answer</span>' +
            '<p class="fc-a">' + esc(correct) + '</p>' +
            '<p class="fc-exp">' + esc(q.explanation) + '</p>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="fc-controls" id="fc-controls"></div>';

    document.getElementById('fc-card').addEventListener('click', flip);
    renderControls();
  }

  // Swap only the controls area (Reveal button vs. rating buttons) so the
  // card element itself is never re-created and the flip keeps animating.
  function renderControls() {
    var el = document.getElementById('fc-controls');
    if (!el) return;
    if (state.flipped) {
      el.innerHTML =
        '<p class="fc-rate-prompt">How well did you recall it?</p>' +
        '<div class="fc-rate-btns">' +
          '<button class="btn fc-again" data-q="0"><span class="fc-rate-key">1</span>Again</button>' +
          '<button class="btn fc-hard" data-q="3"><span class="fc-rate-key">2</span>Hard</button>' +
          '<button class="btn fc-good" data-q="4"><span class="fc-rate-key">3</span>Good</button>' +
          '<button class="btn fc-easy" data-q="5"><span class="fc-rate-key">4</span>Easy</button>' +
        '</div>';
      el.querySelectorAll('.fc-rate-btns button').forEach(function (b) {
        b.addEventListener('click', function () { rate(parseInt(b.dataset.q, 10)); });
      });
    } else {
      el.innerHTML =
        '<div class="fc-flip-row">' +
          '<button class="btn btn-primary" id="fc-flip">&#128260; Reveal Answer</button>' +
          '<button class="btn btn-outline" id="fc-end">End session</button>' +
        '</div>';
      el.querySelector('#fc-flip').addEventListener('click', function (e) { e.stopPropagation(); flip(); });
      el.querySelector('#fc-end').addEventListener('click', function () { renderDone(false); });
    }
  }

  function flip() {
    state.flipped = !state.flipped;
    var card = document.getElementById('fc-card');
    if (card) card.classList.toggle('flipped', state.flipped);
    renderControls();
  }

  function rate(quality) {
    var q = state.queue[state.idx];
    var sched = loadSched();
    var card = sched[q.id] || defaultCard();
    sched[q.id] = sm2(card, quality);
    saveSched(sched);
    state.reviewedThisSession++;
    // If "Again", requeue the card near the end of this session
    if (quality < 3) state.queue.push(q);
    state.idx++;
    state.flipped = false;
    renderCard();
  }

  function renderDone(nothingDue) {
    var c = counts(state.cert);
    root.innerHTML =
      '<div class="card quiz-panel fc-done">' +
        '<div class="card-icon">' + (nothingDue ? '&#127881;' : '&#9989;') + '</div>' +
        '<h2 style="margin-top:0">' + (nothingDue ? 'All caught up!' : 'Session complete') + '</h2>' +
        '<p style="color:var(--text-muted)">' +
          (nothingDue
            ? 'No cards are due right now for ' + esc(state.cert === 'ALL' ? 'your selection' : state.cert) + '. Come back later, or pick another certification.'
            : 'You reviewed ' + state.reviewedThisSession + ' card' + (state.reviewedThisSession === 1 ? '' : 's') + '. ' + c.due + ' still due, ' + c.learned + ' learned.') +
        '</p>' +
        '<div class="quiz-nav">' +
          '<button class="btn btn-primary" id="fc-more">Study more</button>' +
          '<button class="btn btn-outline" id="fc-home">Back to start</button>' +
        '</div>' +
      '</div>';
    document.getElementById('fc-more').addEventListener('click', function () {
      state.queue = buildQueue(state.cert); state.idx = 0; state.flipped = false; state.reviewedThisSession = 0;
      if (!state.queue.length) { renderDone(true); return; }
      renderCard();
    });
    document.getElementById('fc-home').addEventListener('click', renderStart);
  }

  // Keyboard shortcuts: Space/Enter to flip; 1-4 to rate when flipped
  document.addEventListener('keydown', function (e) {
    if (!document.getElementById('fc-card')) return;
    var tag = (document.activeElement && document.activeElement.tagName) || '';
    if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
    if ((e.key === ' ' || e.key === 'Enter') && !state.flipped) { e.preventDefault(); flip(); }
    else if (state.flipped && ['1', '2', '3', '4'].indexOf(e.key) !== -1) {
      e.preventDefault();
      var map = { '1': 0, '2': 3, '3': 4, '4': 5 };
      rate(map[e.key]);
    }
  });

  // ---- Boot ----------------------------------------------------------------
  root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Loading flashcards&hellip;</p></div>';
  fetch(DATA_URL, { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (data) {
      state.all = (data && data.questions) || [];
      if (!state.all.length) { root.innerHTML = '<div class="card quiz-panel"><p>No cards available yet.</p></div>'; return; }
      var params = new URLSearchParams(location.search);
      var wanted = (params.get('cert') || '').toUpperCase();
      var avail = state.all.map(function (q) { return q.cert.toUpperCase(); });
      if (wanted && avail.indexOf(wanted) !== -1) {
        state.cert = state.all.filter(function (q) { return q.cert.toUpperCase() === wanted; })[0].cert;
      }
      renderStart();
    })
    .catch(function () {
      root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Could not load flashcards. Please refresh the page.</p></div>';
    });
})();
