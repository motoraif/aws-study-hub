/* AWS Study Hub - Shared Navbar + Footer */
(function(){
  const segs=location.pathname.split('/').filter(Boolean);
  const inDocs=segs.includes('docs');
  const root=inDocs?'../':'./';

  const nav=`<nav class="navbar"><div class="container navbar-inner">
  <a class="navbar-brand" href="${root}index.html">&#9729;&#65039; AWS Study Hub</a>
  <button class="nav-toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
  <div class="nav-links" id="nav-links">
    <a href="${root}index.html">Home</a>
    <div class="nav-dropdown">
      <button class="nav-dropdown-btn">Foundations <span class="caret">&#9662;</span></button>
      <div class="nav-dropdown-menu">
        <a href="${root}docs/foundations-linux.html">&#128039; Linux Fundamentals</a>
        <a href="${root}docs/foundations-networking.html">&#127760; Networking Fundamentals</a>
      </div>
    </div>
    <div class="nav-dropdown">
      <button class="nav-dropdown-btn">Certifications <span class="caret">&#9662;</span></button>
      <div class="nav-dropdown-menu nav-dropdown-menu-wide">
        <div class="nav-col">
          <span class="nav-col-title">Foundational</span>
          <a href="${root}docs/clf-c02.html">CLF-C02 &middot; Cloud Practitioner</a>
          <a href="${root}docs/aif-c01.html">AIF-C01 &middot; AI Practitioner <span class="nav-pill nav-pill-new">New</span></a>
          <span class="nav-col-title">Associate</span>
          <a href="${root}docs/saa-c03.html">SAA-C03 &middot; Solutions Architect</a>
          <a href="${root}docs/dva-c02.html">DVA-C02 &middot; Developer</a>
          <a href="${root}docs/soa-c02.html">SOA-C02 &middot; SysOps</a>
          <a href="${root}docs/dea-c01.html">DEA-C01 &middot; Data Engineer <span class="nav-pill nav-pill-new">New</span></a>
          <a href="${root}docs/mla-c01.html">MLA-C01 &middot; ML Engineer <span class="nav-pill nav-pill-new">New</span></a>
        </div>
        <div class="nav-col">
          <span class="nav-col-title">Professional</span>
          <a href="${root}docs/sap-c02.html">SAP-C02 &middot; Solutions Architect Pro</a>
          <a href="${root}docs/dop-c02.html">DOP-C02 &middot; DevOps Engineer</a>
          <a href="${root}docs/aip-c01.html">AIP-C01 &middot; GenAI Developer <span class="nav-pill nav-pill-new">New</span></a>
          <span class="nav-col-title">Specialty</span>
          <a href="${root}docs/scs-c02.html">SCS-C02 &middot; Security</a>
          <a href="${root}docs/ans-c01.html">ANS-C01 &middot; Advanced Networking</a>
          <span class="nav-col-title">Retired</span>
          <a href="${root}docs/mls-c01.html">MLS-C01 &middot; ML Specialty <span class="nav-pill nav-pill-retired">Retired</span></a>
          <a href="${root}docs/das-c01.html">DAS-C01 &middot; Data Analytics <span class="nav-pill nav-pill-retired">Retired</span></a>
        </div>
      </div>
    </div>
    <a href="${root}docs/resources.html">Resources</a>
    <a href="${root}docs/labs.html">Labs</a>
    <a href="${root}docs/quiz.html">Quiz <span class="nav-pill nav-pill-new">New</span></a>
    <a href="${root}docs/news.html">News</a>
    <a href="https://github.com/motoraif/aws-study-hub" target="_blank" rel="noopener">GitHub &#11088;</a>
  </div>
</div></nav>`;

  const footer=`<footer><div class="container">
  <div class="footer-grid">
    <div>
      <div class="footer-brand">&#9729;&#65039; AWS Study Hub</div>
      <p class="footer-desc">Community-driven, open-source study platform for all AWS certifications. Free forever.</p>
      <div class="flex-wrap mt-1">
        <a href="https://github.com/motoraif/aws-study-hub" target="_blank" class="btn btn-outline" style="font-size:0.8rem;padding:0.4rem 0.9rem">&#11088; Star on GitHub</a>
        <a href="${root}CONTRIBUTING.md" target="_blank" class="btn btn-outline" style="font-size:0.8rem;padding:0.4rem 0.9rem">&#129309; Contribute</a>
      </div>
    </div>
    <div>
      <h5>Foundations</h5>
      <ul>
        <li><a href="${root}docs/foundations-linux.html">Linux Basics</a></li>
        <li><a href="${root}docs/foundations-networking.html">Networking Basics</a></li>
      </ul>
    </div>
    <div>
      <h5>Certifications</h5>
      <ul>
        <li><a href="${root}docs/clf-c02.html">Cloud Practitioner</a></li>
        <li><a href="${root}docs/aif-c01.html">AI Practitioner &#127381;</a></li>
        <li><a href="${root}docs/saa-c03.html">Solutions Architect Assoc.</a></li>
        <li><a href="${root}docs/dva-c02.html">Developer Associate</a></li>
        <li><a href="${root}docs/soa-c02.html">SysOps Associate</a></li>
        <li><a href="${root}docs/dea-c01.html">Data Engineer Assoc. &#127381;</a></li>
        <li><a href="${root}docs/mla-c01.html">ML Engineer Assoc. &#127381;</a></li>
        <li><a href="${root}docs/sap-c02.html">SA Professional</a></li>
        <li><a href="${root}docs/dop-c02.html">DevOps Professional</a></li>
        <li><a href="${root}docs/aip-c01.html">GenAI Developer Pro &#127381;</a></li>
        <li><a href="${root}docs/scs-c02.html">Security Specialty</a></li>
        <li><a href="${root}docs/ans-c01.html">Networking Specialty</a></li>
        <li><a href="${root}docs/mls-c01.html">ML Specialty (retired)</a></li>
        <li><a href="${root}docs/das-c01.html">Data Analytics (retired)</a></li>
      </ul>
    </div>
    <div>
      <h5>Resources</h5>
      <ul>
        <li><a href="${root}docs/resources.html">All Resources</a></li>
        <li><a href="${root}docs/labs.html">Labs &amp; Practice</a></li>
        <li><a href="${root}docs/quiz.html">Practice Quiz</a></li>
        <li><a href="${root}docs/news.html">AWS News</a></li>
        <li><a href="https://explore.skillbuilder.aws/" target="_blank">AWS Skill Builder</a></li>
        <li><a href="https://www.udemy.com/user/stephane-maarek/" target="_blank">Stephane Maarek</a></li>
        <li><a href="https://tutorialsdojo.com/" target="_blank">Tutorials Dojo</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 AWS Study Hub - MIT License</span>
    <span>Not affiliated with Amazon Web Services.</span>
  </div>
</div></footer>
<button id="scroll-top" title="Back to top">&#8593;</button>`;

  document.addEventListener('DOMContentLoaded',()=>{
    document.body.insertAdjacentHTML('afterbegin',nav);
    document.body.insertAdjacentHTML('beforeend',footer);

    // Mobile hamburger toggle
    const toggle=document.getElementById('nav-toggle');
    const links=document.getElementById('nav-links');
    if(toggle&&links){
      toggle.addEventListener('click',()=>{
        const open=links.classList.toggle('open');
        toggle.classList.toggle('open',open);
        toggle.setAttribute('aria-expanded',open?'true':'false');
      });
    }

    // Dropdown behaviour: hover on desktop (CSS), click/tap on mobile (JS)
    document.querySelectorAll('.nav-dropdown-btn').forEach(btn=>{
      btn.addEventListener('click',e=>{
        if(window.innerWidth<=900){
          e.preventDefault();
          const dd=btn.closest('.nav-dropdown');
          const wasOpen=dd.classList.contains('open');
          document.querySelectorAll('.nav-dropdown.open').forEach(x=>x.classList.remove('open'));
          if(!wasOpen)dd.classList.add('open');
        }
      });
    });

    // Close mobile menu when a real link is clicked
    links&&links.querySelectorAll('a').forEach(a=>{
      a.addEventListener('click',()=>{
        if(window.innerWidth<=900){
          links.classList.remove('open');
          toggle&&toggle.classList.remove('open');
          toggle&&toggle.setAttribute('aria-expanded','false');
        }
      });
    });
  });
})();
