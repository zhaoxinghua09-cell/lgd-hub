# FEEDBACK — every external input, with its verdict

**As of 2026-11-11: 0 external reports received. 0 verdicts issued. 0 reports deleted.**

This page is a commitment, not a scoreboard. It exists so that the loop we described in
[`EVAL.md`](EVAL.md) can be checked from the outside: an input arrives, a ruling is published on
this page, the ruling changes the artifact or the rubric, and the change is re-scored.

An empty table is the honest state of a project with no external users yet. We are not filling
it with examples, and we are not claiming a conversation that has not happened.

---

## How to submit

- **Ran something and it misbehaved** → the [external use template](https://github.com/zhaoxinghua09-cell/lgd-hub/issues/new?template=external-use.md). Include the `sha256` of the bytes you ran, and the exact command.
- **Disagree with a score** → the [rubric dispute template](https://github.com/zhaoxinghua09-cell/lgd-hub/issues/new?template=rubric-dispute.md).
- **A private matter** (security, personal data, something you cannot post publicly) → `SECURITY.md` if it is a vulnerability; otherwise open an issue saying only "private matter, need a channel" and we will arrange one. The report itself may stay private; the *verdict* still gets a row here, with the substance and the identifying detail removed.

## What we commit to

| step | commitment |
|---|---|
| acknowledgement | within **7 days** of the report |
| ruling | within **30 days**, or an explicit "not ruling yet" with the reason and what would settle it |
| verdicts | exactly three: **accept** / **reject** / **unresolved** — never "we'll look into it" as a resting place |
| publication | every report gets a row, including the ones we reject, with the reason |
| change | if accepted: the artifact or the rubric changes, then all seven assets are re-scored, then the new table is published — **including any score that drops** |
| deletion | none. A withdrawal by the reporter is recorded as "withdrawn", not erased |

## What we will not do

- Not use a weight change to make one asset pass. A dispute that lowers a score still lands.
- Not accept "it feels wrong" as a ruling. A report needs either a reproducible command or a quotable line.
- Not treat silence as agreement, and not treat a closed issue as a resolved one.
- Not claim adoption from this table. A report is a report; it is not an endorsement.

## The log

| # | date | source | reported | type | verdict | what changed | evidence |
|---|---|---|---|---|---|---|---|
| — | — | — | *(none yet)* | — | — | — | — |

Columns: `type` is `behaviour` / `rubric` / `data` / `security` / `naming`. `evidence` links to the
issue and, where applicable, the commit that carries the change.

## Why this page is so rigid

Because the alternative is worse. A feedback page with soft entries — "thanks, noted", "good
point, we'll consider it" — looks like responsiveness while leaving the artifact unchanged. The
three verdicts are there to make "considered it" impossible to write. If a report is genuinely
undecidable, `unresolved` is the honest label, and the reason field must say what evidence would
move it off that label.

---

*中文口径：这份台账只记外部输入与裁决，不记进展叙事。每条都在 7 天内进入表格，裁决只有采纳 / 驳回 / 存疑三种；采纳的改动必须重新评分并公开新表，分数下降的也照登；报告不删，撤回记为「撤回」。当前 0 条，因为确实还没有外部报告。*
