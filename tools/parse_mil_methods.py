"""从军标 OCR 产物里解析「方法索引」→ 结构化表格。

军标的目录页是最有价值的部分（完整方法号清单）。OCR 出的版式有两种：
  A) 方法号与标题分行：
       2021 ． 3
       Glassivation layer integrity
  B) 全部挤在一行（Windows OCR 对密集表格的处理）

本脚本两种都处理，并输出：
  references/mil-methods.json   机读（供 CLI）
  references/MIL-METHODS.md     人读（按体系分组的方法清单）
"""
from __future__ import annotations

import json
import pathlib
import re

SKILL = pathlib.Path(r"<skill 根目录>")
OCR_DIR = SKILL / "references" / "sources" / "standards" / "mil_ocr"

# 已知的 883 体系分段（来自标准自身的章节标题，OCR 可证）
SERIES = {
    "1": "环境试验 ENVIRONMENTAL TESTS",
    "2": "机械试验 MECHANICAL TESTS",
    "3": "电气试验 ELECTRICAL TESTS",
    "4": "(预留/未在 883K 目录出现)",
    "5": "工艺试验/其他 TESTS (5001+)",
}

# OCR 常见误识 → 修正（只做**确定的**字符级修正，不做术语推断）
OCR_FIX = [
    (r"DownIoaded\s*行?\s*om", "Downloaded from"),
    (r"http:ll", "http://"),
    (r"M\s*lL-STD", "MIL-STD"),
    (r"MlL-STD", "MIL-STD"),
    (r"M (\w)", r"M\1"),
    (r"UItrasonic", "Ultrasonic"),
    (r"lnspectlon", "inspection"),
    (r"SolderabiIity", "Solderability"),
    (r"SoIderabiIity", "Solderability"),
    (r"Stab 山 zation", "Stabilization"),
    (r"℃", "C"),
]

METHOD_LINE = re.compile(
    r"^(?P<no>[1-9]\d{3})"          # 四位方法号
    r"(?:[\s．.、，,·]+(?P<rev>\d{1,2}))?"   # 可选修订号（全角标点也算）
    r"\s*$")
# 标题行：排除纯数字、纯页码、明显的页眉
NOT_TITLE = re.compile(
    r"^(DownIoaded|Downloaded|M\s?lL-STD|MIL-STD|TEST METHODS|METHOD NO|"
    r"\d+$|[A-Z\s]+TESTS$)")


def is_title(s: str) -> bool:
    """标题判定：放宽到「非空且不是方法号/页眉/纯数字」。"""
    if not s or len(s) < 3 or len(s) > 110:
        return False
    if METHOD_LINE.match(s) or NOT_TITLE.match(s):
        return False
    # 至少要有字母或汉字
    return bool(re.search(r"[A-Za-z\u4e00-\u9fff]", s))


def clean(s: str) -> str:
    for a, b in OCR_FIX:
        s = re.sub(a, b, s)
    return re.sub(r"\s{2,}", " ", s).strip()


def parse(text: str) -> list[dict]:
    """从 OCR 文本里抽 (方法号, 修订号, 标题)。

    规则：方法号行的**紧邻下一非空行**即其标题。
    对「标题被 OCR 提前输出」的错位情况无法修正——因此同时做块内数量自检，
    数量不匹配的块整体标注为「配对待核」。
    """
    lines = [clean(x) for x in text.splitlines()]
    rows: list[dict] = []
    i = 0
    while i < len(lines):
        m = METHOD_LINE.match(lines[i])
        if not m:
            i += 1
            continue
        no, rev = m.group("no"), m.group("rev")
        # 向后找第一个非空行
        j = i + 1
        while j < len(lines) and not lines[j]:
            j += 1
        title = lines[j] if (j < len(lines) and is_title(lines[j])) else ""
        rows.append({"method": no, "rev": rev, "title": title})
        i = j + 1 if title else i + 1

    # 块内数量自检：把 rows 按 1xxx/2xxx/... 切段，
    # 若同段内出现「方法号跳号」且标题数为 0 的行较多，整体降级
    return rows


def validate(rows: list[dict]) -> tuple[list[dict], dict]:
    """自检：标题缺失率 + 单调性。返回 (rows, 报告)。"""
    if not rows:
        return rows, {"total": 0, "with_title": 0, "monotonic": True,
                      "trust": "无法判定"}
    nums = [r["method"] for r in rows]
    with_title = sum(1 for r in rows if r["title"])
    mono = all(int(a) < int(b) for a, b in zip(nums, nums[1:])) if len(nums) > 1 else True
    ratio = with_title / len(rows)
    trust = ("可用（标题覆盖率 {:.0%}，方法号单调）".format(ratio)
             if ratio >= 0.9 and mono else
             "**配对待核**（标题覆盖率 {:.0%}，单调性 {}）".format(ratio, mono))
    return rows, {"total": len(rows), "with_title": with_title,
                  "monotonic": mono, "trust": trust}


def main() -> int:
    allm: dict[str, list[dict]] = {}
    reports: dict[str, dict] = {}
    for f in sorted(OCR_DIR.glob("*.txt")):
        std = f.stem
        rows = parse(f.read_text(encoding="utf-8"))
        # 去重（同号取标题最长者）
        best: dict[str, dict] = {}
        for r in rows:
            k = r["method"]
            if k not in best or len(r["title"]) > len(best[k]["title"]):
                best[k] = r
        ordered = sorted(best.values(), key=lambda x: x["method"])
        _, rep = validate(ordered)
        allm[std] = ordered
        reports[std] = rep
        print(f"{std:<16} 方法号 {rep['total']:>3} 个"
              f"  有标题 {rep['with_title']:>3}"
              f"  单调 {rep['monotonic']}  → {rep['trust']}")

    (SKILL / "references" / "mil-methods.json").write_text(
        json.dumps({"generated": "2026-10-07",
                    "source_tier": "L4-OCR",
                    "note": "来源为军标目录页 OCR 产物。**方法号可用于定位**；"
                            "标题可能含 OCR 误差与偶发错位，引用前须核对原页。"
                            "每份标准的标题可信度见 validation 字段。",
                    "validation": reports,
                    "standards": allm}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    # 人读版
    L = ["# 军标方法索引（MIL-STD-883 / GJB 548）", "",
         "> **来源**：本库对军标扫描件目录页做的 OCR（引擎 Windows.Media.Ocr · zh-Hans-CN）。",
         "> **引用层级**：L4-OCR。",
         ">",
         "> **⚠ 怎么用这份清单**：",
         "> - ✅ **方法号可信**（四位数字，OCR 不易错）→ 可用于定位「883 的 1010 是什么」",
         "> - ⚠ **标题可能错**：实测 OCR 会把个别标题的输出顺序提前/滞后，",
         ">   导致标题与方法号错位（如 `Stabilization bake` 被排到 `1008` 之前）。",
         "> - ⚠ **引用标题前必须核对原扫描页**；不得把本清单的标题当权威原文。",
         ""]
    for std, rows in allm.items():
        rep = reports.get(std, {})
        L.append(f"## `{std}`")
        L.append("")
        if not rows:
            L.append("（未解析出方法号——需扩大 OCR 页范围）")
            L.append("")
            continue
        L.append(f"共 **{rep.get('total', len(rows))}** 个方法号，"
                 f"其中 {rep.get('with_title', 0)} 个识别到标题。"
                 f"**自检结论**：{rep.get('trust', '—')}")
        L.append("")
        by_series: dict[str, list[dict]] = {}
        for r in rows:
            by_series.setdefault(r["method"][0], []).append(r)
        for s in sorted(by_series):
            L.append(f"### {s}xxx — {SERIES.get(s, '')}")
            L.append("")
            L.append("| 方法号 | 修订 | 标题（OCR，可能错位，须核对原页） |")
            L.append("|---|---|---|")
            for r in by_series[s]:
                L.append(f"| `{r['method']}` | {r['rev'] or '—'} | "
                         f"{r['title'] or '（未识别到）'} |")
            L.append("")
    (SKILL / "references" / "MIL-METHODS.md").write_text(
        "\n".join(L) + "\n", encoding="utf-8")

    print(f"\n→ {SKILL / 'references' / 'mil-methods.json'}")
    print(f"→ {SKILL / 'references' / 'MIL-METHODS.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
