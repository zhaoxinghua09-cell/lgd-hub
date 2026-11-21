# XLGD Agent Trust Network —— 技术研究与架构交付

**日期**：2026-11-19 · **性质**：只读研究 + 架构设计 + 本地原型
**授权范围**：仅研究、设计、本地原型。未新建正式项目、未改远端仓库、未发布协议、未对外合作、未提交标准、未作认证或商业承诺。
**标注**：FACT / INFERENCE / NOT VERIFIED / BLOCKED

---

## 0. 一句话结论

**7 个关键验收场景全部在本地原型中跑通（9/9 用例）**，但整套东西是研究件：密码学用 HMAC 代替真实签名，没有真实 Agent、没有真实平台、没有第三方参与。

这轮最大的价值不是"我们有个架构"，而是**第 4 个场景暴露了一个真缺陷**：撤销身份时没把供应链节点标为污染，导致上游感知不到。已修复并重跑。

---

## 1. Agent Trust Architecture（交付物一）

### 1.1 七层结构

```
┌─ L7 跨生态互操作 ── 协议映射 / 外部身份对接 / 跨平台向量       (P4)
├─ L6 Trust API ───── resolve / evidence / evaluation /
│                     authorization / revocation / chain-verify   (P3)
├─ L5 Registry ────── 注册、发现、状态查询、隐私边界              (P3)
├─ L4 供应链 ──────── Skills/MCP/API/模型依赖图、风险传播          (P2)
├─ L3 动态信任 ────── 评测 / 证据 / 授权 / 撤销 四轴分离          (P0)
├─ L2 委托 ────────── 委托链、范围继承、深度限制、再委托           (P1)
└─ L1 身份+证据 ───── 唯一身份、实体关系、行为事件模型             (P0)
```

### 1.2 一条请求的判定顺序（fail-closed 自上而下）

```
1 identity verified?   否 → DENY(identity)
2 evidence VERIFIED?   否 → DENY(evidence: UNKNOWN/INCOMPLETE/STALE)
3 authorization exists? 否 → DENY(NOT_GRANTED)  ← 评分不参与
4 authorization valid?  否 → DENY(expired / scope)
5 delegation chain ok?  否 → DENY(scope exceeds / depth / broken chain)
6 → ALLOW
```

**关键点**：第 3 步。评测分数哪怕 100 分也不会让流程继续——这是 P0 要求的"身份、证据、授权状态分离"的落地形态。

---

## 2. Agent Identity Schema（交付物二）

```json
{
  "agent_id": "agent-A",
  "creator": "creator-X",
  "operator": "op-X",
  "implementer": "impl-X",
  "versions": ["1.0.0", "1.1.0"],
  "key_fingerprint": "fp-A",
  "revoked": false,
  "revocation_reason": ""
}
```

| 字段 | 约束 |
|---|---|
| `agent_id` | **跨版本稳定**；版本变更不等于换身份 |
| `creator / operator / implementer` | 三者分离，允许不同主体（可转让运营权） |
| `versions` | 只追加，不覆盖历史（对应 S1） |
| `key_fingerprint` | 钉扎；presented 不一致即判冒用（对应 S2） |

**身份连续性规则（提议）**：版本升级不改 `agent_id`；若 creator 变更则视为**新身份**，必须重新登记——防止"换壳继承旧信任"。

---

## 3. Behavioral Evidence Schema（交付物三）

```json
{
  "ev_id": "ev-A-1",
  "agent_id": "agent-A",
  "agent_version": "1.0.0",
  "source": "observed",          // observed | declared
  "producer": "monitor-1",
  "payload": {"action": "read_crm"},
  "issued_at": "2026-11-19T10:00:00+00:00",
  "ttl_days": 90,
  "privacy": "redacted",
  "key_id": "k-A",
  "mac": "..."
}
```

| 设计点 | 规则 |
|---|---|
| **观测 vs 声明** | `declared`（自述）不得单独用于授权判定；只有 `observed` 可支撑 VERIFIED |
| **完整性** | 除 mac 外全字段参与规范化哈希，任一字段改动即失败（C2 已验证） |
| **有效期** | 按证据类型分档，不统一（见 §5） |
| **隐私** | `privacy=redacted` 表示公开记录只存摘要，原文留在受控侧 |
| **版本绑定** | `agent_version` 必填；版本不符 → STALE（S1） |

---

## 4. Delegation Model（交付物四）

```json
{
  "deleg_id": "d-2", "from": "agent-A", "to": "agent-B",
  "scope": ["read"], "depth": 2, "max_depth": 2,
  "allow_redelegation": true,
  "expires_at": "2026-12-19T00:00:00+00:00", "revoked": false
}
```

**四条硬约束**：
1. **范围只能是父集子集**——B 请求 `{read,write}` 而父只给 `{read}` → 阻断（S3 实测）
2. **深度**：`depth ≤ max_depth`，超出即链无效
3. **再委托**：`allow_redelegation=false` 时下游不得再授予他人
4. **撤销级联**：撤销 A 的任何一条委托 → 其下游全部失效（`revoke_all_from`）

**委托链验证**：`validate_chain()` 逐跳检查 depth、父节点存在性、再委托许可——缺一跳即 fail-closed。

---

## 5. Dynamic Trust State Model（交付物五）

```
identity_ok      bool
evidence_state   VERIFIED | UNKNOWN | INCOMPLETE | STALE
evaluation_score float|None      ← 只作参考，不进入决策
authorization    {subject, scope, expires_at} | None
```

**决策函数**（`TrustSnapshot.decision()`）：
- 只看 `identity_ok` / `evidence_state` / `authorization`
- `evaluation_score` **完全不参与**——实测传 96 分仍返回 `NOT_GRANTED`

**有效期分档（不同对象不同 TTL，不统一假设）**：

| 对象 | 有效期 | 依据 |
|---|---|---|
| 行为证据（observed） | 30–90 天 | 行为漂移速度 |
| 评测报告 | 90 天或规则版本变更 | 攻击手法演进 |
| 授权 | 30 天或上游失效 | 授权最脆弱 |
| 身份 | 365 天或密钥轮换 | 密钥周期惯例 |

---

## 6. Agent Supply Chain Model（交付物六）

```json
{"agent": "agent-B", "deps": [
  {"name": "agent-C", "version": "1.0.0", "source": "registry"},
  {"name": "skill-pack-7", "version": "2.3.1", "source": "git"},
  {"name": "model-x", "version": "2026-09", "source": "vendored"}
]}
```

**风险传播实测（S4）**：
```
C 被撤销 → invalidate("agent-C") 把依赖图中所有 agent-C 节点标 compromised
        → risk("agent-B") 返回 True，msg="agent-B: ['agent-C']"
        → dependents("agent-C") = ["agent-B"]
```
上游因此进入"必须重新评测"状态——这就是"撤销传播"要的东西。

**缺口（P2 未做）**：跨源版本冲突检测（同一 dep 在 registry 与 git 版本不一致）、传递闭包下的多跳风险聚合权重。**未实现，NOT VERIFIED**。

---

## 7. Trust API Specification（交付物七）

| 方法 | 输入 | 返回 | 失败语义 |
|---|---|---|---|
| `resolve(agent_id)` | id | `{status: REGISTERED/REVOKED/UNKNOWN, versions, creator, operator}` | 未知 → **UNKNOWN**，不抛异常 |
| `query_evidence(id, version)` | id + version | `{state, items[]}` | 无证据 → UNKNOWN；版本不符 → STALE |
| `evaluation(id, version)` | id + version | 报告 + 规则版本 | 无 → UNKNOWN |
| `authorization_check(id, scope)` | id + scope | ALLOW / DENY + reason | 缺授权 → NOT_GRANTED |
| `revocations(id)` | id | 撤销记录列表 | 空即"无记录"，不等于"无撤销" |
| `verify_delegation(agent)` | agent | 链验证结果 | 断链 → DENY |

**统一约定**：任何查询都不返回"看起来正常"的空对象；一律显式 `UNKNOWN` / `NOT_GRANTED`，让调用方必须处理异常态（P0 原则）。

---

## 8. Conformance Test Suite（交付物八）

`proposals/p21_agent_trust/test_acceptance.py` → **9/9 通过**（`evidence/p21_acceptance_results.json`）

| 场景 | 任务书要求 | 实测结果 |
|---|---|---|
| **S1** | 换版本后旧评测证据能否正确识别 | `new=STALE, old=VERIFIED` ✅ |
| **S2** | 身份被冒用后能否撤销并传播 | 指纹不符 → revoked，affected=[agent-A] ✅ |
| **S3** | B 超出 A 授权范围能否阻断 | `scope exceeds delegation: ['write']`，范围内放行 ✅ |
| **S4** | C 被撤销后上游能否感知 | `risk=agent-B: ['agent-C']`，dependents=[agent-B] ✅（**首轮失败，见 §11**） |
| **S5** | 第三方评测结果能否独立验证 | 重算摘要：真实报告一致、篡改报告不一致 ✅ |
| **S6** | 不同平台能否交换解释证据 | 键序不同的同一证据规范化哈希一致 ✅ |
| **S7** | UNKNOWN/INCOMPLETE 是否会被错误放行 | 两者均 DENY；仅评分 → NOT_GRANTED ✅ |
| **C1** | 正向对照 | 完整授权链 ALLOW ✅ |
| **C2** | 完整性对照 | mac 被改 → integrity fail ✅ |

---

## 9. Threat Model（交付物九）

| # | 威胁 | 攻击面 | 现有防护 | 缺口 |
|---|---|---|---|---|
| T1 | 身份冒用 | 伪造 agent_id + 自签密钥 | 指纹钉扎（S2） | 无真实 PKI，指纹靠人工分发 |
| T2 | 版本伪装 | 旧版本冒充新版本 | `agent_version` 绑定证据（S1） | 无版本签名链 |
| T3 | 权限提升 | 超范围委托 | 子集校验 + 深度限制（S3） | 无 scope 语义规范化（"read"含义可能不同） |
| T4 | 撤销不传播 | 下游继续用旧授权 | 级联撤销（S4） | 无跨注册表传播（单点） |
| T5 | 声明冒充观测 | 自述"我很安全" | `source` 字段区分 | 无第三方见证要求 |
| T6 | 供应链投毒 | 依赖包被替换 | compromised 标记传播 | 无来源哈希校验 |
| T7 | 重放 | 旧证据在新上下文复用 | 版本绑定 + TTL | 无 nonce/上下文绑定 |
| T8 | 评分驱动放行 | 把分数当许可 | `decision()` 不读 score（S7） | 产品侧 lgd-gate 仍是"≥96 免审批" |
| T9 | 隐私泄露 | 公开记录含敏感行为 | `privacy=redacted` | 无脱敏策略规范 |
| T10 | 单点停服 | Registry 挂掉 | 证据可离线验 | 状态查询无缓存/联邦 |

**最扎眼的一条**：T8。原型里已经彻底分离，但**产品侧 `lgd-gate/action.yml:86` 依然是"评分 ≥96 → 免审批直接执行"**。原型证明了这条路是错的，产品还没改。

---

## 10. Independent Reproduction Report（交付物十）

**如实报告：第三方复现 = 0。**

| 项 | 状态 |
|---|---|
| 本机自跑 | 9/9 通过（Python 3.13.18 / Windows 11） |
| 独立实现 | 0 |
| 外部节点回传 | 0 |
| `repro_kit` 是否覆盖 Agent 信任网络 | **否**——现有 14 向量只覆盖 UIBC 生命周期五类语义，不含委托链与供应链 |

所以：**不能写"已验证"**，只能写"原型自测通过"。任务书五要求 Independent Reproduction Report，本报告即是，但结论是"未达成"。

---

## 11. 本轮暴露并修复的真实缺陷

| 项 | 内容 |
|---|---|
| 现象 | S4 首轮 FAIL：`risk=""`，上游感知不到 C 被撤销 |
| 根因 | `TrustRegistry.revoke()` 只把 identity 标 revoked，**没有把供应链依赖图中的同名节点标为 compromised**；`SupplyChain.risk()` 只看 `DepNode.compromised` |
| 修复 | 新增 `SupplyChain.invalidate(node)`，在 `revoke()` 内调用；依赖该节点的上游因此进入风险态 |
| 复验 | 重跑 9/9 通过，`affected=['agent-C','agent-B']` |
| 教训 | **"撤销"和"风险传播"是两件事**：撤销一个对象，不等于依赖它的对象自动知道。这正是 WP3/WP4 要解决的核心问题，原型自己先踩了一遍 |

另修一处低级错误：`run("S4", ...)` 被误缩进进函数体成为死代码，导致该用例**静默不执行**——而首轮统计里它"消失"了（8 条而非 9 条）。这就是"静默失败"，比报错更危险。

---

## 12. WP 状态总表

| WP | 内容 | 状态 | 说明 |
|---|---|---|---|
| WP1 身份 | 唯一身份、实体关系、版本连续、冒用撤销 | **原型完成** | S1/S2 通过 |
| WP2 行为证据 | 事件模型、完整性、观测vs声明、有效期隐私 | **原型完成** | C2 通过；声明证据规则已定 |
| WP3 委托 | 链、范围、深度、再委托、撤销传播、审计 | **原型完成** | S3 通过；审计日志未做 |
| WP4 动态信任 | 分数与授权分离、证据与风险分离 | **原型完成** | S7 通过 |
| WP5 供应链 | 依赖图、版本来源、风险传播、变更重评 | **部分** | S4 通过；跨源冲突检测未做 |
| WP6 Registry | 注册发现、证据查询、风险展示、隐私 | **原型完成** | 隐私策略仅字段占位 |
| WP7 Trust API | 6 个查询接口 | **原型完成** | 无 HTTP/鉴权层 |
| WP8 跨生态互操作 | 协议映射、外部身份、跨平台向量 | **仅 S6 同构验证** | 无真实外部体系对接（BLOCKED） |

---

## 13. 下一步（需批准）

| # | 动作 | 需批准 | 理由 |
|---|---|---|---|
| 1 | 把委托链与供应链向量加入 `repro_kit`（14 → 22 条） | 否（内部） | 让外部人能复现 WP3/WP5 |
| 2 | 用真实 Ed25519 替换 HMAC | 否（内部原型） | HMAC 对称密钥无法支撑真实身份 |
| 3 | 起草 Trust API 的 HTTP/JSON 规范 | 否（文档） | P3 前置 |
| 4 | 对接一个真实外部身份体系（如 DID / OIDC） | **是** | 属对外接洽 |
| 5 | 产品侧移除"评分≥96 免审批"语义 | **是** | 改 lgd-gate 产品行为 |

---

## 14. 产物清单

| 文件 | 说明 |
|---|---|
| `proposals/p21_agent_trust/trust_model.py` | 身份/证据/委托/动态信任/供应链/Registry 六模块 |
| `proposals/p21_agent_trust/test_acceptance.py` | 7 场景 + 2 对照，9 用例 |
| `evidence/p21_acceptance_results.json` | 原始运行输出 |
| `Agent信任网络架构_20261119.html` | 架构图与验收结果看板 |
