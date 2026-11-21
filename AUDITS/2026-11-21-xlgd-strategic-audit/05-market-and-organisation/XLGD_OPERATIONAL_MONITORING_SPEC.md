# XLGD_OPERATIONAL_MONITORING_SPEC（自动化运营与异常预警规范 · 2026-11-21）

> 边界：**自动化只做"发现 + 分析 + 建议"，不做任何写操作。** 不自动合并、不发布、不改权限、不联系第三方、不提交文件。
> 依据：本生态已有只读巡检习惯（bootstrap `--check`、`status_page.py --check`、`weknora_sync_state.json`），本规范把它们统一成"事件 → 告警 → 建议"。

## 一、监控对象（14 类，按成本）

| # | 事件 | 来源 | 频率 | 严重度规则 |
|---|---|---|---|---|
| 1 | 核心仓新提交 | GitHub API | 每日 | 影响协议/证据 → HIGH |
| 2 | 新 Issue | GitHub API | 每日 | 标注 `trust` → HIGH |
| 3 | 新 PR | GitHub API | 每日 | 外部人提交 → HIGH（首次外部贡献） |
| 4 | CI 失败 | Actions API | 每日 | main 分支 → HIGH |
| 5 | 依赖漏洞 | Dependabot/OSV | 每日 | 有可用修复 → MED |
| 6 | 发布变化 | Releases API | 每日 | 新 tag → MED（确认是否审批发布） |
| 7 | 文档过期 | 本地比对 | 每周 | 数字与实测不一致 → MED |
| 8 | 版本不兼容 | 契约测试 | 每周 | 旧收据验不过 → HIGH |
| 9 | 许可证变化 | GitHub API license | 每周 | SPDX 变化 → HIGH（法律） |
| 10 | 外部引用 | 搜索 + 反向链接 | 每周 | 新引用 → MED |
| 11 | 新第三方集成 | 仓库/文档关键词 | 每周 | 出现在别人项目 → HIGH（最重要信号） |
| 12 | 竞品新产品 | `COMPETITIVE_INTELLIGENCE_LOG.md` 来源 | 每周 | 直接重叠 → HIGH |
| 13 | 标准工作组动态 | 邮件列表 | 每周 | 与我们议题相关 → MED |
| 14 | 商业机会 | 公开渠道 | 每周 | 明确问询 → HIGH |

## 二、告警字段（强制 8 项）

```json
{
  "ts": "2026-11-21T07:00:00Z",
  "asset": "zhaoxinghua09-cell/uibc-core",
  "event": "new_tag",
  "evidence_url": "https://github.com/.../releases/tag/v0.5.1",
  "impact": "published without recorded approval (pypi env has no reviewers)",
  "severity": "HIGH",
  "suggested_action": "verify release approver; if none, add required reviewer",
  "requires_approval": true
}
```

规则：`requires_approval=true` 的事件**只能写进日报**，不得自动执行。

## 三、三条只读巡检（可直接落地）

| 巡检 | 命令/方式 | 输出 | 频率 |
|---|---|---|---|
| 状态巡检 | `python tools/status_page.py --check`（uibc） | `status.json` | 每日 |
| 文档事实 | `python tools/check_doc_facts.py` | 差异列表 | 每周 |
| 发布审计 | `gh api repos/{r}/releases` + 对比 `pypi` 环境 protection | `release_events.jsonl` | 每日 |

> 本机已验证前两条可跑（V）；第三条为本次新增（API 已验证 `protection_rules: []`）。

## 四、异常升级路径

| 级别 | 触发 | 动作 | 谁能做 |
|---|---|---|---|
| P0 | 假通过（G2/G4 类）/ 证据被篡改 / 未批准发布 | 立即日报 + 建议暂停对外表述 | **Steven** |
| P1 | CI 红、契约测试失败、许可变化 | 当日日报 + 修复建议 | Steven/AI 起草 |
| P2 | 文档过期、依赖更新、外部引用 | 周报汇总 | AI |

## 五、实施方式（不新增系统）

- 复用现有 cron（每日 1 次，只读，≤3 并发）；
- 输出统一 `monitor_events.jsonl` + 一页 Markdown 日报；
- **不新增仓库**，脚本放在现有仓 `tools/` 下（需批准）。

## 六、验收判据

1. 连续 7 天产出日报，且每条告警都有 `evidence_url`；
2. 无一条告警触发写操作；
3. 出现"新 tag 未经审批"时能在 24 小时内报出（这是当前最需要的）。

## 七、不做的事

- 不自动回复 issue、不自动合并 PR、不自动发帖；
- 不做"全网情感监控"（无价值）；
- 不抓非公开数据。
