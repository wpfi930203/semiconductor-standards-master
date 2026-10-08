"""从 GJB 548B/C 的 OCR 文本里提取「方法目录」（方法号 + 中文标题 + 页码）。

GJB 目录页的版式（p2-4）比 MIL-STD-883 规整：
    方法 1001
    低气压（高空工作）
    方法 1002
    浸液

但 OCR 有数字混淆：`101L1`→1011、`201L1`→2011、`101 & 1`→1018.1、`30 巧`→3015。
处理策略（**不做知识注入，只做形态归并 + 交叉校验**）：
  1. 数字归一化：O/o/l/I/L → 0/1（仅在方法号上下文）
  2. 与已解析的 MIL-STD-883 方法号**交叉校验**（GJB 548 源自 MIL-STD-883，方法号同源）
  3. 交叉校验失败或形态无法归一的，标记为「待核」，不猜
"""
from __future__ import annotations

import json
import pathlib
import re

SKILL = pathlib.Path(r"<skill 根目录>")
OCR_DIR = SKILL / "references" / "sources" / "standards" / "mil_ocr"

# 883 体系的方法分组（880/883/548 共用；标准自身的章节标题可证）
SERIES = {
    "1": "环境试验 ENVIRONMENTAL TESTS",
    "2": "机械试验 MECHANICAL TESTS",
    "3": "电气试验 ELECTRICAL TESTS",
    "4": "（预留）",
    "5": "工艺/筛选与程序 TESTS & PROCEDURES (5001+)",
}

# ★ 目录页范围（1-based，闭区间）——实测定位，避免正文污染标题
#   883 目录页经核实；GJB 目录页经核实（548B p2-4、548C p1-3）
TOC_PAGES = {
    "MIL-STD-883K": (5, 7),
    "MIL-STD-883F": (4, 7),
    "GJB-548B": (2, 4),
    "GJB-548C": (1, 3),
}


def slice_pages(text: str, lo: int, hi: int) -> str:
    """只取指定页范围的文本。"""
    parts = re.split(r"\n===== \[PAGE (\d+)\] =====.*?\n", text)
    out = []
    for i in range(1, len(parts), 2):
        try:
            pno = int(parts[i])
        except ValueError:
            continue
        if lo <= pno <= hi:
            out.append(parts[i + 1])
    return "\n".join(out)


# 方法号里常见的 OCR 字符混淆（数字位上的）
DIGIT_FIX = str.maketrans({
    "O": "0", "o": "0", "D": "0", "Q": "0",
    "l": "1", "I": "1", "L": "1", "i": "1", "|": "1", "¡": "1",
    "S": "5", "s": "5", "巧": "15", "勺": "15",
    "B": "8", "&": "8", "曰": "8",
    "g": "9", "q": "9",
    "乙": "2", "Z": "2",
    "了": "7", "T": "7",
})

# 「方法 NNNN」或「方法 NNNN.rev」；数字位允许 OCR 混淆字符
M_CN = re.compile(
    r"方法\s*([0-9OolIQLi|¡Ss巧勺B&曰gq乙Z了T]{2,5})"
    r"(?:\s*[．.、，,·]?\s*(\d{1,2}))?")
# 883 式：行首 NNNN.rev
M_EN = re.compile(r"^(?P<no>[1-9]\d{3})(?:[\s．.、，,·]+(?P<rev>\d{1,2}))?\s*$")

NOT_TITLE = re.compile(
    r"^(\d{1,3}|[IVXLC]+|GJB\s*548|目|录|方法\s*\d|"
    r"DownIoaded|M\s?lL-STD|MIL-STD|TEST METHODS|METHOD NO|[A-Z\s]+TESTS$)")


def norm_num(raw: str) -> tuple[str, bool]:
    """归一化方法号。返回 (号, 是否发生了需人工确认的改写)。"""
    fixed = raw.translate(DIGIT_FIX)
    digits = re.sub(r"\D", "", fixed)
    if len(digits) == 4:
        return digits, fixed != raw
    if len(digits) == 5:
        # 形如 '10051' → 可能是 1005.1 被并吞，取前 4 位
        return digits[:4], True
    return "", True


def is_title(s: str) -> bool:
    if not s or len(s) < 2 or len(s) > 90:
        return False
    if NOT_TITLE.match(s):
        return False
    if re.fullmatch(r"[\d\s．.、，,·％%·]+", s):
        return False
    return bool(re.search(r"[\u4e00-\u9fffA-Za-z]", s))


def squeeze_digits(s: str) -> str:
    """去掉数字之间的空格：OCR 会把 '1011' 拆成 '101 1'。

    这是实测到的现象（883K 目录页 `101 1 ． 9` = 1011.9），不修就会漏掉该号。
    只处理数字↔数字之间，不动其他空格。
    """
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"(\d)\s+(?=\d)", r"\1", s)
    return s


def parse_gjb(text: str) -> list[dict]:
    lines = [squeeze_digits(re.sub(r"\s{2,}", " ", x)).strip()
             for x in text.splitlines()]
    rows, i = [], 0
    while i < len(lines):
        m = M_CN.search(lines[i])
        if m:
            no, altered = norm_num(m.group(1))
            rev = m.group(2)
            if no:
                j = i + 1
                while j < len(lines) and not lines[j]:
                    j += 1
                # 标题可能在同一行（"方法 1004 ， 1 耐湿"）或下一行
                tail = lines[i][m.end():].strip(" ．.、，,·")
                if is_title(tail):
                    title = tail
                    i = i + 1
                elif j < len(lines) and is_title(lines[j]):
                    title = lines[j]
                    i = j + 1
                else:
                    title = ""
                    i += 1
                # 页码：标题行尾部或下一行
                pg = ""
                km = re.search(r"[．.·灬\s]{2,}(\d{1,3})\s*$", title)
                if km:
                    pg = km.group(1)
                    title = title[:km.start()].strip(" ．.、，,·灬")
                rows.append({"method": no, "rev": rev, "title": title,
                             "page": pg, "ocr_altered": altered})
                continue
        i += 1
    return rows


def parse_en(text: str) -> list[dict]:
    lines = [squeeze_digits(x).strip() for x in text.splitlines()]
    rows, i = [], 0
    while i < len(lines):
        m = M_EN.match(lines[i])
        if m:
            j = i + 1
            while j < len(lines) and not lines[j]:
                j += 1
            title = lines[j] if (j < len(lines) and is_title(lines[j])) else ""
            rows.append({"method": m.group("no"), "rev": m.group("rev"),
                         "title": title, "page": "", "ocr_altered": False,
                         "source": "目录页"})
            i = j + 1 if title else i + 1
        else:
            i += 1
    return rows


# 正文节标题：`方法 NNNN 标题`（同一行，无页码）——用于补齐目录页缺失的项
M_BODY_CN = re.compile(
    r"方法\s*([0-9OolIQLi|¡Ss巧勺B&曰gq乙Z了T]{2,5})"
    r"[\s，,．.、·]+([\u4e00-\u9fff][^\n]{0,40})")


def parse_gjb_body(text: str, have: set[str]) -> list[dict]:
    """从正文补齐：只取「方法号 + 标题同一行」的节标题，且只补目录里没有的号。

    为什么可信：节标题的号与标题在同一行、同一 text run，不存在错位问题
    （目录页的错位来自两栏分离）。但因为可能撞上正文交叉引用，
    来源标注为「正文节标题」，与目录项区分开。
    """
    out = []
    for m in M_BODY_CN.finditer(text):
        no, _ = norm_num(m.group(1))
        if not no or no in have:
            continue
        title = m.group(2).strip(" ．.、，,·灬：:")
        if len(title) < 2:
            continue
        out.append({"method": no, "rev": None, "title": title, "page": "",
                    "ocr_altered": False, "source": "正文节标题"})
    return out


def gaps_of(rows: list[dict]) -> dict:
    """识别**同一系列内**的号段不连续处。

    ⚠ 这不等于「提取遗漏」——标准本身也跳号（如 883 的 1xxx 是 1001~1023 然后
    直接跳 1030）。所以只声明「号段不连续」，并同时给出可能的两种解释，
    不替读者下结论。
    """
    by_series: dict[str, list[int]] = {}
    for r in rows:
        m = r["method"]
        by_series.setdefault(m[0], []).append(int(m))
    out = {}
    for s, nums in sorted(by_series.items()):
        nums = sorted(set(nums))
        lo, hi = nums[0], nums[-1]
        have = set(nums)
        miss = [n for n in range(lo, hi + 1) if n not in have]
        runs, cur = [], []
        for n in miss:
            if cur and n == cur[-1] + 1:
                cur.append(n)
            else:
                if cur:
                    runs.append(cur)
                cur = [n]
        if cur:
            runs.append(cur)
        if runs:
            out[s] = [{"from": f"{r[0]:04d}", "to": f"{r[-1]:04d}",
                       "count": len(r)} for r in runs]
    return {
        "series_gaps": out,
        "meaning": "号段不连续。可能是(a)该号在标准中本就不存在（标准跳号），"
                   "也可能是(b)目录页 OCR 漏识。**本 skill 不判断是哪种**，"
                   "需查原页确认。",
    }


def sibling_fill(std: str, rows: list[dict],
                 siblings: dict[str, list[dict]]) -> list[dict]:
    """用同源标准的目录补齐缺口（**明确标注来源与风险**，不冒充本标准内容）。

    GJB 548C 取代 548B；548C 的目录 I 页（方法 1001~1030）在扫描件中缺失，
    故用 548B 的目录作参考。548C 有修订说明列出变更，标题可能不同 —— 必须标注。
    """
    partner = {"GJB-548C": "GJB-548B", "GJB-548B": "GJB-548C"}.get(std)
    if not partner or partner not in siblings:
        return rows
    ref = {r["method"]: r for r in siblings[partner]}
    have = {r["method"] for r in rows}
    added = []
    for no, r in sorted(ref.items()):
        if no not in have and r.get("title"):
            added.append({
                "method": no, "rev": None, "title": r["title"], "page": "",
                "ocr_altered": False, "source": "同源标准参考",
                "source_detail": f"据 {partner} 目录（{std} 目录相应页在扫描件中缺失）；"
                                 f"**{std} 可能已修订该标题，不得直接引用**",
            })
    if added:
        print(f"    {std}: 用 {partner} 目录补 {len(added)} 个缺口（已标注来源与风险）")
    return sorted(rows + added, key=lambda x: x["method"])


def validate(rows: list[dict]) -> tuple[list[dict], dict]:
    """自检：标题覆盖率 + 方法号单调性。返回 (rows, 报告)。"""
    if not rows:
        return rows, {"total": 0, "with_title": 0, "monotonic": True,
                      "trust": "无法判定"}
    nums = [r["method"] for r in rows]
    with_title = sum(1 for r in rows if r["title"])
    mono = (all(int(a) < int(b) for a, b in zip(nums, nums[1:]))
            if len(nums) > 1 else True)
    ratio = with_title / len(rows)
    trust = ("可用（标题覆盖率 {:.0%}，方法号单调）".format(ratio)
             if ratio >= 0.9 and mono else
             "**配对待核**（标题覆盖率 {:.0%}，单调性 {}）".format(ratio, mono))
    return rows, {"total": len(rows), "with_title": with_title,
                  "monotonic": mono, "trust": trust}


def main() -> int:
    reports: dict[str, dict] = {}
    mp = SKILL / "references" / "mil-methods.json"
    M = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {"standards": {}}
    stds: dict[str, list[dict]] = M.get("standards", {})

    # 883 侧用英文式解析（覆盖旧的解析结果）
    for std in ("MIL-STD-883K", "MIL-STD-883F"):
        f = OCR_DIR / f"{std}.txt"
        if not f.exists():
            continue
        lo, hi = TOC_PAGES.get(std, (1, 9999))
        best: dict[str, dict] = {}
        for r in parse_en(slice_pages(f.read_text(encoding="utf-8"), lo, hi)):
            k = r["method"]
            if k not in best or len(r["title"]) > len(best[k]["title"]):
                best[k] = r
        stds[std] = sorted(best.values(), key=lambda x: x["method"])

    # GJB 侧用中文式解析
    for std in ("GJB-548B", "GJB-548C"):
        f = OCR_DIR / f"{std}.txt"
        if not f.exists():
            continue
        lo, hi = TOC_PAGES.get(std, (1, 9999))
        full = f.read_text(encoding="utf-8")
        best = {}
        for r in parse_gjb(slice_pages(full, lo, hi)):
            k = r["method"]
            r.setdefault("source", "目录页")
            if k not in best or len(r["title"]) > len(best[k]["title"]):
                best[k] = r
        n_before = len(best)
        stds[std] = sorted(best.values(), key=lambda x: x["method"])
        print(f"    {std}: 目录页 {n_before} 个")

    # 先记录补齐前的自检（未被同源参考污染）
    for std, rows in stds.items():
        _, reports[std] = validate(rows)

    # ★ 缺口声明 + 同源补齐（在交叉校验之前做，让校验看到补齐后的结果）
    gaps = {std: gaps_of(rows) for std, rows in stds.items()}
    for std in ("GJB-548B", "GJB-548C"):
        if std in stds:
            stds[std] = sibling_fill(std, stds[std], stds)

    # ★ 交叉校验：GJB 548 源自 MIL-STD-883，方法号应基本一致
    ref = {r["method"] for r in stds.get("MIL-STD-883K", [])} | \
          {r["method"] for r in stds.get("MIL-STD-883F", [])}
    xcheck = {}
    for std in ("GJB-548B", "GJB-548C"):
        if std not in stds:
            continue
        got = {r["method"] for r in stds[std]}
        if not ref or not got:
            xcheck[std] = {"status": "无法交叉校验（一侧为空）"}
            continue
        only_gjb = sorted(got - ref)
        only_883 = sorted(ref - got)
        xcheck[std] = {
            "gjb_only": only_gjb,
            "mil883_only": only_883,
            "agree_ratio": f"{len(got & ref)}/{len(got)} = "
                           f"{len(got & ref) / max(1, len(got)) * 100:.0f}%",
            "altered_count": sum(1 for r in stds[std] if r.get("ocr_altered")),
            "note": "GJB 548 与 MIL-STD-883 方法号同源，故可作为独立交叉校验。"
                    "gjb_only 多为 OCR 数字混淆残留或 883 侧尚未 OCR 到的号。",
        }

    M.update({
        "generated": "2026-10-08",
        "gaps": gaps,
        "cross_validation": xcheck,
        "standards": stds,
    })
    mp.write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")

    print("=== 方法号提取 ===")
    for std, rows in stds.items():
        alt = sum(1 for r in rows if r.get("ocr_altered"))
        wt = sum(1 for r in rows if r["title"])
        g = gaps.get(std, {}).get("series_gaps", {})
        gs = "、".join(f"{s}xxx:" + ",".join(f"{x['from']}~{x['to']}" for x in v)
                       for s, v in list(g.items())[:2]) or "无"
        print(f"  {std:<16} {len(rows):>3} 个  有标题 {wt:>3}  "
              f"OCR归一 {alt:>2}  缺口 {gs}")
    print("\n=== 交叉校验（GJB 548 vs MIL-STD-883）===")
    for std, x in xcheck.items():
        if "agree_ratio" in x:
            print(f"  {std}: 与 883 方法号重合 {x['agree_ratio']}  "
                  f"仅GJB有 {len(x['gjb_only'])} 个 {x['gjb_only'][:8]}")
        else:
            print(f"  {std}: {x['status']}")

    # ── 人读版 ─────────────────────────────────────────────
    L = ["# 军标方法索引（MIL-STD-883 / GJB 548）", "",
         "> **来源**：本库对军标扫描件**目录页**做的 OCR"
         "（引擎 Windows.Media.Ocr · zh-Hans-CN）。**引用层级：L4-OCR**。", "",
         "## ⚠ 怎么用这份清单", "",
         "| 可用 | 不可用 |",
         "|---|---|",
         "| ✅ **方法号**——四位数字，OCR 不易错，可用于定位 | ❌ 把标题当权威原文引用 |",
         "| ✅ 交叉校验结论（GJB 548 与 MIL-STD-883 方法号同源） | ❌ 忽略「同源参考」标记的标题 |",
         "| ✅ 作为查找原扫描页的索引 | ❌ 无视缺口声明 |", "",
         "**三种来源标记**：", "",
         "| 标记 | 含义 | 可信度 |",
         "|---|---|---|",
         "| `目录页` | 该标准自己的目录页 OCR | 标题可能因读序错位，**须核对原页** |",
         "| `同源标准参考` | 本标准目录页缺失，借用同源标准目录 | **可能已被修订，不得直接引用** |",
         "| `OCR归一` | 号中含 OCR 混淆字符（O/l/L/巧/&），已按规则归一 | 号可信；建议核对 |", "",
         "---", ""]
    for std, rows in stds.items():
        rep = reports.get(std, {})
        L.append(f"## `{std}`")
        L.append("")
        n_src = {}
        for r in rows:
            n_src[r.get("source", "目录页")] = n_src.get(r.get("source", "目录页"), 0) + 1
        L.append(f"共 **{len(rows)}** 个方法号；标题 {sum(1 for r in rows if r['title'])} 个。"
                 f"来源构成：" + "、".join(f"{k} {v}" for k, v in n_src.items()) + "。")
        g = gaps.get(std, {}).get("series_gaps", {})
        if g:
            gs = "；".join(f"{s}xxx 缺 " + "、".join(
                (x["from"] if x["from"] == x["to"] else f"{x['from']}~{x['to']}")
                for x in v) for s, v in sorted(g.items()))
            L.append("")
            L.append(f"**号段不连续**：{gs}。"
                     "⚠ 这可能是标准本身跳号，也可能是 OCR 漏识——**本清单不判断是哪种**。")
        L.append("")
        by_series: dict[str, list[dict]] = {}
        for r in rows:
            by_series.setdefault(r["method"][0], []).append(r)
        for s in sorted(by_series):
            L.append(f"### {s}xxx — {SERIES.get(s, '')}")
            L.append("")
            L.append("| 方法号 | 修订 | 标题（OCR，标题可能错位/未修订，须核对原页） | 来源 |")
            L.append("|---|---|---|---|")
            for r in by_series[s]:
                m = r["method"] + ("*" if r.get("ocr_altered") else "")
                L.append(f"| `{m}` | {r['rev'] or '—'} | {r['title'] or '（未识别到）'} | "
                         f"{r.get('source', '目录页')} |")
            L.append("")
    L.append("> `*` = 方法号含 OCR 混淆字符，已按规则归一。")
    L.append("")
    (SKILL / "references" / "MIL-METHODS.md").write_text(
        "\n".join(L) + "\n", encoding="utf-8")

    print(f"\n→ {mp}")
    print(f"→ {SKILL / 'references' / 'MIL-METHODS.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
