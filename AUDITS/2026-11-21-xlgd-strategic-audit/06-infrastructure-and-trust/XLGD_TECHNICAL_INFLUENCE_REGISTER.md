# XLGD_TECHNICAL_INFLUENCE_REGISTER（技术影响力与引用登记 · 2026-11-21）

> 铁律：**Mention ≠ Citation ≠ Integration ≠ Adoption ≠ Formal Standardization。**
> 现状（V）：Mention 1（且是分歧记录）、Citation 0、Integration 0、Adoption 0、Standardization 0。

## 一、五级定义

| 级 | 定义 | 判据 | 当前 |
|---|---|---|---|
| **M1 Mention** | 提到我们（含批评） | 有链接、有原文 | **1**（DEV.to / AER-1 作者，记录 9/9 vs 0/9 分歧） |
| **M2 Citation** | 作为引用来源出现在他人作品 | 有正式引用条目 | **0** |
| **M3 Integration** | 别人的代码/流程用了我们的工具或格式 | 有提交记录 | **0** |
| **M4 Adoption** | 他人生产使用（有使用者承认） | 有公开声明 | **0** |
| **M5 Standardization** | 进入正式标准 | 有编号/文本 | **0** |

## 二、引用基础设施现状

| 要件 | 现状 | 判定 |
|---|---|---|
| Citation Metadata（`CITATION.cff`） | **有**（uibc-core、lgd-engine、LGD-Eval、lgd-hub） | ✅ |
| 作者归属 | ORCID `0009-0001-0512-1237` 已索引作品（V） | ✅ |
| Canonical Project URLs | 多数仓有 homepage（skillgate/synomos 缺） | ⚠️ |
| Versioned Technical References | 有 release（0.4.0/0.4.1/0.5.0） | ✅ |
| Specification References | 有 `SPEC-PROPOSAL-v0.1` / `draft-…-00` | ⚠️（未成正式 RFC 编号） |
| External Usage Evidence | 只有 1 条 mention | ❌ |

## 三、现有 1 条 mention 的性质（重要）

- **它是分歧，不是背书**：AER-1 作者记录"我们跑出 9/9，他们 0/9"。
- 价值：证明"有人真的跑了"，这是最珍贵的信号（比 star 更真）。
- 风险：如果我们把这条写成"被引用"，就是撒谎，且对方会立刻反驳。

**正确表述**：`One external party ran our vectors and published a differing result; we disagree on X, and the disagreement is documented.`

## 四、如何把 mention 变成 citation（三步）

| 步 | 动作 | 成本 |
|---|---|---|
| 1 | 把技术说明做成可引用格式（有 DOI/稳定 URL/版本） | 低（Zenodo 已有偏好记录） |
| 2 | 在文档里给出"如何引用我们"的 BibTeX | 低 |
| 3 | 主动（经批准）回应分歧：把两边命令与输出并排公开 | 中 |

## 五、如何把 citation 变成 integration

- 只做一件事：**让我们的输出格式被别人的脚本消费**（`lgd-trust-decision/0.2` JSON + 一个 `pip install` 的 CLI）；
- 不追"框架适配器"（0 用户）。

## 六、对外表述模板（按级别严格对应）

| 级别 | 可以说 | 不能说 |
|---|---|---|
| M1 | "有外部研究者公开复跑并记录了分歧" | "被业界采用" |
| M2 | "被 X 篇论文引用"（需列出） | "广泛引用" |
| M3 | "被 X 项目集成"（需给出 PR/commit） | "生态已形成" |
| M4 | "被 X 用于生产"（需对方同意） | "行业标准" |
| M5 | "被 X 标准采纳（编号 Y）" | — |

## 七、验收判据

1. 每季度更新本表（当前全 0，除 M1）；
2. 任何对外材料不得越级表述；
3. 引用条目可点开、可核对作者与日期。

> 诚实条款：M1 的 1 条是我们**唯一**的外部痕迹，且性质是分歧；把这一点写清楚，比多找 10 个 star 更有价值。
