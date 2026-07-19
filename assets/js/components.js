/* AWS Study Hub — Shared Navbar + Footer */
(function(){
  const segs=location.pathname.split('/').filter(Boolean);
  const inDocs=segs.includes('docs');
  const root=inDocs?'../':'./';

  const nav=`<nav class="navbar"><div class="container navbar-inner">
  <a class="navbar-brand" href="${root}index.html">&#9729;&#65039; AWS Study Hub</a>
  <div class="nav-links">
    <a href="${root}index.html">Home</a>
    <a href="${root}docs/foundations-linux.html">Linux</a>
    <a href="${root}docs/foundations-networking.html">Networking</a>
    <a href="${root}docs/clf-c02.html">CLF</a>
    <a href="${root}docs/saa-c03.html">SAA</a>
    <a href="${root}docs/dva-c02.html">DVA</a>
    <a href="${root}docs/soa-c02.html">SOA</a>
    <a href="${root}docs/sap-c02.html">SAP</a>
    <a href="${root}docs/dop-c02.html">DOP</a>
    <a href="${root}docs/scs-c02.html">Security</a>
    <a href="${root}docs/ans-c01.html">Networking+</a>
    <a href="${root}docs/mls-c01.html">ML</a>
    <a href="${root}docs/das-c01.html">Data</a>
    <a href="${root}docs/resources.html">Resources</a>
    <a href="${root}docs/labs.html">Labs</a>
    <a href="https://github.com/motoraif/aws-study-hub" target="_blank" rel="noopener">GitHub &#11088;</a>
  </div>
  <div class="nav-search">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8B949E" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
    <input id="global-search" type="text" placeholder="Search topics…" autocomplete="off">
  </div>
</div></nav>`;

  const footer=`<footer><div class="container">
  <div class="footer-grid">
    <div>
      <div class="footer-brand">&#9729;&#65039; AWS Study Hub</div>
      <p class="footer-desc">Community-driven, open-source study platform for all AWS certifications. Free forever.</p>
      <div class="flex-wrap mt-1">
        <a href="https://github.com/motoraif/aws-study-hub" target="_blank" class="btn btn-outline" style="font-size:0.8rem;padding:0.4rem 0.9rem">&#11088; Star on GitHub</a>
        <a href="https://github.com/motoraif/aws-study-hub/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener" class="btn btn-outline" style="font-size:0.8rem;padding:0.4rem 0.9rem">&#129309; Contribute</a>
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
        <li><a href="${root}docs/saa-c03.html">Solutions Architect Assoc.</a></li>
        <li><a href="${root}docs/dva-c02.html">Developer Associate</a></li>
        <li><a href="${root}docs/soa-c02.html">SysOps Associate</a></li>
        <li><a href="${root}docs/sap-c02.html">SA Professional</a></li>
        <li><a href="${root}docs/dop-c02.html">DevOps Professional</a></li>
        <li><a href="${root}docs/scs-c02.html">Security Specialty</a></li>
        <li><a href="${root}docs/ans-c01.html">Networking Specialty</a></li>
        <li><a href="${root}docs/mls-c01.html">ML Specialty</a></li>
        <li><a href="${root}docs/das-c01.html">Data Analytics Specialty</a></li>
      </ul>
    </div>
    <div>
      <h5>Resources</h5>
      <ul>
        <li><a href="${root}docs/resources.html">All Resources</a></li>
        <li><a href="${root}docs/labs.html">Labs &amp; Practice</a></li>
        <li><a href="https://explore.skillbuilder.aws/" target="_blank">AWS Skill Builder</a></li>
        <li><a href="https://www.udemy.com/user/stephane-maarek/" target="_blank">Stephane Maarek</a></li>
        <li><a href="https://tutorialsdojo.com/" target="_blank">Tutorials Dojo</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2025 AWS Study Hub &mdash; MIT License</span>
    <span>Not affiliated with Amazon Web Services.</span>
  </div>
</div></footer>
<button id="scroll-top" title="Back to top">&#8593;</button>`;

  document.addEventListener('DOMContentLoaded',()=>{
    document.body.insertAdjacentHTML('afterbegin',nav);
    document.body.insertAdjacentHTML('beforeend',footer);
  });
})();
