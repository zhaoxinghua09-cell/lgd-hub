# XLGD_VERSIONING_AND_MIGRATION_POLICY（版本与迁移策略 · 2026-11-21）

> 现状（V）：**版本化是"半套"的** —— `uibc-core` 有语义化版本与 release（v0.4.0/0.4.1/0.5.0），`lgd-engine` 0.1.1，`synomos` 1.2.2；但 **12 个主线仓无版本文件**，`LGD-Eval` 的 `engine_version` 硬编码 `1.1.0` 而 SARIF 写 `1.0.0`，证据 JSON 里**没有版本字段**。

## 一、版本兼容矩阵（九类对象 × 现状）

| 对象 | 版本机制 | 兼容声明 | 现状判定 |
|---|---|---|---|
| UIBC 协议 | semver + release（0.5.0） | 有 conformance 语料 | **PARTIALLY**（0.5.0 与 0.4.x 行为差异未列 breaking 清单） |
| LGD 规则 | 规则 ID（R-SEC-xx） | 无规则版本号随输出 | **NOT VERIFIED**（`rule_version` 不进证据 JSON） |
| Evidence Schema | 无 schema 版本 | 无 | `PARTIALLY`（字段在变，但无 `schema` 字段） |
| Passport Schema | 无 | 无 | `NOT VERIFIED` |
| Registry Schema | 无实现 | 无 | `NOT VERIFIED` |
| API | 无独立 API 版本 | 无 | `NOT VERIFIED` |
| CLI | 参数稳定但退出码语义未定义 | 无 | `PARTIALLY` |
| JSON Output | 键随实现变（evaluation 键集已确认） | 无 | `PARTIALLY` |
| Test Fixtures | 6 条固定 SHA | 有 SHA256SUMS | **VERIFIED**（这一点做得好） |

## 二、六个关键问题（照指令回答）

**1. v0.1 → v0.2 老实现还能跑吗？**
现状无法回答：没有"契约测试"断言旧输入在新实现下的行为。建议：把 v0.1 收据纳入回归集，每次发版必跑（当前 1015 例测试覆盖的是代码，不是协议兼容）。

**2. 旧证据是否仍有效？**
**不能判定（N）**：证据无 `version`/`valid_until`，也无"哪个协议版本生成的"字段。这既是兼容问题也是生命周期问题（见 `EVIDENCE_LIFECYCLE_AUDIT.md`）。

**3. 老版本评测能否复现？**
**不能**：`engine_version` 硬编码且与 SARIF 不一致；没有 `evaluation_version`；规则变更不留版本。同一技能在不同时间跑出不同分数是必然的，且**无法解释差异**。

**4. Registry 能否同时存多版本？**
无 Registry 实现，谈不上。设计上必须支持"一个对象 × 多版本 × 每版本多条结果"（见 `TRUST_REGISTRY_GOVERNANCE.md`）。

**5. 新规则能否重评旧对象？**
技术上可以重跑，但**结果会覆盖历史**（无历史留存）。应改为"追加新结果 + 旧结果标 `SUPERSEDED`"。

**6. 能否识别不兼容变化？**
**不能**：无 schema 校验、无 breaking 变更检测。若某天 `verified` 字段删掉，消费方会静默失效。

## 三、五件必备物的写法（建议）

### 1) Version Compatibility Matrix（写进 README）
| 协议版本 | 支持对象 | 向后兼容 | 备注 |
|---|---|---|---|
| 0.5.x | 0.4.x 收据 | 是（只读兼容） | 0.5.0 起新增 checkpoint 签名校验 |

### 2) Breaking Change Policy
- 触发条件：字段删除、语义变更（如 `verified` 拆成两个字段）、退出码改变；
- 流程：先发 `-rc` → 保留一个版本的双写（新旧字段并存）→ 下个大版本移除旧字段；
- 每次 breaking 必须附"迁移脚本 + 迁移前后输出对比"。

### 3) Deprecation Policy
- 弃用字段保留 ≥1 个 minor 版本，并在输出里给 `deprecated: true` + `replacement`；
- 文档标注 `DEPRECATED since X.Y`。

### 4) Migration Guide
每条 breaking 一页：为什么改、怎么改、如何验证改对了（给一条命令 + 期望输出）。

### 5) 双向兼容测试
- **Backward**：旧输入（v0.4 收据）喂新实现 → 必须仍 `VERIFIED`；
- **Forward**：新输入喂旧实现 → 必须明确报"不支持"而非静默乱判。

## 四、必须补的三个字段（最小改动）

```json
{"schema": "lgd-verification-result/0.2", "protocol_version": "0.5.0",
 "evaluation_version": "1.1.0", "rule_version": "2026-11-r1",
 "subject": {"version": "0.5.0", "fingerprint": "sha256:..."}}
```

理由：没有这四项，**"同输入同结果"只在同一台机器同一时刻成立**（本日实测指纹稳定，但那是同一进程内的稳定性，不是版本稳定性）。

## 五、发布节奏建议

| 动作 | 频率 | 约束 |
|---|---|---|
| 功能发版 | ≤1 次/2 周 | 必须通过全量回归（1015 例） |
| 规则更新 | ≤1 次/月 | 必须带"旧样本复评差异表" |
| 协议变更 | ≤1 次/季度 | 必须附兼容矩阵与迁移指南 |

## 六、验收判据

1. 任一输出可读出 `protocol_version` + `evaluation_version` + `rule_version`；
2. 存在一条 **v0.4 收据 → 0.5.x 实现** 的回归用例（当前可做，成本半天）；
3. 任一 breaking 变更都有迁移脚本与前后对比；
4. 旧结果不被覆盖，只被标 `SUPERSEDED`。

> 诚实条款：本节内容为设计（TESTED 级）；当前实际兼容性测试覆盖为 0，"0.1→0.2 老实现能否运行"这一问**无法回答**（N）。
