"""蒸馏 L3 机翻标准：产出可用的条款级 digest。

机翻件不能引用措辞（术语被译坏），但**结构与数值可用**。本脚本产出：
  1. 章节结构（含条款号还原 —— 实测 20% 的条款号存在确定性的数字错位，可逆）
  2. 关键数值条件（温度/时长/湿度/循环/电/尺寸/力）
  3. 该文件命中的已知术语错误 + 次数
  4. 内容概要（每节首句）

输出：references/digests/<std_id>.md  +  references/digests/_INDEX.md
"""
from __future__ import annotations

import json
import pathlib
import re

SKILL = pathlib.Path(r"<skill 根目录>")
SRC = SKILL / "references" / "sources" / "standards"
OUT = SKILL / "references" / "digests"
CORPUS = json.loads((SKILL / "data" / "corpus.json").read_text(encoding="utf-8"))

# ── 已核实的机翻术语错误（每项都有与英文原件的对齐证据）────────────────────
TERMS = [
    ("模具垫", "芯片焊盘 / 芯片键合垫", "die pad",
     "B116B 机翻 L95「模具垫金属化」↔ 英文原件 L206「the die pad metallization」"),
    ("模具", "芯片 / 裸片", "die",
     "B116B 机翻 L202「模具的表面与剪切工具的剪切面」↔ 英文 L461「surface of the die … shearing plane」"),
    ("球键", "球焊点", "ball bond",
     "B116B 机翻 L68「球键的质量」↔ 英文 L149 上下文 ball bond"),
    ("线束", "键合线", "wire bond",
     "B116B 机翻「线束剪切试验」↔ 英文标题「Wire Bond Shear Test Method」"),
    ("热膜", "热超声", "thermosonic",
     "B116B 机翻 L69「热膜（球）键」↔ 英文 L153「thermosonic (ball) bonds」"),
    ("针线", "针脚焊点", "stitch bond",
     "B116B 机翻 L73「通常为针线」↔ 英文 L162「typically a stitch bond」"),
    ("冶金键", "冶金结合", "metallurgical bond",
     "B116B 机翻 L67「已形成的冶金键」↔ 英文 L149「the metallurgical bond」"),
    ("骰子", "芯片 / 晶粒", "dice",
     "J-STD-020 目录「JEP160 电子固态晶片、骰子和设备…」↔ JEP160 英文标题「Wafers, Dice, and Devices」"),
    ("偏见", "偏压 / 偏置", "bias",
     "A110E「偏见指南」= Bias Guidelines；同一文件他处已用「偏置」，前后不一致"),
    ("偏差", "偏压 / 偏置", "bias",
     "A110E L159「连续或周期性偏差」——同一文件内 bias 有「偏见/偏差/偏置」三种译法"),
]

# ── 数值条件单位 ──────────────────────────────────────────────────────────
UNITS = re.compile(
    r"(±\s*\d|\d+\s*°\s*C|\d+\s*[º℃]|\d+\s*%\s*RH|\d+\s*%|\d+\s*h\b|\d+\s*小时|"
    r"\d+\s*分钟|\d+\s*min|\d+\s*cph|\d+\s*次|\d+\s*cycles?|\d+\s*V\b|\d+\s*m[AVW]\b|"
    r"\d+\s*µ\s*m|\d+\s*um\b|\d+\s*mm\b|\d+\s*mil|\d+\s*g\b|\d+\s*MPa|\d+\s*kPa)",
    re.I)

SEC = re.compile(r"^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\s*([^\s].{0,60})$", re.M)
SEC_BROKEN = re.compile(r"^\.(\d{2,3})\s*([^\s].{0,60})$", re.M)


def repair(numpart: str) -> str:
    """还原条款号错位：实测规则为「首位数字被移到末尾」。
    .32 → 2.3 / .162 → 2.16 / .21 → 1.2
    """
    d = numpart
    if len(d) < 2:
        return d
    return f"{d[-1]}.{d[:-1]}"


def load_body(p: pathlib.Path) -> str:
    t = p.read_text(encoding="utf-8")
    head, _, body = t.partition("=" * 78)
    return head, body


def sections(body: str) -> list[tuple[str, str, bool]]:
    """返回 [(条款号, 标题, 是否为还原值)]，按出现顺序去重。"""
    found = []
    seen = set()
    for m in SEC.finditer(body):
        key = m.group(1)
        if key not in seen:
            seen.add(key)
            found.append((key, m.group(2).strip(), False))
    for m in SEC_BROKEN.finditer(body):
        key = repair(m.group(1))
        if key not in seen:
            seen.add(key)
            found.append((key, m.group(2).strip(), True))
    found.sort(key=lambda x: [int(i) for i in x[0].split(".")])
    return found


def numeric_lines(body: str, limit: int = 40) -> list[str]:
    out, seen = [], set()
    for ln in body.splitlines():
        s = ln.strip()
        if len(s) < 4 or len(s) > 200:
            continue
        if re.search(r"^=====|^\[PAGE", s):
            continue
        if UNITS.search(s) and re.search(r"\d", s):
            k = re.sub(r"\s+", "", s)[:60]
            if k not in seen:
                seen.add(k)
                out.append(s)
        if len(out) >= limit:
            break
    return out


def term_hits(body: str) -> list[tuple[str, str, str, str, int]]:
    """返回 [(机翻译法, 应为, 英文原词, 核实依据, 次数)]，按次数降序。"""
    res = []
    for bad, good, en, ev in TERMS:
        n = body.count(bad)
        if n:
            res.append((bad, good, en, ev, n))
    return sorted(res, key=lambda x: -x[4])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    l3 = [e for e in CORPUS["entries"] if e["tier"] == "L3"]
    index_rows = []

    for e in l3:
        f = SKILL / e["corpus_path"]
        if not f.exists():
            continue
        head, body = load_body(f)
        secs = sections(body)
        nums = numeric_lines(body)
        terms = term_hits(body)

        L = []
        L.append(f"# {e['std_id']} — 条款级 digest（L3 机翻件）")
        L.append("")
        L.append(f"> **引用层级**：{e['tier']}｜{e['tier_name']}")
        L.append(f"> **类别**：{e['cat']}　**适用范围**：{e['scope']}")
        if e.get("key_points"):
            L.append(f"> **关键条目**：{e['key_points']}")
        L.append(f"> **源文件**：`{e['source_file']}`")
        L.append(f"> **SHA256(16)**：`{e['sha16']}`　**页数**：{e.get('pdf_pages')}　"
                 f"**文本层**：{e.get('text_chars'):,} 字符")
        L.append(f"> **自述版本**：{'、'.join(e['self_version_tokens'][:4]) or '（未识别）'}　"
                 f"**自述日期**：{'、'.join(e['self_date_tokens'][:3]) or '（未识别）'}")
        L.append("")
        L.append("## ⚠ 引用限制（先读这段）")
        L.append("")
        L.append("| 能用 | 不能用 |")
        L.append("|---|---|")
        L.append("| ✅ 章节结构（含条款号）与表格数值 | ❌ **术语译名**（已被机翻译坏） |")
        L.append("| ✅ 用于理解与索引、定位 | ❌ 作为「标准原文」引用措辞 |")
        L.append("| ✅ 与英文原文交叉核对后使用 | ❌ 单独作为判定依据 |")
        L.append("")
        L.append("**条款号还原说明**：实测本库机翻件有约 20% 的条款号存在确定性错位"
                 "（首位数字被移到末尾），如 `.32` 实为 `2.3`、`.162` 实为 `2.16`。"
                 "下表已还原，还原项标 `（还原）`。**引用条款号前须回英文原文核对。**")
        L.append("")

        if terms:
            L.append("## 术语纠错（本文件命中）")
            L.append("")
            L.append("| 机翻译法 | 出现 | 应为 | 英文原词 | 核实依据 |")
            L.append("|---|---:|---|---|---|")
            for bad, good, en, ev, n in terms:
                L.append(f"| 「{bad}」 | {n} 次 | **{good}** | `{en}` | {ev} |")
            L.append("")

        L.append("## 章节结构")
        L.append("")
        if secs:
            L.append("| 条款号 | 标题 |")
            L.append("|---|---|")
            for num, title, repaired in secs:
                tag = " （还原）" if repaired else ""
                L.append(f"| `{num}`{tag} | {title} |")
        else:
            L.append("（未识别出结构化章节号——该文件可能为表格型或扫描型）")
        L.append("")

        L.append("## 关键数值条件（含单位的行）")
        L.append("")
        if nums:
            for s in nums:
                L.append(f"- {s}")
        else:
            L.append("（未提取到含单位的数值行）")
        L.append("")
        L.append("---")
        L.append("")
        L.append(f"全文语料：`{e['corpus_path']}`")
        L.append("")
        (OUT / f"{e['std_id']}.md").write_text("\n".join(L), encoding="utf-8")

        index_rows.append({
            "std_id": e["std_id"], "cat": e["cat"], "scope": e["scope"],
            "sections": len(secs), "repaired": sum(1 for s in secs if s[2]),
            "numeric_lines": len(nums),
            "term_hits": sum(t[4] for t in terms),
            "digest": f"references/digests/{e['std_id']}.md",
        })
        print(f"  ✓ {e['std_id']:<20} 章节 {len(secs):>3}（还原 {sum(1 for s in secs if s[2]):>2}）"
              f" 数值行 {len(nums):>3} 术语错误 {sum(t[4] for t in terms):>4}")

    # 索引
    L = ["# 机翻标准条款级 digest 索引（L3）", "",
         f"> 共 {len(index_rows)} 份。由 `tools/distill_l3.py` 生成。",
         ">",
         "> **这批 digest 的价值**：机翻件的**结构与数值**可用（数字不受翻译影响），",
         "> 但**术语被译坏**、约 20% 的条款号错位。所以本 digest 的定位是",
         "> **「让你知道每份标准里有什么、在哪一节」**，不是「可以引用的原文」。", "",
         "| 标准 | 类别 | 适用范围 | 章节 | 其中还原 | 数值行 | 术语错误命中 | digest |",
         "|---|---|---|---:|---:|---:|---:|---|"]
    for r in sorted(index_rows, key=lambda x: (x["cat"], x["std_id"])):
        L.append(f"| `{r['std_id']}` | {r['cat']} | {r['scope'][:34]} | {r['sections']} | "
                 f"{r['repaired']} | {r['numeric_lines']} | {r['term_hits']} | "
                 f"[打开]({r['std_id']}.md) |")
    L.append("")
    L.append("## 术语纠错总表（已核实，对齐英文原件）")
    L.append("")
    L.append("| 机翻译法 | 应为 | 英文原词 | 核实依据 |")
    L.append("|---|---|---|---|")
    for bad, good, en, ev in TERMS:
        L.append(f"| 「{bad}」 | **{good}** | `{en}` | {ev} |")
    L.append("")
    L.append("> 用法：读到机翻件里的左列词时，**心里替换成中间列**，"
             "引用时用英文原词。这样 L3 语料就从「不可用」变成「可用但需转译」。")
    (OUT / "_INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    (OUT / "_index.json").write_text(
        json.dumps({"generated": "2026-10-07", "count": len(index_rows),
                    "terms": [{"bad": b, "good": g, "en": e, "evidence": v}
                              for b, g, e, v in TERMS],
                    "entries": index_rows}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    tot_sec = sum(r["sections"] for r in index_rows)
    tot_rep = sum(r["repaired"] for r in index_rows)
    tot_num = sum(r["numeric_lines"] for r in index_rows)
    tot_term = sum(r["term_hits"] for r in index_rows)
    print(f"\ndigest 生成完毕：{len(index_rows)} 份")
    print(f"  章节合计 {tot_sec}（其中还原 {tot_rep}，"
          f"占 {tot_rep / max(1, tot_sec) * 100:.0f}%）")
    print(f"  数值条件行合计 {tot_num}")
    print(f"  术语错误命中合计 {tot_term} 次")
    print(f"→ {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
