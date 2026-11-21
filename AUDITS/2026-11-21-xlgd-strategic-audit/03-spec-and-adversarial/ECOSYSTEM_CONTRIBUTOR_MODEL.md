# ECOSYSTEM_CONTRIBUTOR_MODEL（贡献者价值机制 · 2026-11-21）

> 现实起点（V）：目前外部人类贡献者 **0**，star 12/9/7/5/3/1。所以本文件不是"社区运营方案"，而是**最低成本的"第一步可参与"设计**——让一个人能在 15–60 分钟内做完一件被看见的事。

## 一、九类角色 × 门槛 × 得到什么

| 角色 | 做什么 | 门槛 | 可获得的记录 | 明确得不到 |
|---|---|---|---|---|
| Failure Contributor | 提交一条失败案例（现象+复现） | 极低（0.5 h） | `SF-xxx` 编号署名 | 任何"认证" |
| Test Vector Contributor | 提交一条测试向量 + 期望结果 | 低 | 向量 ID 署名 | 分数加成 |
| Independent Verifier | 按 kit 跑一遍并签名发布 | 低（15 min） | 验证者身份 + 结果签名 | 作者身份 |
| Protocol Implementer | 写第二实现 | 高 | 实现者署名 + 兼容性报告 | 自动"官方实现" |
| Adapter Developer | 接一个新平台 | 中 | 适配器清单署名 | 官方背书 |
| Evaluator | 对某对象出评测结论 | 中 | 评测记录 | 结论免审 |
| Research Contributor | 写分析/攻击报告 | 中 | 引用条目 | 结论采纳权 |
| Documentation Contributor | 翻译/补 FAQ | 极低 | 文档贡献记录 | — |
| Integration Partner | 在产品里接入 | 高 | 合作伙伴条目 | 商业授权（需另签） |

## 二、贡献记录的机器格式（`contribution-record/0.1`）

```json
{
  "schema": "contribution-record/0.1",
  "contributor": {"handle": "@x", "identity_proof": "github-org|key|orcid"},
  "type": "failure|vector|verification|implementation|adapter|evaluation|research|doc",
  "artifact": {"id": "SF-017", "sha256": "…", "url": "…"},
  "signed": {"alg": "ed25519", "sig": "…"},
  "coi": {"affiliated_with_author": false},
  "ts": "2026-11-21T…Z"
}
```

用途：可被引用、可被第三方校验、可被未来换算法重算。**不是积分系统，不产生排名。**

## 三、四条禁止（照指令原文，必须写进 CONTRIBUTING）

1. **贡献 ≠ 认证**：任何贡献记录不得渲染成 PASS/等级。
2. **不得以数量换 PASS**：评测结论与贡献数无关，规则里不得出现"贡献加分"。
3. **不得把贡献者身份当验证结果**：`contributor` 与 `verifier` 是两个字段，不能互相替代。
4. **作者关联者不算独立验证者**：`coi.affiliated_with_author=true` 时，`verdict` 最高只能到 `TESTED`（与 SPEC §3 一致）。

## 四、为什么现在没人来（诚实的四个原因）

1. **没有"下一步做什么"**：README 说"这是什么"，没说"你可以做哪件小事"；
2. **没有可见回报**：没有署名位置、没有被引用入口；
3. **门槛被隐藏**：跑测试要先修 Windows PATH（V）、评测入口会崩（P1-1）；
4. **风险不对称**：贡献者担心"我的样本被用来证明产品好"，缺少"允许发布负面结论"的明确承诺（kit 已有，但未广而告之）。

## 五、三件立刻可做的事

| 动作 | 成本 | 判据 |
|---|---|---|
| 在每个核心仓 README 顶部加 `Good first issue` 三件（提交 1 条失败案例 / 跑 1 次 kit / 翻译 1 页） | 0.5 h | 出现第一条外部 PR |
| `silent-failure-catalog` 开"提交案例"模板（含 SHA、期望、为什么难） | 1 h | 收到第一条外部案例 |
| 公开"验证者名单"页（可匿名，只要签名） | 1 h | 名单出现第 1 个非作者条目 |

## 六、验收判据

- 30 天内出现 **≥1 条外部 contribution-record**（任意类型）；
- 该记录能被第三方用 `sha256` 校验；
- 该记录**没有被换算成任何分数或等级**（这是"没走偏"的判据）。
