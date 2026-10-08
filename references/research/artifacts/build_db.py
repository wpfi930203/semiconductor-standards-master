#!/usr/bin/env python3
"""从 YAML/JSON 源构建 SQLite 查表库。零第三方依赖（仅标准库）。"""
import json, re, sqlite3, sys, unicodedata
from pathlib import Path

# ---- 编号归一化：这是整个 CLI 的核心 ----
RULES = [
    (r"[\u2010-\u2015\u2212]", "-"),   # 各种 dash → ASCII hyphen
    (r"\s+",""),                      # 去所有空白（含全角空格 U+3000 由 \s 覆盖）
    (r"\.0(?=[A-Z]|$)","") if False else (r"(?<=[A-Z])\.0(?![0-9])",""),  # A104.0 → A104
]
ORG_PREFIX = {  # 别名前缀 → 规范前缀
    "jedec":"JESD","jesd":"JESD","jesd22":"JESD22","jes22":"JESD22",
    "jedec22":"JESD22","jep":"JEP","std":"JESD","mil":"MIL-STD","milstd":"MIL-STD",
}
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", str(s)).upper()
    for pat, rep in RULES: s = re.sub(pat, rep, s)
    s = s.replace("_","-").replace(" ","")
    return s
def canon(s: str) -> str:
    """归一化 + 别名前缀展开：jedec22-a104 -> JESD22A104"""
    n = norm(s)
    m = re.match(r"^([A-Z]+)(\d+)(.*)$", n)
    if m:
        head, num, rest = m.groups()
        long = ORG_PREFIX.get(head.lower())
        if long: head = long
        return f"{head}{num}{rest}"
    long = ORG_PREFIX.get(n.lower())
    return long or n

def build(src: Path, db: Path):
    data = json.loads(src.read_text(encoding="utf-8"))
    std = {s["id"]: s for s in data["standards"]}
    con = sqlite3.connect(db); cur = con.cursor()
    cur.executescript("""
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS std(
      id TEXT PRIMARY KEY, org TEXT, title_en TEXT, title_zh TEXT,
      status TEXT, edition TEXT, pub_date TEXT, stability_date TEXT,
      supersedes TEXT, superseded_by TEXT, source_url TEXT, local_pdf TEXT, note TEXT);
    CREATE TABLE IF NOT EXISTS alias(alias TEXT PRIMARY KEY, std_id TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS ref(
      src TEXT NOT NULL, dst TEXT NOT NULL, kind TEXT NOT NULL DEFAULT 'normative',
      clause TEXT, note TEXT, PRIMARY KEY(src,dst,kind,clause));
    CREATE TABLE IF NOT EXISTS clause(
      std_id TEXT, no TEXT, title TEXT, kind TEXT, text TEXT,
      UNIQUE(std_id,no));
    CREATE INDEX IF NOT EXISTS ix_ref_dst ON ref(dst);
    CREATE INDEX IF NOT EXISTS ix_ref_src ON ref(src);
    CREATE INDEX IF NOT EXISTS ix_alias ON alias(alias);
    """)
    for s in data["standards"]:
        cur.execute("INSERT OR REPLACE INTO std VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (canon(s["id"]), s.get("org",""), s.get("title_en",""), s.get("title_zh",""),
             s.get("status",""), s.get("edition",""), s.get("pub_date",""),
             s.get("stability_date",""), canon(s["supersedes"]) if s.get("supersedes") else None,
             canon(s["superserseded_by"]) if s.get("superseded_by") else None,
             s.get("source_url",""), s.get("local_pdf",""), s.get("note","")))
        for a in s.get("aliases",[]):
            cur.execute("INSERT OR REPLACE INTO alias VALUES(?,?)",(canon(a),canon(s["id"])))
    for e in data.get("references",[]):
        cur.execute("INSERT OR REPLACE INTO ref VALUES(?,?,?,?,?)",
            (canon(e["src"]),canon(e["dst"]),e.get("kind","normative"),e.get("clause",""),e.get("note","")))
    for c in data.get("clauses",[]):
        cur.execute("INSERT OR REPLACE INTO clause VALUES(?,?,?,?,?)",
            (canon(c["std_id"]),c["no"],c.get("title",""),c.get("kind",""),c.get("text","")))
    con.commit()
    n=lambda t:cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"[built] {db}  std={n('std')} alias={n('alias')} ref={n('ref')} clause={n('clause')}")
if __name__=="__main__":
    build(Path(sys.argv[1]), Path(sys.argv[2]))
