/* AWS Study Hub - Quiz Engine
   Client-side quiz: loads data/quiz-questions.json, filters by cert,
   shuffles, times, scores, shows a domain breakdown, and stores
   best scores + history in localStorage. No backend required. */
(function () {
  var root = document.getElementById('quiz-app');
  if (!root) return;

  // Resolve data path relative to the page (quiz.html lives in /docs/)
  var DATA_URL = '../data/quiz-questions.json';
  var LS_KEY = 'quiz_history_v1';

  var state = {
    all: [],
    cert: 'ALL',
    pool: [],
    idx: 0,
    answers: [],       // selected option index per question (null if skipped)
    startTime: 0,
    timerId: null
  };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function loadHistory() {
    try { return JSON.parse(localStorage.getItem(LS_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function saveResult(cert, pct, correct, total) {
    var h = loadHistory();
    var rec = h[cert] || { attempts: 0, best: 0, last: 0, history: [] };
    rec.attempts += 1;
    rec.last = pct;
    rec.best = Math.max(rec.best, pct);
    rec.history.push({ d: new Date().toISOString().slice(0, 10), pct: pct, correct: correct, total: total });
    if (rec.history.length > 20) rec.history = rec.history.slice(-20);
    h[cert] = rec;
    try { localStorage.setItem(LS_KEY, JSON.stringify(h)); } catch (e) {}
  }

  // ---- Screens -------------------------------------------------------------

  function renderStart() {
    if (state.timerId) { clearInterval(state.timerId); state.timerId = null; }
    var certs = ['ALL'].concat(
      state.all.map(function (q) { return q.cert; })
        .filter(function (v, i, a) { return a.indexOf(v) === i; })
        .sort()
    );
    var hist = loadHistory();
    var opts = certs.map(function (c) {
      var count = c === 'ALL' ? state.all.length
        : state.all.filter(function (q) { return q.cert === c; }).length;
      var label = c === 'ALL' ? 'All certifications' : c;
      return '<option value="' + esc(c) + '">' + esc(label) + ' (' + count + ' questions)</option>';
    }).join('');

    var statsRows = Object.keys(hist).map(function (c) {
      var r = hist[c];
      return '<tr><td>' + esc(c) + '</td><td>' + r.attempts + '</td><td>' + r.best + '%</td><td>' + r.last + '%</td></tr>';
    }).join('');

    root.innerHTML =
      '<div class="card quiz-panel">' +
        '<h2 style="margin-top:0">Start a Quiz</h2>' +
        '<p style="color:var(--text-muted)">Pick a certification, choose how many questions, and test yourself. Your best scores are saved in your browser.</p>' +
        '<div class="quiz-controls">' +
          '<label>Certification<br><select id="quiz-cert">' + opts + '</select></label>' +
          '<label>Questions<br><select id="quiz-count">' +
            '<option value="5">5</option><option value="10" selected>10</option><option value="20">20</option><option value="0">All</option>' +
          '</select></label>' +
        '</div>' +
        '<button class="btn btn-primary" id="quiz-start">Start Quiz &rarr;</button>' +
      '</div>' +
      (statsRows ?
        '<div class="card quiz-panel" style="margin-top:1.5rem"><h3 style="margin-top:0">&#128202; Your Progress</h3>' +
        '<div class="table-wrap"><table><thead><tr><th>Cert</th><th>Attempts</th><th>Best</th><th>Last</th></tr></thead><tbody>' +
        statsRows + '</tbody></table></div>' +
        '<button class="btn btn-outline" id="quiz-reset" style="margin-top:1rem;font-size:0.8rem">Clear my quiz history</button></div>'
        : '');

    document.getElementById('quiz-start').addEventListener('click', function () {
      var cert = document.getElementById('quiz-cert').value;
      var count = parseInt(document.getElementById('quiz-count').value, 10);
      startQuiz(cert, count);
    });
    var reset = document.getElementById('quiz-reset');
    if (reset) reset.addEventListener('click', function () {
      if (confirm('Clear all saved quiz history?')) { localStorage.removeItem(LS_KEY); renderStart(); }
    });
  }

  function startQuiz(cert, count) {
    state.cert = cert;
    var filtered = cert === 'ALL' ? state.all : state.all.filter(function (q) { return q.cert === cert; });
    var pool = shuffle(filtered);
    if (count && count > 0) pool = pool.slice(0, count);
    state.pool = pool;
    state.idx = 0;
    state.answers = pool.map(function () { return null; });
    state.startTime = Date.now();
    renderQuestion();
  }

  function fmtTime(ms) {
    var s = Math.floor(ms / 1000);
    var m = Math.floor(s / 60);
    return m + ':' + ('0' + (s % 60)).slice(-2);
  }

  function renderQuestion() {
    var q = state.pool[state.idx];
    var n = state.pool.length;
    var picked = state.answers[state.idx];

    // Present options in a stable shuffled order per question instance
    if (!q._order) q._order = shuffle(q.options.map(function (_, i) { return i; }));

    var optsHtml = q._order.map(function (origIdx, displayI) {
      var letter = String.fromCharCode(65 + displayI);
      var sel = picked === origIdx ? ' selected' : '';
      return '<button class="quiz-option' + sel + '" data-opt="' + origIdx + '">' +
        '<span class="quiz-letter">' + letter + '</span>' + esc(q.options[origIdx]) + '</button>';
    }).join('');

    root.innerHTML =
      '<div class="card quiz-panel">' +
        '<div class="quiz-meta">' +
          '<span class="badge badge-blue">' + esc(q.cert) + '</span>' +
          '<span class="badge">' + esc(q.domain) + '</span>' +
          '<span class="quiz-progress-text">Question ' + (state.idx + 1) + ' of ' + n + '</span>' +
          '<span class="quiz-timer" id="quiz-timer">0:00</span>' +
        '</div>' +
        '<div class="progress-bar" style="margin:0.75rem 0"><div class="progress-fill" style="width:' + Math.round((state.idx) / n * 100) + '%"></div></div>' +
        '<p class="quiz-question">' + esc(q.question) + '</p>' +
        '<div class="quiz-options">' + optsHtml + '</div>' +
        '<div class="quiz-nav">' +
          '<button class="btn btn-outline" id="quiz-prev"' + (state.idx === 0 ? ' disabled' : '') + '>&larr; Previous</button>' +
          '<button class="btn btn-primary" id="quiz-next">' + (state.idx === n - 1 ? 'Finish' : 'Next &rarr;') + '</button>' +
        '</div>' +
      '</div>';

    // Timer
    if (state.timerId) clearInterval(state.timerId);
    var timerEl = document.getElementById('quiz-timer');
    state.timerId = setInterval(function () {
      if (timerEl) timerEl.textContent = fmtTime(Date.now() - state.startTime);
    }, 1000);
    if (timerEl) timerEl.textContent = fmtTime(Date.now() - state.startTime);

    root.querySelectorAll('.quiz-option').forEach(function (b) {
      b.addEventListener('click', function () {
        state.answers[state.idx] = parseInt(b.dataset.opt, 10);
        root.querySelectorAll('.quiz-option').forEach(function (x) { x.classList.remove('selected'); });
        b.classList.add('selected');
      });
    });
    document.getElementById('quiz-prev').addEventListener('click', function () {
      if (state.idx > 0) { state.idx--; renderQuestion(); }
    });
    document.getElementById('quiz-next').addEventListener('click', function () {
      if (state.idx < n - 1) { state.idx++; renderQuestion(); }
      else renderResults();
    });
  }

  function renderResults() {
    if (state.timerId) { clearInterval(state.timerId); state.timerId = null; }
    var pool = state.pool;
    var correct = 0;
    var byDomain = {};
    pool.forEach(function (q, i) {
      var ok = state.answers[i] === q.answer;
      if (ok) correct++;
      var d = q.domain || 'General';
      byDomain[d] = byDomain[d] || { c: 0, t: 0 };
      byDomain[d].t++; if (ok) byDomain[d].c++;
    });
    var total = pool.length;
    var pct = total ? Math.round(correct / total * 100) : 0;
    var elapsed = fmtTime(Date.now() - state.startTime);
    saveResult(state.cert, pct, correct, total);

    var pass = pct >= 70;
    var domainRows = Object.keys(byDomain).map(function (d) {
      var v = byDomain[d];
      var p = Math.round(v.c / v.t * 100);
      return '<tr><td>' + esc(d) + '</td><td>' + v.c + '/' + v.t + '</td><td>' + p + '%</td></tr>';
    }).join('');

    var review = pool.map(function (q, i) {
      var picked = state.answers[i];
      var ok = picked === q.answer;
      var pickedTxt = picked == null ? '<em>Skipped</em>' : esc(q.options[picked]);
      return '<div class="card quiz-review ' + (ok ? 'ok' : 'bad') + '" style="margin-bottom:0.75rem">' +
        '<p style="margin:0 0 0.4rem"><strong>Q' + (i + 1) + '.</strong> ' + esc(q.question) + '</p>' +
        '<p style="margin:0.2rem 0">' + (ok ? '&#9989;' : '&#10060;') + ' Your answer: ' + pickedTxt + '</p>' +
        (ok ? '' : '<p style="margin:0.2rem 0;color:var(--aws-orange)">Correct: ' + esc(q.options[q.answer]) + '</p>') +
        '<p style="margin:0.4rem 0 0;color:var(--text-muted);font-size:0.9rem">' + esc(q.explanation) + '</p>' +
      '</div>';
    }).join('');

    root.innerHTML =
      '<div class="card quiz-panel quiz-result ' + (pass ? 'pass' : 'fail') + '">' +
        '<div class="quiz-score">' + pct + '%</div>' +
        '<p class="quiz-score-sub">' + correct + ' of ' + total + ' correct &middot; ' + esc(state.cert) + ' &middot; ' + elapsed + '</p>' +
        '<p class="quiz-verdict">' + (pass ? '&#127881; Passing score! (70%+)' : 'Keep practicing - aim for 70%+') + '</p>' +
        '<div class="table-wrap" style="margin-top:1rem"><table><thead><tr><th>Domain</th><th>Score</th><th>%</th></tr></thead><tbody>' + domainRows + '</tbody></table></div>' +
        '<div class="quiz-nav" style="margin-top:1rem">' +
          '<button class="btn btn-primary" id="quiz-again">Try Again</button>' +
          '<button class="btn btn-outline" id="quiz-home">Back to Start</button>' +
        '</div>' +
      '</div>' +
      '<h3 style="margin:1.5rem 0 0.75rem">Review &amp; Explanations</h3>' + review;

    document.getElementById('quiz-again').addEventListener('click', function () {
      // clear per-instance option order so a fresh shuffle happens
      state.pool.forEach(function (q) { delete q._order; });
      startQuiz(state.cert, state.pool.length);
    });
    document.getElementById('quiz-home').addEventListener('click', renderStart);
  }

  // ---- Boot ----------------------------------------------------------------

  root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Loading question bank&hellip;</p></div>';
  fetch(DATA_URL, { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
    .then(function (data) {
      state.all = (data && data.questions) || [];
      if (!state.all.length) {
        root.innerHTML = '<div class="card quiz-panel"><p>No questions available yet.</p></div>';
        return;
      }
      renderStart();
    })
    .catch(function () {
      root.innerHTML = '<div class="card quiz-panel"><p style="color:var(--text-muted)">Could not load the question bank. Please refresh the page.</p></div>';
    });
})();
