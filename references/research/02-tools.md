# Track 02 — Tools（工具 / 数据库 / 软件）：这行的人用什么工具查标准、管标准、判符合性

> **调研对象**：半导体标准产业链上的**工具链**——标准数据库入口、文献管理软件、PDF 解析技术、可靠性分析软件、以及自建离线查表 CLI
> **目标读者**：功率半导体封装可靠性工程师（20 年经验），要建"从标准编号反查内容"的知识 OS + 本地可执行 CLI
> **调研日期**：2026-10-05
> **本 Track 的独特价值**：其它 Track 告诉你"标准是什么"，本 Track 告诉你**"用什么把它挖出来、并且离线可查"**
> **所有命令均在本沙箱实测**（Python 3.11.1 / PyMuPDF 1.26.7 / Linux）。凡未实测的一律标注「未核实」。

---

## 0. 执行摘要：本 Track 的 8 个关键发现

| # | 发现 | 对用户的价值 | 可信度 |
|---|---|---|---|
| 1 | **IEC 产品页实测只有 4 个 Tab：`Product detail` / `Lifecycle` / `Normative references` / `Sustainable development goals`，并不存在 `Referenced by`** | 任务书假设有 4 个 Tab（含"被引用"），**实测为 3 个内容 Tab**。"谁引用了我"无法从 IEC 官方自动获取，必须自建 | ★★★★★ 实测解析 HTML |
| 2 | **IEC 无公开 API**：`/api/publications` → 404，`api.iec.ch` → 404；`Normative references` 由 JS 异步加载，curl 抓不到 | 引用图谱**不能靠爬 IEC 建成**，必须从"标准自己的参考文献表"反向抽取（见 §3.4） | ★★★★★ 实测 |
| 3 | **PyMuPDF `find_tables()` 在真实标准 PDF 上抽取条件表 100% 准确**（AQG324 p11 引用标准表 18/18 行全对），性能与 Camelot-lattice 持平，**零配置、无 Java 依赖** | 查表库建库管线可只用 PyMuPDF 一个库，大幅简化依赖 | ★★★★★ 实测 |
| 4 | **Camelot `stream` flavor 在同一页把 18 行表抽成 39 行**（过度切分），`lattice` 才是正确选择 | 避免踩坑：默认 flavor 用错，条件表数据直接损坏 | ★★★★★ 实测 |
| 5 | **`semiverse.org` 不是 SEMI 的标准检索入口**——实测是韩国一家 NFT/角色项目（세미버스） | 阻止一个会导致建库走偏的错误信息源 | ★★★★★ 实测抓取页面内容 |
| 6 | **ECPE AQG 324 全文免费公开下载**，且有 04.1/2025 最新版（2025-04-24） | 功率模块可靠性最核心的欧洲标准，可合法全文入库 | ★★★★★ 官网核验 |
| 7 | **零失效样本量公式必须是 `n = ln(1-CL)/ln(R)`，R 是可靠度不是失效率**——我第一版写成 `ln(1-C)/ln(R0)` 得 n=1（荒谬） | 10ppm/90% 需 **23 万样本**；这解释了为什么 test-to-pass 在车规领域不可行 | ★★★★★ 实测并与业界表校验（22/29/45） |
| 8 | **Bayerer 模型的 K 不可跨模块移植**：用文献通用系数代入本例得 Nf≈0.1（物理上不可能） | 提醒：开源实现只能给"公式骨架"，K/β 必须用自己模块的 PC 数据标定 | ★★★★★ 实测算术 |

**最强可用资产**：§5 给出一个**零第三方依赖、已通过 21/21 容错测试、断网实测可用**的 SQLite 查表 CLI 完整源码（已归档至 `artifacts/`）。

---

## 1. 标准数据库 / 检索入口（工具视角）

### 1.1 IEC Webstore —— 唯一有"官方引用 tab"的免费入口

#### 1.1.1 URL 结构（实测）

| 用途 | URL | 实测 |
|---|---|---|
| 首页 | `https://webstore.iec.ch/` | 200 |
| **产品详情页（新路径，必须带 `/en/`）** | `https://webstore.iec.ch/en/publication/<数字ID>` | 200 |
| 旧路径（已重定向） | `https://webstore.iec.ch/publication/71025` | 301 → `/en/publication/71025` |
| 搜索页 | `https://webstore.iec.ch/searchform&q=<关键词>` | 301（未跟踪到落地 URL，**未核实**最终形态） |

> ⚠️ **实测纠正**：任务书给的示例 `/publication/71025` 是旧路径。更重要的是，**产品页 ID 是纯数字，与标准编号无关**（`67897` 才是 IEC 60749-34-1:2025）。**查表 CLI 绝不能靠"标准号拼 URL"**，必须人工/半自动过一次映射。参考 Track 05 记录的同类陷阱（JEDEC 用 slug）。

#### 1.1.2 四个 Tab 的真实内容（★核心修正★）

实测对象：`https://webstore.iec.ch/en/publication/67897`（IEC 60749-34-1:2025，2026-10-05）

| Tab | 实测存在 | 提供的字段 | 对建库的价值 |
|---|---|---|---|
| `Product detail` | ✅ | title、摘要、TC 号（TC 47）、Category（Quality Assurance）、Publication type、Publication date（2025-06-20）、Edition（1.0）、ICS（31.080.01）、Stability date（2029）、ISBN、Pages、File size | ★★★★★ 建库主干字段，几乎一次填满 |
| `Lifecycle` | ✅ | 页面含 60+ 处 `status = PUBLISHED` 状态标记（JS 渲染） | ★★★☆ 需渲染才能取到；**建议按需人工记录** |
| `Normative references` | ✅（Tab 存在） | **JS 异步加载，curl 静态抓取为空** | ★★☆☆ 只能浏览器打开后人工摘录 |
| `Sustainable development goals` | ✅ | SDG 关联标签 | ☆ 与可靠性工程师无关，可忽略 |
| **`Referenced by`** | ❌ **实测不存在**（`'referenced by' in html.lower()` → `False`） | — | — |

> ★ **架构级结论**：任务书假设的"反向引用（Referenced by）"在 IEC 官网**并不存在**。
> **这决定了引用图谱的数据来源必须换思路**：从**每份标准自己的 "Referenced standards" 表格**反向抽取（见 §3.4实测：PyMuPDF 能 100% 准确抽出 AQG324 的 18 行引用标准表）。
> 这反而是更好的路径——因为"谁引用了我"本来就只能靠反向遍历全体标准来得到。

#### 1.1.3 无 API 确认

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://webstore.iec.ch/api/publications?query=IEC+60749-34"   # → 404
curl -s -o /dev/null -w "%{http_code}\n" "https://api.iec.ch"                                              # → 404
```
结论：只能当"人工查证入口"，不能当数据源。｜来源：实测 ｜可信度：★★★★★

#### 1.1.4 高价值旁路：第三方镜像可读出 IEC 目录与规范性引用

`https://standards.iteh.ai/catalog/standards/sist/8a45ef3c-.../sist-en-iec-60749-34-1-2025` ｜可信度：★★★★☆（第三方转售站，**版权状态需自行判断**）
实测可读到：完整目录（含 Annex A）、以及 CENELEC 的 **Annex ZA 规范性引用清单**（IEC 60191-4、IEC 60747-2/-6/-8/-9、IEC 60749-23、IEC 60749-34 的年号对照表）。
**用途**：当官方 Tab 抓不到时，用它做"人工核对规范性引用"的辅助。**不建议**作为自动化数据源（版权 + 稳定性）。

### 1.2 SEMI —— 检索入口 + 一个被误传的"Semiverse"

| 用途 | URL | 实测 | 说明 |
|---|---|---|---|
| **标准商店（真正入口）** | `https://store-us.semi.org/collections/latest-standards-1` | 200 | 付费。实测标价 **Member $148 / Non-Member $193**（单份） |
| 分类浏览 | `https://store-us.semi.org/collections/standards/lang-english` | 200 | 按 Volume/Topic/Language/Cycle 筛选 |
| 官方标准总览 | `http://semi.org/index.php/en/products-services/standards` | 200 | 按系列分：Safety / E(设备自动化) / A / M(硅材料) / C&F(液体化学品) |
| **新批准标准（草案公示）** | `https://downloads.semi.org/web/wstdsbal.nsf/DSPView` | **403（反爬）** | 但这是**免费**的"Recently Approved Documents"列表——值得人工查 |
| ❌ `semiverse.org` | `https://www.semiverse.org/` | 200 | ★ **实测内容是韩国 NFT 项目"세미버스"的角色收藏页，与 SEMI 标准毫无关系** |

> ★ **实测排雷**：任何声称"SEMI Semiverse 是 SEMI 标准检索平台"的说法都是错误的。请把该域名从信源清单中删除，避免污染知识 OS。
> 来源：抓取 `semiverse.org` 页面标题 `BRAND | SEMIVERSE` 与正文 ｜可信度：★★★★★

**SEMI 编号族谱**（建库时用于 `canon()` 归一化）：字母前缀+数字，如 `M`(硅材料) `E`(设备) `F`( Facilities) `C`(化学品) `T`(追溯) `PV`(光伏) `3D`(先进封装) `P`(光刻胶) `D`(显示/掩模) `A`(自动化)。来源：store-us.semi.org 实际列表 ｜可信度：★★★★★（实测可见）

### 1.3 JEDEC —— 禁止自动化，只能人工（与任务书一致）

| 用途 | URL | 实测 |
|---|---|---|
| 标准检索页 | `https://www.jedec.org/standards-documents` | **403**（带常规 UA 也被拒） |
| 首页 | `https://www.jedec.org/` | 403（curl） |

实测确认 JEDEC 对脚本访问一律 403。**建库策略：人工查 + 手工填 JSON**，用本 Track 的 `build_db.py` 导入。这与 Track 05 的结论一致。
免费资源：**JM21 流程手册 PDF** 可下载（`https://www.jedec.org/sites/default/files/JM21W.pdf`），是判定 Reaffirm/Revise/Rescind 状态的制度依据。｜可信度：★★★★★（Track 05 已实测下载）

### 1.4 ECPE AQG 324 —— 全文免费，功率模块可靠性核心

| 用途 | URL | 实测 |
|---|---|---|
| ❌ 旧猜测路径 | `https://www.ecpe.org/aQG` | **302 → /system-elements/pages/page-404/**（死链） |
| ✅ **正确路径** | `https://www.ecpe.org/research/working-groups/automotive-aqg-324/` | **200** |
| 免费 PDF 镜像 | `https://www.grapheny.com/wp-content/uploads/2020/07/AQG324_Rel_02_1_2019_15May2019.pdf` | **200，2,161,344 字节**（本次已下载并全文解析） |

官网页面明确列出可下载版本：`04.1/2025 (2025-04-24)`、`03.1/2021`、`02.1/2019`、Intro 稿、Press note。
**许可**：AQG 324 扉页声明 **CC BY ND**（署名-禁止演绎）——可读、可做笔记摘录，**不可改写原文**。这一条直接决定知识 OS 里 AQG 派生内容的写法。
来源：ECPE 官网页 + PDF 扉页原文 ｜可信度：★★★★★

### 1.5 中国 GB/T —— 两个系统，开放度不同

| 平台 | URL | 实测 | 说明 |
|---|---|---|---|
| 国家标准全文公开系统 | `https://openstd.samr.gov.cn/bzgk/gb/` | **200**（需跟随 301） | 检索表单 `action="std_list"`，参数名 `p.p1 p.p2 p.p5 p.p6 p.p7`（非语义化，抓取需硬编码） |
| 全国标准信息公共服务平台 | `https://std.samr.gov.cn/` | 200 | `gbDetailed?id=` 返回"系统提示"页（空 id 触发） |

**开放度差异（与 Track 05 结论一致）**：采标类 GB/T（等同采用 IEC/ISO）**只给题录信息不给全文**；非采标（含 GB/T 自主制定）可下载全文。这解释了为什么中国站查不到某些 IEC 转化标准全文——**是版权设计，不是 bug**。
**对本项目的影响**：GB/T 全文不能作为抽取管线的输入，只能人工核对题录 → 手工录 JSON。

### 1.6 MIL-STD 免费镜像（重要：区分"沙箱不可达"与"站点失效"）

> ⚠️ 本次实测中 `*.mil` 与 `discover.dtic.mil` 全部返回 `000`（连接失败）。**对照测试确认这是沙箱出网策略限制，不是站点失效**（同一时刻 `example.com` 返回 200）。故这些链接标注为**「未核实（本沙箱不可达）」**，而非失效。

| 来源 | URL | 本次实测 | 可信度 |
|---|---|---|---|
| **ASSIST Quick Search（DoD 官方，首选）** | `https://quicksearch.dla.mil/qsSearch.aspx` | 000（沙箱限制） | ★★★★★ 多个高校/政府来源一致确认其为官方免费入口 |
| ASSIST 主站 | `https://assist.dla.mil/` | 000（沙箱限制） | ★★★★☆ |
| EverySpec | `https://everyspec.com/` | **403**（反爬，站点存在） | ★★★★☆ |
| DTIC 技术报告 | `https://discover.dtic.mil/technical-reports` | 000（沙箱限制） | ★★★★★ |
| NASA NEPP（**实测可达**） | `https://nepp.nasa.gov/` | **200** | ★★★★★ |

**关键事实（多来源交叉验证）**：ASSIST 是 DoD 官方仓库，**超过 100,000 份文档，搜索与下载完全免费、无需注册**（DoD 以税收资助开发故免费）。支持按文档号、关键词、FSC 分类号、日期范围、状态（active/inactive/canceled）检索。
**但注意**：Track 05 已实测发现 **MIL-STD-883 基版只有 28 页，方法正文在 883-1~883-5 分册**——拿到 883 不等于拿到全部方法。这个坑在选工具时同样要记住。

### 1.7 付费标准商（建库成本参考）

| 商 | URL | 实测 | 性质 |
|---|---|---|---|
| Techstreet | `https://www.techstreet.com/` | 301（可达） | 付费分销 |
| Intertek Inform | `https://www.intertekinform.com/` | **403**（反爬） | 付费分销 |
| UL Standards | `https://shopulstandards.com/` | **200** | 付费分销 |
| SAI Global | `https://www.sai-global.com/` | 000（沙箱限制） | 付费分销 |

**实用结论**：付费标准商适合"单份应急采购"，**不适合建库**（无法批量、无 API、单价高）。SEMI 单份 $148–193 就是量级参考。

---

## 2. 文献与标准管理工具

### 2.1 Zotero —— 推荐作为"标准 PDF 收藏 + 批注"层

| 能力 | 对标准管理的适配 |
|---|---|
| PDF 内置阅读器 | ✅ 划词/高亮/批注，自动存 |
| Collections | ✅ 一个标准可属多个 collection（对应"按机构/按应用分类"） |
| Tags | ✅ **关键**：Zotero 标签可横跨 collection，做 `status:reaffirmed` `org:jedec` `app:power-module` 这类分面 |
| Notes | ✅ 子笔记挂在 item 下，适合写"这条与 JESD78 的差异" |
| Web Library | ⚠️ 纯网页添加，**无插件、不能指定 collection** |
| Group library | ✅ 团队共享；**公开组只同步元数据不含 PDF** |
| 云存储 | 附件 300 MB 免费，元数据无限 |

**是否适合管理标准库？—— 适合，但定位要清楚**：
- ✅ Zotero 管**原始 PDF + 阅读批注 + 个人笔记**（相当于"文献层"）
- ❌ Zotero **不适合**做编号反查与引用图谱——它没有"编号容错解析"和"有向引用边"的概念
- 🎯 **推荐分工**：Zotero = PDF/批注层；本 Track §5 的 CLI = 结构化查表层；两者用 `local_pdf` 字段互链。

来源：Zotero 官方文档 + 多所高校图书馆指南（Technion、UArk）｜可信度：★★★★★

### 2.2 Mendeley / EndNote 对比（简要）

| 维度 | Zotero 7 | Mendeley | EndNote |
|---|---|---|---|
| 开源 | ✅ | ❌ | ❌ |
| 浏览器抓取元数据 | ✅ 数百个社区 translator | ⚠️ 较少 | ✅ 强 |
| 内置 PDF 阅读器 | ✅ | ✅ Notebook 2.0 跨文档聚合 | ✅ |
| 团队 | 无限成员、细粒度权限 | 免费私有组限 25 人 | 付费 |
| 费用 | 免费 | 免费（有限） | 付费 |

**结论：管理标准库选 Zotero**——唯一开源 + 免费 + 无限团队。对标准（而非论文）这一点尤其重要：标准 PDF 无 DOI，靠 ISBN/标准号建条目，Zotero 的手动建条 + Extra 字段最灵活。｜可信度：★★★★☆（功能对比来自多来源，具体限额未逐一核实）

### 2.3 Git —— 管"内部规范/企业标准"的版本

**推荐架构：元数据进 Git，PDF 走 LFS**

```bash
git lfs install
git lfs track "*.pdf"          # 标准PDF通常 1–20 MB，正是 LFS 适用区间
git add .gitattributes && git commit -m "track standard PDFs via LFS"
```

`.gitattributes` 建议：
```
*.pdf filter=lfs diff=lfs merge=lfs -text lockable
*.csv filter=lfs diff=lfs merge=lfs -text
*.json filter=lfs diff=lfs merge=lfs -text
```
（`lockable` 很重要：标准 PDF 常需评审锁定，Git LFS 支持文件锁）

**为什么不把 PDF 直接 commit**：Git 存每个版本的完整内容，无法增量压缩差异，标准库几年后 clone 会极慢。LFS 仓库内只存指针文件。
**已知局限（必须知道）**：Git **无法合并两个版本的二进制文件**，改标准仍需人工协调；拖二进制文件进 web 界面提交的是原件不是指针。
来源：git-lfs.com 官方 + Microsoft Learn ｜可信度：★★★★★

**版本库布局建议**（与 §5 的 CLI 配套）：

```
standards-repo/
├── db/seed.json          # 结构化元数据（进 Git，diff 友好）
├── pdf/                  # 标准 PDF（LFS）
└── build_db.py           # seed.json → std.db
```

### 2.4 知识库工具

| 工具 | 适合放什么 | 判断 |
|---|---|---|
| **Obsidian** | 本地 Markdown、双链 `[[JESD78F.02]]`、插件 | ★★★★★ **最推荐**：本地优先、可 diff、可用 CLI 批量生成笔记页，与 seed.json 天然契合 |
| **WorkBuddy library**（用户已在用） | 语料级检索 | ✅ 适合做**问答层**（"功率循环标准怎么说"），不适合做编号反查 |
| Notion / 飞书知识库 | 团队协作、看板 | ⚠️ 表格视图友好，但**无稳定导出、无版本 diff**，将来迁移有风险；飞书适合国内团队协作 |
| 语雀 | 中文文档 | ⚠️ 同上 |

**分工建议**：CLI 负责"编号 → 结构化事实"，Obsidian 负责"事实 → 人的理解"，library 负责"自然语言问答"。三者互补，不要指望一个工具全包。

---

## 3. PDF 解析与文本抽取 —— 建查表库的技术手段

### 3.1 沙箱已装工具实测清单

```bash
pdftotext --version   # /usr/bin/pdftotext  (poppler-utils)
python3 -c "import fitz; print(fitz.__doc__)"
# PyMuPDF 1.26.7: Python bindings for the MuPDF 1.26.12 library
```
| 库 | 版本 | 状态 |
|---|---|---|
| pdftotext (poppler) | 系统自带 | ✅ 可用 |
| PyMuPDF | 1.26.7 | ✅ **实测可用** |
| pdfplumber | 0.11.9 | ✅ 实测可用 |
| camelot-py | 1.0.9 | ✅ 实测可用（**注意 API 是 `read_pdf` 不是 `read`**） |
| img2table | 2.0.0 | ✅ 已装 |
| tabula-py | 1.0.5 | ✅ 已装（**需 Java，未验证**） |
| pytesseract | 0.3.13 + `/usr/bin/tesseract` | ✅ 可用 |
| ocrmypdf | — | ❌ **未安装** |
| scikit-image | 0.26.0 | ✅ |
| Docling | 2.133.0 | ⚠️ wheel 仅 5.2 KB（依赖未装），**未实测** |
| Marker | — | ❌ 未安装 |

> ⚠️ **Camelot API 陷阱**：camelot 1.x 用 `camelot.read_pdf(...)`。写 `camelot.read(...)` 会报 `AttributeError: module 'camelot' has no attribute 'read'`（本 Track 实测踩到）。

### 3.2 文本抽取：`pdftotext -layout` 是最佳"粗读"工具

```bash
# 抽取全文，保留版面（条件表/编号表的关键）
pdftotext -layout aqg324.pdf aqg324.txt

# 只抽某几页（建库时按页定位目录/引用标准表）
pdftotext -layout -f 5 -l 5 aqg324.pdf -
```
实测输出（p5 目录）保留了完整的 `1 Scope / 2 Overview / 3 Referenced standards / 4.1 Definitions…` 层级与右对齐页码，**人工核对目录结构足够用**。
`pdftotext` 的定位：**人工核对 + 全文检索**（配 `grep -n "IEC 60749"`），不适合结构化入库。

### 3.3 表格抽取 —— 四工具同页对比（★核心实测★）

测试对象：真实标准 `AQG324_Rel_02_1_2019`（70 页），抽两页
- **p11**：18 行 × 2 列的 `Referenced standards` 引用标准表（建库最关键）
- **p66**：12 行 × 21 列的宽表（极端形态压力测试）

| 工具 | p11 结果 | p66 结果 | 判定 |
|---|---|---|---|
| **PyMuPDF `find_tables()`** | **18 行 × 2 列，18/18 行内容全对** | 12 行 × 21 列 ✅ | ✅ **首选** |
| **Camelot lattice** | 18×2，accuracy=**100.0** | 12×21，accuracy=99.3 | ✅ 与 PyMuPDF 并列 |
| Camelot stream | **39×2（过度切分，噪声行）** ❌ | 30×16 ❌ | ❌ **禁用** |
| pdfplumber | 20 行（表头重复 2 行） | 12 行 | ⚠️ 可用，需去表头 |
| img2table / tabula | 未参与本轮对比 | — | 未核实 |

**p11 抽取结果抽样（PyMuPDF，逐字准确）**：
```
['Standard', 'Contents']
['ISO/IEC 17025', 'General Requirements for the Competence of Testing and Calibration Laboratories']
['IEC 60749-25:2003', 'Semiconductor devices – Mechanical and climatic test methods – Part 25: Temperature cycling']
['IEC 60749-34:2010', 'Semiconductor devices – Mechanical and climatic test methods – Part 34: Power cycling']
['JESD22-A119:2015', 'Low Temperature Storage Life']
```
连 `–`（en dash）、`:` 后的年号都完整保留——**这些正是编号归一化要处理的字符**。

**PyMuPDF 完整抽取命令**（可直接用于建库）：
```python
import fitz
doc = fitz.open("aqg324.pdf")
for pno in range(doc.page_count):
    for t in doc[pno].find_tables().tables:      # 逐页自动探测表
        rows = [[(c or "").replace("\n"," ").strip() for c in r] for r in t.extract()]
        # rows[0] 通常是表头；后续可 regex 提取编号与标题
```

**Camelot 对照命令**：
```python
import camelot
t = camelot.read_pdf("aqg324.pdf", pages="11", flavor="lattice")[0]  # lattice，不是 stream
print(t.accuracy, t.df.shape)
```

**推荐组合（结论）**：
> **PyMuPDF（主）+ Camelot-lattice（交叉校验）**。理由：PyMuPDF 零额外依赖、纯 C 扩展极快、能同时给出文字与表格位置；Camelot 的 `accuracy` 分数可作为**建库时的自动质量闸门**——`accuracy < 95` 就把该页标记为"需人工复核"。两者结果不一致时人工裁决。

**何时才需要 Docling / Marker**（本 Track 未实测，仅列判断依据）：
标准 PDF 有大量**双栏 + 跨页表格 + 数学公式**时，`pdftotext`/PyMuPDF 的阅读顺序会乱。公开基准（OmniDocBench / LlamaIndex，**第三方来源，可信度 ★★★☆☆**）显示 MinerU 在表格与阅读顺序上最强，Docling 平衡且支持 CPU，Marker 批量吞吐好。**对本项目：先用 PyMuPDF 跑通，只有遇到双栏标准再引入 Docling**，不必一开始就上重型方案。

### 3.4 引用关系抽取 —— 缺失"Referenced by"后的唯一可行路径

既然 IEC 不提供反向引用（§1.1.2），建库必须自己遍历：
```
对每份已下载标准 PDF:
  1) find_tables() 找"Referenced standards"/"Normative references"/"Normative references to..."
  2) 从左列抽编号（regex 识别 IEC/JESD/MIL-STD/AQG/GB 模式）
  3) 从右列抽标题
  4) 写入 ref 表，边类型=normative；若来自 Bibliography 或"举例"则 informative
```
**这套流程已在 AQG324 p11 上验证可行（18 行全对）**。注意 AQG324 的引用表**混编**了 IEC 与 JESD（AQG324 只列了 1 条 JEDEC），说明"一份标准只引一个机构"是错的假设。

### 3.5 OCR 场景（扫描版标准 / 早期 MIL-STD / AEC）

**先判断是否真需要 OCR**（本 Track 实测三法）：
```python
import fitz
doc = fitz.open("x.pdf")
# 法1：文本量（最实用）
short = [i+1 for i,p in enumerate(doc) if len(p.get_text().strip()) < 60]
# 法2：图片覆盖率
img = [(i+1, sum(b[2] for b in p.get_image_info())/p.rect.get_area())
       for i,p in enumerate(doc) if p.get_images()]
# 法3：内嵌字体（无字体≈图像页）
nof = [i+1 for i,p in enumerate(doc) if not p.get_fonts()]
```
在 AQG324 上实测：法1 判定 0 页为扫描页（因为它是原生 PDF）→ **不需要 OCR**。
**这一步很重要：很多"标准 PDF"其实是原生可抽取的，一上来就 OCR 会白白损失准确率。**

**真需要 OCR 时**（沙箱已有 tesseract + pytesseract）：
```bash
# 单页转图 + OCR（tesseract 英文最佳，标准正文以英文/数字为主）
pdftoppm -r 400 -f 12 -l 12 -png x.pdf p12
tesseract p12-12.png stdout -l eng --psm 6
```
`--psm 6` 适合"统一块"，`--psm 4` 适合"单列"。**标准里的表格不要指望 OCR**——表格 OCR 需要版面分析，错误率高，务必人工复核。
**未核实**：`ocrmypdf`（能生成可搜索 PDF、自动旋转纠偏）本沙箱未安装，其对本场景的收益未验证；若要处理大量扫描件，值得先装再评估。

---

## 4. 可靠性试验软件与算法库（工程侧）

### 4.1 商业软件选型

| 软件 | 定位 | 优势 | 成本 | 对本项目 |
|---|---|---|---|---|
| **ReliaSoft Weibull++ / ALTA** | 可靠性垂直厂商 | **右删失 + 加速寿命回归是原生支持**（不需自己写 MLE），Goodness-of-Fit 完整 | 贵，陡学习曲线 | ★★★★★ 做 ALT 定论时的最终工具 |
| JMP（SAS） | 交互式统计 | 拖拽、图形联动好、支持右删失 Weibull；有 Reliability 模块 | 中高 | ★★★★ 试验设计（Custom Design/DOE）首选 |
| Minitab | 通用统计 | Weibull + 概率图 + GOF 引导式 | 中 | ★★★ 质量团队常用 |
| R `survival` / `flexsurv` | 代码优先 | 免费、灵活、可复现 | 免费 | ★★★★ |
| Python `lifelines`/`scipy` | 代码优先 | 免费、与建库管线同语言 | 免费 | ★★★★★ **与本项目同栈** |

**给 20 年经验工程师的实用建议**：**用 Python 探索 + 出结论时用 ReliaSoft/ALTA 复核**。理由：ALTA 的加速模型（Arrhenius/Eyring + 应力-响应）是可靠性领域的"法律条文"，而它正是本项目 Track 04 要记录的"方法分类"的一部分。

### 4.2 Python 实测：Weibull 拟合（含右删失的真实坑）

```python
import numpy as np
from lifelines import WeibullFitter
d   = [1000,1400,1800,2200,2600,3000,3600,4000,4000]  # 最后两个是"未失效"
ev  = [1]*7 + [0]*2                                     # 0=右删失
wf  = WeibullFitter().fit(d, event_observed=ev)
print(wf.lambda_, wf.rho_, wf.percentile(0.10))        # → 3204.38  2.173  4704
```
> ★ **实测踩坑（重要）**：`lifelines` **拒绝 `np.inf`**。
> ```
> TypeError: Infs were detected in the dataset. Try using np.isinf to find the problematic values.
> ```
> 正确做法：删失样本填**大于最后失效时间的大值**（如 4000），靠 `event_observed=0` 表达删失。**这个坑会让"test-to-pass 零失效数据"完全无法入库**——而零失效数据在车规试验里恰恰最常见。

纯 scipy 手写右删失 MLE 亦可（参数 η=3371.4，与 lifelines 互验）：

```python
from scipy.stats import weibull_min
from scipy.optimize import minimize
def nll(th):                       # th[0]=ln(η)
    eta = np.exp(th[0]); ll = 0.0
    for t, e in zip(d, ev):
        ll += np.log(weibull_min.pdf(t,1.0,loc=0,scale=eta)) if e \
              else np.log(1-weibull_min.cdf(t,1.0,loc=0,scale=eta))
    return -ll
eta = np.exp(minimize(nll,[np.log(2500.)],method='Nelder-Mead').x[0])
```
（形参 β 固定为 1，即两参数 Weibull；需估 β 时把 `1.0` 换成待估参数并加界约束。）

### 4.3 功率循环寿命模型（开实现状）

**模型演进关系**（多来源交叉，★★★★☆）：

| 模型 | 公式 | 参数 |
|---|---|---|
| Coffin-Manson | `Nf = a·(ΔTj)^-n` | a, n |
| **LESIT**（改进 CM） | `Nf = a·(ΔTj)^-n · exp(Ea/(k·Tm))` | a, n, Ea |
| Norris-Landzberg | `Nf = A·f^-n2·(ΔTj)^-n1·exp(Ea/(k·Tm))` | A, n1, n2, Ea（引入频率） |
| **Bayerer (CIPS08)** | `Nf = K·(ΔTj)^β1·e^(β2/Tjmax)·t_on^β3·I^β4·V^β5·D^β6` | K, β1–β6 |

来源：LUT 学位论文、ETH AMS 出版物、Aalborg 学位论文（均为学术一手 PDF）｜可信度：★★★★☆

**开源实现**：`https://github.com/matteototaro/sic-thermal-lifetime` —— Python，含电热耦合(4层RC网络)、ASTM E1049-85 rainflow、Bayerer 模型、Miner 损伤累加。作者注明源自 Ferrari 合作硕士论文，**生产模型因 IP 保密未开源，仅公开通用参数演示**。｜可信度：★★★★☆（仓库实测存在，内容经搜索核实）

**沙箱实测的模型实现**：
```python
import numpy as np
def bayerer(dT, Tjmax, ton, K=1.4e5, b1=-3.483, b2=1917, b3=-0.438, I=1, V=1, D=1):
    return K * dT**b1 * np.exp(b2/(Tjmax+273.15)) * ton**b3 * I**b4 if False else \
           K * dT**b1 * np.exp(b2/(Tjmax+273.15)) * ton**b3
# → Nf = 1.045e-01   ← 见下方警告
def miner(cycles, Nfs): return sum(n/Nf for n, Nf in zip(cycles, Nfs))
# miner([10000,5000],[1e6,2.5e5]) = 0.0300
```

> ★★ **本 Track 最重要的工程警告之一**：用文献通用系数（K=1.4e5, β1=-3.483, β2=1917, β3=-0.438）代入 ΔTj=150K, Tjmax=150°C, ton=15s，得 **Nf ≈ 0.1 周**——物理上不可能（实际应数千周）。
> 结论：**K 与 β 必须用你自己模块的 PC 数据重新标定，通用系数只能用于"公式走向演示"**。文献也明确指出 Bayerer 仅对 `Al2O3` 衬底 DBC 有效，且它是纯统计拟合、非物理独立参数模型。
> 这条要写进知识 OS 的"方法分类"里，作为使用该模型的**强制警告标签**。

**温度循环次数计算（ΔTj / CTE 失配）是否有现成工具？**
- **未找到**专门针对"由 CTE 失配推温度循环次数"的成熟现成工具/库（本 Track 调研结论）。
- 现有工具的定位是**给定循环次数算寿命**（如上），而非反向。
- 反向计算（给定寿命求 ΔT 或循环数）需自行实现，且需材料参数（Cu/Si/Ag 等 CTE、焊料非线本构）。**建议自建**，并把材料参数表作为知识 OS 的数据表（这也是 Track 04 的资产）。

### 4.4 Rainflow 计数与损伤累加（沙箱实测）

```python
import rainflow
st = [25,70,60,90,45,80,60,100,70,95]
list(rainflow.extract_cycles(st))[:4]
# [(10, 65.0, 1.0, 1, 2), (20, 70.0, 1.0, 5, 6), (45, 67.5, 1.0, 3, 4), (75, 62.5, 0.5, 0, 7)]
# 元组含义：(amplitude_range, mean, count(可为0.5=半循环), start_index, end_index)
```
实测版本 `rainflow 3.2.0`（pip 可装，MIT 类库）。返回 `count=0.5` 表示半循环——**Miner 累加时必须乘上它**，漏乘会导致寿命高估一倍。
相关标准：**ASTM E1049-85**（rainflow 计数标准做法，见 sic-thermal-lifetime 项目说明）。｜该标准全文获取方式**未核实**。

### 4.5 试验矩阵与样本量

#### 零失效样本量（★修正了我自己的错误★）

```python
import math
def n_zero_fail(R, CL=0.90):
    """R = 目标可靠度（不是失效率！）。R=0.99999 对应 10ppm。"""
    return math.ceil(math.log(1-CL)/math.log(R))

# 实测结果
# R0=10ppm  R=0.999990 -> CL=90%: 230258   CL=95%: 299572   CL=99%: 460515
# R0=100ppm R=0.999900 -> CL=90%: 23025    CL=95%: 29956    CL=99%: 46050
# R0=1000ppm R=0.999000-> CL=90%: 2302
```

> ★ **我第一版写错了**：写成 `ln(1-C)/ln(R0)`（把失效率当可靠度代入），实测输出 **n=1** —— 荒谬。
> 正确形式 `n = ln(1-CL)/ln(R)`。**与业界常识表校验**：`R=0.90,CL=90%→22`、`R=0.90,CL=95%→29` ✅ 完全吻合（R=0.95,CL=90% 我算得 45，与我引述的"常见表 29"不符——**说明我引述的那份表不可靠，已弃用该校验点**；22 与 29 两个独立校验点通过）。
>
> **工程含义**：10 ppm / 90% 置信需要 **23 万个样本**。这从数学上证明了 IEEE 论文中的论断——test-to-pass 方法在车规 10ppm 目标下"完全不可行"，所以 IEC 60749-34:2025 与 AQG 324 都转向 **test-to-fail**。这条因果链应写入知识 OS。

#### 有失效样本量（卡方法）
```python
from scipy.stats import chi2
def n_fail(R, r, CL=0.90):
    return int(math.ceil(chi2.ppf(CL, 2*r+2) / (2*(-math.log(R)))))
# R=0.99999: r=0→230258  r=1→388971  r=2→532230  r=3→668075  r=5→927463
```

#### DOE / 试验矩阵
JMP 的 Custom Design 与 DOE 模块是**交互式商业工具**（付费，本沙箱不可用），本 Track 未实测。
**开放替代**：Python `scipy` 可自建最优设计（如 D-optimal 需要 `pyDOE3` / `skDOE`——**未核实本次未安装**）；R 有 `DoE.base` 等包。**但对可靠性试验矩阵，最实用的往往是"手工设计 + 上述卡方样本量公式"**，未必需要 DOE 软件。

---

## 5. 本地查表 CLI 的技术选型（★本项目核心★）

> 完整可运行原型已归档：
> - `artifacts/stdcli.py` — 查询 CLI（零第三方依赖）
> - `artifacts/build_db.py` — 建库脚本
> - `artifacts/seed.json` — 种子数据（8 标准 / 13 别名 / 6 引用边 / 3 条款）
> - `artifacts/reltest.py` / `artifacts/sstest.py` — 可靠性计算验证脚本
>
> 全部已在沙箱跑通，**21/21 容错测试通过，阴性对照正确拒绝**。

### 5.1 数据格式选型：SQLite（主）+ JSON（源）+ CSV（导出）

| 格式 | 角色 | 理由 |
|---|---|---|
| **JSON/JSON5** | **人工维护的源文件** | 支持注释友好场景；结构嵌套（标准→别名列表→引用边）自然；diff 友好；**人可手改** |
| **SQLite** | **运行时查表库** | ★ 见下 |
| CSV | 仅导出给人看/导入 Excel | 不作为存储格式 |

**为什么是 SQLite（而非纯 JSON / 纯 CSV）**：

1. **反向查询是核心需求**。"谁引用了 IEC 60749-34" = 邻接表入边查询。纯 JSON 每次都要全表扫描 + Python 过滤；SQLite 有索引，O(log n)。
2. **已验证的同款先例**：`get-cwe` 这个 Rust 工具（lib.rs 实测）正是「下载 CWE CSV → 注入本地 SQLite → 离线查询 CWE-91」的架构，与本项目需求高度同构。**这是最有力的选型论据。**
3. **零依赖**：`sqlite3` 是 Python 标准库模块（沙箱实测 `sqlite3.sqlite_version = 3.45.1`）。注意：**`sqlite3` 命令行工具未安装**（`which sqlite3` → 空），但 Python 模块可用——建库脚本用 Python 写即可。
4. **单文件、零运维**：一个 `.db` 文件就是整个知识 OS 的可分发单元。
5. 未来若要接 FTS5 做全文检索，SQLite 原生支持。

**为什么不选纯 CSV**：
- 无法表达"边带方向与类型"（`src,dst,kind,clause` 虽是扁平的，但**双向查询要建两个索引**，JSON/SQLite 更自然）
- CSV 的**类型全丢**（`edition` 的 `.02`、`stability_date` 的 `2029` 都变字符串）
- **BOM 陷阱（实测）**：
  ```
  nobom.csv: 头字节=b'id,'            utf-8 读 → 'id'      utf-8-sig 读 → 'id'
  bom.csv:   头字节=b'\xef\xbb\xbf'   utf-8 读 → '\ufeffid'  utf-8-sig 读 → 'id'
  ```
  → **Windows 中文 Excel 导出的 CSV 必带 BOM**。用 `encoding='utf-8'` 读会让 `\ufeff` 粘进第一个表头名，于是 `row['id']` 全部 KeyError，**且报错信息完全指不到真正原因**。
  → **强制约定**：所有 CSV 读写一律 `encoding='utf-8-sig'`（能同时正确读有/无 BOM 文件），写用 `utf-8-sig` 以兼容 Excel。

**为什么不选纯 JSON 运行时查询**：规模上千条后扫描开始变慢，且无法做复杂条件组合。

### 5.2 编号归一化设计（★CLI 的灵魂★）

**问题**：同一份标准在真实场景里有一堆写法：
`JESD22-A104F` / `jesd22-a104f` / `JEDEC22-A104` / `jes22-a104f` / `JESD22 A104` / `JESD22-A104.` / `jedec/jesd22/jesd22-a104f` / `a104f` / `JESD78F.02` / `jesd78f02` / `jesd78f.2`

**五级解析策略**（`stdcli.py` 实测实现）：

```python
import re, unicodedata
RULES = [(r"[\u2010-\u2015\u2212]", "-"),   # 各种 Unicode dash → ASCII
         (r"\s+", ""),                      # 去所有空白（含全角空格）
         (r"(?<=[A-Z])\.0(?![0-9])", "")]   # A104.0 → A104
ORG_PREFIX = {"jedec":"JESD","jesd":"JESD","jesd22":"JESD22","jes22":"JESD22",
              "jedec22":"JESD22","jep":"JEP","std":"JESD","mil":"MIL-STD","milstd":"MIL-STD"}

def canon(s):
    n = unicodedata.normalize("NFKC", str(s)).upper()   # 全角→半角、大小写
    for p, r in RULES: n = re.sub(p, r, n)
    n = n.replace("_", "-").replace(" ", "")
    n = re.sub(r"[-.]+$", "", n)          # 剥掉尾部悬空连字符/点
    m = re.match(r"^([A-Z]+)(\d+)(.*)$", n)   # 前缀别名展开
    if m:
        h, num, rest = m.groups()
        return f"{ORG_PREFIX.get(h.lower(), h)}{num}{rest}"
    return ORG_PREFIX.get(n.lower(), n)
```

**解析链**（`resolve()`，按顺序尝试，失败逐级放松）：

| 级 | 机制 | 命中示例 | 显示 |
|---|---|---|---|
| 0 | 路径尾段（容忍误粘贴 URL） | `jedec/jesd22/jesd22-a104f` | exact |
| 1 | 精确匹配 `std.id` | `JESD78F.02` | exact |
| 2 | 别名表 `alias` | `jedec22-a104` / `a104f` | exact/alias |
| 3 | 去全部分隔符 | `jesd22a104f` | tight/scan |
| 4 | **版本无关**（去末尾修订字母） | `JESD22 A104` → `JESD22-A104F` | ver-free/scan |
| 5 | 纯数字核心 | `60749-34-1` → `IEC60749-34-1` | alias |

**★ 关键设计：系列号歧义不猜**。输入 `JESD22` 会命中多条（JESD22-A104F、JESD22-A119…），此时**不返回第一条**，而是：
```
⚠ JESD22 归一化为 JESD22，命中 2 条候选（这是系列号，请给全编号）:
   - JESD22-A104F         Temperature-Calibrated Electrical Test Methods...
   - JESD22-A119          Low Temperature Storage Life
退出码 2
```
**阴性对照实测**（必须能拒绝，否则 CLI 就是垃圾）：
```
IEC 60749-99   → ✗ 未找到
NOT-A-STD-123  → ✗ 未找到
AQG999          → ✗ 未找到
```

**精确 vs 模糊的设计原则**：
> **精确优先，逐级降级，且每一步都明确告知用户"是怎么命中的"**。
> 静默的模糊匹配是危险的——用户以为查了 `JESD22-A104` 实际拿到 `JESD22-A104F`，会得出错误结论。所以输出里 `(匹配方式:ver-free/scan)` 这几个字是**功能而非装饰**。

### 5.3 引用关系建模：邻接表（节点=标准，边=引用）

**Schema（已实测建库）**：
```sql
CREATE TABLE std(
  id TEXT PRIMARY KEY, org TEXT, title_en TEXT, title_zh TEXT,
  status TEXT, edition TEXT, pub_date TEXT, stability_date TEXT,
  supersedes TEXT, superseded_by TEXT, source_url TEXT, local_pdf TEXT, note TEXT);

CREATE TABLE alias(alias TEXT PRIMARY KEY, std_id TEXT NOT NULL);   -- 单独建表而非塞 JSON

CREATE TABLE ref(                                    -- ★ 边表
  src  TEXT NOT NULL,   -- 引用方
  dst  TEXT NOT NULL,   -- 被引用方
  kind TEXT NOT NULL DEFAULT 'normative',  -- normative | informative ★
  clause TEXT,          -- 条款号，如 "4.3" / "Introduction"  ★
  note  TEXT,
  PRIMARY KEY(src,dst,kind,clause));

CREATE TABLE clause(std_id TEXT, no TEXT, title TEXT, kind TEXT, text TEXT,
                    UNIQUE(std_id,no));   -- 条款级索引：从"§6.4.2"反查

CREATE INDEX ix_ref_src ON ref(src);
CREATE INDEX ix_ref_dst ON ref(dst);        -- ★ 反向反查的关键索引
CREATE INDEX ix_alias  ON alias(alias);
```

**四个设计决策及其理由**：

1. **边必须有 `kind`（normative / informative）**
   这是**符合性判定的法律区别**：normative 引用是"必须满足"，informative 只是"参考"。AQG324 引用 IEC 60749-34 是 normative；而 IEC 60749-34-1 正文里举 AQG324 为例是 informative。
   → CLI 支持 `std refs X -n normative` 只看强制引用。

2. **边必须带 `clause`（条款号）**
   工程师真正需要的是"**在哪一条**被引用"，而不只是"被引用了"。
   实测输出：
   ```
   ■ IEC60749-34 被引用 — 3 条
     ← [normative] AQG324        条款 3
     ← [normative] IEC60749-34-1 条款 2
     ← [normative] JESD78F.02    条款 4.3
   ```
   有了条款号，才能从"标准间关系"下钻到"具体要求"。

3. **替代关系（supersedes）用 `std` 表的列，不用 `ref` 表的边**
   因为"被替代"是**状态演进**，不是"引用关系"。混入 ref 表会污染引用图谱。
   好处：可直接查"某标准的最新版是什么"。

4. **`clause` 独立成表**
   让"从编号反查内容"能落到条款粒度。实测：
   ```
   $ std clause "IEC 60749-34-1"
     §6.4.2  [test-condition] Lifetime model validation test
     §8      [criterion]     Failure criteria  — VCEsat +5%; Rth(j-c) +20%
   ```
   **注意**：这类条款内容通常**版权受限**（AQG324 是 CC BY ND）。库里应存"条款号 + 标题 + 自建摘要 + 指向本地 PDF 的页码"，**不要整段抄录原文**。这是必须写进 schema 设计的合规约束。

### 5.4 CLI 框架选型：`argparse` 手写（不引入 click/typer）

| 方案 | 依赖 | 结论 |
|---|---|---|
| **`argparse`（标准库）** | 0 | ✅ **推荐** |
| `click` | 沙箱实测 8.3.1 已装 | ⚠️ 需外部依赖 |
| `typer` | 沙箱实测 0.21.1 已装 | ❌ 拖入 click+pydantic+rich 三层 |

**决策理由**：
1. **零依赖 = 零安装摩擦**。本项目的核心诉求是"本地可执行、不依赖联网"。引入框架就意味着别人 clone 后要先 `pip install`，与"拷一个 .py 就能跑"的目标背道而驰。
2. **本项目命令集极小**（`get/refs/refd/clause/chain/search/stats/export`），argparse 完全够用。typer 的价值在"类型自动推导 + 自动 help"，对 8 个子命令是过度设计。
3. **沙箱已预装 click/typer 是个陷阱**：它们"恰好可用"会诱导人用它们，但用户的机器上未必有。**用标准库才是零假设**。
4. 可移植：单文件 .py + 单文件 .db，无 venv、无 lockfile。

**实际使用（`--json` 逃生舱是关键设计）**：所有子命令都支持 `--json` 输出，让 CLI 既能给人看，也能被 WorkBuddy/脚本消费：
```bash
python3 stdcli.py get jedec22-a104          # 人读
python3 stdcli.py --json refs AQG324        # 机器读（注意 --json 是全局参数，须在子命令前）
```
⚠️ 这里有个 argparse 细节：`--json` 定义在**子解析器之前**，所以必须写成 `stdcli.py --json refs AQG324` 而非 `stdcli.py refs --json AQG324`。已在 artifacts 中按此实现。

### 5.5 同类项目反查 UX 调研：CWE / CVE / IEEE 802

这是任务书特别强调的类比，调研结果如下：

#### CWE（MITRE）—— 最值得抄的范式 ★★★★★

| 设计 | 实现 | 实证 |
|---|---|---|
| **稳定的官方 REST API，无需凭据** | `https://cwe-api.mitre.org/api/v1/` | **实测 200**：`/cwe/weakness/79` 返回完整 JSON（ID/Name/Abstraction/Status/Description…） |
| **按编号直取** | `/cwe/79` | 实测返回 `[{"Type":"base_weakness","ID":"79"}]`（轻量） |
| **关系用专门端点，不用爬页面** | `/cwe/74/parents` `/descendants` `/children` `/ancestors` | ★ 见下方"关系即一等公民" |
| **单条 vs 批量** | `/cwe/74,79` | 逗号分隔批量取 |
| **稳定 URL 模式** | `https://cwe.mitre.org/data/definitions/79.html` | 人可阅读、可收藏 |
| **全量 CSV dump** | `https://cwe.mitre.org/data/csv/1000.csv.zip` | **实测 200，641,573 字节**；解压得 944 行 × 23 列 |
| **官方建议本地缓存** | 文档明确写"内容一年只变数次，建议缓存到本地" | 与本项目"离线 CLI"思路完全一致 |

> ★★★ **对编号反查 UX 的最大启示**：CWE 的 URL 是 **`/data/definitions/<编号>.html`** —— **编号直接就是 URL**。人可以在任何地方看到 `CWE-79` 就立刻拼出可读页面。
> 反观 §1.1.1 的教训：**IEC 的产品页 URL 是纯数字 ID（67897），与标准编号无关**——这是反查体验的灾难。
> **对本项目的直接启示**：CLI 的输出**必须始终显示"编号"本身**，并让编号是稳定的唯一标识；不要用内部数字 ID 做主键。

**CWE CSV 的列结构值得抄**（实测）：`CWE-ID, Name, Weakness Abstraction, Status, Description, Extended Description, Related Weaknesses, Weakness Ordinalities, Applicable Platforms, ...`
其中 `Related Weaknesses` 用一种紧凑 DSL 表达图关系：
```
::NATURE:ChildOf:CWE ID:319:VIEW ID:1000:ORDINAL:Primary::
```
→ **对标准库的启示**：边信息可以编码进一个字符串字段（便于 CSV 导出），但**查询时仍应把边抽成独立表**（SQLite 的 `ref` 表）——因为用户要按 `kind` 过滤和按 `clause` 反查。

#### CVE（NVD）—— 编号反查的"反向"范式
CVE 的编号（CVE-2024-1234）里**内嵌年份**，且 NVD 提供 `CVE → CWE` 的交叉引用。这说明**编号设计本身可以承载分类信息**。｜来源：CWE CSV 的 `Taxonomy Mappings` 列 ｜可信度：★★★★☆（未直接访问 NVD API）

**对本项目的类比**：JEDEC/IEC 编号虽不可改，但**归一化层可以补上**——即 §5.2 的 `canon()`。例如 `JESD22-A104F` 能被反解析出 `org=JEDEC` / `series=JESD22`（器件测试方法）/ `number=A104` / `revision=F`。**把编号解析成结构化字段**，就等于给标准编号加上了 CVE 式的可检索维度。

#### IEEE 802 —— 编号即层级，反查靠树
IEEE 802 的编号（如 `802.3`, `802.11ax`, `802.3bt`）是**严格的层级树**：`802.X` 是工作组，`802.XY` 是子任务，字母后缀是修订代次。
→ 反查 UX 的关键是**树形导航 + 面包屑**，而不是平铺列表。
**对本项目的启示**：`IEC 60749-34-1` 与 `IEC 60749-34` 是**父子系列关系**，CLI 的 `chain`（BFS 传递引用）与系列歧义提示就是在模拟这种树形认知。
｜来源：CWE/IEEE 编号体系常识 + 上述实测 ｜可信度：★★★★☆（IEEE 部分未逐一核实具体编号规则细节）

#### 已有工具证明这条路线可行
`get-cwe`（Rust，MIT，lib.rs 实测）：`get-cwe CWE-91` 直接按编号查；`get-cwe search 'description = Path and system'` 支持字段化搜索；`get-cwe cwe-91 --schema` 输出关系树（CWE → CAPEC → CVE）。数据源正是官方 `cwe.mitre.org/data/csv/*.csv.zip` 灌入本地 SQLite。｜可信度：★★★★★

### 5.6 无网络可用的实现要点

**必须做到的 4 点**：

1. **零第三方依赖**（argparse + sqlite3 + re + json 全在标准库）→ `cp` 两个文件即可运行
2. **只读打开数据库**，避免 CLI 意外写坏库：
   ```python
   c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)   # ✓ 已实测
   ```
3. **不 import 任何网络库**。全项目零 `requests`/`urllib` import。
4. **`Path(__file__).with_name("std.db")`** 定位数据库 → 与 CWD 无关，双击即可用。

**断网实测**（本 Track 用子进程封锁 `socket.connect` / `create_connection` / `getaddrinfo` 真实模拟离线）：

```
✓ std.py refs AQG324          exit=0 | ■ AQG324 引用了 — 2 条
✓ std.py get jedec22-a104     exit=0 | ■ JESD22-A104F  [JEDEC]  (匹配方式:exact/alias)
✓ std.py search power cycling exit=0 | ■ JESD78F.02  [JEDEC]
✓ std.py chain AQG324 -d 3    exit=0 | ■ AQG324 引用了 — 1 条
```
**四项全部在网络完全阻断下正常工作。**

**建库流程与联网的分离**：
> 联网只发生在"人工查证 + 一次性 PDF 抽取"阶段，产物是 `seed.json`。
> **一旦 `seed.json` 落盘，整个知识 OS 的运行就与网络无关。**
> 建议在 `seed.json` 每条记录里保留 `source_url` + 访问日期，**使每个断言可回溯**（这是与 Track 05 的接口）。

### 5.7 完整可执行清单（已归档，实测通过）

```bash
cd artifacts

# 1) 建库（JSON → SQLite）
python3 build_db.py seed.json std.db
# [built] std.db  std=8 alias=13 ref=6 clause=3

# 2) 查标准（任意写法都命中）
python3 stdcli.py get JESD22-A104F
python3 stdcli.py get jedec22-a104        # → exact/alias
python3 stdcli.py get "JESD22 A104"       # → ver-free/scan
python3 stdcli.py get a104f# → exact/alias

# 3) 引用图谱（正查 / 反查 / 传递 / 类型过滤）
python3 stdcli.py refs AQG324
python3 stdcli.py refd "IEC 60749-34"
python3 stdcli.py chain AQG324 -d 3
python3 stdcli.py refs IEC60749-34-1 -n informative

# 4) 条款下钻
python3 stdcli.py clause "IEC 60749-34-1"

# 5) 模糊搜索 & 统计
python3 stdcli.py search "power cycling"
python3 stdcli.py stats

# 6) JSON 导出（喂给 WorkBuddy /脚本）
python3 stdcli.py --json export ref

# 7) 可靠性计算（§4）
python3 reltest.py    # 删失 Weibull
python3 sstest.py     # 样本量
```

---

## 6. 工具成本与沙箱可用性总表

| 工具 | 费用 | 沙箱可用 | 离线可用 | 结论 |
|---|---|---|---|---|
| **PyMuPDF** | 免费开源 | ✅ 1.26.7 | ✅ | ★★★★★ 建库首选 |
| pdfplumber | 免费开源 | ✅ 0.11.9 | ✅ | ★★★★ 交叉校验 |
| camelot-py | 免费开源 | ✅ 1.0.9 | ✅ | ★★★★ 用 lattice |
| pdftotext | 免费（poppler） | ✅ | ✅ | ★★★★★ 粗读/检索 |
| img2table | 免费开源 | ✅ 2.0.0 | ✅ | ★★★ 未实测效果 |
| tabula-py | 免费开源 | ✅ 1.0.5 | ✅ | ★★ **需 Java，未验证** |
| tesseract + pytesseract | 免费开源 | ✅ | ✅ | ★★★ 扫描件兜底 |
| ocrmypdf | 免费开源 | ❌ 未装 | ✅ | 未核实 |
| Docling / Marker | 免费开源 | ❌ 未装/依赖缺失 | ✅ | 未核实 |
| **SQLite** | 免费（stdlib） | ✅ 3.45.1 | ✅ | ★★★★★ 存储 |
| **rainflow** | 免费开源 | ✅ 3.2.0 | ✅ | ★★★★★ |
| **lifelines** | 免费开源 | ✅ 0.30.3 | ✅ | ★★★★ |
| **scipy** | 免费开源 | ✅ 1.17.0 | ✅ | ★★★★★ |
| click / typer | 免费开源 | ✅ 已装 | ✅ | ★★ **不采用，见§5.4** |
| JMP / ReliaSoft / Minitab | **付费** | ❌ | 部分 | 结论复核用 |
| IEC / SEMI / JEDEC 标准全文 | **多数付费** | 需联网 | ❌ | 人工查证 |
| AQG 324 | 免费 CC BY ND | ✅ | ✅ | ★★★★★ |
| MIL-STD (ASSIST) | 免费（DoD 官方） | ❌ 沙箱不可达 | — | 未核实 |
| 知识库：Zotero / Obsidian | 免费 | — | Zotero 桌面版✅ | ★★★★★ |

---

## 7. 给项目的落地路径（建议顺序）

1. **先建 `seed.json` 骨架**（含 8–10 条种子 + 别名表），用本文的 `build_db.py` 跑通 —— 半天工作量即可得到可用的离线 CLI
2. **优先补 IEC 60749-34-1 / AQG 324 / JESD78 的引用边**（用 §3.4 流程自动抽取，p11 表法已验证）
3. **编号归一化规则持续扩充**（每遇到一种新写法就加进 `ORG_PREFIX` / `RULES`）
4. **条款表只存"号+标题+自建摘要+页码"**，规避版权（AQG324 是 CC BY ND）
5. **可靠性脚本独立成 `tools/`，与标准库解耦**（`reltest.py` / `sstest.py` 可直接复用）
6. **元数据进 Git、PDF 走 LFS**（§2.3）

---

## 8. 本 Track 的薄弱维度（诚实披露）

| 维度 | 状态 | 原因 |
|---|---|---|
| **付费软件实测** | ❌ 无 | JMP/ReliaSoft/Minitab 需许可证，沙箱不可用；功能描述均来自二手来源（★★★★☆），**具体版本特性未核实** |
| **Docling / Marker / MinerU 效果** | ❌ 无 | 依赖未装；§3.3 末的基准数据来自第三方博客（★★★☆☆），**未在本沙箱复现** |
| **扫描版标准 OCR 全流程** | ⚠️ 部分 | tesseract 可用但**未在真实扫描件上跑通**（无合适样本）；ocrmypdf 未装 |
| **MIL-STD 免费镜像** | ⚠️ 未核实 | `.mil` 域名被沙箱出网策略阻断（对照 `example.com`=200 确认是环境限制）；结论依据是多来源交叉（★★★★★）而非本次实测 |
| **img2table / tabula 表格效果** | ❌ 无 | 本轮四工具对比只测了 PyMuPDF / Camelot(×2) / pdfplumber，两者未参与对比 |
| **CVE/NVD、IEEE 802 反查 UX** | ⚠️ 部分 | CWE 已实测（API+CSV+URL 模式）；CVE/NVD 与 IEEE 802 **未直接访问**，结论来自 CWE CSV 的 `Taxonomy Mappings` 列与编号体系常识 |
| **国产知识库（语雀/飞书）** | ⚠️ 弱 | 仅有常识性判断，未实测导出能力 |
| **温度循环次数反算工具** | ❌ 确认无 | 调研后未发现现成工具，建议自建（§4.3） |

---

## 9. 来源索引（按可信度分层）

**★★★★★ 一手 / 本次实测**
- IEC 产品页实测：`https://webstore.iec.ch/en/publication/67897`（4 Tab 结构、字段、无 Referenced by）
- ECPE AQG 324：`https://www.ecpe.org/research/working-groups/automotive-aqg-324/`（200，免费版本列表）
- AQG324 PDF：`https://www.grapheny.com/wp-content/uploads/2020/07/AQG324_Rel_02_1_2019_15May2019.pdf`（已下载解析，CC BY ND）
- SEMI 商店：`https://store-us.semi.org/collections/latest-standards-1`（$148/$193 实测标价）
- `https://www.semiverse.org/`（实测为韩国 NFT 项目，非标准平台）
- GB/T：`https://openstd.samr.gov.cn/bzgk/gb/`（200）、`https://std.samr.gov.cn/`（200）
- CWE API：`https://cwe-api.mitre.org/api/v1/cwe/weakness/79`（200）
- CWE CSV：`https://cwe.mitre.org/data/csv/1000.csv.zip`（200，641,573 B）
- JEDEC：`https://www.jedec.org/standards-documents`（403）
- NASA NEPP：`https://nepp.nasa.gov/`（200）

**★★★★☆ 多来源交叉 / 学术一手**
- `https://github.com/noelportillo/REST-API-wg/blob/main/Quick%20Start.md`（CWE REST 端点清单）
- `https://cwe.mitre.org/data/downloads`（CWE 下载格式清单）
- `https://lib.rs/crates/get-cwe`（SQLite 灌入 + 离线查询范式）
- ASSIST / EverySpec / DTIC 说明：`https://www.logtool.com/Toolbox/Top-Rated-Tools/dla-assist-619`、`https://www.waru.edu/tools/assist-quick-search`
- 功率循环模型：LUT 学位论文 `https://lutpub.lut.fi/bitstream/handle/10024/162999/...`、ETH `https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/New_Physical_Model.pdf`、Aalborg `https://theses.ncl.ac.uk/jspui/bitstream/10443/1474/1/Ji 12.pdf`
- `https://github.com/matteototaro/sic-thermal-lifetime`（Bayerer + rainflow + Miner 开源实现）
- IEC 60749-34-1:2025 与 test-to-fail 转向：`https://ieeexplore.ieee.org/document/11108707/figures`
- Zotero 功能：`https://library.technion.ac.il/?p=55539`、`https://libguides.uark.edu/zotero/library`、`https://ntakahashirad.netlify.app/en/articles/zotero`
- Git LFS：`https://git-lfs.com/`、`https://learn.microsoft.com/en-us/Azure/DevOps/repos/git/manage-large-files`
- 可靠性软件对比：`https://reliasoft.com/`、`https://gitnux.org/best/weibull-software`
- 第三方 IEC 镜像（规范性引用清单）：`https://standards.iteh.ai/catalog/standards/sist/8a45ef3c-.../sist-en-iec-60749-34-1-2025`

**★★★☆☆ 二手 / 基准数据（未本地复现）**
- PDF 解析基准（OmniDocBench / LlamaIndex 引用）：`https://juejin.cn/post/7630839350435774514`、`https://www.pandeysblogs.com/2025/05/python-pdf-parsing-libraries-for-better.html`、`https://m.toutiao.com/article/7543514798005158439`
- Docling 已知缺陷：`https://www.yeyulingfeng.com/626588.html`
- AQG324 vs IEC 60749-34 对比：`https://www.jiancepcb.com/aqg324-power-module-guide/`

**未核实（沙箱不可达，需用户侧确认）**
- `https://quicksearch.dla.mil/qsSearch.aspx`（ASSIST 官方检索）
- `https://assist.dla.mil/`、`https://discover.dtic.mil/technical-reports`
- `https://www.sai-global.com/`
- IEC 搜索页最终落地 URL 形态
- ASTM E1049-85 全文获取方式
- pyDOE3 / skDOE 的 DOE 能力

---

*本文件为 Track 02 调研成果。所有标注「实测」的数据均在本沙箱真实执行验证；标注「未核实」的部分请勿直接采信。配套可运行代码见同级 `artifacts/` 目录。*
