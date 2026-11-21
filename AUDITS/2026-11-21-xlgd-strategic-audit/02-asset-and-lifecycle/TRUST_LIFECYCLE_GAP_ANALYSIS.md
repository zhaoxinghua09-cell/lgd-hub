# TRUST_LIFECYCLE_GAP_ANALYSIS（信任生命周期闭环缺口 · 2026-11-21）

> 方法：对 10 个阶段逐一问四个问题——**有没有可执行资产、有没有失败状态、有没有机器可读结果、能不能跨工具/离线传递**。
> 证据来源：同日只读审计（`XLGD_最新阶段推进报告_20261121.md`、`sub_LGD-Eval_audit_20261121.md`）、仓库实读、`XLGD_ASSET_REGISTRY.md`。
> 标注：**V** 实查 / **P** 部分 / **N** 未查证 / **I** 推断。

## 一、总表

| # | 阶段 | 现有可执行资产 | 失败状态 | 机器可读 | 离线 | 跨工具 | 判定 | 最大缺口 |
|---|---|---|---|---|---|---|---|---|
| 1 | Identity 身份 | ai-passport-spec（规格）、identity-verify、Synomos `passport_lookup` | 无显式失败态（lookup 返回 `found:false`） | 是（JSON） | 是 | **否** | **P** | 规格与实现是两套：spec 无 conformance，lookup 是 3 条硬编码 |
| 2 | Registration 登记 | uibc-core `registry/`（状态机）、`skill-registry` 仓 | uibc-core 有包级状态校验；registry 仓无 | 是 | 是 | 否 | **P** | 无真实登记记录、无写入 API、无撤销入口 |
| 3 | Evidence 证据 | uibc-core 证据包（manifest + 证据根 + 锚定） | 有（exit 0/1/2） | 是 | 是（除签名需可选依赖） | **P**（ASQAV 形状；Rekor receipt） | **V** | 证据"完整性"可验，"真实性"不可验（已明示） |
| 4 | Validation 校验 | `uibc-iverify` / `cross_check.py`（70/0）、`lgd-xverify`、Rekor 三段 | 有（0/1/2） | 是 | 是 | P | **V**（uibc 线） | 三个校验器三套语义，未统一 CLI |
| 5 | Risk Assessment 风险评估 | LGD-Eval（五维/三律）、`skillgate` | **无三值态**；空对象 fail-open | 是（JSON/SARIF） | 是 | 否 | **P** | 会放行真实恶意样本（P0-1/P0-2） |
| 6 | Governance 治理 | Synomos MCP 6 工具、`xcgs-governance` | 工具层有 `ok:false`，治理层无 | 是 | 是 | P | **P** | 只有"模板/自评"，没有裁决与留痕防篡改 |
| 7 | Authorization 授权 | `d4-evidence-authorization`（草稿）、uibc-core policy/gate、LGD-Eval L0–L5（仅文案） | d4 无实现；LGD-Eval 无强制 | 否 | 否 | 否 | **N** | **授权层没有可执行实现**，只有文档 |
| 8 | Monitoring 监控 | **无仓库**（关键词 `monitor` 命中 0） | — | — | — | — | **N** | 完全没有 |
| 9 | Re-evaluation 复评 | LGD-Eval 可重跑；uibc-core 可按版本重算 | 无"过期/版本变更自动触发" | 是 | 是 | 否 | **N** | 没有"PASS 不继承"的强制规则 |
| 10 | Revocation 撤销 | 仅 `fg-tida-r04-contrib` 文档提到 revocation | 无 | 否 | 否 | 否 | **N** | 没有撤销对象、没有撤销记录 |

**闭环结论（V）**：1→5 段有可执行资产且能出机器可读结果；**6→10 五段没有可执行的裁决/时序机制**。所以现在不是"闭环"，是"前半段有工具、后半段有文档"。

## 二、逐阶段的关键判断

### 1 Identity
- `ai-passport-spec`（Medxpert-org，NOASSERTION，2026-11-18）是规格；`identity-verify`（MIT）是脚本级；Synomos `passport_lookup` 的台账只有 3 条。
- **不允许"身份验证替代安全验证"这条规则，代码层目前天然成立**（身份查询不产出任何 PASS），但也没有任何地方阻止调用方把它当 PASS 用——这需要在 Passport 的数据结构里用字段名强制区分（见 `INDEPENDENT_VERIFICATION_SPEC.md` §4）。

### 2 Registration
- uibc-core 的 `registry/` 有状态机与校验；`skill-registry` 仓只有索引骨架（1 star，16 KB），无写入端点。
- **缺**：登记时的"谁授权登记""登记即冻结版本"两条规则没有实现。

### 3 Evidence
- uibc-core 证据包是本生态唯一**同日实测通过**的链路：manifest → 证据根 → checkpoint → Rekor inclusion → 树头一致性。
- 已明示的边界：`Evidence Integrity ≠ Evidence Truth`。这句话在仓内多处出现，属真实口径（V）。

### 4 Validation
- `cross_check.py`：70 项比对 0 分歧（V）；`uibc-iverify` 是"第二实现"，但它与主实现同作者同仓，**不构成独立验证**（V/常识）。
- 缺：验证者身份、验证时间、环境记录没有进标准输出（kit 里补了模板，但工具自身不产）。

### 5 Risk Assessment
- LGD-Eval 三问：分数能不能授权（不能，但 README 教人这么用）；不确定态有没有位置（没有）；恶意样本能不能拦（5 拦 3 漏 2）。
- 这一段是"有引擎、缺可信度"。

### 6 Governance
- Synomos MCP 能出六类证据模板、合规清单、PII 扫描；但审计日志无链式哈希、写失败被吞（P2-1），"治理留痕"目前不可作为证据。

### 7 Authorization
- `d4-evidence-authorization` 只有 112 KB 文档、无许可证、无测试；uibc-core 有 policy/gate 代码但**不产出"授权令牌"**；LGD-Eval 的 L0–L5 是 print 文案。
- **这一段没有可执行实现，是整条链最硬的缺口**。

### 8 Monitoring
- 全生态 141 个自有仓里，名称/描述含 `monitor` 的为 **0**。没有运行时监控、没有"证据过期告警"、没有"分数漂移告警"。

### 9 Re-evaluation
- 可以"再跑一次"，但没有"什么时候必须再跑"的规则。指令里的"不允许上一版本 PASS 自动继承到新版本"目前**没有代码强制**——只能靠人记得重跑。
- 最小可落地：在 Passport 里加 `valid_for_versions` 与 `expires_at`，验证 CLI 对不匹配版本直接返回 `EXPIRED`。

### 10 Revocation
- 只有 ITU 贡献文档提到撤销；没有任何对象可撤、没有撤销广播、没有撤销查询。
- 最小可落地：Passport 增加 `revoked_at`/`revocation_reason`/`superseded_by`，验证 CLI 读取后返回 `REVOKED`（不删记录）。

## 三、按指令"十个要求"的逐条对照

| 要求 | 现状 | 判定 |
|---|---|---|
| 每阶段明确输入/输出/数据结构 | 1–5 段有（uibc-core 的 manifest/receipt 最完整）；6–10 段无 | P |
| 每阶段有失败状态 | 1–4 有 exit 码；5 无三值态；6–10 无 | P |
| 每阶段有机器可读结果 | 1–6 产出 JSON；7–10 无 | P |
| 支持跨工具/跨实现传递 | uibc-core 内有 interop matrix，但反向"他们验我们"全部 not tested | P |
| 支持离线验证 | uibc 线可；签名需 `cryptography`；Synomos 可 | P |
| 支持证据失效/撤销/更新 | **无** | N |
| 支持版本变化后的重新评估 | 可手动重跑，无强制 | N |
| 不允许旧 PASS 自动继承 | 无代码强制 | N |
| 不允许身份验证替代安全验证 | 代码天然成立、结构未强制 | P |
| 不允许评测 PASS 自动获得授权 | 结构上成立，但文档在教人用分数授权 | P |

## 四、最小补齐顺序（只做 3 件，先闭环再扩）

1. **授权层落地（把 7 段接上）**：定义 `authorization_record`（谁批、批了哪个 fingerprint、有效期、限制项），由 uibc-core 签发、Synomos 记录；没有它，前面 6 段全部只是"报告"。
2. **过期与撤销（把 9/10 段接上）**：Passport 增 `expires_at` / `valid_for_versions` / `revoked_at`，验证 CLI 增 `EXPIRED` / `REVOKED` 两个返回码；这一步不需要新仓，改数据结构即可。
3. **监控最小版（把 8 段接上）**：不做平台，只做一个 cron：对已登记资产的 fingerprint 变化、证据过期、分数漂移发一次告警（复用本机定时任务能力），产出机器可读 `monitor_event.json`。

> 这三件都不新建仓；全部改动涉及代码，需 Steven 单独批准（本文件只做只读审计与设计）。
