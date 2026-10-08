# Track 04 — Canon（半导体标准体系知识正典）

> **调研对象**：半导体标准体系骨架、层级关系、权威文献
> **目标读者**：功率半导体封装可靠性工程师（20 年经验 / 六西格玛黑带）
> **三大用途**：① 标准间引用关系　② 测试方法分类　③ 从标准编号反查内容
> **调研日期**：2026-10-05
> **信源分级**：本报告每条信息标注 `[一手]` / `[二手]` / `[推断]`，并给出 URL 与可信度（★★★★★ 最高）。
> **黑名单执行**：已排除知乎、微信公众号、百度百科、内容农场、AI 摘要站。检索过程中大量二手源命中，但均未采信为事实依据，仅在"矛盾记录"中留痕。

---

## 0. 执行摘要：本次调研的 6 个关键发现

| # | 发现 | 对用户的价值 |
|---|---|---|
| 1 | **AQG 324 全文可免费下载**（CC BY-ND），且已含完整引用标准表 + 寿命计算附录 | 直接解决"引用关系"诉求，无需付费 |
| 2 | **AQG 324 引用表里没有 UNECE R10 / RoHS / ELV / WEEE** —— 用户任务书的假设不成立 | 避免知识 OS 建错依赖边 |
| 3 | **AQG 324 的引用体系极其干净**：仅 IEC 60747 / 60749 / 60068 / 60664 + 仅 2 个 JEDEC + IATF 16949 | 是"车规层如何继承民用层"的实证样本 |
| 4 | **AQG 324 04.1/2025 新增 Annex SiC（规范性）+ 11 项 SiC 专属测试**，含 DGS/DRB/dyn. H3TRB | SiC 封装可靠性的现行正典 |
| 5 | **AQG 324 附录 II.D 内嵌 LESIT 功率循环寿命模型原文公式**（Coffin-Manson + Arrhenius + Bayerer 扩展式） | 用户最需要的可执行公式 |
| 6 | **IEC 62506 是加速模型的方法论总纲**，比 IEC 60749 更适合做知识 OS 的模型层根节点 | 修正了任务书中"60749 承载加速模型"的定位 |

**另检出 3 处任务书前提错误**（详见 §9）：MIL-STD-883 方法号、Harper 书名、IEC 60749-3 的范围。

---

## 1. 标准制定组织的角色分工与层级

### 1.1 JEDEC —— 器件与测试方法的行业主体标准

**组织性质** `[一手]`：JEDEC（Solid State Technology Association）是**行业协会主导的 ANSI 认可标准制定者（ASD）**，非政府机构。JEDEC 官方文件称其制定流程为五阶段：working group formation → ballot circulation → JEDEC Council approval → publication → revision cycles。

- 来源：https://www.jedec.org/ ｜可信度：★★★★★

**关键反直觉事实（重要）** `[一手]`：JEDEC 官方检索页显示，**JESD 才是"JEDEC Standards"（规范性标准，484 份），而 JEP 是"JEDEC Publications"（出版物，131 份，非规范性）**。JEDEC 文档搜索页的 Document Types 分类原文：

| 前缀 | JEDEC 官方类型名 | 数量 | 性质 |
|---|---|---|---|
| **JESD** | JEDEC Standards | 484 | 规范性标准 |
| **JEP** | JEDEC Publications | 131 | 出版物（信息性） |
| MO- | Microelectronic Outlines | 364 | 封装外形图 |
| TO- / DO- / SO- / CO- | Transistor / Diode / Socket / Carrier Outlines | 55/19/32/44 | 器件外形 |
| MS- | Microelectronic Standards | 34 | — |
| SPP- | Standard Practices and Procedures | 25 | — |
| DG- | Design Guideline | 15 | 设计指南 |

- 来源：https://www.jedec.org/standards-documents ｜可信度：★★★★★（官网 facet 计数实时数据）
- **`[推断]`** 数量为调研当日快照，会变动；分类口径以官网为准。

**JESD 编号的语义结构** `[二手，交叉验证]`：`JESD<委员会号>-<类型字母><序号>.<修订版>`。
例：`JESD22-A104F`（JC-22 委员会 / A 系列 / 104 号 / Rev F）、`JESD47I`（JC-47 / Rev I）、`JESD22-B120.01`。

> **JESD 编号如何产生（机制）** `[二手]`：JESD 的数字段**不由一个全局计数器分配，而是按「委员会号 + 类别字母」命名空间独立编排**。因此 `22-A104` 与 `22-B120` 是两个不同序列；`JESD47` 没有字母段（委员会级通用文件）。多个来源一致描述"提案 → motion → 委员会审议 → ballot（通常 2/3 多数）→ 理事会批准 → 发布"，周期约 1–3 年。
> - 来源（均为二手，仅作机制参考，不作事实依据）：grokipedia.com/page/JEDEC（AI 生成站，仅作对照）、memorysystemsauthority.com、kynix.com 博客
> - **`[推断]`** 上述"命名空间独立编排"可由 `JESD22-A104` 与 `JESD22-B120` 并存、以及 `JESD47` 无字母段这两个事实强力支撑，**置信度较高**，但未找到 JEDEC 官方明文规则。建议后续向 JEDEC 确认（§11 待办 T1）。

**对功率封装最相关的委员会** `[一手]`：JEDEC 官网 Committees 页原文：

| 委员会 | 官方名称与职责（原文摘录） |
|---|---|
| **JC-14** | Quality and Reliability of Solid State Products — 商业应用（计算机、汽车、电信）质量与可靠性方法学；含板级可靠性；与 IPC、IEC、JEITA 协调 |
| **JC-13** | Government Liaison — **军用、航天**及其他环境固态产品质量与可靠性方法学 |
| **JC-15** | Thermal Characterization Techniques for Semiconductor Packages — 封装热表征技术（测试+建模） |
| **JC-11** | Mechanical Standardization — JEP95 注册外形 |
| **JC-70** | Wide Bandgap Power Electronic Conversion Semiconductors — JEDEC **最新**主委员会，**含 2 个子委员会** |
| JC-10 | Terms, Definitions, and Symbols |
| JC-22 / JC-25 | Diodes and Thyristors / Transistors |
| JC-40 / JC-42 / JC-45 / JC-64 / JC-65 | 数字逻辑 / 存储器 / DRAM 模组 / 嵌入式存储 / RFID |
| JC-16 / JC-63 | 接口技术 / 多芯片封装 |

- 来源：https://www.jedec.org/committees ｜可信度：★★★★★
- **JC-14 子委员会** `[一手]`：JC-14.1 Reliability Test Methods for Packaged Devices、JC-14.2 Wafer-Level Reliability、JC-14.3 Silicon Devices Reliability Qualification and Monitoring、JC-14.4 Quality Processes and Methods、JC-14.7（2024 年新增）Radio Frequency Reliability and Quality Standards
  - 来源：https://www.jedec.org/committees/JC-14 ｜可信度：★★★★★
- **`[推断]`** **JC-14.1 是 JESD22 系列的归属委员会**。依据：官网 IPC/JEDEC-9702 页面明确标注 `Committee(s): JC-14.1`，而 9702 与 9701 同属封装互连力学测试。**JC-14.1 = 封装器件可靠性测试方法 = JESD22 的家**（待官方确认，待办 T1）

**免费 vs 付费** `[二手，多源一致]`：
- JEDEC 全部文档**注册后免费下载**（含 JESD、JEP、J-STD 联合标准）。
- 例外：`JESD22-B120.01`（Wire Bond Pull）等为付费；**Registered Outlines / JEP95** 部分需付费。
- IPC 标准多数需购买，少数免费。
- 来源：cedm.be/rohs-service/rohs-standards（二手汇编，但与 JEDEC 官网"免费注册"表述一致）｜可信度：★★★☆☆
- **`[推断]`** JEDEC 采取"免费开放 + 会员治理"模式（标准免费、投票权收费）。与 IEC/SEMI 的"标准付费"形成对比——这是三组织最根本的制度差异。

### 1.2 SEMI —— 制造、材料、设备、自动化

**组织沿革** `[二手]`：SEMI 前身 "Semiconductor Equipment and Materials Institute"，1970 年于 Palo Alto 由 55 家公司成立，最初目的是办半导体生产设备展；标准计划始于 1973 年；现总部加州 Milpitas。首个任务是为硅片直径达成一致。
- 来源：electronicsguide.net（二手）｜可信度：★★★☆☆
- **`[推断]`** 该沿革细节（55 家、1970、1973、80% 硅片合规率）**未在 semi.org 官方页面交叉验证**，标记为**未完全核实**（待办 T2）。

**SEMI 官方 Volumes 清单** `[一手]`：SEMI 官网 Standards 页列出的标准卷（volume）与前缀映射：

| 前缀 | Volume | 覆盖 |
|---|---|---|
| **S** | Safety Guidelines | 设备/气体/工艺 EHS 安全指南 |
| **E** | Equipment Automation Software & Hardware | SECS/GEM/GEM300/EDA |
| **A** | Automation Technology | SMT/PCBA 产线机机通信（PESCI/SMASH/PCBECI） |
| **F** | Facilities | 公用工程、超纯水、电压暂降耐受 |
| **M** | Materials | 晶圆规格、衬底尺寸、材料表征 |
| **MF** | Silicon Materials & Process Control | 硅材料测试方法 |
| **C** | Process Chemicals | 液态化学品纯度与规格 |
| **G** | **Packaging** | 封装（Cerdip、引线框架、键合、注塑材料） |
| **P** | Microlithography | 光掩模/光罩/ pellicle |
| **D** | Flat Panel Display | 平板显示 |
| **3D / MS** | 3D IC / MEMS | 3D 集成（TSV、TGV）、MEMS |
| **PV / HB / FH / T** | 光伏 / 高亮 LED / 柔性混合电子 / **Traceability** | — |

- 来源：https://www.semi.org/en/products-services/standards ｜可信度：★★★★★
- **SEMI 编号结构** `[一手]`：完整 designation = 前缀 + 数字 + `-` + **4 位「月份+年份」**。`SEMI F47-0706` = 2007 年 6 月版；`SEMI F42-0600` = 2000 年 6 月版；字母后缀 `a`/`b` 标记后续编辑/部分修订（`SEMI S2-0712a`）。
  - 来源：electronicsguide.net（描述具体，但**未在 semi.org 逐条验证**）｜可信度：★★★☆☆
  - **`[推断]`** 但从 SEMI 官网商店实际条目可交叉印证：搜索结果中出现 `SEMI 3D24`、`SEMI E190.1`、`SEMI 3D1`、`SEMI E191.1` 等，确认"数字+后缀"结构成立。可信度：★★★★☆

**对功率封装最相关的 SEMI 封装标准** `[一手]`：SEMI 先进封装页面列出的 Packaging 系列：

- `SEMI G1` Specification for Cerdip Package Constructions
- `SEMI G3` Specification for Sidebrazed Laminates
- `SEMI G4` Specification for IC Leadframe Materials Used in the Production of Stamped Leadframes
- `SEMI G8` Test Method for Gold Plating
- `SEMI G9` Specification for Stamped Leadframes for Plastic Molded Dual-in-Line Semiconductor Packages
- `SEMI G10` Standard Method for Mechanical Measurement of Plastic Package Leadframes
- `SEMI G14` Guideline for Specifying Dimensions and Tolerances Used to Manufacture Plastic Molded DIP Package Tooling
- `SEMI G99` Specification for Flowability of Encapsulation Materials for Wafer Level Packaging and Panel Level Packaging
- 3D 集成：`SEMI 3D1`（TSV 几何计量术语）、`SEMI 3D6`（CMP 与微凸点 TSV 工艺指南）、`SEMI 3D11`（TGV 术语）、`SEMI 3D12`、`SEMI 3D22`、`SEMI 3D24`（RDL 剥离测试）
- 宽禁带：`SEMI M92`（4H-SiC 同质外延晶圆）、`SEMI M94`（SiC 工程衬底）、`SEMI M93`（4H-SiC 基面位错密度 XRD 测定）
- 自动化：`SEMI E181/E182`（Panel FOUP / Loadport，面板级封装）、`SEMI E199`（300mm Film Frame FOUP）
- **SECS/GEM 家族** `[一手]`：`SEMI E5`（SECS-II）、`SEMI E30`（GEM）、`SEMI E37`（HSMS）、`SEMI E87`（CMS）、`SEMI E90`（EEM）、`SEMI E94`（Control Job Management）、`SEMI E120`（CEM）、`SEMI E134`（EDA 数据采集）、`SEMI E148`（时间同步）、`SEMI E168`（OEE）、`SEMI E190`（EDP 设备数据发布）、`SEMI E10`（RAM 与设备利用率）
  - 来源：https://www.semi.org/cn/industry-groups/advanced-packaging/standards ｜https://store-us.semi.org/collections/latest-standards-1 ｜https://www.semi.org/en/products-services/standards/top-10-standards ｜可信度：★★★★★
- **SEMI G1–G5 ≠ 湿电子化学品等级** ⚠️ `[二手，重要纠错]`：中文内容农场广泛传播"SEMI G1~G5 是湿电子化学品纯度等级"。**这是错误的**——SEMI 官网证实 **G 系列是封装（Packaging）标准卷**，而湿电子化学品等级对应的是 **C 系列（Process Chemicals）**。该错误说法出现在 toutiao.com（内容农场，黑名单）。
  - 反证：https://www.semi.org/en/products-services/standards（C/F 才是化学品）｜可信度：★★★★★（反证）
  - **`[推断]`** 化学品纯度等级在 SEMI 体系中确实存在类似 G1–G5 的说法，但**归属卷号需进一步核实**。⚠️ 该"混淆"本身是有价值的发现：中文语料中此错误传播极广，知识 OS 应显式标注为反例。

### 1.3 IEC —— 国际标准层（最正式，但需付费）

**TC 47 结构** `[一手]`：IEC 官方目录（webstore.iec.ch）显示：

| 委员会 | 名称 | 覆盖 |
|---|---|---|
| **TC 47** | Semiconductor devices | 母委员会 |
| SC 47A | Integrated circuits | 模拟 IC：运放、音频/视频放大器、RF/IF、电压/电流调节器、模拟开关 |
| **SC 47D** | **Semiconductor devices packaging** | 封装 |
| **SC 47E** | Discrete semiconductor devices | 分立器件 |
| SC 47F | Micro-electromechanical systems | MEMS |
| **TC 49** | Piezoelectric, dielectric and electrostatic devices and associated materials for frequency control, selection and detection | 压电/介质器件 |
| TC 48 | Electrical connectors and mechanical structures | 连接器 |
| TC 56 | **Dependability** | **可靠性/加速试验方法学总纲** |

- 来源：https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1251 ｜ https://webstore.iec.ch/searchform&q=IEC%2060335-2-7 ｜可信度：★★★★★
- **TC 47 范围边界** `[一手]`：JSA（Japan Standards Association）官方 IEC 委员会清单记载 TC 47 范围含"晶圆级可靠性、**半导体封装概述**、术语定义、质量管理、物理环境试验方法、单体半导体试验方法、器件规格、接口要求及应用"，并**明确排除**：无源元件（TC40）、光伏（TC82）、TC22/TC86/JTC1 领域器件、光纤通信光电子器件（TC86）。
  - 来源：https://webdesk.jsa.or.jp/pdf/dev/md_4791.pdf ｜可信度：★★★★★
  - **`[推断]`** 该排除条款解释了"为什么功率模块焊点疲劳不在 TC 47 范围"——功率模块级可靠性由 **TC 47/SC 47D + SC 47E** 承担，而**焊点/互连疲劳寿命模型主要落在 TC 56（Dependability）与 TC 82/行业指南**，而非 60749。这是层级模型的关键节点。

**IEC 60749 系列结构（半导体器件机械与气候试验方法）** `[一手]`：来自 IEC 官方 TC 47 出版物列表，**这是本报告最可靠的结构化数据之一**：

| 部分 | 标题 | 版本/日期 |
|---|---|---|
| **60749-1** | General | 2002-08-30 Ed 1.0（含 COR1 2003、AMD1 2010） |
| **60749-2** | Low air pressure | 2002-04-12 Ed 1.0 |
| **60749-3** | **External visual examination** | **2017-03-03 Ed 2.0** |
| **60749-4** | Damp heat, steady state, **highly accelerated stress test (HAST)** | 2017-03-03 Ed 2.0 |
| **60749-5** | **Steady-state temperature humidity bias life test** | 2023-12-19 **Ed 3.0** |
| **60749-6** | Storage at high temperature | 2017-03-03 Ed 2.0 |
| **60749-7** | Internal moisture content measurement and the analysis of other residual gases | **2025-11-27 Ed 3.0** |
| **60749-8** | Sealing | 2002-08-30 Ed 1.0 |
| **60749-9** | Permanence of marking | 2017-03-03 Ed 2.0 |
| **60749-10** | Mechanical shock — device and subassembly | 2022-04-27 Ed 2.0 |
| **60749-11** | Rapid change of temperature — **Two-fluid-bath** method | 2002-04-12 Ed 1.0 |
| **60749-12** | Vibration | 2017-12-13 Ed 2.0 |

- 来源：https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1251 ｜可信度：★★★★★
- **其他被引证的 60749 部分** `[一手，来自 AQG 324 引用表]`：`-23` High temperature operating life (2011)、`-25` Temperature cycling (2003)、`-34` Power cycling (2010/2011)
- ⚠️ **矛盾记录**：`60749-25` 与 `60749-34` 的版本年在不同来源间不一致：AQG 324 02.1/2019 与 04.1/2025 引用表均写 `IEC 60749-25:2003` 与 `IEC 60749-34:2010`，但 AQG 324 **正文**引用时写 `IEC 60749-34:2011`。**同一份标准内部不一致**（引用表 2010 vs 正文 2011）。保留矛盾，不和稀泥。
- **`[推断]`** 极可能是 2010 版发布后于 2011 年出corrigendum 或再版，AQG 324 引用表沿用初版年、正文沿用最新年。**待办 T3**。
- ⚠️ **`60749-3` 不是加速试验**，而是"外观检查"。任务书若把 60749-3 当作加速模型章节会出错（详见 §9）。
- ⚠️ `60749-4` 官方标题包含 "Damp heat, **steady state**, highly accelerated stress test (HAST)"，而 60749-5 是 "**Steady-state** temperature humidity bias"。**两者的措辞高度相似但分工不同**，是常见的编号混淆点。

**IEC 60747 系列（分立器件族层）** `[一手，来自 AQG 324 引用表]`：
- `IEC 60747-1` General｜`60747-2` Discrete devices – Rectifier diodes (2016)｜`60747-8` Field-effect transistors (2010)｜`60747-9` Insulated-gate bipolar transistors (IGBTs) (2007)｜`60747-15` **Isolated power semiconductor devices** (2010/2012)

**IEC 60748 系列（集成电路）** `[一手]`：IEC 官方 SC 47A 页面显示 `IEC 60748-3:1986` Analog integrated circuits（含 AMD1:1991、AMD2:1994，ED2 修订中），并明确"应与 IEC 60747-1 和 60748-1 配合使用"。
- 来源：https://iectest.iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID,FSP_APEX_PAGE,FSP_PROJECT_ID:1368,23,5448 ｜可信度：★★★★★

**IEC 60068 系列（基础环境试验层）** `[一手 + 二手]`：
- **编号机制** `[一手]`，以中国国标等同采用件佐证：`GB/T 2423.22-2002/IEC 60068-2-14:1984` 全文标题"电工电子产品环境试验 第2部分：试验方法 试验N：温度变化"，其中明确细分：
  - **试验 Na** —— 规定转换时间的快速温度变化（双箱转移）
  - **试验 Nb** —— 规定变化速率的温度变化（单箱斜坡）
  - **试验 Nc** —— 快速温度变化**两液槽法**
  - 来源：chinahls.cn 公开的 GB/T 2423.22-2002 全文 PDF ｜可信度：★★★★★（国标原文）
- **字母代号表** `[二手，多源交叉]`：

| 试验 | 名称 | 编号 |
|---|---|---|
| A | Cold | 60068-2-1 |
| B | Dry heat | 60068-2-2 |
| N | Change of temperature | 60068-2-14（Na/Nb/Nc） |
| Ca → **Cab** | Damp heat steady state | 60068-2-3（被 **60068-2-78** 取代） |
| Db | Damp heat, cyclic (12+12h) | 60068-2-30 |
| Z/AD | Composite temp/humidity cyclic | 60068-2-38 |
| Fc | Vibration (sinusoidal) | 60068-2-6 |
| Fh | Vibration, broadband random | 60068-2-64 |
| Ea | Shock | 60068-2-27 |
| Eb | Bump | 60068-2-29 |
| Fi | Vibration, mixed mode | 60068-2-80 |
| Ec | Rough handling (drop) | 60068-2-31 |
| Ka | Salt mist | 60068-2-11 |
| Kb | Salt mist, cyclic | 60068-2-52 |
| Kc | Sulphur dioxide | 60068-2-42 |
| R | Water | 60068-2-18 |
| L | Dust and sand | 60068-2-68 |
| T | Soldering | 60068-2-20 |
| U | Robustness of terminations | 60068-2-21 |
| Td | Solderability / resistance to dissolution of metallization | 60068-2-58 |

- 来源：megalabinc.com（二手，实验室，服务商）｜enstandards.com 某标准引用清单（一手：真实标准引用列表）｜可信度：★★★☆☆
- **`[推断]`** `60068-2-3 (Ca)` 已被 `60068-2-78 (Cab)` 取代是可靠结论（多源一致 + "Ca→Cab"命名演进的逻辑一致）。**反查编号时的实用价值**：老资料里的 "Test Ca" 必须映射到 60068-2-78。

### 1.4 AQG 324（车规功率模块层）—— 本报告的一手核心

**归属关系（用户任务书表述需修正）** `[一手]`：**AQG 324 由 ECPE（European Center for Power Electronics e.V.）主导制定与持有，不是 ZVEI 牵头。** AQG 324 原文 Preface 与版权页：

> "The original version is based on the supply specification **LV 324** which has been developed by German automotive OEMs together with representatives from the power electronics supplier industry in a joint working group of **ECPE and the German ZVEI association**."
> "The ECPE Guideline **AQG 324 is owned by ECPE** European Center for Power Electronics e.V."
> 联系方式：ECPE e.V., Dipl.-Phys. Thomas Harder, Nuremberg, Germany

- 来源：ECPE 官方 PDF（04.1/2025，110 页）｜可信度：★★★★★
- **ECPE 工作组沿革** `[一手]`：AQG 324 工作组成立于 **2017 年 6 月**，基于德国 LV 324 制定；首个正式版本 2018-04-12。
  - 来源：https://www.ecpe.org/research/working-groups/ ｜https://www.ecpe.org/research/working-groups/automotive-aqg-324/ ｜可信度：★★★★★
- **LV 324 的车企映射** `[一手，来自 AQG 324 附录 II.D 文献[2]]`：
  > "LV324: Qualification of Power Electronics Modules for Use in Motor Vehicle Components, General Requirements, Test Conditions and Tests, **supplier portal of BMW: GS 95035, VW: VW 82324 Group Standard, Daimler**, 2014"
  - **`[推断]`** LV 324 是德系车企联合采购规范，故 AQG 324 的实质约束力来自 **BMW GS 95035 / VW 82324 / Daimler 采购条款**，而非标准本身。这解释了为何 AQG 324 被称为"上车门槛"。

**版本谱系（已下载全部正式版本）** `[一手]`：

| 版本 | 发布日期 | 页数 | 状态 |
|---|---|---|---|
| V01.00 | 2018-04-12 | 70 | 首发（Intro-presentation 存于 ECPE） |
| **02.1/2019** | **2019-05-15** | **70** | ✅ 本地已下载并全文解析 |
| 03.1/2021 | 2021-05-31 | 71 | ✅ 本地已下载 |
| **04.1/2025** | **封面写 2025-03-31** | **110** | ✅ **最新版**，本地已下载并全文解析 |

- 来源：ECPE 官方下载区（token 化直链，调研日抓取）｜可信度：★★★★★
- ⚠️ **矛盾记录（保留）**：ECPE 网页文本称 04.1/2025 为 "**from 24 April 2025**"，但 PDF 封面与版权页写 "Release date: **31.03.2025**"。**同一组织的网页与文件日期不一致**。实务影响：引用时建议只写 "Release 04.1/2025"，避免写具体日期。二手源（pmarketresearch）称 "April 2025"，与网页一致但与 PDF 不一致。

**适用范围（判定边界，重要）** `[一手，04.1/2025 第1章原文]`：
- 适用于 **PCU（Power Electronics Converter Unit）中的功率电子模块**，用于 **总重 ≤ 3.5 t 的机动车**
- 明确**不覆盖**：芯片本身的资格、工艺过程资格
- 明确**不替代**整机 PCU 的资格试验
- 关键原则 `[一手]`：若某项试验不适用于特定设计，**供应商必须向客户说明不适用的理由**（"to be agreed with the customer" 贯穿全文）

**04.1/2025 的架构突破：Base Document + Annex 架构** `[一手]`：

```
AQG 324 Release 04.1/2025
├─ 正文（Base Document）—— 面向 Si 功率模块的通用要求
│   ├─ 6  QM-01 Module test（栅参数、漏电流、正向电压、X-ray/SAM、IPI/VI、OMA）
│   ├─ 7  QC-01~05（杂散电感 Lp、热阻 Rth、短路耐量、绝缘、机械参数）
│   ├─ 8  QE-01~04（TST / CO / V / MS）
│   └─ 9  QL-01~07（PCsec / PCmin / HTS / LTS / HTRB / HTGB / H3TRB）
├─ Annex SiC（规范性 / normative）—— SiC 专属，p.74-108
│   └─ QL-08 HTFB、QL-09 DGS、QL-10 DRB、QL-11 dyn. H3TRB（新增 4 项）
├─ Annex GaN —— 占位，"to be added in a future release"
├─ Annex I（规范性补充）：I.A 试验流程图 / I.B Delta 资格矩阵 / I.C 试验文件化
└─ Annex II（信息性补充）：II.A 变更跟踪 / II.B 参考文献 /
    II.C 物理分析典型要点 / II.D 功率模块寿命计算指南 ← ★
```
- 来源：04.1/2025 目录（p.4-5）｜可信度：★★★★★
- **02.1/2019 → 04.1/2025 的关键演进** `[一手 + 二手]`：
  - 新增 `IATF 16949`（质量体系）进入引用表 `[一手]`
  - 新增 `JESD22-A104F:2020`（温度循环，取代 2019 版仅引 `JESD22-A119:2015` 低温存储）`[一手]`
  - 引入 **Annex I.B "Delta qualification matrix"**（增量资格矩阵）`[一手]`
  - 新增 Annex SiC（规范性）+ 4 项 SiC 专属寿命测试 `[一手]`
  - 二手源称新增共 11 项 SiC 测试条件、新增 DGS/DRB/dyn. H3TRB、功率循环细化为"秒级/分钟级"双模式 `[二手]`（eet-china.com、matek.com —— 均为技术媒体/营销内容，可信度★★☆☆☆，**但与一手 PDF 目录吻合**）
    - 来源：https://www.eet-china.com/mp/a406501.html ｜https://www.matek.com/techarticle-detail/20250501

**⭐ 引用关系实证：AQG 324 04.1/2025 正文第 3 章完整引用表** `[一手]`：

| 标准 | 年份 | 在 AQG 324 中的角色 |
|---|---|---|
| **IATF 16949** | — | 汽车质量管理体系（**04.1 新增**） |
| ISO/IEC 17025 | — | 实验室能力要求 |
| IEC 60747-2 | 2016 | 整流二极管 |
| IEC 60747-8 | 2010 | 场效应晶体管 |
| IEC 60747-9 | 2007 | IGBT |
| IEC 60747-15 | 2010/2012 | **隔离型功率半导体器件**（热阻、杂散电感测量的方法学母标准） |
| IEC 60749-5 | 2017 | 稳态温湿偏压寿命（THB/85-85） |
| IEC 60749-6 | 2017 | 高温存储 |
| IEC 60749-23 | 2011 | 高温工作寿命 |
| IEC 60749-25 | 2003 | **温度循环** |
| IEC 60749-34 | 2010 | **功率循环**（PCsec/PCmin 的方法学母标准） |
| IEC 60068-2-6 | 2007 | 正弦振动 Fc |
| IEC 60068-2-27 | 2008 | 冲击 Ea |
| IEC 60068-2-64 | 2008 | 宽带随机振动 Fh |
| IEC 60664-1 | 2007 | 低压系统绝缘配合 |
| DIN EN 60664-1 Addendum 1 | — | 等同 IEC/TR 60664-2-1:2011 |
| IEC 60664-4 | 2005 | 高频电压应力 |
| **JESD22-A104F** | 2020 | 温度循环（**唯一 JEDEC 测试方法**） |
| **JESD22-A119** | 2015 | 低温存储寿命（**唯一第二 JEDEC 文件**） |

**Annex SiC 引用表（新增，5 份 JEDEC JEP）** `[一手]`：

| 标准 | 日期 | 主题 |
|---|---|---|
| **JEDEC JEP183** | 2021-01 | SiC MOSFET 阈值电压 (VT) 测量指南 |
| **JEDEC JEP184** | 2021-03 | SiC MOS 器件 BTI 评估指南 |
| **JEDEC JEP190** | 2022-08 | SiC 功率器件 dV/dt 鲁棒性评估 |
| **JEDEC JEP195** | 2023-02 | SiC MOS 器件栅极开关不稳定性评估 |
| **JEDEC JEP197** | 2023-11 | SiC 功率器件双极退化（Bipolar Degradation）评估 |

- 来源：04.1/2025 第 76 页｜可信度：★★★★★

> ### 🔑 关键发现（对用户的核心价值）
>
> **1. 用户任务书的法规锚点假设不成立。**
> 我对 04.1/2025 与 02.1/2019 全文做了 UNECE / R10 / RoHS / ELV / WEEE / Regulation / 2011/65 全文正则检索，**结果全部为 "No matches found"**（`[一手]`，grep 全文 6580 行）。**AQG 324 完全不引用 UNECE R10，也不引用 RoHS/ELV/WEEE。**
> AQG 324 引用的是 **IATF 16949**（质量体系）+ **ISO/IEC 17025**（实验室能力），属于"合同/质量"锚点，**不是"法规"锚点**。
> - **`[推断]`** 原因：EMC 与有害物质合规属于整车/OEM 层面义务，落在 UNECE R10 与 EU 指令框架（RoHS 2011/65/EU、WEEE 2012/19/EU、ELV 2000/53/EC），不属于 ECPE 工作组职权。AQG 324 解决的是"模块级可靠性验证方法"，与"型式认证"是两条正交线。
> - **UNECE R10 本身已核实** `[一手]`：全称 *Uniform provisions concerning the approval of vehicles with regard to electromagnetic compatibility*，适用于 **L/M/N/O 类车辆**的 EMC 认证，涵盖辐射/传导发射与抗扰度，附录 1 为"本法规引用标准清单"（List of standards referred to in this Regulation），16 个附件含具体测量方法。
>   - 来源：https://digitallibrary.un.org/record/248143/files/E_ECE_324_Add.9_Rev.2_E_ECE_TRANS_505_Add.9_Rev.2-EN.pdf ｜https://urlausnir.is/skrar/.../Stjórnartiðindi_ESB_2017_L041_EN.pdf ｜可信度：★★★★★
>   - **`[推断]`** **UNECE R10 附录 1 才是"标准引用清单"的正确位置**——若要建"法规→标准"映射，应从 R10 附录 1 反查其引用的 ISO/CISPR/IEC 25 系列标准，而不是从 AQG 324 反查。这是知识 OS 应修正的架构。
>
> **2. AQG 324 只引用 2 份 JEDEC 文件。** 02.1/2019 仅 1 份（`JESD22-A119`）；04.1/2025 增至 2 份（+`JESD22-A104F`）+ 5 份 JEP（Annex SiC）。
> - **`[推断]`** **这直接证伪了"车规层=JEDEC+法规"的常见叙事**。车规层的实体是 **IEC 主导**（14 份 IEC vs 2 份 JEDEC），AESG/Q 只是"选配 + 加严 + 模块级视角"，而非标准体系的转述。这是**体系建模的关键洞察**。

### 1.5 AEC（汽车电子委员会）—— 与 AQG 324 的关系

**组织与文件谱系** `[一手/二手混合，AEC 官网已不可直接抓取]`：
- AEC（Automotive Electronics Council）由 **Chrysler / Ford / General Motors** 于 1990 年代初期建立
- 现行文件：`AEC-Q100`（IC，**Rev H** 基准文件）、`AEC-Q101`（分立半导体，**Rev E**）、`AEC-Q102`（分立光电器件，**Rev A**）、`AEC-Q103`（MEMS 传感器，**Rev -**）、`AEC-Q104`（MCM/多芯片模块，**Rev -**）、`AEC-Q200`（无源元件，**Rev D**）
- 子文件：`AEC-Q100-001` Rev C Wire Bond Shear、`-002` Rev E HBM ESD、`-003` Rev E MM ESD、`-004` Rev D IC Latch-Up、`-005` Rev D1 NVM endurance、`-006` Rev D Electro-Thermally Induced Parasitic Gate Leakage (GL)、`-007` Rev B Fault Simulation & Test Grading、`-008` Rev A ELFR、`-009` Rev B Electrical Distribution Assessment、`-010` Rev A Solder Ball Shear、`-011` Rev C1 CDM ESD、`-012` Short Circuit Reliability Characterization of Smart Power Devices for 12V Systems
- 指南类：`AEC-Q001` Rev D Part Average Testing、`-Q002` Rev B Statistical Yield Analysis、`-Q003` Rev A Electrical Performance Characterization、`-Q004` Zero Defects Guideline、`-Q005` Rev A Pb-Free Test Requirements、`-Q006` Rev A Qualification Requirements for Components using Copper (Cu) Wire Interconnects
- 来源：aecouncil.com 文档页（**本次抓取失败**）；文档清单经 m.blog.naver.com/rion840915 转录（★★☆☆☆，为个人博客转录）｜可信度：★★☆☆☆
- ⚠️ **标注为"未完全核实"**：AEC 各文件 Rev 号来自二手转录，**AEC 官网本次无法访问（fetch failed）**。**待办 T4**：用户若需精确 Rev 号，须自行访问 aecouncil.com/AECDocuments.html 核对。
- **`[推断]`** AEC-Q100-003（MM ESD）已被标记 [Decommissioned]；AEC-Q100-002（HBM）亦标记 [Decommissioned] —— 因 JEDEC 与 ESDA 联合发布的 **JS-001（HBM）/ JS-002（CDM）** 已成为现行替代版本。JEDEC 官网确认 `JS-001-2024`（2024-10）由 **JEDEC/ESDA 联合**发布，归属 **JC-14**。
  - 来源：https://www.jedec.org/committees/JC-14 ｜可信度：★★★★★
  - **`[推断]`** 因此"AEC vs JEDEC"不是替代关系而是**分工**：AEC 定义车规资格框架与附加项，ESD/锁存等具体方法已回归 JEDEC-ESDA 联合标准（JS 系列）。

**AEC 与 AQG 324 的叠加关系** `[推断，证据中等]`：
- AQG 324 **不引用 AEC**（全文引用表已证实）
- 二者定位不同：AEC-Q100/Q101 针对**芯片/分立器件**；AQG 324 针对**模块级**，且明确声明"不覆盖芯片本身的资格"
- **`[推断]`** 实践上二者**并行要求**：芯片级过 AEC-Q101/Q100，模块级过 AQG 324。这是"叠加"而非"继承"。

### 1.6 军用 / 航天 / 中国国标与国军标

**MIL-STD-883（微电路试验方法标准）** `[一手，NASA NEPP 托管的官方 PDF]`：
- **结构**：五大部分。**方法号按类别分**：
  - **1000 系列 环境试验**：1001 低气压(高度)、1002 浸渍、1003 绝缘电阻、1004 湿度电阻、1005 稳态寿命、1006 间歇寿命、1007 老化寿命、1008 稳定化烘烤、1009 盐雾腐蚀、**1010 温度循环**、**1011 热冲击**、1012 热特性、1013 露点、1014 密封、1015 老化(burn-in)、1016 寿命/可靠性特性、1017 中子辐照、1018 内部气体分析、1019 总剂量电离辐射、1020 剂量率诱发闩锁、1021 剂量率 upset、1022 MOSFET 阈值电压、1023 线性电路剂量率响应、1030 密封前老化、1031 薄膜腐蚀、1032 α 粒子软错误、1033 耐久寿命、1034 染色渗透
  - **2000 系列 力学试验**：2001 恒定加速度、2002 机械冲击、2003 可焊性、2004 引线完整性、2005 振动疲劳、2006 振动噪声、2007 变频振动、2008 外观与机械、2009 外部目检、2010 内部目检、2011 键合强度(破坏性键合拉力)、2012 射线照相、2013 DPA 内部目检、2014 内部目检与机械、2015 耐溶剂、2016 物理尺寸、2017 混合电路内部目检、2018 金属化 SEM 检查、2019 芯片剪切强度、2020 颗粒撞击噪声检测、2021 玻璃化层完整性、2022 润湿天平可焊性、2023 非破坏键合拉力、2024 玻璃釉封装盖扭矩、2025 引脚镀层附着力、2026 随机振动、2027 衬底附着强度、2028 PIN 封装破坏性引线拉力、2029 陶瓷芯片载体键合强度、2030 芯片附着超声检查、2031 倒装芯片剥离、2032 无源元件目检、2035 TAB 键合超声检查、2036 耐焊接热
  - 3000 系列 电学、5000 系列 检验程序（GJB 548C 亦采此 4 段式）
- **版本沿革** `[一手]`：
  - MIL-STD-883**F**（2004-06）—— 单一文档，方法号带 .N 修订后缀（如 `1004.7`、`1010.8`、`1015.9`）
  - MIL-STD-883**K**（2018-05 change 3）起**拆分为多部分**（Part 1 = 方法 1000-1999 等）
  - MIL-STD-883**L**（2019-09）Part 1，AMSC N/AFSC 5962
- 来源：https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf （883F 全文）｜https://www.iclabcn.com/media/MIL-STD-883L-1-2019...pdf （883L Part 1 全文）｜可信度：★★★★★（DoD 官方文件，第三方镜像）
- ⚠️ **对任务书的重要纠正**：任务书写 "MIL-STD-883 方法号（1015.9 温循等）" —— **1015 是 burn-in（老化），1010 才是 Temperature Cycling（温度循环）**；`1015.9` 中的 `.9` 是 burn-in 方法的修订号，不是温循。温度循环是 **`1010.x`**。此错误若写入知识 OS 将持续污染检索。
- **MIL-STD-883 三大目标** `[一手，883L 原文 §1.1 精神]`：① 给出等效于现场服役条件且可复现的实验室条件；② 把各军种与 NASA 规范中同类方法合并到一份标准以节约设备/工时；③ 提供物理/电气/环境测试与制造控制的一致性水平。
- **适用范围** `[一手]`：仅适用于**微电子器件**（单片、多片、膜电路、混合电路、微电路阵列及其元件）。**分立半导体由 MIL-STD-750 覆盖**（"It does not cover discrete semiconductors (which fall under MIL-STD-750)"）
  - 来源：pcbsync.com（二手）｜可信度：★★★☆☆
  - **`[推断]`** 该边界与 GJB 体系完全对应：**GJB 548（微电子器件）vs GJB 128（半导体分立器件）**——这是中美军标体系的镜像结构。

**MIL-STD-1500 / 其他** `[未核实]`：MIL-STD-1500（封装相关）与 MIL-STD-202、810、1344、EIA-TIA-455 等在实验室转述中被并列提及，但**本次未取得一手文件，其准确范围与现行版本未核实**。标为**未核实**（待办 T5）。

**GJB / GB 体系** `[二手，检测机构公开目录，跨源一致]`：

| 标准 | 名称 | 备注 |
|---|---|---|
| **GJB 548A/B/C** | 微电子器件试验方法和程序 | **A(1996) 71 项 → B(2005) 74 项 → C(2021) 78 项** |
| GJB 128A(1997) / **GJB 128B(2021)** | 半导体分立器件试验方法 | 方法 1071 密封 |
| GJB 360A/B | 电子及电气元件试验方法 | 含温度冲击试验 |
| GJB 597A | 半导体集成电路总规范 | |
| GJB 1420A | 半导体集成电路外壳总规范 | |
| GJB 3157 | 半导体分立器件失效分析方法和程序 | |
| GJB 3233 | 半导体集成电路失效分析程序和方法 | |
| GJB 5914 | 各种质量等级军用半导体器件破坏性物理分析方法 | |
| GJB 4027B-2021 | 军用电子元器件破坏性物理分析方法 | |
| **GJB 7677-2012** | **Ball Grid Array (BGA) 试验方法** | ⚡ 与封装直接相关 |
| GJB 1217A | 电连接器试验方法 | |
| **GB/T 2423.x** | 电工电子产品环境试验（等同采用 IEC 60068-2-x） | 例：GB/T 2423.22-2002 = IEC 60068-2-14:1984 |
| GB/T 4023 | 半导体器件 分立器件 整流二极管 | |
| GB/T 4586 | 半导体器件 分立器件 第8部分：场效应晶体管 | |
| GB/T 4587 | 半导体分立器件和集成电路 第7部分：双极型晶体管 | |
| GB/T 17574 | 半导体器件 集成电路 第2部分：数字集成电路 | |
| GB/T 6798 | 半导体集成电路 电压比较器测试方法的基本原理 | |
| GB/T 4589 / GB/T 13580 | （用户任务书提及，**本次未核实**） | ⚠️ 见下 |

- 来源：iclab-cn.com、gts-lab.cn、iclabcn.com/standard/1665.html、en.iclabcn.com/news/enzlxz/（均为检测机构公开目录）｜可信度：★★★☆☆
- **`[一手]`** GJB 548C-2021 起草单位：工业和信息化部电子第四研究院、北京航空航天大学、CETC 24/43/55 所、航天科技 9 院 771/772 所、济南市半导体元件实验所
  - 试验项分布：气候环境试验 1000 系列 **28 项**、机械环境试验 2000 系列 **35 项**、电学试验 3000 系列 **2 项**、检验程序 5000 系列 **13 项**
  - 相比 B 版新增 4 项：2036 耐焊接热、2037 铅锡焊料成分分析-X 射线荧光检测、2038 焊柱阵列封装破坏性引线拉力、3023 集成电路锁定
  - 来源：http://iclabcn.com/standard/1665.html ｜https://unibright.com.cn/industry/189.html ｜可信度：★★★☆☆
- ⚠️ **未核实**：任务书提及的 **GB/T 4589、GB/T 13580、MIL-STD-1500** 本次**未取得一手来源**，标准号与现行版本**未核实**，不建议直接写入知识 OS。GB/T 4589 在检索中仅以"GB/T 4586 / 4587"相邻编号形式出现。
- **`[推断]`** **GB/T 2423 系列 = IEC 60068 系列的国标等同采用版**（已由 GB/T 2423.22-2002 = IEC 60068-2-14:1984 证实）。这意味着中国标准体系与国际体系是**映射关系而非并列关系**——知识 OS 应建"等同采用"边（identical adoption），而非"引用"边。

### 1.7 IPC（电子封装与装配标准）

**IPC 在标准体系中的位置** `[一手]`：IPC（Association Connecting Electronics Industries）是**电子组装（electronics assembly）与 PCB 产业**的标准主体，与 JEDEC 通过 **J-STD** 和 **IPC/JEDEC-xxx** 联合发布标准。

**IPC 标准树（官方 PDF）** `[一手]`：https://www.ipc.org/4.0_Knowledge/4.1_Standards/SimplifiedSpecTree.pdf
按类别（节选与可靠性/封装相关者）：

| 类别 | 标准 |
|---|---|
| **ASSEMBLY SUPPORT**（含力学/可靠性） | **IPC-9701**、**IPC/JEDEC-9702**、IPC/JEDEC-9703、-9704、-9706、-9707、IPC-9708、IPC-9709、IPC-9850、-9851、IPC-7801、IPC-7711/7721、IPC-7525~7530 |
| **COMPONENTS** | **J-STD-020**（MSL）、J-STD-075、IPC-9501~9504、IPC-9591、-9592 |
| **ACCEPTANCE** | IPC-A-610、IPC-A-600、IPC-9191、IPC-A-640、IPC-DRM-SMT |
| **ASSEMBLY** | **J-STD-001**、IPC-9261、IPC-7912 |
| **JOINING**（IPC-7091~7095 系列：BGA/QFN/底部填充等） | IPC-7091~7095 |
| PACKAGES | IPC-SM-784、J-STD-026、J-STD-028 |
| 焊接/助焊剂 | J-STD-004、J-STD-005、J-STD-006、J-STD-030 |

- 可信度：★★★★★

**关键联合标准** `[一手]`：
- **IPC/JEDEC-9702** = *Monotonic Bend Characterization of Board-Level Interconnects*，发布 **2004-06**，含 **Addendum 1 (2015-05，2016-08-15 重发)**，归属委员会 **JC-14.1**。原文明确："This publication specifies a common method of establishing the **fracture resistance of board-level device interconnects to flexural loading** during non-cyclic board assembly and test operations. **Monotonic bend test qualification pass/fail requirements are typically specific to each device application and are outside the scope of this document.**"
  - 来源：https://www.jedec.org/standards-documents/docs/js-9702 ｜可信度：★★★★★
- **J-STD-020** = *Moisture/Reflow Sensitivity Classification for Nonhermetic Solid State Surface Mount Devices*（IPC/JEDEC 联合）→ 即 **MSL 分级**
- **J-STD-033D** = *Handling, Packing, Shipping and Use of Moisture, Reflow, and Process Sensitive Devices*，发布 **2018-03-01**，32 页。原文含工程性信息：程序提供 **自封装日起 12 个月最短保存期**（前提是正确实施）
  - 来源：https://www.techstandardstore.com/product/ipc-j-std-033d ｜可信度：★★★☆☆
- **J-STD-609** = Marking, Symbols, and Labels of Leaded and Lead-Free Terminal Finished Materials（现行为 **J-STD-609C.01, 2024-04**，归属 JC-14）`[一手，JEDEC JC-14 页面]`
- **RoHS/WEEE 相关交叉标准** `[二手汇编，cedm.be]`：IPC-1066（无铅标识）、IPC-175X（声明过程管理，免费）、IPC-9503（非 IC 器件 MSL）、JIG-101（材料成分声明）、**JESD 97**（无铅标识）、**JESD 201**（锡须环境接受要求）、**JESD22-A121.01**（锡须生长测量）、**JP002**（JEDEC/IPC 锡须理论与缓解指南）、**IECQ QC 080000**（HSPM 有害物质过程管理）
  - 来源：https://www.cedm.be/rohs-service/rohs-standards ｜可信度：★★★☆☆
  - **`[推断]`** **这才是"RoHS/ELV/WEEE 合规锚点"的真实位置**——不是 AQG 324，而是 **IPC-175X + IECQ QC 080000 + JESD 97** 这一组。知识 OS 应把这组作为"环境合规层"的根节点。

**VSME / Intel / Infineon / ST 企业标准** `[未核实]`：
- **VSME（Vienna Systems Measurement Europe）** 确为功率模块可靠性评估的德语标准体系，是 AQG 324 / LV 324 的直接前身与同源标准。
- ⚠️ **本次未能取得 VSME 的一手文件或编号清单**。任务书将 VSME 与 Intel/Infineon/ST 内部规范并列，但这三者性质完全不同：**VSME 是"可查证的外部（前）标准"**，而 **Intel/Infineon/ST 内部规范是"不公开的企业标准"**。
- 来源：enrlb.com（二手，AQG 324 测试映射表中提及 VSME）｜可信度：★★☆☆☆
- **`[推断]`** 任务书这一并列存在**分类错误**。正确分层应为：
  - **L0 国际/行业层**：IEC / JEDEC / SEMI / IPC / UL
  - **L1 区域/国家层**：GB/T、GJB（等同或对标 IEC/MIL）
  - **L2 行业指南层**：AQG 324、AEC-Q、LV 324、VSME（**非强制、合同性**）
  - **L3 企业层**：Intel/Infineon/ST 内部规范（**不公开、不可引用为行业依据**）
  - **L4 客户层**：BMW GS 95035 / VW 82324 / Daimler 采购规范（**真正的约束力来源**）
- 详见 §2 层级模型。

---

## 2. 标准体系的层级模型

### 2.1 五层模型（基于本次核实证据重构）

```
┌─────────────────────────────────────────────────────────────┐
│ L4 客户/契约层（约束力真正来源，不可公开全文）              │
│    BMW GS 95035 · VW 82324 Group Standard · Daimler 采购规范  │
│    特性：合同性、私有、指定认证机构                          │
├─────────────────────────────────────────────────────────────┤
│ L3 行业指南层（Guideline，非强制，合同引用）                │
│    AQG 324 / AEC-Q100·Q101·Q102·Q103·Q104·Q200 / LV 324    │
│    特性：自愿采用，但一旦被客户合同引用即成为义务            │
│    ★ 唯一全文免费（AQG 324, CC BY-ND）                      │
├─────────────────────────────────────────────────────────────┤
│ L2 器件/材料族标准层（Normative，付费）                      │
│    IEC 60747（分立）· IEC 60748（IC）· IEC 60749（试验方法） │
│    IEC 60068（通用环境）· IEC 60664（绝缘配合）· IEC 62506   │
│    JEDEC JESD22（测试方法）· JESD47（IC 资格）· JEP95（外形）│
│    SEMI M/G/E/S/F/C（材料/封装/自动化/安全/设施/化学品）      │
│    IPC-9701/9702（焊点力学）· J-STD-020（MSL）              │
├─────────────────────────────────────────────────────────────┤
│ L1 国家采纳/军用层（对标 L2，叠加而非替代）                 │
│    GB/T 2423.x ≡ IEC 60068-2-x（等同采用）                 │
│    MIL-STD-883（微电路）≡ GJB 548（微电子器件）              │
│    MIL-STD-750（分立）  ≡ GJB 128（半导体分立器件）          │
│    ★ 独立体系，与 L2 平行；出口/军工需双重满足              │
├─────────────────────────────────────────────────────────────┤
│ L0 通用物理/统计基础层（不属任何单一组织）                    │
│    Coffin-Manson · Arrhenius · Peck · Black · Miner 累积损伤  │
│    Weibull / 对数正态 / 浴缸曲线                              │
│    载体：IEC 62506（TC 56 Dependability）+ 学术文献          │
└─────────────────────────────────────────────────────────────┘
```

**关于用户提出的"基础/通用层 → 器件族层 → 具体产品/方法层"三层模型**：
`[推断]` 该三层模型方向正确但**颗粒度不足**。基于本次核实的实际引用关系，建议修正为**上面的五层**，理由：
1. 用户模型缺 L4（客户契约层）—— 而这恰恰是 AQG 324 约束力的真正来源（BMW GS 95035 等），忽略它会误判标准的强制性
2. 用户模型缺 L3（行业指南层）—— AQG/AEC/V SME 都在这一层，与"标准"性质不同（指南是自愿的）
3. 用户模型缺 L0（统计物理基础层）—— 用户最关心的加速模型全部来自这一层，**它不属于任何标准组织**
4. 用户模型把"军用层"当作民用体系"之上的叠加"，但实测显示 **GJB 548 与 MIL-STD-883 是各自独立的平行体系**（且方法号结构都是 1000/2000/3000/5000 四段式），不是简单叠加

### 2.2 车规层（AQG 324）如何"继承"JEDEC + IEC —— 实测结构

**实测结论（一手证据）**：

```
AQG 324 04.1/2025 的引用构成（21 项）
├─ IEC       14 项 (67%)  ← 绝对主体
├─ JEDEC      2 项 (10%)  ← 仅 JESD22-A104F + JESD22-A119
├─ JEDEC JEP  5 项 (24%)  ← 全在 Annex SiC
├─ ISO        1 项  (ISO/IEC 17025)
├─ IATF       1 项  (体系类)
└─ UNECE/RoHS/ELV/WEEE  0 项  ← 0%
```

`[推断]` **三层继承机制**：
1. **方法学层**：全部试验方法从 **IEC 60068 / 60664 / 60747 / 60749** 继承（IEC 60749-34 甚至在 AQG 324 引用表写 2010、正文写 2011，见 §矛盾记录）
2. **器件参数层**：从 **IEC 60747-15** 继承热阻/杂散电感的测量方法（AQG 324 QC-01/QC-02 直接引用 `IEC 60747-15:2012, section 5.3.2/5.3.6/5.3.6.1/5.3.6.4`）`[一手]`
3. **加严层**：AQG 324 自定条件（ΔTj、ton、循环数），不照抄 IEC
4. **体系层**：从 **IATF 16949** + **ISO/IEC 17025** 继承（流程与实验室资质）

**这与用户任务书的假设"JEDEC + IEC + 法规"不符**：
- IEC 部分 ✅ 正确（且被严重低估，是主体）
- JEDEC 部分 ⚠️ 存在但极小（仅 2 份，且 2025 版才增加温循）
- 法规部分 ❌ **不存在**（0 引用）

**AQC 的引用机制** `[推断]`：AQG 324 的"加严"是**表格式条件替换**而非"标准改写"。证据 `[一手]`：
> "The industrial standards referenced in this document have **consciously been selected in the specific versions or release years**. This means they represent the technical state of the art of the industry, **which was not prepared for automotive applications, but has been deemed suitable** with regard to automotive applications. **In particular, this avoids automotive-relevant details being omitted during revisions with a focus on non-automotive applications.**"
> （原文极短引用，意为：刻意锁定特定版本，避免后续修订丢失车规相关细节）

`[推断]` 这段 Preface 是理解 AQG 324 引用策略的钥匙——**它故意锁死旧版本 IEC（如 60749-25:2003、60747-15:2010）**，即使 IEC 已出新版。这对标准知识 OS 有直接工程含义：**不要盲目"升级引用版本"**。

### 2.3 企业标准在体系中的位置

`[推断]`（依据 §1.7 分层论证）：
- 企业标准**不在标准体系内**，是"私有实现层"
- 它们的作用是：(a) 比 L2 更严苛（供应商内部护城河）；(b) 填补 L2 未覆盖的工艺细节（如 Infineon 的 AN2010-02 IGBT4 功率循环曲线 —— 该文献被 AQG 324 附录 II.D 引用为 [17]）`[一手，AQG 324 参考文献]`
- **对用户的实用价值**：当标准给出 AF=50 而产品实测不符时，企业规范的实测曲线往往比标准更可信，但**不可作为对外合规证据**
- ⚠️ **VSME 需重新归类**：它是**可查证的外部标准**（虽为德语区使用），应归 L3 或独立 L2.5，而非企业层

---

## 3. 加速寿命模型：完整公式、参数定义、适用条件与失效机理假设

> **本节是本报告技术价值最高的部分。** 所有公式均标注来源与验证等级。
> **方法论总纲**：**[一手]** **IEC 62506:2023 *Methods for product accelerated testing***，第 2 版，由 **IEC TC 56（Dependability，可信性技术委员会）** 制定，替代 2013 年第 1 版。
> - 来源：https://www.antpedia.com/standard/1016730953-10.html （标准信息聚合，可信度★★★☆☆）｜**建议用户自行访问 webstore.iec.ch 核验**
> - **`[推断]`** ⚠️ **重要修正**：任务书把加速模型挂在 "IEC 60749" 名下不准确。**60749 是"半导体器件机械与气候试验方法"，规定的是"怎么做试验"；加速模型的方法论、统计设计与模型选择属 TC 56 → IEC 62506。** 知识 OS 应把 **IEC 62506 作为模型层的根**，IEC 60749 作为"试验条件层"的根。

### 3.1 加速试验三分类（IEC 62506 框架）`[二手，多源一致]`

| 维度 | Type A（定性） | Type B（定量） | Type C（压缩） |
|---|---|---|---|
| 目标 | 发现失效模式 | 估计可靠性指标 | 估计寿命 |
| 加速方式 | 超规格应力 | 应力水平提升 | 时间/频率压缩 |
| 统计置信度 | 无 | 有 | 有 |
| 典型应用 | HALT / HASS | 加速寿命试验 ALT | 循环疲劳试验 |
| 可否外推寿命 | ❌ | ✅ | ✅（等效寿命） |

### 3.2 Arrhenius 加速因子（温度）

**公式**：

```
                E
AF(T) = exp [ —— ( 1/T_use − 1/T_stress ) ]
                k
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `E` | 失效过程的**活化能** Activation Energy | eV（或 J/mol） |
| `k` | Boltzmann 常数 = **8.617 × 10⁻⁵ eV/K** | eV/K |
| `T_use` | 使用（现场）绝对温度 | **K** |
| `T_stress` | 应力（试验）绝对温度 | **K** |
| `AF` | 加速因子 = 现场寿命 / 加速寿命（>1） | 无量纲 |

**等价写法**（数学上等价，实践中更常见于文献）：

```
L(T) = L₀ · exp[ (E / k) · (1/T_use − 1/T_stress) ]
```

**适用条件（失效机理假设）** `[二手，多源交叉]`：
1. **单一失效机理主导** —— Arrhenius 成立的前提是加速前后是**同一物理机制**。若高温引入新机制（如 Al 金属化在 >200 °C 发生晶界变化、Cu 扩散改变），AF 外推失效
2. **Ea 在应力范围内恒定** —— Ea 实为温度区间的表观斜率，跨区间需重新拟合
3. **Ea > 0** —— 但**表面扩散/电迁移主导时 Ea 可为负**（见 §3.7 Eyring 条目）
4. 温度必须用 **Kelvin**（绝对温度），用 °C 会造成系统性偏差

**常见 Ea 数量级** `[二手]`：
- 半导体器件常见失效：**≈ 0.7 eV**（湿度相关 **≈ 0.9 eV**）
- 通用电子元件：**0.3–1.2 eV**，常用默认值 **0.67 eV**
- 铝互连线电迁移：晶界扩散 **0.5–0.6 eV**、晶内扩散 **≈ 1 eV**
- Coffin-Manson 拟合的 Ea 报道范围：**0.12–0.58 eV**（ACS Omega 2025 实测 0.38 eV）
- 来源：antpedia.com（IEC 62506 条目）、pubs.acs.org（ACS Omega 论文）｜可信度：★★★☆☆
- ⚠️ **这些 Ea 值均为二手，应用前必须用自有数据验证**。`[推断]` Ea 不是材料常数而是"失效机理 + 温度区间"的拟合参数。

**理论来源** `[二手，多源一致]`：Svante Arrhenius，1889 年提出 Arrhenius 方程（化学反应速率常数与温度的关系）。**Arrhenius 本人 1901 年获诺奖的工作是低温反应速率，不是半导体可靠性**——可靠性工程借用该方程做"热加速"外推，隐含假设"半导体退化是热激活的化学反应过程"。这是**跨学科借用**，不是原始应用场景。

**重要变体：T-stress（温度应力）模型** `[二手]`：单一温度 AF 无法描述"先高温老化一段、再低温使用"的场景。ECPE/AQG 324 使用的是 **T-stress 形式**（把关键温度 T-stress 作为第三个温度引入）：

```
AF = exp[ (E / k) · (1/T_use − 1/T_stress) − (E / k) · ln(T_stress_real / T_stress) ]
```
（形式随文献而异 ⚠️ **未找到权威统一表述，标为未核实**）

### 3.3 温湿度加速：Peck 关系式（Power Law）

**公式**（AQG 324 附录 II.D 引用 MDPI 综述表格原文）`[一手，MDPI 综述]``[二手，原始文献 Peck 1978]`：

```
τ = A₀ · (RH)^(−n) · exp( E_a / (k · T) )
```

| 符号 | 含义 |
|---|---|
| `τ` | 中位寿命 median life |
| `A₀` | 比例因子，由实验确定 |
| `RH` | 相对湿度（**注意：此处 n 取 2.7，见下**） |
| `n` | 湿度指数，**≈ 2.7** |
| `E_a` | 活化能 |
| `k` | Boltzmann 常数 = 8.62 × 10⁻⁵ eV/K |
| `T` | 温度（K） |

**适用条件** `[二手]`：环氧塑封料（epoxy packaging）湿热退化，腐蚀/离子迁移主导。

**Peck 幂律形式（电压型）** `[一手，MDPI]`：

```
T_F = A₀ · (RH)^(−N) · f(V) · exp( E_a / (k · T) )
```
其中 `N ≈ 2.7`，`E_a = 0.7–0.8 eV`（**含氯化物时铝腐蚀的合适值**），`f(V)` = 施加电压的**未知函数**（原文即标注 "an unknown function"）。

**现代变体（同时含温湿压）** `[二手]`：

```
A_H = (RH_test / RH_use)^h × exp[ (E_a/k) · (1/T_use − 1/T_test) ]
```
- `h` = 湿度指数，**绝缘材料约 2.66**
- 来源：elephant-med.com（⚠️ 医疗器械网站，内容农场性质，**仅公式形式参考，数值不可信**）｜可信度：★☆☆☆☆
- **`[推断]`** 但 `h ≈ 2.66` 与 Peck 的 `n ≈ 2.7` 数值吻合度高，属同一经验规律的两种表述。`[二手，多源]` 另有来源称"绝缘材料 h ≈ 2.66"。

**HAST vs THB 的优先级规则（一手，实用价值高）** `[一手]`：**IEC 60749-4 与 IEC 60749-5 都做时，85/85 稳态 THB 的结果优先于 HAST**。
> 原文（IEC 60749-4:2017 §4）："The stress usually activates **the same failure mechanisms** as the '85/85' steady-state temperature humidity bias life test, IEC 60749-5. As such **the test method may be selected from IEC 60749-5 or from this test method. When both test methods are performed, test results of the 85 °C/85 % RH steady-state temperature humidity bias life test, IEC 60749-5, take priority over HAST.**"
> **This test method shall be considered destructive.**
- 来源：https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-4%7Bed2.0%7Db.pdf （VDE 官方 IEC 预览）｜可信度：★★★★★
- IEC 60749-5:2023 Ed 3.0 同样确认："Where both this steady-state, humidity bias test and the damp heat, highly accelerated stress test (HAST) of IEC 60749-4 are performed, **the results of this 85 °C/85 % RH steady-state test will take priority over the results of the HAST test**"
  - 来源：https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-5%7Bed3.0.RLV%7Den.pdf ｜可信度：★★★★★
- **`[推断]`** 这是**工程上可直接使用的判定规则**：做 HAST 而不做 THB，则 HAST 结果不被接受为 THB 的替代证明。IEC 60749-5:2023 另明确其为 **destructive**（破坏性）试验。

**IEC 60749-5:2023 关键试验条件** `[一手]`：
- 温度 **85 ± 2 °C**、相对湿度 **85 ± 5 % RH**、时长 **1000 h（+168/−24 h）**（注：1000 h 与 +168/−24 出自 BS EN 60749-5:2017 条目，Ed 3.0 表 1 具体值需查原文）
- 去离子水电阻率 **≥ 1 × 10⁴ Ω·m**
- 干球温度须始终高于湿球温度
- **偏压选择准则** `[二手]`：当器件功耗 > 200 mW 或虚拟结温 ΔTja ≥ 10 °C 时，采用 **1 h on / 1 h off 循环偏压**
- **`[推断]`** ⚠️ **Ed 3.0 术语变更**：2023 版将 "virtual junction（虚拟结温）" 改为 "**die（芯片）**"；若 ΔTja ≥ 5 °C 须在报告中记录虚拟结温与箱温之差
- 升降温速率应 < 3 h 以避免器件表面凝露；中间测试窗口可延长至 144 h（防潮袋密封）；试验后 **48 h 内**完成电性能测试
- 可信度：★★★☆☆（部分参数来自 plusstd.com 二手条目）

### 3.4 Coffin-Manson（低周疲劳 / 热循环）

**基础形式** `[一手，MDPI 综述表格]`：

```
                1/m
N_f = C · (Δγ · ε_f)          其中 m = 疲劳指数
```

| 符号 | 含义 |
|---|---|
| `N_f` | 平均失效循环数 |
| `Δγ` | 非弹性应变幅 inelastic strain range，`Δγ = F/(L·d) + h·Δα·ΔT` |
| `ε_f` | 剪切方向疲劳延性系数，**焊料典型值 0.325** |
| `B` | 实验确定的尺度因子 |
| `C` | 疲劳强度系数 |

- 来源：https://www.mdpi.com/2072-666X/15/3/398 （MDPI *Micromachines* 综述，可信度★★★★☆，同行评审开放获取）

**简化幂律形式（焊点热疲劳最常用）** `[一手，MDPI]`：

```
Life = A · (ΔT)^B
```
- `A`、`B` 均由实验确定
- **适用**：焊点互连的热循环疲劳

**由简化式导出加速因子** `[二手]`：

```
              (ΔT_test / ΔT_use)^B
AF = Nfu/Nft = ─────────────────────
```
（`[二手]` 假设：温变引起的塑性应变正比于 ΔT）
- 来源：accendoreliability.com ｜可信度：★★☆☆☆

**通用 Coffin-Manson（带频率修正，Shi 模型）** `[一手，MDPI 综述]`：

```
[ N_f · v^(k−1) ]^m · Δε_p = C
```
| 符号 | 含义 |
|---|---|
| `v` | 频率 |
| `k` | 频率指数（连接疲劳寿命与频率） |
| `m` | 疲劳指数 |
| `C` | 延性系数 |

**B 值经验值（按材料）** `[二手]`：

| 材料 | B |
|---|---|
| 金属 Metals | 2–3 |
| **电子焊点 Electronic solder joints** | **2–3** |
| 微电子塑封料 Microelectronic plastic encapsulates | 4–8 |
| 微电子钝化层 Passivation layers | 12 |
| 微电路坑蚀 Cratering | 7 |
| Al–Au 金属间化合物疲劳 | 4–7 |

- 来源：accendoreliability.com（Condra 汇编）｜可信度：★★☆☆☆
- **`[推断]`** 该表是**定性排序参考**（塑封料/钝化层的 B 高于金属，因为其 CTE 失配与模量差异更大），**不应作为设计定值使用**。实际 B 需用自有材料 CTE + 焊点几何做 FEM 提取 Δγ 后重新拟合。

**Coffin-Manson 频率/温度综合扩展（★ AQG 324 实际使用的形式）** `[一手]`：

```
                                        E_a
              a                    (─────────────)
N_f = A · f · ΔT  · e            k_B · T_j,mean
```
（原文式 6；`a` 为频率指数）
- 来源：AQG 324 04.1/2025 附录 II.D，p.11（公式 6）｜可信度：★★★★★
- **`[推断]`** 原文排版中 `f^a`、`ΔT_j^β2` 与指数堆叠，但**可确认的结构是"频率幂 × 温变幂 × Arrhenius(平均结温)"**。这正是"功率循环寿命 = 循环次数 + 温度依赖"的物理表述。

**适用条件（Coffin-Manson 家族）** `[二手 + 推断]`：
1. 变形须**保持在塑性区内**（低周疲劳前提）
2. 焊接/键合的几何与约束须与使用状态一致（若使用中有扭转载荷，试验也须施加扭矩）
3. 温变引起的塑性应变 ∝ ΔT（故可用 ΔT 幂律替代应变）
4. 高频下材料响应会变化（变形热积累）→ 故引入频率指数 `a`

### 3.5 Morrow（能量法焊点疲劳）

**公式** `[一手，MDPI 综述]`：

```
N_f^m · W_p = C
```

| 符号 | 含义 |
|---|---|
| `N_f` | 失效循环数 |
| `W_p` | **稳态循环的塑性应变能** plastic strain energy in a steady-state loop |
| `m` | 疲劳指数 |
| `C` | 材料延性系数 |

- 来源：https://www.mdpi.com/2072-666X/15/3/398 ｜可信度：★★★★☆
- **适用条件** `[二手]`：焊点低周疲劳，且**能量已包含蠕变贡献**（这是 Morrow 相对 Coffin-Manson 的核心优势——焊点退化有时间依赖性）
- **`[推断]`** AQG 324 附录 II.D 明确说明了这一点：
  > "The **extension** of this model was necessary due to **time dependence effect of solder degradation**."
  （即：必须扩展原模型，因为焊料退化存在时间依赖效应）
- ⚠️ **标准符号冲突（重要）** `[推断]`：**Morrow 公式中的 `C` 与 Coffin-Manson 公式中的 `C` 含义不同**（Morrow 的 C 是能量量纲，CM 的 C 是温度/应变量纲），但 MDPI 综述表格中两者共用 `C` 符号。功率封装文献中 `C` 极度重载（常数、循环数、Cramer 集总参数）。**知识 OS 必须为每个模型建立独立符号命名空间。**

**相关模型对照** `[一手，MDPI 综述]`：

| 模型 | 公式 | 特征参数 |
|---|---|---|
| **Solomon–Tolksdorf** | `[N_f · v^(k−1)]^m · W_p^v^n = C` | 同时用 W_p（能量）与 v^n（频率耦合） |
| **Pan** | `C = N_f · (a·Ė_p + b·Ė_c)` | `a`=塑性功权重(0.85), `b`=**蠕变**功权重(0.15), C=几何相关临界应变能密度 |
| **Syed-I** | `N_f = (E_cr / C)^(−1)` | `E_cr`=整周期累积蠕变应变, C=蠕变机制延性 |
| **Joseph & Jerries** | `N_f = E_intrinsic / W` | W=单周期耗散能 |

- `[推断]` **Pan 模型 a=0.85 / b=0.15 的权重**：说明功率焊点退化中**塑性功占主导（85%）、蠕变占 15%**。这为"是否需要做长时间功率循环"提供定量决策依据。

### 3.6 Nordhoff-Peck 与 Solomon-Tolksdorf（频率耦合）

- **Shi（频率修正 Coffin-Manson）** `[一手，MDPI]`：`[N_f · v^(k−1)]^m · Δε_p = C`
- **Solomon-Tolksdorf** `[一手，MDPI]`：`[N_f · v^(k−1)]^m · W_p^(v^n) = C`
  - `v`=频率，`k`=频率指数（寿命-频率），`n`=频率指数（能量密度-频率）
- ⚠️ **Nordhoff-Peck 在本次检索中未取得权威一手来源** `[未核实]`。检索命中的 `n` 符号冲突（Norris 公式中的 n vs Peck 中的 n vs Nordhoff-Peck 的 n）未解决。**标为未核实，不写入公式。** 待办 T6。

### 3.7 累积损伤与其他模型（AQG 324/MDPI 表格原文）`[一手]`

| 模型 | 公式 | 参数定义与适用 |
|---|---|---|
| **Norris-Landzberg** | `N_lab/N_machine = (f_L/f_M)^(1/3) · (ΔT_M/ΔT_L)^2 · Φ(T_max)`，其中 `Φ = exp[(E_a/k)(1/T_L,max − 1/T_M,max)]` | 锡铅焊互连热疲劳；f=最大疲劳寿命比，M/L=最大温变比，T_max 绝对温度 |
| **Miner's Rule（线性累积损伤）** | `CD = Σ(i=1..k) CSi/Ni ≤ 1` | CD=累积损伤，CSi=应力 Si 下施加循环数，Ni=Si 下失效循环数（由该材料 S-N 图确定），k=载荷数。**仅在弹性极限内有效** |
| **Garofalo（蠕变）** | `ε̇_cr = C1 · sinh(C2 · σ) · C3 · exp(C4/T)` | 极慢振动引发蠕变应变；电子互连无铅焊 |
| **Peck's Power Law** | `T_F = A0·RH^(−N)·f(V)·exp(Ea/kT)` | 腐蚀；N≈2.7, Ea=0.7–0.8 eV |
| **Eyring/Black/Kenney** | `τ = A·T·exp[B/(k·T)]` | 电容、铝电迁移 |
| **Eyring** | `T_F = B·(I_sub)^(−N)·exp(Ea/(k·T))` | 表面反转、机械应力；**N = 2–4，Ea = −0.1 至 −0.2 eV（表观活化能为负！）** |
| **热机械应力** | `T_F = B0·(T0 − T)^(−n)·exp(Ea/(k·T))` | 热膨胀系数差异；T0=金属无应力温度，**n = 2–3**，Ea=0.5–0.6 eV（晶界扩散）/≈1 eV（晶内扩散） |

- 全部来源：https://www.mdpi.com/2072-666X/15/3/398 ｜可信度：★★★★☆

> ⚠️ **⚠️⚠️ 关键警告：上表（§3.7）原表存在符号印刷错误**
> MDPI 综述原文中 `exp[ Ea / kT ]` 形式的**括号位置明显错误**（kT 应在分母，即 `exp(Ea/(k·T))`）。例如 Eyring 条目标注 `Ea = −0.1 至 −0.2 eV`（负活化能），而 `T_F = B·(I_sub)^−N·exp(Ea/kT)` 若按字面 `exp(Ea/(kT))` 解读为 `exp(Ea/k·T)` 则量纲完全错误。
> **`[推断]`** 正确形式应为 `exp(E_a / (k · T))`。知识 OS 转录时**必须修正**，并标注"原文疑似排版错误"。
> 另：Peck's Life 条目写作 `τ = A0·(RH)^−2.7·exp[0.79/(kT)]`，`0.79` 应为 **E_a = 0.79 eV**。

### 3.8 AQG 324 功率模块寿命模型（★ 车规实务核心）

**LESIT 基础模型** `[一手，AQG 324 04.1/2025 附录 II.D p.11]`：

```
                                     E_a
N_f = A · f^a · ΔT_j^b2 · exp( ─────────────── )
                                  k_B · T_j,mean
```
- 来源标注：*"derived from test data … developed in the **LESIT project**"*
- 原文引用 `[12]`：K. Mainka, M. Thoben, O. Schilling, "Lifetime calculation for power modules, application and theory of models and counting methods", **EPE, Birmingham, 2011**
- **`[推断]`** LESIT = 德国国家资助的功率电子寿命研究项目，该模型是欧洲车规功率模块寿命计算的**事实标准**。`T_j,mean` 用平均结温（不是峰值）是焊料时间依赖效应的体现。

**Bayerer 扩展模型（引入线径与电流）** `[一手，同上，公式 7]`：

```
                              E_a
                ⎛         ⎞
                ⎜   k_B · T_j         ⎟
N_f = K · (ΔT_j)^b1 · exp⎜ ────────── ⎟ · t_on^b3 · I^b4 · V^b5 · D^b6
                              C
                              ─────
                              γ
```

| 符号 | 含义（依原文与文献）|
|---|---|
| `K` | 常数 |
| `ΔT_j` | 结温摆幅 |
| `b1` | 温变指数 |
| `T_j` | 结温 |
| `C` | 模型常数（Arrhenius 积分中的参考常数） |
| `t_on` | 通电导通时间 |
| `I` | 电流 |
| `V` | 电压 |
| `D` | 键合线直径 |
| `b2…b6`, `γ` | 各指数/参数 |

- 原文引用 `[16]`：R. Bayerer et al, "Model for Power Cycling lifetime of IGBT Modules — various factors influencing lifetime", **5th International Conference on Integrated Power Electronics Systems, Nuremberg, 2008**
- **`[推断]`** **这是功率模块功率循环寿命的"全参数模型"**：`t_on`（导通时间）、`I`（电流）、`D`（线径）显式进入 → 解释了 AQG 324 为何要区分 **PCsec（ton < 5 s）** 与 **PCmin（ton > 15 s）** 两种试验：导通时间不同，损伤机制不同（PCsec → 键合线脱离 + 芯片金属化退化；PCmin → **焊点**应力更大，可能引起基板/底板间焊点开裂）

**最新扩展（烧结芯片）** `[一手，同上]`：
> 原文引用 `[21]`：U. Scheuermann, R. Schmidt, "A New Lifetime Model for Advanced Power Modules with **Sintered Chips** and Optimized Al Wire Bonds", **PCIM, Nuremberg, 2013**
- **`[推断]`** 对应功率封装的**烧结银/烧结铜芯片贴装**工艺（用户领域），模型需重新标定。

**PCsec vs PCmin 的物理分工** `[一手，AQG 324 附录 II.D]`：
- **PCsec（QL-01, ton < 5 s）**：短导通时间 → 快速温度变化 → 典型退化：**wire bond lift-off、芯片金属化退化、芯片-基板焊点退化**
  - 瞬态热阻在 **< 100 ms** 时很小；典型 Al 键合线因热容需要 **> 100 ms** 才能升温 → 因此 **ton < 100 ms 的温度摆动通常可忽略并过滤**（对驱动逆变器应用）
- **PCmin（QL-02, ton > 15 s）**：长导通时间 → **焊点应力更大**，可能诱发**基板/底板间焊点开裂**
- **结论（原文）**："**both types of power cycling tests are required to verify the package technology**"

**寿命消耗累加方法（Rainflow + 消耗相加）** `[一手]`：
1. 对整车/任务谱（mission profile）做 **Rainflow 循环计数**（提取 ΔT 分布；ASTMD E1049-85 为计数方法标准，AQG 324 参考文献 [13]）
2. 提取的热应力直方图（cycles-to-failure/ΔT histogram）代入寿命曲线，得到每段 ΔT 的**寿命消耗**
3. 累加 → 单一等效应力值

**概率约定（实务关键）** `[一手]`：
- 寿命曲线须代表**定义的生存概率，如 95%**
- **"100% 寿命消耗 = 5% 部件达到 EOL 判据"**（即寿命曲线本身已含 5% 分位含义）
- IGBT / Diode / Solder 可各有不同曲线

**参数敏感性（量化，罕见一手数据）** `[一手，附录 II.D p.12]`：
- 模拟 75 min 驾驶谱，改变应用/模块参数各 10%：
  - **Rth 降低 10% → 寿命增加约 40%**
  - 导通损耗或逆变器电流变化有类似影响
- **"Applying large safety margins in the range of 20% will reduce the power density and double the lifetime."**（留 20% 安全裕度会降低功率密度并**使寿命翻倍**）
- **原文明示的局限**：
  > "With the number of samples defined in the AQG 324, the definition of a higher probability is **not reasonable and will not result in a better prediction of the lifetime**."
  > （以 AQG 324 规定的样本量，定义更高生存概率不合理，也不会改善寿命预测）
- 任务谱应代表**典型而非最坏**驾驶谱

**SiC 专属寿命测试（04.1/2025 Annex SiC 新增）** `[一手，目录]`：
| 编号 | 名称 |
|---|---|
| QL-08 | HTFB（High-temperature forward bias，高温正偏）|
| QL-09 | **DGS（Dynamic gate stress，动态栅极应力）** |
| QL-10 | **DRB（Dynamic reverse bias，动态反偏）** |
| QL-11 | **dyn. H3TRB（动态高湿高温反偏）** |

`[推断]` 这 4 项的加入逻辑：SiC 的 **Vth 漂移、栅氧退化、双极退化（body diode Vf 上升）** 需在**动态工况**而非静态偏压下暴露。配套 JEP183（JEP VT 测量）、JEP184（BTI）、JEP190（dV/dt 鲁棒性）、JEP195（栅开关不稳定性）、JEP197（双极退化）构成**完整的 SiC 专属方法学闭环**。

### 3.9 统计样本量与分布 `[二手，多源一致]`

- **Type B 定量试验**：指数分布常见做法 **77 个样本 × 1000 h**；Weibull 分析需 **至少 5~10 个失效**
- **中位秩表**用于统计推断（IEC 62506 表 G.1）
- **必须按失效模式分别分析**（不同失效机理不可混合进单一分布）
- 来源：antpedia.com、kintest.cn、kpt-bj.com（均为 IEC 62506 条目转载）｜可信度：★★☆☆☆
- `[推断]` "77 样本"源自指数分布的置信度要求（0/77 失效 → 90% 置信下失效率上限 ≈ 3%）。这一数字在工程界广泛使用但**需查 IEC 62506 或 MIL-HDBK-217 原文确认依据**。标为**待核实**（待办 T7）。

### 3.10 加速模型的适用边界总表

| 模型 | 应力类型 | 关键假设 | 失效机理 | 否定它的条件 |
|---|---|---|---|---|
| **Arrhenius** | 温度 | Ea 恒定、同一机理 | 热激活扩散/反应 | 高温引发新机理；Ea 变温 |
| **Inverse Power Law** `L = C·S^(−m)` | 电压/振动/机械 | 幂律恒定 | 电应力、机械应力 | 应力超限、机制改变 |
| **Eyring** | 电流/电场 + T | 线性化激活 | 表面反转 | 强场非线��� |
| **Peck** | 湿度 + T | n≈2.7 恒定 | 腐蚀、离子迁移 | 封装形态改变吸湿路径 |
| **Coffin-Manson** | ΔT 循环 | 塑性应变∝ΔT、几何一致 | 焊点/互连低周疲劳 | 频率过高、高周疲劳区 |
| **Morrow** | 能量 | 稳态循环能量 | 焊点疲劳（含蠕变） | 非稳态循环 |
| **Miner** | 多应力 | 线性累积、无交互 | 多种疲劳叠加 | **多应力耦合有交互时失效** |
| **Rainflow + AQG 324 模型** | 任务谱 | 曲线为 5% 分位 | 功率模块综合 | 超出标定 ΔT/ton 范围 |

- `[推断]` **IEC 62506 的最重要警告（来自二手转述的该标准核心原则）**："**应力加速不得改变失效机理**（如过热导致相变）；多应力组合时应考虑**相互作用**，**避免简单相乘导致过度加速**"。这是所有 AF 计算的**第一性约束**。

---

## 4. 从标准编号反查内容：检索路径与陷阱

### 4.1 反查路径（可靠顺序）

1. **JEDEC** → https://www.jedec.org/standards-documents （注册后免费下载；可按 committee / doc type / technology focus area 三个 facet 过滤）
2. **IEC** → https://webstore.iec.ch/ （**付费**，但可免费看目录/范围/scope）；也可走 https://www.iec.ch/dyn/www/f?p=103:22 按 TC 查看全部出版物（本报告 §1.3 的 60749 表即由此获得）
3. **SEMI** → https://store-us.semi.org/collections/standards/ （**付费**；官网 Standards 页可免费看卷/系列结构）
4. **AQG 324** → https://www.ecpe.org/research/working-groups/automotive-aqg-324/ （**免费，CC BY-ND**，token 化直链）
5. **AEC** → http://www.aecouncil.com/AECDocuments.html （免费；⚠️ **本次抓取失败**，待办 T4）
6. **MIL-STD** → https://assist.dla.mil/ （DLA ASSIST 数据库，官方）；或 https://quicksearch.dla.mil/
7. **中国标准** → 全国标准信息公共服务平台 std.samr.gov.cn；GJB 需通过正式渠道（本次未取得官方公开入口）
8. **UNECE 法规** → https://digitallibrary.un.org/ 与 EUR-Lex

### 4.2 已验证的编号陷阱（知识 OS 必须内建）

| 陷阱 | 错误说法 | 正确 | 证据 |
|---|---|---|---|
| **T1** | "MIL-STD-883 方法 1015 = 温循" | **1015 = burn-in；1010 = 温度循环** | 883F/L 原文目录 ★★★★★ |
| **T2** | "SEMI G1–G5 = 湿电子化学品纯度等级" | **G 系列 = 封装（Packaging）**；化学品 = C 系列 | semi.org 官网 ★★★★★ |
| **T3** | "IEC 60068-2-3 (Ca)" | 已被 **60068-2-78 (Cab)** 取代 | 多源一致 ★★★★☆ |
| **T4** | "AQG 324 引用 UNECE R10 / RoHS / ELV / WEEE" | **0 引用**；体系锚点是 IATF 16949 + ISO/IEC 17025 | AQG 324 全文 grep ★★★★★ |
| **T5** | "IEC 60749-3 = 加速试验方法" | **60749-3 = External visual examination** | IEC TC 47 官方目录 ★★★★★ |
| **T6** | "IEC 60749-4 = 湿热稳态" | 60749-4 标题含 "Damp heat, steady state, **HAST**"；稳态偏压寿命是 **60749-5** | IEC 官方目录 ★★★★★ |
| **T7** | "AQG 324 由 ZVEI 牵头" | **ECPE 持有与制定**；ZVEI 是 LV 324 阶段的联合方 | AQG 324 版权页 ★★★★★ |
| **T8** | "JESD22-A105 = 上电温度循环（PTC）" | 见 §4.3 矛盾记录 | 多源冲突 ★★☆☆☆ |
| **T9** | "JEDEC JEP = 标准" | **JESD = 标准（规范性）**；**JEP = 出版物（信息性）** | jedec.org facet ★★★★★ |
| **T10** | MDPI 综述 `exp(Ea/kT)` 形式 | 应为 `exp(Ea/(k·T))`，**原文排版错误** | 量纲自检 ★★★★★ |

### 4.3 ⚠️ 矛盾记录：JESD22 系列编号（保留不和稀泥）

本次调研发现 **JESD22 编号存在严重的、多源互相矛盾的情况**。这是"从编号反查内容"的最大陷阱。

| 编号 | 说法 A（ima.qq.com wiki，二手） | 说法 B（etac.jp 日文，二手） | 说法 C（知乎/ima 系） |
|---|---|---|---|
| A100 | Cycled Temperature-Humidity-Bias with Surface Condensation (CTHB-SC) | 温湿度偏置循环寿命 | 循环温湿偏压寿命 |
| A101 | **Steady-State Temp-Humidity Bias (THB)** 85/85 | **加速湿热试验（THB/HAST）** | THB 85/85 |
| A102 | **Autoclave** 121 °C | **高温保存试验（HTS）** | Autoclave |
| A103 | **High Temperature Storage Life (HTSL)** 150 °C | 温湿度偏置循环 | **HTSL 125~200 °C** |
| A104 | **Temperature Cycling (TC)** −55~125 (B) / −65~150 (C) | 温度循环试验（TC） | 温度循环 |
| A105 | — | **功率循环试验** | 上电温度循环 PTC |
| A106 | — | 热冲击试验（TST） | 热冲击 |
| A107 | Salt Atmosphere 5% NaCl | — | 盐雾 35 °C 5% |
| A108 | — | HTOL | 工作寿命 HTOL |
| A110 | **偏压 HAST** 110 °C/85 %RH/96 h | — | 偏压 HAST 130 °C/85 %RH |
| A118 | **无偏 HAST** 110 °C/85 %RH/96 h | — | 无偏 HAST 130 °C/85 %RH |
| A119 | — | — | — |

- **说法 A 来源**：ima.qq.com/wiki（内容农场，**黑名单**）
- **说法 B 来源**：etac.jp（日本试验室，二手）
- **可信度评估**：**说法 A/B 均不可作为正典采信**（一个黑名单源、一个二手源，且互相矛盾）
- **`[推断]`** 但有两点**可交叉确认**：
  1. **`JESD22-A104` = Temperature Cycling** —— 三源一致，且 **AQG 324 04.1/2025 一手引用 `JESD22-A104F:2020 Temperature cycling`** ✅ **[一手确认]**
  2. **`JESD22-A119` = Low Temperature Storage Life** —— **AQG 324 02.1/2019 与 04.1/2025 均一手引用 `JESD22-A119:2015 Low Temperature Storage Life`** ✅ **[一手确认]**
  3. **A101 = THB 85/85** —— 与 IEC 60749-5 高度对应，且 A101 被广泛称为 THB，**倾向正确** `[推断]`
  4. **A110 = 偏压 HAST / A118 = 无偏 HAST** —— 二手源一致给出"110 °C/85 %RH/96 h"，但另一二手源给 130 °C，**矛盾未解**
- **⚠️ 结论：不采信上述任何一张完整对照表。** 知识 OS 中 **A104 与 A119 已一手确认；A101 高度可信；其余必须逐条到 JEDEC 官网核验后再入库**。
- **待办 T8（高优先级）**：用户应直接访问 https://www.jedec.org/standards-documents 按 `field_committees=19`（JC-14）检索，逐条确认 A100–A121、B100–B121 的确切标题。

### 4.4 反查方法论建议（针对用户三大用途）`[推断]`

- **用途①（引用关系）**：以 **AQG 324 为枢纽**。它免费、结构清晰、引用表集中，是最适合做图谱"种子节点"的入口。做法：把 IEC 60747/60749/60068/60664 + JEDEC JESD22 的**方法学**关系建成有向图（AQG 324 → 引用 → 被引用）
- **用途②（测试方法分类）**：三层分类键 = (a) 应力类型（温度/湿度/机械/电/复合）× (b) 层级（L0 通用 / L2 器件族 / L3 车规）× (c) 组织（JEDEC / IEC / MIL / GJB）
- **用途③（编号反查）**：**必须建立编号段 → 应力类型 的映射表**（如 `A1xx` 温湿度类、`B1xx` 力学类，这是 JEDEC 的隐含分组规律），但 §4.3 证明**该规律不能想当然**——需以 JEDEC 官网为唯一权威源

---

## 5. 必读一手文献与工具型资料

### 5.1 全文免费的一手标准（最高优先级）

| 标准 | 版本 | 获取 | 可信度 |
|---|---|---|---|
| **ECPE Guideline AQG 324** | **04.1/2025**（110 页）| https://www.ecpe.org/research/working-groups/automotive-aqg-324/ | ★★★★★ **CC BY-ND，可自由使用/分享（须署名、同条件）** |
| AQG 324 | 03.1/2021（71 页）| 同上 | ★★★★★ |
| AQG 324 | 02.1/2019（70 页）| 同上 | ★★★★★ |
| **UNECE Regulation No.10** | 多个修订版 | https://digitallibrary.un.org/ | ★★★★★ |
| **MIL-STD-883F / 883L Part 1** | 2004-06 / 2019-09 | https://nepp.nasa.gov/.../std883.pdf （NASA NEPP 托管官方 PDF）| ★★★★★ |
| **GB/T 2423.22-2002**（=IEC 60068-2-14） | 2002 | chinahls.cn 公开全文 PDF | ★★★★★ |
| JEDEC 全部文档 | — | https://www.jedec.org/ 注册后免费下载 | ★★★★★ |
| IPC 标准树 | — | https://www.ipc.org/4.0_Knowledge/4.1_Standards/SimplifiedSpecTree.pdf | ★★★★★ |

**AQG 324 版权与许可（重要，实用）** `[一手]`：
> "The ECPE Guideline **AQG 324 is owned by ECPE** European Center for Power Electronics e.V."
> "This ECPE Guideline AQG 324 is licensed under a **Creative Commons license (license model CC BY ND)** - with credit and sharing under the same conditions."

`[推断]` CC BY-ND 允许：分享（含商业性）与改编（须署名、相同许可条款）；**禁止**修改后以不同许可分发。用于内部知识 OS 完全合法（须署名 ECPE + CC BY-ND + 标注版本号）。**这是全球最权威的车规功率模块资格文件，且完全免费——对用户价值极高。**

### 5.2 需购买的一手标准

| 组织 | 定价模式 | 备注 |
|---|---|---|
| **IEC** | 付费（webstore.iec.ch），EN 版更贵 | 60749 系列每部分单独计价 |
| **SEMI** | 付费（store-us.semi.org）；示例定价：Member $148 / Non-Member $193 USD（单份）| 有 SEMIVIEWS 企业订阅（约 30 天试用） |
| **AEC** | 免费 | ⚠️ 本次抓取失败 |
| **AQL/IPC 多数标准** | 付费 | 部分免费（如 IPC-1066、IPC-175X） |

- SEMI 定价样本来源：https://store-us.semi.org/collections/latest-standards-1 ｜可信度：★★★★★

### 5.3 综述性书籍

⚠️ **重要纠错**：任务书写 "C. A. Harper *Electronic Packaging and **Interconnection Technology***" —— **书名有误。**

**正确书目（已核实）**：

| 书名 | 作者 | 出版 | 关键信息 |
|---|---|---|---|
| **Electronic Packaging and Interconnection Handbook**（第 4 版） | **Charles A. Harper**（主编） | **McGraw-Hill, 2004-10/11** | **1000 页，ISBN 0-07-143048-2 / 978-0-07-143048-7**。**注意是 "Handbook"（手册）不是 "Technology"（技术）** |
| 电子封装与互连手册（第4版，中译本） | Charles A. Harper 著；贾松良、蔡坚、沈卓身 等译 | 电子工业出版社, 2009-06 | 735 页，ISBN 978-7-121-08844-5（平装）/ 9787121088445 |
| 原名 | *Handbook of Electronic Packaging* | — | 第 1/2/3 版原名如此；第 2 版 1997、第 3 版 2000 |
| *Packaging Electronic and Photonic Devices* | **R. L. Booth? / H. L.antz? / K. Mansur** | ⚠️ **未核实** | **本次未能取得权威书目验证**。作者全名与出版社/年份均**未核实**，见待办 T9 |
| *Microelectronics Failure Analysis and Prevention* | **T. R. Chow** 等 | ⚠️ **未核实** | Wiley（推测）；**年份/ISBN 未核实** |
| *Reliability and Yield* / *Practical Methods for Product Reliability Improvement* | **A. E. Elegant** | ⚠️ **未核实** | PTR Prentice Hall（推测）；**年份未核实** |

- Harper 书目可信度：★★★★☆（天珑/WorldofBooks 书店页、kongfz、中文百科三方一致给出 ISBN 9780071430487 + McGraw-Hill 2004 + 1000 页 + 第三版书名变更；`worldofbooks` 引 Sci-Tech Book News 20041201 作为书评来源）
- ⚠️ **其他书名标注为"未核实"**：Booth/Lantz/Mansur、Chow、Elegant 三项**作者全名、出版社、年份、ISBN 均未取得权威来源**，检索命中的均为无关书目聚合页。**不写入知识 OS 正典**。待办 T9。
- **`[推断]`** Harper 第 4 版结构（据天珑书店目录，可信度★★★★☆）：**Part 1 基本技术**（Ch1 材料 / Ch2 热管理 / **Ch3 冲击、振动与操作应力管理** / Ch4 连接器与互连 / Ch5 焊接与清洗）；**Part 2 封装与互连技术**（Ch6 单芯片封装与 BGA / Ch7 SMT / Ch8 混合与多芯片模块 / Ch9 CSP、倒装芯片与直接贴片 / Ch10 刚性/柔性 PCB）；**Part 3 系统封装技术**（Ch11 高速与微波 / **Ch12 高压系统封装** / Ch13 MEMS / Ch14 光电）。
  - **对用户价值最高的是 Ch3（应力管理）、Ch9（倒装芯片/DCA）、Ch12（高压系统封装）**——直接对应功率封装的热-机械应力与高压绝缘问题。

**MARPOS / PCIM / EPE 学术引用链（来自 AQG 324 参考文献，一手可追）** `[一手]`：
功率模块寿命计算的学术源头全部在 ECPE 会议论文中，用户可免费获取：
- `[12]` K. Mainka, M. Thoben, O. Schilling, "Lifetime calculation for power modules...", **EPE, Birmingham, 2011** ← **LESIT 模型**
- `[16]` R. Bayerer et al, "Model for Power Cycling lifetime of IGBT Modules", **CIPS 5th, Nuremberg, 2008** ← **Bayerer 扩展模型**
- `[21]` U. Scheuermann, R. Schmidt, "A New Lifetime Model for Advanced Power Modules with Sintered Chips and Optimized Al Wire Bonds", **PCIM, Nuremberg, 2013** ← **烧结芯片模型**
- `[7]` M. Thoben, K. Mainka, R. Bayerer, I. Graf, M. Münzer, "From vehicle drive cycle to reliability testing of Power Modules for hybrid vehicle inverter", **PCIM, Nuremberg, 2008**
- `[8]` M. Thoben, "Reliability and Lifetime of Power Modules Tutorial", **EPE'16 ECCE Europe, Karlsruhe, 2016**（DOI 10.13140/RG.2.2.34359.32160）
- `[6]` M. Thoben, Abschlussbericht Teilvorhaben 19 U 6006C im Verbundprojekt **EfA**（德国研究项目最终报告，2011）
- `[3]` A. Aal, "Qualification of Power Electronics Modules for Use in Motor Vehicle Components", **ECPE WS Intelligent Reliability Testing, Nuremberg, 2014**
- `[13]` **ASTM E1049-85 (Reapproved 2005)** Standard Practices for Cycle Counting in Fatigue Analysis ← **Rainflow/循环计数方法标准**
- `[15]` E. Wolfgang, "From Fit for Standard to Fit for Application", **Int. Symposium 3D-PEIM, College Park, MD, 2018**
- `[22]` A. Dehbi, W. Wondrak et al, "Efficient Electrothermal Simulation of Power Electronics for Hybrid Electric Vehicle", **EuroSimE 2008, Freiburg**

`[推断]` **这一组文献是功率模块可靠性领域的"最小充分集"**。用户若要深入，**Mainka/Thoben 2011 (EPE) + Bayerer 2008 (CIPS) + Scheuermann/Schmidt 2013 (PCIM)** 三篇即可覆盖从基础模型到烧结工艺的完整演进。ECPE 的 Tutorial（"Testing Automotive Power Modules according to the AQG 324"）由 AQG 324 Core Team 讲授，是**最权威的实务教材**。

### 5.4 标准原文可免费预览的技巧（实用发现）

`[一手]`：**VDE Verlag（德国 VDE 出版社，IEC 官方合作出版方）提供 IEC 标准的多页免费预览 PDF**，含 Scope、Normative references、Terms and definitions 全文。
- 样本：`info_iec60749-5{ed3.0.RLV}en.pdf`（Ed 3.0 含完整 §1 Scope、§4 General、§5 Equipment、§6 Test conditions 表格）
- `info_iec60749-4{ed2.0}b.pdf`（Ed 2.0 双语对照预览）
- 入口：https://www.vde-verlag.de/iec-normen/preview-pdf/... ｜可信度：★★★★★
- **`[推断]`** **这是获取 IEC 标准实质内容（而非仅目录）的最佳免费途径**——IEC 官网仅给目录，而 VDE 预览给出前十余页的完整正文。§4 General（失效机理描述）与 §5 Equipment（设备要求）正是加速模型前提条件的所在处。

**其他实用预览源** `[一手]`：iTeh Standards（`standards.iteh.ai`）与 `cdn.standards.iteh.ai/samples/...` 提供部分标准的 Sample PDF（同样多为前几页）。

### 5.5 工业界技术会议与期刊

**会议** `[推断，基于 AQG 324 引用链]`：
| 会议 | 全称 | 与用户相关性 |
|---|---|---|
| **ECPE** | European Center for Power Electronics 会议 | ★★★★★ **最高**（AQG 324 母体；每年 Tutorial） |
| **PCIM** | Power Conversion, Intelligent Motion | ★★★★★（功率模块寿命模型主战场） |
| **EPE** | European Power Electronics and Applications | ★★★★★（LESIT 模型首发处） |
| **CIPS** | International Conference on Power Electronics in Power Systems | ★★★★（Bayerer 模型首发处） |
| **EuroSimE** | European Simulation and Modeling Conference | ★★★（电热耦合仿真） |
| **3D-PEIM** | 3D Packaging, Equipment and Materials | ★★★（先进封装） |
| APEC | Applied Power Electronics Conference | ★★★ |

**期刊** `[推断 + 部分一手]`：
- **IEEE Transactions on Components, Packaging and Manufacturing Technology (TCPMT)** —— 封装可靠性顶刊
- **IEEE Transactions on Electron Devices (TED)**
- **Journal of Electronic Packaging (ASME)** —— 任务书提及
- **Microelectronics Reliability** —— 可靠性领域核心期刊
- **Solidification Technology** —— ⚠️ **任务书提及的"SEMI 技术期刊 Solidification Technology"存在混淆**：`Solidification Technology` 属 **Elsevier**（ casting/solidification 领域），**非 SEMI 出版**。⚠️ 标为**需核实**（待办 T10）
- **ECIA**（Electronic Components Industry Association）：行业协会，发布市场数据而非测试标准
- **IEEE Xplore**：检索入口

⚠️ **本报告未逐项核实上述期刊/会议的出版方与收录范围**（除 AQG 324 引用链已确认的 ECPE/PCIM/EPE/CIPS/EuroSimE/3D-PEIM/ASTM E1049）。标注为**推断/待核实**。

---

## 6. 交叉引用图谱（可直接转为知识 OS 的图结构）

### 6.1 以 AQG 324 为中心的一手引用图

```
                    [L4] BMW GS 95035 · VW 82324 · Daimler 采购规范
                                    │（真正约束力）
                                    ▼
                    [L3] AQG 324 Release 04.1/2025 (ECPE)
                          ├── Annex SiC (normative)
                          └── Annex GaN (future)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
  [体系/能力]                 [试验方法]                   [器件参数]
  IATF 16949                 IEC 60749-5  (THB 85/85)      IEC 60747-2  (整流二极管)
  ISO/IEC 17025              IEC 60749-6  (高温存储)          IEC 60747-8  (FET)
                             IEC 60749-23 (高温工作寿命)      IEC 60747-9  (IGBT)
                             IEC 60749-25 (温度循环)          IEC 60747-15 (隔离功率器件)
                             IEC 60749-34 (功率循环)          ↑ 热阻/杂散电感测量母标准
                             IEC 60068-2-6  (振动 Fc)
                             IEC 60068-2-27 (冲击 Ea)
                             IEC 60068-2-64 (随机振动 Fh)
                                    │
                                    ├──► JEDEC JESD22-A104F:2020 (温度循环)
                                    └──► JEDEC JESD22-A119:2015 (低温存储)
                                    ├──► IEC 60664-1 / Add.1 / -4 (绝缘配合)

  [SiC 专属方法学 — 全在 Annex SiC]
  JEDEC JEP183 (2021-01)  VT 测量
  JEDEC JEP184 (2021-03)  BTI
  JEDEC JEP190 (2022-08)  dV/dt 鲁棒性
  JEDEC JEP195 (2023-02)  栅开关不稳定性
  JEDEC JEP197 (2023-11)  双极退化
```

### 6.2 加速模型的知识图谱

```
[L0 统计物理基础]
   Arrhenius ──────┐
   Peck (RH^-2.7) ─┼──► IEC 62506 (TC 56 Dependability)  ← 模型方法论总纲
   Inverse Power ──┤        ▲
   Eyring/Black ───┘        │
   Coffin-Manson ──┐        │
   Morrow (W_p) ───┼──► 学术源头 (ECPE/PCIM/EPE/CIPS) + 教材
   Nordhoff-Peck ──┤
   Pan (蠕变权重) ┤
   Miner (累积损伤)┘
        ▲
        │ 被引用为方法学/数学
   [L2 试验条件层]
   IEC 60068 (通用环境) · IEC 60749 (半导体机械气候试验) · MIL-STD-883 (军用微电路)
   JEDEC JESD22 (封装器件试验) · GJB 548 (军用微电子) · GB/T 2423 (IEC 等同采用)
        ▲
        │ 被加严/改写/加条件
   [L3 车规层]
   AQG 324 (QL-01 PCsec / QL-02 PCmin) ◄── 内嵌 LESIT+Bayerer 寿命模型（附录 II.D）
```

---

## 7. 矛盾与未核实事项汇总（保留，不和稀泥）

| ID | 事项 | 矛盾详情 | 处置 |
|---|---|---|---|
| **C1** | JESD22-A100~A121 编号含义 | 至少三张互相矛盾的对照表（见 §4.3）；来源含黑名单 | **A104、A119 已一手确认；其余逐条核验** |
| **C2** | AQG 324 发布日期 | ECPE 网页写 04.1/2025 = "24 April 2025"；PDF 封面写 "31.03.2025" | 建议只引 "Release 04.1/2025" |
| **C3** | IEC 60749-34 年份 | AQG 324 引用表写 **2010**，正文写 **2011** | 同文件内部不一致，保留 |
| **C4** | HAST 条件温度 | 二手源给 110 °C 与 130 °C 两种 | 未核实 |
| **C5** | JEDEC 会员规模 | 二手源给 "380 members/3000 volunteers"、"300+ members"、"over 50 committees" | 未采信具体数字 |
| **C6** | JEDEC 投票门槛 | 二手源给 "75% board vote"、"2/3 majority" | 未核实 |
| **C7** | JEDEC 起始年份 | 中文源给 1958-09-26 首次会议；另有源称 1950s/1944(JETEC)/1999 独立 | 需官方确认（待办 T1） |
| **C8** | IEC 62506 现行版本与 2023 变更 | 仅二手转述（"修正计算错误、更新引用"） | 建议查 webstore.iec.ch（待办 T7） |
| **C9** | Nordhoff-Peck 公式 | 未取得权威来源 | **未核实，不写入** |
| **C10** | 三本书的作者/年份/ISBN（Booth/Lantz/Mansur、Chow、Elegant） | 检索命中的均为无关书目页 | **未核实，不写入** |
| **C11** | GB/T 4589、GB/T 13580、MIL-STD-1500 | 无一手来源 | **未核实** |
| **C12** | AEC 各文件 Rev 号 | aecouncil.com 抓取失败，来源为个人博客转录 | **未核实**（待办 T4） |
| **C13** | SEMI G1–G5 化学品等级说法 | 内容农场广泛传播，与 SEMI 官网 G=Packaging 冲突 | **判定为错误说法，但化学品等级归属仍需确认** |
| **C14** | "Solidification Technology 是 SEMI 期刊" | 疑为 Elsevier 出版 | **需核实**（待办 T10） |
| **C15** | VSME 编号与内容 | 无一手来源 | **未核实** |
| **C16** | MDPI 综述公式排版 | `exp(Ea/kT)` 应为 `exp(Ea/(k·T))` | **已判定为原文排版错误，转录时须修正** |

---

## 8. 优先级建议（针对用户的可执行结论）

**立即可做（零成本、高价值）**：
1. 下载 **AQG 324 04.1/2025 全文**（免费 CC BY-ND），把 §3 引用表 + Annex SiC + 附录 II.D 寿命模型做成知识 OS 的**核心种子**
2. 下载 **AQG 324 02.1/2019**，与 04.1/2025 做**版本 diff**（可靠性演进的可追溯证据）
3. 下载 **MIL-STD-883F 与 883L Part 1**（NASA NEPP 托管，免费），建立 1000/2000/3000/5000 四段式方法号索引
4. 用 **VDE Verlag 预览 PDF** 补齐 IEC 60749 各部分的 Scope/General/Equipment 条款
5. 读 **Mainka/Thoben 2011 (EPE)** + **Bayerer 2008 (CIPS)** + **Scheuermann/Schmidt 2013 (PCIM)** 三篇，建立功率循环寿命模型的完整学术链

**优先补齐**：
6. JEDEC 官网逐条核实 JESD22 系列（待办 T8）—— 这是最大缺口
7. 核实 AEC 各文件 Rev 号（待办 T4）
8. 核实 IEC 62506:2023 全文（待办 T7）

**体系建模建议** `[推断]`：
- 采纳 §2.1 的**五层模型**（而非三层）
- 知识 OS 应把 **IEC 62506** 而非 60749 作为**加速模型层根节点**
- 把 **AQG 324** 作为**引用关系图谱的枢纽节点**（免费、结构清晰、引用集中）
- 法规层（UNECE R10 / RoHS / WEEE）应从 **UNECE R10 附录 1** 与 **IPC-175X / IECQ QC 080000** 反查，而非从 AQG 324
- 中国国标应建"**等同采用**"边（GB/T 2423.x ≡ IEC 60068-2-x、GJB 548 ≡ MIL-STD-883），而非"引用"边

---

## 9. 任务书前提错误清单（供用户核对）

| # | 任务书表述 | 核实结果 | 依据 |
|---|---|---|---|
| 1 | MIL-STD-883 方法号 "1015.9 温循" | ❌ **1015 = burn-in；温循 = 1010.x** | MIL-STD-883F/L 官方目录 ★★★★★ |
| 2 | C. A. Harper《Electronic Packaging and **Interconnection Technology**》 | ❌ **书名为 "Handbook"**（4th ed., McGraw-Hill 2004, ISBN 9780071430487, 1000 页） | 书店目录三方一致 ★★★★☆ |
| 3 | "AQG 324 如何引用 … UNECE R10 / ELV / RoHS / WEEE 作合规锚点" | ❌ **AQG 324 零引用**；锚点是 IATF 16949 + ISO/IEC 17025 | AQG 324 全文 grep ★★★★★ |
| 4 | "AQG 324（由 ZVEI 牵头）" | ❌ **由 ECPE 持有与制定**；ZVEI 是 LV 324 阶段的联合方 | AQG 324 版权页 ★★★★★ |
| 5 | "IEC 60749 的实验设计与加速模型" | ⚠️ **部分不准确**：加速模型方法论属 **TC 56 → IEC 62506**；60749 规定试验条件 | IEC TC 组织架构 ★★★★★ |
| 6 | "IEC 60749 3" 隐含加速试验内容 | ❌ **60749-3 = External visual examination** | IEC TC 47 官方目录 ★★★★★ |
| 7 | "SEMI Mxxx 等" 隐含 M 为主要段 | ⚠️ **封装是 G 系列**（G1/G3/G4/G8/G9/G10/G14/G99），功率封装用户应主攻 G + 3D + M(SiC) | semi.org 先进封装页 ★★★★★ |
| 8 | "IEC 61800" 列入 IEC 半导体系列 | ⚠️ **未在 TC 47 出版物列表中出现**；TC 47 范围明确排除 TC 22/TC 86/JTC1 领域。IEC 61800 属调整电机驱动（TC 22/SC 22）| IEC TC 47 目录 ★★★★☆ |
| 9 | 三本参考书（Booth/Lantz/Mansur、Chow、Elegant） | ⚠️ **书目信息未核实**，本次不采信 | — |
| 10 | "Solidification Technology"作为 SEMI 技术期刊 | ⚠️ **疑为 Elsevier 出版**，需核实 | — |

---

## 10. 信源清单（一手优先）

| # | 来源 | 类型 | 可信度 | 用于 |
|---|---|---|---|---|
| 1 | https://www.ecpe.org/research/working-groups/automotive-aqg-324/ → token 直链 4 个 PDF | **一手（AQG 324 官方全文 02.1/2019、03.1/2021、04.1/2025）** | ★★★★★ | §1.4 §3.8 §6 |
| 2 | https://www.jedec.org/committees 与 /standards-documents | **一手（JEDEC 官网）** | ★★★★★ | §1.1 §4.1 |
| 3 | https://www.jedec.org/standards-documents/docs/js-9702 | **一手（JEDEC 官网）** | ★★★★★ | §1.7 |
| 4 | https://www.iec.ch/dyn/www/f?p=103:22:0::::FSP_ORG_ID:1251 | **一手（IEC TC 47 官方出版物列表）** | ★★★★★ | §1.3 |
| 5 | https://iectest.iec.ch/dyn/www/f?p=103:38:...（SC 47A） | **一手（IEC SC 47A 项目页）** | ★★★★★ | §1.3 |
| 6 | https://webstore.iec.ch/ | **一手（IEC 商店，TC 目录）** | ★★★★★ | §1.3 |
| 7 | https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-5{ed3.0.RLV}en.pdf | **一手（VDE=IEC 出版方，标准正文预览）** | ★★★★★ | §3.3 §5.4 |
| 8 | https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-4{ed2.0}b.pdf | **一手（同上）** | ★★★★★ | §3.3 |
| 9 | https://nepp.nasa.gov/docuploads/.../std883.pdf （MIL-STD-883F） | **一手（DoD 标准全文，NASA 托管）** | ★★★★★ | §1.6 |
| 10 | https://www.iclabcn.com/media/MIL-STD-883L-1-2019...pdf | **一手（MIL-STD-883L Part 1 全文）** | ★★★★★ | §1.6 |
| 11 | https://www.semi.org/en/products-services/standards | **一手（SEMI 官网）** | ★★★★★ | §1.2 |
| 12 | https://www.semi.org/cn/industry-groups/advanced-packaging/standards | **一手（SEMI 先进封装标准页）** | ★★★★★ | §1.2 |
| 13 | https://store-us.semi.org/collections/latest-standards-1 | **一手（SEMI 商店，含定价）** | ★★★★★ | §1.2 §5.2 |
| 14 | https://www.ipc.org/4.0_Knowledge/4.1_Standards/SimplifiedSpecTree.pdf | **一手（IPC 官方标准树）** | ★★★★★ | §1.7 |
| 15 | https://digitallibrary.un.org/record/248043/... (UNECE R10) | **一手（联合国数字图书馆）** | ★★★★★ | §1.4 |
| 16 | https://www.mdpi.com/2072-666X/15/3/398 | 同行评审开放获取综述 | ★★★★☆ | §3.4 §3.5 §3.7 |
| 17 | http://www.chinahls.cn/photos/.../GB/T 2423.22-2002...pdf | **一手（中国国标全文）** | ★★★★★ | §1.3 |
| 18 | https://webdesk.jsa.or.jp/pdf/dev/md_4791.pdf | **一手（JSA IEC 委员会清单，含 TC 47 范围与排除条款）** | ★★★★★ | §1.3 |
| 19 | https://pubs.acs.org/doi/10.1021/acsomega.5c06959 | 同行评审论文 | ★★★★☆ | §3.2 Ea 值 |
| 20 | http://iclabcn.com/standard/1665.html | 检测机构公开目录 | ★★★☆☆ | §1.6 GJB |
| 21 | https://www.cedm.be/rohs-service/rohs-standards | 二手汇编（RoHS/WEEE 标准清单） | ★★★☆☆ | §1.7 |
| 22 | https://www.antpedia.com/standard/1016730953-10.html | 二手（IEC 62506 条目） | ★★★☆☆ | §3.1 §3.2 §3.9 |
| 23 | https://www.eet-china.com/mp/a406501.html | 二手技术媒体 | ★★☆☆☆ | §1.4 版本演进佐证 |
| 24 | https://www.matek.com/techarticle-detail/20250501 | 二手技术媒体 | ★★☆☆☆ | §1.4 SiC 新增项佐证 |
| 25 | https://www.techstandardstore.com/product/ipc-j-std-033d | 二手书店 | ★★★☆☆ | §1.7 J-STD-033D |
| 26 | https://electronicsguide.net/.../semi-standards | 二手 | ★★★☆☆ | §1.2 SEMI 编号格式 |
| 27 | https://megalabinc.com/services/environmental-testing/iec-60068 | 二手（实验室） | ★★★☆☆ | §1.3 IEC 60068 字母表 |
| 28 | https://accendoreliability.com/metal-fatigue-failure-mechanism-accelerated-life-testing/ | 二手 | ★★☆☆☆ | §3.4 B 值表 |
| 29 | https://www.tenlong.com.tw/products/9780071430487 | 二手书店（书目） | ★★★★☆ | §5.3 Harper |
| 30 | https://www.worldofbooks.com/en-gb/products/electronic-packaging-and-interconnection-handbook-4-e... | 二手书店（书目） | ★★★★☆ | §5.3 Harper |

**已排除信源**（黑名单/低质）：知乎、微信公众号（eet-china / matek 的公众号版本）、百度百科（baike.baidu.com、newton.com.tw 的百科条目）、ima.qq.com（内容农场，且 JESD22 编号表有明显错误）、toutiao.com（内容农场，且 SEMI G1–G5 说法错误）、grokipedia.com（AI 生成站）、enrlb.com（营销站，其 AQG 324 测试映射表与一手 PDF 引用表**不一致**——见下）。

> ⚠️ **一个重要的"反例"记录**：enrlb.com（营销站）给出的 AQG 324 测试项目→标准映射表，与 AQG 324 04.1/2025 **一手引用表存在多处不符**：
> - 引用了 `DIN EN 60669-2-6`、`DIN EN 60669-2-27`、`DIN EN 60669-2-64` —— 但 **60669 系列是"电子开关"标准（electromechanical switches），与振动/冲击无关**；AQG 324 正确引用的是 **IEC 60068-2-6 / -2-27 / -2-64**。
> - 引用了 `IEC 60749-5:2003` / `IEC 60749-6:2002` —— 但一手引用表为 **2017** / **2017**。
> - 引用了 `IEC 60747-15:2012` 作为"引用标准"，但一手引用表为 **2010**（2012 是正文引用）。
> - 该站称 AQG 324 由"ZVEI 牵头"（❌）。
> **`[推断]`** 这个案例极好地印证了二手源的危害：**它把不同标准的编号张冠李戴，若入库会造成"引用关系"的系统性污染**。这正是"一手/二手/推断"三级标注的必要性。

---

## 11. 待办清单（需进一步核实）

| ID | 任务 | 优先级 | 方法 |
|---|---|---|---|
| **T1** | JEDEC 历史（1958 首次会议 / 1999 独立）、投票门槛、会员数、JESD 编号分配规则、JC-14.1 是否为 JESD22 归属委员会 | 高 | 查 JEDEC 官网 About / JM18 *JEDEC Committee Scope Manual* |
| **T2** | SEMI 沿革（1970/55 家/1973/80% 硅片） | 中 | 查 semi.org About / History |
| **T3** | IEC 60749-25 / -34 的确切现行版本年 | 高 | 查 webstore.iec.ch |
| **T4** | AEC-Q100/101/102/103/104/200 各文件 Rev 号与 [Decommissioned] 状态 | 高 | 访问 aecouncil.com/AECDocuments.html（本次 fetch failed）|
| **T5** | MIL-STD-1500、MIL-STD-202/810/1344、EIA-TIA-455 的范围与现行版本 | 中 | assist.dla.mil / quicksearch.dla.mil |
| **T6** | Nordhoff-Peck 关系式的权威表述与参数 | 中 | 学术数据库（IEEE Xplore / Springer）|
| **T7** | IEC 62506:2023 全文；"77 样本"依据；Type A/B/C 分类原文 | 高 | webstore.iec.ch |
| **T8** | **JESD22 A100–A121、B100–B121 各条确切标题** | **最高** | jedec.org 按 JC-14 facet 逐条 |
| **T9** | Booth/Lantz/Mansur、Chow、Elegant 三本书的书目信息 | 中 | WorldCat / Library of Congress / 出版社官网 |
| **T10** | Solidification Technology 出版方；VSME 编号体系 | 中 | 期刊官网 / 检索 |
| **T11** | GB/T 4589、GB/T 13580 现行版本 | 中 | std.samr.gov.cn |
| **T12** | JEDEC JESD22-A104 各温度条件字母（B/G/J/K/M）的确切定义 | 中 | 购 JEDEC 标准或经 jedec.org 查 scope |

---

**报告结束。**
**一手来源占比**：约 60% 的技术论断基于一手（标准全文/官网），二手仅用于交叉验证与反例标注。
**最大薄弱环节**：JESD22 系列编号（§4.3）—— 因核心源（jedec.org）需注册且本次未逐条核验；加速模型的数值参数（Ea、B、h、n）全部来自二手，须用自有数据标定。
