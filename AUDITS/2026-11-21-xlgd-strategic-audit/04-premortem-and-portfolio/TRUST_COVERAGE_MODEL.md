# TRUST_COVERAGE_MODEL（风险覆盖与盲区可视化 · 2026-11-21）

> 目的：**不只报告"检测到什么"，还要报告"没检测什么"。** 漂亮的分数最容易造成"错误信心"，覆盖矩阵就是解药。
> 下面每一格都基于本三轮实测（V）或代码实查（P），不做乐观填充。

## 一、覆盖矩阵（八类风险 × 三套工具）

状态取值：`TESTED`（有样本且实测）/ `PARTIALLY` / `NOT_TESTED` / `FAILED`（测了但结论错）/ `INCONCLUSIVE`

| 风险类别 | UIBC 证据链 | LGD-Eval | SynomosAI | 证据 | 置信度 | 局限 |
|---|---|---|---|---|---|---|
| **Identity** | `PARTIALLY` | `NOT_TESTED` | `PARTIALLY` | uibc 有 logID/origin 但零宽字符不拒（S10）；synomos 护照 3 条硬编码 | 低 | 无主体身份绑定（谁在调用） |
| **Permission** | `NOT_TESTED` | `NOT_TESTED` | `PARTIALLY` | `gov_scan` 扫敏感路径/密钥**存在**，但不判权限越界 | 低 | 无 OAuth scope 检查 |
| **Tool Execution** | `NOT_TESTED` | `PARTIALLY` | `NOT_TESTED` | 有 `--sandbox`（需 docker/Linux），本机未跑通（N） | 极低 | 无运行时 trace |
| **Data Leakage** | `NOT_TESTED` | **`FAILED`** | `PARTIALLY` | **凭证外发样本 100/A+（G2）**；`~/.ssh` 写入漏报 | 已验证"会漏" | 规则为形态匹配，可绕过 |
| **Prompt Injection** | `NOT_TESTED` | `PARTIALLY` | `NOT_TESTED` | 有 R-SEC-11/12/13 文本规则，但用 `# skillgate: ignore` 可关（G4） | 低 | 无对抗样本回归 |
| **Governance** | `NOT_TESTED` | `NOT_TESTED` | `PARTIALLY` | synomos 有 a3 评分（1,1,1,1=4 拒绝），但无决策层 | 低 | 无授权层实现 |
| **Provenance** | **`TESTED`** | `PARTIALLY` | `PARTIALLY` | Rekor 三段实测通过 + kit 6/6 | **高** | 只覆盖构建/收据来源 |
| **Version Integrity** | `INCONCLUSIVE` | `NOT_TESTED` | `NOT_TESTED` | 收据无 version；评测 JSON 无 version（V） | — | 无法判断"这是哪个版本" |

**一眼可见的结论**：
- 唯一 `TESTED` 且高置信的是 **Provenance**；
- 唯一 `FAILED` 的是 **Data Leakage**（不是未测，是测了但结论错——这比未测更危险）；
- 八类里有 **4 类完全未测**。

## 二、"未测"必须显式出现在输出里

三种呈现方式（任选一种，但必须有）：

1. **CLI 末尾固定打印**：`Coverage: 1/8 verified, 1 failed, 2 partial, 4 not tested.`
2. **JSON 的 `evidence.coverage`**（见 `TRUST_DECISION_OUTPUT_SPEC.md`）；
3. **报告首页的灰条**：未测类别用灰色块，与绿色"通过"块视觉区分开。

禁止：只显示"检测到 N 项"，不显示"未检测 M 类"。

## 三、置信度定义（防止自评高估）

| 置信 | 条件 |
|---|---|
| HIGH | 有固定向量 + 负向控制 + 跨环境复现（≥2 台机器/≥2 个运行时） |
| MEDIUM | 有固定向量 + 负向控制，单环境 |
| LOW | 只有规则文本，无样本 |
| NONE | 无任何实现 |

按此标准：Provenance=MEDIUM（单机实测，虽有 kit 但外部未跑）、Data Leakage=已证 FAILED、其余 LOW/NONE。

## 四、缺口补齐顺序（成本 × 风险）

| 顺序 | 补什么 | 成本 | 为什么优先 |
|---|---|---|---|
| 1 | Data Leakage 从 FAILED 修到 TESTED | 低（加数据流规则 + 回归样本） | 已证会漏，且最容易对外被复现 |
| 2 | Version Integrity | 低（加 version 字段） | 一行字段解决"旧证据用于新版本" |
| 3 | Permission | 中（需 OAuth scope 解析） | 企业采购必问 |
| 4 | Prompt Injection | 中（需对抗样本集） | 规则已有但可关 |
| 5 | Identity | 中（需主体密钥） | 与 Registry 绑定 |
| 6 | Tool Execution | 高（需沙箱跨平台） | Windows 下不可用 |
| 7 | Governance | 高（需授权层） | 最后 |

## 五、一句话对外措辞

`We verify provenance end-to-end. We detect some data-leakage patterns and are known to miss others. Permission, tool execution and runtime intent are not tested.`

> 诚实条款：本矩阵的 `FAILED` 与 `TESTED` 有实跑支撑；`PARTIALLY` 与 `NOT_TESTED` 的界线是"是否有可执行代码"，不是"是否有文档"。
