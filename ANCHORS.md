# Anchor manifest — 31 core assets

Author: Xinghua Zhao (Steven Zhao) · ORCID 0009-0001-0512-1237
Two revisions are recorded here on purpose — see the note below the first table.

## Current revision (H) — trigger conditions made machine-visible, 2026-11-11

These are the hashes of the files as they are now. Revision H raises trigger design in four assets: `read_when` is now a top-level key, so the trigger conditions a reader could already see are also visible to a scorer — in `skill-preflight` it had been nested under `metadata:`. Same rubric, same weights, no scorer edit; shelf average 0.928 → 0.952. Revision G had finished the disclosure sweep: remaining machine-specific paths were replaced with placeholders, one correspondence receipt had its message identifier and personal address redacted in place, and the two credential helper scripts now read their key-file location from an environment variable instead of a hard-coded path. The 24 assets that carry an `EVIDENCE.md` also had that snapshot regenerated against the same gate run. Earlier hashes — revision A (proof-bound) and revision B (paths sanitized) — remain verifiable below.

| # | asset | sha256 (rev H) | proof | bitcoin block |
|---|---|---|---|---|
| 1 | `agent-evolution` | `6592c2ab99f65a6e9ec1da46534caea8bb2a0679e2d8637465a9b64e015905a8` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 2 | `evidence-chain-builder` | `d40b23a015f1c487703bf900684d8997fd066a835523beef0efd067b52d03481` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 3 | `evidence-chain-check` | `50c26142e9cca31a2c372a832c51b5a29749b8c4db7436a88500b61663002d3d` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 4 | `evidence-chain-suite` | `857ddde056c3a49e24bff3be7820ed6878056fa7cfec42b76ef10e1f8144726c` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 5 | `intl-participation-pipeline` | `f335d29905cf0fe3e01f41458c92109a7f44ee38ab42ec2b9cb987756c13fdb5` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 6 | `iso-standards-readiness` | `719b0cc1a5ef94b7bc18749e17de2e7e13e7a9cf373e649a82ffb2c15e1749a2` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 7 | `lgd-gate-methodology` | `cb2f6aa9f68e3771ee89f650a5603c2a6e96ee5ada37f1db82d90e22f3ac7ca6` | `SKILL.md.ots` | Confirmed · block 975422 + 975424 |
| 8 | `lgd-three-laws-auditor` | `5d5699432104e7b9386b2b89dad624a261a171267911093700f810357c7b2ef7` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 9 | `medical-device-compliance-grader` | `ba94b808e824779a700355392f465ed24ad926bc38462a949173c40bbf68c16e` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 10 | `medical-device-qms-gmp` | `e8197884268ce6521fd88a82ed3fc2de360d8e4a3ccda0e83e70190d3b470d78` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 11 | `medical-device-reg-dossier` | `328c2e1c3e28ef1ca972ebe8b6fb239c9b4c247739a883aa828fb816a9ed5b49` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 12 | `medical-device-risk-management` | `890637a0408b23a5c4f916316c3a99b4ed1e7ff796d276e405f93f3a784bc88d` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 13 | `medxpert-reg-hub` | `068da1aa4a1ae1e169613fdfd7568d303c635d97e05504727fd4ad48f8ac5f26` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 14 | `medxpert-termbase` | `b8c56de80ce22bdfe36490b725e81fa9618d64b37072604ef1fcca26436bf81b` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 15 | `ots-timestamp-anchor` | `4c289da7cd7a84c25ffdb9cdbb59b7b21d7b7e727d1d221d0472331551ed1123` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 16 | `publish-quality-gate` | `cf857a14a8b79426198c6b5c85570480177aa08a4cf6ef23fde2c897b72771e4` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 17 | `publish-redteam-review` | `efa12c82ae1a31c736ea914d9c4391b27a08a568391970fe0c9e241cd5ae0d93` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 18 | `skill-auditor` | `a61ecbcbf629823f83a3dff6a1cca5b4c7e68118043834ee45d9e5a8eca78361` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 19 | `skill-carrier-rights-layer` | `a80bffa087c6687993a4fbddf6e22af4e68ebdc8075cde9f30fc8597c455e6a3` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 20 | `skill-doctor` | `11757c8fce3f06fccb1dce127c6c8a47f0ee683660236bab4967fe285fe89b0c` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 21 | `skill-preflight` | `588ec5c1e0d03d881d0f739fe39067e5cfa08dc827e5ffb0a2273f44f81c7e6b` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 22 | `skill-release-gate` | `cda902c109587830e38d6dc999a4597af5bef65faa99c9804605043310bb72f7` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 23 | `standards-contribution-substantiation` | `7d06f5f912dec22c9925f53dd16b01fe0cd78f5bd7f5fa3c05a8b464cb9a9f64` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 24 | `uibc-challenge` | `1d28e6ee000dd740325c1de7ecfc6bf3695aaf273b2e2d4b4de82d59dad301ae` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 25 | `uibc-team-crypt` | `f58f7934e62f6825fc9752d1bce53d570071b1cb0bdaac5cde4c8f8f28e95e1a` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 26 | `uibc-team-fin` | `e38e17cf1db15673aca72d06270c76769a6a4ec20894640908d300dedf62bc80` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 27 | `uibc-team-gov` | `5a300eff6169368b2ef9c21451b6f1539b3ed6ea4e76c197626dbac5bb77d4b1` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 28 | `uibc-team-law` | `b161ae7dab8289f17c96d8a41f93277fb481b0bdd2dd6746b9ae334f05405e66` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 29 | `uibc-team-med` | `b8979ca86c289640a4d7e06ae2e7190d681912ded2c9509c400daedc1779ceb3` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 30 | `uibc-team-rob` | `ff0f26b70ebd64a4ed476191d4fb9244855390d4c7c3d0699ebf864847516507` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |
| 31 | `uibc-team-uas` | `6686bbb33aa71bc5e463ecc0d829cf4356090b99fe1a195cc5eaec0ad4938fd8` | `SKILL.md.ots` | Confirmed · block 975424 + 975429 |

## Revision A — the bytes the `.ots` proofs commit to

The 31 `.ots` proofs were produced from these hashes. If you are verifying a proof file rather than the current file, use this table. For 4 of the 31 assets rev A and rev H are identical and are not repeated here.

| asset | sha256 (rev A, proof-bound) | sha256 (rev H, current) | what changed |
|---|---|---|---|
| `lgd-gate-methodology` | `80b33e13125d4aeeccfdfee5f556c20afd6ac6a3cc96bbe15ed393d967d8fb66` | `cb2f6aa9f68e3771ee89f650a5603c2a6e96ee5ada37f1db82d90e22f3ac7ca6` | 补英文字段（rev C）；补 `scripts/gate_scorecard.py` + `references/seven-layer-matrix.md` + 红线段与可复跑命令（rev D） |
| `publish-redteam-review` | `248bf4194edf47aa313f92d08369357279e1e7872a1ea8525e23726082d9d2cd` | `efa12c82ae1a31c736ea914d9c4391b27a08a568391970fe0c9e241cd5ae0d93` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `publish-quality-gate` | `77b20aafd9013c9706ecad7c1dc250a4718e31a8d8c29a5981f1330c53455dc3` | `cf857a14a8b79426198c6b5c85570480177aa08a4cf6ef23fde2c897b72771e4` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-challenge` | `9dfe360889e341793b6926f809b25e0ee530d81f576bf7e7c51cfb3815742e13` | `1d28e6ee000dd740325c1de7ecfc6bf3695aaf273b2e2d4b4de82d59dad301ae` | 补英文字段（rev C）；补 `scripts/submission_check.py` + `references/rubric.md` + 红线段与自查命令（rev D） |
| `uibc-team-med` | `1798aea6d4fa37d5ab97358d0b5c96ead747c8a33318ea61ad2d1b672dbcd729` | `b8979ca86c289640a4d7e06ae2e7190d681912ded2c9509c400daedc1779ceb3` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-law` | `24ba9621bed1fcb2fff2586f3800c8d0c1d01b662d5e4db8f87e63856be51203` | `b161ae7dab8289f17c96d8a41f93277fb481b0bdd2dd6746b9ae334f05405e66` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-fin` | `47a6affac39310d08cb0db0b3c7ddf3d7644a7c38e65ccd30653f692fa5802be` | `e38e17cf1db15673aca72d06270c76769a6a4ec20894640908d300dedf62bc80` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-gov` | `74484673c566dd7542cd0a792bce7cd63dec64589b285a99fe24e448be521bca` | `5a300eff6169368b2ef9c21451b6f1539b3ed6ea4e76c197626dbac5bb77d4b1` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-rob` | `9b713f18bb9a8e49909624f86239c5b774121a78c53746543b09be1186e88803` | `ff0f26b70ebd64a4ed476191d4fb9244855390d4c7c3d0699ebf864847516507` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-uas` | `dcf80e436051f6553ffda833630bd20138fbcf58c9497fa57ea3e28f3bb0b54c` | `6686bbb33aa71bc5e463ecc0d829cf4356090b99fe1a195cc5eaec0ad4938fd8` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `uibc-team-crypt` | `cbc29f6286db72ea051821c8ec5a8c84a3efb36b3452cd20fb27f78fdf5728ea` | `f58f7934e62f6825fc9752d1bce53d570071b1cb0bdaac5cde4c8f8f28e95e1a` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `evidence-chain-builder` | `3e7b29d0ed0efb2c72169addf4d4b6f0138620edee991520eaf70efa7e4d5b06` | `d40b23a015f1c487703bf900684d8997fd066a835523beef0efd067b52d03481` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `evidence-chain-check` | `c6f71ff117cc4bcf1f014b81b32817c59108c553c10df2787047415a8c003a5b` | `50c26142e9cca31a2c372a832c51b5a29749b8c4db7436a88500b61663002d3d` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `evidence-chain-suite` | `addb9dcad8fb8a7bcb519f618762f8acb597b8d9d089aa65cd7223bd232bbb11` | `857ddde056c3a49e24bff3be7820ed6878056fa7cfec42b76ef10e1f8144726c` | 补英文字段（rev C）；补 `scripts/chain_verify.py` + `references/evidence-chain-rubric.md` + 触发段与红线段（rev E） |
| `skill-carrier-rights-layer` | `2c14351754bd831159ee20d1daa8f1cc62bb9ea4df1a4e02ad8d12d06d1c0f11` | `a80bffa087c6687993a4fbddf6e22af4e68ebdc8075cde9f30fc8597c455e6a3` | 工作目录路径换成占位符（rev B）；补英文字段（rev C） |
| `ots-timestamp-anchor` | `1870e25e548d730ff0ad979bf4e0f689cc22085d231aebacc93a17add0eb6add` | `4c289da7cd7a84c25ffdb9cdbb59b7b21d7b7e727d1d221d0472331551ed1123` | 解释器与工作目录路径换成占位符（rev B）；补英文字段（rev C） |
| `medxpert-reg-hub` | `e352df537d78b44b87ae00657e72d916f7b146ac9c5d62ffb467b515b6a530b2` | `068da1aa4a1ae1e169613fdfd7568d303c635d97e05504727fd4ad48f8ac5f26` | 补英文字段（rev C）；补 `scripts/hub_verify.py`（按 manifest 逐文件复算哈希，含 `--restate`）、顶层 `read_when`、触发词、何时不用段（rev F）；manifest 哈希已同步重述并记录 `restated_utc` |
| `medical-device-compliance-grader` | `4ccb5e29646fddb745847c6e2e55a24c238174a48b199c57f9adad67217c7b27` | `ba94b808e824779a700355392f465ed24ad926bc38462a949173c40bbf68c16e` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `medical-device-reg-dossier` | `ec9418d1b7f37a2fbd9f727f4dbcbe6bb9d3960f68b180f495382eb76bdd7619` | `328c2e1c3e28ef1ca972ebe8b6fb239c9b4c247739a883aa828fb816a9ed5b49` | 版权行改自然人（去公司名）（rev B）；补英文字段（rev C） |
| `medical-device-qms-gmp` | `5ed5da23d21c57236229c406628c5087ffcb270157e70dc55e6e759ca7b72f4e` | `e8197884268ce6521fd88a82ed3fc2de360d8e4a3ccda0e83e70190d3b470d78` | 版权行改自然人（去公司名）（rev B）；补英文字段（rev C） |
| `medxpert-termbase` | `03f18d01e1168aa0502a7000acf05c192e06b64f0d9f3686fb23976a42868893` | `b8c56de80ce22bdfe36490b725e81fa9618d64b37072604ef1fcca26436bf81b` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `medical-device-risk-management` | `c631eb9560512ac1df638952b9189644f1f1f18dff44126db322b7db78e54c3c` | `890637a0408b23a5c4f916316c3a99b4ed1e7ff796d276e405f93f3a784bc88d` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `intl-participation-pipeline` | `d44762b5487f93bf693b9c9c8c64067e02adc0b63ae9e28c591413972073b359` | `f335d29905cf0fe3e01f41458c92109a7f44ee38ab42ec2b9cb987756c13fdb5` | 私钥落点与保险库路径换成占位符（rev B）；补英文字段（rev C）；补划清其余本机路径、回执里的 Message-ID 与个人邮箱就地脱敏、凭据落点描述改为『凭据内容』措辞、两个取凭据脚本改读环境变量 `GITHUB_KEY_FILE`（rev G） |
| `standards-contribution-substantiation` | `cf679f8bd87ff0a0a75aa550f333f4e0d49ffb2884f1b3508691da9950b32267` | `7d06f5f912dec22c9925f53dd16b01fe0cd78f5bd7f5fa3c05a8b464cb9a9f64` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `iso-standards-readiness` | `7f0a95e62763c2a8f6157ada4734a640fb79ba85c24bed1a0d9c06bf14a9f97a` | `719b0cc1a5ef94b7bc18749e17de2e7e13e7a9cf373e649a82ffb2c15e1749a2` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `skill-doctor` | `51bd567950e99e6b349c7d114034fc485b3d93686a6cf52d96c46733fea02c54` | `11757c8fce3f06fccb1dce127c6c8a47f0ee683660236bab4967fe285fe89b0c` | 补英文字段（rev C）；顶层 `read_when`、触发词、何时不用段、红线段、`assets/grade-thresholds.json` 与召回查询模板（rev F） |
| `skill-auditor` | `b9479596117b1c1595788c70bb4937d156f7bad8ab5dedb529dd12faf4cfcace` | `a61ecbcbf629823f83a3dff6a1cca5b4c7e68118043834ee45d9e5a8eca78361` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `skill-preflight` | `d6593fadda3bc0d86a3061d79bc2a861180743d3baac35f94cd0b2589ae7cd16` | `588ec5c1e0d03d881d0f739fe39067e5cfa08dc827e5ffb0a2273f44f81c7e6b` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |
| `skill-release-gate` | `8ee2d5210cfcfce1309e8c16fb818b13afa3e77d5d24eee472431e52e77a968b` | `cda902c109587830e38d6dc999a4597af5bef65faa99c9804605043310bb72f7` | 补 `display_name_en` / `description_en`（rev C）；刷新 `EVIDENCE.md` 门禁快照（rev G，正文未改） |

## How to check a row yourself

1. Get the asset's `SKILL.md`.
2. Run `sha256sum SKILL.md` (or `Get-FileHash SKILL.md -Algorithm SHA256`).
3. Compare with the rev G row (current file) or the rev A row (proof-bound file).
4. If it matches, this file plus the commit that introduced it give you a public time reference for that exact byte content.

## Status note (2026-11-11)

- All 31 commitments were submitted and produced `.ots` proof files.
- On 2026-11-11 retrieval from `a.pool` / `b.pool` / `alice.btc` returned `CommitmentNotFoundError` (kept as history: at that moment no aggregated proof was served), including for a freshly submitted control hash — the calendars, not our files, are the limiting side.
- Every row now names the Bitcoin blocks its proof commits to. Each was checked offline: the proof tree contains a node equal to that block's merkle root, parsed from a locally held 80-byte header whose double SHA-256 equals the block hash — no calendar or block explorer is trusted.
- Blocks: 30 assets at **975424** and **975429**; `lgd-gate-methodology` at **975422** and **975424**.
- Revision B exists because publishing machine-specific paths — including one to a plaintext key store — is a disclosure risk. Revision C adds English metadata so an English query can find the assets. Revision D adds a runnable script, a reference sheet and red-line sections to two assets. Revision E does the same for `evidence-chain-suite`. Revision F closes the last two: `medxpert-reg-hub` gained a package-integrity checker and its manifest hashes were restated with the original timestamps preserved and the reason recorded; `skill-doctor` gained machine-readable grade thresholds. Revision H raises trigger design in four assets: `read_when` is now a top-level key, so the trigger conditions a reader could already see are also visible to a scorer — in `skill-preflight` it had been nested under `metadata:`. Same rubric, same weights, no scorer edit; shelf average 0.928 → 0.952. Revision G had finished the disclosure sweep: remaining machine-specific paths became placeholders, a correspondence receipt had its message identifier and personal address redacted in place, the credential helpers now take their key-file location from an environment variable, and every `EVIDENCE.md` was re-generated from one gate run. No claim or licence line was changed in C, D, E, F or G.
