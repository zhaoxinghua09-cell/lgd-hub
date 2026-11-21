# XLGD / LGD 战略审计档案 · 2026-11-21

> 这不是对外宣传材料，是一次**自我审**的完整留档：五个阶段、逐条证据、按 VERIFIED /
> PARTIALLY VERIFIED / NOT VERIFIED / INFERENCE 分档，**不把设计当实现、不把参与当采纳、
> 不把自评当独立验证**。凡结论与仓库现状不符，以仓库与可复跑脚本为准。

## 一、这份档案怎么用

| 你想知道 | 看哪一组 |
|---|---|
| 评测器到底可不可信、修了什么 | `01-runtime-and-evaluator` |
| 有哪些资产、许可证与 DX 现状 | `02-asset-and-lifecycle` |
| 规范能否被第三方独立实现 | `03-spec-and-adversarial` |
| 三年内可能怎么死、组合该怎么砍 | `04-premortem-and-portfolio` |
| 市场、定价、GTM、治理与品牌 | `05-market-and-organisation` |
| 基础设施地位、信任网络、可迁移性、资源配置 | `06-infrastructure-and-trust` |

## 二、分级口径（本档案的硬约定）

| 档 | 含义 |
|---|---|
| **VERIFIED** | 本机实测或公开可查数据支撑，含反例与失败样本 |
| **PARTIALLY VERIFIED** | 部分实测、部分依赖外部文献 |
| **NOT VERIFIED** | 设计/计划/推断，尚无运行证据 |
| **FAILED** | 实测证明我们自己的结论不成立（最该被保留的一档） |
| **INFERENCE** | 判断与推断，标注为判断 |

## 三、三处最不体面的结论（原样保留）

1. **评测器在修之前不可信**：凭证外发载荷拿 `100/A+`、`# skillgate: ignore` 一行注释即可关掉全部规则、
   载荷放 `demo/` 完全不扫描、空目录也能得 `67/C`。握有这四条，任何对外评分都是负债。
   → 已在 `01-runtime-and-evaluator/XLGD_HARDENING_EXECUTION_REPORT` 中给出前后对照，
   并落到仓库 PR（见文末）。
2. **证据层是唯一接近基础设施的一层**，其余（规范形式、互操作、多方治理）仍是「单实现 + 零外部使用」。
3. **外部验证者 = 0**，外部引用 = 0，唯一的外部痕迹是一次**分歧记录**（对方复跑得 0/9，我们 9/9），
   而不是背书。这一条写在 `06-infrastructure-and-trust/XLGD_TECHNICAL_INFLUENCE_REGISTER` 里，不能美化。

## 四、档案构成

| 组 | 文件数 | 目录 |
|---|---|---|
| `01-runtime-and-evaluator` | 3 | [01-runtime-and-evaluator/](./01-runtime-and-evaluator/) |
| `02-asset-and-lifecycle` | 5 | [02-asset-and-lifecycle/](./02-asset-and-lifecycle/) |
| `03-spec-and-adversarial` | 13 | [03-spec-and-adversarial/](./03-spec-and-adversarial/) |
| `04-premortem-and-portfolio` | 12 | [04-premortem-and-portfolio/](./04-premortem-and-portfolio/) |
| `05-market-and-organisation` | 14 | [05-market-and-organisation/](./05-market-and-organisation/) |
| `06-infrastructure-and-trust` | 14 | [06-infrastructure-and-trust/](./06-infrastructure-and-trust/) |

共 **61** 份文档。

## 五、复跑入口（任何人都能做）

```bash
# 证据（离线，不需要联网）
python tools/verify_rekor_inclusion.py --file samples/rekor_entry.json --log-key samples/log.pub
# 退出码：0 verified / 1 failed / 2 invalid input / 3 inconclusive（见 docs/EXIT-CODES.md）

# 评测器硬化前后对照（仓库内 7 个回归用例）
python -m pytest tests/test_safety_veto_hardening.py -q
```

## 六、对应的代码改动

| 仓库 | PR | 内容 |
|---|---|---|
| `zhaoxinghua09-cell/uibc-core` | #360 | 三值结论（缺依赖不得报 verified）+ `docs/EXIT-CODES.md`、`SPEC-MUST-INDEX`、`BUS_FACTOR`、`LICENSE-DECISION` |
| `LGD-Eval/LGD-Eval` | #19 | 四类绕过（凭证外发 / 注释豁免 / 夹具目录 / 空对象）+ 7 个回归用例 + `ALLOWLIST-AND-SCOPE` |

## 七、边界声明

- 本档案中的分数与等级是**自评**，不是认证、不是合规结论、不是监管批准；
- 涉及第三方产品的判断（如竞品替代性）标为判断，不构成对第三方的指控；
- 引用外部研究时给出链接；未给链接的结论按 INFERENCE 对待。
