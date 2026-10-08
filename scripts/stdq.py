#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semiconductor-standards-master — 标准编号反查 CLI

零依赖（仅 Python 3 标准库：argparse / json / re / pathlib / difflib）。

用法：
  stdq find <编号>          # 反查：编号 → 标题/内容/状态
  stdq find <编号> --json   # 机器可读输出
  stdq refs <编号>          # 该标准引用了谁（上游依赖）
  stdq cited-by <编号>      # 谁引用了它（下游影响面）
  stdq classify <编号>      # 编号结构解析（体系/段语义/年代/状态词）
  stdq check <编号>         # 防错：误传纠正 + 废止拦截
  stdq tree [关键词]         # 测试方法分类树检索
  stdq unverified           # 查看全部未核实项
  stdq miscon               # 查看常见误传纠正表
  stdq stats                # 库统计

设计原则（对应 research/06-glossary.md §E2）：
  1. 版本号必须保留：A104 ≠ A104F.01
  2. F.01 是增补不是年份；JS-001-2017 中 2017 才是年份
  3. 失效编号先拦截并给替代项，不直接返回标题
  4. MIL-STD-883 必须四位
  5. 硬编码断言（JESD204≠DDR4 等）
  6. 未核实项只返回警示，不返回标题断言
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# ── 可信度标记 ────────────────────────────────────────────────
CONF = {"A": "A｜一手权威", "B": "B｜二手交叉验证", "C": "C｜待人工确认"}

# ── 编号归一化 ────────────────────────────────────────────────
SEP = re.compile(r"[\s_\-–—/\\.,()（）]+")
CASE_MAP = {"jedec": "JESD", "jesd": "JESD", "jesp": "JESD", "jep": "JEP", "js": "JS",
            "semiconductor": "", "std": "STD", "milstd": "MIL-STD", "iec": "IEC",
            "semi": "SEMI", "aec": "AEC", "aqg": "AQG", "ipc": "IPC", "j-std": "J-STD",
            "tf": "TF", "tft": "TFT"}


def norm(s: str) -> str:
    """归一化：全角转半角、去分隔符、统一大写。"""
    s = unicodedata.normalize("NFKC", s or "").strip()
    return SEP.sub("", s).upper()


def load(name: str) -> dict:
    p = DATA_DIR / name
    if not p.exists():
        print(f"[错误] 数据文件缺失: {p}", file=sys.stderr)
        sys.exit(2)
    with p.open(encoding="utf-8") as f:
        return json.load(f)


# ── 本地资料库（三层证据：编号库 / 全文语料 / 引用分层）────────
def load_corpus() -> dict:
    """本地资料库索引。缺失时返回空壳而不是退出——老版本仍可用。"""
    p = DATA_DIR / "corpus.json"
    if not p.exists():
        return {"entries": [], "scanned_held": [], "tiers": {}, "stats": {},
                "missing": True}
    with p.open(encoding="utf-8") as f:
        return json.load(f)


CORPUS = load_corpus()
CORPUS_BY_KEY: dict[str, list[dict]] = {}
for _e in CORPUS.get("entries", []):
    CORPUS_BY_KEY.setdefault(norm(_e["std_id"]), []).append(_e)


class Index:
    """库索引：多键归一化 → 记录。"""

    MAX_FUZZY = 5  # 降级路径命中上限：超过说明编号识别失败，应报未核实而非倾泻

    def __init__(self):
        self.db = load("standards.json")
        self.rel = load("relations.json")
        self.records = self.db["standards"]
        self.by_key: dict[str, list[dict]] = {}
        self._index()

    def _add(self, key: str, rec: dict, kind: str = "std"):
        k = norm(key)
        # ⚠ 安全闸：禁止把编号削成空壳（如 JESD22- → JESD22）——那会让 38 条记录共用一个键
        if not k or len(re.sub(r"[^A-Z0-9]", "", k)) < 3:
            return
        bucket = self.by_key.setdefault(k, [])
        rid = rec.get("id") or rec.get("old") or ""
        if any((b.get("id") or b.get("old")) == rid for b in bucket):
            return  # 去重：同一归一化键不重复追加同一条记录
        bucket.append({**rec, "_kind": kind})

    def _index(self):
        for r in self.records:
            sid = r["id"]
            for key in (sid, sid.replace("JESD", "JEDEC"), sid.replace("JESD", "JEDEC-"),
                        sid + r.get("version", ""), sid + r.get("version", "").replace(".", ""),
                        f"JEDEC {sid}"):
                self._add(key, r)
            # JESD22 方法的【裸组号+方法号】（A104 / A122 / B110 / C101）
            m = re.match(r"^JESD22-([ABC]\d+)([A-Z]?(\.\d+)?)$", sid)
            if m:
                self._add(m.group(1), r)                    # A104
                if m.group(2):
                    self._add(m.group(1) + m.group(2), r)  # A104F
        for d in self.db.get("deprecations", []):
            self._add(d["old"], d, kind="deprecated")
        # MIL-STD-883 四位方法号 → JESD22 映射索引（仅 1xxx 段可靠，见数据注释）
        for mnum, val in self.rel.get("milstd883_crossmap", {}).items():
            key = str(mnum).strip()
            if not key.isdigit():
                continue
            # 从描述中提取 JESD 编号（如 "...↔ JESD22-A108" → "JESD22-A108"）
            # ⚠ 不可用 re.split(r"[\s(（]")[0]，那是把整个描述当编号切
            mj = re.search(r"JESD22-[ABC]\d+|J-STD-\d+|IPC-[\w-]+", str(val))
            tgt = next((r for r in self.records if mj and r["id"] == mj.group(0)), None)
            if tgt:
                for pre in ("METHOD", "MILSTD883", "883", "MIL-STD-883"):
                    self._add(f"{pre}{key}", tgt)

    def lookup(self, raw: str) -> tuple[list[dict], str]:
        """五级降级解析。返回 (命中列表, 解析方式)。

        ⚠ 安全设计（三重）：
        1) 未核实清单最先拦截 —— 绝不返回标题断言
        2) 降级路径设 MAX_FUZZY 上限 —— 编号识别失败时报错，而非倾泻几十条
        3) JESD22-Axxx 形式（组别+3位方法号）若库中无该方法号，直接判定未命中，
           不允许退到模糊匹配（否则 A200 会匹配到 A120/A100 等无关方法）
        """
        n = norm(raw)
        # 0) 未核实清单拦截优先
        for u in self.db["unverified"]:
            if norm(u) == n:
                return [], "未核实清单内编号"

        # 0b) JESD22 完整方法号形式：库中无此方法号 → 直接未命中（禁止模糊兜底）
        # ⚠ norm() 已剥离连字符，故索引键与比较串均为无连字符形式（JESD22A104）
        mfull = re.match(r"^JESD22([ABC]\d{3})([A-Z]?(\.\d+)?)$", n)
        if mfull:
            base = f"JESD22{mfull.group(1)}"
            for cand in (base, base + (mfull.group(2) or "")):
                if cand in self.by_key:
                    return self.by_key[cand], "精确匹配"
            return [], f"库内无此方法号（{base}）"

        # 1) MIL-STD-883 四位方法号（须在剥分隔符前抽 4 位）
        m = re.search(r"(?:METHOD|M)?(\d{4})", (raw or "").upper())
        if m:
            for pre in ("METHOD", "MILSTD883", "883", "MIL-STD-883"):
                k = pre + m.group(1)
                if k in self.by_key:
                    return self.by_key[k], f"MIL-STD-883 方法 {m.group(1)} → 跨体系映射"
        if n in self.by_key:
            return self.by_key[n], "精确匹配"
        # 2) 去组织前缀
        for pre in ("JEDEC", "JESD", "IEC", "SEMI", "AEC", "IPC", "JSTD"):
            if n.startswith(pre) and n[len(pre):] in self.by_key:
                return self.by_key[n[len(pre):]], "去前缀匹配"
        # 3) 去 revision 后缀（带边界守卫 + 数量上限）
        b = re.sub(r"([A-Z])(\.?\d+)?$", "", n)
        if b != n and b in self.by_key and len(self.by_key[b]) <= self.MAX_FUZZY:
            return self.by_key[b], "去版本后缀匹配"
        # 4) 裸编号形式（JESD22 组别+方法号）已在索引中，此处不再模糊匹配
        #    但保留 MIL-STD-883 方法号（METHOD1010 / 1010 四位）→ 允许走映射
        if re.match(r"^([ABC]\d{3}|[A-Z]?\d+)$", n) and not re.match(r"^METHOD\d{4}$", n) \
                and not re.match(r"^\d{4}$", n):
            return [], "库内无此编号（不启用模糊匹配，避免误配）"
        # 5) 模糊匹配（数量上限保护）
        import difflib
        cand = difflib.get_close_matches(n, self.by_key.keys(), n=3, cutoff=0.82)
        if cand:
            out = []
            for c in cand:
                out += self.by_key[c]
            if len(out) <= self.MAX_FUZZY:
                return out, f"模糊匹配（{', '.join(cand)}）"
            return [], f"模糊匹配候选 {len(out)} 条（超过上限，已拒绝）"
        return [], "未命中"


IDX: Index | None = None


def get_idx() -> Index:
    global IDX
    if IDX is None:
        IDX = Index()
    return IDX


# ── 输出工具 ──────────────────────────────────────────────────
def out_json(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def print_rec(r: dict, level: int = 0) -> None:
    pad = "  " * level
    if r.get("_kind") == "deprecated":
        st = r.get("status", "废止")
        print(f"{pad}⚠ [{st}] {r['old']}  —— {r.get('old_title', '（标题未核实）')}")
        if r.get("replaced_by"):
            print(f"{pad}  → 替代: {r['replaced_by']}   动作: {r.get('action', '')}")
        else:
            print(f"{pad}  → 无替代。{r.get('action', '')}")
        print()
        return

    v = r.get("version", "")
    print(f"{pad}【{r['id']}】{(' 版本 ' + v) if v else ''}")
    print(f"{pad}  {r.get('title', '—')}")
    if r.get("title_zh"):
        print(f"{pad}  {r['title_zh']}")
    meta = []
    for k, lab in (("org", "组织"), ("group", "组别"), ("type", "类型")):
        if r.get(k):
            meta.append(f"{lab}={r[k]}")
    if r.get("date"):
        meta.append(f"日期={r['date']}")
    if r.get("status"):
        meta.append(f"状态={r['status']}")
    if meta:
        print(f"{pad}  " + " ｜ ".join(meta))
    print(f"{pad}  可信度: {CONF.get(r.get('confidence', 'C'), r.get('confidence', '?'))}")

    if r.get("note"):
        for line in wrap(r["note"], 78, pad + "  "):
            print(line)
    if r.get("conditions") and isinstance(r["conditions"], str):
        for line in wrap("条件: " + r["conditions"], 78, pad + "  "):
            print(line)
    if r.get("usage"):
        for line in wrap("用途: " + r["usage"], 78, pad + "  "):
            print(line)

    conds = r.get("conditions")
    if isinstance(conds, list):
        print(f"{pad}  ── 试验条件表（{len(conds)} 组）──")
        print(f"{pad}   {'条件':<6}{'Ts(min)':>9}{'Ts(max)':>9}{'ΔT':>7}{'cph':>10}  soak")
        for c in conds:
            dt = c["ts_max"] - c["ts_min"]
            print(f"{pad}   {c['id']:<7}{c['ts_min']:>8}{c['ts_max']:>9}{dt:>7}"
                  f"{c['cph']:>11}  {c['soak']}")
        if r.get("soak_modes"):
            print(f"{pad}   Soak Mode: " + ", ".join(
                f"{k}={v}" for k, v in r["soak_modes"].items()))
    if r.get("cautions"):
        print(f"{pad}  ── 原标准 CAUTION ──")
        for c in r["cautions"]:
            for line in wrap("• " + c, 78, pad + "    "):
                print(line)
    if r.get("solder_interconnect_reco"):
        for line in wrap("焊互连建议: " + r["solder_interconnect_reco"], 78, pad + "  "):
            print(line)
    if r.get("pc_physics"):
        print(f"{pad}  ── 功率循环物理（AQG 324 附录 II.D）──")
        for k, v in r["pc_physics"].items():
            for line in wrap(f"{k}: {v}", 78, pad + "    "):
                print(line)
    if r.get("url"):
        print(f"{pad}  原文: {r['url']}")
    if r.get("refs"):
        print(f"{pad}  引用: {', '.join(r['refs'])}")
    print()


def dw(s: str) -> int:
    """字符串显示宽度（中文/全角算 2）。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def wrap(text: str, width: int, pad: str) -> list[str]:
    """按显示宽度换行（中文算 2 宽）。pad 为续行前缀，不计入首行。"""
    out: list[str] = []
    limit = max(width - dw(pad), 20)
    cur, w = "", 0
    for ch in text:
        cw = 2 if unicodedata.east_asian_width(ch) in "WF" else 1
        if w + cw > limit:
            out.append(cur)
            cur, w = "", 0
        cur += ch
        w += cw
    if cur.strip():
        out.append(cur)
    return out


# ── 子命令 ────────────────────────────────────────────────────
def cmd_find(a) -> int:
    idx = get_idx()
    nq = norm(a.query)

    # 0) 三位 MIL-STD-883 方法号 → 编号错误（find 与 check 口径一致）
    m3 = re.search(r"M-?(\d{3})(?!\d)", a.query)
    if m3:
        print(f"✗ 编号错误: MIL-STD-883 方法号是【四位】，不存在三位号 M-{m3.group(1)}")
        print("  方法号区间: 1001-1034(环境) / 2001-2035(机械) / 3xxx(电气) / 5xxx(工艺)")
        print("  可用: stdq classify 'MIL-STD-883 Method 1010'")
        return 1

    # 1) 未核实项优先判定
    unv_exact = [u for u in idx.db["unverified"] if norm(u) == nq]
    hits, how = idx.lookup(a.query)
    if unv_exact and (not hits or how != "精确匹配"):
        print(f"⚠ 未命中 / 需人工核实: {a.query}")
        print("  此编号属【未核实清单】，库内不返回标题断言。")
        print(f"    未核实项: {unv_exact[0]}")
        print("    核实入口: JEDEC https://www.jedec.org/document_search")
        print("              IEC  https://webstore.iec.ch")
        return 1

    if not hits:
        unv = [u for u in idx.db["unverified"]
               if nq and (nq in norm(u) or norm(u) in nq)]
        print(f"✗ 未命中: {a.query}")
        print(f"  解析方式: {how}")
        if unv:
            print("  ⚠ 此编号属【未核实清单】，禁止断言其内容。")
            print(f"    需人工确认: {unv[0]}")
            print("    核实入口: JEDEC https://www.jedec.org/document_search")
        else:
            print("  建议核实入口: JEDEC document_search / IEC webstore / store-us.semi.org")
        return 1

    if a.json:
        out_json({"query": a.query, "match_type": how, "count": len(hits),
                  "results": [{k: v for k, v in h.items() if k != "_kind"} for h in hits]})
        return 0

    print(f"✓ 命中 {len(hits)} 条（{how}）\n")
    for h in hits:
        print_rec(h)
        print_corpus_note(h)
    check_assertions(a.query, hits)
    return 0


def print_corpus_note(rec: dict) -> None:
    """把「本地资料库持有情况」贴到每条 find 结果后——让引用纪律自动生效。

    这是本 skill 的关键机制：用户问某标准时，答案会自动带上
    「资料在不在库 / 能引用到什么程度」，不需要额外查询。
    """
    ids = [rec.get("id", "")]
    ids += rec.get("aka", []) or []
    hit = None
    for i in ids:
        if not i:
            continue
        if (c := CORPUS_BY_KEY.get(norm(i))):
            hit = c[0]
            break
    if not hit:
        # 版本无关匹配：JESD22-A104F.01 → 库里有 JESD22-A104F
        for i in ids:
            k = norm(i)
            if len(k) < 5:
                continue
            for ck, cv in CORPUS_BY_KEY.items():
                if ck.startswith(k) or k.startswith(ck):
                    hit = cv[0]
                    break
            if hit:
                break

    print()
    if not hit:
        print("  ⚫ 本地资料库：**未持有该标准全文** → 条款内容只能声明「无法确认」")
        print("     （可查 `stdq corpus` 看全库范围）")
        return

    print(f"  {TIER_ICON[hit['tier']]} 本地资料库：{hit['tier']}｜{hit['tier_name']}")
    if hit.get("corpus_path"):
        print(f"     全文语料: {hit['corpus_path']}")
    if not hit.get("can_cite_wording"):
        print("     ⚠ 该资料**不可直接引用原文措辞**"
              + ("（机翻件，术语须回英文原文）" if hit["tier"] == "L3"
                 else "（扫描件，未做文字识别）"))
    if hit["tier"] == "L0":
        pass
    print(f"     出处: {hit['source_file']}")
    print(f"     详情: stdq source {hit['std_id']}")


def check_assertions(q: str, hits: list[dict]) -> None:
    """硬编码断言与误传纠正。"""
    n = norm(q)
    for m in get_idx().db.get("misconceptions", []):
        key = norm(re.sub(r"[A-Za-z]+\d+(-\d+)?", lambda x: x.group(0), m["wrong"]))
        if n and (n in norm(m["wrong"]) or norm(m["wrong"]) in n) and len(n) > 4:
            print(f"⚠ 常见误传纠正（{CONF.get(m['confidence'], m['confidence'])}）")
            print(f"  误: {m['wrong']}")
            print(f"  实: {m['truth']}\n")


def cmd_refs(a) -> int:
    idx = get_idx()
    hits, how = idx.lookup(a.query)
    if not hits:
        print(f"✗ 未命中: {a.query}")
        return 1
    sid = hits[0]["id"] if hits[0].get("_kind") != "deprecated" else hits[0]["old"]
    edges = [e for e in idx.rel["edges"]
             if norm(e["src"]) == norm(sid) and e["kind"] in ("normative", "informative", "replaced_by")]
    if a.json:
        out_json({"src": sid, "refs": edges})
        return 0
    print(f"← {sid} 引用了以下标准（{how}）\n")
    if not edges:
        print("  （库内无已核实的引用边）")
    icon = {"normative": "◆规范性", "informative": "◇资料性", "replaced_by": "→替代"}
    for e in edges:
        print(f"  {icon.get(e['kind'], '·')} {e['dst']}  [{CONF.get(e.get('confidence', 'C'))}]")
        if e.get("clause"):
            print(f"     条款/场景: {e['clause']}")
        if e.get("note"):
            print(f"     注: {e['note']}")
    print(f"\n  ⚠ {idx.rel['_meta']['coverage_caveat']}")
    return 0


def cmd_cited_by(a) -> int:
    idx = get_idx()
    hits, how = idx.lookup(a.query)
    if not hits:
        print(f"✗ 未命中: {a.query}")
        return 1
    sid = hits[0]["id"] if hits[0].get("_kind") != "deprecated" else hits[0]["old"]
    edges = [e for e in idx.rel["edges"] if norm(e["dst"]) == norm(sid)]
    if a.json:
        out_json({"dst": sid, "cited_by": edges})
        return 0
    print(f"→ 引用了 {sid} 的标准（{how}）\n")
    if not edges:
        print("  （库内无已核实的反向引用边）")
    for e in edges:
        print(f"  {e['src']}   [{e['kind']} / {CONF.get(e.get('confidence', 'C'))}]")
        if e.get("clause"):
            print(f"     {e['clause']}")
        if e.get("note"):
            print(f"     注: {e['note']}")
    # AQG 324 引用构成（原本是死数据，接入输出）
    prof = idx.rel.get("aqg324_references_profile")
    if prof and norm(sid) in ("AQG324", "AQG", "AQG32404.1"):
        print(f"\n  ── AQG 324 引用构成（04.1/2025 一手核实）──")
        for k, v in prof.items():
            if not k.startswith("_") and isinstance(v, (int, float)):
                bar = "█" * int(v * 50)
                print(f"    {k:<16} {v*100:>5.0f}%  {bar}")
        if prof.get("_critical"):
            for line in wrap(prof["_critical"], 76, "      "):
                print(line)
    print(f"\n  ⚠ {idx.rel['_meta']['coverage_caveat']}")
    return 0


PATTERNS = [
    ("JESD22", r"^JESD22-?([ABC])(\d+)", "JEDEC JESD22 方法",
     "第2段字母=应力类别（A 环境/寿命 · B 机械/几何 · C 电/ESD），第3段=方法号，尾字母=版本"),
    ("JEDEC-top", r"^JESD(\d+)", "JEDEC 顶级标准",
     "资格标准/术语/接口类，非方法库"),
    ("JEDEC-JEP", r"^JEP(\d+)", "JEDEC 实践说明（JEP）", "方法论/加速模型/测量类参考文件"),
    ("JEDEC-JS", r"^JS-?(\d{3})", "ESDA/JEDEC 联合标准", "后缀年份（如 2017）是年份"),
    ("MILSTD", r"^(?:MIL-?STD-?883)?METHOD(\d{4})", "MIL-STD-883 微电路试验方法",
     "⚠ 方法号必须四位；首位数字=域（1 环境 / 2 机械 / 3 电气 / 5 工艺）"),
    ("IEC", r"^IEC(\d{5})-?(\d+)?", "IEC 国际标准",
     "6 位主编号=领域，其后 Part 号=具体部分"),
    ("SEMI", r"^SEMI([A-Z]+)(\d+)", "SEMI 行业标准",
     "字母前缀=板块（M 材料 / N 设备 / T 测试 / E 设备 / S 安全 / F 设施），序号越大通常越新"),
    ("AEC", r"^AEC-?Q(\d{3})", "AEC 汽车电子委员会",
     "Q100=IC / Q101=分立半导体 / Q2xx-Q3xx=其他元件"),
    ("AQG", r"^AQG(\d{3})", "AQG 汽车资格指南", "由 ECPE 持有"),
    ("IPC-TM", r"^IPC-?TM-?(\d+)", "IPC 试验方法", "数字段=方法大类，格式 2.x.x"),
    ("IPC-A", r"^IPC-?A-?(\d+)", "IPC 电子组件要求", "可接受性/焊点/封装要求"),
    ("J-STD", r"^J-?STD-?(\d+)", "J-STD 联合标准", "IPC/JEDEC/AESA 联合，焊料与元器件互连"),
]


def cmd_classify(a) -> int:
    idx = get_idx()
    n = norm(a.query)
    for name, pat, kind, desc in PATTERNS:
        m = re.match(pat, n)
        if not m:
            continue
        if a.json:
            out_json({"input": a.query, "system": kind, "structure": desc,
                      "groups": list(m.groups())})
            return 0
        print(f"体系: {kind}")
        print(f"结构: {desc}")
        print(f"解析: {a.query} → {list(m.groups())}")
        hits, how = idx.lookup(a.query)
        if hits:
            print(f"\n库内状态: {how}")
            print_rec(hits[0])
        else:
            unv = [u for u in idx.db["unverified"] if norm(u) == n or n in norm(u)]
            if unv:
                print(f"\n⚠ 未核实项: {unv[0]} —— 禁止断言内容")
        return 0
    print(f"✗ 无法识别编号体系: {a.query}")
    print("  可识别: " + ", ".join(p[0] for p in PATTERNS))
    return 1


def cmd_check(a) -> int:
    idx = get_idx()
    n = norm(a.query)
    issues = 0

    m = re.search(r"M-?(\d{3})(?!\d)", a.query)
    if m:
        print(f"✗ 编号错误: MIL-STD-883 方法号是【四位】，不存在三位号 M-{m.group(1)}")
        print("  方法号区间: 1001-1034(环境) / 2001-2035(机械) / 3xxx(电气) / 5xxx(工艺)")
        issues += 1

    for dep in idx.db["deprecations"]:
        if norm(dep["old"]) == n or n in norm(dep["old"]):
            print(f"⚠ 已废止/被替代: {dep['old']}  [{dep.get('status', '')}]")
            print(f"  原标题: {dep.get('old_title', '（未核实）')}")
            print(f"  → 替代: {dep.get('replaced_by') or '无'}")
            print(f"  动作: {dep.get('action', '')}")
            issues += 1
            break

    for mis in idx.db.get("misconceptions", []):
        wn = norm(mis["wrong"])
        if n and len(n) > 3 and (n in wn or wn in n):
            print(f"⚠ 常见误传 [{CONF.get(mis['confidence'])}]")
            print(f"  误: {mis['wrong']}")
            print(f"  实: {mis['truth']}\n")
            issues += 1

    unverified_hit = None
    if norm(a.query) in [norm(u) for u in idx.db["unverified"]]:
        unverified_hit = norm(a.query)
        print("⚠ 此编号属【未核实清单】—— 禁止返回标题断言，需人工核实")
    else:
        # 包含/前缀匹配：清单项可能是「JESD22-A200 系列全部」这类描述
        nq = norm(a.query)
        part = [u for u in idx.db["unverified"]
                if nq and len(nq) > 3 and (nq in norm(u) or norm(u).startswith(nq))]
        if part:
            unverified_hit = part[0]
            print(f"⚠ 此编号属【未核实清单】—— 禁止返回标题断言，需人工核实")
            print(f"    对应清单项: {part[0]}")

    # 无异常时给出显式回执——否则调用方无法区分「检查通过」与「什么都没查到」
    if issues == 0 and not unverified_hit:
        hits, how = idx.lookup(a.query)
        if hits:
            h = hits[0]
            title = h.get("title") or h.get("title_zh") or ""
            print(f"✓ 未发现误传/废止问题: {a.query}  [{h.get('id', '')}]"
                  f"{'  ' + title if title else ''}   （匹配方式: {how}）")
            print(f"  状态: {h.get('status', '（未标注）')}｜ 可信度: "
                  f"{CONF.get(h.get('confidence'), h.get('confidence'))}")
            ca = h.get("cautions") or []
            if ca:
                print(f"  注意: 该条目带 {len(ca)} 条 CAUTION，用前先读 "
                      f"`stdq find {a.query}`")
        else:
            print(f"⚠ 库中无此编号: {a.query} —— 可能拼写错误或超出本库覆盖范围。"
                  f"禁止编造标题，须回标准原文核对。")
            return 1

    return 1 if issues else 0


TREE = {
    "L1 热-机械": {
        "温度循环类": ["JESD22-A104 (TC)", "JESD22-A106 (TST 热冲击)", "IPC-9704 (板级温循)"],
        "功率循环类(热-电耦合)": ["JESD22-A122 (PC 功率循环)", "JESD22-A105 (PTC 功率温度循环)",
                        "AQG 324 QL-01/QL-02 + IEC 60749-34 (PCsec/PCmin 双轨)"],
        "机械应力类": ["JESD22-B103 (变频振动)", "JESD22-B110 (机械冲击)", "JESD22-B111 (板级跌落)",
                   "JESD22-B113 (板级循环弯折/互连)", "JESD22-B105 (引线完整性)", "JESD22-B116 (键合线剪切)"],
        "几何尺寸类": ["JESD22-B115 (焊球剪切)", "JESD22-B109 (倒装拉脱)", "JESD22-B108 (共面性)",
                  "JESD22-B112 (高温翘曲)"],
    },
    "L2 热-电（偏压寿命）": ["JESD22-A108 (TBL/HTOL 母标准)", "IEC 60749-3 (HTRB)", "AQG 324 HTGB (半数正压半数负压)",
                     "JESD22-A103 (HTSL 高温存储)", "JESD22-A119 (LTSL 低温存储)", "JESD22-A109 (气密性)"],
    "L3 湿热/电-化学": ["JESD22-A101 (THB 85/85, 1000h)", "JESD22-A100 (循环湿热)", "JESD22-A110 (HAST 有偏压)",
                  "JESD22-A118 (uHAST 无偏压)", "JESD22-A102 (蒸煮 AC)", "H3TRB / HV-H3TRB (AEC-Q101 加严项)",
                  "JESD22-A113 (预处理 PC，TC/HAST 前必做)"],
    "L4 电应力/ESD": ["JS-001-2017 (HBM 器件级)", "JS-002-2018 (CDM 器件级)",
                 "JESD22-A115 (MM 机器模型, inactive)", "JESD78 (闩锁 —— 注意与 ESD 无关)"],
    "L5 键合与互连专项": ["IPC-SM-785 (焊点疲劳加速指南)", "MIL-STD-883 2011/2012 (键合拉力/剪切)",
                   "JESD22-B109 / 内部规范 (焊层空洞 X-ray/SAM)", "85/85 后 FA (ECM/迁移)"],
    "L6 失效分析辅助": ["JESD22-B101 (外观目检)", "JESD22-B107/B114 (标识耐久/可读)",
                  "J-STD-002D (可焊性)", "JESD22-A121 (锡须)", "MIL-STD-883 5xxx (切片金相/SEM/EDS)"],
}

PHENOMENA = {
    "焊点开裂": ("TC (A104) / PC (A122 / AQG 324 QL-01~02)", "焊层剪切率下降、A104 §7(d) special acceptance criteria"),
    "键合线疲劳": ("PC 短 ton (PCsec, ton<5s)", "拉力下降 ≥ 20% (AQG 324)"),
    "陶瓷基板裂纹": ("TC / PC", "X-ray 空洞、切片裂纹"),
    "分层/popcorn": ("预处理 PC + 蒸煮/HAST", "饱和气泡密度、MSL 分级"),
    "塑封料开裂(超 Tg)": ("先核对 Tg 再定 TC 条件", "A104 CAUTION 1"),
    "栅氧退化": ("TBL/A108、TDDB", "漂移率、Weibull β"),
    "ECM/腐蚀": ("THB 85/85", "漏电流、绝缘电阻"),
    "锡须": ("A121", "须晶高度/密度"),
}


def cmd_tree(a) -> int:
    kw = (a.query or "").strip()
    if not kw:
        print("=== 测试方法分类树（按失效物理机理组织，跨标准体系）===\n")
        for l1, subs in TREE.items():
            print(f"{l1}")
            if isinstance(subs, dict):
                for l2, items in subs.items():
                    print(f"  {l2}")
                    for it in items:
                        print(f"    · {it}")
            else:
                for it in subs:
                    print(f"    · {it}")
            print()
        print("=== 失效现象 → 试验 → 判据速查 ===\n")
        for k, (t, j) in PHENOMENA.items():
            print(f"  {k:<18} → {t}")
            print(f"  {'':<18}   判据: {j}")
        return 0

    for k, (t, j) in PHENOMENA.items():
        if kw in k or kw in t or kw in j:
            print(f"{k}  →  试验: {t}\n{'':<20}判据: {j}")
            return 0
    for l1, subs in TREE.items():
        blob = json.dumps(subs, ensure_ascii=False)
        if kw in l1 or kw in blob:
            print(f"匹配: {l1}\n{json.dumps(subs, ensure_ascii=False, indent=2)}")
            return 0
    print(f"✗ 未匹配: {kw}（试试 '焊点' / '湿热' / 'ESD' / '分层'）")
    return 1


def cmd_unverified(a) -> int:
    idx = get_idx()
    u = idx.db["unverified"]
    print(f"⚠ 未核实项清单（{len(u)} 项）—— CLI 对这些禁止返回标题断言\n")
    for i, x in enumerate(u, 1):
        print(f"  {i:>2}. {x}")
    print(f"\n核实入口: {idx.db['fallback_urls']['JEDEC 文档检索']}")
    return 0


def cmd_miscon(a) -> int:
    idx = get_idx()
    m = idx.db["misconceptions"]
    print(f"常见误传纠正表（{len(m)} 条，全部来自一手核实）\n")
    for i, x in enumerate(m, 1):
        print(f"{i:>2}. [{CONF.get(x['confidence'], x['confidence'])}]")
        print(f"    误: {x['wrong']}")
        print(f"    实: {x['truth']}\n")
    return 0


def _aqg() -> dict:
    for r in get_idx().db["standards"]:
        if r["id"] == "AQG324":
            return r
    return {}


STAT_LABELS = {
    "distribution": "分布选择", "B_value": "B 值要求", "confidence": "置信度",
    "allowed_alt": "允许的替代法", "documentation": "须记录的过程",
    "data_reuse": "数据复用", "user_relevance": "工程含义",
}

QL_LABELS = {
    "physics": "考核物理", "ton": "导通时间 ton", "IL": "负载电流 IL", "Vgate": "栅压 Vgate",
    "Qcool": "冷却流量", "eol": "EOL 判据", "requirement": "要求", "note": "注",
    "hard_rules": "硬性规则", "duration": "试验时长", "Ta": "环境温度 Ta",
    "Tvj": "结温 Tvj", "VCE/VDS/VR": "阻断电压", "VGE/VGS": "栅压",
    "VCE/VDS": "漏源电压", "variant": "电压变体", "load": "负载方式",
    "critical_note": "⚠ 官方警告", "applicability": "适用性", "records": "须记录",
    "targets": "考核目标", "extra": "附加要求", "base_method": "母方法",
    "table": "条件表", "status": "状态", "purpose": "目的", "three_methods": "三种评估路径",
    "failure_criterion": "失效判据", "mode": "测试模式", "VDS": "漏源电压",
    "VDS,DC": "直流测试电压", "ABS(dVGS/dt)": "栅压摆率", "f": "开关频率", "duty": "占空比",
    "VGS,on": "开态栅压", "VGS,off": "关态栅压", "ID": "漏极电流 IDS",
    "RH": "相对湿度", "dV/dt turn on": "开通 dV/dt", "dV/dt turn off": "关断 dV/dt",
    "dV/dt on/off": "dV/dt（开通/关断）",
}


def cmd_ql(a) -> int:
    """AQG 324 第9章 QL 试验条件查询：stdq ql QL-01 / stdq ql PCsec"""
    rec = _aqg()
    ql = rec.get("ql_tests", {})
    if a.json:
        out_json({"aqg324": rec.get("version"), "ql_tests": ql})
        return 0
    q = a.query.strip().upper()
    if not q:
        print(f"◀ AQG 324 {rec.get('version')} 试验清单（{len([k for k in ql if not k.startswith('_')])} 项）\n")
        for k, v in ql.items():
            if k.startswith("_"):
                continue
            st = v.get("status", "")
            print(f"  {k.split('_')[0]:<8} {v.get('name',''):<52} {st}")
        print("\n  用法: stdq ql <编号或名称>  例: stdq ql QL-01 / stdq ql PCsec / stdq ql H3TRB")
        return 0
    hits = []
    for key, v in ql.items():
        if key.startswith("_"):
            continue
        if q in key.upper() or (q and q in str(v.get("name", "")).upper()):
            hits.append((key, v))
    if not hits:
        print(f"✗ 未命中: {a.query}")
        print("  可用编号: " + ", ".join(k.split("_")[0] for k in ql if not k.startswith("_")))
        print("  可用名称: PCsec / PCmin / HTS / LTS / HTRB / HTGB / H3TRB / HTFB / DGS / DRB")
        return 1
    print(f"◀ AQG 324 {rec.get('version')}  {rec.get('date')}  —— 一手条件表\n")
    for key, v in hits:
        print("─" * 78)
        print(f"【{key.split('_')[0]}】{v.get('name','')}")
        if v.get("table"):
            print(f"  条件表: {v['table']}")
        if v.get("status"):
            print(f"  ⚠ 状态: {v['status']}")
        if v.get("base_method"):
            bm = v["base_method"]
            print(f"  母方法: {', '.join(bm) if isinstance(bm, list) else bm}")
        for k, v2 in v.items():
            if k.startswith("_") or k in ("name", "table", "base_method"):
                continue
            if isinstance(v2, list):
                print(f"  {QL_LABELS.get(k, k)}:")
                for x in v2:
                    for j, ln in enumerate(wrap(str(x), 72, "     ")):
                        print(("     · " + ln) if j == 0 else "       " + ln)
            else:
                lbl = QL_LABELS.get(k, k)
                pad = " " * (dw(lbl) + 3)
                for i, ln in enumerate(wrap(str(v2), 78, pad)):
                    print(f"  {lbl}: {ln}" if i == 0 else f"  {pad}{ln}")
        print()
    print("─" * 78)
    print("⚠ ΔTvj 温升与循环次数 AQG 324 不规定，由模块厂按寿命模型自定；标准只给边界与判据。")
    print("⚠ 全部数据来源: references/sources/books/AQG324_04.1_2025.pdf（本地全文可查）")
    return 0


def cmd_aqg(a) -> int:
    """AQG 324 引用构成与统计判据"""
    idx = get_idx()
    rec = _aqg()
    prof = idx.rel.get("aqg324_references_profile", {})
    if a.json:
        out_json({"references_profile": prof, "statistics": rec.get("statistics"),
                  "lifetime_models": rec.get("lifetime_models"),
                  "doc_defects": rec.get("doc_defects")})
        return 0
    print(f"◀ AQG 324 {rec.get('version')} 引用构成（{prof.get('_note','')}）\n")
    cnt = prof.get("_count_by_org", {})
    tot = sum(cnt.values()) or 1
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        share = v / tot * 100
        bar = "█" * max(1, int(share / 3))
        print(f"  {k:<22} {v:>4} 次  {share:>5.1f}%  {bar}")
    if prof.get("iec_breakdown"):
        print("\n  IEC 内部拆分:")
        for k, v in prof["iec_breakdown"].items():
            print(f"    {k:<22} {v} 个 Part")
    print()
    for key in ("_structural_insight", "_correction_vs_v1", "_critical"):
        for i, ln in enumerate(wrap(prof.get(key, ""), 76, "    ")):
            print(("  " + ln) if i == 0 else ln)
    st = rec.get("statistics", {})
    if st:
        print("\n  强制统计判据（Annex I.C）:")
        for k in ("distribution", "B_value", "confidence", "allowed_alt",
                  "documentation", "data_reuse", "user_relevance"):
            if st.get(k):
                lbl = STAT_LABELS.get(k, k)
                pad = " " * (dw(lbl) + 3)
                for i, ln in enumerate(wrap(str(st[k]), 78, pad)):
                    print(("  " + lbl + ": " + ln) if i == 0 else "  " + pad + ln)
    dd = rec.get("doc_defects") or []
    if dd:
        print("\n  ⚠ 文档自身缺陷（引用时须注意）:")
        for x in dd:
            for i, ln in enumerate(wrap(str(x), 82, "    ")):
                print(("  " + ln) if i == 0 else ln)
    return 0


def cmd_ql_lifetime(a) -> int:
    """AQG 324 Annex II.B 寿命公式"""
    rec = _aqg()
    lm = rec.get("lifetime_models", {})
    if a.json:
        out_json(lm)
        return 0
    print("◀ AQG 324 Annex II.B 寿命模型（一手转录）\n")
    for k, v in lm.items():
        if k == "_note":
            continue
        if k == "engineering_insights":
            continue
        print(f"  【{k}】")
        for i, ln in enumerate(wrap(str(v), 72, "     ")):
            print("  " + ln)
        print()
    print("  【工程洞见（一手数据）】")
    for i, x in enumerate(lm.get("engineering_insights", []), 1):
        for j, ln in enumerate(wrap(str(x), 72, "     ")):
            print(f"  {i}. {ln}" if j == 0 else ln)
    return 0


def cmd_stats(a) -> int:
    idx = get_idx()
    recs = idx.db["standards"]
    by_org: dict = {}
    by_conf: dict = {}
    for r in recs:
        by_org[r["org"]] = by_org.get(r["org"], 0) + 1
        by_conf[r.get("confidence", "?")] = by_conf.get(r.get("confidence", "?"), 0) + 1
    print(f"库统计（built {idx.db['_meta']['built_date']}）\n")
    print(f"  标准条目: {len(recs)}")
    print(f"  引用边:   {len(idx.rel['edges'])}")
    print(f"  废止/替代: {len(idx.db['deprecations'])}")
    print(f"  未核实项: {len(idx.db['unverified'])}")
    print(f"  误传纠正: {len(idx.db['misconceptions'])}")
    print("\n  按组织:")
    for k, v in sorted(by_org.items(), key=lambda x: -x[1]):
        print(f"    {k:<8} {v}")
    print("\n  按可信度:")
    for k, v in sorted(by_conf.items()):
        print(f"    {CONF.get(k, k)}  {v}")
    a0 = by_conf.get("A", 0)
    print(f"\n  一手(A)占比: {a0}/{len(recs)} = {a0 * 100 // max(len(recs), 1)}%")
    return 0


# ── 本地资料库子命令 ──────────────────────────────────────────
TIER_ICON = {"L1": "🟢", "L2": "🟡", "L3": "🟠", "L4": "🔴", "L4-OCR": "🔵",
             "L0": "⚫"}


def _load_digest_index() -> dict:
    p = DATA_DIR.parent / "references" / "digests" / "_index.json"
    if not p.exists():
        return {}
    try:
        with p.open(encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


DIGEST = _load_digest_index()
DIGEST_BY = {norm(d["std_id"]): d for d in DIGEST.get("entries", [])}


def _tier_line(e: dict) -> str:
    return f"{TIER_ICON.get(e['tier'], '?')} {e['tier']}｜{e.get('tier_name', '')}"


def cmd_corpus(a) -> int:
    if CORPUS.get("missing"):
        print("⚠ 本地资料库索引不存在（data/corpus.json）——"
              "本 skill 目前只有编号库，无法回答「资料在不在库」")
        return 1
    s = CORPUS["stats"]
    if getattr(a, "json", False):
        print(json.dumps({"stats": s, "tiers": CORPUS["tiers"],
                          "entries": CORPUS.get("entries", []),
                          "scanned_held": CORPUS.get("scanned_held", [])},
                         ensure_ascii=False, indent=1))
        return 0

    print(f"本地资料库　built {CORPUS.get('built')}")
    print(f"  来源根目录: {CORPUS.get('src_root')}")
    print(f"  提取方式:   {CORPUS.get('extractor')}")
    print()
    print(f"  源 PDF 文件总数:        {s.get('pdf_files_total')}")
    print(f"  去重后不同标准编号:     {s.get('distinct_std_ids_total')}")
    print(f"  已提取文本层:           {s.get('text_extracted')} 份")
    print(f"  扫描件(持有未识别):     {s.get('scanned_not_extracted')} 份文件 "
          f"/ {s.get('scanned_distinct')} 个标准")
    print()
    print("  ── 引用分层（决定能引用到什么程度）──")
    for k in ("L1", "L2", "L3", "L4"):
        n = s.get("by_tier", {}).get(k, 0)
        if not n:
            continue
        t = CORPUS["tiers"][k]
        w = "可引措辞" if t["can_cite_wording"] else "禁引措辞"
        num = "可引数值" if t["can_cite_number"] else "禁引数值"
        print(f"    {TIER_ICON[k]} {k} {t['name']:<16} {n:>2} 份   [{w} / {num}]")
    print()
    print("  ⚠ 文件名不可信：多份标注「完整英文电子版」者实为机翻中文。")
    print("    层级由文档自述 + 实测语种判定。用 `stdq source <编号>` 查单份。")
    return 0


def cmd_source(a) -> int:
    """查单份标准的出处与引用规则——回答「这句话能不能这么写」。"""
    hits = CORPUS_BY_KEY.get(norm(a.query), [])
    if not hits:
        # 退一步模糊匹配
        n = norm(a.query)
        hits = [e for e in CORPUS.get("entries", [])
                if n and len(n) > 3 and (n in norm(e["std_id"])
                                         or norm(e["std_id"]) in n)]
    if getattr(a, "json", False):
        print(json.dumps(hits or {"found": False, "query": a.query},
                         ensure_ascii=False, indent=1))
        return 0 if hits else 1

    if not hits:
        print(f"⚫ 本地资料库【未持有】: {a.query}")
        print("  → 关于该标准的任何条款内容，只能声明「无法确认」，")
        print("     禁止凭记忆或推测作答。可查 `stdq corpus` 看全库范围。")
        return 1

    for e in hits:
        print("─" * 74)
        print(f"【{e['std_id']}】 {_tier_line(e)}")
        if e.get("cat"):
            print(f"  类别:     {e['cat']}")
        if e.get("scope"):
            print(f"  适用范围: {e['scope']}")
        if e.get("key_points"):
            print(f"  关键条目: {e['key_points']}")
        if e.get("self_version_tokens"):
            print(f"  文档自述版本: {'、'.join(e['self_version_tokens'][:4])}")
        if e.get("self_date_tokens"):
            print(f"  文档自述日期: {'、'.join(e['self_date_tokens'][:3])}")
        print(f"  规模:     {e.get('pdf_pages') or '—'} 页 / "
              f"{e.get('text_chars') or 0:,} 文本字符")
        print(f"  源文件:   {e['source_file']}")
        print(f"  SHA256(16): {e.get('sha16')}")
        if e.get("corpus_path"):
            print(f"  全文语料: {e['corpus_path']}")
        else:
            print("  全文语料: （无 —— 扫描件，未做文字识别）")
        if e.get("parts"):
            for p in e["parts"]:
                print(f"     分卷: {p['file']}")
        t = CORPUS["tiers"].get(e["tier"], {})
        print(f"  引用规则: {t.get('rule', '')}")
    return 0


def cmd_digest(a) -> int:
    """查某标准的条款级 digest（章节结构 + 数值条件 + 术语纠错）。"""
    if not DIGEST:
        print("⚠ digest 索引不存在（references/digests/_index.json）")
        return 1
    if getattr(a, "all", False):
        if getattr(a, "json", False):
            print(json.dumps(DIGEST, ensure_ascii=False, indent=1))
            return 0
        print(f"条款级 digest 索引（{DIGEST.get('count')} 份）")
        print("=" * 78)
        print(f"{'标准':<20}{'类别':<16}{'章节':>4}{'还原':>5}{'数值行':>6}{'术语错':>6}")
        print("-" * 78)
        for d in sorted(DIGEST["entries"], key=lambda x: (x["cat"], x["std_id"])):
            print(f"{d['std_id']:<20}{d['cat'][:14]:<16}{d['sections']:>4}"
                  f"{d['repaired']:>5}{d['numeric_lines']:>6}{d['term_hits']:>6}")
        tot = {k: sum(d[k] for d in DIGEST["entries"])
               for k in ("sections", "repaired", "numeric_lines", "term_hits")}
        print("-" * 78)
        print(f"{'合计':<20}{'':<16}{tot['sections']:>4}{tot['repaired']:>5}"
              f"{tot['numeric_lines']:>6}{tot['term_hits']:>6}")
        print(f"\n还原占比 {tot['repaired'] / max(1, tot['sections']) * 100:.0f}%"
              f"（条款号错位是机翻件的固有缺陷，digest 已按确定规则还原）")
        print("术语纠错表见 `stdq terms`；单份详情 `stdq digest <编号>`")
        return 0

    n = norm(a.query)
    hit = DIGEST_BY.get(n)
    if not hit:
        cand = [d for d in DIGEST["entries"]
                if n and len(n) > 3 and (n in norm(d["std_id"])
                                         or norm(d["std_id"]).startswith(n))]
        hit = cand[0] if cand else None
    if not hit:
        print(f"⚫ 无 digest：{a.query}")
        print("  → 该标准未纳入条款级蒸馏（可能不在库、或为扫描件尚未 OCR）。")
        print("    查 `stdq digest --all` 看已有范围。")
        return 1
    if getattr(a, "json", False):
        print(json.dumps(hit, ensure_ascii=False, indent=1))
        return 0

    print(f"【{hit['std_id']}】 条款级 digest")
    print(f"  类别:     {hit['cat']}")
    print(f"  适用范围: {hit['scope']}")
    print(f"  章节:     {hit['sections']}（其中条款号还原 {hit['repaired']}）")
    print(f"  数值条件行: {hit['numeric_lines']}")
    print(f"  术语错误命中: {hit['term_hits']} 次")
    print(f"  文件:     {hit['digest']}")
    print()
    print("  ⚠ digest 是「让你知道有什么、在哪一节」，不是可引用的原文。")
    print("    术语译名与条款号须回英文原文核对（见 `stdq terms`）。")
    return 0


def cmd_terms(a) -> int:
    """已核实的机翻术语纠错表。"""
    terms = DIGEST.get("terms", [])
    if not terms:
        print("⚠ 术语纠错表不存在")
        return 1
    if getattr(a, "json", False):
        print(json.dumps(terms, ensure_ascii=False, indent=1))
        return 0
    print(f"机翻术语纠错表（{len(terms)} 条，每条均与英文原件对齐核实）")
    print("=" * 78)
    for t in terms:
        print(f"\n  「{t['bad']}」 → 应为 **{t['good']}**　(英文原词: {t['en']})")
        print(f"      证据: {t['evidence']}")
    print()
    print("─" * 78)
    print("用法：读到机翻件里的左词时，心里替换成右词，引用时用英文原词。")
    print("这样 L3 语料就从「不可用」变成「可用但需转译」。")
    return 0


def cmd_mil(a) -> int:
    """军标方法索引查询（来自 OCR 的目录页）。

    ⚠ 这是 L4-OCR 内容：方法号可用于定位，标题可能含 OCR 误差。
    """
    p = DATA_DIR.parent / "references" / "mil-methods.json"
    if not p.exists():
        print("⚠ 军标方法索引不存在（references/mil-methods.json）")
        print("  → 先跑 `python tools/ocr_military.py --std <标准> --pages <范围>`，")
        print("    再跑 `python tools/parse_mil_methods.py`")
        return 1
    with p.open(encoding="utf-8") as f:
        M = json.load(f)
    stds = M.get("standards", {})

    if getattr(a, "json", False):
        print(json.dumps(M, ensure_ascii=False, indent=1))
        return 0

    q = (a.query or "").strip()
    if not q:
        print("军标方法索引（来源：目录页 OCR · L4-OCR）")
        print("=" * 74)
        for std, rows in stds.items():
            ser = {}
            for r in rows:
                ser[r["method"][0]] = ser.get(r["method"][0], 0) + 1
            detail = "  ".join(f"{k}xxx:{v}" for k, v in sorted(ser.items()))
            print(f"  {std:<16} {len(rows):>3} 个方法号   {detail}")
        print()
        print("  查具体方法: stdq mil 1010     （或 stdq mil 温度循环）")
        print("  ⚠ 标题为 OCR 产物，可能有个别字符误差；引用前须核对原扫描页。")
        return 0

    # 方法号精确/前缀查
    nq = re.sub(r"\D", "", q)
    hits = []
    if len(nq) >= 3:
        for std, rows in stds.items():
            for r in rows:
                if r["method"].startswith(nq) or nq == r["method"]:
                    hits.append((std, r))
    # 关键词查
    if not hits and q:
        for std, rows in stds.items():
            for r in rows:
                if q.lower() in (r["title"] or "").lower():
                    hits.append((std, r))

    if not hits:
        print(f"未在军标方法索引中命中: {q}")
        print("  → 可能该页尚未 OCR。查 `stdq mil` 看已覆盖的方法号范围。")
        print("  ⚠ 禁止凭记忆给军标方法号的含义。")
        return 1

    print(f"军标方法命中 {len(hits)} 条（L4-OCR 来源）")
    print("=" * 74)
    seen = set()
    for std, r in hits:
        k = (std, r["method"])
        if k in seen:
            continue
        seen.add(k)
        print(f"  【{std}】Method {r['method']}"
              f"{'  rev ' + r['rev'] if r['rev'] else ''}")
        print(f"      {r['title'] or '（未识别到标题）'}")
    print()
    print("  ⚠ 以上来自 OCR，方法号可用于定位；标题可能含字符误差。")
    print("    引用前须核对原扫描页，或查 `stdq source MIL-STD-883K`。")
    return 0


def cmd_coverage(a) -> int:
    """资料覆盖总账：哪些在库、哪些不在。"""
    entries = CORPUS.get("entries", [])
    if not entries:
        print("⚠ 本地资料库索引不存在")
        return 1
    if getattr(a, "json", False):
        print(json.dumps(CORPUS.get("entries", []), ensure_ascii=False, indent=1))
        return 0

    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e.get("cat") or "未分类", []).append(e)

    print(f"资料覆盖总账（{len(entries)} 个标准编号）")
    print("=" * 74)
    for cat in sorted(by_cat, key=lambda c: (-len(by_cat[c]), c)):
        items = sorted(by_cat[cat], key=lambda x: x["std_id"])
        print(f"\n▍{cat}　({len(items)})")
        for e in items:
            note = ""
            if not e["can_cite_wording"] and e["can_cite_number"]:
                note = "  ⚠机翻：术语不可引"
            elif e["tier"] == "L4":
                note = "  ⚠扫描件：内容不可引"
            print(f"   {TIER_ICON[e['tier']]} {e['std_id']:<20}{note}")
    print()
    print("─" * 74)
    print("🟢 L1 英文原文 → 可直接引用　🟡 L2 官方译本 → 引时注明以英文为准")
    print("🟠 L3 机翻中文 → 只能定位条款号/数值，术语必须回原文")
    print("🔴 L4 扫描件   → 内容一律不可引用，只能声明「已持有」")
    print("⚫ 不在库       → 必须声明无法确认")
    return 0


# ── 入口 ──────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(
        prog="stdq", description="半导体标准编号反查工具 (JEDEC/SEMI/IEC/AEC/AQG/IPC/MIL-STD)")
    ap.add_argument("--data", help="数据目录（默认 ../data）")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("find", help="反查：编号 → 内容")
    p.add_argument("query"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_find)

    p = sub.add_parser("refs", help="该标准引用了谁")
    p.add_argument("query"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_refs)

    p = sub.add_parser("cited-by", help="谁引用了它")
    p.add_argument("query"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_cited_by)

    p = sub.add_parser("classify", help="编号结构解析")
    p.add_argument("query"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_classify)

    p = sub.add_parser("check", help="防错：误传纠正 + 废止拦截")
    p.add_argument("query"); p.set_defaults(f=cmd_check)

    p = sub.add_parser("tree", help="测试方法分类树")
    p.add_argument("query", nargs="?"); p.set_defaults(f=cmd_tree)

    p = sub.add_parser("unverified", help="未核实项清单"); p.set_defaults(f=cmd_unverified)
    p = sub.add_parser("miscon", help="常见误传纠正表"); p.set_defaults(f=cmd_miscon)
    p = sub.add_parser("ql", help="AQG 324 试验条件（QL-01~QL-11）")
    p.add_argument("query", nargs="?", default=""); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_ql)
    p = sub.add_parser("aqg", help="AQG 324 引用构成与统计判据"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_aqg)
    p = sub.add_parser("lifetime", help="AQG 324 寿命公式（Annex II.B）"); p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_ql_lifetime)
    p = sub.add_parser("stats", help="库统计"); p.set_defaults(f=cmd_stats)

    p = sub.add_parser("corpus", help="本地资料库概览（分层统计）")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_corpus)

    p = sub.add_parser("source", help="查某标准的出处与引用规则")
    p.add_argument("query"); p.add_argument("--json", action="store_true")
    p.set_defaults(f=cmd_source)

    p = sub.add_parser("coverage", help="资料覆盖总账（按类别）")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_coverage)

    p = sub.add_parser("digest", help="条款级 digest（章节/数值/术语纠错）")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_digest)

    p = sub.add_parser("terms", help="机翻术语纠错表（已核实）")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_terms)

    p = sub.add_parser("mil", help="军标方法索引查询（OCR 来源）")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--json", action="store_true"); p.set_defaults(f=cmd_mil)

    a = ap.parse_args()
    if not getattr(a, "cmd", None):
        ap.print_help()
        return 0
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
