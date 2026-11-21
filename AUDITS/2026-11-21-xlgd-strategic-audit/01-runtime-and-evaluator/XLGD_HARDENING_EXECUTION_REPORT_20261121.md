# XLGD 硬化执行报告 · 2026-11-21（第 6 批：按建议落地）

> 指令：`全部按照你的建议 做到最好`。
> 执行边界（本轮自设，与既有纪律一致）：**本机克隆内改代码 + 跑证据 + 出对照数据**；推送/打 tag/发 PyPI/对外联系**一律未做**，只给出可一键执行的清单等批准。
> 所有"已修"都有前后实测数字；所有"未做"都写在第 5 节，不拿设计当实现。

---

## 1. 一句话结果

Phase V 指出的 Evaluation 成熟度 **D+**，本轮用 4 个补丁把它拉回到"恶意载荷拿不到高分"：
**凭证外发样本 86/A → 49/D（否决）**，**空对象不再有分数（exit 2）**，**正常用法零回归（86/A → 86/A）**；
uibc 的 **fail-open（缺依赖时 verified=True / exit 0）已修成 exit 3（inconclusive）**，全量测试 **1247 passed**。

---

## 2. 改了什么（LGD-Eval，4 个补丁）

| # | 漏洞（本轮之前的实测） | 修法 | 结果 |
|---|---|---|---|
| F1 | 读 `GITHUB_TOKEN`/`OPENAI_API_KEY` 后 POST 陌生主机 = **100/A+，安全 25/25** | 单项凭证环境变量纳入污点源；文件内出现陌生主机 → critical 否决 | **49/D** |
| F2 | 一行 `# skillgate: ignore` 关掉全部规则 = **100/A+** | 无备案豁免失效；改为 `.lgd/allowlist.json`（rule+file+行内容 sha256+reason+reviewer）；**CRITICAL 永不豁免**；未备案豁免注释本身计为发现 | **62/C**；带真实外发的伪豁免 **49/D** |
| F3 | 载荷放 `demo/`、`samples/`、`benchmarks/` 完全不扫 | 只跳过工具/缓存目录；夹具目录须 `.lgd/scope.json` 显式声明（并记入报告） | **49/D** |
| F4 | 空目录 **67/C**、仅 SKILL.md **87/A** | 缺 SKILL.md → `INVALID_SUBJECT exit 2`；无可执行面 → `INCONCLUSIVE exit 2` | **exit 2** |

**防误报**：新增"常规服务端点"分级——读自己的 API key 发给 `api.openai.com` 不扣分，只登记并封顶 A。
实测正常用法 **86/A → 86/A**，干净基线 **86/A → 86/A**。

**一致性**：`vendor/scripts/` 与 `skills/lgd-eval/scripts/` 双副本同步，`tests/test_copy_parity.py` → `OK: 12 个同名脚本，0 个未登记分叉`；`pytest tests` → **4 passed**。

---

## 3. 改了什么（uibc-core，1 个行为修正 + 契约修正）

| 项 | 旧 | 新 |
|---|---|---|
| 缺 `cryptography` | `verified=True` / `exit 0` | `verified=false` / `conclusion=inconclusive` / **`exit 3`** |
| 有 `cryptography` 50.0.2 | `verified=True` / `exit 0` | 不变 |
| 测试契约 | 3 处断言写死 `verified is True`（把 fail-open 固化） | 改为断言 `inconclusive` + `exit 3` |
| 全量测试 | — | **1247 passed / 26 skipped / 87 subtests（213s）** |

同一份 `rekor_entry_2883389783.json`，两个 venv 下跑出的差异就是证据（不是描述）。

---

## 4. 新增文档（4 份，全部落在工作副本里，可审）

| 文件 | 作用 |
|---|---|
| `uibc-core/docs/EXIT-CODES.md` | 统一退出码：`0` 只允许出现在"检查真的执行过"；`3` = 无法判定 |
| `uibc-core/docs/SPEC-MUST-INDEX.md` | `docs/*.md` 中含 MUST 的 20 行 → 16 条编号为条款（`MUST-01…16`），4 条标为引用/评论；映射列留空即 **untested** |
| `uibc-core/docs/BUS_FACTOR.md` | 六维全 1 实测 + 接手 1 天路径（可复制执行）+ 30 天 4 项补漏 |
| `uibc-core/docs/LICENSE-DECISION.md` | 分层定案建议：代码 Apache-2.0 / 文本 CC BY 4.0 / 向量 CC0；改证需逐项批准 |
| `uibc-core/docs/RELEASE-NOTES-0.5.1.md`、`LGD-Eval/docs/RELEASE-NOTES-0.6.0.md` | 发布说明草稿（含对下游的破坏性影响说明） |

---

## 5. 明确没做的（需要你点头）

1. **未推送、未打 tag、未发 PyPI**（`pypi` 环境仍 `protection_rules=[]`）。
2. **未改许可证**：LGD-Eval 仍是 CC BY 4.0；改证影响已发布版本授权，按 `LICENSE-DECISION.md` 逐项批准。
3. **未给 15 个无证仓补 LICENSE**：需先判断对象类型（代码/文本/向量）。
4. **未对外联系任何人**（验证邀请、客户、咨询机构都没发）。
5. **未改 CHANGELOG.md 正文**（uibc 那份 86KB 长文，合并方式需定；改用独立 RELEASE-NOTES）。
6. **未动其余 4 处 `verified=True` 语义**（`benchmark/adapter.py` 等），需逐个评估。
7. **评分权重/分档未动**：仍标 EXPERIMENTAL。本轮只让"否决"生效，不假装权威。

---

## 6. 你批准后的一键执行清单

```powershell
# 0) 先看 diff（3 个补丁文件，共 22.8 KB）
#    patches\01_lgd_eval_hardening.diff / 02_uibc_three_valued_verdict.diff / 03_uibc_tests.diff

# 1) uibc-core：推分支 + 提 PR（不直推 main）
cd <local-work>\uibc-core
git init -b fix/three-valued-verdict ; git add -A ; git commit -m "fix: 缺失依赖时不得报 verified（三值结论 + exit 3）"
git remote add origin https://github.com/zhaoxinghua09-cell/uibc-core.git
git push -u origin fix/three-valued-verdict

# 2) LGD-Eval：同样走分支
cd <local-work>\LGD-Eval
git init -b fix/safety-veto-hardening ; git add -A ; git commit -m "fix(eval): 凭证外发/豁免注释/夹具目录/空对象 四类绕过"
git remote add origin https://github.com/zhaoxinghua09-cell/LGD-Eval.git
git push -u origin fix/safety-veto-hardening

# 3) 发版前必须先做的两道门（否则不要 tag）
#    a. pypi 环境加审批人：gh api -X PUT repos/zhaoxinghua09-cell/uibc-core/environments/pypi \
#         --input '{"reviewers":[{"type":"User","id":<你的 user id>}]}'   ← 需你确认是否执行
#    b. 分支保护要求 1 个 approving review
```

> 提醒：`<local-work>\*` 是从审计克隆复制的**无 .git 副本**，所以上面用 `git init`；这也意味着
> 提交历史不会继承原仓，正式提 PR 前建议改为在原仓分支上打补丁（我可以按你选的路径再做一次）。

---

## 7. 复跑方式（任何人都能做）

```powershell
cd <project-dir>
python verify_hardening.py                 # 前后对照表（9+1 个样本）
python patch_lgd_eval.py                    # F1–F4 补丁（幂等性：片段已被改过会报 MISS 并中止）
python patch2_lgd_eval.py ; python patch3_lgd_eval.py
python patch_uibc_verdict.py                # 三值结论
python gen_must_index.py                    # MUST 索引
```

---

## 8. 结论档位（本报告自身）

| 声明 | 档 | 依据 |
|---|---|---|
| 恶意载荷不再拿 A+/A | **VERIFIED** | 对照实验 + 4 次独立复跑 |
| 正常用法不回归 | **VERIFIED** | legit_api_key 86/A 不变 |
| 缺依赖不再 fail-open | **VERIFIED** | 两个 venv 实测 exit 0 vs 3 |
| 全量测试通过 | **VERIFIED** | 1247 passed（213s） |
| 评分现在"可信" | **NOT VERIFIED** | 权重/阈值未变，仍 EXPERIMENTAL；只保证"已知高危不再被稀释" |
| 可发布 | **NOT VERIFIED** | 未推送/未过评审/未加审批人 |

---

**消耗画像**：子代理 0 / 工具调用约 24 次 / 时长约 35 分钟 / 类型：文件写(13)、PowerShell 只读与执行(9)、pytest 后台(1)、diff 生成(1)。新增代码 3 个补丁脚本 + 2 个验证脚本，新增文档 6 份，补丁 22.8 KB。
