# TRUST_DECISION_OUTPUT_SPEC（信任决策输出规范 · 2026-11-21）

> 出发点：现有输出是 `Score / Grade / PASS / FAIL / Risk`，**这不是决策**。用户真正要问的是"能不能上、要不要人审、要限制什么、还缺什么证据、下一步做什么"。
> 本规范定义三层输出：**Decision → Evidence → Evaluation**，顺序不可颠倒（先给决策，再给依据，最后才是分数）。

## 一、三层结构（机器可读，单一 JSON）

```json
{
  "schema": "lgd-trust-decision/0.2",
  "decision": {
    "decision": "ALLOW | ALLOW_WITH_RESTRICTIONS | REQUIRE_HUMAN_APPROVAL | BLOCK | INSUFFICIENT_EVIDENCE",
    "confidence": "HIGH | MEDIUM | LOW",
    "confidence_basis": ["evidence complete", "verifier independent", "no critical findings"],
    "critical_findings": [{"id": "R-SEC-09", "what": "credential egress to external host", "where": "scripts/x.py:12"}],
    "required_actions": ["remove egress call", "re-run with fixed sample"],
    "approval_requirements": {"human_approver_role": "security-reviewer", "reason": "critical finding"},
    "restrictions": ["network egress disabled", "no filesystem writes outside workdir"]
  },
  "evidence": {
    "references": [{"artifact": "receipt.json", "sha256": "…", "anchor": "rekor:2761485521"}],
    "coverage": {"identity": "TESTED", "permission": "NOT_TESTED", "tool_execution": "PARTIALLY", "data_leakage": "FAILED", "prompt_injection": "NOT_TESTED", "governance": "NOT_TESTED", "provenance": "VERIFIED", "version_integrity": "INCONCLUSIVE"},
    "missing": ["no runtime sandbox trace", "no independent verifier signature"],
    "integrity": "VALID | TAMPERED | UNANCHORED",
    "verification_status": "NOT_TESTED | TESTED | VERIFIED | FAILED | INCONCLUSIVE | EXPIRED | REVOKED"
  },
  "evaluation": {
    "score": 62, "grade": "C", "rule_version": "1.1.0", "evaluation_version": "0.2.3", "risk": "HIGH",
    "score_status": "EXPERIMENTAL"
  }
}
```

## 二、Decision 的五个取值与准入条件

| Decision | 何时给出 | 禁止条件 |
|---|---|---|
| `ALLOW` | 无 CRIT/HIGH；证据完整；验证状态 `VERIFIED` 且未过期 | 缺签名、缺覆盖、有 HIGH 时不得使用 |
| `ALLOW_WITH_RESTRICTIONS` | 有 HIGH 但可限制（如禁网、只读） | 有 CRIT 时不得使用 |
| `REQUIRE_HUMAN_APPROVAL` | 证据不足、或权限越界、或评测为 EXPERIMENTAL | 不得用它掩盖"无法判定" |
| `BLOCK` | 任一 CRIT；或检测到凭证外发/敏感路径写入 | 不得因"分数高"而降级为 ALLOW |
| `INSUFFICIENT_EVIDENCE` | 缺关键证据（无运行 trace、无签名、对象版本不明） | **这是最常用的诚实答案**，不得替换成 ALLOW |

**硬规则**：`decision` 与 `score` **解耦**。分数只出现在 evaluation 层，不能反向决定 decision。

## 三、Confidence 的判定（不许拍脑袋）

| 置信 | 条件（全部满足） |
|---|---|
| HIGH | 证据完整 + 验证者独立（非作者）+ 无 CRIT/HIGH + 覆盖矩阵八类中 ≥6 类为 `TESTED`/`VERIFIED` |
| MEDIUM | 上述缺 1 项（如验证者仍是作者自测） |
| LOW | 覆盖 <4 类，或评分为 EXPERIMENTAL，或对象版本不明 |

## 四、Required Actions / Restrictions 的写法

- **具体到能执行**：`remove egress call at scripts/x.py:12`，不写"加强安全"。
- **限制项可机器执行**：`network_egress: disabled`、`fs_write: workdir_only`、`secrets: none`。
- 每条 action 必须带 `verify` 字段（重跑哪条规则可确认已修）。

## 五、与现有输出的差距（V）

| 现状 | 差距 |
|---|---|
| `evaluate.py` 输出 score/grade/findings/dims | **无 decision 层**；`--fail-under` 是唯一决策（分数阈值） |
| uibc 输出 `verified: true/false` | **只有二值**，没有"证据不足"这一档（缺 `INCONCLUSIVE`） |
| Synomos `gov_scan` 返回命中项 | 无 decision、无 approval、无 restrictions |
| 全部工具 | **无 coverage、无 missing evidence、无 confidence** |

## 六、三条免责与边界（必须写进输出）

1. `"This decision is advisory. The deploying party remains the risk owner."`
2. `"Score is experimental and MUST NOT be used as a security certification."`
3. `"Integrity of evidence does not imply truthfulness of content."`

## 七、验收判据

1. 任一工具输出可被解析为三层 JSON，且 decision 不由 score 推导；
2. 面对"凭证外发"样本，decision 必须是 `BLOCK`（本机 G2 现状会是 `ALLOW` + 100/A+，即失败）；
3. 面对空对象，decision 必须是 `INSUFFICIENT_EVIDENCE`（现状 67/C，即失败）；
4. 每个 decision 都能被第三方向后追溯到具体 evidence reference。

> 诚实条款：本规范是设计（TESTED 级文档），当前**没有任何工具实现 decision 层**；实现它是 Week 3 的事，且会改变现有退出码语义，需批准。
