# EVIDENCE_LIFECYCLE_AUDIT（证据生命周期与撤销 · 2026-11-21）

> 结论：**证据"生成→签名→验证"这段有实现；"更新→取代→过期→撤销"四段没有任何字段、任何代码、任何文档支持（VERIFIED）。** 更要命的是：**缺时间戳的证据仍被判 `verified=True`**（S6），这意味着"证据会过期"这件事在当前实现里不存在。

## 一、七状态 × 现状

| 状态 | 是否有实现 | 证据（本日实查） |
|---|---|---|
| Evidence Created | **有** | `anchor_rekor.py` 生成收据；固定 entry 2883389783 |
| Evidence Signed | **部分** | checkpoint 签名可验；但 `signedEntryTimestamp` 缺失时仍通过（S7） |
| Evidence Verified | **有** | inclusion / consistency 两向实测通过，70 项跨检查 0 分歧 |
| Evidence Updated | **无** | 无"更新"概念，只有重新生成 |
| Evidence Superseded | **无** | 无 `supersedes` / `superseded_by` 字段 |
| Evidence Expired | **无** | 无 `valid_until`；S6 删除 `integratedTime` 仍通过 |
| Evidence Revoked | **无** | 全仓无撤销实现；唯一提及出现在 ITU 贡献稿文本 |

## 二、十个必需字段 × 现状

| 字段 | 现状 | 说明 |
|---|---|---|
| 证据来源 | **有** | `logID` + checkpoint `origin`（但 S10 零宽字符不改判定） |
| 生成时间 | **有但不强制** | `integratedTime` 可缺失（S6 通过） |
| 验证时间 | **无** | 校验结果不含"何时验的"，只有当下输出 |
| 适用版本 | **无** | 收据不含被证对象的 version / fingerprint |
| 适用环境 | **无** | 不记录 OS/Python/依赖 |
| 验证者 | **无** | 输出无签名、无身份；任何人都能产出"同一份"结果 |
| 失效时间 | **无** | 不存在该概念 |
| 撤销状态 | **无** | — |
| 撤销原因 | **无** | — |
| 历史记录 | **无** | 每次输出覆盖式，不保留历史 |

## 三、五个"重点防止"的实测结论

| 防止目标 | 实测 | 判定 |
|---|---|---|
| 旧版本证据被用于新版本 | 证据不含 `version`/`fingerprint`，无法判断"这是哪个版本" | **机制不存在（V）** |
| 已撤销证据继续被引用 | 无撤销字段，撤销后旧收据仍 `verified=True` | **机制不存在（V）** |
| 已过期证据仍有效 | 无有效期；S6 删时间戳仍通过 | **机制不存在（V）** |
| 签名正确但来源错误 | `logID` 可加零宽字符仍通过（S10）；`entry_log_index` 可为 −1（S13） | **来源绑定薄弱（V）** |
| 完整性被误认为真实性 | 文档已自我声明"完整性≠真实性"，但**输出 JSON 里没有这句话** | **有声明、无机器字段（V）** |
| 证据链断后仍 PASS | 缺 `inclusionProof` → exit 2；空 hashes → `verified=False` | **此条做对了（V）** |

## 四、LGD-Eval 侧的同类问题（更严重）

本日实测证据 JSON 的顶层键为：
`dims / engine_version / findings / fingerprint / framework / grade / inputs / reproduce / safety_veto / score`

- **没有时间戳**、**没有验证者**、**没有对象版本**、**没有失效时间**、**没有撤销状态**；
- 因此 LGD-Eval 的"证据"无法支撑任何生命周期判断，只能证明"某一刻跑过一次"；
- 且 `fingerprint` 仅由 score/dims/findings 计算，**同类不同内容的技能可能得到同一指纹**（本日 G1/G7 指纹相同即为实例，V）。

## 五、建议的最小闭环（六个字段起步，不新建仓）

在现有结果 JSON 外层包一个 `evidence_envelope`：

```json
{
  "created_at": "...", "verified_at": "...",
  "subject": {"version": "...", "fingerprint": "sha256:..."},
  "verifier": {"identity": "...", "signature": "..."},
  "valid_until": "2027-11-21T00:00:00Z",
  "status": "ACTIVE|SUPERSEDED|EXPIRED|REVOKED",
  "superseded_by": null, "revocation": {"at": null, "reason": null}
}
```

规则：
1. 缺 `created_at` 或 `valid_until` → `INCONCLUSIVE`，不得 `VERIFIED`；
2. `status != ACTIVE` → 一律不得在门禁中当 PASS；
3. 撤销与取代**追加记录，不删历史**；
4. 输出里必须带一句机器可读声明：`"assurance": "integrity_only"` 或 `"security"`——防止"完整性=真实性"的误读。

## 六、优先级

- **P0**：缺时间 → `INCONCLUSIVE`（S6），因为"永久有效"是当前最容易被外部攻击的一条。
- **P1**：`valid_until` + `status` 字段；`REVOKED` 退出码。
- **P2**：历史留存与 `superseded_by` 链。

> 诚实条款：本生态当前**没有任何一条证据带有效期**，所以"证据生命周期管理"这句话目前只能写成"已识别缺口，未实现"。
