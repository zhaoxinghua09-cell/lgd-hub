# XLGD_ECOSYSTEM_GOVERNANCE_MODEL（生态合作治理模型 · 2026-11-21）

> 两条不可让渡的规则（指令明确要求）：
> 1. **核心维护者身份不自动赋予独立验证资格**；
> 2. **商业合作不得影响技术评测结论**。

## 一、七个角色 × 权限

| 角色 | 能做什么 | 不能做什么 | 独立性判定 |
|---|---|---|---|
| **Core Maintainer** | 合并、发版、改规范 | 不能自签"独立验证" | 与作者同主体 → 验证结论最高 `TESTED` |
| **Protocol Implementer** | 写第二实现、提交兼容报告 | 不能改规范、不能给"官方"背书 | 与作者无雇佣关系才算外部 |
| **Independent Verifier** | 签名发布验证结果（含 FAIL） | 不能参与被验对象的开发 | COI 必须声明；`affiliated=false` |
| **Security Researcher** | 报漏洞、写攻击报告 | 披露前须协调（CVD） | 可匿名 |
| **Test Contributor** | 提交向量/失败案例 | 不能以贡献换 PASS | 贡献≠认证 |
| **Integration Partner** | 在产品中接入 | 不能影响评测结论 | 商业关系必须公开 |
| **Commercial Partner** | 代交付、分成 | 不能改规则、不能决定 verdict | 与评测隔离 |

## 二、决策流程（三类决定）

| 决定类型 | 谁定 | 流程 |
|---|---|---|
| 技术/协议变更（breaking） | Core Maintainer（现为 Steven） | 提案 → 兼容矩阵 → 迁移指南 → 发版 |
| **评测规则变更** | 规则 owner（现为 Steven） + **变更前后差异表必须公开** | 提案 → 旧样本复评 → 发布差异 → 生效 |
| 验证结果 | **验证者本人**（签名） | 作者无权删改，只能回应/争议 |

**关键约束**：规则变更若影响"谁能通过"，必须公布"哪些旧结论会翻转"——否则等于偷改裁判。

## 三、利益冲突（COI）与署名

- 每个角色登记：`identity`（可匿名/假名）、`affiliation`、`coi_declared`；
- `affiliated_with_author=true` → 验证结果最高 `TESTED`（与 `INDEPENDENT_VERIFICATION_SPEC.md` 一致）；
- 署名可撤回；撤回后记录保留但标 `withdrawn`。

## 四、退出与继承（当前最缺的一段）

| 事项 | 现状 | 必须补 |
|---|---|---|
| Maintainer 退出 | 无规则 | 交接清单：密钥、仓库权限、发布权、域名、文档 |
| 验证者退出 | 无规则 | 历史签名仍有效；新结果不再接受 |
| 商业伙伴退出 | 无合同模板 | 终止条款 + 已交付结果的存续 |
| 作者不可用 | **无预案**（Bus Factor=1） | 指定 emergency contact + 只读托管说明 |

## 五、双人规则（最小可行治理）

当有第 2 名 Core Maintainer 时立即生效：
1. 主分支需 1 人评审（当前 0 人）；
2. 发布需 1 人批准（当前 `pypi` 环境无审批人）；
3. 任何人都不能单独签署"独立验证"。

## 六、验收判据

- 存在 `GOVERNANCE.md`，写明上述 7 角色与 3 类决定；
- 任一验证结果能读到 `coi.affiliated_with_author`；
- 商业合同里写明"不影响技术结论"；
- 有一个具名的 emergency contact。

> 诚实条款：以上全部为设计（TESTED 级文档），当前**无任何治理文件**，7 个角色中只有"Core Maintainer"实际存在（1 人）。
