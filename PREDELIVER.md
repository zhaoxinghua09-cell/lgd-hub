# 发布前检查 · PREDELIVER

> 目的：把「发布前要从外人角度全量实测」这件事，从**口头承诺**变成**八项可复跑的检查**。
> 每项都写明「跑什么命令 / 判据 / 失败时说明什么」。跑完把原始输出附在 PR 里，不附结论。

**使用方式**：发布前逐项跑，八项全绿才发。任一项红，先修再跑整轮（不跳项）。

| # | 检查 | 命令 | 判据 |
|---|---|---|---|
| 1 | **数字能被第三方复现** | `python demo/verify.py` | 退出码 0，输出 `151 / 7 / 70` 三项 PASS |
| 2 | **页面数字与真源一致** | `python tools/counts_drift_check.py` | `[PASS]`，且 A 段命中数 > 0（命中 0 说明正则没匹配上，等于没检查） |
| 3 | **这道门本身能失败** | `python tools/counts_drift_check.py selftest` | `N/N 个变异体被拦下；反例误报 0/2` |
| 4 | **结构门** | `python tools/repo_gate_check.py check` | `GREEN`，`0 failed` |
| 5 | **四类编辑事故** | `python tools/deliverable_check.py` | `[PASS] 可机械检查的四类均通过` |
| 6 | **四类事故的检查器能失败** | `python tools/deliverable_check.py --selftest` | `4/4 种形态被抓住` |
| 7 | **线上内容 = 仓库内容** | 见下「第 7 项」 | 逐字节相同；六件机器入口全 200 |
| 8 | **审计归档仍同步** | 见下「第 8 项」 | 三文件 200；八条对照表无遗漏无增补 |

---

## 第 7 项 · 线上与仓库同源

```bash
python - <<'PY'
import pathlib, urllib.request
loc = pathlib.Path("index.html").read_bytes()
live = urllib.request.urlopen("https://zhaoxinghua09-cell.github.io/lgd-hub/", timeout=30).read()
print("本地", len(loc), "线上", len(live), "逐字节相同:", loc == live)
for u in ("world.json", "llms.txt", "AGENTS.md", "agents.txt", "CITATION.cff", "codemeta.json"):
    r = urllib.request.urlopen(f"https://zhaoxinghua09-cell.github.io/lgd-hub/{u}", timeout=20)
    print(f"{u:<16} {r.status}")
PY
```

判据：`逐字节相同: True`，且六件全部 `200`。
**注意**：不要用字节数比对代替逐字节比对——目录链接、CDN 缓存、构建差异都会让字节数变化；也不要拿「HTTP 200」当同源证据（旧版也是 200）。

## 第 8 项 · 审计归档同步

```bash
ls AUDITS/                      # 应有 README.md / .md / .extracted.txt 三份
grep -c "^| " AUDITS/README.md  # 对照表行数
```

判据：三份都在；`AUDITS/README.md` 的八条对照表与 `.extracted.txt` 里的「必须改清单（8 条）」一一对应；`.extracted.txt` 未被改写（改它等于篡改审计原件）。

---

## 不在这八项里的东西（写清楚，不假装覆盖）

- **外部 AI 复评**：不是命令，需人工投喂与复核，见 `外脑投喂_提示词_仅此一段.md` 的做法。
- **「加面不加形态」**：要人读代码判断识别逻辑与声明覆盖是否匹配，机械查不了。
- **外部登记库抽查**（DataCite / SWH / Rekor / ORCID）：这些是抽查性质，脚本化收益低，按需手跑，命令见 `AUDITS/2026-10-22-external-audit.md` 末尾「核验方法留痕」。
- **仓外文件**（兄弟仓的 LICENSE / TRADEMARK）：本仓检查器扫不到，需单独扫一遍兄弟仓——2026-10-22 就因为漏扫 `agent-skills/TRADEMARK.md` 被外部审计抓到。
