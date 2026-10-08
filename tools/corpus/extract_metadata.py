"""从抽取文本的正文自述中提取「标准自报」元数据。

文件名已证明不可信（多份英文名文件实为机翻中文），因此标题/版本一律
以文档首页自述为准，文件名只作对照留痕。
"""
from __future__ import annotations

import json
import pathlib
import re

D = pathlib.Path(r"<skill 根目录>"
                 r"\references\sources\standards")

CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN = re.compile(r"[A-Za-z]")

# 版本号：形如 JESD22-A104F / JS-001-2017 / IPC-7351B / JESD47L / 548C
VER_RE = re.compile(
    r"\b(JESD\d{2}-[A-Z]\d{3}[A-Z]?(?:\.\d+)?|JESD\d{2}[A-Z]?|JS-001-\d{4}|"
    r"J-STD-\d{3}[A-Z]?|IPC-\d{4}[A-Z]?(?:-WAM\d)?|IPC-TM-650\s*[\d.]+[a-z]?|"
    r"[A-Z]?\d{3}[A-Z]\.\d{2}|MIL-STD-\d{3}[A-Z]|GJB\s*\d{3}[A-Z])\b", re.I)

MONTH_RE = re.compile(
    r"\b(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|"
    r"NOVEMBER|DECEMBER)\s+(\d{4})\b", re.I)
YEAR_RE = re.compile(r"\b(19[89]\d|20[0-4]\d)\b")

CN_TITLE_KEYS = ["温度循环", "热冲击", "功率循环", "高温存储", "低温存储", "湿热", "盐雾",
                 "气密", "引线", "键合", "焊球", "可焊", "翘曲", "共面", "跌落", "弯折",
                 "振动", "冲击", "外形", "标识", "预处理", "锡须", "闩锁", "考核", "试验方法"]


def head_text(t: str, n: int = 3500) -> str:
    body = t.split("=" * 78, 1)[-1]
    body = re.sub(r"===== \[PAGE \d+\] =====", "", body)
    # 跳过 JEDEC 的版权样板（约占前 2500 字符）
    return body[:n]


def lang_ratio(t: str) -> float:
    body = t.split("=" * 78, 1)[-1]
    c = len(CJK.findall(body))
    l = len(LATIN.findall(body))
    return c / max(1, c + l)


def detect_lang(t: str, fn: str) -> tuple[str, str]:
    r = lang_ratio(t)
    baked = "_translate_" in fn or "translate_" in fn
    if r > 0.75:
        return ("zh-MT", "机翻中文（文件名多为英文名，内容为机器翻译）")
    if r > 0.25:
        return ("bi", "中英对照（英文段落 + 中文翻译）")
    return ("en", "英文原文")


def main() -> int:
    src_index = json.loads((D.parent / "corpus_index.json").read_text(encoding="utf-8"))
    by_path = {e.get("corpus_path"): e for e in src_index["entries"] if e.get("corpus_path")}

    out = []
    for f in sorted(D.rglob("*.txt")):
        t = f.read_text(encoding="utf-8")
        head = head_text(t)
        # 相对 skill 根，与 corpus_index.json 的 corpus_path 键对齐
        rel = f.relative_to(D.parent.parent.parent).as_posix()
        meta = by_path.get(rel, {})
        plain = t.split("=" * 78, 1)[-1]

        vers = VER_RE.findall(head) or VER_RE.findall(plain[:8000])
        months = MONTH_RE.findall(head) or MONTH_RE.findall(plain[:8000])
        years = YEAR_RE.findall(head)

        # 语言
        lang_code, lang_note = detect_lang(t, meta.get("file", ""))

        # 中文标题线索
        cn_hits = [k for k in CN_TITLE_KEYS if k in head]

        out.append({
            "std_id": meta.get("std_id") or f.stem,
            "org": meta.get("org") or f.parent.name,
            "source_file": meta.get("file"),
            "sha16": meta.get("sha16"),
            "pdf_pages": meta.get("pages"),
            "text_chars": len(plain),
            "language": lang_code,
            "language_note": lang_note,
            "self_version_tokens": sorted({v.upper() for v in vers})[:6],
            "self_date_tokens": sorted({f"{m[0].title()} {m[1]}" for m in months})[:4]
                                + sorted(set(years))[:4],
            "cn_title_hints": cn_hits[:8],
            "corpus_path": rel,
        })

    # 汇总
    from collections import Counter
    print(f"{'语种':<8} {'页':>4} {'字符':>9}  std_id            自报版本线索")
    print("-" * 96)
    for r in sorted(out, key=lambda x: (x["org"], x["std_id"])):
        print(f"{r['language']:<8} {r['pdf_pages'] or 0:>4} {r['text_chars']:>9,}  "
              f"{r['std_id']:<18} {','.join(r['self_version_tokens'][:3])}")

    print("\n语种分布:", dict(Counter(r["language"] for r in out)))
    (D.parent / "corpus_metadata.json").write_text(
        json.dumps({"generated": "2026-10-07", "entries": out},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {D.parent / 'corpus_metadata.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
