# Track 03 — Workflows（工作流 / SOP：标准在工程流程中哪一步介入）

> **调研对象**：半导体标准体系的**使用侧** —— 可靠性工程师实际怎么用标准干活
> **目标读者**：功率半导体封装可靠性工程师（20 年经验 / 六西格玛黑带 / IGBT 模块封装全流程）
> **调研日期**：2026-10-05
> **本track 的独特价值**：Track 04 回答"标准是什么"，本track 回答**"标准在哪一步介入、谁决定、怎么翻译成试验条件、判据从哪来"**
> **信源分级**：每条信息标注 `[一手]` / `[二手]` / `[推断]`，并给 URL 与可信度（★★★★★ 最高）
> **形式要求**：全部写成**编号步骤 + IF-THEN 判断分支**，因为本skill 最终要变成 CLI

---

## 0. 执行摘要：本次调研的 8 个关键发现

| # | 发现 | 对工作流的价值 | 证据等级 |
|---|---|---|---|
| 1 | **JESD22-A104F.01 自己不规定循环次数** —— 原文把次数交给 JESD47 或供采双方约定 | 彻底改变"照抄标准条件"的做法：TC 的次数从来不是标准给的，是**你算出来的** | `[一手]` A104F.01 §5 + §7(b) ★★★★★ |
| 2 | **JESD47 已升版到 N 版（2026-08）**，取代 M:2025；且明确"本标准不适用于汽车 under-the-hood" | 车载功率模块**不能只靠 JESD47**，必须走 AQG 324。这是一条硬性分流规则 | `[一手]` 商店条目 + JESD47 Scope ★★★★☆ |
| 3 | **JESD94（JESD47 引用）才是"从标准条款到试验方案"的官方方法论**，JESD94B 流程 = 使用条件 → FMEA 选失效机理（JEP131）→ 寿命模型（JEP122/JESD91）→ AF 计算 → JEP143 定策略 → 选 JESD22 方法 → 执行报告 | 用户最需要的"翻译流程"有官方骨架，不需要自创 | `[一手]` PSMA/JC-70 演讲中的 JESD94B 流程图 ★★★★☆ |
| 4 | **PCsec / PCmin 的判据是 5% / 20%，但业内对热阻测量的重复性有明确质疑** | 判据不是"标准给的真理"，是"工程共识 +已知缺陷"；报告时必须写清测量不确定度 | `[二手]` 多个实验室技术文章 ★★★☆☆ |
| 5 | **AQG 324 04.1/2025 新增 Annex SiC（规范性）+ QL-08~QL-11 四项SiC 专属寿命试验**；且 **HTGB 改为一半样品正压、一半负压**（旧版允许先正后负） | SiC 模块的验证矩阵与 Si 基完全不同；HTGB 判据的"负压"分支是易漏项 | `[二手]` 安森美技术文章（技术媒体，但与04.1 目录吻合）★★★☆☆ + canon `[一手]` 目录 |
| 6 | **HV-H3TRB 不是独立标准编号**，是 AEC-Q101 语境下 H3TRB 的高压变体（Vds 提到额定值的 80%，如 1200V 器件用 960V） | 用户实际做的 HV-H3TRB 在标准体系中定位为"AEC-Q101 的加严项"，不是 AQG 324 基线要求 | `[二手]` Power Electronics News / Wolfspeed ★★★☆☆ |
| 7 | **抽样体系正在换代**：ISO 2859-1:2026 已发布（2026-01），而中国 GB/T 2828.1-2012 仍现行为 2025-05 复审确认版，**两者不等同** | 合同引用必须写清版本号，否则 Ac/Re 不可比 —— 这是审计高频问题 | `[二手]` ISO 2859 百科条目 + chinavalidate ★★★☆☆ |
| 8 | **"标准未覆盖"是常态而非例外**：JESD47 原文明确列出 4 类必须偏离标准条件的情形| 内部规范的产生不是"标准体系的漏洞"，而是**标准自己授权的** | `[一手]` JESD47 Scope 原文 ★★★★★ |

**另检出 4 处任务书前提错误**（详见 §6）：JESD22-A108 的定位、A104版本号表述、"UNECE 叠加车规"、"A104F.01 条件表已核实"。

---

## 1. 新产品/新平台的可靠性验证流程（Qualification Flow）

### 1.0 先做分流：你的产品该走哪条流程？（最重要的第一个 IF）

> **这是整个工作流的入口分叉。选错流程 = 后面全白做。**

```
IF 产品是 IGBT/SiC 功率模块（多芯片 + 陶瓷基板 + 底板 + 塑封/硅凝胶）
   ├─ 应用在汽车 PCU（整车 ≤ 3.5 t）
   │    → 主流程 = AQG 324（模块级）
   │    → 并行叠加 = AEC-Q101（芯片/单管级，若芯片外购或自产）
   │    → 依据：AQG 324 明确"不覆盖芯片本身的资格、工艺过程资格"
   └─ 应用在工业/能源/轨交
        → 主流程 = IEC 60749-34（功率循环）+ IEC 60749-6/-5（存储/湿热）
        → 参考 = AQG 324 作为设计目标（工业界普遍对标车规）

IF 产品是单管（TO-247 / TO-220 / DFN 等分立器件）
   ├─ 汽车 → AEC-Q101（单管）+ 客户 TS
   └─ 工业/消费 → JESD47 + IEC 60749对应部分

IF 产品是 IC / MCM
   ├─ 汽车 → AEC-Q100（IC）/ AEC-Q104（MCM）
   └─ 其他 → JESD47（基线）+ JEP150（组装态，若已焊到 PWB）

IF 产品已焊到 PWB / 组件级
   → 追加 JEP150（组装态应力测试驱动资格）
   → 依据：JESD47 Scope 原文 "does not cover devices assembled onto a PWB"
```

**证据** `[一手]`：
- AQG 324 04.1/2025 第1章 Scope（见 Track 04 §1.4）
- JESD47N Scope 原文："may not be applicable at extreme use conditions such as military applications, **automotive under-the-hood applications**, or uncontrolled avionics environments" / "does not cover devices assembled onto a PWB, or the like, which may affect the device reliability under assembled state. This is addressed in **JEP150**"
- 来源：https://store.accuristech.com/standards/jedec-jesd47n?product_id=3130401 ｜https://www.kekaoxing.com/wp-content/uploads/user_files/4993/publish/file/file-2020-06-07-12-09-46.pdf （JESD47 全文镜像）｜可信度：★★★★★

> 🔑 **对用户的直接价值**：用户做的是 IGBT 模块封装，如果客户是车企，主流程必须挂 AQG 324；如果客户是工业变频器，挂 IEC 60749-34 但对标 AQG 324 做。**不能拿 JESD47 当车规模块的资格文件。**

### 1.1 资格流程的阶段划分：两套并行语言

行业上并存两套阶段命名，**必须知道它们如何映射**，否则和客户对话会错位：

| 制造业通用语言（消费/互联网硬件） | 半导体/汽车语言 | 用户实际含义（功率模块） |
|---|---|---|
| **EVT**（Engineering Validation Test） | ≈ Reliability Qualification 前的摸底 | **DOE + 工艺窗口摸底**，不追求资格结论 |
| **DVT**（Design Validation Test） | ≈ **Reliability Qualification** 主体 | 正式跑AEC-Q101 / AQG 324 全矩阵 |
| **PVT**（Production Validation Test） | ≈ **Production Qualification** | **MP 前的产线验证**：治具、量测能力、抽检方案 |
| **MP**（Mass Production） | — | 量产 + 持续的可靠性监控 |

**一条来自产业界的实证** `[二手]`：安森美（onsemi）公开的项目开发简表显示——项目开始后先做**多轮 DOE 与前期验证测试**，全部满足要求后才开始做 **B 样**，B 样通过完整 AQG 324 后得到 **C 样**，然后准备量产相关工作。
- 来源：https://www.eet-china.com/mp/a237849.html ｜可信度：★★★☆☆（技术媒体，但流程逻辑与 AQG 324 附录 I.A 试验流程图吻合）

> `[推断]` **"DVT = 完整 AQG 324"这个映射不是标准写的，是行业惯例。** AQG 324 附录 I.A 有"试验流程图"、附录 I.B 有"Delta qualification matrix"，但**没有规定 A样/B样/C样的门限**。这一点在与客户谈进度时要明确：门限是合同/项目定的，不是标准定的。

### 1.2 各阶段标准集合的差异（哪些必须等到量产前）

> **判断依据的标准原文**：A104F.01 §7 明确哪些参数**必须由采购文件（procurement document）指定** —— 这些就是"必须等到有客户/产品定义才能定"的东西。

```
IF 处于 EVT / 前期 DOE 阶段
   → 标准介入方式 = 只用"方法论"，不用"条件"
   → 用：JESD94（知识化测试方法论）+ JEP131（FMEA）+ JEP122（失效机理与模型）
   → 不用：具体应力条件（A104 表1、AQG 324 QL 表）
   → 交付物：失效机理假设表 + 风险排序（供 DOE 选因子）

IF 处于 DVT / Reliability Qualification 阶段
   → 标准介入方式 = 完整矩阵
   → 芯片级：AEC-Q101（A组环境应力 + B组寿命模拟 + C组封装完整性 + D/E组）
   → 模块级：AQG 324（QM 特性 → QC 特性 → QE 环境 → QL 寿命，四段顺序不可乱）
   → 通用基线：JESD47（若非车规/非 under-the-hood）
   → 交付物：Qualification Report + 失效分析（若有失效）

IF 处于 PVT / Production Qualification 阶段
   → 标准介入方式 = 从"可靠性"切换到"过程能力"
   → 介入标准：ISO 2859-1 / GB/T 2828.1（来料与出货抽样）
   │+ IATF 16949 条款 8.5.1（生产件测量系统）+ MSA
   │                + 8.5.6.1（变更控制）
   → 交付物：控制计划 + MSA 报告 + 抽样方案 + PPAP

IF 处于 MP / 量产阶段
   → 标准介入方式 = 持续监控 + 变更触发
   → JESD46（用户通知产品/工艺变更）+ JESD47 的qualification-by-change
   → 定期抽检做趋势监控（SPC），而非重复做资格试验
```

**A104F.01 §7 原文（采购文件必须指定的 6 项）** `[一手]`：
> a) 特殊安装方式（如适用）
> b) **温度极值（见表1）、保温时间（见表2）、样品升降温速率、循环次数**，或特定器件要求
> c) 中间测量间隔（如需要）
> d) 检查、气密测试（气密封装）、内部键合完整性测试、电测试的特殊验收判据
> e) **对于资格试验，样品尺寸和质量等级（sample size and quality level）**
> f) 表1 以外的温度极值。需指定循环次数、温度极值、保温时间、每小时循环数、温度极值容差（若不同于表1）、升温速率、中间测量

- 来源：A104F.01 §7，https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf ｜可信度：★★★★★

> 🔑 **关键洞察**：`7(b)` 和 `7(e)` 揭示了标准体系的**设计意图**——**JESD22 系列是"方法标准"，不是"资格标准"**。循环次数（b）和样品尺寸+质量等级（e）都被显式外置给采购文件。所以 §3 的"从标准条款到试验方案"翻译流程不是"绕过标准"，而是**标准要求的正常用法**。

### 1.3 JESD47 的方法论：资格试验矩阵怎么组织

**版本现状（务必注意）** `[一手/二手混合]`：

| 版本 | 发布日期 | 页数 | 状态 |
|---|---|---|---|
| JESD47M | 2025-08 | 38 | 已被取代 |
| **JESD47N** | **2026-08-01** | 42 | ✅ **现行最新版** |

- 来源：https://store.accuristech.com/standards/jedec-jesd47n?product_id=3130401 ｜https://shop.standards.ie/en-ie/standards/jedec-jesd47n-2026-1137371_saig_jedec_jedec_4039270 ｜可信度：★★★★☆（标准商店条目，摘要含完整 Scope 原文）

> ⚠️ **对用户的版本提示**：Track 04 记录 canon 的 JESD47 相关内容时未涉及版本，**本track 新发现 N 版已发布**。若客户的资格文件仍引用 M 版，需确认是客户未更新还是本项目特定冻结版本。

**JESD47 的 Scope 里最关键的 4 个"不适用"声明** `[一手]`（这是 §1.0 分流的依据，也是"何时该偏离标准"的授权依据）：

```
JESD47 明确声明本标准：
  (1) 针对 "free-standing devices not soldered to a printed wired board (PWB)"
      → 已焊 PWB 的产品需另加 JEP150
  (2) "may not be applicable at ... automotive under-the-hood applications"
      → 车用模块必须走 AQG 324
  (3) "Failure Rate projections usually require larger sample sizes than are
       called out in qualification testing. For guidance ... refer to JESD85"
      → 资格试验的样本量 ≠ 失效率外推的样本量（关键，见 §1.5）
  (4) "This set of tests should not be used indiscriminately. Each qualification
       project should be examined for: a) Any potential new and unique failure
       mechanisms. b) Any situations where these tests/conditions may induce
       invalid or overstress failures."
      → 这是"标准授权你偏离"的原文
```

**JESD47 引用的完整标准族（资格项目的"上游依赖"）** `[一手]`（引自 JESD47 §2 Reference documents 全文）：

| 类别 | 文件 | 作用（对工作流的意义） |
|---|---|---|
| 军用 | MIL-STD-883、MIL-PRF-38535 | 参照基线 |
| 工业 | UL94、ASTM D2863、IEC 695 | 阻燃 |
| 湿度 | **J-STD-020** | MSL 分级 → 决定 TC 前是否预处理 |
| 制造 | JP-001（Foundry Process Qualification Guidelines） | 晶圆厂过程资格 |
| ESD | **JS-001（HBM）**、JS-002（CDM） |已从 JESD22 迁出，见 §5.2 |
| 可焊性 | J-STD-002 | 已从 JESD22-B102 迁出 |
| 方法族 | **JESD22 Series** | 全部试验方法 |
| 变更 | **JESD46** | 用户通知产品/工艺变更 → §5.4 的核心 |
| 资格信息 | **JESD69**（Information Requirements for Qualification of Silicon Devices）、**JESD74**（Early Life Failure Rate Calculation） | 资格报告内容要求 |
| 锁存 | JESD78（IC Latch-Up） | |
| 失效率 | **JESD85**（Methods for Calculating Failure Rates in Units of FITs） | 失效率外推方法学 |
| 电参数 | JESD86（Electrical Parameters Assessment） | |
| 加速模型 | **JESD91**（Methods for Developing Acceleration Models for Electronic Component Failure Mechanisms） | ★ §3 的模型方法论 |
| 应用特定资格 | **JESD94**（Application Specific Qualification using Knowledge Based Test Methodology） | ★ §3 的翻译流程骨架 |
| 失效机理模型 | **JEP122**（Failure Mechanisms and Models for Semiconductor Devices） | Ea 等参数来源 |
| 资格方法论 | **JEP143**（Solid State Reliability Assessment Qualification Methodologies） | 定试验策略 |
| 组装态 | **JEP150**（Stress-Test-Driven Qualification of and Failure Mechanisms Associated with Assembled Solid State Surface-Mount Components） | 焊到 PWB 后 |
| 芯片-封装交互 | **JEP156**（Chip-Package interaction Understanding, Identification and Evaluation） | ★ 与用户 DBC/AMB 封装直接相关 |
| 锡须 | JESD201（Environmental Acceptance Requirements for Tin Whisker） | |

- 来源：JESD47 §2 全文，https://www.kekaoxing.com/wp-content/uploads/user_files/4993/publish/file/file-2020-06-07-12-09-46.pdf ｜可信度：★★★★★

> 🔑 **JEP156 是本track 对用户最有价值的新发现之一**：它专门处理 chip-package interaction（CPI），正是用户 DBC/AMB 陶瓷覆铜板 + 芯片贴装结构的核心问题。Track 04 完全没提到这个文件。**建议纳入知识 OS。**

### 1.4 AEC-Q101/Q100/Q200 的应力梯度与样本量模型

**版本现状** `[二手，canon 已标未核实]`：AEC-Q100 Rev H（IC 基准）、AEC-Q101 Rev E（分立，2021）、AEC-Q200 Rev D（无源）。**AEC 官网本次无法访问，Rev 号为二手转录，建议用户自行到 aecouncil.com 核对。**

**AEC-Q101 的分组结构（A~E 五组）** `[二手]`：

| 组 | 名称 | 代表项目 |
|---|---|---|
| **Group A** | 加速环境应力试验 | PC 预处理、HAST/BHAST、UHAST、AC（autoclave）、TC、PTC/TC alt |
| **Group B** | 加速寿命模拟 | HTRB、HTFB、HTGB、IOL（间歇工作寿命）|
| **Group C** | 封装完整性 | DPA、PD、WBP、WBS、DS、RSH、TR、SD、WG |
| **Group D** | 模具制造可靠性 | DI（介质完整性） |
| **Group E** | 电气验证 | EV、TEST、PV、ESD HBM/CDM |

- 来源：https://www.uk-su.com/news/show-3938.html ｜可信度：★★★☆☆（检测机构技术文章，条目与 AQG 324 分组逻辑一致）

**⚠️ 关于"应力梯度"的重要澄清** `[推断]`：用户任务书假设 AEC-Q100/Q101/Q200 规定了"应力梯度与样本量模型"。**核实后的结论是：AEC-Q 系列规定的是「试验项目 + 条件 + 样本量 + 判据」的矩阵，而不是"梯度模型"。**

```
IF 你想找"AEC 的应力梯度模型"
   → 找不到，因为不存在这个概念
   → AEC 的实际逻辑是：按「失效机理」选项目，每个项目给固定条件
   → 真正的"梯度"思想体现在两处：
      (1) AEC-Q101 的 HTRB 允许 "如果 Tj 提高 25°C，时间可从 1000h 缩到 500h"
          → 这是一个明确的 温度-时间 等效换算（Arrhenius 思想的体现）
      (2) 样本量模型是固定的：3 lots × 77 pcs，0 fails
   → 真正的"梯度"（step-stress）在其他标准里，见下文
```

**HTRB 的温度-时间换算（唯一的"梯度"条款）** `[二手]`：
> "在结温 TJ = 150 °C 条件下持续 1000 小时。**如果将 TJ 增加 25 °C，则可将试验时间缩短至 500 小时。**"
- 来源：https://www.uk-su.com/news/show-2387.html ｜可信度：★★★☆☆
- `[推断]` 这条换算隐含的活化能可反推：设 TJ1=150°C=423.15K，TJ2=175°C=448.15K，t1/t2=2
  - 由 `t1/t2 = exp[(Ea/k)·(1/T2 − 1/T1)]` → `ln2 = (Ea/k)·(1/448.15 − 1/423.15)`
  - `1/448.15 − 1/423.15 = 2.6307e-4− 2.3634e-4 = 2.673e-5 K⁻¹`
  - `Ea = ln2 × 8.617e-5 / 2.673e-5 = 0.6931 × 3.224 = **2.23 eV**`
  - ⚠️ **这个反推值（2.23 eV）远高于功率器件常用的 0.7 eV**，说明这条"25°C↔500h"是**经验规则而非 Arrhenius 严格推导**。**不要用它做外推，只用于判断"标准给的条件是经验性的"这一事实。** 标为 `[推断]`，需用户用自有数据验证。

**样本量模型（AEC-Q101 通用）** `[二手]`：
- **3 lots × 77 pcs = 231 pcs，0 fails**（AEC-Q101 的通行要求）
- 但 Wolfspeed 文档显示**因测试项目而异**（见下表），这是一个**重要的实践洞察**：不是所有项目都要 231 颗

| 项目 | 样品数/批 | 批数 | 供应商/实验室实际执行 |
|---|---|---|---|
| HTRB / HTGB / GSS / TC / H3TRB | 25 | 3 | 3 lots × 25 = 75 |
| 同上（另一档） | 77 | 3 | 3 lots × 77 = 231 |
| PV | 25 | 3 | 3 lots × 25 |
| PC（预处理） | 11 | 2 | 2 lots × 11 |
| MSL | 11 | 2 | — |
| DPA | 2 | 3 | 破坏性抽样 |

- 来源：https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Designed_to_Last_Even_in_the_Harshest_Environments.pdf ｜可信度：★★★★☆（厂商技术文档，表格结构完整，含具体条件）
- `[推断]` **这张表是"资格矩阵如何落地"的最佳实证**：同一份 AEC-Q101，不同实验室/厂商对同一项目用 25 还是 77 颗差异巨大。**这说明 AEC-Q101 的样本量是"要求下限 + 客户约定"双重决定**，报方案时应显式声明 chosen sample size 及其依据。

**Wolfspeed 文档中的 SiC 具体条件（可作参考，但需核对 AEC-Q101 Rev E 原文）** `[一手，厂商技术文档]`：

| 项目 | 条件 |
|---|---|
| HTRB | Vds = 80% Vds,rated；Vgs = 0 V；Ta = 175 °C；1000 h |
| HTGB | Vgs = +Vgs,max，Vds = 0，Ta = Tmax，1000 h；**以及** Vgs = −Vgs.min，Vds = 0，Ta = Tmax，1000 h |
| TC | Ta = −40 °C / +150 °C，1000 cycles |
| H3TRB | Vds = 100 V，Vgs = 0 V，85% RH，Ta = 85 °C，1000 h |
| **HV-H3TRB** | （文档中该项被截断，条件未完整给出 —— 标为 **未核实**）|
| GSS（栅开关应力） | Vgs 从 −Vgs,min 到 +Vgs,max，Ta = 25 °C，1E12 cycles |

> 🔑 **注意 HTGB 的双极性要求**：Vgs = +Vgs,max **和** Vgs = −Vgs.min 各做 1000 h。与 §3 提到的"AQG 324 新版要求一半样品正压一半负压"方向一致 —— **IGBT 模块的 HTGB 是双分支要求，不是单点。** 这一点在用户的实际项目里极易漏项。

### 1.5 抽样：AQL 在来料/出货 vs 寿命试验样本量（这两件事完全不同）

> **这是本 track 最重要的概念区分**：AQL 体系和寿命试验样本量体系是**两套互不通用的统计语言**。

```
【体系 A：计数抽样（AQL 体系）】—— 用于来料检验 / 出货检验
   标准链：MIL-STD-105D(1963) → ISO 2859:1974 → ISO 2859-1:1989
           → ISO 2859-1:1999 → **ISO 2859-1:2026（2026-01 发布）**
           中国：GB/T 2828-1987 → GB/T 2828.1-2003 → **GB/T 2828.1-2012（现行）**
           美国：ANSI/ASQ Z1.4（源自 MIL-STD-105E，1995 撤废）
           ⚠️ MIL-STD-105E 已于 1995 年 withdrawn → **不应再作为合同引用依据**

【体系 B：寿命试验样本量（可靠性演示体系）】—— 用于资格试验
   标准依据：JESD47（资格）+ JESD85（FIT 外推）+ JEP143（方法论）
   核心概念：LTPD / CL（置信度）/ 零失效演示
   与 AQL **完全无关**
```

**体系 A 的关键机制（GB/T 2828.1 / ISO 2859-1）** `[二手]`：

| 要素 | 内容 |
|---|---|
| AQL 定义 | **可接收的最差过程平均质量水平**（不是"允许的不合格品百分比"！）|
| AQL 档位 | 计数调整型抽样中AQL(%) 只能取 0.01, 0.015, …, 1000，共 26 档 |
| 检验水平 | 7 种：一般检验水平 Ⅰ/Ⅱ/Ⅲ + 特殊检验水平 S-1~S-4；**无特殊要求时用一般检验水平 Ⅱ** |
| 样本量字码 | 批量 N + 检验水平 → 查字码表（A/B/C…）→ 查主表得样本量 n、接收数 Ac、拒收数 Re |
| 三种严格度 | 正常 / 加严 / 放宽 |
| 转移规则 | 正常→加严：初次检验中连续 5 批或少于 5 批中有 2 批不被接收 → 转加严 |
| | 加严→正常：加严状态下初次检验接连 5 批被接收 → 恢复正常 |
| | 正常→放宽：转移得分 ≥ 30 分 + 生产稳定 + 负责部门同意 |
| 加严特点 | **样本量原则上不变动，但接收数减小**（强制）|
| 放宽特点 | 样本量约为正常的 40%（非强制）|

- 来源：https://baike.baidu.com/item/%E8%B0%83%E6%95%B4%E5%9E%8B%E6%8A%BD%E6%A0%B7%E6%A3%80%E9%AA%8C/19172886 ｜可信度：★★★☆☆（内容与 ISO 2859-1:1999 结构一致，但百科来源）

**⚠️ 版本陷阱（工作流级高危）** `[二手]`：
- ISO 2859-1:2026 于 **2026-01-22** 发布，取代 1999 版及其修正案，是第 3 版
- 中国 GB/T 2828.1-2012 在 **2025-05 复审后仍现行**，等同采用 **ISO 2859-1:1999**
- **两者不是同一版本，不能互换标注**
- 原文警告："If the purchase contract, inspection brief, factory procedure, or provider template cites GB/T 2828.1-2012, **do not relabel the result as ISO 2859-1:2026**"
- 来源：https://chinavalidate.com/en/blog/pre-shipment-inspection-china ｜https://baike.baidu.com/item/ISO2859 ｜可信度：★★★☆☆

**AQL vs RQL 的区别（用户任务书特别问到）** `[二手]`：

| 概念 | 全称 | 定义 | 统计地位 |
|---|---|---|---|
| **AQL** | Acceptable Quality Level（接收质量限） | 抽样方案**仍会接收**批的最差过程平均质量水平 | 约 95% 的时间被接收 |
| **RQL** | Rejectable Quality Level（拒收质量限），亦称 **LTPD**（Lot Tolerance Percent Defective） | 方案**只肯以约 10% 概率接收**的质量水平 | 10% 接收概率 |

- 关键：两者都是**质量水平（百分比）**，**不是**不合格品**数量**。拒收计数是 Re（来自表格）。
- 原文："AQL is the worst long-run process average that will still usually be accepted. RQL, also called LTPD, is the quality level considered clearly unacceptable, which the plan is built to accept only about 10% of the time."
- 来源：http://www.erp-information.com/acceptable-quality-level.html ｜可信度：★★★☆☆

> 🔑 **对用户的"取严原则"落地建议** `[推断]`：合同里写 AQL 时，**必须同时写明 4 个要素** —— 标准号+版本、检验水平、缺陷分类（critical/major/minor 各自的 AQL）、严格度。原文明确说了"'Inspected to AQL 2.5' is not a specification, because it settles none of those."
> 示例缺陷分类（原文表格，可直接用于功率模块来料检验）：Critical = 可带电部位、禁止锐边、额定电压错误、强制警告缺失；Major = 无电、插销错误、锁扣缺失、条码不可读；Minor = 主视图外的小划痕。

**体系 B：寿命试验样本量（零失效演示）**

**核心公式 1 — 零失效可靠性演示（success-run 定理）** `[二手，数学可自行验证]`：

```
R_L = (1 − CL)^(1/n)

等价地，所需样本量：
n = ⌈ log(1 − CL) / log(R) ⌉
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `R_L` | 置信度下界（one-sided lower confidence bound）of reliability | 无量纲 |
| `R` | 目标可靠性 | 无量纲 |
| `CL` | 置信水平 Confidence Level | 无量纲 |
| `n` | 零失效试验的样本量 | 件 |

**核心公式 2 — 指数分布（含试验/任务时间比δ）** `[二手]`：

```
n = ⌈ log(1 − CL) / (δ · log(R)) ⌉
其中 δ = T / T_m
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `T` | 实际试验时长 | h |
| `T_m` | 要求证明的任务时长（mission time / 保修期） | h |
| `δ` | 试验/任务时间比 test-to-mission ratio | 无量纲 |

**核心公式 3 — Weibull 分布（形状参数 β 已知）** `[二手]`：

```
n = ⌈ log(1 − CL) / [ (T/T_m)^β · log(R) ] ⌉
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `β` | Weibull 形状参数 shape parameter | 无量纲（β>1 耗损期，β<1 早期失效）|

- 来源：https://metricgate.com/docs/reliability-demonstration-test/ ｜可信度：★★★☆☆（在线计算器文档，公式可用 R/Python 独立验证）

**核心公式 4 — 卡方（Chi-Square）失效率与 LTPD（工程常用简化式）** `[二手]`：

```
χ² = 2(C + 1) · LTPD / N
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `C` | 允许失效数（acceptance number） | 件 |
| `N` | 样本量 | 件 |
| `LTPD` | 批允收不良率 | % |
| `χ²` | 卡方统计量（自由度相关） | 无量纲 |

- 来源：https://www.ultrontek.com/news_detail/semiconductor-longevity-jedec-htol-testing-modern-ic-solutions-analysis ｜可信度：★★☆☆☆（技术媒体，公式形式与 ReliaSoft 累计二项式一致）

**零失效样本量的实际含义（工程直觉）** `[推断，用公式自行验算]`：
- `n = 77`、`CL = 90%` → `R_L = (1−0.90)^(1/77) = 0.1^(1/77) = e^(ln0.1/77) = e^(−2.3026/77) = e^(−0.0299) = **0.9705**`
  → 即 77 件零失效只能证明"在 90% 置信下，可靠性 ≥ 97.05%"。**这是很弱的结论。**
- `n = 231`（3 lots × 77）、`CL = 90%` → `R_L = 0.1^(1/231) = e^(−0.009967) = **0.99008**`
  → 231 件零失效 → 90% 置信下 ≥ 99.01%。**这个结论才有工程意义。**

> 🔑 **这解释了"3 lots × 77 = 231，0 fails"这个数字的力学来源**：不是为了"231 这个数好看"，而是要把 R_L 推到 ~99%。而 §4-canon 的 T7 待办（"77 样本依据未核实"）在这里得到了**部分解释**：77 更可能来自 AQG/AEC 试验矩阵的工程惯例与 3 批 × 25/77 的分档，而非严格的 LTPD 推导。**建议用户在正式报告中同时给出 n、CL、R_L 三元组，而不是只写"77 pcs, 0 fails"。**

**⚠️ 资格试验样本量 ≠ 失效率外推样本量** `[一手]`（JESD47 Scope 原文）：
> "Failure Rate projections usually require **larger sample sizes** than are called out in qualification testing. For guidance on projecting failure rates, refer to **JESD85**."
-含义：过了资格试验（231 件 0 失效）**不能**直接声称"失效率 = X FIT"。要外推 FIT，必须按 JESD85 用更大样本。
- `[推断]` 常见的 FIT 外推式（**注意：以下为工程通式，非 JESD85 原文，需核验**）：
  ```
  FIT = [ χ²(1−CL, 2r+2) / (2 · N_sample · t_test · AF_total) ] · 10⁹
  ```
  | 符号 | 含义 | 单位 |
  |---|---|---|
  | `r` | 观察失效数 | 件 |
  | `N_sample` | 总样本数 | 件 |
  | `t_test` | 试验时长 | h |
  | `AF_total` | 总加速因子 | 无量纲 |
  | `χ²(1−CL, 2r+2)` | 卡方分位数（df = 2r+2） | 无量纲 |
  - 零失效时：CL=60% → χ²(0.40, 2) = **1.833**；CL=90% → χ²(0.10, 2) = **4.605**
  - 来源：https://www.chipfoundryservices.com/glossary.php?term=semiconductor-reliability-2 ｜可信度：★★☆☆☆（**该站为内容农场性质，公式形式可用，但 JEDEC 引用关系不可信**）

**Weibull 分布的使用前提（必须遵守）** `[二手，多源一致]`：
1. **至少需要 5~10 个失效**才能做有意义的 Weibull 参数拟合（Track 04 §3.9）
2. **必须按失效模式分别分析** —— 不同失效机理不可混入单一分布
3. 零失效时**无法**用最小二乘或最大似然估计参数，必须用二项式方法（见 ReliaSoft 方法）
- 来源：https://help.reliasoft.com/articles/content/hotwire/issue118/relbasics118.htm ｜https://www.antpedia.com/standard/1016730953-10.html ｜可信度：★★★☆☆

> 🔑 **对用户项目的直接结论**：用户的 HV-H3TRB 试验"1000H 23pcs / 1500H 6pcs / 168H 74pcs 均 PASS" —— **全部零失效**。这意味着：
> 1. **不能对这批数据做 Weibull 拟合**（无失效点）
> 2. 可以做的是：给出 `n`、`CL` 下的 `R_L` 下界
> 3. 更有价值的是：把 168H×74pcs 与 1000H/1500H 数据**合并**做累积暴露量统计（S = n × t = 74×168 + 23×1000 + 6×1500 = 12432 + 23000 + 9000 = **44432 pcs·h**），再反推等效失效率上界。这是从零失效数据中榨取信息的唯一正确方式。

---

## 2. 封装可靠性试验的标准作业流程（SOP）

### 2.0 试验类型选择决策树（本节核心 —— 回应"行业高频困惑"）

> **功率循环 vs 温度循环 vs HTRB 分别模拟什么？为什么都要做？**

```
【第一步：确定被考核的失效机理 —— 这是唯一的正确入口】

IF 失效机理涉及"电流流经路径的电学接触"
   （键合线脱落、焊点开路、接触电阻上升）
   → 应力必须来自"电流发热" → **功率循环 PC**
   → 理由：只有通电才能在互连中产生真实的热-机械循环

IF 失效机理涉及"CTE 失配引起的整体热机械应力"
   （DBC 陶瓷裂纹、铜箔剥离、塑封料开裂、基板分层）
   → 应力可来自"外部环境温度变化" → **温度循环 TC / 热冲击 TST**
   → 理由：这类失效与通电无关，外部温变即可激发

IF 失效机理涉及"电场导致的漏电/击穿/栅氧退化"
   （终端结构缺陷、钝化层裂纹、栅氧 TDDB、Al 腐蚀）
   → 必须加电偏压 → **HTRB（反偏）/ HTGB（栅偏）/ H3TRB（湿热+反偏）**
   → 理由：没有偏压就不会有电场加速

IF 失效机理涉及"水汽 + 电场 + 离子迁移"
   → **H3TRB / HV-H3TRB**（A101稳态湿热偏压 是其温和版）

IF 失效机理涉及"短路耐量/雪崩能力"
   → **Short-circuit（QC-03）** —— 这是**破坏性**试验，每次只毁 1 件
```

```
【第二步：为什么三个都要做？—— 因为它们的 ΔT 空间分布不同】

功率循环 PC（通电发热）
   → 温度梯度：芯片处 ΔTj 很大，壳/底板处 ΔTc/ΔTf 很小
   → 热流路径：热量从芯片向散热器单向流出
   → 覆盖：芯片附近的互连（键合线、芯片焊层）✅
   → 不覆盖：远离芯片的互连（基板-底板焊层）❌

温度循环 TC（外部环境变化）
   → 温度梯度：整体近似均匀（若热质量小、导热好）
   → 覆盖：整个封装的所有 CTE 失配界面 ✅（含基板-底板、陶瓷-铜）
   → 不覆盖：需要"内部电流发热"才能出现的失效 ❌
   → 关键差异：**主动加热整体 vs 被动加热芯片**

HTRB（高温 + 电场，无循环）
   → 温度：恒定高温
   → 应力：纯电场 + 热激活
   → 覆盖：漏电、击穿、栅氧、终端缺陷 ✅
   → 完全不覆盖：机械疲劳 ❌
```

**结论（务必记住这句话）**：
> **PC 与 TC 考核的失效模式高度重叠但不完全相同；PC 不能替代 TC，TC 也不能替代 PC。**
> 决定性差异是**热量从哪里来** —— PC 的热量从芯片内部产生（造成巨大内部温度梯度），TC 的热量从外部环境施加（梯度小得多）。**这个梯度差异决定了谁先坏。**

`[二手]` 一手支撑：Wolfspeed 技术文档明确描述了这一分工——PCsec "heat remains near the die, CTE stress isolated to material near die"；PCmin "heat spreads throughout entire thermal stack, more material effected by CTE mismatch stress: **faster degradation**"。
- 来源：https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Power_Cycling_and_Lifetime_Modeling_Approach.pdf ｜可信度：★★★★☆

**PCsec vs PCmin 分工的物理机制（AQG 324 原文视角）** `[一手，canon 已核实，此处复核]`：
- **PCsec（QL-01，ton < 5 s）**：短导通 → 快速温度变化 → 典型退化：wire bond lift-off、芯片金属化退化、芯片-基板焊点退化
  - 关键数据点：瞬态热阻在 **< 100 ms** 时很小；典型 Al 键合线因热容需要 **> 100 ms** 才能升温 →因此 **ton < 100 ms 的温度摆动通常可忽略并过滤**
- **PCmin（QL-02，ton > 15 s）**：长导通 → **焊点应力更大**，可能诱发**基板/底板间焊点开裂**
- 原文结论："**both types of power cycling tests are required to verify the package technology**"

**IEC 60068-2-14（通用温变）的 Na/Nb/Nc 定位** `[二手]`：当产品不是半导体器件而是机电/整机时，用 Na（快速转换，热冲击）/ Nb（指定速率，单箱）/ Nc（双液槽）。**半导体封装一般不走 60068-2-14，走JESD22-A104**（因为 A104 专门处理了封装材料 CTE 失配、ramp rate、soak mode）。中国等同采用 GB/T 2423.22。
- ⚠️ 二手源对 60068-2-14 的严酷度等级（Pb、Pmin）描述**互相矛盾且未给标准原文**，标为 **未核实，不写入知识 OS**。

### 2.1 试验前：样品准备与基线测量

**（本节的"标准介入点"：JESD22-A104F.01 §4 + §7，以及各标准的"测量"章节）**

```
STEP2.1.1 样品标识与可追溯性
   IF 产品有 SN 编码体系
      → 直接对应 IATF 16949 条款 8.5.2.1 Identification and traceability
      → 8.5.2.1 子条款明确要求：
         a) 标识与追溯须能识别不合格品/可疑品
         b) 隔离不合格品（red boxes / "prison"）
         c) 满足客户或法规的响应时间要求
         d) 按格式保存记录
         e) **"若客户或法规标准规定，须对单个产品做序列化标识"（serialized identification）**
         f) 追溯要求延伸至有安全/法规特性的**外购产品**
         g) 按产品、工艺、制造地点定义追溯系统
   → 这正是用户"SN 编码缺失导致的可追溯性改善"项目的标准依据
   → 来源：https://www.pqbweb.eu/page-iatf-16949-version-2016-requirements-automotive-quality-management-system.php ｜可信度：★★★★☆（逐条列出 IATF 16949:2016 条款号与内容）

STEP2.1.2 应力测量点布置（热学）
   IF 做功率循环
      → 结温必须用**温度敏感电参数（TSP）**间接测量，不能用热像仪直接测（封装不透红外）
      → IGBT：**K 系数法**（Vce(T) 标定）
      → 方法论母标准：**JESD51-14**（Vce(T) 方法）
      → AQG 324 要求：Tj 数据必须通过 Vce(T) 方法测量，试验中必须实时监测 Vce/Vf、ΔTvj、热阻
   IF 做温度循环（A104）
      → 热电偶或等效装置**贴附或嵌入样品本体**
      → 位置要求：**"the corners and middle of the load"**（载荷的角部与中部）
      → 贴附方式要求：胶带/胶水用量最小化，确保**整个样品质量达到温度极值并满足 soak 要求**
      → 原文：NOTE "The thermocouple... attachment method used should ensure that the
              entire mass of the sample(s) is reaching the temperature extremes and the
              soak requirements."
   → 来源：A104F.01 §3.3 + §2.3 NOTE（PDF 页 3-4）｜可信度：★★★★★

STEP2.1.3 基线电性测量（必须在应力前完成并记录）
   功率模块的最小基线集：
   - 静态：VCE(sat)/VF（Ic 条件下的导通压降）、漏电流 ICES、栅极漏电流 IGES、VGE(th)、RDS(on)
   - 动态：td(on)、tr、td(off)、tf、Eon、Eoff、Qg、Qgd
   - 热参数：Rth(j-c)、Zth 瞬态热阻抗曲线、**K 曲线（TSP-Vpn 标定）**
   - AQG 324 QM 组（模块测试）的意义：**先建立特性基线，后续所有寿命试验的判据都以此为基准**
   → 关键理解：**QM 必须在所有 QC/QE/QL 试验的前/后都做**
   → 证据 `[二手]`：AQG 324 体系图中，"QM-01 模块测试"在 QC/QE/QL 的前/后均需执行
   → 来源：https://b2b168.com/wvs204300066.html ｜可信度：★★☆☆☆

STEP2.1.4 无损检测基线（X-ray / SAM）
   - AQG 324 **QM-01 互连层测试**：用 **SAM（声学扫描显微镜）** 检验互连层质量（焊料、扩散焊、烧结互连）
     → 检测目标：**空洞、分层、裂纹** 形式的早期退化失效
   - X-ray 用于焊点空洞率测量
   - 重要：**PC 试验后的 SAM 检查对象是明确的** ——"对被测样中的焊接点裂缝、基座、堆叠部分和外壳可通过声扫进行缺陷检查"
   → 来源：https://b2b168.com/wvs204300066.html（QL-01 说明）｜可信度：★★☆☆☆

STEP2.1.5 IF 涉及 SMD 表面贴装器件的预处理
   → **JESD22-A113**（Preconditioning of Nonhermetic Surface Mount Devices Prior to Reliability Testing）
   → 现行版：**A113I:2020**（Apr 2020）
   → 关联标准：**J-STD-020**（Moisture/Reflow Sensitivity Classification，MSL 分级）
   → AEC-Q101 中作为 **A1 预处理（PC）**：MSL1 走 125°C/24h bake + 85/85/168h + 3×245°C reflow；MSL3 走 125°C/24h bake + 30°C/60%RH/192h + 3×245°C reflow
   - 来源：https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Designed_to_Last_Even_in_the_Harshest_Environments.pdf ｜https://www.cnblogs.com/qixintel/p/18121433 （JESD22 版本/状态表）｜可信度：★★★★☆/★★★☆☆
```

**A104F.01 §7 要求的报告项（之一）—— 与"可追溯性"直接相关** `[一手]`：
> e) **对于资格试验，样品尺寸和质量等级（sample size and quality level）**
> b) 温度极值、保温时间、升降温速率、**循环次数**

→ **这两个参数在报告里缺一不可**，且都必须有来源依据（引 JESD47 / 客户规范 / 自算）。

### 2.2 试验中：主要应力类型的标准方法与条件

#### 2.2.1 温度循环 TC —— JESD22-A104F.01（一手全文已核实）

**版本现状** `[一手]`：

| 版本 | 日期 | 状态 |
|---|---|---|
| A104D | 2009-03 | 已被取代 |
| A104E | 2014-10 | 已被取代 |
| A104F | 2020-11 | 已被取代 |
| **A104F.01** | **2023-04** | ✅ **现行** |

> ⚠️ **纠正任务书表述**：任务书写"JESD22-A104F.01 条件表已核实（04-canon）"。**核实结果：canon 的 T12 待办明确写"JESD22-A104 各温度条件字母（B/G/J/K/M）的确切定义 —— 中优先级 —— 购标准或经 jedec.org 查 scope"，即 canon 并未核实条件表。** 本track 通过下载 A104F.01 一手 PDF 完成了核实，条件表见下。

**表 1 — 温度循环试验条件（一手原文提取）** `[一手]`：

| 试验条件 | 标称 Ts(min) (°C) | 标称 Ts(max) (°C) | 标称 ΔT (°C) `[推断，差值自算]` |
|---|---|---|---|
| A | −55 | +85 | 140 |
| **B** | **−55** | **+125** | **180** |
| **C** | **−65** | **+150** | **215** |
| **G** | **−40** | **+125** | **165** |
| **H** | −55 | +150 | 205 |
| I | −40 | +115 | 155 |
| J | **−0** | +100 | 100 |
| K | −0 | +125 | 125 |
| L | −55 | +110 | 165 |
| **M** | **−40** | **+150** | **190** |
| **N** | **−40** | **+85** | **125** |
| **R** | **−25** | **+125** | **150** |
| **T** | **−40** | **+100** | **140** |

- 来源：A104F.01 §5.2 Table 1，https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf ｜可信度：★★★★★
- ⚠️ **注意 A104F.01 的表 1 只有一个警告块**（4 条注意事项），**没有"应用场景"列**。二手源（antpedia、chipfoundryservices）给每个条件加的"典型应用"（如条件 B = 汽车电子）是**二手推断，不是标准原文**。标为 `[二手]`。
- ⚠️ **纠正一处广泛流传的错误**：chipfoundryservices（内容农场）称 "Condition N −40 to +150, ΔT 190, 3000 cycles, Automotive" —— **把M 的温度和 N 的编号搞混了，且 3000 cycles 不是 A104 的内容**。A104F.01 表 1 中 N 是 −40/+85，M 是 −40/+150。**不采信。**

**表 1 的 4 条 CAUTION（一手原文）** `[一手]`：
> 1) 特定试验条件的 Ts(max) **可能超过某些封装材料的玻璃化转变温度（glass transition temperature）**，从而诱发现场设计应用中不会出现的失效机理
> 2) 需避免 DUT 之间和 DUT 内部的大温度梯度，以保持试验数据完整性
> 3) 试验条件温度范围内的 **CTE 差异可能导致试验板上的镀通孔（plated through holes）提前失效**，从而限制在测器件的电读出能力
> 4) **Ts(max) 超过 125 °C 的试验条件不推荐用于 Pb/Sn 焊料成分**，因可能导致动态再结晶（dynamic recrystallization）

- 来源：A104F.01 §5.2 Table 1 NOTE，同上 URL ｜可信度：★★★★★

> 🔑 **CAUTION 1 和 4 对用户极其重要**：
> - CAUTION 1 直接关系到用户的 AMB/DPC 陶瓷基板与高温密封剂 —— **若 Ts(max)=+150°C 超过密封剂的 Tg，会诱发现场不会出现的失效**。这是"照抄标准条件"最典型的翻车点。
> - CAUTION 4 是**焊料工艺的分水岭**：铅锡（Pb/Sn）焊点在 >125°C 有动态再结晶风险，而**用户的双焊片工艺 + 高温密封剂正是要突破这一限制的做法** —— 这正是"内部规范"的典型产生场景（见 §4.4）。

**表 2 — Soak mode 条件（一手原文提取）** `[一手]`：

| Soak Mode | 在 soak 温度（max）及 soak 温度（min）的**最小 soak 时间**（分钟） | 典型用途（一手 §5.5） |
|---|---|---|
| **1** | **1** | §5.5.1 组件级TC 典型使用（component soak mode） |
| **2** | **5** | §5.5.2 互连（焊点疲劳/蠕变）；§5.5.3 锡须测试（等同 JESD22-A121 的 5–10 min） |
| **3** | **10** | §5.5.2 互连 |
| **4** | **15** | §5.5.2 互连；对应大热质量样品需完全热平衡 |

- 来源：A104F.01 §5.2 Table 2 + §5.5.1/5.5.2/5.5.3，同上 URL ｜可信度：★★★★★

**表 3 — 各条件的典型循环频率与 soak mode（一手原文提取）** `[一手]`：

| 试验条件 | 典型循环数/小时 (Cycles/Hr.) | 典型 Soak Mode |
|---|---|---|
| A | 2–3 | 1, 2 & 3 |
| B | 2–3 | 1 & 2 |
| C | 2 | 1 & 2 |
| G | <1–2 | 1, 2, 3 & 4 |
| H | 2 | 1 & 2 |
| I | 1–2 | 1, 2, 3 & 4 |
| J | 1–3 | 1, 2, 3 & 4 |
| K | 1–3 | 1, 2, 3 & 4 |
| L | 1–3 | 1, 2, 3 & 4 |
| M | 1–3 | 1, 2, 3 & 4 |
| N | 1–3 | 1 & 2 & 3 |
| R | 1–2 | 1 & 2 |
| T | 1–2 | 3 & 4 |

- 来源：A104F.01 §5.6 Table 3，同上 URL ｜可信度：★★★★★

**⚠️ 表 1 的温度容差与 soak time 的定义（一手）** `[一手]`：
- §5.2："The maximum and minimum sample temperatures measured shall be within the range stated in Table 1... Typical boundary values of **+10 °C for Ts(max)** and **−10 °C for Ts(min)** are **discretionary**（任意/酌定）and depending on equipment capability and test objectives."
- §2.9 soak time 定义：soak time 是样品温度处于 `Ts(max)` 标称值的 **−5 °C 到 +10 °C/+15 °C** 范围内的时间（上端），以及 `Ts(min)` 标称值的 **+5 °C 到 −10 °C** 范围内的时间（下端）。**容差依赖试验条件的 tolerance**
- §2.8 **nominal ΔT 定义**："The difference between nominal Ts(max) and nominal Ts(min) for the Temperature Cycling Test Condition; see Table 1."
- 来源：A104F.01 §2.8/2.9/5.2，同上 URL ｜可信度：★★★★★

**升温速率（一手，对焊点疲劳至关重要）** `[一手]`：
- §5.7.1 组件级 ramp rate："Ramp rate is **not generally critical** for most component testing with the exception of interconnects... However, even if using air as the thermal energy coupling medium, it is important to accurately define and control ramp rates as **one may unintentionally generate a near thermal shock test environment** should the stated guidance be surpassed."
- §5.7.2 **互连级 ramp rate**（焊点疲劳评估）：
  - 目标：避免在测样品上出现瞬态热梯度
  - 大热质量、低下传热效率的样品需要足够慢的 ramp rate 以补偿热质量
  - **样品温度在 ramp 期间应处于环境温度的数度范围内**
  - **典型 ramp rate：任何循环段的任一部分 ≤ 15 °C/minute；优选 10 °C 至 14 °C/minute**
  - 大热质量样品可能需要**单区（single zone）箱体**才能达到最佳 ramp rate
  - **NOTE 2（禁止条款）**：**不得用 air-to-air 或 liquid-to-liquid 热冲击箱替代温度循环箱**，因为 DUT 的 ramp rate 很重要，过快会对互连测试产生**不真实的损伤**；且 DUT 上的大温度梯度会导致腔内载荷各处**加速因子不一致**
  - **NOTE 3**：**失控 ramp rate 会无意中造成热冲击试验环境**
- 来源：A104F.01 §5.7.1/5.7.2 NOTE 1-3，同上 URL ｜可信度：★★★★★

**循环次数与中断规则（一手，这是 §3 的关键伏笔）** `[一手]`：
> "The sample shall then be subjected to the specified temperature cycling test condition for **the specified number of cycles (e.g., JESD47 for qualification or as agreed to between the supplier and user)**."
> "Completion of the total number of cycles specified for the test may be interrupted for interim end-point testing, test chamber loading or unloading of device lots, electrical test of samples at specified intervals or as the result of power or equipment failure. **However, if the aggregate number of times of all interruptions exceeds 10% of the total number of cycles specified, the test must be restarted from the beginning.**"
- 来源：A104F.01 §5 Procedure，同上 URL ｜可信度：★★★★★

> 🔑 **这是全track 最重要的单条原文**：
> 1. **A104 不规定循环次数** —— 明确指向 JESD47 或"供采双方约定"
> 2. **中断次数 > 总次数的 10% 必须从头重启** —— 这是硬性规则，写进 SOP
> 3. 中断的**允许事由**被穷举：中间端点测试、装卸样、按规定间隔的电测、**电源或设备故障**
> → `[推断]` "设备故障导致的中断计入 10% 限制"是很多实验室的盲点 —— 意味着设备可靠性直接影响试验有效性，**设备 uptime 是qualification 的一部分**。

**⚠️ 二手源对 A104 的错误信息（不采信）** `[二手，仅作反例]`：
- antpedia 与 kpt-bj 称"保温模式 1/2/3/4 对应 1/5/10/15 分钟，模式 2 用于锡须、模式 3 用于焊点疲劳、模式 4 用于大热质量" —— **模式 1/2/3/4 的时间值正确（1/5/10/15 min 与一手一致）**，但**用途归属描述与一手 §5.5 不完全一致**（一手说模式 2/3/4 都用于互连，模式 2 等同锡须）
- 两源都称 A104F.01 表格中"有 13 个试验条件 A 至 T" —— **实际表 1 是 13 行（A,B,C,G,H,I,J,K,L,M,N,R,T），正确**
- antpedia 称 "Standard allows interruptions... **must not exceed 10%**" —— 与一手一致 ✅
- kpt-bj 称"定义了 4 种 **immersion mode**（浸泡模式）" —— **术语错误**，一手是 **soak mode**（保温/浸温模式），不是 immersion

#### 2.2.2 TBL / HTOL / HTRB / HTGB —— JESD22-A108G

**版本与真名（一手校正）** `[一手]`：
- **JESD22-A108G**，发布 **2022 年 11 月**，取代 A108F（2017）
- 英文标准名：**"Temperature, Bias, and Operating Life"**（TBL = Temperature, Bias, and Life）
- 来源标注：来自 JEDEC Board Ballot **JCB-22-55**，归口 **JC-14.1 Committee**
- **14 页**
- 来源：https://www.antpedia.com/standard/1195904236-10.html ｜https://plusstd.com/1195904236.html ｜可信度：★★★★☆（两个独立二手源给出一致的版本/日期/ballot 号/委员会，可信度较高；但**未取得 JEDEC 一手 PDF，标为"高可信二手"**）

> ⚠️ **纠正任务书表述**：任务书写"功率循环 Power Cycling（JESD22-A108 TBL 与 AQG 324 的 PCsec/PCmin 差别）"。
> **核实结论：A108 = TBL（Temperature, Bias, and Operating Life），是 HTOL/HTRB/HTGB/HTFB/LTOL 的母标准，与功率循环无关。** 功率循环的标准是 **JESD22-A122（Power Cycling）** 与 **JESD22-A105（Power and Temperature Cycling）**，方法学母标准是 **IEC 60749-34**。
> **A108 与 A122 的差别才是用户想知道的"高频困惑"**，见下表。

**JESD22 的"功率/偏压/循环"方法族辨析（这是选型的基础）**：

| 方法 | 英文名 | 是否通电 | 典型定位 | 现行版本 |
|---|---|---|---|---|
| **A108** | Temperature, Bias, and Operating Life (TBL) | ✅ 偏压 | **HTOL / HTRB / HTGB / HTFB / LTOL 的母标准** | **G (2022-11)** |
| **A105** | Power and Temperature Cycling | ✅ 功率 | 上电温循（PTC）；器件在温度变化间做功率循环；聚焦**板级焊点** | **D (2020)** |
| **A122** | Power Cycling | ✅ 功率 | 封装功率循环；功率开关造成封装内**非均匀温度分布** | **A (2016)** |
| **A104** | Temperature Cycling | ❌ | 组件/焊点级等温温度循环 | **F.01 (2023-04)** |
| **A106** | Thermal Shock | ❌ | 快速温变；**非模拟真实使用** | **B.01 (2016-11)** |

- A105 版本与条件：`[二手]` "T_cycle(min) = −40 °C，T_cycle(max) = 80…125 °C，温度循环周期 ≥ 1 h；功率循环 on-time 默认 5 min，off-time 5 min"
- A122 Scope 原文（关键！）：`[一手，A122-2007 摘要]`
  > "In typical use, the on and off power cycles of functional devices will produce **non-uniform temperature distributions** within package components as well as between the package and interconnected hardware such as printed wiring boards (PWB), sockets, or heat sinks. The stresses that result from the temperature gradients found in actual product **may or may not be accurately simulated by use of isothermal temperature cycling**."
  > "This test method is **a characterization tool** which can augment and supplement results obtained with the isothermal chamber-based temperature cycling described in both JESD22-A104 and JESD22-A105. **It should be used as an alternative to JESD22-A104 or JESD22-A105 only if such substitution can be technically justified.**"
  > "The power cycles described in this test method are intended to simulate the range of usage conditions found **from the vicinity of room ambient up to Tj maximum**... and are **not specifically intended as a highly accelerated test** or to apply to harsh application conditions such as those used to simulate some **under-the-hood or aerospace** environments."
- 来源：https://plusstd.com/5148441.html （A122-2007 Scope）｜https://core.ac.uk/download/552888767.pdf （A105/A122 对比）｜https://www.cnblogs.com/qixintel/p/18121433 （版本状态表）｜可信度：★★★★☆（A122 Scope 是标准摘要原文）

> 🔑 **A122 的 Scope 给出了明确的使用规则**：
> 1. A122 是**表征工具（characterization tool）**，不是资格试验本身
> 2. **只有"技术上能论证"（technically justified）时**，才可用A122 替代 A104 或 A105
> 3. A122 **不是高度加速试验**，且**不适用于 under-the-hood 或航空航天等严酷环境**
> → `[推断]` 对用户的车规模块项目：**AQG 324 QL-01/QL-02（PCsec/PCmin）不引用 A122，而是引用 IEC 60749-34**。原因就是 A122 自己声明"不是高度加速试验、不适用 under-the-hood"。这解释了标准体系里 IEC 与 JEDEC 的分工。

**A108G 的条件框架（一手转述，多源一致）** `[二手，高可信]`：

| 要素 | 要求 |
|---|---|
| 环境试验箱 | 需在**样品加载且未通电**状态下，于整个腔室内保持规定温度，**容差 ±5 °C** |
| 仪器 | 数字万用表、示波器等需校准且具长期稳定性 |
| **应力时长** | "设计为达到或超过应用使用条件下的等效现场寿命。时长基于应力加速确定（**参见 JEP122**），由应用资格要求、**JESD47** 或适用采购文件规定" |
| **高温应力环境温度** | 应调整环境温度与偏压，使受应力器件的**最低结温达到 125 °C**，除非另有规定用于扩展使用或其他环境 |
| 低温应力环境温度 | 最高 **−10 °C** |
| **冷却要求** | 高温应力下的器件应在**移除偏压前冷却至 55 °C 或更低**；若制造商提供验证数据，特定技术可能不需要在偏压下冷却 |
| 测量时机 | 初始时、每个中间期结束时、寿命试验结束时 |
| 测量顺序约束 | 中间和最终测量可能包括高温测试，但**高温测试只能在完成规定的室温（及更低温度）测试测量之后**进行 |
| 失效判据 | 器件不符合适用采购文件的要求即为失效 |
| **HTRB 偏压** | 反向偏置主要功率处理结，**静态模式，通常为最大额定击穿电压的 80%–100%** |
| **HTGB 偏压** | 偏置栅极或其他氧化物，**静态模式，接近最大额定氧化物击穿电压** |
| **HTFB 偏压** | 正向偏置主要功率处理结，功率器件/二极管/分立晶体管，静态或脉冲模式，**接近最大额定电流** |
| HTOL | 偏置器件工作节点，逻辑和存储器器件，动态工作模式 |
| LTOL | 偏置器件工作节点，存储器或亚微米器件（检测热载流子引起的失效）|

- 来源：https://plusstd.com/1195904236.html ｜https://www.antpedia.com/standard/1195904236-10.html ｜https://xktest.cn/news/show/38143.html ｜可信度：★★★★☆（三源一致，含 A108G 相对 F 版的4.2.2 / 4.2.3.3 / 第8章变更说明）

**A108G 相对 A108F 的具体变更（一手转述）** `[二手，高可信]`：
- **4.2.2**：重新表述段落，**允许在任何条件下使用较低的工作电压**；增加了"当未使用最大工作电压时，**报告认证期间使用的电压**"
- **4.2.3.3**：在句子中添加了"（**通常为 80% 至 100%**）"的短语
- **第 8 章**：标题从"摘要（Summary）"改为"**寿命测试报告（Life Test Report）**"

> 🔑 **4.2.2 的变更是一条极其实用的合规规则**：**如果你在认证中用了低于最大工作电压的偏压，你必须在报告中声明实际使用的电压。** 很多工程师不知道这一条 —— 报告里只写"1000h @ 150 °C"而不写偏压电压，是不满足 A108G 的。

**A108G 要求寿命试验报告包含的项目（一手转述，13 项）** `[二手，高可信]`：
> 1. 特殊预处理（special preconditioning）
> 2. 应力温度（箱体环境）
> 3. 应力持续时间
> 4. 应力安装方式（若需特殊说明）
> 5. 应力条件与**应力电路原理图**
> 6. **样本量与接收数（sample size and acceptance number）**
> 7. 完成终点测量的时间（若不同于第 6 章规定）
> 8. 工作模式（operating mode）
> 9. 中间读点（若需要）
> 10. **应力期间的最大结温**
> 11. 若未在偏压下冷却，提供验证数据
> （另含 A108G 变更后的第 8 章结构）

> 🔑 **第 5 项"应力电路原理图"和第 6 项"样本量与接收数"是功率模块最容易缺的两项** —— 前者因为模块偏压回路复杂（含栅极驱动、功率回路）常被省略；后者因为"零失效"常被写成"PASS"而不给数字。

**A108G Scope 的关键排除（一手）** `[二手]`：
> "本测试用于确定偏置条件和温度对固态器件随时间变化的影响，以加速方式模拟器件工作条件，**主要用于器件鉴定与可靠性监控**；**不包括用于筛选早期失效的"老化测试"（burn-in）**。老化（burn-in）的详细使用和应用不在本文件范围内。"

> 🔑 **TBL ≠ burn-in。** 这是一条必须内建到知识 OS 的边界（对应 Track 04 的 T1 陷阱：MIL-STD-883 的 1015 = burn-in，不是温循）。

#### 2.2.3 HV-H3TRB / H3TRB / HTRB 的条件与定位

**H3TRB 是什么（用户实际在做的试验）** `[二手]`：

| 变体 | 全称 | 条件 | 来源 |
|---|---|---|---|
| **H3TRB** | High humidity, high temp reverse bias（高温高湿反偏） | T = 85 °C，RH = 85%，**Vds = 100 V**，Vgs = 0 V，t = 1000 h | Power Electronics News★★★★☆ |
| **HV-H3TRB** | High Voltage H3TRB（高压高温高湿反偏） | Vds 提高到**额定值的 80%**，例如 **960 V 用于 1200 V 器件** | 同上 |
| （H3TRB 的 IEC 对应） | Steady-state temperature humidity bias | **IEC 60749-5**（85/85 稳态），H3TRB 概念源自此| canon `[一手]` |

- 来源：https://www.powerelectronicsnews.com/h3trb-reliability-tests-for-sic-power-devices/ ｜可信度：★★★★☆（技术期刊，条件表述与 Wolfspeed 表格完全一致）
- 交叉验证：Wolfspeed 表格给出 H3TRB：Vds=100V、Vgs=0V、85%RH、Ta=85°C、1000 hrs、`[一手]` 厂商技术文档，★★★★☆。**两源一致。**

> 🔑 **HV-H3TRB 不是独立的标准编号**。它是 AEC-Q101 语境下 H3TRB 的**高压变体**：把 Vds 从固定 100 V 提到器件额定值的 80%。
> **用户的 HV-H3TRB（1000H 23pcs / 1500H 6pcs）在标准体系中的定位是"AEC-Q101 的加严项"，用于考核高压 SiC/IGBT 的终端结构与钝化层在湿热+高压下的稳定性。**

**H3TRB 的加速模型（Peck 型，含电压项）** `[二手]`：

```
AF(a/ref) = (RH_test / RH_ref)^x × (V_test / V_ref)^y × exp[ (Ea/k) · (1/T_ref − 1/T_test) ]
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `AF(a/ref)` | 试验条件 a 相对正常使用条件 ref 的加速因子 | 无量纲 |
| `RH_test`, `RH_ref` | 试验/参考相对湿度 | % |
| `V_test`, `V_ref` | 试验/参考电压 | V |
| `x` | **湿度的经验指数** | 无量纲 |
| `y` | **电压的经验指数** | 无量纲 |
| `Ea` | 活化能 | eV |
| `k` | Boltzmann 常数 = 8.617×10⁻⁵ eV/K | eV/K |
| `T_test`, `T_ref` | 试验/参考绝对温度 | K |

- 来源：https://www.powerelectronicsnews.com/h3trb-reliability-tests-for-sic-power-devices/ ｜可信度：★★★☆☆
- `[推断]` 该式与Track 04 §3.3 的 Peck 幂律一致，仅增加了**电压项 f(V) → (V/V_ref)^y**。这是 Peck 模型的电压型扩展。
- ⚠️ **x、y、Ea 的具体数值本文未给出，标为「需查原始文献」**。相关原始文献线索：K. Hatori et al., "Investigation of acceleration factors for HV-H3TRB test on 3.3 kV SiC SBDs," **ECCE 2023**；K. Kitajima et al.（湿度加速）。

**一个极为重要的 H3TRB 工程陷阱（一手级推理，二手证据）** `[推断]`：
> 原文警告："under **constant absolute humidity** conditions, even a small increase in temperature, say from self-heating, can lower the RH significantly and hence **improve lifetimes**."
> → **自加热会降低腔内 RH，从而掩盖失效。** 对大功率模块做 H3TRB 时，**必须监测实际 RH 而非只设���定值**。

**SiC 的 H3TRB 特殊之处（一手厂商数据）** `[二手，高可信]`：
- **AQG 324 对 Si 与 SiC 的 H3TRB 电压要求不同**：Si 强制 **80 V**；SiC 必须为**额定 VDS(max) 的 80%**
- 来源：https://www.eet-china.com/mp/a237849.html（安森美技术文章）｜可信度：★★★☆☆
- SiC 失效特征：Si 器件有 **Al 环终端**，H3TRB 下 Al 环腐蚀 + 表面电荷累积导致击穿电压下降；**SiC 器件通常无 Al 环，表面电荷影响较小**
- 一手数据对比：`[二手]` 相同封装下，Si IGBT 在 **65% 额定电压、2000 h** 应力后出现漏电流升高与击穿电压下降；**SiC MOSFET 在 90% 额定电压下未见可见退化**
- 关键工程结论：**"For SiC power devices, the HV-H3TRB is now considered a key qualification test... With this test, the HAST test is considered unnecessary"** ——即 **SiC 器件做 HV-H3TRB 后可免做 HAST**，理由是 HAST 可能导致电弧早期失效
- 来源：https://www.powerelectronicsnews.com/h3trb-reliability-tests-for-sic-power-devices/ ｜可信度：★★★★☆

> 🔑 **对用户的直接价值**：用户做的是 IGBT（Si 基）模块。**AQG 324 对 Si 基模块的 H3TRB 只要求 80 V，而用户实际做的是 HV-H3TRB（高压）** —— 这说明用户做的是**高于 AQG 324 基线的要求**。这是一个需要在报告中明确的定位（见 §4.2 取严原则）。
> **同时**：用户项目 "168H 74pcs" 这一档很可能是**早期筛选/工艺评估性质**（HV-H3TRB 的 1000 h 才是资格性时长），而 1500H 6pcs 属于**延长确认**。三档并存说明采用了"阶梯应力+样本量递减"的设计，这是合理的工程做法，但**必须在报告中说明三档的定位与统计口径**。

**IEC 60749-5 (THB/85-85) 的条件（一手，canon 已核实，此处复核）** `[一手]`：
- 温度 **85 ± 2 °C**、相对湿度 **85 ± 5 % RH**、时长 **1000 h（+168/−24 h）**
- 去离子水电阻率 ≥ 1 × 10⁴ Ω·m；干球温度须始终高于湿球温度
- 湿球温度 81.0 °C，水蒸气压力 49.1 kPa（7.12 psia）
- 升降温速率应< 3 h 以避免器件表面凝露
- 试验后 **48 h 内**完成电性能测试（IEC 60749-5 Ed 3.0）；A101D.01 则要求 **168 h 内**完成中间和最终测量
- **偏压选择准则** `[二手]`：器件功耗 > 200 mW 或虚拟结温升 ΔTja ≥ 10 °C 时，采用 **1 h on / 1 h off 循环偏压**
- **HAST vs THB 的优先级规则（一手，实用价值高）**：
  > "When both test methods are performed, test results of the 85 °C/85 % RH steady-state temperature humidity bias life test, IEC 60749-5, **take priority over HAST**." + "This test method shall be considered **destructive**."
- 来源：https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-5%7Bed3.0.RLV%7Den.pdf ｜https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-4%7Bed2.0%7Db.pdf ｜可信度：★★★★★（VDE = IEC 出版方，标准正文预览）

> 🔑 **A101D.01 与 IEC 60749-5 的测量窗口不同（168 h vs 48 h）** `[推断]`：这是"同族不同源标准"的典型差异。**报告里应写明依据的是哪一个**，否则会出现"我们 168h 内测了，为什么你们说 48h"的争议。

#### 2.2.4 功率循环 PCsec / PCmin —— AQG 324 + IEC 60749-34

**AEG 324 QL 组完整清单（04.1/2025 目录）** `[一手，canon 已核实]`：

| 编号 | 名称 | 现行版 |
|---|---|---|
| QL-01 | PCsec（秒级功率循环，ton < 5 s） | 02.1/2019 起 |
| QL-02 | PCmin（分钟级功率循环，ton > 15 s） | 02.1/2019 起 |
| QL-03 | HTS（高温存储） | — |
| QL-04 | LTS（低温存储） | — |
| QL-05 | HTRB（高温反偏） | — |
| QL-06 | HTGB（高温栅偏） | — |
| QL-07 | H3TRB（高温高湿反偏） | — |
| **QL-08** | **HTFB**（高温正偏） | **04.1/2025 Annex SiC 新增** |
| **QL-09** | **DGS**（动态栅极应力） | 同上 |
| **QL-10** | **DRB**（动态反偏） | 同上 |
| **QL-11** | **dyn. H3TRB**（动态高湿高温反偏） | 同上 |
| — | GaN | 占位，"to be added in a future release" |

**QL-01/QL-02 的实测条件（多源交叉）** `[二手]`：

| 参数 | PCsec | PCmin | 来源 |
|---|---|---|---|
| 开通时间 ton | **< 5 s** | **> 15 s** | AQG 324（二手转述，多源一致）★★★★☆ |
| 负载加热电流 IL | **> 0.85 I_N** | 同 | ictest8 ★★★☆☆ |
| 栅极电压 Vgate | 15 V | 15 V | ictest8 ★★★☆☆ |
| 控制策略 | **AQG 324 规定恒定结温方式** | 同 | ictest8 ★★★☆☆ |
| 结温测量 | **Vce(T) 方法（参考 JESD51-14）** |同 | ictest8 + AQG ★★★☆☆ |
| ΔTj | 75–125 °C（典型配置） | 同 | Wolfspeed ★★★★☆ |
| Tj,max | 125–175 °C（典型配置） | 同 | Wolfspeed ★★★★☆ |
| **失效判据** | **VCE(sat) 上升 5%** 或 **Rth 上升 20%** | 同 | 多源一致 ★★★★☆ |
| 方法学母标准 | **IEC 60749-34:2011** | 同 | ictest8 / x-ipm ★★★☆☆ |

- ⚠️ **QL-01 特有要求** `[二手，b2b168]`："在测试中做**至少两组对比试验**，即选择两组不同的温升，**温升必须比小温升高出 40%**，以验证靠近芯片互连的可靠性曲线（寿命曲线）"
  → `[推断]` 这实际是要求做**两个应力水平的寿命点**，以便拟合 ΔTj 的幂律指数。**这一条对用户做寿命模型标定极有价值** —— 意味着 AQG 324 本身要求多点数据，而非单点。
- ⚠️ **QL-02 特有要求** `[二手]`："**绘制寿命曲线**"（lifetime curve）
  → 即 PCmin 试验的目的是**建立/验证寿命模型**，不是简单的 pass/fail。

**⚠️ QL-03~QL-07 条件的可靠度警告** `[未核实]`：
一个二手源（x-ipm）给出：QL-03 HTS ≥125 °C/1000 h（IEC 60749-6）；QL-04 LTS ≤−40 °C/1000 h（JESD22-A119:2015）；QL-05 HTRB Tjmax/≥1000 h；QL-06 HTGB Tjmax/≥1000 h；QL-07 H3TRB 85 °C/85%RH/≥1000 h。
**但该源对 QL-06/QL-07 给出的引文明显错位**（QL-07 标为 "IEC 60747-8:2010 (MOSFET)"，而 QL-06 引 "IEC 60747-9:2007 section 7.1.4.1 (IGBT)"，QL-07 标题写 "HSTRB" 但内容是反偏）。
→ **标注为「未核实，需查 AQG 324 04.1/2025 第 9 章原文」。本track 不把这些数值写入知识 OS 的正典区。**

**PC 的四种控制策略（一手，A122 允许四种）** `[二手，引用 A122 §4.2]`：
> a) 恒功率（开环） b) 可变功率（闭环） c) 恒定冷却（开环） d) 可变冷却（闭环）
>
> ⚠️ **一个重要的定量警告**（原文转述）："**variable control of power to reach a constant junction temperature swing during testing may over-estimate the power cycling capability by a factor of 3.2** compared to constant on-time (with constant load current amplitude). The latter is closer to application, where the load will not be reduced during lifetime and thus **degradation of thermal resistance and voltage drop will increase the temperature swings** for the same given load cycle and cause **self-accelerating of degradation** to take place."
- 来源：https://core.ac.uk/download/552888767.pdf ｜可信度：★★★☆☆（学位论文，作者引用 A122 原文）
- `[推断]` **这是 AQG 324 要求"恒定结温方式"的最强理由**：闭环恒 ΔTj 的控制方式会**高估功率循环能力约 3.2 倍**，因为它消除了"退化自加速"效应。**做寿命外推时必须用恒定 on-time + 恒定负载电流模式。**

**功率循环三种设备工作模式** `[二手]`：恒电流、恒功率、恒结温差、恒壳温差。**AQG 324 规定的是恒定结温方式**；SGS 提到"恒定壳温差模式 ΔTc：循环中改变冷板热传导系数，适用于长时间周期的功率循环测试"。

#### 2.2.5 高温存储 HTS / 低温存储 LTS —— JESD22-A103 / A119

**A103（高温存储）条件与条件分级** `[二手]`：

| 条件 | 温度 | 典型时长（按封装与等级） |
|---|---|---|
| A | +125 °C | — |
| B | +150 °C | 1000 h（典型参考值）|
| C | +175 °C | — |
| D | +200 °C | 陶瓷封装 +200 °C/72 h |
| E | +250 °C | 陶瓷封装 +250 °C/10 h |
| F | +300 °C | 极限测试 |

- 温度容差 **−0/+10 °C**
- 条件选择必须考虑：金属材料熔点与冶金界面退化（焊料熔化/界面失效）、封装完整性（玻璃化转变温度、聚合物降解）、湿度等级 J-STD-020 兼容性、硅器件限制（电荷保持能力/NVM 数据丢失）
- **测试时长应在JESD47 等鉴定文件或可靠性监控协议中规定；A103E 版本起强调用 JESD94 使用条件数据 + JEP122 模型确定时长**
- **测量窗口**：中间和最终电测应在器件从试验条件取出后 **168 h 内**完成
- **失效判据**：参数超限、功能丧失、机械损伤。**封装外观缺陷和引线表面退化不算有效失效判据**
- **A103E 相对 A103D 的变更**：参考文献增加 **JEP122 和 JESD94**
- 来源：https://www.antpedia.com/standard/7720056-10.html ｜https://plusstd.com/7720056.html ｜http://www.dgrk17.com/Article/xpickkxyzs.html ｜可信度：★★★★☆（多源一致）

- ⚠️ **撤销一项未经核实的条件表**：chipfoundryservices（内容农场）给出 "Grade 0: +175 °C/1000 h 或 +150 °C/2000 h；Grade 1: +150 °C/1000 h 或 +175 °C/500 h；Grade 2–3: +125 °C/1000 h 或 +150 °C/500 h" —— **这组Grade 分级来自 MIL-STD-883 方法 1035 的等级（grade）体系，不是 JESD22-A103 的条件 A–F**。两者被混淆。**标为未核实，不写入。**

**A119（低温存储）** `[一手，canon 已核实]`：`JESD22-A119:2015 Low Temperature Storage Life`，AQG 324 02.1/2019 与 04.1/2025 **均一手引用**。现行版 A119A:2015。

### 2.3 试验后：失效分析流程

**（本节的"标准介入点"：各标准的"Failure criteria"章节 + 报告章节 + 失效分析标准族）**

```
STEP 2.3.1  电性复测（判定是否真失效）
   IF 判据是"参数漂移"型（如VCE 上升 5%）
      → 必须做**逐器件对照**：与基线数据比对，而非只看是否超规格
      → 报告须给出：漂移量分布（中位数/最大/最小）、判定阈值、阈值来源
   IF 判据是"功能失效"型
      → 按A108G 顺序：先做室温及更低温度测量，再做高温测量
      → 依据：A108G 原文 "high temperature testing shall only be performed after
              the specified room temperature (and lower) test measurements have
              been completed"
   测量时间窗（依标准而异，必须在报告中声明）：
      - JESD22-A108（TBL类）：测试期间 ≤ 55 °C 冷却；报告须含终点测量时间
      - JESD22-A103（HTS）：取出后 **168 h 内**
      - IEC 60749-5（THB）：**48 h 内**
      - JESD22-A101D.01：中间和最终测量在**取出后 168 h 内**
      - AEC-Q101 IOL（Method 10）：**96 h 内**完成端点测量
      → `[推断]` **这些窗口必须在SOP 里做成矩阵**，否则跨项目复用数据会踩坑

STEP 2.3.2  无损定位（电性异常已确认）
   IF 怀疑焊点/键合线/空洞/分层
      → **X-ray**（空洞率、焊点裂纹）
      → **SAM 声学扫描显微镜**（分层、界面空洞）—— AQG 324 QM-01 指定的手段
   IF 怀疑封装整体裂纹/陶瓷裂纹
      → **C-scan 超声扫描**（无损）
   IF 怀疑热阻路径变化
      → 复测 Rth / Zth + **瞬态热阻抗曲线 → 结构函数（structure function）分解**
      → `[二手]` SGS 明确提到"通过瞬态双界面测试法获取不同时刻的瞬态热阻抗曲线，经算法处理得到**结构函数**，用于分析器件内部各层材料的热阻和热容分布"，可"实时显示器件内部降级过程，无需事后破坏性失效分析"
      → 这对"分层/空洞在哪一层"的定位极有价值

STEP 2.3.3  破坏性分析（金相剖切）
   → **切片金相（cross-sectioning）** 是功率模块失效分析的核心手段
   → 典型顺序：灌封 → 切割 → 抛光 → 侵蚀 → 光学/SEM 观察
   → 目标失效模式：芯片焊接层裂纹、DBC 铜箔裂纹、陶瓷裂纹、键合线根部裂纹、塑封料空洞

STEP 2.3.4  微观定位（SEM / EDS / FIB）
   → SEM：键合线断裂面、芯片金属化重构、焊点裂纹扩展路径
   → EDS：元素分析（判断是否 Kirkendall 空洞、Cu 迁移、Ag 烧结层退化）
   → FIB：定点切割，用于 TEM 观察

STEP 2.3.5  失效模式判定（对照标准判据）
   → 必须回到 §2.3.6 的判据表逐条比对
   → 判据不确定时的处置：见 §2.3.7

STEP 2.3.6  失效模式 ↔ 应力条件 ↔ 判据 对照表（★ 用户最需要的表）
```

**功率模块主要失效模式与对应应力/标准（综合多源）** `[二手，★★★★☆ 交叉验证]`：

| 失效模式 | 主控应力 | 主导试验 | 典型判据 | 定位手段 |
|---|---|---|---|---|
| **键合线疲劳断裂/脱落**（PCsec 首要模式） | 通电发热造成芯片附近热循环，ton < 5 s | **AQG QL-01 PCsec** / A122 | **VCE(V)/VCE(sat) 突升 > 5%** | X-ray、SAM、开盖 SEM |
| 芯片金属化退化/重构（Al 晶粒挤出） | 高 Tj + 热循环 | **AQG QL-01 PCsec** | VCE 渐进上升 > 5% | SEM（前后对比）|
| 芯片焊接层（DBC 上）裂纹 | 芯片与 DBC 铜层 CTE 失配 | **PCsec** 或 **TC** | VCE 上升 / Rth 上升 | 切片金相 |
| **基板-底板焊层开裂**（PCmin 首要模式） | ton > 15 s，热量渗透到整个 DBC | **AQG QL-02 PCmin** | **Rth 上升 > 20%** | 切片金相 + SAM |
| 塑封料开裂/分层 | 整体 CTE 失配 + 吸湿 | **TC（A104）**、**TST（A106）** | 外观、SAM 分层面积 | SAM、切片 |
| DBC 陶瓷/铜箔裂纹 | 陶瓷-铜 CTE 失配 + 安装应力 | **TST（需加散热器）** | 绝缘耐压失效 | 切片金相、绝缘耐压 |
| 芯片/钝化层/终端缺陷 | 高温 + 反偏电场 | **HTRB**、**HV-H3TRB** | 漏电流上升、击穿电压下降 | 开盖光学（烧熔洞）、EDS |
| 栅氧退化 | 高温 + 栅偏 | **HTGB** | IGES 上升、Vth 漂移 | 栅极周围烧毁痕迹 |
| 钝化层/PI 层剥离、钝化层裂纹 | 湿热 + 电场 | **H3TRB / HV-H3TRB** | 漏电流上升、击穿电压下降 | 光学（失效点在 PI/钝化层下方）|
| Al 环终端腐蚀 | 湿热 + 反偏 | **H3TRB** | 击穿电压下降（Si 特有） | 光学/化学去层 |

- 来源：https://www.ab-sm.com/a/46818（索力德普实验室技术报告，逐条对应 PCsec/PCmin/HTRB/HTGB/H3TRB/IOL 的失效现象与机理，★★★★☆）｜https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Power_Cycling_and_Lifetime_Modeling_Approach.pdf ｜https://www.ictest8.com/a/seminar/experience/2024/12/AQG.html
- `[推断]` 上述映射与 AQG 324 附录 II.C"物理分析典型要点"应对应 —— **但我未取得附录 II.C 原文，标为待核实**。

**关于"PCsec 焊层裂纹方向"的一条精细知识** `[二手，★★★★☆]`：
> 含铅焊料一般**从芯片的周边逐步向中心开裂**；而含锡、银材料的焊层**由芯片中心出现开裂**。
- 来源：https://www.ab-sm.com/a/46818
- `[推断]` 这对"双焊片工艺"的失效分析极有用：若观察到从芯片中心开裂，指向无铅/银烧结体系；若从周边向中心，指向含铅焊料体系。**这是一个可直接使用的诊断判据。**

**关于"芯片尺寸覆盖性"的一条反直觉知识** `[二手，★★★★☆]`：
> 对于**模块**（DBC 结构）：DBC 铜箔表面应力来源于**陶瓷材料与铜箔的 CTE 差异**，当模块中的**芯片尺寸越小时，DBC 铜箔受到的应力则越大**，此时**无法**用同平台大尺寸芯片的 TS 试验覆盖小尺寸芯片。
> 但**裸 DBC 在热冲击下约 100 次左右就可能出现陶瓷开裂或铜箔脱离；封装完芯片之后，整个 DBC 的可靠性显著提升 —— 再做 100 次试验则很少出现上述情况。**
- 来源：https://www.ab-sm.com/a/46818
- `[推断]` **对用户的直接价值**：
> 1. **不能简单用"大芯片通过"来覆盖"小芯片"的 TS 试验**（这与单管的情况相反）
> 2. **裸 DBC 与封装后 DBC 的可靠性差异巨大** → 意味着 **DBC 来料检验（用户工序①）需要独立的陶瓷可靠性验证**，不能只靠成品模块的 TS/TC 间接覆盖
> 3. 这直接支撑了用户做DBC/AMB/DPC 行业报告的必要性

**STEP 2.3.7  ⚠️ 判据的已知缺陷（必须写进 SOP 的诚实条款）**

`[二手，★★★☆☆，但工程价值极高]` ictest8 的一手实验经验总结（标题即"主驱功率循环实验设计及判据分析研究"）：
> "**基于 AQG324 标准的热阻测量，无法精确和重复，用 20% 的增量作为判据来判定失效，不严谨。**"
>
> 理由（原文四条）：
> 1. 实际功率循环中**热阻测量的重复性不好**；Tc 的测量相对于实际壳温偏高，从而导致**结壳热阻偏小**，功率循环前后其**物理意义发生了很大变化**
> 2. Ts、Tf 的测量同样存在**物理意义会发生变化**的问题
> 3. **双面散热器件的热阻测试完全不靠谱**，因为热是相互耦合的，三维温度场的变化用一维公式计算，**误差无法估计**
> 4. **热阻值的变化体现了系统散热路径上所有材料的降级总和**，包含 Die Attach、焊接层和接触热阻，而**无法确定每一层材料在实际过程中所占的降级权重**
- 来源：http://ictest8.com/a/seminar/experience/2024/12/AQG.html ｜可信度：★★★☆☆（第三方实验室的实测经验总结，非标准原文，但技术论断具体且可检验）

> 🔑 **对用户的 SOP 建议** `[推断]`：
> 1. 报告中**必须写明 Rth 的测量方法**（瞬态法？稳态法？双面散热如何处理？Rthjc / Rthjs / Rthjf 用哪个？）
> 2. **必须给出测量重复性数据**（同一样品多次测量的 σ/Rth）
> 3. **双面散热模块需明确说明热阻测量的局限**，或改用替代指标（如 Zth 结构函数、TSEP）
> 4. 失效判定建议**以 VCE（电学量，直接对应功能）为主判据，Rth 为辅判据**，并用 SEM/金相闭环验证

**STEP 2.3.8  失效分析报告结构（8D / FA Report）**

**A108G 强制要求的寿命试验报告 13 项**（见 §2.2.2）—— 这是**标准强制的最小集合**。

**JESD69（Information Requirements for the Qualification of Silicon Devices）** 是"资格报告内容要求"的专门标准 `[一手，JESD47 §2 引用确认]` —— ⚠️ **未取得原文，内容标注未核实。**

**8D 报告的通用结构** `[推断，基于工程惯例]`：
```
D1  团队（Team）—— 责任人、角色
D2  问题描述（Describe）—— 失效现象、批次、追溯信息（SN 级！此处用到 STEP 1）
D3  临时遏制（Containment）—— 已采取的临时措施
D4  根本原因（Root Cause）—— ★ 必须区分"失效模式"与"根本原因"
D5  永久纠正措施（Corrective Action）
D6  实施与验证（Implement & Validate）—— ★ 需用同一应力条件做验证试验
D7  防止再发（Prevention of Recurrence）—— ★ 修改标准/规范/PFMEA
D8  团队表彰（Recognition）—— 可选
```

> 🔑 **把用户的三个真实项目串起来看**：
> - **PFMEA（AIAG & VDA FMEA 2019 七步法，400+ 行）** →对应 **D7**（防止再发）。VDA FMEA 的七步法（规划/分析/评价/优化/沟通/评审/发布）中的 S4 优化措施应包含"修改可靠性试验条件"
> - **SN 编码追溯改善** → 对应 **D2**（问题描述）与 **IATF 16949 8.5.2.1e**（"若客户或法规标准规定，须对单个产品做序列化标识"）。**SN 编码是 IATF 条款的直接要求，不是"管理改进"**
> - **双焊片+高温密封剂工艺** → 对应 **D5/D7**。注意这正好是 §2.2.1 提到的 A104 CAUTION 4（Pb/Sn >125 °C 动态再结晶）的直接应对 —— **用户已经在做标准驱动的产品改进了**

---

## 3. 从标准条款到试验方案的翻译流程（★ 核心方法论）

> **这是本track 的技术核心，也是用户最需要的部分。**

### 3.0 官方骨架：JESD94（不用自创流程）

**JESD94B 流程图（PSMA 官方演讲中给出的完整链条）** `[一手，JEDEC 官方委员会演讲材料]`：

```
┌─────────────────────────────────────────────────────────────────┐
│ INPUTS输入                                                      │
│  · Component / Device 器件                                        │
│  · Use Condition Elements使用条件要素                             │
│  · Customers 客户          · Market 市场                         │
│  · System & Application (V, T) 系统与应用                         │
│  · Product Req (Lifetime, FIT) 产品要求                            │
│  · MISSION PROFILE 任务谱：典型使用条件                            │
│  · Targeted Lifetime / FIT Rates / MTTF 目标寿命与失效率│
│  · Related Application Standards 相关应用标准                      │
│  · Supplier Knowledge 供应商器件知识                               │
└──────────────────────────┬──────────────────────────────────────┘
                           ↓
              ┌────────────────────────────┐
              │ PROCESSING（方法论处理）      │
              │  Fail Mechanisms Selection  │
              │    (JEP131 FMEA)            │  ★ 失效机理选择 = FMEA
              │           ↓                 │
              │  Development Or Mapping to  │
              │  Rel Models                 │
              │  (JEP122) // (JESD91)       │  ★ 映射到寿命模型
              │           ↓                 │
              │  Req't Calculation         │  ★ 需求计算 = AF
              │           ↓                 │
              │  Qualification Strategy     │
              │  (JEP143)                  │  ★ 定策略
              └────────────┬───────────────┘
                           ↓
              ┌────────────────────────────┐
              │  Stress Tests              │
              │  (JESD22 – Axxx, Bxxx)     │  ★ 才到这里才选具体方法
              └────────────┬───────────────┘
                           ↓
        OUTPUTS 输出：Rel Procedure / Test Methods / Datasheet Parameters
                     可靠性程序 / 试验方法 / 数据手册参数
```

- 来源：https://www.psma.com/sites/default/files/uploads/tech-forums-semiconductor/presentations/is163-status-wide-bandgap-device-qualification-standards-effort-new-jedec-committee-jc70.pdf （JEDEC JC-70 官方演讲，含JESD94B 引入与流程图）｜可信度：★★★★☆

**JESD94B 的核心原则（多条二手源一致）** `[二手，★★★★☆]`：
1. **强调"基于知识"而非"固定应力"**：试验条件应随应用环境变化调整，**避免不真实的失效或漏检**
2. **适用所有应用特定的可靠性试验**；试验时长与条件取决于应用变量
3. **排除**某些表征型/通过失败型试验，如 ESD、latch-up、电过应力
4. 术语定义含**acceleration factor、usage conditions、field life、mini-cycle**
5. **usage conditions 覆盖从制造、运输、存储到运行的所有阶段**，是制定试验计划的基础
6. **应力不得超越材料物理极限**（玻璃化转变温度、延性、界面附着强度）—— 例如过高的 TC 温度会使材料脆化或分层，产生与现场不一致的失效
7. 温湿度试验的 AF 用 **Peck 模型**算铝腐蚀；**HAST 与压力锅可能导致封装材料过度劣化，须谨慎使用**
8. 试验时长应基于**失效模型 + AF + 目标失效率**确定
9. "For application specific qualifications, the power cycling setup should reflect the **actual product situation as close as possible**"
10. TC 的 AF 用 **Norris-Landzberg 修正模型**计算，考虑温变幅、循环频率、最高温度

- 来源：https://plusstd.com/7720055.html ｜https://core.ac.uk/download/552888767.pdf ｜https://www.psma.com/.../is163-...pdf ｜可信度：★★★★☆

### 3.1 七步翻译流程（可直接做成 CLI）

```
STEP 1  明确失效机理假设
   输入：产品的材料体系、层间结构、工艺（用户场景：陶瓷覆铜板 + 双焊片 + 键合线 + 真空灌胶）
   方法：JEP131（FMEA 框架）逐层分析
   工具：用户的 AIAG & VDA FMEA 2019 七步法 400+ 行
   输出：失效机理清单（每条含：位置、应力类型、预期失效模式、判据候选）
   
   IF 某失效机理在标准体系中没有对应试验
      → 记录为"标准未覆盖"，进入 STEP 7（内部规范）
      → 参考 AQG 324 原则："若某项试验不适用于特定设计，供应商必须向客户说明不适用的理由"

STEP 2  选应力类型（三选一或组合）
   热-机械（热循环类）：TC / TST / PC / IOL
   热-电（偏压寿命类）：HTRB / HTGB / HTFB / HTOL
   电-化学（湿热类）：THB(85/85) / H3TRB / H3TRB / AC(PCT)
   IF 机理涉及水汽+电场
      → 优先 H3TRB（不是 HAST）—— 依据 IEC 60749-4 原文"THB 结果优先于 HAST"

STEP 3  选标准方法编号
   优先级顺序（决策规则）：
   ① 客户 TS 明确指定的 → 用它（见 §4.2）
   ② 车规模块 → AQG 324（其引用表已锁定方法，无需自选）
   ③ 通用/工业 → JESD47（基线矩阵）+ IEC 60749 对应部分
   ④ 板级/组件 → 追加 JEP150
   IF 客户 TS 与标准栈都存在
      → 取严（见 §4.2），但**必须在报告中列出差异表**

STEP 4  从标准表格取条件
   IF TC → A104F.01 表1（条件）+ 表2（soak mode）+ 表3（循环频率）
      ⚠️ 循环次数 A104 不提供 → 跳到 STEP 6
   IF PC → AQG 324 QL-01/QL-02（ton, IL, Vgate, ΔTj, Tj,max）+ IEC 60749-34
   IF TBL → A108G（Ta 使 Tjmin ≥ 125 °C；偏压按器件类型；时长按采购文件）
   IF 湿热 → IEC 60749-5（85±2 °C / 85±5 %RH / 1000 h）或 A101D.01

STEP 5  ★ 按自己产品的 ΔTj / CTE / Tg 特性修正（最容易被跳过、也最容易翻车）
   修正项清单（逐条检查）：
   a) **Tg 检查**：A104 CAUTION 1 —— 试验的 Ts(max) 是否超过任一封装材料的 Tg？
      IF 超过（用户的 AMB/DPC 陶瓷 + 高温密封剂 + 环氧塑封料）
         → 必须做 DSC/TMA 测 Tg，并在报告中论证
         → IF 无Tga 数据 → 该条件不可用
   b) **Pb/Sn 检查**：A104 CAUTION 4 —— Ts(max) > 125 °C 不推荐用于 Pb/Sn
      IF 用户的工艺含 Pb/Sn（含铅焊料芯片贴装）
         → 选 Ts(max) ≤ 125 °C 的条件（B/G/K/L/R/N）
         → 或改用无铅/烧结工艺并做等效论证
   c) **ΔTj 修正**：标准条件的 ΔT 是**外部环境温差**，不是产品的 ΔTj
      → 需通过电热仿真把产品的 mission profile 转成结温时间序列
      → 详见 STEP 6
   d) **ramp rate 检查**：焊点/互连评估必须 ≤ 15 °C/min，优选 10–14 °C/min
      → 大热质量的功率模块 → 需单区箱体，否则加速因子在腔内不一致
   e) **soak mode 选择**：组件级 → mode 1（1 min）；焊点疲劳 → mode 2/3/4（5/10/15 min）
   f) **腔体负载**：热质量大的功率模块 → 表3 的循环频率需下调（mode 4 场景）

STEP 6  ★ 样本量与时长计算（标准不管，必须自己算）
   6a) 循环次数推导（TC）—— 见 §3.2
   6b) 时长外推（Arrhenius）—— 见 §3.3
   6c) 样本量与置信度—— 见 §1.5 公式 1-4
   输出三元组：(n, CL, R_L) 或 (n, t, CL)

STEP 7  判据定义
   来源优先级：
   ① 标准明确给出的（如 AQG 324 的 5%/20%）
   ② 采购文件/客户 TS 规定的（如 A104F.01 §7(d) "special acceptance criteria"）
   ③ 数据手册规格的隐含判据（器件规格的 drift 限值）
   IF 标准未给判据
      → 自定义判据，但必须：① 给出物理依据② 用基线数据分布定阈值
      → ⚠️ 参考：2019 版 VDA FMEA 的"预防措施/反应措施"设计原则
```

### 3.2 示例一：从 A104 条件表推导自己模块的循环次数

> **注意：这个推导是方法论示范，具体数值必须用用户自有数据重算。**

```
【输入】
  产品：IGBT 功率模块（陶瓷覆铜板 + 双焊片 + Al 键合线 + 真空灌胶高温密封剂）
  任务剖面（mission profile，来自客户整车/工业工况）
  材料参数（自有）：
    CTE: Al ≈ 17 ppm/°C[二手,sonacme]；Si ≈ 3 ppm/°C[二手,sonacme]；
         环氧塑封料 ≈ 8–20 ppm/°C（随填料含量）
    Tg: 环氧塑封料（需自行 DSC 测定）⚠️ 无自有数据 → 标为待补
    焊料（无铅 SnAg / 含铅 PbSn）：需明确
    陶瓷/铜 CTE 失配（DBC 的主要应力源）

【STEP 5 前置修正】
  IF Tg（环氧） < 150 °C
     → A104 条件 C(−65/+150)、H(−55/+150)、M(−40/+150) 对本产品不可用
        （因为 Ts(max)=150 °C 可能超过 Tg → 诱发非现场失效，A104 CAUTION 1）
     → 候选收窄为：B(−55/+125, ΔT=180) 或 G(−40/+125, ΔT=165)
  IF 芯片贴装用含铅焊料
     → 全部 Ts(max)=+150 条件不可用（CAUTION 4）
  IF 采用无铅/烧结
     → 可考虑 M(−40/+150, ΔT=190)，但需 Tg 论证
```

```
【STEP 6a】循环次数推导（两条路径，建议并行）

── 路径 A：Coffin-Manson 简化幂律（焊点/互连疲劳主导时）──
  Life = A · (ΔT_use)^B→  引入加速因子
  AF = (ΔT_test / ΔT_use)^B
  N_test = N_use / AF

  变量定义与单位：
  N_use  = 现场寿命对应的循环次数      [cycles]
  N_test = 试验应施加的循环次数        [cycles]
  ΔT_use = 现场每次循环的等效温变幅    [K]（★注意：应取结温摆幅 ΔTj，
          而非环境温差；这是最容易出错的地方）
  ΔT_test= 试验的等效温变幅            [K]
  B      = 温变指数（耗损机理指数）    [无量纲]
  A      = 寿命系数（由材料+几何决定）  [K^B·cycles]

  IF B 未知
     → 走路径 B（AF 由模型给出），或用多应力点拟合（正好呼应 AQG 324 QL-01
        要求的"至少两组温升、温升必须比小温升高出 40%"）

── 路径 B：Norris-Landzberg（含频率与最高温度修正）──
  N_lab / N_machine = (f_L / f_M)^(1/3) · (ΔT_M / ΔT_L)^2 · Φ(T_max)
  其中 Φ(T_max) = exp[ (Ea/k) · (1/T_L,max − 1/T_M,max) ]

  变量定义与单位：
  N_lab    = 实验室循环次数              [cycles]
  N_machine= 现场（机器）循环次数        [cycles]
  f_L      = 实验室循环频率              [cycles/h]（= A104 表3 的 Cycles/Hr.）
  f_M      = 现场循环频率                [cycles/h]（从 mission profile 提取）
  ΔT_L     = 实验室温变幅                [K]
  ΔT_M     = 现场温变幅                  [K]
  T_L,max  = 实验室最高绝对温度          [K]
  T_M,max  = 现场最高绝对温度            [K]
  Ea       = 失效过程活化能              [eV]
  k        = Boltzmann 常数= 8.617×10⁻⁵ [eV/K]
  Φ        = Arrhenius 高温修正因子      [无量纲]
  适用范围：锡铅焊互连热疲劳（★ 这是该模型的原始标定对象）
            ⚠️ 用于无铅焊/烧结层时 B=2 与 (1/3) 次频率项均需重新标定

── 路径 C（推荐，配合 AQG 324 做法）：多点实测拟合 ──
  选≥3 个 ΔT 条件（同ΔTj、不同 Tj,max，或不同 ton）
  每个条件做足量样本跑至失效
  拟合 LESIT 模型（见 §3.4），直接得到 Nf(ΔTj, Tj,max, ton)
  → 这是 AQG 324 QL-01/QL-02 的原生做法
```

**⚠️ 三个必须避开的陷阱（写在 SOP 里）** `[推断]`：

| 陷阱 | 后果 | 防御措施 |
|---|---|---|
| **用环境温差 ΔT 代替结温摆幅 ΔTj** | 对功率模块误差极大 —— 功率循环的 ΔTj（芯片处）远大于 ΔTc（壳处） | 做电热仿真，从 mission profile 得到结温时间序列，用 ΔTj 而非 ΔT_env |
| **直接用 A104 的表 1 ΔT 当作产品的 ΔT** | 表 1 的 ΔT 是**外部环境**温差，与产品内部实际承受的热-机械循环不是一回事 | 表 1 条件只决定"环境怎么变"；产品承受多少由 ΔTj 决定，需仿真 |
| **不检查 Tg 就用 +150 °C 条件** | 诱发现场不会发生的失效 → 试验"通过"但产品实际有风险；或"失效"但根因是过应力 | DSC 测 Tg，写进试验前检查表（Checklist） |

### 3.3 示例二：用 Arrhenius 把 1500 h 外推到 15 年

> **这是用户最常问的"外推"操作，也是最容易出错的操作。**

**公式 1：Arrhenius 加速因子** `[Track 04 §3.2 已核实]`

```
                E
AF(T) = exp [ —— ( 1/T_use − 1/T_stress ) ]
                k
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `E`（或 `E_a`） | 失效过程的活化能 Activation Energy | eV（或 J/mol）|
| `k` | Boltzmann 常数 = **8.617 × 10⁻⁵** | eV/K |
| `T_use` | 使用（现场）绝对温度 | **K** |
| `T_stress` | 应力（试验）绝对温度 | **K** |
| `AF` | 加速因子 = 现场寿命 / 加速寿命（>1） | 无量纲 |

**等价写法（文献更常见）**：
```
L(T) = L₀ · exp[ (E / k) · (1/T_use − 1/T_stress) ]
```
| 符号 | 含义 | 单位 |
|---|---|---|
| `L(T)` | 在温度 T 下的寿命 | h |
| `L₀` | 比例常数 | h |

**公式 2：把试验时长外推为现场寿命**
```
L_use = AF · t_test
```
| 符号 | 含义 | 单位 |
|---|---|---|
| `L_use` | 等效现场寿命 | h |
| `t_test` | 实际试验时长 | h |

**公式 3：求"达到目标现场寿命所需的试验时长"**
```
                E      ( 1        1    )
t_test = L_use · exp[ −── ( ───── − ───── ) ]
                k      T_use     T_stress
```

**公式 4：多次读点的合并外推（用户 3 档试验的正确用法）**

用户数据：168 H × 74 pcs（PASS）、1000 H × 23 pcs（PASS）、1500 H × 6 pcs（PASS）

**若三项均为零失效**，可用 **Kruskal-Wallis 型累积暴露量** 或更严格的 **chi-square 零失效合并**：

```
累积失效时间（累积暴露量）：
S = Σᵢ nᵢ · tᵢ = 74×168 + 23×1000 + 6×1500
  = 12,432 + 23,000 + 9,000
  = 44,432  [pcs·h]

零失效下的失效率上界（卡方法）：
λ_use = χ²(1−CL, 2r+2) / (2 · S · AF)      [r = 0]

  CL = 60%：χ²(0.40, 2) = 1.833
    → λ_use = 1.833 / (2 × 44,432 × AF)
  CL = 90%：χ²(0.10, 2) = 4.605
    → λ_use = 4.605 / (2 × 44,432 × AF)
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `S` | 累积暴露量 Σnᵢtᵢ | pcs·h |
| `nᵢ` | 第 i 档样本数 | pcs |
| `tᵢ` | 第 i 档试验时长 | h |
| `r` | 观察失效数（此处 = 0） | 件 |
| `CL` | 置信水平 | 无量纲 |
| `λ_use` | 现场失效率上界 | 1/h（或换算为 FIT）|
| `AF` | 总加速因子 | 无量纲 |

**FIT 换算**：`1 FIT = 1 failure / 10⁹ device-hours`
```
FIT_use = λ_use × 10⁹
```

> `[推断]` **这是用户这三档数据唯一严谨的使用方式。** 单独用 1500H × 6pcs 宣称"通过"是统计上无意义的（6 件样本的 90% 置信下界极低）。合并后 S = 44,432 pcs·h 是一个有意义的暴露量。**建议在报告中以合并形式呈现，而非三档分别"PASS"。**

**Ea 取值：范围与依据** `[Track 04 §3.2 已核实，本次复核]`：

| 失效机理 | Ea 数量级 | 来源与依据 |
|---|---|---|
| 半导体器件通用 | **≈ 0.7 eV** | 二手多源 |
| 湿度相关 | **≈ 0.9 eV** | 二手多源 |
| 通用电子元件 | 0.3–1.2 eV，常用默认 **0.67 eV** | 二手 |
| 铝互连电迁移：晶界扩散 | 0.5–0.6 eV | 二手 |
| 铝互连电迁移：晶内扩散 | ≈ 1 eV | 二手 |
| Coffin-Manson 拟合报道范围 | 0.12–0.58 eV（ACS Omega 2025 实测 0.38 eV） | 同行评审 |
| 铝腐蚀（含氯化物，Peck） | 0.7–0.8 eV | 二手（MDPI 综述）|
| 热机械应力（T₀−T 模型） | 0.5–0.6 eV（晶界扩散）/ ≈1 eV（晶内扩散）| 二手（MDPI 综述）|

- 来源：https://www.antpedia.com/standard/1016730953-10.html ｜https://pubs.acs.org/doi/10.1021/acsomega.5c06959 ｜https://www.mdpi.com/2072-666X/15/3/398 ｜可信度：★★★☆☆
- 🔴 **关键警告（Track 04 已指出，此处强化）**：**Ea 不是材料常数，而是"失效机理 + 温度区间"的拟合参数。** 所有上述数值**必须用自有数据重新标定**，直接套用是外推失效的头号原因。

**T-stress 变体（适用于"先高温老化、再低温使用"场景）** `[未核实]`：
```
AF = exp[ (E / k) · (1/T_use − 1/T_stress) − (E / k) · ln(T_stress_real / T_stress) ]
```
⚠️ **Track 04 已标注：形式随文献而异，未找到权威统一表述。本track 同样未能核实，标为未核实，不写入知识 OS 正典区。**

**Arrhenius 的适用边界（必须写进 SOP 的四条）** `[Track 04 §3.2]`：
1. **单一失效机理主导** —— 加速前后是同一物理机制
2. **Ea 在应力范围内恒定** —— 跨区间需重新拟合
3. **Ea > 0** —— 但表面扩散/电迁移主导时 **Ea 可为负**
4. **温度必须用 Kelvin**

### 3.4 AQG 324 功率循环寿命模型（引用 Track 04 已核实结论 + 本track 复核）

**LESIT 基础模型** `[一手，AQG 324 04.1/2025 附录 II.D p.11 公式 6]`：
```
                                     E_a
N_f = A · f^a · ΔT_j^b2 · exp( ─────────────── )
                                  k_B · T_j,mean
```

| 符号 | 含义 | 单位 |
|---|---|---|
| `N_f` | 平均失效循环数 | cycles |
| `A` | 比例常数 | 依模型量纲 |
| `f` | 循环频率 | cycles/h（或 Hz，依标定）|
| `a` | 频率指数 | 无量纲 |
| `ΔT_j` | 结温摆幅（结温摆幅）| **K** |
| `b2` | 温变指数（原文排版为 b2）| 无量纲 |
| `E_a` | 活化能 | eV |
| `k_B` | Boltzmann 常数 = 8.617×10⁻⁵ | eV/K |
| `T_j,mean` | **平均**结温（不是峰值）| **K** |

- 原文标注："derived from test data … developed in the **LESIT project**"
- 原文引用 [12]：K. Mainka, M. Thoben, O. Schilling, "Lifetime calculation for power modules, application and theory of models and counting methods", **EPE, Birmingham, 2011**
- 来源：AQG 324 04.1/2025 附录 II.D p.11｜可信度：★★★★★（Track 04 已下载全文核实）

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

| 符号 | 含义 | 单位 |
|---|---|---|
| `K` | 常数 | 依模型量纲 |
| `ΔT_j` | 结温摆幅 | K |
| `b1` | 温变指数 | 无量纲 |
| `T_j` | 结温 | K |
| `C` | 模型常数（Arrhenius 积分中的参考常数）| 依模型 |
| `t_on` | **通电导通时间** | s |
| `I` | 电流 | A |
| `V` | 电压 | V |
| `D` | **键合线直径** | mm（或 m，依标定）|
| `b2…b6`, `γ` | 各指数/参数 | 无量纲 |

- 原文引用 [16]：R. Bayerer et al, "Model for Power Cycling lifetime of IGBT Modules — various factors influencing lifetime", **5th International Conference on Integrated Power Electronics Systems, Nuremberg, 2008**
- 可信度：★★★★★

**烧结芯片扩展** `[一手]`：U. Scheuermann, R. Schmidt, "A New Lifetime Model for Advanced Power Modules with **Sintered Chips** and Optimized Al Wire Bonds", **PCIM, Nuremberg, 2013**
- `[推断]` **这一篇对用户直接相关** —— 若用户采用烧结银/烧结铜芯片贴装，必须用此模型重新标定

**雨流计数 + 消耗累加（AQG 324 的任务谱处理方法）** `[一手，附录 II.D]`：
```
1. 对 mission profile 做 Rainflow 循环计数（提取 ΔT 分布）
   → 计数方法标准：ASTM D1049-85（AQG 324 参考文献 [13]）
2. 提取的热应力直方图（cycles-to-failure/ΔT histogram）代入寿命曲线
3. 累加每段 ΔT 的寿命消耗 → 单一等效应力值
```

**概率约定（实务关键）** `[一手，附录 II.D]`：
- 寿命曲线须代表**定义的生存概率，如 95%**
- **"100% 寿命消耗 = 5% 部件达到 EOL 判据"** —— 即寿命曲线本身已含 5% 分位含义
- IGBT / Diode / Solder **可各有不同曲线**

**参数敏感性（罕见的一手量化数据）** `[一手，附录 II.D p.12]`：
- 模拟 75 min 驾驶谱，改变应用/模块参数各 10%：
  - **Rth 降低 10% → 寿命增加约 40%**
  - 导通损耗或逆变器电流变化有类似影响
- **"Applying large safety margins in the range of 20% will reduce the power density and double the lifetime."**（留 20% 安全裕度会降低功率密度并使寿命翻倍）
- **原文明示的局限**：
  > "With the number of samples defined in the AQG 324, the definition of a higher probability is **not reasonable and will not result in a better prediction of the lifetime**."
- 任务谱应代表**典型而非最坏**驾驶谱

> 🔑 **对用户的三条硬性启示**：
> 1. **AQG 324 明确说：用它规定的样本量去定义更高生存概率是无意义的。** 想要更高置信度，只能加样本量或加应力点。
> 2. **Rth 是寿命的强杠杆**（降 10% → 寿命 +40%），比"降 Vce"更有效。这与 §2.3.7 中"热阻测量不可靠"形成张力 —— **建议在报告中同时呈现"电学判据 + 热学判据"，并用结构函数补充定位。**
> 3. **留 20% 裕度 = 寿命翻倍**，这是与客户谈判寿命指标时的有力论据。

**Peck 模型（温湿度 + 电压）** `[二手，见 §2.2.3 完整公式与变量定义]`

**Coffin-Manson 家族（含完整变量定义）** `[Track 04 §3.4 已核实]`：
```
基础形式：      N_f = C · (Δγ · ε_f)^(1/m)
含频率修正(Shi)：[ N_f · v^(k−1) ]^m · Δε_p = C
Morrow（能量法）： N_f^m · W_p = C
```
| 符号 | 含义 | 单位 |
|---|---|---|
| `N_f` | 失效循环数 | cycles |
| `Δγ` | 非弹性应变幅；`Δγ = F/(L·d) + h·Δα·ΔT` | 无量纲 |
| `ε_f` | 剪切方向疲劳延性系数（**焊料典型值 0.325**）| 无量纲 |
| `C` | 疲劳强度系数（★ 各模型中 C 含义不同，见下）| 依模型 |
| `m` | 疲劳指数 | 无量纲 |
| `v` | 频率 | Hz |
| `k` | 频率指数 | 无量纲 |
| `W_p` | 稳态循环的塑性应变能 | J/m³（或依模型）|
| `h` | 焊点高度 | m |
| `Δα` | CTE 失配 | 1/K |
| `ΔT` | 温度摆幅 | K |
| `F`, `L`, `d` | 力、长度、位移 | N, m, m |

- ⚠️ **符号冲突警告（Track 04 已指出，必须内建）**：**Morrow 的 `C` 是能量量纲，CM 的 `C` 是温度/应变量纲**，但 MDPI 综述表格中两者共用 `C`。**知识 OS 必须为每个模型建立独立符号命名空间。**
- ⚠️ **MDPI 综述的排版错误已判定**：`exp(Ea/kT)` 应为 `exp(Ea/(k·T))`

**符号命名空间方案（建议知识 OS 采用）**：
| 模型 | 建议前缀 |
|---|---|
| Arrhenius | `AF_ARR_` |
| Peck | `AF_PECK_` |
| Coffin-Manson | `NF_CM_` |
| Morrow | `NF_MOR_` |
| LESIT | `NF_LESIT_` |
| Bayerer | `NF_BAY_` |
| Norris-Landzberg | `AF_NL_` |
| Rainflow 累加 | `DAMAGE_RF_` |

### 3.5 常见陷阱清单（可直接做 CLI 的 `--warn` 输出）

| # | 陷阱 | 后果 | 检测方法 | 依据 |
|---|---|---|---|---|
| T1 | **照抄标准条件不做产品适配** | ΔTj 不同 → 失效机理不同 → 试验结论无效 | 检查表：Tg / Pb-Sn / ramp rate / ΔTj 四项 | A104 CAUTION 1&4 `[一手]` |
| T2 | **用环境 ΔT 代替 ΔTj** | 功率模块误差极大 | 电热仿真出结温序列 | §3.2 陷阱表 `[推断]` |
| T3 | **样本量不足导致结论不可信** | 6 pcs 声称"通过"无统计意义 | 报告 (n, CL, R_L) 三元组 | §1.5 公式自算 `[推断]` |
| T4 | **把加速试验当等效现场条件** | 过度承诺寿命 | AF 计算 + 机理同一性检查 | Track 04 §3.10 IEC 62506 警告 |
| T5 | **加速引入新失效机理** | 外推失效 | 检查是否超材料物理极限 | JESD94原则 6 `[二手]` |
| T6 | **零失效数据做 Weibull 拟合** | 统计错误 | 零失效时改用二项式/卡方 | §1.5 Weibull 前提 `[二手]` |
| T7 | **用 A104 的表 1 ΔT 当产品 ΔT** | 同 T2 | 表1 只决定环境 | §3.2 `[推断]` |
| T8 | **ramp rate 失控造成热冲击** | 产生不真实损伤 | ≤15 °C/min，优选 10–14 | A104 §5.7.2 NOTE 3 `[一手]` |
| T9 | **中断次数 >10% 未察觉** | 试验须从头重启 | 记录每次中断事由与次数 | A104 §5 `[一手]` |
| T10 | **用闭环恒 ΔTj 做寿命外推** | **高估能力约 3.2 倍** | 改用恒定 on-time + 恒定负载电流 | A122 §4.2 转述 `[二手]` |
| T11 | **设备故障导致的中断未计入 10%** | 试验有效性受损 | 中断台账含设备故障 | A104 §5 `[一手]` |
| T12 | **H3TRB 忽略自加热导致 RH 下降** | 掩盖失效 | 实时监测腔内 RH | Power Electronics News `[二手]` |
| T13 | **判据来源未标注** | 审核时无法追溯 | 报告标注判据出处（标准/客户/自定义） | A104F.01 §7(d) `[一手]` |
| T14 | **A108G 用了低偏压但未报告实际电压** | 不符合 A108G 4.2.2 | 报告写明实际偏压 | A108G 变更说明 `[二手]` |
| T15 | **用大芯片 TS 结果覆盖小芯片** | 漏检（DBC 场景反向） | 分尺寸建模 | §2.3.6 DBC 知识 `[二手]` |
| T16 | **抽样方案跨版本混用**（GB/T 2828.1-2012 与 ISO 2859-1:2026）| Ac/Re 不可比| 合同写死版本号 | §1.5 `[二手]` |

---

## 4. 标准选用决策流程

### 4.0 应用等级 → 标准栈映射

```
【汽车（乘用车 PCU）】
  芯片/单管层：AEC-Q101 Rev E（IGBT/MOSFET/SiC）
  模块层：AQG 324 04.1/2025（主）+ IEC 60747/60749/60068/60664（方法学）
  体系层：IATF 16949 + ISO/IEC 17025（实验室能力）
  组装态：JEP150（若焊到 PWB）
  ★ 关键温区：+175 °C（Wolfspeed SiC HTRB/HTGB 用Ta=175 °C）[一手]
  ★ 关键时长：1000 h 为主（HTRB/HTGB/H3TRB 各 1000 h）[一手]
  ★ 关键应力：HTRB 80% Vds；HTGB ±Vgs 双分支；H3TRB Si 80 V / SiC 80% Vds
  ★ 特殊项：HV-H3TRB（比H3TRB 更严，SiC 器件的关键资格试验）

【工业 / 能源 / 轨交】
  基线：IEC 60749 系列（34功率循环 / 5 稳态湿热 / 6 高温存储 / 23 高温工作寿命 / 25 温度循环）
  功率循环方法学：IEC 60749-34
  参考对标：AQG 324（工业界普遍对标车规做设计目标）
  振动/冲击：IEC 60068-2-6 (Fc) / -2-27 (Ea) / -2-64 (Fh)
  ★ 注意：AQG 324 的适用对象是 PCU 中≤3.5 t 机动车的功率电子模块，
          但 AQG 324 自己声明"An electrical/railway working group"平行存在
          （ECPE 另有 "Power Semiconductor Reliability for Railway Application" 工作组）

【消费电子】
  基线：JESD47（IC）或JESD22 对应部分（分立）
  抽样：ISO 2859-1 / GB/T 2828.1（来料与出货，AQL 体系）
  ★ 温区较窄（如条件 J: 0/+100 °C）
  ★ 大量使用板级试验（JEP150 / B111 跌落 / B113 循环弯曲）

【军用 / 航天】
  微电路：MIL-STD-883（K/L 版Part 1；1000/2000/3000/5000 四段式方法号）
  中国对应：GJB 548（★ 与MIL-STD-883 是平行体系，非简单叠加 —— Track 04 已核实）
  环境：MIL-STD-810（整机层）
  特殊：航天需考虑辐射（总剂量/SEE），见 GB/T 4937 第17/18 部分、IEC 60749-17/-18
```

> ⚠️ **关于"车规最严"的量化对比** `[推断，基于一手条件数据]`：
> | 维度 | 消费 | 工业 | 车规（Si 基）| 车规（SiC）|
> |---|---|---|---|---|
> | HTRB 温度 | 125 °C | 150 °C | Tj,max | **175 °C** |
> | HTRB 时长 | 1000 h | 1000 h | 1000 h | 1000 h |
> | HTRB 电压 | 无严格 | 部分 | 80% Vds | 80% Vds |
> | HTGB | 无 | 125 °C | Tj,max，双分支 | Tj,max 双分支 + DGS |
> | H3TRB 电压 | 不做 | 部分 | 80 V | **80% VDS(max)** |
> | 附加项 | — | — | IOL/PTC | DGS/DRB/dyn.H3TRB/HTFB |
>
> **注意"车规最严"的表述需要修正** `[推断]`：车规并非在所有维度都更严 —— 例如某些消费/航天应用要求更宽温区或更高等级 HTSL。**准确表述是"车规在寿命时长、偏压完整度（双分支 HTGB）、以及电压覆盖（H3TRB 从固定 80 V 升到额定值 80%）三方面最严"。**

### 4.1 决策树

```
STEP 1  产品类型是什么？
   ├─ 芯片/IC → JESD47 + AEC-Q100（车用）
   ├─ 分立器件 → JESD22 + AEC-Q101（车用）
   ├─ 功率模块 → IEC 60749 + AQG 324（车用）★ 用户场景
   └─ 被动元件 → IEC 60068 + AEC-Q200（车用）

STEP 2  应用等级是什么？（见 §4.0）

STEP 3  是否有客户企业规范（TS-xxxx）？
   ├─ 有 → 进入 §4.2 冲突处理
   └─ 无 → 纯标准栈

STEP 4  是否有标准未覆盖的工艺？
   ├─ 有 → 进入 §4.4 内部规范
   └─ 无 → 纯标准执行

STEP 5  报告必须声明三件事：
   ① 每项试验的依据（标准号 + 版本 + 条款号）
   ② 每项判据的出处
   ③ 每个偏离标准的地方及其技术论证
```

### 4.2 客户 TS 与标准的冲突处理：取严原则

**核心规则（业界通行的"取严"原则）** `[推断，标准体系逻辑]`：

```
IF 客户 TS 要求严于通用标准 → 执行 TS
   理由：合同优先。TS 通常反映该客户应用场景的真实风险
   报告：注明"依据 <客户> TS-xxxx 条款 X.X，高于 AQG 324 QL-01 的 XXX 要求"

IF 客户 TS 要求宽于通用标准
   → ⚠️ 不得直接放宽。必须书面澄清后取严
   理由 [推断]：
     ① 客户 TS 通常是"底线"而非"上限"，其宽于标准可能是笔误或基于旧版标准
     ② 车规领域 IATF 16949 与 AQG 324 的体系逻辑不允许以TS 降低通用底线
     ③ 放宽会失去"标准符合性"这一可对外主张的资质

IF 客户 TS 与标准冲突且客户坚持放宽
   → 走"偏离（deviation）"流程：
     ① 书面记录偏离项
     ② 给出技术论证（为什么不按标准也能满足应用要求）
     ③ 取得客户书面批准（邮件即可，需归档）
     ④ 在资格报告中列入"deviations"章节
   → `[推断]` 这套流程与 ISO 9001 的"不符合项/让步接收"逻辑一致
```

**⚠️ 用户任务书的一处需要修正** `[推断]`：任务书说"通常是企业规范更严，取严原则"。
**核实后的更准确表述**：**取严不是自动的**。取严是"在未获书面偏离批准前的默认行为"；若客户坚持放宽并书面批准，则该偏离成立，但**必须在报告中显式列出**。这一区分很重要——它把"取严"从技术偏好变成流程控制。

### 4.3 从 TS 的引用列表反推客户关注哪些可靠性风险点（★ 高价值技巧）

> **这是本track 最有方法论价值的一节。**

```
【核心技巧】客户 TS 的"引用标准列表"就是客户的风险地图。

STEP 1  拿到 TS 的 normative references / 引用标准清单
STEP 2  按 §5 的应力类型分类（热-机械/ 热-电 / 电-化学 / 机械 / 物性）
STEP 3  统计各类占比
STEP 4  读出客户的关注点

【示例解读框架】
IF TS 密集引用 IEC 60749-34（功率循环）+ JEP122（失效模型）+ AQG 324
   → 客户关注【焊点/键合线疲劳】
   → 我方应对：PCsec + PCmin 都要做，且必须做多点寿命模型（呼应 §3.4 路径C）
   → 谈判重点：ΔTj 定义、ton 定义、失效判据的 5%/20%

IF TS 密集引用 IEC 60749-5（85/85 THB）+ J-STD-020（MSL）+ JESD22-A101
   → 客户关注【湿气进入与腐蚀】
   → 我方应对：THB 必做；注意 IEC 60749-4 原文"THB 结果优先于 HAST"（做了 HAST 不做 THB 会被质疑）
   → 谈判重点：偏压配置（连续 vs 1h/1h 循环）、测量窗口 48h vs 168h

IF TS 引用 IEC 60747-15（功率半导体测量：热阻/杂散感测）
   → 客户关注【测量方法学本身的可靠性】
   → 我方应对：热阻测量方法必须在报告里写清楚（AQG 324 QL 用它）
   → 谈判重点：Rth 定义（Rthjc/Rthjs/Rthjf）、测量方法、双面散热如何处理（见 §2.3.7）

IF TS 引用 IATF 16949 + ISO/IEC 17025
   → 客户关注【实验室能力与过程控制】
   → 我方应对：确保实验室资质有效；报告须符合 17025 的报告要求

IF TS 引用 UNECE R10 / RoHS / ELV
   → 客户关注【整车法规合规】（★ 注意：AQG 324 本身零引用这些 —— Track 04 已核实）
   → 我方应对：EMC/有害物质合规是与可靠性正交的另一条线，不要混入 AQG 324 报告

IF TS 引用 MIL-STD-883 或 GJB 548
   → 客户关注【军规级微电路】→ 可能是特殊行业（航空/国防），
     ★ 注意此路径下应走 GJB 548 / MIL-STD-883 体系，不是 AQG 324
```

**为什么这个技巧有效** `[推断]`：客户写 TS 时，**引用哪些标准 = 他们内部失效分析历史经验的沉淀**。一个引用 IEC 60749-34（功率循环）的客户，一定是因为吃过焊点开裂的苦；一个引用 A104（温循）而不引 A122（功率循环）的客户，其应用大概率是环境温度变化远大于内部发热。

### 4.4 内部规范的产生场景（标准未覆盖时）

**AQG 324 自己就写明了这条原则** `[一手]`：
> 关键原则：若某项试验不适用于特定设计，**供应商必须向客户说明不适用的理由**（"to be agreed with the customer" 贯穿全文）
（Track 04 §1.4 一手核实）

**JESD47 明确授权偏离** `[一手]`：
> "If it is known or suspected that failures either are due to new mechanisms or are uniquely induced by the severity of the test conditions, then **the application of the test condition as stated is not recommended**. Alternatively, new mechanisms or uniquely problematic stress levels should be addressed by **building an understanding of the mechanism and its behavior with respect to accelerated stress conditions** (Ref. JESD91 … and JESD94)."
> 考虑 PWB 组装级效应 → 参考 JEP150

**用户实际遇到的三个内部规范场景** `[推断，基于用户项目描述]`：

| # | 场景 | 为什么标准未覆盖 | 内部规范应包含什么 |
|---|---|---|---|
| 1 | **双焊片 + 高温密封剂工艺** | 标准里的封装是"单焊片/标准焊料"体系；用户改动了芯片贴装拓扑与灌封材料 → 引入了标准未表征的新失效模式 | ① 改动机理分析（为何能提升 PC 寿命）② 对应的验证方案（PCsec/PCmin 的应力点、ΔTj 范围）③ 新的失效判据（若 5%/20% 不再适用） ④ 与 A104 CAUTION 4 的关系论证 |
| 2 | **SN 编码追溯要求** | 标准的追溯要求止于"批次/样品级"；用户需要**单件级**追溯 | ① 编码规则（与 IATF 16949 8.5.2.1e 呼应）② 编码载体与打印工艺 ③ 读回验证规则（关键：编码必须在可靠性试验全过程中耐受环境应力） ④ 与 FA 报告的关联字段 |
| 3 | **材料供应商定制规格（DBC/AMB/DPC）** | 陶瓷覆铜板的 CTE、铜层厚度、氧化层/金属化方案是供应商私有 | ① 来料规格（含关键 CTE/导热/强度参数）② 验收试验方法与判据（引用 A104/自建）③ 供应商变更控制要求 |

**内部规范的产生条件（IF-THEN）** `[推断]`：
```
IF 标准方法存在，但条件不覆盖你的材料/结构
   → 建"内部规范"：引用标准方法号 + 写明偏离部分与论证
   → 格式建议：STD-XXX-QP-YYY（企业标准-质量程序-试验）

IF 标准方法不存在（无对应应力类型）
   → 建"内部方法"：需自证方法学有效性（等效性论证）
   → 客户需书面认可

IF 标准明确说"不适用"（如 A104 对 WLCSP 的板级 TC）
   → 走JEP150（A104 原文指向）

IF 是测量方法而非试验方法（如 Rth 测量的具体实现）
   → 参考 IEC 60747-15（AQG 324 用它做热阻/杂散感测的方法学母标准）
```

**内部规范与 IATF 16949 的关系** `[一手，IATF 16949:2016 条款]`：
- **7.5.3.1**（标识与可追溯性）：IATF 8.5.2.1 要求"**Develop and document traceability plans — Based on the levels of risk or failure severity**"
- 即**追溯深度要按风险分级**，不是一刀切 → 内部规范应写明"哪些产品/工序需要单件追溯"
- 来源：https://www.pqbweb.eu/page-iatf-16949-version-2016-requirements-automotive-quality-management-system.php ｜可信度：★★★★☆

---

## 5. 标准演进与版本变更的应对流程

### 5.1 版本变更的追踪方法

**JEDEC 自身的版本号机制** `[一手，A104F.01 标题页与附录 B]`：
- A104F.01 标题页：`(Revision of JESD22-A104F, November 2020)` / `APRIL 2023`
- 附录 B.1："The differences between JESD22-A104F.01 and JESD22-A104F (Nov 2020) are **editorial only**: A superfluous Watermark on the NOTICE page was removed, and the JEDEC logo was replaced (with copyright)."
- 来源：https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf ｜可信度：★★★★★

> 🔑 **A104F → F.01 是纯编辑性变更**（仅去水印+换 logo）。**这是最好的一种升版情形：不影响技术内容，试验报告无需改动。**
> **但报告里应写"F.01（2023-04）"而不是"F"，因为 A104F.01 与 A104F 在引用上是两个不同的编号。**

**变更类型的分级（工程影响判定）** `[推断，据 A104 各版本附录 B 的实际形态]`：

| 变更类型 | 判据 | 对在用试验的影响 | 应对动作 |
|---|---|---|---|
| **T1 编辑性（editorial only）** | 附录 B 明确声明仅排版/水印/logo 变化 | **无影响** | 记录版本号即可，报告格式不改 |
| **T2 新增条款（new clause）** | 附录 B 列出新增条款号 + 描述 | 需读新增条款 | 评估是否与现有方案冲突 |
| **T3 表格变更（table revision）** | 附录 B 提到 Revise Table X | **需逐行比对** | ★ 用 diff 逐行比对新旧表，更新内部规范 |
| **T4 方法学澄清（clarification）** | Scope/术语变化 | 可能改变试验边界 | 评估现有样品是否仍适用 |
| **T5 废止（rescinded/withdrawn）** | 官方标Withdrawn/Rescinded | **停止使用，评估在用试验** | 见 §5.2 |

**A104 版本演进的实证（作为"如何读附录 B"的示范）** `[一手]`：

| 版本对 | 附录 B 列出的变更 |
|---|---|
| F.01 ← F (Nov 2020) | **仅编辑性**：移除 NOTICE 页多余水印；替换 JEDEC logo（含版权） |
| F ← E (Oct 2014) | §1 Scope 澄清为"**仅气态介质中的热循环**"；§5.7.1 将原 5.7.2 的Note 3 移入本节 |
| E ← D (Mar 2009) | §3 术语：新增 **JESD94 引用**、**IPC-SM-785 引用**<br>§5.2 修订表 1：新增 2 个温循剖面（**TCR、TCT**）、修订上下容差列、新增试验条件选择注意事项、新增引**JESD47** 参考<br>§5.6 修订表 3：为 TCR/TCT 增加 soak 建议<br>§5.7.2 修订表 4：为 TCR/TCT 增加焊点互连建议 |

- 来源：A104F.01 附录 B.1/B.2/B.3，同上 URL ｜可信度：★★★★★

> 🔑 **A104 的版本演进史本身就是一部"标准如何吸收 JEDEC 内部方法论"的历史**：
> - E←D 时加入 **JESD94 引用**（知识化测试方法论）
> - F←E 时**Scope 收窄为"仅气态介质"**（把液体的热冲击明确排除）
> - F 版的 §5.2 明确写"**Thermal cycling profiles commonly used for device qualification are referenced in JESD47**; yet, any other profile listed in this document (or custom profiles) may be utilized **in accordance with JESD94**"
> → **这确认了 §1.2/§3 的核心论点：JESD22-A104 是方法库，JESD47/JESD94 才是资格判定者。**

**版本追踪的 SOP** `[推断]`：
```
STEP 1  建立"标准台账"（每份在用标准一行）
   字段：标准号 | 当前版 | 发布日期 | 我方引用位置 | 上次核对日期 | 下一层级依赖
STEP 2  订阅 JEDEC/IEC/ECPE 的发布渠道
   - JEDEC：https://www.jedec.org/standards-documents（注册后可免费下载，按 facet 过滤）
   - IEC：https://webstore.iec.ch/ 或 https://www.iec.ch/dyn/www/f?p=103:22（按 TC）
   - ECPE：https://www.ecpe.org/research/working-groups/automotive-aqg-324/
   - IPC：https://www.ipc.org/4.0_Knowledge/4.1_Standards/SimplifiedSpecTree.pdf
STEP 3  收到升版通知 → 读附录 B（变更清单）→ 按 §5.1 分级判定
STEP 4  T3/T4/T5 → 触发内部规范变更（走 IATF 16949 变更控制，见 §5.3）
STEP 5  评估在用试验：
   - 已在进行中的试验：是否需重启？（参考 A104 的 10% 中断规则类推）
   - 已完成的试验：是否需补做？
   IF 变更仅影响未开始的项目
      → 直接用新版，记录变更点
   IF 变更影响进行中/已完成项目
      → 走"偏离/变更"流程，与客户确认
```

### 5.2 已废止/被取代方法的追踪（★ 用户特别问到）

**已确认的废止/取代链** `[二手/一手混合]`：

| 原方法 | 状态 | 被取代者| 取代关系 | 可信度 |
|---|---|---|---|---|
| **JESD22-B102E**（Solderability 可焊性） | **Withdrawn，撤废日期 2014-01-01** | **J-STD-002D** | JEDEC 官方页面确认；NSAI 标准商店明确"Withdrawn date 01-01-2014, Superseded by IPC J STD 002 : D" | ★★★★★（双源） |
| **JESD22-C101F**（ESD CDM） | **Rescinded 2020-02** | **JS-002-2018** | NASA EEE Parts Bulletin 一手；JEDEC 新闻稿确认 | ★★★★★ |
| **JESD22-A114F**（ESD HBM） | 被取代 | **JS-001**（现行 **JS-001-2017**；2024-10 有新版 JS-001-2024） | NASA EEE Parts Bulletin 一手 | ★★★★★ |
| **JESD22-A115C**（ESD MM 机器模型） | **Inactive as of 2016-09** | 无（JS-002 是 CDM 非 MM） | NASA EEE Parts Bulletin：MM 已inactive；"**JESD22-A115C is a reference document and should not be used as a requirement for IC ESD qualification**" | ★★★★★ |
| **JESD22-A112A**（塑封SMD水汽诱发应力敏感性，1995-11） | **被替代** | **J-STD-020**（MSL 分级） | 二手版本表 | ★★★☆☆ |
| **JESD22-B104C**（机械冲击，2004-11） | **被取代** | **JESD22-B110B**（2013-07） | 二手版本表 | ★★★☆☆ |
| **JESD22-C100**（高温连续性） | **已废止** | — | 二手版本表 | ★★★☆☆ |
| **JESD22-A108F**（2017） | 被取代 | **A108G**（2022-11） | 多源一致 | ★★★★☆ |
| **JESD22-A104F**（2020-11） | 被取代 | **A104F.01**（2023-04，编辑性） | 一手 PDF | ★★★★★ |
| **JESD22-A105 / A122** 等 | 现行 | — | — | ★★★★☆ |
| **MIL-STD-105E** | **Withdrawn 1995** | 后继 **ANSI/ASQ Z1.4** | 二手 | ★★★☆☆ |

- 来源：https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/EEE-Parts-Bltn-2021-Vol-13-No1-ESD-Testing-Standards-GaN-Devices-CL22-0048.pdf （NASA 一手技术通报，★★★★★）｜https://www.jedec.org/node/5911 （JEDEC 新闻稿，★★★★★）｜https://shop.standards.ie/en-ie/standards/jedec-jesd22-b102e-2007-1304391 （标准商店，★★★★★）｜https://www.jedec.org/node/8494 （JEDEC 页面，★★★★★）

**⚠️ 纠正任务书的一处表述**：任务书写"JESD22-B102/B104/A112/A114/C101 已废止"。
**核实结果**：这五个的**状态各不相同，不能一概而论**：
- B102（withdrawn 2014）、C101（rescinded 2020）、A115（inactive 2016）→ **确实已失效**
- A114（被 JS-001 取代）、B104（被 B110 取代）、A112（被 J-STD-020 取代）→ **被取代，但文档本身可能仍可获取**
- **"被取代"与"废止"在流程上的处理不同**（见下）

**废止对在用试验的影响判定（IF-THEN）** `[推断]`：
```
IF 方法被"Rescinded/Withdrawn"（正式失效）
   → ⛔ 不得在新项目中引用
   → 检查在用项目：是否有正在进行/已完成的试验仅依据此方法
      → 是 → 走偏离流程，切换到后继方法，或与客户确认数据是否仍有效
      → 特别关注"后继方法的条件可能更严"的情况
         （如 C101→JS-002：JS-002 的目的是"移除混乱与重复"，通常不是加严）

IF 方法被"Superseded"（被取代但仍可获取）
   → ⚠️ 可继续用于已签署合同的项目，但
   → 新项目应采用后继方法
   → 报告中同时标注两者（便于历史数据可追溯）

IF 方法被"Inactive"（停止使用但保留为参考）
   → ❌ 不得作为资格要求
   → NASA 原文措辞可作SOP 依据："should not be used as a requirement for IC ESD qualification"
```

**⭐ 一个重要的体系性观察** `[推断]`：**ESD 标准的迁移（883/A114/A115/C101 → JS-001/JS-002）说明 JEDEC 在做"方法归并"** —— 把分散在多个 JESD22 方法中的同类试验合并为 JEDEC-ESDA 联合标准。**这带来一个实际影响：JESD22 的方法号不再覆盖所有 JEDEC 测试方法**，知识 OS 必须把 JS-001/JS-002/J-STD-002/J-STD-020 纳入方法族，否则"从JESD22 反查全部方法"会漏。**这与 Track 04 §4.1 的反查路径一致，但补充了一个必要条件。**

### 5.3 内部规范/文件的版本管控（IATF 16949 衔接）

**ISO 9001:2015 §7.5 + IATF 16949 的要求** `[二手/一手混合]`：

**五项核心要求** `[二手，多源一致]`：
1. **识别与描述** —— 有标题、编号、版本、日期，任何副本都能定位到确切版本
2. **发布前评审与批准** —— 由有资格签署的权限人批准适用性
3. **需要时可获得** —— 当前版本在使用地点可获取且清晰可读
4. **版本变更受控** —— 变更受控进行，**修订历史保留**
5. **防止丢失与误用** —— 包括**防止非预期使用过期版本**

**IATF 16949 的附加要求** `[二手]`：
- 文件**变更历史**（change history）
- **外部文件管理**（external documents）—— 如客户规范、法规要求
- 受控过程的**临时变更**（temporary changes）特定控制

- 来源：https://www.paperwise.com/what-is-document-control-in-manufacturing-and-why-does-every-quality-system-require-it/ ｜https://www.fasttqmsoftware.com/iso-for-document-management-system/ ｜https://qt9software.com/glossary/document-control ｜可信度：★★★☆☆

**可与 ISO 9001 区分的条款编号** `[一手]`：
- **ISO 9001:2015** 文件控制 → 条款 **7.5**（Documented Information）
- **IATF 16949:2016** 标识与追溯 → 条款 **8.5.2**，补充条款 **8.5.2.1**
- **IATF 16949:2016** 生产件测量 → **8.5.1.7**
- **IATF 16949:2016** 客诉/售后 → **8.5.5.1**（售后信息反馈流程）
- 来源：https://www.pqbweb.eu/page-iatf-16949-version-2016-requirements-automotive-quality-management-system.php ｜可信度：★★★★☆

**必须受控的文件范围（含判定标准）** `[二手，★★★☆☆]`：
> 判定标准是**影响（impact）** —— "**如果用错版本会导致生产出不合格品或生成无效记录，则该文件受控**"
>
> | 类别 | 典型文件 |
> |---|---|
> | 产品定义 | 图纸、规范、工程标准（含标准引用清单）|
> | 过程控制 | 控制计划、作业指导书、过程表、检验标准 |
> | 质量记录与 PPAP | FMEA、MSA 研究、PPAP 包、质量手册、PSW |
>
> **车规角度的强化**：PPAP 包的**每一个要素**（图纸、FMEA、控制计划、MSA、尺寸结果、PSW）都是受控文件 → **只有"有文件支撑的 PPAP"（document-backed PPAP）才是审核就绪的**
- 来源：https://www.fasttqmsoftware.com/iso-for-document-management-system/

**受控文件的生命周期（5 阶段）** `[二手]`：
```
1 Draft      起草 → 编号、标题、版本、日期；挂到所治理的物项/质量记录上
2 Review & Approve  评审与批准（未批准前不生效 —— 这是控制的"闸门"）
3 Release    发布 → 成为当前版本；使用地点可获取；**任一时刻只有一个当前版本**
4 Change     变更 → 经变更控制（评估影响、新版本批准、**修订历史保留不覆盖**）
5 Withdraw   撤回 → 标记作废并从使用中移除，但**保留记录以供追溯**
```

> 🔑 **两个"闸门"是文件控制的核心**：
> - **批准闸门**：未经批准的文件不生效
> - **变更闸门**：文件不经受控修订不改变
> 这两条一旦建立，ISO 9001 §7.5 的大部分要求自动满足，不依赖个人纪律。

**⚠️ 审核高频失败点（4 个典型）** `[二手，★★★☆☆]`：
1. **版本泛滥（version proliferation）** —— 同一文件多版本并存，最新在 QMS 里，旧版还贴在工位上，另有在班长手册里
2. **作废文件可访问** —— 上述的直接后果，用户无法区分当前/过期
3. **未记录的变更** —— 过程/产品变更先实施、文件后改（"文件说一套，过程做另一套"）
4. **缺修订历史** —— 无法重建某历史时点的过程状态
- **"作废文件撤回是审核最爱"** —— 若审核员要抓文件控制问题，几乎总会抓这一条

**外部文件（客户规范、标准）的管控** `[推断，SOP 建议]`：
```
IF TS-xxxx 客户规范
   → 受控文件台账必须记录：编号、版本、发布日期、来源（客户/官网）、获取日期、存放位置
   → 客户发新版时的处理：
      ① 走 §5.1 的变更分级（读变更清单，评估影响）
      ② 差异分析表（新版 vs 旧版，逐条）
      ③ 影响评估：哪些在用试验受影响？
      ④ 变更控制流程（IATF 16949 8.5.6.1）
      ⑤ 必要时与客户确认
      ⑥ 更新内部规范与试验方案
      ⑦ 归档旧版（标记作废，保留追溯）

IF 公开标准（JESD/IEC/IEC/IPC/ECPE）
   → 同上，但需记录"获取来源 + 版本 + 获取日期"
   → ⚠️ 特别注意：像 A104F→F.01 这类**编辑性升版虽无技术影响，
      但引用编号会变**，台账必须同步更新，否则会出现"引用了已不存在编号"的尴尬
```

### 5.4 IATF 16949 8.5.2.1 追溯要求（与用户的 SN 编码项目直接对应）

**IATF 16949:2016 条款 8.5.2.1 完整子条款** `[一手，逐条列出]`：

| 子条款 | 要求 | 与用户项目的关联 |
|---|---|---|
| 8.5.2.1 | 用追溯支持识别客户收到的产品的**清晰起止点** | ★ 可靠性试验样品的起止点（来料到 FA 结束） |
| 8.5.2.1 | 基于经验教训，识别**可能呈现不符合或安全风险**的产品 | ★ HV-H3TRB 失效样品的追溯 |
| 8.5.2.1 | 实施标识与追溯过程 | — |
| 8.5.2.1 | 进行内部分析：**客户、法规追溯要求** | ★ 车企客户的追溯要求 |
| 8.5.2.1 | **基于风险或失效严重度**（参考 7.5.3.1）制定并记录**追溯计划** | ★★ **这是内部规范的直接依据：追溯深度按风险分级** |
| 8.5.2.1 | 按**产品、工艺、制造地点**定义追溯系统、方法 | ★ 车规模块跨多工序/多地点 |
| a) | 标识不合格品或可疑品（见 8.7.1 / 8.7.1.3）| |
| b) | 隔离不合格品或可疑品（red boxes / "prison"）| ★ FA 样品的物理隔离 |
| c) | 满足**客户或法规的响应时间要求** | ★ FA 报告交付时限 |
| d) | 按格式保存记录（依反应时间约束，见 7.5.3.1）| ★ 试验原始数据保存 |
| e) | **若客户或法规标准规定，须对单个产品做序列化标识（serialized identification）** | ★★★ **这就是用户 SN 编码项目的标准依据** |
| f) | 追溯要求延伸至具有**安全/法规特性**的产品，包括**外购产品** | ★ 芯片/陶瓷基板等外购件的追溯 |

- 来源：https://www.pqbweb.eu/page-iatf-16949-version-2016-requirements-automotive-quality-management-system.php ｜可信度：★★★★☆

> 🔑 **给用户 SN 编码项目的三条具体化建议** `[推断]`：
> 1. **SN 编码不是"管理改进"，是 IATF 16949 8.5.2.1(e) 的条款要求**（若客户或法规规定）。在客户评审中应以此为依据，而非"我们想做得更好"。
> 2. **追溯计划要按 8.5.2.1 的要求"基于风险或失效严重度"分级** —— 不是所有工序都要单件追溯。功率模块的关键工序（芯片贴装、键合、灌封、可靠性试验）需要单件追溯；来料检验可按批。
> 3. **必须验证 SN 在可靠性试验全过程中耐受环境应力** —— 这是最容易被漏的一点：喷码/激光打标在 85/85 高温高湿、150 °C 高温存储、TC 循环后是否仍可读？**建议把"试验后 SN 读回验证"写进 SOP 的 STEP 2.3.1。**

---

## 6. 任务书前提错误清单（供用户核对）

| # | 任务书表述 | 核实结果 | 依据 |
|---|---|---|---|
| 1 | "JESD22-A104 TBL"（把 TBL 与 TC 混为一句）| ❌ **A108 = TBL（Temperature, Bias, and Operating Life）**，是 HTOL/HTRB/HTGB 的母标准。TC 是 **A104**。功率循环是 **A122/A105** + **IEC 60749-34** | A108G 标题页 ★★★★★ |
| 2 | "04-canon 已核实 JESD22-A104F.01 条件表" | ⚠️ **canon的 T12 待办明确写 A104 条件字母定义为待核实**。本track 已通过下载一手 PDF 补齐（表 1 / 表 2 / 表 3 全部提取） | canon T12 + A104F.01 PDF ★★★★★ |
| 3 | "A104 从 F 到 F.01" 需评估影响 | ⚠️ **F→F.01 是纯编辑性变更**（仅去水印+换 logo），技术内容无变化 —— 但引用编号会变 | A104F.01 附录 B.1 一手 ★★★★★ |
| 4 | "车规…还要叠加 UNECE 法规" | ❌ **AQG 324 零引用 UNECE/RoHS/ELV/WEEE**（Track 04 已一手 grep 证实）。若 TS 引用了 UNECE，那是**整车法规线**，与可靠性线正交| canon §1.4 一手 ★★★★★ |
| 5 | "JESD22-B102/B104/A112/A114/C101 **已废止**" | ⚠️ **状态各不相同**：B102 withdrawn(2014)、C101 rescinded(2020)、A115 inactive(2016) 是真失效；A114/B104/A112 是**被取代**（文档可能仍可得） | NASA EEE Bulletin + JEDEC + NSAI ★★★★★ |
| 6 | "AEC-Q100/Q101/Q200 规定的**应力梯度**与样本量**模型**" | ❌ **AEC-Q 不存在"应力梯度模型"**。它给的是「项目+条件+样本量+判据」矩阵。样本量是3 lots × 25或77（因项而异），非推导模型 | Wolfspeed 文档 + 多个实验室表★★★★☆ |
| 7 | "抽样：AQL（GB/T 2828/ISO 2859-1/MIL-STD-105）" | ⚠️ **MIL-STD-105E 已于 1995 withdrawn**，不应再作合同依据；且 **ISO 2859-1:2026 已发布**，与现行的 GB/T 2828.1-2012（等效1999版）**不是同一版本** | ISO 2859 词条 + chinavalidate ★★★☆☆ |
| 8 | "A104 条件表…（作为既有结论引用）" | ⚠️ 见 #2。此外 **二手源广泛误传 A104F.01"有13个条件 A至T"** ——表1 实际13 行但字母跳号（无 D/E/F），且二手源把M 与 N 的温度搞混 | A104F.01 表 1 一手 ★★★★★ |

---

## 7. 未核实事项清单（保留，不和稀泥）

| ID | 事项 | 为何未核实 | 建议核实路径 |
|---|---|---|---|
| **U1** | **AQG 324 04.1/2025 第 9 章 QL-01~QL-07 的完整条件表**（含 ΔTj、Tj,max、循环次数、样本量、判据原文） | ECPE 下载区为token 化直链，本次未取到PDF；二手源（x-ipm）对 QL-06/07 的引文明显错位 | 访问 https://www.ecpe.org/research/working-groups/automotive-aqg-324/ 自行下载（免费 CC BY-ND） |
| **U2** | **AQG 324 附录 I.C（试验文件化）、附录 II.C（物理分析典型要点）原文** | 同上 | 同上 |
| **U3** | **AQG 324 Annex I.B "Delta qualification matrix"的具体内容** | 只有标题，未见内容 | 同上 |
| **U4** | **AEC-Q101 Rev E 的精确项目表与条件**（Rev 号本身 canon 已标未核实）| aecouncil.com 本次无法访问 | http://www.aecouncil.com/AECDocuments.html |
| **U5** | **A108G 一手 PDF** | 现有信息来自三个一致的二手源（antpedia/plusstd/xktest），含 ballot 号 JCB-22-55 与 JC-14.1，但未取得 JEDEC 原文 | 注册 jedec.org 免费下载 |
| **U6** | **JESD22-A101D.01 一手 PDF**（测量窗口 168 h、偏压准则等） | 二手转述| jedec.org |
| **U7** | **JESD69（资格信息要求）、JESD74（早期失效率计算）、JESD85（FIT 计算）原文** | 仅从 JESD47 引用列表确认存在与标题 | jedec.org |
| **U8** | **H3TRB Peck 模型的 x、y、Ea 具体数值** | 二手只给形式 | 查 K. Hatori et al., ECCE 2023；K. Kitajima相关文献 |
| **U9** | **T-stress 模型的权威形式** | Track 04 与本track 均未找到权威统一表述 | IEC 62506:2023 原文 |
| **U10** | **IEC 60068-2-14 的严酷度等级（Pb、Pmin）与 Test Na/Nb/Nc 的精确条件** | 二手源互相矛盾（转移时间有 ≤10 s / 2-3 min 两种说法）| webstore.iec.ch |
| **U11** | **AQG 324 QL-05/QL-06 要求的 HTGB 正负压分配方式**（新版"一半正压一半负压" vs 旧版"先正后负"）| 来源为安森美技术文章（★★★☆☆），未与 04.1/2025 原文比对 | 下载 AQG 324 04.1/2025 |
| **U12** | **GB/T 2828.1 各 AQL 档位与样本量字码的完整表** | 百科来源，非标准原文 | 购买 GB/T 2828.1-2012 |
| **U13** | **"77 pcs" 的原始统计依据** | canon T7 与本track 均未找到标准原文；本track 给出的是自算的 R_L 反推解释（77→R_L=0.9705 @90%CL），但这可能是巧合而非原始依据 | IEC 62506:2023 原文；或 JESD47 原文的 sample size 表 |
| **U14** | **A104 表 1 各条件的"典型应用"对应关系** | 二手源给出（条件 B=汽车等），但 A104F.01 表 1 **无此列** | 无（标准不提供，此列为行业惯例）|
| **U15** | **IEC 60749-34:2011 的完整试验条件表** | 二手仅引ton/电流条件 | webstore.iec.ch |
| **U16** | **HTRB 的"25°C↔500h"换算的原始依据** | 二手；本track 反推出隐含 Ea≈2.23 eV（远高于常用 0.7 eV），疑为经验规则 | MIL-STD-750 方法 1038；AEC-Q101 原文 |

---

## 8. 本track 对知识 OS 的建模范建议

> 提炼本track 最可复用的结构，供master skill 的 scripts/ 与data/ 使用。

### 8.1 标准介入点索引（"标准在哪一步介入"的反向索引）

| 工程环节 | 介入的标准 | 介入形式 | 强制程度 |
|---|---|---|---|
| 概念/需求定义 | JESD47、JESD94、JEP122 | 方法论 | 建议 |
| 失效机理识别 | **JEP131（FMEA）**、JEP122、PFMEA（VDA） | 方法论 | 建议 |
| 应力方案设计 | JESD94、IEC 62506、JESD91 | 方法论 | 建议 |
| 试验条件选取 | JESD22-A1xx / IEC 60749-x / AQG 324 QL/QE | **条件表** | 强制 |
| 循环次数/时长确定 | **JESD47、JESD94、采购文件（客户 TS）** ← **A104 不提供** | 计算 | 强制 |
| 样品量与质量等级 | **采购文件（A104F.01 §7(e)）** | 规定 | 强制 |
| 预处理 | J-STD-020、JESD22-A113 | 条件+分类 | 条件性 |
| 基线测量 | AQG 324 QM 组、IEC 60747-15、IEC 60749-34 | 方法学 | 强制（车规）|
| 试验执行 | 对应方法标准的 Procedure 章节 | — | 强制 |
| 试验后电测窗口 | A108G（≤55 °C 冷却）、A103（168 h）、60749-5（48 h）、A101（168 h）、AEC-Q101 IOL（96 h）| **时限** | 强制 |
| 失效判定 | 方法标准的 Failure criteria + 采购文件的 special acceptance criteria（A104F.01 §7(d)）| 规定/自定义 | 强制 |
| 失效分析 | JEP156（CPI）、MIL-STD-883 2000系列（2011/2019/2012 等）、SEMI 标准 | 方法 | 按需 |
| 报告 | **A108G 13 项**、A104F.01 §7（6 项）| 规定 | 强制 |
| 抽样（来料/出货）| ISO 2859-1 / GB/T 2828.1 / ANSI Z1.4（AQL 体系）| 查表 | 合同 |
| 失效率外推 | JESD85、JEP143 | 方法学 | 按需 |
| 追溯 | **IATF 16949 8.5.2.1(e)**、JESD46（变更通知）| 规定 | 车规强制 |
| 文件管控 | ISO 9001 §7.5 + IATF 16949 | 规定 | 车规强制 |
| 变更控制 | IATF 16949 8.5.6.1、JESD46 | 规定 | 车规强制 |

### 8.2 建议的数据结构（`data/` 目录）

```jsonc
// 试验方法的元数据
{
  "id": "JESD22-A104F.01",
  "org": "JEDEC", "committee": "JC-14.1",
  "revision": "F.01", "date": "2023-04",
  "supersedes": "A104F",           // 编辑性变更 → 单独标记
  "change_class": "editorial_only",
  "ballot": "JCB-00-16, JCB-05-82, JCB-09-20, JCB-14-45, JCB-20-31",
  "scope_limit": "gasous media only; NOT thermal shock",
  "defines_conditions": ["Table1:temp_extremes", "Table2:soak_mode", "Table3:cycle_rate", "ramp_rate"],
  "does_NOT_define": ["number_of_cycles", "sample_size", "quality_level"],
  "delegates_to": ["JESD47", "JESD94", "procurement_document"],
  "source": "https://file.globalso.com/.../jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf",
  "confidence": "primary"
}
```

### 8.3 建议的 CLI 决策树入口

```
$ semiconductor-standards route --product power-module --application automotive
  → 输出：分流结果 + 强制标准栈 + 阶段计划 + 差异说明

$ semiconductor-standards translate --from A104F.01 --product my-module \
     --material-tg 175 --solder Pbfree --delta-tj 100 --mission cycles_per_year 3000
  → 输出：条件选择（含 Tg/Pb 检查）+ 修正记录 + 循环次数计算 + 判据建议

$ semiconductor-standards check-criteria --test pcsec
  → 输出：5%/20% 判据出处 + 测量方法要求 + 已知局限警告（§2.3.7）

$ semiconductor-standards sample-size --n 77 --cl 0.90
  → 输出：R_L= 0.9705（提示"结论很弱"）

$ semiconductor-standards version-check --std A104F
  → 输出：已被A104F.01 取代（编辑性）；引用编号需更新

$ semiconductor-standards read-ts-references --file GS-95035.pdf
  → 输出：按应力类型分类的引用分布 + 风险关注点推断（§4.3）
```

---

## 9. 信源清单（一手优先）

| # | 来源 | 类型 | 可信度 | 用于 |
|---|---|---|---|---|
| 1 | https://file.globalso.com/file_manage/3034/20250321/jedec-jesd22-a104f-01-2023-temperature-cycling-1.pdf | **一手（JEDEC 官方 PDF 全文，已下载解析）** | ★★★★★ | §1.2 §2.2.1 §5.1 §6 |
| 2 | https://www.kekaoxing.com/wp-content/uploads/user_files/4993/publish/file/file-2020-06-07-12-09-46.pdf | **一手（JESD47 全文含 Scope + §2 引用列表）** | ★★★★★ | §1.0 §1.3 §4.4 |
| 3 | https://nepp.nasa.gov/docs/tasks/EEE-Parts-Bulletin/EEE-Parts-Bltn-2021-Vol-13-No1-ESD-Testing-Standards-GaN-Devices-CL22-0048.pdf | **一手（NASA 技术通报）** | ★★★★★ | §5.2 |
| 4 | https://www.jedec.org/node/5911（JEDEC 新闻稿 JS-002） | **一手（JEDEC 官网）** | ★★★★★ | §5.2 |
| 5 | https://shop.standards.ie/.../jedec-jesd22-b102e-2007 （NSAI 标准商店） | **一手状态记录（Withdrawn date/superseded by）** | ★★★★★ | §5.2 |
| 6 | https://www.jedec.org/node/8494（J-STD-002 页面） | **一手（JEDEC 官网）** | ★★★★★ | §5.2 |
| 7 | https://store.accuristech.com/standards/jedec-jesd47n?product_id=3130401 | 一手（JESD47N 完整 Scope 摘要） | ★★★★☆ | §1.3 |
| 8 | https://shop.standards.ie/.../jedec-jesd47n-2026 （版本/日期/页数） | 一手（商店条目） | ★★★★☆ | §1.3 |
| 9 | https://www.psma.com/.../is163-...-jc70.pdf （JEDEC JC-70 官方演讲） | **一手（JEDEC 委员会材料，含 JESD94B 流程图）** | ★★★★☆ | §3.0 |
| 10 | https://www.pqbweb.eu/page-iatf-16949-version-2016-requirements-automotive-quality-management-system.php | **一手（逐条列出 IATF 16949:2016 条款号与内容）** | ★★★★☆ | §2.1 §5.3 §5.4 |
| 11 | https://www.ecpe.org/research/working-groups/automotive-aqg-324/ | **一手（ECPE 官网，AQG 324 工作组沿革）** | ★★★★★ | §1.0 §7（U1 待办） |
| 12 | https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-5{ed3.0.RLV}en.pdf | **一手（VDE=IEC 出版方，标准正文预览）** | ★★★★★ | §2.2.3 |
| 13 | https://www.vde-verlag.de/iec-normen/preview-pdf/info_iec60749-4{ed2.0}b.pdf | **一手（同上）** | ★★★★★ | §2.2.3 |
| 14 | https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Power_Cycling_and_Lifetime_Modeling_Approach.pdf | **一手（厂商技术文档，含 AQG 324 判据与 PCsec/PCmin 分工）** | ★★★★☆ | §2.2.4 |
| 15 | https://assets.wolfspeed.com/uploads/2025/11/Wolfspeed_Designed_to_Last_Even_in_the_Harshest_Environments.pdf | **一手（厂商技术文档，AEC-Q101 条件表）** | ★★★★☆ | §1.4 §2.1 |
| 16 | https://plusstd.com/1195904236.html （JESD22-A108G 解读） | 二手（高可信，含条款级细节与报告 13 项） | ★★★★☆ | §2.2.2 |
| 17 | https://www.antpedia.com/standard/1195904236-10.html （A108G 版本/ballot/变更） | 二手（高可信，多源一致） | ★★★★☆ | §2.2.2 |
| 18 | https://plusstd.com/5148441.html （JESD22-A122-2007 Scope 摘要） | 二手（A122 Scope 原文转述） | ★★★★☆ | §2.2.2 |
| 19 | https://core.ac.uk/download/552888767.pdf（功率循环方法学术对比） | 二手（学位论文，引用 A122/A105 原文，含 3.2 倍高估警告） | ★★★☆☆ | §2.2.2 §2.2.4 |
| 20 | https://plusstd.com/7720055.html （JESD94B 解读） | 二手（高可信，流程与原则） | ★★★★☆ | §3.0 |
| 21 | https://www.ab-sm.com/a/46818（功率器件单管vs模块差异，实验室技术报告） | 二手（技术报告，逐条对应失效机理，★★★★） | ★★★★☆ | §2.2.3 §2.3.6 |
| 22 | https://www.powerelectronicsnews.com/h3trb-reliability-tests-for-sic-power-devices/ | 二手（技术期刊，H3TRB/HV-H3TRB 条件与 Peck 扩展） | ★★★★☆ | §2.2.3 |
| 23 | http://ictest8.com/a/seminar/experience/2024/12/AQG.html（主驱功率循环判据分析） | 二手（实验室实测经验，含热阻判据缺陷 4 条） | ★★★☆☆ | §2.3.7 |
| 24 | http://www.ictest8.com/a/engineering/2022/06/glxh.html（AQG324 功率循环条件） | 二手 | ★★★☆☆ | §2.2.4 |
| 25 | https://www.eet-china.com/mp/a237849.html（安森美 AQG324 解读） | 二手（技术媒体，含 B样/C样流程、SiC HTGB 变更、DGS 状态） | ★★★☆☆ | §1.1 §2.2.3 |
| 26 | https://www.cnblogs.com/qixintel/p/18121433（JESD22 版本/状态表） | 二手（版本状态表，多条与一手交叉验证一致） | ★★★☆☆ | §2.2.2 §5.2 |
| 27 | https://www.chinesestandard.net/Related.aspx/GBT4937.25-2025（GB/T 4937 与 IEC 60749 对应） | 二手（标准条目，含等同采用说明） | ★★★☆☆ | §1.0 |
| 28 | https://std.samr.gov.cn/...（GB/T 4937 第13部分 报批稿） | **一手（国标报批稿，含"GB/T 4937 所有部分均一一对应采用 IEC 60749"）** | ★★★★★ | §1.0 |
| 29 | https://www.erp-information.com/acceptable-quality-level.html（AQL/RQL/LTPD 辨析） | 二手 | ★★★☆☆ | §1.5 |
| 30 | https://chinavalidate.com/en/blog/pre-shipment-inspection-china（ISO 2859-1:2026 版本警示） | 二手 | ★★★☆☆ | §1.5 |
| 31 | https://baike.baidu.com/item/ISO2859（ISO 2859 版本谱系） | 二手（百科） | ★★★☆☆ | §1.5 |
| 32 | https://baike.baidu.com/item/调整型抽样检验/19172886（GB/T 2828.1 转移规则） | 二手（百科，但规则与 ISO 2859-1:1999 一致） | ★★★☆☆ | §1.5 |
| 33 | https://metricgate.com/docs/reliability-demonstration-test/（零失效样本量公式） | 二手（在线计算器文档，公式可独立验证） | ★★★☆☆ | §1.5 |
| 34 | https://help.reliasoft.com/articles/content/hotwire/issue118/relbasics118.htm（ReliaSoft 累计二项式） | 二手（商业软件厂商技术文档，方法论可靠） | ★★★★☆ | §1.5 |
| 35 | https://www.antpedia.com/standard/7720056-10.html（JESD22-A103E 条件） | 二手（高可信，多源一致） | ★★★★☆ | §2.2.5 |
| 36 | https://plusstd.com/7720056.html （A103E 条件/测量窗口/失效判据） | 二手（高可信） | ★★★★☆ | §2.2.5 |
| 37 | https://www.sonacme.com/m/news/280.html（IEC 60068-2-14 Na/Nb） | 二手（设备商，但条件描述与其他源矛盾） | ★★☆☆☆ | §2.2.1（标未核实） |
| 38 | https://metricgate.com/... ；https://www.ultrontek.com/... （χ²/LTPD 公式） | 二手 | ★★☆☆☆ | §1.5 |
| 39 | https://www.chipfoundryservices.com/glossary/... （FIT 公式、A104 条件表） | ⚠️ **内容农场，仅公式形式参考；其 A104 条件表有 M/N 混淆错误** | ★☆☆☆☆ | 反例 |
| 40 | https://antpedia/kpt-bj/b2b168/chinacryo等 | 二手（部分错位：immersion mode 术语错误、QL-06/07 引文错位） | ★★☆☆☆ | 反例 |

**已排除信源（黑名单/低质）**：知乎、微信公众号、百度百科部分词条（"调整型抽样检验"内容与ISO 2859-1 一致故引用，但不作权威依据）、内容农场（chipfoundryservices、grokipedia等）。

---

## 10. 薄弱维度自评（诚实清单）

| 维度 | 强度 | 说明 |
|---|---|---|
| **A104 条件表/Soak mode** | ★★★★★ | 已下载一手 PDF 全文解析，表1/2/3 逐行提取，附录 B 版本史完整 |
| **JESD47 方法论骨架（JESD94/JESD85/JESD91/JEP143/JEP156 的引用关系）** | ★★★★★ | 来自 JESD47 全文 §2 引用列表 |
| **IATF 16949 追溯条款** | ★★★★★ | 逐条列出 8.5.2.1 全部子条款 |
| **ESD 方法废止链** | ★★★★★ | NASA EEE Bulletin + JEDEC 新闻稿双源 |
| **A108G 条件与报告要求** | ★★★★☆ | 三源一致但未取得 JEDEC 一手 PDF |
| **加速模型公式（Arrhenius/Peck/CM/LESIT/Bayerer/Norris-Landzberg）** | ★★★★☆ | 公式结构可靠；**所有数值参数（Ea/B/n/h）来自二手，必须自有数据标定** |
| **AEC-Q101 条件** | ★★★★☆ | 有厂商一手表格，但 AEC 官网无法访问，Rev 号未核实 |
| **失效模式↔应力↔标准映射表** | ★★★★☆ | 多源交叉验证；AQG 附录 II.C 原文未取 |
| **PC 控制策略 3.2 倍高估** | ★★★☆☆ | 单一来源（学位论文引A122），但技术论断具体可检验 |
| **热阻判据的 4 条缺陷** | ★★★☆☆ | 单一实验室经验总结，但论断具体 |
| **AQL/抽样体系** | ★★★☆☆ | 机制清楚，但**表格数据（Ac/Re/样本量字码）未取标准原文** |
| **AQG 324 QL 完整条件表** | ★★☆☆☆ | **最大缺口** —— ECPE token 化下载未取到PDF，二手源引文错位 |
| **汽车 vs 工业 vs 消费 vs 军用的量化对比** | ★★☆☆☆ | 缺各标准的完整条件表，多为二手拼接 |
| **失效分析报告结构（8D）** | ★★☆☆☆ | 通用工程惯例，无标准依据；A108G 13 项是唯一强制部分 |
| **内部规范产生场景** | ★★☆☆☆ | 逻辑推导为主，缺行业实证 |

### 三个最需要补齐的缺口（按优先级）

1. **AQG 324 04.1/2025 全文** —— 价值最高。它一次性解决：QL-01~QL-11 完整条件表、附录 I.C 试验文件化要求、附录 II.C 物理分析要点、附录 I.B Delta 资格矩阵。**免费 CC BY-ND，只需从 ECPE 下载。**
2. **JESD47N 全文** —— 补齐资格矩阵的应力梯度与样本量表（可解决 U13"77 pcs 依据"）。
3. **IEC 60749-34:2011 全文** —— 功率循环的方法学母标准，AQG 324 QL-01/QL-02 引用它。**付费。**

---

**报告结束。**

**本track 的方法论贡献**：Track 04 建立了"标准是什么"的知识骨架；本track 建立了**"标准在哪一步介入"的时序模型**——其核心发现是 **JESD22/IEC 60749 系列是"方法库"，而 JESD47 / JESD94 / 客户采购文件才是"资格判定者"**。这个区分（由 A104F.01 §5 与 §7 原文坐实）决定了所有可靠性工程师的工作方式：**标准给你"怎么做"，你必须自己算"做多少"。**
