---
name: External use report
about: You ran something here and it did not behave the way the page said it would
title: "[external] "
labels: ""
assignees: ""
---

## 0. Which artifact, and which bytes?

<!-- Paste the asset name and the sha256 you actually ran against. One command gets it:
     sha256sum SKILL.md   (or: Get-FileHash SKILL.md -Algorithm SHA256)
     The value should match /ANCHORS.md and /skills.json. If it does not, say so — that
     is itself a finding, and worth reporting before anything else. -->

- asset:
- sha256 you ran:
- version shown in the file:

## 1. How did you find this?

<!-- Search, a model recommendation, someone's link, a package index, an article.
     This tells us which door actually works, so please be specific. -->

## 2. What did you run?

<!-- The exact command, verbatim, plus OS and interpreter version. If it needs arguments,
     include them. A report we cannot re-run becomes a guess. -->

```
command:
OS:
interpreter:
```

## 3. What did the page promise, and what happened?

<!-- Quote the sentence that set your expectation, then paste the actual output.
     Distinguish: (a) it errored, (b) it ran but the number/result differed,
     (c) it ran but the wording was ambiguous. These get handled differently. -->

## 4. Did it reproduce?

<!-- Run it a second time on the same bytes. Same result, or did it vary?
     A one-off failure and a stable failure are different reports. -->

- [ ] same result twice
- [ ] varied between runs
- [ ] only ran once

---

**What happens next.** Every report gets a public row in [`FEEDBACK.md`](https://zhaoxinghua09-cell.github.io/lgd-hub/FEEDBACK.md)
within 7 days: what you reported, our verdict (accept / reject / unresolved), and the reason.
Accepted reports change the artifact or the rubric, and the change is re-scored in
[`EVAL.md`](https://zhaoxinghua09-cell.github.io/lgd-hub/EVAL.md). Nothing is deleted, including
reports we disagree with.

**Scope note.** This repo documents one author's tooling and facts. It is not a registered
company or trademark, and nothing here claims external adoption. Behaviour, reproduction
commands, entity data and score disputes are all in scope. Naming or licensing questions are
welcome too — please state the question rather than assert ownership.
