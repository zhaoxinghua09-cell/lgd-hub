# XLGD Agent Accountability & Resilience —— 资产映射、审计与研究设计

**日期**：2026-11-19
**阶段**：第一阶段 —— 现有资产映射 + 只读审计 + 设计研究
**未做**：未新建仓库、未改代码、未对外发布、未联系客户、未报价、未作合作承诺
**标注**：FACT / INFERENCE / NOT VERIFIED / BLOCKED

---

## 0. 三条硬事实（先看这个，其余都是推论）

### 事实一：责任链是断的 —— 有"谁"，没有"谁批的"和"替谁做"

`uibc-core/uibc_core/aee.py`（63 KB，事件证据模型）字段实测：

| 关键词 | 命中 |
|---|---|
| `subject` | **18** |
| `agent_id` | **0** |
| `human` | **0** |
| `approver` | **0** |
| `on_behalf` | **0** |

它能绑定"发生了什么事"（`subject` 摘要 + corpus/catchPolicy/networkPosture 等环境摘要），但**没有人类批准者字段，也没有"以谁的名义执行"字段**。

**后果**：出了事故，你能证明"这个 subject 做了这个动作"，但**证明不了是谁授权的、谁应当负责**。任务书 WP1 要的四角色（身份/运营者/授权者/执行者）里，只落了 1 个。

### 事实二：召回（Recall）在现有数据上结构性不可答

| 指标 | 实测 |
|---|---|
| `agent-skills` 中 SKILL.md 总数 | **119** |
| 含 `dependencies` 声明 | **109**（全部写作 `dependencies: "none"`） |
| 真实依赖边 | **0** |
| Agent 注册表（记录"谁在用这个 Skill"） | **不存在**（扫描只命中测试夹具） |

**后果**：验证场景 1"高风险 Skill 被撤销后，能否定位依赖它的全部 Agent"——今天**没法答**。不是工具不行，是**数据不存在**：没有任何一条依赖声明，也没有任何 Agent 登记。

### 事实三：事故台账有，但只到"记一笔"

`agent-skills/skills/ai-incident-log` 是真实可执行件（`ai_incident_log.py` 5.6 KB，JSONL 台账），字段：**时间 / 严重度 / 模型 / 动作 / 复盘**。

缺：受影响实体与版本、处置记录、修复记录、复核记录、状态机、公开披露策略、与授权链的关联。任务书 WP2 要六项，它覆盖约两项半。

---

## 1. 资产映射（六个 WP × 现状 × 覆盖度）

| WP | 现有资产（FACT） | 覆盖 | 关键缺口 |
|---|---|---|---|
| **WP1 Accountability Ledger** | `aee.py`（subject 18 处，环境摘要齐全）；`langchain_callback`（工具调用记录） | **1/5 角色** | 授权者、运营者、批准记录、on-behalf 链、保留期限 |
| **WP2 Incident Registry** | `ai-incident-log`（JSONL：时间/严重度/模型/动作/复盘） | **2.5/6** | 受影响实体+版本、处置/修复/复核、状态机、披露策略 |
| **WP3 Recall & Containment** | `p21` 供应链原型（依赖图 + invalidate + dependents，仅原型） | **原型级** | 生产依赖数据（当前 0 边）、撤销通知通道、恢复后复评 |
| **WP4 Observability** | 无。散见"审计"记录，无运行时策略执行指标 | **0** | 策略执行率、异常权限调用、委托链异常、证据过期、控制失败 |
| **WP5 Benchmark** | `failure_corpus` F-001…F-009；`redteam_robustness.py`；`prompt-injection-drill` | **部分** | 跨引擎一致性、故障注入、公开方法、独立复现 |
| **WP6 Economics** | 无 | **0** | 成本基线、审批周期、复核工时、付费意愿 |

**一句话**：六个 WP 里，**两个有真实基础但残（WP1/WP2），一个只有原型（WP3），三个基本为空（WP4/WP5-部分/WP6）**。

---

## 2. 五个优先验证场景：当前可答性

| # | 场景 | 今天 | 卡点 |
|---|---|---|---|
| 1 | 高风险 Skill 撤销 → 定位全部依赖 Agent | ❌ **不可答** | 0 条依赖边、无 Agent 注册 |
| 2 | 权限撤销 → 阻断后续受控调用 | ❌ **不能** | 无执行点（见上一轮控制面审计：PEP 不存在） |
| 3 | 事故后重建身份/版本/证据/授权链 | ⚠️ **半可** | 身份+版本+证据可重建；**授权链断**（无授权者字段） |
| 4 | 不同引擎对同一语料得到可解释结果 | ❌ **不能** | 只有一套引擎；无跨引擎对照语料 |
| 5 | 客户是否愿付费、购买理由 | ❌ **BLOCKED** | 无客户、无报价授权（本阶段禁止联系客户） |

**净结果：0 项完全可答，1 项半可，4 项不可。**

---

## 3. 交付物一：Accountability Data Model

### 3.1 五角色（任务书四角色 + 缺失的"批准者"）

```json
{
  "task_id": "task-2026-11-19-0042",
  "identity":    {"agent_id": "agent-A", "version": "1.1.0", "key_fp": "fp-A"},
  "operator":    {"org": "op-X", "contact": "ops@x.example", "on_call": true},
  "authorizer":  {"human": "alice@x.example", "role": "approver",
                  "authorization_id": "auth-8842", "scope": ["read","write"],
                  "expires_at": "2026-12-19T00:00:00Z"},
  "executor":    {"agent_id": "agent-A", "instance": "run-7741",
                  "on_behalf_of": "alice@x.example", "on_behalf_chain": ["org:op-X", "human:alice@x.example"]},
  "evidence":    {"events_digest": "sha256:...", "tool_calls": 37,
                  "policy_decisions": 37, "policy_version": "2026.11"},
  "retention":   {"class": "P1", "keep_days": 365, "pii": "redacted"}
}
```

**三个必须存在的字段（当前全部缺失）**：
1. `authorizer.human` —— 谁批的（不是"哪个组织批的"）
2. `executor.on_behalf_chain` —— 替谁做（多跳可追）
3. `policy_decisions` 计数 —— 决策是否真的发生过（**没有决策计数，就无法证明控制面在工作**）

### 3.2 保留期限分级

| 级别 | 对象 | 期限 | 依据 |
|---|---|---|---|
| P0 | 高风险操作（支付/删除/外发） | 3 年 | 诉讼时效常见上限 |
| P1 | 一般受控操作 | 1 年 | 审计常态 |
| P2 | 只读操作 | 90 天 | 隐私最小化 |
| 事件 | 事故记录 | **永久**（不可删） | 追责与复现需要 |

**隐私**：默认 `redacted` 存摘要；原文留在受控侧；导出时提供脱敏视图。

---

## 4. 交付物二：Agent Incident Schema

```json
{
  "incident_id": "INC-2026-0007",
  "class": "policy_bypass | data_leak | unsafe_action | supply_chain | identity_abuse | availability",
  "severity": "S1 | S2 | S3 | S4",
  "detected_at": "2026-11-19T10:12:00Z",
  "detected_by": "monitor | human | external_report",
  "affected": {
    "agents": [{"agent_id": "agent-A", "version": "1.1.0"}],
    "skills": [{"name": "skill-pack-7", "version": "2.3.1"}],
    "subjects": ["tenant:acme"],
    "blast_radius": "3 agents / 1 skill / 1 tenant"
  },
  "timeline": [
    {"at": "...", "action": "contained", "by": "ops-oncall"},
    {"at": "...", "action": "authorization_suspended", "scope": ["write"]}
  ],
  "containment": {"recall_ref": "RC-2026-0003", "scope": "all_dependents"},
  "fix": {"status": "fixed | mitigated | open", "verified_by": "re-evaluation|human"},
  "review": {"reviewer": "alice", "at": "...", "conclusion": "closed"},
  "state": "OPEN → CONTAINED → FIXED → REVIEWED → CLOSED",
  "disclosure": {"policy": "private|tenant_notified|public", "decided_by": "alice", "at": "..."}
}
```

**与现有 `ai-incident-log` 的差距**：缺 `affected`、`containment`、`fix`、`review`、`state`、`disclosure` 六组字段。建议**扩展而非另起**——但那是改产品，需批准。

**状态机硬约束**：
- `OPEN → CLOSED` 必须经 `CONTAINED` 与 `REVIEWED`
- `CLOSED → OPEN` 只允许"新证据"触发（复发）
- 事件记录**不可删除**，只可追加更正条目

---

## 5. 交付物三：Recall & Containment Specification

### 5.1 生效前提（今天全不满足）

召回要求三张数据表同时存在：

| 表 | 内容 | 现状 |
|---|---|---|
| **使用关系表** | agent → skill/mcp/model 版本 | **不存在**（0 依赖边） |
| **授权表** | agent → 授权 scope/期限 | **不存在**（除原型） |
| **部署表** | agent → 环境/租户/实例 | **不存在** |

**结论**：召回规范可以先写，但**没有这三张表，规范无法执行**。这是本任务书里最需要向上管理的一句实话。

### 5.2 召回流程（六步，每步有失败行为）

| 步 | 动作 | 失败时 |
|---|---|---|
| 1 | 确定被撤销对象（skill@version / mcp@version / model@version） | 版本不明 → 按"全部版本"处理（从严） |
| 2 | 反查依赖图，取传递闭包 | 图不全 → **标记 UNKNOWN 集合**，不得当作"无影响" |
| 3 | 对受影响 agent 暂停授权（写/删/外发/支付立即停；只读可留） | 暂停失败 → 立即 incident，severity S1 |
| 4 | 通知运营者（结构化：对象/原因/需做什么/截止） | 通知失败 → 记录，转入人工外呼 |
| 5 | 修复后重新评测（新版本 + 新证据） | 无复评不得恢复 |
| 6 | 恢复授权并留痕（谁批、何时、依据哪份复评） | 无审批不得恢复 |

### 5.3 传播范围判定（fail-closed）

```
affected = closure(dependents(revoked))
if graph_coverage < 100%:  affected = closure ∪ UNKNOWN_SET   # 从严
```

**明确禁止**：把"图里没查到"当成"不受影响"。这是召回最常见的失败模式。

---

## 6. 交付物四：Governance Observability Model

### 6.1 五个必须测的量（现在全部无数据）

| 指标 | 定义 | 数据源 | 现状 |
|---|---|---|---|
| 策略执行率 | 有决策记录的调用数 / 总调用数 | PEP 日志 | **无 PEP** |
| 异常权限调用 | 请求 scope ⊄ 授权的次数 | 决策日志 | 0（无数据） |
| 委托链异常 | 断链/超深/超范围的次数 | 委托台账 | 0 |
| 证据过期占比 | 过期证据支撑的调用 / 总调用 | 证据台账 | 0 |
| **控制失败率** | 应当拒绝但实际放行的次数 | 对抗测试 + 线上抽样 | **未测** |

**最后一项是关键**：没有"控制失败率"，可观测性就只是"看起来有日志"。

### 6.2 三条观测纪律

1. **日志≠真实性证明**（任务书原则）：日志能证明"系统记录了什么"，不能证明"Agent 实际做了什么"。要有独立旁路（网络/系统调用层）抽样对账。
2. **抽样必须报偏差**：抽样率、覆盖时段、未覆盖场景，一并写进报告。
3. **指标为 0 时写 0**，不写"持续监控中"。

---

## 7. 交付物五：Agent Governance Benchmark

### 7.1 现有语料盘点（FACT）

| 语料 | 数量 | 是否永久回归 |
|---|---|---|
| `failure_corpus` F-001…F-009 | 9 | 是（CI 跑 redteam_robustness） |
| 变异组合（CI 内） | 14 变异 × 对 × 三元组 | 是 |
| `prompt-injection-drill` | 演练脚本 | 否（手动） |
| 跨引擎对照语料 | **0** | — |

### 7.2 扩展设计

| 类别 | 建议条目 | 判定 |
|---|---|---|
| 攻击语料 | 注入、越权、供应链投毒、证据伪造 | 已有部分 |
| 负向测试 | 应拒绝必须拒绝（含 UNKNOWN/INCOMPLETE） | 有（p20/p21 原型） |
| **故障注入** | PDP 宕机、审计不可写、撤销状态不可查、时钟回拨 | **零** |
| **跨引擎一致性** | 同一语料两引擎跑，差异逐条列 | **零**（只有一套引擎） |

### 7.3 跨引擎一致性怎么测（方法，未执行）

1. 语料带 `expected_verdict` + `rule_version`
2. 引擎 A、B 各自跑，输出 `verdict + codes + 解释`
3. 差异分三类：**判定不同**（严重）、**判定同但解释不同**（中等）、**都通过**（OK）
4. 公开方法 + 公开差异表（这是"可解释"的实证形态）

**当前**：只有一套引擎（LGD-Eval），所以场景 4 无法测——**不是没方法，是没第二个引擎**。

---

## 8. 交付物六：Enterprise ROI Validation Report

### 8.1 诚实的前置声明

**本轮不能产出"客户付费意愿"的验证结论**：无客户、且本阶段明确禁止联系客户。所以这份报告是**测量框架 + 待填基线**，不是结论。

### 8.2 四项成本的测量口径

| 成本项 | 口径 | 采集方法 | 当前值 |
|---|---|---|---|
| 企业审计成本 | 每次审计的人工工时 × 时薪 + 工具费 | 客户访谈 + 工时表 | **未采集** |
| Agent 上线审批周期 | 从提交到批准的自然日 | 流程日志 | **未采集** |
| 人工复核工作量 | 每千次调用的复核次数 | 复核台账 | **未采集** |
| 风险事件处置成本 | 单次事件的工时 + 停机损失 | 事件记录 | **未采集** |

### 8.3 ROI 论证结构（供后续填数）

```
节省 = (审计工时↓ + 审批周期↓ + 复核工时↓ + 事件处置↓) × 频次
成本 = 订阅费 + 接入工时 + 误报处理工时
ROI  = 节省 / 成本
```

**关键变量是"误报处理工时"**：治理工具误报高，客户的实际成本会反而上升。这一项必须实测，不能假设。

### 8.4 付费理由假设（待验证，非结论）

| 假设 | 若成立，客户会买 | 验证方式 |
|---|---|---|
| H1 合规驱动 | 有外部审计要求的行业（医疗/金融） | 访谈 + 采购流程观察 |
| H2 事故成本驱动 | 出过一次事故的企业 | 事件成本对比 |
| H3 交付效率驱动 | 想让 Agent 更快上线 | 审批周期对比 |

**三条都标 NOT VERIFIED**。任何"客户愿意付费"的表述在拿到证据前都不得写入对外材料。

---

## 9. 建议的执行顺序（受边界约束）

| 顺序 | 动作 | 需批准 | 理由 |
|---|---|---|---|
| 1 | 补 `authorizer` / `on_behalf_chain` 字段设计（文档） | 否 | 责任链是其他一切的前提 |
| 2 | 建立使用关系表的最小采集格式（文档） | 否 | 无此表，召回永远是空谈 |
| 3 | 扩展 `ai-incident-log` 到六组字段（设计稿） | 是（改产品） | 影响现有技能 |
| 4 | 写 12 条故障注入用例（设计） | 否 | 补 WP5 最大空洞 |
| 5 | 找第二个评测引擎做一致性对照 | **是**（对外） | 场景 4 唯一解 |
| 6 | 客户访谈与报价 | **是** | 本阶段明确禁止 |

---

## 10. 产物清单

| 文件 | 说明 |
|---|---|
| 本报告 | 六项交付 + 资产映射 + 场景可答性 |
| `责任与召回可行性_20261119.html` | 资产映射矩阵与场景判定看板 |
