# XLGD_SPECIFICATION_MATURITY_MATRIX（规范成熟度矩阵 · 2026-11-21）

> 实测底座（V）：`docs/*.md` 共 **24 处 MUST**、**0 处 SHOULD**、**0 处 MAY**；RFC2119 boilerplate **只出现在 `drafts/draft-zhao-uibc-evidence-chain-00.md`**，未进入正式规范文件；有 **19 项检查的命中矩阵**（`docs/CHECK-MATRIX.md`，由 `tools/check_matrix.py` 生成）；1015 例测试。

## 一、12 项规范要件 × 现状

| 要件 | 现状 | 证据 | 判定 |
|---|---|---|---|
| Terminology | 有 `docs/TERMINOLOGY.md` | 文件存在 | ✅ |
| Scope | 有（README/ARCHITECTURE 说明边界） | — | ✅ |
| Normative Requirements | **有 24 处 MUST，但无编号、无 SHOULD/MAY 分层** | 计数实测 | ⚠️ |
| Optional Requirements | **未区分**（0 处 MAY） | 计数实测 | ❌ |
| Security Considerations | 有 `SECURITY.md` + 规则 | — | ✅ |
| Privacy Considerations | 有数据策略（本轮新增） | — | ⚠️ |
| Compatibility | 有 `VERSIONING.md` / `INTEROP-MATRIX` | — | ⚠️（未测） |
| Error Handling | 有退出码，但**未定义完整表**（S4/S12 崩栈） | 本日实测 | ❌ |
| Versioning | 有 `VERSIONING.md`，但证据无 version 字段 | — | ⚠️ |
| Conformance | 有 `CONFORMANCE.md` + 7 正向 + 6 负向 | — | ✅ |
| Test Vectors | 有固定 SHA 样本 | — | ✅ |
| Implementation Guidance | 有 `ADOPTION-GUIDE` / `QUICKSTART` | — | ✅ |

## 二、"每条 MUST 是否有测试"的核心问题

| 事实 | 说明 |
|---|---|
| 24 处 MUST 分散在 docs 中，**多数无编号** | 无法逐条映射到测试 |
| 有 19 项检查（S1–S19）与攻击矩阵 | 说明"检查级"覆盖不错 |
| 有 1015 例测试 | 说明"代码级"覆盖强 |
| **但"MUST 编号 ↔ 测试"的对应表缺失** | 这是规范成熟度最关键的缺口 |

**结论**：覆盖强、可追溯弱。`CHECK-MATRIX.md` 解决了一半（检查 ↔ 攻击），缺另一半（MUST ↔ 检查/测试）。

## 三、建议的最小整改（不改仓，仅设计）

1. **给 24 处 MUST 编号**（`MUST-01…24`），每条一句话；
2. **每条 MUST 标注级别**：MUST / MUST NOT / SHOULD / MAY（当前 0 SHOULD/MAY，说明规范把太多东西写成了强制）；
3. **每条 MUST 映射到 ≥1 检查（S1…S19）或测试**，缺映射的标 `untested`；
4. **退出码表**：0=VERIFIED / 1=FAILED / 2=INCONCLUSIVE / 3=EXPIRED / 4=REVOKED / 5=ERROR；
5. **在正式规范首页写 RFC2119/RFC8174 声明**（现在只在 draft 里）。

## 四、规范性要求与建议的混用风险

当前文本里"MUST"与普通建议混在同一章节，导致：
- 第三方实现无法判断"哪条不做就不合规"；
- 我们自己的实现也无法被逐条审计。

这是**独立实现挑战的前置条件**：不编号，挑战就无法评分。

## 五、评级

| 项 | 等级 |
|---|---|
| 术语/范围/一致性/向量 | **B（可用）** |
| 规范性编号与分级 | **D（缺失）** |
| 错误处理与退出码 | **D（缺失）** |
| 版本与兼容 | **C（部分）** |
| 整体 | **C+（强实现、弱规范形式）** |

> 诚实条款：MUST/SHOULD/MAY 计数与 CHECK-MATRIX 存在为实查；"哪条 MUST 无测试"因缺编号**无法判定**（N），这本身就是要修的。
