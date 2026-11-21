# TRUST_PORTABILITY_SPEC（信任可迁移性规范 · 2026-11-21）

> 目标：**让证据与结论在离开本生态后仍然可用**，且不强制依赖任何 SaaS。
> 现状（V）：证据侧已部分可迁移（离线 kit、SHA256SUMS、6/6 落预期）；结论侧**不可迁移**（无签名、无版本绑定、无导出格式）。

## 一、七类对象 × 可迁移性现状

| 对象 | 当前形态 | 外部能读吗 | 外部能验吗 | 判定 |
|---|---|---|---|---|
| Agent 身份 | logID / origin /  passport 条目 | 部分 | 部分（零宽字符仍通过，S10） | ⚠️ |
| 版本指纹 | `sha256`（canonical JSON） | 是 | 是（可重算） | ✅（但仅限评测输出） |
| Evidence Manifest | `SHA256SUMS.txt` + 收据 | 是 | 是（kit） | ✅ |
| Evaluation Report | 终端输出 / SARIF / evidence JSON | 是 | 否（无签名） | ⚠️ |
| Verification Record | 无统一结构 | 否 | 否 | ❌ |
| Governance Status | 无 | 否 | 否 | ❌ |
| Revocation Status | 无 | 否 | 否 | ❌ |

## 二、八条要求（逐条对照）

| # | 要求 | 现状 | 缺口 |
|---|---|---|---|
| 1 | 公开数据结构 | 部分（RECEIPT-FORMAT、SARIF、evidence JSON） | 无统一 `result` schema |
| 2 | 公开验证规则 | 部分（规则 ID 公开，权重未公开） | 权重与阈值未写进规范 |
| 3 | 公开兼容性要求 | 有 INTEROP-MATRIX | 但三对端全 not tested |
| 4 | 支持导出 | 部分（JSON/SARIF） | 无 Registry 导出（`export.jsonl`） |
| 5 | 支持离线验证 | **是（kit）** | 需装 `cryptography`；缺依赖时反而"通过" |
| 6 | 支持其他 Registry | 否 | 无导出格式 |
| 7 | 不强制依赖 SaaS | **是**（全本地） | 但依赖 Rekor 在线签发 |
| 8 | 支持迁移到其他实现 | 否（无第二实现） | 无兼容性证据 |

## 三、统一可迁移格式（建议，最小集）

```json
{
  "schema": "lgd-trust-bundle/0.3",
  "subject": {"id": "...", "version": "0.5.0", "fingerprint": "sha256:..."},
  "evidence": [{"path": "receipt.json", "sha256": "...", "anchor": {"kind": "rekor", "log_index": 2761485521}}],
  "result": {"verdict": "VERIFIED|FAILED|INCONCLUSIVE|EXPIRED|REVOKED",
             "result_class": "R1|R2|R3|R4|R5",
             "confidence": "HIGH|MEDIUM|LOW",
             "coverage": {...}, "missing": [...]},
  "evaluator": {"identity": "...", "signature": {"alg": "ed25519", "sig_b64": "..."}},
  "time": {"created_at": "...", "valid_until": "..."},
  "verify": {"command": "python run_verify.py", "offline": true, "deps": ["cryptography"]}
}
```

**字段强制规则**
- 缺 `signature` → `verdict` 最高 `TESTED`；
- 缺 `valid_until` → 视为 `EXPIRED`；
- `evidence[].anchor` 必须可离线校验或明确标 `UNANCHORED`；
- `verify.command` 必须可被陌生人直接执行。

## 四、跨实现的兼容性要求（三种读法都要支持）

1. **宽容读入**：未知字段不得导致失败（但必须在报告中列出被忽略字段）；
2. **严格判定**：必需字段缺失 → `INCONCLUSIVE`，不得默认通过；
3. **确定性输出**：同一 bundle 在任何实现下 canonical 序列化一致（JCS）。

## 五、可迁移性的三条硬测试（当前可做）

| 测试 | 当前 | 判据 |
|---|---|---|
| T-A 离线复验 | ✅（6/6） | 断网可跑 |
| T-B 第三方重建 fingerprint | ✅（可重算） | 与产出方一致 |
| T-C 导出后由另一实现读入 | ❌ | 需第二实现 |

## 六、诚实边界

- 证据"可迁移"到目前只到"可离线校验"这一步；
- **结论"可迁移"为零**：没有签名、没有有效期，别人拿到只是"一段文本"；
- 因此对外只能说：`Evidence bundles are portable and offline-verifiable. Results are not yet portable (no signature/expiry).`

## 七、30 天最小交付

1. 定义 `lgd-trust-bundle/0.3` 并在 1 个真实样本上产出；
2. 加 Ed25519 签名（`verifier sign` / `verify`）；
3. 加 `valid_until` 与 `REVOKED` 返回码；
4. 导出脚本 `bundle export --json`。

> 诚实条款：schema 为设计（TESTED 级）；当前实现只覆盖其中约 40%（evidence + verify）。
