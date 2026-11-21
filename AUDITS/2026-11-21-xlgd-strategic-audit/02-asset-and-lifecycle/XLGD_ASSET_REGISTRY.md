# XLGD_ASSET_REGISTRY（资产主索引 · 2026-11-21）

> 口径：仓库/账号/许可证/最新推送/star 来自 GitHub API 实查（2026-11-21 06:2x CST）；版本来自仓库内 `pyproject.toml` / `package.json` / `VERSION`；可运行性/测试结论引自同日只读审计（`XLGD_最新阶段推进报告_20261121.md`、`sub_LGD-Eval_audit_20261121.md`）。标注：**V**=实查成立，**P**=部分实查，**N**=未查证，**I**=推断。

## 0 · 全景数字（V）

- 自有仓库 **141** 个，fork **31** 个，合计 **172** 个（4 个账号：理论号 / 产品号 / 评测号 / Medxpert-org）。
- 许可证分布：MIT 60、NOASSERTION 38、Apache-2.0 20、无证 15、CC-BY-4.0 7、AGPL-3.0 1。
- 跨账号重名（自有仓）：lgd-theory ×2；lgd-skills ×2；medxpert-skills ×2；.github ×3。
- star 合计：uibc-core 12、silent-failure-catalog 9、lgd-theory 7、agent-skills 5、其余 ≤3；**外部人类贡献者 0**（三个号互不独立）。

## A · 核心资产登记卡（16 张）


### A1 · LGD Theory（理论唯一真源）
- **Asset ID** `LGD-THEORY-001` ｜ **仓库** `zhaoxinghua09-cell/lgd-theory` ｜ **账号** 理论号 ｜ **版本** 未设版（仓库无 VERSION/pyproject）
- **状态** 活跃（2026-11-20 推送，7 stars，5.5 MB）；**用途** 三律/生命周期治理的理论与论文真源；**解决** "判定层缺失"的理论表述
- **依赖** 无运行时依赖（文本+少量脚本）；**上下游** 上游=论文/DOID；下游=uibc-core / lgd-engine / LGD-Eval 均引用它作理论 SSOT
- **License** GitHub 识别为 NOASSERTION（仓内文本保留所有权利）｜ **IP** 赵兴华个人
- **重复** `Medxpert-org/lgd-theory`（历史镜像，最后推送 2026-10-03，内容真源不在此）
- **独立用户/外部集成** 无证据 ｜ **真实使用证据** 仅作者自引 ｜ **可商业化** 间接（作为方法论背书）
- **风险** 缩写 UIBC 两种展开、NOASSERTION 使外部无法判断可用范围 ｜ **下一步** 在 README 顶部写一行 LICENSE 指向 + 镜像仓跳转声明

### A2 · UIBC Protocol / uibc-core（协议与参考实现 + 校验器）
- **Asset ID** `UIBC-CORE-002` ｜ **仓库** `zhaoxinghua09-cell/uibc-core` ｜ **版本** 0.5.0（pyproject），`v0.5.0-20-g2088469`
- **状态** 活跃（12 stars / 2 forks / 1015 tests 全绿）；**用途** 证据包、注册表状态机、门禁、Rekor 锚定与三值校验
- **解决** "一份证据能否被另一台机器独立重算"；**依赖** Python ≥3.10 标准库；签名校验可选 `cryptography`
- **上下游** 上=lgd-theory；下=lgd-engine(判定)、LGD-Eval(评测对象)、lgd-hub(入口)、validator kit
- **License** Apache-2.0（代码）/ 理论文本保留 ｜ **IP** 赵兴华
- **重复** fork：`LGD-Eval/uibc-core`（评测号只读镜像）、`stevenzhao07/uibc-core`
- **独立用户/外部集成** **0 外部人类 PR/issue**；1 条外部公开引用（AER-1 作者，记录 Merkle 分歧）｜ **真实使用证据** 外部节点 1 份（作者邀请）
- **可商业化** 是（按次证据复核）｜ **风险** v0.5.0 不含 #351–#355；缺 `cryptography` 时"签名未验仍 exit 0"
- **下一步** 拆 `verified_*` 字段 + 打 0.5.1 + 把验证者包外发

### A3 · UIBC Competition / Benchmark
- **Asset ID** `UIBC-COMP-003` ｜ **仓库** `zhaoxinghua09-cell/uibc-competition` ｜ **版本** 未设版 ｜ **License** NOASSERTION
- **状态** 3 stars、最后推送 2026-11-13；**用途** 赛事/对标叙事 ｜ **解决** 公开比较场
- **依赖/上下游** 依赖 uibc-core 语料；下游=传播
- **重复** 与 `uibc-core/conformance` 语料存在功能重叠（"比赛"与"语料"两套入口）
- **独立用户** 无 ｜ **可商业化** 弱（可作引流）｜ **风险** 名称与 ORCID 的 "Universal Intelligent-agent Benchmark Championship" 展开冲突
- **下一步** 要么并入 uibc-core 的 conformance 入口，要么明确为"传播页"不与协议同名

### A4 · LGD-Eval（评测引擎与评测档案）
- **Asset ID** `LGD-EVAL-004` ｜ **仓库** `LGD-Eval/LGD-Eval` ｜ **版本** 1.0.0（package.json）｜ **License** CC-BY-4.0（与 MIT 声明冲突）
- **状态** 活跃（2 stars，CI 自评 90 阈值）；**用途** Skill/Agent 五维评分 + 三律 + 整改清单
- **解决** "上架前有没有一道可跑的检查" ｜ **依赖** 纯 stdlib（Python 3.9+）；npm 包装需 Node 16+
- **上下游** 上=lgd-gate（CI action，跨仓）；下=skillgate（同源扫描器）、evaluation-evidence（公开评分卡）
- **重复** fork `zhaoxinghua09-cell/LGD-Eval`；同目录另有 LGD-Eval/lgd-gate、evaluation-protocol、evaluation-evidence、evaluation-reports 四个"评测家族"仓
- **独立用户/外部集成** 无证据 ｜ **真实使用证据** 仅自评（且自评数据与 benchmarks 声称不一致）
- **可商业化** 是，但**当前不可**（3 条 P0：恶意样本放行、SSH 漏报、残缺对象 fail-open）
- **风险** 分数→L0–L5 权限映射被当授权；4 处入口元组崩溃 ｜ **下一步** 先修 P0，再对外

### A5 · SynomosAI Governance MCP
- **Asset ID** `SYN-MCP-005` ｜ **仓库** `zhaoxinghua09-cell/synomosai-governance-mcp` ｜ **版本** 1.2.2（PyPI 一致）
- **状态** 可用（6 工具真握手通过；PyPI 近一日 2 次下载）｜ **用途** A³ 自评、证据工件模板、合规清单、PII 扫描、护照查询、LGD 知识
- **解决** "治理审计从哪问起" ｜ **依赖** 纯 stdlib，stdio + HTTP
- **上下游** 下游=接入方 Agent 平台；上=SynomosAI 方法论
- **License** MIT ｜ **IP** 赵兴华 / SynomosAI（个人品牌，非法人）
- **重复** `Medxpert-org/ubic-governance-mcp`（同名族不同拼写，需并或改名）
- **独立用户** 无 ｜ **可商业化** 是（治理接入）｜ **风险** 审计日志无防篡改、Registry 为 3 条硬编码示例
- **下一步** 审计日志加 hash chain + 真实 Registry 落库

### A6 · Agent Skills（技能库主体）
- **Asset ID** `SKILLS-006` ｜ **仓库** `zhaoxinghua09-cell/agent-skills` ｜ **版本** 未设版 ｜ **License** NOASSERTION
- **状态** 活跃（5 stars，13.9 MB，"119 个零依赖技能"）｜ **用途** 治理/办公/医械技能集合
- **上下游** 下游=skillgate/LGD-Eval 评测；入口=lgd-hub
- **重复** 与 `lgd-skills`（zhaoxinghua09-cell + stevenzhao07 两份）、`Medxpert-org/medxpert-skills` + `stevenzhao07/medxpert-skills` 形成"技能库四分"
- **独立用户** 无 ｜ **可商业化** 是（技能订阅/审核）｜ **风险** 技能数量宣称与可运行验证未对齐；许可证不明确
- **下一步** 技能库合一：一个索引仓 + 三个主题子目录，停止新增同名仓

### A7 · MedXpert Skills / MedXpert 应用线
- **Asset ID** `MEDX-SKILLS-007` ｜ **仓库** `Medxpert-org/medxpert-skills`（Apache-2.0）＋ `stevenzhao07/medxpert-skills`（MIT，镜像）
- **状态** 两边各 1 star、11-08/11-09 后未动 ｜ **用途** NMPA/FDA/510(k)/MDR 医械合规技能
- **解决** 注册事务的重复劳动 ｜ **上下游** 下游=medxpert-reg-hub / reg-connector（MCP）
- **重复** 同名两仓（许可证不同）｜ **独立用户** 无 ｜ **可商业化** 最成熟（医械注册是真实付费场景）
- **风险** 品牌被表述为公司（红线）；技能与法规版本绑定缺失 ｜ **下一步** 定一个真源仓，另一仓改为归档+跳转

### A8 · Trust Registry（注册表）
- **Asset ID** `REGISTRY-008` ｜ **仓库** `zhaoxinghua09-cell/skill-registry`（MIT，1 star）＋ uibc-core 内 `registry/`、`registry_server/`
- **状态** 组件存在、无真实注册数据 ｜ **用途** 身份码/版本/证据指针登记
- **解决** "这个 agent/skill 是谁、哪个版本" ｜ **依赖** uibc-core
- **重复** 与 SynomosAI 的 `PASSPORT_LEDGER`（硬编码 3 条）功能重叠
- **独立用户** 无 ｜ **可商业化** 间接 ｜ **风险** 无外部写入、无撤销语义 ｜ **下一步** 与 Trust Passport 合并为一张表

### A9 · Evidence Engine（证据引擎）
- **Asset ID** `EVIDENCE-009` ｜ **仓库** `zhaoxinghua09-cell/evidence-anchor`（MIT）＋ `claim-audit`（MIT）＋ uibc-core 内 `uibc_core/evidence*`
- **状态** 组件级可用（evidence-anchor 解析 file:line；claim-audit 复算文档宣称）｜ **用途** 证据锚定与宣称复核
- **上下游** 上=uibc-core 证据包；下=LGD-Eval 的报告证据
- **重复** 与 `evidence-gated-medical-agent-demo`、`d4-evidence-authorization` 部分重叠
- **独立用户** 无 ｜ **可商业化** 是（证据复核服务）｜ **风险** 无统一 Evidence Manifest 规范 ｜ **下一步** 定 Evidence Manifest v1（字段与哈希口径）

### A10 · Trust Passport
- **Asset ID** `PASSPORT-010` ｜ **仓库** `Medxpert-org/ai-passport-spec`（NOASSERTION）＋ `stevenzhao07/ai-model-passport` ＋ SynomosAI `passport_lookup`
- **状态** 规格存在、实现为示例台账 ｜ **用途** 可携带信任凭证
- **重复** 三处口径（spec / model passport / MCP lookup）
- **独立用户** 无 ｜ **可商业化** 是（企业审计入口）｜ **风险** "Passport ≠ 认证"需在规格第一行写死
- **下一步** 用 A2 的证据包做 Passport 的 evidence 段，禁止另造数据结构

### A11 · Silent Failure Catalog（失败目录）
- **Asset ID** `FAILCAT-011` ｜ **仓库** `zhaoxinghua09-cell/silent-failure-catalog` ｜ **版本** 未设版 ｜ **License** NOASSERTION
- **状态** 活跃（9 stars，2026-11-20 推送）｜ **用途** 16 类"通过但没检查"的失败模式（SF-001…SF-016）+ `patterns.json` + 27 个工具
- **解决** 把"检查器自身的假通过"变成可复现案例 ｜ **上下游** 上=lgd-theory；下=LGD-Eval 规则、skill-redteam-suite
- **重复** fork `stevenzhao07/`、`LGD-Eval/`（两个只读镜像）
- **独立用户** 无（9 star 无外部 issue）｜ **可商业化** 是（失败样本库是壁垒）｜ **风险** 案例缺"外部复现状态/修复版本"字段
- **下一步** 按本指令五的 18 字段统一案例结构（现有案例只覆盖前 10 个字段）

### A12 · Assayance
- **Asset ID** `ASSAY-012` ｜ **仓库** `zhaoxinghua09-cell/assayance` ｜ **版本** 未设版 ｜ **License** NOASSERTION
- **状态** 1 star、11-06 后未动、无 tests ｜ **用途** "一个检查是不是检查"的元方法
- **重复** 与 silent-failure-catalog 概念重叠 ｜ **可商业化** 弱 ｜ **下一步** 并入 FAILCAT 作为方法章，或明确为论文配套

### A13 · LGD Hub（入口）
- **Asset ID** `HUB-013` ｜ **仓库** `zhaoxinghua09-cell/lgd-hub` ｜ **版本** 未设版 ｜ **License** NOASSERTION
- **状态** 活跃（3 stars，11-20 推送；#77 "invites 02–05 recorded as not_counted"）｜ **用途** 7 个治理技能的可运行入口
- **重复** 与 `zhaoxinghua09-cell/LGD`（入口仓，Apache-2.0，1 star）功能重叠
- **独立用户** 无（邀请 4 个、均未计入）｜ **可商业化** 间接 ｜ **风险** 入口分散 ｜ **下一步** 合并为唯一入口页

### A14 · LGD Engine（判定核）
- **Asset ID** `ENGINE-014` ｜ **仓库** `Medxpert-org/lgd-engine` ｜ **版本** 0.1.1 ｜ **License** Apache-2.0
- **状态** 可用（89 passed / 5 skipped；OpenAPI 20/20）｜ **用途** 医械变更五档判定（510(k)/PCCP/MDR/NMPA）
- **重复** 与 lcas（变更裁决规范）部分重叠 ｜ **独立用户** 无 ｜ **可商业化** 是（医械变更判定）｜ **风险** TS 第二实现未与 Python 逐条对账（L3 自评"部分"）
- **下一步** 把 TS 实现接入同一批 conformance 向量

### A15 · 独立验证组件（xverify / iverify / gate）
- **Asset ID** `VERIFY-015` ｜ 仓：`zhaoxinghua09-cell/lgd-xverify`（Apache）、`uibc-iverify`（Apache）、`LGD-Eval/lgd-gate`（MIT）
- **状态** 组件可跑；`uibc-iverify` 17 KB 级、`lgd-xverify` 57 KB 级；lgd-gate 被 CI 当 action 调用（黑盒）
- **重复** 三套"跨格式裁决"入口 ｜ **独立用户** 无 ｜ **可商业化** 是（作为核验服务的执行端）
- **风险** lgd-gate 退出语义不在本仓、不可审计 ｜ **下一步** 统一到一个 CLI + 一份 spec

### A16 · 授权与生命周期（d4 / a22 / xcgs）
- **Asset ID** `LIFECYCLE-016` ｜ 仓：`d4-evidence-authorization`（无许可证）、`a22-trust-lifecycle`（无许可证）、`Medxpert-org/xcgs-governance`（v1.2, MIT）
- **状态** 均为**草稿/输入文档**，无 tests（a22 1.8 KB README、d4 112 KB）｜ **用途** 授权有效期、生命周期框架、A³/护照
- **重复** 三者对"授权/生命周期"各说一套 ｜ **风险** 无许可证=不可被外部采用 ｜ **下一步** 合成一份 `TRUST_LIFECYCLE_SPEC`（见 B 文件）


## B · 全量自有仓附录（按最新推送排序）

| # | 仓库 | 账号 | 类别 | License | 最新推送 | ★ | 大小 KB | 重复名 |
|---|---|---|---|---|---|---|---|---|
| 1 | silent-failure-catalog | 理论号 | 其他 | NOASSERTION | 2026-11-20 | 9 | 717 |  |
| 2 | uibc-core | 理论号 | 协议 | Apache-2.0 | 2026-11-20 | 12 | 4238 |  |
| 3 | lgd-hub | 理论号 | LGD 线 | NOASSERTION | 2026-11-20 | 3 | 1189 |  |
| 4 | LGD-Eval | 评测号 | LGD 线 | CC-BY-4.0 | 2026-11-20 | 2 | 699 |  |
| 5 | evaluation-reports | 评测号 | MedXpert | CC-BY-4.0 | 2026-11-20 | 1 | 289 |  |
| 6 | lgd-theory | 理论号 | LGD 线 | NOASSERTION | 2026-11-20 | 7 | 5538 | 是 |
| 7 | lgd-glossary | 理论号 | LGD 线 | NOASSERTION | 2026-11-20 | 2 | 71 |  |
| 8 | lgd-skill-review | 理论号 | LGD 线 | MIT | 2026-11-20 | 0 | 1358 |  |
| 9 | evaluation-evidence | 评测号 | Skills/评测 | CC-BY-4.0 | 2026-11-20 | 1 | 406 |  |
| 10 | evaluation-protocol | 评测号 | 其他 | CC-BY-4.0 | 2026-11-20 | 2 | 563 |  |
| 11 | nti-lgd-transition-contract | 理论号 | LGD 线 | NOASSERTION | 2026-11-19 | 1 | 19 |  |
| 12 | lgd-engine | Medxpert-org | LGD 线 | Apache-2.0 | 2026-11-19 | 0 | 786 |  |
| 13 | debug-pro | 理论号 | 其他 | MIT | 2026-11-19 | 0 | 509 |  |
| 14 | agent-skills | 理论号 | Skills/评测 | NOASSERTION | 2026-11-19 | 5 | 13955 |  |
| 15 | wechat-viral-topic | 理论号 | 其他 | NOASSERTION | 2026-11-19 | 1 | 643 |  |
| 16 | summarize-pro | 理论号 | 其他 | MIT | 2026-11-19 | 1 | 673 |  |
| 17 | d4-evidence-authorization | 理论号 | 证据 | none | 2026-11-18 | 0 | 112 |  |
| 18 | lgd-loop-fixture | 理论号 | LGD 线 | MIT | 2026-11-18 | 0 | 2 |  |
| 19 | lgd-skills | 理论号 | LGD 线 | MIT | 2026-11-18 | 0 | 1229 | 是 |
| 20 | c45-skill-metrics | 理论号 | Skills/评测 | none | 2026-11-18 | 0 | 26 |  |
| 21 | a18-skill-supply-chain | 理论号 | Skills/评测 | none | 2026-11-18 | 0 | 26 |  |
| 22 | a28-behavioural-signals | 理论号 | 其他 | none | 2026-11-18 | 0 | 28 |  |
| 23 | uibc-iverify | 理论号 | 协议 | Apache-2.0 | 2026-11-18 | 0 | 17 |  |
| 24 | a22-trust-lifecycle | 理论号 | 其他 | none | 2026-11-18 | 0 | 89 |  |
| 25 | lgd-hit-list | 理论号 | LGD 线 | none | 2026-11-18 | 0 | 4 |  |
| 26 | claim-audit | 理论号 | Skills/评测 | MIT | 2026-11-18 | 0 | 28 |  |
| 27 | skill-redteam-suite | 理论号 | Skills/评测 | MIT | 2026-11-18 | 0 | 28 |  |
| 28 | evidence-anchor | 理论号 | 证据 | MIT | 2026-11-18 | 0 | 19 |  |
| 29 | skill-improver | 理论号 | Skills/评测 | MIT | 2026-11-18 | 0 | 25 |  |
| 30 | lgd-skills | 产品号 | LGD 线 | MIT | 2026-11-18 | 0 | 1282 | 是 |
| 31 | lcas | Medxpert-org | 其他 | Apache-2.0 | 2026-11-18 | 0 | 806 |  |
| 32 | ai-passport-spec | Medxpert-org | Agent 基建 | NOASSERTION | 2026-11-18 | 0 | 405 |  |
| 33 | skillgate | 理论号 | LGD 线 | MIT | 2026-11-18 | 0 | 501 |  |
| 34 | fgtida-paris-input-2026 | 理论号 | 其他 | MIT | 2026-11-18 | 0 | 614 |  |
| 35 | medxpert-reg-connector | 理论号 | MedXpert | Apache-2.0 | 2026-11-18 | 1 | 282 |  |
| 36 | regdoc-commons | 产品号 | 其他 | Apache-2.0 | 2026-11-18 | 0 | 200 |  |
| 37 | lgd-xverify | 理论号 | LGD 线 | Apache-2.0 | 2026-11-18 | 0 | 57 |  |
| 38 | skill-scout | 评测号 | LGD 线 | MIT | 2026-11-18 | 0 | 95 |  |
| 39 | doc-translate-keep-layout | 产品号 | 其他 | MIT | 2026-11-18 | 0 | 97 |  |
| 40 | medxpert-ortho-mcp | 理论号 | MedXpert | NOASSERTION | 2026-11-18 | 0 | 50 |  |
| 41 | lgd-skill-marketplace | 理论号 | LGD 线 | MIT | 2026-11-18 | 1 | 29 |  |
| 42 | lgd-skeleton | 理论号 | LGD 线 | MIT | 2026-11-18 | 1 | 70 |  |
| 43 | fgtida-contribution-discovery-evidence | 理论号 | 证据 | MIT | 2026-11-18 | 0 | 109 |  |
| 44 | skill-scorecard | 理论号 | Skills/评测 | Apache-2.0 | 2026-11-18 | 1 | 80 |  |
| 45 | Nomos | 理论号 | 其他 | NOASSERTION | 2026-11-18 | 1 | 38 |  |
| 46 | synomosai-governance-mcp | 理论号 | LGD 线 | MIT | 2026-11-17 | 1 | 82 |  |
| 47 | fg-tida-r04-contrib | 理论号 | Agent 基建 | CC-BY-4.0 | 2026-11-17 | 1 | 142 |  |
| 48 | conformance-surface-2026-11 | 理论号 | Agent 基建 | CC-BY-4.0 | 2026-11-17 | 0 | 42 |  |
| 49 | theme50-contribution-matrix | 理论号 | 其他 | CC-BY-4.0 | 2026-11-17 | 0 | 39 |  |
| 50 | evidence-gated-medical-agent-demo | 理论号 | Agent 基建 | Apache-2.0 | 2026-11-17 | 0 | 47 |  |
| 51 | xlgd | 理论号 | LGD 线 | MIT | 2026-11-17 | 3 | 43 |  |
| 52 | awesome-trusted-agents | 理论号 | Skills/评测 | MIT | 2026-11-17 | 1 | 100 |  |
| 53 | skill-skeleton-generator | 理论号 | LGD 线 | MIT | 2026-11-17 | 1 | 15 |  |
| 54 | skill-registry | 理论号 | Skills/评测 | MIT | 2026-11-17 | 1 | 16 |  |
| 55 | skill-quality-gate | 理论号 | LGD 线 | MIT | 2026-11-17 | 1 | 15 |  |
| 56 | silent-failure-scanner | 理论号 | 其他 | MIT | 2026-11-17 | 1 | 15 |  |
| 57 | prompt-injection-guard | 理论号 | 其他 | MIT | 2026-11-17 | 1 | 18 |  |
| 58 | llms-generator | 理论号 | Agent 基建 | MIT | 2026-11-17 | 1 | 15 |  |
| 59 | badge-studio | 理论号 | 其他 | MIT | 2026-11-17 | 1 | 15 |  |
| 60 | medxpert-standards-connector | 理论号 | MedXpert | Apache-2.0 | 2026-11-16 | 1 | 95 |  |
| 61 | ubic-governance-mcp | Medxpert-org | 证据 | MIT | 2026-11-16 | 0 | 160 |  |
| 62 | medxpert-library-connector | 理论号 | MedXpert | NOASSERTION | 2026-11-16 | 3 | 86 |  |
| 63 | medxpert-reg-hub | 产品号 | Skills/评测 | MIT | 2026-11-16 | 0 | 459 |  |
| 64 | med-device-compliance-toolkit | 理论号 | 其他 | MIT | 2026-11-16 | 1 | 57 |  |
| 65 | medical-device-testing-link | 理论号 | 其他 | MIT | 2026-11-16 | 1 | 335 |  |
| 66 | medical-device-reg-translator | 理论号 | 其他 | MIT | 2026-11-16 | 1 | 22 |  |
| 67 | medxpert-standards | 理论号 | MedXpert | MIT | 2026-11-16 | 3 | 117 |  |
| 68 | uibc-competition | 理论号 | 协议 | NOASSERTION | 2026-11-13 | 3 | 126 |  |
| 69 | ai-governance-checklist | 产品号 | 其他 | NOASSERTION | 2026-11-13 | 0 | 70 |  |
| 70 | lgd-gate | 评测号 | LGD 线 | MIT | 2026-11-13 | 1 | 168 |  |
| 71 | skill-audit | 评测号 | Skills/评测 | Apache-2.0 | 2026-11-11 | 2 | 310 |  |
| 72 | medical-ai-toolkit | 产品号 | LGD 线 | NOASSERTION | 2026-11-09 | 1 | 207 |  |
| 73 | medxpert-skills | 产品号 | Skills/评测 | MIT | 2026-11-09 | 1 | 63 | 是 |
| 74 | samd-ra-toolkit | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 1 | 64 |  |
| 75 | iso14971-risk-file | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 0 | 47 |  |
| 76 | device-regulatory-map | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 0 | 56 |  |
| 77 | ai-model-passport | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 0 | 68 |  |
| 78 | medxpert-fhir | 产品号 | MedXpert | none | 2026-11-09 | 0 | 59 |  |
| 79 | sterilization-validation | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 0 | 49 |  |
| 80 | udi-assignment | 产品号 | 其他 | NOASSERTION | 2026-11-09 | 0 | 46 |  |
| 81 | ubic-site | Medxpert-org | 其他 | MIT | 2026-11-09 | 0 | 51 |  |
| 82 | agent-runtime-governance | Medxpert-org | Agent 基建 | Apache-2.0 | 2026-11-09 | 0 | 62 |  |
| 83 | .github | Medxpert-org | MedXpert | NOASSERTION | 2026-11-09 | 0 | 46 | 是 |
| 84 | stevenzhao07 | 产品号 | 其他 | Apache-2.0 | 2026-11-09 | 0 | 56 |  |
| 85 | dsh-plugin-lgd-trust | 评测号 | LGD 线 | NOASSERTION | 2026-11-09 | 0 | 80 |  |
| 86 | competitor-comparison | 评测号 | Skills/评测 | none | 2026-11-08 | 0 | 91 |  |
| 87 | lgd-skills-index | 理论号 | LGD 线 | NOASSERTION | 2026-11-08 | 0 | 73 |  |
| 88 | medxpert-skills | Medxpert-org | Skills/评测 | Apache-2.0 | 2026-11-08 | 1 | 44 | 是 |
| 89 | medxpert-skill-index | Medxpert-org | Skills/评测 | Apache-2.0 | 2026-11-08 | 1 | 20 |  |
| 90 | delivery-guard | 产品号 | MedXpert | NOASSERTION | 2026-11-06 | 1 | 103 |  |
| 91 | multilingual-ifu | 产品号 | 其他 | NOASSERTION | 2026-11-06 | 0 | 84 |  |
| 92 | xcgs-manifesto | 理论号 | 其他 | NOASSERTION | 2026-11-06 | 2 | 17 |  |
| 93 | terminance | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 2 | 10 |  |
| 94 | runtigil | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 10 |  |
| 95 | project-ops-protocol | 理论号 | Agent 基建 | NOASSERTION | 2026-11-06 | 1 | 14 |  |
| 96 | mnemoship | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 10 |  |
| 97 | medxpert-voice-kb | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 108 |  |
| 98 | medxpert-registration-ops | 理论号 | MedXpert | Apache-2.0 | 2026-11-06 | 1 | 1999 |  |
| 99 | medxpert-reg-kb | 理论号 | MedXpert | NOASSERTION | 2026-11-06 | 1 | 60 |  |
| 100 | medxpert-llm-library | 理论号 | Skills/评测 | MIT | 2026-11-06 | 2 | 89 |  |
| 101 | medical-device-reg-expert | 理论号 | Agent 基建 | Apache-2.0 | 2026-11-06 | 1 | 25 |  |
| 102 | lgd-demo-organization | 理论号 | LGD 线 | MIT | 2026-11-06 | 0 | 68 |  |
| 103 | identity-verify | 理论号 | Skills/评测 | MIT | 2026-11-06 | 1 | 36 |  |
| 104 | fingerprint-delivery | 理论号 | Agent 基建 | MIT | 2026-11-06 | 1 | 50 |  |
| 105 | dsh-secret-leakage-scan | 理论号 | 其他 | MIT | 2026-11-06 | 1 | 14 |  |
| 106 | culpachain | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 9 |  |
| 107 | credential-vault-design | 理论号 | Skills/评测 | MIT | 2026-11-06 | 1 | 530 |  |
| 108 | context-token-budget | 理论号 | 其他 | MIT | 2026-11-06 | 1 | 12 |  |
| 109 | a3-law-operational | 理论号 | 其他 | MIT | 2026-11-06 | 1 | 11 |  |
| 110 | assayance | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 1777 |  |
| 111 | assurability | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 10 |  |
| 112 | authz-code-design | 理论号 | Skills/评测 | MIT | 2026-11-06 | 1 | 62 |  |
| 113 | agent-soul-os | 理论号 | Skills/评测 | Apache-2.0 | 2026-11-06 | 1 | 451 |  |
| 114 | agent-memory-service | 理论号 | Agent 基建 | AGPL-3.0 | 2026-11-06 | 1 | 236 |  |
| 115 | paper1-verifier-side-silent-failures | 理论号 | Agent 基建 | NOASSERTION | 2026-11-06 | 1 | 208 |  |
| 116 | zhaoxinghua09-cell | 理论号 | 其他 | none | 2026-11-06 | 1 | 42 |  |
| 117 | medxpert-reg-path-skill | 产品号 | Skills/评测 | MIT | 2026-11-06 | 0 | 64 |  |
| 118 | LGD | 理论号 | 协议 | Apache-2.0 | 2026-11-06 | 1 | 82 |  |
| 119 | agent-trust-identity-spec | 理论号 | Agent 基建 | MIT | 2026-11-06 | 3 | 95 |  |
| 120 | lgd-medai-demo | 理论号 | LGD 线 | Apache-2.0 | 2026-11-06 | 1 | 62 |  |
| 121 | medxpert-ai-gov-kb | 理论号 | LGD 线 | NOASSERTION | 2026-11-06 | 1 | 291 |  |
| 122 | medxpert-pre-submission-check-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 14 |  |
| 123 | medxpert-master-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 5 |  |
| 124 | medxpert-labeling-ifu-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 23 |  |
| 125 | medxpert-deficiency-reply-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 21 |  |
| 126 | medxpert-clinical-eval-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 11 |  |
| 127 | medxpert-ai-samd-reg-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 15 |  |
| 128 | medxpert-test-lab-selection-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 6 |  |
| 129 | medxpert-risk-management-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 5 |  |
| 130 | medxpert-postmarket-surveillance-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 6 |  |
| 131 | medxpert-oem-cmo-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 6 |  |
| 132 | medxpert-hospital-bid-skill | 产品号 | Skills/评测 | MIT | 2026-10-31 | 0 | 5 |  |
| 133 | xcgs-governance | Medxpert-org | 证据 | MIT | 2026-10-28 | 1 | 118 |  |
| 134 | .github | 产品号 | Agent 基建 | none | 2026-10-24 | 0 | 7 | 是 |
| 135 | .github | 评测号 | LGD 线 | none | 2026-10-24 | 0 | 7 | 是 |
| 136 | robot-ota-regate-eval | 评测号 | LGD 线 | none | 2026-10-18 | 0 | 0 |  |
| 137 | robot-blackbox-replay-eval | 评测号 | LGD 线 | none | 2026-10-18 | 0 | 0 |  |
| 138 | robot-identity-registry-eval | 评测号 | LGD 线 | none | 2026-10-18 | 0 | 0 |  |
| 139 | itu-fg-tida | Medxpert-org | 其他 | none | 2026-10-08 | 0 | 1 |  |
| 140 | lgd-theory | Medxpert-org | LGD 线 | NOASSERTION | 2026-10-03 | 0 | 12 | 是 |
| 141 | traceability-audit | Medxpert-org | 其他 | MIT | 2026-08-29 | 0 | 80 |  |

## C · 资产重复与整合建议（I，基于以上实查）


| 重复簇 | 成员 | 冲突点 | 建议（只做建议，不动仓） |
|---|---|---|---|
| 理论 | `zhaoxinghua09-cell/lgd-theory` vs `Medxpert-org/lgd-theory` | 镜像停在 10-03，内容真源只在个人号 | 镜像仓 README 首行放"已归档，见真源"，禁止再改内容 |
| 协议 | `uibc-core` 三个（1 主 2 fork） | fork 各自有独立推送时间，外部会误认多个版本 | fork 改为只读镜像并关闭 Actions |
| 评测家族 | LGD-Eval 侧 5 仓（LGD-Eval / lgd-gate / evaluation-protocol / evaluation-evidence / evaluation-reports） | 谁是"引擎"、谁是"报告"没有单一入口 | 以 LGD-Eval 为引擎，另四个在 README 顶部互链成"引擎→规范→证据→报告"一条链 |
| 技能库 | `agent-skills` / `lgd-skills`×2 / `medxpert-skills`×2 | 四个"技能库"，两两不同许可证 | 定一个索引仓，其余归档；许可证统一到一个 |
| 入口 | `LGD` / `lgd-hub` / `xlgd` | 三个"入口" | 合为一个导航页（见 E 文件思考） |
| 治理 MCP | `synomosai-governance-mcp` / `ubic-governance-mcp` | 名称近似、内容不同 | 保留前者为产品，后者并入或改名 |
| 独立验证 | `lgd-xverify` / `uibc-iverify` / `lgd-gate` | 三套裁决入口 | 合成一个 CLI：`verify --profile uibc|lgd|gate` |
| 生命周期 | `d4-evidence-authorization` / `a22-trust-lifecycle` / `xcgs-governance` | 各说一套、两个无许可证 | 收敛到一份 TRUST_LIFECYCLE_SPEC，草稿仓转为引用 |


## D · 许可证与知识产权风险（V）


- **无许可证的仓 15 个**（含 `d4-evidence-authorization`、`a22-trust-lifecycle`、`uibc-competition`、`c45-skill-metrics`、`a18-skill-supply-chain`）：法律上"保留所有权利"，外部**不能**合法复用，这会直接卡开发者采用。
- **NOASSERTION 38 个**：GitHub 无法识别，外部同样无法判断权利范围（理论仓、失败目录、LGD Hub、Agent Skills 都在这类）。
- **LGD-Eval 四方口径冲突**：LICENSE=CC BY 4.0 / package.json+pyproject=MIT / README 工具=Apache-2.0（P1-9）。
- 本清单只陈述事实，**不改变任何许可证**（按指令原则七）。


## E · 结论（三句话）


1. **资产不缺，缺"唯一入口 + 唯一真源"**：141 个自有仓里，真正承担主线的只有 16 个，其余大量是草稿、镜像、一次性实验。
2. **最大的外部摩擦不是能力，而是许可证与重名**：38 个 NOASSERTION + 15 个无证 + 4 组同名，让外部开发者"想用也不敢用、想引用也不知道引哪个"。
3. **唯一有外部痕迹的资产是 uibc-core（1 条外部引用 + 120 次/日 PyPI 下载）**，其余资产的"独立用户/外部集成/真实使用证据"三列全为 0——这是差距，不是描述口径问题。
