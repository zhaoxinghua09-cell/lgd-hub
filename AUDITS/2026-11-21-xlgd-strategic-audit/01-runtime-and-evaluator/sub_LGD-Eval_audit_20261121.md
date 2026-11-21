# LGD-Eval 评测引擎独立审计报告（只读）

- **审计对象**：`<audit-root>\LGD-Eval`
- **锚定版本**：`git rev-parse HEAD` = `db1d87a6cfa100de303eeb88655ab2440601bad5`（与 GitHub `LGD-Eval/LGD-Eval` main 一致，pushed 2026-11-20T12:21:09Z）
- **审计日期**：2026-11-21
- **执行环境**：Windows / PowerShell 7.6.4 / Python 3.13.18；全程离线，未安装任何包
- **审计方自建样本**：6 个（5 恶意 + 1 干净），路径 `<project-dir>\_audit_scratch\C_bench\`
- **只读声明**：审计前后 `git status --porcelain` 均为空（退出码 0）；未 commit / push / 发布 / 外联；未在仓库内新建或修改任何文件；未执行任何被测样本中的脚本代码
- **样本量与口径**：检出/误报部分为 **N=6 定性基准**，**不计算、不外推任何百分比**；CI 通过、作者文档自述、`benchmarks/README.md` 的「人工复核误报 0」均**不作为**安全成立的证据

---

## ① 结论摘要

**七问判定分布：2 条 VERIFIED，4 条 PARTIALLY VERIFIED，1 条 NOT VERIFIED。**

| 问题 | 判定 | 一句话结论 |
|---|---|---|
| Q1 评分与授权/放行是否完全分离 | **NOT VERIFIED**（"完全分离"不成立） | `skillgate.py` 是「发现物 + 分数」双条件（半分离）；但主 CLI `evaluate.py`、`lgd_audit.py`、`eval_mcp.py` 的退出码**只比较总分**，且 L0–L5 权限档是纯分数阈值映射 → 主通道是分数耦合 |
| Q2 不确定态是否阻止不安全放行 | **VERIFIED**（结论=不阻止） | 引擎**不存在** UNKNOWN/INCOMPLETE/FAILED 三值态；空目录/空 SKILL.md/纯乱码等"可解析但残缺"对象 **exit 0 放行**，空目录还给 67 分 C 级 |
| Q3 指纹/版本绑定是否真实可复现 | **PARTIALLY VERIFIED** | `fingerprint` 与 `tree_sha256` **同输入必同值且跨绝对路径稳定**（实测 5 次全等）；但 `evaluation_id` **不存在**、`rule_version` 不进证据 JSON、`engine_version` 硬编码 `1.1.0`（SARIF 另写 `1.0.0`） |
| Q4 恶意样本检出实测 | **PARTIALLY VERIFIED** | 5 个恶意样本中 3 个被阻断（命令注入、eval 混淆、多阶段+隐瞒话术），**2 个完全漏报且门禁放行**：凭证外发得 89/A，写 `~/.ssh` 得 100/A+ |
| Q5 重复运行一致性 | **VERIFIED** | 同一输入 3 次，score/dims/findings/fingerprint 逐字段完全一致，无漂移 |
| Q6 误报/漏报人工基准（N=6） | **PARTIALLY VERIFIED** | 干净样本两侧均无安全误报；漏报集中在「凭证→外发」数据流与「SSH 目录写入」两类；N=6 不作统计结论 |
| Q7 第三方可独立运行 | **PARTIALLY VERIFIED** | 核心评分在干净离线 venv（零第三方依赖）跑通且指纹与系统 Python 一致；但官方 `_demo/` 攻击夹具**不在公开克隆**，4 个包装入口调用即崩，`cryptography` 未声明 |

**三个最硬的结论（按对外影响排序）**

1. **门禁会放行真实恶意技能。** 自建样本「读 `GITHUB_TOKEN`/`OPENAI_API_KEY` 后 POST 到外部域名」在 `evaluate.py` 下得 **89/100 A**、0 条安全发现、`--fail-under 80` 退出码 0；在 `skillgate.py` 下得 **100/100 A+**、唯一 1 条 INFO、退出码 0。样本「追加写 `~/.ssh/authorized_keys`、覆写 `~/.ssh/config`」在 `skillgate` 下 **100/100 A+、0 findings、退出码 0**。根因可定位：`skillgate.py:123` 的 SSH 正则是 `~\.ssh/`，**不匹配标准写法 `~/.ssh/`**（实测 `'~/.ssh/config' → False`）；`evaluate.py:416-422,637-647` 的外泄规则只认「整份 environ 打包」，`os.environ.get("GITHUB_TOKEN")` 这种单变量读取不是污点源。
2. **门禁对"残缺/评不了"是 fail-open。** 空目录（连 SKILL.md 都没有）得 **67/100 C、exit 0**；空 SKILL.md 得 **61/100 C、exit 0**；超长乱码 61/C、exit 0。`--fail-under` 默认 0 且被 `if args.fail_under:` 判为假 → **不传阈值时门禁整体关闭**。空目录在 `--fail-under 60` 下仍 exit 0。调用方无法区分"评测完整可信"和"输入残缺勉强跑完"。
3. **对外声明与实测不一致。** README 的「分数决定权限」档位表（≥96 = L0 免审批直接执行）与 SPEC 的主张上限（"不可声称分数等于安全认证"）自相矛盾；`benchmarks/README.md:10` 声称本引擎包 `skillgate` 侧「0 findings，100/A+」，实测同一 HEAD 为 **86/A、10 条 findings（2 MEDIUM / 6 LOW / 2 INFO）**；`LICENSE` 是 CC BY 4.0，而 `package.json` 与 `pyproject.toml` 均写 MIT。

**已验证成立的正面事实（不应被上面的否定项掩盖）**

- 副本一致性成立：`vendor/scripts` 与 `skills/lgd-eval/scripts` 的 12 个 `.py` **SHA256 全部相同**，README「与 GitHub 源码逐字节相同」在当前 HEAD **可复现**。
- 指纹工程做得对：载荷只吃结论数据，**不含时间戳/主机名/用户名/随机数/绝对路径**；目录搬到另外两个绝对路径后 `fingerprint` 与 `tree_sha256` 不变。
- 确定性成立：三次重复运行逐字段一致（这一点很多同类引擎做不到）。
- 核心评分零第三方依赖：干净 venv（`pip list` 仅 `pip 26.3`）跑通，且与系统 Python 3.13 指纹完全一致。
- 规则表内的显式恶意模式能命中：`os.system`、`subprocess(shell=True)`、`eval/exec`、base64+eval 混淆特征、SKILL.md 里的"隐瞒用户/外泄凭证"话术，均在 `--fail-under 80` 下阻断。
- 引擎自评 100/100 A+ **可复现**（`evaluate.py` 对 `skills/lgd-eval` 实测 100/100 A+、exit 0），仓库根 `pytest` 实测 `4 passed in 0.05s`。

---

## ② 逐条回答

### Q1 评分逻辑与授权/放行逻辑是否完全分离

**判定：NOT VERIFIED —— "完全分离"不成立。分三条通道，两条耦合、一条半分离。**

**结论**：不存在单一的"分数高就放行"总闸，但主 CLI 通道的放行判定**只读总分**。`skillgate.py` 把 CRITICAL/HIGH 作为独立的硬阻断条件（这是好的设计），但它只是可用通道之一；`evaluate.py`（对外主入口、npm 包转发的那个）、`lgd_audit.py`、`eval_mcp.py` 的退出码都只比分数。更关键的是 `evaluate.py:802-814` 把分数直接映射成 L0–L5 执行权限，README 又把这张表对外说成权限规则——这是整个仓库里最接近"分数即授权"的位置。

**证据命令**
```powershell
$s='<audit-root>\LGD-Eval\skills\lgd-eval\scripts'
Select-String -Path "$s\*.py" -Pattern 'sys\.exit|fail.under|critical_count|high_count|trust_score <|score >=|score <' |
  Select-Object Filename,LineNumber,Line | Format-Table -AutoSize -Wrap
```

**「分数 → 决策」调用链（谁读分做决策，实测行号）**

| 通道 | 位置 | 判定条件 | 性质 |
|---|---|---|---|
| 主 CLI `evaluate.py` | `1627-1633` | `if args.fail_under:` → `if score < args.fail_under: sys.exit(1)` | **分数单条件**（无 findings==0 / 签名 / 人工复核） |
| `skillgate.py` CI 退出 | `1279-1290` | `critical_count>0 or high_count>0` → 1；**或** `trust_score < fail_under` → 1 | **双条件，半分离** |
| `skillgate.py` 批量 / agent 格式 | `1576-1583` / `1621-1622` | 只看 CRIT/HIGH；agent 格式**忽略 `--fail-under`** | 分数不参与 |
| `lgd_audit.py` | `782` | `sys.exit(0 if score >= 90 else 1)` | **分数单条件** |
| `eval_mcp.py` | `229-231` | `if args.fail_under and total < args.fail_under: sys.exit(1)` | **分数单条件** |
| `autofix.py` | `337-343, 359-364` | 达标即 `break`，未达标只打印 | **不产生非零退出码** |
| 分数→权限档 L0–L5 | `evaluate.py:802-814` | `score>=96 → L0 免审批` … `else → L5 拒绝执行` | **纯阈值映射，仅 print** |
| 三律 L1/L2/L3 | `evaluate.py:832-851` | 文件存在性 + finding 关键词 | **只打印，不写退出码、不写 gate 状态** |
| CI | `.github/workflows/auto-eval.yml:27-31` | 调外部 action `LGD-Eval/lgd-gate@main`，`threshold: '90'` | **本仓不可见的黑盒** |

**证据输出（`evaluate.py:802-814` 原文骨架 + 门禁分支）**
```python
if score >= 96:   gate = "L0 免审批（可直接运行，无需限流）"
elif score >= 81: gate = "L1 一次性确认（限流 60 次/分）"
elif score >= 51: gate = "L2 人工复核（限流 30 次/分）"
elif score >= 31: gate = "L3 沙箱运行（每次调用强制确认）"
elif score >= 11: gate = "L4 隔离环境（仅允许只读调用）"
else:             gate = "L5 拒绝执行（需重写后重新评测）"
# 1627-1633
if args.fail_under:
    if score < args.fail_under:
        print("  ⛔ 门禁未通过：{score} < {args.fail_under}（退出码 1）"); sys.exit(1)
```

**实证后果（与 Q4 交叉）**：恶意外发样本 s2 在 `evaluate.py` 得 89/A，`--fail-under 80` **exit 0**；按 README 档位表 89 分对应「L1 一次性确认」，但代码里没有任何东西执行这个"确认"。也就是说：**分数档位是文案，放行是退出码，两者之间没有强制绑定。**

**证据位置**：`skills/lgd-eval/scripts/evaluate.py:802-814, 1627-1633`；`skillgate.py:1279-1290, 1318-1324, 1576-1583, 1621-1622`；`lgd_audit.py:782`；`eval_mcp.py:229-231`；`autofix.py:337-343, 359-364`；`README.md:46-57`（"## 分数决定权限"档位表）；`SPEC.md:22-25`（主张上限，"不可声称分数等于安全认证"）。

**未覆盖**：外部 action `LGD-Eval/lgd-gate@main` 的内部判定不在本仓，threshold 90 如何映射成 job 成败 **NOT VERIFIED**。

---

### Q2 不确定态（UNKNOWN/INCOMPLETE/FAILED）是否阻止不安全放行

**判定：VERIFIED —— 前提不成立：引擎没有三值态，且对"可解析但残缺"的对象默认 fail-open 放行。**

**结论（硬）**：
- **不存在** UNKNOWN / INCOMPLETE / FAILED 状态。实际语义是「**exit 0/1 二值 + A+/A/B/C/D[/F] 字母等级 + findings/warnings 列表**」。全仓检索 `UNKNOWN|INCOMPLETE|FAILED` 只命中自检脚本里的局部变量与异常文本，评测输出结构里没有该状态字段。
- **fail-open 实证**：空目录、空 SKILL.md、纯乱码 → 照常出分、出等级、**exit 0**。只有"路径不存在 / 缺位置参数"是 fail-closed（exit 1）；二进制损坏文件是**未捕获异常 traceback 退出 1**（非零但不是结构化失败态）。
- `--fail-under` 的判定量是**封顶后的总分**（不是等级、不是五维、不是 raw_score）；阈值为 0 被 falsy 语义判为"关闭门禁"；越界值（101）无校验，必然失败。

**证据命令**
```powershell
$base='<project-dir>\_audit_scratch\B_dynamic'
$eng='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\evaluate.py'
python $eng "$base\does_not_exist"      # 路径不存在
python $eng "$base\case_empty"          # 空目录，无 SKILL.md
python $eng "$base\case_empty_md"       # SKILL.md 存在但为空
python $eng "$base\case_bad_md"         # SKILL.md 二进制/非法 UTF-8
python $eng                             # 缺位置参数
python $eng "$base\sample_good" --fail-under 0
python $eng "$base\sample_good" --fail-under 60
python $eng "$base\sample_good" --fail-under 101
python $eng "$base\case_empty"  --fail-under 60
```

**证据输出（退出码实测）**

| 输入 | 总分/等级 | 退出码 | 语义 |
|---|---|---|---|
| 路径不存在 | — | **1** | ❌ `路径不存在或不是目录`（fail-closed） |
| 空目录（无 SKILL.md） | **67 / C** | **0** | 缺 SKILL.md/LICENSE/README/scripts/examples 仍放行（**fail-open**） |
| SKILL.md 为空 | **61 / C** | **0** | 字段缺失一堆，仍放行（**fail-open**） |
| SKILL.md 二进制非法 UTF-8 | — | **1** | 未捕获 `UnicodeDecodeError`，栈到 `evaluate.py:130` |
| 可解码超长乱码 | **61 / C** | **0** | 走"单文件模式"，放行 |
| 缺位置参数 | — | **1** | 用法提示后退出 |
| `--fail-under 0`（对象 93 分） | 93 / A+ | **0** | 阈值 0 关闭门禁，未打印门禁行 |
| `--fail-under 60`（对象 93 分） | 93 / A+ | **0** | `✅ 门禁通过：93 ≥ 60` |
| `--fail-under 101`（越界） | 93 / A+ | **1** | `⛔ 93 < 101`（无范围校验，必然失败） |
| `--fail-under 60`（空目录 67 分） | 67 / C | **0** | **空壳技能通过 60 分门禁** |
| `--fail-under 70`（空目录 67 分） | 67 / C | **1** | 才被卡住 |

**证据位置**：`evaluate.py:98-105`（路径不存在 exit 1）；`129-130, 210-211, 744-745, 755-756`（严格 utf-8 打开，对照 `678, 1130, 1391` 用 `errors="ignore"`）；`781-795`（A+/A/B/C/D 等级）；`1504`（`--fail-under` default=0，仅 `type=int`）；`1627-1633`（门禁分支）。三值裁决只存在于独立子系统 `ai-index-gate/adjudicator.py:122-136` + `gate.py:317-318`（`uncertain → REVIEW`），**不属于 lgd-eval 主引擎**，不能据此声称主引擎具备不确定态。

**未覆盖**：未构造权限不可读目录、磁盘 I/O 错误、数万文件超大目录；未测 `--sandbox`/`--llm-review` 失败路径的退出码。

---

### Q3 fingerprint / evaluation_id / engine_version / rule_version 是否真实存在且可复现

**判定：PARTIALLY VERIFIED —— 两个哈希真实、可复现、跨路径稳定；但 `evaluation_id` 不存在，`rule_version` 不在证据 JSON 里，版本号硬编码且两处不一致。**

**结论**：
- 硬结论 1：**同一输入 → 同一 `fingerprint`、同一 `tree_sha256` 实测成立**，且**不绑定绝对路径**（同一份内容复制到 `copyA` 与 `copyA_deep\copyA` 后哈希不变）。
- 硬结论 2：**`evaluation_id` 全仓 0 命中，该字段不存在。**
- 硬结论 3：**`rule_version` 不存在于 `evaluate.py` 的证据 JSON**（显式核查 `rule_version / rules_version / rule_set_version / ruleset_version / schema_version / policy_version / spec_version / version` 8 个候选名，全部 ABSENT）；仅 `skillgate.py:306` 有常量 `v3.1.3`，经 `asdict` 进 skillgate 的 JSON。
- `engine_version` 硬编码 `"1.1.0"`（`evaluate.py:1230`，`build_attestation` 内），无读 git tag / 包元数据的逻辑；**SARIF 输出另硬编码 `"1.0.0"`**（`1483`），两者不一致。
- 我方补测（同一 HEAD）：`evaluate.py` 对自身包给 **100/100 A+、exit 0**（README 自评分可复现）；但 `skillgate.py` 对同一包给 **86/A、10 条 findings**（2 MEDIUM/6 LOW/2 INFO），与 `benchmarks/README.md:10` 声明的「0 findings，100/A+」**不符**。

**证据命令**
```powershell
$base='<project-dir>\_audit_scratch\B_dynamic'
$eng='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\evaluate.py'
python $eng "$base\sample_good" --evidence-json "$base\out1.json"
python $eng "$base\sample_good" --evidence-json "$base\out2.json"
python $eng "$base\copyA"             --evidence-json "$base\out3.json"
python $eng "$base\copyA_deep\copyA"  --evidence-json "$base\out4.json"
python "$base\analyze_q3q5.py"
# 我方补充：自评口径复现
python $eng '<audit-root>\LGD-Eval\skills\lgd-eval'
python '<audit-root>\LGD-Eval\skills\lgd-eval\scripts\skillgate.py' scan '<audit-root>\LGD-Eval\skills\lgd-eval' --format json
```

**证据输出（`analysis_q3q5.txt` 原文摘录）**
```
out1: fp=sha256:afa2deff...d3586adff  tree=sha256:fa477a37...1c2dfeb
out2: fp=sha256:afa2deff...d3586adff  tree=sha256:fa477a37...1c2dfeb
out3: fp=sha256:afa2deff...d3586adff  tree=sha256:fa477a37...1c2dfeb
out4: fp=sha256:afa2deff...d3586adff  tree=sha256:fa477a37...1c2dfeb
r3  : fp=sha256:afa2deff...d3586adff  tree=sha256:fa477a37...1c2dfeb
same-path fp identical out1==out2==r3 : True
cross-copy fp identical out1==out3==out4 : True
cross-copy tree identical out1==out3==out4: True
no timestamp/hostname/user/random/abs-path key or value found
```
- attestation 顶层 key 共 10 个：`dims / engine_version / findings / fingerprint / framework / grade / inputs / reproduce / safety_veto / score`
- `inputs` 子键：`file_count / files（相对路径→sha256 映射）/ tree_sha256 / note`；`findings[i]` 子键：`rule_id / dimension / file / line / evidence / fix / verify / severity`
- 自评补测：`LGD Trust Score: 100/100 🏆 A+`，`SELF_EXIT=0`；skillgate：`trust_score=86, grade=A, rule_version=v3.1.3, MEDIUM x2, LOW x6, INFO x2`，`EXIT=0`（2 条 MEDIUM 不阻断，符合"只有 CRIT/HIGH 才阻断"）

**算法定义（静态核实）**
- `fingerprint` = `sha256(canonical_dumps({object:{score,grade}, dims, findings, [veto]}))`（`evaluate.py:1210-1220`），键排序 + 紧凑分隔（`1185-1187`）→ 哈希对象是**评测结论快照**，不是纯输入。
- `tree_sha256` = 逐文件 `sha256(文件字节)` 组成 `{相对路径: 内容哈希}` 再整体 sha256（`1190-1205`）；跳过 `.git/__pycache__/node_modules/.venv/venv`（`1193`）；**mtime 不进哈希，绝对路径不进哈希**。

**可复现承诺的真实边界**：指纹对"同一份输入的同一份结论"稳定（这一点很强），但因为载荷里含 `score/grade/dims/findings` 这些**输出量**，它无法区分"同一结论来自不同引擎版本"——规则改了而 `engine_version` 没 bump，两代引擎会产出同一指纹；又因为证据 JSON 里没有 `rule_version`，历史证明无法回溯"当时按哪版规则评的"。这是可追溯性缺口，不是可复现性缺口，两者要分开说。

**证据位置**：`evaluate.py:1185-1187, 1190-1205, 1208-1220, 1223-1239, 1230, 1483`；`skillgate.py:306, 1640`；`benchmarks/README.md:9-10`。

**未覆盖**：未跨 Python 版本、跨 OS 比对；未验证 `safety_veto.applied=true` 时指纹是否仍稳定；未构造 findings 文本里嵌入绝对路径的样本。

---

### Q4 自建恶意 Skill 样本实测（5 个）

**判定：PARTIALLY VERIFIED —— 规则表内的显式模式被阻断，两类真实攻击（凭证外发、SSH 目录写入）双侧零发现且门禁放行。**

**样本与结果总览（实测）**

| 样本 | 人工标注 | evaluate 分数 | evaluate 安全命中 | skillgate 分数 | skillgate findings | eval 退出码（无阈值 / `--fail-under 80`） | gate 退出码（无阈值 / `--fail-under 80`） |
|---|---|---|---|---|---|---|---|
| s1 命令注入 | 未过滤拼接 + `os.system` + `shell=True` | 69 / C | 2：`R-SEC-03`(run.py:14)、`R-SEC-05`(run.py:10) | 72 / B | 2 CRITICAL | 0 / **1** | **1 / 1** |
| s2 凭证外发 | 读 `GITHUB_TOKEN`+`OPENAI_API_KEY` → POST 外部域名 | **89 / A** | **0**（安全 25/25） | **100 / A+** | 仅 1 INFO（`requests 网络库`） | 0 / **0** | **0 / 0** |
| s3 base64+eval | 解码 blob 后 `eval` | 69 / C | 2：`R-SEC-04`、`R-SEC-08` | 87 / A | 1 CRITICAL（仅 eval） | 0 / **1** | **1 / 1** |
| s4 写 SSH 目录 | 追加 `~/.ssh/authorized_keys`、覆写 `~/.ssh/config` | **89 / A** | **0**（安全 25/25） | **100 / A+** | **0** | 0 / **0** | **0 / 0** |
| s5 多阶段外传+隐瞒 | env → 临时文件 → `curl` 外发；注释藏"不要告诉用户" | 49 / D | 4：`R-SEC-03`×2、`R-SEC-12`、`R-SEC-14` | 83 / A | 1 CRITICAL + 1 MEDIUM | 0 / **1** | **1 / 1** |
| s6 干净基线 | 仅本地 JSON 读写 | 89 / A | 0 | 100 / A+ | 0 | 0 / 0 | 0 / 0 |

> 注：`evaluate.py` 无阈值时退出码恒为 0（只看 `--fail-under`）；`skillgate` 只要存在任一 CRITICAL/HIGH 即 exit 1，与分数阈值无关。

**证据命令（对任一样本）**
```powershell
$eng='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\evaluate.py'
$gate='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\skillgate.py'
$s='<project-dir>\_audit_scratch\C_bench\s2-env-exfil'
python $eng $s
python $eng $s --fail-under 80
python $gate scan $s --format json
python $gate scan $s --fail-under 80
```

**两处完全漏报的机理（已定位到行）**

1. **s2 凭证外发**
   - `evaluate.py`：外泄规则 `R-SEC-21` 只认**整份 environ 打包**（`ENV_BULK_RE`，`416-422`；组合判定 `637-647`）；污点源只认 `open()` 折叠出敏感路径常量（`387`），**不认环境变量凭证**；`SEC_RULES`（`424-446`）无"凭证随 POST 外发"的通用规则。
   - `skillgate.py`：网络正则在**剥离字符串后的代码行**上匹配（`578`, `666`）→ 外发 URL 在字符串内被抹成空格；凭证正则只覆盖 `os.environ["TOKEN"]` 下标形式与 `os.getenv(...)`（`120-122`），**不认 `os.environ.get(...)` 方法形式**。
2. **s4 写 SSH 目录**
   - `skillgate.py:123` 的 SSH 正则是 `~\.ssh/`，只读复算实测：
     ```
     '~/.ssh/config'           → False
     '~/.ssh/authorized_keys'  → False
     '~.ssh/config'            → True   # 只有非标准写法才命中
     ```
   - `evaluate.py`：`SEC_RULES` 无 SSH 路径规则；污点源要求 `open()` 参数折叠出常量路径，本样本 `open(authorized, ...)` 收的是变量名，未被识别。

**部分漏报（s5）**："env 凭证 → 临时文件 → curl"的多阶段污点链两侧都未串联；curl 与外部端点在字符串剥离后漏检；`skillgate` 的 MD 外泄规则只覆盖 `EXCESSIVE_AGENCY` 短语（`831-848`），没覆盖"forward the API key / do not tell the user"这类话术（而 `evaluate` 的 `R-SEC-14` 恰好命中）→ **同一技能在两套扫描器下结论不一致**。

**边界**：两引擎均为静态规则 + 轻量 AST，**不做运行期行为观测、不解码还原载荷**（引擎自述见 `skills/lgd-eval/SKILL.md:97-111`）。"未命中"只代表"在这套规则下未命中"，不等于无风险；反之命中也不等于已证实真实外发。

**证据位置**：见各样本 `C_bench\_logs\` 下 `eval_*.txt` / `gate_*.json` / `evidence_*.json` / `*_fail80.txt`；引擎侧行号：`evaluate.py:317-321, 387-400, 416-422, 424-446, 547-551, 637-658, 675-692`；`skillgate.py:120-123, 578, 666, 674-700, 831-848`。

---

### Q5 重复运行一致性

**判定：VERIFIED —— 三次运行逐字段完全一致，无漂移字段。**

**证据命令**
```powershell
$base='<project-dir>\_audit_scratch\B_dynamic'
$eng='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\evaluate.py'
python $eng "$base\sample_good" --evidence-json "$base\out1.json"
python $eng "$base\sample_good" --evidence-json "$base\out2.json"
python $eng "$base\sample_good" --evidence-json "$base\r3.json"
python "$base\analyze_q3q5.py"    # findings 先按 (rule_id,file,line,evidence) 排序再 diff
```

**证据输出（`analysis_q3q5.txt` 原文）**
```
score: identical=True  values=[93, 93, 93]
grade: identical=True  values=['A+', 'A+', 'A+']
dims: identical=True  values=[{'安全':25,'文档质量':13,'生态兼容性':15,'目录结构':15,'结构完整性':25}, ...]
fingerprint: identical=True  values=['sha256:afa2deff...d3586adff', ...]
findings (sorted) : identical=True
```
三次 findings 也完全一致：`R-DOC-01 缺少使用场景说明`、`R-DOC-03 缺少示例`、`R-DOC-04 建议加上已知限制说明`（warning）。

**一致性来源**：评分是确定性文本/存在性判定，哈希经 `canonical_dumps` 规范化；耗时 `elapsed`（`evaluate.py:771,815`）只打印到终端，不进证据 JSON。跨解释器也一致（venv 与系统 Python 3.13 指纹相同）。

**证据位置**：`evaluate.py:771-800, 1139-1182, 1185-1187`；比对脚本 `...\B_dynamic\analyze_q3q5.py`。

**未覆盖**：单一良性夹具 ×3 次，未做 10+ 次长程；未测 `__pycache__`、隐藏临时文件对树哈希的影响（代码已排除常见目录，`1193`）。

---

### Q6 误报 / 漏报人工基准

**判定：PARTIALLY VERIFIED —— 人工标注先于引擎结果落盘（顺序未反），干净样本无安全误报，漏报集中在两类；N=6，仅定性。**

**方法与纪律**：6 个样本建好后，先在 `_annotations_pre_engine.md` 写下逐样本的人工判定（基于源码），**之后**才跑引擎。样本量 **N=6**（5 恶意 + 1 干净），**不计算误报率/检出率百分比，不外推为生态结论**。

**误报清单（引擎报、人工判无害；安全域）**
- **本批 N=6 未观察到安全类误报。**
- s6 干净样本：`evaluate` 0 条安全发现、`skillgate` 0 findings；其余 5 条扣分是结构/文档质量项（缺 LICENSE/README/examples/示例/限制说明），不计入安全误报。
- s2 的 `INFO requests 网络库（常见）` 是库导入提示，级别 INFO，不构成安全误报，但说明"用了网络库"本身不产生外泄判定。
- **边界声明**：不得据此声称误报率为 0；未覆盖第三方库良性用法、文档示例代码块等更易触发误报的形态。

**漏报清单（人工判有害、引擎未报）**

| # | 样本 | 实际恶意行为 | evaluate 缺失 | skillgate 缺失 | 证据 |
|---|---|---|---|---|---|
| F-1 | s2-env-exfil | 读两个凭证环境变量 → POST 外部域名 | `R-SEC-21` 只认整份 environ 打包（`416-422,637-647`）；无"凭证随 POST 外发"规则（`424-446`） | 只报 1 INFO；URL 在字符串剥离后漏检（`578,666`）；凭证正则不认 `os.environ.get(...)`（`120-122`） | `collect.py:8-14`；89/A + 100/A+ 双放行 |
| F-2 | s4-ssh-write | 追加 `authorized_keys`、覆写 `config` | 无 SSH 路径规则；污点源要求 open() 常量路径（`387-400`） | 正则 `~\.ssh/` 不匹配 `~/.ssh/`（`123`，实测三种写法） | `setup.py:6-15`；两侧 0 findings，gate 100/A+ |
| F-3 | s5-stealth-tmp-curl | env → 临时文件 → curl 外发；注释藏指令 | 数据流未串联，env 读取非污点源 | 未识别 curl/env/中转；MD 话术规则不含该表述（`831-848`） | `telemetry.py:8-18`；`SKILL.md:22` |
| F-4 | s3-obfuscated | base64 解码层混淆还原 | 已报 `R-SEC-08`（覆盖到） | 只报 eval 调用，未标记解码/混淆特征 | `payload.py:5-7` |
| F-5 | s1-cmd-injection | 未转义输入拼接（注入根因） | 只命中 shell 通道关键字，未标"输入未转义"根因 | 同左（AST 报调用不报污点） | `run.py:9,14`（属深度边界，非整体漏报） |

**真阳性**：s1 命令注入通道、s3 `eval` 动态执行、s5 `shell=True` 与文档隐瞒/外泄话术（均 `--fail-under 80` 退出 1）。**真阴性**：s6 干净基线。
**对照结论**：规则以"关键字 + 单文件单调用"匹配为主，**跨阶段、跨写法（`/` vs `\`、`.get()` vs `[]`、字符串拼接）的变体容易绕过**。

**证据位置**：`C_bench\_annotations_pre_engine.md`（先于引擎）、`C_bench\_logs\`（引擎原始输出）；`skills/lgd-eval/SKILL.md:97-111`（引擎自述静态边界）。

**未覆盖**：未测 JS/TS、shell 脚本、postinstall 供应链路径；未测 L2 LLM 复核与 L3 沙箱（未配 `LGD_LLM_BASE/KEY`、未启用 docker）。

---

### Q7 第三方可独立运行材料

**判定：PARTIALLY VERIFIED —— 核心评分在干净离线 venv 可跑通（VERIFIED）；检测能力的阳性复现路径与部分入口不可用（阻塞）。**

**能跑通的（实测）**
```powershell
$base='<project-dir>\_audit_scratch\B_dynamic'
$eng='<audit-root>\LGD-Eval\skills\lgd-eval\scripts\evaluate.py'
python -m venv "$base\.venv_q7"
& "$base\.venv_q7\Scripts\python.exe" -m pip list          # 仅 pip 26.3
& "$base\.venv_q7\Scripts\python.exe" $eng "$base\sample_good" --evidence-json "$base\venv_out.json"
python --version                                            # Python 3.13.18
```
- 干净 venv（`pip list` 只有 `pip 26.3`）退出码 0，`93/100 A+`，`fp match system vs venv: True`，`tree match: True`。
- 运行期**零第三方依赖**：顶层 import 全为标准库（`evaluate.py:9-19`），函数内惰性导入 `io/tokenize/base64/math/argparse`。
- 未发现写死的作者本机绝对路径（路径均由 `__file__` 或入参 `abspath` 派生）。
- 仓库根自测：`python -m pytest tests -q -p no:cacheprovider` → **4 passed in 0.05s**，`git status --porcelain` 仍为空。

**阻塞点（第三方照文档做会卡住的地方）**

| # | 阻塞 | 证据 | 影响 |
|---|---|---|---|
| 1 | 官方攻击样本夹具缺失：`skills/lgd-eval/tests/README.md:8-14` 让你跑 `_demo/mitiga-style`、`_demo/poisoned-skill`，但**公开克隆根目录没有 `_demo/`**（`Test-Path` = False，递归无 demo/samples/testdata） | `tests/README.md:8-14`；`skills/lgd-eval/tests/` 下仅 `README.md`(624B) | 第三方**无法复现"检测器能抓恶意样本"这条路径**，只能自建样本（本次即如此） |
| 2 | 四个包装入口调用即崩：`evaluate_skill` 返回 **6 元组**（`evaluate.py:873` `return score, grade, dims, findings, warnings, veto_info`），`scorecard.py:48`、`lgd_web.py:88,120`、`lgd_mcp_server.py:92`、`autofix.py:338` 全部按 **5 元组**解包 → `ValueError: too many values to unpack (expected 5)` | `evaluate.py:873`；上述 5 行（我方已独立复核 import 指向同一函数：`lgd_web.py:39`、`lgd_mcp_server.py:33`、`scorecard.py:23`、`autofix.py:23`） | Web UI / MCP / 评分卡 / autofix 四条入口的评测功能不可用；仅主 CLI 正常 |
| 3 | 未声明第三方依赖：`ai-index-gate/sign.py:23-24` 用 `cryptography`，但 `package.json` 无 `dependencies`、`pyproject.toml` 只列 `pytest` | `sign.py:23-24`；`pyproject.toml:14-15` | 按清单装齐环境后签名/验签仍不可用（`demo.py:95-96` 自述跳过签名） |
| 4 | 跨仓黑盒：`auto-eval.yml:28` 调外部 action `LGD-Eval/lgd-gate@main`；`scanner-gate.yml:19` 运行时 `curl` 拉远端 `skill-audit/main/scanner.py`（注释 v0.3.0 vs 仓内 `scanner.py:31` VERSION=0.3.4） | 工作流行号 | CI 门禁实际执行版本不可控；扫描步骤 `|| true` 显式不阻断 |
| 5 | 许可证口径冲突：`LICENSE` 第 1 行 `Attribution 4.0 International`（CC BY 4.0），而 `package.json` 与 `pyproject.toml` 都写 `MIT`，README:84 又写工具另署 Apache-2.0 | `LICENSE:1`；`package.json` `"license":"MIT"`；`pyproject.toml` `license={text="MIT"}` | 第三方采用/再分发时无法判定适用条款 |
| 6 | 元数据不同源：`package.json` 的 `repository` 指向 `LGD-Eval/lgd-gate`，当前仓库是 `LGD-Eval/LGD-Eval` | `package.json:16-19` | 溯源/供应链审计时指向另一仓 |

**最小补齐建议（仅建议，未改仓库）**
1. 公开包内补一份**脱敏/合成**的阳性+阴性样本夹具（或明确写"阳性样本需向何处获取"），让 `tests/README.md` 指引可跑。
2. 统一 `evaluate_skill` 返回契约（包装处补第 6 个 `veto_info`，或主引擎改回 5 元组），并为 `scorecard/lgd_web/MCP/autofix` 各加一条离线冒烟测试。
3. `cryptography` 显式声明为 optional extra，README 注明"核心扫描零依赖"。
4. `LICENSE` 与 `package.json`/`pyproject.toml`/README 四方口径对齐。
5. 工作流改为 pin 住外部 action 版本（`@v1` 而非 `@main`），扫描步骤去掉 `|| true`。

---

## ③ 缺陷清单（按 P0 / P1 / P2）

> 分级口径：P0 = 直接导致恶意技能被放行或安全结论失真；P1 = 关键入口不可用、结论不可追溯、对外声明与实际不符；P2 = 工程卫生与一致性。

### P0（3 条）

| # | 缺陷 | 证据位置 | 影响 |
|---|---|---|---|
| P0-1 | 单凭证环境变量读取 + HTTP 外发**双侧漏报**，门禁放行 | 样本 `C_bench\s2-env-exfil\scripts\collect.py:8-14`；`evaluate.py:416-422,424-446,637-647`；`skillgate.py:120-122,578,666`；实测 `evaluate 89/A exit 0`、`skillgate 100/A+ exit 0` | 典型凭证外泄样本可直过"上架前快筛" |
| P0-2 | SSH 目录写入（`authorized_keys` / `config`）**双侧漏报**，gate 给 100/A+ | 样本 `s4-ssh-write\scripts\setup.py:6-15`；`skillgate.py:123`（`~\.ssh/` 不匹配 `~/.ssh/`）；`evaluate.py` 无 SSH 规则 | 持久化后门式配置篡改不被阻断 |
| P0-3 | 残缺/不可完整评测对象默认 **fail-open**（exit 0 + C 级数字分），无 INCOMPLETE/UNKNOWN 标识 | `evaluate.py:771-815,1627-1633`；实测空目录 67/C exit 0、空 SKILL.md 61/C exit 0、乱码 61/C exit 0；空目录过 `--fail-under 60` | 空壳/残缺技能可能被门禁默认放过；调用方无法判断评测是否完整可信 |

### P1（9 条）

| # | 缺陷 | 证据位置 | 影响 |
|---|---|---|---|
| P1-1 | 主 CLI / `lgd_audit` / `eval_mcp` 退出码**只比较总分**，无"零高危 + 签名 + 复核"并列条件 | `evaluate.py:1627-1633`；`lgd_audit.py:782`；`eval_mcp.py:229-231` | 残留 MEDIUM/LOW 或结构缺口可凭分数越门禁；"放行"语义偏分数耦合 |
| P1-2 | 分数→L0–L5 权限档纯阈值映射并对外表述为权限规则，与 SPEC 主张上限自相矛盾 | `evaluate.py:802-814`；`README.md:46-57`；`SPEC.md:22-25` | 高分被解读为授权依据，存在过度信任风险 |
| P1-3 | 四个包装入口 5 元组解包 6 元组返回值，调用即 `ValueError`（已复现） | `evaluate.py:873`；`scorecard.py:48`、`lgd_web.py:88,120`、`lgd_mcp_server.py:92`、`autofix.py:338` | Web/MCP/评分卡/autofix 评测功能不可用 |
| P1-4 | 二进制/非法 UTF-8 的 SKILL.md 触发**未捕获** `UnicodeDecodeError`，以 traceback 退出；同文件 4 处严格 utf-8、3 处 `errors="ignore"`，解码策略不一致 | `evaluate.py:129-130,210-211,744-745,755-756` vs `678,1130,1391` | 下游只能拿到非零码，无法区分"输入损坏"与"引擎内部错误"，且栈轨迹泄漏路径 |
| P1-5 | `benchmarks/README.md:10` 声明本引擎包 `skillgate` 侧「0 findings，100/A+」，实测同一 HEAD 为 **86/A、10 findings（2 MEDIUM/6 LOW/2 INFO）** | `benchmarks/README.md:10`；实测命令与输出见 Q3 | 自评基准不可复现，对外引用会失真 |
| P1-6 | 许可证四方口径冲突（LICENSE=CC BY 4.0 vs package.json/pyproject=MIT vs README 工具 Apache-2.0） | `LICENSE:1`；`package.json`；`pyproject.toml` | 第三方采用/再分发无法判定条款 |
| P1-7 | 官方攻击样本 `_demo/` 不在公开克隆，`tests/README.md` 指引的复现路径跑不通 | `skills/lgd-eval/tests/README.md:8-14`；`Test-Path _demo` = False | 外部无法复现检测器基线（作者已在 `SPEC.md:33` 自认该缺口） |
| P1-8 | 多阶段外传（env → 临时文件 → curl）污点链不串联；字符串剥离使网络/端点规则失效 | `telemetry.py:8-18`；`evaluate.py:387-400,637-658`；`skillgate.py:578,666` | 拆分式外发绕过数据流判定，只靠 `shell=True` 兜底 |
| P1-9 | `skillgate` 无独立混淆/解码特征规则，base64+eval 只报 eval 调用，与 `evaluate` 的 `R-SEC-08` 不对齐 | `payload.py:5-7`；`evaluate.py:547-551`；gate findings 仅 1 条 AST | 同一技能两套扫描器结论不一致，混淆层风险在 gate 口径被低估 |

### P2（11 条）

| # | 缺陷 | 证据位置 | 影响 |
|---|---|---|---|
| P2-1 | 证据 JSON 无 `rule_version`；`engine_version` 硬编码 `1.1.0`，SARIF 另写 `1.0.0`（不一致）；`evaluation_id` 不存在 | `evaluate.py:1230,1483`；`skillgate.py:306` | 跨规则/跨版本评测身份无法追溯 |
| P2-2 | `--fail-under 0` 被 `if args.fail_under:` 判为 falsy → 门禁关闭；>100 越界无校验 | `evaluate.py:1504,1627-1633` | 门禁配置误用风险，参数越界无提示 |
| P2-3 | `skillgate --format agent` 分支只看 CRIT/HIGH，忽略 `--fail-under` | `skillgate.py:1621-1622` | agent 消费方可能拿到"分数不达阈却 exit 0" |
| P2-4 | 解析/读取失败静默跳过，AST 失败文件在安全维度**不扣分**、不标"不可评" | `evaluate.py:371-372,458-459,592-593,680-681,700-701`；`skillgate.py:574,736,860,916,941` | "评不了"与"没风险"无法区分，偏向漏报 |
| P2-5 | `cryptography` 未在任何清单声明 | `ai-index-gate/sign.py:23-24` | 按清单装不齐签名/验签能力 |
| P2-6 | CI 扫描器版本漂移（远端 v0.3.0 vs 仓内 0.3.4）且扫描步骤 `|| true` 不阻断 | `scanner-gate.yml:19,23`；`scanner.py:31` | 门禁实际执行版本不可控，扫描失败不卡 PR |
| P2-7 | 外部 gate action 为黑盒（`LGD-Eval/lgd-gate@main`），threshold 90 的退出语义本仓不可见 | `auto-eval.yml:27-31` | CI 放行判断存在不可审计环节 |
| P2-8 | `--chart` 把 `radar.svg` 静默写入进程 cwd；单文件模式把输入复制进系统临时目录 | `evaluate.py:1537,1549` | 未知 cwd 下可能覆盖同名文件、残留临时目录 |
| P2-9 | 同一 `shell=True` 由正则与 AST 双通道各报一条（未跨通道去重） | `s5 telemetry.py:14/17`；`evaluate.py` findings 两条 `R-SEC-03` | 重复计数影响扣分与证据链整洁度 |
| P2-10 | `SPEC.md:31` 仍把「`ast_analyzer.py` 两处副本已分叉」列为已知缺口，实际两侧 12 个 `.py` SHA256 全等，`known_divergence.txt` 已写明"当前状态：空…2026-11-18 已同步" | `SPEC.md:31`；`known_divergence.txt`；我方 SHA256 比对 | 陈旧文档让外部误判供应链风险（属文档漂移，非代码缺陷） |
| P2-11 | `BENCHMARK_RESEARCH.md:13` 写有「DeepEval…150K+ 开发者 · 1 亿+ 日评测 · 被 OpenAI/Google/Microsoft 使用」等第三方采用数据，未附来源 | `BENCHMARK_RESEARCH.md:13` | 对外引用时构成不可核验的第三方背书，有合规/信誉风险 |

---

## ④ 可复跑的最小验证步骤

以下每条均可由第三方在干净机器上复跑；`$R` 为仓库根，`$S` 为审计 scratch 根。**只读，不需要写仓库。**

```powershell
$R='<audit-root>\LGD-Eval'
$S='<project-dir>\_audit_scratch'
$eng="$R\skills\lgd-eval\scripts\evaluate.py"
$gate="$R\skills\lgd-eval\scripts\skillgate.py"

# 0 基线与只读核验
git -C $R rev-parse HEAD            # 期望 db1d87a6cfa100de303eeb88655ab2440601bad5
git -C $R status --porcelain        # 期望空
python --version                    # 期望 3.13.x
cd $R; python -m pytest tests -q -p no:cacheprovider   # 期望 4 passed

# 1 副本一致性（README:70「逐字节相同」）
Get-ChildItem "$R\skills\lgd-eval\scripts" -Filter *.py | ForEach-Object {
  $h1=(Get-FileHash $_.FullName -Algorithm SHA256).Hash
  $h2=(Get-FileHash "$R\vendor\scripts\$($_.Name)" -Algorithm SHA256).Hash
  if($h1 -eq $h2){"$($_.Name) SAME"}else{"$($_.Name) DIFF"} }   # 期望 12 个全 SAME

# 2 Q3/Q5 指纹与重复性（需要 B 路夹具；或自建任意良性技能目录替代）
python $eng "$S\B_dynamic\sample_good" --evidence-json "$S\B_dynamic\out1.json"
python $eng "$S\B_dynamic\sample_good" --evidence-json "$S\B_dynamic\out2.json"
python $eng "$S\B_dynamic\sample_good" --evidence-json "$S\B_dynamic\r3.json"
python "$S\B_dynamic\analyze_q3q5.py"    # 期望 score/dims/findings/fingerprint 全 identical=True

# 3 Q3 跨路径稳定性
python $eng "$S\B_dynamic\copyA" --evidence-json "$S\B_dynamic\out3.json"
python $eng "$S\B_dynamic\copyA_deep\copyA" --evidence-json "$S\B_dynamic\out4.json"

# 4 Q2 fail-open 实证
python $eng "$S\B_dynamic\case_empty"            # 期望 67/100 C，EXIT=0
python $eng "$S\B_dynamic\case_empty_md"         # 期望 61/100 C，EXIT=0
python $eng "$S\B_dynamic\case_empty" --fail-under 60   # 期望 PASS，EXIT=0
python $eng "$S\B_dynamic\case_bad_md"           # 期望 UnicodeDecodeError traceback，EXIT=1
python $eng "$S\B_dynamic\does_not_exist"        # 期望 EXIT=1

# 5 Q4/Q6 恶意样本双侧对照（P0-1 / P0-2）
python $eng  "$S\C_bench\s2-env-exfil" --fail-under 80          # 期望 89/A 且 EXIT=0（漏报）
python $gate scan "$S\C_bench\s2-env-exfil" --format json       # 期望 trust_score=100 A+、仅 INFO
python $eng  "$S\C_bench\s4-ssh-write"  --fail-under 80         # 期望 89/A 且 EXIT=0（漏报）
python $gate scan "$S\C_bench\s4-ssh-write" --format json       # 期望 trust_score=100 A+、0 findings
python $gate scan "$S\C_bench\s1-cmd-injection" --format json   # 期望 2 CRITICAL、EXIT=1（检出）

# 6 Q7 第三方复现
python -m venv "$S\B_dynamic\.venv_q7"
& "$S\B_dynamic\.venv_q7\Scripts\python.exe" -m pip list        # 期望只有 pip
& "$S\B_dynamic\.venv_q7\Scripts\python.exe" $eng "$S\B_dynamic\sample_good" --evidence-json "$S\B_dynamic\venv_out.json"

# 7 P1-3 入口崩溃（只读调用，不写仓库）
python "$R\skills\lgd-eval\scripts\autofix.py" "$S\C_bench\s6-clean-notes" --dry-run   # 期望 ValueError: expected 5

# 8 P1-5 自评口径复现
python $eng "$R\skills\lgd-eval"                                             # 期望 100/100 A+ EXIT=0
python $gate scan "$R\skills\lgd-eval" --format json                         # 期望 86/A、10 findings（≠ benchmarks 声明的 0/100）
```

**证据留存位置**
- 片段原文：`<project-dir>\_audit_fragments\`（`A_static.md`、`B_dynamic.md`、`C_bench.md`、`_FORMAT_SPEC.md`、`_ORGANIZER_FACTS.md`）
- 动态证据：`_audit_scratch\B_dynamic\`（`out1~out4.json`、`r3.json`、`venv_out.json`、`analyze_q3q5.py`、`analysis_q3q5.txt`、`q2_*.log`、`q7_venv.log`）
- 样本与标注：`_audit_scratch\C_bench\`（6 个样本目录、`_annotations_pre_engine.md`（先于引擎）、`_logs\`）

---

## 附录 A：口径与边界声明

1. **所有"未命中"结论只针对静态规则快筛**。两引擎均不运行被测技能、不做运行期观测、不解码还原载荷（`skills/lgd-eval/SKILL.md:97-111` 自述）。运行期沙箱是否也会漏，本轮**未验证**。
2. **CI 通过不等于安全成立**：本仓 `pytest` 实测 4 passed，只覆盖副本一致性与评分卡契约（`test_copy_parity.py`、`test_scorecard_contract.py`），不覆盖任何检出能力。
3. **作者自证未采信**：`benchmarks/README.md` 的「人工复核误报 0」、`BENCHMARK_RESEARCH.md` 的第三方采用数据均未作为本报告证据；本报告的检出/漏报结论全部来自审计方自建样本与实测输出。
4. **N=6 定性基准**：不外推检出率/漏报率百分比，不对真实生态投毒包做任何统计判断。
5. **未验证范围**：外部 gate action 内部逻辑、`--llm-review`（未配凭证）、`--sandbox`（未启 docker/unshare）、跨 OS / 跨 Python 小版本一致性、JS/TS 与 shell 脚本扫描路径。
6. **作者已自认的缺口**（与本报告独立结论一致，避免误当新发现）：`SPEC.md:33` 明确写「恶意样本不外发 → 检测能力只到 L1」「评测器自身无对照基准 → 分数准不准无法外部检验」。
