/* AWS Study Hub - Main JS */
(function(){const b=document.getElementById('scroll-top');if(!b)return;window.addEventListener('scroll',()=>b.classList.toggle('visible',window.scrollY>400));b.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));})();

(function(){const p=location.pathname.replace(/\/$/,'');document.querySelectorAll('.nav-links a').forEach(a=>{const h=a.getAttribute('href').replace(/\/$/,'');if(p===h||(h!=='/'&&p.startsWith(h)))a.classList.add('active');});})();

document.querySelectorAll('.tab-container').forEach(c=>{const btns=c.querySelectorAll('.tab-btn'),panes=c.querySelectorAll('.tab-pane');btns.forEach((b,i)=>{b.addEventListener('click',()=>{btns.forEach(x=>x.classList.remove('active'));panes.forEach(x=>x.classList.remove('active'));b.classList.add('active');panes[i]&&panes[i].classList.add('active');});});if(btns[0])btns[0].click();});

(function(){const boxes=document.querySelectorAll('.checklist input[type="checkbox"]');boxes.forEach(cb=>{const k='chk_'+(cb.dataset.id||cb.closest('li')?.textContent?.trim().slice(0,60)||Math.random());cb.checked=localStorage.getItem(k)==='1';cb.closest('li')?.classList.toggle('done',cb.checked);cb.addEventListener('change',()=>{localStorage.setItem(k,cb.checked?'1':'0');cb.closest('li')?.classList.toggle('done',cb.checked);up();});});function up(){document.querySelectorAll('.progress-section').forEach(s=>{const b=s.querySelectorAll('input[type="checkbox"]'),d=[...b].filter(x=>x.checked).length,f=s.querySelector('.progress-fill'),l=s.querySelector('.progress-pct'),p=b.length?Math.round(d/b.length*100):0;if(f)f.style.width=p+'%';if(l)l.textContent=p+'%';});}up();})();

document.querySelectorAll('pre').forEach(pre=>{const btn=document.createElement('button');btn.textContent='Copy';btn.style.cssText='position:absolute;top:8px;right:8px;background:rgba(255,255,255,0.1);color:#ccc;border:1px solid rgba(255,255,255,0.2);border-radius:4px;padding:2px 10px;font-size:0.75rem;cursor:pointer;';pre.appendChild(btn);btn.addEventListener('click',()=>{navigator.clipboard.writeText(pre.querySelector('code')?.textContent||pre.textContent).then(()=>{btn.textContent='Copied!';setTimeout(()=>btn.textContent='Copy',1500);});});});

(function(){const h=document.querySelectorAll('h2[id],h3[id]'),l=document.querySelectorAll('.sidebar a');if(!h.length||!l.length)return;new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){l.forEach(x=>x.classList.remove('active'));const a=document.querySelector(`.sidebar a[href="#${e.target.id}"]`);if(a)a.classList.add('active');}});},{rootMargin:'0px 0px -70% 0px'}).observe&&h.forEach(x=>new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){l.forEach(y=>y.classList.remove('active'));const a=document.querySelector(`.sidebar a[href="#${e.target.id}"]`);if(a)a.classList.add('active');}});},{rootMargin:'0px 0px -70% 0px'}).observe(x));})();


/* ── Scroll reveal + staggered children + animated stat counters ── */
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Auto-tag sections and grids on the homepage-style pages for reveal (skip hero which has its own entrance)
  var revealTargets = [];
  document.querySelectorAll('.section, .cert-path').forEach(function(el){
    if (el.closest('.hero')) return;
    el.classList.add('reveal');
    revealTargets.push(el);
  });
  // Grids inside sections get staggered children
  document.querySelectorAll('.grid-2, .grid-3, .grid-4').forEach(function(el){
    if (el.closest('.hero')) return;
    el.classList.add('reveal-stagger');
    revealTargets.push(el);
  });

  if (reduce) {
    // Reveal everything immediately for reduced-motion users
    revealTargets.forEach(function(el){ el.classList.add('is-visible'); });
  } else if ('IntersectionObserver' in window) {
    // Apply a small stagger delay to direct children of stagger containers
    document.querySelectorAll('.reveal-stagger').forEach(function(c){
      Array.prototype.forEach.call(c.children, function(child, i){
        child.style.transitionDelay = (i * 0.07) + 's';
      });
    });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealTargets.forEach(function(el){ io.observe(el); });
  } else {
    revealTargets.forEach(function(el){ el.classList.add('is-visible'); });
  }

  // Animated count-up for hero stats (e.g., "12+", "200+", "500+", "100%")
  var stats = document.querySelectorAll('.stat-number');
  if (stats.length){
    stats.forEach(function(el){
      var raw = el.textContent.trim();
      var m = raw.match(/^(\d[\d,]*)(.*)$/);
      if (!m){ return; } // leave non-numeric labels as-is
      var target = parseInt(m[1].replace(/,/g,''), 10);
      var suffix = m[2] || '';
      if (reduce || !('IntersectionObserver' in window) || isNaN(target)){ return; }
      el.dataset.target = target;
      el.dataset.suffix = suffix;
      el.textContent = '0' + suffix;
    });

    if (!reduce && 'IntersectionObserver' in window){
      var seen = false;
      var sObs = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if (e.isIntersecting && !seen){
            seen = true;
            stats.forEach(function(el){
              if (!el.dataset.target) return;
              var target = parseInt(el.dataset.target, 10);
              var suffix = el.dataset.suffix || '';
              var dur = 1200, start = null;
              function step(ts){
                if (!start) start = ts;
                var p = Math.min((ts - start) / dur, 1);
                var eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
                el.textContent = Math.round(eased * target).toLocaleString() + suffix;
                if (p < 1) requestAnimationFrame(step);
              }
              requestAnimationFrame(step);
            });
          }
        });
      }, { threshold: 0.4 });
      var host = document.querySelector('.hero-stats') || stats[0];
      sObs.observe(host);
    }
  }
})();
