# INDEPENDENT_VERIFICATION_SPEC（独立验证规范 v0.1 · 2026-11-21）

> 状态：**草案**。本文件不修改任何仓库，仅定义"什么样的结果才算独立验证"，供 uibc-core / lgd-xverify / lgd-gate / SynomosAI 共用。
> 依据：本日实查（`XLGD_最新阶段推进报告_20261121.md` 第二/三节 + `sub_LGD-Eval_audit_20261121.md`）。凡与现有工具不一致处，以"工具现状"列写明，不粉饰。

## 一、七个状态（必须互斥，必须有机器可读值）

| 状态 | 含义 | 谁可以给出 | 现有工具能否给出 |
|---|---|---|---|
| `NOT_TESTED` | 没有跑过，或只读了文档 | 任何人 | 不能（uibc 工具无此值） |
| `TESTED` | 跑了，但没有独立证据（无签名/无环境记录/无样本哈希） | 任何人 | 不能 |
| `VERIFIED` | 有独立证据链且校验通过 | 验证者（带身份与时间） | **能**（`verified=true`，但不区分签名缺失） |
| `FAILED` | 有独立证据链且校验失败 | 验证者 | 能（exit 1） |
| `INCONCLUSIVE` | 输入不足以判定（缺依赖、缺样本、跨 shard、证据不全） | 验证者 | **不能**（缺依赖时反而给 `VERIFIED`） |
| `EXPIRED` | 曾经 VERIFIED，但超出有效期或版本已变 | 验证者/登记方 | 不能（无有效期字段） |
| `REVOKED` | 被签发方或登记方撤销 | 签发方/登记方 | 不能（无撤销字段） |

**硬规则**
1. `TESTED` 不得被展示成 `VERIFIED`；`VERIFIED` 不得被展示成"安全"。
2. `INCONCLUSIVE` 不得被任何门禁当作 PASS；门禁遇到 `INCONCLUSIVE` 必须非零退出。
3. `EXPIRED` / `REVOKED` 不得被"重跑一次新的"覆盖掉历史——历史保留，新结果另起一条记录。
4. 一个结果只能属于**一个具体对象版本**（fingerprint + version）。跨版本继承一律视为无结果。

## 二、五条必须写进第一屏的区分

```
Self-Evaluation ≠ Independent Verification
CI Pass ≠ Security Assurance
Evidence Integrity ≠ Evidence Truth
Verified Version ≠ Verified Future Version
Registry Entry ≠ Official Endorsement
```

## 三、"独立"的判定标准（本条是本规范的核心，也是最容易被绕过的地方）

**不算独立**（实查已存在的情形）：
- 同一作者的不同 GitHub 账号（本生态：理论号 / 产品号 / 评测号 / org 全部同一人）→ 只能算 `TESTED`。
- 同一作者仓库里的"第二实现"（如 `uibc-iverify` 与 `uibc-core` 同作者）→ 只能算"内部对拍"，不是独立验证。
- fork 出来的仓（本生态 31 个 fork 全是自己的）→ 不算任何独立性。
- 只在同一台机器、同一个 Python、同一批缓存上跑 → 环境未独立。

**算独立**（至少满足 3 条）：
1. **主体独立**：验证者与作者无雇佣/合作/资金关系，且公开声明 COI（或匿名但可验证的假名身份）。
2. **环境独立**：不同机器/不同操作系统/不同语言运行时；环境记录可复核（OS、版本、命令、SHA）。
3. **输入独立**：使用**固定样本 + 固定 SHA**（不是作者现场生成的样本）。
4. **结论独立**：结果由验证者自己签名并发布，作者无权预先审改。
5. **可重复**：任何第三人按同一 README 能在 15 分钟内复现同一结论（成功或失败都算）。

> 现有唯一可用的独立验证通道，是本日交付的 `validator-kit-20261121/`：固定 SHA、离线、一条成功 + 五条失败、允许发布负面结果。它满足 3/4/5，缺 1/2 的登记——所以下面的 §5 要补"验证者身份"。

## 四、验证结果的数据结构（建议，字段名与 uibc-core 现状对齐）

```json
{
  "schema": "lgd-verification-result/0.1",
  "subject": {
    "kind": "skill|agent|package|evidence-bundle",
    "id": "zhaoxinghua09-cell/uibc-core",
    "version": "0.5.0",
    "fingerprint": "sha256:…",
    "artifact_sha256": "…"
  },
  "verdict": "VERIFIED|FAILED|INCONCLUSIVE|EXPIRED|REVOKED|TESTED|NOT_TESTED",
  "scope": "inclusion|checkpoint-signature|tree-consistency|skill-scan|full",
  "checks": [
    {"id": "inclusion-fold", "expect": "pass", "actual": "pass", "evidence": "receipt.json#/folds_against"}
  ],
  "environment": {
    "os": "Windows 11", "python": "3.13.18", "deps": {"cryptography": "50.0.2"},
    "commands": ["python run_verify.py"], "network": "offline"
  },
  "verifier": {"identity": "LGD-Eval|independent-human:<keyid>", "coi_declared": true, "independent_of_author": true},
  "timing": {"started_at": "2026-11-21T05:00:00Z", "finished_at": "…", "valid_until": "2027-11-21T00:00:00Z"},
  "signature": {"alg": "ed25519", "key_id": "…", "sig_b64": "…"},
  "anchor": {"kind": "rekor|rfc3161|none", "entry_uuid": "…", "log_index": 2761485521},
  "report_url": "https://…"
}
```

**字段强制规则**
- `verdict=VERIFIED` 时 `checks` 必须非空，且每条 check 都指向可复核证据。
- `signature` 缺失 → 最高只能是 `TESTED`。
- `anchor=none` → 允许，但必须在报告顶部写明"未锚定，可被事后替换"。
- `valid_until` 缺失 → 视为 `EXPIRED`（默认过期，不默认长期有效）。
- 一个 `fingerprint` 对应一个 `verdict` 历史列表，不允许覆盖。

## 五、验证者身份（现有工具完全缺，必须新增）

最小实现（不新建仓，挂在 `lgd-xverify` 或 kit 里）：
1. `verifier init` 生成 Ed25519 密钥对；公钥用 GitHub 账号或 ORCID 发布一次（形成"验证者身份"）。
2. 每次验证用私钥签 `result.json` 的 canonical 字节（JCS）。
3. 把 `result.json` 的哈希锚定到 Rekor（已有能力，直接复用）。
4. 提供 `verifier verify result.json --pubkey …` 离线复核签名 + 重新跑 checks。

**反作弊**：`independent_of_author` 不是自填字段，而要能核验——例如要求验证者用**与作者无关的账号**发布结果，或由第三方在报告页签名见证。

## 六、失败样本（Negative Controls）的最低要求

每个被验证对象必须提供且只能提供"**能失败**"的样本，否则不给 `VERIFIED`：
- ≥1 条应当通过的样本（证明链路通）；
- ≥3 条应当失败的样本（篡改内容/篡改签名/缺证据/过期）；
- 每条样本固定 SHA，附期望退出码与期望字段；
- "对所有输入都说 PASS"的验证器**必然**通不过这套样本（kit 的 6 条样本即按此设计）。

## 七、跨版本与过期

- 结果绑定 `version + fingerprint`；版本变化 → 旧结果为 `EXPIRED`，必须重跑。
- 有效期默认 12 个月；高风险对象（可执行代码）建议 90 天。
- 撤销：签发方发布 `revocation.json`（含 `fingerprint`、`revoked_at`、`reason`、`superseded_by`），验证 CLI 读到即返回 `REVOKED`，**保留历史不删记录**。

## 八、第三方复现的 15 分钟门槛（可验收）

1. 拿到 `validator-kit`（zip，23 KB）；
2. `sha256sum -c SHA256SUMS.txt` 全绿；
3. `python run_verify.py` 6/6 落在预期；
4. 填环境记录（OS/Python/依赖/网络）；
5. 签名并发布（可匿名）；
6. 允许贴出 FAIL 结果。

验收标准：**一个从未接触本项目的人，在无作者协助下 15 分钟内能产出带签名的 `VERIFIED` 或 `FAILED` 或 `INCONCLUSIVE` 结果**。目前 kit 满足 1–4、6，缺 5（签名工具）——这就是 §5 要补的东西。

## 九、与现有资产的对接（不重复造）

| 能力 | 已有 | 缺 | 接法 |
|---|---|---|---|
| 证据包与校验 | uibc-core（V） | 结果签名、有效期、撤销 | 在 receipt 外再包一层 `verification-result` |
| 跨格式裁决 | lgd-xverify / uibc-iverify | 统一 CLI、三值语义 | `verify --profile` |
| 门禁 | lgd-gate（黑盒 action） | 退出语义可见、INCONCLUSIVE 非零 | 把 gate 的判定改成读 `verdict` 字段 |
| 评测 | LGD-Eval | 三值态、fail-closed | 见 `XLGD_最新阶段推进报告` P0-1..3 |
| 登记 | skill-registry | 写入 API、撤销入口 | 存 `verification-result` 列表，不存"分数" |

## 十、这份规范自己也要被验证（诚实条款）

- 本规范由作者本人起草，属 `TESTED` 级设计，**不是** `VERIFIED` 标准。
- 要让本规范成立，最低需要 **1 个外部验证者**按 §8 跑通并发布结果；在拿到之前，任何"已建立独立验证机制"的表述都不成立。
