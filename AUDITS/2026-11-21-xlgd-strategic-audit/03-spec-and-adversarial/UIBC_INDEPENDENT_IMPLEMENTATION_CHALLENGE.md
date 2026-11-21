# UIBC_INDEPENDENT_IMPLEMENTATION_CHALLENGE（独立实现挑战 · 设计稿 · 2026-11-21）

> 状态：**挑战已设计，尚未发出；外部独立实现数 = 0（VERIFIED）。**
> 因此从现在到第一个外部实现跑通之前，**不得对外描述"已形成可独立实现的生态"**。本文给出挑战的全部要素，供发起时直接使用。

## 一、挑战要解决什么

现在"能不能第三方实现"这件事**没有证据**：唯一被称作"第二实现"的 `uibc-iverify` 与 `uibc-core` 同作者（VERIFIED，见 `SINGLE_MAINTAINER_RISK_AUDIT.md`）。所以挑战的目标不是宣传，而是**证伪**——证明"仅凭公开规范能否写出结果一致的实现"。

## 二、我们发什么 / 不发什么

**发（公开、固定 SHA）**
- `uibc-core` 的规范文本（`SPEC` / `conformance` 文档）；
- 公共测试向量（JSON）+ 每条的期望结果与退出码；
- 正向集 / 负向集 / 边界集（数量见下表）；
- 机器可读结果格式（`uibc-challenge-result/0.1`）。

**不发**
- 作者实现的任何源码（含 `verify_rekor_inclusion.py`、`independent_verifier/`）；
- 任何提示性片段、内部注释、调试输出。

**判据**：如果挑战包解压后能直接跑出答案，说明我们发多了；如果解压后连"从哪开始"都不知道，说明规范不足——两者都是挑战的失败模式。

## 三、向量集设计（当前可用素材已点清）

| 集 | 数量（现有） | 内容 | 期望 |
|---|---|---|---|
| 正向 | 7（kit `samples/`） | 真 Rekor 收据、跨索引折叠、一致性前缀 | 全部 `VERIFIED`，exit 0 |
| 负向 | 6（kit + 历史负面结果） | 篡改 inclusion、篡改 root、篡改签名、缺 inclusionProof、非法 JSON、错 first root | 全部 `FAILED` 或明确 `INCONCLUSIVE`，exit 1/2 |
| 边界 | 待补 ≥8 | 空 hashes、大写 hex、字符串型 index、负 index、零宽字符 logID、重复 JSON key、缺 timestamp、缺 SET | 见 §六"已知歧义"，须先定语义 |

> 边界集是本次新增的**关键**：本日实测（`SPECIFICATION_ATTACK_REPORT.md` S4/S5/S10/S13）显示这些输入当前行为不一致——**挑战必须在这些语义定稿后才能发**，否则第三方实现必然与我们对不上，反而制造分歧。

## 四、结果格式（第三方只填这个，不填别的）

```json
{
  "schema": "uibc-challenge-result/0.1",
  "implementation": {"name": "…", "language": "…", "repo": "…", "commit": "…"},
  "vectors": [
    {"id": "POS-01", "expected": "VERIFIED", "actual": "VERIFIED", "match": true, "ms": 12},
    {"id": "NEG-04", "expected": "FAILED", "actual": "FAILED", "match": true},
    {"id": "BND-03", "expected": "INCONCLUSIVE", "actual": "VERIFIED", "match": false,
     "note": "把 entry_log_index 当校验条件，与本规范 §语义不符"}
  ],
  "summary": {"total": 21, "matched": 19, "mismatched": 2, "conformance": 0.905},
  "differences": ["字符串型 logIndex：我方抛 TypeError，对方返回 FAILED"],
  "spec_issues": [{"vector": "BND-03", "issue": "规范未规定 entry_log_index 是否必须校验", "proposal": "…"}]
}
```

## 五、验收标准（照指令 §15 逐条落地）

| 指令要求 | 判据 | 当前 |
|---|---|---|
| 至少一个独立实现能启动 | 外部人 clone 后 N 分钟内跑出一条结果 | ✗（0 个） |
| 不依赖作者私有代码 | 挑战包内无作者源码（`sha256sum -c` 校验包内文件清单） | 设计满足 |
| 通过公开一致性测试 | 正向集 7/7 match | 待外部跑 |
| 失败于指定负向测试 | 负向集 6/6 不 match=失败 | 待外部跑 |
| 输出机器可读结果 | 符合 §四 schema | 设计满足 |

**只有五项全绿，才能写"可独立实现"。少一项就只能写"规范已公开，挑战进行中"。**

## 六、已知歧义（挑战前必须先定，否则会误伤第三方）

1. `entry_log_index` 为负值仍判 `verified=True`（S13）——是否应 `INCONCLUSIVE`？
2. 缺 `integratedTime` / 缺 `signedEntryTimestamp` 仍 `verified=True`（S6/S7）——时间与作者签名是否属于必需字段？
3. 重复 JSON key 静默取后者（S5）——是否应拒绝？
4. 字符串型 `logIndex` 抛 `TypeError` 栈（S4）——应统一为 `INCONCLUSIVE` + exit 2。
5. `logID` 含零宽字符仍通过（S10）——logID 是否需要与 checkpoint origin 做等值校验？

## 七、发起方式（不自动执行，需批准）

- 渠道优先级：① IETF SCITT 列表（已有 1 帖、零回复，成本最低）；② `agent-receipts` 维护者；③ AER-1 作者（已有公开分歧记录，最适合做第一个外部实现）；④ W3C `public-agentprotocol`（已有 1 条他人回复）。
- 一次性发出内容：挑战包 zip + 一页 README + 结果格式 + "允许发布失败结论"的声明。
- **所有对外发送必须先经 Steven 批准**；本文件不代表已发出。

## 八、诚实条款

- 挑战设计本身是 `TESTED` 级（作者自测 6/6 落预期），不是 `VERIFIED`。
- 若 30 天内无外部实现启动，结论应写成"规范可读性不足或激励不足"，而不是"第三方不愿参与"——前者可修，后者不可辩。
