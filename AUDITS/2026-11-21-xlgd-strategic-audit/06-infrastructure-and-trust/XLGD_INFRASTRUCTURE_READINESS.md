# XLGD_INFRASTRUCTURE_READINESS（基础设施就绪度 · 2026-11-21）

> 判定规则：九问全绿才算"基础设施"；有一项缺，只能叫"组件"。
> **结论：七层中只有 Evidence 层接近"基础设施"，其余为"规范草案 + 单实现 + 零外部使用"。**

## 一、七层 × 九问

| 层 | 正式定义 | 公开规范 | 参考实现 | 自动化测试 | 外部使用者 | 独立实现 | 跨平台 | 业务场景 | 长期维护 |
|---|---|---|---|---|---|---|---|---|---|
| 1 规范 Spec | ✅ | ✅ | ✅ | ✅（1015 例） | ❌ 0 | ❌ 0 | ✅（Win/Linux 记录） | 部分（医械用法文档） | ⚠️ 单人 |
| 2 身份 Identity | ⚠️ 部分（PUBLISHER-IDENTITY.md） | ✅ | ⚠️ 部分（目录密钥，无 DID） | ⚠️ 部分（S2/S10 实测有缺口） | ❌ | ❌ | ⚠️ | ⚠️ | ❌ |
| 3 **证据 Evidence** | ✅（RECEIPT-FORMAT / ATTESTATION / verdict-and-seal） | ✅ | ✅ | ✅（三段 + 19 检查矩阵 + 6/6 kit） | ❌（只有作者邀请的节点） | ❌ | ✅（本机 + Linux 记录 + 第二台机记录） | ✅（受监管团队的用例文档） | ⚠️ 单人 |
| 4 评测 Eval | ✅ | ✅ | ✅ | ✅（4 例 + 我们 11 例对抗） | ❌ | ❌ | ⚠️（Windows 要修 PATH） | ⚠️ | ❌（P0 未修） |
| 5 治理 Governance | ✅（GOVERNANCE/COI/SUCCESSION/VERSIONING） | ✅ | ⚠️（a3 评分、gov_scan） | ⚠️ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ |
| 6 登记 Registry | ✅（INTEROP-REGISTRY / ai-passport-spec） | ✅ | ❌（3 条硬编码） | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 7 互操作 Interop | ✅（INTEROP-MATRIX / 适配器映射） | ✅ | ⚠️（A2A 映射是"未来适配器"） | ⚠️ | ❌ | ❌ | N/A | ❌ | ❌ |

图例：✅ 具备 / ⚠️ 部分 / ❌ 缺

## 二、每层一句话判词

1. **规范**：文本与测试是这套体系最扎实的部分（24 处 MUST、19 项检查矩阵、1015 例测试），**但没有一份 RFC2119 关键词声明落在正式规范文件里**（只在 `drafts/draft-…-00.md` 有 boilerplate）。
2. **身份**：有"发布者身份"文档，但实现层无绑定（零宽字符 logID 仍通过，S10；负索引仍通过，S13）。
3. **证据**：**唯一接近基础设施的一层**。有格式、有实现、有负向样本、有跨机记录、有外部节点尝试（但外部节点仍是"作者邀请"）。
4. **评测**：有引擎与规则，但**结论会被一行注释关闭**（SP-14），且有 `benchmarks/README.md` 自述数字与实测不一致。
5. **治理**：GOVERNANCE/SUCCESSION 文档质量不错（七步变更流程、决策记录），**但没有第二个执行者**，文档是"单人自我约束"。
6. **登记**：只有规格与 3 条硬编码示例，**没有写入、撤销、导出**。
7. **互操作**：A2A 映射明确标注"normative for the future adapter"——**即尚未实现**。

## 三、能不能称"AI Trust Infrastructure"

**不能（V）。** 行业基础设施的最低门槛是"别人能在不知道作者的情况下用起来并互通"。当前硬指标：
- 外部使用者 0、独立实现 0、注册表可写性 0、互操作实测 0；
- 唯一可对外的强项是"证据链可离线复验"（kit 6/6）。

**可以怎么称（建议措辞）**
> `A specification-plus-reference-implementation project for verifiable evidence chains, with one verified end-to-end path (provenance) and an explicit list of what it does not verify.`

## 四、距离"基础设施"的三个最短路径

| 步 | 动作 | 成本 | 完成后可称 |
|---|---|---|---|
| 1 | 把 24 处 MUST 抽成带编号的规范性要求表 + 每条对应测试（CHECK-MATRIX 已有一半） | 2 天 | "规范可被逐条实现" |
| 2 | 1 个外部实现跑通正向 7 + 负向 6 | 需外部人 | "可独立实现" |
| 3 | Registry 可写 + 可导出 + 第三方重建 | 3 天 | "登记可迁移" |

> 诚实条款：本表"是否具备"基于文件与实跑；"业务场景"依据 `USE-CASE-regulated-agent-team-delivery.md` 等文档的存在，**不等于有人用**。
