# XLGD_SUPPLY_CHAIN_SECURITY_AUDIT（供应链与发布安全审计 · 2026-11-21）

> 范围：`uibc-core`（13 个 workflow，实查）+ 其余 4 个克隆的依赖与许可证（点查）。**只用只读命令；任何 workflow/权限/secret 修改都需单独批准。**
> 结论先行：**"钉 SHA、最小权限、OIDC、attestation"做得相当好；最大的洞是"标签一推即发布，且无审批人、无评审要求"。**

## 一、逐项结论

| # | 检查项 | 结论 | 证据（V/P） |
|---|---|---|---|
| 1 | GitHub Actions 权限 | **良好** | 每个 workflow 显式 `permissions:`；默认 `contents: read`；仅 provenance/publish 有 `id-token: write` |
| 2 | CI Token | **良好** | 无 `write-all`；未用 PAT，走 OIDC |
| 3 | Release Workflow | **有风险** | `publish-pypi.yml`：`on: push tags: v*` / `release` / `workflow_dispatch`；`publish-mcp.yml`：`tags: v*.*.*` |
| 4 | PyPI 发布 | **可未经审批触发** | job `environment: pypi`，但 API 返回 `protection_rules: []` → **无必需审批人**（V） |
| 5 | npm 发布 | **不存在** | 13 个 workflow 中无 npm（V） |
| 6 | 依赖钉版 | **参差** | `uibc-core` pyproject：2 处 `==`、4 处范围；`lgd-engine`/`synomos`：未见钉版（P，正则近似） |
| 7 | 依赖漏洞 | **有扫描** | `security-baseline.yml` + Dependabot（github-actions + pip，weekly，V） |
| 8 | Secret 暴露 | **顶层未发现** | 4 仓顶层关键词扫描 0 命中（限顶层，P）；`PYPI_API_TOKEN` 作为 OIDC 失败兜底存在（V） |
| 9 | Provenance | **有** | `build-provenance.yml` 用 `attest-build-provenance` + OIDC（V） |
| 10 | 制品完整性 | **有** | `release-integrity.yml` 定期校验；发布后有"Verify the version is actually on PyPI"步骤（V，含"publish said success but published nothing"的防护） |
| 11 | 签名发布 | **有**（sigstore 路径） | attestation + Rekor 锚定 |
| 12 | SBOM | **无** | workflow 中无 cyclonedx/syft 关键词（V） |
| 13 | 可重现构建 | **未证明** | 无 `SOURCE_DATE_EPOCH` / 双跑比对 |
| 14 | 维护者权限 | **单人全权** | 分支保护 `required_approving_review_count = null`（0 人）、`enforce_admins=true`、`strict=true`、2 个必需检查、禁强推（V） |
| 15 | 分支保护 | **部分** | 有强推保护与状态检查；**无评审要求** → 单人可直接推 main |
| 16 | Dependabot | **有** | 双生态 weekly（V） |
| 17 | 发布回滚 | **弱** | 未见回滚 workflow；PyPI 只能 yank（需人工） |
| 18 | `pull_request_target` | **未使用（好）** | 关键词 0 命中（V） |

## 二、五个关键问题的直接回答

1. **Tag 能否触发未经批准的发布？** **能（V）**：`v*` tag → publish-pypi（`environment: pypi` 无 protection rules）。这是本条审计最需要处理的一项。
2. **Workflow 是否有不必要的写权限？** 基本没有；`id-token: write` 仅在两处，属必要。
3. **PR 能否影响发布流程？** 不能直接影响（发布由 tag/release 触发）；但 PR 可改 workflow 文件本身——**因无评审要求，改 workflow 的 PR 也可被自己直接合并**（结构性风险）。
4. **是否存在 Secrets 暴露？** 顶层未见；但 `PYPI_API_TOKEN` 长期存在（与 Trusted Publishing 并行），令牌泄露面大于纯 OIDC。
5. **发布物能否对应源码与提交？** 能：attestation + `reproduce` 字段 + 版本校验步骤；但**无 SBOM、无重现构建**，仍不是完整 SLSA 级溯源。

## 三、风险分级与建议（均需批准后执行）

| 级别 | 项 | 建议 |
|---|---|---|
| **高** | pypi 环境无审批人 | 给 `pypi` 环境加 required reviewers（1 人）；或改为仅 `workflow_dispatch` + tag 双条件 |
| **高** | 主分支 0 评审 | 设 `required_approving_review_count=1`（需第二名 maintainer，回到 R1） |
| 中 | `PYPI_API_TOKEN` 兜底 | 改为纯 Trusted Publishing，删除长期令牌 |
| 中 | 无 SBOM | 发布时生成 CycloneDX，随 release 附件 |
| 中 | 依赖未钉版（lgd-engine/synomos） | 加 `requirements.lock` 或上限约束 |
| 低 | 无重现构建 | 双跑比对 + `SOURCE_DATE_EPOCH` |
| 低 | 无回滚流程 | 写 `ROLLBACK.md`（yank + 撤回 release + 通知） |

## 四、必须承认的局限

- Secret 扫描只覆盖顶层文件，**未递归全仓**（P）；
- 代码中的漏洞扫描（CodeQL/Scorecard）存在，但本审计**未读其结果页**（N）；
- 依赖钉版结论来自正则近似，**未解析依赖树**（P）。

> 诚实条款：供应链"工程实践"这一块是本生态**做得最好的部分之一**（钉 SHA、OIDC、attestation、校验"说成功但没发布"），但"发布审批"这一环是空的——这两件事必须分开说，不能互相背书。
