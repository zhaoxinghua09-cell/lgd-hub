# XLGD_IDENTITY_AND_BRAND_ARCHITECTURE（身份与品牌分层架构 · 2026-11-21）

> 目标：**让"作者是谁 / 生态是什么 / 产品卖什么"三层清楚，且不制造任何未经证实的机构背书。**

## 一、三层结构

### Layer 1 · Personal Authority（个人学术/技术身份）
| 标识 | 用途 | 现状（V） |
|---|---|---|
| Steven Zhao / Xinghua Zhao | 对外署名、会议、邮件 | 使用中 |
| ORCID `0009-0001-0512-1237` | 论文/技术作品索引 | **已索引多篇作品**（V） |
| GitHub `zhaoxinghua09-cell`（主理论/协议）、`stevenzhao07`（产品）、`LGD-Eval`（评测）、`StevenZhao2023`（历史） | 分工 | **4 个身份同属一人**（V，contributors 实查） |
| LinkedIn / 个人站 | 职业身份 | 未核实一致性 |

### Layer 2 · Ecosystem Identity（生态/协议）
| 名称 | 定位 | 当前问题 |
|---|---|---|
| **XLGD** | 生态总称（建议唯一主名） | 与 LGD 并存，边界模糊 |
| **LGD** | 理论/品牌前缀 | 与 XLGD 混用 |
| **UIBC** | 协议名（证据/生命周期） | 名字与"Core"混用 |
| **LGD-Eval** | 评测工具 | 同时是账号名、仓库名、产品名 |
| **SynomosAI** | 治理 MCP 服务器 | 与"AI"后缀易与公司混淆 |

### Layer 3 · Product Identity（可售物）
| 名称 | 客户看到的是什么 | 现状 |
|---|---|---|
| MCP Trust Audit | 一次只读审计 + 证据包 | 建议的唯一产品名 |
| Governance MCP | 一个 MCP 服务器 | 已有 |
| MedXpert | 医械合规品牌 | 已有（独立线） |
| Enterprise Services | 企业服务 | 未定义 |

## 二、四个必须修的关系

| 问题 | 风险 | 建议 |
|---|---|---|
| 4 个 GitHub 账号同属一人 | 外部误认为"多个组织/多个团队"；也让"独立验证"显得可疑 | README 明确"同一作者的不同职能账号" |
| XLGD / LGD 混用 | AI 检索时分裂；品牌无积累 | 定一个主名，另一个标"历史/别名" |
| LGD-Eval 一号多义（账号/仓库/产品） | 引用混乱 | 产品名与仓库名分离（如产品叫 Trust Audit） |
| 未定义"机构关系" | 容易被读成"有机构背书" | 所有页面写明"独立研究者/个人项目，无机构背书" |

## 三、对外表述的统一口径（可直接用）

```
Author: Xinghua (Steven) Zhao, independent researcher (ORCID 0009-0001-0512-1237).
Ecosystem: XLGD — an evidence-first trust infrastructure project. Not affiliated with any
standards body, university or vendor. Participation in ITU/W3C/IETF mailing lists does not
constitute endorsement or adoption.
Accounts: multiple GitHub accounts are roles of the same author, not separate teams.
```

**禁止**：`我们与 XX 大学合作`（无证据）、`某标准组织成员`（无成员身份）、`被 XX 采纳`。

## 四、一致性地基检查清单（每季度一次）

| 检查 | 判据 |
|---|---|
| GitHub 简介 | 四个账号互相指向 + 写明"same author" |
| ORCID | 作品列表含核心仓/论文；单位字段准确 |
| 项目官网/Pages | 一处 canonical URL；写明非机构背书 |
| 论文/技术文档 | 作者名一致（Xinghua Zhao 优先） |
| 社交平台 | 不做"官方账号"暗示（除非真为组织） |

## 五、品牌与商业的分层规则

1. 生态名（XLGD）**不出现在报价单**上作为"认证"；
2. 产品名（MCP Trust Audit）可以商业化，但必须带"advisory only"；
3. 个人名（Steven Zhao）用于署名与研究，不用于背书产品；
4. 医械品牌（MedXpert）与信任基础设施**分开叙事**，避免"卖器械又卖认证"的利益冲突观感。

## 六、验收判据

- 任一外部页面能在 30 秒内回答"这是谁的项目、有没有机构背书、账号为什么有四个"；
- 不存在"标准组织成员/合作机构"的无据表述；
- 生态名与产品名在 10 个页面内一致。
