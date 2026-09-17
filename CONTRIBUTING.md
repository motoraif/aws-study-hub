# 🤝 Contributing to AWS Study Hub

Thank you for helping make AWS Study Hub the best free AWS certification resource!

## Ways to Contribute

| Type | Examples |
|------|----------|
| 🐛 Bug fix | Broken link, typo, wrong information |
| 📝 Improve content | Expand a section, add an exam tip |
| 🆕 Add new content | New topic, service section, practice question |
| 🔗 Add resources | New free course, cheat sheet, tool |

## Quick Start

```bash
# Fork → Clone → Branch
git checkout -b fix/broken-link-clf-page

# Make changes, test in browser
python3 -m http.server 8080

# Commit (Conventional Commits format)
git commit -m "fix: update broken Skill Builder link for CLF-C02"

# Push and open PR
```

## Commit Message Format

```
feat: add EKS section to SAA-C03 page
fix: correct Lambda timeout (15 min not 10 min)
content: add 5 new practice questions to labs page
link: update Stephane Maarek DVA course URL
```

## Content Guidelines

- Verify facts from official AWS documentation
- Link to the official source when adding facts/limits/prices
- Only add exam tips based on verified community knowledge
- Test all external links before submitting

## HTML Template (for new sections)

```html
<section id="my-section">
  <h2>My Topic</h2>
  <p>Clear explanation...</p>
  <div class="callout tip">
    <div class="callout-title">💡 Exam Tip</div>
    <p>Key insight here...</p>
  </div>
  <pre><code>aws service command --option value</code></pre>
</section>
```

## Questions?

Open an [Issue](https://github.com/motoraif/aws-study-hub/issues/new) to ask a question or start a conversation.

Thank you! ☁️
