"""盘点源资料：去重 + 文本层探测。不改动任何源文件，只读。"""
import hashlib
import json
import pathlib
import re
import sys

import pymupdf

SRC = pathlib.Path(r"<本地标准资料库>")
OUT = pathlib.Path(__file__).resolve().parent / "inventory.json"


def longpath(p: pathlib.Path) -> pathlib.Path:
    """绕开 Win32 MAX_PATH(260) 限制——本目录有 263 字符的路径。"""
    s = str(p)
    if sys.platform == "win32" and not s.startswith("\\\\?\\") and len(s) >= 240:
        return pathlib.Path("\\\\?\\" + s)
    return p


def walk_pdfs(root: pathlib.Path):
    """rglob 在长路径上会静默漏项，改用 os.scandir 递归。"""
    import os
    stack = [root]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(longpath(cur)) as it:
                for e in it:
                    p = cur / e.name
                    if e.is_dir(follow_symlinks=False):
                        stack.append(p)
                    elif e.name.lower().endswith(".pdf"):
                        yield p
        except OSError as ex:
            print(f"  !! 无法遍历 {cur}: {ex}", file=sys.stderr)


def sha(p, n=1 << 20):
    h = hashlib.sha256()
    with open(longpath(p), "rb") as f:
        while chunk := f.read(n):
            h.update(chunk)
    return h.hexdigest()[:16]


def clean_name(name: str) -> str:
    """从文件名里剥出标准编号与标题。"""
    s = pathlib.Path(name).stem
    s = re.sub(r"_1_\d+_translate_\d+$", "", s)
    s = re.sub(r"\s*-\s*完整英文(电子)?版.*$", "", s)
    s = re.sub(r"\s*完整英文版.*$", "", s)
    return s.strip()


rows = []
for p in sorted(walk_pdfs(SRC), key=lambda x: str(x)):
    rel = p.relative_to(SRC).as_posix()
    size = longpath(p).stat().st_size
    digest = sha(p)
    try:
        doc = pymupdf.open(longpath(p))
        pages = doc.page_count
        # 采样前 3 页 + 中间 + 末页，判断是否含文本层
        probe_pages = sorted({0, min(1, pages - 1), pages // 2, pages - 1})
        chars = 0
        for i in probe_pages:
            if 0 <= i < pages:
                chars += len(doc[i].get_text().strip())
        doc.close()
    except Exception as e:
        pages, chars = -1, -1
        print(f"  !! 打开失败 {rel}: {e}", file=sys.stderr)

    rows.append({
        "rel": rel,
        "dir": p.parent.relative_to(SRC).as_posix() or ".",
        "size": size,
        "sha16": digest,
        "pages": pages,
        "probe_chars": chars,
        "has_text": chars > 200,
        "clean_name": clean_name(p.name),
    })

# 按内容哈希归并重复文件
by_hash = {}
for r in rows:
    by_hash.setdefault(r["sha16"], []).append(r)

print(f"PDF 文件总数        : {len(rows)}")
print(f"按内容哈希去重后    : {len(by_hash)} 个不同文件")
print(f"有文本层（可提取）  : {sum(1 for r in rows if r['has_text'])}")
print(f"疑似扫描件（无文本）: {sum(1 for r in rows if not r['has_text'] and r['pages'] > 0)}")
print(f"总页数              : {sum(r['pages'] for r in rows if r['pages'] > 0):,}")
print(f"总体积              : {sum(r['size'] for r in rows)/1024/1024:.0f} MB")

print("\n=== 重复文件组（同一内容出现多次）===")
for h, g in sorted(by_hash.items()):
    if len(g) > 1:
        print(f"\n[{h}] x{len(g)}  {g[0]['pages']}p  {g[0]['clean_name'][:70]}")
        for r in g:
            print(f"    - {r['rel']}")

OUT.write_text(json.dumps({
    "src_root": str(SRC),
    "file_count": len(rows),
    "unique_by_content": len(by_hash),
    "rows": rows,
}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n→ 清单已写入 {OUT}")
