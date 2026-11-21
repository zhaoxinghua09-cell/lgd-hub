# XLGD_SERVICE_QUALITY_MODEL（生态服务质量与客户信任指标 · 2026-11-21）

> 铁律：**没有测量过的指标不得对外宣传为服务水平。** 本文件把 10 个指标分成四类：已测量 / 无数据 / 仅部署后可得 / 不能承诺。

## 一、十项指标现状

| # | 指标 | 现状 | 数值（实测） | 分类 |
|---|---|---|---|---|
| 1 | **Availability** | 无托管服务 | 不适用（只有 PyPI/GitHub Pages 依赖上游） | 不能承诺 |
| 2 | **Evaluation Latency** | 已测 | 单技能评测 ~0.2–1 s（本机 11 例均秒级）；1015 测试 159 s | 已测量 |
| 3 | **Reproducibility** | 已测 | 同输入同指纹（3 次一致）；跨路径稳定 | 已测量（单机） |
| 4 | **False Positive Rate** | 仅计数 | 6 例样本：0 误报 | 计数，不作百分比 |
| 5 | **False Negative Rate** | 仅计数 | 6 例样本：2 漏报（凭证外发、SSH 写入）；另 G2/G4 为"更严重漏报" | 计数 |
| 6 | **Evidence Completeness** | 部分 | 有 SHA/命令/环境；缺 verifier、缺时间戳、缺有效期 | 无数据（字段缺失） |
| 7 | **Report Quality** | 主观 | 有 detail/why_not；无标准化"能/不能"段落 | 无数据 |
| 8 | **Support Response Time** | 无渠道 | 0 | 不能承诺 |
| 9 | **Version Compatibility** | 未测 | 兼容测试覆盖 0（0.4 收据未回归） | 无数据 |
| 10 | **Incident Resolution** | 未启动 | 见事件响应文件（False PASS 目前是未关闭事件） | 无数据 |

## 二、四个分类的用法

### 已测量（可对外，但必须带条件）
- `Evaluation Latency: sub-second per skill (local, single machine, no sandbox).`
- `Reproducibility: identical fingerprint on repeated runs of the same input (single machine).`

### 无数据（禁止对外）
- 误报率/漏报率（只有 6 例计数，写"2/6 漏报"而不是"33%"）；
- 证据完整性、报告质量、版本兼容。

### 仅企业部署后可得
- Availability（客户环境）、Incident Resolution（有事件才知道）、Support Response（有客户才知道）。

### 不能承诺（永远不说）
- `99.9% uptime`、`SLA`、`认证级`、`零误报`。

## 三、对外措辞模板（客户可直接引用）

```
Measured: per-item latency (sub-second), reproducibility (same input → same fingerprint),
coverage (1 of 8 risk classes verified, 1 failed, 2 partial, 4 not tested).
Not measured: availability, false-positive/negative rates at scale, support response.
Not promised: SLA, certification, "zero misses".
```

## 四、服务质量的责任边界

| 事项 | 我们负责 | 客户负责 |
|---|---|---|
| 报告所述事实（可复核） | ✅ | — |
| 发现项的修复建议 | ✅（建议，不代修） | 执行 |
| 未覆盖类别的漏检 | ❌（已在"不能验"里明示） | 自评 |
| 上线决策后果 | ❌ | ✅ |
| 运行时行为 | ❌（不做沙箱） | ✅ |

## 五、三个必须建立的测量（90 天内）

1. **5 分钟跑通率**（陌生人首次运行成功比例）——当前未测，这是最影响采用的指标；
2. **跨环境复现率**（≥2 台机器/2 个运行时跑同一 kit）——当前只有 1 台；
3. **每类风险的漏报计数**（用固定样本集，报计数不报比例）。

## 六、诚实条款

- 本文件的最大价值是"列出没有数据的东西"，而不是列出漂亮的数字；
- 当前对外可说的只有两句（延迟、可复现），且都必须附"单机、无沙箱"。
