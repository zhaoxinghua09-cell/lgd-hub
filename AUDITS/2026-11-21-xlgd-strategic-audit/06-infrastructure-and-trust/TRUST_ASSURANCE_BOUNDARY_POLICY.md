# TRUST_ASSURANCE_BOUNDARY_POLICY（信任结果的责任边界政策 · 2026-11-21）

> 一句话：**本生态输出的是"技术事实与建议"，不是安全保证、不是认证、不是监管批准。**
> 本文把七种结果与六种误读逐一钉死，并给出可直接贴在报告首页的措辞。

## 一、七种结果的边界

| 结果类型 | 我们提供的是什么 | 谁负责 | 不得表述为 |
|---|---|---|---|
| Technical Assessment（技术评估） | 事实清单（字段、权限、命中项） | 我们（限事实准确） | "安全评估通过" |
| Security Testing（安全测试） | 规则扫描结果（含明确覆盖缺口） | 我们（限已声明范围） | "无漏洞" |
| Independent Verification（独立验证） | 对**证据完整性/来源**的复核 | 验证者 | "内容真实" |
| Governance Recommendation（治理建议） | 建议与限制项 | 客户 | "合规结论" |
| Human Approval（人工批准） | 无（由客户的人做） | 客户 | "我们批准" |
| Legal Certification（法律认证） | **不提供** | 认证机构 | "认证" |
| Regulatory Approval（监管批准） | **不提供** | 监管机构 | "已获批/可用于注册" |

## 二、六种误读 × 反制措辞

| 误读 | 反制措辞（放报告首页） |
|---|---|
| PASS = 绝对安全 | `A pass means "no finding within the declared scope". It does not mean the subject is safe.` |
| A+ = 可无条件部署 | `The score is EXPERIMENTAL. Do not deploy on the strength of a grade.` |
| Identity Verified = 行为可信 | `Identity attests the binding between a key and an identifier, not the behaviour of the holder.` |
| Evidence Verified = 内容真实 | `Integrity binds bytes to a key. It does not make the bytes accurate.` |
| Registry Listed = 官方认可 | `Listing is a record, not an endorsement.` |
| LGD 结果 = 法定认证 | `Our outputs are not certification, not legal advice, and not regulatory approval.` |

## 三、必须写进每个输出的三句话（机器可读）

```json
{
  "assurance": {
    "scope": "integrity|behaviour|identity",
    "advisory_only": true,
    "not_certification": true,
    "risk_owner": "deploying_party",
    "coverage_gaps_declared": true
  }
}
```

## 四、责任分配的四个边界

| 边界 | 我们 | 客户 |
|---|---|---|
| 报告所述事实 | ✅ 准确（发现错误免费更正） | — |
| 未覆盖类别的漏检 | ❌ 已明示"未测" | ✅ 自评 |
| 上线决策 | ❌ | ✅ **风险自担** |
| 运行时行为 | ❌（不做动态利用） | ✅ |

## 五、对三类特殊对象的额外限制

| 对象 | 限制 |
|---|---|
| 医械/受监管 Agent | **不得**用于注册申报的"符合性证据"，除非监管方明确接受；只能作"内部审查辅助" |
| 客户生产系统 | 只读，不做主动利用；不触碰真实凭证 |
| 第三方产品 | 触达漏洞须走协调披露（CVD），不公开细节 |

## 六、违约句式（内部禁用清单）

- ❌ "经我们认证" / "符合 XX 标准" / "通过合规审查"
- ❌ "安全可信" / "零风险" / "绝对安全"
- ❌ "可用于 FDA/NMPA 申报"
- ✅ "在我们声明的检查范围内未发现 X"；"以下类别未测试"；"建议人工复核"

## 七、验收判据

1. 每个输出可解析 `assurance` 块；
2. 报告首页含"范围 + 未测类别 + advisory"三段；
3. 销售材料零禁用句式（逐份检查）；
4. 客户合同中写明"风险由部署方承担"。

> 诚实条款：本政策是文本约束（TESTED 级），**没有任何代码强制**；一旦有人绕过，只能靠评审发现。
