# ECOSYSTEM_INTEROPERABILITY_MATRIX（跨平台互操作矩阵 · 2026-11-21）

> 结论先行：**只有 MCP 与 GitHub Actions 两条是真实可跑；LangChain / AutoGen / CrewAI / OpenAI-compatible 生态为 0 行代码**（实查：四个本地克隆中该四个关键词命中 0 个文件）。
> 因此策略不是"写 11 个适配器"，而是**先站稳 MCP（已有）+ GitHub Actions（已有）两个入口**。

## 一、矩阵（V=已跑通实查；P=原型；PL=计划；N=未测/无代码）

| 目标入口 | UIBC-Core | LGD-Eval | SynomosAI | 备注（实查依据） |
|---|---|---|---|---|
| **MCP（stdio）** | **V** | P | **V** | Synomos：`initialize` 握手 → `protocolVersion 2025-03-26`、6 个工具、未知工具返 `-32602`；LGD-Eval `lgd_mcp_server.py` 存在但包装入口解包必崩（P1-1） |
| **Agent Skills（SKILL.md）** | V（规范） | **V**（本生态自身即 skill） | V（skill 形态） | LGD-Eval 以 skill 形式分发；`skills/lgd-eval/` 可被读 |
| **openai-compatible（function calling）** | N | N | N | 无 function schema 导出 |
| **LangChain** | **N** | **N** | **N** | 关键词 0 命中（Grep 实查） |
| **AutoGen** | **N** | **N** | **N** | 同上 |
| **CrewAI** | **N** | **N** | **N** | 同上 |
| **CI/CD（通用）** | V | P | N | uibc 测试套 1015 例可在 CI 跑；LGD-Eval `--fail-under` 可用但 exit 语义弱 |
| **GitHub Actions** | V | P | N | `lgd-gate`（action）存在；uibc 有 workflows |
| **企业内部 Agent 平台** | N | N | N | 无 Helm/离线包/SLA，见企业阻力审计 |
| **Local Agent（本机）** | V | V | V | 三者在 Windows 本机均已跑过 |
| **Cloud Agent** | N | N | N | 无托管形态，只有 PyPI 包 |

## 二、四个问题（按指令逐条回答）

**1. 用户量最大的目标入口？**
现实答案：**MCP**。理由（V）：Synomos 已是标准 MCP 服务器，6 工具可被任何 MCP 客户端即插即用，且本生态有真实 MCP 握手记录；对比 LangChain/AutoGen/CrewAI 为 0 代码。**不要凭"框架热度"判断，要看已有可跑代码在哪。**（I，基于现状而非市场调研）

**2. 最低开发成本的接入？**
**GitHub Actions**：现成 `lgd-gate` + `evaluate.py --fail-under`，改一行 YAML 即可在 PR 上跑；成本最低、可验证性最强（能直接在 PR 里看到红绿）。

**3. 最容易产生实际使用的接口？**
**Agent Skills 形态 + MCP 工具**：因为二者"装上即可用"，不需要用户写代码；Skill 形态还能被 AI 直接读（与 §23 可发现性直接联动）。

**4. 最具战略价值的协议边界？**
**"证据包 + 结论签名"这一层**（不是平台 SDK）。谁定义"可携带、可验证、会过期"的证据格式，谁就占据边界；适配器再多也只是消费方。

## 三、执行取舍（明确不做）

- **不写** LangChain / AutoGen / CrewAI 适配器（0 用户证据、维护成本高、易被上游 breaking change 拖死）。
- **不为每个平台做 SDK**；只提供一个**薄 CLI + 一个 JSON 结果格式**，任何平台都能 shell 调用。
- **不做** 企业平台专用集成，直到出现第一个付费客户并指明平台。

## 四、三件该做的事（成本从低到高）

| 动作 | 成本 | 判据 |
|---|---|---|
| 把 `lgd-gate` 的 Action 用法写成 10 行 YAML 示例，并在 uibc-core 自身 PR 上跑一次 | 0.5 天 | PR 里出现红/绿 |
| 修 `lgd_mcp_server.py` 入口崩溃，让 LGD-Eval 成为真正的 MCP 工具（P→V） | 0.5 天 | MCP `tools/list` 出现评测工具 |
| 发布统一结果 JSON schema（`lgd-verification-result/0.1`），任何平台只消费它 | 1 天 | 两个不同调用方产出同构结果 |

## 五、诚实标注规则

- 矩阵中任何一格若未在**本机实际跑过**，不得标 V；原型必须有代码路径；计划必须写"何时做"。
- 对外描述建议：`MCP-native (verified) · GitHub Actions (prototype) · 其他生态未测试`，**不要写"支持主流 Agent 框架"**。
