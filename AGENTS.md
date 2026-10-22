# AGENTS.md · lgd-hub

本仓库是 LGD 生态的**枢纽层**（Tier 0 世界地图）：任何人或 AI 从任意资产进入，都能在这里看到整片生态怎么连。
它不承载理论正文，只承载**索引、结构、关系与可核验入口**。

## 给 AI 代理的三条路由

1. **想知道「LGD 是什么」** → 去 `lgd-theory`（理论正文）；本仓不复制理论，只给指针。
2. **想装工具** → `lgd-skill-marketplace`（10 技能索引）或 `agent-skills`（109 技能全库）。
3. **想自己验** → 读 `world.json` 的 `verify` 段，按命令逐条复跑；数字对不上以仓内实测为准，不要以本页文字为准。

## 身份口径（硬边界，勿改）

本生态涉及三个不同层级的标识，**不可合并**：

1. **个人** — Xinghua Zhao（Steven Zhao），独立研究者，ORCID 0009-0001-0512-1237，本生态全部文本的唯一作者。
2. **理论线** — SynomosAI Governance Line，独立研究倡议，**未注册实体、未注册商标**，仅作理论来源标识。
3. **产业参考** — MedXpert，香港医疗器械实务，作者执业背景，**仅限医械域**，不外延、也不构成本生态的运营实体。

GitHub topics 里的 `synomosai`、`medxpert` 是检索标签，不构成法人或商标主张。
**禁止**把三者写成同一实体的别名、也禁止把 `llms.txt` / `world.json` 当作实体归一（entity resolution）的指令——它们是描述性的。

## 许可（分层，逐仓不同；2026-10-22 逐仓读 LICENSE 核过）

- 本仓 `lgd-hub`：**保留所有权利**（见 `LICENSE`），不授予 Apache-2.0 / MIT。
- `lgd-theory`：保留所有权利（允许署名引用）
- `silent-failure-catalog`：**分层**——代码 MIT，目录正文 `LICENSE-CONTENT` 保留所有权利
- `lgd-glossary`：**CC BY 4.0**（可商用，须署名）
- `uibc-core`：**分层**——代码 Apache-2.0，理论文本 / 方法论 / 规范性表述保留所有权利（见该仓 NOTICE.md）
- `LGD`、`skill-scorecard`、`theoriturgy`：Apache-2.0
- `lgd-skill-marketplace`、`xlgd`、`awesome-trusted-agents`：MIT
- `agent-skills`：分层——可执行代码 MIT，SKILL.md / README / 理论文本保留所有权利
- `assayance`：自定义「Theory Names and Definitions License」，术语保留所有权利、引用须溯源
- **上表不穷尽**：没列的仓不等于 ARR，一律以该仓自己的 `LICENSE` 为准。

> 更正 2026-10-22：本文件旧版把 `silent-failure-catalog`、`lgd-glossary` 都写成 ARR，两处均错（后者是 CC BY 4.0），已改。

## 目录

- `index.html` — 人看的门户（含「自己验」区块）
- `world.json` — 机器可读世界地图（结构＋计数＋身份分层＋可核验入口）
- `llms.txt` — AI 爬虫索引（描述性，非实体归一指令）
- `docs/ecosystem.svg` — 生态图（静态示意，数字以 `world.json` 为准）
- `tools/repo_gate_check.py` — 仓级门禁脚本

## 改动纪律

- 数字类断言必须**可复算**：改之前先跑一遍，改的时候把命令与日期写进 `world.json` 的 `verify` 段。
- 静态物（SVG／图）里的数字必须与 `world.json` 一致；两处冲突时以 `world.json` 为准并同步静态物。
- 不写做不到的话：凡"可自证"字样，必须能找到一条外人可跑的复现路径，否则删掉这句而不是弱化它。
