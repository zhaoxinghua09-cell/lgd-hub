# XLGD_AI_NATIVE_INTEGRATION_PLAN（AI 原生集成方案 · 2026-11-21）

> 目标：让 Agent **能调用**而不是"能读文档"。
> 现状（V）：Synomos 已是真 MCP 服务器（6 工具、stdio 握手 `protocolVersion 2025-03-26`）；LGD-Eval 有 MCP 入口但会崩（P1-1）；uibc 无 MCP，只有 CLI。

## 一、八个接口 × 现状

| 接口 | 现状 | 判定 |
|---|---|---|
| MCP Tools | Synomos 6 个可调（V）；LGD-Eval 入口崩（P） | ⚠️ |
| Machine-readable Specs | 有文档 + 部分 JSON；**无 JSON Schema** | ❌ |
| CLI | 有（uibc tools / lgd-eval） | ✅ |
| JSON Schema | **无**（结果结构靠文档描述） | ❌ |
| API（HTTP） | 无 | ❌ |
| Agent Skills | 有 `skills/lgd-eval` 形态 | ✅ |
| Evaluation Workflow | 有 CLI 流程 | ⚠️（无决策层） |
| Evidence Retrieval | 无"按对象取证据"的接口 | ❌ |
| Verification Workflow | CLI + kit（离线） | ✅ |
| Governance Actions | 无（`a3` 只是评分） | ❌ |

## 二、九步 Agent 流程（含人工审批边界）

```
1 Discover Protocol     ← llms.txt / AGENTS.md（已有）
2 Identify Subject      ← subject id + version + fingerprint（需补 version）
3 Collect Evidence      ← 收据 / manifest / SHA（已有）
4 Evaluate              ← 规则评测（已有，但结论不可信 → 必须标 EXPERIMENTAL）
5 Verify                ← 离线 kit（已有）
6 Check Governance      ← 无实现 → 返回 INSUFFICIENT_EVIDENCE
7 Request Human Approval← 【人工边界】必须由人确认
8 Record Result         ← 签名 + 锚定（待建）
9 Report                ← 三层 JSON（待建）
```

**人工审批边界（硬性）**：步骤 7 之前，Agent 只能"取数与计算"，**不得**：发布、撤销、联系第三方、改权限、签"通过"。

## 三、要让 AI 真正能用，缺的四件

| # | 缺件 | 成本 | 判据 |
|---|---|---|---|
| 1 | `lgd-trust-decision/0.2` 的 **JSON Schema** | 0.5 天 | Agent 可校验输出 |
| 2 | 一个 MCP 工具 `verify_bundle`（输入 bundle，返回 verdict） | 1 天 | MCP `tools/list` 出现 |
| 3 | `evidence get <subject>` 检索接口（本地文件即可） | 0.5 天 | 可按键取证据 |
| 4 | `governance check` 返回 `INSUFFICIENT_EVIDENCE`（而不是假装有结论） | 0.5 天 | 无授权层时诚实返回 |

## 四、反模式（必须避免）

- ❌ 让 Agent 直接"签字通过"（人必须介入）；
- ❌ 让 Agent 自动发 PR/评论/邮件；
- ❌ 把"分数"当工具返回值给 Agent 决策（分数 EXPERIMENTAL）；
- ❌ 提供"一键认证"这类工具——法律与信誉双重风险。

## 五、最小可用形态（30 天内）

```
$ mcp-audit https://server/mcp     → 权限与敏感面清单（JSON）
$ uibc verify receipt.json         → verdict + 覆盖缺口
$ lgd-decision bundle.json         → decision + confidence + missing
```

三者输出同一 `schema` 字段族，任何 Agent 都能串起来。

> 诚实条款：本文 8 个接口中 3 个已有、2 个部分、4 个缺；"AI 原生"目前只到"能被 AI 读到并调用一两个工具"。
