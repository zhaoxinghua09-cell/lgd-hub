#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""demo/verify.py — 五分钟自验：把门户上写着的那三条命令真跑一遍，并核对数字。

为什么有这个东西
----------------
门户声称「不要求你相信，只提供你能自己跑一遍的证据」。但在此之前，读者要自己
找仓库、自己找 commit、自己判断输出对不对。这份脚本把这三步固定下来：
克隆 → 切到页面锚定的 commit → 跑三条命令 → **自动比对**页面写的三个数字。

设计约束
--------
1. 只用标准库 + git 命令，不装任何依赖；
2. 三个数字（151 / 7 / 70）写死在这里，**故意不与 world.json 联动**——
   否则源文件被改错时脚本会跟着一起错，失去"独立复现"的意义；
3. 找不到 git 或网络不通时，如实报「无法验证」，不假装通过；
4. 输出 PASS / FAIL 表，任何一项不符即非零退出。

用法
----
    python demo/verify.py                  # 克隆到临时目录，跑完即弃
    python demo/verify.py --keep           # 保留克隆目录，便于自己再看
    python demo/verify.py --dir <path>     # 用已有的 uibc-core 克隆
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

COMMIT = "73f31ccf58df63772cd5fc084839341a2bca31aa"
REPO = "https://github.com/zhaoxinghua09-cell/uibc-core"
# 页面写的三个数字（刻意不读 world.json，见文件头第 2 条）
EXPECT = {
    "unittest": ("Ran 151 tests", 151),
    "stress": ("Ran 7 tests", 7),
    "cross": ("checks compared: 70", 70),
}
CHECKS = [
    ("unittest", ["-m", "unittest", "discover", "-s", "tests"], EXPECT["unittest"]),
    ("stress", ["-m", "unittest", "tests.stress_test"], EXPECT["stress"]),
    ("cross_check", ["independent_verifier/cross_check.py"], EXPECT["cross"]),
]


def run(cmd, cwd, timeout=600):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


def _note(out):
    """失败时给一行可读原因：跳过 ResourceWarning 这类噪音行。"""
    lines = [l.strip() for l in (out or "").splitlines()
             if l.strip() and "Warning" not in l and not l.strip().startswith("File ")]
    return lines[-1][:120] if lines else "无输出"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", help="已有的 uibc-core 克隆")
    ap.add_argument("--keep", action="store_true", help="保留临时克隆")
    a = ap.parse_args()

    source = None
    tmp = None
    if a.dir:
        source = pathlib.Path(a.dir).resolve()
    else:
        if not shutil.which("git"):
            print("[无法验证] 本机没有 git —— 请先安装 git，或手动克隆后加 --dir")
            return 2
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="lgd_demo_"))
        source = tmp / "uibc-core"
        print(f"克隆 {REPO} …")
        r = run(["git", "clone", "-q", REPO, str(source)], cwd=tmp)
        if r.returncode != 0:
            print(f"[无法验证] 克隆失败：{r.stderr.strip()[:200]}")
            print("         （多半是网络问题；换网络或手动克隆后加 --dir）")
            return 2

    try:
        head = run(["git", "rev-parse", "HEAD"], cwd=source).stdout.strip()
        if not head.startswith(COMMIT[:7]):
            print(f"切换 commit {COMMIT[:7]} …")
            r = run(["git", "checkout", "-q", COMMIT], cwd=source)
            if r.returncode != 0:
                print(f"[无法验证] 切不到该 commit：{r.stderr.strip()[:200]}")
                return 2
        head = run(["git", "rev-parse", "--short", "HEAD"], cwd=source).stdout.strip()
        print(f"当前 commit：{head}（页面锚定 {COMMIT[:7]}）")
        if not head.startswith(COMMIT[:7]):
            print("[FAIL] 当前 commit 与页面锚定的不一致")
            return 1

        print()
        rows, bad = [], 0
        for name, args, (needle, n) in CHECKS:
            cmd = [sys.executable, *args]
            r = run(cmd, cwd=source)
            out = (r.stdout or "") + (r.stderr or "")
            hit = needle in out
            m = re.search(r"Ran (\d+) tests", out) or re.search(r"checks compared: (\d+)", out)
            got = int(m.group(1)) if m else None
            ok = hit and got == n and r.returncode == 0
            if not ok:
                bad += 1
            rows.append((name, " ".join(args), got, n, r.returncode, "PASS" if ok else "FAIL",
                         "" if ok else _note(out)))   # 只在失败时给原因，成功不刷噪音

        print(f"{'检查':<14}{'实测':>6}{'应得':>6}{'退出码':>7}  判定")
        for name, cmd, got, exp, rc, verdict, note in rows:
            print(f"{name:<14}{str(got):>6}{exp:>6}{rc:>7}  {verdict}" + (f"   ← {note}" if note else ""))
        print()
        if bad:
            print(f"[FAIL] {bad} 项与页面所写不符 —— 页面上的数字在这一版上不成立")
            return 1
        print("[PASS] 三条命令全部复现，数字与页面一致：151 / 7 / 70")
        print("       页面还写着「同 commit 的 CI 亦为绿」，CI 记录：")
        print("       https://github.com/zhaoxinghua09-cell/uibc-core/actions/runs/39159391899")
        return 0
    finally:
        if tmp and not a.keep:
            shutil.rmtree(tmp, ignore_errors=True)
        elif tmp:
            print(f"\n克隆保留在：{tmp}")


if __name__ == "__main__":
    sys.exit(main())
