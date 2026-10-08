#!/usr/bin/env python3
"""std — 半导体标准查表CLI。零第三方依赖（argparse + sqlite3 + re）。
用法: std.py <query> | refs|refd|clause|chain|search|stats|export"""
import argparse, json, re, sqlite3, sys, unicodedata
from pathlib import Path

DEFAULT_DB = Path(__file__).with_name("std.db")
RULES = [(r"[\u2010-\u2015\u2212]","-"), (r"\s+",""), (r"(?<=[A-Z])\.0(?![0-9])","")]
ORG_PREFIX = {"jedec":"JESD","jesd":"JESD","jesd22":"JESD22","jes22":"JESD22",
              "jedec22":"JESD22","jep":"JEP","std":"JESD","mil":"MIL-STD","milstd":"MIL-STD"}
def canon(s):
    n = unicodedata.normalize("NFKC", str(s)).upper()
    for p,r in RULES: n = re.sub(p,r,n)
    n = n.replace("_","-").replace(" ","")
    n = re.sub(r"[-.]+$","",n)          # 去掉尾部悬空连字符/点： "JESD22-A104." -> "JESD22-A104"
    m = re.match(r"^([A-Z]+)(\d+)(.*)$", n)
    if m:
        h,num,rest = m.groups()
        return f"{ORG_PREFIX.get(h.lower(),h)}{num}{rest}"
    return ORG_PREFIX.get(n.lower(), n)

def conn(p): 
    c = sqlite3.connect(f"file:{p}?mode=ro", uri=True); c.row_factory = sqlite3.Row; return c

def _variants(k):
    """由归一化键生成 progressively looser 的匹配键。"""
    yield k
    yield re.sub(r"[^A-Z0-9]","",k)                       # 去分隔符
    m=re.match(r"^([A-Z]+)(\d+)-?([A-Z]*)$",k)              # 去尾部版本字母 JESD22-A104F -> JESD22A104
    if m: yield f"{m.group(1)}{m.group(2)}"
    m=re.match(r"^([A-Z]*)(\d+)(-[\d.]*[A-Z]?)?$",k)       # 纯数字核心60749-34-1 -> 60749-34
    if m and m.group(3):
        base=f"{m.group(1)}{m.group(2)}"
        yield base + re.sub(r"\.[0-9]+$","",m.group(3))
    m=re.match(r"^([A-Z]+)(\d+)-(\d+)(-\d+)?$",k)         # IEC 60749-34-1 -> 60749-34
    if m: yield f"{m.group(2)}-{m.group(3)}"

def resolve(c, q):
    """五级解析：路径尾段→ 精确 → 逐级宽松 → 版本无关 → 纯数字核心。返回 (row, how)"""
    raw = str(q).strip().split("/")[-1]          # 容忍 "jedec/jesd22/jesd22-a104f" 这类路径
    keys = list(_variants(canon(raw)))
    seen=set()
    for i,k in enumerate(keys):
        if k in seen: continue
        seen.add(k)
        how = ["exact","alias","tight","ver-free","ver-free","num-core"][min(i,5)]
        if r:=c.execute("SELECT * FROM std WHERE id=?",(k,)).fetchone(): return r,how
        if r:=c.execute("SELECT s.* FROM alias a JOIN std s ON s.id=a.std_id WHERE a.alias=?",(k,)).fetchone():
            return r,how+"/alias"
    # 终态兜底：去分隔符全等
    qt=re.sub(r"[^A-Z0-9]","",k)
    for r in c.execute("SELECT * FROM std"):
        if re.sub(r"[^A-Z0-9]","",r["id"])==qt: return r,"tight/scan"
    # 版本无关：忽略末尾修订字母/版次（JESD22-A104F -> JESD22A104）
    hits=[r for r in c.execute("SELECT * FROM std")
          if re.sub(r"[^A-Z0-9]","",r["id"]).startswith(qt)
          and re.fullmatch(r"[A-Z]?\d*[A-Z]?(\d+)?", re.sub(r"[^A-Z0-9]","",r["id"])[len(qt):] or "x")
          and len(re.sub(r"[^A-Z0-9]","",r["id"]))>len(qt)]
    if len(hits)==1: return hits[0],"ver-free/scan"
    if len(hits)>1: return hits,"AMBIGUOUS"   # 系列号歧义：JESD22 / JESD51 ...
    return None,None

def out(r, how=None):
    if not r: return
    print(f"■ {r['id']}  [{r['org']}]" + (f"  (匹配方式:{how})" if how else ""))
    if r["title_en"]: print(f"  英文标题: {r['title_en']}")
    if r["title_zh"]: print(f"  中文标题: {r['title_zh']}")
    meta=[]
    for lbl,k in (("状态","status"),("版本","edition"),("发布","pub_date"),("稳定期至","stability_date")):
        if r[k]: meta.append(f"{lbl}={r[k]}")
    if meta: print("  " + " | ".join(meta))
    for lbl,k in (("被…替代","superseded_by"),("替代了","supersedes")):
        if r[k]: print(f"  {lbl}: {r[k]}")
    for lbl,k in (("来源","source_url"),("本地PDF","local_pdf"),("备注","note")):
        if r[k]: print(f"  {lbl}: {r[k]}")

def main():
    ap = argparse.ArgumentParser(prog="std", description="半导体标准查表CLI（离线）")
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("cmd", choices=["get","refs","refd","clause","chain","search","stats","export"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("-n","--kind", default="", help="引用类型过滤 normative|informative")
    ap.add_argument("-d","--depth", type=int, default=2)
    a = ap.parse_args()
    c = conn(a.db)
    if a.cmd == "stats":
        for t in ("std","alias","ref","clause"):
            print(f"{t:8s} {c.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")
        print("\n-- 按机构 --")
        for r in c.execute("SELECT org,COUNT(*) n FROM std GROUP BY org ORDER BY n DESC"):
            print(f"  {r['org'] or '(空)':10s} {r['n']}")
        return
    if a.cmd == "search":
        rows = c.execute("SELECT * FROM std WHERE id LIKE ? OR title_en LIKE ? OR title_zh LIKE ?",
                         (f"%{canon(a.arg)}%",f"%{a.arg}%",f"%{a.arg}%")).fetchall()
        if a.json: print(json.dumps([dict(r) for r in rows],ensure_ascii=False,indent=2)); return
        for r in rows: out(r); print()
        print(f"[共 {len(rows)} 条]") if rows else print("无匹配")
        return
    if a.cmd == "export":
        tbl = a.arg or "std"
        rows = c.execute(f"SELECT * FROM {tbl}").fetchall()
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2)); return
    r, how = resolve(c, a.arg)
    if isinstance(r, list):   # 系列号歧义：列出候选而非猜一个
        print(f"⚠ {a.arg} 归一化为 {canon(a.arg)}，命中 {len(r)} 条候选（这是系列号，请给全编号）:")
        for x in r: print(f"   - {x['id']:20s} {x['title_en'][:56]}")
        sys.exit(2)
    if not r:
        print(f"✗ 未找到: {a.arg}  (归一化后 {canon(a.arg)})", file=sys.stderr); sys.exit(1)
    if a.cmd == "get": out(r, how); return
    if a.cmd == "clause":
        rows = c.execute("SELECT * FROM clause WHERE std_id=? ORDER BY no",(r["id"],)).fetchall()
        if a.json: print(json.dumps([dict(x) for x in rows],ensure_ascii=False,indent=2)); return
        for x in rows:
            print(f"  §{x['no']}  [{x['kind']}] {x['title']}" + (f"  — {x['text']}" if x["text"] else ""))
        return
    sql = ("SELECT * FROM ref WHERE src=? " + ("AND kind=? " if a.kind else "") + "ORDER BY dst") if a.cmd=="refs" \
        else ("SELECT * FROM ref WHERE dst=? " + ("AND kind=? " if a.kind else "") + "ORDER BY src")
    if a.kind: rows = c.execute(sql,(r["id"],a.kind)).fetchall()
    else:     rows = c.execute(sql,(r["id"],)).fetchall()
    other = "dst" if a.cmd=="refs" else "src"
    if a.json: print(json.dumps([dict(x) for x in rows],ensure_ascii=False,indent=2)); return
    lbl = {"refs":"引用了","refd":"被引用","chain":"引用了"}[a.cmd]
    print(f"■ {r['id']} {lbl} — {len(rows)} 条")
    for x in rows:
        tgt = c.execute("SELECT id,title_en,status FROM std WHERE id=?",(x[other],)).fetchone()
        arrow = "→" if a.cmd=="refs" else "←"
        print(f"  {arrow} [{x['kind']}] {x[other]:16s} {tgt['title_en'][:52] if tgt else '(未建档)'}")
        print(f"       条款 {x['clause'] or '-'}" + (f"  备注: {x['note']}" if x["note"] else ""))
    if a.cmd == "chain":
        print(f"\n  [传递引用 BFS 深度≤{a.depth}]")
        seen={r["id"]}; frontier={r["id"]}
        for lvl in range(1,a.depth+1):
            nxt=set()
            for f in frontier:
                for x in c.execute("SELECT dst FROM ref WHERE src=?",(f,)):
                    if x["dst"] not in seen:
                        seen.add(x["dst"]); nxt.add(x["dst"])
                        t=c.execute("SELECT title_en FROM std WHERE id=?",(x["dst"],)).fetchone()
                        print(f"  L{lvl} → {x['dst']}  {t['title_en'][:50] if t else '(未建档)'}")
            frontier=nxt
            if not frontier: break
if __name__ == "__main__": main()
