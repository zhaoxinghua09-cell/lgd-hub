# XLGD_PORTFOLIO_DECISION_MATRIX（资产组合决策矩阵 · 2026-11-21）

> 由 `gen_portfolio.py` 依据 `repos_inventory.json`（172 仓实查）生成；规则见文末。**本文件只给建议，不执行任何归档/合并/删除。**

## 一、结论分布

| 决策 | 数量 | 含义 |
|---|---|---|
| KEEP | 14 | 继续作为核心资产 |
| MONETIZE | 1 | 进入商业产品路径 |
| REPOSITION | 1 | 重新定位（入口/文档） |
| MERGE | 11 | 合并到更明确的核心项目 |
| EXPERIMENT | 112 | 保留实验性质，限时观察 |
| ARCHIVE | 2 | 保留历史，停止活跃建设 |

自有仓 141 个、fork 31 个。**建议合并 11 个、归档 2 个**——即维护面可从 141 收窄到约 128。

## 二、核心资产决策（16 项优先）

| 仓 | 决策 | 为什么 | 战略 | 独特 | 12m 价值 |
|---|---|---|---|---|---|
| `uibc-core` | **KEEP** | 协议唯一实现 + 一致性语料 | 5 | 5 | 3 |
| `lgd-engine` | **MONETIZE** | 唯一可卖给合规场景的判定器 | 4 | 4 | 3 |
| `silent-failure-catalog` | **KEEP** | 唯一负向语料库，最难复制 | 5 | 4 | 3 |
| `lgd-theory` | **KEEP** | 理论 SSOT，可被引用 | 4 | 2 | 3 |
| `LGD-Eval` | **KEEP** | 评测引擎，三条 P0 未修 | 4 | 3 | 3 |
| `synomosai-governance-mcp` | **KEEP** | 唯一真 MCP 服务器 | 4 | 3 | 3 |
| `agent-skills` | **KEEP** | 技能唯一索引 | 3 | 2 | 3 |
| `lgd-hub` | **REPOSITION** | 应做唯一入口页 | 3 | 1 | 2 |
| `skillgate` | **MERGE** | 入口应与 LGD-Eval 合并 | 3 | 2 | 2 |
| `xcgs-governance` | **MERGE** | 与 lgd-engine 治理能力重叠 | 3 | 2 | 2 |
| `uibc-iverify` | **KEEP** | 内部对拍实现（非独立） | 3 | 2 | 3 |
| `lgd-xverify` | **MERGE** | 并入统一 verify CLI | 3 | 2 | 2 |
| `ldg-gate` | **MERGE** | 入口合并 | 2 | 1 | 2 |
| `lgd-gate` | **KEEP** | CI 门禁原型，成本最低的入口 | 3 | 3 | 3 |
| `assayance` | **ARCHIVE** | 无版本、无测试、无用户 | 1 | 1 | 2 |
| `uibc-competition` | **EXPERIMENT** | 竞赛形态，无参与者 | 1 | 1 | 2 |
| `a22-trust-lifecycle` | **MERGE** | 内容应并入生命周期文档 | 2 | 1 | 2 |
| `ai-passport-spec` | **MERGE** | 护照三处实现需统一 | 3 | 2 | 2 |
| `ai-model-passport` | **MERGE** | 同上 | 2 | 1 | 2 |
| `lgd-skills` | **MERGE** | 与 agent-skills 重复 | 2 | 1 | 2 |
| `medxpert-skills` | **MERGE** | 同上 | 2 | 1 | 2 |
| `registry` | **EXPERIMENT** | 无实现 | 2 | 1 | 2 |
| `lgd-skill-review` | **MERGE** | 并入 LGD-Eval | 2 | 1 | 2 |
| `fg-tida-r04-contrib` | **KEEP** | 国际组织贡献稿唯一载体 | 3 | 1 | 3 |

## 三、全量自有仓（141）决策表

> 列：决策 / 战略重要性 / 技术独特性 / 实际用户 / 外部贡献 / 重复程度 / 维护成本(高=4) / 商业可能 / 12 月价值（1–5，5 最好）

| owner | repo | 决策 | 战略 | 独特 | 用户 | 贡献 | 重复 | 维护 | 商业 | 12m | License | ★ | 最后推送 | 依据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zhaoxinghua09-cell | `silent-failure-catalog` | **KEEP** | 5 | 4 | 3 | 1 | 1 | 3 | 2 | 3 | NOASSERTION | 9 | 2026-11-20 | 唯一负向语料库，最难复制 |
| zhaoxinghua09-cell | `uibc-core` | **KEEP** | 5 | 5 | 3 | 1 | 1 | 2 | 2 | 3 | Apache-2.0 | 12 | 2026-11-20 | 协议唯一实现 + 一致性语料 |
| LGD-Eval | `LGD-Eval` | **KEEP** | 4 | 3 | 2 | 1 | 1 | 3 | 2 | 3 | CC-BY-4.0 | 2 | 2026-11-20 | 评测引擎，三条 P0 未修 |
| zhaoxinghua09-cell | `lgd-theory` | **KEEP** | 4 | 2 | 3 | 1 | 2 | 2 | 2 | 3 | NOASSERTION | 7 | 2026-11-20 | 理论 SSOT，可被引用 |
| Medxpert-org | `lgd-theory` | **KEEP** | 4 | 2 | 1 | 1 | 2 | 4 | 2 | 3 | NOASSERTION | 0 | 2026-10-03 | 理论 SSOT，可被引用 |
| zhaoxinghua09-cell | `synomosai-governance-mcp` | **KEEP** | 4 | 3 | 2 | 1 | 1 | 4 | 2 | 3 | MIT | 1 | 2026-11-17 | 唯一真 MCP 服务器 |
| zhaoxinghua09-cell | `agent-skills` | **KEEP** | 3 | 2 | 3 | 1 | 1 | 2 | 2 | 3 | NOASSERTION | 5 | 2026-11-19 | 技能唯一索引 |
| zhaoxinghua09-cell | `agent-trust-identity-spec` | **KEEP** | 3 | 2 | 2 | 1 | 1 | 4 | 1 | 3 | MIT | 3 | 2026-11-06 | 有外部可见度 |
| zhaoxinghua09-cell | `fg-tida-r04-contrib` | **KEEP** | 3 | 1 | 2 | 1 | 1 | 4 | 2 | 3 | CC-BY-4.0 | 1 | 2026-11-17 | 国际组织贡献稿唯一载体 |
| LGD-Eval | `lgd-gate` | **KEEP** | 3 | 3 | 2 | 1 | 1 | 4 | 2 | 3 | MIT | 1 | 2026-11-13 | CI 门禁原型，成本最低的入口 |
| zhaoxinghua09-cell | `medxpert-library-connector` | **KEEP** | 3 | 2 | 2 | 1 | 1 | 4 | 1 | 3 | NOASSERTION | 3 | 2026-11-16 | 有外部可见度 |
| zhaoxinghua09-cell | `medxpert-standards` | **KEEP** | 3 | 2 | 2 | 1 | 1 | 4 | 1 | 3 | MIT | 3 | 2026-11-16 | 有外部可见度 |
| zhaoxinghua09-cell | `uibc-iverify` | **KEEP** | 3 | 2 | 1 | 1 | 1 | 4 | 2 | 3 | Apache-2.0 | 0 | 2026-11-18 | 内部对拍实现（非独立） |
| zhaoxinghua09-cell | `xlgd` | **KEEP** | 3 | 2 | 2 | 1 | 1 | 4 | 1 | 3 | MIT | 3 | 2026-11-17 | 有外部可见度 |
| Medxpert-org | `lgd-engine` | **MONETIZE** | 4 | 4 | 1 | 1 | 1 | 3 | 4 | 3 | Apache-2.0 | 0 | 2026-11-19 | 唯一可卖给合规场景的判定器 |
| zhaoxinghua09-cell | `lgd-hub` | **REPOSITION** | 3 | 1 | 2 | 1 | 1 | 3 | 2 | 2 | NOASSERTION | 3 | 2026-11-20 | 应做唯一入口页 |
| Medxpert-org | `ai-passport-spec` | **MERGE** | 3 | 2 | 1 | 1 | 1 | 3 | 2 | 2 | NOASSERTION | 0 | 2026-11-18 | 护照三处实现需统一 |
| zhaoxinghua09-cell | `lgd-xverify` | **MERGE** | 3 | 2 | 1 | 1 | 1 | 4 | 2 | 2 | Apache-2.0 | 0 | 2026-11-18 | 并入统一 verify CLI |
| zhaoxinghua09-cell | `skillgate` | **MERGE** | 3 | 2 | 1 | 1 | 1 | 3 | 2 | 2 | MIT | 0 | 2026-11-18 | 入口应与 LGD-Eval 合并 |
| Medxpert-org | `xcgs-governance` | **MERGE** | 3 | 2 | 2 | 1 | 1 | 4 | 2 | 2 | MIT | 1 | 2026-10-28 | 与 lgd-engine 治理能力重叠 |
| zhaoxinghua09-cell | `a22-trust-lifecycle` | **MERGE** | 2 | 1 | 1 | 1 | 1 | 4 | 2 | 2 | none | 0 | 2026-11-18 | 内容应并入生命周期文档 |
| stevenzhao07 | `ai-model-passport` | **MERGE** | 2 | 1 | 1 | 1 | 1 | 4 | 2 | 2 | NOASSERTION | 0 | 2026-11-09 | 同上 |
| zhaoxinghua09-cell | `lgd-skill-review` | **MERGE** | 2 | 1 | 1 | 1 | 1 | 3 | 2 | 2 | MIT | 0 | 2026-11-20 | 并入 LGD-Eval |
| zhaoxinghua09-cell | `lgd-skills` | **MERGE** | 2 | 1 | 1 | 1 | 2 | 3 | 2 | 2 | MIT | 0 | 2026-11-18 | 与 agent-skills 重复 |
| stevenzhao07 | `lgd-skills` | **MERGE** | 2 | 1 | 1 | 1 | 2 | 3 | 2 | 2 | MIT | 0 | 2026-11-18 | 与 agent-skills 重复 |
| stevenzhao07 | `medxpert-skills` | **MERGE** | 2 | 1 | 2 | 1 | 2 | 4 | 2 | 2 | MIT | 1 | 2026-11-09 | 同上 |
| Medxpert-org | `medxpert-skills` | **MERGE** | 2 | 1 | 2 | 1 | 2 | 4 | 2 | 2 | Apache-2.0 | 1 | 2026-11-08 | 同上 |
| stevenzhao07 | `.github` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 2 | 4 | 1 | 1 | none | 0 | 2026-10-24 | 未定型，限时观察 |
| LGD-Eval | `.github` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 2 | 4 | 1 | 1 | none | 0 | 2026-10-24 | 未定型，限时观察 |
| Medxpert-org | `.github` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 2 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `LGD` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `Nomos` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `a18-skill-supply-chain` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `a28-behavioural-signals` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `a3-law-operational` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `agent-memory-service` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | AGPL-3.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| Medxpert-org | `agent-runtime-governance` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 0 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `agent-soul-os` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | Apache-2.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `ai-governance-checklist` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-13 | 未定型，限时观察 |
| zhaoxinghua09-cell | `assurability` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `authz-code-design` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `awesome-trusted-agents` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `badge-studio` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `c45-skill-metrics` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `claim-audit` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| LGD-Eval | `competitor-comparison` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-08 | 未定型，限时观察 |
| zhaoxinghua09-cell | `conformance-surface-2026-11` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | CC-BY-4.0 | 0 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `context-token-budget` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `credential-vault-design` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `culpachain` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `d4-evidence-authorization` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `debug-pro` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | MIT | 0 | 2026-11-19 | 未定型，限时观察 |
| stevenzhao07 | `delivery-guard` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `device-regulatory-map` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| stevenzhao07 | `doc-translate-keep-layout` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| LGD-Eval | `dsh-plugin-lgd-trust` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `dsh-secret-leakage-scan` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| LGD-Eval | `evaluation-evidence` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | CC-BY-4.0 | 1 | 2026-11-20 | 未定型，限时观察 |
| LGD-Eval | `evaluation-protocol` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | CC-BY-4.0 | 2 | 2026-11-20 | 未定型，限时观察 |
| LGD-Eval | `evaluation-reports` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | CC-BY-4.0 | 1 | 2026-11-20 | 未定型，限时观察 |
| zhaoxinghua09-cell | `evidence-anchor` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `evidence-gated-medical-agent-demo` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 0 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `fgtida-contribution-discovery-evidence` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `fgtida-paris-input-2026` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `fingerprint-delivery` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `identity-verify` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `iso14971-risk-file` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| Medxpert-org | `itu-fg-tida` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-10-08 | 未定型，限时观察 |
| Medxpert-org | `lcas` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | Apache-2.0 | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-demo-organization` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-glossary` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 2 | 2026-11-20 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-hit-list` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-loop-fixture` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-medai-demo` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-skeleton` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-skill-marketplace` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `lgd-skills-index` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-08 | 未定型，限时观察 |
| zhaoxinghua09-cell | `llms-generator` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `med-device-compliance-toolkit` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-16 | 未定型，限时观察 |
| stevenzhao07 | `medical-ai-toolkit` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medical-device-reg-expert` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medical-device-reg-translator` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-16 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medical-device-testing-link` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | MIT | 1 | 2026-11-16 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-ai-gov-kb` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-ai-samd-reg-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-clinical-eval-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-deficiency-reply-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-fhir` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-11-09 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-hospital-bid-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-labeling-ifu-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-llm-library` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 2 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-master-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-oem-cmo-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-ortho-mcp` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-18 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-postmarket-surveillance-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-pre-submission-check-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-reg-connector` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-18 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-reg-hub` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | MIT | 0 | 2026-11-16 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-reg-kb` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-reg-path-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-registration-ops` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | Apache-2.0 | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-risk-management-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| Medxpert-org | `medxpert-skill-index` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-08 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-standards-connector` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-16 | 未定型，限时观察 |
| stevenzhao07 | `medxpert-test-lab-selection-skill` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-10-31 | 未定型，限时观察 |
| zhaoxinghua09-cell | `medxpert-voice-kb` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `mnemoship` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `multilingual-ifu` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `nti-lgd-transition-contract` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-19 | 未定型，限时观察 |
| zhaoxinghua09-cell | `paper1-verifier-side-silent-failures` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `project-ops-protocol` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `prompt-injection-guard` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| stevenzhao07 | `regdoc-commons` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 0 | 2026-11-18 | 未定型，限时观察 |
| LGD-Eval | `robot-blackbox-replay-eval` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-10-18 | 未定型，限时观察 |
| LGD-Eval | `robot-identity-registry-eval` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-10-18 | 未定型，限时观察 |
| LGD-Eval | `robot-ota-regate-eval` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | none | 0 | 2026-10-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `runtigil` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-06 | 未定型，限时观察 |
| stevenzhao07 | `samd-ra-toolkit` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 1 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `silent-failure-scanner` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| LGD-Eval | `skill-audit` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | Apache-2.0 | 2 | 2026-11-11 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-improver` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-quality-gate` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-redteam-suite` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-registry` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-scorecard` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 1 | 2026-11-18 | 未定型，限时观察 |
| LGD-Eval | `skill-scout` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-18 | 未定型，限时观察 |
| zhaoxinghua09-cell | `skill-skeleton-generator` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | MIT | 1 | 2026-11-17 | 未定型，限时观察 |
| stevenzhao07 | `sterilization-validation` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| stevenzhao07 | `stevenzhao07` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | Apache-2.0 | 0 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `summarize-pro` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | MIT | 1 | 2026-11-19 | 未定型，限时观察 |
| zhaoxinghua09-cell | `terminance` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 2 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `theme50-contribution-matrix` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | CC-BY-4.0 | 0 | 2026-11-17 | 未定型，限时观察 |
| Medxpert-org | `ubic-governance-mcp` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-16 | 未定型，限时观察 |
| Medxpert-org | `ubic-site` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-11-09 | 未定型，限时观察 |
| stevenzhao07 | `udi-assignment` | **EXPERIMENT** | 2 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 0 | 2026-11-09 | 未定型，限时观察 |
| zhaoxinghua09-cell | `wechat-viral-topic` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | NOASSERTION | 1 | 2026-11-19 | 未定型，限时观察 |
| zhaoxinghua09-cell | `xcgs-manifesto` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | NOASSERTION | 2 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `zhaoxinghua09-cell` | **EXPERIMENT** | 2 | 1 | 2 | 1 | 1 | 4 | 1 | 1 | none | 1 | 2026-11-06 | 未定型，限时观察 |
| zhaoxinghua09-cell | `uibc-competition` | **EXPERIMENT** | 1 | 1 | 2 | 1 | 1 | 4 | 2 | 1 | NOASSERTION | 3 | 2026-11-13 | 竞赛形态，无参与者 |
| zhaoxinghua09-cell | `assayance` | **ARCHIVE** | 1 | 1 | 2 | 1 | 1 | 3 | 2 | 1 | NOASSERTION | 1 | 2026-11-06 | 无版本、无测试、无用户 |
| Medxpert-org | `traceability-audit` | **ARCHIVE** | 1 | 1 | 1 | 1 | 1 | 4 | 1 | 1 | MIT | 0 | 2026-08-29 | 已归档 |

## 四、Fork（31）统一处置

全部 fork **一律不视为实现、不视为背书、不计入生态规模**；建议在 fork 的 README/描述加 `fork: not an implementation`，或直接归档。理由（V）：31 个 fork 全属作者本人账号，外部人看到会误认为「有 31 个派生实现」。

## 五、规则（可复算）

1. `archived=true` → ARCHIVE；
2. 命中 16 项核心清单 → 按人工给定决策；
3. `stars≥3` → KEEP（有外部可见度）；
4. 最后推送早于 2026-10 且 `stars==0` → ARCHIVE；
5. 其余 → EXPERIMENT（限时观察，不新增功能）。

## 六、执行约束

- 任何 ARCHIVE/MERGE 动作都需单独批准，且**保留历史、不删仓库**（GitHub Archive 是只读，不是删除）。
- 合并顺序建议：先 `skillgate`/`lgd-xverify`/`lgd-skill-review` → `LGD-Eval`；再 `ai-passport-spec`/`ai-model-passport` → 统一 `verification-result`；最后 `lgd-hub` 升格为唯一入口。
