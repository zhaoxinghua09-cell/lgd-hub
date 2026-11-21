# SPECIFICATION_ATTACK_REPORT（规范漏洞与歧义攻击 · 2026-11-21）

> 方法：不止读文档。本报告 **15 条**结论中，**13 条由本机实际运行复现**（`phase2_spec.py` 变体注入 + `phase2_probe2.py` 规则对抗），2 条为代码静态确认。原始输出：`phase2_spec_out.txt`、`phase2_probe2_out.txt`。
> 四档标注：V = 已复现；P = 部分复现；N = 不成立；I = 推断。

## A. UIBC 收据 / 校验语义（对 `verify_rekor_inclusion.py` 注入变体，固定 entry 2883389783）

| ID | 位置 | 触发条件 | 最小复现 | 预期 | 实际 | 影响 | 修复 | 兼容性 |
|---|---|---|---|---|---|---|---|---|
| SP-01 | 收据 schema | `logIndex` 为字符串 | `{"logIndex":"2883389783"}` | 拒绝或 `INCONCLUSIVE` | **`TypeError` 栈崩，exit 1，无结论**（V） | 任何类型漂移都变成崩溃而非判定 | 入口做类型校验，统一映射 `INCONCLUSIVE`/exit 2 | 不破坏 |
| SP-02 | 收据 schema | JSON 出现重复 key | `"logIndex": 2883389783, "logIndex": 1` | 拒绝重复 key | **静默取最后一个（entry.index=1），仍 `verified=True`**（V） | 签名方/校验方解析不一致可造分歧 | 用 `object_pairs_hook` 检测重复 | 严格化，可能拒旧输入 |
| SP-03 | 收据 schema | 缺 `integratedTime` | 删除该字段 | 拒绝（无时间不可判有效期） | **仍 `verified=True`，exit 0**（V） | 与"证据会过期"直接冲突 | 时间字段必需或返回 `INCONCLUSIVE` | 是（需版本化） |
| SP-04 | 收据 schema | 缺 `verification.signedEntryTimestamp` | 删除 SET | 至少 `signature_verified=false` | **仍 `verified=True`、`checkpoint.signature=True`**（V） | "作者签名未验"被读成"签名已验证" | 输出拆分 `verified_inclusion` / `verified_set` | 是（字段新增） |
| SP-05 | 索引语义 | `entry_log_index = -1` | 改成 -1 | 拒绝（不可能索引） | **`verified=True`、`entry.index=-1`**（V） | 收据可携带任意/伪造索引且不报错 | 校验 index 范围 + 与 proof 关系 | 不破坏 |
| SP-06 | logID 绑定 | logID 尾加零宽字符 `U+200B` | 追加零宽符 | 拒绝或警示 | **`verified=True`**（V） | 来源标识可被"看起来一样"地替换 | 规范化（NFC + 去零宽）后等值校验 | 是（Unicode 规范化） |
| SP-07 | 编码一致性 | root 改大写 hex | `.upper()` | 规范化后通过或明确拒绝 | **`verified=False`，exit 1，理由清晰**（V，行为正确） | — | 建议文档写明要求小写 | 否 |
| SP-08 | 输入健壮性 | `body = null` | 置 null | 明确错误码 | **`KeyError: 'body'` 栈崩**（V） | 异常输入不成结论 | 包 `try` 并映射退出码 | 不破坏 |
| SP-09 | 缺 proof | 删除 `verification.inclusionProof` | 删除 | 明确失败 | **exit 2，无结论输出**（V，行为可接受） | 但 exit 2 的语义未在文档定义 | 文档补退出码表 | 否 |
| SP-10 | 空 hashes | `inclusionProof.hashes=[]` | 置空 | 失败 | **`verified=False` exit 1**（V，正确） | — | — | — |
| SP-11 | 未知字段 | 顶层/`verification` 加未知字段 | 加 `x_extra` / `note` | 容忍（前向兼容） | **容忍且 `verified=True`**（V） | 需明确"未知字段不影响判定"，否则被当成可通过点 | 文档写明 forward-compat 策略 | 否 |
| SP-12 | 重放 | 同一收据跑两次 | 连续两次 | 一致 | **两次结果一致 `verified=True`**（V） | 校验本身无重放防护（离线校验可接受），但若用于"一次性凭证"则危险 | 文档写明"验证不等于消费" | 否 |
| SP-13 | 退出码语义 | 各类失败 | 见上 | 0/1/2 有定义 | **`0`=通过、`1`=不通过、`2`=缺 proof；但 `1` 同时混有崩溃**（V） | 调用方无法区分"验证失败"与"程序错误" | 崩溃统一为 2，并给 `error` 字段 | 是 |

## B. LGD-Eval 规则与评分（自建样本，`evaluate.py`）

| ID | 位置 | 触发条件 | 最小复现 | 预期 | 实际 | 影响 | 修复 | 兼容性 |
|---|---|---|---|---|---|---|---|---|
| SP-14 | `evaluate.py:613` 等 | 命中行尾加 `# skillgate: ignore` | `subprocess.run(c, shell=True)  # skillgate: ignore` | 只允许白名单场景，且留痕 | **100/A+、安全 25/25、0 安全命中**（V） | 一行注释即可关闭全部规则 | 取消注释式豁免；改基线白名单文件 + 理由必填 | 是 |
| SP-15 | `evaluate.py:568-573` | 代码放 `samples/`、`demo/`、`fixtures/`、`corpus/`、`benchmarks/` 等目录 | `samples/payload.py` 放凭证外发 | 仍应扫描或明确"不扫描" | **完全不扫描**（V，由 skip_dirs 决定） | 一条 `mkdir samples` 即可藏载荷 | skip 仅限仓库内测试夹具并校验来源；对外部技能一律扫描 | 是 |
| SP-16 | `SEC_RULES` R-SEC-03 | `shell=True` 经 dict 展开 | `KW={'shell':True}; subprocess.run(c, **KW)` | 命中 | **未命中 R-SEC-03**（V，安全维仅扣 6 分至 19/25） | 正则绕过后仍能 69/C 过 60 门槛 | AST 追踪 kwargs dict 展开 | 是 |
| SP-17 | 安全维整体 | `os.environ.get("GITHUB_TOKEN")` + `urllib.request.urlopen` | 见 `phase2_probe2.py` G2 | 命中凭证外发 | **100/A+、安全 25/25、零命中**（V） | 最危险的一类样本拿满分 | 新增数据流规则（env→网络） | 是 |
| SP-18 | 维度上限 | 单维最多扣满 25 | 多个 HIGH 叠加 | 任一 HIGH 触发上限 | **安全维扣满 25，总分 69/C，exit 0**（V） | 严重不安全仍可过默认门禁 | CRIT/HIGH 触发 veto（skillgate 已是双条件，主 CLI 不是） | 是 |

## C. 未在本次复现但代码可见（P）

| ID | 事实 | 依据 |
|---|---|---|
| SP-19 | `evaluate_skill` 返回 6 元组，4 个包装入口按 5 元组解包 → `ValueError` | 上一轮已复现（`B_dynamic.md`），本日未重跑 |
| SP-20 | `engine_version` 硬编码 `1.1.0`，SARIF 写 `1.0.0` | 代码静态确认 |

## D. 共性问题（比单条 bug 更重要）

1. **"通过"与"无法判定"没有分开**：崩溃、缺字段、类型错都被压成 exit 1 或直接 `verified=True`，调用方无法区分。
2. **默认放行的方向一致**：未知字段 → 放行；缺时间 → 放行；缺签名 → 放行；空目录 → 67/C；只有"路径不存在"才拒绝。
3. **规范文本没有定义退出码表与时序语义**：这直接导致独立实现必然分歧（见挑战文档 §六）。

## E. 建议的修订顺序（不改仓库，仅列）

1. 先定"七状态 + 退出码表"（0/1/2/3/4 → VERIFIED/FAILED/INCONCLUSIVE/EXPIRED/REVOKED），写进规范第一屏。
2. 再定"必需字段"清单（时间、SET、index 范围、logID 规范形式），缺一项即 `INCONCLUSIVE`。
3. 最后开规则修复（SP-14/15/16/17/18），并把这 5 条作为回归样本加入隐藏测试集。

> 诚实条款：SP-03/04/05/06 的"预期"是**我方判断**（I），规范原文未明确；因此这些不是"实现违反规范"，而是"规范未定义"。修复前不应把它们写成"对方实现错误"。
