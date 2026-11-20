#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""external_runs_gate.py — 外部运行台账的格式门 + 叙述一致性门

为什么要有这个门
----------------
"外部第三方复跑回执 = 1" 这句话，此前只存在于 EVIDENCE-INDEX 与几份对外件的散文里。
散文里的数字可以被悄悄改大，而没有任何东西会报错。2026-11-20 起改为：
数字必须能由 `external-runs.json` 算出来，算不出就判红。

门的判据（三条，逐条可复核）
  1. 台账合法：每行必须有 required_fields 里的字段；`run_label` / `evidence` 必须落在
     已定义的三级/两级刻度里；`result` 必须落在 PASS / PASS-with-changes / FAIL /
     INCONCLUSIVE 之内。缺字段时允许写 null，但必须同时有 `<field>_note` 说明——
     缺席的字段和未记录的事实，在 diff 里看起来一样，所以不许静默省略。
  2. 回执可寻：`receipt_ref` 非空。没有回执指向的行不是"外部运行"，是传闻。
  3. 叙述一致：扫描指定面，凡出现"外部回执 N"形状的数字，N 必须等于台账里
     `run_label=independent 且 receipt_ref 非空 且 counts_toward_m4=true` 的行数。
     出现数字但台账算不出来的，判红；叙述里没出现数字则只提示，不判红。

退出码：0 通过 / 1 判红 / 2 台账本身读不了。
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = "external-runs.json"
RESULT_SCALE = {"PASS", "PASS-with-changes", "FAIL", "INCONCLUSIVE"}

# 叙述面（相对仓库根）。只扫"对外会说外部回执数量"的那几面。
SURFACES = ["README.md", "llms.txt", "agents.txt"]
# 形如"外部回执 1"、"外部回执 = 1"、"external receipts: 1"、"L4 外部节点 1"
NUM_PATTERNS = [
    r"外部回执\s*[=:：]?\s*(\d+)",
    r"外部节点\s*[=:：]?\s*(\d+)",
    r"external\s+receipts?\s*[=:：]?\s*(\d+)",
    r"external\s+nodes?\s*[=:：]?\s*(\d+)",
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    path = os.path.join(ROOT, LEDGER)
    try:
        doc = load(path)
    except Exception as e:
        print("[FATAL] 读不了 %s：%s" % (LEDGER, e))
        return 2

    problems = []
    warnings = []

    required = doc.get("required_fields") or []
    labels = set((doc.get("run_label_scale") or {}).keys()) - {"note"}
    evidences = set((doc.get("evidence_scale") or {}).keys()) - {"note"}

    runs = doc.get("runs") or []
    for i, row in enumerate(runs):
        rid = row.get("id") or "runs[%d]" % i
        for field in required:
            if field not in row:
                problems.append("%s: 缺字段 %s（缺就写 null 并加 %s_note）" % (rid, field, field))
                continue
            if row[field] is None and ("%s_note" % field) not in row:
                problems.append("%s: %s 为 null 但没有 %s_note" % (rid, field, field))
        if row.get("run_label") not in labels:
            problems.append("%s: run_label=%r 不在刻度 %s 内" % (rid, row.get("run_label"), sorted(labels)))
        if row.get("evidence") not in evidences:
            problems.append("%s: evidence=%r 不在刻度 %s 内" % (rid, row.get("evidence"), sorted(evidences)))
        if row.get("result") not in RESULT_SCALE:
            problems.append("%s: result=%r 不在 %s 内" % (rid, row.get("result"), sorted(RESULT_SCALE)))
        if not row.get("receipt_ref"):
            problems.append("%s: receipt_ref 为空 —— 没有回执指向的行不算外部运行" % rid)
        if row.get("run_label") == "independent" and row.get("evidence") == "blind" \
                and not row.get("environment"):
            warnings.append("%s: 声称 independent+blind 却没记环境（OS/Python）" % rid)

    counted = [
        r for r in runs
        if r.get("run_label") == "independent"
        and r.get("receipt_ref")
        and r.get("counts_toward_m4") is True
    ]
    derived = len(counted)

    # 叙述一致
    found = []
    for surf in SURFACES:
        p = os.path.join(ROOT, surf)
        if not os.path.isfile(p):
            continue
        txt = open(p, encoding="utf-8").read()
        for pat in NUM_PATTERNS:
            for m in re.finditer(pat, txt):
                ln = txt[:m.start()].count("\n") + 1
                found.append((surf, ln, int(m.group(1)), m.group(0)))

    print("=" * 72)
    print("外部运行台账门")
    print("台账：%s（schema=%s，更新 %s）" % (LEDGER, doc.get("schema"), doc.get("updated")))
    print("行数：%d；可计入 M4：%d" % (len(runs), derived))
    print("=" * 72)

    for surf, ln, n, raw in found:
        if n == derived:
            print("[OK]   %-24s :%-5s 叙述 %r 与台账推出值 %d 一致" % (surf, ln, raw, derived))
        else:
            problems.append("%s:%s 叙述写 %d，台账推出 %d" % (surf, ln, n, derived))

    if not found:
        warnings.append("叙述面里没有出现外部回执数字（可接受，但外人就看不到这个数）")

    for w in warnings:
        print("[WARN] %s" % w)
    if problems:
        for p in problems:
            print("[FAIL] %s" % p)
        print()
        print("合计问题：%d" % len(problems))
        print("结论：FAIL —— 台账或叙述不一致。改台账，不要改叙述。")
        return 1
    print("[PASS] 台账合法 + 每行回执可寻 + 叙述数字与台账推出值一致")
    print("结论：PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
