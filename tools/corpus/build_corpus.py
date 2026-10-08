"""蒸馏整合：把抽取出的语料 + 元数据，编译成 skill 可直接消费的资料库。

产出：
  data/corpus.json                      机器可读（供 stdq corpus / source 子命令）
  references/LOCAL-CORPUS.md            人读覆盖清单（类别/适用范围/关键条目/出处）

设计要点：
  ★ 引用分层（evidence tier）是本文件的核心。文件名已实测不可信
    （多份「英文电子版」实为机翻中文），因此一律以文档自述 + 实测语种定级。
  ★ 机翻件只能定位结构，不能引用术语译名 —— 已实测确证多例术语错误。
"""
from __future__ import annotations

import json
import pathlib
import re

SKILL = pathlib.Path(r"<skill 根目录>")
SRC = SKILL / "references" / "sources"
META = json.loads((SRC / "corpus_metadata.json").read_text(encoding="utf-8"))
INDEX = json.loads((SRC / "corpus_index.json").read_text(encoding="utf-8"))

# ---- 引用分层模型 -----------------------------------------------------------
TIERS = {
    "L1": {
        "name": "英文原文在库",
        "can_cite_wording": True,
        "can_cite_number": True,
        "rule": "可直接引用措辞与数值；引用时标注标准编号 + 版本 + 页/条",
    },
    "L2": {
        "name": "官方中文译本在库",
        "can_cite_wording": True,
        "can_cite_number": True,
        "rule": "可引用，但须注明「官方译本，冲突时以英文版为准」",
    },
    "L3": {
        "name": "机器翻译在库",
        "can_cite_wording": False,
        "can_cite_number": True,
        "rule": "仅可用于【条款号 / 章节结构 / 表格位置 / 数值条件】定位；"
                "**禁止引用其术语译名**（实测已有 Wire Bond→「线束」等硬错）",
    },
    "L4": {
        "name": "扫描件在库未提取",
        "can_cite_wording": False,
        "can_cite_number": False,
        "rule": "不得引用任何内容；只能声明「已持有该标准扫描件，未做文字识别」",
    },
    "L4-OCR": {
        "name": "扫描件已定向 OCR",
        "can_cite_wording": False,
        "can_cite_number": False,
        "rule": "可用于理解与索引；**引用条款号/数值前必须人工核对原扫描页**"
                "（OCR 是个别字符可能出错的过程）",
    },
    "L0": {
        "name": "不在库",
        "can_cite_wording": False,
        "can_cite_number": False,
        "rule": "必须声明无法确认，禁止推测或从记忆回答",
    },
}

# ---- 每份资料的蒸馏注解（人工判断：类别 / 适用范围 / 关键条目 / 出处）--------
# key = std_id（B116B_2 为英文原件的独立条目）
ANNO = {
    "JESD22-A100E": {
        "cat": "湿热/电化学", "scope": "循环温湿度偏压（带表面凝露）",
        "key": "CTC 循环剖面；凝露条件；与 A101 稳态 THB 的区别在'循环'与'凝露'",
    },
    "JESD22-A101D.01": {
        "cat": "湿热/电化学", "scope": "稳态温湿度偏压寿命（THB 85/85）",
        "key": "85±2°C / 85±5%RH / 1000h；Peck 模型的理论出处；无偏压变体见 A102/A118",
    },
    "JESD22-A102E": {
        "cat": "湿热/电化学", "scope": "加速耐湿—无偏压蒸煮（Autoclave / PCT）",
        "key": "121°C 饱和蒸汽、无偏压 → 考核封装吸湿与分层，**不含电化学腐蚀**",
    },
    "JESD22-A103E": {
        "cat": "热-电（存储）", "scope": "高温存储寿命 HTSL",
        "key": "Ta 150°C/1000h 族；考核金属间化合物生长、Kirkendall 空洞",
    },
    "JESD22-A104F": {
        "cat": "热-机械", "scope": "温度循环 TC（单/双/三箱，空气介质）",
        "key": "★ 13 组条件（A/B/C/G/H/I/J/K/L/M/N/R/T）+ 4 种 soak mode + 每条件典型 cph；"
               "§5 明确循环次数由 JESD47 或供需约定；§7 列出采购文件须规定项；"
               "表1 脚注给出 3 条选条件注意事项 + Pb/Sn 超 125°C 不推荐",
    },
    "JESD22-A105D": {
        "cat": "热-电耦合", "scope": "功率与温度循环 PTC（通电+环境箱叠加）",
        "key": "与 A122 的差别：A105 是「环境箱 + 通电自加热」组合，A122 是纯功率循环",
    },
    "JESD22-A106B.01": {
        "cat": "热-机械", "scope": "热冲击 TST（两液槽，转换 <10s）",
        "key": "★ 与 A104 的关键区别证据在此：依赖液体耦合介质的快速升降温",
    },
    "JESD22-A107C": {
        "cat": "环境腐蚀", "scope": "盐雾 Salt Atmosphere",
        "key": "盐雾浓度/温度/时长；考核引线框架与镀层",
    },
    "JESD22-A108F": {
        "cat": "热-电（偏压寿命）", "scope": "Temperature, Bias, and Operating Life（业界俗称 TBL/HTOL 母标准）",
        "key": "★ 官方标题为 Temperature, Bias, and Operating Life —— 无 Voltage；"
               "Ta 需使 Tj(min) ≥ 125°C；是 HTOL/HTRB/HTGB 的母方法",
    },
    "JESD22-A109B": {
        "cat": "封装完整性", "scope": "气密性 Hermeticity（细检/粗检）",
        "key": "氦细检泄漏率、氟碳粗检；判据按封装腔体积分档",
    },
    "JESD22-A110E": {
        "cat": "湿热/电化学", "scope": "HAST 高加速温湿度应力（有偏压）",
        "key": "★ 常用 130°C/85%RH、110°C/85%RH；与 THB 的优先关系由 IEC 60749-4 裁决",
    },
    "JESD22-A111B": {
        "cat": "工艺能力", "scope": "整器件浸焊评估底面贴装能力",
        "key": "小外形表面贴装器件底部焊接的评估程序",
    },
    "JESD22-A113I": {
        "cat": "预处理", "scope": "非气密封装器件可靠性试验前的预处理",
        "key": "★ 回流前烘烤 → 吸湿 → 3 次回流模拟 → 后续试验；与 J-STD-020 的 MSL 配合使用",
    },
    "JESD22-A117E": {
        "cat": "存储器专项", "scope": "EEPROM 擦写耐久与数据保持",
        "key": "擦写循环次数 + 数据保持（高温烘烤后读）双考核",
    },
    "JESD22-A118B.01": {
        "cat": "湿热/电化学", "scope": "无偏压 HAST（uHAST）",
        "key": "与 A110 的区别：**无偏压** → 只考核吸湿/分层，不考核电化学",
    },
    "JESD22-A119A": {
        "cat": "热-电（存储）", "scope": "低温存储寿命 LTSL",
        "key": "★ AQG 324 QL-04 的母方法（cond. A，1000h @ ≤-40°C）",
    },
    "JESD22-A120B": {
        "cat": "材料表征", "scope": "有机材料水分扩散系数与溶解度测量",
        "key": "为吸湿仿真提供 D 与 S 参数；不是可靠性试验，是材料参数试验",
    },
    "JESD22-A121A": {
        "cat": "失效机理专项", "scope": "锡及锡合金镀层锡须生长测量",
        "key": "★ 锡须浸泡模式 = 5~10 min，等价 soak mode 2（A104 §5.5.3 有交叉引用）",
    },
    "JESD22-A122A": {
        "cat": "热-电耦合", "scope": "功率循环 PC（纯通电加热）",
        "key": "★ 与 A104 机理不同：通电自加热 → 考核键合线/金属化/焊层；"
               "AQG 324 QL-01/QL-02 的车规化版本",
    },
    "JESD22-B100B": {"cat": "几何/外观", "scope": "物理尺寸", "key": "外形尺寸测量方法"},
    "JESD22-B101C": {"cat": "几何/外观", "scope": "外部目检 External Visual",
                     "key": "外观验收准则；与 B118（晶圆/芯片背面）配套"},
    "JESD22-B105E": {"cat": "机械应力", "scope": "引线完整性 Lead Integrity",
                     "key": "引线拉伸/弯曲疲劳；" },
    "JESD22-B106E": {"cat": "焊接耐受力", "scope": "通孔器件耐焊接热冲击",
                     "key": "波峰焊模拟下的耐热性"},
    "JESD22-B107D": {"cat": "标识", "scope": "标识永久性 Mark Permanency",
                     "key": "溶剂擦拭后标识保留；与 B114（标识可读性）配套"},
    "JESD22-B108B": {"cat": "几何/外观", "scope": "共面性 Coplanarity",
                     "key": "表面贴装器件引脚/焊球共面性测量"},
    "JESD22-B109C": {"cat": "互连强度", "scope": "倒装芯片拉伸拉脱 Flip Chip Tensile Pull",
                     "key": "★ 与 B115（焊球拉）区分：B109 是倒装凸点整体拉脱"},
    "JESD22-B110B.01": {"cat": "机械应力", "scope": "机械冲击（器件与子组件）",
                        "key": "冲击谱/峰值加速度"},
    "JESD22-B111A": {"cat": "板级可靠性", "scope": "手持产品板级跌落试验",
                     "key": "★ 板级（PCB 组装后）而非器件级；与 JESD22-B113 弯折互补"},
    "JESD22-B112B": {"cat": "几何/外观", "scope": "高温下封装翘曲测量",
                     "key": "★ 与回流温度相关的动态翘曲；是 BGA 焊接良率的关键参数"},
    "JESD22-B113B": {"cat": "板级可靠性", "scope": "板级循环弯折（互连可靠性表征）",
                     "key": "手持产品 SMT IC 互连弯折疲劳"},
    "JESD22-B114B": {"cat": "标识", "scope": "标识可读性 Mark Legibility",
                     "key": "字符可辨识度；与 B107（永久性）配套"},
    "JESD22-B115A.01": {"cat": "互连强度", "scope": "焊球拉脱 Solder Ball Pull",
                        "key": "★ 拉脱（pull）而非剪切（shear）；与 B117 区分"},
    "JESD22-B116B": {"cat": "互连强度", "scope": "键合线剪切 Wire Bond Shear",
                     "key": "★ 机翻件，术语不可引用（把 Wire Bond 译成「线束/钢丝」）。"
                            "英文原件见同目录 JESD22-B116B（英文原文条目）"},
    "JESD22-B116B_2": {"cat": "互连强度", "scope": "键合线剪切 Wire Bond Shear（★英文原文）",
                       "key": "★ 库里唯一的 B116B 英文原件，29 页版；"
                              "球键剪切工具几何、15~76µm 线径适用范围、破坏性试验"},
    "JESD22-B117B": {"cat": "互连强度", "scope": "焊球剪切 Solder Ball Shear",
                     "key": "★ 剪切（shear）而非拉脱；与 B115 区分"},
    "JESD22-B118": {"cat": "几何/外观", "scope": "晶圆与芯片背面外部目检",
                    "key": "背面外观验收准则；与 B101（封装外观）配套"},
    "JESD47L": {
        "cat": "资格标准（裁判）", "scope": "集成电路应力试验驱动型资格考核",
        "key": "★ 中英对照双语。Table1 零失效样本量 / Table2 器件考核 / Table3 非易失存储器附加 / "
               "Table4 ELFR 样本量（60% 置信度）/ Table5 非气密封装 / Table6 气密封装 / "
               "Table7 变更选型 / Table8 键合最小拉力 / Table10 90% 置信度最大不良率。"
               "正文明确：ELFR 按 60% 置信度评估；通用数据可用卡方分布按 90% 置信限换算；"
               "单件昂贵器件可用 1/3 样本量",
    },
    "JESD51-2A": {"cat": "热测试", "scope": "集成电路热测试环境条件—自然对流（静止空气）",
                  "key": "静止空气下的 Rθja 测试环境；与 JESD51-6 强制对流成对"},
    "JESD51-6": {"cat": "热测试", "scope": "集成电路热测试环境条件—强制对流（流动空气）",
                 "key": "风冷下的 Rθja 测试环境；风速与测试板规格相关"},
    "JS-001": {
        "cat": "电应力/ESD", "scope": "HBM 人体模型组件级 ESD 敏感度测试",
        "key": "★ 机翻件。JS-001-2017 新增 50V 测试级别与新分类（原文前言自述）；"
               "替代 JS-001-2014。分类等级须回英文原文核对",
    },
    "J-STD-020": {
        "cat": "封装/回流", "scope": "非气密封装湿敏等级 MSL 分级与回流分类",
        "key": "★ 机翻件。MSL 1~6 分级、回流峰值温度与 profile；"
               "与 JESD22-A113 预处理配套使用",
    },
    "IPC-7351": {
        "cat": "设计/焊盘图形", "scope": "表面贴装设计与连接盘图形通用要求（2005-02 原版）",
        "key": "★ 英文原文。2005 年 2 月版，取代 IPC-SM-782A（含修正 1&2）",
    },
    "IPC-7351B": {
        "cat": "设计/焊盘图形", "scope": "表面贴装设计与连接盘图形通用要求（2010-06 B 版）",
        "key": "★ 英文原文。取代 IPC-7351A（2007-02）；含密度等级 A/B/C 与焊盘生成公式",
    },
    "IPC-7095D": {
        "cat": "封装/组装工艺", "scope": "BGA 设计与组装工艺的实施（2019，含修正 1）",
        "key": "★ 官方中文译本（IPC-7095D-WAM1 CN，取代 IPC-7095D-2018）。"
               "文档自带声明：中英冲突以英文版为准",
    },
    "IPC-TM-650-2.4.22c": {
        "cat": "试验方法", "scope": "印制板弓曲与扭曲（bow & twist）测量",
        "key": "★ 英文原文。三种程序；非矩形样品的特殊处理",
    },
    "MIL-STD-883F": {"cat": "军标（试验方法）", "scope": "微电子器件试验方法与程序 F 版",
                     "key": "★ 扫描件，未文字识别。仅可声明持有（708 页全本 + 1-349/359-708 分卷）"},
    "MIL-STD-883K": {"cat": "军标（试验方法）", "scope": "微电子器件试验方法与程序 K 版",
                     "key": "★ 扫描件，未文字识别。仅可声明持有（768 页全本 + 1-399/400-768 分卷）"},
    "GJB-548B": {"cat": "国军标（试验方法）", "scope": "微电子器件试验方法和程序 B 版（2005）",
                 "key": "★ 扫描件，未文字识别。仅可声明持有（393 页全本 + 1-199/200-396 分卷）"},
    "GJB-548C": {"cat": "国军标（试验方法）", "scope": "微电子器件试验方法和程序 C 版（2021）",
                 "key": "★ 扫描件，未文字识别。仅可声明持有（460 页）"},
}


def tier_for(entry: dict) -> str:
    if entry["language"] == "en":
        return "L1"
    if entry["std_id"] == "IPC-7095D":
        return "L2"   # 官方中文译本（文档自带 conflict 声明）
    if entry["language"] == "bi":
        return "L2"
    return "L3"


# ---- 扫描件（无文本层）单独成组 -------------------------------------------------
OCR_DIR = SKILL / "references" / "sources" / "standards" / "mil_ocr"


def ocr_progress(std_id: str) -> dict:
    p = OCR_DIR / f"{std_id}.progress.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


scanned = {}
for e in INDEX["entries"]:
    if e.get("extracted") or e.get("already_in_skill"):
        continue
    scanned.setdefault(e["std_id"], {"std_id": e["std_id"], "org": e["org"],
                                     "file": e["file"], "parts": [],
                                     "sha16": e["sha16"]})
    scanned[e["std_id"]]["parts"].append(
        {"file": e["file"], "dup_in_group": e.get("dup_in_group"),
         "is_split": e.get("is_split")})

# ---- 组装 -------------------------------------------------------------------
out_entries = []
for m in META["entries"]:
    sid = m["std_id"]
    a = ANNO.get(sid, {})
    tier = tier_for(m)
    out_entries.append({
        "std_id": sid,
        "org": m["org"],
        "cat": a.get("cat", "未分类"),
        "scope": a.get("scope", ""),
        "key_points": a.get("key", ""),
        "tier": tier,
        "tier_name": TIERS[tier]["name"],
        "language": m["language"],
        "source_file": m["source_file"],
        "sha16": m["sha16"],
        "pdf_pages": m["pdf_pages"],
        "text_chars": m["text_chars"],
        "corpus_path": m["corpus_path"],
        "self_version_tokens": m["self_version_tokens"],
        "self_date_tokens": m["self_date_tokens"],
        "can_cite_wording": TIERS[tier]["can_cite_wording"],
        "can_cite_number": TIERS[tier]["can_cite_number"],
    })

# 扫描件也作为 L4 条目并入，让 CLI 能统一回答「这个标准在不在库」
for sid, v in scanned.items():
    a = ANNO.get(sid, {})
    prog = ocr_progress(sid)
    n_ocr = len(prog.get("done_pages", []))
    tier = "L4-OCR" if n_ocr else "L4"
    out_entries.append({
        "std_id": sid,
        "org": v["org"],
        "cat": a.get("cat", "军标（扫描件）"),
        "scope": a.get("scope", ""),
        "key_points": a.get("key", ""),
        "tier": tier,
        "tier_name": TIERS[tier]["name"],
        "language": "scan",
        "source_file": v["file"],
        "sha16": v["sha16"],
        "pdf_pages": None,
        "text_chars": 0,
        "corpus_path": (f"references/sources/standards/mil_ocr/{sid}.txt"
                        if n_ocr else None),
        "self_version_tokens": [],
        "self_date_tokens": [],
        "parts": v["parts"],
        "ocr": ({"pages_done": n_ocr, "pages_total": prog.get("total_pages"),
                 "engine": prog.get("engine"), "dpi": prog.get("dpi")}
                if n_ocr else None),
        "can_cite_wording": False,
        "can_cite_number": False,
    })

all_entries = out_entries
corpus = {
    "schema": 1,
    "built": "2026-10-07",
    "src_root": INDEX["src_root"],
    "extractor": INDEX["extractor"],
    "tiers": TIERS,
    "stats": {
        "pdf_files_total": INDEX["total_pdfs"],
        "distinct_std_ids_total": INDEX["distinct_std_ids"],
        "text_extracted": sum(1 for e in out_entries if e.get("corpus_path")),
        "entries_total": len(all_entries),
        "scanned_not_extracted": sum(len(v["parts"]) for v in scanned.values()),
        "scanned_distinct": len(scanned),
        "by_tier": {t: sum(1 for e in all_entries if e["tier"] == t) for t in TIERS},
    },
    "entries": sorted(all_entries, key=lambda x: (x["org"], x["std_id"])),
    "scanned_held": sorted(scanned.values(), key=lambda x: x["std_id"]),
}

(SKILL / "data" / "corpus.json").write_text(
    json.dumps(corpus, ensure_ascii=False, indent=1), encoding="utf-8")

print("=== 资料库统计 ===")
s = corpus["stats"]
for k, v in s.items():
    print(f"  {k:<24} {v}")
print("\n分层明细:")
for t, n in s["by_tier"].items():
    if n:
        print(f"  {t} {TIERS[t]['name']:<16} {n:>2} 份")
print("\n已提取条目:", len(out_entries))
print("扫描件（仅声明持有）:")
for v in corpus["scanned_held"]:
    print(f"  {v['std_id']:<16} {len(v['parts'])} 份文件")
print(f"\n→ {SKILL / 'data' / 'corpus.json'}")
