#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""proof_claim_check — 校验「外锚已确认」这类声称的四处落点是否互相对得上。

背景：red-team（G2）实测发现原有 repo_gate 存在三个漏放：
  D) ANCHORS.md 把区块高度写错（975424 → 975400），门禁 rc=0；
  E) skills.json 把 state 改成 Confirmed 但删掉高度，门禁 rc=0；
  F) skills.json 少一条（6/7），门禁 rc=0。
本脚本用一张定值表（tools/proof_claims.json）把这些声称钉死，四处落点逐项对账。

用法：
  python tools/proof_claim_check.py --root .
  python tools/proof_claim_check.py --root . --claims tools/proof_claims.json
退出码：0 全对；1 有落点对不上（打印具体哪条、期望 vs 实际）；2 定值表缺失或不可解析。

判据（任何一条 FAIL 即 rc=1）：
  1. 定值表条目数 == skills.json 的 items 长度 == skills.json 的 count
  2. 定值表里的每个名字在 ANCHORS.md 有行，且该行 sha256 与定值表一致
  3. 该行的区块高度集合与定值表一致（顺序不限，但必须完全相同）
  4. skills.json 每个条目的 sha256 与定值表一致
  5. skills.json 每个条目的 timestamp_proof.state 必须写明 Confirmed，且高度集合与定值表一致
  6. EVAL.md / FACTS.md 的汇总句必须包含定值表里出现的全部高度
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HEIGHT_RE = re.compile(r"\b(9\d{5})\b")


def read(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def heights_in(text):
    return sorted({int(h) for h in HEIGHT_RE.findall(text or "")})


def parse_anchors(md):
    """从 ANCHORS.md 表格抓 name -> (sha256, heights)。"""
    rows = {}
    for line in (md or "").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        name_m = re.search(r"`([a-z0-9][a-z0-9\-_]+)`", cells[1]) if len(cells) > 1 else None
        sha_m = re.search(r"`([a-f0-9]{64})`", cells[2]) if len(cells) > 2 else None
        if not (name_m and sha_m):
            continue
        rows[name_m.group(1)] = (sha_m.group(1), heights_in(cells[-1]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--claims", default="tools/proof_claims.json")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    cpath = a.claims if os.path.isabs(a.claims) else os.path.join(root, a.claims)

    claims = read(cpath)
    if claims is None:
        print("[FAIL] 定值表缺失：%s" % a.claims)
        return 2
    try:
        cj = json.loads(claims)
        entries = cj["claims"] if isinstance(cj, dict) else cj
    except Exception as e:
        print("[FAIL] 定值表不可解析：%s" % e)
        return 2
    pinned = {e["name"]: (e["sha256"], sorted(int(x) for x in e["heights"])) for e in entries}

    fails = []

    # 1/2/3 ANCHORS.md
    anchors = parse_anchors(read(os.path.join(root, "ANCHORS.md")))
    if not anchors:
        fails.append("ANCHORS.md 抓不到任何行（表格结构变了？）")
    for name, (sha, hs) in pinned.items():
        if name not in anchors:
            fails.append("ANCHORS.md 缺行：%s" % name)
            continue
        a_sha, a_hs = anchors[name]
        if a_sha != sha:
            fails.append("ANCHORS.md sha 不符：%s 期望 %s… 实际 %s…" % (name, sha[:10], a_sha[:10]))
        if a_hs != hs:
            fails.append("ANCHORS.md 高度不符：%s 期望 %s 实际 %s" % (name, hs, a_hs))

    # 4/5/1 skills.json
    raw = read(os.path.join(root, "skills.json"))
    if raw is None:
        fails.append("skills.json 缺失")
        sj = {}
    else:
        try:
            sj = json.loads(raw)
        except Exception as e:
            fails.append("skills.json 不可解析：%s" % e)
            sj = {}
    items = sj.get("items", []) if isinstance(sj, dict) else []
    if len(items) != len(pinned):
        fails.append("skills.json 条目数不符：期望 %d 实际 %d" % (len(pinned), len(items)))
    if isinstance(sj, dict) and "count" in sj and sj["count"] != len(items):
        fails.append("skills.json count 与 items 长度不符：count=%s items=%d" % (sj["count"], len(items)))
    seen = set()
    for it in items:
        name = it.get("name")
        seen.add(name)
        if name not in pinned:
            fails.append("skills.json 出现定值表外条目：%s" % name)
            continue
        exp_sha, exp_hs = pinned[name]
        if it.get("sha256") != exp_sha:
            fails.append("skills.json sha 不符：%s 期望 %s… 实际 %s…" % (name, exp_sha[:10], str(it.get("sha256"))[:10]))
        tp = it.get("timestamp_proof") or {}
        state = str(tp.get("state", ""))
        if not state.startswith("Confirmed"):
            fails.append("skills.json 状态非 Confirmed：%s state=%r" % (name, state))
        hs = heights_in(state)
        if hs != exp_hs:
            fails.append("skills.json 状态高度不符（或无高度背书）：%s 期望 %s 实际 %s (state=%r)" % (name, exp_hs, hs, state))
    for name in pinned:
        if name not in seen and items:
            fails.append("skills.json 缺条目：%s" % name)

    # 6 EVAL.md / FACTS.md 汇总句
    all_h = sorted({h for _, hs in pinned.values() for h in hs})
    for fname in ("EVAL.md", "FACTS.md"):
        txt = read(os.path.join(root, fname))
        if txt is None:
            fails.append("%s 缺失" % fname)
            continue
        miss = [h for h in all_h if str(h) not in txt]
        if miss:
            fails.append("%s 未出现高度 %s（汇总句与定值表不一致）" % (fname, miss))

    if fails:
        print("[FAIL] proof-claim 对账失败 %d 条：" % len(fails))
        for f in fails:
            print("  - " + f)
        return 1
    print("[PASS] proof-claim 对账通过：%d 条声称 × ANCHORS/skills/EVAL/FACTS 四处一致" % len(pinned))
    return 0


if __name__ == "__main__":
    sys.exit(main())
