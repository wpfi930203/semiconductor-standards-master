"""军标/国军标 OCR 运行器（双引擎：Windows 内置 OCR / RapidOCR）。

★ 引擎选择依据（实测）：
    Windows 内置 OCR (WinRT, zh-Hans-CN)  ：16~30 秒/页   ← 首选
    RapidOCR PP-OCRv3 + onnxruntime CPU   ：36~262 秒/页  ← 回退
  同一台机器同一天的实测对比，相差 5~10 倍。

设计要点：
  1. 逐页落盘 —— 每页识别完立即 append，中断不丢已完成部分
  2. 断点续跑 —— 重跑时跳过已完成页（读 .progress.json）
  3. 可限页   —— --max-pages 控制规模（定向 OCR 用）
  4. 版面还原 —— 按 y 间距分段，不做换行合并（Windows OCR 已给出行）
  5. 如实标注 —— 头部写明引擎/DPI/页数/耗时，并声明「OCR 产物，非原生文本层」

用法：
  python ocr_military.py --list
  python ocr_military.py --std MIL-STD-883K --pages 4-8          # 只跑目录页
  python ocr_military.py --std MIL-STD-883K --max-pages 60       
  python ocr_military.py --std MIL-STD-883K --resume             # 续跑
  python ocr_military.py --std MIL-STD-883K --engine rapid       # 强制回退引擎
"""
from __future__ import annotations

import argparse
import asyncio
import json
import pathlib
import sys
import time

import pymupdf

SRC = pathlib.Path(r"<本地标准资料库>")
SKILL = pathlib.Path(r"<skill 根目录>")
DEST = SKILL / "references" / "sources" / "standards" / "mil_ocr"
TMP = SKILL / "references" / "sources" / "standards" / "mil_ocr" / "_pages"
LONG = "\\\\?\\"

TARGETS = {
    "MIL-STD-883F": "美军标 MIL-STD-883F.pdf",
    "MIL-STD-883K": "美军标 MIL-STD-883K.pdf",
    "GJB-548B": "国军标GJB 548B-2005微电子器件试验方法和程序.pdf",
    "GJB-548C": "GJB 548C-2021-.pdf",
}

WIN_ENGINE = "Windows.Media.Ocr (WinRT) · zh-Hans-CN"
RAPID_ENGINE = "RapidOCR (PP-OCRv3 det/rec + v2 cls, onnxruntime CPU)"


def lp(p: pathlib.Path) -> pathlib.Path:
    s = str(p)
    return pathlib.Path(LONG + s) if len(s) >= 240 else p


def log(*a):
    print(*a, flush=True)


def parse_pages(spec: str) -> list[int]:
    """'4-8' / '4,5,9' / '1-3,10' → 0-based 页号列表。"""
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out += list(range(int(a) - 1, int(b)))
        elif part:
            out.append(int(part) - 1)
    return sorted(set(out))


# ── 引擎 A：Windows 内置 OCR ────────────────────────────────────────────────
class WinOcr:
    name = WIN_ENGINE

    def __init__(self):
        import winrt.windows.globalization as wg
        import winrt.windows.media.ocr as wocr
        self._wocr = wocr
        engine = None
        for tag in ("zh-Hans-CN", "en-US", ""):
            try:
                engine = wocr.OcrEngine.try_create_from_language(wg.Language(tag)) \
                    if tag else wocr.OcrEngine.try_create_from_user_profile_languages()
            except Exception:
                engine = None
            if engine:
                self.lang_used = tag or "user-profile"
                break
        if engine is None:
            raise RuntimeError("Windows OCR 无可用语言引擎")
        self.engine = engine

    def extract(self, png: pathlib.Path) -> tuple[str, float]:
        return asyncio.run(self._aextract(png))

    async def _aextract(self, png: pathlib.Path) -> tuple[str, float]:
        import winrt.windows.graphics.imaging as wgi
        import winrt.windows.storage as ws
        f = await ws.StorageFile.get_file_from_path_async(str(png))
        stream = await f.open_async(ws.FileAccessMode.READ)
        dec = await wgi.BitmapDecoder.create_async(stream)
        bmp = await dec.get_software_bitmap_async()
        t0 = time.time()
        res = await self.engine.recognize_async(bmp)
        dt = time.time() - t0
        return render_lines(res), dt


CJK = r"\u3000-\u303f\u4e00-\u9fff\uff00-\uffef"


def collapse_cjk_spaces(s: str) -> str:
    """Windows OCR 对中文会在字间插空格（'微 电 子 器 件'）。

    这是引擎的版面切分行为，不是真空格。此处把两个 CJK 字符之间的空格去掉，
    但保留 CJK 与拉丁/数字之间的空格（那是有意义的词边界）。
    """
    import re as _re
    prev = None
    while prev != s:
        prev = s
        s = _re.sub(rf"([{CJK}])\s+([{CJK}])", r"\1\2", s)
    return s


def render_lines(res, fix_cjk: bool = True) -> str:
    """按行的 y 位置分段（相邻行间距 > 1.2 倍行高视为新段）。"""
    items = []
    for ln in res.lines:
        words = list(ln.words)
        if not words:
            continue
        ys = [w.bounding_rect.y for w in words]
        hs = [w.bounding_rect.height for w in words]
        t = ln.text.strip()
        if fix_cjk:
            t = collapse_cjk_spaces(t)
        items.append({"t": t, "y": min(ys),
                      "h": max(hs) if hs else 10.0})
    items = [i for i in items if i["t"]]
    if not items:
        return ""
    items.sort(key=lambda i: i["y"])
    out, prev = [], None
    for it in items:
        if prev is not None:
            gap = it["y"] - (prev["y"] + prev["h"])
            if gap > prev["h"] * 1.2:
                out.append("")
        out.append(it["t"])
        prev = it
    return "\n".join(out)


# ── 引擎 B：RapidOCR（回退）────────────────────────────────────────────────
class RapidOcr:
    name = RAPID_ENGINE

    def __init__(self):
        import numpy as np
        from rapidocr_onnxruntime import RapidOCR
        self.np = np
        self.ocr = RapidOCR()

    def extract(self, png: pathlib.Path) -> tuple[str, float]:
        import numpy as np
        pix = pymupdf.Pixmap(str(png))
        if pix.n > 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n)[:, :, :3]
        t0 = time.time()
        res, _ = self.ocr(arr)
        dt = time.time() - t0
        if not res:
            return "", dt
        return "\n".join(r[1].strip() for r in res if r[1].strip()), dt


def build_engine(kind: str):
    if kind in ("win", "auto"):
        try:
            e = WinOcr()
            log(f"  引擎: {e.name}（语言 {e.lang_used}）")
            return e
        except Exception as ex:
            if kind == "win":
                raise
            log(f"  Windows OCR 不可用（{type(ex).__name__}），回退 RapidOCR")
    e = RapidOcr()
    log(f"  引擎: {e.name}")
    return e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--std")
    ap.add_argument("--max-pages", type=int, default=0)
    ap.add_argument("--pages", help="指定页范围，如 4-8 或 1,5,9")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--engine", choices=["auto", "win", "rapid"], default="auto")
    a = ap.parse_args()

    if a.list:
        for k, v in TARGETS.items():
            d = pymupdf.open(lp(SRC / v))
            log(f"  {k:<16} {d.page_count:>4} 页   {v}")
            d.close()
        return 0

    if not a.std or a.std not in TARGETS:
        log(f"用法：--std <{'|'.join(TARGETS)}>")
        return 2

    DEST.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    pdf = SRC / TARGETS[a.std]
    out_txt = DEST / f"{a.std}.txt"
    prog_p = DEST / f"{a.std}.progress.json"

    doc = pymupdf.open(lp(pdf))
    total = doc.page_count
    if a.pages:
        pages = [p for p in parse_pages(a.pages) if 0 <= p < total]
    else:
        n = min(total, a.max_pages) if a.max_pages else total
        pages = list(range(n))

    prog = (json.loads(prog_p.read_text(encoding="utf-8"))
            if (a.resume and prog_p.exists()) else
            {"done_pages": [], "total_pages": total})
    done = set(prog.get("done_pages", []))

    log(f"[{a.std}] {total} 页，本次 {len(pages)} 页，已跳过 {len(done & set(pages))} 页")
    engine = build_engine(a.engine)

    if not out_txt.exists():
        out_txt.write_text(
            f"# SOURCE: {pdf.name}\n"
            f"# 文字识别方式: {engine.name}\n"
            f"# DPI: {a.dpi}   全本页数: {total}\n"
            f"# ⚠ 本文件为 **OCR 产物**，非标准原生文本层。识别会有个别字符误差\n"
            f"#   （实测样例: 'http://' 被识成 'http:ll'、词间空格丢失、'Stabilization' 被识成 'Stab 山 zation'）。\n"
            f"#   引用条款号 / 方法号 / 数值前，**必须人工核对原扫描页**。\n"
            f"# ⚠ 引用层级：L4-OCR（内容可用于理解与索引，不得当作权威原文直接引用）\n"
            f"{'=' * 78}\n", encoding="utf-8")

    t_all = time.time()
    n_done = 0
    for pno in pages:
        if pno in done:
            continue
        png = TMP / f"{a.std}_p{pno + 1}.png"
        t0 = time.time()
        if not png.exists():
            pix = doc[pno].get_pixmap(dpi=a.dpi, colorspace=pymupdf.csRGB)
            pix.save(str(png))
        t_render = time.time() - t0
        try:
            text, dt = engine.extract(png)
        except Exception as ex:
            log(f"  p{pno + 1} 失败: {type(ex).__name__}: {ex}")
            continue
        with out_txt.open("a", encoding="utf-8") as f:
            f.write(f"\n\n===== [PAGE {pno + 1}] =====  (识别 {dt:.1f}s)\n{text}\n")
        done.add(pno)
        n_done += 1
        prog_p.write_text(json.dumps({
            "std_id": a.std, "done_pages": sorted(done), "total_pages": total,
            "dpi": a.dpi, "engine": engine.name,
            "elapsed_sec": round(time.time() - t_all, 1),
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        avg = (time.time() - t_all) / n_done
        todo = len([p for p in pages if p not in done])
        log(f"  p{pno + 1}/{total}  渲染{t_render:.1f}s 识别 {dt:6.1f}s  "
            f"均 {avg:5.1f}s/页  本次剩余 {todo} 页 约 {avg * todo / 60:.0f} 分钟")

    doc.close()
    log(f"\n[{a.std}] 本次完成 {n_done} 页，用时 {(time.time() - t_all) / 60:.1f} 分钟")
    log(f"  累计 {len(done)}/{total} 页")
    log(f"→ {out_txt}  ({out_txt.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
