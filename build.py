#!/usr/bin/env python3
"""Build all AWS Study Hub HTML pages."""
import os, textwrap
BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = f"{BASE}/docs"
os.makedirs(DOCS, exist_ok=True)

# Canonical site URL (custom domain). Used for SEO tags and sitemap.
SITE_URL = "https://toraif.com/aws-study-hub"
OG_IMAGE = f"{SITE_URL}/assets/og-image.svg"

# Shared social / SEO meta tags injected into every page's <head>.
def seo_tags(title, desc, root):
    full_title = f"{title} - AWS Study Hub"
    return f"""  <meta name="robots" content="index,follow">
  <meta name="author" content="AWS Study Hub">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="AWS Study Hub">
  <meta property="og:title" content="{full_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:url" content="{SITE_URL}/">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{full_title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"{SITE_URL}/#website","name":"AWS Study Hub","url":"{SITE_URL}/","description":"Free, open-source study platform for every AWS certification.","inLanguage":"en","publisher":{{"@id":"{SITE_URL}/#org"}}}},{{"@type":"EducationalOrganization","@id":"{SITE_URL}/#org","name":"AWS Study Hub","url":"{SITE_URL}/","description":"Free, community-driven study resources for AWS certifications."}}]}}</script>"""

HEAD = lambda t,d: f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{t} - AWS Study Hub</title>
  <meta name="description" content="{d}">
{seo_tags(t, d, "../")}
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x2601;</text></svg>">
  <link rel="manifest" href="../manifest.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css">
  <script src="../assets/js/components.js"></script>
  <script src="../assets/js/search.js" defer></script>
</head><body>"""

HEAD_ROOT = lambda t,d: f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{t} - AWS Study Hub</title>
  <meta name="description" content="{d}">
{seo_tags(t, d, "")}
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x2601;</text></svg>">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <script src="assets/js/components.js"></script>
  <script src="assets/js/search.js" defer></script>
</head><body>"""

FOOT      = '<script src="../assets/js/main.js"></script></body></html>'
FOOT_ROOT = '<script src="assets/js/main.js"></script></body></html>'

def crumb(cert):
    return f'<div class="container" style="padding-top:2rem;"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Certifications</span> / <span>{cert}</span></div></div>'

def phdr(bcls,btxt,icon,title,desc,badges="",extra_badge=""):
    eb = f' {extra_badge}' if extra_badge else ''
    return f'<div class="page-header"><div class="container"><span class="badge {bcls}">{btxt}</span>{eb}<h1 style="margin-top:0.75rem;">{icon} {title}</h1><p>{desc}</p><div class="flex-wrap mt-1">{badges}</div></div></div>'

def quiz_cta(code):
    """A 'test yourself' CTA bar linking to a deep-linked quiz. Used on all cert pages."""
    return (f'<div class="container" style="padding-top:1.25rem"><div class="quiz-cta">'
            f'<span>&#129513; Ready to test yourself on {code}?</span>'
            f'<span class="quiz-cta-actions">'
            f'<a class="btn btn-primary" href="quiz.html?cert={code}">Quiz yourself &rarr;</a>'
            f'</span></div></div>')

def newcert_page(code, title, desc, level_cls, level_txt, icon, badges, notice_html, toc, body_html, extra_badge="", meta_desc=None):
    """Build a 'newer cert' page (AIF/DEA/MLA/AIP) that has a custom notice card and
    preserved body sections. `desc` is the visible header paragraph; `meta_desc`
    (defaults to desc) is the SEO/meta description."""
    header = phdr(level_cls, level_txt, icon, f"{code} - {title}", desc, badges, extra_badge)
    return (HEAD(f"{code} - {title}", meta_desc or desc) + crumb(code) + header + notice_html
            + quiz_cta(code) + wrap(toc, body_html) + FOOT)

NEW_CERT_BADGE = '<span class="badge badge-green">&#127381; New Certification</span>'
def new_notice(title_html, body_html):
    return ('\n<div class="container" style="padding-top:1.5rem"><div class="card" style="border:1px solid #2e7d32;background:rgba(46,125,50,0.12)">\n'
            f'  <h3 style="margin-top:0">{title_html}</h3>\n'
            f'  <p style="color:var(--text-muted);margin:0">{body_html}</p>\n'
            '</div></div>')

def wrap(toc,body):
    links="".join(f'<a href="#{a}">{b}</a>\n' for a,b in toc)
    return f'<div class="container" style="padding-bottom:4rem;"><div class="doc-layout"><aside class="sidebar"><h4>Contents</h4>{links}</aside><main>{body}</main></div></div>'

def chk(items,nf,nl):
    rows="".join(f'<li><input type="checkbox"><span>{i}</span></li>' for i in items)
    return f'<section id="checklist" class="progress-section"><h2>&#128203; Study Checklist</h2><div class="progress-wrap"><div class="progress-label"><span>Progress</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div><ul class="checklist">{rows}</ul><div class="mt-2"><a href="{nf}" class="btn btn-primary">Next: {nl} &rarr;</a></div></section>'

def exam(cn,cu,egu,sq,dur,q,ps,domains):
    dr="".join(f"<tr><td>{d}</td><td>{p}%</td></tr>" for d,p in domains)
    return f"""<section id="overview"><h2>Exam Overview</h2>
<div class="grid-2">
  <div class="card"><h3>Exam Details</h3><ul>
    <li><strong>Duration:</strong> {dur}</li><li><strong>Questions:</strong> {q}</li>
    <li><strong>Passing Score:</strong> {ps}/1000</li>
    <li><strong>Format:</strong> Multiple choice &amp; multiple response</li>
    <li><strong>Cost:</strong> ~$150-300 USD</li><li><strong>Validity:</strong> 3 years</li>
  </ul></div>
  <div class="card"><h3>&#127891; Official Resources</h3><ul>
    <li><a href="{cu}" target="_blank" rel="noopener">Free Skill Builder: {cn}</a></li>
    <li><a href="{egu}" target="_blank" rel="noopener">Official Exam Guide (PDF)</a></li>
    <li><a href="{sq}" target="_blank" rel="noopener">Official Sample Questions (PDF)</a></li>
    <li><a href="https://aws.amazon.com/certification/" target="_blank" rel="noopener">Schedule Your Exam</a></li>
    <li><a href="https://tutorialsdojo.com/" target="_blank" rel="noopener">Tutorials Dojo Practice Exams</a></li>
    <li><a href="https://www.udemy.com/user/stephane-maarek/" target="_blank" rel="noopener">Stephane Maarek on Udemy</a></li>
  </ul></div>
</div>
<h3>Exam Domains</h3>
<div class="table-wrap"><table><thead><tr><th>Domain</th><th>Weight</th></tr></thead><tbody>{dr}</tbody></table></div>
</section>"""

def _page_url(path):
    """Absolute canonical URL for a written file, based on its path relative to BASE."""
    rel = os.path.relpath(path, BASE).replace(os.sep, "/")
    return f"{SITE_URL}/{rel}"

def _breadcrumb_jsonld(path, content):
    """BreadcrumbList JSON-LD for a page, using its <title> as the page name."""
    import json as _j, re as _re, html as _h
    rel = os.path.relpath(path, BASE).replace(os.sep, "/")
    url = f"{SITE_URL}/{rel}"
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"}]
    if rel != "index.html":
        m = _re.search(r"<title>(.*?)</title>", content, _re.S)
        name = _h.unescape(m.group(1)).replace(" - AWS Study Hub", "").strip() if m else rel
        items.append({"@type": "ListItem", "position": 2, "name": name, "item": url})
    return ('<script type="application/ld+json">'
            + _j.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, ensure_ascii=False)
            + '</script>')

def write(path,content):
    # For HTML pages, inject per-page canonical, og:url, and breadcrumb structured data.
    if path.endswith(".html"):
        url = _page_url(path)
        if '<link rel="canonical"' not in content:
            content = content.replace('  <link rel="manifest"',
                                      f'  <link rel="canonical" href="{url}">\n  <link rel="manifest"', 1)
        content = content.replace(f'<meta property="og:url" content="{SITE_URL}/">',
                                  f'<meta property="og:url" content="{url}">', 1)
        if 'BreadcrumbList' not in content:
            content = content.replace('</head>', '  ' + _breadcrumb_jsonld(path, content) + '\n</head>', 1)
    with open(path,'w') as f: f.write(content)
    print(f"  Written: {path.split('/')[-1]}")

print("Building AWS Study Hub pages...")


# ── index.html ──────────────────────────────────────────────
index_body = """
<section class="hero"><div class="container">
  <div class="hero-eyebrow">&#128640; Open Source &middot; Community Driven &middot; Always Free</div>
  <h1>The Ultimate AWS<br>Certification Study Hub</h1>
  <p class="subtitle">Everything you need to pass every AWS certification - official Skill Builder courses, curated Udemy courses, hands-on labs, practice questions, Linux &amp; networking foundations. All free, all in one place.</p>
  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
    <a href="docs/clf-c02.html" class="btn btn-primary">&#127891; Start Learning</a>
    <a href="docs/resources.html" class="btn btn-outline">&#128218; Browse Resources</a>
    <a href="https://github.com/motoraif/aws-study-hub" target="_blank" class="btn btn-outline">&#11088; Star on GitHub</a>
  </div>
  <div class="hero-stats">
    <div class="stat-item"><div class="stat-number">12+</div><div class="stat-label">AWS Certifications</div></div>
    <div class="stat-item"><div class="stat-number">200+</div><div class="stat-label">Study Topics</div></div>
    <div class="stat-item"><div class="stat-number">500+</div><div class="stat-label">Practice Questions</div></div>
    <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Free Forever</div></div>
  </div>
</div></section>

<section style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:1.5rem 0;">
<div class="container"><div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;justify-content:center;">
  <span style="color:var(--text-muted);font-size:0.88rem;font-weight:600;">RECOMMENDED PATH:</span>
  <a href="docs/foundations-linux.html" class="badge badge-teal" style="text-decoration:none">1. Linux Basics</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/foundations-networking.html" class="badge badge-blue" style="text-decoration:none">2. Networking Basics</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/clf-c02.html" class="badge badge-orange" style="text-decoration:none">3. CLF-C02</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/saa-c03.html" class="badge badge-orange" style="text-decoration:none">4. SAA-C03</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/dva-c02.html" class="badge badge-orange" style="text-decoration:none">5. DVA-C02</a><span style="color:var(--text-muted)">&rarr;</span>
  <span class="badge badge-purple">Pro / Specialty</span>
</div></div></section>

<section class="section"><div class="container">
  <div class="text-center mb-2"><h2>&#129139; Start with the Foundations</h2><p style="color:var(--text-muted);max-width:600px;margin:0 auto;">Before diving into AWS, build solid Linux and networking fundamentals. These skills make every cert exam significantly easier.</p></div>
  <div class="grid-2">
    <a href="docs/foundations-linux.html" class="card" style="text-decoration:none;color:var(--text)">
      <div class="card-icon">&#128039;</div><h3>Linux Fundamentals</h3>
      <p style="color:var(--text-muted);font-size:0.92rem">File system, permissions, processes, networking, shell scripting, systemd - everything for AWS exams.</p>
      <div class="flex-wrap mt-1"><span class="badge badge-teal">Beginner Friendly</span><span class="badge badge-green">20 Topics</span></div>
    </a>
    <a href="docs/foundations-networking.html" class="card" style="text-decoration:none;color:var(--text)">
      <div class="card-icon">&#127760;</div><h3>Networking Fundamentals</h3>
      <p style="color:var(--text-muted);font-size:0.92rem">OSI model, TCP/IP, DNS, CIDR, subnetting, routing, load balancers, firewalls - the backbone of every AWS service.</p>
      <div class="flex-wrap mt-1"><span class="badge badge-blue">Essential</span><span class="badge badge-green">25 Topics</span></div>
    </a>
  </div>
</div></section>

<section class="section" style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
<div class="container">
  <div class="text-center mb-2"><h2>&#9729;&#65039; AWS Certifications</h2><p style="color:var(--text-muted);max-width:600px;margin:0 auto;">From beginner to expert. Each page includes official Skill Builder links, key topics, cheat sheets, and practice questions.</p></div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Foundational</h3>
  <a href="docs/clf-c02.html" class="cert-path" style="margin-bottom:2rem">
    <div class="cert-path-icon">&#127885;</div>
    <div><div class="cert-path-title">CLF-C02 - AWS Certified Cloud Practitioner</div>
    <div class="cert-path-meta">The perfect entry point. No technical background required. Cloud concepts, core services, security &amp; billing.</div>
    <div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-orange">Foundational</span><span class="badge badge-green">~6 hrs study</span></div></div>
  </a>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem;margin-top:2rem">Associate</h3>
  <div class="grid-3" style="margin-bottom:2rem">
    <a href="docs/saa-c03.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#127959;</div><div><div class="cert-path-title">SAA-C03</div><div class="cert-path-meta">Solutions Architect Associate - Most popular AWS cert.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
    <a href="docs/dva-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128104;&#8205;&#128187;</div><div><div class="cert-path-title">DVA-C02</div><div class="cert-path-meta">Developer Associate - Lambda, DynamoDB, CI/CD.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
    <a href="docs/soa-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#9881;</div><div><div class="cert-path-title">SOA-C02</div><div class="cert-path-meta">SysOps Administrator - Monitoring, automation, DR.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
  </div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Professional</h3>
  <div class="grid-2" style="margin-bottom:2rem">
    <a href="docs/sap-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129504;</div><div><div class="cert-path-title">SAP-C02 - Solutions Architect Professional</div><div class="cert-path-meta">Advanced architecture, org complexity, migration planning.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-purple">Professional</span></div></div></a>
    <a href="docs/dop-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128260;</div><div><div class="cert-path-title">DOP-C02 - DevOps Engineer Professional</div><div class="cert-path-meta">CI/CD, IaC, containers, monitoring at professional level.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-purple">Professional</span></div></div></a>
  </div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Specialty</h3>
  <div class="grid-4">
    <a href="docs/scs-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128274;</div><div><div class="cert-path-title">SCS-C02</div><div class="cert-path-meta">Security Specialty</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
    <a href="docs/ans-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#127760;</div><div><div class="cert-path-title">ANS-C01</div><div class="cert-path-meta">Advanced Networking</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
    <a href="docs/mls-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129302;</div><div><div class="cert-path-title">MLS-C01</div><div class="cert-path-meta">Machine Learning</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
    <a href="docs/das-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128202;</div><div><div class="cert-path-title">DAS-C01</div><div class="cert-path-meta">Data Analytics</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="text-center mb-2"><h2>&#10024; Why AWS Study Hub?</h2></div>
  <div class="grid-3">
    <div class="card"><div class="card-icon">&#127358;</div><h3>100% Free</h3><p style="color:var(--text-muted);font-size:0.9rem">Every resource is free or points to the best-value paid options. We prioritize free official AWS content first.</p></div>
    <div class="card"><div class="card-icon">&#127963;</div><h3>Official First</h3><p style="color:var(--text-muted);font-size:0.9rem">All content links back to AWS Skill Builder, official whitepapers, and official exam guides.</p></div>
    <div class="card"><div class="card-icon">&#129309;</div><h3>Community Driven</h3><p style="color:var(--text-muted);font-size:0.9rem">Open source on GitHub. Anyone can contribute. PRs and issues welcome!</p></div>
    <div class="card"><div class="card-icon">&#128202;</div><h3>Progress Tracking</h3><p style="color:var(--text-muted);font-size:0.9rem">Interactive checklists saved in your browser. Track what you've studied without an account.</p></div>
    <a href="docs/news.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#128260;</div><h3>Auto-Updated</h3><p style="color:var(--text-muted);font-size:0.9rem">GitHub Actions pulls the latest AWS news weekly so content stays fresh. <span style="color:var(--aws-orange)">View news &rarr;</span></p></a>
    <div class="card"><div class="card-icon">&#129139;</div><h3>Full-Stack Learning</h3><p style="color:var(--text-muted);font-size:0.9rem">Starts from Linux and networking basics, building up to professional and specialty certifications.</p></div>
  </div>
</div></section>

<section class="section" style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border);">
<div class="container">
  <div class="text-center mb-2"><h2>&#128279; Top Study Resources</h2></div>
  <div class="grid-4">
    <a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#127891;</div><h3 style="font-size:1rem">AWS Skill Builder</h3><p style="font-size:0.85rem;color:var(--text-muted)">Official free courses, labs, and exam prep from AWS.</p><span class="badge badge-green">FREE</span></a>
    <a href="https://www.udemy.com/user/stephane-maarek/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#11088;</div><h3 style="font-size:1rem">Stephane Maarek</h3><p style="font-size:0.85rem;color:var(--text-muted)">#1 rated AWS instructor on Udemy. 1M+ students.</p><span class="badge badge-orange">PAID</span></a>
    <a href="https://tutorialsdojo.com/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#128221;</div><h3 style="font-size:1rem">Tutorials Dojo</h3><p style="font-size:0.85rem;color:var(--text-muted)">Best practice exams. Cheat sheets and study guides.</p><span class="badge badge-blue">FREE+PAID</span></a>
    <a href="https://learn.cantrill.io/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#127919;</div><h3 style="font-size:1rem">Adrian Cantrill</h3><p style="font-size:0.85rem;color:var(--text-muted)">Deep-dive technical courses with amazing diagrams.</p><span class="badge badge-orange">PAID</span></a>
  </div>
  <div class="text-center mt-2"><a href="docs/resources.html" class="btn btn-outline">View All Resources &rarr;</a></div>
</div></section>

<section class="section"><div class="container">
  <div class="card" style="text-align:center;max-width:700px;margin:0 auto;padding:3rem">
    <div style="font-size:3rem;margin-bottom:1rem">&#129309;</div>
    <h2 style="margin-top:0">Help Make This the #1 AWS Study Resource</h2>
    <p style="color:var(--text-muted)">This project thrives on community contributions. Passed an exam? Share your notes. Found a great resource? Add it. Found a bug? Fix it.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem">
      <a href="https://github.com/motoraif/aws-study-hub/blob/main/CONTRIBUTING.md" target="_blank" class="btn btn-primary">Read Contributing Guide</a>
      <a href="https://github.com/motoraif/aws-study-hub/issues/new/choose" target="_blank" class="btn btn-outline">Open an Issue</a>
    </div>
  </div>
</div></section>
"""
write(f"{BASE}/index.html", HEAD_ROOT("AWS Study Hub - Ultimate AWS Certification Study Platform","Free open-source study hub for all AWS certifications. Official resources, labs, practice questions, Linux and networking foundations.")+index_body+FOOT_ROOT)
print("  index.html done")


# ── index.html ──────────────────────────────────────────────
index_html = HEAD_ROOT("AWS Study Hub - Ultimate AWS Certification Study Platform","Free community-driven study hub for all AWS certifications.") + """
<section class="hero"><div class="container">
  <div class="hero-eyebrow">&#128640; Open Source &middot; Community Driven &middot; Always Free</div>
  <h1>The Ultimate AWS<br>Certification Study Hub</h1>
  <p class="subtitle">Everything you need to pass every AWS certification - official Skill Builder courses, curated Udemy courses, hands-on labs, practice questions, Linux &amp; networking foundations. All free, all in one place.</p>
  <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
    <a href="docs/clf-c02.html" class="btn btn-primary">&#127891; Start Learning</a>
    <a href="docs/quiz.html" class="btn btn-outline">&#129513; Take a Quiz</a>
    <a href="docs/resources.html" class="btn btn-outline">&#128218; Browse Resources</a>
    <a href="https://github.com/motoraif/aws-study-hub" target="_blank" class="btn btn-outline">&#11088; Star on GitHub</a>
  </div>
  <div class="hero-stats">
    <div class="stat-item"><div class="stat-number">12+</div><div class="stat-label">AWS Certifications</div></div>
    <div class="stat-item"><div class="stat-number">200+</div><div class="stat-label">Study Topics</div></div>
    <div class="stat-item"><div class="stat-number">500+</div><div class="stat-label">Practice Questions</div></div>
    <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Free Forever</div></div>
  </div>
</div></section>

<section style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:1.5rem 0">
<div class="container"><div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;justify-content:center">
  <span style="color:var(--text-muted);font-size:0.88rem;font-weight:600">RECOMMENDED PATH:</span>
  <a href="docs/foundations-linux.html" class="badge badge-teal" style="text-decoration:none">1. Linux</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/foundations-networking.html" class="badge badge-blue" style="text-decoration:none">2. Networking</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/clf-c02.html" class="badge badge-orange" style="text-decoration:none">3. CLF-C02</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/saa-c03.html" class="badge badge-orange" style="text-decoration:none">4. SAA-C03</a><span style="color:var(--text-muted)">&rarr;</span>
  <a href="docs/dva-c02.html" class="badge badge-orange" style="text-decoration:none">5. DVA-C02</a><span style="color:var(--text-muted)">&rarr;</span>
  <span class="badge badge-purple">Pro / Specialty</span>
</div></div></section>

<section class="section" style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border)"><div class="container">
  <div class="text-center mb-2"><h2>&#128640; Interactive Study Tools</h2><p style="color:var(--text-muted);max-width:620px;margin:0 auto">Go beyond reading. Test yourself, review the tricky comparisons, and track your readiness - all free and saved privately in your browser.</p></div>
  <div class="grid-3">
    <a href="docs/quiz.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#129513;</div><h3>Practice Quiz</h3><p style="color:var(--text-muted);font-size:0.92rem">Timed, randomized questions per certification with instant scoring, a domain breakdown, and explanations for every answer.</p><div class="flex-wrap mt-1"><span class="badge badge-blue">63+ questions</span><span class="badge badge-green">Instant scoring</span></div></a>
    <a href="docs/cheatsheets.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#128221;</div><h3>Confusing Pairs Cheat Sheet</h3><p style="color:var(--text-muted);font-size:0.92rem">Side-by-side comparisons of the look-alike services that trip people up: SG vs NACL, SQS vs SNS, EBS vs EFS vs FSx, and more.</p><div class="flex-wrap mt-1"><span class="badge badge-teal">Quick reference</span><span class="badge badge-orange">Exam gold</span></div></a>
    <a href="docs/dashboard.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#128202;</div><h3>My Progress</h3><p style="color:var(--text-muted);font-size:0.92rem">Your quiz readiness per certification and study-checklist completion in one dashboard. Private and local - no account needed.</p><div class="flex-wrap mt-1"><span class="badge badge-green">Track readiness</span><span class="badge badge-blue">Saved locally</span></div></a>
  </div>
  <div class="text-center mt-2"><p style="color:var(--text-muted);font-size:0.9rem">Tip: press <kbd style="background:var(--bg-hover);border:1px solid var(--border);border-radius:4px;padding:0.05em 0.4em">/</kbd> anywhere to search the whole site.</p></div>
</div></section>

<section class="section"><div class="container">
  <div class="text-center mb-2"><h2>&#129139; Foundations First</h2><p style="color:var(--text-muted);max-width:600px;margin:0 auto">Build solid Linux and networking fundamentals before diving into AWS. These skills make every cert exam significantly easier.</p></div>
  <div class="grid-2">
    <a href="docs/foundations-linux.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#128039;</div><h3>Linux Fundamentals</h3><p style="color:var(--text-muted);font-size:0.92rem">File system, permissions, processes, networking, shell scripting, systemd.</p><div class="flex-wrap mt-1"><span class="badge badge-teal">Beginner Friendly</span><span class="badge badge-green">20 Topics</span></div></a>
    <a href="docs/foundations-networking.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#127760;</div><h3>Networking Fundamentals</h3><p style="color:var(--text-muted);font-size:0.92rem">OSI model, TCP/IP, DNS, CIDR, subnetting, routing, load balancers, firewalls.</p><div class="flex-wrap mt-1"><span class="badge badge-blue">Essential</span><span class="badge badge-green">25 Topics</span></div></a>
  </div>
</div></section>

<section class="section" style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
<div class="container">
  <div class="text-center mb-2"><h2>&#9729;&#65039; AWS Certifications</h2><p style="color:var(--text-muted);max-width:600px;margin:0 auto">From beginner to expert. Each page includes official Skill Builder links, key topics, cheat sheets, and practice questions.</p></div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Foundational</h3>
  <div class="grid-2" style="margin-bottom:2rem">
    <a href="docs/clf-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#127885;</div><div><div class="cert-path-title">CLF-C02 - Cloud Practitioner</div><div class="cert-path-meta">The perfect entry point. Cloud concepts, core services, security &amp; billing.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-orange">Foundational</span></div></div></a>
    <a href="docs/aif-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129504;</div><div><div class="cert-path-title">AIF-C01 - AI Practitioner</div><div class="cert-path-meta">Foundational AI, ML &amp; generative AI concepts and AWS AI services.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-orange">Foundational</span><span class="badge badge-green">New &#127381;</span></div></div></a>
  </div>
  <h3 style="color:var(--aws-orange);margin:2rem 0 1rem">Associate</h3>
  <div class="grid-3" style="margin-bottom:2rem">
    <a href="docs/saa-c03.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#127959;</div><div><div class="cert-path-title">SAA-C03</div><div class="cert-path-meta">Solutions Architect Associate</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
    <a href="docs/dva-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128187;</div><div><div class="cert-path-title">DVA-C02</div><div class="cert-path-meta">Developer Associate</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
    <a href="docs/soa-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#9881;</div><div><div class="cert-path-title">SOA-C02</div><div class="cert-path-meta">SysOps Administrator</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span></div></div></a>
    <a href="docs/dea-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128202;</div><div><div class="cert-path-title">DEA-C01</div><div class="cert-path-meta">Data Engineer Associate</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span><span class="badge badge-green">New &#127381;</span></div></div></a>
    <a href="docs/mla-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129302;</div><div><div class="cert-path-title">MLA-C01</div><div class="cert-path-meta">Machine Learning Engineer Associate</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-blue">Associate</span><span class="badge badge-green">New &#127381;</span></div></div></a>
  </div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Professional</h3>
  <div class="grid-3" style="margin-bottom:2rem">
    <a href="docs/sap-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129504;</div><div><div class="cert-path-title">SAP-C02 - Solutions Architect Pro</div><div class="cert-path-meta">Advanced architecture, org complexity, migration planning.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-purple">Professional</span></div></div></a>
    <a href="docs/dop-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128260;</div><div><div class="cert-path-title">DOP-C02 - DevOps Engineer Pro</div><div class="cert-path-meta">CI/CD, IaC, containers, monitoring at professional level.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-purple">Professional</span></div></div></a>
    <a href="docs/aip-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#129504;</div><div><div class="cert-path-title">AIP-C01 - GenAI Developer Pro</div><div class="cert-path-meta">Build production generative AI apps: Bedrock, agents, RAG, guardrails.</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-purple">Professional</span><span class="badge badge-green">New &#127381;</span></div></div></a>
  </div>
  <h3 style="color:var(--aws-orange);margin-bottom:1rem">Specialty</h3>
  <div class="grid-4">
    <a href="docs/scs-c02.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#128274;</div><div><div class="cert-path-title">SCS-C02</div><div class="cert-path-meta">Security Specialty</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
    <a href="docs/ans-c01.html" class="cert-path" style="text-decoration:none;color:var(--text)"><div class="cert-path-icon">&#127760;</div><div><div class="cert-path-title">ANS-C01</div><div class="cert-path-meta">Advanced Networking</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge badge-red">Specialty</span></div></div></a>
    <a href="docs/mls-c01.html" class="cert-path" style="text-decoration:none;color:var(--text);opacity:0.7"><div class="cert-path-icon">&#129302;</div><div><div class="cert-path-title">MLS-C01</div><div class="cert-path-meta">Machine Learning - use MLA-C01 instead</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge" style="background:#6b1010;color:#ffb3b3;border:1px solid #a33">&#9940; Retired</span></div></div></a>
    <a href="docs/das-c01.html" class="cert-path" style="text-decoration:none;color:var(--text);opacity:0.7"><div class="cert-path-icon">&#128202;</div><div><div class="cert-path-title">DAS-C01</div><div class="cert-path-meta">Data Analytics - use DEA-C01 instead</div><div class="flex-wrap" style="margin-top:0.4rem"><span class="badge" style="background:#6b1010;color:#ffb3b3;border:1px solid #a33">&#9940; Retired</span></div></div></a>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="text-center mb-2"><h2>&#10024; Why AWS Study Hub?</h2></div>
  <div class="grid-3">
    <div class="card"><div class="card-icon">&#127358;</div><h3>100% Free</h3><p style="color:var(--text-muted);font-size:0.9rem">Every resource is free or points to the best-value paid options. Official AWS content first.</p></div>
    <div class="card"><div class="card-icon">&#127963;</div><h3>Official First</h3><p style="color:var(--text-muted);font-size:0.9rem">All content links back to AWS Skill Builder, official whitepapers, and exam guides.</p></div>
    <div class="card"><div class="card-icon">&#129309;</div><h3>Community Driven</h3><p style="color:var(--text-muted);font-size:0.9rem">Open source on GitHub. Anyone can contribute. PRs and issues welcome!</p></div>
    <div class="card"><div class="card-icon">&#9989;</div><h3>Progress Tracking</h3><p style="color:var(--text-muted);font-size:0.9rem">Interactive checklists saved in your browser. No account needed.</p></div>
    <a href="docs/news.html" class="card" style="text-decoration:none;color:var(--text)"><div class="card-icon">&#128260;</div><h3>Auto-Updated</h3><p style="color:var(--text-muted);font-size:0.9rem">GitHub Actions pulls the latest AWS news weekly so content stays fresh. <span style="color:var(--aws-orange)">View news &rarr;</span></p></a>
    <div class="card"><div class="card-icon">&#129139;</div><h3>Full-Stack Learning</h3><p style="color:var(--text-muted);font-size:0.9rem">Linux basics &rarr; Networking &rarr; AWS Associate &rarr; Professional &rarr; Specialty.</p></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="text-center mb-2"><h2>&#128240; Latest AWS News</h2><p style="color:var(--text-muted);max-width:600px;margin:0 auto">Fresh from the official AWS What's New feed, updated automatically every week.</p></div>
  <div id="home-news" class="grid-3">
    <div class="card"><p style="color:var(--text-muted)">Loading latest AWS news&hellip;</p></div>
  </div>
  <div class="text-center mt-2"><a href="docs/news.html" class="btn btn-outline">View All AWS News &rarr;</a></div>
</div></section>
<script>
(function(){
  var el = document.getElementById("home-news");
  if(!el) return;
  function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}[c]; }); }
  fetch("data/aws-news.json",{cache:"no-cache"})
    .then(function(r){ if(!r.ok) throw new Error("HTTP "+r.status); return r.json(); })
    .then(function(data){
      var items=((data&&data.items)||[]).slice(0,3);
      if(!items.length){ el.innerHTML='<div class="card"><p style="color:var(--text-muted)">No news items yet.</p></div>'; return; }
      el.innerHTML=items.map(function(it){
        return '<a href="'+esc(it.link||"#")+'" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);display:block">'+
               '<div class="flex-wrap" style="margin-bottom:0.5rem"><span class="badge badge-orange">'+esc(it.date||"")+'</span></div>'+
               '<h3 style="font-size:1rem;margin:0 0 0.4rem">'+esc(it.title||"")+'</h3>'+
               '<p style="color:var(--text-muted);font-size:0.85rem;margin:0">'+esc((it.summary||"").slice(0,140))+'</p></a>';
      }).join("");
    })
    .catch(function(){ el.innerHTML='<div class="card"><p style="color:var(--text-muted)">Could not load news. <a href="docs/news.html">Open the News page &rarr;</a></p></div>'; });
})();
</script>

<section class="section" style="background:var(--bg-card);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
<div class="container">
  <div class="text-center mb-2"><h2>&#128279; Top Study Resources</h2></div>
  <div class="grid-4">
    <a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#127891;</div><h3 style="font-size:1rem">AWS Skill Builder</h3><p style="font-size:0.85rem;color:var(--text-muted)">Official free courses, labs, exam prep.</p><span class="badge badge-green">FREE</span></a>
    <a href="https://www.udemy.com/user/stephane-maarek/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#11088;</div><h3 style="font-size:1rem">Stephane Maarek</h3><p style="font-size:0.85rem;color:var(--text-muted)">#1 rated AWS instructor on Udemy. 1M+ students.</p><span class="badge badge-orange">PAID</span></a>
    <a href="https://tutorialsdojo.com/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#128221;</div><h3 style="font-size:1rem">Tutorials Dojo</h3><p style="font-size:0.85rem;color:var(--text-muted)">Best practice exams and cheat sheets.</p><span class="badge badge-blue">FREE+PAID</span></a>
    <a href="https://learn.cantrill.io/" target="_blank" rel="noopener" class="card" style="text-decoration:none;color:var(--text);text-align:center"><div style="font-size:2.5rem;margin-bottom:0.75rem">&#127919;</div><h3 style="font-size:1rem">Adrian Cantrill</h3><p style="font-size:0.85rem;color:var(--text-muted)">Deep-dive technical courses with amazing diagrams.</p><span class="badge badge-orange">PAID</span></a>
  </div>
  <div class="text-center mt-2"><a href="docs/resources.html" class="btn btn-outline">View All Resources &rarr;</a></div>
</div></section>

<section class="section"><div class="container">
  <div class="card" style="text-align:center;max-width:700px;margin:0 auto;padding:3rem">
    <div style="font-size:3rem;margin-bottom:1rem">&#129309;</div>
    <h2 style="margin-top:0">Help Make This the #1 AWS Study Resource</h2>
    <p style="color:var(--text-muted)">Passed an exam? Share your tips. Found a great resource? Add it. Found a bug? Fix it. Every contribution helps thousands of learners.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem">
      <a href="https://github.com/motoraif/aws-study-hub/blob/main/CONTRIBUTING.md" target="_blank" class="btn btn-primary">Read Contributing Guide</a>
      <a href="https://github.com/motoraif/aws-study-hub/issues/new/choose" target="_blank" class="btn btn-outline">Open an Issue</a>
    </div>
  </div>
</div></section>
""" + FOOT_ROOT
write(f"{BASE}/index.html", index_html)


# ── CLF-C02 ─────────────────────────────────────────────────
clf = HEAD("CLF-C02 - AWS Cloud Practitioner","Complete CLF-C02 study guide. Cloud concepts, shared responsibility, IAM, core services, billing, and support plans.") + crumb("CLF-C02") + phdr("badge-orange","Foundational","&#127885;","CLF-C02 - AWS Certified Cloud Practitioner","The entry-level AWS certification. Cloud concepts, core services, security, billing, and support. No technical background required.",'<span class="badge badge-green">90 min | 65 questions</span><span class="badge badge-blue">Passing: 700/1000</span><span class="badge badge-teal">No prerequisites</span>') + quiz_cta("CLF-C02") + wrap([
("overview","Exam Overview"),("cloud-concepts","Cloud Concepts"),("shared-resp","Shared Responsibility"),("global-infra","Global Infrastructure"),("iam","IAM"),("core-services","Core Services"),("billing","Billing &amp; Pricing"),("checklist","Checklist")],
exam("AWS Cloud Practitioner Essentials","https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials","https://d1.awsstatic.com/training-and-certification/docs-cloud-practitioner/AWS-Certified-Cloud-Practitioner_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-cloud-practitioner/AWS-Certified-Cloud-Practitioner_Sample-Questions.pdf","90 minutes","65","700",[("Cloud Concepts","24"),("Security &amp; Compliance","30"),("Cloud Technology &amp; Services","34"),("Billing, Pricing &amp; Support","12")])+"""
<section id="cloud-concepts"><h2>Cloud Concepts</h2>
<h3>The 6 Advantages of Cloud Computing</h3>
<div class="grid-2">
  <div class="card"><h4>1. Trade CapEx for Variable Expense</h4><p>Pay only for what you consume instead of investing upfront in data centers and servers.</p></div>
  <div class="card"><h4>2. Massive Economies of Scale</h4><p>AWS pools usage from hundreds of thousands of customers - passes savings to you.</p></div>
  <div class="card"><h4>3. Stop Guessing Capacity</h4><p>Scale up or down in minutes. No over/under provisioning ever again.</p></div>
  <div class="card"><h4>4. Increase Speed &amp; Agility</h4><p>Deploy resources in minutes vs weeks. Experiment faster, fail cheaper.</p></div>
  <div class="card"><h4>5. Stop Spending on Data Centers</h4><p>Focus on your business, not racking servers and running cables.</p></div>
  <div class="card"><h4>6. Go Global in Minutes</h4><p>Deploy in multiple Regions worldwide instantly. Low latency globally.</p></div>
</div>
<h3>Cloud Service Models</h3>
<div class="table-wrap"><table><thead><tr><th>Model</th><th>You Manage</th><th>AWS Manages</th><th>AWS Examples</th></tr></thead><tbody>
  <tr><td><strong>IaaS</strong></td><td>OS, runtime, apps, data</td><td>Servers, storage, networking, virtualization</td><td>EC2, VPC, EBS</td></tr>
  <tr><td><strong>PaaS</strong></td><td>Apps, data</td><td>OS, runtime, middleware</td><td>Elastic Beanstalk, RDS</td></tr>
  <tr><td><strong>SaaS</strong></td><td>Nothing (just use it)</td><td>Everything</td><td>WorkMail, Chime</td></tr>
</tbody></table></div></section>

<section id="shared-resp"><h2>Shared Responsibility Model</h2>
<div class="callout warn"><div class="callout-title">&#9888; Most Tested CLF Topic</div><p>The Shared Responsibility Model is the most commonly tested concept on CLF. Know it perfectly.</p></div>
<div class="grid-2">
  <div class="card" style="border-color:var(--aws-orange)"><h3>AWS - "Security OF the Cloud"</h3><ul>
    <li>Physical data center security</li><li>Hardware &amp; global network infrastructure</li>
    <li>Hypervisor / virtualization layer</li><li>Managed service OS patching (RDS, Lambda)</li>
  </ul></div>
  <div class="card" style="border-color:var(--aws-blue)"><h3>Customer - "Security IN the Cloud"</h3><ul>
    <li>EC2 OS patching &amp; updates</li><li>Application code security</li>
    <li>IAM users, roles, policies</li><li>Data encryption &amp; backups</li>
    <li>Security Groups &amp; Network ACLs</li>
  </ul></div>
</div>
<div class="callout tip"><div class="callout-title">&#128161; Quick Rule</div><p>"If you can configure it in the AWS Console, it's your responsibility." EC2 OS = you. RDS OS = AWS (managed). S3 bucket policy = you. S3 physical hardware = AWS.</p></div></section>

<section id="global-infra"><h2>AWS Global Infrastructure</h2>
<div class="grid-3">
  <div class="card"><h3>&#127757; Regions</h3><p>Geographically separate areas (e.g., us-east-1). Each has 2+ AZs. Choose by: latency, compliance, cost, services available. AWS has 34+ Regions.</p></div>
  <div class="card"><h3>&#127968; Availability Zones</h3><p>One or more data centers in a Region with redundant power/networking. Deploy across 2+ AZs for high availability. 108+ AZs globally.</p></div>
  <div class="card"><h3>&#127760; Edge Locations</h3><p>400+ CDN endpoints globally for CloudFront &amp; Route 53. Cache content close to users for low latency.</p></div>
</div></section>

<section id="iam"><h2>IAM - Identity &amp; Access Management</h2>
<div class="grid-2">
  <div><h3>Components</h3><ul>
    <li><strong>Root User</strong> - master account; enable MFA; never use for daily tasks</li>
    <li><strong>Users</strong> - individual people or service accounts</li>
    <li><strong>Groups</strong> - collections of users sharing policies</li>
    <li><strong>Roles</strong> - temporary permissions assumed by services/users</li>
    <li><strong>Policies</strong> - JSON documents defining Allow/Deny</li>
  </ul></div>
  <div><h3>Best Practices</h3><ul>
    <li>&#128274; Never use root for daily tasks</li><li>&#128274; Enable MFA on root and admins</li>
    <li>&#128274; Grant least privilege</li><li>&#128274; Use IAM Roles for EC2/Lambda (not keys)</li>
    <li>&#128274; Rotate access keys regularly</li><li>&#128274; Use Organizations for multi-account</li>
  </ul></div>
</div></section>

<section id="core-services"><h2>Core Services Cheat Sheet</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Category</th><th>What It Does</th></tr></thead><tbody>
  <tr><td>EC2</td><td>Compute</td><td>Virtual servers. Many types: General, Compute, Memory, Storage, GPU.</td></tr>
  <tr><td>Lambda</td><td>Serverless</td><td>Run code without servers. Pay per invocation. Max 15 min timeout.</td></tr>
  <tr><td>S3</td><td>Storage</td><td>Object storage. Unlimited capacity. 11 9s durability (99.999999999%).</td></tr>
  <tr><td>EBS</td><td>Storage</td><td>Block storage for EC2. Like a hard drive attached to your server.</td></tr>
  <tr><td>RDS</td><td>Database</td><td>Managed relational DB. MySQL, PostgreSQL, Aurora, Oracle, SQL Server.</td></tr>
  <tr><td>DynamoDB</td><td>Database</td><td>Serverless NoSQL. Single-digit ms latency. Auto-scaling.</td></tr>
  <tr><td>VPC</td><td>Networking</td><td>Isolated virtual network. Subnets, route tables, security groups, NACLs.</td></tr>
  <tr><td>CloudFront</td><td>CDN</td><td>Content delivery network. 400+ edge locations globally.</td></tr>
  <tr><td>Route 53</td><td>DNS</td><td>Scalable DNS service. Domain registration. Health checking.</td></tr>
  <tr><td>SNS</td><td>Messaging</td><td>Pub/sub. Push to email, SMS, Lambda, SQS.</td></tr>
  <tr><td>SQS</td><td>Messaging</td><td>Message queue. Decouple microservices. Standard &amp; FIFO.</td></tr>
  <tr><td>CloudWatch</td><td>Monitoring</td><td>Metrics, logs, alarms, dashboards. Monitor everything.</td></tr>
  <tr><td>CloudTrail</td><td>Governance</td><td>Audit log of all API calls. Who did what, when, from where.</td></tr>
</tbody></table></div></section>

<section id="billing"><h2>Billing &amp; Pricing</h2>
<h3>EC2 Pricing Models</h3>
<div class="grid-2">
  <div class="card"><h4>On-Demand</h4><p>Pay per hour/second. No commitment. Best for: testing, unpredictable workloads.</p></div>
  <div class="card"><h4>Reserved (1 or 3 year)</h4><p>Up to 72% off. Best for: steady-state predictable workloads.</p></div>
  <div class="card"><h4>Spot Instances</h4><p>Up to 90% off spare capacity. Can be interrupted with 2-min notice. Best for: fault-tolerant batch jobs.</p></div>
  <div class="card"><h4>Savings Plans</h4><p>Commit to $/hr for 1-3 years. Flexible. Covers EC2, Lambda, Fargate.</p></div>
</div>
<h3>AWS Support Plans</h3>
<div class="table-wrap"><table><thead><tr><th>Plan</th><th>Price</th><th>Critical Response</th><th>Key Features</th></tr></thead><tbody>
  <tr><td>Basic</td><td>Free</td><td>No tech support</td><td>7 Trusted Advisor checks, docs, forums</td></tr>
  <tr><td>Developer</td><td>$29+/mo</td><td>Business hours</td><td>Email, general guidance</td></tr>
  <tr><td>Business</td><td>$100+/mo</td><td>24/7, 1 hour</td><td>Phone, all TA checks, Health API</td></tr>
  <tr><td>Enterprise On-Ramp</td><td>$5,500+/mo</td><td>30 minutes</td><td>Pool of TAMs, concierge</td></tr>
  <tr><td>Enterprise</td><td>$15,000+/mo</td><td>15 minutes</td><td>Dedicated TAM, architectural reviews</td></tr>
</tbody></table></div></section>
""" + chk(["Explain the 6 advantages of cloud computing","Describe IaaS, PaaS, SaaS with AWS examples","Explain the Shared Responsibility Model perfectly","Know Regions, AZs, Edge Locations differences","Understand IAM: Users, Groups, Roles, Policies","Know IAM best practices (MFA, least privilege, no root)","Know core services: EC2, S3, RDS, Lambda, VPC, DynamoDB","Explain S3 storage classes (Standard, IA, Glacier)","Know EC2 pricing: On-Demand, Reserved, Spot, Savings Plans","Explain AWS Support plans and response times","Know AWS Organizations and SCPs","Know AWS Well-Architected Framework 6 pillars","Understand Trusted Advisor 5 categories","Know cost tools: Cost Explorer, Budgets, Pricing Calculator","Know difference between CloudTrail vs CloudWatch","Understand AWS Shield, WAF, Inspector, Macie","Know the AWS Free Tier limits","Explain SNS vs SQS use cases","Understand Auto Scaling and Elastic Load Balancing","Know AWS Artifact and compliance programs"],"saa-c03.html","Solutions Architect Associate (SAA-C03)")) + FOOT
write(f"{DOCS}/clf-c02.html", clf)


# ── SAA-C03 ──────────────────────────────────────────────────
saa = HEAD("SAA-C03 - Solutions Architect Associate","Complete SAA-C03 study guide. EC2, S3, VPC, RDS, serverless, HA design patterns, security.") + crumb("SAA-C03") + phdr("badge-blue","Associate","&#127959;","SAA-C03 - AWS Certified Solutions Architect Associate","The most popular AWS certification. Design resilient, performant, secure, cost-optimized architectures.",'<span class="badge badge-green">130 min | 65 questions</span><span class="badge badge-blue">Passing: 720/1000</span>') + quiz_cta("SAA-C03") + wrap([("overview","Exam Overview"),("ec2","EC2 Deep Dive"),("s3","S3 Deep Dive"),("vpc","VPC &amp; Networking"),("ha","HA &amp; Resilient Design"),("serverless","Serverless"),("security","Security"),("checklist","Checklist")],
exam("AWS Solutions Architect Associate","https://explore.skillbuilder.aws/learn/course/external/view/elearning/1044/aws-certified-solutions-architect-associate-official-practice-question-set-saa-c03-english","https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf","130 minutes","65","720",[("Design Secure Architectures","30"),("Design Resilient Architectures","26"),("Design High-Performing Architectures","24"),("Design Cost-Optimized Architectures","20")])+"""
<section id="ec2"><h2>EC2 Deep Dive</h2>
<h3>Instance Type Families</h3>
<div class="table-wrap"><table><thead><tr><th>Family</th><th>Types</th><th>Use Cases</th></tr></thead><tbody>
  <tr><td>General Purpose</td><td>T, M</td><td>Web servers, dev, code repos</td></tr>
  <tr><td>Compute Optimized</td><td>C</td><td>Batch processing, ML, HPC, gaming</td></tr>
  <tr><td>Memory Optimized</td><td>R, X, z</td><td>In-memory DBs, big data analytics</td></tr>
  <tr><td>Storage Optimized</td><td>I, D, H</td><td>NoSQL DBs, data warehousing, Hadoop</td></tr>
  <tr><td>Accelerated</td><td>P, G, Inf</td><td>GPU-based ML, video encoding</td></tr>
</tbody></table></div>
<h3>EC2 Storage Options</h3>
<div class="table-wrap"><table><thead><tr><th>Storage</th><th>Type</th><th>Persistence</th><th>Key Facts</th></tr></thead><tbody>
  <tr><td>EBS gp3</td><td>Block</td><td>Persistent</td><td>Default SSD; 3,000 IOPS baseline; 16,000 max IOPS</td></tr>
  <tr><td>EBS io2</td><td>Block</td><td>Persistent</td><td>High IOPS; 64,000 IOPS; Multi-Attach capable</td></tr>
  <tr><td>EBS st1</td><td>Block</td><td>Persistent</td><td>Throughput HDD; big data, log processing</td></tr>
  <tr><td>Instance Store</td><td>Block</td><td>Ephemeral</td><td>Physically attached; lost on stop; very high IOPS</td></tr>
  <tr><td>EFS</td><td>File (NFS)</td><td>Persistent</td><td>Shared across many EC2; auto-scales; Linux only</td></tr>
</tbody></table></div></section>

<section id="s3"><h2>S3 Deep Dive</h2>
<h3>Storage Classes</h3>
<div class="table-wrap"><table><thead><tr><th>Class</th><th>Availability</th><th>Retrieval</th><th>Use Case</th></tr></thead><tbody>
  <tr><td>S3 Standard</td><td>99.99%</td><td>Instant</td><td>Frequently accessed data</td></tr>
  <tr><td>S3 Intelligent-Tiering</td><td>99.9%</td><td>Instant</td><td>Unknown access patterns</td></tr>
  <tr><td>S3 Standard-IA</td><td>99.9%</td><td>Instant</td><td>Infrequent, rapid retrieval</td></tr>
  <tr><td>S3 One Zone-IA</td><td>99.5%</td><td>Instant</td><td>Reproducible infrequent data</td></tr>
  <tr><td>S3 Glacier Instant</td><td>99.9%</td><td>Milliseconds</td><td>Archive, instant retrieval</td></tr>
  <tr><td>S3 Glacier Flexible</td><td>99.99%</td><td>1-12 hours</td><td>Archive, flexible retrieval</td></tr>
  <tr><td>S3 Glacier Deep Archive</td><td>99.99%</td><td>12-48 hours</td><td>Compliance archive, cheapest</td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; S3 Key Facts to Memorize</div><ul>
  <li>Max object size: <strong>5 TB</strong> (multipart upload required for &gt;5 GB)</li>
  <li>Durability: <strong>11 9s</strong> (99.999999999%)</li>
  <li>S3 is <strong>region-scoped</strong>, bucket names are <strong>globally unique</strong></li>
  <li>Enable versioning to protect against accidental deletes</li>
  <li>S3 Transfer Acceleration uses CloudFront edges to speed up uploads</li>
</ul></div></section>

<section id="vpc"><h2>VPC &amp; Networking</h2>
<div class="table-wrap"><table><thead><tr><th>Component</th><th>Function</th><th>Key Details</th></tr></thead><tbody>
  <tr><td>VPC</td><td>Isolated virtual network</td><td>Region-scoped; CIDR /16 to /28</td></tr>
  <tr><td>Public Subnet</td><td>Has route to IGW</td><td>Resources can have public IPs</td></tr>
  <tr><td>Private Subnet</td><td>No IGW route</td><td>Use NAT Gateway for outbound internet</td></tr>
  <tr><td>Internet Gateway</td><td>Public subnet &harr; internet</td><td>Highly available; attach one per VPC</td></tr>
  <tr><td>NAT Gateway</td><td>Private subnet &rarr; internet</td><td>Managed, per-AZ; needs Elastic IP</td></tr>
  <tr><td>Security Group</td><td>Stateful firewall (instance)</td><td>Allow only; return traffic auto-allowed</td></tr>
  <tr><td>NACL</td><td>Stateless firewall (subnet)</td><td>Allow &amp; Deny; numbered rules</td></tr>
  <tr><td>VPC Peering</td><td>Connect two VPCs</td><td>No transitive routing</td></tr>
  <tr><td>Transit Gateway</td><td>Hub-and-spoke for VPCs</td><td>Transitive routing; scales to thousands</td></tr>
  <tr><td>VPC Endpoint (Gateway)</td><td>Private S3/DynamoDB access</td><td>No NAT needed; free</td></tr>
  <tr><td>VPC Endpoint (Interface)</td><td>Private access to 150+ services</td><td>PrivateLink; costs money</td></tr>
</tbody></table></div></section>

<section id="ha"><h2>High Availability &amp; Resilient Design</h2>
<h3>Load Balancers</h3>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>Layer</th><th>Protocols</th><th>Features</th></tr></thead><tbody>
  <tr><td>ALB</td><td>7</td><td>HTTP, HTTPS, gRPC</td><td>Path/host-based routing, Lambda targets, WAF</td></tr>
  <tr><td>NLB</td><td>4</td><td>TCP, UDP, TLS</td><td>Static IP, ultra-low latency, PrivateLink</td></tr>
  <tr><td>GLB</td><td>3</td><td>All IP</td><td>Inline inspection; route through firewalls/IDS</td></tr>
</tbody></table></div>
<h3>RDS Multi-AZ vs Read Replicas</h3>
<div class="grid-2">
  <div class="card"><h4>Multi-AZ (HA)</h4><ul><li>Synchronous replication to standby</li><li>Automatic failover (~1-2 min)</li><li>Same Region only</li><li>Standby is NOT readable</li><li>For: disaster recovery</li></ul></div>
  <div class="card"><h4>Read Replicas (Performance)</h4><ul><li>Asynchronous replication</li><li>Up to 15 replicas (Aurora), 5 (RDS)</li><li>Cross-Region possible</li><li>Replicas ARE readable</li><li>For: read-heavy workloads</li></ul></div>
</div></section>

<section id="serverless"><h2>Serverless Architecture</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Purpose</th><th>Key Limits</th></tr></thead><tbody>
  <tr><td>Lambda</td><td>Event-driven functions</td><td>15 min timeout, 10 GB memory, 1000 concurrent</td></tr>
  <tr><td>API Gateway</td><td>HTTP API front door</td><td>29s timeout (REST), 10MB payload</td></tr>
  <tr><td>DynamoDB</td><td>NoSQL database</td><td>400KB max item; unlimited storage</td></tr>
  <tr><td>S3</td><td>Object storage</td><td>5TB max object; unlimited buckets</td></tr>
  <tr><td>SQS</td><td>Message queue</td><td>256KB max message; 14-day retention</td></tr>
  <tr><td>SNS</td><td>Pub/Sub notifications</td><td>256KB message; 10M subscribers per topic</td></tr>
  <tr><td>EventBridge</td><td>Event bus</td><td>Schedule or pattern-based routing to 20+ targets</td></tr>
  <tr><td>Step Functions</td><td>Workflow orchestration</td><td>Visual workflow; Lambda chaining; error handling</td></tr>
</tbody></table></div></section>

<section id="security"><h2>Security Services</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>What It Does</th><th>Think of It As</th></tr></thead><tbody>
  <tr><td>KMS</td><td>Key Management Service - encryption keys</td><td>Encryption key vault</td></tr>
  <tr><td>Secrets Manager</td><td>Store/rotate secrets, DB passwords, API keys</td><td>Password manager for apps (auto-rotation)</td></tr>
  <tr><td>ACM</td><td>SSL/TLS certificate management</td><td>Free HTTPS certificates</td></tr>
  <tr><td>WAF</td><td>Block SQLi, XSS, rate limiting at Layer 7</td><td>Web application firewall</td></tr>
  <tr><td>Shield</td><td>DDoS protection (Standard=free, Advanced=paid)</td><td>DDoS protection</td></tr>
  <tr><td>GuardDuty</td><td>Threat detection - analyzes VPC/DNS/CloudTrail logs</td><td>Automated threat detective</td></tr>
  <tr><td>Inspector</td><td>Vulnerability scanning for EC2/ECR/Lambda</td><td>Security scanner</td></tr>
  <tr><td>Macie</td><td>Discover sensitive data (PII) in S3</td><td>S3 data privacy guard</td></tr>
</tbody></table></div></section>
""" + chk(["Design a multi-tier web app (VPC, ALB, EC2/ASG, RDS Multi-AZ)","Explain S3 storage classes and when to use each","Understand EBS volume types (gp3, io2, st1, sc1)","Design a highly available RDS setup (Multi-AZ + Read Replicas)","Explain VPC: IGW, NAT Gateway, Route Tables, SGs, NACLs","Know VPC Peering vs Transit Gateway vs PrivateLink","Design a serverless architecture (API Gateway + Lambda + DynamoDB)","Explain S3 security: bucket policies, pre-signed URLs, MFA Delete","Know CloudFront origins, behaviors, and cache invalidation","Explain SQS standard vs FIFO queues","Know SNS fan-out pattern with SQS","Understand KMS CMK types (AWS-managed vs customer-managed)","Explain ALB vs NLB differences and use cases","Know Auto Scaling policies and cooldown periods","Understand CloudWatch Metrics, Alarms, and Logs","Explain Route 53 routing policies: Weighted, Failover, Latency, Geolocation","Know Aurora vs RDS differences (5x MySQL speed, 15 replicas)","Understand ElastiCache Redis vs Memcached","Know IAM roles for cross-account access","Explain AWS Organizations SCPs and account structure"],"dva-c02.html","Developer Associate (DVA-C02)")) + FOOT
write(f"{DOCS}/saa-c03.html", saa)


# ── DVA-C02, SOA-C02, SAP-C02, DOP-C02, SCS-C02, ANS-C01, MLS-C01, DAS-C01 ─
# (concise but complete pages for each)

def cert_page(code, level_cls, level_txt, icon, title, desc, badges, exam_args, toc, body_html, checklist_items, next_file, next_label, extra_badge="", notice=""):
    # extra_badge: optional status badge shown next to the level badge (e.g. RETIRED / Updating)
    # notice: optional banner card (retirement / new-version notice) shown right after the page header
    header = phdr(level_cls, level_txt, icon, f"{code} - {title}", desc, badges, extra_badge)
    cta = quiz_cta(code)
    return (HEAD(f"{code} - {title}", desc) + crumb(code) + header + notice + cta
            + wrap(toc, exam(*exam_args) + body_html + chk(checklist_items, next_file, next_label)) + FOOT)

# ── Status badges & notice banners (keep build output in sync with published site) ──
RETIRED_BADGE = lambda txt: f'<span class="badge" style="background:#6b1010;color:#ffb3b3;border:1px solid #a33">&#9940; RETIRED - {txt}</span>'
UPDATING_BADGE = lambda txt: f'<span class="badge" style="background:#5a4a00;color:#ffe08a;border:1px solid #b89100">&#9888;&#65039; Updating - {txt}</span>'

def retired_notice(name_html, replacement_html):
    return ('\n<div class="container" style="padding-top:1.5rem"><div class="card" style="border:1px solid #a33;background:rgba(160,40,40,0.12)">\n'
            '  <h3 style="margin-top:0">&#9940; This certification has been retired</h3>\n'
            f'  <p style="color:var(--text-muted);margin-bottom:0.75rem">{name_html}</p>\n'
            f'  <p style="margin:0"><strong>Replacement:</strong> {replacement_html}</p>\n'
            '</div></div>')

def updating_notice(new_code, body_html):
    return ('<div class="container" style="padding-top:1.5rem"><div class="card" style="border:1px solid #b89100;background:rgba(180,145,0,0.12)">\n'
            f'  <h3 style="margin-top:0">&#9888;&#65039; A new version is coming: {new_code}</h3>\n'
            f'  <p style="color:var(--text-muted);margin:0">{body_html}</p>\n'
            '</div></div>')

# DVA-C02
dva_body = """
<section id="lambda"><h2>Lambda Deep Dive</h2>
<div class="grid-2">
  <div class="card"><h3>Limits</h3><ul><li>Memory: 128 MB – 10,240 MB</li><li>Timeout: max <strong>15 minutes</strong></li><li>Temp storage (/tmp): 512 MB – 10 GB</li><li>Concurrent executions: 1,000 (soft limit)</li><li>Package: 50 MB zipped, 250 MB unzipped</li></ul></div>
  <div class="card"><h3>Invocation Types</h3><ul><li><strong>Synchronous</strong> - wait for result (API Gateway, ALB)</li><li><strong>Asynchronous</strong> - no wait (S3, SNS, EventBridge); retries 2x; DLQ</li><li><strong>Poll-based</strong> - Lambda polls (SQS, Kinesis, DynamoDB Streams)</li></ul></div>
</div>
<h3>Lambda Features</h3>
<ul><li><strong>Versions</strong> - immutable snapshots of code + config</li><li><strong>Aliases</strong> - named pointers to versions (PROD, DEV)</li><li><strong>Canary / Linear deployments</strong> - gradual traffic shifts with CodeDeploy</li><li><strong>Layers</strong> - reusable dependencies shared across functions</li><li><strong>Container Images</strong> - up to 10 GB; use Lambda base images</li></ul></section>

<section id="dynamodb"><h2>DynamoDB for Developers</h2>
<div class="table-wrap"><table><thead><tr><th>Concept</th><th>Description</th></tr></thead><tbody>
  <tr><td>Primary Key</td><td>Partition Key only (simple) OR Partition Key + Sort Key (composite)</td></tr>
  <tr><td>GSI</td><td>Global Secondary Index - different partition key; eventual consistency</td></tr>
  <tr><td>LSI</td><td>Local Secondary Index - same partition key, different sort key; must be at creation</td></tr>
  <tr><td>Read Consistency</td><td>Eventually Consistent (default, cheaper) vs Strongly Consistent</td></tr>
  <tr><td>DynamoDB Streams</td><td>Ordered record of item changes; trigger Lambda</td></tr>
  <tr><td>TTL</td><td>Auto-delete items after expiry timestamp (free)</td></tr>
  <tr><td>DAX</td><td>In-memory cache; microsecond read latency; write-through</td></tr>
  <tr><td>Transactions</td><td>ACID transactions across multiple items/tables</td></tr>
</tbody></table></div></section>

<section id="cicd"><h2>CI/CD on AWS</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Purpose</th><th>Like</th></tr></thead><tbody>
  <tr><td>CodeCommit</td><td>Private Git repositories</td><td>GitHub/GitLab</td></tr>
  <tr><td>CodeBuild</td><td>Build &amp; test (compile, run tests, create artifacts)</td><td>Jenkins, GitHub Actions</td></tr>
  <tr><td>CodeDeploy</td><td>Deploy to EC2, Lambda, ECS, on-premises</td><td>Spinnaker</td></tr>
  <tr><td>CodePipeline</td><td>Orchestrate full CI/CD pipeline</td><td>GitLab CI</td></tr>
  <tr><td>CodeArtifact</td><td>Artifact repository (npm, Maven, PyPI)</td><td>Nexus</td></tr>
</tbody></table></div>
<h3>CodeDeploy Deployment Strategies</h3>
<div class="table-wrap"><table><thead><tr><th>Strategy</th><th>Behavior</th></tr></thead><tbody>
  <tr><td>In-Place (EC2)</td><td>Deploy to existing instances; brief downtime per instance</td></tr>
  <tr><td>Blue/Green (EC2)</td><td>New instances; shift traffic via LB; zero downtime</td></tr>
  <tr><td>All-at-once (Lambda)</td><td>Immediate 100% shift</td></tr>
  <tr><td>Canary (Lambda/ECS)</td><td>X% traffic for N minutes, then 100%</td></tr>
  <tr><td>Linear (Lambda/ECS)</td><td>Gradual shift X% every N minutes</td></tr>
</tbody></table></div></section>

<section id="api-gw"><h2>API Gateway</h2>
<ul>
  <li><strong>REST API</strong> - full features, 29s timeout, edge-optimized or regional</li>
  <li><strong>HTTP API</strong> - simpler, 70% cheaper than REST API</li>
  <li><strong>WebSocket API</strong> - bidirectional; real-time apps, chat, gaming</li>
  <li><strong>CORS</strong> - must be enabled for browser cross-origin calls</li>
  <li><strong>Stages</strong> - dev, staging, prod; each can have throttling/canary settings</li>
  <li><strong>Usage Plans &amp; API Keys</strong> - throttle and monetize APIs</li>
  <li><strong>Caching</strong> - reduce backend calls; TTL 0-3600s</li>
</ul></section>

<section id="xray"><h2>Monitoring &amp; X-Ray</h2>
<div class="grid-2">
  <div class="card"><h3>CloudWatch</h3><ul><li>Metrics - every service sends metrics (CPU, requests, errors)</li><li>Alarms - trigger SNS/ASG when threshold breached</li><li>Logs - Lambda writes here automatically</li><li>Log Insights - SQL-like query language for logs</li></ul></div>
  <div class="card"><h3>X-Ray</h3><ul><li>Distributed tracing for microservices &amp; Lambda</li><li>Service Map - visual of all components</li><li>Requires: X-Ray SDK + X-Ray Daemon (EC2) or active tracing (Lambda)</li><li>Annotations (indexed) vs Metadata (not indexed)</li><li>Sampling rules - control % of requests to trace</li></ul></div>
</div></section>"""
dva = cert_page("DVA-C02","badge-blue","Associate","&#128187;","AWS Certified Developer Associate","Develop, deploy, and debug cloud-based apps on AWS. Lambda, DynamoDB, API Gateway, CI/CD, X-Ray.",'<span class="badge badge-green">130 min | 65 questions</span><span class="badge badge-blue">Passing: 720/1000</span>',("Developing on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/764/developing-on-aws","https://d1.awsstatic.com/training-and-certification/docs-dev-associate/AWS-Certified-Developer-Associate_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-dev-associate/AWS-Certified-Developer-Associate_Sample-Questions.pdf","130 minutes","65","720",[("Development with AWS Services","32"),("Security","26"),("Deployment","24"),("Troubleshooting &amp; Optimization","18")]),
[("overview","Exam Overview"),("lambda","Lambda Deep Dive"),("dynamodb","DynamoDB"),("cicd","CI/CD"),("api-gw","API Gateway"),("xray","Monitoring &amp; X-Ray"),("checklist","Checklist")],
dva_body,["Configure AWS CLI with profiles","Know SDK credential resolution order","Understand Lambda invocation types (sync, async, poll)","Know Lambda limits: 15 min, 10 GB memory, 250 MB package","Explain Lambda versions, aliases, canary deployments","Know DynamoDB primary keys, GSI vs LSI","Understand DynamoDB capacity modes (provisioned vs on-demand)","Explain DAX, Streams, TTL, Transactions","Know CodeCommit, CodeBuild, CodeDeploy, CodePipeline","Explain blue/green, canary, linear deployment strategies","Configure API Gateway REST vs HTTP API","Enable CORS in API Gateway","Use CloudWatch Logs, Metrics, and Alarms","Implement distributed tracing with X-Ray","Use SSM Parameter Store vs Secrets Manager","Understand SQS visibility timeout and DLQs","Know Kinesis Data Streams shards and partition keys","Use Elastic Beanstalk deployment policies","Understand Cognito User Pools vs Identity Pools","Know S3 pre-signed URLs for temporary access"],"soa-c02.html","SysOps Administrator (SOA-C02)",
extra_badge=UPDATING_BADGE("last day for DVA-C02: Nov 30, 2026"),
notice=updating_notice("DVA-C03","AWS is updating this exam. Registration for <strong>DVA-C03</strong> opens <strong>Oct 27, 2026</strong>, with GA delivery on <strong>Dec 1, 2026</strong>. The last day to take the current <strong>DVA-C02</strong> is <strong>Nov 30, 2026</strong>. DVA-C03 adds AI-assisted development, AI security (Amazon Bedrock, Bedrock AgentCore, Amazon Q, Kiro), and container management (ECR/ECS/EKS/Fargate). This guide covers DVA-C02; content still broadly applies."))
write(f"{DOCS}/dva-c02.html", dva)


# SOA-C02
soa_body = """
<section id="cloudwatch"><h2>CloudWatch Deep Dive</h2>
<div class="table-wrap"><table><thead><tr><th>Feature</th><th>Description</th><th>Key Details</th></tr></thead><tbody>
  <tr><td>Metrics</td><td>Numerical data over time</td><td>Default 1-min resolution; custom up to 1-second; retained 15 months</td></tr>
  <tr><td>Alarms</td><td>Act on metric thresholds</td><td>States: OK, ALARM, INSUFFICIENT_DATA; notify SNS, trigger ASG</td></tr>
  <tr><td>Logs</td><td>Centralized log storage</td><td>Log Groups &rarr; Streams; retention 1 day to indefinite</td></tr>
  <tr><td>Log Insights</td><td>Query logs with SQL-like syntax</td><td>Query across multiple log groups</td></tr>
  <tr><td>CloudWatch Agent</td><td>Collect OS-level metrics</td><td>Memory, disk usage (NOT default EC2 metrics)</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; Memory &amp; Disk are NOT default EC2 metrics!</div><p>CPU, Network, and EBS metrics ARE default. To get <strong>memory usage</strong> and <strong>disk space</strong>, install the CloudWatch Agent on the EC2 instance.</p></div></section>

<section id="ssm"><h2>AWS Systems Manager (SSM)</h2>
<div class="table-wrap"><table><thead><tr><th>Feature</th><th>What It Does</th><th>Use Case</th></tr></thead><tbody>
  <tr><td>Session Manager</td><td>Browser-based SSH/RDP without port 22/3389</td><td>Secure shell access; audit trail in CloudTrail</td></tr>
  <tr><td>Run Command</td><td>Run scripts on many EC2 at once without SSH</td><td>Patch, configure, update many instances</td></tr>
  <tr><td>Patch Manager</td><td>Automated OS patching</td><td>Schedule patching windows; compliance reporting</td></tr>
  <tr><td>Parameter Store</td><td>Store config and secrets (strings, SecureString)</td><td>App config, non-critical secrets</td></tr>
  <tr><td>Inventory</td><td>Collect software/hardware inventory</td><td>Compliance, auditing</td></tr>
</tbody></table></div></section>

<section id="dr"><h2>Backup &amp; Disaster Recovery</h2>
<h3>Recovery Strategies (Cost vs RTO)</h3>
<div class="table-wrap"><table><thead><tr><th>Strategy</th><th>RTO</th><th>RPO</th><th>Cost</th><th>Description</th></tr></thead><tbody>
  <tr><td>Backup &amp; Restore</td><td>Hours</td><td>Hours</td><td>$</td><td>Cheapest. Backup to S3/Glacier; restore on disaster.</td></tr>
  <tr><td>Pilot Light</td><td>Minutes-Hours</td><td>Minutes</td><td>$$</td><td>Core systems in AWS; scale up on disaster.</td></tr>
  <tr><td>Warm Standby</td><td>Minutes</td><td>Seconds-Minutes</td><td>$$$</td><td>Scaled-down version of prod running; scale up fast.</td></tr>
  <tr><td>Multi-Site Active/Active</td><td>Real-time</td><td>~0</td><td>$$$$</td><td>Full duplicate; DNS routes to both. Zero downtime.</td></tr>
</tbody></table></div></section>

<section id="cfn"><h2>CloudFormation</h2>
<div class="table-wrap"><table><thead><tr><th>Section</th><th>Purpose</th><th>Required?</th></tr></thead><tbody>
  <tr><td>AWSTemplateFormatVersion</td><td>Always "2010-09-09"</td><td>No</td></tr>
  <tr><td>Parameters</td><td>Input values at deploy time</td><td>No</td></tr>
  <tr><td>Mappings</td><td>Static key-value lookup (e.g., AMI by region)</td><td>No</td></tr>
  <tr><td>Conditions</td><td>Create resources conditionally</td><td>No</td></tr>
  <tr><td><strong>Resources</strong></td><td>AWS resources to create</td><td><strong>YES</strong></td></tr>
  <tr><td>Outputs</td><td>Values to export or display</td><td>No</td></tr>
</tbody></table></div>
<ul><li><strong>StackSets</strong> - deploy stacks to multiple accounts/regions</li><li><strong>Nested Stacks</strong> - reusable stacks as components</li><li><strong>Change Sets</strong> - preview changes before applying</li><li><strong>Drift Detection</strong> - find resources changed outside CloudFormation</li></ul></section>"""
soa = cert_page("SOA-C02","badge-blue","Associate","&#9881;","AWS Certified SysOps Administrator Associate","Deploy, manage, and operate workloads on AWS at scale. Monitoring, automation, reliability, compliance.",'<span class="badge badge-green">180 min | 65 questions + exam lab</span><span class="badge badge-blue">Passing: 720/1000</span>',("AWS SysOps Admin","https://explore.skillbuilder.aws/learn/course/external/view/elearning/1573/aws-certified-sysops-administrator-associate-official-practice-question-set-soa-c02-english","https://d1.awsstatic.com/training-and-certification/docs-sysops-associate/AWS-Certified-SysOps-Administrator-Associate_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-sysops-associate/AWS-Certified-SysOps-Administrator-Associate_Sample-Questions.pdf","180 minutes","65 + exam lab","720",[("Monitoring, Logging &amp; Remediation","20"),("Reliability &amp; Business Continuity","16"),("Deployment, Provisioning &amp; Automation","18"),("Security &amp; Compliance","16"),("Networking &amp; Content Delivery","18"),("Cost &amp; Performance Optimization","12")]),
[("overview","Exam Overview"),("cloudwatch","CloudWatch Deep Dive"),("ssm","Systems Manager"),("dr","Backup &amp; DR"),("cfn","CloudFormation"),("checklist","Checklist")],
soa_body,["Install CloudWatch Agent for memory/disk metrics","Create CloudWatch Alarms connected to Auto Scaling or SNS","Use SSM Session Manager for SSH without port 22","Use SSM Run Command for mass instance management","Configure SSM Patch Manager with maintenance windows","Know all 4 DR strategies and their RTO/RPO","Configure AWS Backup with cross-region copy","Understand IAM policy evaluation order (deny &gt; allow &gt; implicit deny)","Explain SCPs vs Permission Boundaries vs Resource Policies","Create cross-account IAM roles with sts:AssumeRole","Write a CloudFormation template with Parameters, Resources, Outputs","Use Change Sets and Drift Detection","Understand CloudFormation StackSets","Configure S3 lifecycle policies for cost optimization","Know EC2 Health Check vs ELB Health Check differences","Understand Auto Scaling lifecycle hooks","Use AWS Config for compliance checking","Configure CloudTrail for API audit logging","Know Trusted Advisor check categories","Understand AWS Cost Explorer and Compute Optimizer"],"sap-c02.html","Solutions Architect Professional (SAP-C02)")
write(f"{DOCS}/soa-c02.html", soa)

# SAP-C02
sap_body = """
<section id="prereq"><h2>Prerequisites & Study Tips</h2>
<div class="callout warn"><div class="callout-title">Hardest AWS Exam</div><p>SAP-C02 is widely considered the hardest AWS cert. Questions present complex multi-service architectures with subtle trade-offs. You need deep SAA-level experience.</p></div>
<h3>Recommended Before Attempting</h3><ul>
  <li>Active SAA-C03 + 2+ years real AWS experience</li>
  <li>Adrian Cantrill SAP course or Stephane Maarek SAP course on Udemy</li>
  <li>Complete all Tutorials Dojo SAP practice exams (target 75%+ before booking)</li>
</ul></section>

<section id="orgs"><h2>AWS Organizations & Multi-Account</h2>
<ul><li><strong>SCPs</strong> - org-level guardrails; restrict max permissions; never grant permissions</li>
<li><strong>OUs</strong> - group accounts hierarchically; SCPs inherit down the tree</li>
<li><strong>Control Tower</strong> - sets up governed multi-account landing zones; uses SCPs + Config Rules</li>
<li><strong>RAM (Resource Access Manager)</strong> - share subnets, TGWs, Route 53 rules across accounts without VPC Peering</li>
<li><strong>Delegated Admin</strong> - member account manages a service (e.g., GuardDuty) for the org</li></ul>
<h3>Identity Federation</h3>
<div class="table-wrap"><table><thead><tr><th>Pattern</th><th>When to Use</th></tr></thead><tbody>
  <tr><td>IAM Identity Center (SSO)</td><td>Internal employees, multiple AWS accounts; SAML 2.0 with corporate IdP</td></tr>
  <tr><td>Web Identity Federation</td><td>Mobile/web app users (millions); Cognito → AWS STS tokens</td></tr>
  <tr><td>SAML 2.0 Federation</td><td>Enterprise with existing IdP; STS AssumeRoleWithSAML</td></tr>
</tbody></table></div></section>

<section id="advanced-net"><h2>Advanced Networking</h2>
<h3>Transit Gateway (TGW)</h3>
<ul><li>Regional hub; connect VPCs and on-premises at scale</li>
<li>Transitive routing - VPC A → TGW → VPC B (unlike VPC Peering)</li>
<li>TGW Route Tables - isolate VPC groups (prod vs dev)</li>
<li>Inter-Region Peering - connect TGWs across regions</li></ul>
<h3>Direct Connect</h3>
<ul><li>Dedicated Connection: 1/10/100 Gbps - physical port at DX location</li>
<li>Hosted Connection: 50 Mbps – 10 Gbps via DX partner</li>
<li>VIF Types: Private VIF (VPC), Public VIF (AWS public services), Transit VIF (TGW)</li>
<li>DX Gateway: Connect one DX to multiple VPCs across regions</li>
<li>Resilience: 2 DX locations + Site-to-Site VPN backup for critical workloads</li></ul></section>

<section id="migration"><h2>Migration Strategies (7 Rs)</h2>
<div class="table-wrap"><table><thead><tr><th>Strategy</th><th>Description</th><th>Effort</th></tr></thead><tbody>
  <tr><td>Retire</td><td>Decommission - app no longer needed</td><td>None</td></tr>
  <tr><td>Retain</td><td>Keep on-premises for now</td><td>None</td></tr>
  <tr><td>Rehost (Lift &amp; Shift)</td><td>Move to EC2 with no changes</td><td>Low</td></tr>
  <tr><td>Replatform (Lift &amp; Reshape)</td><td>Minor optimizations (move DB to RDS)</td><td>Low-Medium</td></tr>
  <tr><td>Repurchase (Drop &amp; Shop)</td><td>Move to SaaS (Salesforce, ServiceNow)</td><td>Medium</td></tr>
  <tr><td>Refactor / Re-architect</td><td>Rebuild for cloud-native (microservices)</td><td>High</td></tr>
  <tr><td>Relocate</td><td>Move VMware VMs to VMware Cloud on AWS</td><td>Low</td></tr>
</tbody></table></div>
<h3>Migration Tools</h3>
<div class="table-wrap"><table><thead><tr><th>Tool</th><th>Use For</th></tr></thead><tbody>
  <tr><td>Application Migration Service (MGN)</td><td>Continuous replication; cutover with minimal downtime</td></tr>
  <tr><td>Database Migration Service (DMS)</td><td>Migrate databases; supports heterogeneous (Oracle → Aurora)</td></tr>
  <tr><td>DataSync</td><td>Migrate/sync NFS/SMB data to S3/EFS/FSx</td></tr>
  <tr><td>Snowball / Snowmobile</td><td>Physical data transfer for large datasets (TB – EB)</td></tr>
</tbody></table></div></section>

<section id="cost"><h2>Cost Optimization</h2>
<ul><li><strong>Compute Optimizer</strong> - ML-based right-sizing for EC2, EBS, Lambda, ECS</li>
<li><strong>Cost Allocation Tags</strong> - see cost breakdown per team/project</li>
<li><strong>S3 Lifecycle</strong> - auto-move to cheaper storage classes</li>
<li><strong>Spot for fault-tolerant workloads</strong> - up to 90% savings</li>
<li><strong>Reserved Instances for steady-state</strong> - up to 72% savings</li>
<li><strong>Savings Plans</strong> - Compute (most flexible), EC2 Instance (most discount)</li></ul></section>"""
sap = cert_page("SAP-C02","badge-purple","Professional","&#129504;","AWS Certified Solutions Architect Professional","Advanced multi-account architectures, migration planning, cost optimization, complex hybrid designs.",'<span class="badge badge-green">180 min | 75 questions</span><span class="badge badge-purple">Passing: 750/1000</span><span class="badge badge-red">Hardest AWS exam</span>',("AWS Advanced Architecting","https://explore.skillbuilder.aws/learn/course/external/view/elearning/1313/aws-certified-solutions-architect-professional-official-practice-question-set-sap-c02-english","https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf","180 minutes","75","750",[("Design for Org Complexity","26"),("Design for New Solutions","29"),("Migration Planning","15"),("Cost Control","20"),("Continuous Improvement","10")]),
[("overview","Exam Overview"),("prereq","Prerequisites"),("orgs","Organizations & Multi-Account"),("advanced-net","Advanced Networking"),("migration","Migration (7 Rs)"),("cost","Cost Optimization"),("checklist","Checklist")],
sap_body,["Explain AWS Organizations: OUs, SCPs, delegated admin, Control Tower","Know all identity federation patterns and when to use each","Understand RAM - what can be shared and how","Design Transit Gateway with route table isolation","Know Direct Connect: connection types, VIFs, DX Gateway","Design Route 53 hybrid DNS with Resolver Endpoints","Know the 7 Rs of migration and when to use each","Understand Application Migration Service (MGN) vs DMS vs DataSync","Design cost-optimized architectures with Savings Plans and Spot","Use Compute Optimizer for right-sizing","Design event-driven patterns: fan-out, CQRS, Saga, Strangler Fig","Understand Step Functions Standard vs Express workflows","Design multi-region active-active architectures","Understand Global Accelerator vs CloudFront use cases","Design disaster recovery: pilot light, warm standby, active-active","Know Kinesis Data Streams vs Firehose vs MSK","Understand AWS Service Catalog for governed self-service","Know Lake Formation for data lake governance","Design EKS/ECS advanced deployment patterns","Understand Outposts and Local Zones for edge scenarios"],"dop-c02.html","DevOps Engineer Professional (DOP-C02)",
extra_badge=UPDATING_BADGE("last day for SAP-C02: Nov 16, 2026"),
notice=updating_notice("SAP-C03","AWS is updating this exam. Registration for <strong>SAP-C03</strong> opens <strong>Oct 27, 2026</strong>, with GA delivery on <strong>Nov 17, 2026</strong>. The last day to take the current <strong>SAP-C02</strong> is <strong>Nov 16, 2026</strong>. SAP-C03 adds GenAI/agentic AI architectures (Amazon Bedrock, Bedrock AgentCore, RAG, Guardrails), resilience engineering (FIS, Resilience Hub, ARC), cloud-native patterns, DevSecOps, data lakehouse, and post-quantum cryptography. This guide covers SAP-C02; core architecture content still applies."))
write(f"{DOCS}/sap-c02.html", sap)

# DOP-C02
dop_body = """
<section id="cicd-pro"><h2>Advanced CI/CD</h2>
<h3>CodePipeline Advanced Patterns</h3>
<ul><li><strong>Manual Approval</strong> - pause pipeline; require human sign-off before prod deploy</li>
<li><strong>Cross-Account Pipeline</strong> - deploy from one account's pipeline to another account's environment</li>
<li><strong>Multi-Region Deploy</strong> - parallel deploy to multiple regions simultaneously</li></ul>
<h3>CodeBuild buildspec.yml</h3>
<pre><code>version: 0.2
env:
  parameter-store:
    DB_PASSWORD: /myapp/db-password
  secrets-manager:
    API_KEY: myapp/api-key:apiKey
phases:
  install:
    commands: [pip install -r requirements.txt]
  build:
    commands:
      - docker build -t myapp .
      - docker push $ECR_URI:latest
reports:
  pytest-reports:
    files: [reports/junit.xml]
    file-format: JUNITXML</code></pre></section>

<section id="iac-pro"><h2>Infrastructure as Code at Scale</h2>
<h3>CloudFormation Advanced</h3>
<ul><li><strong>StackSets</strong> - deploy to multiple accounts/regions from management account</li>
<li><strong>Nested Stacks</strong> - reusable stack modules</li>
<li><strong>Custom Resources</strong> - extend CFN with Lambda for anything not natively supported</li>
<li><strong>Hooks</strong> - pre/post-provision validation via Lambda</li>
<li><strong>Drift Detection</strong> - compare stack's actual state to expected template state</li></ul>
<h3>AWS CDK</h3>
<pre><code>from aws_cdk import Stack, aws_s3 as s3, aws_lambda as lambda_
class MyStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        bucket = s3.Bucket(self, "MyBucket", versioned=True)
        fn = lambda_.Function(self, "MyFn",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda"))
        bucket.grant_read(fn)</code></pre></section>

<section id="containers-devops"><h2>Containers at Scale</h2>
<div class="table-wrap"><table><thead><tr><th>Factor</th><th>ECS</th><th>EKS</th></tr></thead><tbody>
  <tr><td>Learning curve</td><td>Low - AWS native</td><td>High - Kubernetes expertise needed</td></tr>
  <tr><td>Control plane</td><td>Managed by AWS (free)</td><td>Managed by AWS ($0.10/hr)</td></tr>
  <tr><td>Portability</td><td>AWS-only</td><td>Run anywhere Kubernetes runs</td></tr>
  <tr><td>Fargate support</td><td>Excellent</td><td>Supported (EKS Fargate profiles)</td></tr>
</tbody></table></div></section>

<section id="monitoring-pro"><h2>Monitoring & Observability at Scale</h2>
<h3>Centralized Logging</h3>
<pre><code>Account A → CloudWatch Logs → Kinesis Firehose → S3 (Log Archive Account)
Account B → CloudWatch Logs → Kinesis Firehose ↗
Account C → CloudWatch Logs → Kinesis Firehose ↗
                                      ↓
                          OpenSearch (search/visualize)
                          Athena (SQL queries)</code></pre>
<h3>AWS Config for Continuous Compliance</h3>
<ul><li><strong>Config Rules</strong> - evaluate resource configs (managed or custom Lambda)</li>
<li><strong>Conformance Packs</strong> - bundle of rules for compliance standards (PCI-DSS, HIPAA)</li>
<li><strong>Remediation</strong> - auto-fix non-compliant resources via SSM Automation</li>
<li><strong>Aggregator</strong> - centralize Config data from all accounts/regions</li></ul></section>"""
dop = cert_page("DOP-C02","badge-purple","Professional","&#128260;","AWS Certified DevOps Engineer Professional","CI/CD automation, IaC, containers, monitoring, compliance, and incident response at professional level.",'<span class="badge badge-green">180 min | 75 questions</span><span class="badge badge-purple">Passing: 750/1000</span>',("DevOps Engineering on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/16408/aws-certified-devops-engineer-professional-official-practice-question-set-dop-c02-english","https://d1.awsstatic.com/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Sample-Questions.pdf","180 minutes","75","750",[("SDLC Automation","22"),("Configuration Management & IaC","17"),("Resilient Cloud Solutions","15"),("Monitoring & Logging","15"),("Incident & Event Response","14"),("Security & Compliance","17")]),
[("overview","Exam Overview"),("cicd-pro","Advanced CI/CD"),("iac-pro","IaC at Scale"),("containers-devops","Containers"),("monitoring-pro","Monitoring & Observability"),("checklist","Checklist")],
dop_body,["Build CodePipeline with manual approval and cross-account deploy","Write advanced buildspec.yml with Parameter Store and Secrets Manager","Design blue/green ECS deployment with CodeDeploy","Use CloudFormation StackSets for multi-account deployments","Write CDK code to define AWS infrastructure","Know Terraform state management with S3 + DynamoDB locking","Decide between ECS and EKS for containerized workloads","Design centralized logging with Kinesis Firehose","Configure X-Ray sampling rules and trace groups","Use AWS Config Conformance Packs for compliance","Build EventBridge auto-remediation rules","Configure OpsCenter and Incident Manager","Know CloudWatch Contributor Insights and Synthetics Canaries","Implement canary deployments with Lambda aliases and CodeDeploy","Design zero-downtime deployments with ALB weighted target groups","Understand chaos engineering with Fault Injection Simulator","Use Service Catalog for governed self-service infrastructure","Design GitOps workflows with CodePipeline + CodeCommit","Know service quotas and how to request increases","Use Systems Manager Automation documents for remediation"],"scs-c02.html","Security Specialty (SCS-C02)")
write(f"{DOCS}/dop-c02.html", dop)

# SCS-C02
scs_body = """
<section id="threat"><h2>Threat Detection Services</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>What It Detects</th><th>Data Sources</th></tr></thead><tbody>
  <tr><td><strong>GuardDuty</strong></td><td>Threats: crypto-mining, credential theft, C2 comms, port scans</td><td>VPC Flow Logs, DNS logs, CloudTrail events</td></tr>
  <tr><td><strong>Security Hub</strong></td><td>Aggregates findings from all security services; compliance scores</td><td>GuardDuty, Inspector, Macie, Config, partners</td></tr>
  <tr><td><strong>Inspector</strong></td><td>Vulnerabilities in EC2 OS, Lambda, ECR images</td><td>SSM Agent, ECR scans, Lambda code</td></tr>
  <tr><td><strong>Macie</strong></td><td>Sensitive data (PII, credit cards) in S3</td><td>S3 object metadata &amp; content</td></tr>
  <tr><td><strong>Detective</strong></td><td>Root cause analysis; investigate security findings</td><td>VPC Flow Logs, CloudTrail, GuardDuty findings</td></tr>
</tbody></table></div></section>

<section id="iam-sec"><h2>IAM & Access Control Deep Dive</h2>
<h3>Policy Types</h3>
<div class="table-wrap"><table><thead><tr><th>Policy Type</th><th>Attached To</th><th>Purpose</th></tr></thead><tbody>
  <tr><td>Identity Policy</td><td>Users, Groups, Roles</td><td>What the identity can do</td></tr>
  <tr><td>Resource Policy</td><td>S3, KMS, SQS, Lambda...</td><td>Who can access the resource</td></tr>
  <tr><td>SCP</td><td>AWS Org OU/Account</td><td>Max permissions guardrail (never grants)</td></tr>
  <tr><td>Permission Boundary</td><td>Users, Roles</td><td>Max permissions an admin can grant</td></tr>
  <tr><td>Session Policy</td><td>AssumeRole calls</td><td>Further restrict a temporary session</td></tr>
</tbody></table></div></section>

<section id="encryption"><h2>Data Encryption</h2>
<h3>KMS Key Types</h3>
<div class="table-wrap"><table><thead><tr><th>Key Type</th><th>Control</th><th>Cost</th></tr></thead><tbody>
  <tr><td>AWS Managed Keys (aws/s3, aws/rds)</td><td>Minimal</td><td>Free</td></tr>
  <tr><td>Customer Managed Keys (CMK)</td><td>Full (key policy, grants, rotation)</td><td>$1/month + API calls</td></tr>
  <tr><td>Customer-Provided (SSE-C)</td><td>Complete (you store key)</td><td>No KMS cost</td></tr>
  <tr><td>CloudHSM</td><td>Dedicated HSM hardware</td><td>High</td></tr>
</tbody></table></div>
<h3>S3 Encryption Options</h3>
<ul><li><strong>SSE-S3</strong> - AWS manages keys; AES-256; default for new buckets</li>
<li><strong>SSE-KMS</strong> - CMK; audit via CloudTrail; possible KMS throttling</li>
<li><strong>SSE-C</strong> - customer provides key per request; HTTPS only</li>
<li><strong>Client-Side</strong> - encrypt before upload; AWS never sees plaintext</li></ul>
<h3>Secrets Manager vs Parameter Store</h3>
<div class="grid-2">
  <div class="card"><h4>Secrets Manager</h4><ul><li>Built-in automatic rotation (Lambda)</li><li>Native RDS/Redshift integration</li><li>$0.40/secret/month</li><li>Cross-account sharing via resource policy</li></ul></div>
  <div class="card"><h4>Parameter Store</h4><ul><li>Standard tier: free; Advanced: $0.05/param/month</li><li>SecureString uses KMS encryption</li><li>Hierarchical naming (/app/db/password)</li><li>No automatic rotation (use Lambda + EventBridge)</li></ul></div>
</div></section>

<section id="netsec"><h2>Network Security</h2>
<ul><li><strong>AWS WAF</strong> - Layer 7; block SQLi, XSS, rate limiting; attach to ALB, CloudFront, API Gateway</li>
<li><strong>AWS Shield Standard</strong> - free; automatic DDoS protection Layer 3/4</li>
<li><strong>AWS Shield Advanced</strong> - $3,000/month; DRT team; cost protection</li>
<li><strong>Firewall Manager</strong> - centrally manage WAF, Shield, Security Groups across org</li>
<li><strong>Network Firewall</strong> - stateful managed firewall in VPC; deep packet inspection; IDS/IPS</li>
<li><strong>VPC Traffic Mirroring</strong> - copy traffic from ENIs to intrusion detection appliances</li></ul></section>"""
scs = cert_page("SCS-C02","badge-red","Specialty","&#128274;","AWS Certified Security Specialty","Threat detection, identity management, data protection, infrastructure security, and compliance governance.",'<span class="badge badge-green">170 min | 65 questions</span><span class="badge badge-red">Passing: 750/1000</span>',("Security Engineering on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/97/security-engineering-on-aws","https://d1.awsstatic.com/training-and-certification/docs-security-spec/AWS-Certified-Security-Specialty_Exam-Guide.pdf","https://d1.awsstatic.com/training-and-certification/docs-security-spec/AWS-Certified-Security-Specialty_Sample-Questions.pdf","170 minutes","65","750",[("Threat Detection & Incident Response","14"),("Security Logging & Monitoring","18"),("Infrastructure Security","20"),("Identity & Access Management","16"),("Data Protection","18"),("Security Governance","14")]),
[("overview","Exam Overview"),("threat","Threat Detection"),("iam-sec","IAM Deep Dive"),("encryption","Data Encryption"),("netsec","Network Security"),("checklist","Checklist")],
scs_body,["Know all threat detection services: GuardDuty, Inspector, Macie, Security Hub, Detective","Explain all IAM policy types and evaluation logic","Configure S3 security: Block Public Access, bucket policies, pre-signed URLs, WORM","Know KMS key types: AWS-managed, CMK, SSE-C, CloudHSM","Explain S3 encryption: SSE-S3, SSE-KMS, SSE-C, client-side","Know when to use Secrets Manager vs Parameter Store","Understand automatic secret rotation with Secrets Manager","Configure WAF rules: SQLi, XSS, rate limiting, IP reputation","Know Shield Standard vs Advanced differences","Understand Firewall Manager centralized policy management","Configure Network Firewall for deep packet inspection","Enable CloudTrail in all regions with log file integrity validation","Configure S3 Access Analyzer and IAM Access Analyzer","Understand KMS key policies and grants for cross-account access","Use Config Conformance Packs for compliance standards","Design incident response playbooks with EventBridge + Lambda","Know ACM: public vs private CAs","Know Cognito User Pools vs Identity Pools security implications","Configure GuardDuty with automated remediation","Understand VPC Traffic Mirroring for intrusion detection"],"ans-c01.html","Advanced Networking Specialty (ANS-C01)")
write(f"{DOCS}/scs-c02.html", scs)

# ANS-C01, MLS-C01, DAS-C01 - concise specialty pages
# Per-cert status extras (badge shown in header + notice banner after header)
CERT_EXTRAS = {
    "MLS-C01": {
        "extra_badge": RETIRED_BADGE("Exam ended Mar 31, 2026"),
        "notice": retired_notice(
            "<strong>AWS Certified Machine Learning - Specialty (MLS-C01)</strong> was retired on <strong>March 31, 2026</strong>. Existing credentials remain valid for 3 years from the date earned, but the exam can no longer be taken.",
            '<a href="mla-c01.html">AWS Certified Machine Learning Engineer - Associate (MLA-C01) &rarr;</a> &nbsp;|&nbsp; See also <a href="aip-c01.html">Generative AI Developer - Professional (AIP-C01)</a>'),
    },
    "DAS-C01": {
        "extra_badge": RETIRED_BADGE("Exam ended Apr 8, 2024"),
        "notice": retired_notice(
            "<strong>AWS Certified Data Analytics - Specialty (DAS-C01)</strong> was retired on <strong>April 9, 2024</strong> (last exam date April 8, 2024). Existing credentials remain valid for 3 years from the date earned, but the exam can no longer be taken.",
            '<a href="dea-c01.html">AWS Certified Data Engineer - Associate (DEA-C01) &rarr;</a>'),
    },
}
for code,lcls,ltxt,icon,title,desc,badges,ea,body_html,chklist,nf,nl in [
  ("ANS-C01","badge-red","Specialty","&#127760;","AWS Certified Advanced Networking Specialty",
   "Complex AWS networking: VPC design, Direct Connect, Transit Gateway, Route 53, CloudFront.",
   '<span class="badge badge-green">170 min | 65 questions</span><span class="badge badge-red">Passing: 750/1000</span>',
   ("Advanced Networking on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/2833/advanced-networking-on-aws",
    "https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS-Certified-Advanced-Networking-Specialty_Exam-Guide.pdf",
    "https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS-Certified-Advanced-Networking-Specialty_Sample-Questions.pdf",
    "170 minutes","65","750",[("Network Design","30"),("Network Implementation","26"),("Network Management & Operations","20"),("Network Security & Governance","24")]),
   """<section id="vpc-adv"><h2>Advanced VPC Design</h2>
<ul><li>Use /16 VPCs - 65,536 IPs; /24 subnets - 251 usable IPs (AWS reserves 5)</li>
<li>Non-overlapping CIDRs across all VPCs required for peering/TGW</li>
<li>Secondary CIDRs - add up to 5 CIDR blocks to a VPC (e.g., EKS pods)</li>
<li>VPC Sharing (RAM) - share subnets from central VPC to multiple accounts</li></ul>
<h3>VPC Endpoints Deep Dive</h3>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>Services</th><th>Cost</th></tr></thead><tbody>
  <tr><td>Gateway Endpoint</td><td>S3, DynamoDB only</td><td>Free</td></tr>
  <tr><td>Interface Endpoint (PrivateLink)</td><td>150+ AWS services</td><td>$0.01/hr + data</td></tr>
  <tr><td>GWLB Endpoint</td><td>Third-party appliances</td><td>$0.01/hr + data</td></tr>
</tbody></table></div></section>
<section id="route53-adv"><h2>Route 53 Routing Policies</h2>
<div class="table-wrap"><table><thead><tr><th>Policy</th><th>Use Case</th><th>Key Detail</th></tr></thead><tbody>
  <tr><td>Simple</td><td>Single resource</td><td>Can return multiple values; client picks</td></tr>
  <tr><td>Weighted</td><td>A/B testing, gradual migration</td><td>Assign weights 0-255; 0 = stop traffic</td></tr>
  <tr><td>Latency</td><td>Route to lowest-latency region</td><td>Based on AWS latency data</td></tr>
  <tr><td>Failover</td><td>Active-passive DR</td><td>Primary/Secondary; health check required</td></tr>
  <tr><td>Geolocation</td><td>Route by user's geography</td><td>Country/continent; default for unmatched</td></tr>
  <tr><td>Geoproximity</td><td>Route by proximity with bias</td><td>Traffic Flow only; bias expands/shrinks regions</td></tr>
  <tr><td>Multi-Value</td><td>Simple load balancing</td><td>Up to 8 records; health checked</td></tr>
  <tr><td>IP-Based</td><td>Route by client CIDR</td><td>Map IP ranges to endpoints</td></tr>
</tbody></table></div></section>
<section id="cf-adv"><h2>CloudFront Advanced</h2>
<ul><li><strong>OAC (Origin Access Control)</strong> - restricts S3 to CloudFront only (replaces OAI)</li>
<li><strong>Lambda@Edge</strong> - all 4 request/response phases; 5-30s timeout; Node.js/Python</li>
<li><strong>CloudFront Functions</strong> - viewer req/res only; sub-millisecond; JavaScript; cheapest</li>
<li><strong>Signed URLs</strong> - single file access; <strong>Signed Cookies</strong> - multiple files (video streaming)</li>
<li><strong>Origin Groups</strong> - primary + failover origin; auto-failover</li></ul></section>""",
   ["Design multi-VPC architectures with non-overlapping CIDRs","Know all 3 VPC Endpoint types and when to use each","Design DX with primary + backup VPN","Understand BGP: AS_PATH prepending, Local Preference, MED","Design TGW with route table segmentation and Appliance Mode","Know all 8 Route 53 routing policies and use cases","Design hybrid DNS with Route 53 Resolver endpoints","Configure CloudFront with OAC, Lambda@Edge, signed URLs","Know Network Firewall stateful vs stateless rule groups","Design IPv6 dual-stack VPCs with Egress-Only IGW","Know VPC Flow Log format and Athena analysis","Design multi-region active-active with Route 53 + health checks","Understand AWS Global Accelerator for TCP/UDP workloads","Know PrivateLink and VPC Endpoint Services","Understand prefix lists for CIDR management","Know ELB cross-zone load balancing behavior","Design AWS Global Network vs public internet routing","Understand BGP communities for DX routing","Configure Transit Gateway Connect with GRE tunnels","Know Direct Connect Gateway for multi-region VPC access"],
   "mls-c01.html","Machine Learning Specialty (MLS-C01)"),

  ("MLS-C01","badge-red","Specialty","&#129302;","AWS Certified Machine Learning Specialty",
   "Design, build, train, and deploy ML solutions. SageMaker deep dive, AI services, MLOps, data engineering.",
   '<span class="badge badge-green">180 min | 65 questions</span><span class="badge badge-red">Passing: 750/1000</span>',
   ("Machine Learning on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/1340/aws-certified-machine-learning-specialty-official-practice-question-set-mls-c01-english",
    "https://d1.awsstatic.com/training-and-certification/docs-ml/AWS-Certified-Machine-Learning-Specialty_Exam-Guide.pdf",
    "https://d1.awsstatic.com/training-and-certification/docs-ml/AWS-Certified-Machine-Learning-Specialty_Sample-Questions.pdf",
    "180 minutes","65","750",[("Data Engineering","24"),("Exploratory Data Analysis","26"),("Modeling","36"),("ML Implementation & Operations","14")]),
   """<section id="ml-services"><h2>AWS ML Services Overview</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Category</th><th>Use Case</th></tr></thead><tbody>
  <tr><td><strong>SageMaker</strong></td><td>Full ML Platform</td><td>Build, train, deploy any ML model end-to-end</td></tr>
  <tr><td><strong>Rekognition</strong></td><td>Vision AI</td><td>Image/video: objects, faces, text, content moderation</td></tr>
  <tr><td><strong>Comprehend</strong></td><td>NLP</td><td>Sentiment, entities, key phrases, language detection</td></tr>
  <tr><td><strong>Textract</strong></td><td>Document AI</td><td>Extract text and data from scanned forms and documents</td></tr>
  <tr><td><strong>Transcribe</strong></td><td>Speech-to-Text</td><td>Automatic speech recognition; call center transcription</td></tr>
  <tr><td><strong>Polly</strong></td><td>Text-to-Speech</td><td>Convert text to lifelike speech; SSML support</td></tr>
  <tr><td><strong>Lex</strong></td><td>Conversational AI</td><td>Chatbots and voice interfaces (same tech as Alexa)</td></tr>
  <tr><td><strong>Forecast</strong></td><td>Time Series</td><td>ML-based demand/inventory forecasting</td></tr>
  <tr><td><strong>Personalize</strong></td><td>Recommendations</td><td>Real-time personalized recommendations</td></tr>
  <tr><td><strong>Bedrock</strong></td><td>Generative AI</td><td>Foundation models via API (Claude, Llama, Titan, Stable Diffusion)</td></tr>
</tbody></table></div></section>
<section id="sagemaker"><h2>SageMaker Deep Dive</h2>
<div class="table-wrap"><table><thead><tr><th>Component</th><th>Purpose</th></tr></thead><tbody>
  <tr><td>Studio</td><td>Web-based IDE for complete ML lifecycle</td></tr>
  <tr><td>Ground Truth</td><td>Data labeling with human reviewers + ML auto-labeling</td></tr>
  <tr><td>Data Wrangler</td><td>Data prep and transformation; 300+ transforms; no-code</td></tr>
  <tr><td>Feature Store</td><td>Centralized features; online (real-time) + offline (batch)</td></tr>
  <tr><td>Training Jobs</td><td>Managed training; spot training for 70% cost savings</td></tr>
  <tr><td>Automatic Model Tuning</td><td>Hyperparameter optimization (Bayesian/random/grid)</td></tr>
  <tr><td>Endpoints (Real-time)</td><td>Low-latency inference; auto-scaling; multi-model endpoints</td></tr>
  <tr><td>Batch Transform</td><td>Offline bulk inference on S3 data</td></tr>
  <tr><td>Pipelines</td><td>MLOps CI/CD for ML workflows</td></tr>
  <tr><td>Clarify</td><td>Detect bias and explain model predictions</td></tr>
  <tr><td>Model Monitor</td><td>Detect data drift and model quality degradation in production</td></tr>
</tbody></table></div>
<h3>Built-in Algorithms</h3>
<div class="table-wrap"><table><thead><tr><th>Algorithm</th><th>Problem Type</th><th>Use Case</th></tr></thead><tbody>
  <tr><td>XGBoost</td><td>Classification/Regression</td><td>Tabular data; most popular for structured data</td></tr>
  <tr><td>Linear Learner</td><td>Classification/Regression</td><td>Large sparse datasets; fast training</td></tr>
  <tr><td>K-Means</td><td>Clustering</td><td>Customer segmentation</td></tr>
  <tr><td>BlazingText</td><td>NLP</td><td>Text classification; word embeddings</td></tr>
  <tr><td>DeepAR</td><td>Time Series Forecasting</td><td>Multiple related time series</td></tr>
  <tr><td>Random Cut Forest</td><td>Anomaly Detection</td><td>Detect anomalies in streaming data</td></tr>
  <tr><td>Image Classification</td><td>Vision</td><td>Classify images (ResNet)</td></tr>
</tbody></table></div></section>""",
   ["Know all AWS AI/ML managed services and their use cases","Understand SageMaker components: Studio, Data Wrangler, Feature Store","Know SageMaker built-in algorithms and when to use each","Explain SageMaker training: CPU vs GPU instance types","Know SageMaker Spot Training for cost savings","Design end-to-end ML pipeline with SageMaker Pipelines","Understand hyperparameter tuning strategies","Know SageMaker Model Monitor for drift detection","Understand A/B testing and shadow deployment for models","Know data formats: CSV, RecordIO-Protobuf, Parquet, Pipe Mode","Design data pipelines with Glue, Athena, Kinesis for ML","Understand bias detection with SageMaker Clarify","Know Rekognition: image analysis, facial analysis, content moderation","Understand Comprehend for NLP tasks","Know when to use Forecast vs DeepAR","Understand Bedrock: foundation models, RAG, Agents","Know SageMaker endpoints: real-time, serverless, batch, async","Understand Feature Store: online vs offline store","Design cost-optimized ML with managed spot training","Know evaluation metrics: accuracy, F1, AUC-ROC, RMSE"],
   "das-c01.html","Data Analytics Specialty (DAS-C01)"),

  ("DAS-C01","badge-red","Specialty","&#128202;","AWS Certified Data Analytics Specialty",
   "Design scalable analytics solutions. Kinesis, Glue, Redshift, Athena, Lake Formation, QuickSight.",
   '<span class="badge badge-green">180 min | 65 questions</span><span class="badge badge-red">Passing: 750/1000</span>',
   ("Data Analytics on AWS","https://explore.skillbuilder.aws/learn/course/external/view/elearning/3498/data-analytics-fundamentals",
    "https://d1.awsstatic.com/training-and-certification/docs-data-analytics-specialty/AWS-Certified-Data-Analytics-Specialty_Exam-Guide.pdf",
    "https://d1.awsstatic.com/training-and-certification/docs-data-analytics-specialty/AWS-Certified-Data-Analytics-Specialty_Sample-Questions.pdf",
    "180 minutes","65","750",[("Collection","18"),("Storage","22"),("Processing","24"),("Analysis & Visualization","18"),("Security","18")]),
   """<section id="kinesis"><h2>Amazon Kinesis Family</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>Purpose</th><th>Key Details</th></tr></thead><tbody>
  <tr><td>Kinesis Data Streams</td><td>Real-time streaming</td><td>Shards (1 MB/s in, 2 MB/s out); retention 1-365 days; consumers: Lambda, KDA, KCL</td></tr>
  <tr><td>Kinesis Data Firehose</td><td>Load streaming data to destinations</td><td>Managed; near real-time (60s buffer); destinations: S3, Redshift, OpenSearch, Splunk</td></tr>
  <tr><td>Kinesis Data Analytics</td><td>SQL/Flink on streaming data</td><td>Real-time analytics; output to Firehose or streams</td></tr>
  <tr><td>MSK (Managed Kafka)</td><td>Apache Kafka managed service</td><td>Full Kafka compatibility; MSK Serverless</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; Kinesis vs SQS</div><ul>
  <li>Use <strong>Kinesis</strong> when: multiple consumers, replay needed, ordered per shard, real-time analytics</li>
  <li>Use <strong>SQS</strong> when: decoupling, one consumer, simplicity</li>
</ul></div></section>
<section id="glue"><h2>AWS Glue</h2>
<div class="table-wrap"><table><thead><tr><th>Component</th><th>Purpose</th></tr></thead><tbody>
  <tr><td>Data Catalog</td><td>Metadata repository; tables, schemas, partitions; integrates with Athena, EMR, Redshift</td></tr>
  <tr><td>Crawlers</td><td>Auto-discover schema from S3, RDS, DynamoDB; update Data Catalog</td></tr>
  <tr><td>ETL Jobs</td><td>PySpark/Python scripts; serverless; transform data between sources</td></tr>
  <tr><td>DataBrew</td><td>No-code data preparation; visual transformations; 250+ transforms</td></tr>
  <tr><td>Streaming ETL</td><td>Continuous ETL from Kinesis/Kafka to S3/Redshift</td></tr>
</tbody></table></div></section>
<section id="redshift"><h2>Amazon Redshift</h2>
<ul><li><strong>Columnar storage</strong> - optimized for OLAP aggregations</li>
<li><strong>MPP</strong> - Massively Parallel Processing; leader node + compute nodes</li>
<li><strong>Redshift Spectrum</strong> - query S3 directly without loading into Redshift</li>
<li><strong>Redshift Serverless</strong> - no cluster management; auto-scaling; pay per compute</li>
<li><strong>Distribution Styles</strong>: EVEN, KEY, ALL - control data distribution across nodes</li>
<li><strong>Sort Keys</strong>: COMPOUND or INTERLEAVED - optimize query predicates</li></ul></section>
<section id="lake-formation"><h2>Lake Formation</h2>
<ul><li>Simplifies building secure data lakes on S3</li>
<li>Fine-grained access: table, column, row, cell-level permissions</li>
<li>Governed Tables - ACID transactions on S3 with automatic compaction</li>
<li>Tag-Based Access Control (LF-TBAC) - scale permissions with tags</li>
<li>Cross-account sharing of databases/tables</li></ul>
<h3>Data Lake Architecture</h3>
<pre><code>Bronze (Raw)      → Glue Crawlers → Data Catalog
       ↓
Silver (Cleansed) → Glue ETL → Parquet/ORC partitioned by date
       ↓
Gold (Curated)    → Redshift / Athena for analytics
       ↓
Visualization     → QuickSight / Grafana dashboards</code></pre></section>""",
   ["Design end-to-end analytics pipelines on AWS","Know Kinesis: Streams, Firehose, Analytics","Understand Kinesis shard sizing and partition keys","Know when to use Kinesis vs SQS vs MSK","Use Glue Crawlers and Data Catalog for schema management","Write Glue ETL jobs in PySpark","Design Redshift cluster: node types, distribution, sort keys","Use Redshift Spectrum to query S3","Design a data lake with Bronze/Silver/Gold layers","Configure Lake Formation for fine-grained access control","Use Athena with partitioning and columnar formats for cost efficiency","Know OpenSearch: indexing, shards, replicas","Design real-time dashboards with QuickSight","Understand EMR: cluster types, Spark on EMR","Know DynamoDB Streams → Lambda → Kinesis for CDC","Understand S3 lifecycle + Intelligent-Tiering for data lake cost","Configure CloudTrail data events for S3 analytics access logging","Know encryption for data at rest and in transit","Understand QuickSight SPICE vs direct query mode","Design for compliance: data residency, encryption, audit"],
   "resources.html","Resources Page"),
]:
  page = cert_page(code,lcls,ltxt,icon,title,desc,badges,ea,
    [("overview","Exam Overview")]+[(f"s{i}",h.split('>')[1].split('<')[0]) for i,h in enumerate(body_html.split('<section id="')[1:]) if '>' in h],
    body_html,chklist,nf,nl,
    extra_badge=CERT_EXTRAS.get(code,{}).get("extra_badge",""),
    notice=CERT_EXTRAS.get(code,{}).get("notice",""))
  write(f"{DOCS}/{code.lower().replace('-','')}.html", page)

# Fix filenames (hyphenated)
import shutil
for code in ["ANS-C01","MLS-C01","DAS-C01"]:
    src = f"{DOCS}/{code.lower().replace('-','')}.html"
    dst = f"{DOCS}/{code.lower()}.html"
    if os.path.exists(src): shutil.move(src,dst)

print("All cert pages done!")

# ── Newer cert pages (AIF-C01, DEA-C01, MLA-C01, AIP-C01) ────
# These use newcert_page() to get SEO tags, the quiz CTA, and reproducibility.
_new_toc = [("overview","Exam Overview"),("who","Who It's For"),("domains","Exam Domains"),
            ("topics","Key Topics"),("services","Key AWS Services"),("checklist","Study Checklist")]

# AIF-C01
write(f"{DOCS}/aif-c01.html", newcert_page(
  "AIF-C01","AWS Certified AI Practitioner",
  "Validate a foundational understanding of AI, machine learning, and generative AI concepts and their practical business applications on AWS. No coding required.",
  "badge-orange","Foundational","&#129504;",
  '<span class="badge badge-green">90 min | 65 questions</span><span class="badge badge-orange">Passing: 700/1000</span><span class="badge badge-teal">No prerequisites</span>',
  new_notice("&#127381; Newly launched certification",
    'The <strong>AWS Certified AI Practitioner (AIF-C01)</strong> is a foundational-level credential aimed at anyone who wants to demonstrate an overall understanding of AI/ML and generative AI on AWS - including non-technical roles. It pairs well with Cloud Practitioner (CLF-C02) as an entry point into the AI track.'),
  _new_toc,
  """<section id="overview"><h2>Exam Overview</h2>
<div class="grid-2">
  <div class="card"><h3>Exam Details</h3><ul>
    <li><strong>Code:</strong> AIF-C01</li>
    <li><strong>Level:</strong> Foundational</li>
    <li><strong>Duration:</strong> 90 minutes</li>
    <li><strong>Questions:</strong> 65</li>
    <li><strong>Passing Score:</strong> 700/1000</li>
    <li><strong>Cost:</strong> ~$100 USD</li>
    <li><strong>Validity:</strong> 3 years</li>
  </ul></div>
  <div class="card"><h3>&#127891; Official Resources</h3><ul>
    <li><a href="https://aws.amazon.com/certification/certified-ai-practitioner/" target="_blank" rel="noopener">Official Certification Page</a></li>
    <li><a href="https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html" target="_blank" rel="noopener">Official Exam Guide</a></li>
    <li><a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener">AWS Skill Builder - AI Practitioner path</a></li>
    <li><a href="https://aws.amazon.com/certification/" target="_blank" rel="noopener">Schedule Your Exam</a></li>
    <li><a href="https://tutorialsdojo.com/" target="_blank" rel="noopener">Tutorials Dojo Practice Exams</a></li>
  </ul></div>
</div></section>

<section id="who"><h2>&#128100; Who It's For</h2>
<div class="card"><p style="color:var(--text-muted)">Designed for individuals who use or interact with AI/ML solutions on AWS but do not necessarily build them. Recommended (not required): up to 6 months of exposure to AI/ML technologies on AWS. Ideal for business analysts, product managers, sales/marketing, IT support, and anyone starting the AWS AI learning path.</p></div>
</section>

<section id="domains"><h2>&#128202; Exam Domains</h2>
<div class="table-wrap"><table><thead><tr><th>Domain</th><th>Weight</th></tr></thead><tbody>
  <tr><td>1. Fundamentals of AI and ML</td><td>20%</td></tr>
  <tr><td>2. Fundamentals of Generative AI</td><td>24%</td></tr>
  <tr><td>3. Applications of Foundation Models</td><td>28%</td></tr>
  <tr><td>4. Guidelines for Responsible AI</td><td>14%</td></tr>
  <tr><td>5. Security, Compliance, and Governance for AI Solutions</td><td>14%</td></tr>
</tbody></table></div>
<p style="color:var(--text-muted);font-size:0.85rem">Domain weights reflect the AIF-C01 exam guide. Always confirm against the latest official guide.</p>
</section>

<section id="topics"><h2>&#128218; Key Topics</h2>
<div class="grid-2">
  <div class="card"><h3>AI/ML Fundamentals</h3><ul>
    <li>AI vs. ML vs. deep learning vs. generative AI</li>
    <li>Supervised, unsupervised, and reinforcement learning</li>
    <li>Training data, features, labels, inference</li>
    <li>Common use cases: classification, regression, forecasting, NLP, computer vision</li>
    <li>Model evaluation basics (accuracy, precision, recall)</li>
  </ul></div>
  <div class="card"><h3>Generative AI &amp; Foundation Models</h3><ul>
    <li>Foundation models (FMs) and large language models (LLMs)</li>
    <li>Tokens, embeddings, context windows, temperature</li>
    <li>Prompt engineering basics; zero/few-shot prompting</li>
    <li>Retrieval-Augmented Generation (RAG)</li>
    <li>Fine-tuning vs. prompt engineering vs. RAG trade-offs</li>
  </ul></div>
  <div class="card"><h3>Responsible AI</h3><ul>
    <li>Bias, fairness, transparency, explainability</li>
    <li>Hallucinations and how to mitigate them</li>
    <li>Human-in-the-loop and guardrails</li>
    <li>Amazon Bedrock Guardrails; SageMaker Clarify</li>
  </ul></div>
  <div class="card"><h3>Security &amp; Governance</h3><ul>
    <li>Data privacy: inputs/outputs not used to train FMs</li>
    <li>IAM for AI services; least privilege</li>
    <li>Encryption, VPC endpoints/PrivateLink for AI workloads</li>
    <li>Governance, compliance, and audit considerations</li>
  </ul></div>
</div></section>

<section id="services"><h2>&#9729;&#65039; Key AWS Services to Know</h2>
<div class="table-wrap"><table><thead><tr><th>Service</th><th>What to know</th></tr></thead><tbody>
  <tr><td>Amazon Bedrock</td><td>Managed access to foundation models; RAG (Knowledge Bases), Agents, Guardrails</td></tr>
  <tr><td>Amazon SageMaker AI</td><td>Build/train/deploy ML models; SageMaker Clarify (bias), JumpStart</td></tr>
  <tr><td>Amazon Q</td><td>Generative AI assistant for business and builders</td></tr>
  <tr><td>Amazon Comprehend</td><td>NLP: sentiment, entities, PII detection</td></tr>
  <tr><td>Amazon Rekognition</td><td>Image and video analysis</td></tr>
  <tr><td>Amazon Transcribe / Polly / Translate</td><td>Speech-to-text, text-to-speech, translation</td></tr>
  <tr><td>Amazon Textract</td><td>Extract text and data from documents</td></tr>
  <tr><td>Amazon Kendra</td><td>Intelligent enterprise search</td></tr>
</tbody></table></div></section>

<section id="checklist" class="progress-section"><h2>&#128203; Study Checklist</h2>
<div class="progress-wrap"><div class="progress-label"><span>Progress</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div>
<ul class="checklist">
  <li><input type="checkbox"><span>Read the official AIF-C01 exam guide</span></li>
  <li><input type="checkbox"><span>Understand AI vs ML vs deep learning vs generative AI</span></li>
  <li><input type="checkbox"><span>Learn foundation model concepts: tokens, embeddings, prompts</span></li>
  <li><input type="checkbox"><span>Understand RAG vs fine-tuning vs prompt engineering trade-offs</span></li>
  <li><input type="checkbox"><span>Explore Amazon Bedrock: models, Knowledge Bases, Guardrails, Agents</span></li>
  <li><input type="checkbox"><span>Review responsible AI: bias, fairness, explainability, hallucinations</span></li>
  <li><input type="checkbox"><span>Learn AI security & governance: data privacy, IAM, encryption</span></li>
  <li><input type="checkbox"><span>Know the AWS AI/ML service portfolio and use cases</span></li>
  <li><input type="checkbox"><span>Complete the AWS Skill Builder AI Practitioner learning plan</span></li>
  <li><input type="checkbox"><span>Score 75%+ on practice exams before booking</span></li>
</ul>
<div class="mt-2"><a href="mla-c01.html" class="btn btn-primary">Next: MLA-C01 (ML Engineer Associate) &rarr;</a></div>
</section>""",
  extra_badge=NEW_CERT_BADGE,
  meta_desc="AIF-C01 study guide. Foundational AI, ML, and generative AI concepts, Amazon Bedrock, SageMaker, responsible AI, and prompt engineering basics."))

# DEA-C01
write(f"{DOCS}/dea-c01.html", newcert_page(
  "DEA-C01","AWS Certified Data Engineer Associate",
  "Design and build data pipelines: ingestion, transformation, storage, and operations. The modern replacement for the retired Data Analytics Specialty.",
  "badge-blue","Associate","&#128202;",
  '<span class="badge badge-green">130 min | 65 questions</span><span class="badge badge-blue">Passing: 720/1000</span>',
  new_notice("&#127381; Newly launched - replaces DAS-C01",
    'The <strong>AWS Certified Data Engineer - Associate (DEA-C01)</strong> launched in 2024 as the modern successor to the retired <a href="das-c01.html">Data Analytics - Specialty (DAS-C01)</a>. It focuses on building and operating data pipelines rather than analytics tooling alone.'),
  _new_toc,
  """<section id="overview"><h2>Exam Overview</h2>
<div class="grid-2">
  <div class="card"><h3>Exam Details</h3><ul>
    <li><strong>Code:</strong> DEA-C01</li>
    <li><strong>Level:</strong> Associate</li>
    <li><strong>Duration:</strong> 130 minutes</li>
    <li><strong>Questions:</strong> 65</li>
    <li><strong>Passing Score:</strong> 720/1000</li>
    <li><strong>Cost:</strong> ~$150 USD</li>
    <li><strong>Validity:</strong> 3 years</li>
  </ul></div>
  <div class="card"><h3>&#127891; Official Resources</h3><ul>
    <li><a href="https://aws.amazon.com/certification/certified-data-engineer-associate/" target="_blank" rel="noopener">Official Certification Page</a></li>
    <li><a href="https://docs.aws.amazon.com/aws-certification/latest/data-engineer-associate-01/data-engineer-associate-01.html" target="_blank" rel="noopener">Official Exam Guide</a></li>
    <li><a href="https://d1.awsstatic.com/training-and-certification/docs-data-engineer-associate/AWS-Certified-Data-Engineer-Associate_Exam-Guide.pdf" target="_blank" rel="noopener">Exam Guide (PDF)</a></li>
    <li><a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener">AWS Skill Builder - Data Engineer path</a></li>
    <li><a href="https://tutorialsdojo.com/" target="_blank" rel="noopener">Tutorials Dojo Practice Exams</a></li>
  </ul></div>
</div></section>

<section id="who"><h2>&#128100; Who It's For</h2>
<div class="card"><p style="color:var(--text-muted)">Data engineers and related roles. AWS recommends 2-3 years of data engineering experience and 1-2 years of hands-on experience with AWS services. Strong fit for anyone who previously targeted the retired DAS-C01, plus ETL/pipeline developers and analytics engineers.</p></div>
</section>

<section id="domains"><h2>&#128202; Exam Domains</h2>
<div class="table-wrap"><table><thead><tr><th>Domain</th><th>Weight</th></tr></thead><tbody>
  <tr><td>1. Data Ingestion and Transformation</td><td>34%</td></tr>
  <tr><td>2. Data Store Management</td><td>26%</td></tr>
  <tr><td>3. Data Operations and Support</td><td>22%</td></tr>
  <tr><td>4. Data Security and Governance</td><td>18%</td></tr>
</tbody></table></div>
<p style="color:var(--text-muted);font-size:0.85rem">Domain weights reflect the DEA-C01 exam guide. Confirm against the latest official guide.</p>
</section>

<section id="topics"><h2>&#128218; Key Topics</h2>
<div class="grid-2">
  <div class="card"><h3>Ingestion &amp; Transformation</h3><ul>
    <li>Batch vs. streaming ingestion patterns</li>
    <li>Kinesis Data Streams / Data Firehose, MSK (Kafka)</li>
    <li>AWS Glue ETL, Glue crawlers, Glue Data Catalog</li>
    <li>Spark on EMR; AWS DMS for migration/CDC</li>
    <li>Orchestration: Step Functions, MWAA (Airflow), EventBridge</li>
  </ul></div>
  <div class="card"><h3>Data Store Management</h3><ul>
    <li>S3 data lake design, partitioning, file formats (Parquet/ORC)</li>
    <li>Redshift architecture, distribution/sort keys, Spectrum</li>
    <li>Lake Formation permissions and governed tables</li>
    <li>Apache Iceberg / data lakehouse patterns</li>
    <li>Choosing the right store (DynamoDB, RDS, OpenSearch)</li>
  </ul></div>
  <div class="card"><h3>Operations &amp; Support</h3><ul>
    <li>Monitoring pipelines with CloudWatch, Glue job metrics</li>
    <li>Cost & performance optimization (compression, partition pruning)</li>
    <li>Troubleshooting failed jobs, retries, DLQs</li>
    <li>Automation and CI/CD for data pipelines</li>
  </ul></div>
  <div class="card"><h3>Security &amp; Governance</h3><ul>
    <li>Encryption at rest/in transit; KMS</li>
    <li>IAM, Lake Formation fine-grained access, row/column security</li>
    <li>Data quality, cataloging, lineage</li>
    <li>PII detection and masking (Macie, Glue)</li>
  </ul></div>
</div></section>

<section id="services"><h2>&#9729;&#65039; Key AWS Services to Know</h2>
<div class="table-wrap"><table><thead><tr><th>Category</th><th>Services</th></tr></thead><tbody>
  <tr><td>Ingestion</td><td>Kinesis Data Streams, Data Firehose, MSK, DMS, DataSync</td></tr>
  <tr><td>Transformation</td><td>AWS Glue (ETL, crawlers, Data Catalog), EMR (Spark), Lambda</td></tr>
  <tr><td>Storage</td><td>S3, Redshift, Lake Formation, DynamoDB, RDS/Aurora</td></tr>
  <tr><td>Query &amp; Analytics</td><td>Athena, Redshift Spectrum, OpenSearch Service, QuickSight</td></tr>
  <tr><td>Orchestration</td><td>Step Functions, MWAA (Airflow), EventBridge</td></tr>
  <tr><td>Security &amp; Governance</td><td>IAM, KMS, Lake Formation, Macie, Glue Data Quality</td></tr>
</tbody></table></div></section>

<section id="checklist" class="progress-section"><h2>&#128203; Study Checklist</h2>
<div class="progress-wrap"><div class="progress-label"><span>Progress</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div>
<ul class="checklist">
  <li><input type="checkbox"><span>Read the official DEA-C01 exam guide</span></li>
  <li><input type="checkbox"><span>Master S3 data lake design: partitioning, Parquet/ORC</span></li>
  <li><input type="checkbox"><span>Build a Glue ETL job with a crawler and Data Catalog</span></li>
  <li><input type="checkbox"><span>Understand Kinesis Data Streams vs Data Firehose vs MSK</span></li>
  <li><input type="checkbox"><span>Learn Redshift distribution/sort keys and Spectrum</span></li>
  <li><input type="checkbox"><span>Orchestrate a pipeline with Step Functions or MWAA (Airflow)</span></li>
  <li><input type="checkbox"><span>Configure Lake Formation fine-grained permissions</span></li>
  <li><input type="checkbox"><span>Query S3 with Athena; understand Iceberg/lakehouse</span></li>
  <li><input type="checkbox"><span>Practice monitoring and cost/performance optimization</span></li>
  <li><input type="checkbox"><span>Score 75%+ on practice exams before booking</span></li>
</ul>
<div class="mt-2"><a href="resources.html" class="btn btn-primary">Browse Study Resources &rarr;</a></div>
</section>""",
  extra_badge=NEW_CERT_BADGE,
  meta_desc="DEA-C01 study guide. Data ingestion, transformation, storage, and operations - pipelines with Glue, Kinesis, Redshift, Lake Formation, and more."))

# MLA-C01
write(f"{DOCS}/mla-c01.html", newcert_page(
  "MLA-C01","AWS Certified Machine Learning Engineer Associate",
  "Build, deploy, operationalize, and monitor ML and generative AI solutions on AWS. The modern replacement for the retired ML Specialty.",
  "badge-blue","Associate","&#129302;",
  '<span class="badge badge-green">130 min | 65 questions</span><span class="badge badge-blue">Passing: 720/1000</span>',
  new_notice("&#127381; Newly launched - replaces MLS-C01",
    'The <strong>AWS Certified Machine Learning Engineer - Associate (MLA-C01)</strong> is the modern successor to the retired <a href="mls-c01.html">Machine Learning - Specialty (MLS-C01)</a>. Note: AWS is refreshing this exam - <strong>MLA-C02</strong> beta opened Sep 2026 (adds GenAI, agentic AI, and LLM workloads), with MLA-C01 retiring in all languages on Jan 14, 2027. This guide covers MLA-C01.'),
  _new_toc,
  """<section id="overview"><h2>Exam Overview</h2>
<div class="grid-2">
  <div class="card"><h3>Exam Details</h3><ul>
    <li><strong>Code:</strong> MLA-C01 (MLA-C02 beta from Sep 2026)</li>
    <li><strong>Level:</strong> Associate</li>
    <li><strong>Duration:</strong> 130 minutes</li>
    <li><strong>Questions:</strong> 65</li>
    <li><strong>Passing Score:</strong> 720/1000</li>
    <li><strong>Cost:</strong> ~$150 USD</li>
    <li><strong>Validity:</strong> 3 years</li>
  </ul></div>
  <div class="card"><h3>&#127891; Official Resources</h3><ul>
    <li><a href="https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/" target="_blank" rel="noopener">Official Certification Page</a></li>
    <li><a href="https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-01/machine-learning-engineer-associate-01.html" target="_blank" rel="noopener">Official Exam Guide</a></li>
    <li><a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener">AWS Skill Builder - ML Engineer path</a></li>
    <li><a href="https://aws.amazon.com/certification/" target="_blank" rel="noopener">Schedule Your Exam</a></li>
    <li><a href="https://tutorialsdojo.com/" target="_blank" rel="noopener">Tutorials Dojo Practice Exams</a></li>
  </ul></div>
</div></section>

<section id="who"><h2>&#128100; Who It's For</h2>
<div class="card"><p style="color:var(--text-muted)">ML engineers, MLOps engineers, and developers who build and operationalize ML/GenAI solutions. AWS recommends ~1 year using Amazon SageMaker AI and related services, plus ~1 year in a related role (backend dev, DevOps, data engineer, or data scientist). A great next step after AI Practitioner (AIF-C01).</p></div>
</section>

<section id="domains"><h2>&#128202; Exam Domains</h2>
<div class="table-wrap"><table><thead><tr><th>Domain</th><th>Weight</th></tr></thead><tbody>
  <tr><td>1. Data Preparation for Machine Learning</td><td>28%</td></tr>
  <tr><td>2. ML Model Development</td><td>26%</td></tr>
  <tr><td>3. Deployment and Orchestration of ML Workflows</td><td>22%</td></tr>
  <tr><td>4. ML Solution Monitoring, Maintenance, and Security</td><td>24%</td></tr>
</tbody></table></div>
<p style="color:var(--text-muted);font-size:0.85rem">Domain weights reflect the MLA-C01 exam guide. MLA-C02 keeps the same domain structure but adds GenAI/agentic AI coverage. Confirm against the latest official guide.</p>
</section>

<section id="topics"><h2>&#128218; Key Topics</h2>
<div class="grid-2">
  <div class="card"><h3>Data Preparation</h3><ul>
    <li>Feature engineering, transformation, and selection</li>
    <li>SageMaker Data Wrangler, Feature Store, Processing jobs</li>
    <li>Handling missing data, encoding, scaling, imbalance</li>
    <li>Data ingestion from S3, Glue, streaming sources</li>
  </ul></div>
  <div class="card"><h3>Model Development</h3><ul>
    <li>Algorithm selection; SageMaker built-in algorithms</li>
    <li>Training, hyperparameter tuning (AMT), evaluation metrics</li>
    <li>Overfitting/underfitting, cross-validation</li>
    <li>SageMaker JumpStart; foundation models via Bedrock (C02)</li>
  </ul></div>
  <div class="card"><h3>Deployment &amp; Orchestration</h3><ul>
    <li>Real-time endpoints, batch transform, async & serverless inference</li>
    <li>SageMaker Pipelines; CI/CD for ML (MLOps)</li>
    <li>Model registry, versioning, A/B and shadow testing</li>
    <li>Infrastructure choices and cost optimization</li>
  </ul></div>
  <div class="card"><h3>Monitoring &amp; Security</h3><ul>
    <li>SageMaker Model Monitor: data/model drift</li>
    <li>SageMaker Clarify: bias & explainability</li>
    <li>CloudWatch metrics/alarms; retraining triggers</li>
    <li>IAM, VPC, encryption for ML workloads</li>
  </ul></div>
</div></section>

<section id="services"><h2>&#9729;&#65039; Key AWS Services to Know</h2>
<div class="table-wrap"><table><thead><tr><th>Category</th><th>Services</th></tr></thead><tbody>
  <tr><td>Core ML</td><td>Amazon SageMaker AI (Studio, Training, Endpoints, Pipelines, Model Monitor, Clarify, Feature Store, JumpStart)</td></tr>
  <tr><td>Generative AI (C02)</td><td>Amazon Bedrock, Bedrock AgentCore, foundation models, RAG</td></tr>
  <tr><td>Data</td><td>S3, Glue, Athena, Kinesis, Feature Store</td></tr>
  <tr><td>Orchestration &amp; MLOps</td><td>SageMaker Pipelines, Step Functions, CodePipeline, EventBridge</td></tr>
  <tr><td>Monitoring &amp; Security</td><td>CloudWatch, IAM, KMS, VPC, Model Monitor</td></tr>
</tbody></table></div></section>

<section id="checklist" class="progress-section"><h2>&#128203; Study Checklist</h2>
<div class="progress-wrap"><div class="progress-label"><span>Progress</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div>
<ul class="checklist">
  <li><input type="checkbox"><span>Read the official MLA-C01 (or MLA-C02) exam guide</span></li>
  <li><input type="checkbox"><span>Prepare data with SageMaker Data Wrangler & Feature Store</span></li>
  <li><input type="checkbox"><span>Train and tune a model with SageMaker built-in algorithms + AMT</span></li>
  <li><input type="checkbox"><span>Deploy real-time, batch, async, and serverless inference</span></li>
  <li><input type="checkbox"><span>Build an MLOps pipeline with SageMaker Pipelines + model registry</span></li>
  <li><input type="checkbox"><span>Configure Model Monitor for drift and Clarify for bias</span></li>
  <li><input type="checkbox"><span>Explore generative AI via Amazon Bedrock (esp. for MLA-C02)</span></li>
  <li><input type="checkbox"><span>Secure ML workloads: IAM, VPC, KMS encryption</span></li>
  <li><input type="checkbox"><span>Complete the AWS Skill Builder ML Engineer learning plan</span></li>
  <li><input type="checkbox"><span>Score 75%+ on practice exams before booking</span></li>
</ul>
<div class="mt-2"><a href="aip-c01.html" class="btn btn-primary">Next: AIP-C01 (Generative AI Developer Pro) &rarr;</a></div>
</section>""",
  extra_badge=NEW_CERT_BADGE,
  meta_desc="MLA-C01 study guide. Build, deploy, operationalize, and monitor ML and generative AI solutions on AWS with Amazon SageMaker AI and Bedrock."))

# AIP-C01
write(f"{DOCS}/aip-c01.html", newcert_page(
  "AIP-C01","AWS Certified Generative AI Developer Professional",
  "Integrate foundation models into production applications and business workflows using Amazon Bedrock, agents, RAG, and guardrails - with security and cost efficiency.",
  "badge-purple","Professional","&#129504;",
  '<span class="badge badge-green">180 min | 65 questions</span><span class="badge badge-purple">Passing: 750/1000</span>',
  new_notice("&#127381; Newly launched professional-level AI certification",
    'The <strong>AWS Certified Generative AI Developer - Professional (AIP-C01)</strong> is a professional-level credential for developers who build production generative AI solutions. The beta period ended March 31, 2026, and the exam is now generally available. It sits at the top of the AWS AI track alongside the foundational <a href="aif-c01.html">AI Practitioner (AIF-C01)</a>.'),
  _new_toc,
  """<section id="overview"><h2>Exam Overview</h2>
<div class="grid-2">
  <div class="card"><h3>Exam Details</h3><ul>
    <li><strong>Code:</strong> AIP-C01</li>
    <li><strong>Level:</strong> Professional</li>
    <li><strong>Duration:</strong> 180 minutes</li>
    <li><strong>Questions:</strong> 65</li>
    <li><strong>Passing Score:</strong> 750/1000</li>
    <li><strong>Cost:</strong> ~$300 USD</li>
    <li><strong>Validity:</strong> 3 years</li>
  </ul></div>
  <div class="card"><h3>&#127891; Official Resources</h3><ul>
    <li><a href="https://aws.amazon.com/certification/certified-generative-ai-developer-professional/" target="_blank" rel="noopener">Official Certification Page</a></li>
    <li><a href="https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01.html" target="_blank" rel="noopener">Official Exam Guide</a></li>
    <li><a href="https://explore.skillbuilder.aws/" target="_blank" rel="noopener">AWS Skill Builder - Generative AI Developer path</a></li>
    <li><a href="https://aws.amazon.com/certification/" target="_blank" rel="noopener">Schedule Your Exam</a></li>
    <li><a href="https://tutorialsdojo.com/" target="_blank" rel="noopener">Tutorials Dojo Practice Exams</a></li>
  </ul></div>
</div></section>

<section id="who"><h2>&#128100; Who It's For</h2>
<div class="card"><p style="color:var(--text-muted)">Developers who build production generative AI applications. No formal prerequisites, but AWS recommends 2+ years of AWS experience and 1+ year of hands-on generative AI development. Recommended after gaining GenAI experience and ideally the AI Practitioner and/or ML Engineer Associate credentials.</p></div>
</section>

<section id="domains"><h2>&#128202; Exam Domains</h2>
<div class="table-wrap"><table><thead><tr><th>Domain (representative)</th><th>Focus</th></tr></thead><tbody>
  <tr><td>1. Foundation Model Selection &amp; Integration</td><td>Choosing FMs, invoking via Bedrock, embeddings, multimodal</td></tr>
  <tr><td>2. Prompt Engineering &amp; Application Design</td><td>Advanced prompting, RAG, agents, orchestration</td></tr>
  <tr><td>3. Customization &amp; Optimization</td><td>Fine-tuning, distillation, evaluation, cost/latency tuning</td></tr>
  <tr><td>4. Responsible AI, Security &amp; Operations</td><td>Guardrails, privacy, monitoring, deployment, governance</td></tr>
</tbody></table></div>
<p style="color:var(--text-muted);font-size:0.85rem">The exam guide defines the authoritative domains and weights - this is a representative summary. Always confirm against the official AIP-C01 exam guide.</p>
</section>

<section id="topics"><h2>&#128218; Key Topics</h2>
<div class="grid-2">
  <div class="card"><h3>Foundation Models &amp; Bedrock</h3><ul>
    <li>Selecting FMs by capability, cost, latency, context window</li>
    <li>Bedrock InvokeModel / Converse APIs; streaming</li>
    <li>Embeddings and vector representations</li>
    <li>Multimodal inputs (text, image)</li>
  </ul></div>
  <div class="card"><h3>RAG &amp; Agents</h3><ul>
    <li>Retrieval-Augmented Generation architectures</li>
    <li>Bedrock Knowledge Bases; vector stores (OpenSearch, Aurora pgvector)</li>
    <li>Bedrock Agents & AgentCore for tool use and workflows</li>
    <li>Chunking, re-ranking, grounding strategies</li>
  </ul></div>
  <div class="card"><h3>Customization &amp; Evaluation</h3><ul>
    <li>Fine-tuning vs. RAG vs. prompt engineering trade-offs</li>
    <li>Model distillation; continued pre-training</li>
    <li>Evaluation: automated metrics, human eval, LLM-as-judge</li>
    <li>Latency, throughput, and cost optimization (caching, batching)</li>
  </ul></div>
  <div class="card"><h3>Responsible AI &amp; Security</h3><ul>
    <li>Bedrock Guardrails: content filtering, PII, denied topics</li>
    <li>Prompt injection defense; tool-use authorization</li>
    <li>Data privacy: VPC endpoints, no-train guarantees</li>
    <li>Monitoring, logging, human-in-the-loop oversight</li>
  </ul></div>
</div></section>

<section id="services"><h2>&#9729;&#65039; Key AWS Services to Know</h2>
<div class="table-wrap"><table><thead><tr><th>Category</th><th>Services</th></tr></thead><tbody>
  <tr><td>Core GenAI</td><td>Amazon Bedrock (models, Knowledge Bases, Agents, Guardrails, Evaluations), Bedrock AgentCore</td></tr>
  <tr><td>Vector / Retrieval</td><td>OpenSearch Service, Aurora PostgreSQL (pgvector), Kendra</td></tr>
  <tr><td>ML platform</td><td>Amazon SageMaker AI (for custom models / hosting)</td></tr>
  <tr><td>App integration</td><td>Lambda, API Gateway, Step Functions, EventBridge</td></tr>
  <tr><td>Security &amp; Ops</td><td>IAM, KMS, VPC/PrivateLink, CloudWatch, CloudTrail</td></tr>
</tbody></table></div></section>

<section id="checklist" class="progress-section"><h2>&#128203; Study Checklist</h2>
<div class="progress-wrap"><div class="progress-label"><span>Progress</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div>
<ul class="checklist">
  <li><input type="checkbox"><span>Read the official AIP-C01 exam guide</span></li>
  <li><input type="checkbox"><span>Invoke foundation models via Bedrock (InvokeModel / Converse)</span></li>
  <li><input type="checkbox"><span>Build a RAG app with Bedrock Knowledge Bases + a vector store</span></li>
  <li><input type="checkbox"><span>Create a Bedrock Agent / AgentCore workflow with tool use</span></li>
  <li><input type="checkbox"><span>Configure Bedrock Guardrails (content filters, PII, denied topics)</span></li>
  <li><input type="checkbox"><span>Compare fine-tuning vs RAG vs prompt engineering</span></li>
  <li><input type="checkbox"><span>Evaluate model quality (automated + human + LLM-as-judge)</span></li>
  <li><input type="checkbox"><span>Optimize latency and cost (caching, batching, model choice)</span></li>
  <li><input type="checkbox"><span>Secure GenAI apps: prompt injection defense, VPC endpoints, IAM</span></li>
  <li><input type="checkbox"><span>Score 75%+ on practice exams before booking</span></li>
</ul>
<div class="mt-2"><a href="resources.html" class="btn btn-primary">Browse Study Resources &rarr;</a></div>
</section>""",
  extra_badge=NEW_CERT_BADGE,
  meta_desc="AIP-C01 study guide. Integrate foundation models into production apps with Amazon Bedrock, agents, RAG, and guardrails - securely and cost-efficiently."))

# ── foundations-linux.html ──────────────────────────────────
linux_html = HEAD("Linux Fundamentals","Complete Linux guide for AWS certification candidates.").replace("../assets","../assets") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Foundations</span> / <span>Linux Fundamentals</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-teal">Foundations</span>
  <h1 style="margin-top:0.75rem">&#128039; Linux Fundamentals</h1>
  <p>Master essential Linux skills needed for every AWS certification and real-world cloud engineering. From the file system and permissions to text processing, storage, shell scripting, systemd, security hardening, containers, and a full troubleshooting playbook.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-green">Beginner Friendly</span><span class="badge badge-blue">21 Topics</span><span class="badge badge-orange">Essential for all AWS Certs</span></div>
</div></div>
""" + wrap([("why","Why Linux for AWS?"),("distros","Distributions & Shells"),("filesystem","File System"),("navigation","Navigation & Files"),("permissions","Permissions"),("users","Users & Groups"),("text","Text Processing"),("commands","Command Reference"),("processes","Processes & Signals"),("resources","Memory, CPU & Disk"),("storage","Disks, Partitions & Mounts"),("packages","Package Management"),("networking","Networking Commands"),("scripting","Shell Scripting"),("cron","Cron & Scheduling"),("logs","Logs & journald"),("ssh","SSH & EC2 Access"),("systemd","Systemd & Services"),("security","Security Hardening"),("containers","Containers on Linux"),("troubleshooting","Troubleshooting Playbook"),("checklist","Checklist")], """
<section id="why"><h2>Why Linux for AWS?</h2>
<p>Over <strong>90% of cloud workloads</strong> run on Linux. EC2 instances, ECS/EKS containers, Lambda execution environments, and most managed services run on a Linux kernel under the hood. Solid Linux skills let you:</p>
<ul><li>Debug EC2 instances over SSH and Session Manager</li><li>Write UserData / cloud-init bootstrap scripts</li><li>Build and run Docker containers for ECS, EKS, and Fargate</li><li>Read logs, trace processes, and diagnose performance issues</li><li>Answer scenario questions on SOA-C02, DVA-C02, and SAP-C02 exams</li></ul>
<div class="callout tip"><div class="callout-title">&#128161; Tip</div><p>On EC2, <code>/var/log/cloud-init-output.log</code> captures your UserData script output - the first place to look when a bootstrap fails.</p></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Amazon Linux 2023</div><p>AL2023 is the current default Amazon Linux. It uses <code>dnf</code> (not <code>yum</code>), <code>systemd</code>, and ships with SELinux in permissive mode. The default login user is <code>ec2-user</code>.</p></div></section>

<section id="distros"><h2>Distributions &amp; Shells</h2>
<div class="table-wrap"><table><thead><tr><th>Distro</th><th>Package Mgr</th><th>Default EC2 User</th><th>Notes</th></tr></thead><tbody>
  <tr><td>Amazon Linux 2023</td><td>dnf</td><td>ec2-user</td><td>AWS-tuned, current default</td></tr>
  <tr><td>Amazon Linux 2</td><td>yum</td><td>ec2-user</td><td>Legacy, still widely used</td></tr>
  <tr><td>Ubuntu</td><td>apt</td><td>ubuntu</td><td>Popular, large ecosystem</td></tr>
  <tr><td>RHEL / Rocky / Alma</td><td>dnf/yum</td><td>ec2-user / rocky</td><td>Enterprise, RPM-based</td></tr>
  <tr><td>Debian</td><td>apt</td><td>admin</td><td>Stable, minimal</td></tr>
  <tr><td>SUSE (SLES)</td><td>zypper</td><td>ec2-user</td><td>SAP workloads</td></tr>
</tbody></table></div>
<p>The <strong>shell</strong> is the program that interprets your commands. <code>bash</code> is the most common; <code>sh</code>, <code>zsh</code>, and <code>dash</code> also appear. Check yours with <code>echo $SHELL</code>.</p>
<pre><code>cat /etc/os-release       # Identify the distribution and version
echo $SHELL               # Your login shell
uname -r                  # Kernel version
hostnamectl               # Host, OS, kernel summary (systemd)</code></pre></section>

<section id="filesystem"><h2>Linux File System (FHS)</h2>
<p>Linux follows the <strong>Filesystem Hierarchy Standard</strong>. Everything is a file, and everything hangs off a single root <code>/</code>.</p>
<div class="table-wrap"><table><thead><tr><th>Directory</th><th>Purpose</th></tr></thead><tbody>
  <tr><td><code>/</code></td><td>Root of the entire filesystem</td></tr>
  <tr><td><code>/bin</code>, <code>/usr/bin</code></td><td>Essential and user binaries (ls, cp, mv)</td></tr>
  <tr><td><code>/sbin</code>, <code>/usr/sbin</code></td><td>System admin binaries (mount, iptables)</td></tr>
  <tr><td><code>/etc</code></td><td>System-wide configuration files</td></tr>
  <tr><td><code>/home</code></td><td>User home directories</td></tr>
  <tr><td><code>/root</code></td><td>Home directory of the root user</td></tr>
  <tr><td><code>/var</code></td><td>Variable data (logs, spools, caches, mail)</td></tr>
  <tr><td><code>/var/log</code></td><td>Log files - your debugging home base</td></tr>
  <tr><td><code>/tmp</code></td><td>Temporary files (often cleared on reboot)</td></tr>
  <tr><td><code>/proc</code></td><td>Virtual FS exposing kernel/process info</td></tr>
  <tr><td><code>/sys</code></td><td>Virtual FS for devices and kernel objects</td></tr>
  <tr><td><code>/dev</code></td><td>Device files (disks: /dev/xvda, /dev/nvme0n1)</td></tr>
  <tr><td><code>/opt</code></td><td>Optional / third-party software packages</td></tr>
  <tr><td><code>/mnt</code>, <code>/media</code></td><td>Mount points for extra filesystems</td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; Everything is a file</div><p>Disks, processes, and even network sockets are represented as files. That is why tools like <code>cat /proc/cpuinfo</code> and <code>cat /proc/meminfo</code> work.</p></div></section>

<section id="navigation"><h2>Navigation &amp; File Operations</h2>
<pre><code># Where am I / what is here
pwd                       # Print working directory
ls -la                    # Long listing incl. hidden files
ls -lh                    # Human-readable sizes
tree -L 2                 # Directory tree (2 levels)

# Moving around
cd /var/log; cd ~; cd -   # Absolute, home, previous dir

# Create / copy / move / delete
mkdir -p a/b/c            # Create nested directories
touch file.txt           # Create empty file / update timestamp
cp -r src/ dest/          # Recursive copy
mv old.txt new.txt        # Rename or move
rm -i file.txt           # Interactive delete (safer)
rm -rf dir/              # Recursive force delete (dangerous)

# Read files
cat file.txt              # Dump whole file
less file.txt             # Page through (q to quit)
head -n 20 file.txt       # First 20 lines
tail -n 50 file.txt       # Last 50 lines
tail -f /var/log/syslog   # Follow live (Ctrl+C to stop)

# Links
ln -s /path/target link   # Symbolic link
</code></pre>
<div class="callout warn"><div class="callout-title">&#9888; rm -rf is irreversible</div><p>There is no recycle bin. <code>rm -rf /</code> or a mistyped variable like <code>rm -rf $DIR/</code> (when <code>$DIR</code> is empty) can wipe a system. Double-check paths and prefer <code>rm -i</code> when unsure.</p></div></section>

<section id="permissions"><h2>File Permissions &amp; Ownership</h2>
<pre><code>-rwxr-xr-- 1 ubuntu aws-team 1234 Jul 10 12:00 deploy.sh
│└──┬──┘└──┬──┘└──┬──┘
│   │      │      └── Other: r-- (4)
│   │      └───────── Group: r-x (5)
│   └──────────────── Owner: rwx (7)
└── File type: - file, d directory, l symlink</code></pre>
<div class="table-wrap"><table><thead><tr><th>Permission</th><th>Symbol</th><th>Octal</th></tr></thead><tbody>
  <tr><td>Read</td><td>r</td><td>4</td></tr><tr><td>Write</td><td>w</td><td>2</td></tr>
  <tr><td>Execute</td><td>x</td><td>1</td></tr><tr><td>None</td><td>-</td><td>0</td></tr>
</tbody></table></div>
<pre><code>chmod 755 script.sh          # rwxr-xr-x
chmod 640 secret.conf        # rw-r-----
chmod +x script.sh           # Add execute for all
chmod -R g+w /shared         # Recursive group write
chown ubuntu:team file.txt   # Change owner:group
chgrp team file.txt          # Change group only
umask 022                    # Default permission mask</code></pre>
<h3>Special permission bits</h3>
<div class="table-wrap"><table><thead><tr><th>Bit</th><th>Octal</th><th>Effect</th></tr></thead><tbody>
  <tr><td>setuid</td><td>4000</td><td>Run as file owner (e.g. <code>passwd</code>)</td></tr>
  <tr><td>setgid</td><td>2000</td><td>Run as group / inherit group on dirs</td></tr>
  <tr><td>sticky</td><td>1000</td><td>Only owner can delete (e.g. <code>/tmp</code>)</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>SSH private keys must be <code>chmod 400</code> (or 600). SSH refuses to use a <code>.pem</code> that is readable by group/other with an "UNPROTECTED PRIVATE KEY FILE" error.</p></div></section>

<section id="users"><h2>Users, Groups &amp; sudo</h2>
<pre><code># Identity
whoami; id                    # Current user, UID/GID/groups
who; w                        # Who is logged in

# Manage users (need root/sudo)
sudo useradd -m -s /bin/bash alice   # Create user with home + shell
sudo passwd alice                    # Set password
sudo usermod -aG docker alice        # Add to supplementary group
sudo userdel -r alice                # Delete user and home

# Groups
sudo groupadd deploy
groups alice                         # Show a user's groups

# Elevated privileges
sudo command                         # Run one command as root
sudo -i                              # Interactive root shell
visudo                               # Safely edit /etc/sudoers</code></pre>
<div class="table-wrap"><table><thead><tr><th>File</th><th>Contents</th></tr></thead><tbody>
  <tr><td><code>/etc/passwd</code></td><td>User accounts (name, UID, GID, home, shell)</td></tr>
  <tr><td><code>/etc/shadow</code></td><td>Hashed passwords (root-only)</td></tr>
  <tr><td><code>/etc/group</code></td><td>Group definitions and members</td></tr>
  <tr><td><code>/etc/sudoers</code></td><td>Who can run sudo and how</td></tr>
</tbody></table></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; AWS Context</div><p>On EC2, the default user (<code>ec2-user</code> / <code>ubuntu</code>) is granted passwordless sudo via a file in <code>/etc/sudoers.d/</code>. SSM Session Manager connects as <code>ssm-user</code>.</p></div></section>

<section id="text"><h2>Text Processing (grep, sed, awk)</h2>
<pre><code># grep - search text
grep -i "error" app.log          # Case-insensitive
grep -r "TODO" src/              # Recursive
grep -c "404" access.log         # Count matches
grep -v "DEBUG" app.log          # Invert (exclude)
grep -E "warn|error" app.log     # Extended regex

# sed - stream editor (find/replace)
sed 's/foo/bar/g' file.txt       # Replace all foo with bar
sed -i 's/8080/80/g' app.conf    # In-place edit
sed -n '10,20p' file.txt         # Print lines 10-20

# awk - column/field processing
awk '{print $1}' access.log      # First field of each line
awk -F',' '{print $3}' data.csv  # CSV third column
awk '$9 == 500 {print}' access.log  # Rows where field 9 is 500
awk '{sum+=$1} END {print sum}' nums.txt  # Sum a column

# cut / sort / uniq / wc
cut -d':' -f1 /etc/passwd         # First colon-delimited field
sort file.txt | uniq -c | sort -rn  # Frequency count, descending
wc -l file.txt                    # Count lines</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Real-world combo</div><p>Find the top 10 IPs hitting your server: <code>awk '{print $1}' access.log | sort | uniq -c | sort -rn | head</code></p></div></section>

<section id="commands"><h2>Command Reference</h2>
<pre><code># Pipes and redirection
command | other           # Pipe stdout to next command
command > file            # Redirect stdout (overwrite)
command >> file           # Redirect stdout (append)
command 2> err.log        # Redirect stderr
command > out.log 2>&1    # Redirect both stdout and stderr
command < input.txt       # Feed file as stdin
command1 && command2      # Run command2 only if command1 succeeds
command1 || command2      # Run command2 only if command1 fails

# Search the filesystem
find / -name "*.log" -type f          # By name
find /var -size +100M                 # Files larger than 100MB
find . -mtime -1                      # Modified in last 24h
find /tmp -type f -delete             # Find and delete
which python3; whereis nginx; type ls # Locate binaries

# Archives & compression
tar -czvf archive.tar.gz /mydir       # Create gzip tarball
tar -xzvf archive.tar.gz              # Extract gzip tarball
tar -tzvf archive.tar.gz              # List contents
zip -r backup.zip /mydir; unzip backup.zip
gzip file; gunzip file.gz

# Transfer & sync
scp -i key.pem file ec2-user@IP:/tmp/ # Secure copy
rsync -avz src/ ec2-user@IP:/dest/    # Efficient sync
curl -O https://example.com/file.tgz  # Download
wget https://example.com/file.tgz     # Download</code></pre></section>

<section id="processes"><h2>Processes &amp; Signals</h2>
<pre><code>ps aux                    # All running processes
ps aux | grep nginx       # Filter for nginx
ps -ef --forest           # Process tree
pgrep -a nginx            # PIDs by name
top                       # Real-time process viewer
htop                      # Friendlier top (if installed)

# Sending signals
kill PID                  # SIGTERM (15) - graceful stop
kill -9 PID               # SIGKILL (9) - force kill
kill -HUP PID             # SIGHUP (1) - reload config
pkill nginx               # Kill by name
killall -9 python3        # Kill all matching

# Job control
command &                 # Run in background
jobs                      # List background jobs
fg %1; bg %1              # Foreground / background a job
nohup long_task &         # Survive logout
</code></pre>
<div class="table-wrap"><table><thead><tr><th>Signal</th><th>Number</th><th>Meaning</th></tr></thead><tbody>
  <tr><td>SIGTERM</td><td>15</td><td>Polite request to terminate (default)</td></tr>
  <tr><td>SIGKILL</td><td>9</td><td>Force kill, cannot be caught</td></tr>
  <tr><td>SIGHUP</td><td>1</td><td>Hang up / reload configuration</td></tr>
  <tr><td>SIGINT</td><td>2</td><td>Interrupt (Ctrl+C)</td></tr>
</tbody></table></div></section>

<section id="resources"><h2>Memory, CPU &amp; Load</h2>
<pre><code>free -h                   # Memory usage (human readable)
vmstat 1                  # Virtual memory stats every 1s
top                       # CPU + memory live view
uptime                    # Load averages (1, 5, 15 min)
nproc                     # Number of CPU cores
cat /proc/cpuinfo         # CPU details
cat /proc/meminfo         # Memory details
iostat -x 1               # Disk I/O stats (sysstat pkg)
sar -u 1 5                # Historical CPU sampling</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Reading load average</div><p>Load average is the number of processes waiting to run. On a machine with 4 cores, a load of 4.0 means fully busy. A load consistently above your core count means CPU saturation - a common CloudWatch alarm scenario.</p></div></section>

<section id="storage"><h2>Disks, Partitions &amp; Mounts</h2>
<pre><code>df -h                     # Disk usage per filesystem
du -sh /var/log           # Size of a directory
du -sh * | sort -rh | head  # Biggest items in current dir
lsblk                     # Block devices tree
blkid                     # Show UUIDs and filesystem types
mount | column -t         # Currently mounted filesystems

# Format and mount a new EBS volume (Nitro: /dev/nvme1n1)
sudo mkfs -t xfs /dev/nvme1n1
sudo mkdir /data
sudo mount /dev/nvme1n1 /data
# Persist across reboot via /etc/fstab (use UUID from blkid)
echo 'UUID=xxxx /data xfs defaults,nofail 0 2' | sudo tee -a /etc/fstab</code></pre>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>On Nitro-based instances, EBS volumes appear as NVMe devices (<code>/dev/nvme1n1</code>), not <code>/dev/xvdf</code>. Use <code>lsblk</code> to map them. Always add <code>nofail</code> in <code>/etc/fstab</code> so a missing volume does not block boot.</p></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Grow a filesystem after resizing EBS</div><p>After increasing an EBS volume: <code>sudo growpart /dev/nvme0n1 1</code> then <code>sudo xfs_growfs /</code> (xfs) or <code>sudo resize2fs /dev/nvme0n1p1</code> (ext4).</p></div></section>

<section id="packages"><h2>Package Management</h2>
<div class="grid-2">
  <div class="card"><h3>dnf / yum (Amazon Linux, RHEL)</h3><pre><code>sudo dnf update -y
sudo dnf install -y nginx
sudo dnf remove nginx
dnf search keyword
dnf list installed
rpm -qa | grep nginx</code></pre></div>
  <div class="card"><h3>apt (Ubuntu, Debian)</h3><pre><code>sudo apt update
sudo apt upgrade -y
sudo apt install -y nginx
sudo apt remove nginx
apt search keyword
dpkg -l | grep nginx</code></pre></div>
</div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>Amazon Linux 2 uses <code>yum</code>; Amazon Linux 2023 uses <code>dnf</code>; Ubuntu uses <code>apt</code>. UserData scripts must match the AMI's package manager or the bootstrap fails silently.</p></div></section>

<section id="networking"><h2>Linux Networking Commands</h2>
<pre><code># Interfaces & addresses
ip addr show                  # Show IP addresses (modern)
ip route                      # Routing table
ip link                       # Network interfaces

# Connectivity
ping -c 4 8.8.8.8             # ICMP reachability
traceroute google.com         # Path to a host
mtr google.com                # Live traceroute + loss

# DNS
nslookup example.com          # Basic DNS lookup
dig example.com               # Detailed DNS query
dig +short example.com        # Just the answer
host example.com              # Simple lookup

# Ports & sockets
ss -tulnp                     # Listening TCP/UDP + PIDs (modern)
netstat -tulnp                # Legacy equivalent
lsof -i :80                   # What is using port 80

# HTTP debugging
curl -I https://example.com   # Response headers only
curl -v https://api.example.com   # Verbose handshake
curl -s -o /dev/null -w "%{http_code}\\n" URL  # Just status code</code></pre>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>If you can ping an EC2 instance but cannot reach port 22, check the <strong>Security Group inbound rules</strong> and <strong>Network ACLs</strong> first. AWS network controls are evaluated before traffic ever reaches the OS firewall.</p></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Instance Metadata (IMDS)</div><p>Query instance metadata from inside EC2. Prefer IMDSv2 (token-based):</p><pre><code>TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \\
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \\
  http://169.254.169.254/latest/meta-data/instance-id</code></pre></div></section>

<section id="scripting"><h2>Shell Scripting</h2>
<pre><code>#!/bin/bash
set -euo pipefail          # Exit on error, unset var, pipe failure

# Variables
REGION="us-east-1"
NAME="${1:-default}"       # First arg or "default"
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \\
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \\
  http://169.254.169.254/latest/meta-data/instance-id)

# Conditionals
if [ -f "/etc/nginx/nginx.conf" ]; then
  echo "Nginx config exists"
elif [ -d "/etc/nginx" ]; then
  echo "Directory exists but no config"
else
  echo "Nginx not installed"
fi

# Loops
for FILE in /var/log/*.log; do
  echo "Processing: $FILE"
done

COUNT=0
while [ $COUNT -lt 3 ]; do
  echo "Attempt $COUNT"; COUNT=$((COUNT+1))
done

# Functions
log() { echo "[$(date +%FT%T)] $*"; }
log "Bootstrap starting"

# Exit codes
if command -v docker &gt;/dev/null 2&gt;&amp;1; then
  log "docker present"
else
  log "docker missing"; exit 1
fi</code></pre>
<h3>Typical EC2 UserData bootstrap</h3>
<pre><code>#!/bin/bash
dnf update -y
dnf install -y nginx
systemctl enable --now nginx
echo "&lt;h1&gt;Hello from $(hostname)&lt;/h1&gt;" &gt; /usr/share/nginx/html/index.html</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Test conditions</div><p><code>-f</code> file exists, <code>-d</code> directory exists, <code>-z</code> string empty, <code>-n</code> string not empty, <code>-eq/-ne/-lt/-gt</code> numeric comparisons.</p></div></section>

<section id="cron"><h2>Cron &amp; Scheduling</h2>
<pre><code>crontab -e                # Edit current user's crontab
crontab -l                # List cron jobs

# Format:  minute hour day month weekday  command
# ┌── min (0-59)
# │ ┌── hour (0-23)
# │ │ ┌── day of month (1-31)
# │ │ │ ┌── month (1-12)
# │ │ │ │ ┌── day of week (0-6, Sun=0)
# * * * * * /path/script.sh

0 2 * * *   /opt/backup.sh          # Every day at 02:00
*/15 * * * * /opt/healthcheck.sh    # Every 15 minutes
0 0 * * 0   /opt/weekly.sh          # Weekly, Sunday midnight
@reboot     /opt/startup.sh         # Once at boot</code></pre>
<div class="callout info"><div class="callout-title">&#9729;&#65039; systemd timers</div><p>Modern alternative to cron. List active timers with <code>systemctl list-timers</code>. Timers give logging via journald and dependency handling.</p></div></section>

<section id="logs"><h2>Logs &amp; journald</h2>
<pre><code># Traditional log files
tail -f /var/log/messages         # Amazon Linux / RHEL
tail -f /var/log/syslog           # Ubuntu / Debian
less /var/log/secure              # Auth events (RHEL family)
less /var/log/auth.log            # Auth events (Debian family)
cat /var/log/cloud-init-output.log  # UserData output on EC2

# systemd journal
journalctl -u nginx -f            # Follow one service
journalctl -u nginx --since "1 hour ago"
journalctl -xe                    # Recent entries + explanations
journalctl -p err -b              # Errors from current boot
journalctl --disk-usage           # How much space logs use</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Ship logs to CloudWatch</div><p>Install the CloudWatch agent to stream <code>/var/log/*</code> to CloudWatch Logs, then query with Logs Insights. Common on SOA-C02 monitoring scenarios.</p></div></section>

<section id="ssh"><h2>SSH &amp; EC2 Access</h2>
<pre><code># Connect to EC2
chmod 400 my-key.pem
ssh -i my-key.pem ec2-user@54.123.45.67   # Amazon Linux
ssh -i my-key.pem ubuntu@54.123.45.67     # Ubuntu

# SSH config (~/.ssh/config)
Host my-ec2
    HostName 54.123.45.67
    User ec2-user
    IdentityFile ~/.ssh/my-key.pem
# Then just: ssh my-ec2

# Copy files
scp -i key.pem file.txt ec2-user@IP:/home/ec2-user/
scp -i key.pem -r localdir/ ec2-user@IP:/tmp/

# Port forwarding (tunnel to a private RDS through a bastion)
ssh -i key.pem -L 5432:rds-endpoint:5432 ec2-user@IP

# Jump host / bastion
ssh -i key.pem -J ec2-user@BASTION ec2-user@PRIVATE_IP

# Generate a new key pair
ssh-keygen -t ed25519 -C "you@example.com"</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Prefer SSM Session Manager</div><p>AWS Systems Manager Session Manager gives shell access with <strong>no open port 22, no bastion, and no key pairs</strong> - access is controlled by IAM and fully logged. Frequently the "most secure" exam answer: <code>aws ssm start-session --target i-0abc123</code>.</p></div></section>

<section id="systemd"><h2>Systemd &amp; Services</h2>
<pre><code>systemctl start nginx        # Start now
systemctl stop nginx         # Stop now
systemctl restart nginx      # Restart
systemctl reload nginx       # Reload config without downtime
systemctl enable nginx       # Auto-start on boot
systemctl enable --now nginx # Enable and start in one step
systemctl disable nginx      # Do not start on boot
systemctl status nginx       # Current status + recent logs
systemctl is-active nginx    # Quick active check
systemctl daemon-reload      # Reload unit files after edits</code></pre>
<h3>A minimal unit file</h3>
<pre><code># /etc/systemd/system/myapp.service
[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=always
User=appuser

[Install]
WantedBy=multi-user.target</code></pre>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Why systemd matters on AWS</div><p><code>Restart=always</code> keeps your app alive after crashes, and <code>enable</code> ensures it survives instance reboots and Auto Scaling replacements.</p></div></section>

<section id="security"><h2>Security Hardening Basics</h2>
<ul>
  <li><strong>Least privilege:</strong> avoid logging in as root; use <code>sudo</code> per command.</li>
  <li><strong>Key-only SSH:</strong> disable password auth (<code>PasswordAuthentication no</code> in <code>/etc/ssh/sshd_config</code>).</li>
  <li><strong>Patch regularly:</strong> <code>dnf update -y</code> / <code>apt upgrade -y</code>, or use SSM Patch Manager.</li>
  <li><strong>Host firewall:</strong> <code>firewalld</code> (RHEL family) or <code>ufw</code> (Ubuntu) in addition to Security Groups.</li>
  <li><strong>SELinux / AppArmor:</strong> mandatory access control; check with <code>getenforce</code>.</li>
  <li><strong>Fail2ban:</strong> block repeated failed logins.</li>
</ul>
<pre><code>ufw allow 22/tcp; ufw enable        # Ubuntu firewall
firewall-cmd --add-service=https --permanent  # RHEL family
getenforce                          # SELinux mode
sudo lastb                          # Failed login attempts</code></pre>
<div class="callout warn"><div class="callout-title">&#9888; Defense in depth</div><p>Security Groups protect the network edge, but OS-level controls (firewall, SELinux, patching) matter too. Exams reward layered security answers.</p></div></section>

<section id="containers"><h2>Containers on Linux</h2>
<pre><code># Docker basics (foundation for ECS / EKS / Fargate)
docker ps                     # Running containers
docker ps -a                  # All containers
docker images                 # Local images
docker run -d -p 80:80 nginx  # Run detached, map port
docker exec -it CID /bin/bash # Shell into a container
docker logs -f CID            # Follow container logs
docker build -t myapp:1.0 .   # Build from Dockerfile
docker stop CID; docker rm CID

# Push to Amazon ECR
aws ecr get-login-password --region us-east-1 \\
  | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag myapp:1.0 ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0</code></pre>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Namespaces &amp; cgroups</div><p>Containers are just Linux processes isolated with <strong>namespaces</strong> (what they can see) and limited with <strong>cgroups</strong> (how much CPU/memory they can use). No VM involved.</p></div></section>

<section id="troubleshooting"><h2>Troubleshooting Playbook</h2>
<div class="table-wrap"><table><thead><tr><th>Symptom</th><th>First commands to run</th></tr></thead><tbody>
  <tr><td>Instance out of disk</td><td><code>df -h</code>, then <code>du -sh /* | sort -rh</code></td></tr>
  <tr><td>High CPU / slow</td><td><code>top</code>, <code>uptime</code>, <code>ps aux --sort=-%cpu | head</code></td></tr>
  <tr><td>Out of memory / OOM kills</td><td><code>free -h</code>, <code>dmesg | grep -i oom</code></td></tr>
  <tr><td>Service will not start</td><td><code>systemctl status svc</code>, <code>journalctl -u svc -xe</code></td></tr>
  <tr><td>Cannot SSH in</td><td>Check SG, NACL, subnet route, key perms, <code>/var/log/secure</code></td></tr>
  <tr><td>App cannot reach internet</td><td><code>ip route</code>, <code>curl -v</code>, check NAT/IGW route</td></tr>
  <tr><td>UserData did not run</td><td><code>cat /var/log/cloud-init-output.log</code></td></tr>
  <tr><td>Port not listening</td><td><code>ss -tulnp</code>, <code>lsof -i :PORT</code></td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; The universal first step</div><p>When something on Linux breaks, <strong>read the logs</strong>: <code>journalctl -xe</code> and <code>tail -f /var/log/...</code>. Ninety percent of issues announce themselves there.</p></div></section>
""" + chk(["Identify the distribution with cat /etc/os-release","Understand the Linux directory structure (FHS)","Navigate with cd, ls, pwd, find, tree","Know how file permissions work (rwx / octal)","Use chmod, chown, chgrp and understand umask","Understand setuid, setgid, and the sticky bit","Manage users and groups (useradd, usermod, groups)","Use sudo and understand /etc/sudoers","Process text with grep, sed, awk, cut, sort, uniq","Use pipes and redirects (|, >, >>, 2>&1, &&, ||)","Manage processes with ps, top, kill and know signals (15, 9, 1)","Check memory, CPU, and load (free, top, uptime, vmstat)","Inspect disks and mounts (df, du, lsblk, mount, /etc/fstab)","Format and mount an EBS/NVMe volume","Install packages with dnf, yum, and apt","Use networking commands (ip, ping, dig, ss, curl, traceroute)","Query IMDSv2 for instance metadata","Write a bash script with variables, conditionals, loops, functions","Use set -euo pipefail for safe scripts","Schedule tasks with cron and systemd timers","Read logs with tail -f, less, and journalctl","Connect to EC2 via SSH, SCP, tunnels, and jump hosts","Prefer SSM Session Manager over open port 22","Manage services with systemctl and write a unit file","Apply basic hardening (key-only SSH, patching, firewall, SELinux)","Run containers with Docker and push images to ECR","Follow a troubleshooting playbook for common EC2 issues"],"foundations-networking.html","Networking Fundamentals")) + FOOT
write(f"{DOCS}/foundations-linux.html", linux_html)

# ── foundations-networking.html ─────────────────────────────
net_html = HEAD("Networking Fundamentals","OSI model, TCP/IP, DNS, CIDR, subnetting, AWS VPC concepts for AWS certifications.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Foundations</span> / <span>Networking Fundamentals</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-blue">Foundations</span>
  <h1 style="margin-top:0.75rem">&#127760; Networking Fundamentals</h1>
  <p>Deep understanding of networking is essential for AWS. From the OSI model, TCP/IP, and subnetting to DNS, routing, load balancers, TLS, and full VPC connectivity - all rooted in networking fundamentals.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-green">Essential for SAA / ANS / SCS</span><span class="badge badge-blue">19 Topics</span></div>
</div></div>
""" + wrap([("osi","OSI & TCP/IP Models"),("encapsulation","Encapsulation"),("tcpip","TCP vs UDP"),("handshake","Handshake & Connections"),("ip","IP Addressing"),("cidr","CIDR & Subnetting"),("subnetex","Subnetting Worked Example"),("ipv6","IPv6"),("ports","Protocols & Ports"),("dns","DNS Deep Dive"),("dhcp","DHCP & ARP"),("nat","NAT"),("routing","Routing"),("lb","Load Balancers"),("firewalls","Firewalls & ACLs"),("tls","TLS & Certificates"),("vpc-intro","AWS VPC Overview"),("vpc-connect","VPC Connectivity"),("troubleshooting","Troubleshooting Playbook"),("checklist","Checklist")], """
<section id="osi"><h2>The OSI &amp; TCP/IP Models</h2>
<p>The OSI model is a 7-layer conceptual framework. The TCP/IP model is the 4-layer version networks actually run on. Knowing how they map helps you reason about where a problem lives.</p>
<div class="table-wrap"><table><thead><tr><th>OSI Layer</th><th>Name</th><th>Examples</th><th>TCP/IP</th><th>AWS Service</th></tr></thead><tbody>
  <tr><td>7</td><td>Application</td><td>HTTP, HTTPS, FTP, DNS</td><td>Application</td><td>API Gateway, CloudFront</td></tr>
  <tr><td>6</td><td>Presentation</td><td>SSL/TLS, JPEG, encoding</td><td>Application</td><td>ACM (TLS certs)</td></tr>
  <tr><td>5</td><td>Session</td><td>NetBIOS, RPC, sockets</td><td>Application</td><td> - </td></tr>
  <tr><td>4</td><td>Transport</td><td>TCP, UDP</td><td>Transport</td><td>NLB (Layer 4)</td></tr>
  <tr><td>3</td><td>Network</td><td>IP, ICMP, routing</td><td>Internet</td><td>VPC, Route Tables, GLB</td></tr>
  <tr><td>2</td><td>Data Link</td><td>Ethernet, MAC, ARP</td><td>Link</td><td>ENI, Direct Connect</td></tr>
  <tr><td>1</td><td>Physical</td><td>Cables, fiber, radio</td><td>Link</td><td>Direct Connect (physical)</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>ALB = Layer 7 (HTTP-aware). NLB = Layer 4 (TCP/UDP). GLB = Layer 3 (IP). This mapping is tested constantly - memorize it.</p></div></section>

<section id="encapsulation"><h2>Encapsulation</h2>
<p>As data travels down the stack, each layer wraps it with its own header. This is <strong>encapsulation</strong>; the receiver reverses it (decapsulation).</p>
<pre><code>Application data
  → + TCP header      = Segment      (Layer 4)
    → + IP header     = Packet       (Layer 3)
      → + Frame header/trailer = Frame (Layer 2)
        → bits on the wire            (Layer 1)</code></pre>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Why it matters</div><p>MTU (typically 1500 bytes) limits frame size. AWS supports <strong>jumbo frames (9001 MTU)</strong> within a VPC for higher throughput, but paths crossing the internet or some gateways fall back to 1500.</p></div></section>

<section id="tcpip"><h2>TCP vs UDP</h2>
<div class="grid-2">
  <div class="card"><h3>TCP</h3><ul><li>Connection-oriented (3-way handshake)</li><li>Reliable, ordered, retransmitted delivery</li><li>Flow control &amp; congestion control</li><li>Higher overhead</li><li>Use for: HTTP(S), SSH, FTP, SMTP, database</li></ul></div>
  <div class="card"><h3>UDP</h3><ul><li>Connectionless - fire and forget</li><li>No guarantee of delivery or order</li><li>Very low latency, minimal overhead</li><li>No congestion control</li><li>Use for: DNS, VoIP, video streaming, gaming, QUIC</li></ul></div>
</div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>NLB supports both TCP and UDP listeners. ALB is HTTP/HTTPS only. If a scenario needs UDP (gaming, IoT, DNS), the answer is NLB, not ALB.</p></div></section>

<section id="handshake"><h2>Handshake &amp; Connection Lifecycle</h2>
<pre><code>TCP 3-way handshake (open):
  Client → SYN            → Server
  Client ← SYN, ACK       ← Server
  Client → ACK            → Server
  [connection established]

TCP 4-way teardown (close):
  Client → FIN → Server
  Client ← ACK ← Server
  Client ← FIN ← Server
  Client → ACK → Server</code></pre>
<div class="callout tip"><div class="callout-title">&#128161; Debugging tip</div><p>A connection stuck in <code>SYN_SENT</code> usually means a firewall/Security Group is silently dropping the SYN. A flood of <code>TIME_WAIT</code> sockets is normal after many short-lived connections. Inspect with <code>ss -tan</code>.</p></div></section>

<section id="ip"><h2>IP Addressing</h2>
<p>A 32-bit IPv4 address written as 4 octets: <code>192.168.1.100</code>. Each address has a <strong>network</strong> portion and a <strong>host</strong> portion, determined by the subnet mask.</p>
<h3>Private IP Ranges (RFC 1918)</h3>
<pre><code>10.0.0.0/8        → 10.0.0.0    - 10.255.255.255   (common for AWS VPCs)
172.16.0.0/12     → 172.16.0.0  - 172.31.255.255   (AWS default VPC: 172.31.0.0/16)
192.168.0.0/16    → 192.168.0.0 - 192.168.255.255  (home networks)</code></pre>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>Example</th><th>Notes</th></tr></thead><tbody>
  <tr><td>Public</td><td>54.239.28.85</td><td>Routable on the internet</td></tr>
  <tr><td>Private</td><td>10.0.1.20</td><td>RFC 1918, not internet-routable</td></tr>
  <tr><td>Loopback</td><td>127.0.0.1</td><td>The local host itself</td></tr>
  <tr><td>Link-local</td><td>169.254.0.0/16</td><td>Includes IMDS at 169.254.169.254</td></tr>
</tbody></table></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; AWS Context</div><p>VPCs use private ranges. The default VPC is <code>172.31.0.0/16</code>. The special address <code>169.254.169.254</code> serves EC2 instance metadata.</p></div></section>

<section id="cidr"><h2>CIDR &amp; Subnetting</h2>
<p>CIDR notation pairs an IP with a prefix length: <code>10.0.0.0/16</code>. The prefix says how many leading bits are the network portion. Smaller prefix = bigger network.</p>
<div class="table-wrap"><table><thead><tr><th>CIDR</th><th>Subnet Mask</th><th>Total IPs</th><th>AWS Usable</th></tr></thead><tbody>
  <tr><td>/16</td><td>255.255.0.0</td><td>65,536</td><td>65,531</td></tr>
  <tr><td>/20</td><td>255.255.240.0</td><td>4,096</td><td>4,091</td></tr>
  <tr><td>/24</td><td>255.255.255.0</td><td>256</td><td>251</td></tr>
  <tr><td>/25</td><td>255.255.255.128</td><td>128</td><td>123</td></tr>
  <tr><td>/26</td><td>255.255.255.192</td><td>64</td><td>59</td></tr>
  <tr><td>/27</td><td>255.255.255.224</td><td>32</td><td>27</td></tr>
  <tr><td>/28</td><td>255.255.255.240</td><td>16</td><td>11</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Reserves 5 IPs Per Subnet</div><p>Network address (.0), VPC router (.1), Amazon DNS (.2), future use (.3), and network broadcast (last). A /24 therefore gives <strong>251</strong> usable IPs, not 254. Frequently tested!</p></div>
<pre><code># Total IPs in a block = 2^(32 - prefix)
/28 = 2^4  = 16 IPs   (11 usable in AWS)
/24 = 2^8  = 256 IPs  (251 usable in AWS)
/16 = 2^16 = 65,536 IPs
# VPC CIDR can be /16 (max) to /28 (min) in AWS</code></pre></section>

<section id="subnetex"><h2>Subnetting: Worked Example</h2>
<p>Split a VPC <code>10.0.0.0/16</code> into public and private subnets across two AZs:</p>
<div class="table-wrap"><table><thead><tr><th>Subnet</th><th>CIDR</th><th>AZ</th><th>Purpose</th><th>Usable IPs</th></tr></thead><tbody>
  <tr><td>Public A</td><td>10.0.0.0/24</td><td>us-east-1a</td><td>ALB, NAT GW</td><td>251</td></tr>
  <tr><td>Public B</td><td>10.0.1.0/24</td><td>us-east-1b</td><td>ALB, NAT GW</td><td>251</td></tr>
  <tr><td>Private A</td><td>10.0.10.0/24</td><td>us-east-1a</td><td>App servers</td><td>251</td></tr>
  <tr><td>Private B</td><td>10.0.11.0/24</td><td>us-east-1b</td><td>App servers</td><td>251</td></tr>
  <tr><td>DB A</td><td>10.0.20.0/24</td><td>us-east-1a</td><td>RDS</td><td>251</td></tr>
  <tr><td>DB B</td><td>10.0.21.0/24</td><td>us-east-1b</td><td>RDS</td><td>251</td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; Design rule</div><p>Never overlap CIDR blocks between VPCs you plan to peer or connect - overlapping ranges make routing impossible. Plan address space up front.</p></div></section>

<section id="ipv6"><h2>IPv6 Basics</h2>
<p>128-bit addresses written in hex, e.g. <code>2001:db8::1</code>. Solves IPv4 exhaustion. In AWS, IPv6 addresses are <strong>globally unique and public by default</strong> - there is no NAT for IPv6.</p>
<pre><code>::1                 # IPv6 loopback (like 127.0.0.1)
fe80::/10           # Link-local
2001:db8::/32       # Documentation range</code></pre>
<div class="callout info"><div class="callout-title">&#9729;&#65039; Egress-Only Internet Gateway</div><p>Because IPv6 has no NAT, AWS uses an <strong>Egress-Only Internet Gateway</strong> to allow outbound-only IPv6 traffic from private subnets - the IPv6 equivalent of a NAT Gateway.</p></div></section>

<section id="ports"><h2>Key Protocols &amp; Ports</h2>
<div class="table-wrap"><table><thead><tr><th>Protocol</th><th>Port</th><th>Transport</th><th>Use</th></tr></thead><tbody>
  <tr><td>HTTP</td><td>80</td><td>TCP</td><td>Web (plaintext)</td></tr>
  <tr><td>HTTPS</td><td>443</td><td>TCP</td><td>Web (TLS)</td></tr>
  <tr><td>SSH</td><td>22</td><td>TCP</td><td>Secure shell</td></tr>
  <tr><td>RDP</td><td>3389</td><td>TCP</td><td>Windows remote desktop</td></tr>
  <tr><td>DNS</td><td>53</td><td>UDP/TCP</td><td>Name resolution</td></tr>
  <tr><td>DHCP</td><td>67/68</td><td>UDP</td><td>Dynamic IP assignment</td></tr>
  <tr><td>NTP</td><td>123</td><td>UDP</td><td>Time sync</td></tr>
  <tr><td>SMTP</td><td>25/587</td><td>TCP</td><td>Email send</td></tr>
  <tr><td>MySQL/Aurora</td><td>3306</td><td>TCP</td><td>Database</td></tr>
  <tr><td>PostgreSQL</td><td>5432</td><td>TCP</td><td>Database</td></tr>
  <tr><td>Redis (ElastiCache)</td><td>6379</td><td>TCP</td><td>Cache</td></tr>
  <tr><td>NFS (EFS)</td><td>2049</td><td>TCP</td><td>Network file system</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; AWS Exam Tip</div><p>When a Security Group question involves a database, remember the port: RDS MySQL/Aurora = 3306, PostgreSQL = 5432, EFS = 2049. The SG on the DB must allow the app tier's SG on that port.</p></div></section>

<section id="dns"><h2>DNS Deep Dive</h2>
<h3>Record types</h3>
<div class="table-wrap"><table><thead><tr><th>Record</th><th>Purpose</th><th>Example</th></tr></thead><tbody>
  <tr><td>A</td><td>Name → IPv4</td><td>example.com → 93.184.216.34</td></tr>
  <tr><td>AAAA</td><td>Name → IPv6</td><td>example.com → 2606:2800::1</td></tr>
  <tr><td>CNAME</td><td>Alias to another name</td><td>www → example.com</td></tr>
  <tr><td>MX</td><td>Mail server + priority</td><td>10 mail.example.com</td></tr>
  <tr><td>TXT</td><td>Text (SPF, DKIM, verification)</td><td>"v=spf1 ..."</td></tr>
  <tr><td>NS</td><td>Name servers for a zone</td><td>ns-1.awsdns.com</td></tr>
  <tr><td>SOA</td><td>Zone authority / metadata</td><td>primary NS + serial</td></tr>
  <tr><td>Alias (Route 53)</td><td>Map apex to AWS resource</td><td>example.com → ALB DNS</td></tr>
</tbody></table></div>
<h3>How a lookup works</h3>
<pre><code>Browser → Recursive resolver → Root (.) → TLD (.com) → Authoritative NS → Answer
                                (cached along the way, controlled by TTL)</code></pre>
<h3>Route 53 routing policies</h3>
<div class="table-wrap"><table><thead><tr><th>Policy</th><th>Use</th></tr></thead><tbody>
  <tr><td>Simple</td><td>One record, no logic</td></tr>
  <tr><td>Weighted</td><td>Split traffic by percentage (A/B, canary)</td></tr>
  <tr><td>Latency</td><td>Route to lowest-latency region</td></tr>
  <tr><td>Failover</td><td>Primary/secondary with health checks</td></tr>
  <tr><td>Geolocation</td><td>Route by user's country/continent</td></tr>
  <tr><td>Geoproximity</td><td>Route by geographic distance + bias</td></tr>
  <tr><td>Multivalue</td><td>Return several healthy IPs</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; CNAME vs Alias</div><p>You <strong>cannot</strong> use a CNAME at the zone apex (naked domain like <code>example.com</code>). Use a Route 53 <strong>Alias</strong> record instead - it maps to AWS resources (ALB, CloudFront, S3) and is free of charge.</p></div></section>

<section id="dhcp"><h2>DHCP &amp; ARP</h2>
<p><strong>DHCP</strong> hands out IP configuration automatically via the DORA exchange:</p>
<pre><code>Discover → Offer → Request → Acknowledge  (client gets IP, mask, gateway, DNS)</code></pre>
<p><strong>ARP</strong> (Address Resolution Protocol) maps an IP address to a MAC address on the local link, so frames can be delivered at Layer 2.</p>
<div class="callout info"><div class="callout-title">&#9729;&#65039; DHCP Option Sets</div><p>In a VPC, AWS runs DHCP for you. <strong>DHCP Option Sets</strong> let you customize the DNS servers and domain name handed to instances - useful for hybrid setups pointing at on-prem DNS.</p></div></section>

<section id="nat"><h2>NAT Gateway vs NAT Instance</h2>
<div class="grid-2">
  <div class="card"><h3>NAT Gateway (Managed)</h3><ul><li>Fully managed, highly available within an AZ</li><li>Private subnet → internet, outbound only</li><li>Requires an Elastic IP, lives in a public subnet</li><li>Scales automatically up to 100 Gbps</li><li>No security group (it is managed)</li></ul></div>
  <div class="card"><h3>NAT Instance (Legacy)</h3><ul><li>An EC2 instance doing NAT manually</li><li>Must disable Source/Destination Check</li><li>You manage patching, sizing, and HA</li><li>Can double as a bastion host</li><li>Cheaper at tiny scale, more work</li></ul></div>
</div>
<div class="callout tip"><div class="callout-title">&#128161; HA pattern</div><p>Deploy one NAT Gateway per AZ and point each AZ's private route table at its local NAT GW. This avoids cross-AZ data charges and survives an AZ failure.</p></div></section>

<section id="routing"><h2>Routing &amp; Route Tables</h2>
<p>A route table is a set of rules matching destination CIDRs to targets. The <strong>most specific (longest prefix) match wins</strong>.</p>
<div class="table-wrap"><table><thead><tr><th>Destination</th><th>Target</th><th>Meaning</th></tr></thead><tbody>
  <tr><td>10.0.0.0/16</td><td>local</td><td>Traffic inside the VPC (always present)</td></tr>
  <tr><td>0.0.0.0/0</td><td>igw-xxxx</td><td>Default route to internet (public subnet)</td></tr>
  <tr><td>0.0.0.0/0</td><td>nat-xxxx</td><td>Default route via NAT (private subnet)</td></tr>
  <tr><td>172.16.0.0/12</td><td>pcx-xxxx</td><td>Peered VPC</td></tr>
  <tr><td>192.168.0.0/16</td><td>vgw-xxxx</td><td>On-prem via VPN/Direct Connect</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; Longest prefix match</div><p>If both <code>0.0.0.0/0</code> and <code>10.0.5.0/24</code> could match, the <code>/24</code> wins because it is more specific. This is how you steer specific traffic to a firewall appliance while everything else uses the default route.</p></div></section>

<section id="lb"><h2>Load Balancers</h2>
<div class="table-wrap"><table><thead><tr><th>Type</th><th>OSI Layer</th><th>Protocol</th><th>Best For</th></tr></thead><tbody>
  <tr><td>ALB</td><td>7</td><td>HTTP, HTTPS, gRPC</td><td>Web apps, microservices, path/host routing</td></tr>
  <tr><td>NLB</td><td>4</td><td>TCP, UDP, TLS</td><td>Ultra-low latency, static IP, gaming, IoT</td></tr>
  <tr><td>GLB</td><td>3</td><td>IP (GENEVE)</td><td>Inline virtual appliances (firewalls, IDS/IPS)</td></tr>
</tbody></table></div>
<h3>Key features</h3>
<ul>
  <li><strong>Health checks:</strong> unhealthy targets are removed from rotation automatically.</li>
  <li><strong>Target groups:</strong> route to EC2, IPs, Lambda (ALB), or other resources.</li>
  <li><strong>Cross-zone load balancing:</strong> spread traffic evenly across AZs (on by default for ALB).</li>
  <li><strong>Sticky sessions:</strong> pin a client to one target (ALB cookies).</li>
  <li><strong>ALB routing:</strong> by path (<code>/api/*</code>), host header, HTTP header, or query string.</li>
</ul>
<div class="callout warn"><div class="callout-title">&#9888; Static IP need?</div><p>Only NLB provides a static IP per AZ (and supports Elastic IPs). ALB's IPs change, so front it with a DNS name or use NLB when a fixed IP is required.</p></div></section>

<section id="firewalls"><h2>Security Groups vs Network ACLs</h2>
<div class="grid-2">
  <div class="card"><h3>Security Groups</h3><ul><li>Operate at the instance / ENI level</li><li><strong>Stateful</strong> - return traffic is auto-allowed</li><li>ALLOW rules only (no explicit deny)</li><li>All rules evaluated together</li><li>Default: deny all inbound, allow all outbound</li></ul></div>
  <div class="card"><h3>Network ACLs</h3><ul><li>Operate at the subnet level</li><li><strong>Stateless</strong> - must allow both directions</li><li>ALLOW and DENY rules</li><li>Rules evaluated in number order, lowest first</li><li>Default NACL allows all; custom NACL denies all</li></ul></div>
</div>
<div class="callout warn"><div class="callout-title">&#9888; Stateful vs stateless</div><p>Because NACLs are stateless, you must open <strong>ephemeral ports (1024-65535)</strong> for return traffic. Security Groups handle return traffic automatically. This distinction is a classic exam trap.</p></div></section>

<section id="tls"><h2>TLS &amp; Certificates</h2>
<p>TLS encrypts traffic and authenticates the server via a certificate signed by a trusted CA. The handshake negotiates keys before any application data flows.</p>
<pre><code>Client Hello → Server Hello (+ certificate)
  → key exchange → Finished → encrypted application data</code></pre>
<ul>
  <li><strong>ACM (AWS Certificate Manager):</strong> free public certs, auto-renewed, integrates with ALB, CloudFront, API Gateway.</li>
  <li><strong>TLS termination:</strong> the load balancer decrypts, so backends can serve HTTP internally.</li>
  <li><strong>End-to-end encryption:</strong> re-encrypt from LB to target when compliance requires it.</li>
  <li><strong>SNI:</strong> host multiple certs/domains on one listener.</li>
</ul>
<div class="callout tip"><div class="callout-title">&#128161; ACM region gotcha</div><p>For CloudFront, the ACM certificate <strong>must be in us-east-1</strong>, regardless of where your origin lives. For a regional ALB, the cert lives in the ALB's region.</p></div></section>

<section id="vpc-intro"><h2>AWS VPC Overview</h2>
<p>A VPC (Virtual Private Cloud) is your logically isolated network in AWS.</p>
<ul>
  <li><strong>VPC</strong> - the network boundary; a CIDR block such as <code>10.0.0.0/16</code>.</li>
  <li><strong>Subnets</strong> - subdivide the VPC; each subnet lives in exactly one AZ.</li>
  <li><strong>Internet Gateway (IGW)</strong> - enables internet access for public subnets.</li>
  <li><strong>Route Tables</strong> - control where subnet traffic is directed.</li>
  <li><strong>NAT Gateway</strong> - outbound-only internet for private subnets.</li>
  <li><strong>Elastic Network Interface (ENI)</strong> - a virtual NIC attached to instances.</li>
  <li><strong>Elastic IP (EIP)</strong> - a static public IPv4 you own.</li>
</ul>
<div class="callout tip"><div class="callout-title">&#128161; Public vs Private Subnet</div><p>A <strong>public subnet</strong> has a route <code>0.0.0.0/0 → igw-xxx</code>. A <strong>private subnet</strong> has no direct route to an IGW. The difference lives entirely in the route table.</p></div></section>

<section id="vpc-connect"><h2>VPC Connectivity Options</h2>
<div class="table-wrap"><table><thead><tr><th>Option</th><th>Connects</th><th>Notes</th></tr></thead><tbody>
  <tr><td>VPC Peering</td><td>Two VPCs</td><td>1:1, <strong>non-transitive</strong>, no overlapping CIDRs</td></tr>
  <tr><td>Transit Gateway</td><td>Many VPCs + on-prem</td><td>Hub-and-spoke, <strong>transitive</strong>, scales to thousands</td></tr>
  <tr><td>VPC Endpoint (Gateway)</td><td>VPC → S3 / DynamoDB</td><td>Free, via route table, stays on AWS network</td></tr>
  <tr><td>VPC Endpoint (Interface)</td><td>VPC → most AWS services</td><td>PrivateLink ENI, hourly + data cost</td></tr>
  <tr><td>Site-to-Site VPN</td><td>VPC ↔ on-prem</td><td>Over internet, IPsec encrypted, quick to set up</td></tr>
  <tr><td>Direct Connect (DX)</td><td>VPC ↔ on-prem</td><td>Dedicated private link, consistent low latency</td></tr>
  <tr><td>PrivateLink</td><td>Consumer VPC → provider service</td><td>Expose a service privately without peering</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; Peering is not transitive</div><p>If VPC A peers with B, and B peers with C, A <strong>cannot</strong> reach C through B. For any-to-any connectivity at scale, use a Transit Gateway.</p></div>
<div class="callout info"><div class="callout-title">&#9729;&#65039; VPN + DX</div><p>A common resilient hybrid design: primary connectivity over Direct Connect for performance, with a Site-to-Site VPN as an encrypted failover path.</p></div></section>

<section id="troubleshooting"><h2>Connectivity Troubleshooting Playbook</h2>
<div class="table-wrap"><table><thead><tr><th>Symptom</th><th>Check in this order</th></tr></thead><tbody>
  <tr><td>Cannot SSH/RDP to instance</td><td>Security Group inbound → NACL → route table → key/user → OS firewall</td></tr>
  <tr><td>Instance has no internet (public)</td><td>Public IP assigned? IGW attached? Route <code>0.0.0.0/0 → igw</code>? SG outbound?</td></tr>
  <tr><td>Private instance no outbound</td><td>NAT Gateway healthy? Route <code>0.0.0.0/0 → nat</code>? NAT in a public subnet?</td></tr>
  <tr><td>Cannot reach RDS</td><td>DB Security Group allows app SG on 3306/5432? Same VPC / peered? Subnet route?</td></tr>
  <tr><td>DNS not resolving</td><td>VPC <code>enableDnsSupport</code> &amp; <code>enableDnsHostnames</code>? Resolver at .2? <code>dig</code> output</td></tr>
  <tr><td>Peered VPC unreachable</td><td>Routes on both sides? Non-overlapping CIDRs? SG/NACL allow peer CIDR?</td></tr>
  <tr><td>Intermittent packet loss</td><td>MTU mismatch (jumbo frames)? Check with <code>ping -M do -s 8972</code></td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; Use VPC tooling</div><p><strong>VPC Reachability Analyzer</strong> traces the configured path between two resources and tells you exactly which SG, NACL, or route blocks it. <strong>VPC Flow Logs</strong> show ACCEPT/REJECT per flow - invaluable for diagnosing silent drops.</p></div></section>
""" + chk(["Map the 7 OSI layers to the 4 TCP/IP layers","Explain encapsulation and MTU / jumbo frames","Explain the difference between TCP and UDP","Describe the TCP 3-way handshake and connection states","Identify private IP ranges (RFC 1918) and special addresses","Calculate the number of IPs in a CIDR block","Know why AWS reserves 5 IPs per subnet","Design a multi-AZ public/private subnet layout without overlaps","Understand IPv6 basics and the Egress-Only Internet Gateway","Know common ports: 22, 80, 443, 53, 3306, 5432, 2049, 3389","Explain DNS record types: A, AAAA, CNAME, MX, TXT, NS, Alias","Describe how a recursive DNS lookup works and the role of TTL","Compare Route 53 routing policies (weighted, latency, failover, geo)","Explain CNAME vs Alias and the zone apex rule","Understand DHCP (DORA) and ARP","Explain NAT Gateway vs NAT Instance and the per-AZ HA pattern","Read a route table and apply longest-prefix match","Explain ALB vs NLB vs GLB and their layers","Explain Security Groups vs Network ACLs (stateful vs stateless)","Understand ephemeral ports for stateless NACL return traffic","Understand TLS handshake, ACM, and TLS termination","Know the CloudFront us-east-1 certificate requirement","Understand core VPC components: IGW, route tables, subnets, ENI, EIP","Compare VPC Peering, Transit Gateway, and VPC Endpoints","Explain Site-to-Site VPN vs Direct Connect and hybrid failover","Know that VPC Peering is non-transitive","Use Reachability Analyzer and VPC Flow Logs to troubleshoot"],"clf-c02.html","Cloud Practitioner (CLF-C02)")) + FOOT
write(f"{DOCS}/foundations-networking.html", net_html)

# ── resources.html ──────────────────────────────────────────
res_html = HEAD("Resources","All AWS certification study resources: Skill Builder, Stephane Maarek, Tutorials Dojo, Adrian Cantrill, whitepapers, YouTube channels.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Resources</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-teal">Study Resources</span>
  <h1 style="margin-top:0.75rem">&#128279; All Study Resources</h1>
  <p>Hand-picked, trusted resources used by thousands of AWS certified professionals. Official AWS content first, best community resources second.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-green">Official AWS Sources First</span><span class="badge badge-blue">50+ Curated Links</span></div>
</div></div>
<div class="container" style="padding-bottom:4rem"><div class="doc-layout">
<aside class="sidebar"><h4>Contents</h4>
  <a href="#skill-builder">AWS Skill Builder</a>
  <a href="#official-guides">Official Exam Guides</a>
  <a href="#stephane">Stephane Maarek</a>
  <a href="#tutorials-dojo">Tutorials Dojo</a>
  <a href="#adrian">Adrian Cantrill</a>
  <a href="#free">Free Resources</a>
  <a href="#whitepapers">Whitepapers</a>
  <a href="#youtube">YouTube</a>
  <a href="#communities">Communities</a>
</aside>
<main>

<section id="skill-builder"><h2>&#127891; AWS Skill Builder (Official - FREE)</h2>
<div class="callout tip"><div class="callout-title">&#128161; Best Free Resource</div><p>AWS Skill Builder is the official AWS training platform with hundreds of free digital courses, official practice question sets, and hands-on labs. <strong>Always start here.</strong></p></div>
<div class="table-wrap"><table><thead><tr><th>Course</th><th>Cert</th><th>Link</th></tr></thead><tbody>
  <tr><td>AWS Cloud Practitioner Essentials</td><td>CLF-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials" target="_blank">Free Course &#8594;</a></td></tr>
  <tr><td>AWS Cloud Quest: Cloud Practitioner (gamified!)</td><td>CLF-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/11458/aws-cloud-quest-cloud-practitioner" target="_blank">Free Game &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: CLF-C02</td><td>CLF-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/16434/exam-prep-official-practice-question-set-aws-certified-cloud-practitioner-clf-c02-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: SAA-C03</td><td>SAA-C03</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/1044/aws-certified-solutions-architect-associate-official-practice-question-set-saa-c03-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: DVA-C02</td><td>DVA-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/14161/aws-certified-developer-associate-official-practice-question-set-dva-c02-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: SOA-C02</td><td>SOA-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/1573/aws-certified-sysops-administrator-associate-official-practice-question-set-soa-c02-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: SAP-C02</td><td>SAP-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/1313/aws-certified-solutions-architect-professional-official-practice-question-set-sap-c02-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: DOP-C02</td><td>DOP-C02</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/16408/aws-certified-devops-engineer-professional-official-practice-question-set-dop-c02-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Official Practice Questions: MLS-C01</td><td>MLS-C01</td><td><a href="https://explore.skillbuilder.aws/learn/course/external/view/elearning/1340/aws-certified-machine-learning-specialty-official-practice-question-set-mls-c01-english" target="_blank">Free &#8594;</a></td></tr>
  <tr><td>Browse All Courses</td><td>All</td><td><a href="https://explore.skillbuilder.aws/" target="_blank">Skill Builder &#8594;</a></td></tr>
</tbody></table></div></section>

<section id="official-guides"><h2>&#128196; Official Exam Guides &amp; Sample Questions</h2>
<p>Read the official exam guide PDF before anything else. It tells you exactly what domains and topics are tested.</p>
<div class="table-wrap"><table><thead><tr><th>Certification</th><th>Exam Guide</th><th>Sample Questions</th></tr></thead><tbody>
  <tr><td>CLF-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-cloud-practitioner/AWS-Certified-Cloud-Practitioner_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-cloud-practitioner/AWS-Certified-Cloud-Practitioner_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>SAA-C03</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>DVA-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-dev-associate/AWS-Certified-Developer-Associate_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-dev-associate/AWS-Certified-Developer-Associate_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>SOA-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sysops-associate/AWS-Certified-SysOps-Administrator-Associate_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sysops-associate/AWS-Certified-SysOps-Administrator-Associate_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>SAP-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-sa-pro/AWS-Certified-Solutions-Architect-Professional_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>DOP-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-devops-pro/AWS-Certified-DevOps-Engineer-Professional_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>SCS-C02</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-security-spec/AWS-Certified-Security-Specialty_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-security-spec/AWS-Certified-Security-Specialty_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>ANS-C01</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS-Certified-Advanced-Networking-Specialty_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-advnetworking-spec/AWS-Certified-Advanced-Networking-Specialty_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>MLS-C01</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-ml/AWS-Certified-Machine-Learning-Specialty_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-ml/AWS-Certified-Machine-Learning-Specialty_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
  <tr><td>DAS-C01</td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-data-analytics-specialty/AWS-Certified-Data-Analytics-Specialty_Exam-Guide.pdf" target="_blank">PDF &#8594;</a></td><td><a href="https://d1.awsstatic.com/training-and-certification/docs-data-analytics-specialty/AWS-Certified-Data-Analytics-Specialty_Sample-Questions.pdf" target="_blank">PDF &#8594;</a></td></tr>
</tbody></table></div></section>

<section id="stephane"><h2>&#11088; Stephane Maarek - #1 Udemy Instructor</h2>
<div class="callout info"><div class="callout-title">Why Stephane?</div><p>Stephane Maarek is the #1 rated AWS instructor on Udemy with 1M+ students and 12 AWS certifications himself. His courses are incredibly detailed, well-organized, and regularly updated. The single most recommended resource on r/AWSCertifications.</p></div>
<div class="callout tip"><div class="callout-title">&#128161; Udemy Sales Tip</div><p>Never pay full price. Udemy runs sales constantly - courses often go for $10-15. Wait for a sale notification or check on a weekday.</p></div>
<div class="table-wrap"><table><thead><tr><th>Course</th><th>Cert</th><th>Link</th></tr></thead><tbody>
  <tr><td>Ultimate AWS Certified Cloud Practitioner</td><td>CLF-C02</td><td><a href="https://www.udemy.com/course/aws-certified-cloud-practitioner-new/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified Solutions Architect Associate</td><td>SAA-C03</td><td><a href="https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified Developer Associate</td><td>DVA-C02</td><td><a href="https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified SysOps Administrator</td><td>SOA-C02</td><td><a href="https://www.udemy.com/course/ultimate-aws-certified-sysops-administrator-associate/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified Solutions Architect Professional</td><td>SAP-C02</td><td><a href="https://www.udemy.com/course/aws-solutions-architect-professional/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified DevOps Engineer Professional</td><td>DOP-C02</td><td><a href="https://www.udemy.com/course/aws-certified-devops-engineer-professional-hands-on/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>Ultimate AWS Certified Security Specialty</td><td>SCS-C02</td><td><a href="https://www.udemy.com/course/ultimate-aws-certified-security-specialty/" target="_blank" rel="noopener">View &#8594;</a></td></tr>
  <tr><td>All courses &amp; practice exams</td><td>All</td><td><a href="https://www.udemy.com/user/stephane-maarek/" target="_blank" rel="noopener">Profile &#8594;</a></td></tr>
</tbody></table></div></section>

<section id="tutorials-dojo"><h2>&#128221; Tutorials Dojo - Best Practice Exams</h2>
<div class="callout tip"><div class="callout-title">&#128161; The Practice Exam Standard</div><p>Tutorials Dojo by Jon Bonso is the gold standard for AWS practice exams. If you're consistently scoring <strong>75%+ on Tutorials Dojo, you're ready to book the real exam.</strong></p></div>
<div class="grid-2">
  <div class="card"><h3>Free Cheat Sheets</h3><p>Comprehensive cheat sheets for every AWS service. Excellent quick reference during final study days.</p><a href="https://tutorialsdojo.com/aws-cheat-sheets/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.85rem">Free Cheat Sheets &#8594;</a></div>
  <div class="card"><h3>Practice Exams (Paid)</h3><p>Timed and review modes. Detailed explanations for every answer. Updated regularly.</p><a href="https://tutorialsdojo.com/courses/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.85rem">Practice Exams &#8594;</a></div>
</div></section>

<section id="adrian"><h2>&#127919; Adrian Cantrill - Deep-Dive Technical Courses</h2>
<div class="card">
  <p>Adrian Cantrill's courses at <a href="https://learn.cantrill.io/" target="_blank">learn.cantrill.io</a> are famous for extraordinary depth, beautiful animated diagrams, and technical accuracy. If you want to truly <em>understand</em> AWS (not just pass), Adrian is the best for SAA and SAP.</p>
  <div class="grid-2" style="margin-top:1rem">
    <div><h4>What makes Adrian different:</h4><ul><li>Hours of animated architecture diagrams</li><li>Scenario-based hands-on labs</li><li>Extremely deep technical detail</li><li>Active Discord community</li></ul></div>
    <div><h4>Available Courses:</h4><ul>
      <li><a href="https://learn.cantrill.io/p/aws-certified-solutions-architect-associate-saa-c03" target="_blank">SAA-C03</a></li>
      <li><a href="https://learn.cantrill.io/p/aws-certified-solutions-architect-professional" target="_blank">SAP-C02</a></li>
      <li><a href="https://learn.cantrill.io/p/aws-certified-developer-associate" target="_blank">DVA-C02</a></li>
      <li><a href="https://learn.cantrill.io/p/aws-certified-advanced-networking-specialty" target="_blank">ANS-C01</a></li>
    </ul></div>
  </div>
</div></section>

<section id="free"><h2>&#127358; Top Free Resources</h2>
<div class="grid-3">
  <div class="card"><div class="card-icon">&#127968;</div><h3>AWS Well-Architected Labs</h3><p>Official hands-on labs for each WA pillar.</p><a href="https://www.wellarchitectedlabs.com/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Start Labs &#8594;</a></div>
  <div class="card"><div class="card-icon">&#127947;</div><h3>AWS Workshops</h3><p>200+ official and community workshops for specific AWS services.</p><a href="https://workshops.aws/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Browse &#8594;</a></div>
  <div class="card"><div class="card-icon">&#127358;</div><h3>AWS Free Tier</h3><p>Practice with real AWS. 750hrs EC2 t3.micro, 5GB S3, 1M Lambda invocations/month.</p><a href="https://aws.amazon.com/free/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Start Free &#8594;</a></div>
  <div class="card"><div class="card-icon">&#128250;</div><h3>freeCodeCamp (Andrew Brown)</h3><p>Full free CLF, SAA, DVA courses on YouTube. 12-hour complete courses.</p><a href="https://www.youtube.com/@freecodecamp" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Watch &#8594;</a></div>
  <div class="card"><div class="card-icon">&#128217;</div><h3>Digital Cloud Training</h3><p>Neal Davis's free AWS cheat sheets and practice questions.</p><a href="https://digitalcloud.training/aws-cheat-sheets/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Cheat Sheets &#8594;</a></div>
  <div class="card"><div class="card-icon">&#127760;</div><h3>AWS Documentation</h3><p>Official service documentation - always the most accurate source.</p><a href="https://docs.aws.amazon.com/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Read Docs &#8594;</a></div>
</div></section>

<section id="whitepapers"><h2>&#128220; Must-Read AWS Whitepapers</h2>
<div class="table-wrap"><table><thead><tr><th>Whitepaper</th><th>Relevant For</th><th>Link</th></tr></thead><tbody>
  <tr><td>AWS Well-Architected Framework</td><td>All certs</td><td><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html" target="_blank">Read &#8594;</a></td></tr>
  <tr><td>Security Pillar</td><td>SCS-C02, SAP-C02</td><td><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html" target="_blank">Read &#8594;</a></td></tr>
  <tr><td>AWS Overview of Security Processes</td><td>SCS-C02, CLF-C02</td><td><a href="https://d1.awsstatic.com/whitepapers/Security/AWS_Security_Whitepaper.pdf" target="_blank">Read &#8594;</a></td></tr>
  <tr><td>AWS Disaster Recovery</td><td>SAA-C03, SAP-C02</td><td><a href="https://d1.awsstatic.com/whitepapers/aws-disaster-recovery.pdf" target="_blank">Read &#8594;</a></td></tr>
  <tr><td>Big Data Analytics Options on AWS</td><td>DAS-C01</td><td><a href="https://d1.awsstatic.com/whitepapers/Big_Data_Analytics_Options_on_AWS.pdf" target="_blank">Read &#8594;</a></td></tr>
</tbody></table></div></section>

<section id="youtube"><h2>&#9654;&#65039; YouTube Channels</h2>
<div class="grid-3">
  <div class="card"><h3>AWS Official</h3><p>Service launches, re:Invent talks, tutorials, architecture deep-dives.</p><a href="https://www.youtube.com/@amazonwebservices" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Subscribe &#8594;</a></div>
  <div class="card"><h3>Be a Better Dev</h3><p>Bite-sized AWS service explanations. Great for quick refreshers before the exam.</p><a href="https://www.youtube.com/@BeABetterDev" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Watch &#8594;</a></div>
  <div class="card"><h3>NetworkChuck</h3><p>Networking and cloud fundamentals in an engaging, beginner-friendly way.</p><a href="https://www.youtube.com/@NetworkChuck" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Watch &#8594;</a></div>
</div></section>

<section id="communities"><h2>&#129309; Communities</h2>
<div class="grid-3">
  <div class="card"><h3>Reddit r/AWSCertifications</h3><p>Most active community for AWS cert tips, pass/fail posts, and resource recommendations.</p><a href="https://www.reddit.com/r/AWSCertifications/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Join &#8594;</a></div>
  <div class="card"><h3>AWS re:Post</h3><p>Official AWS community Q&amp;A forum. Get answers from AWS experts.</p><a href="https://repost.aws/" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Join &#8594;</a></div>
  <div class="card"><h3>This Hub on GitHub</h3><p>Star, contribute, open issues, or add resources!</p><a href="https://github.com/motoraif/aws-study-hub" target="_blank" class="btn btn-outline" style="margin-top:0.75rem;font-size:0.82rem">Contribute &#8594;</a></div>
</div></section>

</main></div></div>
""" + FOOT
write(f"{DOCS}/resources.html", res_html)

# ── labs.html ───────────────────────────────────────────────
labs_html = HEAD("Practice Labs & Questions","Free AWS hands-on labs, practice questions with answers, architecture challenges, and exam strategies.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Labs &amp; Practice</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-green">Practice &amp; Labs</span>
  <h1 style="margin-top:0.75rem">&#129514; Practice Labs &amp; Exam Questions</h1>
  <p>Hands-on labs, practice questions with answers, architecture challenges, and proven exam strategies.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-green">Free Labs</span><span class="badge badge-blue">Practice Questions + Answers</span><span class="badge badge-orange">Architecture Challenges</span></div>
</div></div>
<div class="container" style="padding-bottom:4rem"><div class="doc-layout">
<aside class="sidebar"><h4>Contents</h4>
  <a href="#lab-platforms">Free Lab Platforms</a>
  <a href="#questions">Practice Questions</a>
  <a href="#arch">Architecture Challenges</a>
  <a href="#strategy">Exam Strategy</a>
  <a href="#patterns">Question Patterns</a>
  <a href="#lab-checklist">Lab Checklist</a>
</aside>
<main>

<section id="lab-platforms"><h2>&#127358; Free Hands-On Lab Platforms</h2>
<div class="grid-2">
  <div class="card" style="border-color:var(--aws-orange)"><h3>&#129351; AWS Free Tier</h3><p>Practice in a real AWS account:</p><ul><li>750 hrs/month EC2 t3.micro</li><li>5 GB S3 storage</li><li>750 hrs RDS (MySQL/PostgreSQL)</li><li>1 million Lambda invocations/month</li><li>25 GB DynamoDB storage</li></ul><a href="https://aws.amazon.com/free/" target="_blank" class="btn btn-primary" style="margin-top:1rem;font-size:0.85rem">Create Free Account &#8594;</a></div>
  <div class="card"><h3>&#127891; AWS Skill Builder Labs</h3><p>Official guided labs in real AWS accounts. No credit card needed for sandbox environments.</p><ul><li>Step-by-step instructions</li><li>Temporary AWS sandbox</li><li>Covers most certification topics</li><li>Requires Skill Builder subscription ($29/mo)</li></ul><a href="https://explore.skillbuilder.aws/" target="_blank" class="btn btn-outline" style="margin-top:1rem;font-size:0.85rem">Access Labs &#8594;</a></div>
  <div class="card"><h3>&#127968; AWS Well-Architected Labs</h3><p>Free official labs for each WA pillar: Security, Reliability, Performance, Cost, Operations, Sustainability.</p><a href="https://www.wellarchitectedlabs.com/" target="_blank" class="btn btn-outline" style="margin-top:1rem;font-size:0.85rem">Start Labs &#8594;</a></div>
  <div class="card"><h3>&#127947; AWS Workshops</h3><p>200+ community and official workshops for specific services. EKS Workshop, Serverless Workshop, Security Workshop, and more.</p><a href="https://workshops.aws/" target="_blank" class="btn btn-outline" style="margin-top:1rem;font-size:0.85rem">Browse &#8594;</a></div>
  <div class="card"><h3>&#128039; LocalStack</h3><p>Run AWS services locally on your machine. Free tier covers S3, Lambda, DynamoDB, SQS, SNS, IAM. No AWS account needed.</p><a href="https://localstack.cloud/" target="_blank" class="btn btn-outline" style="margin-top:1rem;font-size:0.85rem">Get LocalStack &#8594;</a></div>
  <div class="card"><h3>&#128218; ExamPro (Andrew Brown)</h3><p>Free AWS courses on freeCodeCamp YouTube. Full CLF, SAA, DVA courses in one video each.</p><a href="https://www.youtube.com/@ExamProChannel" target="_blank" class="btn btn-outline" style="margin-top:1rem;font-size:0.85rem">Watch &#8594;</a></div>
</div></section>

<section id="questions"><h2>&#128221; Practice Questions</h2>
<div class="callout info"><div class="callout-title">How to Use These</div><p>Cover the answers, think through your answer first, then reveal and read the explanation - especially for wrong answers. Understanding <em>why</em> wrong answers are wrong is just as important.</p></div>

<h3>CLF-C02 Questions</h3>
<div class="card" style="margin-bottom:1rem"><p><strong>Q1.</strong> A company needs to run a workload that can be interrupted and restarted without data loss. It must complete within 24 hours. Which EC2 pricing option provides the most cost savings?</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Reveal Answer</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px">
<p><strong>&#9989; Spot Instances</strong></p><p>Up to 90% discount over On-Demand. Since the workload can be interrupted (and restarted), and has a 24-hour window, Spot is perfect. On-Demand is most expensive. Reserved requires 1-3 year commitment. Savings Plans apply to consistent usage.</p>
</div></details></div>

<div class="card" style="margin-bottom:1rem"><p><strong>Q2.</strong> Under the AWS Shared Responsibility Model, which is the customer's responsibility when using Amazon RDS?<br>A) Patching the database engine &nbsp; B) Managing the underlying EC2 instances &nbsp; C) Configuring security groups and network access &nbsp; D) Replacing failed storage hardware</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Reveal Answer</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px">
<p><strong>&#9989; C) Configuring security groups and network access</strong></p><p>With managed services like RDS, AWS handles: OS patching, DB engine patches, hardware replacement. The customer is responsible for: security groups, NACLs, IAM, encryption settings, backup configuration, and the data itself.</p>
</div></details></div>

<h3>SAA-C03 Questions</h3>
<div class="card" style="margin-bottom:1rem"><p><strong>Q3.</strong> A web application experiences high read traffic on its MySQL database. The team wants to improve performance without changing application code. What is the MOST cost-effective solution?<br>A) Migrate to Aurora &nbsp; B) Add RDS Read Replicas &nbsp; C) Use ElastiCache &nbsp; D) Enable Multi-AZ</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Reveal Answer</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px">
<p><strong>&#9989; B) Add RDS Read Replicas</strong></p><p>Read Replicas offload read traffic. No app code changes needed if configured at the connection string level. ElastiCache (C) requires app code changes to check cache first. Multi-AZ (D) is for HA, not performance - standby is not readable. Aurora (A) requires migration effort.</p>
</div></details></div>

<div class="card" style="margin-bottom:1rem"><p><strong>Q4.</strong> A company wants S3 objects accessible ONLY through CloudFront, not directly via S3 URL. What should they configure?<br>A) S3 bucket ACL = private &nbsp; B) CloudFront Signed URLs &nbsp; C) Origin Access Control (OAC) &nbsp; D) S3 Transfer Acceleration</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Reveal Answer</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px">
<p><strong>&#9989; C) Origin Access Control (OAC)</strong></p><p>OAC restricts S3 bucket access so only CloudFront can read it. The bucket policy is updated to allow only the CloudFront service principal. Signed URLs (B) restrict who can access CloudFront content, not how CloudFront accesses S3.</p>
</div></details></div>

<h3>DVA-C02 Questions</h3>
<div class="card" style="margin-bottom:1rem"><p><strong>Q5.</strong> A Lambda function has S3 read permission in its IAM role. It gets AccessDenied on an S3 bucket that has a bucket policy with an explicit Deny all. Why?</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Reveal Answer</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px">
<p><strong>&#9989; The explicit Deny in the bucket policy overrides the Allow in the IAM role.</strong></p><p>IAM evaluation order: an <strong>explicit Deny always wins</strong>, regardless of any Allow policies. The bucket policy must be updated to remove the explicit Deny or add an exception for the Lambda execution role ARN. This is one of the most tested IAM concepts.</p>
</div></details></div>

<div class="callout tip"><div class="callout-title">&#128161; Want 500+ More Practice Questions?</div><p>Visit <a href="https://tutorialsdojo.com/" target="_blank">Tutorials Dojo</a> for the most realistic practice exams per certification, or use the official <a href="https://explore.skillbuilder.aws/" target="_blank">AWS Skill Builder</a> practice question sets.</p></div></section>

<section id="arch"><h2>&#127959; Architecture Challenges</h2>
<p>Try designing these architectures yourself before looking at the solution. Use <a href="https://draw.io" target="_blank">draw.io</a> or paper.</p>

<div class="card" style="margin-bottom:1rem"><h3>Challenge 1: Three-Tier Web Application (SAA level)</h3>
<p><strong>Requirements:</strong> Highly available, fault-tolerant, auto-scaling web app. Web tier, application tier, MySQL database. Handles 10,000 concurrent users. RTO &lt; 1 hour.</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Show Reference Architecture</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px"><pre><code>Internet → Route 53 → CloudFront (CDN)
                           ↓
               Application Load Balancer (Multi-AZ)
                  ↙              ↘
         AZ-A                    AZ-B
    EC2 Auto Scaling         EC2 Auto Scaling (Web Tier)
         ↓                         ↓
    EC2 Auto Scaling         EC2 Auto Scaling (App Tier)
         ↓                         ↓
    RDS MySQL Multi-AZ Primary ←→ RDS Standby
         ↓
    ElastiCache (session store)
    S3 (static assets) + Secrets Manager (DB credentials)</code></pre></div></details></div>

<div class="card" style="margin-bottom:1rem"><h3>Challenge 2: Serverless Event-Driven Pipeline (DVA level)</h3>
<p><strong>Requirements:</strong> Users upload images to S3. Auto-resize to 3 thumbnail sizes, store metadata in DynamoDB, notify subscribers. Handle 1000 uploads/minute.</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Show Reference Architecture</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px"><pre><code>S3 PutObject Event
       ↓
Lambda (Image Processor)
   → Resize to 3 sizes → Store thumbnails in S3
   → Write metadata to DynamoDB
   → Publish to SNS Topic
          ↓
    ┌─────┼──────┐
   SQS   Email  Lambda (webhook)
  Queue  Sub
    ↓
  Lambda (downstream processing)

DLQ attached to Lambda for failed events
X-Ray tracing enabled + CloudWatch alarms on errors</code></pre></div></details></div>

<div class="card" style="margin-bottom:1rem"><h3>Challenge 3: Disaster Recovery (SAP level)</h3>
<p><strong>Requirements:</strong> Financial app in us-east-1. RTO &lt; 15 min, RPO &lt; 5 min. Data must stay in US regions. Moderate budget.</p>
<details style="margin-top:0.75rem"><summary style="cursor:pointer;color:var(--aws-orange);font-weight:600">Show Reference Architecture</summary>
<div style="margin-top:0.75rem;padding:1rem;background:var(--bg-hover);border-radius:8px"><pre><code>Strategy: Warm Standby (meets RTO 15 min, RPO 5 min within budget)

Primary (us-east-1):
  ALB → EC2 ASG (full scale) → RDS MySQL Multi-AZ
  Route 53 Failover routing (health check on ALB)

DR (us-west-2):
  ALB → EC2 ASG (2 instances - warm) → RDS Read Replica
  (async replication ~5 min lag = RPO ✓)

Failover:
1. Route 53 detects unhealthy primary (60s TTL)
2. DNS fails over to us-west-2 ALB
3. Read Replica promoted to primary (2-3 min)
4. ASG scales up in us-west-2 (5-10 min)
Total RTO: ~10-15 minutes ✓</code></pre></div></details></div></section>

<section id="strategy"><h2>&#127919; Exam Strategy</h2>
<div class="grid-2">
  <div class="card"><h3>Before the Exam</h3><ul><li>Score 75%+ on Tutorials Dojo before booking</li><li>Review all wrong answers - understand WHY they're wrong</li><li>Read the official exam guide domains the week before</li><li>Review your weak areas using our cert checklists</li><li>Get a good night's sleep - don't cram the night before</li></ul></div>
  <div class="card"><h3>During the Exam</h3><ul><li>Read every word - key qualifiers matter</li><li>Look for: "MOST cost-effective", "LEAST operational overhead"</li><li>Eliminate obviously wrong answers first</li><li>Flag difficult questions and return later</li><li>Trust your first instinct - don't second-guess without reason</li></ul></div>
</div></section>

<section id="patterns"><h2>&#128218; Question Pattern Recognition</h2>
<div class="table-wrap"><table><thead><tr><th>If the question says...</th><th>Think about...</th></tr></thead><tbody>
  <tr><td>"MOST cost-effective" / "cheapest"</td><td>Spot, Reserved, Savings Plans, S3 Glacier, serverless, Fargate Spot</td></tr>
  <tr><td>"LEAST operational overhead" / "fully managed"</td><td>RDS, Lambda, Fargate, DynamoDB, ElastiCache, Aurora Serverless</td></tr>
  <tr><td>"highly available" across AZs</td><td>Multi-AZ RDS, ALB, EFS, DynamoDB Global Tables, ASG multi-AZ</td></tr>
  <tr><td>"decoupled" / "loose coupling"</td><td>SQS, SNS, EventBridge, Step Functions</td></tr>
  <tr><td>"near real-time analytics"</td><td>Kinesis Data Streams, Kinesis Analytics, OpenSearch</td></tr>
  <tr><td>"millions of users" / "global"</td><td>CloudFront, Global Accelerator, Route 53 latency, DynamoDB Global Tables</td></tr>
  <tr><td>"compliance" / "audit"</td><td>CloudTrail, Config, Macie, Security Hub, Artifact</td></tr>
  <tr><td>"temporary credentials"</td><td>STS AssumeRole, IAM Roles, Cognito Identity Pools</td></tr>
  <tr><td>"on-premises to AWS"</td><td>Site-to-Site VPN, Direct Connect, DataSync, DMS, MGN, Snowball</td></tr>
  <tr><td>"encrypt existing unencrypted EBS"</td><td>Snapshot → Copy snapshot with encryption → New volume from encrypted snapshot</td></tr>
</tbody></table></div></section>

<section id="lab-checklist" class="progress-section"><h2>&#129514; Hands-On Lab Checklist</h2>
<div class="progress-wrap"><div class="progress-label"><span>Labs Completed</span><span class="progress-pct">0%</span></div><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div></div>
<h3>Core Labs (Do These First)</h3>
<ul class="checklist">
  <li><input type="checkbox"><span>Launch an EC2 instance, SSH in, install nginx, configure Security Groups</span></li>
  <li><input type="checkbox"><span>Create an S3 bucket, upload files, enable versioning, configure lifecycle policy</span></li>
  <li><input type="checkbox"><span>Create a VPC with public + private subnets, IGW, NAT Gateway, route tables</span></li>
  <li><input type="checkbox"><span>Launch RDS MySQL in private subnet, connect from EC2 in public subnet</span></li>
  <li><input type="checkbox"><span>Create a Lambda function triggered by S3 upload</span></li>
  <li><input type="checkbox"><span>Set up an ALB with 2 EC2 targets in different AZs</span></li>
  <li><input type="checkbox"><span>Configure Auto Scaling Group with target tracking scaling policy</span></li>
  <li><input type="checkbox"><span>Create IAM roles and test with STS assume-role cross-account</span></li>
  <li><input type="checkbox"><span>Deploy a CloudFormation stack with EC2, SG, and outputs</span></li>
  <li><input type="checkbox"><span>Set up CloudWatch alarms and send SNS notifications</span></li>
</ul>
<h3>Intermediate Labs</h3>
<ul class="checklist">
  <li><input type="checkbox"><span>Deploy a serverless app: API Gateway + Lambda + DynamoDB</span></li>
  <li><input type="checkbox"><span>Set up SQS queue with Lambda consumer and DLQ</span></li>
  <li><input type="checkbox"><span>Configure S3 Cross-Region Replication</span></li>
  <li><input type="checkbox"><span>Set up CloudFront distribution with S3 origin and OAC</span></li>
  <li><input type="checkbox"><span>Implement SSM Session Manager for SSH-less EC2 access</span></li>
  <li><input type="checkbox"><span>Enable CloudTrail and query logs with Athena</span></li>
  <li><input type="checkbox"><span>Configure KMS customer-managed key and encrypt EBS volume</span></li>
  <li><input type="checkbox"><span>Deploy a container on ECS Fargate with ECR image</span></li>
  <li><input type="checkbox"><span>Create a CodePipeline: CodeCommit → CodeBuild → CodeDeploy</span></li>
  <li><input type="checkbox"><span>Configure Route 53 failover routing with health checks</span></li>
</ul>
<h3>Advanced Labs</h3>
<ul class="checklist">
  <li><input type="checkbox"><span>Set up VPC Peering between two VPCs and test connectivity</span></li>
  <li><input type="checkbox"><span>Configure Transit Gateway with 3 VPCs and route table segmentation</span></li>
  <li><input type="checkbox"><span>Set up Kinesis Data Streams with Lambda consumer and error handling</span></li>
  <li><input type="checkbox"><span>Train a SageMaker ML model with built-in XGBoost algorithm</span></li>
  <li><input type="checkbox"><span>Build a Glue ETL pipeline: S3 CSV → Parquet → Athena query</span></li>
  <li><input type="checkbox"><span>Implement GuardDuty + EventBridge + Lambda auto-remediation</span></li>
  <li><input type="checkbox"><span>Deploy multi-region active-passive with Route 53 failover</span></li>
  <li><input type="checkbox"><span>Configure cross-account IAM role and use from another account</span></li>
  <li><input type="checkbox"><span>Set up AWS Config rules with automatic SSM remediation</span></li>
  <li><input type="checkbox"><span>Deploy a CDK stack to create infrastructure from Python code</span></li>
</ul></section>

</main></div></div>
""" + FOOT
write(f"{DOCS}/labs.html", labs_html)

# ── quiz.html ───────────────────────────────────────────────
quiz_html = HEAD("Practice Quiz","Interactive AWS certification practice quiz with instant scoring, domain breakdown, and explanations. Free and open source.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Practice Quiz</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-green">Interactive</span>
  <h1 style="margin-top:0.75rem">&#129513; Practice Quiz</h1>
  <p>Test yourself with timed, randomized questions per certification. Get instant scoring, a domain-by-domain breakdown, and an explanation for every answer. Your best scores are saved in your browser - no account needed.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-blue">Instant Scoring</span><span class="badge badge-orange">Explanations</span><span class="badge badge-green">Progress Saved Locally</span></div>
</div></div>
<div class="container" style="padding:2rem 0 4rem">
  <div id="quiz-app"></div>
  <div class="callout info" style="margin-top:2rem"><div class="callout-title">&#128161; Want to add questions?</div><p>This question bank is open source. Add or improve questions by editing <code>data/quiz-questions.json</code> and opening a pull request. Each question needs a cert, domain, options, the correct answer index, and an explanation.</p></div>
</div>
<script src="../assets/js/quiz.js"></script>
""" + FOOT
write(f"{DOCS}/quiz.html", quiz_html)

# ── cheatsheets.html (confusing pairs) ──────────────────────
cheat_toc = [("compute","Compute"),("storage","Storage"),("databases","Databases"),
             ("networking","Networking"),("integration","Messaging & Integration"),
             ("security","Security & Identity"),("deployment","Deployment & DR"),
             ("analytics","Analytics & AI")]
cheatsheets_html = HEAD("Confusing Pairs Cheat Sheet","Side-by-side comparisons of commonly confused AWS services: SG vs NACL, SQS vs SNS vs EventBridge, EBS vs EFS vs FSx, ALB vs NLB, and more.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>Cheat Sheets</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-teal">Exam Cheat Sheet</span>
  <h1 style="margin-top:0.75rem">&#128221; Confusing Pairs Cheat Sheet</h1>
  <p>The AWS service comparisons that trip people up on exams, side by side. Skim these before test day - knowing the difference between look-alike services is worth easy points.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-blue">Quick Reference</span><span class="badge badge-orange">All Certs</span></div>
</div></div>
""" + wrap(cheat_toc, """
<section id="compute"><h2>&#128187; Compute</h2>
<h3>ALB vs NLB vs GLB</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>ALB</th><th>NLB</th><th>GLB</th></tr></thead><tbody>
  <tr><td>OSI Layer</td><td>7 (HTTP/HTTPS)</td><td>4 (TCP/UDP/TLS)</td><td>3 (IP)</td></tr>
  <tr><td>Routing</td><td>Path, host, header, query</td><td>Flow hash (fast)</td><td>To virtual appliances</td></tr>
  <tr><td>Static IP</td><td>No (DNS name)</td><td>Yes (per AZ / EIP)</td><td>No</td></tr>
  <tr><td>Best for</td><td>Web apps, microservices</td><td>Low latency, gaming, IoT</td><td>Firewalls, IDS/IPS inline</td></tr>
</tbody></table></div>
<h3>ECS vs EKS vs Fargate</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>ECS</th><th>EKS</th><th>Fargate</th></tr></thead><tbody>
  <tr><td>What</td><td>AWS-native container orchestrator</td><td>Managed Kubernetes</td><td>Serverless compute for containers</td></tr>
  <tr><td>Control plane</td><td>Managed by AWS (free)</td><td>Managed K8s (hourly fee)</td><td>N/A - launch type</td></tr>
  <tr><td>Use when</td><td>Simple, AWS-only</td><td>K8s portability/ecosystem</td><td>No servers to manage (works with ECS/EKS)</td></tr>
</tbody></table></div>
<h3>Lambda vs Fargate vs EC2</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Lambda</th><th>Fargate</th><th>EC2</th></tr></thead><tbody>
  <tr><td>Unit</td><td>Function (event)</td><td>Container (task)</td><td>Virtual machine</td></tr>
  <tr><td>Max run time</td><td>15 min</td><td>No hard limit</td><td>No limit</td></tr>
  <tr><td>Scaling</td><td>Automatic, to zero</td><td>Task-based</td><td>Auto Scaling groups</td></tr>
  <tr><td>Use when</td><td>Event-driven, spiky</td><td>Long-running containers, no server mgmt</td><td>Full control / legacy</td></tr>
</tbody></table></div>
</section>

<section id="storage"><h2>&#128190; Storage</h2>
<h3>EBS vs EFS vs FSx vs S3</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>EBS</th><th>EFS</th><th>FSx</th><th>S3</th></tr></thead><tbody>
  <tr><td>Type</td><td>Block</td><td>File (NFS)</td><td>File (Windows/Lustre)</td><td>Object</td></tr>
  <tr><td>Attach</td><td>One instance (or multi-attach io2)</td><td>Many instances, multi-AZ</td><td>Many instances</td><td>Over HTTP API</td></tr>
  <tr><td>Scope</td><td>Single AZ</td><td>Regional (multi-AZ)</td><td>Varies</td><td>Regional, 11 9s durability</td></tr>
  <tr><td>Use for</td><td>Boot volumes, databases</td><td>Shared Linux file storage</td><td>Windows shares, HPC</td><td>Static assets, data lake, backup</td></tr>
</tbody></table></div>
<h3>S3 Standard-IA vs One Zone-IA vs Glacier</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Standard-IA</th><th>One Zone-IA</th><th>Glacier Flexible</th></tr></thead><tbody>
  <tr><td>Retrieval</td><td>Milliseconds</td><td>Milliseconds</td><td>Minutes to hours</td></tr>
  <tr><td>AZs</td><td>Multi-AZ</td><td>Single AZ</td><td>Multi-AZ</td></tr>
  <tr><td>Use for</td><td>Infrequent, needs durability</td><td>Infrequent, reproducible data</td><td>Archive</td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128161; Instance store vs EBS</div><p>Instance store is ephemeral (data lost on stop/terminate); EBS persists independently of the instance lifecycle.</p></div>
</section>

<section id="databases"><h2>&#128202; Databases</h2>
<h3>RDS vs Aurora vs DynamoDB vs Redshift</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>RDS</th><th>Aurora</th><th>DynamoDB</th><th>Redshift</th></tr></thead><tbody>
  <tr><td>Model</td><td>Relational</td><td>Relational (MySQL/PG compatible)</td><td>NoSQL key-value/document</td><td>Columnar data warehouse</td></tr>
  <tr><td>Scale</td><td>Vertical + read replicas</td><td>Auto-scaling storage, 15 replicas</td><td>Horizontal, virtually unlimited</td><td>MPP cluster / serverless</td></tr>
  <tr><td>Use for</td><td>Traditional apps</td><td>High-performance relational</td><td>Massive scale, low latency</td><td>OLAP / analytics</td></tr>
</tbody></table></div>
<h3>RDS Multi-AZ vs Read Replicas</h3>
<div class="grid-2">
  <div class="card"><h3>Multi-AZ</h3><ul><li>Purpose: high availability / failover</li><li>Synchronous standby, not readable</li><li>Automatic failover on outage</li></ul></div>
  <div class="card"><h3>Read Replicas</h3><ul><li>Purpose: scale read traffic</li><li>Asynchronous, readable</li><li>Can be promoted to standalone</li></ul></div>
</div>
<h3>ElastiCache Redis vs Memcached</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Redis</th><th>Memcached</th></tr></thead><tbody>
  <tr><td>Data structures</td><td>Rich (lists, sets, sorted sets)</td><td>Simple key-value</td></tr>
  <tr><td>Persistence / replication</td><td>Yes (backups, replicas, Multi-AZ)</td><td>No</td></tr>
  <tr><td>Use for</td><td>Leaderboards, pub/sub, HA cache</td><td>Simple, multi-threaded caching</td></tr>
</tbody></table></div>
</section>

<section id="networking"><h2>&#127760; Networking</h2>
<h3>Security Group vs Network ACL</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Security Group</th><th>Network ACL</th></tr></thead><tbody>
  <tr><td>Level</td><td>Instance / ENI</td><td>Subnet</td></tr>
  <tr><td>State</td><td>Stateful (return auto-allowed)</td><td>Stateless (allow both directions)</td></tr>
  <tr><td>Rules</td><td>Allow only</td><td>Allow and Deny</td></tr>
  <tr><td>Evaluation</td><td>All rules</td><td>In order, lowest number first</td></tr>
</tbody></table></div>
<div class="callout warn"><div class="callout-title">&#9888; Ephemeral ports</div><p>Because NACLs are stateless, you must allow the ephemeral port range (1024-65535) for return traffic. Security Groups handle this automatically.</p></div>
<h3>VPC Peering vs Transit Gateway vs PrivateLink</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>VPC Peering</th><th>Transit Gateway</th><th>PrivateLink</th></tr></thead><tbody>
  <tr><td>Topology</td><td>1:1</td><td>Hub-and-spoke (many)</td><td>Expose a single service</td></tr>
  <tr><td>Transitive</td><td>No</td><td>Yes</td><td>N/A</td></tr>
  <tr><td>Overlapping CIDRs</td><td>Not allowed</td><td>Not allowed</td><td>Works despite overlap</td></tr>
</tbody></table></div>
<h3>NAT Gateway vs Internet Gateway vs Egress-Only IGW</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>NAT Gateway</th><th>Internet Gateway</th><th>Egress-Only IGW</th></tr></thead><tbody>
  <tr><td>Direction</td><td>Outbound only (IPv4)</td><td>Inbound + outbound</td><td>Outbound only (IPv6)</td></tr>
  <tr><td>Subnet</td><td>Private -> internet</td><td>Public subnet</td><td>Private IPv6 -> internet</td></tr>
</tbody></table></div>
</section>

<section id="integration"><h2>&#128233; Messaging &amp; Integration</h2>
<h3>SQS vs SNS vs EventBridge vs Kinesis</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>SQS</th><th>SNS</th><th>EventBridge</th><th>Kinesis</th></tr></thead><tbody>
  <tr><td>Pattern</td><td>Queue (pull)</td><td>Pub/sub (push)</td><td>Event bus + routing rules</td><td>Streaming</td></tr>
  <tr><td>Consumers</td><td>One (per message)</td><td>Many subscribers</td><td>Many targets, filtered</td><td>Many, can replay</td></tr>
  <tr><td>Ordering</td><td>FIFO option</td><td>FIFO option</td><td>No</td><td>Per-shard order + replay</td></tr>
  <tr><td>Use for</td><td>Decouple, buffer work</td><td>Fan-out notifications</td><td>SaaS/AWS event routing</td><td>Real-time analytics, big streams</td></tr>
</tbody></table></div>
<h3>Step Functions: Standard vs Express</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Standard</th><th>Express</th></tr></thead><tbody>
  <tr><td>Duration</td><td>Up to 1 year</td><td>Up to 5 minutes</td></tr>
  <tr><td>Rate</td><td>Lower throughput</td><td>Very high throughput</td></tr>
  <tr><td>Use for</td><td>Long-running, auditable workflows</td><td>High-volume, short event processing</td></tr>
</tbody></table></div>
</section>

<section id="security"><h2>&#128274; Security &amp; Identity</h2>
<h3>SCP vs IAM Policy vs Permission Boundary</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>SCP</th><th>IAM Policy</th><th>Permission Boundary</th></tr></thead><tbody>
  <tr><td>Scope</td><td>Whole account/OU (Org)</td><td>User/role/group</td><td>Max perms for a principal</td></tr>
  <tr><td>Grants access?</td><td>No - only limits</td><td>Yes</td><td>No - only caps</td></tr>
  <tr><td>Use for</td><td>Org-wide guardrails</td><td>Day-to-day permissions</td><td>Delegated admin limits</td></tr>
</tbody></table></div>
<h3>Cognito User Pool vs Identity Pool</h3>
<div class="grid-2">
  <div class="card"><h3>User Pool</h3><ul><li>User directory &amp; sign-in</li><li>Issues JWT tokens</li><li>Answers "who is this user?"</li></ul></div>
  <div class="card"><h3>Identity Pool</h3><ul><li>Exchanges identity for temporary AWS credentials</li><li>Maps to IAM roles</li><li>Answers "what AWS resources can they use?"</li></ul></div>
</div>
<h3>Secrets Manager vs Parameter Store</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Secrets Manager</th><th>Parameter Store</th></tr></thead><tbody>
  <tr><td>Rotation</td><td>Built-in automatic</td><td>Manual (Lambda + EventBridge)</td></tr>
  <tr><td>Cost</td><td>Per secret/month</td><td>Standard tier free</td></tr>
  <tr><td>Use for</td><td>DB creds, rotating secrets</td><td>Config values, non-rotating secrets</td></tr>
</tbody></table></div>
<h3>KMS vs CloudHSM</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>KMS</th><th>CloudHSM</th></tr></thead><tbody>
  <tr><td>Tenancy</td><td>Multi-tenant managed</td><td>Single-tenant dedicated HSM</td></tr>
  <tr><td>Control</td><td>AWS-managed FIPS 140-2</td><td>You fully control keys</td></tr>
  <tr><td>Use for</td><td>Most encryption needs</td><td>Strict compliance, custom key store</td></tr>
</tbody></table></div>
</section>

<section id="deployment"><h2>&#128640; Deployment &amp; DR</h2>
<h3>Deployment strategies</h3>
<div class="table-wrap"><table><thead><tr><th>Strategy</th><th>Behavior</th><th>Downtime / rollback</th></tr></thead><tbody>
  <tr><td>All-at-once</td><td>Replace everything at once</td><td>Downtime; fast but risky</td></tr>
  <tr><td>Rolling</td><td>Replace in batches</td><td>Reduced capacity during deploy</td></tr>
  <tr><td>Blue/Green</td><td>New env beside old, then switch</td><td>Zero downtime, instant rollback</td></tr>
  <tr><td>Canary</td><td>Small % first, then rest</td><td>Limited blast radius</td></tr>
</tbody></table></div>
<h3>DR strategies (RTO/RPO vs cost)</h3>
<div class="table-wrap"><table><thead><tr><th>Strategy</th><th>RTO/RPO</th><th>Cost</th></tr></thead><tbody>
  <tr><td>Backup &amp; Restore</td><td>Hours</td><td>Lowest</td></tr>
  <tr><td>Pilot Light</td><td>Tens of minutes</td><td>Low</td></tr>
  <tr><td>Warm Standby</td><td>Minutes</td><td>Medium</td></tr>
  <tr><td>Multi-Region Active-Active</td><td>Near zero</td><td>Highest</td></tr>
</tbody></table></div>
</section>

<section id="analytics"><h2>&#128200; Analytics &amp; AI</h2>
<h3>Athena vs Redshift vs EMR</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Athena</th><th>Redshift</th><th>EMR</th></tr></thead><tbody>
  <tr><td>What</td><td>Serverless SQL on S3</td><td>Managed data warehouse</td><td>Managed Hadoop/Spark clusters</td></tr>
  <tr><td>Pay for</td><td>Data scanned per query</td><td>Cluster / serverless capacity</td><td>Cluster runtime</td></tr>
  <tr><td>Use for</td><td>Ad-hoc queries, occasional</td><td>Frequent BI on structured data</td><td>Big data processing, custom frameworks</td></tr>
</tbody></table></div>
<h3>Kinesis Data Streams vs Data Firehose</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Data Streams</th><th>Data Firehose</th></tr></thead><tbody>
  <tr><td>Management</td><td>You manage shards/consumers</td><td>Fully managed delivery</td></tr>
  <tr><td>Latency</td><td>Real-time (sub-second)</td><td>Near real-time (buffered)</td></tr>
  <tr><td>Use for</td><td>Custom real-time processing, replay</td><td>Load to S3/Redshift/OpenSearch</td></tr>
</tbody></table></div>
<h3>Fine-tuning vs RAG vs Prompt Engineering</h3>
<div class="table-wrap"><table><thead><tr><th>&nbsp;</th><th>Prompt Engineering</th><th>RAG</th><th>Fine-tuning</th></tr></thead><tbody>
  <tr><td>Changes model?</td><td>No</td><td>No (adds context)</td><td>Yes (weights)</td></tr>
  <tr><td>Uses private data</td><td>In the prompt</td><td>Retrieved at query time</td><td>Baked into the model</td></tr>
  <tr><td>Effort / cost</td><td>Lowest</td><td>Medium</td><td>Highest</td></tr>
</tbody></table></div>
<div class="callout tip"><div class="callout-title">&#128221; Contribute</div><p>Spot a missing pair? Add it to the cheat sheet source in <code>build.py</code> and open a pull request.</p></div>
</section>
""") + FOOT
write(f"{DOCS}/cheatsheets.html", cheatsheets_html)

# ── dashboard.html (progress) ───────────────────────────────
dashboard_html = HEAD("My Progress","Your personal AWS study dashboard: quiz readiness per certification and study-checklist completion, all saved privately in your browser.") + """
<div class="container" style="padding-top:2rem"><div class="breadcrumb"><a href="../index.html">Home</a> / <span>My Progress</span></div></div>
<div class="page-header"><div class="container">
  <span class="badge badge-green">Personal</span>
  <h1 style="margin-top:0.75rem">&#128202; My Progress</h1>
  <p>Your quiz readiness by certification and overall study-checklist completion, in one place. Everything here is stored privately in your browser - no account, nothing uploaded.</p>
  <div class="flex-wrap mt-1"><span class="badge badge-blue">Quiz Scores</span><span class="badge badge-orange">Checklist Completion</span><span class="badge badge-green">Private &amp; Local</span></div>
</div></div>
<div class="container" style="padding:2rem 0 4rem">
  <div id="dashboard-app"></div>
</div>
<script src="../assets/js/dashboard.js"></script>
""" + FOOT
write(f"{DOCS}/dashboard.html", dashboard_html)

# ── SEO & PWA assets: sitemap.xml, robots.txt, manifest, OG image ──
import datetime
today = datetime.date.today().isoformat()

# Discover all generated pages for the sitemap (root index + docs/*.html)
sitemap_pages = ["index.html"] + sorted(
    f"docs/{n}" for n in os.listdir(DOCS) if n.endswith(".html")
)
# Priority hints: homepage highest, foundations/quiz high, rest default
def _priority(path):
    if path == "index.html": return "1.0"
    if "foundations" in path or path.endswith("quiz.html"): return "0.9"
    if path.endswith(("resources.html", "labs.html")): return "0.8"
    return "0.7"

urls = "".join(
    f'  <url><loc>{SITE_URL}/{p}</loc><lastmod>{today}</lastmod>'
    f'<changefreq>weekly</changefreq><priority>{_priority(p)}</priority></url>\n'
    for p in sitemap_pages
)
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f"{urls}</urlset>\n")
write(f"{BASE}/sitemap.xml", sitemap)

# ── Search index (client-side search, no external deps) ──────
import re as _re, json as _json, html as _html
_search_docs = []
for _p in sitemap_pages:
    _fp = f"{BASE}/{_p}"
    try:
        _txt = open(_fp, encoding="utf-8").read()
    except OSError:
        continue
    _title_m = _re.search(r"<title>(.*?)</title>", _txt, _re.S)
    _title = _html.unescape(_title_m.group(1).strip()) if _title_m else _p
    _title = _title.replace(" - AWS Study Hub", "")
    _desc_m = _re.search(r'<meta name="description" content="(.*?)"', _txt, _re.S)
    _desc = _html.unescape(_desc_m.group(1).strip()) if _desc_m else ""
    # Section headings (h2/h3), strip any inner tags/emoji entities
    _heads = []
    for _h in _re.findall(r"<h[23][^>]*>(.*?)</h[23]>", _txt, _re.S):
        _clean = _re.sub(r"<[^>]+>", "", _h)
        _clean = _re.sub(r"&#\d+;|&#x[0-9a-fA-F]+;", "", _clean)
        _clean = _html.unescape(_clean).strip()
        if _clean:
            _heads.append(_clean)
    # URL relative to site root (index.html at root, others under docs/)
    _url = _p
    _search_docs.append({
        "title": _title,
        "url": _url,
        "desc": _desc,
        "headings": _heads[:25],
    })
_search_index = {"version": 1, "generated": today, "docs": _search_docs}
os.makedirs(f"{BASE}/data", exist_ok=True)
write(f"{BASE}/data/search-index.json", _json.dumps(_search_index, ensure_ascii=False, indent=0) + "\n")


robots = ("User-agent: *\n"
          "Allow: /\n\n"
          f"Sitemap: {SITE_URL}/sitemap.xml\n")
write(f"{BASE}/robots.txt", robots)

manifest = ('{\n'
            '  "name": "AWS Study Hub",\n'
            '  "short_name": "AWS Study Hub",\n'
            '  "description": "Free, open-source study platform for every AWS certification.",\n'
            '  "start_url": "./index.html",\n'
            '  "display": "standalone",\n'
            '  "background_color": "#0f1117",\n'
            '  "theme_color": "#ff9900",\n'
            '  "icons": [\n'
            '    { "src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any" }\n'
            '  ]\n'
            '}\n')
write(f"{BASE}/manifest.webmanifest", manifest)

# Simple SVG app icon and OG image (no binary assets; git-friendly)
icon_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            '<rect width="512" height="512" rx="96" fill="#0f1117"/>'
            '<text x="256" y="340" font-size="300" text-anchor="middle" font-family="sans-serif">&#x2601;</text>'
            '</svg>\n')
write(f"{BASE}/assets/icon.svg", icon_svg)

og_svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
          '<rect width="1200" height="630" fill="#0f1117"/>'
          '<text x="80" y="300" font-size="92" font-weight="800" fill="#ffffff" font-family="sans-serif">AWS Study Hub</text>'
          '<text x="80" y="380" font-size="40" fill="#ff9900" font-family="sans-serif">Free study platform for every AWS certification</text>'
          '<text x="80" y="470" font-size="34" fill="#9aa4b2" font-family="sans-serif">Foundations &#183; 12 certs &#183; labs &#183; interactive quiz</text>'
          '<text x="1040" y="150" font-size="120" font-family="sans-serif">&#x2601;</text>'
          '</svg>\n')
write(f"{BASE}/assets/og-image.svg", og_svg)

print("\nAll pages generated successfully!")
