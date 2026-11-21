# XLGD Agent Governance Control Plane —— 能力审计、架构与原型计划

**日期**：2026-11-19
**阶段**：按任务书六要求执行 —— **先只读审计 → 架构与缺口报告 → 提交本地原型计划**
**未做**：未写原型代码、未改远端仓库、未合并、未发布、未部署、未对外承诺
**标注**：FACT / INFERENCE / NOT VERIFIED / BLOCKED

---

## 0. 审计结论（一句话）

**现有资产里没有任何一处真正在 tool call 路径上做阻断。**

三类资产的实际形态：

| 形态 | 代表 | 能否强制 |
|---|---|---|
| **记录器** | `uibc-core/adapters/frameworks/langchain_callback.py` | ❌ 其 docstring 自己写明 *"Nothing is wrapped, nothing is intercepted"* |
| **清单生成器** | `agent-skills/skills/agent-kill-switch/scripts/agent_kill_switch.py` | ❌ 生成"制动卡"JSON 并校验完整性，不执行任何停止动作 |
| **关键词建议器** | `agent-skills/skills/tool-call-guard/scripts/tool_guard.py` | ❌ 输出 BLOCK/ALLOW 字符串，是否采纳取决于 Agent 自己 |

三个都是好东西，但它们都是**决策建议**，不是**执行点**。控制面缺的正是 PEP。

---

## 1. 八个 WP 的现有能力实盘

| WP | 现有资产（FACT） | 形态 | 覆盖度 |
|---|---|---|---|
| **WP1 Policy Engine** | 无治理策略引擎。`skill-audit` 的规则是**静态扫描规则**，不是治理策略；无版本、无优先级、无冲突处理 | — | **0** |
| **WP2 Pre-execution Gate** | `tool_guard.py`（2.5 KB，关键词五级分级：读/写/删/外发/支付） | 建议器，需 Agent 主动调用 | **部分** |
| **WP3 Runtime Enforcement** | `langchain_callback.py`（5 KB，真 BaseCallbackHandler） | **记录器**，明确不拦截 | **0（强制）** |
| **WP4 Post-execution Audit** | `aee.py`（63 KB 事件模型）、callback 记录、`audit_log` 类记录 | 有真东西 | **部分**（有记录，缺与 authorization 绑定） |
| **WP5 Human Override** | `agent_kill_switch.py`（6 KB，生成/校验制动卡）、skills 里的审批模板 | 文档 + 清单 | **0（执行）** |
| **WP6 Fail-safe & Recovery** | 分散在 `api-resilience` 等技能文档里 | 文档 | **0** |
| **WP7 Risk-based Governance** | `tool_guard` 五级分级 + 各仓 `severity` 字段 | 分级存在 | **部分**（无风险预算、无分级控制策略） |
| **WP8 Control Effectiveness** | `prompt-injection-drill`、`prompt-injection-shield` 演练脚本 | 演练 | **部分**（无绕过率/漏报率统计） |

扫描基数（FACT）：`policy` 命中 65、`runtime enforcement` 63、`audit` 201、`human override` 56、`fail-safe` 61、`risk` 470、`bypass` 58 —— 但命中数不等于能力，逐条看下来绝大多数是**技能文档里的描述**。

---

## 2. 八个验收场景的当前判定（今天能不能过）

| # | 场景 | 当前能否通过 | 依据 |
|---|---|---|---|
| 1 | 未授权 Agent 请求高风险工具 → 阻断 | ❌ **不能** | 无授权概念；`tool_guard` 只给建议 |
| 2 | 授权过期后无法继续执行 | ❌ **不能** | 全生态无 "授权" 对象 |
| 3 | 授权服务不可用时不默认放行 | ❌ **不能** | 无 fail-closed 执行点；无服务可谈 |
| 4 | 超出任务范围被发现并控制 | ❌ **不能** | 有 scope 校验原型（p21），未接入执行 |
| 5 | 人工撤销后后续执行被阻断 | ❌ **不能** | kill switch 是卡片，不是开关 |
| 6 | 运行记录关联身份/版本/证据/授权 | ⚠️ **部分** | 记录有身份与工具调用，**无授权字段** |
| 7 | 策略升级后复测旧案例识别行为变化 | ❌ **不能** | 无策略版本、无回归语料库 |
| 8 | 故障后不静默恢复已撤销权限 | ❌ **不能** | 无状态重建机制 |

**净结果：0 / 8 强制通过，1 项部分。**

这不是坏消息——这正是本轮审计的价值：**在动手建控制面之前，先证明控制面不存在**。

---

## 3. 交付物一：Governance Control Plane Architecture

### 3.1 四类功能点（PDP / PEP / PAP / PIP）

```
                    ┌──────────── PAP（管理面）────────────┐
                    │  策略编写 · 版本 · 审批 · 回滚        │
                    └───────────────┬────────────────────┘
                                    ▼  policy bundle（已签名）
 ┌──────────┐   决策请求    ┌───────────────┐   决策    ┌──────────────┐
 │   Agent   │──────────────▶│ PDP 决策点     │─────────▶│ PEP 执行点    │──▶ 工具实际调用
 │ (subject) │               │ deny-overrides│          │ 唯一强制位置  │
 └──────────┘◀──────────────└───────────────┘◀─────────└──────────────┘
        ▲                            ▲                        │
        │  审批/撤销                  │ 证据/授权状态           │ 事件
 ┌──────┴───────┐            ┌───────┴────────┐               ▼
 │ Human Override│            │ PIP（信息点）   │        ┌──────────────┐
 │ 审批·急停·撤销 │            │ identity/evidence│       │ 审计存储      │
 └──────────────┘            │ /authorization  │        │ (append-only) │
                             └────────────────┘        └──────────────┘
```

**核心断言（必须机器保证）**：
1. **PDP 与 PEP 分离**：判断在 PDP，阻断在 PEP；PDP 挂了 PEP 必须 deny（fail-closed）
2. **PEP 是唯一强制位置**：任何绕过 PEP 的调用路径 = 控制面失效
3. **Evaluation 不产生 Authorization**：评测分数只进 PIP，不进决策的"允许"分支

### 3.2 三阶段控制

| 阶段 | 控制点 | 失败行为 |
|---|---|---|
| 执行前 | 身份、证据有效期、版本/依赖、授权范围、高风险审批 | 任一不满足 → DENY |
| 执行中 | 工具权限、行为监测、超范围阻断、异常暂停 | 越界 → 立即阻断 + 暂停会话 |
| 执行后 | 执行记录、工具证据、审批记录、责任关联、完整性验证 | 记录缺 → 任务标记 INCOMPLETE |

---

## 4. 交付物二：Policy Schema

```yaml
policy_version: "2026.11"
issuer: "governance-admin"
valid_from: "2026-11-01T00:00:00Z"
combining_algorithm: deny-overrides     # 唯一允许：deny 优先
rules:
  - id: P-001
    priority: 100
    effect: deny
    subject: {agent_trust_level: ["unverified"]}
    action: {tool_class: ["delete", "pay", "external_send"]}
    condition: "always"
    obligation: "block_and_notify_owner"
  - id: P-002
    priority: 90
    effect: permit
    subject: {agent_id: "agent-A", authorization_scope: ["read"]}
    action: {tool_class: ["read", "search"]}
    condition: "authorization.not_expired AND evidence.state == VERIFIED"
  - id: P-003
    priority: 95
    effect: deny
    subject: {any: true}
    action: {tool_class: ["pay"]}
    condition: "risk_level >= 3 AND NOT human_approved_within(24h)"
```

| 字段 | 约束 |
|---|---|
| `policy_version` | 单调递增；每个决策记录引用当时的版本 |
| `combining_algorithm` | **只允许 deny-overrides**（同时 permit 与 deny → deny） |
| `priority` | 高优先级先评；同优先级冲突 → deny |
| `obligation` | 决策附带义务（通知、双人复核、事后审计级别） |
| 回滚 | 保留全部历史版本，回滚 = 切回旧版本并记录（**不得删除新版本**） |

**策略测试**：每次变更必须跑全量回归语料（§8），行为差异逐条列出——这就是场景 7。

---

## 5. 交付物三：Authorization Decision Model

```json
{
  "decision_id": "dec-2026-11-19-0001",
  "effect": "deny",
  "reason": "authorization expired",
  "policy_version": "2026.11",
  "subject": {"agent_id": "agent-A", "version": "1.1.0"},
  "action": {"tool": "delete_file", "params_digest": "sha256:..."},
  "inputs_snapshot": {
    "identity": "VERIFIED", "evidence": "VERIFIED",
    "authorization": {"state": "EXPIRED", "expires_at": "..."}
  },
  "obligations": ["notify_owner"],
  "ttl_seconds": 30,
  "issued_at": "2026-11-19T10:00:00Z"
}
```

**决策语义**：
- 默认 `deny`；无策略命中 = deny（不是 permit）
- `inputs_snapshot` 必须落库——**决策可复盘**，否则审计等于没做
- `ttl_seconds` 短（30–300 秒），避免"决策缓存变成永久许可"
- `params_digest` 绑定实际参数，防止"批了 A 却执行 B"

---

## 6. 交付物四：Runtime Enforcement Specification

| 要求 | 规格 |
|---|---|
| 拦截点 | 工具调用**唯一入口**；SDK 内不允许存在绕过路径（框架 hook 只能作为辅助，不能作为唯一防线） |
| 决策缓存 | 同 (subject, tool, params_digest) 在 TTL 内复用；**TTL 过期必须重评** |
| PDP 不可达 | **DENY**（fail-closed）。降级模式只允许"只读工具"，写/删/外发/支付一律拒绝 |
| 超范围 | 请求 scope ⊄ 授权 scope → 阻断 + 记事件 + 可选暂停会话 |
| 异常暂停 | 连续 N 次 deny、或触发注入特征 → 会话挂起，需人工恢复 |
| 撤销生效时延 | 目标 ≤ 5 秒（本地缓存失效 + 长连接推送）；超过即视为控制面缺陷 |

**关键一条**：`langchain_callback.py` 那种"框架主动回调"是好设计，但它只记录。控制面需要的是**在调用前拿到决策**——即在 `on_tool_start` 里抛异常阻断，而不是在 `on_tool_end` 里补记。

---

## 7. 交付物五：Human Override Specification

| 动作 | 触发者 | 生效方式 | 记录 |
|---|---|---|---|
| 审批（临时放行） | 指定审批人 | 生成一次性 permit（绑定 params_digest + TTL） | 审批人、时间、理由、有效期 |
| 紧急暂停 | 任意运维 + 值班 | 全局 kill switch，PEP 立即 deny-all（只读除外） | 触发人、范围、恢复条件 |
| 授权撤销 | 管理员 | 撤销授权记录 + 传播至 PEP 缓存 | 撤销原因、影响对象 |
| 恢复审批 | **双人复核** | 两人分别确认后才解除暂停 | 两条独立记录 |
| 双人复核适用 | 高风险类（pay/delete/external_send） | 单人无法完成 | 两条审批 + 一致性校验 |

**纪律**：人工接管必须经过**实际故障与绕过测试**（任务书原则 6）——不能因为"文档写了有这个功能"就认为有。

---

## 8. 交付物六：Fail-safe & Recovery Specification

| 故障 | 处理 | 禁止 |
|---|---|---|
| PDP 不可用 | deny（只读放行需显式白名单） | 默认放行 |
| 撤销状态无法确认 | **视为已撤销**（fail-closed） | 视为有效 |
| 审计存储不可写 | 拒绝执行高风险操作 | 先执行后补记 |
| 进程崩溃重启 | 从 append-only 审计重建状态 | 用内存快照恢复 |
| 恢复后状态冲突 | 取**更严格**方（撤销优先于授权） | 取更宽松方 |
| 策略版本丢失 | 停止新决策，仅维持已批准 TTL 内操作 | 用默认策略继续 |

**场景 8 的实现要求**：恢复流程必须有"已撤销集合"的外部持久化副本，重启后先加载撤销集合再加载授权——顺序反了就会静默恢复权限。

---

## 9. 交付物七：Adversarial Test Suite（设计，未运行）

> 本轮按任务书六只交计划，**不写不跑原型**。下表是下一轮的用例清单，每条都要求"输入 / 预期 / 实际 / 复现证据"。

| ID | 用例 | 输入 | 预期 |
|---|---|---|---|
| AT-01 | 未授权 Agent 调高风险工具 | unverified agent → delete | DENY + 通知 owner |
| AT-02 | 授权过期边界 | expires 前 1 秒 / 后 1 秒 | ALLOW / DENY |
| AT-03 | PDP 宕机 | 断 PDP → delete | DENY（不得放行） |
| AT-04 | 超范围 | scope={read} → write | DENY + 会话标记 |
| AT-05 | 撤销时延 | revoke → 立即调用（<1s） | DENY 或明确拒绝理由 |
| AT-06 | 参数替换 | 批准 `a.txt` 执行 `b.txt` | DENY（params_digest 不符） |
| AT-07 | 策略回滚回归 | 新策略 vs 旧策略跑同一语料 | 逐条列出行为差异 |
| AT-08 | 崩溃恢复 | 撤销后 kill -9 → 重启 | 仍 DENY（不得静默恢复） |
| AT-09 | 绕过 PEP 直连 | 绕过 SDK 调工具 | 必须失败（无第二入口） |
| AT-10 | 缓存滥用 | TTL 内换参数 | 重评，不得复用旧决策 |
| AT-11 | 双人复核单人完成 | 单人两次确认 | 拒绝 |
| AT-12 | 审计缺失 | 审计不可写 → 高风险操作 | DENY |

**指标**：误报率、漏报率必须统计（任务书 WP8）。**红线**：不统计就等于没测。

---

## 10. 交付物八：Control Effectiveness Report（当前实测）

| 控制项 | 有效性 | 证据 |
|---|---|---|
| 执行前授权检查 | **不存在** | 全生态无 authorization 对象（除 p21 原型） |
| 运行时阻断 | **不存在** | `langchain_callback.py` docstring 自述不拦截 |
| 人工急停 | **不存在（仅清单）** | `agent_kill_switch.py` 生成 JSON 卡片 |
| 撤销传播 | **不存在** | p21 原型有级联，未接入执行 |
| 审计完整性 | **部分** | 有事件记录，无 authorization 绑定 |
| 策略可测试 | **不存在** | 无策略版本、无回归语料 |
| 故障安全 | **不存在** | 无 fail-closed 执行点 |

**结论**：当前控制有效性 = **接近零**，且这一结论**有代码证据**，不是猜测。

---

## 11. 本地原型计划（下一轮执行，需批准）

**范围**：单进程最小控制面，不接真实 Agent 平台。

| 模块 | 内容 | 验收 |
|---|---|---|
| `pdp.py` | 策略加载、deny-overrides、优先级、决策对象 | AT-01/02/04/07 |
| `pep.py` | 唯一执行入口 + 决策缓存 + TTL + fail-closed | AT-03/09/10 |
| `audit.py` | append-only 事件 + 决策快照落库 | 场景 6 |
| `override.py` | 审批 / 急停 / 撤销 / 双人复核 | AT-05/11 |
| `recover.py` | 撤销集合优先加载 + 状态重建 | AT-08 |
| `test_at.py` | 12 条对抗用例 + 误报/漏报统计 | 全部 |

**预计规模**：约 900 行，纯标准库，本机可跑。
**不做的**：不接 LangChain（先证明控制逻辑，再谈集成）；不做多租户；不做 UI。

**需要批准**：① 是否允许写原型代码（本轮按边界未写）；② 原型放 `proposals/p22_control_plane/` 是否可接受。

---

## 12. 三条要立刻记住的教训

1. **"有记录"不等于"有控制"**。`langchain_callback` 记录了每一次 tool call，但它自己在文档里就承认不拦截。控制面要的是**调用前的 deny**。
2. **"有清单"不等于"有开关"**。`agent_kill_switch` 是部署前检查表，它能拦住"没想清楚怎么停"的 Agent 上线，但拦不住已经上线的 Agent 继续跑。
3. **"有关键词分级"不等于"有授权"**。`tool_guard` 按关键词判读/写/删，误报率天然高（前几轮污点原型在真实语料上 3/3 全是误报）。它可以做第一道粗筛，不能做授权判定。
