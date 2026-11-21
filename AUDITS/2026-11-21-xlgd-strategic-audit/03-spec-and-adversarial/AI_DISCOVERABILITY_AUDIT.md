# AI_DISCOVERABILITY_AUDIT（AI 可发现性审计 · 2026-11-21）

> 目标不是 SEO，而是**当 AI 被问到 Agent Trust / Evidence Verification / MCP Security / Skill Security 时，能读到准确、可引用、不夸大的公开信息**。
> 实查范围：uibc-core、lgd-engine、LGD-Eval（LGD-Eval 组织号）、silent-failure-catalog、lgd-theory、lgd-hub、synomosai-governance-mcp。

## 一、元数据矩阵（V=有，P=有但不全，N=无）

| 项 | uibc-core | lgd-engine | LGD-Eval | failure-catalog | lgd-theory | lgd-hub | synomos |
|---|---|---|---|---|---|---|---|
| README | V | V | V | V | V | V | V |
| 仓库描述 | V | V | V | V | V | V | V |
| Topics（数量） | 20 | 15 | **0**（组织号为 15） | 19 | 18 | 12 | 12 |
| Homepage | V | V | V | V | V | V | **N** |
| Releases | V（v0.4.0/0.4.1/0.5.0） | V（v0.1.1） | P | N | N | N | V（PyPI 1.2.2） |
| 可运行示例 | V（examples/） | V | P | V（examples 14） | N | N | P |
| CLI 明确 | V | V | V | V | N | N | V（MCP 工具） |
| FAQ / 排障 | **N** | **N** | **N** | P | N | N | P |
| `llms.txt` | **V** | **V** | **V** | N | N | **V** | **V** |
| `AGENTS.md` | **V** | N | **V** | N | N | **V** | **V** |
| `CITATION.cff` | **V** | **V** | **V** | N | N | **V** | N |
| 跨仓互链 | P（指向 lgd-theory） | P | P | N | N | V（导航） | N |
| 版本化规范 | V（conformance） | P（OpenAPI） | N | N | N | N | N |

## 二、十个问题 × 能否被回答（这是 AI 真正要的）

| 问题 | uibc-core | LGD-Eval | 缺口 |
|---|---|---|---|
| What is this? | ✓ | ✓ | — |
| What problem does it solve? | ✓ | ✓ | — |
| Who should use it? | P | P | 未写"不适合谁" |
| How does it work? | ✓ | P | 评测算法未公开（权重） |
| How can AI use it? | ✓（llms.txt/AGENTS.md） | P | 无 function schema |
| How can developers integrate? | P | N | 缺 10 行接入示例 |
| What can it verify? | ✓ | P | 未列出规则清单 |
| **What can it NOT verify?** | P | **N** | 这是最该写却没写的 |
| What is the evidence? | ✓ | P | 证据 JSON 不可自助解读 |
| **How can an independent person reproduce it?** | ✓（kit） | **N** | 无第三方复现路径 |

## 三、三个最影响 AI 引用的问题

1. **LGD-Eval 的 Topics = 0**（zhaoxinghua09-cell 名下）：AI 检索时几乎不会命中；应补齐 `agent-security`、`skill-security`、`code-review` 等 8–12 个。
2. **"不能验证什么"缺失**：AI 引用时最容易把"能验完整性"写成"能验安全"；必须每仓写明 `not-verify: truthfulness, intent, runtime behavior`。
3. **两个仓无 homepage**（skillgate、synomos）：缺少 canonical URL，AI 引用时只能引 GitHub 页，且无法指向规范页。

## 四、必须避免的三种"假曝光"

- 堆砌关键词（topics 里塞 `ai`、`trust`、`blockchain` 等无关词）→ 会降低可信度；
- 自述"业界首个/唯一"（无第三方证据）；
- 把 ITU/W3C/IETF 的**参与**写成**采纳**（实查：仅 1 帖 + 1 回复 + 1 份本地 TD，无提交/采纳记录，V）。

## 五、七个“一分钟可做”的改动（不改代码）

1. LGD-Eval 补 topics（0 → 10）；
2. skillgate、synomos 补 homepage（指向各自 README 的 GitHub Pages 或规范）；
3. 每个 README 顶部加三行：`能验 / 不能验 / 15 分钟复现路径`；
4. 给 LGD-Eval 补 `llms.txt`（已有 CITATION/AGENTS，缺 llms.txt）；
5. failure-catalog 补 `llms.txt` + `CITATION.cff`；
6. lgd-theory 补 `AGENTS.md`（写明"理论可被引用，解释权不排他"）；
7. 所有仓在 README 末尾加 6 条交叉链接（theory ↔ core ↔ eval ↔ failures ↔ kit ↔ registry）。

## 六、验收判据

- 任选一个 AI 检索场景（"how to verify an agent evidence bundle"），能命中 uibc-core 或 kit 页，且页面 30 秒内回答"能验什么/不能验什么/怎么复现"；
- LGD-Eval 的 topics ≥10；
- 无任何"首个/唯一/标准采纳"的自述。
