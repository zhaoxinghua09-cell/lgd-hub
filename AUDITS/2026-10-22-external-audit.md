# LGD Hub 外部审计报告（结构化整理版）

> **来源与保真声明**
> 本文件由审计报告 PDF 抽取后整理：**仅合并 PDF 断行、增加标题层级与表格边界，措辞一字未改**。
> 逐字原文见同目录 `2026-10-22-external-audit.extracted.txt`；**两者若有出入，以 .txt 为准**。
>
> 审计对象：https://zhaoxinghua09-cell.github.io/lgd-hub/ （仓库 `zhaoxinghua09-cell/lgd-hub`，含其 NOTICE.md / README.md / world.json / codemeta.json）
> 审计日期：2026-10-22
> 审计方式：独立第三方核验。页面断言逐条对照公开登记库（DataCite / Zenodo API、Software Heritage API、Sigstore Rekor API、ORCID 公开记录、GitHub API），uibc-core 数字在锚定 commit 上本机实跑复现。
> **结论：改完再说（见第四步）**

## 第一步 · 清点

### 能核的断言（第三方一条命令 / 一次点击 / 一个公开登记库可对上）

| # | 断言（页面原文摘要） | 出处 |
|---|---|---|
| 1 | 精选 81 个技能（全库 109），分类 治理 31 · 工程 16 · 安全合规 10 · 效率 15，旗舰 9 | 技能矩阵节 |
| 2 | uibc-core：151 项测试、7 个压力场景、70 项对拍 0 分歧，锚定 73f31cc，同 commit CI 为绿（附 CI 运行链接） | 自己验节 |
| 3 | lgd-theory：12 个域码、13 篇域论文全文 | 自己验节 / 理论资产节 |
| 4 | silent-failure-catalog：SF-001 至 SF-014 共 14 个模式，每个附最小复现与检测判据 | 自己验节 |
| 5 | 三个 SWHID 快照（完整 40 位），各注 visit 号 / full / 2026-10-15 | SWH 节 |
| 6 | Rekor 条目 logIndex 2883389783：hashedrekord、logID c0d23d6a…、treeID 1193050959916656506、integratedTime 2026-09-18T05:50:12Z、带 inclusion proof | Sigstore 节 |
| 7 | SLSA provenance 管线 2026-10-18 起失败（缺 attestations: write），修复已备未合 | Sigstore 节 |
| 8 | Zenodo：v1.7.0 版本 DOI 与概念 DOI 两个链接 | 理论资产节 / 首屏卡 |
| 9 | 分层许可表（NOTICE.md，13 个仓，称 2026-10-22 逐仓读 LICENSE 核对） | 许可与贡献节 → NOTICE.md |
| 10 | 页脚身份：赵兴华 / Xinghua Zhao · 独立研究者 · ORCID 0009-0001-0512-1237 | 页脚 |

### 不能核的断言（形容词 / 定位 / 承诺类）

- 「可复核的纪律」「理论不是论文，是跑得起来的东西」—— 定位语，无真伪可言。
- 「三律全映射」（旗舰 9 个）—— 需逐技能读其映射表才能判，本次列入「无法判断」。
- 「已报名微信大赛，AppID 仍在审批中（截至 2026-10-22）」—— 无公开登记库可查，列入「无法判断」。
- 「按项目评估报价，不构成要约」—— 自我限定语，已自带免责口径，无问题。

## 第二步 · 逐条核验（自洽 / 支撑 / 越界）

**断言 1（技能计数）—— 属实。** GitHub API 实测 `agent-skills/skills/` 共 109 个技能目录；首页链接的 81 个全部存在；分类计数 `9 + 31 + 16 + 10 + 15 = 81`，与页面公式「精选 81 = 旗舰 9 + 本页 72」一致。

**断言 2（uibc-core 数字）—— 数字全部属实，复现路径不全（见 (e)）。** 在 `73f31cc` 本机实跑（Python 3.12.3，与页面标注的 3.13.14 不同机不同版本，计数与环境无关）：

```
python -m unittest discover -s tests        → Ran 151 tests, OK ✓
python -m unittest tests.stress_test         → Ran 7 tests, OK ✓
python independent_verifier/cross_check.py   → checks compared: 70, mismatches: 0, AGREEMENT: PASS ✓
```

CI 运行 `39159391899`：`completed / success`，`head_sha` 正是 `73f31ccf58df` ✓ ——「同 commit 的 CI 亦为绿」属实。计时（约 17 秒 / 约 35 秒）为作者机器数据，本机更快，属「约」值，不构成问题。

**断言 3（lgd-theory）—— 属实。** `lgd-theory/docs/` 根目录实有 13 篇域论文（AUT/BIO/CRYPT/DAT/EDU/FIN×2/GOV/IND/LAW/MED/ROB/UAS），覆盖 12 个域码。「13 篇」与「12 个域码」两个数同时成立（FIN 有两篇）。但页面另一处与此打架，见 (a) / 必须改第 1 条。

**断言 4（SF 目录）—— 属实。** 仓内恰有 SF-001 至 SF-014 共 14 篇；抽查 SF-001、SF-007，均含 "Minimal reproduction" 与 "Self-check" 两节。「每个附最小复现与检测判据」在抽查范围内成立（未逐篇全查）。

**断言 5（SWH）—— 逐字属实。** SWH API 实测：三快照均存在；origin visits 与页面标注逐项一致 —— lgd-theory visit 1 / full / 2026-10-15、lgd-hub visit 1 / full / 2026-10-15、uibc-core visit 3 / full / 2026-10-15（uibc-core 另有 visit 1、2 在 9 月）。页面自带「取回仍依赖 SWH 服务可用 —— 这是存档证据，不是可用性承诺」的限定，准确。

**断言 6（Rekor）—— 逐字属实。** Rekor API 实测条目存在：logID `c0d23d6ad406973f…`（64 位十六进制）、integratedTime `1789710612` = 2026-09-18T05:50:12Z、kind = hashedrekord、inclusion proof 存在；`/api/v1/log` 的 treeID = `1193050959916656506`，与页面一致。页面「能证明什么 / 不能证明什么」的表述（不能证明签名者是谁、不能证明摘要属于哪个文件）在密码学上准确，是全页最严谨的一节。

**断言 7（SLSA 失败披露）—— 属实。** uibc-core 的 `build-provenance` 工作流仅有两次运行（2026-10-18），结论均为 failure；其 workflow 文件权限只有 `id-token: write` + `contents: read`，确实缺 `attestations: write`。页面主动披露自家管线坏了，与事实一致。

**断言 8（DOI）—— 理论资产节正确，首屏卡标错（见必须改第 5 条）。** DataCite 元数据：`10.5281/zenodo.22456647` 是概念 DOI（带 9 条 HasVersion 关系）；`10.5281/zenodo.23446125` 是版本 DOI（IsVersionOf 概念 DOI），Zenodo 记录显示其 version = 1.7.0。理论资产节「读 v1.7.0（版本 DOI）→ 23446125」「概念 DOI → 22456647」两个链接都对。但首屏卡文字写「附 Zenodo 版本 DOI」，按钮实际链到概念 DOI 22456647 —— 标签与所指不符（仓库 README 第 52 行把 22456647 正确标为 concept DOI，可见仓内口径本身是对的，错在首页首屏卡）。

**断言 9（许可表）—— 抽查 8 个仓，全部与各仓原文一致。** 逐仓读根目录权利文件实测：lgd-hub LICENSE = 自定义 ARR ✓；lgd-theory LICENSE = ARR ✓；silent-failure-catalog：LICENSE = MIT、LICENSE-CONTENT = ARR，分层属实 ✓；uibc-core：LICENSE = Apache-2.0，其 NOTICE.md 明写理论文本 ARR，分层属实 ✓；agent-skills：LICENSE 首页即范围声明（代码 MIT、文本 ARR），README 同步声明，分层属实 ✓；lgd-glossary LICENSE = CC BY 4.0 ✓；LGD LICENSE = Apache-2.0 ✓（首页「贡献入口（Apache-2.0）」标签正确）；lgd-skill-marketplace = MIT ✓。NOTICE 表「13 个仓」计数与表内行数一致（13）✓。NOTICE 自曝旧版曾把两仓写错并已更正 —— 更正后的版本经本次抽查属实。

**断言 10（身份）—— 属实。** ORCID `0009-0001-0512-1237` 公开记录存在，登记名 Steven Zhao。

## 第三步 · 五类专查

### (a) 过度宣称

「闭环」被页面自己的文字证伪（首屏）。首屏主张「把 AI 治理的判断做成可引用、可安装、可独立验证的闭环」；但理论资产节自承四件套中「身份护照那一项仍在内测、尚未开放，不参与『已可复算』计数」。四件缺一且未开放，对读者而言这个环没有闭合。页内限定语救了详情节，救不了首屏的无限制版主张。同理，产品节首的漏斗卡（第 03 步）把记忆护照写成已落地能力（「落地有籍·有证·有门禁」），产品详情节却写「内测中，暂未开放」—— 同一页两种状态。

「每个快照可用 SWHID 直接定址」—— 已实测成立，不算过度宣称。

「70 项规范一致性对拍」—— 注意 world.json 自带说明：对拍是「同一作者、两套实现、一份规范」，证明的是规范确定性而非第三方独立性。首页用词是「对拍 / 一致性」，没有冒称第三方独立验证，不算越界；但 `independent_verifier` 这个目录名容易让读者高估，页面未作澄清（仅记录，不列入必须改）。

### (b) 证据归属

未发现违规。本页在这一点上异常克制：SWH 快照只称「存档证据，不是可用性承诺」；Rekor 条目明写「不能证明签名者是谁，也不能证明摘要属于哪个文件或版本」；Zenodo 只称存稿存在与版本对应。没有出现"存在一条记录 ⇒ 证明是我的 / 证明我做了"的偷换。

### (c) 主体混淆

页面本体守住了。页脚三层分明：个人（赵兴华，独立研究者，ORCID）∕理论线（SynomosAI Governance Line —— 未注册实体、未注册商标，仅作来源标识）∕产业参考（MedXpert —— 仅指执业背景，不构成背书）；NOTICE.md 与 world.json 的 `identity_layers`（`policy: "do not merge"`）与页脚口径一致。正文各节未发现把服务归于机构名下、或把倡议写成法人之处。

**一处站外联动问题**（不在本页，但本页把该仓作为技能来源与许可汇总对象）：`agent-skills/TRADEMARK.md` 正文仍写「以下内容不属于 MIT 许可授权范围，权利归 SynomosAI」—— 权利归于一个未注册倡议，与本生态 2026-10-22 自己定的更正口径（`world.json` `legacy_metadata_note` 称已把 (c) 位的倡议名改为自然人）不一致。该仓页脚已改、正文未改。

### (d) 权属表述

NOTICE.md 称「下表于 2026-10-22 逐仓读 LICENSE 正文核对」—— 抽查 8 个仓（超过要求的 3 个），表内表述与各仓根目录权利文件原文全部一致，包括三个分层仓（silent-failure-catalog 代码 MIT / 正文 ARR；uibc-core 代码 Apache-2.0 / 理论 ARR；agent-skills 代码 MIT / 文本 ARR）的分层细节。页面「许可与贡献」节的概括（部分仓 Apache-2.0 / MIT，理论文本 ARR）与表一致。

**一处指引精度问题**：该节写「逐仓以 LICENSE 为准」—— 但 uibc-core 的分层写在其 NOTICE.md 里，其根 LICENSE 是纯 Apache-2.0 正文；只读 LICENSE 的读者会把该仓理论文本误当 Apache 授权，与作者本意相反。见必须改第 7 条。

### (e) 可复现性

三个数字中两个给了命令、且实跑得到相同结果（7 个压力场景、70 项对拍 0 分歧）✓。

「151 项测试」在页面上没有复现命令：卡片只印了 stress 与 cross_check 两条命令；跑出 151 的命令是 `python -m unittest discover -s tests`，只记在 world.json 里，没印在卡片上。更糟的是，陌生人最自然的试法 `python -m unittest`（无参数）在该 commit 上是 `Ran 0 tests` —— 页面等于亲手给"数字造假"的误判递了刀子。见必须改第 2 条。

页面另有一处可见的渲染垃圾：`index.html` 第 144 行附近有一个字面量 `\1` 印在 uibc-core 卡片正文与命令之间，线上页面可见。见必须改第 4 条。

### 无法判断（缺材料，不猜）

1. 「旗舰 9 个 · 三律全映射」—— 需逐个技能读其三律映射表逐项核对，本次未做全量阅读，无法判断。
2. 「81 个技能零依赖」—— 全量需审 106 个脚本的 import；抽查 4 个（agent-boarding-pass、agent-output-registry、ai-policy-radar、agent-redteam-kit）均为纯标准库，未发现反例，但不等于全量成立，无法判断。
3. 「已报名微信大赛，AppID 仍在审批中」—— 无公开渠道可核，无法判断（页面已自注日期，风险低）。
4. SkillPie 上架状态 —— 页面自带「以市场实时结果为准」的对冲表述，不构成固定断言，不核。

## 第四步 · 结论

**改完再说。**

理由：本页的可核验核心是真的 —— 计数、归档、签名日志、许可表、测试数字，本次逐项实测无一造假，多处自我披露（管线失败、护照未开放、Rekor 证明力边界）甚至严于行业常态，不存在撤下的理由。但首屏层面的三处毛病（闭环无限制宣称、本域化论文 12 与 4 自相矛盾、151 无复现命令）恰好都长在这页自称的卖点上（"可复核"），不改则伤的是它自己的立身之本。

### 必须改清单（8 条）

1. 跨域论文卡自相矛盾：「金融 / 法律 / 政务 / 隐私计算四域已有本域化论文」与旗舰卡「12 个域码的本域化论文」冲突（仓内实情为 12 域均有）。改为：「12 个域码均有本域化论文（见 lgd-theory/docs）；其中金融 / 法律 / 政务 / 隐私计算四域另有配套守门技能（C1–C4）」—— 若"四域"另有所指，必须写明指什么。
2. uibc-core 卡补第三条命令：在现有两条命令前加一行 `python -m unittest discover -s tests`，使「151 项测试」可从本页直接复现。
3. 首屏「闭环」加限定：改为「……可独立验证的四件套（三项已可复算，身份护照内测中）」，或护照开放前不在首屏使用无限制「闭环」。
4. 删掉 `index.html` 中的字面量 `\1`（自己验节 uibc-core 卡片正文与命令之间，约第 144 行）。
5. 首屏理论卡 DOI 标签改正：「附 Zenodo 版本 DOI」与所链概念 DOI 不符 —— 或把按钮改链 `10.5281/zenodo.23446125`（v1.7.0 版本 DOI），或把文字改为「附 Zenodo 概念 DOI」。
6. 第 03 步漏斗卡加状态：「记忆护照小程序」卡加「（内测中，暂未开放）」，与产品详情节口径一致。
7. 许可指引改词：「逐仓以 LICENSE 为准」改为「逐仓以各仓 LICENSE 与 NOTICE 为准」（uibc-core、agent-skills 的分层写在 NOTICE / 许可范围声明里）。
8. （站外联动）`agent-skills/TRADEMARK.md`：「权利归 SynomosAI」改为权利人「赵兴华 / Steven Zhao」，与全生态 2026-10-22 更正口径统一。

## 附 · 核验方法留痕

DateCite API：`api.datacite.org/dois/10.5281/zenodo.22456647` 与 `…/23446125`（关系字段 HasVersion / IsVersionOf）；Zenodo API record 23446125（version=1.7.0）。

SWH API：三个 snapshot 端点 + 三个 origin 的 visits 列表。

Rekor API：`rekor.sigstore.dev/api/v1/log/entries?logIndex=2883389783` 与 `/api/v1/log`。

GitHub API / raw 原文：agent-skills 技能目录树、各仓 LICENSE / NOTICE / LICENSE-CONTENT 原文、uibc-core commit `73f31cc` 与 Actions run `39159391899`、build-provenance 工作流运行记录、lgd-theory 与 silent-failure-catalog 文件树。

本机实跑：uibc-core `73f31cc` 快照（tarball）上执行页面与 world.json 所载三条命令，输出如报告所述。

ORCID 公开 API：`0009-0001-0512-1237` 记录。
