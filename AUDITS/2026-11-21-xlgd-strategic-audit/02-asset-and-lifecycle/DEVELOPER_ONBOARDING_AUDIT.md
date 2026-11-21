# DEVELOPER_ONBOARDING_AUDIT（真实开发者接入审计 · 2026-11-21）

> 方法说明（重要）：本审计分两层。
> **L1 实查（V/P）**：本日实际 clone、安装、运行、调用得到的结果（uibc-core / lgd-engine / LGD-Eval / synomosai-governance-mcp 四仓为实测；其余为读过 README 与文件树）。
> **L2 评分（I）**：十项 rubic 依据 README/文件是否存在打分，**未对 10 仓逐一真跑**，因此分数是"文档可得性"而非"实际可跑通性"，置信度低，只用于排序。
> 十项 = 安装命令、快速开始、最小可运行示例、预期输出、失败案例、机器可读输出、CLI/API 明确、测试可跑、Windows 适配、FAQ/排障。

## 一、评分表（0–10，越高越好；分数为 L2 评分，括号内为 L1 实测补充）

| 仓库 | 分 | 缺什么（直接影响新人） | L1 实测 |
|---|---|---|---|
| `uibc-core` | **8** | Windows 说明、FAQ | 实测：clone 后 `python -m unittest discover tests` = **1015 tests 通过**（159 s），但**先要修 PATH**——本机 `git` 指向 `.cmd` 包装，2 个测试直接 `FileNotFoundError`；把真 `git.exe` 目录前置后才全绿 |
| `lgd-engine` | **8** | 机器可读输出、FAQ | 实测：`pytest -q` = **89 passed / 5 skipped / 212 subtests**；`docs/validate_openapi.py` = 20/20，但 README 写 17 项 |
| `silent-failure-catalog` | **8** | 版本号、许可证 | 实读：16 个编号案例 + `patterns.json`，结构对新人友好；无版本文件 |
| `lgd-theory` | **7** | 可执行入口、许可证 | 实读：纯文档为主，新人"读完不知道下一步跑什么" |
| `LGD-Eval` | **5** | 预期输出、失败案例、Windows、FAQ | 实测：根 `pytest tests` = 4 passed（0.08 s），但 4 个包装入口必崩（5 元组解包 6 元组）；空目录给 67/C 且 exit 0 |
| `lgd-gate` | **5** | 安装与退出语义 | 只在 CI action 场景被用，本地无法独立跑 |
| `synomosai-governance-mcp` | **4** | 安装命令、最小示例、FAQ | 实测：stdio 握手 OK、6 工具可调；但 PyPI `requires_dist=None`，接入方不知道装什么；近一日下载 **2 次** |
| `assayance` | **4** | 几乎全部（无 tests、无版本） | 实读 |
| `uibc-competition` | **3** | 无安装/无示例/无许可证 | 实读 |
| `lgd-hub` | **2** | 无版本、无安装、无示例 | 实读；#77 记录"邀请 02–05 未计入" |

## 二、一个新人真实的 30 分钟路径（按现状推演，I）

1. 搜 "LGD / UIBC" → 命中 `lgd-theory`（7 star，纯理论）或 `lgd-hub`（3 star，导航）。
2. 从导航进 `uibc-core`（12 star）→ README 清楚，`pip install` 正常。
3. 跑测试 → **在 Windows 上大概率先撞 PATH 的 `.cmd` 问题**（本机已验证），需要自己修，README 没写。
4. 想验一个证据包 → 工具要求 `cryptography`，**没装时仍然 exit 0 且 `verified=true`**（本机无 site-packages venv 实测），新人会以为"验过了"，其实签名没验。
5. 想知道"这算不算通过安全" → README 的 L0–L5 权限档会被读成授权规则，实际是分数映射。
6. 去评价自己写的 skill → 到 `LGD-Eval`，发现 5 个仓（engine/gate/protocol/evidence/reports）不知从哪个开始；README 的徽标数字与 benchmarks 页不一致。
7. 想引用/复用 → 38 个仓 NOASSERTION、15 个无许可证，**法律上不能用**。
8. 放弃点最可能出现在第 4–7 步之间（**I**，依据是"缺预期输出 + 许可证不明 + 入口分散"三项同时出现）。

## 三、十个阻断项（按修复成本排序）

| 优先级 | 阻断项 | 影响 | 修复成本 |
|---|---|---|---|
| 1 | 许可证不明（38 NOASSERTION + 15 无证） | 企业法务直接否决 | 低（加 LICENSE 文件） |
| 2 | 缺 `cryptography` 时仍 `verified=true` | 产生"假通过"，比缺功能更危险 | 低（一行判定） |
| 3 | Windows 下 `git` 子进程失败无提示 | 新人在第一步就失败 | 低（PATH 兜底 + README） |
| 4 | 四个包装入口元组崩溃 | 任何脚本化调用都失败 | 低（改解包） |
| 5 | LGD-Eval 空对象 fail-open | 门禁形同虚设 | 中（加三值态） |
| 6 | 评测家族 5 仓无入口顺序 | 新人不知从哪开始 | 低（README 互链） |
| 7 | 徽标/文档数字与实测不一致 | 降低可信度 | 低 |
| 8 | 缺"预期输出"段落 | 无法判断成功 | 低 |
| 9 | MCP 包无依赖声明 | 安装不可复现 | 低 |
| 10 | 无 FAQ/排障 | 每个新人都重复踩坑 | 中 |

## 四、"5 分钟可跑通"目标（建议的最小验收）

一个没读过任何文档的开发者，在干净机器上：
1. `pip install uibc-core`（或 clone）→ 一条命令跑通示例；
2. 看到**明确的预期输出**（含退出码与关键字段）；
3. 能看到**至少一条会失败的例子**，并知道为什么失败；
4. 能拿到一个**机器可读结果**（JSON），可粘进自己的流水线；
5. 不需要装可选依赖就能得到**诚实的结论**（缺签名时明确说"签名未验证"，而不是 `verified=true`）。

当前 5 项里，1 通过、2 部分、3 无、4 部分、5 不通过（本机实测）。这就是 DX 的真实分数。

## 五、结论

- 纸面（L2）看，uibc-core / lgd-engine / silent-failure-catalog 已达"像样开源项目"的 8 分。
- 实跑（L1）看，**Windows 路径、可选依赖的假通过、评测入口分散**三件事会把新人挡在门外；其中"假通过"最伤信任。
- 所以"开发者体验"当前不是排版问题，而是**正确性问题**：工具在没验签名时说自己验过了。修这一条，比写十篇 quickstart 有效。
