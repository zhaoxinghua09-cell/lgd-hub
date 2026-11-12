# EVAL — what these seven assets were scored on, and what we did about it

**Published 2026-11-11. Machine-readable companion: `/skills.json`. Per-file hashes: `/ANCHORS.md`.**

This page exists because of one sentence: *if a person or an agent comes to evaluate this work, they should get an authoritative result and a remediation path — and the work should then be able to improve itself, be re-evaluated, and go up.*

So the scoring is not a verdict handed down from outside. The rubric is published, one of the seven assets **is** the scorer, and every number below can be reproduced with two commands.

---

## 1. The rubric

Ten dimensions, weighted. Weights and thresholds are fixed in the scorer's source, not negotiated per asset.

| dim | what it measures | weight |
|---|---|---|
| D1 | trigger design — does the description say *what it does, when to use it, and on what words*; is there a top-level `read_when` | 0.14 |
| D2 | metadata — name / description / version / author / license / category | 0.14 |
| D3 | structure — a runnable script, ≥3 numbered steps, ≥1 code block | 0.14 |
| D4 | verifiability — a check word, an acceptance word, a self-check script or table | 0.12 |
| D5 | boundary honesty — what it does **not** apply to, red lines, "when not to use" | 0.10 |
| D6 | disclosure hygiene — no machine-specific paths, no key-shaped material, no internal strategy words | 0.10 |
| D7 | size — 80–600 lines is the healthy band; too short is a shell, too long crowds the context | 0.08 |
| D8 | provenance — theory anchor, author, license | 0.06 |
| D9 | internationalisation — a top-level English display name or description | 0.04 |
| D10 | supporting resources — `references/` + `scripts/` + `assets/`, at least two of the three | 0.08 |

Tiers: **A ≥ 0.80 · B 0.68–0.80 · C 0.55–0.68 · D < 0.55.** A blocker (key-shaped secret, or a claimed Bitcoin confirmation without one) makes an asset unpublishable regardless of score.

The scorer is `skill-preflight` — one of the seven below. It is rated by the same rubric it applies, which is either a conflict of interest or the cheapest possible audit. We chose to call it the second thing, and to publish the fact rather than hide it.

## 2. The result, 2026-11-11 19:24

| asset | version | score | tier | blockers |
|---|---|---|---|---|
| `lgd-gate-methodology` | 1.0.0 | 0.970 | A | 0 |
| `uibc-challenge` | 1.0.0 | 0.970 | A | 0 |
| `evidence-chain-suite` | 2.0.0 | 0.970 | A | 0 |
| `medxpert-reg-hub` | 1.6.0 | 0.965 | A | 0 |
| `skill-doctor` | 1.0.0 | 0.964 | A | 0 |
| `skill-preflight` | 1.2.1 | 0.936 | A | 0 |
| `publish-quality-gate` | 1.3.0 | 0.887 | A | 0 |

Shelf average **0.952**, seven of seven publishable, zero blockers.

## 3. What we changed this round — and what it moved

Four assets were losing the same 0.042: they had a description and trigger words but no **top-level** `read_when`, so the scorer could not see their trigger conditions at all. `skill-preflight` had one, but nested under a `metadata:` block — present to a reader, invisible to a machine. That is the exact failure this rubric is meant to catch, and it was sitting in the judge itself.

| asset | before | after |
|---|---|---|
| `lgd-gate-methodology` | 0.928 | **0.970** |
| `uibc-challenge` | 0.928 | **0.970** |
| `skill-preflight` | 0.894 | **0.936** |
| `publish-quality-gate` | 0.845 | **0.887** |
| shelf average | 0.928 | **0.952** |

No weight, threshold or scorer line was touched. The four files were edited; then everything was re-scored; then the new hashes were published as revision H so the numbers and the bytes stay tied together.

## 4. A gap we are not going to paper over

`skill-preflight`'s author whitelist reads `("注册老炮", "medxpert", "synomos", "buda pan", "潘布达", "zhaoxinghua")`. The canonical byline used across this shelf is `赵兴华（Steven Zhao）`, which appears in none of those strings. So D8's author sub-score is structurally unreachable for our own assets: **0.75 is the ceiling here, not a deduction we earned.**

The fix would take one line — add the name to the whitelist. We are not taking it. Editing the judge so the judged look better is precisely what this page is supposed to make impossible. It is recorded here as a known rubric defect instead, with the disclosure that our D8 scores are capped by it and not by the assets.

## 5. Reproduce it

```bash
# one asset
python scripts/preflight.py <asset-dir> --json

# the whole shelf, against the same rubric
python lgd_eval_runner.py --shelf
```

Expected: average 0.952, tiers `{A: 7}`, blockers 0, exit 0.

Then check the bytes:

```bash
sha256sum <asset>/SKILL.md       # compare with /skills.json and /ANCHORS.md
```

## 6. What this is not

- Not a certification, an accreditation, or a third-party audit. The scorer is ours; the audit trail is public so that the claim can be checked rather than trusted.
- Not a claim of external adoption. Inbound issues from accounts outside the three maintainers: **0** as of 2026-11-11.
- Not a timestamp claim beyond what the proofs show. The 31 `.ots` proofs carry Bitcoin block attestations at **975424** and **975429** (30 assets) and **975422** / **975424** (`lgd-gate-methodology`). Each was verified offline: a node in the proof tree equals the block's merkle root, read from a locally held header whose `sha256d` is the block hash. The 2026-11-11 `CommitmentNotFoundError` from the calendars is kept as history, not as the current state.
- Not a finished scoreboard. D10 still lacks `references/` on 19 library assets, and we declined to fill them with generated restatements of their own bodies. A dimension that can be satisfied by padding is a dimension that should stay unsatisfied until there is a real need for it.


## 7. Disagree with any number here?

Every score on this page can be disputed. Send a [rubric dispute](https://github.com/zhaoxinghua09-cell/lgd-hub/issues/new?template=rubric-dispute.md) or an [external use report](https://github.com/zhaoxinghua09-cell/lgd-hub/issues/new?template=external-use.md); each one gets a public row in [`FEEDBACK.md`](FEEDBACK.md) within 7 days with a verdict of accept / reject / unresolved, and an accepted change is re-scored against all seven — including any score that falls. A dispute that lowers a number still lands.

---

*Rubric and results in Chinese: see `/FACTS.md` and the shelf report. 判据与结果的中文口径见 `/FACTS.md`；本页只写数字、改了什么、以及哪一条我们拒绝去改。*
