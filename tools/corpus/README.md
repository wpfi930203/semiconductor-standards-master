# 本地资料库抽取流水线

把源目录里的标准 PDF 蒸馏进本 skill 的 `references/sources/standards/`。

## 五步

```bash
SRC="<本地标准资料库>"   # 源目录（只读）

python inventory_sources.py      # ① 去重 + 文本层探测 → tools/inventory.json
python extract_corpus.py         # ② 抽文本层 → references/sources/standards/
                                 #    + references/sources/corpus_index.json
python extract_metadata.py       # ③ 文档自述元数据（版本/日期以正文为准）
                                 #    → references/sources/corpus_metadata.json
python build_corpus.py           # ④ 资料库索引（含引用分层）→ data/corpus.json
python build_manifest_md.py      # ⑤ 人读覆盖清单 → references/LOCAL-CORPUS.md
```

## 依赖

- Python 3.9+（仅标准库）
- `pymupdf`（`python -m pip install pymupdf`）—— 仅用于读 PDF

## 路径配置

脚本顶部的 `SRC` / `SKILL` 是绝对路径常量。换机器或换目录时改这两行：

| 脚本 | 常量 |
|---|---|
| `inventory_sources.py` | `SRC` |
| `extract_corpus.py` | `SRC`（源）、`SKILL`（目标） |
| `extract_metadata.py` | `D`（= `<skill>/references/sources/standards`） |
| `build_corpus.py` | `SKILL` |
| `build_manifest_md.py` | `SKILL` |

## 三条铁律

1. **源目录只读** —— 绝不移动、重命名、删除源 PDF。全部脚本只做 `open(..., 'rb')` 与 `write` 到 skill 内。
2. **不做 OCR** —— 扫描件如实登记为 L4，内容一律不引用。军标页码多、字形老化，OCR 错误率高于收益。
3. **不信文件名** —— 语种必须实测（CJK 占比）。实测发现多份标注「完整英文电子版」者正文是机翻中文。
   **机翻件不得因「有了文件」而升为 A 级。**

## 已知陷阱

| 陷阱 | 表现 | 处理 |
|---|---|---|
| Win32 MAX_PATH 260 | 路径 ≥240 字符的文件 `stat()` 报 FileNotFoundError，`rglob` 静默漏项 | 用 `\\?\` 前缀 + `os.scandir` 递归（脚本已处理） |
| 文件名词条错位 | 中文名文件是英文原件，英文名文件是机翻件 | 一律以正文自述定级 |
| 表格符号丢失 | PDF 表格抽成竖排文本时会丢掉负号（`-55` → `55`，`0` → `-0`） | 数值须与原文交叉核对 |
| 拆分卷误当独立标准 | `MIL-STD-883F(1-349)` 是全本的分卷 | 归入全本条目的 `parts` 字段 |
| 同名多版本 | `IPC-7351`(2005) 与 `IPC-7351B`(2010) 是两份文件 | 分别建档，`std_id` 带版本后缀 |
| **源目录里嵌着 skill 自身快照** | 实测：源目录下有 `semiconductor-standards-master/semiconductor-standards-master/`，是**本 skill 的 v1.0.0 旧快照**（含 AQG 324 PDF 与 research 文件） | 它是**派生产物不是标准资料**：① 其 `AQG324_*.pdf` 已由 `extract_corpus.py` 识别为 `already_in_skill` 跳过；② 其余 `.md/.json` 因不是 PDF 天然被跳过；③ **绝不要把这份快照当成"新资料"再蒸馏一遍** —— 那是自我循环 |

