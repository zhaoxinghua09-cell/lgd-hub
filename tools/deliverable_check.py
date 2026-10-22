#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""deliverable_check.py — 交付前检查器（专治「同类错误反复犯」）

为什么有这个脚本
----------------
2026-10-22 一天里，同一个作者（我）在同一类事情上栽了五次，每次都被外部席抓出来：

  1. 行尾归一 —— 用文本模式读写把 CRLF 改成 LF，8 个文件出现 1092/1092 整文件假改动；
  2. 回代残留 —— 用 re.search 手工拼接替换，模板里的 \\1 被当字面量写进 HTML，
     线上「自己验」第一条命令被它吃掉；
  3. 目录链接 —— 文档里写 [AUDITS/](AUDITS/)，Pages 目录无 index.html ⇒ 404；
  4. 自述与产物不符 —— 占位符写「81 张」，实际只折叠了 72 张；
  5. 加面不加形态 —— 号称「扫描面从 5 扩到 8」，但新面的自然形态（JSON 值 / SVG 文本节点）
     没进识别逻辑，等于没修。

前三条可以机械检查，第四条只能查已知形态，第五条查不了（要人读代码）。
所以本脚本只做 1/2/3 + 4 的占位符形态，并把「查不了什么」明写出来——不许假装全覆盖。

为什么不接 CI
-------------
第 1 项依赖 git 历史（`git diff --numstat` 对比文件行数），CI 是浅克隆，历史不全，
在 CI 上跑会得到假绿。所以本脚本定位为**本地交付前自检**，不接 CI，也不假装接了。

用法
----
    python tools/deliverable_check.py              # 检查工作区改动集
    python tools/deliverable_check.py --staged     # 只看已暂存
    python tools/deliverable_check.py --selftest   # 变异体自检（必须能失败）
退出码：0 通过 / 1 有问题 / 2 用法错
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKREF_EXACT = re.compile(r"^\\[1-9]$")
BACKREF_CMD = re.compile(r'<span class="cmd">\s*\\[1-9]\s*</span>')
BACKREF_SVG = re.compile(r">\s*\\[1-9]\s*<")
TEXT_EXT = {".md", ".html", ".htm", ".txt", ".svg", ".json"}
LINK_RE = re.compile(r'\]\(([^)\s]+)\)|href="([^"#][^"]*)"')


def git(args):
    return subprocess.run(["git", "-c", "core.quotepath=false", *args],
                          cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")


def changed_files(staged=False):
    args = ["diff", "--numstat"]
    if staged:
        args.append("--cached")
    out = git(args).stdout
    rows = []
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) != 3:
            continue
        add, dele, path = parts
        rows.append((path, add, dele))
    return rows


def check_lineend(files):
    """改动行数占全文件行数比例过高 ⇒ 疑似行尾归一（把整文件重写了一遍）。"""
    fails = []
    for path, add, dele in files:
        p = ROOT / path
        if not p.exists() or p.suffix.lower() not in TEXT_EXT:
            continue
        if not add.isdigit() or not dele.isdigit():
            continue
        a, d = int(add), int(dele)
        try:
            total = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        except Exception:
            continue
        if total < 20 or a + d == 0:
            continue
        if (a + d) >= total * 0.9 and a >= 10:
            fails.append((path, f"改动 {a}+{d} 行 / 全文 {total} 行（≥90%）—— 疑似行尾归一或整文件重写，请核对是否只想改几行"))
    return fails


def check_backref(files):
    fails = []
    for path, _, _ in files:
        p = ROOT / path
        if not p.exists() or p.suffix.lower() not in TEXT_EXT:
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, ln in enumerate(lines, 1):
            s = ln.strip()
            if BACKREF_EXACT.match(s) or BACKREF_CMD.search(ln) or BACKREF_SVG.search(ln):
                fails.append((f"{path}:{i}", f"回代残留「{s[:40]}」"))
    return fails


def check_dirlinks(files):
    """指向目录的链接：目录里没有 index.html 的话，线上就是 404。"""
    fails = []
    for path, _, _ in files:
        p = ROOT / path
        if not p.exists() or p.suffix.lower() not in {".md", ".html", ".htm"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1) or m.group(2) or ""
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("?")[0].split("#")[0]
            if not target.endswith("/"):
                continue
            d = (ROOT / target).resolve()
            if d.is_dir() and not (d / "index.html").exists():
                fails.append((path, f"链接指向目录「{target}」但该目录无 index.html —— 静态托管上会 404"))
    return fails


def check_placeholder_counts(files):
    """已知形态：［此处 N 张…］里的 N 必须等于该区实际卡片数（本仓 index.html 专用）。"""
    fails = []
    p = ROOT / "index.html"
    if not p.exists():
        return fails
    html = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"［此处 (\d+) 张", html):
        claimed = int(m.group(1))
        # 该占位符所在 section 的实际卡片数
        start = html.rfind("<section", 0, m.start())
        end = html.find("</section>", m.start())
        if start < 0 or end < 0:
            continue
        actual = len(re.findall(r'<div class="card">', html[start:end]))
        if claimed != actual:
            fails.append(("index.html", f"占位符写 {claimed} 张，该区实际 {actual} 张"))
    return fails


CHECKS = [
    ("① 行尾归一（整文件重写）", check_lineend),
    ("② 回代残留 \\1-\\9", check_backref),
    ("③ 目录链接（无 index.html 会 404）", check_dirlinks),
    ("④ 占位符数字 vs 实际数", check_placeholder_counts),
]

NOT_COVERED = "「加面不加形态」查不了（要人读代码判断识别逻辑与声明覆盖是否匹配）——不许当成已覆盖。"


def run(staged=False, quiet=False):
    files = changed_files(staged)
    if not quiet:
        print(f"改动集：{len(files)} 个文件（{'已暂存' if staged else '工作区'}）\n")
    total = 0
    for name, fn in CHECKS:
        fails = fn(files)
        total += len(fails)
        status = "PASS" if not fails else f"FAIL {len(fails)}"
        if not quiet:
            print(f"[{status}] {name}")
        for where, why in fails:
            print(f"    {where}: {why}")
    if not quiet:
        print(f"\n未覆盖：{NOT_COVERED}")
        print("\n[PASS] 可机械检查的四类均通过" if total == 0 else f"\n[FAIL] 共 {total} 条，见上")
    return 0 if total == 0 else 1


# ── 变异体自检：每条检查都必须能失败 ────────────────────────────────
MUTANTS = [
    ("行尾归一：把整文件的 CRLF 改成 LF", "lineend"),
    ("回代残留：把一条命令换成 \\1", "backref"),
    ("目录链接：指向无 index.html 的目录", "dirlink"),
    ("占位符数字改错", "placeholder"),
]


def selftest():
    print(f"selftest：{len(MUTANTS)} 种形态，每种都必须让本脚本判红\n")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="dc_selftest_"))
    caught, escaped = 0, []
    try:
        for name, kind in MUTANTS:
            work = tmp / ("case_" + kind)
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            # 造初始化仓库 + 改动
            subprocess.run(["git", "init", "-q"], cwd=work, check=False)
            subprocess.run(["git", "add", "-A"], cwd=work, check=False)
            subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"],
                           cwd=work, check=False)
            if kind == "lineend":
                p = work / "README.md"
                b = p.read_bytes().replace(b"\r\n", b"\n")
                p.write_bytes(b)
            elif kind == "backref":
                p = work / "index.html"
                t = p.read_text(encoding="utf-8", errors="replace")
                t = t.replace('<span class="cmd">python -m unittest discover -s tests</span>', "\\1", 1)
                p.write_text(t, encoding="utf-8")
            elif kind == "dirlink":
                p = work / "README.md"
                p.write_text(p.read_text(encoding="utf-8", errors="replace")
                             + "\n- [假目录](no-such-dir/)\n", encoding="utf-8")
                (work / "no-such-dir").mkdir()
            elif kind == "placeholder":
                # 真实源文件里没有占位符，所以不能靠替换 —— 必须主动注入一个数字错的占位符
                p = work / "index.html"
                t = p.read_text(encoding="utf-8", errors="replace")
                m = re.search(r'(<section[^>]*id="skills"[^>]*>\s*<div class="wrap">)', t)
                if m:
                    t = t[:m.end()] + "［此处 999 张技能卡，注入用］" + t[m.end():]
                p.write_text(t, encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=work, check=False)
            rc = subprocess.run([sys.executable, str(work / "tools" / "deliverable_check.py"), "--staged"],
                                cwd=work, capture_output=True, text=True,
                                encoding="utf-8", errors="replace").returncode
            if rc == 1:
                caught += 1
                print(f"  [CAUGHT] {name}")
            else:
                escaped.append(name)
                print(f"  [ESCAPED] {name}  ← 该形态没被抓住")
        print(f"\n结论：{caught}/{len(MUTANTS)} 种形态被抓住")
        if escaped:
            for e in escaped:
                print("  - 逃逸:", e)
            return 1
        print("[PASS] 四种形态全部可被本脚本判红（负对照成立）")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    args = sys.argv[1:]
    if "selftest" in args:
        return selftest()
    if any(a not in ("--staged", "--quiet") for a in args):
        print(__doc__)
        return 2
    return run(staged="--staged" in args, quiet="--quiet" in args)


if __name__ == "__main__":
    sys.exit(main())
