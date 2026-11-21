# XLGD_PHASE_V_STRATEGIC_ASSESSMENT（第五阶段 · 最终战略地位评估 · 2026-11-21）

> 本文件不做"总评级"。十项成熟度分列，每一项都有自己的证据与缺口。**如果只能记一句话：这是一个"证据层接近基础设施、其余全部处于原型期"的单人项目。**

## 一、十项成熟度（逐项）

### 1. Research Maturity
- **当前等级：B-（内部成熟、外部为零）**
- 证据（V）：三律/判定器/13 域文档体系；`ADR-001-three-valued-verdict`；`CROSSWALK-*` 逐条覆盖且带"未覆盖"列；ORCID 作品已索引。
- 缺失：无同行评议；无预印本被引；无外部研究者复现（唯一外部痕迹是分歧记录，非背书）。
- 外部验证状态：**NONE（1 条 mention，性质为分歧）**
- 下一阶段目标：1 篇可被引用的技术说明（稳定 URL + 版本），并把 AER-1 分歧的命令与输出并排公开。

### 2. Protocol Maturity
- **当前等级：C（有骨架、缺形式）**
- 证据（V）：`docs/` 24 处 MUST、**0 SHOULD、0 MAY**；RFC2119 声明只在 draft 中；19 项检查的命中矩阵（S1–S19）；`CONFORMANCE.md` 7 正向 + 6 负向。
- 缺失：MUST 无编号、无分级、无"MUST↔测试"映射；无完整退出码表；证据无 `version` 字段。
- 外部验证状态：**NONE（0 外部实现）**
- 下一阶段目标：24 条 MUST 编号 + 分级；退出码表；缺依赖→INCONCLUSIVE。

### 3. Implementation Maturity
- **当前等级：B（单实现扎实、可复跑）**
- 证据（V）：uibc-core HEAD `2088469d…`，1015 例测试全绿（PATH 修正后）；Rekor 三段实测通过（inclusion/checkpoint/consistency）；6 条负向符合契约；`--sandbox` 有实现但 Windows 实测受限。
- 缺失：第二实现为 0；Windows 沙箱不能用；缺依赖时**静默通过**（P1 缺陷）。
- 外部验证状态：**NONE**
- 下一阶段目标：修 3 个 P0/P1；发布 0.5.1 并拆分 `verified_inclusion`/`verified_signature`。

### 4. Evaluation Maturity
- **当前等级：D+（自评失效）**
- 证据（V，本机对抗实测）：凭证外发载荷 **100/A+（安全 25/25）**；`# skillgate: ignore` **100/A+**；空目录 67/C；仅 SKILL.md 87/A；`samples/`/`demo/` 不扫描；14 例收据变体 6 例误判（字符串 logIndex 崩栈、重复 key、缺 SET、缺 integratedTime、负 index、零宽 logID 全通过）。
- 缺失：安全维度为一票否决；注释豁免；空对象 fail-closed；扫描范围含 samples。
- 外部验证状态：**FAILED（我们自己证明了它不可信）**
- 下一阶段目标：**止血**——恶意样本必须 0 通过；在此之前任何对外评分都标 EXPERIMENTAL。

### 5. Evidence Maturity
- **当前等级：B+（最接近基础设施的一层）**
- 证据（V）：离线 validator kit（6/6 落预期、zip 23,512B、`SHA256SUMS`）；固定 Rekor 样本可在断网复验；负向样本覆盖 6 类；`REPRODUCTION-REGISTER.md` 存在。
- 缺失：结论无签名、无 `valid_until`、无撤销；单一锚（Rekor 在线）；`cryptography` 缺失时 fail-open。
- 外部验证状态：**SELF-ONLY（自测通过，0 外部执行）**
- 下一阶段目标：Ed25519 签名 + 有效期 + 撤销返回码 + 第二锚（OTS/RFC3161）。

### 6. Governance Maturity
- **当前等级：C-（文件齐、执行体只有 1 人）**
- 证据（V）：`GOVERNANCE.md` 七步流程、`COI.md`、`SUCCESSION.md`、`ENDORSEMENTS.md`、`INDEPENDENCE.md` 均已存在且质量不错；但 contributors 六维全 1（仅本人 + dependabot）；分支 `required_approving_review_count=null`；`pypi` 环境 `protection_rules=[]`。
- 缺失：无第二 maintainer；发布无审批；无安全公告流程（Security Advisory Process 缺失）。
- 外部验证状态：**NONE**
- 下一阶段目标：G0→G1 触发条件写入文档；`pypi` 加审批人；30 天内上线安全公告流程。

### 7. Interoperability Maturity
- **当前等级：D（有矩阵、无对端）**
- 证据（V）：`INTEROP-MATRIX.md`、`SCITT-CROSSWALK.md`、`CROSSWALK-ASQAV-COMPLIANCE.md`、`CROSSWALK-ISC-0174.md`、`SECOND-IMPLEMENTATION.md`、`STRANGER-TRIAL.md`、`OUTSIDER-RUN.md` 均已存在（文档先行，质量高）。
- 缺失：三对端全部 `not tested`；无第二实现；无跨实现事件互操作。
- 外部验证状态：**NONE**
- 下一阶段目标：1 个外部实现对同一 bundle 输出相同 verdict。

### 8. Ecosystem Maturity
- **当前等级：D+（172 仓、0 外部人）**
- 证据（V）：自有 141 / fork 31；许可证 MIT 60 / NOASSERTION 38 / Apache 20 / 无证 15 / CC-BY 7 / AGPL 1；重名 4 组；PyPI 近一日 uibc-core 120 次、synomos 2 次；组合矩阵 141 行中 **EXPERIMENT 112**；DX 十项最高 8 分、hub 仅 2 分；5 仓 llms.txt、4 仓 CITATION.cff。
- 缺失：无外部贡献者；112 个实验仓 = 认知负担；许可证不统一（LGD-Eval CC BY 4.0 vs MIT vs Apache）。
- 外部验证状态：**NONE**
- 下一阶段目标：ARCHIVE/MERGE 一轮（112→~60）；15 无证仓补 LICENSE；许可证定案。

### 9. Market Maturity
- **当前等级：C-（需求有外部证据、客户 0）**
- 证据（V，外部）：ClawHub 2,857 技能中 341 恶意（11.9%）；MCP 21,000+ 实例中 91.8% 缺 OAuth、687 工具暴露 shell；21,643 服务器中 40.6% 静默改声明、370 台换端点（OR 2.96）；Viper-MCP 39,884 仓 106 个 0-day。→ 9 个需求分档：Skills/MCP/重评为 **Confirmed**；Evidence/Governance 为 **Weak**。
- 缺失：0 客户访谈；0 付费；05 个竞品有免费替代。
- 外部验证状态：**PARTIAL（第三方研究，非我方客户）**
- 下一阶段目标：3 次行业对话（医械合规 + 咨询机构渠道），不带报价。

### 10. Commercial Maturity
- **当前等级：F（未开始）**
- 证据（V）：收入 0；无报价；无合同模板；无 SLA 能力（10 项服务质量仅 2 项可对外）；唯一可交付项是"专业审计"。
- 缺失：产品化、报价、交付模板、客户、渠道。
- 外部验证状态：**NONE**
- 下一阶段目标：1 份样张报告 + 1 套模板 + 1 次免费试点。

## 二、八问（直接回答）

**Q1 它究竟是什么？**
**四者都不是完整形态，准确说：一个"以证据完整性为核心的协议原型 + 一组开源工具"，其中 Evidence 层已具备基础设施属性（可离线复验、可锚定、可复现），其余层是设计与单实现。** 不能称"已具备实际基础设施属性"——因为基础设施的判据是"别人依赖它"，而外部使用数为 0。

**Q2 哪些能力已有证据？**
① 收据/证据的离线校验（kit 6/6）；② Rekor 锚定与一致性校验（三段实测）；③ 1015 例测试；④ 19 项检查的命中矩阵；⑤ 对抗测试**证明了自身的失效模式**（这是最硬的证据）；⑥ 供应链钉 SHA 与最小权限；⑦ 172 仓/许可证/流量的实测清点。

**Q3 哪些能力仍只是设计？**
签名与有效期、撤销、Registry 导出、跨 Registry、第二实现兼容、monitoring、SLA、多方治理、AI 决策层（`lgd-trust-decision`）、商业产品与定价。

**Q4 最值得继续投入？**
按 ROI 排序：**① 修评分安全一票否决（信任的地基）② 缺依赖→INCONCLUSIVE ③ 外部人（邀请 + 名单页 + 故障库外部化）④ 一键 CLI ⑤ monitoring 最小版**。前两项各 1–2 小时，收益最大。

**Q5 哪些应开放给第三方？**
规范、参考实现、测试向量、**校验器**、公共结果（含失败）。理由：不开放则无法独立实现、无法验证、也无法形成网络效应。**校验器永久免费，且不得对"验证"收费。**

**Q6 哪些能形成收入？**
只有"人做的判断与责任"能卖：专业审计（MCP 权限/证据包）、持续监控订阅、企业部署与培训、私有证据管理、咨询机构分成。**不卖通过、不卖认证、不卖评级、不卖"付费优先上榜"。**

**Q7 怎样避免被单一作者/单一服务控制？**
四个动作：① 写 `BUS_FACTOR.md` + 异地备份 + 恢复码离线（当前**无**）；② 引入第二 maintainer（触发条件写进 `GOVERNANCE.md`）；③ 加第二锚（OTS/RFC3161）+ Registry 导出，避免被 Rekor/GitHub 锁死；④ 把"验证"这件事的最终判定权交给任何能跑 kit 的人——包括与我们意见不同的人。

**Q8 怎样建立长期信任与互操作价值？**
顺序不能颠倒：**证据可复现（已有）→ 结果可迁移（缺签名/有效期）→ 多方验证（缺人）→ 互操作（缺实现）→ 商业（缺客户）**。任何一步跳过都会变成"自说自话"——本轮的对抗实测已经演示了跳过第一步的后果（100/A+ 的恶意载荷）。

## 三、评级汇总（分列，不合并）

| 维度 | 等级 | 外部验证 |
|---|---|---|
| Research | B- | NONE（1 分歧记录） |
| Protocol | C | NONE |
| Implementation | B | NONE |
| Evaluation | **D+** | **FAILED** |
| Evidence | **B+** | SELF-ONLY |
| Governance | C- | NONE |
| Interoperability | D | NONE |
| Ecosystem | D+ | NONE |
| Market | C- | PARTIAL（第三方研究） |
| Commercial | **F** | NONE |

> **不给出总体评级**：因为把 B+ 与 F 平均成"B-"会误导决策。真实形态是"一个非常强的证据校验器 + 一个失效的评分器 + 一个不存在的市场"。

## 四、Phase V 十四份文档索引

INFRASTRUCTURE_READINESS / TRUST_NETWORK_EFFECTS / MULTI_PARTY_TRUST_GOVERNANCE / TRUST_PORTABILITY_SPEC / TRUST_ASSURANCE_BOUNDARY_POLICY / XLGD_ECOSYSTEM_ECONOMICS / XLGD_CRITICAL_DEPENDENCY_MAP / XLGD_SPECIFICATION_MATURITY_MATRIX / INDEPENDENT_VALIDATOR_NETWORK_PLAN / XLGD_AI_NATIVE_INTEGRATION_PLAN / XLGD_FUTURE_GOVERNANCE_EVOLUTION / XLGD_TECHNICAL_INFLUENCE_REGISTER / XLGD_12_MONTH_RESOURCE_ALLOCATION / 本文件。

## 五、必须由 Steven 拍板后才能动的（本阶段新增）

1. 三条 P0 是否开工（改仓库）；
2. 0.5.1 与 `verified_*` 拆分；
3. LGD-Eval 许可证定案；
4. `pypi` 环境加审批人；
5. 验证邀请发给谁（Zambo / SCITT 提问者 / agent-receipts）；
6. 主名称统一（XLGD / LGD / UIBC）；
7. 15 无证仓是否补 LICENSE；
8. 是否启动"付费审计"对话（含报价）。

> 诚实条款：本文所有等级来自本轮实测与前序五阶段证据；MARKET 为 PARTIAL 是因外部研究证实"需求存在"，但那不是"我们的客户"。
