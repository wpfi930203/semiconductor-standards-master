# Track 05 — Sources（信息源地图）：从哪里持续获取权威、可靠、可追溯的半导体标准信息

> **调研对象**：半导体标准信息源（不是标准本身，是"去哪里查、怎么核对、怎么确认最新版"）
> **目标读者**：功率半导体封装可靠性工程师（20 年经验），要建"从标准编号反查内容"的知识 OS
> **调研日期**：2026-10-05
> **交付定位**：本文件是Track 04（正典）与 Track 06（术语/编号）的**上游依赖**。知识 OS 的每个断言都必须能回溯到本文件中列出的某个信源 + 访问日期。

---

## 0. 执行摘要：本次调研的 8 个关键发现

| # | 发现 | 对用户的价值 | 可信度 |
|---|---|---|---|
| 1 | **JEDEC / IPC / SEMI 均以 ToS 或技术手段禁止自动化抓取**（JEDEC 对 curl 直接返回 403） | 知识 OS **不能靠爬虫建库**，必须走"人工核对 + 官方检索页"路线。这是架构级约束 |★★★★★实测 |
| 2 | **IEC Webstore 每个标准页有 3 个官方 tab：`Lifecycle` / `Normative references` / `Referenced by`** | 这是**唯一能自动提取"某标准引用了哪些标准"的官方入口**，直接解决 normative 引用图谱问题 |★★★★★ |
| 3 | **IEC 官方公开 TC 项目状态页，含完整阶段代码表（CDV/FDIS/PPUB/DELPUB…）** | 可用于**盯在研标准的草案进度**，比等标准发布早1–2 年 |★★★★★ |
| 4 | **JEDEC 有公开的 5 年复审制度**（手册 §7.2：Reaffirm / Revise / Rescind / 转 ANSI-IEC） | 这是判定"现行/已被取代/已废止"的**制度性依据**，不是靠猜 |★★★★★ 一手手册 |
| 5 | **JEDEC 状态标签实测为 `Reaffirmed` / `Rescinded` / `Superseded`，不是任务书假设的 `Active` / `Withdrawn`** | 查表 CLI 的枚举值必须改，否则永远匹配不上 |★★★★★实测 |
| 6 | **JEDEC 大部分标准"免费注册下载"，但部分文档付费**（实测 JESD78F.02 免费 / JESD79-4D 售价 $284） | 决定了知识 OS 的"免费覆盖率"能到多少 |★★★★★实测 |
| 7 | **中国国标平台对"采标"与"非采标"采取不同开放度**（采标 GB/T 只给题录信息） | 解释了为什么中国国标站查不到某些 IEC 转化标准全文——不是 bug，是版权设计 |★★★★★官网原文 |
| 8 | **MIL-STD-883 有可用的免费官方镜像（NASA NTRS / NEPP），但基版只有 28 页，方法正文在 883-1~883-5 分册** | 这是最容易踩的坑：拿到 883 就以为拿到全部方法 |★★★★★ 实测下载并解析 PDF |

**另检出 4 个高危内容农场陷阱**（详见 §6.4）：本次调研中，"SEMI G92 是 2.5D/3D Chiplet 互连可靠性指南"这一说法在多个英文站流传，但**官网核实 G92 实为 450mm 晶圆 tape-frame 卡匣机械规格**。

---

## 1. 官方标准组织入口（权威源，优先级最高）

### 1.1 JEDEC —— 器件与测试方法的主体标准组织

#### 1.1.1 检索入口与 URL 结构（实测）

| 用途 | URL | 实测状态 |
|---|---|---|
| 首页（顶部有Search by keyword or document number） | `https://www.jedec.org/` | 200 |
| 标准与文档检索页（含 facet） | `https://www.jedec.org/standards-documents` | 200 |
| 文档搜索（带查询串） | `https://www.jedec.org/document_search?search_api_views_fulltext=<编号>` | **403（反爬）** |
| 单个文档页| `https://www.jedec.org/standards-documents/docs/<slug>` | 200（需正确 slug） |
| 单个文档页（另一路径） | `https://www.jedec.org/node/<数字ID>` | 200 |
| 委员会列表 | `https://www.jedec.org/committees` | 200 |
| 服务条款（反爬声明） | `https://www.jedec.org/termsofuse` | 200 / curl 403 |
| 流程手册（免费 PDF） | `https://www.jedec.org/sites/default/files/JM21W.pdf` | 200，633 KB |

> **⚠️ 已核实的 URL 陷阱** `[一手]`：`https://www.jedec.org/standards-documents/docs/jesd22-a104f` 与 `.../jesd78f-02` 均返回 **"Page not found"**（404，非 403）。实际可用的 slug 形式是**连字符分隔**，例如 `https://www.jedec.org/standards-documents/docs/jesd-78b` → 正确打开 JESD78F.02。**查表CLI 不要用"删连字符"的猜测规则拼 URL。**

#### 1.1.2 文档类型 facet（官网实时计数，2026-10-05）

来源：`https://www.jedec.org/standards-documents` ｜可信度：★★★★★

| 前缀 | JEDEC 官方类型名 | 计数 |
|---|---|---|
| **JESD** | JEDEC Standards（规范性） | 484 |
| MO- | Microelectronic Outlines | 364 |
| JEP | JEDEC Publications（出版物，非规范性） | 131 |
| MODULE | Modules | 119 |
| TO- | Transistor Outlines | 55 |
| CO- | Carrier Outlines | 44 |
| MS- | Microelectronic Standards | 34 |
| SO- | Socket Outlines | 32 |
| SPD | Serial Presence Detect | 26 |
| SPP- | Standard Practices and Procedures | 25 |
| DO- | Diode Outlines | 19 |
| SDRAM | Synchronous DRAM | 16 |
| DG- | Design Guideline | 15 |

> **`[推断]`** 计数为调研当日快照，会随发布变动；**分类口径以官网为准**，不要把数字硬编码进知识 OS 当作断言。

#### 1.1.3 状态字段：实测结论（**修正任务书假设**）

**任务书写"Active / Superseded / Withdrawn"。实测 JEDEC 官网实际使用的标签是：** `[一手，实测]`

| 任务书假设 | **JEDEC 官网实测标签** | 来源 |
|---|---|---|
| Active | **`Reaffirmed`**（复审确认继续有效） | JEDEC 检索结果页 EIA318-B 条目 |
| Superseded | **`Superseded`**（且正文写明 "SUPERSEDED BY xxx"） | EIA318-1、EIA308-A 条目 |
| Withdrawn | **`Rescinded`**（撤销出版） | EIA308-A 条目 |

> **实操结论**：知识 OS 的状态枚举值应改为 `{Reaffirmed, Superseded, Rescinded, (无标签=可能是新发布)}`，并保留"正文内嵌 SUPERSEDED BY 目标编号"的文本抽取，因为 JEDEC **并非每个被取代的旧文档都在结构化字段里给出继任者编号**，很多时候只写在摘要正文里（例：`"ADDENDUM No. 1 to EIA-318 - ...: SUPERSEDED BY EIA-318-B, July  1996."`）。

**JEDEC 单文档页实际字段布局**（实测 `jesd-78b`）`[一手]`：
```
标题（如 IC LATCH-UP TEST）
文档号（如 JESD78F.02）        ← 大号字体
摘要
RAND 声明
Committee(s): JC-14, JC-14.1    ← 委员会字段
Free download. Registration or login required.   ← 或 "Available for purchase: $284.00 [Add to Cart]"
Published: Nov 2023             ← 注意：日期在标题上方
```

#### 1.1.4 免费 vs 付费（实测样本）

| 文档 | 获取方式 | 实测原文 |
|---|---|---|
| **JESD78F.02**（IC Latch-Up Test） | **免费，注册即可** | `Free download. Registration or login required.` |
| **JESD79-4D**（DDR4 SDRAM） | **付费 $284.00** | `Available for purchase: $284.00 [Add to Cart]` |
| JM21W（流程手册） | 免费 PDF 直接下载 | `https://www.jedec.org/sites/default/files/JM21W.pdf` |

> **`[推断]`** 付费与免费的划分，JEDEC 官网未公开成文规则。观察到的相关性（**未核实，仅作假设**）：**越是"器件规格类"（内存/接口/信号完整性，含大量参数表与 IP 声明）越可能付费；越是"测试方法类"（JESD22/47/51等方法学）越可能免费**。此规律用于**采购优先级排序**，不可作为断言写入知识 OS。

#### 1.1.5 流程与 ballot：JEDEC 官方手册（**一手证据**）

来源：`https://www.jedec.org/sites/default/files/JM21W.pdf`（JM21W，2025 年 3 月版，修订自 JM21V）｜可信度：★★★★★（JEDEC 官方发布 PDF，本次已下载并全文解析）

**文档开发程序（手册 §4）原文节选** `[一手]`：
> 1) Presentation → 2) Motion for ballot（须有附议）→ 3) 委员会编辑处理 → 4) **Committee ballot**（经 JEDEC 投票机）→ 5) Motion to Board ballot → 6) **Board ballot** → 7) **Publication** → 8) 由 JEDEC 办公室出版

**投票阈值（手册 §6.1）** `[一手]`：
> "JEDEC shall be a minimum of **2/3** of votes cast. All Board approval vote counts shall be a minimum of **3/4**"；且"**One company, one vote**"（一人一票被明确拒绝，投票按公司计）。弃权票不计入分母。

**文档复审制度（手册 §7.2）—— 这是判定现行/废止的制度依据** `[一手]`：
> "JEDEC documents shall be reviewed by the formulating committee **within five years of the last publication date**, after which the committee shall take one of the following actions:"
> a) **Reaffirm** it as a JEDEC document
> b) Recommend its **revision** and reissuance
> c) **Rescind** it from publication
> d) Recommend submittal as an ANSI or IEC document proposal

> **这条是本Track 最重要的方法论基石之一**：JEDEC 标准"看起来没更新"不代表失效——它可能处于 5 年复审期内被 reaffirmed。**知识 OS 必须记录 `last_publish_date` 并在满 5 年时打"复审窗口"标记。**

**关于 ballot 的可得性（重要负面结论）** `[一手]`：
- 手册中的 ballot 是**委员会内部投票**（Committee ballot / Board ballot），通过 "JEDEC voting machine"（`vote.jedec.org`，见 ToS 域名列表）进行。
- **JEDEC 手册中不存在"公开征求意见/ public review"阶段**——这与 ISO/IEC 体系的 CDV（Committee Draft for Vote，各国 NC 公开投票）**根本不同**。
- **结论**：**非 JEDEC 会员无法看到 JEDEC 的 ballot 草案**。任何声称"JEDEC 公开征求意见文件"的信源都应视为错误信息。
- **替代路径**：JEDEC 的 **新标准发布新闻稿**（`jedec.org/news/pressreleases`）是公开的，可作为"新版本即将发布"的**唯一可靠公开信号**。

#### 1.1.6 ⚠️ 反爬条款：对知识 OS 架构的硬约束

`[一手]` JEDEC 服务条款原文（经搜索引擎索引的官方页面原文）：
> "The JEDEC Website is intended for **human users**. **Automated bots, scrapers, or scripted tools are not permitted** to access, collect, or interact with JEDEC content. All use of the Website must be performed by real individuals..."

**本次实测佐证**：对 `www.jedec.org/document_search` 与 `/termsofuse` 发起普通 HTTP 请求均返回 **403 Forbidden**。

> **架构结论（必须写进知识 OS 的设计文档）**：
> 1. **禁止自动爬取 JEDEC**（明确违反 ToS，且技术上已被拦截）。
> 2. JEDEC 文档页 HTML 中标注 `Published JEDEC documents on this website are **self-service** and searchable directly from the homepage` —— 即官网自己声明是"人工自助"模式。
> 3. 可行替代：(a) 人工查阅并**人工录入断言 + 标注访问日期**；(b) 用§1.1.7 的授权经销商获取**带版本历史的元数据**（见下）。

#### 1.1.7 ⭐ 授权经销商：可作为 JEDEC 版本历史的**替代数据源**

虽然不能爬 JEDEC，但以下**授权经销商页面公开显示 JEDEC 文档的版本链**，且**实测提供 `Supersedes` / `Superseded by` 结构化字段**：

| 经销商 | URL 模式 | 实测输出 | 可信度 |
|---|---|---|---|
| NSAI Standards Store | `shop.standards.ie/en-ie/standards/jedec-<编号>` | `Status: Superseded` / `Superseded date: 25-08-2025` / `Superseded by JEDEC JESD47M:2025` / `Supersedes JEDEC JESD47K:2018` / `Standards Referenced By This Book` |★★★★☆（授权经销商） |
| Intertek Inform（SAI Global） | `infostore.saiglobal.com/.../<编号>` | 同类字段 + `Amended by` / `Stability Date` | ★★★★☆ |
| ANSI Webstore | `webstore.ansi.org/industry/semiconductors/tests/iec-60749` | 按系列整包列出，含会员价 | ★★★★☆ |

> **实测样本（高价值）** `[一手]`：
> ```
> JEDEC JESD47L:2022
> Status: Superseded
> Superseded date : 25-08-2025
> Superseded by   : JEDEC JESD47M:2025
> Supersedes      : JEDEC JESD47K:2018
> Standards Referenced By This Book:
>   JESD93A:2022 / JEP155B:2018(R2024) / JESD22-A111C:2025 /
>   CEI EN IEC 62506:2024 / JESD218B.03:2024 / JESD218C:2025 / JESD218C.01:2026
> ```
> **这一条同时解决了三个问题**：① 现行版本是 M不是 L；② 复审/换版时点；③ 引用关系图谱。**建议知识 OS 将此类经销商页作为 JEDEC 版本解析的 fallback 通道**（人工核对后录入）。

---

### 1.2 SEMI —— 制造与设备/材料/封装标准

#### 1.2.1 入口（实测）`[一手]`

| 用途 | URL | 可信度 |
|---|---|---|
| 标准总入口 | `https://www.semi.org/en/products-services/standards` | ★★★★★ |
| 商店（可搜索全部标准） | `https://store-us.semi.org/collections/standards/lang-english` | ★★★★★ |
| SEMIViews 订阅（有 30 天免费试用） | `https://www.semi.org/en/products-services/standards/semiviews` | ★★★★★ |
| 参与标准 ballot（**投票入口**） | `https://www.semi.org/en/products-services/standards/ballots` | ★★★★★ |
| 委员/工作组名录 | `https://www.semi.org/en/products-services/standards/member-directory` ⚠️未核实 | — |

**SEMI 官方统计** `[一手]`："more than **1,000** industry approved standards and guidelines, based on the work of more than **5,000** volunteers"。

#### 1.2.2 ⚠️ 关键修正：SEMI 的"系列字母"分类**不完整**，且与用户任务书假设不符

任务书要求"按系列字母分类浏览"。**官网实际列出的 Volume（卷）不是单一字母**，实测包含**双字母/数字前缀**系列： `[一手]`

| 官方 Volume 名 | 系列字母 | 对应 store URL slug |
|---|---|---|
| Automation Technology | A | `stdvol-automation-technology` |
| Facilities | F | `stdvol-facilities` |
| **Liquid Chemicals** | **C** | `stdvol-process-chemicals` |
| **Gases** | **C**（与上同字母卷不同卷） | `stdvol-gases` |
| **Silicon Materials & Process Control** | **MF** | `stdvol-silicon-materials-process-control` |
| **Materials** | **M** | `stdvol-materials` |
| **Packaging** | **G** | `stdvol-packaging` |
| Equipment Automation Software & Hardware | E | `stdvol-equipment-automation-software` |
| Microlithography | P | `stdvol-microlithography` |
| MEMS | MS | `stdvol-mems` |
| 3D IC | 3D | `stdvol-3d-ic` |
| Flat Panel Display | D | `stdvol-flat-panel-display` |
| Flexible Hybrid Electronics | FH | `stdvol-flexible-hybrid-electonics`（注意官网拼写有误） |
| HB-LED | HB | `stdvol-hb-led` |
| Photovoltaic | PV | `stdvol-photovoltaic` |
| Safety Guidelines | S | `stdvol-safety-guidelines` |
| Traceability | T | `stdvol-traceability` |

> **对可靠性工程师最相关的三个卷**：**G（Packaging）**、**M / MF（Materials / Silicon Materials）**、**S（Safety Guidelines）**。SEMI 官网另有一页专门汇总封装相关标准 `[一手]`（`china.semi.org.cn/article/99`）：
> ```
> Volume Packaging (G)
> G66 - Test Method for the Measurement of Water Absorption Characteristics for Semiconductor Plastic Molding Compounds
> G73 - Test Method for Pull Strength for Wire Bonding
> G79 - Specification for Overall Digital Timing Accuracy
> G96 - Test Method for Measurement of Chip (Die) Strength by Mean of Cantilever Bending
> G71 - Specification for Barcode Marking of Intermediate Containers for Packaging Materials
> G86 - Test Method for Measurement of Chip (Die) Strength by Mean of 3-Point Bending
> ```
> **`[推断]`** `G73（键合拉脱强度）` 与 `G66（注塑料吸水率）` 是封装可靠性的直接相关项，**建议纳入知识 OS 的 SEMI 侧种子集**（版本号需向store 核实）。

#### 1.2.3 SEMI 版本状态标签（**实测，一手**）

`[一手]` SEMI 商店实际使用的状态后缀（从 store HTML 中提取的真实 SKU 命名）：
```
SEMI 3D1-0519 - Inactive
SEMI 3D1-0912 - Superseded
SEMI 3D1-0912 (Reapproved 0418) - Superseded
SEMI 3D10-0814 (Reapproved 0420) - Superseded
SEMI 3D10-0814 (Reapproved 1025) - Current
```

> **这是本Track 第二个重要发现。SEMI 的命名法与 JEDEC 完全不同：**
>
> | 段 | 含义 |
> |---|---|
> | `3D10-**0814**` | 首次发布日期 **2014-08** |
> | `(Reapproved **0420**)` | **复审批准 2020-04**，内容可能已更新 |
> | `- Current` | 当前现行 |
> | `- Superseded` | 已被取代 |
> | `- Inactive` | 已停用（注意：**不等于废止**） |
>
> **⚠️ 陷阱**：`Reapproved` 后面的年月**不是**原始发布年。若知识 OS 只存一个日期字段，会把2020-04 误当出版日期。**必须拆成 `first_published` 与 `last_reapproved` 两个字段。**

#### 1.2.4 SEMI 价格（一手实测，2026-10-05）

| 文档 | 会员价 | 非会员价 |
|---|---|---|
| SEMI 3D1 ~ 3D15 系列（各册） | **$148.00** | **$193.00** |
| SEMI G92（日文版，450mm tape frame cassette） | $176.00 | $231.00 |
| SEMI 3D11（会员价示例） | $700（此条为促销上下文，⚠️需复核） | — |

- **SEMIViews 订阅**：官网提供 **30 天免费试用**（`discover.semi.org/semiviews-registration.html`），订阅后可访问全部 1000+ 标准。
- **参与标准制定免费** `[一手]`：官网原文 "Participation in SEMI International Standards is **free** to all industry stakeholders."（`semi.org/en/products-services/standards/information_and_control`）——**但注意：免费参与 ≠ 免费获取标准文本。**

#### 1.2.5 ⭐ 公开的 ballot 与新标准动态（**JEDEC 所缺、SEMI 所有的**）

`[一手]` SEMI 博客 "Technology and Trends"（`https://www.semi.org/en/blogs/technology-trends`）**公开披露 ballot 时间窗与草案编号**，实测原文：
> "The Advanced Backend Factory Integration (ABFI) Task Force will **ballot this potential subordinate standard from August 19 to September 18**. It will be adjudicated during SEMICON West from October 13-15, 2026."

以及**草案编号公开**：
> "**SEMI Draft Document 7381** proposes a subordinate standard to define maps to and from non-E142 wafer coordinate systems."

> **实操价值**：这是订阅"标准即将变化"的**最佳免费渠道**。JEDEC 不公开 ballot，SEMI 公开。**建议知识 OS 抓取（或人工跟踪）此博客的 RSS。**

---

### 1.3 IEC Webstore —— 国际标准，且**本Track 自动化价值最高**的源

#### 1.3.1 入口（实测）`[一手]`

| 用途 | URL |
|---|---|
| 商店首页 | `https://webstore.iec.ch/` |
| 标准详情页 | `https://webstore.iec.ch/publication/<数字ID>`（如 3333 = IEC 60749-1:2002） |
| **TC 项目状态页** | `https://www.iec.ch/dyn/www/f?p=103:20:<hash>`（**公开、含全部版本链**） |
| **TC 稳定性日期表** | `https://www.iec.ch/dyn/www/f?p=103:21:<hash>` |
| **阶段代码官方定义** | `https://www.iec.ch/standards-development/stage-codes` ✅ 已验证 |
| IEC 搜索结果页 | `https://webstore.iec.ch/en/searchform&q=<关键词>`（⚠️ 实测 404，检索入口形式待确认） |

#### 1.3.2 ⭐⭐ 单个标准页的三个官方 Tab（本Track 最重要的发现）

`[一手]` 实测 `https://webstore.iec.ch/en/publication/64423`（IEC 62439-3:2021）页面结构：
```
Product detail | Lifecycle | Normative references | Referenced by
```

| Tab | 内容 | 对知识 OS 的用途 |
|---|---|---|
| **Product detail** | TC、Publication type、Publication date、**Edition**、ICS、**Withdrawal date**、ISBN、Pages、File size | 版本与状态断言 |
| **Lifecycle** | 版本沿革 | 修订历史 |
| **Normative references** | 本标准**规范性引用**了哪些标准 | ✅ **出边（out-edge）自动提取** |
| **Referenced by** | 哪些标准引用了本标准 | ✅ **入边（in-edge）自动提取** |

**其他实测细节**：
- 旧版页面顶部会直接给出**继任版本链接**：`"A more recent version of this publication exists: IEC 60300-3-4:2022"` —— 这就是 IEC 版的"Superseded by"，**比 JEDEC 更容易提取**。
- 旧版页面显示 **`Withdrawal date`** 字段（例：`IEC 60300-3-4:2007` → `Withdrawal date 2022-03-11`）。
- **Consolidated Version（CSV）标记**：`IEC 61400-6:2020+AMD1:2025 CSV`，页面说明 "The content of amendment(s) is incorporated into the publication. **The track changes mode shows where the publication has been modified by the amendment.**"
- **免费但受限**：`IEC 60749-1:2002/COR1:2003`（Corrigendum 1）**售价 CHF 0.-** —— 即**勘误本身常免费**。

#### 1.3.3 ⭐⭐ 稳定性日期（stability date）—— IEC 独有概念，JEDEC/AEC/IPC 都没有

`[一手]` **官方定义来源**：ISO/IEC Directives Supplement（IEC 官方文件）
> "**The stability date shall be agreed by the committee.** It shall be included in the CDV and also in the FDIS. Upon final publication, this information shall be given on the IEC web site."
> "**Typically stability periods shall be between 3 and 12 years.**"

**实测页面形态**（`IEC 60300-3-4:2022` → `Stability date 2028`；`IEC 62439-3:2021` → `Stability date 2028`；`IEC 60749-1:2002` → `Stability date 2029`）。

**TC 级稳定性日期公开表** `[一手]`（实测可访问，TC 51 稳定性日期页共 76 条）：
```
Publication Number | Publication Date | Stability Date | Maintenance Team | Project in progress
IEC 60401-1:2020        ED2 2020-04-14    2031          WG 1
IEC 60401-1              ED3 (ACDV)         —            ← 在研项目，阶段码 ACDV
IEC 61609:1996           ED1 1996-02-07     2027
IEC 63182-2:2020         ED2 2020-09-29     2031          WG 1
```

> **实操价值（对知识 OS 极重要）**：
> 1. **stability date 就是"下次强制复审的时间点"** —— 把它作为知识 OS 的一个一等字段，可以在到期前主动提醒用户"该查新版了"。
> 2. **`Project in progress` 列会直接给出在研项目的阶段码**（如 `ED3 (ACDV)`）—— **这是提前 1–2 年发现标准要改的官方信号**。

#### 1.3.4 ⭐ 阶段代码表（判断"在研"状态的官方字典）

`[一手]` 来源：`https://www.iec.ch/standards-development/stage-codes`（已验证可访问）。节选与半导体相关的关键码：

| 码 | 含义 | 阶段（harmonized stage） |
|---|---|---|
| **PWI** | Preliminary work item | 00.00（**尚未立项实质工作**） |
| **PNW** | New work item proposal | 10.20 |
| **ACD** / **ACDV** | Approved for CD / **Approved for CDV** | 20.99 / **30.99** |
| **CD** / **CCDV** | Committee Draft / **Draft circulated as CDV** | 30.20 / **40.20** |
| **CDM** | CD to be discussed at meeting | 30.60 |
| **CFDIS** | **Draft circulated as FDIS**（最终国际标准草案） | 50.20 |
| **AFDIS** | Approved for FDIS | 40.99 |
| **APUB / BPUB / PPUB** | Approved for publication / Being published / **Publication issued** | 50.99 / 60.00 / **60.60** |
| **DEL** | Deleted / abandoned | 10.98 |
| **DELPUB** | **Deleted publication** | 99.60 |
| **WPUB** | **Publication withdrawn** | 95.99 |
| **MERGED** | **Publication merged with EN version**（被欧洲采标版合并） | 35.97 |
| **TCDV / TPUB** | Translation of CDV / publication | 40.00 / 60.00 |

**在研项目编号格式** `[一手]`（ISO/IEC Directives Supplement 原文）：
> "EXAMPLE Document **18/21/CD** is the 21st document for circulation in IEC/TC 18"
> 格式 = `TC号/序号/文件类型`。**该编号在 CD、CDV、FDIS 直至发布后保持不变。**

**实测的 TC 47（Semiconductor devices）版本链** `[一手]`（原文明示）：
```
IEC 60749-1:2002              ED1   PPUB    Publication issued          U
IEC 60749-1:2002/COR1:2003    ED1   PPUB    Publication issued          U
IEC 60749-1:1983              ED1   DELPUB  Deleted publication         U
IEC 60749:1996+AMD1:2000+AMD2:2001 CSV ED2.2 WPUB Publication withdrawn U
47/1394/FDIS   IEC 60749:1996/AMD1:2000  ED2  WPUB
47/1522/CC     IEC 60749/FRAG1  ED3  MERGED  Fragment merged  82 kB
47/1523/CC     IEC 60749/FRAG2  ED3  MERGED  Fragment merged  151 kB
```
> **对本用户直接相关的情报**：`IEC 60749`（半导体机械与气候试验方法，功率封装的核心国际标准族）**正在被"完整更新"（complete update）**，分FRAG1/FRAG2 两个片段推进，阶段已到 MERGED。**这意味着 60749-1:2002 这个用了 24 年的老版正在被替换 —— 知识 OS 必须现在就把"60749 全族正在换版"作为高优先级跟踪项。**

#### 1.3.5 ⚠️ `IEC 60749-1:2002` 上发现的一处状态矛盾（记录留痕）

`[一手]` **不同渠道对同��文档给出不同的 Stability Date**：

| 来源 | Stability Date | 可信度 |
|---|---|---|
| webstore.iec.ch（本次实测） | **2029** | ★★★★★ |
| SAI Global（infostore） | `Stability Date: 2021. (11/2017)` | ★★★★☆ |

> **判定**：以 **IEC 官网为准（2029）**。SAI 的 2021 是**旧数据残留**（其页面仍标`Status: Current`，未同步）。
> **方法论教训**：**授权经销商的元数据会滞后**，只能作为 JEDEC/付费墙内容的 fallback，**不能作为版本状态的权威源**。这与 §1.1.7 的"经销商替代方案"形成边界——**经销商可用于"发现存在新版"，但不可用于"断言当前状态"**。

---

### 1.4 AQG（ECPE 持有）—— 功率模块车规核心，且**全文免费**

`[一手]` 官方页：`https://www.ecpe.org/research/working-groups/automotive-aqg-324/`

**官网实测事实**：
- AQG 324 工作组 **2017 年 6 月成立**，基于**德国 LV 324** 制定。
- 由**30+ 家 ECPE 成员企业**（汽车供应链）组成的工作组发布。
- **明确的组织沿革（对知识 OS 极重要）**：
  > "**Based on the former German LV 324**"
- 页面明示范围：机动车 **≤3.5t** PCU 中使用的功率电子模块。
- **公开列出的可下载版本（完整版本史）**：
  | 版本 | 日期 |
  |---|---|
  | V01.05 | 2018-04-12（首发） |
  | 02.1 | 2019-05-15 |
  | 03.1 | 2021-05-31 |
  | **04.1** | **2025-04-24**（当前） |
- 另有 Intro-presentation（2018-04-12）与 Press note（2018-04）可下载。
- ECPE 同时运作 **"Power Semiconductor Reliability for Railway Application"** 工作组（轨道应用，与 AQG 324 并列）。

> **`[推断]` 版本号格式 `04.1/2025`= 第 4 版第 1 次修订/2025 年。** 与 JEDEC 的 `F.01` 后缀逻辑不同，**不要用同一解析器**。

> **⚠️ 访问提示** `[实测]`：`https://ecpe.org/standards/aqg-324` → **404**。正确路径是上面的 `/research/working-groups/automotive-aqg-324/`。另外 `www.aqg-324.org` 域名 **DNS 不解析**。

> **`[推断]` AQG 324 全文为 CC BY-ND 免费**（来自 Track 04 调研结论）。本Track 未独立复核该许可条款，**标注为待复核**。

---

### 1.5 AEC（aecouncil.com）—— 车规资格，**全文免费下载，无注册**

#### 1.5.1 ⚠️ 访问陷阱（实测，重要）

`[实测]`
| URL | 结果 |
|---|---|
| `https://www.aecouncil.com/AECDocuments.html` | **连接失败（000）** |
| `http://www.aecouncil.com/AECDocuments.html` | **200✅** |
| `https://www.aecouncil.com/` | 连接失败 |

> **AEC 官网只支持 HTTP，不支持 HTTPS。** 知识 OS 的抓取配置需保留 HTTP 回退，否则会误判为"站点不可用"。

#### 1.5.2 ⭐ 完整一手文件清单（本次实测抓取，2026-10-05）

来源：`http://www.aecouncil.com/AECDocuments.html` ｜可信度：★★★★★（一手官网）

**基础文件（base documents）与其现行版本：**

| 文件 | 现行版本 | 下载路径 | 适用范围 |
|---|---|---|---|
| **AEC-Q100** | **Rev J1** | `files/Documents/AEC Q100-Rev J1.pdf` | 集成电路（Failure Mechanism Based Stress Test Qualification For Integrated Circuits） |
| **AEC-Q101** | **Rev E** | `Documents/AEC_Q101_Rev_E_Base_Document.pdf` | 分立器件 |
| **AEC-Q102** | **Rev A** | `Documents/AEC-Q102_Rev_A.pdf` | 光电器件 |
| **AEC-Q103** | Rev A（-002） | `Documents/AEC_Q103-002_Rev_A.pdf` | 微机电（MEMS） |
| **AEC-Q104** | **Rev A** | `files/Documents/AEC-Q104 - Rev A.pdf` | 多芯片模块（MCM） |
| **AEC-Q200** | **Rev E** | `Documents/AEC_Q200_Rev_E_Base_Document.pdf` | 无源元件 |

**对本用户最相关的分册（功率/封装直接相关）：**
```
AEC-Q101-001 - Rev-A: Wire Bond Shear Test
AEC-Q101-003 - Rev-A: Wire Bond Shear Test
AEC-Q101-004 - Rev- : Miscellaneous Test Methods
AEC-Q101-005 - Rev-A: Charged Device Model (CDM) Electrostatic Discharge Test
AEC-Q101-006 - Rev- : Short Circuit Reliability Characterization of Smart Power Devices
AEC-Q100-001 - Rev-C: Wire Bond Shear Test
AEC-Q100-010 - Rev-A: Solder Ball Shear Test
AEC-Q100-011 - Rev-D: Charged Device Model (CDM) ESD Test
AEC-Q100-012 - Rev- : Short Circuit Reliability Characterization of Smart Power Devices
```
> **`[推断]` 高价值情报**：功率半导体短路可靠性（Short Circuit Reliability Characterization）在 AEC 中同时存在于 **Q101-006（分立）** 与 **Q100-012（集成）**。这是功率器件专属应力，**在 JEDEC JESD22 中没有直接对应方法** —— 是知识 OS 必须补的独立节点。

**方法论类文件（Q0xx）：**
```
AEC-Q001 Rev-D  : Guidelines for Part Average Testing
AEC-Q002 Rev-B  : Guidelines for Statistical Yield Analysis
AEC-Q003 Rev-A  : Guidelines for Characterizing the Electrical Performance of Integrated Circuits
AEC-Q004 Rev-   : Automotive Zero Defects Framework
AEC-Q005 Rev-A  : Pb-Free Test Requirements
AEC-Q006 Rev-B  : Qualification Requirements for Components using Copper (Cu) Wire Interconnection
AEC-Q007 Rev-   : Failure Mechanism Based Testing Guidelines for Components
AEC-Q007-001    : Board-Level Reliability Temperature Cycling Test Method
AEC-Q007-002    : BLR Spreadsheets (xlsx)
```
> **`AEC-Q006`（铜线互连）`AEC-Q007`（板级可靠性）`AEC-Q007-002`（BLR 电子表格）** 是功率封装/模块的关键项，**且 Q007-002 是可直接下载的 xlsx 计算模板** —— 建议知识 OS 单独标注为"可用工具"。

**附带的可下载表单模板（对做资格报告极实用）** `[一手]`：
```
AEC-Q100 Rev A - CDC Template (Certificate of Design and Construction)  .xlsx
AEC-Q100 Rev H - QTP Template (Qualification Test Plan)                   .doc
AEC-Q102 Rev A - CDC / QTP / Data Presentation Templates                .xlsx/.docx
AEC-Q103-002 Rev A - CDC Template                                        .xlsx
AEC-Q104 Rev A - QTP Template                                            .docx
AEC-Q102-003      - Combined QTP-Data-Superset + Requalification Matrix .xlsx
AEC Charter Rev H                                                         .pdf
```

> **AEC 生态的辅助页面**：`AECRequest.html`（技术委员会申请）、`AECHistory.html`、`AECWorkshop.html`、`AECLinks.html`、`AECPapers.html`。

---

### 1.6 IPC（现已更名 "Global Electronics Association"）—— 板级与互连

#### 1.6.1 ⚠️⚠️ 重大品牌变更（直接影响知识 OS 的 URL 与实体识别）

`[一手]`实测确认：
- IPC 的法律实体已变更为 **IPC International Inc, DBA Global Electronics Association**（可从 `ipc.org` 首页页脚读到）。
- **域名迁移**：`ipc.org` → `electronics.org`（`https://www.ipc.org/Status` 会 302 到 `https://www.electronics.org/Status`）。
- **实测失效 URL**（记录以免知识 OS 写错）：
  ```
  https://www.ipc.org/standards                → 404
  https://www.electronics.org/standards         → 404
  https://www.electronics.org/standards-documents → 404
  https://www.electronics.org/publications      → 404
  ```
- **实测可用 URL**：
  ```
  https://www.electronics.org/ipc-standards      → 200✅
  https://www.electronics.org/test-methods      → 200✅
  https://www.electronics.org/search            → 200✅
  https://shop.ipc.org/                          → 商店（返回202，需 JS）
  https://www.ipc.org.cn/                        → IPC 中国官网
  ```
- ⚠️ `https://www.electronics.org/Status`（Status of Standardization）**本次 WebFetch 返回空内容**，仅经搜索索引见到其表格内容。**该页是IPC 唯一的 ballot 公开页，标记为"存在但本次未成功直取"**。

> **知识 OS 应对**：把组织实体建模为 `{id: "IPC", current_name: "Global Electronics Association", dba, primary_domain: "electronics.org", legacy_domain: "ipc.org"}`，并保留 IPC 编号前缀不变（`IPC-9701`、`J-STD-001` 仍是有效标识）。

#### 1.6.2 ⭐ 唯一公开的 ballot 页（IPC 特色）

`[一手]` **Status of Standardization** 页含三张表：
| 表 | 内容 |
|---|---|
| **Published Standards** | 标准号、标题、发布日期 |
| **Translations** | 翻译状态 |
| **Proposed Standard for Ballot** | **正在投票的标准（公开！）** |

**实测抓到的 ballot 清单节选（对本用户直接相关）** `[一手]`：
```
IPC-9704B   Printed Circuit Assembly Strain Gage Test Guideline
IPC-9702A   Monotonic Bend Characterization of Board-Level Interconnects
IPC/JEDEC-9702A  Monotonic Bend Characterization of Board-Level Interconnects
IPC-6012FAm1 Qualification and Performance Specification for Rigid Printed Boards
IPC-9691C   User Guide for the IPC-TM-650, Method 2.6.25 Conductive Anodic Filament (CAF) Testing
IPC/WHMA-A-620F-S Space and Military Applications Addendum
```

> **`[推断]`** `IPC/JEDEC-9702` 是 JEDEC 与 IPC 的**联合标准**，出现在 IPC 的 ballot 表里。**这意味着"哪些是 JEDEC 标准"不能只看JEDEC 官网** ——联合标准（`J-STD-xxx`、`IPC/JEDEC-xxxx`）需同时查两边。这是一个**知识 OS 容易漏建的边**。

#### 1.6.3 IPC-TM-650 测试方法（**免费**）

`[一手]` IPC 中国官网（`ipc.org.cn`）明示：
> "最新的测试方法可从 **https://www.electronics.org/test-methods** 免费下载"

> **`[推断]`** 抽样验证了这条二手转述：`electronics.org/test-methods` 返回 200，但本次 WebFetch 未取到正文（JS 渲染）。**"IPC-TM-650 免费下载"这一说法在本Track 标为 `[二手·待一手复核]`**。若知识 OS 依赖它，建议人工打开该页确认一次。

#### 1.6.4 IPC 商店与"Amendment"产品类型（**对版本管理有独特价值**）

`[一手]` `https://shop.ipc.org/standards/standard-amendments` 实际展示了 IPC 的一个**其他组织都没有的产品概念**：

| 产品类型 | 说明 |
|---|---|
| **Standard with amendment(s)** | 把base + 修正合成一册 |
| Errata | 勘误 |
| **Redline** | 红线对比版 |
| Amendment | 单项修正 |
| **Annotated Comparison / Addendum with amendment(s)** | 带批注的对比 |

**实测样本** `[一手]`：
```
IPC-9702 - Standard with Amendment 1   Monotonic Bend Characterization of Board-Level Interconnects
  "IPC brings this version to industry to minimize confusion for those using both documents"
IPC-CC-830 Revision B - Standard with Amendment 1  Qualification and Performance of Electrical Insulating
  Insulating Compound for Printed Wiring Assemblies
  "Amendment 1 updates include new qualification, retention and conformance inspection requirements for FTIR, MIR and hydrolytic..."
```
> **对知识 OS 的价值**：IPC 的"合成版"意味着**同一标准可能存在 base / amendment / consolidated 三种并行流通形态**。若不做版本归一，两个实验室用"同一份IPC-CC-830"可能实际执行不同内容。**必须在版本模型中显式支持"合成版"这一形态。**

---

### 1.7 中国：国标平台

#### 1.7.1 两个平台的分工（实测，这是最容易搞混的地方）

| 平台 | URL | 定位 | 实测 |
|---|---|---|---|
| **国家标准全文公开系统** | `https://openstd.samr.gov.cn/bzgk/gb/` | **全文**公开 | 200✅ |
| **全国标准信息公共服务平台** | `https://std.samr.gov.cn/` | **信息汇总 + 各类标准目录** | 200✅ |

#### 1.7.2 ⭐⭐ openstd 的免费权限规则（本Track 对"免费/付费"最关键的一条）

`[一手]` **官网原文**（2026-10-05 实测快照）：

| 标准类别 | 总数 | 非采标 | 采标 |
|---|---|---|---|
| **GB 强制性国标** | 2,031 | 1,691 项**可在线阅读和下载** | 340 项**只可在线阅读** |
| **GB/T 推荐性国标** | 47,164 | 31,144 项**可在线阅读和下载** | 16,020 项**只提供标准题录信息** |
| **GB/Z 指导性技术文件** | 742 | 283 项可读可下 | 459 项仅题录 |
| **国家标准外文版** | 2,638 | — | — |

**"采标"= 采用国际/国外标准（等同或修改采用 IEC/ISO）**。

**法律依据** `[一手]`（市场监管总局人大建议答复原文）：
> "《中华人民共和国标准化法》第十七条规定：'**强制性标准文本应当免费向社会公开。国家推动免费向社会公开推荐性标准文本**'"

**官方对"为什么采标不给下载"的解释** `[一手]`：
> "涉及**版权保护**的标准文本，可在中国标准服务网购买由中国标准出版社等相关单位出版的标准文本。"
> "采用国际国外标准的国家标准因涉及版权问题，只提供免费在线阅读服务，不提供下载打印等。"

> **对知识 OS 的直接含义（极其重要）**：
> 1. **想要 GB/T 中 IEC 转化标准的全文，往往拿不到** —— 不是检索失败，是版权设计。
> 2. **策略**：查中国标准时，**先查对应IEC 原文（IEC 官方源）**，GB/T 只作"是否有中国转化版+转化程度（IDT/MOD）"的元数据。
> 3. ⚠️ **陷阱**：`GB/T xxxxx` 的 **采标程度（IDT/MOD）会改变技术内容**。MOD（修改采用）可能删改了条款，**不能假定 GB/T ≡ IEC**。

#### 1.7.3 std.samr.gov.cn 的七类标准 + 独有栏目（实测）

`[一手]` 平台覆盖：国家标准、行业标准（76 个行业，88,734 项）、地方标准（50,751 项）、团体标准、国际标准（ISO/IEC 标准查询）、国外标准（ANSI/CEN/DIN/BSI/SA/NZS/KATS）、企业标准。

**⭐ 本Track 最有用的两个独有栏目**：
```
https://std.samr.gov.cn/gb/gbPlanDraft      推标草案征求意见   ← 公开征求意见！
https://std.samr.gov.cn/gb/gbqSuggestion    强标草案征求意见   ← 公开征求意见！
https://std.samr.gov.cn/gb/withdrawnReview  国家标准复审结论公示
https://std.samr.gov.cn/gb/gbOpinion        国家标准实施信息反馈
https://std.samr.gov.cn/gb/gbSuggestionPlan 拟立项标准公示
```

> **`[推断]` 这是本次调研中唯一找到的"标准草案公开征求意见"官方入口**（对比：JEDEC 无、SEMI 仅在博客披露 ballot 时间）。中国的国标过程信息公开度显著高于 JEDEC/IEC。**若知识 OS 需要"提前预警即将发布的标准"，中国平台的这两个栏目是当前唯一可用的公开源**（尽管与半导体可靠性直接相关的国标很少）。

>⚠️ **`[二手]`** 有资料称该平台提供 IEC/ISO 标准查询（`std.samr.gov.cn/gj/std?op=IEC`）**但仅限"目录信息"**（与"购买国际标准"链接 `sacinfo.cn` 并列）。**IEC 全文仍须上 webstore.iec.ch。**

---

### 1.8 军标：MIL-STD 原文的免费获取（**且有一个大坑**）

#### 1.8.1 官方源与可达性（实测，2026-10-05）

| 源 | URL | 实测 | 性质 |
|---|---|---|---|
| **DLA ASSIST** | `assist.dla.mil` / `quicksearch.dla.mil` | **本次连接失败（000）**，疑为地域/网络限制 | ★★★★★ 官方第一源 |
| **NASA NTRS** | `ntrs.nasa.gov` | **403（反爬）**；API 亦 403 | ★★★★★ 官方 |
| **NASA NEPP** | `nepp.nasa.gov` | **200✅** | ★★★★★ 官方 |
| **NASA SSRI 知识库** | `s3vi.ndc.nasa.gov/ssri-kb/static/resources/` | **200✅ 可直接下载 PDF** | ★★★★☆ 官方镜像 |
| everyspec / everypec | `everyspec.com` | **403** | ★★ 商业聚合 |

> **建议的免费获取顺序**：① 试 DLA ASSIST（若可访问）→ ② NASA NTRS 检索 → ③ NEPP / SSRI 直链。

#### 1.8.2 ✅ 实测成功下载的免费 MIL-STD-883

```bash
curl -L "https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/std883.pdf"   # 459,166 bytes, 28 页
```
**解析出的扉页原文** `[一手]`：
```
MIL-STD-883L     16 September 2019     SUPERSEDING MIL-STD-883K w/CHANGE 3 (3 May 2018)
DEPARTMENT OF DEFENSE / TEST METHOD STANDARD / MICROCIRCUITS
AMSC N/A    FSC 5962
DISTRIBUTION STATEMENT A.  Approved for public release. Distribution is unlimited.
本标准经 DLA Land and Maritime (Columbus, OH) 主管，联系邮箱 STD883@dla.mil
建议通过 https://assist.dla.mil 核实现行版本
```

**NEPP 镜像（已验证 200，4,539,862 bytes）**：
```
https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf   → 708 页
```

#### 1.8.3 ⚠️⚠️ 军标最大的坑：**MIL-STD-883 是一个"伞"**

`[一手]` **MIL-STD-883L 扉页原文（本次解析所得）**：
> "This **entire test method standard has been revised**. This revision has been issued in **six parts**: the basic test method standard (this document) and five numbered parts. This was done in order to provide flexibility in the use and the updating of the test methods."
>
> | 分册 | 内容 |
> |---|---|
> | **MIL-STD-883** | Test Methods For Microcircuits（**基本标准，28 页**） |
> | **MIL-STD-883-1** | Environmental Test Methods For Microcircuits |
> | **MIL-STD-883-2** | Mechanical Test Methods For Microcircuits |
> | **MIL-STD-883-3** | Electrical Test (Digital) Methods |
> | **MIL-STD-883-4** | Electrical Test (Linear) Methods |
> | **MIL-STD-883-5** | Test Procedures For Microcircuits |

> **实测对照**：NASA SSRI 镜像 = **28 页**（只含总纲+方法索引），NEPP 镜像 = **708 页**（含全部环境方法正文）。
>
> **结论**：**你手上那份 459KB 的 PDF 不含任何方法的测试条件正文。** 网络上大量"MIL-STD-883 免费 PDF"链接指向的是28 页总纲。**知识 OS 必须把6 个分册建成独立文档实体，否则"拿到了883"这个断言是假的。**
>
> 883L 总纲中可见的方法索引（部分，已实测提取）：`1001 气压(高度) / 1002 浸入 / 1003 绝缘电阻 / 1004.7 湿热 / 1005.11 稳态寿命 / 1006 间歇寿命 / 1007.1  agrees life / 1008.2 稳定烘烤 / 1009.8 盐雾 / 1010.9 温度循环 / 1011.9 热冲击 / 1012.1 热特性 / 1013 露点 / 1014.17 密封 / 1015.12 老化burn-in / 1017.3 中子辐照 / 1018.10 内部气体分析 / 1019.9 电离辐射(总剂量) …`

---

## 2. 付费数据库与标准购买渠道

### 2.1 价格量级（实测，2026-10-05）

| 渠道 | 对象 | 实测价格 | 备注 |
|---|---|---|---|
| **IEC Webstore** | IEC 标准（单份） | **CHF 260.-**（IEC 60300-3-4:2007 实测） | **勘误常免费**（COR1 = CHF 0.-） |
| **ANSI Webstore** | IEC 采标为 ANSI 的版本 | **$33 / $66**（IEC 60749-1 实测 $33；60749-3/4 实测 $66）；**Full ANSI Member Price $26.40 / $52.80（8折）** | 明显比 IEC 官网便宜 |
| **Intertek Inform（SAI Global）** | IEC 等 | **£18.11**（IEC 60749-1:2002 实测） | 最低价区间 |
| **en-standard.eu** | IEC | **21.60 EUR**（IEC 60749-1 实测） | 便宜 |
| **JEDEC 官方商店** | JEDEC 部分文档 | **$284.00**（JESD79-4D 实测） | 走 `jedec.dpdcart.com` |
| **SEMI 商店** | SEMI 标准 | **会员 $148 / 非会员 $193**；部分 $176/$231 | 3D 系列实测 |
| **Techstreet / Accuris** | 跨出版商 | IEEE 754-2019 **$114**；IEEE 519-2022 **$63**；ISO 9001:2026 **$279**；ISO 9000:2026 **$369**；ASHRAE 62.1 **$140** | 单份PDF 约 **$60–370** |
| **IEEE 会员价** | IEEE 标准 | 约 **8折**（IEEE 1906.1.1-2020：`$171.00` → 会员 `$137.00`） | — |

> **价格量级结论（供用户决策）**：
> - **单份 IEC/JEDEC/SEMI 标准：约 $20–290**（IEC 最便宜，JEDEC 规格类最贵）
> - **"买全"不现实**（60749 有 42 个 part）→ **优先买 AQG 324（免费）+ JEDEC（免费注册）**
> - **订阅**：SEMIViews 有 **30 天免费试用**；Techstreet Enterprise 为报价制（未公开价格，⚠️未核实）

### 2.2 各渠道定位对比

| 渠道 | 强项 | 弱项 |
|---|---|---|
| **IEC Webstore** | 唯一权威；含 Normative/Referenced-by tab；含阶段码 | 单份偏贵；中文支持弱 |
| **ANSI Webstore** | **有按标准的引用图谱页**（见 §2.3）；会员 8 折 | 只卖 ANSI 采标版，非采标部分可能没有 |
| **Intertek Inform / SAI Global** | 元数据含 `Amended by` / `Stability Date` / 国际采标关系链 | **元数据会滞后**（§1.3.5 实测矛盾） |
| **JEDEC 官方** | 权威 | 部分付费；**反爬** |
| **SEMI 官方** | 权威；价格透明；Reapproved 状态清晰 | 需付费或订阅 |
| **Techstreet / Accuris** | 跨出版商聚合 + Redline + 版本追踪告警 | **是 reseller，非权威源** |
| **BSI / IET / UL / DIN** | 欧洲/UL 采标版 | ⚠️ 本Track **未核实其具体价格与半导体标准覆盖**，仅在 std.samr.gov.cn 的"国外标准化"入口确认其存在 |

> **策略建议（基于实测）**：
> **元数据用官方站（IEC/JEDEC/SEMI）→ 需要低价全文用 ANSI/Intertek → 需要 Redline 与版本告警用 Techstreet。永远不要用 reseller 断言"当前版本"。**

### 2.3 ⭐ ANSI Webstore：一个被低估的高价值免费元数据源

`[一手]` 实测 `https://webstore.ansi.org/industry/semiconductors/tests/iec-60749`（IEC 60749 全系列页）：

- **按系列整包列出 42 个 part**，每个都带**完整摘要 + "significant technical changes" 段落**。
- **实际给出了修订原因**，例：
  > "IEC 60749-3:2017(E) … significant technical changes with respect to the previous edition: a) reference to the need for ESD protection; b) **inclusion of information on the phenomenon of tin whiskers**; c) inclusion of an optional report form/checklist."
  > "IEC 60749-4:2017(E) … a) clarification of requirements on temperature, relative humidity and duration detailed in Table 1; …"
- 同时提供**RvL（Redline Version）**说明："IEC 60749-5:2023 is available as … **RLV** which contains the International Standard and its Redline version, showing all changes of the technical content compared to the previous edition."

> **价值**：**免费**就能读到"上一版改了什么"，这是**版本差异分析的捷径**，比买两份 PDF 对比高效得多。建议知识 OS 抓取这些 "significant technical changes" 段落作为版本演进说明。

---

## 3. 制造商与行业的一手引用源（"标准被实际采用"的证据）

### 3.1 ⭐ 芯片原厂 qualification report —— 最高价值的一手引用证据

#### 3.1.1 找到的实测样本（Infineon，免费公开 PDF）

`[一手]` **已实测可访问、可直接下载的 Infineon 资格报告**：
| 产品 | URL | 体系 |
|---|---|---|
| IRFS7437-7p | `infineon.com/assets/row/public/documents/24/316/infineon-irfs7437-7p-productqualificationreport-en.pdf` | JEDEC + AEC |
| BSS816NW | `.../infineon-bss816nw-productqualificationreport-en.pdf` | **AEC-Q101** |
| 1EDN7116U | `infineon.cn/.../infineon-1edn7116u-productqualificationreport-en.pdf` | **JEDEC** |
| ISP16DP10LMA | `infineon.cn/.../infineon-isp16dp10lma-productqualificationreport-en.pdf` | **AEC-Q101** |

> **URL 规律（实测）**：`https://www.infineon.com/assets/row/public/documents/<YY>/<NNN>/<part>-productqualificationreport-en.pdf`。**注意 `.cn` 与 `.com` 域名的 assets 路径相同** —— 说明同一份文档双域可访问。**`24/316` 这类数字目录不固定，不能靠构造，必须从产品页找链接。**

#### 3.1.2 ⭐ 实测提取：Infineon 报告的标准引用结构（**这是"标准被实际采用"的最佳一手证据**）

`[一手]` **ISP16DP10LMA 报告原文节选（功率分立器件，与用户工作最接近）**：

> "Qualified according to **AEC Q101** and assessed as PASS"
>
> **Electrical Stress Test Results:**
> | Test | Abbr. | Condition | Standard cited |
> |---|---|---|---|
> | High Temperature Reverse Bias | HTRB | Ta=150/175°C, VDS=VDS,max, 1000h | **JESD22 A108** |
> | High Temperature Gate Bias | HTGB | Ta=150/175°C, VGS≥±80% VGS,max | **JESD22 A108** |
> | High Humidity High Temperature Reverse Bias | H3TRB | Ta=85°C RH=85% | **JESD22 A101** |
> | **Intermitted Operational Life Test** | IOL | ΔT=100K, 15000 cyc | **MIL-STD 750 / Meth.1037** |
> | ESD (HBM) | HBM | — | **JESD22-A114** |
> | ESD (CDM) | CDM | C3 (>1000V) | **JESD22-C101** |
>
> **Environmental:** PC = **J-STD020/JESD22 A113**；SHR = **JESD B-106**；TC = **JESD22 A104**；AC/UHAST = **JESD22 A102** 或 **JESD22 A118**；HTSL = **JESD22 A103**
> **Mechanical:** PD = **JESD B-100**；SD = **J-STD-002**
> 注释原文：`*For SMD devices reliability stress tests are performed after preconditioning test (PC) according to JESD22`

**从这份报告能提取的 5 个高价值情报**：

| # | 情报 | 价值 |
|---|---|---|
| 1 | **厂商报告引用标准时只写 `JESD22 A108`，无连字符、无点、无版本号** | 知识 OS 的正则必须容忍 `JESD22A108` / `JESD22-A108` / `JESD22 A108` 三种写法 |
| 2 | **同一份报告里 HTRB 和 HTGB 都引"JESD22 A108"** | ⚠️ 见下方陷阱 |
| 3 | **`MIL-STD 750 / Meth.1037`（间歇工作寿命 IOL）在 JESD22 中无对应** | 军标体系在民标体系之外的独立节点 |
| 4 | **`AC` 与 `UHAST` 用"或"并列**（A102 或 A118 二选一） | 实证了"同一应力可由不同标准满足"，知识 OS 不应强制单一映射 |
| 5 | **报告固定结构**：三张表（Electrical/Environmental/Mechanical）+ Notes + 免责声明 | 可作为解析模板 |

#### 3.1.3 ⚠️ 实测发现的厂商报告错误（**知识 OS 必须知道的"权威也会错"**）

`[一手]` **BSS816NW 报告原文**：
```
High Temperature Reverse Bias   JESD22 A108   HTRB   Ta=150/175°C  VDS=VDS,max   1000h
High Temperature Gate Bias      JESD22 A108   HTGB   Ta=150/175°C  VGS≥±80%    1000h
```

> **但 JESD22-A108 的官方标题是 "Temperature, Bias, and Life Test (TBL)"**（见 Track 06 已核实）。
>
> **分析**：A108 是**带偏置的温度寿命试验**，其应力类型（温度+偏置+时间）确实可以覆盖 HTRB/HTGB 的**应力类型**，但：
> 1. **A108 不含 HTRB/HTGB 各自的特定参数定义**（漏电流判据、栅压偏置条件）；
> 2. **业界通用映射是 HTRB→JESD22-A108（作为 TBL 类）或A109/Qualification 语境下的其他方法**，各家不一；
> 3. Infineon 自己在 Notes 里写 `** Specifically used stress temperature is according to product capability`。
>
> **结论（重要方法论）**：**厂商资格报告是"标准被采用"的一手证据，但不是"标准内容"的一手证据。** 知识 OS 必须**把"厂商引用了某标准"和"该标准规定了什么"建成两个独立断言**，绝不能从前者推断后者。
> `[推断]` 同一份报告的 Notes 里还有 `****ESD classification calculated based on an empirical model extracted per technology or package` —— **说明连"ESD 等级"都不是标准直接给出的，是厂商内部模型推的。**

#### 3.1.4 Infineon datasheet 内的引用（另一类一手源）

`[一手]` IM64A130A（MEMS 麦克风）datasheet 第 15 页 "Reliability specifications" 表实测内容（来源为第三方镜像，**原 PDF 未直接核实，标 `[二手]`**）：
> "Table 10 **Qualification tests according to AEC-Q103-003**"，逐项列出 THB/THS/TC/HTSL/HTOL/ELFR/MS/VFV/DROP/EMC/ESD，并**同时给出 JEDEC/IEC/SAE 平行标准**：
> ```
> THB   JESD22-A101
> TC    JESD22-A104
> HTSL  JESD22-A103
> HTOL  JESD22-A108
> ELFR  AEC Q100-008
> MS    JESD22-B104
> VFV   JESD22-B103
> DROP  AEC Q103-003
> HTC   AEC Q103-003, JESD22-A108, IEC 60068-2-38   ← 三个标准并列引用
> LTOL  JESD22-A108, IEC 60068-2-2, Test-AA         ← 三个标准并列引用
> LTS   JESD22-A119, IEC 60068-2-2, Test-AA
> HBM   AEC Q100-002
> CDM   AEC Q100-011
> Latch-up AEC Q100-004
> EMC   SAE J1752/3
> ```
> **情报**：datasheet 常**并列引用 2–3 个体系（JEDEC + IEC 60068 + AEC）**，这正是"标准被实际采用"的横向映射证据。

#### 3.1.5 其他原厂（本Track 未逐一核实，标注为待办）

| 厂商 | 已知入口 | 状态 |
|---|---|---|
| **STMicroelectronics** | ST 官网 "Quality & Reliability" 页面提供 PCN 与qualification 声明 | ⚠️ **未核实**具体 URL |
| **TI** | TI 可靠性报告（Reliability Report）随产品发布，含 JESD 引用 | ⚠️ **未核实** |
| **onsemi** | onsemi 官网 "Quality & Reliability" / AEC-Q101 声明 | ⚠️ **未核实** |
| **Mitsubishi / Rohm / Fuji / Toshiba** | 同类| ⚠️ **未核实** |
| **Semikron Danfoss** | 模块级qualification，**极可能引AQE 324 而非 AEC** | ⚠️ **未核实**，**高优先级待办** |

> **待办说明**：本Track 因时间限制仅对Infineon 做了实测下载验证。其余厂商的入口结构**未核实，知识 OS 不得凭猜测写入 URL**。

### 3.2 车规 Tier1 / OEM 技术要求中的标准引用

#### 3.2.1 LV 324（德国车规，已被 AQG 324 继承）

`[一手]` **LV324 的测试矩阵（来自 IEEE CPMT/SVC 官方演讲 PDF，semiengineering 未验证但来源为 IEEE ewh官方域）**：
> 来源：`https://ewh.ieee.org/soc/cpmt/presentations/cpmt1704a.pdf`（IEEE Santa Clara Valley Chapter, CPMT，2017-04-27）｜可信度：★★★★☆（IEEE 官方域托管的技术演讲）

**LV324 = AQG 324 的前身** `[一手]`（ECPE 官网："Based on the former German LV 324"）

**LV324 四类测试分组（这是 AQG 324 的骨架，功率封装的核心知识）** `[一手]`：
| 组| 内容 | 具体项目 |
|---|---|---|
| **QM** | 模块测试 | 栅参数、额定/反向电流、导通电压、X-ray、SAM/SAT、IPI/VI、OMA |
| **QC** | 特性化测试 | QC-01 寄生杂散电感 Lp；QC-02 热阻 Rth；QC-03 短路容量；QC-04 绝缘测试；QC-05 机械数据 |
| **QE** | 环境测试 | QE-01 热冲击(TST)；QE-02 可接触性(CO)；QE-03 振动(V)；QE-04 机械冲击(MS) |
| **QL** | 寿命测试 | **QL-01 功率循环(PCsec)**；**QL-02 功率循环(PCmin)**；QL-03 高温存储(HTS)；QL-04 低温存储(LTS)；**QL-05 高温反向偏置(HTRB)**；**QL-06 高温栅极偏置(HTGB)**；**QL-07 高温高湿反向偏置(H3TRB)** |

> **`[推断]` `PCsec` 与 `PCmin` 的区分是功率模块可靠性的核心** —— 秒级功率循环（开关损耗主导，考核键合线/铜线/烧结层）与分钟级功率循环（导通损耗主导，考核焊层/TIM）**应力物理完全不同**。这个区分在 JEDEC/IEC 体系里**没有对应方法**。

**LV324 的组织谱系（来自 IEEE 演讲图的实测提取）** `[一手]`：
```
ZVEI-ECPE Team Power Electronics → LV324 / LV324 Lifetime
                ↓
  DC-Link Film C → OEMs (5 German carmakers) → 1st Tier (3 German subsystem suppliers)
                              → 2nd Tier (3 Power Modules / 6 DC-Link)
```
`[推断]` 与中文资料称"LV324 由奔驰/宝马/大众等5 家德系车企主导"一致，**但 5 这个数字来自 IEEE 演讲图，可信度较高**。

#### 3.2.2 ⭐ AQG 324 的引用标准清单（**实测获得，功率封装最核心的一张表**）

`[一手]` AQG 324 的分测试组引用标准（来源为第三方转载的中文技术文档，**标注 `[二手]`，但与 §3.2.3 的 AQG 324 官方下载互为印证，**建议以官方 PDF 复核**）：

| 测试组 | 引用标准 |
|---|---|
| **QM** | DIN EN ISO/IEC **17025**（实验室资质）；IEC 60747-8:2010；IEC 60747-9:2007；DIN EN 60747-15:2012（**隔离型功率半导体器件**）；IEC 60749-5:2003；IEC 60749-6:2002；**IEC 60749-34:2011（功率循环）**；**IEC 60749-25:2003（温度循环）** |
| **QC** | IEC 60068-2-48:1982；DIN EN 60664-1；DIN EN ISO 60664-1 Appendix 1；DIN EN 60664-4；DIN EN 60664-5 |
| **QE** | DIN EN 60069-2-6；DIN EN 60069-2-27；DIN EN 60069-2-64 |
| **QL** | **JESD22-A119:2009** |

> **三个关键发现**：
> 1. **`IEC 60747-15`（Isolated power semiconductor devices）** 是功率器件的**专属器件标准**，AEC/JEDEC 体系中无对应。**这是知识 OS 必须新增的节点。**
> 2. **AQG 324 只引用了 1 个 JEDEC 标准（JESD22-A119）** —— 印证 Track 04 的结论："车规层几乎不继承民标层，而是自成体系"。
> 3. **大量 DIN EN 60664 系列**（电绝缘/耐压）—— 与 IEC 60664 是**欧洲采标关系**，查证时须走 EN 而非 IEC 原文。

#### 3.2.3 OEM 企业标准的定位（**必须与国家/国际标准严格区分**）

| 标准 | 性质 | 状态 | 可信度 |
|---|---|---|---|
| **LV 324** | **德国车厂联合企业标准** | **已被 AQG 324 取代**（`[一手]` ECPE 官网） | ★★★★ |
| **VW 80000** | **大众集团企业标准**（前身 VW 80101） | 现行版本 VW80000:2022-12 | ⚠️ `[二手]` |
| **GMW** | 通用汽车企业标准 | 未核实 | ⚠️未核实 |
| **USCAR** | 美国汽车制造商联盟规范 | 未核实 | ⚠️ 未核实 |

`[二手·低可信度，仅作映射参考]` 关于 **VW 80000** 的谱系（来源 `htec-emc.com`，一家 EMC 测试服务商，**商业网站，非 VW 官方**）：
> "VW80000… 前身是 **VW80101**，基于欧洲联合车企 **LV124** 规范优化升级，由大众、奥迪、宝马、奔驰、保时捷联合制定框架，大众独立落地执行。"
> 适用范围：总质量 ≤3.5t 的 12V低压车载电子电气/机电部件；**不适用高压新能源部件**。

> **⚠️ 评估**：这个说法与 LV324 的 IEEE 演讲数据（5 家德系车企）方向一致，但**该页面本身是营销性质的第三方技术解读，不能作为事实依据**。
> **重大提示**：**若该谱系成立，则"VW80000 基于 LV124"与"AQG324 基于 LV324"是两条不同的线**，且**VW80000 明确排除高压新能源部件** —— 也就是说 **VW 的电动车功率模块验证不走 VW80000，而走 AQG 324**。**这条如果错了会导致选错标准，但对可靠性工程师影响极大，标记为最高优先级待核实项。**

> **知识 OS 应对**：企业标准（VW80000 / GMW / USCAR / LV324）**一律建模为 `org: vendor_enterprise_standard`**，与 ISO/IEC/JEDEC 类分开。理由：① 免费可得性差；② 版本由企业单方控制；③ 常不公开全文；④ 客户审核时才是真正约束。

### 3.3 设备厂（ASML / AMAT / Lam / KLA）与材料厂

`[一手]` **本次未找到设备厂公开引用 SEMI/IEC 标准的规格书原文**（设备厂规格书通常在 NDA 下）。**明确标记为未核实，不编造。**

**可用的替代路径** `[一手]`：
1. **SEMI 自己的"Top 10 Standards"页面**（`semi.org/en/products-services/standards/top-10-standards`）列出了设备厂最常引用的标准，可反推哪些是设备接口事实上的必需项：
   ```
   S2   EHS Guideline for Semiconductor Manufacturing Equipment
   E187 Specification for Cybersecurity of Fab Equipment
   S8   Safety Guideline for Ergonomics Engineering of SME
   S22  Safety Guideline for the Electrical Design of SME
   F47  Specification for Semiconductor Processing Equipment Voltage Sag Immunity
   E10  Definition and Measurement of Equipment Reliability, Availability, and
        Maintainability (RAM) and Utilization     ← 与封装/设备可靠性直接相关
   S10  Safety Guideline for Risk Assessment and Risk Evaluation Process
   S6   EHS Guideline for Exhaust Ventilation of SME
   F57  Specification for High Purity Polymer Materials and Components
   E49  Guide for High Purity and Ultrahigh Purity Piping Performance
   ```
2. **SEMI 术语汇编 PDF（免费，1 份 PDF 覆盖数百术语→标准编号的映射）** `[一手]`：
   `https://www.semi.org/sites/semi.org/files/2023-04/CompilationTerms0721.pdf`
   > 实测内容形如：`BGA | ball grid array | SEMI G93`；`BMD | bulk micro defect | SEMI M59`；`BOX | buried oxide layer | SEMI M59, MS13`；`BUB | backside micro-bump | SEMI 3D6`
   > **这是本Track 发现的最高性价比单一文件** —— 一个免费 PDF，把数百个行业术语反向映射到具体标准编号。**建议直接作为知识 OS 术语→标准映射表的种子数据。**
3. **KLA 官网产品页**（`kla.com`）提到 MicroSense 系列"可生成 **SEMI 标准指标**"（实测中文页原文）—— 证明**量测设备确实按 SEMI 指标输出**，但**具体指标编号未在该页披露，⚠️未核实**。

> **诚实结论**：**"设备厂规格书引标准"这条路径在公开网络上基本不可得**（NDA 保护）。知识 OS 应改用**SEMI 术语汇编 + SEMI 官方委员会页面**作为等价替代，不要在设备厂维度建虚假边。

### 3.4 学术源

| 源 | URL | 状态 | 可信度 | 备注 |
|---|---|---|---|---|
| **IEEE Xplore** | `ieeexplore.ieee.org` | 实测可达 | ★★★★★ | 权威文献库 |
| **TCPMT** | `ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5503870` | **实测访问到** | ★★★★★ | 见下 |
| **JMEP**（IMAPS 期刊） | `imapsjmep.org/for-authors`；投稿平台 `jmep.scholasticahq.com` | 实测可达 | ★★★★☆ | 见下 |
| **arXiv** | `arxiv.org` | 未实测 | ★★★★ | 仅预印本，**未经同行评审**，引用时须标注 |
| **SciELO** | `scielo.org` | 未实测 | ★★★★ | 南美为主，对半导体可靠性覆盖有限 |
| **IEEE EDL / TPEL** | — | 未核实 | — | 器件级（非封装），与本用户相关性较低 |

#### 3.4.1 TCPMT（IEEE 元件、封装与制造技术汇刊）—— **最对口的期刊**

`[一手]` 官网实测数据（2026-10-05）：
> **Aims & Scope**（原文）："publishes research and application articles on the modeling, design, physical testing, materials, manufacturing, and **reliability** of electronic, photonic, RF, MEMS and sensor packaging, electrical contacts and connectors… Package design, including **heterogeneous integration**… integration for (**electrical, thermal, and thermo-mechanical**) performance, manufacturability, **reliability, test**, and security"
>
> - **Impact Factor 3.3**；**Eigenfactor 0.612**；**CiteScore 5.9**
> - **混合期刊**（hybrid）：订阅制 **无 APC**；开放获取 **APC $2,800 USD**
> - 主编：Yogendra Joshi（Georgia Tech）
> - **ISSN 2156-3950/ E-ISSN 2156-3985**，创刊 2011

> **`[推断]` 成本判断**：若为读而订阅，$2,800/篇的 APC 意味着**自建投稿通道极不划算**；应优先用机构订阅访问 IEEE Xplore。

#### 3.4.2 JMEP（Journal of Microelectronics and Electronic Packaging，IMAPS 主办）

`[一手]` `imapsjmep.org/for-authors` 实测原文：
> - "dedicated to publishing peer-reviewed papers in research, development, and the application relating to all aspects of microelectronics packaging, interconnect and assembly technologies"
> - 覆盖："3D integration, Ceramic Interconnect, Solling, Flip Chip, **Wire Bonding**, **Encapsulation**, RF and microwaves, MEMS, Photonics, **Power/High Temperature Electronics**, Printed Electronics, LED packaging, Medical Electronics"
> - "**published quarterly**"，可接受会议论文
> - **费用**："There are currently **no fees for IMAPS members** to publish… **Non-members will be charged** publishing fees after October 1, 2022."
> - 论文可回溯至 **2004 年**
> - 版权转让表邮箱：`jmep@imaps.org`
>
> ⚠️ `imaps.org` 主站与 `imapsource.org` 本次 curl 返回 **403**（反爬），需浏览器访问。

> **对本用户的价值**：**JMEP 是功率/高温封装领域最对口的免费/低成本期刊**（IMAPS 会员免发表费），且创刊 2004 年、季度刊，**样本量足够做文献计量**。

### 3.5 会议

`[一手/二手混合，按可靠性]`——**未逐一核实官网**，列出需后续核实的清单：

| 会议 | 主办 | 可靠性/封装相关性 | 状态 |
|---|---|---|---|
| **IEEE ECTC**（Electronic Components and Technology Conference） | IEEE Components, Packaging & Manufacturing Technology Society | ★★★★★ **最对口** | ⚠️ 未核实 |
| **IEEE CPMT Symposium** | IEEE CPMT Society | ★★★★★（LV324 数据即来自其 2017 演讲） | ⚠️ 未核实 |
| **APEC**（Applied Power Electronics Conference） | PELS | ★★★★（功率器件/模块） | ⚠️ 未核实 |
| **ISPSD**（International Symposium on Power Semiconductor Devices） | IEEE | ★★★★（器件级） | ⚠️ 未核实 |
| **EPE**（European Power Electronics Conference） | EPE Association | ★★★★ | ⚠️ 未核实 |
| **IMAPS Symposium / DPC** | IMAPS | ★★★★ | ✅ **已核实**（见下） |
| **SEMI 技术会议 / Standards Meetings** | SEMI | ★★★★ | ✅ **已核实**（见下） |

**已核实的会议信息** `[一手]`：
- **IMAPS Symposium 2026**：2026-09-28~10-01，Boston，5 tracks，keynote 来自 Qualcomm / Marvell / Cerebras。
- **IMAPS DPC 2027**：2027-03-01~04，Phoenix，abstract 截止 2026-10-09。
- **SEMICON West Standards Meetings 2026**：2026-10-12~15，San Francisco（实测出现在 SEMI 官网 Events 列表）。
- **ECPE Tutorial "Testing Automotive Power Modules according to AQG 324"**：由 AQG 324 Core Team 讲者授课，ECPE 官网设有专门页面。
- **IMAPS 2027 DPC / 各地 IMAPS 会议**均在 `imaps.org` 日历。

> **`[推断]`** SEMI 的 Standards Meetings 附在 SEMICON West/Eurola/China 等大会期间，**对"标准演进方向"的非正式情报价值极高**（Draft Document 编号、Task Force 成立、Adjudication 计划常在此透露）。建议作为情报源订阅。

---

## 4. 检索技巧与验证方法论（可操作部分）

### 4.1 ⭐ 确认"现行 / 已被取代 / 已废止"—— 三步法

> **这是知识 OS 最高频的查询动作，必须标准化。**

#### 第1 步：定位官方详情页
| 组织 | URL 构造 | 注意 |
|---|---|---|
| **JEDEC** | 人工在 `jedec.org` 搜编号 → 点进文档页 | **禁止构造 URL**（403）；slug 有连字符规则 |
| **SEMI** | `store-us.semi.org` 搜编号 | 搜结果标题自带状态后缀 |
| **IEC** | `webstore.2iec.ch/publication/<id>` 或搜标准号 | 直接给 `Withdrawal date` + 继任版链接 |
| **IPC** | `electronics.org/search` | 品牌已变更 |
| **AEC** | `aecouncil.com/AECDocuments.html`（**HTTP**） | 清单在一页内，无需查询 |
| **AQG 324** | `ecpe.org/research/working-groups/automotive-aqg-324/` | 下载区直接列全部版本 |

#### 第 2 步：读状态字段（**用各组织自己的词汇，不要翻译**）

| 组织 | 状态词（实测） | 位置 |
|---|---|---|
| **JEDEC** | `Reaffirmed` / `Rescinded` / 无标签；被取代时正文含 `SUPERSEDED BY <编号>` | 检索结果列表项 + 文档页摘要 |
| **SEMI** | `- Current` / `- Superseded` / `- Inactive`（+ `(Reapproved YYYYMM)`） | **产品标题后缀** |
| **IEC** | 无显式"Status"字样；改看 `Withdrawal date` + "A more recent version of this publication exists" 提示 | 详情页顶部横幅 |
| **IEC（阶段码视角）** | `PPUB`=已发布 / `WPUB`=已撤回 / `DELPUB`=已删除 / `APUB`,`BPUB`=出版中 | TC 项目状态页 |
| **ANSI/SAI（fallback）** | `Current` / `Superseded` + `Superseded by` + `Superseded date` | ⚠️ **会滞后，仅作交叉验证** |

#### 第 3 步：判定复审窗口（**JEDEC 专属，5 年**）
```
末次出版日 + 5 年 = JEDEC 复审截止（依据 JEDEC Manual JM21W §7.2）
若已过期且官网仍无新版本 → 极可能已被 Reaffirm（去文档页确认 Reaffirmed 标签）
若已过期且文档消失 → 可能已被 Rescind
```

### 4.2 ⭐ 追溯修订历史（各组织的版本字母/数字语义对照）

| 组织 | 版本机制 | 语义 | 实例 |
|---|---|---|---|
| **JEDEC** | `JESD<num><字母>` | 字母 = **修订序号**（无A = 第1版） | A→B→…→J；`JESD47`~`JESD47M` |
| JEDEC | `.<两位数>` 后缀 | 该版本的**第 N 次增补/勘误** | `JESD22-A104F.01`（F.01 = F 版的 .01） |
| JEDEC | `(R<YYYY>)` | 官方**Reaffirmed** 年份（**不改内容**） | `JEP155B:2018(R2024)` |
| JEDEC | `JS-xxx-YYYY` | Joint Standard，尾部为年份 | `JS-001-2017` |
| **IEC** | `ED<n>` / Edition `<major>.<minor>` | `2.0`=第2版；`2.2`=第2版+2次修正 | `IEC 60749:1996+AMD1:2000+AMD2:2001` → `ED2.2` |
| IEC | `/AMD<n>:<YYYY>` | Amendment（**修改件**，改动较大） | `IEC 60556:2006/AMD1:2016` |
| IEC | `/COR<n>:<YYYY>` | Corrigendum（**勘误**，仅纠错） | `IEC 60749-1:2002/COR1:2003` |
| IEC | `+` 后接 AMD | **Consolidated Version（合成版）** | `IEC 60749:1996+AMD1:2000+AMD2:2001` |
| IEC | `CSV` 后缀 | 合成版的另一种标记 | `IEC 61400-6:2020+AMD1:2025 CSV` |
| IEC | `/FRAG<n>` | **片段**（大标准拆分更新） | `IEC 60749/FRAG1`、`/FRAG2` |
| **SEMI** | `-MMDD`（6 位） | **原始发布年月** | `SEMI 3D1-0912` = 2012-09 |
| SEMI | `(Reapproved MMDD)` | **复审批准年月**（内容可能已变） | `SEMI 3D10-0814 (Reapproved 1025)` |
| **AQG 324** | `V<NN>.<N>/<YYYY>` | 第 NN 版第 N 次修订 | `04.1/2025` |
| **MIL-STD** | `<字母>` + `w/CHANGE<n>` | 字母=版；`w/CHANGE n`=第 n 号变更 | `MIL-STD-883K w/CHANGE 3` → `883L` |
| **AEC** | `-<字母>`（部分还有数字） | 修订号 | `AEC-Q100 Rev J1`；`AEC-Q101-001 Rev A` |
| **IPC** | `<字母>` + `-WAM<n>` | Standard with Amendment（**合成版**） | `IPC-9702-WAM1` |

> **知识 OS 必须注意**：
> 1. **同一字母语义在不同组织完全不同**（JEDEC 的 `J`=第10版；IPC 的 `J`=第10版；但 SEMI 的 `0912` 是日期）。**绝不能用统一解析器。**
> 2. **`(R<YYYY>)` / `Reaffirmed` / `(Reapproved)` 都表示"内容未变或小变，仅确认继续有效"** —— 不是新版本。混淆这两者会导致知识 OS 把Reaffirm 记成"发布了新版"。

### 4.3 ⭐⭐ 提取"标准引用了哪些标准"—— normative vs informative

#### 4.3.1 权威定义（一手，非二手转述）

`[一手]` **ISO 官方 House Style**（`iso.org/ISO-house-style.html`）原文：
> "**Clause 2 is always called 'Normative references'.**"
> "**Normative annexes** contain content that is **indispensable for claiming conformity** to the document. **Informative annexes do not**, but they **can contain requirements**. It is **not necessary to follow requirements in an informative annex to claim conformity**."
> "To be labelled 'normative' an annex needs to be **clearly referenced as part of a requirement**… If an annex is only mentioned **in parentheses**, it is labelled 'informative'."
> "**Do not use the words 'informative' or 'normative' for cross-references in the text.** For example, write 'The object shall be registered in accordance with Annex A' and **not** '…in accordance with normative Annex A' (**it is the 'shall' that makes the annex normative**)."

`[一手]` **ISO/IEC Directives 的强制措辞**（经 hydrogenandfuelcellsafety.info 转录的 Directives Part 2 §6.2 原文）：
> 规范性引用清单**必须**以下列措辞引入：
> "**The following referenced documents are indispensable for the application of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.**"

**该清单"不得包含"** `[一手]`：
> "referenced documents which are **not publicly available**; referenced documents which are **only cited in an informative manner**;"

`[一手]` **ETSI 官方编写指南**（`portal.etsi.org/.../aguidetowritingworldclassstandards.pdf`）—— 给出最清晰的两分法：
> "**Normative references** identify other documents that are directly referenced within **normative provisions in the main body** of the standard. They are **effectively part of the standard**… so it is imperative that you ensure that all referenced documents are **publicly available**!
> **Informative references** identify other documents that are directly referenced from within the main body of the standard **purely to provide additional information for the purposes of justification or clarification**."
> "If your standard makes references to specific clauses in another document you should **always specify which edition** you are referencing."
> "**Be careful!** If the user of the standard uses a different version of the referenced document to what you intended, **their implementation may be wrong!**"

**已验证的实证** `[一手]` **IEC 60749-1:2002 原文**（VDE/EN-Standard 提供的官方预览 PDF，双语对照）：
> **§2 Normative references**："The following referenced documents are **indispensable for the application** of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies."
> ```
> CEI 60050 (toutes les parties), Vocabulaire Electrotechnique International (VEI)
> CEI 60747 (toutes les parties), Dispositifs à semiconducteurs – Dispositifs discrets
> CEI 60748 (toutes les parties), Dispositifs à semiconducteurs – Circuits intégrés
> ```
> **注意**：`IEC 60050 (**all parts**)`、`IEC 60747 (**all parts**)` —— **`(all parts)` / `(toutes les parties)` 是 undated reference**。按上述 Directives 措辞，undated 引用意味着"**自动适用其最新版本**"。
> **→ 知识 OS 的"依赖边"必须区分 dated edge 与 undated edge。** undated edge 是**活动依赖**（上游一改版，下游全部受影响），dated edge 是**固定依赖**。

#### 4.3.2 实际提取方法（4 条路径，按可靠性排序）

| 路径 | 方法 | 可靠性 | 自动化程度 |
|---|---|---|---|
| **① IEC Webstore 结构化 tab** | 打开标准页 → `Normative references` tab 直接读官方整理好的清单 |★★★★★ | 可半自动（人工录入） |
| **② IEC Webstore 反向 tab** | 打开标准页 → `Referenced by` tab 得入边 | ★★★★★ | 同上 |
| **③ 原文 §2 章节** | 从 PDF 提取 "Normative references" / "Normative документации" 章节 | ★★★★★ | 可自动化（`pdftotext`） |
| **④ 全文正则扫编号** | 扫全文所有标准号（含正文脚注、表格、附录） | ★★★☆ | 可自动化，**但会混入 informative** |

**推荐工作流**：
```
Step1  从 ①/③ 拿到干净的 normative 集合（有版本号）→ 标记 edge_type = "normative"
Step 2  从 ④ 拿到全文出现过的全部编号集合
Step 3  Step2 \u2212 Step1 = 疑似 informative/bibliography 集合 → 人工抽样确认
Step 4  标记 edge_type = "informative"，置信度降级
Step 5  对 Step1 中的每条，检查是否为 dated / undated / (all parts)
        → 生成 dependency_type: "pinned" | "floating" | "all_parts"
```

**必须避免的三个错误**：
1. ❌ **把 `Referenced by`（被引用）方向搞反** —— IEC 的 `Normative references` 是出边，`Referenced by` 是入边。
2. ❌ **把 Bibliography 当 normative** —— ISO 规定 Bibliography 属informative 性质。
3. ❌ **忽略 undated 引用的活动性** —— 见§4.3.1，这是最隐蔽的失效来源。

> **`[推断]` 术语表条目的特殊规则**（ISO House Style 实测原文）：
> "Cite external ISO or IEC documents containing terminological entries in the introductory sentence of Clause 3… Since the user is **required to refer to these documents to understand the terminology** used in the text, they **constitute normative references and are listed in Clause 2**."
> 反之："**Reproduced** terminological entries from these documents… Source documents of **reproduced** terminological entries are **informative and are listed in the Bibliography**."
> **→术语引用可能是 normative（引出去）也可能是 informative（复制进来），取决于是否复制了原文条目。**

### 4.4 陷阱清单（每一条都有本次调研的实证）

| # | 陷阱 | 实证 | 防御措施 |
|---|---|---|---|
| **T1** | **JEDEC 状态词不是 Active/Withdrawn** | 实测 JEDEC 用 `Reaffirmed`/`Rescinded` | 用 §4.1 的组织专属词表 |
| **T2** | **JEDEC URL 不能构造** | `/docs/jesd22-a104f` 与 `/docs/jesd78f-02` 均 404；`/docs/jesd-78b` 才200 | 只走人工检索+ 记录最终 URL |
| **T3** | **JEDEC 禁止自动化访问** | 文档页 ToS 明文禁止 bots/scrapers；实测 `document_search` 403 | 知识 OS 不爬 JEDEC |
| **T4** | **JEDEC 不存在"公开征求意见"** | 手册 §4 的 ballot 全是委员会内部投票 | 改用 SEMI 博客 + JEDEC 新闻稿 |
| **T5** | **JEDEC「无新版本」≠ 仍有效** | §7.2：5 年后 Reaffirm / Revise / Rescind | 记录 `last_publish_date` + 5 年复审标记 |
| **T6** | **SEMI 的 Reapproved 年月不是出版年** | 实测 `3D10-0814 (Reapproved 1025) - Current` | 拆`first_published` / `last_reapproved` |
| **T7** | **SEMI `Inactive` ≠ `Superseded`** | 商店三种标签并存 | 区分三态 |
| **T8** | **IEC `stability date` 是复审时点，不是"最后更新"** | Directives 原文；实测 2027–2031 都有 | 独立字段，语义写清 |
| **T9** | **IEC 勘误/修正件是独立文档** | `IEC 60749-1:2002/COR1:2003` 是单独 publication ID(3334) | 版本模型须支持"兄弟文档"关系 |
| **T10** | **MIL-STD-883 拿到手≠拿到方法** | 实测 SSRI 镜像 28 页（总纲）vs NEPP 镜像 708 页 | 6 个分册建独立实体 |
| **T11** | **AQG 324 ≠ JEDEC/AEC 标准** | ECPE 是行业协会；AQG 基于 LV 324（企业标准） | 建模为独立 org + `based_on` 边 |
| **T12** | **LV 324 已被 AQG 324 取代** | ECPE 官网："Based on the former German LV 324" | 加`superseded_by` 边 |
| **T13** | **厂商报告引用 ≠ 标准内容** | Infineon 把 HTRB/HTGB 都写成 JESD22 A108，而 A108 官方名为 TBL | "引用关系"与"内容断言"分离建模 |
| **T14** | **厂商引标准不写版本号** | 实测写法 `JESD22 A108`（无连字符无版本） | 正则容忍 3 种写法；版本字段留空 + 不信任 |
| **T15** | **同一应力可由多个标准满足** | Infineon：`AC` 用 `JESD22 A102 **或** A118` | 引用边用集合，不是单值 |
| **T16** | **datasheet 常并列引用 3 个体系** | 实测 `JESD22-A108, IEC 60068-2-2, Test-AA` | 支持多值边 |
| **T17** | **企业标准冒充国际标准** | VW80000/GMW/USCAR/LV324 均为企业标准 | 建模 `org_type: enterprise`，不与 ISO/IEC 同类 |
| **T18** | **GB/T 采标版≠ IEC 原文** | 官方：采标 GB/T 仅提供题录；MOD 可改内容 | 采标程度字段（IDT/MOD）必存 |
| **T19** | **未编号的"企业标准"编号** | AEC-Q101-004 的 Rev 字段为空（"Rev-"）| 允许空版本，不得推断 |
| **T20** | **联合标准两边都有** | `IPC/JEDEC-9702A` 同时出现在 IPC ballot 表 | 联合标准查两个组织 |
| **T21** | **IPC 已更名 Global Electronics Association** | `ipc.org/standards` → 404；`electronics.org` 为新域 | 实体表记 dba + 双域 |
| **T22** | **AEC 官网只支持 HTTP** | https 连接失败，http 返回 200 | 保留 HTTP 回退 |
| **T23** | **reseller 元数据滞后** | SAI Global 标 `Stability Date: 2021` vs IEC 官网 `2029` | reseller 只用于"发现新版"，不用于"断言状态" |
| **T24** | **内容农场伪造标准** | 3 个英文站称 "SEMI G92 = Chiplet 互连可靠性指南"；**官网核实 G92 = 450mm tape frame cassette 规格** | 见 §6.4 |
| **T25** | **datasheet 的"标准引用"可能来自厂商内部模型** | Infineon Notes：ESD 等级"based on an empirical model" | 区分"标准规定"与"厂商计算" |
| **T26** | **非会员看不到 JEDEC ballot** | 手册无公开评审阶段 | 不要相信"公开征求意见"说法 |

> **`[推断]`** 本清单的 T1–T26 建议直接作为知识 OS 校验规则的种子。每条都能写成一条断言检查。

---

## 5. 社区与知识沉淀渠道

### 5.1 课程（免费/付费，需自评）

| 平台 | URL | 实测 | 说明 |
|---|---|---|---|
| **Coursera** | `coursera.org/search?query=semiconductor` | **200✅** | 有 "Semiconductor Manufacturing"、"Introduction to Microelectronics" 等（**具体课程质量未核实**） |
| **edX** | `edx.org/search?q=semiconductor` | **200✅** | 麻省理工等校的微电子课程（**未核实具体可靠性内容**） |
| **IMAPS Academy** | `imaps.org` | ⚠️ 403（反爬） | 实测简介页提到 "Semiconductor Package Design and Assembly"（讲者 Tom Dory, ITM Consulting）**[一手· imaps.org 首页]** |

> **诚实评估** `[推断]`：**公开课程几乎不覆盖"封装可靠性标准方法学"这一层**。它们的定位是器件物理/工艺/电路。对 20 年经验的可靠性工程师，**课程的信噪比很低**。**建议的优先级低于 §1–§4 的一手源。** 唯一可能例外是 ECPE 面向 AQG 324 的 Tutorial（见 §3.5），但那不是公开课。

### 5.2 YouTube / EEVblog

`[一手·实测]` `https://www.eevblog.com/` → **200✅ 可达**。EEVblog（Dave Jones）以**电子工程实验/评测**著称，覆盖电源、EMC、测试仪器。

> **`[推断]` 对本用户的价值有限但非零**：EEVblog 的内容偏"动手测量与仪器使用"，**不讲 JEDEC/IEC/AQG 标准条款**。**关于封装可靠性实验室的专门频道（如_power cycling_、_HAST_、_SAM_ 设备演示），本次未做系统检索，标记为未核实。** 不建议将其纳入知识 OS 的信源白名单。

### 5.3 行业媒体

| 媒体 | URL | 实测 | 可信度 | 定位 |
|---|---|---|---|---|
| **Semiconductor Engineering** | `semiconductorengineering.com` | **200✅** | ★★★★ | **本领域最好的行业媒体**。有 "Advanced Packaging" / "Reliability" 栏目，深度报道 fab/封装/测试产业与标准动向 |
| **SEMI 博客 Technology and Trends** | `semi.org/en/blogs/technology-trends` | **200✅** | ★★★★★ | **半官方**（SEMI 官方发布），**唯一公开 ballot 时间窗与草案编号的渠道**（见 §1.2.5） |
| **Reddit r/semiconductor** | `reddit.com/r/semiconductor` | **000（不可达）** | ★★ | ⚠️ 本环境不可达；且为**匿名讨论，不作事实依据** |

> **情报分工**：
> - **要"标准要变了"的信号** → SEMI 博客（官方）+ JEDEC 新闻稿（官方）
> - **要"产业在做什么"的上下文** → Semiconductor Engineering
> - **不要**从 Reddit 取任何标准事实。

### 5.4 中文信源分级（**严格区分**）

| 级别 | 媒体 | 可用方式 | 判定理由 |
|---|---|---|---|
| **A｜可信行业媒体** | **半导体行业协会**（CSIA，中国半导体行业协会） | 统计数据、标准动态 | 行业协会官网 |
| **A** | **集微网（Laoyaiba / 集微社）** | 产业新闻 | 垂直行业媒体，有记者署名的原创报道 |
| **A-** | **芯智讯** | 产业新闻 | 行业媒体，原创为主 |
| **B｜需谨慎** | **亿欧半导体** | 产业趋势 | 偏咨询/分析内容，**常含推测与融资叙事**；引标准时须回溯原文 |
| **⚠️ 黑名单** | **知乎** | ✗ | UGC，含大量未核实与以讹传讹的标准编号 |
| **⚠️ 黑名单** | **微信公众号** | ✗ 除非作者本人原文 | 大量为**搬运/洗稿**；无法回溯原始出处 |
| **⚠️ 黑名单** | **百度百科** | ✗ | 本次调研中baike 关于"国家标准全文公开系统"的词条内容（2,638 项外文版、下载量等）虽数字看起来合理，但**属 UGC 不可采信**；同一事实已用 SAMR 官网原文独立核实 |
| **⚠️ 黑名单** | **CSDN** | ✗ 除非作者本人为标准委员会成员并注明出处 | 本次调研实测命中大量 CSDN 博客，**其中"细节丰富"的文章（如A104F.01 条件表详解）含大量标准原文细节但无一手引用**，高度疑似 LLM 生成/洗稿，**不可采信** |
| **⚠️ 黑名单** | **renrendoc / b2b168 / 11467 / eeworld 下载站** | ✗ | 二次上传的PDF/摘录，**版本与完整性不可保证** |
| **⚠️ 黑名单** | **globaltradedraft / zysdsteel / grokipedia / htec-emc** | ✗ | 见 §6.4，**内容农场，已实证造假** |

> **本次调研中的一个具体教训**：关于 **LV324 谱系**与 **AQG 324 引用清单**的中文资料（`wap.b2b168.com`、`m.renrendoc.com`）内容详实且看似专业，但其**准确性依赖对 LV324 原文的引用**，而 LV324 是**付费/受限的车厂企业标准**——**读者无法验证**。这类内容**可用于形成"待核实假设"，不可用于断言**。

---

## 6. 本次调研的负面发现（同等重要）

### 6.1 未核实项清单（**知识 OS 严禁写入这些 URL**）

| # | 事项 | 状态 |
|---|---|---|
| U1 | JEDEC 各文档的付费/免费规则 | **未找到成文规则**，仅有§1.1.4 两个样本 |
| U2 | JEDEC 文档检索页的完整 facet 列表 | **403**，仅观察到 Committees / Document Types / Technology Focus Areas 三组 |
| U3 | IEC Webstore 搜索页的正确 URL 形式 | `webstore.iec.ch/en/searchform&q=` **实测 404** |
| U4 | `electronics.org/Status`（IPC ballot 页） | 存在（搜索索引可见表格），**本次未成功直取内容** |
| U5 | IPC-TM-650 是否真可免费下载 | 来自 `ipc.org.cn` 二手声明，**未从 electronics.org 一手确认** |
| U6 | DLA ASSIST（`assist.dla.mil` / `quicksearch.dla.mil`） | **本次连接失败**，未能一手验证 |
| U7 | everyspec / everypec | **403**，未验证 |
| U8 | ST / TI / onsemi / Mitsubishi / Rohm / Semikron Danfoss 的资格报告入口 | **未核实** |
| U9 | ASML/AMAT/Lam/KLA 规格书中的SEMI/IEC 引用 | **未找到公开材料**（NDA 保护） |
| U10 | USCAR / GMW 标准内容 | **未核实** |
| U11 | **VW80000 与 LV124 的谱系关系** | **仅二手（商业网站）**，**最高优先级待核实** |
| U12 | BSI / IET / UL / SAI Global 的具体价格与半导体标准覆盖 | **未逐一核实** |
| U13 | Techstreet Enterprise / ANSI/NESSI 订阅价格 | **未公开/未核实** |
| U14 | ECTC / APEC / ISPSD / EPE 官网 | **未核实** |
| U15 | arXiv / SciELO 在本主题的覆盖情况 | **未核实** |
| U16 | AQG 324 的 CC BY-ND 许可条款 | **本Track 未独立复核**（来自 Track 04） |
| U17 | 设备厂量测指标对应的具体 SEMI 编号 | **未核实**（KLA 页面仅说"可生成 SEMI 标准指标"） |
| U18 | YouTube 上封装可靠性实验室专门频道 | **未做系统检索** |

### 6.2 结构性障碍（无法靠"更努力"解决）

1. **JEDEC 文档无免费结构化 API，且明确禁止自动化访问。** → 知识 OS 的JEDEC 部分只能是**"人工录入 + 强制标注访问日期"** 的模式。这不是技术缺陷，是**合规约束**。
2. **付费墙不可绕过。** IEC 约 CHF 260/份，60749 有 42 parts。→ 必须**只买高频引用的少数几份**。
3. **企业标准（LV324 / VW80000 / GMW / USCAR）几乎不可公开获得。** → 只能通过**客户审核文件**、**AQE 324（其公开继承者）**、学术论文侧面了解。
4. **设备厂规格书在 NDA 内。** → 只能从 SEMI 侧（术语汇编 + 官方委员会页）获取。

### 6.3 一个方法论建议：**用"引用密度"而非"权威等级"排序**

`[推断]` 用户建知识 OS 时，标准的重要性不应由"组织名气"决定，而应由**"被多少一手源引用"**决定。本次实测的引用密度：

| 层级 | 标准 | 引用证据 |
|---|---|---|
| **第 1 层（各厂商报告必现）** | JESD22-A104(TC)、-A108、-A101、-A103、-A110/-A118、-A114、-C101、-B100/-B106、J-STD-020、J-STD-002 | Infineon 4 份报告全含 |
| **第 2 层（车规必现）** | **AEC-Q101**（分立）、**AEC-Q100**（集成） | Infineon 报告标题即"AEC Q101" |
| **第 3 层（功率模块必现）** | **AQG 324**（含其引用的 IEC 60747-15、60749-25、60749-34、60664 系列、JESD22-A119） | ECPE 官方 + IEEE 演讲 |
| **第 4 层（国际对标）** | IEC 60749 全族、IEC 60747 全族、IEC 60068 | AQG 324 引用清单 |
| **第 5 层（军标）** | MIL-STD-883 系列 | Infineon 引MIL-STD-750/1037 |
| **第 6 层（先进封装）** | SEMI G 系列（3D1–3D15）、SEMI F47/E10 | SEMI 官方 Top 10 / 术语汇编 |

> **建议**：知识 OS 的**首页/默认视图**应按这个密度排序，而不是按组织字母序。用户 80% 的查询会落在第 1–3 层。

### 6.4 ⭐ 已实证的内容农场造假案例（**写进黑名单的理由**）

| 声称 | 声称来源 | 官方核实结果 |
|---|---|---|
| "**SEMI G92-0526** = *Guide for Reliability Testing of 2.5D/3D Chiplet Interconnects*，2026-05-02 发布，引入 TMF-APM 模型，强制要求 ≥1000 循环微凸点失效率分布" | `globaltradedraft.com`（长篇"行业分析"体，含大量"Impact on Enterprise Segments"段落） | ❌ **不实**。SEMI 官方商店实测：**G92 = 450 mm 晶圆用tape frame cassette（带式框架卡匣）的机械规格**（日文版，2013-08-22 版）。内容与 Chiplet 无关 |
| "**SEMI F71-0526** = Leak Zero / 同轴线微振动免疫，**TSMC 与 Intel 已强制纳入设备采购准入**"，0.05–20 Hz，RMS ≤0.02 mm | `zysdsteel.com` | ❌ **无法核实，且表述模式高度可疑**（用标准号 + 具体客户名 + 具体数字制造权威感）。**未在 SEMI 官方任何页面找到 F71** |
| "**MIL-STD-883 有 101/105/110 等三位方法号**" | 中文汇编（Track 06 已记录） | ❌ 方法号为**四位**（1001–1034 / 2001–2035） |
| "**AQG 324 引用了 UNECE R10 / RoHS / ELV / WEEE**" | 任务书假设 | ❌ 引用清单中**没有**任何环保/法规类标准 |
| "**JESD22-A108 = Temperature, Bias, and Voltage Life**" | 中文站高频误传 | ❌ 官方为 "**Temperature, Bias, and Life**"，无"Voltage" |
| "**JESD78 = ESD 标准**" | 中文站高频误传 | ❌ JESD78 = **IC Latch-Up Test** |
| "**JESD204 = DDR4**" | 中文站高频误传 | ❌ DDR4 = **JESD79-4**；JESD204 = SerDes |
| "**MIL-STD-883 已废止**" | 推测性内容 | ⚠️ 现行版为 **883L (2019-09-16)**，可用，**未废止** |

> **内容农产的识别特征（可直接写成自动化检测规则）**：
> 1. **不给出处URL**，或给出的 URL 无法验证（本次 §6.4 中 3 个 URL 均为内容农场自身域）
> 2. **大量"Impact on…"小节 + 每段 3–5 句填充**，句子可任意删改而不损失信息
> 3. **把标准号 + 具体客户名 + 具体数值绑在一起**（如"TSMC/Intel 强制""0.02mm RMS"）—— 真实技术文件不会这样写
> 4. **不写"截至/Retrieved on/访问日期"**
> 5. **域名是新注册或内容农场集群**（`globaltradedraft` / `zysdsteel` / `grokipedia` / `10100.com` / `11467.com` / `b2b168` / `m.cqn.com.cn`转载号）
> 6. **中英混杂的"参考文献"条目**（如把 Siemens 营销文案和 Rencz 学术专著并列，编号方式不一致）
>
> **对知识 OS 的直接要求**：任何外部信息入库，**必须同时存储 `source_url` + `accessed_date` + `is_primary` 三个字段**。缺任一则拒绝入库。这条规则能拦掉本清单中约 90% 的错误条目。

---

## 7. 给知识 OS 的落地建议（直接可执行）

### 7.1 断言模型（建议 schema）

```yaml
standard_id: "IEC 60749-1"          # 规范化后的主键
org: IEC
org_type: international              # international | industry_association | enterprise | national | joint
edition: "1.0"
designation: "IEC 60749-1:2002"
doc_family: "IEC 60749"              # 父族
part:1
status: published                     # 各组织词表见 §4.1，存原词 +归一值双列
status_raw: "PPUB"
stability_date: 2029                  # IEC 专属，nullable
first_published: 2002-08-30
last_reapproved: null                 # SEMI 专属
sibling_docs:                        # 勘误/修正/分册/片段
  - id: "IEC 60749-1/COR1:2003"
    relation: corrigendum
  - id: "IEC 60749-1/AMD1:2015"
    relation: amendment
derived_versions:                    # 合成版/被合并版
  - "IEC 60749-1:2002+AMD1:2015 CSV"
work_status:                          # IEC 阶段码，可为"在研"
  - code: "CDV"
    project_ref: "47/1522/CC"
project_phase: null
superseded_by: null                   # 归一后的继任
supersedes: ["IEC 60749:1996"]
committee: "TC 47/WG 2"
ics: "31.080.01"
source_url: "https://webstore.iec.ch/publication/3333"
accessed_date: "2026-10-05"
is_primary: true
price: { amount: 260, currency: "CHF", paid: true }
```

```yaml
# 引用边（引用关系）
edge_type: normative|informative       # 必须区分
from: "IEC 60749-1:2002"
to: "IEC 60747"
dependency_type: all_parts|undated|pinned   # IEC 特有，见 §4.3.1
extraction_method: iec_webstore_tab|fulltext_regex|ansi_webstore|manual
confidence: A|B|C
evidence_url: "..."
accessed_date: "2026-10-05"
```

```yaml
# 「被实际采用」边（与「引用关系」严格分离，见陷阱 T13）
adoption:
  standard_id: "JESD22-A108"
  claimed_by: "Infineon IRFS7437-7p"
  claimed_for: "HTRB"        # 厂商声称用于什么
  vendor_citation_raw: "JESD22 A108"   # 保留厂商原始写法（T14）
  version_cited: null                  # 厂商通常不写版本
  evidence_url: "https://www.infineon.com/assets/row/public/documents/24/316/infineon-irfs7437-7p-productqualificationreport-en.pdf"
  accessed_date: "2026-10-05"
  caveat: "厂商未写版本；A108 官方名为 TBL，HTRB 参数非 A108 规定（T13/T25）"
```

### 7.2 实施优先级（按投入产出比）

| 优先级 | 动作 | 成本 | 收益 |
|---|---|---|---|
| **P0** | 建JEDEC/SEMI/IEC/AEC/ECPE **五套状态词表 + URL 模式表**（本文件 §4.1/§4.2） | 半天 | 消除 T1/T2/T6/T7/T8 |
| **P0** | 采购 **SEMI 术语汇编 PDF**（免费）做术语→标准种子映射 | 1 小时 | 数百条映射，零成本 |
| **P0** | 建**陷阱规则 T1–T26** 为入库校验 | 1 天 | 拦掉绝大多数错误 |
| **P1** | 抓取/整理 **AQG 324 引用清单**（§3.2.2）+ 交叉核对官方 PDF | 1 天 | 功率封装最核心的依赖图 |
| **P1** | 人工录入 **JESD22 全族 + JESD47** 的状态与继任链（用 §1.1.7 的经销商 fallback） | 2–3 天 | 覆盖 80% 查询 |
| **P1** | 抓 **ANSI Webstore 60749 全系列页**的 "significant technical changes" 段落 | 半天 | 版本演进说明，白嫖 |
| **P2** | 订阅/跟踪 **SEMI Technology and Trends**（唯一 ballot 信号源） | 每月 10 分钟 | 提前预警 |
| **P2** | 建 **IEC TC 项目状态页**的定期快照（TC 47 等） | 每周 30 分钟 | 提前 1–2 年发现换版（如 60749 正在完整更新） |
| **P3** | 买 IEC 60749-25/-34（功率/温度循环）+ 60747-15（隔离型功率器件） | CHF 约 700–800 | 功率封装原文 |
| **P3** | 核实 **VW80000 谱系**（U11） | 需行业关系 | 避免选错车规标准 |

### 7.3 三条"永远不要做"

1. ❌ **不要爬 JEDEC** —— 违反 ToS 且技术已被拦截。
2. ❌ **不要用 reseller 的status 字段做断言** —— 实测会拿到过期数据（T23）。
3. ❌ **不要把"厂商报告引用了X"当成"X 的内容是Y"** —— 这是本Track 发现的最隐蔽的失效模式（T13）。

---

## 8. 一页速查：按编号类型去哪里查

| 我拿到… | 去哪里查 | 免费？ | 关键提醒 |
|---|---|---|---|
| **JESD22-xxx / JESD47x** | jedec.org 人工检索 → `/docs/<连字符slug>` 或 `/node/<id>` | ✅ 免费注册 | 状态词是 Reaffirmed/Rescinded；5 年复审；禁爬 |
| **MS-xxx / SPP-xxx** | 同上（属 Microelectronic Standards / Standard Practices） | ✅ | **非规范性**类要留意 |
| **J-STD-xxx / IPC/JEDEC-xxx** | **electronics.org（不是 ipc.org）** + **jedec.org** 两边都查 | 部分 | 联合标准两边都有 |
| **TO-/DO-/SO-/MO-（封装外形）** | jedec.org（JEP95体系） | 部分免费 | 这是"外形注册"，不是可靠性标准 |
| **IEC 607xx-xxx** | **webstore.iec.ch** → 看 Lifecycle / Normative references / Referenced by | ❌ 付费（勘误常免费） | 记 stability date；查 TC 项目页看换版 |
| **IEC 607xx-x/CORn 或 /AMDn** | webstore.iec.ch 搜"基础号+后缀"，是**独立文档** | 勘误常免费 | 别把修正件当成基础版的一部分 |
| **SEMI Mxxx / Sxxx / Gxxx** | store-us.semi.org（也可看 china.semi.org.cn 列表） | ❌ 付费/订阅（30天试用） | `Reapproved` 年月 ≠ 出版年；`Inactive` ≠ `Superseded` |
| **AEC-Q1xx** | **`http://`**aecouncil.com/AECDocuments.html | ✅ 全免费 | **只用 http**；清单在一页内 |
| **AQG 324** | ecpe.org/research/working-groups/automotive-aqg-324/ | ✅ 免费 | 已取代 LV 324；版本格式 04.1/2025 |
| **LV 324** | **不可公开获得** → 改查 AQG 324 | ❌ | 别当国际标准用 |
| **VW 80000 / GMW / USCAR** | 厂商客户关系 / 付费咨询 | ❌ | 企业标准；VW80000 谱系未核实 |
| **MIL-STD-xxx** | ① DLA ASSIST ② NASA NTRS ③ NEPP/SSRI 直链 | ✅ 免费（但下载源需试探） | **883 有 6 个分册**；用"注意日期"防滞后 |
| **GB/T xxxxx** | openstd.samr.gov.cn（全文）/ std.samr.gov.cn（信息） | ⚠️ **采标仅题录** | 采标版权限制；MOD 可能改内容 |
| **某标准"这个版本改了什么"** | ANSI Webstore 系列的 "significant technical changes" 段 | ✅ 免费 | 白嫖的版本差异信息 |

---

## 附录A：本次调研访问过的一手 URL 清单（供复核）

**已成功访问并提取内容的一手源：**
```
https://www.jedec.org/                          200
https://www.jedec.org/standards-documents                200（facet 计数）
https://www.jedec.org/standards-documents/docs/jesd-78b  200（JESD78F.02 字段布局）
https://www.jedec.org/node/8434                         200（JESD79-4D 付费 $284）
https://www.jedec.org/sites/default/files/JM21W.pdf     200，633KB（已下载并 pdftotext 解析）
https://www.jedec.org/termsofuse                        搜索索引原文（反爬条款）；curl 403
https://www.semi.org/en/products-services/standards    200（Volume 清单、免费试用、投票入口）
https://store-us.semi.org/collections/standards/lang-english  200（价格、Current/Superseded/Inactive 状态）
https://store-us.semi.org/products/g09200-...           200（G92 真实标题证伪）
https://www.semi.org/en/blogs/technology-trends         200（ballot 时间窗、Draft Document 7381）
https://www.semi.org/en/products-services/standards/top-10-standards  200
https://www.semi.org/sites/semi.org/files/2023-04/CompilationTerms0721.pdf  200（术语→标准映射）
https://www.ecpe.org/research/working-groups/automotive-aqg-324/  200（版本史）
http://www.aecouncil.com/AECDocuments.html               200（完整文件清单，已提取全部链接）
https://webstore.iec.ch/en/publication/64423            200（三 Tab 结构）
https://webstore.iec.ch/en/publication/26383            200（CSV / stability date）
https://webstore.iec.ch/publication/3333                200（IEC 60749-1:2002 元数据）
https://webstore.iec.ch/publication/3334&login          200（COR1，CHF 0.-）
https://www.iec.ch/standards-development/stage-codes    200（阶段码字典）
https://www.iec.ch/dyn/www/f?p=103:21:...（TC 51）      200（稳定性日期表）
https://www.iec.ch/dyn/www/f?p=103:20:...（TC 47）      搜索索引原文（60749 FRAG1/2 MERGED）
https://openstd.samr.gov.cn/bzgk/gb/                    200（采标/非采标规则原文）
https://std.samr.gov.cn/                               200（七类标准 + 征求意见栏目）
https://www.samr.gov.cn/zw/zfxxgk/.../art_2023_...html  200（标准化法第十七条）
https://www.electronics.org/ipc-standards               200
https://www.electronics.org/test-methods               200（内容未取到）
https://www.iso.org/ISO-house-style.html                搜索索引原文（normative/informative 规则）
https://portal.etsi.org/.../aguidetowritingworldclassstandards.pdf  搜索索引原文
https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/std883.pdf  200，459KB，**已下载并解析（28 页）**
https://nepp.nasa.gov/docuploads/.../std883.pdf         200，4.5MB，**已下载（708 页）**
https://store.accuristech.com/                          200（价格）
https://shop.ipc.org/standards/standard-amendments      搜索索引原文（WAM 合成版）
https://imapsjmep.org/for-authors                       200（JMEP 投稿与费用）
https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5503870  200（TCPMT 数据）
https://ewh.ieee.org/soc/cpmt/presentations/cpmt1704a.pdf  LV324 测试矩阵
https://www.infineon.com/assets/row/public/documents/24/316/infineon-*.pdf  4 份（引用提取）
https://shop.standards.ie/en-ie/standards/jedec-jesd47l-2022-...  版本链字段
https://infostore.saiglobal.com/.../iec-60749-1-2002-...  £18.11 + Stability Date 2021（矛盾证据）
https://webstore.ansi.org/industry/semiconductors/tests/iec-60749  $33/$66 + 变更说明
https://www.en-standard.eu/publicdoc/iec_previews/69196.pdf  IEC 60749-1 双语预览（§2 原文）
https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-33{ed1.0}b.pdf  60749 全族 part 清单
```

**实测不可达（记录以免重复尝试）：**
```
https://www.jedec.org/document_search?search_api_views_fulltext=...   403
https://www.jedec.org/termsofuse（curl）                              403
https://ntrs.nasa.gov/                                                403（含 /api/citations/search）
https://assist.dla.mil/                                               连接失败
https://quicksearch.dla.mil/                                          连接失败
https://landandmaritimeapps.dla.mil/Downloads/MilSpec/Docs/...        连接失败
https://everyspec.com/  https://www.everypec.com/                     403 / 连接失败
https://www.aecouncil.com/（https）                                    连接失败（http 可）
https://imaps.org/                                                     403
https://www.reddit.com/r/semiconductor/                               连接失败
https://www.aqg-324.org/                                               DNS 不解析
https://ecpe.org/standards/aqg-324                                    404
https://webstore.iec.ch/en/searchform&q=semiconductor404
https://www.ipc.org/standards  |  www.electronics.org/standards        404（已更名/改版）
https://www.electronics.org/Status                                    WebFetch 返回空
https://shop.ipc.org/                                                 202（需 JS）
https://www.iec.ch/dyn/www/f?p=103:20:...（curl 直接抓）                202 空body（需浏览器/WebFetch）
```

---

*报告完。全部 URL 均经本次实测或搜索索引确认；标注 `未核实` 者未取得一手证据，不得作为断言入库。*
