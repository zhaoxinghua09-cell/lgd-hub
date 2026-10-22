#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""counts_drift_check.py — 数字与「货不对板」门（lgd-hub）

存在理由
--------
2026-10-22 一天内踩到三类错，都是「说了但撑不住」：
  ① 同一个数字散在多个静态面，改一处忘一处（榜单 44 vs 45）；
  ② 页面写「9 域 rubric 全文」，而理论仓里 rubric 产物为 0；
  ③ 许可表把 MIT / CC BY 4.0 都写成 ARR（把开源说成闭源）。
后来又经红队变异测试发现：只做「数字+量词」正则时，7/10 变异体能逃过检查。
所以本门分四段，且自带 selftest（用变异体证明它真会失败）。

  A 跨面数字漂移：以 world.json 的 counts 为唯一真源，扫各散文面。
                 缺省不算错（不是每个面都必须写每个数字），但写了就必须对。
  B 真源内部自洽：counts 与 verify 段期望输出显式配对、徽章 32=16×2、域论文注记。
  C 货不对板：① 禁用说法（产物不存在的宣称）② 许可表 13 仓覆盖 ③ 许可**值**比对
             ④ 分层许可的仓必须同时出现「分层」与「ARR」两类词（防被压成单一许可）。
  D selftest：把已知变异体注入副本，断言本门必须判红（无负对照=无证据）。

用法
----
    python tools/counts_drift_check.py            # 退出码 0=通过 1=有漂移 2=用法错
    python tools/counts_drift_check.py --verbose  # 打印每条命中
    python tools/counts_drift_check.py selftest   # 跑变异体，证明本门会失败
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRUTH = ROOT / "world.json"

PROSE_SURFACES = [
    "README.md", "llms.txt", "index.html", "AGENTS.md",
    "agents.txt", "docs/ecosystem.svg", "CITATION.cff", "codemeta.json",
]

# (正则, counts 键, 同行出现这些词就跳过该匹配)
# 跳过机制：同一行可能合法地出现多个计数（"full library, 109 skills" / "Ran 7 tests"），
# 没有它，好文案会被误判成漂移。
PATTERNS = [
    (r"(\d+)\s*(?:entries|条目)", "list_entries", ()),
    (r"(\d+)\s*(?:PASS|条通过)", "list_passed", ()),
    (r"(\d+)\s*skills\b(?!\s*library)", "skills_marketplace", ("library",)),
    (r"(\d+)\s*(?:个)?精选", "skills_curated", ()),
    (r"精选\s*[:：]?\s*(\d+)", "skills_curated", ()),
    (r"全库\s*[:：]?\s*(\d+)", "skills_library_total", ()),
    (r"(\d+)\s*(?:domain papers|篇域论文|篇理论论文)", "domain_papers", ()),
    (r"(?:domain papers|域论文)\s*[:：]?\s*(\d+)", "domain_papers", ()),
    (r"(\d+)\s*个域码", "domain_codes", ()),
    (r"域码\s*[:：]?\s*(\d+)", "domain_codes", ()),
    (r"(\d+)\s*SVGs?\b", "badge_svgs", ()),
    (r"(\d+)\s*(?:directions|个方向)", "badge_directions", ()),
    (r"(\d+)\s*(?:tests|项测试)", "uibc_core_tests", ("stress", "cross", "compared")),
    (r"(\d+)\s*个场景", "uibc_core_stress_scenarios", ()),
    (r"(\d+)\s*项[^，。\n]{0,10}对拍", "uibc_core_cross_checks", ()),  # 容「70 项规范一致性对拍」这类中间插字
    (r"SF-001\s*(?:…|\.\.\.)?\s*SF-0(\d+)", "silent_failure_patterns", ()),
]

INTERNAL_PAIRS = [
    ("uibc_core_tests", "uibc_core_tests"),
    ("uibc_core_stress_scenarios", "uibc_core_stress"),
    ("uibc_core_cross_checks", "uibc_core_cross_check"),
]

FORBIDDEN_CLAIMS = [
    ("域rubric", "理论仓内 rubric 命名的产物为 0，域论文正文亦不使用该词；技能里确有 rubric，但那是技能产物不是域论文（2026-10-22 审计确认）"),
    ("域化rubric", "同上：没有任何「本域化 rubric」产物"),
]

LICENSE_TABLE_EXPECTED = [
    "lgd-hub", "lgd-theory", "silent-failure-catalog", "lgd-glossary",
    "uibc-core", "LGD", "skill-scorecard", "theoriturgy",
    "lgd-skill-marketplace", "xlgd", "awesome-trusted-agents",
    "agent-skills", "assayance",
]

LICENSE_EXPECTED = {
    "lgd-hub": "All Rights Reserved",
    "lgd-theory": "All Rights Reserved",
    "silent-failure-catalog": "MIT",
    "lgd-glossary": "CC BY 4.0",
    "uibc-core": "Apache-2.0",
    "LGD": "Apache-2.0",
    "skill-scorecard": "Apache-2.0",
    "theoriturgy": "Apache-2.0",
    "lgd-skill-marketplace": "MIT",
    "xlgd": "MIT",
    "awesome-trusted-agents": "MIT",
    "agent-skills": "MIT",
    "assayance": "Theory Names and Definitions License",
}

LICENSE_EXPECTED_MD = {
    "lgd-hub": ["保留所有权利"],
    "lgd-theory": ["保留所有权利"],
    "silent-failure-catalog": ["MIT"],
    "lgd-glossary": ["CC BY 4.0"],
    "uibc-core": ["Apache-2.0"],
    "LGD": ["Apache-2.0"],
    "skill-scorecard": ["Apache-2.0"],
    "theoriturgy": ["Apache-2.0"],
    "lgd-skill-marketplace": ["MIT"],
    "xlgd": ["MIT"],
    "awesome-trusted-agents": ["MIT"],
    "agent-skills": ["MIT"],
    "assayance": ["Theory Names and Definitions License"],
}

# 分层许可的仓：说法里必须同时出现「分层」和「ARR/保留所有权利」两类词。
# 没有这条，把「代码 MIT + 正文 ARR」压成单一许可（红队变异体 #6）就能过门。
LAYERED_REQUIRED = {
    "silent-failure-catalog": (r"分层|layered", r"保留所有权利|All Rights Reserved|ARR"),
    "agent-skills": (r"分层|layered", r"保留所有权利|All Rights Reserved|ARR"),
    "uibc-core": (r"分层|layered", r"保留所有权利|All Rights Reserved|ARR"),
}


def load_truth():
    d = json.loads(TRUTH.read_text(encoding="utf-8"))
    c = dict(d["counts"])
    c["list_entries"] = 45
    c["list_passed"] = 43
    return d, c


def check_prose(truth, verbose):
    fails, hits = [], 0
    for name in PROSE_SURFACES:
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for rx, key, skip_words in PATTERNS:
            if key not in truth:
                continue
            for m in re.finditer(rx, text):
                ls = text.rfind("\n", 0, m.start()) + 1
                le = text.find("\n", m.end())
                line_txt = text[ls: le if le > 0 else len(text)].lower()
                if any(w in line_txt for w in skip_words):
                    continue
                hits += 1
                got, want = int(m.group(1)), truth[key]
                line = text[: m.start()].count("\n") + 1
                snip = text[max(0, m.start() - 30): m.end() + 20].replace("\n", " ")
                if got != want:
                    fails.append((name, line, key, got, want, snip))
                elif verbose:
                    print(f"[ok] {name}:{line} {key}={got}")
    return hits, fails


def check_internal(doc, truth):
    fails = []
    verify = doc.get("verify", {})
    for ckey, vkey in INTERNAL_PAIRS:
        want = truth.get(ckey)
        exp = verify.get(vkey, {}).get("expected", "")
        if want is None:
            fails.append((vkey, "counts 缺键 " + ckey))
        elif str(want) not in exp:
            fails.append((vkey, f"counts.{ckey}={want}，verify.{vkey}.expected=「{exp}」"))
    if truth.get("badge_svgs") != truth.get("badge_directions", 0) * 2:
        fails.append(("badge", f"badge_svgs={truth.get('badge_svgs')} ≠ badge_directions×2"))
    if "#11" not in doc.get("counts", {}).get("domain_papers_note", ""):
        fails.append(("domain_papers_note", "未写明 #11 未发布"))
    return fails


def check_claims(doc):
    fails = []
    prose_files = ["README.md", "index.html", "llms.txt", "AGENTS.md", "agents.txt"]
    for name in prose_files:
        p = ROOT / name
        if not p.exists():
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        compact = re.sub(r"\s+", "", raw.lower())
        for word, why in FORBIDDEN_CLAIMS:
            key = re.sub(r"\s+", "", word.lower())
            if key in compact:
                line = next((i + 1 for i, ln in enumerate(raw.splitlines())
                             if re.sub(r"\s+", "", ln.lower()).find(key) >= 0), 0)
                fails.append((f"{name}:{line}", f"出现禁用说法「{word}」——{why}"))

    # 回代残留：编辑脚本用 re.search 手动拼接时，替换模板里的 \\1 可能被当字面量写进文件。
    # 2026-10-22 实测发生过一次（验真卡的主命令被一条 \\1 吃掉，线上可见）。
    #
    # 2026-10-22 红队 Q2 修正：初版用 r"\\[1-9]" 直接搜整行，会误伤合法写法
    #   （`解压到 C://Users//1//lgd-hub`、`sed -E 's/x([0-9]+)/y\1/'`），
    # 而且只扫 5 个面，漏了 world.json 与 docs/ecosystem.svg。
    # 现在：① 只认「整行就是一个回代」或「回代被 cmd 样式包着」两种形态；
    #       ② 扫描面与 A 段对齐（PROSE_SURFACES 8 面）；
    #       ③ selftest 同时有正例（必须判红）与反例（必须不判红）。
    for name in PROSE_SURFACES:
        p2 = ROOT / name
        if not p2.exists():
            continue
        for i, ln in enumerate(p2.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = ln.strip()
            if re.fullmatch(r"\\[1-9]", s) or re.search(r'<span class="cmd">\s*\\[1-9]\s*</span>', ln):
                fails.append((f"{name}:{i}", f"出现回代残留「{s[:40]}」——替换模板未展开"))
            # 形态三：XML/SVG 文本节点，如 <text>\1</text>（2026-10-23 复核 R2）
            if re.search(r">\s*\\[1-9]\s*<", ln):
                fails.append((f"{name}:{i}", f"SVG/XML 文本节点是回代残留「{s[:40]}」"))

    # 形态四：JSON 字符串值本身就是回代残留（2026-10-23 复核 R1）
    # 只加扫描面不加形态等于没修：world.json 里的自然形态是 "cmd": "\\1"，
    # 既不是整行、也没有 cmd 样式包着，旧断言全部放行。
    for jf in ("world.json", "codemeta.json", "package.json"):
        jp = ROOT / jf
        if not jp.exists():
            continue
        try:
            jdata = json.loads(jp.read_text(encoding="utf-8"))
        except Exception:
            continue
        stack2 = [(jf, jdata)]
        while stack2:
            jpath, node = stack2.pop()
            if isinstance(node, str):
                if re.fullmatch(r"\\[1-9]", node.strip()):
                    fails.append((jpath, f"JSON 字符串值就是回代残留「{node.strip()}」"))
            elif isinstance(node, dict):
                stack2.extend((f"{jpath}.{k}", v) for k, v in node.items())
            elif isinstance(node, list):
                stack2.extend((f"{jpath}[{i2}]", v) for i2, v in enumerate(node))

    by_repo = doc.get("license", {}).get("by_repo", {})
    for r in LICENSE_TABLE_EXPECTED:
        if r not in by_repo:
            fails.append(("world.json license.by_repo", f"缺仓：{r}"))
    for repo, expect in LICENSE_EXPECTED.items():
        val = by_repo.get(repo, "")
        if expect.lower() not in str(val).lower():
            fails.append((f"world.json by_repo[{repo}]", f"写的是「{val}」，应含「{expect}」"))

    notice = ROOT / "NOTICE.md"
    if notice.exists():
        ntext = notice.read_text(encoding="utf-8", errors="replace")
        rows = [ln for ln in ntext.splitlines() if ln.strip().startswith("|")]
        for repo, expect in LICENSE_EXPECTED_MD.items():
            row = next((ln for ln in rows if f"`{repo}`" in ln), "")
            if not row:
                fails.append((f"NOTICE.md 表[{repo}]", "表格里没有这一行"))
            elif not any(k.lower() in row.lower() for k in expect):
                fails.append((f"NOTICE.md 表[{repo}]", f"该行未写 {expect}：{row.strip()[:80]}"))

    # 分层许可：JSON 值与 NOTICE 行都必须同时含「分层」与「ARR」两类词
    for repo, (lay_pat, arr_pat) in LAYERED_REQUIRED.items():
        val = str(by_repo.get(repo, ""))
        if not (re.search(lay_pat, val, re.I) and re.search(arr_pat, val, re.I)):
            fails.append((f"world.json by_repo[{repo}]", f"分层许可被压成单一：{val[:80]}"))
        if notice.exists():
            row = next((ln for ln in rows if f"`{repo}`" in ln), "")
            if row and not (re.search(lay_pat, row, re.I) and re.search(arr_pat, row, re.I)):
                fails.append((f"NOTICE.md 表[{repo}]", f"分层许可被压成单一：{row.strip()[:80]}"))
    return fails


def run_all(verbose=False, quiet=False):
    doc, truth = load_truth()
    hits, pf = check_prose(truth, verbose)
    inf = check_internal(doc, truth)
    cf = check_claims(doc)
    if not quiet:
        print(f"\nA 段·跨面：扫描 {len(PROSE_SURFACES)} 面 / 命中 {hits} 条 / 真源 {TRUTH.name}")
        print(f"B 段·内部：配对 {len(INTERNAL_PAIRS)} 组 + 徽章倍数 + 域论文注记")
        print(f"C 段·货不对板：禁用说法 {len(FORBIDDEN_CLAIMS)} 条 + 许可 {len(LICENSE_TABLE_EXPECTED)} 仓覆盖/值/分层三类")
    if pf:
        print(f"\n[FAIL] A 段漂移 {len(pf)} 条：")
        for name, line, key, got, want, snip in pf:
            print(f"  {name}:{line}  {key}: 写的是 {got}，真源是 {want}")
            print(f"      原文：…{snip.strip()}…")
    if inf:
        print(f"\n[FAIL] B 段内部不一致 {len(inf)} 条：")
        for k, why in inf:
            print(f"  {k}: {why}")
    if cf:
        print(f"\n[FAIL] C 段货不对板 {len(cf)} 条：")
        for w, why in cf:
            print(f"  {w}: {why}")
    total = len(pf) + len(inf) + len(cf)
    if total:
        return 1
    if not quiet:
        print("\n[PASS] 数字一致 + 真源自洽 + 无「产物不存在」类宣称 + 许可覆盖/值/分层全对")
    return 0


# ── D 段：selftest（变异体）──────────────────────────────────────────────
# 每个变异体都必须让本门判红。变异体取自 2026-10-22 红队实测逃过旧版的那批。
MUTANTS = [
    ("精选 81 → 910（index）", "index.html", "精选 81 个", "精选 910 个"),
    ("全库 109 → 190（index）", "index.html", "全库 109", "全库 190"),
    ("domain papers 13 → 23（world）", "world.json", '"domain_papers": 13', '"domain_papers": 23'),
    ("70 项对拍 → 99（index）", "index.html", "70 项规范一致性对拍", "99 项规范一致性对拍"),
    ("12 个域码 → 9（index）", "index.html", "12 个域码", "9 个域码"),
    ("agent-skills 分层 → 纯 MIT（NOTICE）", "NOTICE.md",
     "| `agent-skills` | **分层**：可执行代码 MIT，SKILL.md / README / 理论文本保留所有权利 |",
     "| `agent-skills` | MIT |"),
    ("uibc-core 分层 → 单一 Apache-2.0（world）", "world.json",
     "layered — code Apache-2.0, theory text / methodology / normative statements All Rights Reserved (its NOTICE.md states this)",
     "Apache-2.0"),
    ("榜单 45 → 44（README）", "README.md", "首批 45 条目", "首批 44 条目"),
    ("lgd-glossary CC BY → ARR（world）", "world.json", "CC BY 4.0 (commercial use allowed with attribution)", "All Rights Reserved"),
    ("151 项测试 → 999（index）", "index.html", "151 项测试", "999 项测试"),
    ("命令被回代残留吃掉（index）", "index.html", "<span class=\"cmd\">python -m unittest discover -s tests</span>", "\\1"),
]


# 反例：形似回代残留、但属合法写法，必须**不**判红（误报对照）。
# 2026-10-22 红队 Q2 实测：初版断言对这两类合法写法误伤，故固化为反例。
NEGATIVE_MUTANTS = [
    ("合法 Windows 路径 C:\\Users\\1", "README.md", "## 联系 / Contact",
     r"解压到 C:\Users\1\lgd-hub 即可" + "\n\n## 联系 / Contact"),
    ("合法的 sed 反向引用", "README.md", "## 联系 / Contact",
     r"sed -E 's/x([0-9]+)/y\1/' file" + "\n\n## 联系 / Contact"),
]


# 2026-10-23 复核席 R1/R2：只加扫描面不加识别形态等于没修。
# 补两个「文件里的自然形态」变异体：JSON 字符串值、SVG 文本节点。
_BS = chr(92)
MUTANTS += [
    ("world.json 的 command 变成回代残留", "world.json",
     '"command": "python -m unittest discover -s tests"',
     '"command": "' + _BS + _BS + '1"'),
    ("SVG 文本节点变成回代残留", "docs/ecosystem.svg",
     "<text", "<text>" + _BS + "1</text><text"),
]


def selftest():
    total = len(MUTANTS)
    print(f"selftest：{total} 个变异体（必须判红）+ {len(NEGATIVE_MUTANTS)} 个反例（必须不判红）\n")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="lgd_mut_"))
    escaped, caught, false_pos = [], 0, []

    def make_case(tag):
        # 每个用例一个独立目录：不覆盖、不删除，因此不需要任何 destructive 操作
        work = tmp / ("case_" + re.sub(r"[^0-9A-Za-z]+", "_", tag))
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return work

    def run_case(name, fname, old, new, expect_fail):
        work = make_case(name)
        target = work / fname
        if not target.exists():
            print(f"  [SKIP] {name} —— {fname} 不存在")
            return None
        text = target.read_text(encoding="utf-8", errors="replace")
        if old not in text:
            print(f"  [SKIP] {name} —— 锚点未命中（文案已变，需更新用例）")
            return None
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        rc = subprocess.run([sys.executable, str(work / "tools" / "counts_drift_check.py")],
                            capture_output=True, text=True, encoding="utf-8", errors="replace").returncode
        if expect_fail:
            if rc == 1:
                print(f"  [CAUGHT] {name}")
                return True
            print(f"  [ESCAPED] {name}  ← 门没拦住，需补断言")
            escaped.append(name)
            return False
        if rc == 0:
            print(f"  [OK-NEG] {name} —— 合法写法未误报")
            return True
        print(f"  [FALSE-POSITIVE] {name}  ← 合法写法被误判为违规")
        false_pos.append(name)
        return False

    try:
        for name, fname, old, new in MUTANTS:
            if run_case(name, fname, old, new, True):
                caught += 1
        for name, fname, old, new in NEGATIVE_MUTANTS:
            run_case(name, fname, old, new, False)
        print(f"\n结论：{caught}/{total} 个变异体被拦下；反例误报 {len(false_pos)}/{len(NEGATIVE_MUTANTS)}")
        if escaped or false_pos:
            print("问题清单：")
            for e in escaped:
                print("  - 逃逸:", e)
            for e in false_pos:
                print("  - 误报:", e)
            return 1
        print("[PASS] 全变异体判红 + 全反例不判红（双向负对照成立）")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    args = sys.argv[1:]
    if "selftest" in args:
        return selftest()
    unknown = [a for a in args if a not in ("--verbose", "--quiet")]
    if unknown:
        print(f"[ERROR] 未知参数 {unknown}；用法：counts_drift_check.py [--verbose] [selftest]")
        return 2
    return run_all(verbose="--verbose" in args)


if __name__ == "__main__":
    sys.exit(main())
