# TRUST_REGISTRY_GOVERNANCE（Registry 治理设计 · 2026-11-21）

> 原则一句话：**Registry 是信任信息的公告板，不是信任的裁决者。**
> 现状（VERIFIED）：`ai-passport-spec` + SynomosAI `passport_lookup` 只有 **3 条硬编码示例**、口径单一 `found/not found`，没有"注册≠认证"的分层，也没有写入 API、撤销、争议、导出。

## 一、七个状态必须分开（不得合并成一个"在册"）

| 状态 | 含义 | 谁能写入 | 谁能否决 | 展示要求 |
|---|---|---|---|---|
| `REGISTERED` | 对象存在、坐标可解析 | 任何人（自主注册） | 无人 | 必须与"认证"视觉分离 |
| `IDENTITY_CONFIRMED` | 控制者证明了对该标识的控制（域名/DNS、GitHub 组织、密钥挑战） | 对象控制者 | Registry 可拒（证据不足） | 显示验证方式与时间 |
| `EVIDENCE_AVAILABLE` | 有可下载的证据包（含 SHA） | 任何人 | 无人 | 只说明"有证据"，不说"证据为真" |
| `EVALUATED` | 某评测者给出分数/结论 | 评测者（署名） | 对象可回应 | 必须显示评测者与规则版本 |
| `INDEPENDENTLY_VERIFIED` | 作者之外的验证者签名并锚定 | 验证者（签名） | 作者无权删改 | 必须显示验证者身份与 COI |
| `AUTHORIZED` | 被授权方明确批准某用途 | 授权方（如厂商/平台） | 授权方 | 必须写用途与期限 |
| `REVOKED` | 被撤销（任意前述状态可转） | 签发方/登记方/授权方 | — | 保留历史，展示原因与时间 |

**硬规则**：`REGISTERED` 永远不能渲染成绿色通过；一个对象可以同时有 `REGISTERED` + `EVALUATED` + `REVOKED`（历史并存）。

## 二、架构（可被他人实现，避免单一权威）

```
写入方（多） ──► 签名事件流（append-only） ──► 只读索引（可重建）
                     │
                     ├─ 事件类型：register / claim / evidence / evaluate / verify / authorize / revoke / dispute
                     └─ 每条事件带：actor、signature、ts、subject_fingerprint、prev_hash
```

- **append-only + 可重建**：索引是投影，事件流是真源；任何人可用事件流重算出同一索引（这是"可迁移/可导出"的技术前提）。
- **多 Registry 兼容**：导出格式即导入格式（`registry-export/0.1.jsonl`），允许第三个 Registry 读取我们的导出并独立呈现，**不要求它同意我们的结论**。
- **争议机制**：`dispute` 事件（谁对哪条 `evaluate`/`verify` 有异议 + 反证链接），争议不删除原结论，只在旁边挂"存在争议"标记。

## 三、与现行三处"护照/台账"的接口

| 现状 | 问题 | 接法 |
|---|---|---|
| Synomos `PASSPORT_LEDGER`（3 条硬编码） | 不可写、不可撤销 | 改为读 `registry-export` 文件/HTTP |
| `FINGERPRINT` 为服务常量 `FP-GOV-6999EE1111DE` | **所有查询回报同一个指纹** | 指纹必须按 subject 计算 |
| `passport_lookup(example-ai-brand)` → `found=true` | 示例被当真实登记 | 示例移入 `examples/` 并标 `sample=true` |

## 四、必须防的四件事

1. **注册=认证的暗示**：任何 UI/JSON 不得用 ✅ 表示"在册"；用灰底 `REGISTERED` 徽标。
2. **单一写入方**：若只有作者能写，Registry 立刻变成"作者的名单"，必须至少允许"自主注册 + 第三方验证者写入"。
3. **不可导出**：不能导出即锁定；导出必须含事件流而非仅最终状态。
4. **撤销被隐藏**：撤销后条目不得消失，必须显示 `REVOKED` 与原因。

## 五、最小实现（不新建仓，约 2–3 天量）

- `registry events append --type verify --subject <fp> --sig <...>` → JSONL；
- `registry build` → 重建只读索引（`index.json` + 每对象一页 MD）；
- `registry export` → `registry-export/0.1.jsonl`；
- `registry lookup <id>` → 返回**七状态数组**而非单一 `found`。

## 六、验收判据

1. 一个对象能同时显示"已注册 + 未验证"，且不误导；
2. 任意第三方可用导出重建出**逐字节一致**的索引（这是可迁移性的硬判据）；
3. 撤销一条后，旧记录仍在，`status=REVOKED`，门禁返回非零；
4. 第二个 Registry 能读我们的导出并展示，**结论可以与我们不同**。

> 诚实条款：以上全部是设计（TESTED 级文档），当前**没有任何一条代码实现**；`passport_lookup` 的 3 条示例不具备任何治理含义。
