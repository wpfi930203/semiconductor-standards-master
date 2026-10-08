# Track 06 — Glossary：术语 + 编号体系 + 标准清单

> **本文件的红线**：以下每一条「编号 ↔ 标题 ↔ 适用范围」都标注了来源与可信度。凡标 `⚠️未核实` 的条目，**禁止**直接喂给查表 CLI 作为断言使用。
>
> **可信度分级**
> - **A｜一手权威**：标准组织官网（jedec.org / webstore.iec.ch / aecouncil.com / ecpe.org / semi.org）或标准原文 PDF 可查证。
> - **B｜二手交叉验证**：多个独立来源标题一致，但未取得原文（典型如中文行业汇编）。
> - **C｜待人工确认**：仅单一来源、或来源之间互相矛盾、或原文付费墙内未验证。

---

## 0. 本次调研发现的 6 个高危纠错（务必先读）

用户在需求中给出的若干前提，经一手来源核实为**错误**。这些是最容易造成工程事故的点。

| # | 常见误传 | 核实结论 | 证据 | 可信度 |
|---|---|---|---|---|
| 1 | JESD22-A108 = "Temperature, Bias and **Voltage** Life" | **错误**。官方标题为 **"Temperature, Bias, and Life Test (TBL)"**。全称无 "Voltage"。 | JEDEC 原文 PDF 扉页 "TEST METHOD A108E Temperature, Bias, and Life"；[xktest 深度解析](http://www.xktest.cn/news/show/38143.html) 明确写 "Temperature, Bias, and Life Test (TBL)" | **A** |
| 2 | MIL-STD-883 有 "M-101 降额 / M-105 功率循环 / M-110 盐雾" 等三位方法号 | **错误**。MIL-STD-883 方法号为**四位**（1001–1034 环境、2001–2035 机械）。不存在 101/105 这类三位号。降额(derating)在 MIL-STD-883 中**不以此编号存在**。 | MIL-STD-883F 原文 PDF 目录页（NASA NEPP 托管）[std883.pdf](https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf) | **A** |
| 3 | MIL-STD-883 = 环境试验方法（与 JESD22 并列） | **误导**。MIL-STD-883 是**微电路试验方法总纲**，环境(1xxx)+机械(2xxx)+电气(3xxx)+工艺(5xxx) 全含；且 **1xxx 系列与 JESD22 的 A/B/C 系列几乎一一对应**（如 1010 温循↔A104、1011 热冲击↔A106、1005 稳态寿命↔A108、1014 密封↔A109）。这是跨体系反查最有价值的一组映射。 | [MIL-STD-883F 原文](https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf)；映射交叉见 [experiorlabs](https://experiorlabs.com/mil-std-883/) | **A** |
| 4 | ESD 体系 = "JESD78-01 / JESD78-02" | **错误**。JESD78 是 **IC Latch-Up Test（闩锁测试）**，与 ESD 无关。现行版为 **JESD78F.02 (2023-11)**。ESD 体系另见 §1.4。 | [JEDEC 官方页 jesd-78b](https://www.jedec.org/standards-documents/docs/jesd-78b)；[globalspec 版本史](https://standards.globalspec.com/std/14646186/jesd78f-02) | **A** |
| 5 | JESD204 = DDR4 SDRAM | **错误**。**JESD79-4 = DDR4 SDRAM STANDARD**。JESD204 = **SerDes（串行器/解串器）接口标准**，用于数据转换器↔FPGA/ASIC。 | [JEDEC DDR4 新闻稿](https://www.jedec.org/news/pressreleases/jedec-announces-publication-ddr4-standard)（明示 "JEDEC DDR4 (JESD79-4)"）；[JEDEC node/8434 JESD79-4D](https://www.jedec.org/node/8434)；JESD204 用途见 [TI JESD204B/C 时钟培训材料](https://www.ti.com/content/dam/videos/external-videos/ko-kr/7/3816841626001/6168424753001.mp4/subassets/clocks-and-timing-clocking-jesd204bc-systems-presentation-quiz.pdf) | **A** |
| 6 | JESD22-A121 = ESD 测试 | **错误**（检索中高频误传）。**A121 = 锡及锡合金表面镀层晶须生长的测试方法（Tin Whisker）**。 | [eet-china JESD22 全表](https://mbb.eet-china.com/blog/4061550-455299.html)；A104F.01 §5.1.3 原文引用 "as stated in JESD22-A121" 对应锡须循环 | **B**（标题一致，版本号需复核） |

---

## A. 编号命名规则

### A1. JEDEC JESD 编号结构

#### A1.1 格式解析

JEDEC 文档**没有单一的官方编号文法**，实际是多套历史格式并存。查表 CLI 应按下表做**模式匹配**，而非试图用一条规则解析所有 JESD 编号。

| 模式 | 示例 | 段含义 | 可信度 |
|---|---|---|---|
| `JESD{N}` | JESD47、JESD48、JESD78、JESD201 | 顶级独立标准。N 为流水号 | **A** |
| `JESD{N}-{M}` | JESD79-4、JESD204-1、JESD3-1、JESD8-1 | 顶级标准下的**第 M 分部分/子标准**。注意此处数字**不是年份** | **A** |
| `JESD{N}{L}{NNN}` | JESD22-A104、JESD22-B105、JESD22-C101、JESD47D、JESD78F | `{L}` 为组别字母（A/B/C 见下）；`{NNN}` 为方法序号 | **A** |
| `JESD{N}-{L}{NNN}` | JESD8-11、JESD8-12 | 顶级 8 系列下的分项 | **A** |
| `JESD{N}{rev}` | JESD47H、JESD78F、JESD201A | 尾部**大写字母 = 版本修订号**，非系列字母 | **A** |
| `JESD{N}{rev}.{NN}` | JESD22-A104F.01、JESD78F.02、JESD47H.01、JESD9B | `F.01` = 版本 F 的**第 1 号增补/勘误** | **A** |
| `JESD{N}-{Letter}` | JESD7-A | 带字母后缀的分部分 | **B** |
| `JS-{NNN}[-YYYY]` | JS-001-2017、JS-002-2018 | **JS** = Joint Standard，JEDEC 与其他组织**联合**标准；后缀为年份 | **A** |
| `JEP{NNN}` | JEP122、JEP143、JEP47 | JEDEC **出版物/实践指南**（Practice/Guide），非强制标准 | **A** |
| `J-{STD}-{NNN}` | J-STD-020、J-STD-033、J-STD-002 | JEDEC 与 **IPC** 联合标准（Joint IPC/JEDEC） | **A** |
| `MO-/TO-/DO-{NNN}` | MO-047、TO-220、DO-214 | **JEP95** 下的封装外形注册号，见 §A1.5 | **B** |

#### A1.2 JESD22 的 A/B/C 组别划分（可靠性工程师最核心的一张表）

`JESD22` 全称 **"Reliability Test Methods for Packaged Devices"**（封装器件可靠性试验方法），由 **JC-14.1** 委员会维护。三组划分是按**应力物理类别**，不是按编号顺序：

| 组别 | 类别 | 覆盖应力 | 典型方法 |
|---|---|---|---|
| **A1xx** | **环境应力 / 寿命试验** | 温、湿度、电流、时间 | A104 温循、A108 TBL、A103 高温存储、A110 HAST |
| **B1xx** | **机械应力 / 几何** | 力、振动、冲击、尺寸 | B104 机械冲击、B105 引脚完整性、B112 封装翘曲 |
| **C1xx** | **电应力 / ESD** | 静电、电荷 | C101 场感应 CDM（**已废止**） |

来源：[eet-china JESD22 全表](https://mbb.eet-china.com/blog/4061550-455299.html)、[CALCE 方法表](https://web.calce.umd.edu/TSFA/methods2.htm) | 可信度 **B**

> ⚠️ 规律提示：编号递增**不代表年代先后**。A100~A108 与 A110~A122 并非严格时间排序，A109 密封、A111、A112、A116 编号在后续年份才被占用。

#### A1.3 顶级 JESD 编号（已核实者）

| 编号 | 官方标题 | 类别 | 可信度/来源 |
|---|---|---|---|
| **JESD47** | Stress-Test-Driven Qualification of Integrated Circuits | 应力测试驱动的 IC 鉴定（**最核心**，当前版 N，2026-08） | **A** [JEDEC JC-14 页](https://www.jedec.org/node/19) |
| **JESD47H.01** | Stress-Test-Driven Qualification of Integrated Circuits | 历史版（2011-04） | **A** [audace 课件](http://audace-reliability.crihan.fr/Ateliers_files/1-JEDEC%20standards%20for%20product%20level%20qualification.pdf) |
| **JESD78F.02** | IC Latch-Up Test | 闩锁测试（现行版 2023-11，94 页） | **A** [JEDEC](https://www.jedec.org/standards-documents/docs/jesd-78b) |
| **JESD79-4D** | DDR4 SDRAM STANDARD | DDR4 存储器（2021-07；前版 JESD79-3=DDR3） | **A** [JEDEC node/8434](https://www.jedec.org/node/8434) |
| **JESD79-4 (2006/2007 版)** | Low Power Double Data Rate (LPDDR) SDRAM Specification | **注意**：JESD79 顶层历史上承载过 LPDDR，DDR4 才落到 -4 分部 | **A** [globalspec 版本史](https://standards.globalspec.com/std/10163298/jedec-jesd-79-4) |
| **JESD204C** | Serializer-Deserializer (SerDes) | 高速串行接口（ADC/DAC↔FPGA）；原始版 2006-04 | **A** [TI 材料](https://www.ti.com/content/dam/videos/external-videos/ko-kr/7/3816841626001/6168424753001.mp4/subassets/clocks-and-timing-clocking-jesd204bc-systems-presentation-quiz.pdf) |
| **JESD88E** | Dictionary of Terms for Solid-State Technology | **术语字典**（查术语的首选权威） | **B** [semiengineering 归档](https://semiengineering.com/entities/jedec/) |
| **JESD201** | Environmental Acceptance Requirements for Tin Whisker Susceptibility of Tin and Tin Alloy Surface Finishes | 锡须环境验收要求 | **B** [tw-redi 汇编](http://tw-redi.com/forum.php?mod=viewthread&ordertype=2&tid=1166) |
| **JESD29A** | Failure-Mechanism-Driven Reliability Monitoring of Silicon Devices | ⚠️**已撤销**，由 JESD659 取代 | **B** 同上 |
| **JESD34** | Failure-Mechanism-Driven Reliability Qualification of Silicon Devices | ⚠️**2004 年撤销，无后续** | **B** 同上 |
| **JESD37** | Standard for Lognormal Analysis of Uncensored Data, and of Singly Right-Censored Data Utilizing the Persson and Rootzen Method | 对数正态分析（Persson/rootzen） | **B** 同上 |
| **JESD659** | Failure-Mechanism-Driven Reliability Monitoring | 取代 JESD29 | **B** 同上 |
| **JESD74A** | Early Life Failure Rate Calculation Procedure for Semiconductor Components | 早期失效率（ELFR）计算 | **B** 同上 |
| **JESD85** | Methods for Calculating Failure Rates in Units of FITs | FIT 失效率换算 | **B** 同上 |
| **JESD91** | Methods for Developing Acceleration Models for Electronic Component Failure Mechanisms | 加速模型建立（含 Arrhenius Ea 拟合） | **B** [electronicsguide](https://www.electronicsguide.net/professional-practice/reliability-engineering/standards-and-best-practices/international-reliability-standards) |
| **JESD94** | Application Specific Qualification using Knowledge Based Test Methodology | 基于知识的应用特定鉴定（**A104 自定义温循 profile 的授权依据**） | **B** 同上 |
| **JESD9B** | Inspection Criteria for Microelectronic Packages and Covers | 封装与盖板检验准则 | **B** [semiengineering](https://semiengineering.com/entities/jedec/) |
| **JESD12 / JESD12-1B~6** | Semicustom Integrated Circuits 系列（Addendum 1–6，含 Terms and Definitions for Gate Arrays and Cell-Based ICs） | 半定制 IC | **A** [JEDEC JC-44 页](https://www.jedec.org/committees/JC-44) |
| **JESD19** | General Standard for Statistical Process Control (SPC) | 统计过程控制 | **B** [tw-redi](http://tw-redi.com/forum.php?mod=viewthread&ordertype=2&tid=1166) |
| **JESD220 / -1 / -2 / -3** | Universal Flash Storage (UFS) 及其扩展/主机控制器接口 | UFS 闪存 | **B** [semiengineering](https://semiengineering.com/entities/jedec/) |
| **JESD230** | NAND Flash Interface Interoperability | NAND 闪存接口 | **B** 同上 |
| **JESD235** | High Bandwidth Memory (HBM) | 高带宽存储 | **B** [chiplet 标准 PDF](https://apexstandards.com/APEX%20STANDARDS%20N4000222%20Semiconductor%20Chiplet%20and%20Innovation%20Policy.pdf) |
| **JESD229 / -3** | Wide I/O / Wide I/O 2 | 芯粒互连 | **B** 同上 |
| **JESD71** | System-on-Chip (SoC) | SoC | **B** 同上 |
| **JESD89-1/-2/-3** | Soft Error Rate (SER) 测试 | 软错误率（AEC-Q100 E10 引用） | **B** [jjrlab AEC 对照表](https://www.jjrlab.com/news/aec-q100-ic-integrated-circuit-compliance-testing.html) |
| **JESD265** | Procedure for Reliability Characterization of Middle-Of-Line Dielectrics | 中线介质可靠性 | **B** [JEDEC JC-14](https://www.jedec.org/node/19) |
| **JESD264** | Silicon Photonics Qualification and Reliability Requirements | 硅光可靠性（2026-08） | **B** 同上 |
| **JESD82-x** | 存储器相关（Test Methods for…），如 -10/-11/-12 | ⚠️仅确认编号存在，**具体标题未核实** | **C** [snti 存档](https://snti.ru/snips_jedec-all.htm) |
| **JESD671 / JESD48 / JESD51** | — | ⚠️ **未核实**。JESD51 经证实为 LED 热测试系列（-50/-51/-52/-53），非其他含义。JESD48、JESD671 未取得权威标题，**禁止猜测** | **C** |

> `JESD8-x` 已核实为 **数字集成电路 DC 接口/逻辑电平标准族**（如 JESD8-23 "Unified Wide Power Supply Voltage Range CMOS DC Interface Standard…"），由 JC-16 维护，**与可靠性试验无关**，仅在查"逻辑电平/电源电压范围"时命中。来源：[JEDEC 文档检索](https://www.jedec.org/document_search/field_doc_type/148/field_keywords/wide-range-1956?items_per_page=5) | **A**

#### A1.4 编号整合 / 合并 / 替代案例（查表 CLI 的高价值规则）

| 旧编号 | 状态 | 现行替代 | 替代理由 |
|---|---|---|---|
| **JESD22-A114** (HBM ESD) | 已被 JS-001-2010 取代，JS-001 又迭代至 **JS-001-2017** | **ANSI/ESDA/JEDEC JS-001** | 与 ANSI/ESD STM5.1 合并，消除双重 HBM 标准 |
| **JESD22-C101** (CDM) | **2020-02 撤销** | **JS-002-2018** | 与 ANSI/ESD S5.3.1 合并 |
| **JESD22-A115** (MM) | **2016-09 起 inactive**，为参考文档，不得作为 IC 鉴证要求 | 无（MM 整体退出） | MM 产业废弃 |
| **JESD22-A112** | **被替代** | **IPC/JEDEC J-STD-020** | 湿敏等级改由 IPC 联合标准治理 |
| **JESD22-B102** (可焊性) | **2014 年废止** | **J-STD-002D** | 同上，转 IPC 体系 |
| **JESD22-B104** (机械冲击) | **2013-07 被取代** | **JESD22-B110** | B110 为现行组件机械冲击方法 |
| **JESD22-C100** (高温连续性) | 已废止 | — | — |
| **JESD29A** | 已撤销 | **JESD659C** | — |
| **JESD34** | 2004 撤销，无后续 | — | — |

**兼容条款（重要，报告/审厂常问）**：JS-001-2017 明文规定——"Data previously generated with testers meeting all waveform criteria of **ANSI/ESDA/JEDEC JS-001-2010** 及后续版本、**ANSI/ESD STM5.1-2007**、或 **JESD22-A114F** 的数据，视为有效测试数据"。
来源：[NASA EEE Parts Bulletin Vol.13 No.1](https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/EEE-Parts-Bltn-2021-Vol-13-No1-ESD-Testing-Standards-GaN-Devices-CL22-0048.pdf) | **A**

#### A1.5 JEDEC 的文档类型前缀（决定文件法律地位）

| 前缀 | 含义 | 强制性 |
|---|---|---|
| **JESD** | JEDEC Standard，**正式标准** | 强制 |
| **JS** | Joint Standard，与外部组织联合标准 | 强制 |
| **JEP** | JEDEC 出版物 / 实践指南 / 信息 | **非强制** |
| **JEB** | JEDEC Bulletin，公报 | 非强制 |
| **TENTSTD** | Tentative Standard，尝试性标准 | 试行 |
| **JES** | JEDEC Engineering Specification | — |
| **J-STD-** | IPC/JEDEC 联合标准 | 强制 |

来源：[tw-redi JEDEC 沿革与文件类型](https://tw-redi.com/forum.php?mod=viewthread&tid=977) | **B**

**JEP95 封装外形注册表**：`MO-xxx`（多端子 IC：SOP/QFP/QFN/BGA）、`TO-xxx`（晶体管外形：TO-220/TO-247/D2PAK/DPAK）、`DO-xxx`（二极管外形：DO-214 SMA/SMB/SMC）。来源：[Kynix Blog](https://www.kynix.com/Blog?CateID=24) | **B**（⚠️ 具体编号如 MO-047 未逐一核实）

#### A1.6 JESD 与 IPC / JEITA 的分工

| 组织 | 定位 | 与 JEDEC 的边界 |
|---|---|---|
| **IPC** | 电子装配（PCB/PCBA/线缆/底填） | **J-STD-020 / J-STD-033 / J-STD-002 / J-STD-001** 均 IPC+JEDEC 联合。IPCTM-650 专注 PCB 物理/化学/电气试验方法 |
| **JEITA** | 日本电子信息技术产业协会 | **EM-xxxx** 系列，多为 SEMI M 系列的**平行/竞争对应件**（如 EM-3601A ↔ SEMI M16 多晶硅；EM-3603B ↔ SEMI M41/M71 SOI；EM-3501~3504 ↔ SEMI MF 各项） |
| **JEDEC** | 器件级可靠性与接口 | — |

JE↔SEMI 对应表来源：[SEMI 5893.pdf](https://downloads.semi.org/web/wstdsbal.nsf/de4d7939711aeedf8825753e0078317f/2e9c9b25d56f36a588257edf007f4c4a/$FILE/5893.pdf)（**A**，SEMI 官方文档）→ JEITA EM-3401 平整度术语、EM-3501 晶向、EM-3502 复合寿命微波反射法、EM-3503 替位碳 FTIR、EM-3504 间隙氧 FTIR、EM-3508 微缺陷密度与 Denuded Zone、EM-3601A 高纯多晶硅、EM-3602 镜面硅片尺寸、EM-3603B SOI

---

### A2. SEMI 编号结构

#### A2.1 格式与前缀板块

**格式**：`SEMI {系列字母}{可选第二字母}{数字}-{修订码}`
其中 `-{修订码}` 为**年月修订号**，如 `SEMI M1-0924` = 2024 年 9 月版，`SEMI MF1530-0707` = 2007 年 7 月版，`SEMI S2-0818E` = 2018 年 8 月版 + 版本字母 E。

| 前缀 | 板块 | 性质 | 可信度 |
|---|---|---|---|
| **M** | Silicon Materials 硅材料与衬底 | **规范/规格（Specification）** | **A** |
| **MF** | M 系列的**试验方法**（F = test method） | Test Method | **A** |
| **E** | Equipment 设备（自动化/机械接口/通信） | 规范 | **B** |
| **ES** | E 系列的**安全**类 | 安全 | **C** |
| **S** | Safety 安全指南（EHS） | **指南（Guideline）** | **A** |
| **F** | Facilities 设施配套 | 规范 | **B** |
| **N** | ⚠️**未核实**（N1 标题未取得权威确认） | — | **C** |
| **T** | Traceability 追溯性 | 规范 | **B** |
| **C/F（合）** | Liquid Chemicals 液体化学品 + 相关设施 | 规范 | **B** |
| **G** | 用于基板/载具/掩模框类（因字母已用尽而新增） | 规范 | **C** |
| **P** | 制程工艺（含光掩模、先进封装） | 规范 | **C** |
| **A** | 自动化（**SMPT** 与 PCBA 产线机器间通信） | 规范 | **B** |
| **PV** | Photovoltaic 光伏 | 规范 | **A** |
| **MS/ME/MI** | 硅材料的试验方法/惯例/接口类细分 | — | **C** |

来源：[SEMI 中国 标准介绍](https://china.semi.org.cn/article/136)、[SEMI 中国 STANDARDS](https://china.semi.org.cn/article/240)、[SEMI 450mm Overview PDF](https://www.semi.org/sites/semi.org/files/2020-08/AUX023-00-0915.pdf) | **A/B**（分类**B**，MF/S/PV 分级 **A**）

> ⚠️ **重要**：网络上流传的"SEMI 六大系列"说法（含"C/G=化学品特气"、"E=设备自动化"、"S=EHS"、"F=工厂配套"、"M=硅材料"、"P=制程工艺"）来自自媒体（今日头条），与 SEMI 官网口径**部分不符**（官网明确 E=设备自动化、S=安全指南、F=设施、C&F=液体化学品与设施）。**以 SEMI 官网为准**。

#### A2.2 SEMI vs JEDEC vs IEC 的分界

| 主题 | SEMI | JEDEC | IEC |
|---|---|---|---|
| **硅片几何规格** | ✅ **SEMI M1** 唯一权威（直径/厚度/TTV/bow/warp/边缘排除） | ❌ 不做 | ❌ |
| **单晶硅测试方法** | ✅ SEMI MF 系列 | ❌ | ❌ |
| **SOI 硅片** | ✅ SEMI M41 / M71 | ❌ | ❌ |
| **封装器件可靠性试验** | ❌ | ✅ **JESD22** | ✅ **IEC 60749** |
| **环境应力基础方法** | ❌ | ✅（A/B/C 系列） | ✅ **IEC 60068**（通用，被 60749 引用） |
| **设备安全** | ✅ **SEMI S2** 等 | ❌ | ✅ IEC 61010/60335（通用机械电气安全） |
| **设备自动化通信** | ✅ **SEMI E5/E30（SECS/GEM）、E87** | ⚠️ JEP30（PartModel）偏产品数据模型 | ❌ |

**已核实的关键对照**：SEMI M1 §2.6 明确把非晶/外延/SOI/测试片/再生片**排除**在自己范围外，并逐一指向别家：
> "Polycrystalline silicon (refer to **SEMI M16** or JEITA EM-3601A), Epitaxial wafers (**SEMI M62**), Epitaxial wafers with buried layer (**SEMI M61**), Test wafers (**SEMI M8**), Premium wafers (**SEMI M24**), Reclaimed wafers (**SEMI M38**), Annealed wafers (**SEMI M57**), SOI wafers (**SEMI M41, SEMI M71**, or JEITA EM-3603B), Solar-grade (**SEMI PV22**)"
来源：[SEMI M1 官网条目全文](https://store-us.semi.org/products/m00100-semi-m1-specification-for-polished-single-crystal-silicon-wafers) | **A** — 这是 SEMI 内部交叉引用体系的权威一手证据。

#### A2.3 已核实的 SEMI 具体标准

| 编号 | 官方英文标题 | 可信度/来源 |
|---|---|---|
| **SEMI M1** | Specification for Polished Single Crystal Silicon Wafers | **A** [SEMI store](https://store-us.semi.org/products/m00100-semi-m1-specification-for-polished-single-crystal-silicon-wafers) |
| **SEMI M8** | Specification for Polished Monocrystalline Silicon Test Wafers | **A** 同上（M1 引用列表） |
| **SEMI M12** | Specification for Serial Alphanumeric Marking of the Front Surface of Wafers | **A** 同上 |
| **SEMI M13** | Specification for Alphanumeric Marking of Silicon Wafers | **A** 同上 |
| **SEMI M16** | Specification for Polycrystalline Silicon | **A** 同上 |
| **SEMI M18** | Guide for Developing Specification Forms for Order Entry of Silicon Wafers | **A** 同上 |
| **SEMI M20** | Practice for Establishing a Wafer Coordinate System | **A** 同上 + [MF1530 原文引用](https://img.antpedia.com/standard/files/pdfs_ora/20240730/SEMI%20MF%201530-0707-2007.pdf) |
| **SEMI M24** | Specification for Polished Monocrystalline Silicon Premium Wafers | **A** 同上 |
| **SEMI M38** | Specification for Polished Reclaimed Silicon Wafers | **A** 同上 |
| **SEMI M40** | Guide for Measurement of Roughness of Planar Surfaces on Silicon Wafers | **A** 同上 |
| **SEMI M41** | Specification of Silicon-On-Insulator (SOI) for Power Device/ICs | **A** 同上（⚠️ 与 M71 标题近似，差异需复核） |
| **SEMI M43** | Guide for Reporting Wafer Nanotopography | **A** 同上 |
| **SEMI M49** | Guide for Specifying Geometry Measurement Systems for Silicon Wafers for the 130 nm to 16 nm Technology Generations | **A** 同上 + [450mm PDF](https://www.semi.org/sites/semi.org/files/2020-08/AUX023-00-0915.pdf) |
| **SEMI M57** | Guide for Specifying Silicon Annealed Wafers | **A** 同上 |
| **SEMI M59** | Terminology for Silicon Technology | **A** 同上 — **硅领域术语权威** |
| **SEMI M61** | Specification for Silicon Epitaxial Wafers with Buried Layers | **A** 同上 |
| **SEMI M62** | Specification for Silicon Epitaxial Wafers | **A** 同上 |
| **SEMI M67** | Practice for Determining Wafer Near-Edge Geometry … Using the ESFQR, ESFQD and ESBIR Metrics | **A** 同上 |
| **SEMI M68** | Test Method for Determining Wafer Near-Edge Geometry … Using a Curvature Metric, ZDD | **A** 同上 |
| **SEMI M70** | Test Method for Determining Wafer-Near-Edge Geometry Using Partial Wafer Site Flatness | **A** 同上 |
| **SEMI M71** | Specification for Silicon-On-Insulator (SOI) Wafers for CMOS LSI | **A** 同上 |
| **SEMI M73** | Test Methods for Extracting Relevant Characteristics from Measured Wafer Edge Profiles | **A** 同上 |
| **SEMI M77** | Test Method for Determining Wafer Near-Edge Geometry Using Roll-Off Amount, ROA | **A** 同上 |
| **SEMI MF1388** | Test Method for Generation Lifetime and Generation Velocity of Silicon Material by Capacitance-Time Measurements of MOS Capacitors | **A** [SEMI 5893.pdf](https://downloads.semi.org/web/wstdsbal.nsf/de4d7939711aeedf8825753e0078317f/2e9c9b25d56f36a588257edf007f4c4a/$FILE/5893.pdf) |
| **SEMI MF1390** | Test Method for Measuring Bow and Warp on Silicon Wafers by Automated Noncontact Scanning | **A** 同上 |
| **SEMI MF1391** | Test Method for Substitutional Atomic Carbon Content of Silicon by Infrared Absorption | **A** 同上 |
| **SEMI MF1451** | Test Method for Measuring Sori on Silicon Wafers by Automated Noncontact Scanning | **A** 同上 |
| **SEMI MF1528** | Test Method for Measuring Boron Contamination in Heavily Doped n-Type Silicon Substrates by SIMS | **A** 同上 |
| **SEMI MF1530** | Test Method for Measuring Flatness, Thickness, and Total Thickness Variation on Silicon Wafers by Automated Noncontact Scanning | **A** 同上 + [标准原文 PDF](https://img.antpedia.com/standard/files/pdfs_ora/20240730/SEMI%20MF%201530-0707-2007.pdf) |
| **SEMI MF1535** | Test Method for Carrier Recombination Lifetime in Silicon Wafers by Noncontact Measurement of Photoconductivity Decay by Microwave Reflectance | **A** [SEMI 5893.pdf](https://downloads.semi.org/web/wstdsbal.nsf/de4d7939711aeedf8825753e0078317f/2e9c9b25d56f36a588257edf007f4c4a/$FILE/5893.pdf) |
| **SEMI MF1617** | Test Method for Measuring Surface Sodium, Aluminum, Potassium, and Iron on Silicon and Epi Substrates by SIMS | **A** 同上 |
| **SEMI MF1619** | Test Method for Measurement of Interstitial Oxygen Content of Silicon Wafers by Infrared Absorption Spectroscopy with p-Polarized Radiation Incident at the Brewster Angle | **A** 同上 |
| **SEMI MF1726** | Practice for Analysis of Crystallographic Perfection of Silicon Wafers | **A** 同上 |
| **SEMI MF1727** | Practice for Detection of Oxidation Induced Defects in Polished Silicon Wafers | **A** 同上 |
| **SEMI MF1809** | Guide for Selection and Use for Etching Solutions to Delineate Structural Defects in Silicon | **A** 同上 |
| **SEMI MF1982** | Test Methods for Analyzing Organic Contaminants on Silicon Wafer Surfaces by Thermal Desorption Gas Chromatography | **A** 同上 |
| **SEMI MF2074** | Guide for Measuring Diameter of Silicon and Other Semiconductor Wafers | **A** 同上 |
| **SEMI PV13** | Test Method for Contactless Excess-Charge-Carrier Recombination Lifetime Measurement … Using an Eddy-Current Sensor | **A** 同上 |
| **SEMI PV22** | Specification for Silicon Wafers for Use in Photovoltaic Solar Cells | **A** 同上 |
| **SEMI S2** | Environmental, Health, and Safety Guideline for Semiconductor Manufacturing Equipment | **B** [china.semi.org](https://china.semi.org.cn/article/136) |
| **SEMI F47** | 电压暂降（Voltage Sag）抗扰规范 | **B** 同上 — 官网称为「Voltage Sag Standard」 |
| **SEMI T3** | Specification for Wafer Box Labels | **A** [SEMI 5893.pdf](https://downloads.semi.org/web/wstdsbal.nsf/de4d7939711aeedf8825753e0078317f/2e9c9b25d56f36a588257edf007f4c4a/$FILE/5893.pdf) |
| **SEMI T7** | Specification for Back Surface Marking of Double-sided Polished Wafers with a Two-Dimensional Matrix Code Symbol | **A** 同上 |
| **SEMI E83** | Specification for PGV Mechanical Docking Flange | **A** [450mm PDF](https://www.semi.org/sites/semi.org/files/2020-08/AUX023-00-0915.pdf) |
| **SEMI E154** | Mechanical Interface for 450mm Load Port | **A** 同上 |
| **SEMI E156** | Mechanical Specification for 450mm AMHS Stocker to Transport Interface | **A** 同上 |
| **SEMI E158 / E159** | Mechanical Specification for Fab Wafer Carrier … (450 FOUP) / (450 MAC) and Kinematic Coupling | **A** 同上 |
| **SEMI E162** | Mechanical Interface Specification for 450 mm FOUP Load Port | **A** 同上 |
| **SEMI E166** | Specification for 450 mm Cluster Module Interface | **A** 同上 |
| **SEMI G88 / G92** | Specification for Tape Frame / Tape Frame Cassette for 450 mm Wafer | **A** 同上 |
| **SEMI G95** | Mechanical Interface Specification for 450 mm Load Port for Tape Frame Cassettes in the Backend Process | **A** 同上 |
| **SEMI S1/S3~S15** | 安全指南系列（S1 视觉警示、S3 加热化学槽、S8 人机工程、S10 风险评估、S14 火灾风险、S15 有毒可燃气体检测…） | **B** [china.semi.org](https://china.semi.org.cn/article/136) — ⚠️ 第三方认证站汇编，**编号↔标题对照建议以 SEMI 官网复核** |

⚠️ **SEMI N1 / SEMI C1 / SEMI T10 / SEMI E10**：本次调研**未能**从 semi.org 取得权威标题。按红线要求标注为 **C 级**，不得猜测。相关测试中出现的"SEMI M40 = 硅片表面粗糙度测量指南"已核实为正确（见上表）。

---

### A3. IEC 编号结构

#### A3.1 半导体相关 IEC 系列总览

| 系列 | 名称 | 地位 |
|---|---|---|
| **IEC 60749-x** | Semiconductor devices – Mechanical and climatic test methods | **半导体器件试验的核心系列**，共约 **42 个 part**，对标/互映射 JESD22 A+B 系列 |
| **IEC 60747-x** | Semiconductor devices – Discrete devices（分立器件） | 分立器件（含整流器、晶闸管）的特性与测量 |
| **IEC 60748-x** | Semiconductor devices – Physical/chemical characterization（物理特性测量） | 材料与界面表征 |
| **IEC 60068-x** | Environmental testing（环境试验） | **通用环境试验母标准**，半导体试验方法大量引用 |
| **IEC 60529** | Degrees of protection provided by enclosures (IP Code) | IP 防护等级 |
| **IEC 60651 / 60851** | 绕组（音频/脉冲）测量 | 磁性元件，基本不涉及半导体器件 |
| **IEC 60364** | Low-voltage electrical installations | 建筑电气，**与半导体无关**（用户清单中此项建议移除） |
| **IEC 61000-x** | Electromagnetic compatibility (EMC) | EMC 抗扰度，与 **SEMI S2 / SEMI F47** 在设备端互补 |
| **IEC 62368-x** | Audio/video, information and communication technology equipment safety | IT/音视频设备安全（**半导体器件本身很少引用**） |
| **IEC 60730-x** | Automatic electrical controls for household and similar use | 家控，**与半导体无关** |
| **IEC 61800-x** | Adjustable speed electrical power drive systems | 变频驱动，功率模块的**应用侧**标准 |

来源：[IEC TC47 官方文档列表](https://www.iec.ch/dyn/www/f?p=103:20:3655892773077::::FSP_ORG_ID,FSP_LANG_ID:1251,25) | **A**；系列规模见 [ANSI webstore](https://webstore.ansi.org/industry/semiconductors/tests/iec-60749) | **B**（"42 part series"）

#### A3.2 IEC 60749-x 逐 Part 对照表（已核实）

> 来源：**IEC 60749-35:2006 标准原文前言**（含完整 Part 1–39 清单）[enstandards PDF](https://www.enstandards.com/wp-content/uploads/pdfs/preview/1278100) | 可信度 **A**（IEC 官方文件转载，含完整结构表）；版本年份另经 [IEC TC47 列表](https://www.iec.ch/dyn/www/f?p=103:20:3655892773077::::FSP_ORG_ID,FSP_LANG_ID:1251,25) 交叉 | **A**

| Part | 英文标题 | 版本/年份 | 可信度 |
|---|---|---|---|
| 1 | General | 2002 ED1（+COR1 2003） | **A** |
| 2 | Low air pressure | 2002 ED1 | **A** |
| 3 | External visual examination（ED1 为 External visual **inspection**，2002，已删除） | **2017 ED2** | **A** |
| 4 | Damp heat, steady state, highly accelerated stress test (**HAST**) | **2017 ED2**（ED1 2002 已删除） | **A** |
| 5 | Steady-state temperature humidity bias life test | **2023 ED3**（ED2 2017 删除） | **A** |
| 6 | Storage at high temperature | 2017 ED2 | **A** |
| 7 | Internal moisture content measurement and the analysis of other residual gases | 2011 ED2 | **A** |
| 8 | Sealing（Etanchéité） | — | **A** |
| 9 | Permanence of marking | — | **A** |
| 10 | Mechanical shock | — | **A** |
| 11 | Rapid change of temperature – **Two-fluid-bath method** | — | **A** |
| 12 | Vibration, variable frequency | — | **A** |
| 13 | Salt atmosphere | — | **A** |
| 14 | Robustness of terminations | — | **A** |
| 15 | Resistance to soldering temperature for through-hole mounted devices | — | **A** |
| 16 | Particle impact noise detection (**PIND**) | — | **A** |
| 17 | Neutron irradiation | — | **A** |
| 18 | Ionizing radiation (total dose) | — | **A** |
| 19 | **Die shear strength** | — | **A** |
| 20 | Resistance of plastic-encapsulated SMDs to the combined effect of moisture and soldering heat | — | **A** |
| 21 | Solderability（Brasabilité） | — | **A** |
| 22 | **Bond strength** | — | **A** |
| 23 | **High temperature operating life** | — | **A** |
| 24 | Accelerated moisture resistance – Unbiased **HAST** | — | **A** |
| 25 | **Temperature cycling**（空气-空气） | 2003（BS EN 版 2003-10-30） | **A** |
| 26 | ESD sensitivity testing – **Human body model (HBM)** | — | **A** |
| 27 | ESD sensitivity testing – **Machine model (MM)** | — | **A** |
| 28 | ESD sensitivity testing – **Charged device model (CDM)**（2006 时在研） | — | **A** |
| 29 | **Latch-up test**（Essai de verrouillage） | — | **A** |
| 30 | Preconditioning of components for surface mount mounting, nonhermetic, prior to reliability testing | — | **A** |
| 31 | Flammability of plastic-encapsulated devices (internal ignition origin) | — | **A** |
| 32 | Flammability of plastic-encapsulated devices (external ignition origin) | — | **A** |
| 33 | Accelerated moisture resistance – **Unbiased autoclave** | — | **A** |
| 34 | **Power cycles**（Cycles en puissance） | — | **A** |
| 35 | **Acoustic microscopy for plastic encapsulated electronic components** | — | **A** |
| 36 | Constant acceleration | — | **A** |
| 37 | Component-level drop test method for portable electronic products（待发布） | — | **C** |
| 38 | Test method for logic errors of semiconductor devices with memory（在研） | — | **C** |
| 39 | Moisture diffusivity and water solubility in organic materials used in semiconductor devices（待发布） | — | **C** |

> ⚠️ **Part 25 标题陷阱**：IEC 60749-25 的英文标题在 **"Rapid change of temperature"** 与 **"Temperature cycling"** 之间存在版本/翻译差异（空气-空气法 vs 双液槽法 Part 11）。国内中文资料常统一译为"快速温度变化"。查表时应保留英文原文并注明 "-25"。| **A**

**Part 编排逻辑总结**：1=总则，2–7=环境应力（气压/HAST/THB/高温存储/内部湿气），8–9=密封与标识，10–13=机械与气候（冲击/温变/振动/盐雾），14–16=互连与端子（引线/焊接热/PIND），17–18=辐射，19–23=封装力学（芯片剪切/湿热+焊接热/可焊性/键合强度/高温工作寿命），24–28=湿气与 ESD，29=闩锁，30=预处理，31–32=阻燃，33–36=AC/功率循环/声扫/恒定加速度，37–39=新兴领域。**分组不严格连续，且后续 Part 编号是逐步追加的。**

#### A3.3 JEDEC JESD22 ↔ IEC 60749 ↔ MIL-STD-883 三体系交叉映射

这是本文件**最实用的一张表**——用户日常跨体系查标准时的实际跳转路径。

| 试验 | JEDEC | IEC 60749 | MIL-STD-883 | 备注 |
|---|---|---|---|---|
| 温度循环 TC | **A104** | Part 25 | 1010 | |
| 热冲击 | A106 | Part 11（双液槽） | 1011 | A104 明确**不涵盖**热冲击 |
| 高温存储 HTSL | A103 | Part 6 | 1008（stabilization bake，近似） | |
| 高温工作寿命 HTOL/TBL | **A108** | Part 23 | 1005（steady state life） | A108 即 HTOL |
| 间歇寿命 | — | — | 1006 | |
| 湿热偏置 THB | A101 | Part 5 | 1004（moisture resistance） | |
| 循环湿热偏置 | A100 | — | — | |
| HAST（有偏压） | A110 | Part 4 | — | |
| 加速蒸煮（无偏压） | A102 | Part 33 | — | |
| HAST（无偏压） | A118 | Part 24 | — | |
| 盐雾 | A107 | Part 13 | 1009（salt atmosphere） | |
| 密封/气密性 | A109 | Part 8 | **1014** | A109 已指向军标 |
| 机械冲击 | B104→**B110** | Part 10 | 2002 | |
| 变频振动 | B103 | Part 12 | 2007 | |
| 恒定加速度 | — | Part 36 | 2001 | |
| 芯片剪切强度 | — | **Part 19** | 2019 | |
| 键合强度 | — | **Part 22** | 2011 / 2023(ND pull) | |
| 球键合剪切 | B117 | — | — | |
| 焊球剪切 | B115 / B116 | — | — | AEC-Q100-010 |
| 倒装芯片拉脱 | B109 | — | **2031** | |
| 可焊性 | B102（**废止**→J-STD-002） | Part 21 | 2003 / 2022 | |
| 耐焊接热（通孔） | B106 | Part 15 | 2036 | |
| 引线完整性 | B105 | Part 14 | 2004 | |
| ESD HBM | A114（→**JS-001**） | Part 26 | **3015** | |
| ESD CDM | C101（→**JS-002**） | Part 28 | — | |
| ESD MM | A115（inactive） | Part 27 | — | |
| 闩锁 | **JESD78** | Part 29 | — | |
| 功率循环 | A105 / **A122** | Part 34 | — | 功率模块核心 |
| 高温功率循环 HTRB | — | — | — | 见 AQG 324 章节 |
| 老化 burn-in | JEP143 指南 | — | 1015 | |
| 预处理 | A113 | Part 30 | — | 对应 J-STD-020 |

可信度：**交叉映射整体 B**（各体系内部标题 A 级，但"哪两条互为对等"这一判断多为来源推断，非官方明示）。**⚠️ 使用建议：作为查表 CLI 的跳转建议可以，但不要在输出中宣称"官方等同"。**

---

### A4. 其他体系编号

#### A4.1 IPC 编号结构

**格式**：`IPC-{文档类型字母}-{主题号}[-{分部分}]`

| 段 | 取值 | 含义 |
|---|---|---|
| 文档类型 | **A** | **Acceptability（可接受性）** — 判定"能不能用" |
| | **B** | Binary（已废止） |
| | **C** | Coded（已废止） |
| | **D** | Design（设计标准） |
| | **J** | Joint（与 JEDEC/ASTM 联合） |
| | **S** | Specification（性能规范） |
| | **TM** | **Test Method（试验方法手册）** |
| | **SMC** | SMC 成型卡 |
| | **WH** | Wheel |
| | **SL** | Specification for Labels |
| | **E** | Engineering（内含 IPC-TM、IPC-TY、IPC-S、IPC-DS 等子类） |
| 主题号 | 数字 | 2=线缆/预浸材；22=通用设计；41=覆铜板基材；222x=PCB 设计；4101=基材；4562=铜箔；6012=刚性板；6013=柔板/刚柔板；A-600=裸板可接受性；A-610=组件可接受性；9701=焊接可靠性；7095=底部填充；1782=?? |

**IPC-TM-650 方法号结构**：`TM-650 {大类.小类.序号}`，小类含义：

| 小类 | 类别 | 典型方法 |
|---|---|---|
| **1.x** | 报告与测量分析 | 校准、环境条件、结果格式、精度 |
| **2.1** | 显微切片 / 外观 | 2.1.1 显微切片；2.1.1.1 陶瓷基板切片 |
| **2.2** | 尺寸 | 孔径、铜厚、尺寸稳定性 |
| **2.3** | 化学 | 离子污染、离子色谱、萃取物电阻率 |
| **2.4** | 机械 | 剥离强度、弯曲、扭曲 |
| **2.5** | 电气 | 电阻、绝缘、介电 |
| **2.6** | 环境/热 | Tg、T260/T288、热循环、SIR、**CAF**、回流模拟 |
| **2.8** | 电气 | 绝缘电阻、介电强度 |
| **2.9** | 表面 | 可焊性、润湿性 |

⚠️ **小类归属在各来源间不一致**（electroniccomponent.com 将 2.5 标为 Environmental、2.6 为 Thermal、2.8 为 Electrical；qfpcb 将 2.5 标为 Electrical、2.6 为 Environmental）| 可信度 **C**，需以 IPC 官方 TM-650 目录为准。

**已核实的具体方法**：2.4.18 剥离强度 / 2.4.27 扭曲与翘曲 / 2.6.2.1 DSC 测 Tg / 2.6.2.2 TMA 测 Tg / 2.6.2.4 T260-T288 / 2.6.7 热应力(288°C,10s) / 2.6.27 TMA 测 CTE / 2.3.25 离子色谱 / 2.6.3.2 表面绝缘电阻 SIR / **2.6.25 CAF（导电阳极丝）** | **B**（[electronicsguide](https://www.electronicsguide.net/professional-practice/reliability-engineering/industry-specific-applications/electronics-reliability) 明确 2.6.25 = CAF 测试；[electroniccomponent](https://electroniccomponent.com/ipc-standards-system-core-standards-electronics-manufacturing) 给全表）
⚠️ 另有来源称 2.4.22 = 热应力、2.3.25 = 剥离强度、2.6.3.7 = SIR，与上表**冲突** → 全部降为 **C 级**，**必须逐项向 IPC 官方核实后再用**。

| 编号 | 标题 | 可信度 |
|---|---|---|
| **IPC-TM-650** | Test Methods Manual（试验方法手册，非单一标准） | **A** |
| **IPC-A-610** | Acceptability of Electronic Assemblies（电子组件可接受性，Class 2/3 体系；现行 H 版 2020） | **B** |
| **IPC-A-600** | Acceptability of Printed Boards（裸板可接受性） | **B** |
| **IPC-6012** | Qualification and Performance Specification for Rigid Printed Boards | **B** |
| **IPC-6013** | Qualification and Performance Specification for Flexible and Rigid-Flexible Printed Boards | **B** |
| **IPC-9701** | Solder Attachment Reliability Testing（焊点连接可靠性，定义 TC1–TC5 测试条件） | **B** |
| **IPC-2221 / -2222** | Generic Design / 刚性板设计 | **B** |
| **IPC-4101 / -4562** | 覆铜板基材 / 铜箔 | **B** |
| **IPC-7711 / -7721** | 维修与返工 | **B** |
| **IPC-9252** | Guidelines and Requirements for Electrical Testing of Unpopulated Printed Boards | **B** |
| **IPC-7095** | Design and Assembly Process Implementation for Bottom Mount Underfill Components | **B** |
| **IPC-1782** | ⚠️ **未核实** | **C** |
| **IPC/JEDEC J-STD-020E** | Moisture/Reflow Sensitivity Classification for Nonhermetic Solid State Surface Mount Devices | **B** |
| **IPC/JEDEC J-STD-033D** | Handling, Packing, Shipping and Use of Moisture/Reflow Sensitive Surface Mount Devices | **B** |
| **J-STD-001** | Requirements for Soldered Electrical and Electronic Assemblies（**J-STD-001 规范过程，IPC-A-610 判定结果**） | **B** |
| **J-STD-002** | Solderability Tests for Component Leads, Terminations, Lugs…（取代 JESD22-B102） | **B** |
| **J-STD-004** | Flux（助焊剂）分类 | **B** |
| **J-STD-005** | Solder Paste | **B** |
| **J-STD-020 / -033 配套符号** | JEP113-B Symbol and Labels for Moisture-Sensitive Devices | **B** |

来源：[electroniccomponent IPC 体系](https://electroniccomponent.com/ipc-standards-system-core-standards-electronics-manufacturing)、[benewavetech](https://www.benewavetech.com/blog-insights/ipc-standards-in-pcb-assembly-manufacturing.html)、[qwctest JEDEC/IPC 对照](https://www.qwctest.com/m/news_detail.aspx?id=703)

#### A4.2 AQG 324（汽车功率模块，功率封装工程师最相关）

| 项 | 内容 |
|---|---|
| **全称** | **AQG 324 — Qualification of Power Modules for Use in Power Electronics Converter Units (PCUs) in Motor Vehicles** |
| **发布方** | **ECPE**（European Center for Power Electronics e.V.）工作组 **"Automotive Power Module Qualification"** |
| **前身** | **LV 324**（德国 OEM + 功率电子供应商编制规范） |
| **首版** | 2017 启动，**2018-04 首版发布** |
| **现行版** | **Release 04.1/2025，日期 2025-03-31**（主文件覆盖 Si 基功率半导体模块，SiC 模块置于专门附录） |
| **适用范围** | 模块设计与**模块级器件（即封装体）**鉴定；**不涵盖芯片本身或制造工艺**的鉴定 |
| **起草方** | 奥迪、BMW、戴姆勒、保时捷、大众等厂代 + 功率电子供应商 |

**四大测试类别与项目**（源自标准章节编码）：

| 章节 | 类别 | 测试项目 |
|---|---|---|
| **QM** | 模块检测 | 栅极阈值电压、栅极漏电流、集射极反向漏电流、饱和压降、连接层检测 (**SAM**)、外观检 IPI/目检 VI/光学显微镜评估 OMA |
| **QC** | 模块特性测试 | 寄生杂散电感、热阻值、**短路耐量**、绝缘测试、机械参数检测 |
| **QE** | 环境测试 | 热冲击、机械振动、机械冲击 |
| **QL** | 寿命测试 | **功率循环 (PCsec / PCmin)**、高温存储、低温存储、高温反偏(HTRB)、高温栅偏(HTGB)、高温高湿反偏(H3TRB) |

**PCsec vs PCmin（功率模块最核心的区分）**：

| 模式 | 通电时间 | ΔTj | 主要考核失效部位 |
|---|---|---|---|
| **PCsec** | ton ≈ **2 s**（秒级） | 大（≈80–100 K） | **键合线 / 芯片近旁连接**（wire bond fatigue、bond lift-off） |
| **PCmin** | ton > **15 s**（通常 60–120 s，分钟级） | 较小 | **基板焊料层**（solder layer fatigue、DBC 界面） |

**2025 版 SiC 扩展项**：动态栅极应力 (**DGS**)、动态反偏 (**DRB**)、动态 **H3TRB**、**Delta Qualification Matrix**（简化变更验证）

**典型失效判据**：V_CE(on) 增加 > 初始值 5% 或 20%、热阻增加 > 20%、出现热失控。
**样品要求**：≥3 个不同生产批次；各测试项目 6–10 颗，总数 50–100 颗；须为最终量产封装。

来源：[ECPE Tutorial 官方文件（Release 04.1/2025 表述）](https://www.ecpe.org/index.php?eID=dumpFile&t=f&f=48794&token=037807486092cda70980da9de21e3ed0b16646eb) | **A**；[英飞凌知识库（LV324 前身与 AQG324 关系）](https://community.infineon.com/t5/%E7%9F%A5%E8%AF%86%E5%BA%93%E6%96%87%E7%AB%A0/IGBT%E5%92%8C%E6%A8%A1%E5%9D%97%E7%9A%84%E6%A0%87%E5%87%86%E4%BD%93%E7%B3%BB%E8%A7%A3%E8%AF%BB/ta-p/436857) | **A**；章节编码与条件范围 | **B**（[enrlb](http://www.enrlb.com/Faq-157.html)、[jiancepcb](https://www.jiancepcb.com/aqg324-power-module-guide/)）

> ⚠️ 具体数值条件（如 ΔTj=60–100 K、3–5 万次循环、85°C/85%RH 1000 h）来自第三方检测站，**各检测站之间存在差异**（如 dsfjiance 称功率循环"3–5 万次"，jiancepcb 称"数万循环"）| **C 级**，实际取值须以 Release 04.1/2025 原文为准。

#### A4.3 AEC-Q1xx 编号结构

**格式**：`AEC-Q{产品类}{序号}[-{试验项序号}]`
- **Q100** = Integrated Circuits（IC）
- **Q101** = Discrete Semiconductors（分立器件）
- **Q102** = Discrete Optoelectronic Semiconductors
- **Q103** = Sensors（含 MEMS 压力传感器、MEMS 麦克风）
- **Q104** = Multichip Modules (MCM)
- **Q200** = Passive Components
- **Q001/Q002/Q003/Q005/Q006** = 指南类（非 Q1xx 试验项）

**修订号规则**：Q100 主体用**大写字母**（Rev-H 2014-09-11、**Rev-I**、**Rev-J** 当前）；附件用**数字**（Q100-002 Rev-E）。这与 JEDEC 的版本号规则一致。

**Q100 附件全清单（官方一手核实）**：

| 附件编号 | 官方标题 | 状态 |
|---|---|---|
| **Q100-001** | Wire Bond Shear Test | Rev-C |
| **Q100-002** | Human Body Model (HBM) Electrostatic Discharge Test | Rev-E |
| ~~Q100-003~~ | ~~Machine Model (MM) Electrostatic Discharge Test~~ | **DECOMMISSIONED**（Rev-H 起移除，行业测试过时） |
| **Q100-004** | IC Latch-Up Test | Rev-D |
| **Q100-005** | Non-Volatile Memory Program/Erase Endurance, Data Retention, and Operational Life Test | Rev-D1 |
| ~~Q100-006~~ | ~~Electro-Thermally Induced Parasitic Gate Leakage (GL) Test~~ | **DECOMMISSIONED**（缺少行业需求） |
| **Q100-007** | Fault Simulation and Test Grading | Rev-B |
| **Q100-008** | Early Life Failure Rate (ELFR) | Rev-A |
| **Q100-009** | Electrical Distribution Assessment | Rev-B |
| **Q100-010** | Solder Ball Shear Test | Rev-A |
| **Q100-011** | Charged Device Model (CDM) Electrostatic Discharge Test | Rev-D |
| **Q100-012** | Short Circuit Reliability Characterization of Smart Power Devices for 12V Systems | Rev- |

**Q101 附件**：Q101-001 HBM (Rev-A)、Q101-003 Wire Bond Shear (Rev-A)、Q101-004 Miscellaneous Test Methods、Q101-005 CDM (Rev-A)、Q101-006 Short Circuit Reliability 12V
**Q200 附件**：Q200-001 Flame Retardance (Rev-B)、Q200-002 HBM (Rev-B)、Q200-003 Beam Load (Rev-B)、Q200-004 Resettable Fuses (Rev-A)、Q200-005 Board Flex/Terminal Bond Strength (Rev-A)、Q200-006 Terminal Strength (SMD)/Shear (Rev-A)、Q200-007 Voltage Surge (Rev-A)

来源：**[AEC 官方文档页](http://aecouncil.com/Documents/AECDocuments.html)** | **A** — 这是本表中可信度最高的一组，**零歧义**。

**AEC-Q100 Grade 温度分级**：Grade 0 = −40~+150 °C；Grade 1 = −40~+125 °C；Grade 2 = −40~+105 °C；Grade 3 = −40~+85 °C（**Grade 4 = 0~+70 °C 已在 Rev-H 中删除**）| **A**（[AEC-Q100 Rev-H PDF](http://www.aecouncil.com/Documents/AEC_Q100_Rev_H_Base_Document.pdf) 明确 "eliminated Grade 4 entry"）

**AEC 与 JEDEC 的引用关系**（经 [jjrlab 对照表](https://www.jjrlab.com/news/aec-q100-ic-integrated-circuit-compliance-testing.html) | **B** 交叉）：AEC-Q100-002 基于 JS-001；Q100-011 基于 JS-002；Q100-004 基于 JESD78；SER 用 JESD89-1/-2/-3；EMC 用 SAE J1752/3。

**AEC-Q100 测试组结构**：Group A（应力试验）、Group B（加速寿命）、Group C（封装完整性）、Group D（晶圆级）、Group E（缺陷筛查）、Group F（缺陷筛查）… 各组代号在来源间不一致（如 jjrlab 用 E1–E11 / G1–G8，AEC 原文用 A1–A6/B1–B3/C3–C9/E1–E5/E10）| **B**，建议直接查 AEC 原文 Table 2。

#### A4.4 MIL-STD-883 方法号（权威版，NASA NEPP 托管原文）

**格式**：`MIL-STD-883 {Method No.}`，方法号为**四位**：
- **1xxx** = 环境试验（Environmental Tests）
- **2xxx** = 机械试验（Mechanical Tests）
- **3xxx** = 电气试验
- **5xxx** = 工艺/试验程序（Process Tests）

**1xxx 环境试验完整清单**（来自 MIL-STD-883F 原文目录）：

| 方法号 | 标题 |
|---|---|
| 1001 | Barometric pressure, reduced (altitude operation) |
| 1002 | Immersion |
| 1003 | Insulation resistance |
| 1004.7 | Moisture resistance |
| **1005.8** | **Steady state life** ← HTOL 军标对应 |
| 1006 | Intermittent life |
| 1007 | Agree life |
| 1008.2 | Stabilization bake |
| 1009.8 | Salt atmosphere (corrosion) |
| **1010.7/1010.8** | **Temperature cycling** |
| **1011.9** | **Thermal shock** |
| 1012.1 | Thermal characteristics |
| 1013 | Dew point |
| **1014.11** | **Seal** |
| 1015.9 | Burn-in test |
| 1016.1 | Life/reliability characterization tests |
| 1017.2 | Neutron irradiation |
| **1018.4** | Internal water-vapor content |
| 1019.6 | Ionizing radiation (total dose) test procedure |
| 1020.1 | Dose rate induced latchup test procedure |
| 1021.2 | Dose rate upset testing of digital microcircuits |
| 1022 | MOSFET threshold voltage |
| 1023.2 | Dose rate response of linear microcircuits |
| 1030.2 | Preseal burn-in |
| 1031 | Thin film corrosion test |
| 1032.1 | Package induced soft error test procedure (due to alpha particles) |
| 1033 | Endurance life test |
| 1034.1 | Die penetrant test (for plastic devices) |

**2xxx 机械试验完整清单**：

| 方法号 | 标题 | 封装相关性 |
|---|---|---|
| 2001.2 | Constant acceleration | ★ |
| 2002.3 | Mechanical shock | ★ |
| 2003.7 | Solderability | ★ |
| 2004.5 | Lead integrity | ★ |
| 2005.2 | Vibration fatigue | |
| 2006.1 | Vibration noise | |
| 2007.2 | Vibration, variable frequency | ★ |
| 2008.1 | Visual and mechanical | |
| **2009.9** | **External visual** | ★ |
| 2010.10 | Internal visual (monolithic) | ★ |
| **2011.7** | **Bond strength (destructive bond pull test)** | ★★★ 键合 |
| 2012.7 | Radiography | ★ |
| 2013.1 | Internal visual inspection for DPA | |
| 2014 | Internal visual and mechanical | ★ |
| 2015.11 | Resistance to solvents | |
| 2016 | Physical dimensions | ★ |
| 2017.7 | Internal visual (hybrid) | |
| 2018 | **Scanning electron microscope (SEM) inspection of metallization** | ★★★ 失效分析 |
| **2019.5** | **Die shear strength** | ★★★ 芯片剪切 |
| 2020.7 | Particle impact noise detection test | |
| 2021.3 | Glassivation layer integrity | ★ |
| 2022.2 | Wetting balance solderability | ★ |
| **2023.5** | **Nondestructive bond pull** | ★★★ 键合 |
| **2024.2** | **Lid torque for glass-frit-sealed packages** | ★★★ 陶瓷盖板 |
| 2025.4 | Adhesion of lead finish | ★ |
| 2026 | Random vibration | |
| **2027.2** | **Substrate attach strength** | ★★★ 基板附着 |
| 2028.4 | Pin grid package destructive lead pull test | |
| 2029 | Ceramic chip carrier bond strength | ★★★ 陶瓷载板 |
| **2030** | **Ultrasonic inspection of die attach** | ★★★ 超声扫描 die attach |
| **2031** | **Flip chip pull-off test** | ★★★ 倒装拉脱 |
| 2032 | Visual inspection of passive elements | |
| **2035** | **Ultrasonic inspection of TAB bonds** | ★★★ TAB |
| 2036 | Resistance to soldering heat | ★ |

来源：[MIL-STD-883F 原文 PDF（NASA NEPP）](https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf) | **A**（政府托管的标准原文）

**其他军标方法号**（用户清单中缺失但重要）：
- **MIL-STD-750 方法 1020** = ESD 敏感度分类（HBM）| **A** [NASA EEE Bulletin](https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/EEE-Parts-Bltn-2021-Vol-13-No1-ESD-Testing-Standards-GaN-Devices-CL22-0048.pdf)
- **MIL-STD-883 TM3015** = 微电路 ESD 敏感度分类 | **A** 同上
- **MIL-STD-750A 方法 2030** = 陶瓷芯片载体键合强度 | **C**

> ⚠️ 用户清单中的 "MIL-STD-883 Method 5011 = 商用塑封件的军用认证途径" 来自第三方，**未核实** | **C**

#### A4.5 GJB / GB/T / SAE / JIS / UL

| 体系 | 编号逻辑 | 已核实要点 | 可信度 |
|---|---|---|---|
| **GJB（国军标）** | `GJB {类别码}-{序号}-{年号}`，如 GJB 548A-2012 | 体系对标 MIL-STD-883，方法号编排类似。⚠️ 具体某编号对应标题**未核实** | **C** |
| **GB/T** | `{GB/T {序号}-{年号}}`，序号 14264=半导体材料术语、1550=导电类型、1553=间隙氧红外吸收、1554=晶体完整性腐蚀检验、14140=硅片直径 XRD 定向法、24578=硅片表面金属沾污 TXRF、4937=半导体器件系列（机械与气候试验方法） | GB/T 4937 是 **IEC 60749 的等同采用**（对应关系：GB/T 4937 第 x 部分 ↔ IEC 60749-x）| **B** [bjhgyjs 硅片检测](https://www.bjhgyjs.cn/news/qitajiance/2022/05/200293.html) |
| **SAE** | `SAE J{number}`，如 **SAE J1752/3** = 辐射发射 | AEC-Q100 E8 EMC 引用 SAE J1752/3 | **B** [jjrlab](https://www.jjrlab.com/news/aec-q100-ic-integrated-circuit-compliance-testing.html) |
| **JIS** | `JIS H {序号}-{年号}`，如 **JIS H 0604** = 少数载流子寿命光电导衰减法 | JIS H 0604 对应 SEMI MF1535 / JEITA EM-3502 | **A**（SEMI 官方文件 [5893.pdf](https://downloads.semi.org/web/wstdsbal.nsf/de4d7939711aeedf8825753e0078317f/2e9c9b25d56f36a588257edf007f4c4a/$FILE/5893.pdf) 内列出） |
| **JESD22 / GB/T 对照** | GB/T 4937 等同采用 IEC 60749，**不是** JESD22 | — | **C** |
| **UL** | `UL {序号}`；**UL 1557** = Standard for Electrically Isolated Semiconductor Devices | IGBT 模块的 UL 认证执行 **UL 1557**（有 COA，认可条件限定）| **B** [英飞凌](https://community.infineon.com/t5/%E7%9F%A5%E8%AF%86%E5%BA%93%E6%96%87%E7%AB%A0/IGBT%E5%92%8C%E6%A8%A1%E5%9D%97%E7%9A%84%E6%A0%87%E5%87%86%E4%BD%93%E7%B3%BB%E8%A7%A3%E8%AF%BB/ta-p/436857) |
| **Telcordia** | GR-468-CORE（光电器件可靠性要求）、GR-63-CORE（NEBS 物理防护）、GR-1089-CORE（EMC 与电气安全）、SR-332（失效率预测） | 通信设备领域；SR-332 基于电信元件数据，通常比 MIL-HDBK-217 乐观，**两者不可直接比较** | **B** [electronicsguide](https://www.electronicsguide.net/professional-practice/reliability-engineering/standards-and-best-practices/international-reliability-standards) |
| **IEC 60068** | `{IEC 60068-2-xx}`（环境试验 2-xxx 系列） | 半导体试验方法的通用母标准 | **B** |

---

## C. JESD22 系列方法清单（核心交付物）

> **字段说明**：应力条件列为标准内的**典型**条件；具体验收判据须查对应版次原文。
> **来源**：标题列综合 [eet-china JESD22 全表](https://mbb.eet-china.com/blog/4061550-455299.html)、[qwctest 汇编](https://www.qwctest.com/m/news_detail.aspx?id=703)、[CALCE](https://web.calce.umd.edu/TSFA/methods2.htm)、[eetop 版本表](https://bbs.eetop.cn/thread-960721-1-1.html) | 标题可信度 **B**；A104/A108/A110 等有官方或原文佐证者为 **A**。

### C1. A1xx — 环境应力 / 寿命试验

| 编号 | 英文标题（原文） | 试验类型 | 典型应力条件 | 封装可靠性用途 | 版本/状态 | 可信度 |
|---|---|---|---|---|---|---|
| **JESD22-A100** | Cycled Temperature-Humidity Bias Life Test | 湿热偏置寿命（循环） | 交替冷凝/干燥周期，加偏压 | 湿气+电化学迁移、腐蚀 | **E**, Nov 2020 | **B** |
| **JESD22-A101** | Steady State Temperature Humidity Bias Life Test | 稳态湿热偏置寿命（THB） | 85 °C/85 %RH，1000 h，加偏压 | 湿气驱动的腐蚀与迁移 | **D.01**, Jan 2021 | **B** |
| **JESD22-A102** | Accelerated Moisture Resistance — Unbiased Autoclave | 加速蒸煮（无偏压） | 121 °C / 100 %RH / 15–30 psig，96–1000 h | 塑封体吸湿爆裂、分层 | **E**, Jan 2021 | **B** |
| **JESD22-A103** | High Temperature Storage Life | 高温存储寿命（HTSL） | 150 °C，1000 h，**无偏压** | 模塑料/粘接层热稳定性 | **E.01**, Jul 2021 | **B** |
| **JESD22-A104** | **Temperature Cycling** | **温度循环（TC）** | **见 §C5 完整表** | **焊点疲劳、分层、键合疲劳（核心）** | **F.01**, Apr 2023 | **A** |
| **JESD22-A105** | **Power and Temperature Cycling** | 功率温度循环（PTC） | 外部加热 + 通电循环 | 功率器件热循环 | **D**, Jan 2020 | **B** |
| **JESD22-A106** | Thermal Shock | 热冲击（TS） | 两液槽法，转换时间 <10 s | 快速温变应力（**与 TC 是不同试验**） | **B.01**, Nov 2016 | **B** |
| **JESD22-A107** | Salt Atmosphere | 盐雾 | — | 离子污染腐蚀 | **C**, Apr 2013 | **B** |
| **JESD22-A108** | **Temperature, Bias, and Life Test (TBL)** ★ | 高温工作寿命（HTOL） | Tj ≥125 °C，1000 h，**动态偏压** | 栅氧/互连/HCI 长期寿命 | **G**, 2022（替代 F/2017-07）| **A** |
| **JESD22-A109** | Hermeticity | 气密性 | 氦细漏/碳氢化合物粗漏 | 陶瓷/气密封装的密封性 | **B**, Nov 2011（**现行，指向军标**）| **B** |
| **JESD22-A110** | Highly-Accelerated Temperature and Humidity Stress Test (**HAST**) | 有偏压 HAST | 130 °C/85 %RH，96 h，加偏压 | 湿热+偏压综合 | **E.01**, May 2021 | **B** |
| **JESD22-A111** | (Surface Mount Solidity Test for)(Components Mounted in a Single Panel on the Bottom) | 单面板底面小型表贴器件耐浸焊能力评价流程 | — | 可焊性/浸焊 | **B**, Mar 2018 | **B** |
| ~~JESD22-A112~~ | ~~Moisture-Induced Stress Sensitivity for Plastic Surface Mount Devices~~ | ⚠️ **被替代 → J-STD-020** | — | — | A, Nov 1995 | **B** |
| **JESD22-A113** | Preconditioning of Nonhermetic Surface Mount Devices Prior to Reliability Testing | 预处理（PC） | 按 MSL 分级的 soak + 红外 + **回流** | MSL 相关的分层/爆裂（**TC/HAST 前必做**）| **I**, Apr 2020 | **B** |
| ~~JESD22-A114~~ | ~~ESD Sensitivity Testing, Human Body Model (HBM)~~ | ⚠️ **→ JS-001** | — | — | F, Dec 2008 | **A** |
| **JESD22-A115** | ESD Sensitivity Testing, Machine Model (MM) | MM ESD | — | — | **C**，2016-09 inactive | **A** |
| **JESD22-A117** | Electrically Erasable Programmable ROM (EEPROM) Program/Erase Endurance and Data Retention Test | EEPROM 耐久 | — | 存储类 | **E**, Nov 2018 | **B** |
| **JESD22-A118** | Accelerated Moisture Resistance — Unbiased HAST | 无偏压 HAST（uHAST） | 130 °C/85 %RH | 湿气分层（无偏压） | **B.01**, May 2021 | **B** |
| **JESD22-A119** | Low Temperature Storage Life | 低温存储寿命（LTSL） | — | 低温 CTE 失配 | **A**, Oct 2015 | **B** |
| **JESD22-A120** | Test Method for the Measurement of Moisture Diffusivity and Water Solubility in Organic Materials Used in Integrated Circuits | 有机材料湿气扩散率与水溶解度 | — | **模塑料/底填胶吸湿建模** | **B**, Jul 2014 | **B** |
| **JESD22-A121** | Test Method for **Tin Whisker** Growth… | 锡须生长 | **约 3 cph**，soak 5–10 min | 纯锡镀层/焊接球须晶 | **A**, Jul 2008 | **B** |
| **JESD22-A122** | **Power Cycling** | 功率循环（PC） | 通电加热循环 | **IGBT/SiC 模块键合与焊层疲劳（核心）** | **A**, Jun 2016 | **B** |
| **JESD22-A200 系列** | ⚠️ **未核实** | — | — | — | — | **C** |

> ⚠️ **A108 版本说明**：A108F = 2017-07；**A108G = 2022** 替代 F。有来源称 A108G 名为 "Temperature, Bias, and Life Test (TBL)"，与 F 版标题 "Temperature, Bias, and Operating Life" 略有差异 → **A 版本间标题有变，查表时应写 A108 + 版本号**。

### C2. B1xx — 机械应力 / 几何

| 编号 | 英文标题 | 典型用途 | 版本 | 状态 | 可信度 |
|---|---|---|---|---|---|
| **JESD22-B100** | Physical Dimensions | 外形尺寸测量 | B, Jun 2003 | 现行 | **B** |
| **JESD22-B101** | External Visual | 外观目检 | C, Oct 2015 | 现行 | **B** |
| ~~JESD22-B102~~ | ~~Solderability Test Method~~ | 可焊性 | E, Oct 2007 | ⚠️**2014 废止 → J-STD-002D** | **B** |
| **JESD22-B103** | Vibration, Variable Frequency | 变频振动 | B.01, Sep 2016 | 现行 | **B** |
| ~~JESD22-B104~~ | ~~Mechanical Shock~~ | 机械冲击 | C, Nov 2004 | ⚠️**2013-07 → B110** | **B** |
| **JESD22-B105** | Lead Integrity | 引线完整性（Lead Integrity） | E, Feb 2017 | 现行 | **B** |
| **JESD22-B106** | Resistance to Soldering Temperature for Through-Hole Mounted Devices | 通孔件耐焊接热 | E, Nov 2016 | 现行 | **B** |
| **JESD22-B107** | Marking Permanency | 标识耐久性 | D, Mar 2011 | 现行 | **B** |
| **JESD22-B108** | Coplanarity Test for Surface-Mount Semiconductor Devices | 表贴器件共面性 | B, Sep 2010 | 现行 | **B** |
| **JESD22-B109** | Flip Chip Pull-off Test | 倒装芯片拉脱 | C, Mar 2021 | 现行 | **B** |
| **JESD22-B110** | Mechanical Shock（Component） | **现行**机械冲击 | B.01, Jun 2019 | 现行 | **B** |
| **JESD22-B111** | Board Level Drop Test Method of Components for Handheld Electronic Products | 板级跌落 | A, Nov 2016 | 现行 | **B** |
| **JESD22-B112** | Package Warp Test Method at High Temperature | 高温封装翘曲 | B, Aug 2018 | 现行 | **B** |
| **JESD22-B113** | Board Level Cyclic Bend Test Method for Interconnect Reliability Characterization of Components for Handheld Electronic Products | 板级循环弯折（**互连可靠性**） | B, Aug 2018 | 现行 | **B** |
| **JESD22-B114** | Marking Legibility | 标识可识别性 | B, Jan 2020 | 现行 | **B** |
| **JESD22-B115** | Ball Shear Test | **焊球剪切**（对应 AEC-Q100-010） | A.01, Jul 2016 | 现行 | **B** |
| **JESD22-B116** | Wire Bond Shear Test Method | **引线键合剪切**（对应 AEC-Q100-001） | **C**, Aug 2026 | 现行 | **B** |
| **JESD22-B117** | BGA Ball Shear | 焊球剪切（BGA） | B, May 2014 | 现行 | **B** |
| **JESD22-B118** | Visual Inspection of Semiconductor Wafers and Wafers with Backside Coating | 晶圆/背面涂覆目检 | A, Nov 2021 | 现行 | **B** |
| **JESD22-B119** | Steady Mechanical Pressure | 稳态机械压力 | — | ⚠️ **未核实** | **C** |
| **JESD22-B121A** | （X 射线 TID 试验相关） | — | A, Aug 2026 | ⚠️ **未核实标题** | **C** |
| **JESD22-B122** | Board Level Vibration Test Method of Semiconductor Packages for General Electronic and Automotive Products | 板级振动（通用+汽车） | — | Sep 2026 | **B** |

### C3. C1xx — 电应力 / ESD

| 编号 | 英文标题 | 状态 | 可信度 |
|---|---|---|---|
| ~~JESD22-C100~~ | ~~High Temperature Continuity~~ | **已废止** | **B** |
| ~~JESD22-C101~~ | ~~Field-Induced Charged-Device Model Test Method for Electrostatic Discharge Withstand Thresholds of Microelectronic Components~~ | ⚠️ **2020-02 撤销 → JS-002-2018** | **A** |

### C4. 非 JESD22 但高频的 JEDEC 编号

| 编号 | 标题 | 用途 | 可信度 |
|---|---|---|---|
| **JESD47** | Stress-Test-Driven Qualification of Integrated Circuits | **鉴证总纲**：定义哪些试验、各多少样本、验收判据 | **A** |
| **JESD78** | IC Latch-Up Test | 闩锁（**注意：与 ESD 无关**）| **A** |
| **JESD88** | Dictionary of Terms for Solid-State Technology | **术语字典** | **B** |
| **JESD201** | Environmental Acceptance Requirements for Tin Whisker Susceptibility… | 锡须验收 | **B** |
| **JESD91** | Methods for Developing Acceleration Models for Electronic Component Failure Mechanisms | **加速模型（含 Ea 拟合）** | **B** |
| **JESD94** | Application Specific Qualification using Knowledge Based Test Methodology | 自定义应力条件的授权依据 | **B** |
| **JESD85** | Methods for Calculating Failure Rates in Units of FITs | FIT 换算 | **B** |
| **JEP122** | Failure Mechanisms and Models for Semiconductor Devices | **失效机理与 Ea 表（PoF 基础）** | **B** |
| **JEP143** | Solid State Reliability Assessment Qualification Methodologies（burn-in 指南）| 老化 | **B** |
| **JEP131** | Potential Failure Mode and Effects Analysis (FMEA) | FMEA | **B** |
| **JEP148** | Reliability Qualification of Semiconductor Devices Based on Physics of Failure Risk and Opportunity Assessment | 基于 PoF 的鉴定 | **B** |
| **JEP150** | Stress-Test-Driven Qualification and Failure Mechanisms Associated with Assembled Solid State Surface-Mount Components | 表贴组件 | **B** |
| **JEP174** | Understanding Electrical Overstress — EOS | EOS 理解 | **B** |
| **JEP140** | Beaded Thermocouple Measurement of Semiconductor Packages | 热电偶测温（**A104 引用的方法文件**）| **A**（A104F.01 参考文献原文） |
| **JEP153** | Characterization and Monitoring of thermal Stress Test Oven Temperatures | 烘箱温度监控（**A104 引用**）| **A**（同上） |
| **JS-001-2017** | ESDA/JEDEC Joint Standard for ESD Sensitivity Testing — HBM — Component Level | HBM 现行 | **A** |
| **JS-002-2018** | ESDA/JEDEC Joint Standard for ESD Sensitivity Testing — CDM — Device Level | CDM 现行 | **A** |
| **IPC-SM-785** | Guidelines for Accelerated Reliability Testing of Surface Mount Solder Attachments | **焊点可靠性加速测试指南（A104 引用）** | **A**（A104F.01 参考文献原文） |

### C5. JESD22-A104F.01 温度循环完整条件表（一手原文核实）

> 来源：**JEDEC JESD22-A104F.01 (April 2023) 原文 PDF**，§5.2 Table 1 / Table 2 / Table 3 / Table 4。
> 下载地址（本次实际抓取）：`https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf` | 可信度 **A**（标准原文；但该 URL 为第三方镜像，**正式引用应改用 jedec.org**）

**Table 1 — 温度循环试验条件（Test Condition）**：

| Test Condition | Nominal Ts(min) (°C) | Nominal Ts(max) (°C) | 典型 cycle rate (cph) | 典型 Soak Mode |
|---|---|---|---|---|
| **A** | −55 | +85 | 2–3 | 1, 2 & 3 |
| **B** | −55 | +125 | 2–3 | 1 & 2 |
| **C** | −65 | +150 | 2 | 1 & 2 |
| **G** | −40 | +125 | <1–2 | 1, 2, 3 & 4 |
| **H** | −55 | +150 | 2 | 1 & 2 |
| **I** | −40 | +115 | 1–2 | 1, 2, 3 & 4 |
| **J** | 0 | +100 | 1–3 | 1, 2, 3 & 4 |
| **K** | 0 | +125 | 1–3 | 1, 2, 3 & 4 |
| **L** | −55 | +110 | 1–3 | 1, 2, 3 & 4 |
| **M** | −40 | +150 | 1–3 | 1, 2, 3 & 4 |
| **N** | −40 | +85 | 1–3 | 1, 2 & 3 |
| **R** | −25 | +125 | 1–2 | 1 & 2 |
| **T** | −40 | +100 | 1–2 | 3 & 4 |

> **原标准三点警示（CAUTION，逐字要点）**：
> 1) 某 Test Condition 的 **Ts(max) 可能超过某些封装材料的玻璃化转变温度 Tg**，从而诱发现场应用中不会出现的失效机理；
> 2) 必须避免 DUT 器件之间和器件内部的**大温度梯度**；
> 3) 试验温区内的 **CTE 失配可能导致试验板电镀通孔提前失效**，限制电测读出能力；
> 4) **Ts(max) 超过 125 °C 的 Test Condition 不推荐用于 Pb/Sn 焊料成分**，因可能导致动态再结晶。

**Table 2 — Soak Mode 定义（决定保温时长）**：

| Soak Mode | 上下端保温最小时间（min） |
|---|---|
| **1** | **1** |
| **2** | **5** |
| **3** | **10** |
| **4** | **15** |

- Soak temperature 判定窗口：高温端 Ts 在 nominal Ts(max) 的 **−5 °C ~ +10 °C**（或 +15 °C，视容差）；低温端 Ts 在 nominal Ts(min) 的 **+5 °C ~ −10 °C**
- 器件级通常用 **Soak Mode 1**；**焊点疲劳/蠕变用 Soak Mode 2/3/4**；锡须用 **5–10 min**（A121）

**Table 4 — 焊互连推荐条件**：

| Test Condition | Soak Mode | Ramp Rate (°C/min) | Cycle Rate (cph) |
|---|---|---|---|
| G, I, J, K, L, T | 2 | Thermal Mass Dependent | 2 |
| G, I, J, K, L, T | 3 | Thermal Mass Dependent | <2 |
| G, I, J, K, L, T | 4 | Thermal Mass Dependent | <1 |
| R | 1 | Thermal Mass Dependent | 2 |

**升温/降温速率（ramp rate）**：
- 器件级：通常不关键，但**必须明确控制**，否则无意中接近热冲击
- **焊互连级：≤ 15 °C/min（优选 10–14 °C/min）**，任何部分均适用
- 测量方式：**profile 线性段**，一般取温度区间的 **10%–90%** 点之间
- 大热质量样品可能需要**单区（single zone）** 箱体才能达到最佳 ramp rate
- **热冲击箱（air-to-air 或 liquid-to-liquid）不得替代温循箱**

**循环速率（cycle rate）经验值**：
- 器件级：1–3 cph（>3 cph 仅用于球焊键合完整性等特定机理）
- **焊互连级：1–2 cph**（倒装、BGA、堆叠等）；**cycle time < 30 min 不推荐**
- 锡须：约 3 cph（A121）

**中断规则（易被忽略，工程上极重要）**：
> 总循环数可因中途电测、上下料、设备故障而中断；但**若所有中断次数之和超过规定总循环数的 10%，试验必须从头重启**。

**双箱载荷转移时间（load transfer time）**：**< 1 分钟**。

**循环次数**：**1000 次**（JESD47 鉴证常用；JESD47 引用的温循曲线为常用 profile）。A104F.01 本身不规定固定次数——次数由 JESD47（鉴证）或供方/用户约定确定。
⚠️ 中期复测点常在 **200 / 500 / 700 / 1000** 次 | 可信度 **C**（来自检测站，非 A104/JESD47 原文）
⚠️ AEC-Q100 组别另有 TC 500–1000 次的说法 | **B**

---

## D. 高频术语表（中英对照）

> **可信度说明**：术语本身为行业通用名词，标注的是**定义口径**是否有一手依据。凡涉及具体参数/公式的，给出来源。
> 图标：★ = 功率封装高频；⚠ = 常见误用/需注意。

### D1. 封装与互连

| English | 中文 | 要点/区分 | 可信度 |
|---|---|---|---|
| **DBC**（Direct Bonding Copper） | 直接覆铜陶瓷基板 | AlN/Si₃N₄ 陶瓷上直接键合铜层；功率模块主流基板 | **B** |
| **AMB**（Active Metal Braze） | 活性金属钎焊基板 | 铜箔与陶瓷用活性钎焊料（Ag-Cu-Ti）结合；可做多层 | **B** |
| **die attach** | 芯片贴装/芯片附着 | 焊料焊(DBC)、铜烧结、银烧结、锡膏、导电胶 | **B** |
| **solder alloy** | 焊料合金 | **SnAg**（SA，如 SAC305=Sn3Ag0.5Cu0.5）｜**SAC**（Sn-Ag-Cu 无铅主流）｜**AuSn**（共晶 80Au/20Sn，高温高可靠）｜**PbSn**（含铅 63/37 共晶，**A104 警告 >125 °C 会动态再结晶**）| **B**（PbSn 警示 **A**，出自 A104F.01 原文 CAUTION） |
| **wire bond** | 引线键合 | **Al**（传统，Ultrasonic 超声焊）｜**Au**（低热阻、易加工）｜**Cu**（导热最佳但需 AQG/Q100 的 Cu wire 专项验证）| **B**（Cu 需专项验证见 AEC-Q100 Rev-I §3.4） |
| **double bond** | 双键合 | 同一引线键两处 die pad，降低电流密度 | **C** |
| **clip bond** | 夹片键合 | 用金属夹(clip)替代键线，IGBT 模块常用 | **C** |
| **sintered die attach** | 烧结芯片贴装 | 银烧结 / 铜烧结，无有机物，高可靠性 | **B** |
| **QFN**（Quad Flat No-Lead） | 四边扁平无引脚封装 | 底部散热焊盘，功率器件常用 | **B** |
| **LGA**（Land Grid Array） | 焊盘栅格阵列 | 无引脚，靠压接 | **B** |
| **BGA**（Ball Grid Array） | 焊球栅格阵列 | — | **B** |
| **CSP**（Chip Scale Package） | 芯片级封装 | — | **B** |
| **TSV**（Through-Silicon Via） | 硅通孔 | 3D 堆叠互连；填充 Cu；热应力开裂风险 | **B** |

### D2. 可靠性物理失效机理

| English | 中文 | 要点 | 可信度 |
|---|---|---|---|
| **delamination** | 分层 | 界面脱粘；TC/HAST/MSL 场景核心 | **B** |
| **popcorn**（popcorning） | 爆米花（现象） | 塑封体吸湿后回流瞬间水汽膨胀开裂；**术语来源即"爆开时的爆裂声"** | **B** |
| **Moisture Sensitivity Level (MSL)** | 湿度敏感等级 | J-STD-020 定义；**Floor Life = 干燥包装开封后可暴露在空气中的累计时间** | **B**（等级表见 §A4.1） |
| **via failure** | 通孔失效 | 含 PTH 失效、TSV 开裂 | **C** |
| **TSV crack** | TSV 裂纹 | 热循环下 Cu 与 Si CTE 失配 | **B** |
| **whisker**（tin whisker） | 须晶/锡须 | 纯锡镀层自发生长；JESD201、A121 | **B** |
| **corrosion** | 腐蚀 | 湿热 + 离子污染；ECM 前奏 | **B** |
| **electrochemical migration (ECM)** | 电化学迁移 | 阳极溶解→离子迁移→阴极沉积；需水膜+电位差+离子 | **B** |
| **dendrite** | 枝晶 | ECM 生成的树枝状金属，须桥连才短路；**可能间歇**（细丝熔断再生长）| **B** |
| **CAF**（Conductive Anodic Filament） | 导电阳极丝 | 玻纤-环氧界面铜迁移；**IPC-TM-650 2.6.25**（编号待核实）| **B** |
| **SPI / 机构应力**（stress induced by... ）| ⚠️ "SPI" 在封装语境下**含义歧义** | 本领域 "SPI" 最可能指 **Scanning/Stress…**；亦可能指串行外设接口。**需向原作者确认** | **C — 未核实，建议弃用该缩写** |
| **CBS**（Connecting Bond Stress） | 连接键合应力 | 键合界面应力；非通用标准术语 | **C — 未核实** |
| **MLF**（Mass Lead Frame） | 实体引线框架 | 也可能指 Molded Lead Frame（模塑引线框架）。**两种用法都存在，必须看上下文** | **C — 歧义** |
| **die edge crack** | 芯片边缘开裂 | 切割/崩边；应力集中 | **C** |
| **die-attach fatigue** | 芯片贴装层疲劳 | 焊料层低周疲劳；**PCmin 主要考核对象** | **B** |
| **bond lift-off** | 键合脱离 | 键线根部界面分离；**PCsec 主要考核对象** | **B** |
| **delamination（mold compound interface）** | 模塑料界面分层 | MSL + 回流引发 | **B** |

### D3. 功率模块专有

| English | 中文 | 要点 | 可信度 |
|---|---|---|---|
| **power cycling (PC)** | 功率循环 | 通电发热循环；**PCsec（秒级，考键合）/ PCmin（分钟级，考焊层）** | **B**（AQG 324 框架 **A**） |
| **thermal cycling (TC)** | 温度循环 | 被动温变，**不施加功率** | **A**（A104） |
| **power temperature cycling (PTC)** | 上电温循 | A105 | **B** |
| **thermal shock (TS)** | 热冲击 | 快速转换；**A104 明确不涵盖** | **A**（A104 §1） |
| **HTRB**（High Temperature Reverse Bias） | 高温反偏 | 阻断态加高压，考核体二极管/表面漏电 | **B**（AQG 324 QL 项） |
| **H3TRB** | 高温高湿反偏 | HTRB + 湿热；动态 H3TRB 见 AQG 324 2025 SiC 扩展 | **B** |
| **HTGB**（High Temperature Gate Bias） | 高温栅偏 | 考核栅氧化层可靠性 | **B** |
| **dynamic avalanche** | 动态雪崩 | 感性负载关断时的雪崩耐受 | **B**（AQG 324 DRB） |
| **short-circuit withstand / SCSW** | 短路耐受 | 短路脉冲耐受时间 | **B**（AEC-Q100-012 / Q101-006 / AQG 324 QC） |
| **dV/dt** | 电压变化率 | 感性关断 EMI 与误触发风险 | **B** |
| **gate oxide reliability** | 栅氧化层可靠性 | — | **B** |
| **TDDB**（Time Dependent Dielectric Breakdown） | 时间相关介质击穿 | **Weibull β 是核心指标**（见 D4）| **B** |
| **body diode** | 体二极管 | IGBT/MOSFET 内部寄生二极管 | **B** |
| **SiC MOSFET** | 碳化硅 MOSFET | 高 dv/dt、高结温；动态栅应力敏感 | **B** |
| **IGBT** | 绝缘栅双极晶体管 | 尾随电流（TIG tail）；关断 dv/dt | **B** |
| **Rth(j-c) / Zth** | 结-壳热阻 / 瞬态热阻抗 | Zth 为瞬态热阻抗曲线 | **B** |
| **ΔTj** | 结温变化幅度 | 功率循环的核心严酷度参数 | **B** |

### D4. 试验与统计

| English | 中文 | 要点/公式 | 可信度 |
|---|---|---|---|
| **Arrhenius equation** | 阿伦尼斯方程 | AF = exp[ Ea/k · (1/T_use − 1/T_stress) ]；温度加速主导 | **B** |
| **activation energy (Ea)** | 活化能 | 单位 eV 或 kJ/mol；查 **JEP122** 各机理 Ea 表 | **B** |
| **acceleration factor (AF)** | 加速因子 | 应力条件加速倍数 | **B** |
| **Cochran-Manson** | — | 焊点热机械疲劳寿命模型（Nf = Nf0 (ΔT/Td)^n）| **C — 未核实具体指数 n，需查 IPC-SM-785** |
| **Morrow** | — | 焊点疲劳寿命模型（Darveaux 模型系列）| **C — 未核实** |
| **power-law (temp-humidity)** | 幂律模型 | 湿热加速 **THB/SIR/CAF** 用**幂律**，非 Arrhenius | **B** |
| **S/N**（stress / natural） | 应力比 | 加速试验设计核心量 | **B** |
| **MTTF** | 平均无故障时间 | 指数分布下 = 1/λ | **B** |
| **B10** | 10% 失效率对应寿命 | 可靠度指标 | **B** |
| **Weibull β** | 威布尔形状参数 | **β>1 磨损耗尽（wear-out）；β<1 早期失效（infant mortality）；β=1 随机失效** | **B** |
| **DV@T**（Density / Volume… ）| ⚠️ **含义不确定** | 可能是 "Dwell time at Temperature"。**需确认** | **C — 未核实** |
| **FIT**（Failures In Time） | — | **1 FIT = 1 次失效 / 10⁹ 器件小时**；JESD85 给出换算方法 | **B** |
| **sample size & confidence** | 样本量与置信度 | 零失效时 n = ln(1−C)/ln(1−R) | **B** |
| **HBM / CDM / MM** | 人体模型 / 带电器件模型 / 机器模型 | 体系见 §A1.4；**MM 已退出** | **A** |
| **HTOL** | 高温工作寿命 | = JESD22-A108(TBL)；⚠️ 常见误写"Voltage Life" | **A** |
| **ELFR** | 早期失效率 | JESD74；指数/Weibull 假设 | **B** |

### D5. 材料与工艺

| English | 中文 | 要点 | 可信度 |
|---|---|---|---|
| **CTE**（Coefficient of Thermal Expansion） | 热膨胀系数 | 分 z 轴（Tg 以下/以上）；**Tg 上下 CTE 失配是分层主因** | **B** |
| **Tg**（Glass Transition Temperature） | 玻璃化转变温度 | **TC 上限超过 Tg 会诱发非现场失效机理**（A104 CAUTION 明文）| **A**（A104 原文）+ **B**（定义） |
| **Tf**（Flow Temperature） | 流动温度 | — | **C — 未核实** |
| **Td**（Decomposition Temperature） | 分解温度 | 印制板 T260/T288 即此概念 | **C — 未核实具体定义** |
| **CTI**（Comparative Tracking Index） | 相比漏电起痕指数 | 高压应用 | **C** |
| **CTH** | — | ⚠️ **含义不确定** | **C — 未核实** |
| **MoM**（Moment over Method）| 矩量法 vs 方法比 | 剥离强度评价方法 | **C** |
| **UL 94** | 阻燃等级 | **V-0** = 垂直燃烧 5 s 内自熄、无滴落；IPC-6012 等引用 | **B** |
| **Rogers** | 罗杰斯高频基材 | PTFE/陶瓷填充，常用于微波板 | **B** |
| **Polyimide (PI)** | 聚酰亚胺 | 高温高介电强度 | **B** |
| **mold compound (EMC)** | 环氧模塑料 | 注意 **EMC 也指电磁兼容性**，语境区分 | **B** |
| **silicone gel** | 硅凝胶 | 灌封/缓冲，去耦应力 | **B** |
| **underfill** | 底部填充胶 | 填充 BGA/CSP 焊点下方；**IPC-7095** | **B** |
| **MSL floor life** | 地面暴露寿命 | 见 §A4.1 | **B** |

### D6. 质量体系

| English | 中文 | 要点 | 可信度 |
|---|---|---|---|
| **IATF 16949** | 汽车质量管理体系 | 取代 TS 16949；含 VDA 6.3、PPAP 等要求 | **C — 未在本次检索中一手核实** |
| **AEC**（Automotive Electronics Council） | 汽车电子委员会 | Q100/Q101/Q102/Q103/Q104/Q200，见 §A4.3 | **A** |
| **PPAP**（Production Part Approval Process） | 生产件批准程序 | — | **C — 未一手核实** |
| **8D** | 八步问题解决法 | D4=根因、D5=永久纠正措施 | **C** |
| **5 Why** | 五问法 | — | **C** |
| **Fishbone / Ishikawa** | 鱼骨图/石川图 | — | **C** |
| **PFMEA** | 过程 FMEA | JEP131 提供 FMEA 方法 | **B** |
| **AIAG-VDA FMEA** | AIAG-VDA FMEA | 取代 AIAG-VDA 第一版；**Action Priority(AP)** 取代 RPN | **C — 未一手核实** |
| **MSA / GR&R** | 量具系统分析 / 重复性与再现性 | — | **C** |
| **SPC / Cpk** | 统计过程控制 / 过程能力 | JEDEC **JESD19** 为 SPC 标准；AEC-Q003 为 Cpk 表征文件 | **B** |
| **OQC** | 出货质量检验 | — | **C** |
| **Acceptable / Target / Defect Condition** | 可接受/目标/缺陷状态 | IPC-A-610 三分类 | **B** |

---

## E. 给查表 CLI 的实现建议

### E1. 解析器优先级（按成功率从高到低）

| 优先级 | 模式 | 处理方式 |
|---|---|---|
| 1 | `JESD22-[ABC]\d+[A-Z]?(\.\d+)?` | 查 C1/C2/C3 表。**A/B/C 组别先分流，再查方法号** |
| 2 | `MIL-STD-883[A-Z]?,? Method (\d{4})` | 查 §A4.4，按首位数字分流 1xxx/2xxx/3xxx/5xxx |
| 3 | `IEC 60749-\d+` | 查 §A3.2 |
| 4 | `SEMI ([A-Z]+)\s?(\d+)(-\d+)?` | 按前缀分流：MF→M 系列试验方法；M→材料规范；S→安全；E→设备 |
| 5 | `JS-\d{3}(-YYYY)?` / `J-STD-\d{3}` / `JEP\d+` | 查 §A1.4 / §A4.1 / §C4 |
| 6 | `AEC-Q\d{3}(-\d+)?` | 查 §A4.3 |
| 7 | `JESD\d+(-?\d+)?([A-Z]?)(\.\d+)?` | 顶级编号，查 §A1.3 |

### E2. 必须内建的防错规则

1. **版本号必须保留**：JESD22-A104 ≠ JESD22-A104F.01。查表输出应回显完整编号。
2. **`F.01` 后缀是增补不是年份**：`JESD78F.02` 中 F=版本、02=增补号；而 `JS-001-2017` 中 2017 才是年份。
3. **拦截已知失效编号**：命中 A114/C101/B102/B104/A115/A112/C100/JESD29/JESD34 时，**先提示已废止/被替代，并给出替代编号**，不要直接返回标题。
4. **MIL-STD-883 必须是 4 位**：若输入 3 位（101/105 等），判定为编号错误并提示。
5. **JESD204 ≠ DDR4**：DDR4 是 JESD79-4。可作为硬编码断言。
6. **A121 ≠ ESD**：锡须测试，勿与 A114/A115/C101 混淆。
7. **JESD78 = Latch-Up**：若用户以"ESD 体系"名义查询 JESD78，应主动纠正。

### E3. 未核实项清单（输出时必须带警示或暂不返回）

以下条目**必须**先经人工核实，禁止作为断言输出：

`JESD48`｜`JESD671`｜`JESD82-x` 各具体标题｜`JESD22-A200` 系列全部｜`JESD22-B119`｜`JESD22-B121A`｜`SEMI N1`｜`SEMI C1`｜`SEMI T10`｜`SEMI E10`｜`SEMI MS/ME/MI` 分级｜`IPC-1782`｜`IPC-TM-650` 各具体方法号（2.3.25/2.4.22/2.6.3.7/2.6.25 存在来源冲突）｜`MIL-STD-883 Method 5011`｜`MIL-STD-750A 2030`｜`GJB` 任何具体编号｜术语 `SPI`、`CBS`、`MLF`、`DV@T`、`Tf`、`CTH`、`MoM` 的确切定义｜AQG 324 具体数值条件（ΔTj、循环次数、时长）｜`JESD22-A108` F 版与 G 版标题差异｜`IATF 16949`/`PPAP`/`8D`/`AIAG-VDA FMEA` 的一手依据

### E4. 权威查询入口（供 CLI 兜底）

| 组织 | URL |
|---|---|
| JEDEC 文档检索 | `https://www.jedec.org/document_search` |
| JEDEC JC-14 委员会页（含最新文档列表） | `https://www.jedec.org/node/19` |
| IEC TC 47 文档列表 | `https://www.iec.ch/dyn/www/f?p=103:20:3655892773077` |
| IEC Webstore | `https://webstore.iec.ch` |
| SEMI 标准商店 | `https://store-us.semi.org` |
| AEC 官方文档列表 | `http://aecouncil.com/Documents/AECDocuments.html` |
| AEC-Q100 原文（Rev-I） | `http://aecouncil.com/Documents/AEC_Q100_Rev_I.pdf` |
| ECPE（AQG 324） | `https://www.ecpe.org` |
| MIL-STD-883F 原文（NASA 托管） | `https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf` |
| NASA EEE Parts Bulletin（ESD 体系权威综述） | `https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/` |

---

## F. 主要来源清单

| # | URL | 用于 | 可信度 |
|---|---|---|---|
| 1 | `https://nepp.nasa.gov/docuploads/31ECBD46-FFA0-43AE-82C09A3B2B6FE26B/std883.pdf` | MIL-STD-883F 方法号全表 | **A** 政府托管原文 |
| 2 | `https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/EEE-Parts-Bltn-2021-Vol-13-No1-ESD-Testing-Standards-GaN-Devices-CL22-0048.pdf` | ESD 体系演进（JS-001/JS-002 替代关系与兼容条款）| **A** |
| 3 | `https://www.jedec.org/node/19` | JC-14 范围与最新文档、现行 JESD47 版本 | **A** 官网 |
| 4 | `https://www.jedec.org/standards-documents/docs/jesd-78b` | JESD78 = IC Latch-Up Test | **A** 官网 |
| 5 | `https://www.jedec.org/node/8434` | JESD79-4D = DDR4 SDRAM | **A** 官网 |
| 6 | `https://www.jedec.org/news/pressreleases/jedec-announces-publication-ddr4-standard` | 确认 DDR4 = JESD79-4 | **A** 官网 |
| 7 | `https://www.jedec.org/node/5896` | JS-001-2010 发布公告（替代 A114F + STM5.1）| **A** 官网 |
| 8 | `https://www.jedec.org/committees/JC-44` | JESD12 系列标题 | **A** 官网 |
| 9 | `https://www.jedec.org/document_search/field_doc_type/148/...` | JESD8-x 系列性质 | **A** 官网 |
| 10 | `https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf` | **A104 Table 1/2/3/4、soak、ramp、中断规则** | **A** 标准原文（第三方镜像） |
| 11 | `https://www.iec.ch/dyn/www/f?p=103:20:3655892773077...` | IEC 60749 Part 标题 + 版本年份 | **A** IEC 官网 |
| 12 | `https://www.enstandards.com/wp-content/uploads/pdfs/preview/1278100` | IEC 60749-35 原文前言（Part 1–39 全表）| **A** IEC 文件 |
| 13 | `https://webstore.ansi.org/industry/semiconductors/tests/iec-60749` | IEC 60749 系列规模与各 Part Scope | **B** |
| 14 | `https://store-us.semi.org/products/m00100-semi-m1-...` | SEMI M1 全文范围与内部交叉引用清单 | **A** SEMI 官网 |
| 15 | `https://downloads.semi.org/web/wstdsbal.nsf/.../5893.pdf` | SEMI MF 系列标题 + JEITA/JIS 对应 | **A** SEMI 官方 |
| 16 | `https://www.semi.org/sites/semi.org/files/2020-08/AUX023-00-0915.pdf` | SEMI M/E/G 系列标题（450mm）| **A** SEMI 官网 |
| 17 | `https://china.semi.org.cn/article/136`、`/article/240` | SEMI 系列分类 | **B** SEMI 中国 |
| 18 | `http://aecouncil.com/Documents/AECDocuments.html` | **AEC 全部编号↔标题↔版本** | **A** 官网 |
| 19 | `http://aecouncil.com/Documents/AEC_Q100_Rev_I.pdf` | Q100 附件全名、Grade 4 删除、Cu wire | **A** 官网原文 |
| 20 | `http://www.aecouncil.com/Documents/AEC_Q100_Rev_H_Base_Document.pdf` | Grade 4 删除出处、MM/GL 退役说明 | **A** 官网原文 |
| 21 | `https://www.ecpe.org/index.php?eID=dumpFile&t=f&f=48794&...` | AQG 324 发布方、前身 LV324、Release 04.1/2025 | **A** ECPE 官网 |
| 22 | `https://community.infineon.com/.../ta-p/436857` | LV324→AQG324、AEC-Q101、UL 1557 | **A** 厂商一手 |
| 23 | `https://mbb.eet-china.com/blog/4061550-455299.html` | JESD22 A/B/C 全表与分组说明 | **B** |
| 24 | `https://www.qwctest.com/m/news_detail.aspx?id=703` | JEDEC 标准分类一览（含旧版本）| **B** |
| 25 | `https://web.calce.umd.edu/TSFA/methods2.htm` | JESD22 ↔ MIL-STD-883 方法名对照 | **B** |
| 26 | `https://standards.globalspec.com/std/14646186/jesd78f-02` | JESD78 完整版本史（1997–2023）| **B** |
| 27 | `https://standards.globalspec.com/std/10163298/jedec-jesd-79-4` | JESD79 版本史（LPDDR→DDR4 演进）| **B** |
| 28 | `https://www.ti.com/content/dam/videos/external-videos/.../clocks-and-timing-clocking-jesd204bc-systems-presentation-quiz.pdf` | JESD204 = SerDes 及各版速率 | **B**（TI 官方培训）|
| 29 | `https://www.eurofins.cn/en/materials-and-engineering/service/esd-and-latch-up-testing/` | ESD 三标准现行/失效状态、TLP、闩锁 | **B** |
| 30 | `http://www.xktest.cn/news/show/38143.html` | A108G 标题 = TBL | **B** |
| 31 | `http://tw-redi.com/forum.php?mod=viewthread&tid=977` | JEDEC 文件类型、JEP 清单、失效机理 | **B** |
| 32 | `http://tw-redi.com/forum.php?mod=viewthread&ordertype=2&tid=1166` | JEDEC 可靠性标准清单 | **B** |
| 33 | `https://www.electronicsguide.net/professional-practice/reliability-engineering/standards-and-best-practices/international-reliability-standards` | JESD47/85/91/94、Telcordia、CAF/2.6.25 | **B** |
| 34 | `http://audace-reliability.crihan.fr/Ateliers_files/1-JEDEC%20standards%20for%20product%20level%20qualification.pdf` | JESD47H.01、A113 预处理流程图 | **B**（大学课件）|
| 35 | `https://electroniccomponent.com/ipc-standards-system-core-standards-electronics-manufacturing` | IPC 体系与 TM-650 分组 | **C**（小类归属与其他来源冲突）|
| 36 | `https://www.benewavetech.com/blog-insights/ipc-standards-in-pcb-assembly-manufacturing.html` | IPC-A-610 H 版 2020、Class 体系 | **B** |
| 37 | `https://www.jjrlab.com/news/aec-q100-ic-integrated-circuit-compliance-testing.html` | AEC-Q100 各组测试与 JEDEC 对应 | **B** |
| 38 | `https://img.antpedia.com/standard/files/pdfs_ora/20240730/SEMI%20MF%201530-0707-2007.pdf` | SEMI MF1530 原文（含 ASTM F1530 沿革、参考 M1/M20/M59）| **A** |
| 39 | `https://snti.ru/snips_jedec-all.htm` | JESD 编号存在性（含 8-1~8-35、82-x）| **C** |
| 40 | `https://apexstandards.com/APEX%20STANDARDS%20N4000222...pdf` | JESD204/220/229/230/235/71 主题 | **C**（智库报告）|

---

*编制：Track 06 调研 ｜ 核实基准日：2026-10 ｜ 建议每 6 个月复核 JEDEC 现行版本列表与 IEC TC 47 页面*