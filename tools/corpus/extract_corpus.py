"""全量抽取半导体标准 PDF 文本层 → skill 内 references/sources/standards/。

只读源目录，不修改、不移动、不重命名源文件。
扫描件（无文本层）不做 OCR —— 如实登记，交由调用方声明边界。

用法：
  python tools/extract_corpus.py --dry-run
  python tools/extract_corpus.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

import pymupdf

SRC = pathlib.Path(r"<本地标准资料库>")
SKILL = pathlib.Path(r"<skill 根目录>")
DEST = SKILL / "references" / "sources" / "standards"
LONG = "\\\\?\\"


def lp(p: pathlib.Path) -> pathlib.Path:
    s = str(p)
    return pathlib.Path(LONG + s) if len(s) >= 240 else p


def walk(root: pathlib.Path):
    import os
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(lp(cur)) as it:
                for e in it:
                    p = cur / e.name
                    if e.is_dir(follow_symlinks=False):
                        stack.append(p)
                    elif e.name.lower().endswith(".pdf"):
                        yield p
        except OSError as ex:
            print(f"  !! 无法遍历 {cur}: {ex}", file=sys.stderr)


def sha(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(lp(p), "rb") as f:
        while c := f.read(1 << 20):
            h.update(c)
    return h.hexdigest()[:16]


# ---- 编号识别（顺序敏感：更具体的放前面）------------------------------------
def std_id(name: str) -> str:
    s = pathlib.Path(name).stem
    s = re.sub(r"_1_\d+_translate_\d+$", "", s)
    s = re.sub(r"\s*-\s*完整英文(电子)?版.*$", "", s).strip()

    m = re.search(r"JESD22[- ]([A-Z])(\d{3})([A-Z]?(?:\.\d+)?)", s, re.I)
    if m:
        return f"JESD22-{m.group(1).upper()}{m.group(2)}{m.group(3).upper()}"

    m = re.search(r"JESD(\d+)(-\d+)?([A-Z]?(?:\.\d+)?)", s, re.I)
    if m:
        return f"JESD{m.group(1)}{m.group(2) or ''}{m.group(3).upper()}"

    m = re.search(r"JS-?001", s, re.I)
    if m:
        return "JS-001"

    m = re.search(r"J-STD-?(\d+)", s, re.I)
    if m:
        return f"J-STD-{m.group(1)}"

    m = re.search(r"IPC[-_ ]?TM[-_ ]?650\s*([\d.]+[a-z]?)", s, re.I)
    if m:
        return f"IPC-TM-650-{m.group(1)}"

    m = re.search(r"IPC[-_ ]?(\d{4})([A-Z]?)", s, re.I)
    if m:
        return f"IPC-{m.group(1)}{m.group(2).upper()}"

    m = re.search(r"MIL-STD-(\d+)([A-Z]?)", s, re.I)
    if m:
        return f"MIL-STD-{m.group(1)}{m.group(2).upper()}"

    m = re.search(r"GJB\s*(\d+)([A-Z]?)", s, re.I)
    if m:
        return f"GJB-{m.group(1)}{m.group(2).upper()}"

    if "AQG324" in s.upper().replace(" ", ""):
        m = re.search(r"(\d\d\.\d)_(\d{4})", s)
        return f"AQG324-{m.group(1)}_{m.group(2)}" if m else "AQG324-other"
    return "UNKNOWN"


def org_of(sid: str, rel: str) -> str:
    if sid.startswith("JESD") or sid.startswith("JS-") or sid.startswith("J-STD"):
        return "jedec"
    if sid.startswith("IPC"):
        return "ipc"
    if sid.startswith("MIL-STD"):
        return "mil"
    if sid.startswith("GJB"):
        return "gjb"
    if sid.startswith("AQG324"):
        return "aqg324"
    return "other"


def version_hint(name: str) -> str | None:
    """从文件名抽年份/版本线索（仅作提示，不当作核实结论）。"""
    s = pathlib.Path(name).stem
    m = re.search(r"[：:]\s*(\d{4})", s)
    if m:
        return m.group(1)
    m = re.search(r"(19|20)\d{2}", s)
    return m.group(0) if m else None


# 拆分件识别：仅对军标/GJB 生效（这些才有 (1-349) / 1-199 之类分卷）
SPLIT_RE = re.compile(r"[（(]?\s*\d+\s*[-–]\s*\d+\s*[）)]?")
SPLIT_STD = ("MIL-STD-883", "GJB-548")


def is_split(name: str, sid: str) -> bool:
    if not sid.startswith(SPLIT_STD):
        return False
    base = pathlib.Path(name).stem
    # 去掉标准编号本身再找区间，避免 "883F" "548B" 被误判
    base = re.sub(r"(MIL-STD-883|国军标GJB\s*548B-2005|GJB\s*548[BC])[A-Z]?", "", base)
    base = re.sub(r"[-–]?(19|20)\d{2}", "", base)
    return bool(SPLIT_RE.search(base))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    groups: dict[str, list[pathlib.Path]] = {}
    for p in walk(SRC):
        rel = p.relative_to(SRC).as_posix()
        sid = std_id(p.name)
        groups.setdefault(sid, []).append(p)
        _ = rel

    # 同内容去重
    index = []
    for sid in sorted(groups):
        cands = groups[sid]
        by_hash: dict[str, list[pathlib.Path]] = {}
        for c in cands:
            by_hash.setdefault(sha(c), []).append(c)

        org = org_of(sid, cands[0].relative_to(SRC).as_posix())

        # 选代表：非拆分件优先 → 页数最多 → 路径最短
        reps = []
        for h, g in by_hash.items():
            rep = min(g, key=lambda x: (len(str(x)), str(x)))
            reps.append((h, g, rep))
        reps.sort(key=lambda t: (is_split(t[2].name, sid), -len(str(t[2])), str(t[2])))

        for h, g, rep in reps:
            rel = rep.relative_to(SRC).as_posix()
            split = is_split(rep.name, sid)
            vh = version_hint(rep.name)

            if a.dry_run:
                print(f"[{org:7}] {sid:<20} {len(g)}份 dup {'拆' if split else '全'} "
                      f"{rep.name[:58]}")
                continue

            # AQG 324 已在 skill 内（references/sources/books/），不重复提取
            if org == "aqg324":
                index.append({
                    "std_id": sid, "org": org, "file": rel, "sha16": h,
                    "dup_in_group": len(g), "is_split": split, "year_hint": vh,
                    "extracted": False, "already_in_skill": True,
                    "reason": "AQG 324 三版 PDF 已存在于 skill 内 references/sources/books/，"
                              "本次为同源副本，不重复提取",
                })
                print(f"  = 已在库 {sid:<26} (同源副本，跳过)", file=sys.stderr)
                continue

            try:
                doc = pymupdf.open(lp(rep))
                n = doc.page_count
                chunks = []
                for i in range(n):
                    t = doc[i].get_text()
                    if t.strip():
                        chunks.append(f"\n\n===== [PAGE {i + 1}] =====\n{t.strip()}")
                body = "".join(chunks)
                doc.close()
            except Exception as ex:
                index.append({"std_id": sid, "org": org, "file": rel, "sha16": h,
                              "extracted": False, "reason": f"打开失败: {ex}"})
                continue

            if len(body) < 200:
                index.append({
                    "std_id": sid, "org": org, "file": rel, "sha16": h,
                    "pages": n, "chars": len(body), "dup_in_group": len(g),
                    "is_split": split, "year_hint": vh,
                    "extracted": False,
                    "reason": "无文本层（扫描件），未 OCR —— 禁止据此编造内容",
                })
                print(f"  · 扫描未提取 {sid:<18} {n:>4}p  ({len(g)}份)",
                      file=sys.stderr)
                continue

            d = DEST / org
            d.mkdir(parents=True, exist_ok=True)
            tag = "-part" if split else ""
            txt = d / f"{sid}{tag}.txt"
            k = 2
            while txt.exists():
                txt = d / f"{sid}{tag}_{k}.txt"
                k += 1
            txt.write_text(
                f"# SOURCE: {rep.name}\n"
                f"# 原始路径: {rel}\n"
                f"# SHA256(16): {h}   页数: {n}   文本层字符: {len(body):,}\n"
                f"# 同内容副本数: {len(g)}   是否拆分件: {'是' if split else '否'}\n"
                f"# 文件名年份线索: {vh or '（无）'}\n"
                f"# 提取方式: PyMuPDF 文本层抽取 —— 未 OCR、未翻译、未改写\n"
                f"{'=' * 78}\n" + body,
                encoding="utf-8")
            index.append({
                "std_id": sid, "org": org, "file": rel, "sha16": h,
                "pages": n, "chars": len(body), "dup_in_group": len(g),
                "is_split": split, "year_hint": vh,
                "extracted": True,
                "corpus_path": f"references/sources/standards/{org}/{txt.name}",
            })
            print(f"  ✓ {sid+tag:<26} {n:>4}p {len(body):>9,}c")

    if a.dry_run:
        return 0

    DEST.parent.mkdir(parents=True, exist_ok=True)
    (DEST.parent / "corpus_index.json").write_text(json.dumps({
        "src_root": str(SRC),
        "extracted_at": "2026-10-07",
        "extractor": "PyMuPDF 文本层抽取（无 OCR / 无翻译 / 无改写）",
        "total_pdfs": sum(len(v) for v in groups.values()),
        "distinct_std_ids": len(groups),
        "extracted_count": sum(1 for i in index if i["extracted"]),
        "scanned_count": sum(1 for i in index if not i["extracted"]),
        "entries": sorted(index, key=lambda x: (x["org"], x["std_id"])),
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    ok = sum(1 for i in index if i["extracted"])
    print(f"\n文本层提取: {ok} 份；扫描件登记未提取: {len(index) - ok} 份")
    print(f"→ {DEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
