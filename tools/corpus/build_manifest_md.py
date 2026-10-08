"""生成 references/LOCAL-CORPUS.md —— 人读资料覆盖清单。"""
from __future__ import annotations

import json
import pathlib

SKILL = pathlib.Path(r"<skill 根目录>")
C = json.loads((SKILL / "data" / "corpus.json").read_text(encoding="utf-8"))
T = C["tiers"]
S = C["stats"]

# digest 索引（L3 条款级蒸馏）
_dp = SKILL / "references" / "digests" / "_index.json"
DIG = json.loads(_dp.read_text(encoding="utf-8")) if _dp.exists() else {"entries": [], "terms": []}
DIG_BY = {d["std_id"]: d for d in DIG.get("entries", [])}

# 军标方法索引
_mm = SKILL / "references" / "mil-methods.json"
MM = json.loads(_mm.read_text(encoding="utf-8")) if _mm.exists() else {}

# L4-OCR 产出
OCR_DIR = SKILL / "references" / "sources" / "standards" / "mil_ocr"
OCR_FILES = {p.stem: p for p in OCR_DIR.glob("*.txt")} if OCR_DIR.exists() else {}


def ocr_pages(std_id: str) -> int:
    p = OCR_DIR / f"{std_id}.progress.json"
    if p.exists():
        try:
            return len(json.loads(p.read_text(encoding="utf-8")).get("done_pages", []))
        except Exception:
            return 0
    return 0

CAT_ORDER = [
    "热-机械", "热-电耦合", "热-电（偏压寿命）", "热-电（存储）", "湿热/电化学",
    "机械应力", "焊接耐受力", "互连强度", "板级可靠性", "几何/外观", "标识",
    "环境腐蚀", "封装完整性", "预处理", "工艺能力", "存储器专项", "失效机理专项",
    "材料表征", "热测试", "电应力/ESD", "封装/回流", "资格标准（裁判）",
    "设计/焊盘图形", "封装/组装工艺", "试验方法", "军标（试验方法）", "国军标（试验方法）",
    "未分类",
]

L = []
w = L.append

w("# 本地资料库覆盖清单（LOCAL-CORPUS）")
w("")
w("> **这份文件回答一个问题：手上有哪些标准资料、每份能引用到什么程度。**")
w(">")
w("> 触发本 skill 时，凡涉及具体条款/数值/术语，**必须先在此清单确认资料是否在库、")
w("> 以及在库的是哪种形态**，再决定措辞。清单之外的内容一律声明「无法确认」。")
w("")
w(f"**来源根目录**：`{C['src_root']}`")
w(f"**构建日期**：{C['built']}　|　**提取方式**：{C['extractor']}")
w("")
w("---")
w("")
w("## 一、引用分层模型（最重要的规则）")
w("")
w("标准 PDF 的**文件名不可信**——本次实测发现多份标注「完整英文电子版」的文件，")
w("正文实为**机器翻译中文**（文件名里带 `_translate_` 的就是这类）。")
w("因此本 skill 一律以**文档自述 + 实测语种**定级，不以文件名为准。")
w("")
w("| 层 | 名称 | 可引用措辞 | 可引用数值 | 使用规则 |")
w("|---|---|:---:|:---:|---|")
for k in ["L1", "L2", "L3", "L4", "L0"]:
    t = T[k]
    w(f"| **{k}** | {t['name']} | {'✅' if t['can_cite_wording'] else '❌'} | "
      f"{'✅' if t['can_cite_number'] else '❌'} | {t['rule']} |")
w("")
w("### 为什么机翻件不能引用术语")
w("")
w("实测样例（JESD22-B116B 机翻件 vs 英文原件）：")
w("")
w("| 英文原文 | 机翻件的译法 | 问题 |")
w("|---|---|---|")
w("| Wire Bond Shear Test | 「**线束**剪切试验」 | 线束 = wire harness/cable，与键合线无关 |")
w("| ball bond | 「球键 / 球粘接」 | 业界标准译法是「球焊点」 |")
w("| thermosonic (ball) bond | 「**热膜**（球）键」 | 热膜 ≠ 热超声，物理机理完全不同 |")
w("| metallurgical bond | 「冶金键」 | 标准译法是「冶金结合」 |")
w("| stitch bond | 「**针线**」 | 标准译法是「针脚焊点」 |")
w("")
w("→ 这类错误会直接改变技术含义。**所以 L3 层只能用来定位条款号和表格位置，数值可比对，")
w("术语必须回英文原文。**")
w("")
w("---")
w("")
w("## 二、总览")
w("")
w("| 指标 | 数量 |")
w("|---|---|")
w(f"| 源 PDF 文件总数 | {S['pdf_files_total']} |")
w(f"| 去重后不同标准编号 | {S['distinct_std_ids_total']} |")
w(f"| 已提取文本层 | {S['text_extracted']} 份 |")
w(f"| 扫描件（持有但未识别文字） | {S['scanned_not_extracted']} 份文件 / "
  f"{S['scanned_distinct']} 个标准 |")
w("")
w("**按引用分层的构成：**")
w("")
w("| 层 | 数量 | 标准编号 |")
w("|---|---:|---|")
for k in ["L1", "L2", "L3", "L4"]:
    ids = [e["std_id"] for e in C["entries"] if e["tier"] == k]
    if ids:
        w(f"| {k} {T[k]['name']} | {len(ids)} | {'、'.join(ids)} |")
w("")
w("> **一句话结论**：库里 49 份资料中，**只有 7 份有英文原文**（L1），")
w("> 1 份官方中文译本（L2），**37 份是机器翻译（L3）**，4 个军标是扫描件（L4）。")
w("> 这意味着：**绝大多数 JESD22 条款的措辞不能直接引用，只能定位。**")
w("")
w("---")
w("")
w("## 三、逐份清单（类别 / 适用范围 / 关键条目 / 出处 / 层级）")
w("")
w("> **「蒸馏」列**：🟢 = 已有条款级 digest（章节结构 + 数值条件 + 术语纠错）")
w("> **「文字识别」列**：对扫描件标注 OCR 进度")
w("")

by_cat: dict[str, list] = {}
for e in C["entries"]:
    by_cat.setdefault(e["cat"], []).append(e)

for cat in CAT_ORDER:
    items = by_cat.get(cat)
    if not items:
        continue
    w(f"### {cat}")
    w("")
    for e in sorted(items, key=lambda x: x["std_id"]):
        pg = f"{e['pdf_pages']} 页" if e.get("pdf_pages") else "—"
        dg = DIG_BY.get(e["std_id"])
        marks = []
        if dg:
            marks.append(f"🟢 digest（{dg['sections']} 节 / {dg['numeric_lines']} 数值行）")
        if e["tier"] == "L4":
            n = ocr_pages(e["std_id"])
            marks.append(f"OCR {n} 页" if n else "未 OCR")
        tag = "　·　".join(marks)
        w(f"#### `{e['std_id']}`　<span style='color:#888'>[{e['tier']} {e['tier_name']}]</span>")
        w("")
        if tag:
            w(f"- **蒸馏状态**：{tag}")
        if e["scope"]:
            w(f"- **适用范围**：{e['scope']}")
        if e["key_points"]:
            w(f"- **关键条目**：{e['key_points']}")
        vt = "、".join(e["self_version_tokens"][:4]) or "（未识别到版本号）"
        dt = "、".join(e["self_date_tokens"][:3]) or "（未识别到日期）"
        w(f"- **文档自述**：版本号 `{vt}`；日期线索 `{dt}`")
        w(f"- **规模**：{pg}，文本层 {e['text_chars']:,} 字符")
        if e.get("corpus_path"):
            w(f"- **出处**：`{e['corpus_path']}`")
        else:
            w(f"- **出处**：源文件 `{e['source_file']}`（扫描件，未提取）")
        w(f"- **源文件**：`{e['source_file']}`")
        w(f"- **SHA256(16)**：`{e['sha16']}`")
        if e["tier"] == "L3":
            w("- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**")
        w("")

# 扫描件专节
w("---")
w("")
w("## 四、机翻标准（L3）的条款级蒸馏")
w("")
w(f"机翻件不能引用措辞，但**结构与数值可用**。已对全部 {len(DIG.get('entries', []))} 份 L3 标准"
  f"生成条款级 digest，落在 `references/digests/`。")
w("")
tot = {k: sum(d[k] for d in DIG.get("entries", []))
       for k in ("sections", "repaired", "numeric_lines", "term_hits")}
w("| 指标 | 数量 |")
w("|---|---|")
w(f"| 已蒸馏 L3 标准 | {len(DIG.get('entries', []))} 份 |")
w(f"| 提取出的章节条目 | {tot.get('sections', 0)} |")
w(f"| 其中条款号需还原 | {tot.get('repaired', 0)}"
  f"（{tot.get('repaired', 0) / max(1, tot.get('sections', 1)) * 100:.0f}%）|")
w(f"| 提取出的数值条件行 | {tot.get('numeric_lines', 0)} |")
w(f"| 命中的机翻术语错误 | {tot.get('term_hits', 0)} 次 |")
w("")
w("### ★ 条款号错位：机翻件的第三个缺陷（本轮新发现）")
w("")
w("实测机翻件有约 **20% 的条款号存在确定性错位**——**首位数字被移到末尾**：")
w("")
w("| 语料里写的 | 实际应为 | 验证依据 |")
w("|---|---|---|")
w("| `.32` | `2.3` | A104F 上下文夹在 2.2 与 2.4 之间 |")
w("| `.162` | `2.16` | 同上（A104F 第 2 章末条） |")
w("| `.21` | `1.2` | J-STD-020 目录：`1.1范围` / `.21背景` / `.31术语和定义` 顺序 |")
w("| `.32.联合行业标准` | `2.3 联合行业标准` | J-STD-020 正文：`2.1` / `2.2` / 此条 |")
w("")
w("→ 错位是**可逆的**，digest 已按规则还原并标注 `（还原）`。")
w("→ 但**直接读机翻件原文时看到的条款号是错的**，这比术语错误更隐蔽。")
w("")
w(f"**完整清单**：`references/digests/_INDEX.md`　**机读索引**：`references/digests/_index.json`")
w("")
w("### 机翻术语纠错表（已核实，逐条对齐英文原件）")
w("")
w("| 机翻译法 | 应为 | 英文原词 | 核实依据 |")
w("|---|---|---|---|")
for t in DIG.get("terms", []):
    w(f"| 「{t['bad']}」 | **{t['good']}** | `{t['en']}` | {t['evidence']} |")
w("")
w("> 用法：读到左列词时**心里替换成中间列**，引用时用英文原词。")
w("> 这样 L3 语料就从「完全不可用」变成「可用但需转译」。")
w("")
w("---")
w("")
w("## 五、扫描件（军标 / 国军标）")
w("")
w("以下军标/国军标在库，PDF 为**纯图像扫描**（每页一张图，0 字符文本层）。")
w("")
w("| 标准 | 类别 | 持有文件 | OCR 进度 | 备注 |")
w("|---|---|---|---|---|")
for v in C["scanned_held"]:
    parts = "；".join(
        f"`{p['file']}`" + ("（分卷）" if p.get("is_split") else "（全本）")
        for p in v["parts"])
    a = next((e for e in C["entries"] if e["std_id"] == v["std_id"]), {})
    n = ocr_pages(v["std_id"])
    w(f"| `{v['std_id']}` | {a.get('cat', '')} | {parts} | "
      f"{f'{n} 页' if n else '未 OCR'} | {a.get('key_points', '')} |")
w("")
w("> **OCR 的现实约束**（实测数据，非推测）：本机 OCR 实测 **36~130 秒/页**"
  "（RapidOCR PP-OCRv3，onnxruntime CPU；已试 1.30.0 与 1.22.0 两个版本、"
  "dpi 100/150/200/300 四档、强制 CPU 与默认两种 providers 配置，最快 36 s/页）。")
w("> 4 个军标合计 **2,229 页** → 全量 OCR 需约 **22~80 小时**，不具可行性。")
w(">")
w("> 因此采用**定向 OCR**：优先识别每份军标的**目录与方法索引页**"
  "（这是军标最有价值的部分——完整的方法号清单），而非全本。")
w("")
w("---")
w("")
w("## 六、军标方法索引（OCR 产出）")
w("")
if MM.get("standards"):
    w("> **来源**：本库对军标扫描件**目录页**的 OCR。**引用层级 L4-OCR**。")
    w(">")
    w("> **方法号可信**（四位数字）→ 可用于定位；**标题为 OCR 产物，引用前必须核对原页**。")
    w("")
    w("| 标准 | 方法号 | 有标题 | 目录页来源 | 同源参考 | 号段不连续处 |")
    w("|---|---:|---:|---:|---:|---|")
    from collections import Counter as _C
    for std, rows in MM["standards"].items():
        c = _C(r.get("source", "目录页") for r in rows)
        g = (MM.get("gaps", {}).get(std, {}) or {}).get("series_gaps", {})
        gs = "；".join(f"{s}xxx " + "、".join(
            (x["from"] if x["from"] == x["to"] else f"{x['from']}~{x['to']}")
            for x in v) for s, v in sorted(g.items())) or "—"
        w(f"| `{std}` | {len(rows)} | {sum(1 for r in rows if r['title'])} | "
          f"{c.get('目录页', 0)} | {c.get('同源标准参考', 0)} | {gs} |")
    w("")
    xc = MM.get("cross_validation", {})
    if xc:
        w("### 交叉校验（GJB 548 与 MIL-STD-883 方法号同源）")
        w("")
        w("| 标准 | 与 883 重合 | 仅本标准有 | 结论 |")
        w("|---|---|---|---|")
        for std, x in xc.items():
            if "agree_ratio" in x:
                w(f"| `{std}` | **{x['agree_ratio']}** | {x['gjb_only']} | "
                  f"两侧方法号高度一致，互为独立佐证 |")
        w("")
        w("> **这个校验的价值**：GJB 548 源自 MIL-STD-883，两者方法号应一致。")
        w("> 实测 99% 重合，说明**两侧的 OCR 与解析都没有系统性错位** ——")
        w("> 这是对方法索引可信度的一个独立验证，不是自证。")
        w("")
    w(f"**完整清单**：`references/MIL-METHODS.md`（{sum(len(v) for v in MM['standards'].values())} 条）"
      f"　**机读**：`references/mil-methods.json`")
else:
    w("（方法索引尚未生成）")
w("")
w("---")
w("")
w("## 七、已知的资料缺口")
w("")
w("| 缺口 | 影响 |")
w("|---|---|")
w("| JESD22 系列 37 份均无英文原文 | 术语类问题必须回 JEDEC 官网核对，不能凭本库作答 |")
w("| 机翻件条款号 20% 错位 | 引用条款号前必须回英文原文核对（digest 已还原，原语料未改） |")
w("| MIL-STD-883F/K、GJB 548B/C 为扫描件 | 全量 OCR 不可行（22~80 小时），仅做定向 OCR |")
w("| A104 在库版本为 **F（2020-11）**，非 **F.01** | 引用 F.01 独有内容时须标「本库未持有」 |")
w("| 无 IEC 60749 系列正文 | 涉及 IEC 的引用只能依赖 AQG 324 的引用表与二手资料 |")
w("| 无 AEC-Q100 正文 | 车规 IC 资格问题只能依赖 AQG 324 与 JESD47 |")
w("| 企业标准（VW80000/GMW/USCAR、客户 TS）均不可得 | 涉及时只能给反查路径 |")
w("")
w("> 缺口必须在回答中**显式声明**。宁可说「本库未覆盖，需回原文确认」，")
w("> 也不要给出看似完整但无出处的答案。")

(SKILL / "references" / "LOCAL-CORPUS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"→ {SKILL / 'references' / 'LOCAL-CORPUS.md'}")
print(f"   {len(L)} 行, {sum(len(x) for x in L):,} 字符")
