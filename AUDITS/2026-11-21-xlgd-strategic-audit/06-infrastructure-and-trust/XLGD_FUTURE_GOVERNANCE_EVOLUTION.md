# XLGD_FUTURE_GOVERNANCE_EVOLUTION（治理演进机制 · 2026-11-21）

> 原则：**早期不应为显得正式而创建空洞组织。** 治理机构应与"参与者数量"匹配，而不是与"野心"匹配。

## 一、六种机制 × 触发条件 × 成本

| 机制 | 何时需要（触发条件） | 成本 | 现在建会怎样 |
|---|---|---|---|
| **Specification Working Group** | ≥2 个独立实现 + ≥3 个外部贡献者 | 中（会议/纪要/流程） | 空壳，只有 1 人开会 |
| **Technical Steering Committee** | ≥5 名 maintainer，跨组织 | 高（决策僵局风险） | 空壳，且削弱唯一执行力 |
| **Maintainer Council** | ≥3 名 active maintainer | 低 | 暂无 = 0 |
| **Independent Review Panel** | 出现 ≥3 条需仲裁的争议 | 中 | 无争议可仲裁 |
| **Security Advisory Process** | 有外部使用者（≥1 生产使用） | 低-中 | **可以先做**（成本低、必要性已有） |
| **Community Governance** | ≥10 名外部参与者 | 高 | 无社区可治理 |

## 二、现在就做的一件事

**Security Advisory Process**（安全公告流程）——理由：它不依赖社区规模，而且我们已经有一个 P0（False PASS）需要按流程处理。成本 1 页文档 + 1 个邮箱别名。

## 三、演进阶梯（四个阶段，每阶段有明确判据）

| 阶段 | 判据 | 治理形态 | 决策方式 |
|---|---|---|---|
| G0（现在） | 1 maintainer、0 外部 | **单人 + 文档自我约束**（GOVERNANCE.md 已存在） | 本人决定，公开决策记录 |
| G1 | ≥2 maintainer | 双人规则：分支 1 评审、发布 1 批准 | 二人一致 |
| G2 | ≥3 maintainer + ≥5 外部贡献 | Maintainer Council + 变更流程 | 多数 + 公开异议 |
| G3 | ≥2 独立实现 + 跨组织 | Spec WG + Review Panel | 程序化投票 |

**当前在 G0**（V：contributors 全为本人；分支 0 评审；发布无审批）。

## 四、避免"治理剧场"的四条

1. 不设没有成员的组织（如"指导委员会"只有 1 人）；
2. 不设没有程序的投票（先有争议案例，再有仲裁机制）；
3. 不设无法执行的规则（如"SLA"）；
4. 任何治理文件必须写明"当前阶段与触发下一次演进的条件"。

## 五、与现有文档的关系（已存在，质量不错）

| 文件 | 内容 | 评价 |
|---|---|---|
| `GOVERNANCE.md` | 七步变更流程、决策记录 | **好**（但执行者只有 1 人） |
| `COI.md` | 利益冲突 | 好 |
| `SUCCESSION.md` | 继承 | 好（需补 emergency contact 实名） |
| `VERSIONING.md` | 版本与兼容 | 好（需落实到输出字段） |
| `INDEPENDENCE.md` | 独立性声明 | 好（需与 `result_class` 对齐） |

## 六、验收判据

1. 任一治理文件写明"阶段 + 下一阶段触发条件"；
2. 不出现"无成员的组织"；
3. Security Advisory Process 可在 30 天内上线；
4. 治理变更本身留决策记录。

> 诚实条款：GOVERNANCE/COI/SUCCESSION 等文件已存在且质量不错（V），但它们目前是"单人对自己的约束"，不是"多方治理"。
