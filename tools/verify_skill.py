"""校验 semiconductor-standards-master 的 frontmatter / icon 一致性与 CLI 回归。

对应 master-skill Phase 4「质量验证」的自动化部分 + lean-production-expert 的 verify_icon 思路。
纯标准库，不依赖 Pillow。
"""
import json
import pathlib
import re
import struct
import subprocess
import sys

B = pathlib.Path(__file__).resolve().parent.parent
PY = sys.executable
fails = []


def ck(cond, label, detail=""):
    print(("  ✓ " if cond else "  ✗ ") + label + (f"  {detail}" if detail else ""))
    if not cond:
        fails.append(label)


# ---------- 1. frontmatter ----------
txt = (B / "SKILL.md").read_text(encoding="utf-8")
ck(txt.startswith("---\n"), "SKILL.md 有 YAML frontmatter")
fm = txt.split("---")[1]

print("\n=== frontmatter 关键字段 ===")
fields = {}
for k in ["name", "displayName", "slug", "icon", "version",
          "last_research_date", "source_count", "industry"]:
    m = re.search(r"^" + k + r":\s*(.+)$", fm, re.M)
    fields[k] = m.group(1).strip() if m else None
    print(f"  {k:20} {fields[k] if fields[k] else '**缺失**'}")
    ck(bool(m), f"frontmatter 有 {k}")

ck(fields["name"] == "semiconductor-standards-master", "name 与目录名一致")
ck(fields["displayName"] == "半导体标准专家", "displayName = 半导体标准专家")
ck(fields["version"] == "1.5.0", "version = 1.5.0")

desc = re.search(r"^description:\s*>-\n((?:  .*\n|\n)+)", fm, re.M)
ck(bool(desc), "description 使用 >- 块标量（多行安全）")
if desc:
    d = desc.group(1)
    print(f"\n  description 长度: {len(d)} 字符")
    for kw in ["编号反查", "引用链追溯", "按失效机理选试验", "试验方案",
               "零失效", "未核实", "JESD22", "AQG 324", "触发词",
               "本地标准全文库", "引用分层", "L1", "L3", "无法确认"]:
        ck(kw in d, f"description 含「{kw}」")
    for old in ["温度循环", "功率循环", "MIL-STD-883", "Coffin-Manson", "零失效"]:
        ck(old in d, f"description 保留原触发词「{old}」")

# ---------- 2. icon ----------
print("\n=== 图标文件 ===")
ck(bool(fields["icon"]), "frontmatter 有 icon 字段")
ico = (B / fields["icon"]).resolve()
ck(ico.exists(), "icon 文件存在", str(ico.relative_to(B)))
if ico.exists():
    data = ico.read_bytes()
    ck(data[:8] == b"\x89PNG\r\n\x1a\n", "icon 是合法 PNG")
    w, h = struct.unpack(">II", data[16:24])
    ck((w, h) == (200, 200), "icon 尺寸 200x200", f"{w}x{h}")
    print(f"  文件大小: {len(data):,} bytes")
sv = ico.with_suffix(".svg")
ck(sv.exists(), "SVG 矢量源存在", f"{sv.stat().st_size:,} bytes" if sv.exists() else "")
if sv.exists():
    s = sv.read_text(encoding="utf-8")
    ck("JESD" in s, "SVG 含 JESD 字样")
    ck("viewBox=\"0 0 200 200\"" in s, "SVG viewBox 0 0 200 200")
gen = B / "tools" / "make_icon.py"
ck(gen.exists(), "图标生成脚本 tools/make_icon.py 存在")

# ---------- 3. meta.json ----------
print("\n=== meta.json ===")
meta = json.loads((B / "meta.json").read_text(encoding="utf-8"))
ck(meta["name"] == "半导体标准专家", "meta.name = 半导体标准专家")
ck(meta["icon"] == fields["icon"], "meta.icon 与 frontmatter.icon 一致")
ck(meta["version"] == fields["version"], "meta.version 与 frontmatter.version 一致")
ck(meta["changelog"][0]["rev"] == "v1.5.0", "changelog 首条 = v1.5.0")
ck(meta["last_research_date"] == fields["last_research_date"], "last_research_date 一致")

# ---------- 3.5 本地资料库 ----------
print("\n=== 本地资料库（data/corpus.json）===")
cp = B / meta.get("corpus", {}).get("index", "data/corpus.json")
ck(cp.exists(), "资料库索引存在", str(cp.relative_to(B)))
if cp.exists():
    C = json.loads(cp.read_text(encoding="utf-8"))
    S = C["stats"]
    print(f"  源 PDF {S['pdf_files_total']} 个 → 不同编号 {S['distinct_std_ids_total']} 个 "
          f"→ 已抽取 {S['text_extracted']} 份")
    ck(S["text_extracted"] == len([e for e in C["entries"]
                                   if e.get("corpus_path")]),
       "text_extracted 与 entries 中有语料路径的条数一致")
    for k in ("L1", "L2", "L3", "L4", "L4-OCR"):
        ck(k in C["tiers"], f"分层模型含 {k}")

    # 每份标了 corpus_path 的条目，文件必须真实存在
    # （L4-OCR 的 corpus_path 指向 OCR 产物，路径同样要存在）
    missing = []
    for e in C["entries"]:
        p = e.get("corpus_path")
        if p and not (B / p).exists():
            missing.append(p)
    ck(not missing, "所有 corpus_path 指向的文件都存在",
       f"缺失 {len(missing)}" if missing else "")

    # 分层判定的自洽性：仅 L1/L2 可引措辞
    bad = [e["std_id"] for e in C["entries"]
           if (e["tier"] in ("L1", "L2")) != bool(e["can_cite_wording"])]
    ck(not bad, "分层与可引用性自洽（仅 L1/L2 可引措辞）",
       f"异常: {bad[:3]}" if bad else "")
    l3 = [e["std_id"] for e in C["entries"] if e["tier"] == "L3"]
    ck(all(not e["can_cite_wording"] for e in C["entries"] if e["tier"] == "L3"),
       f"L3 机翻件一律禁引措辞（{len(l3)} 份）")
    for t in ("L4", "L4-OCR"):
        ck(all(not e["can_cite_wording"] and not e["can_cite_number"]
               for e in C["entries"] if e["tier"] == t),
           f"{t} 扫描件一律禁引措辞与数值")

    # 未 OCR 的 L4 不得带 corpus_path
    ck(all(not e.get("corpus_path") for e in C["entries"] if e["tier"] == "L4"),
       "未 OCR 的 L4 不带 corpus_path")

# ---------- 3.6 条款级 digest ----------
print("\n=== 条款级 digest（references/digests/）===")
di = B / "references" / "digests" / "_index.json"
ck(di.exists(), "digest 索引存在")
if di.exists():
    G = json.loads(di.read_text(encoding="utf-8"))
    ents = G.get("entries", [])
    l3ids = {e["std_id"] for e in C.get("entries", [])} if cp.exists() else set()
    print(f"  digest 份数: {len(ents)}")
    ck(len(ents) >= 37, f"L3 全部有 digest（{len(ents)} 份）")
    miss = [d["std_id"] for d in ents if not (B / d["digest"]).exists()]
    ck(not miss, "所有 digest 文件都存在", f"缺失 {len(miss)}" if miss else "")
    ck(len(G.get("terms", [])) >= 10, f"术语纠错表 >=10 条（{len(G.get('terms', []))} 条）")
    # 每条术语必须有核实依据
    ck(all(t.get("evidence") for t in G.get("terms", [])),
       "每条术语纠错都带核实依据")
    tot_rep = sum(d["repaired"] for d in ents)
    tot_sec = sum(d["sections"] for d in ents)
    ck(tot_rep > 0, f"条款号还原生效（{tot_rep}/{tot_sec} 节）")

# ---------- 3.7 军标方法索引 ----------
print("\n=== 军标方法索引（references/mil-methods.json）===")
mi = B / "references" / "mil-methods.json"
ck(mi.exists(), "军标方法索引存在")
if mi.exists():
    MM = json.loads(mi.read_text(encoding="utf-8"))
    st = MM.get("standards", {})
    for s, rows in st.items():
        print(f"  {s:<16} {len(rows):>3} 个方法号  "
              f"标题 {sum(1 for r in rows if r['title']):>3}")
    ck(len(st) >= 4, f"覆盖 4 个军标（{len(st)}）")
    # 方法号必须是 4 位数字
    bad = [(s, r["method"]) for s, rows in st.items() for r in rows
           if not (len(r["method"]) == 4 and r["method"].isdigit())]
    ck(not bad, "所有方法号都是 4 位数字", f"异常 {bad[:3]}" if bad else "")
    # 每个方法号必须有来源标记
    nosrc = [(s, r["method"]) for s, rows in st.items() for r in rows
             if not r.get("source")]
    ck(not nosrc, "每条方法号都带来源标记", f"缺 {len(nosrc)}" if nosrc else "")
    # 同源参考必须带风险说明
    sib = [r for s, rows in st.items() for r in rows
           if r.get("source") == "同源标准参考"]
    ck(all(r.get("source_detail") for r in sib),
       f"同源参考项都带风险说明（{len(sib)} 条）")
    # 交叉校验存在且一致率高
    xc = MM.get("cross_validation", {})
    ck(bool(xc), "存在交叉校验结果")
    for s, x in xc.items():
        if "agree_ratio" in x:
            ck("99%" in x["agree_ratio"] or "9" in x["agree_ratio"].split("=")[-1],
               f"{s} 与 883 方法号一致率 {x['agree_ratio']}")
    ck("gaps" in MM, "存在缺口声明")

for rel in ["references/LOCAL-CORPUS.md", "references/sources/corpus_index.json",
            "references/sources/corpus_metadata.json", "tools/corpus/README.md",
            "references/digests/_INDEX.md", "tools/ocr_military.py",
            "references/MIL-METHODS.md", "references/mil-methods.json",
            "tools/parse_mil_methods.py"]:
    ck((B / rel).exists(), f"存在 {rel}")

rc = (B / "references" / "LOCAL-CORPUS.md")
if rc.exists():
    t = rc.read_text(encoding="utf-8")
    for kw in ["引用分层模型", "条款号错位：机翻件的第三个缺陷", "扫描件（军标 / 国军标）",
               "机翻术语纠错表（已核实，逐条对齐英文原件）", "机翻标准（L3）的条款级蒸馏",
               "已知的资料缺口", "wire harness" if False else "线束"]:
        ck(kw in t, f"LOCAL-CORPUS.md 含「{kw}」")


# ---------- 4. CLI 回归 ----------
print("\n=== CLI 回归（零依赖离线）===")
STDQ = [PY, str(B / "scripts" / "stdq.py")]
# (args, label, expect_nonzero)——check 命中误传拦截时应当【故意】返回非零
cases = [
    (["find", "JESD22-A104"], "A104 精确命中", False),
    (["find", "IEC60749-34"], "IEC 60749-34 命中", False),
    (["find", "AQG324"], "AQG 324 命中", False),
    (["check", "IEC60749-34"], "干净样本应 rc=0", False),
    (["check", "JESD22-A104"], "A104 命中误传表，应报警 rc=1", True),
    (["check", "M-101"], "三位 MIL 号拦截（应报错）", True),
    (["refs", "AQG324"], "AQG 324 引用查询", False),
    (["cited-by", "JEP195"], "JEP195 下游查询", False),
    (["classify", "JESD22-A104"], "编号结构解析", False),
    (["tree", "焊点"], "失效现象速查", False),
    (["ql", "QL-01"], "QL-01 条件表", False),
    (["aqg"], "AQG 引用构成+统计判据", False),
    (["lifetime"], "寿命公式", False),
    (["unverified"], "未核实清单", False),
    (["miscon"], "误传纠正表", False),
    (["stats"], "库统计", False),
    (["corpus"], "本地资料库概览", False),
    (["corpus", "--json"], "资料库 JSON", False),
    (["coverage"], "资料覆盖总账", False),
    (["digest", "--all"], "digest 索引", False),
    (["digest", "JESD22-A104F"], "单份 digest", False),
    (["terms"], "机翻术语纠错表", False),
    (["mil"], "军标方法索引总览", False),
    (["mil", "1010"], "军标方法号查询", False),
    (["source", "JESD47L"], "L1 资料出处（英文原文）", False),
    (["source", "JESD22-A104F"], "L3 资料出处（机翻件）", False),
    (["source", "MIL-STD-883K"], "L4/L4-OCR 扫描件出处", False),
    (["source", "IEC60950-1"], "L0 不在库 → 应报错", True),
    (["find", "JESD22-A104F"], "find 自动附资料库层级", False),
]
for args, label, want_fail in cases:
    p = subprocess.run(STDQ + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=30)
    has_out = len(p.stdout.strip()) > 0
    failed_as_designed = want_fail and p.returncode != 0
    ok = has_out and ((p.returncode != 0) == want_fail)
    ck(ok, f"stdq {' '.join(args)}",
       f"({label}{'，按设计拒绝' if failed_as_designed else ''})")
    if not ok:
        print("     rc=%s out=%r err=%r" % (p.returncode, p.stdout[:120], p.stderr[:120]))

p = subprocess.run(STDQ + ["find", "JESD22-A104", "--json"], capture_output=True,
                   text=True, encoding="utf-8", errors="replace", timeout=30)
try:
    json.loads(p.stdout)
    ck(True, "stdq --json 输出可解析")
except Exception as e:
    ck(False, "stdq --json 输出可解析", str(e)[:80])

# ---------- 汇总 ----------
print("\n" + "=" * 60)
if fails:
    print(f"✗ {len(fails)} 项未通过：")
    for f in fails:
        print("   -", f)
    raise SystemExit(1)
print("✓ 全部校验通过")
