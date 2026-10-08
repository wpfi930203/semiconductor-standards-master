# 本地资料库覆盖清单（LOCAL-CORPUS）

> **这份文件回答一个问题：手上有哪些标准资料、每份能引用到什么程度。**
>
> 触发本 skill 时，凡涉及具体条款/数值/术语，**必须先在此清单确认资料是否在库、
> 以及在库的是哪种形态**，再决定措辞。清单之外的内容一律声明「无法确认」。

**来源根目录**：`<本地标准资料库>`
**构建日期**：2026-10-07　|　**提取方式**：PyMuPDF 文本层抽取（无 OCR / 无翻译 / 无改写）

---

## 一、引用分层模型（最重要的规则）

标准 PDF 的**文件名不可信**——本次实测发现多份标注「完整英文电子版」的文件，
正文实为**机器翻译中文**（文件名里带 `_translate_` 的就是这类）。
因此本 skill 一律以**文档自述 + 实测语种**定级，不以文件名为准。

| 层 | 名称 | 可引用措辞 | 可引用数值 | 使用规则 |
|---|---|:---:|:---:|---|
| **L1** | 英文原文在库 | ✅ | ✅ | 可直接引用措辞与数值；引用时标注标准编号 + 版本 + 页/条 |
| **L2** | 官方中文译本在库 | ✅ | ✅ | 可引用，但须注明「官方译本，冲突时以英文版为准」 |
| **L3** | 机器翻译在库 | ❌ | ✅ | 仅可用于【条款号 / 章节结构 / 表格位置 / 数值条件】定位；**禁止引用其术语译名**（实测已有 Wire Bond→「线束」等硬错） |
| **L4** | 扫描件在库未提取 | ❌ | ❌ | 不得引用任何内容；只能声明「已持有该标准扫描件，未做文字识别」 |
| **L0** | 不在库 | ❌ | ❌ | 必须声明无法确认，禁止推测或从记忆回答 |

### 为什么机翻件不能引用术语

实测样例（JESD22-B116B 机翻件 vs 英文原件）：

| 英文原文 | 机翻件的译法 | 问题 |
|---|---|---|
| Wire Bond Shear Test | 「**线束**剪切试验」 | 线束 = wire harness/cable，与键合线无关 |
| ball bond | 「球键 / 球粘接」 | 业界标准译法是「球焊点」 |
| thermosonic (ball) bond | 「**热膜**（球）键」 | 热膜 ≠ 热超声，物理机理完全不同 |
| metallurgical bond | 「冶金键」 | 标准译法是「冶金结合」 |
| stitch bond | 「**针线**」 | 标准译法是「针脚焊点」 |

→ 这类错误会直接改变技术含义。**所以 L3 层只能用来定位条款号和表格位置，数值可比对，
术语必须回英文原文。**

---

## 二、总览

| 指标 | 数量 |
|---|---|
| 源 PDF 文件总数 | 63 |
| 去重后不同标准编号 | 52 |
| 已提取文本层 | 49 份 |
| 扫描件（持有但未识别文字） | 10 份文件 / 4 个标准 |

**按引用分层的构成：**

| 层 | 数量 | 标准编号 |
|---|---:|---|
| L1 英文原文在库 | 7 | IPC-7351、IPC-7351B、IPC-TM-650-2.4.22c、JESD22-B116B、JESD47L、JESD51-2A、JESD51-6 |
| L2 官方中文译本在库 | 1 | IPC-7095D |
| L3 机器翻译在库 | 37 | J-STD-020、JESD22-A100E、JESD22-A101D.01、JESD22-A102E、JESD22-A103E、JESD22-A104F、JESD22-A105D、JESD22-A106B.01、JESD22-A107C、JESD22-A108F、JESD22-A109B、JESD22-A110E、JESD22-A111B、JESD22-A113I、JESD22-A117E、JESD22-A118B.01、JESD22-A119A、JESD22-A120B、JESD22-A121A、JESD22-A122A、JESD22-B100B、JESD22-B101C、JESD22-B105E、JESD22-B106E、JESD22-B107D、JESD22-B108B、JESD22-B109C、JESD22-B110B.01、JESD22-B111A、JESD22-B112B、JESD22-B113B、JESD22-B114B、JESD22-B115A.01、JESD22-B116B、JESD22-B117B、JESD22-B118、JS-001 |

> **一句话结论**：库里 49 份资料中，**只有 7 份有英文原文**（L1），
> 1 份官方中文译本（L2），**37 份是机器翻译（L3）**，4 个军标是扫描件（L4）。
> 这意味着：**绝大多数 JESD22 条款的措辞不能直接引用，只能定位。**

---

## 三、逐份清单（类别 / 适用范围 / 关键条目 / 出处 / 层级）

> **「蒸馏」列**：🟢 = 已有条款级 digest（章节结构 + 数值条件 + 术语纠错）
> **「文字识别」列**：对扫描件标注 OCR 进度

### 热-机械

#### `JESD22-A104F`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（33 节 / 19 数值行）
- **适用范围**：温度循环 TC（单/双/三箱，空气介质）
- **关键条目**：★ 13 组条件（A/B/C/G/H/I/J/K/L/M/N/R/T）+ 4 种 soak mode + 每条件典型 cph；§5 明确循环次数由 JESD47 或供需约定；§7 列出采购文件须规定项；表1 脚注给出 3 条选条件注意事项 + Pb/Sn 超 125°C 不推荐
- **文档自述**：版本号 `JESD22、JESD22-A104F、JESD94`；日期线索 `（未识别到日期）`
- **规模**：15 页，文本层 7,130 字符
- **出处**：`references/sources/standards/jedec/JESD22-A104F.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A104F ：2020 Temperature Cycling - 完整英文电子版（15页）_1_15_translate_20240815160915.pdf`
- **SHA256(16)**：`5c47caf0284c123f`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A106B.01`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（3 节 / 2 数值行）
- **适用范围**：热冲击 TST（两液槽，转换 <10s）
- **关键条目**：★ 与 A104 的关键区别证据在此：依赖液体耦合介质的快速升降温
- **文档自述**：版本号 `106B.01、A106B.01、JESD22、JESD22-A106`；日期线索 `（未识别到日期）`
- **规模**：7 页，文本层 3,256 字符
- **出处**：`references/sources/standards/jedec/JESD22-A106B.01.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A106B.01：2016 Thermal Shock - 完整英文电子版（7页）_1_7_translate_20240815161248.pdf`
- **SHA256(16)**：`4d88d5c339a73d0c`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 热-电耦合

#### `JESD22-A105D`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（9 节 / 7 数值行）
- **适用范围**：功率与温度循环 PTC（通电+环境箱叠加）
- **关键条目**：与 A122 的差别：A105 是「环境箱 + 通电自加热」组合，A122 是纯功率循环
- **文档自述**：版本号 `JESD22、JESD22-A105D`；日期线索 `（未识别到日期）`
- **规模**：10 页，文本层 3,264 字符
- **出处**：`references/sources/standards/jedec/JESD22-A105D.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A105D ：2020 Power and Temperature Cycling - 完整英文电子版（9页）_1_9_translate_20240815161215.pdf`
- **SHA256(16)**：`f9b6d3bbfae89bee`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A122A`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（17 节 / 3 数值行）
- **适用范围**：功率循环 PC（纯通电加热）
- **关键条目**：★ 与 A104 机理不同：通电自加热 → 考核键合线/金属化/焊层；AQG 324 QL-01/QL-02 的车规化版本
- **文档自述**：版本号 `JESD22、JESD22-A122A`；日期线索 `（未识别到日期）`
- **规模**：16 页，文本层 6,970 字符
- **出处**：`references/sources/standards/jedec/JESD22-A122A.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A122A：2016 Power Cycling - 完整英文电子版（16页）_1_16_translate_20240815163259.pdf`
- **SHA256(16)**：`669de30235ded58a`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 热-电（偏压寿命）

#### `JESD22-A108F`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（15 节 / 10 数值行）
- **适用范围**：Temperature, Bias, and Operating Life（业界俗称 TBL/HTOL 母标准）
- **关键条目**：★ 官方标题为 Temperature, Bias, and Operating Life —— 无 Voltage；Ta 需使 Tj(min) ≥ 125°C；是 HTOL/HTRB/HTGB 的母方法
- **文档自述**：版本号 `JESD22、JESD22-A108F、JESD47`；日期线索 `（未识别到日期）`
- **规模**：10 页，文本层 4,392 字符
- **出处**：`references/sources/standards/jedec/JESD22-A108F.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A108F-2017 Temperature, Bias, And Operating Life - 完整英文版（10页）_1_10_translate_20240815161453.pdf`
- **SHA256(16)**：`599c015a6a7c0281`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 热-电（存储）

#### `JESD22-A103E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（5 节 / 2 数值行）
- **适用范围**：高温存储寿命 HTSL
- **关键条目**：Ta 150°C/1000h 族；考核金属间化合物生长、Kirkendall 空洞
- **文档自述**：版本号 `J-STD-020、JESD22、JESD22-A103E、JESD22-A113`；日期线索 `2015`
- **规模**：9 页，文本层 3,366 字符
- **出处**：`references/sources/standards/jedec/JESD22-A103E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A103E：2015 High Temperature Storage Life（高温储存寿命）- 完整英文版（9页）_1_9_translate_20240815160838.pdf`
- **SHA256(16)**：`7a65fc59e00776c7`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A119A`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（5 节 / 2 数值行）
- **适用范围**：低温存储寿命 LTSL
- **关键条目**：★ AQG 324 QL-04 的母方法（cond. A，1000h @ ≤-40°C）
- **文档自述**：版本号 `JESD22、JESD22-A119A`；日期线索 `2015`
- **规模**：7 页，文本层 2,244 字符
- **出处**：`references/sources/standards/jedec/JESD22-A119A.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A119A：2015 Low Temperature Storage Life - 完整英文电子版（7页）_1_7_translate_20240815163005.pdf`
- **SHA256(16)**：`1ba5887b6c84dc32`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 湿热/电化学

#### `JESD22-A100E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（14 节 / 19 数值行）
- **适用范围**：循环温湿度偏压（带表面凝露）
- **关键条目**：CTC 循环剖面；凝露条件；与 A101 稳态 THB 的区别在'循环'与'凝露'
- **文档自述**：版本号 `JESD22、JESD22-A100E`；日期线索 `（未识别到日期）`
- **规模**：8 页，文本层 3,941 字符
- **出处**：`references/sources/standards/jedec/JESD22-A100E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A100E：2020 Cycled Temperature-Humidity-Bias with Surface Condensation Life Test - 完整英文电子版（8页）_1_8_translate_20240815160349.pdf`
- **SHA256(16)**：`1eb7743d59ba5758`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A101D.01`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（16 节 / 18 数值行）
- **适用范围**：稳态温湿度偏压寿命（THB 85/85）
- **关键条目**：85±2°C / 85±5%RH / 1000h；Peck 模型的理论出处；无偏压变体见 A102/A118
- **文档自述**：版本号 `A101D.01、JESD22`；日期线索 `（未识别到日期）`
- **规模**：10 页，文本层 4,642 字符
- **出处**：`references/sources/standards/jedec/JESD22-A101D.01.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A101D.01：2021 Steady-State Temperature-Humidity Bias Life Test - 完整英文电子版（10页）_1_10_translate_20240815160457.pdf`
- **SHA256(16)**：`20b96b81d72ec04f`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A102E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（8 节 / 15 数值行）
- **适用范围**：加速耐湿—无偏压蒸煮（Autoclave / PCT）
- **关键条目**：121°C 饱和蒸汽、无偏压 → 考核封装吸湿与分层，**不含电化学腐蚀**
- **文档自述**：版本号 `JESD22、JESD22-A102A、JESD22-A102B、JESD22-A102E`；日期线索 `2012`
- **规模**：9 页，文本层 3,684 字符
- **出处**：`references/sources/standards/jedec/JESD22-A102E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A102E：2015(R2021) Accelerated Moisture Resistance - Unbiased Autoclave - 完整英文电子版（9页）_1_9_translate_20240815160638.pdf`
- **SHA256(16)**：`eb9588ec31529d71`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A110E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（14 节 / 29 数值行）
- **适用范围**：HAST 高加速温湿度应力（有偏压）
- **关键条目**：★ 常用 130°C/85%RH、110°C/85%RH；与 THB 的优先关系由 IEC 60749-4 裁决
- **文档自述**：版本号 `JESD22、JESD22-A110E`；日期线索 `（未识别到日期）`
- **规模**：12 页，文本层 5,094 字符
- **出处**：`references/sources/standards/jedec/JESD22-A110E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A110E：2015 Highly Accelerated Temperature and Humidity Stress Test (HAST) - 完整英文电子版（12页）_1_12_translate_20240815162215.pdf`
- **SHA256(16)**：`cba1c9e52f47cbfd`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-A118B.01`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（13 节 / 20 数值行）
- **适用范围**：无偏压 HAST（uHAST）
- **关键条目**：与 A110 的区别：**无偏压** → 只考核吸湿/分层，不考核电化学
- **文档自述**：版本号 `A118B.01、JESD22、JESD22-A118B.01`；日期线索 `2015`
- **规模**：9 页，文本层 4,212 字符
- **出处**：`references/sources/standards/jedec/JESD22-A118B.01.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A118B.01：2021 Accelerated Moisture Resistance - Unbiased HAST - 完整英文电子版（9页）_1_9_translate_20240815162906.pdf`
- **SHA256(16)**：`7abf499d004fc598`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 机械应力

#### `JESD22-B105E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（37 节 / 14 数值行）
- **适用范围**：引线完整性 Lead Integrity
- **关键条目**：引线拉伸/弯曲疲劳；
- **文档自述**：版本号 `JESD22、JESD22-A109、JESD22-B105E`；日期线索 `（未识别到日期）`
- **规模**：18 页，文本层 8,526 字符
- **出处**：`references/sources/standards/jedec/JESD22-B105E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B105E：2018 Lead Integrity - 完整英文电子版（18页）_1_18_translate_20240813153612.pdf`
- **SHA256(16)**：`cd8515a9f5440f57`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B110B.01`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（39 节 / 12 数值行）
- **适用范围**：机械冲击（器件与子组件）
- **关键条目**：冲击谱/峰值加速度
- **文档自述**：版本号 `B110B.01、JESD22-B110B.01`；日期线索 `（未识别到日期）`
- **规模**：12 页，文本层 6,151 字符
- **出处**：`references/sources/standards/jedec/JESD22-B110B.01.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B110B.01：2019 Mechanical Shock – Device and Subassembly - 完整英文电子版（11页）_1_11_translate_20240815164141.pdf`
- **SHA256(16)**：`ec06018a52c5b3cd`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 焊接耐受力

#### `JESD22-B106E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（18 节 / 27 数值行）
- **适用范围**：通孔器件耐焊接热冲击
- **关键条目**：波峰焊模拟下的耐热性
- **文档自述**：版本号 `JESD22、JESD22-A111、JESD22-B106E`；日期线索 `（未识别到日期）`
- **规模**：12 页，文本层 4,906 字符
- **出处**：`references/sources/standards/jedec/JESD22-B106E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B106E：2016 Resistance to Solder Shock for Through-Hole Mounted Devices - 完整英文电子版（11页）_1_11_translate_20240815163938.pdf`
- **SHA256(16)**：`bfd6ea552056c1d4`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 互连强度

#### `JESD22-B109C`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（30 节 / 3 数值行）
- **适用范围**：倒装芯片拉伸拉脱 Flip Chip Tensile Pull
- **关键条目**：★ 与 B115（焊球拉）区分：B109 是倒装凸点整体拉脱
- **文档自述**：版本号 `JESD22-B109C`；日期线索 `（未识别到日期）`
- **规模**：14 页，文本层 5,059 字符
- **出处**：`references/sources/standards/jedec/JESD22-B109C.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B109C：2021 Flip Chip Tensile Pull - 完整英文电子版（13页）_1_13_translate_20240815164100.pdf`
- **SHA256(16)**：`b9942ac1ad3123d7`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B115A.01`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（18 节 / 12 数值行）
- **适用范围**：焊球拉脱 Solder Ball Pull
- **关键条目**：★ 拉脱（pull）而非剪切（shear）；与 B117 区分
- **文档自述**：版本号 `B115A.01、IPC-9708、JESD22、JESD22-B115A.01`；日期线索 `（未识别到日期）`
- **规模**：22 页，文本层 12,061 字符
- **出处**：`references/sources/standards/jedec/JESD22-B115A.01.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B115A.01：2016 Solder Ball Pull - 完整英文电子版（22页）_1_22_translate_20240815164641.pdf`
- **SHA256(16)**：`cd89bce20aa11115`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B116B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（23 节 / 11 数值行）
- **适用范围**：键合线剪切 Wire Bond Shear
- **关键条目**：★ 机翻件，术语不可引用（把 Wire Bond 译成「线束/钢丝」）。英文原件见同目录 JESD22-B116B（英文原文条目）
- **文档自述**：版本号 `JESD22、JESD22-B116B`；日期线索 `（未识别到日期）`
- **规模**：29 页，文本层 15,138 字符
- **出处**：`references/sources/standards/jedec/JESD22-B116B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B116B：2017 Wire Bond Shear Test Method - 完整英文电子版（29页）_1_29_translate_20240815164821.pdf`
- **SHA256(16)**：`98988d35d1cde403`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B116B`　<span style='color:#888'>[L1 英文原文在库]</span>

- **蒸馏状态**：🟢 digest（23 节 / 11 数值行）
- **适用范围**：键合线剪切 Wire Bond Shear
- **关键条目**：★ 机翻件，术语不可引用（把 Wire Bond 译成「线束/钢丝」）。英文原件见同目录 JESD22-B116B（英文原文条目）
- **文档自述**：版本号 `JESD22-B116A、JESD22-B116B`；日期线索 `April 2017、August 2009、2009`
- **规模**：32 页，文本层 57,739 字符
- **出处**：`references/sources/standards/jedec/JESD22-B116B_2.txt`
- **源文件**：`JESD22-B116B引线键合的剪切试验.pdf`
- **SHA256(16)**：`78c40073518ec3e4`

#### `JESD22-B117B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（17 节 / 17 数值行）
- **适用范围**：焊球剪切 Solder Ball Shear
- **关键条目**：★ 剪切（shear）而非拉脱；与 B115 区分
- **文档自述**：版本号 `JESD22-B117B`；日期线索 `（未识别到日期）`
- **规模**：19 页，文本层 9,659 字符
- **出处**：`references/sources/standards/jedec/JESD22-B117B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B117B：2014 Solder Ball Shear - 完整英文电子版（19页）_1_19_translate_20240815164936.pdf`
- **SHA256(16)**：`f8a9909e43797252`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 板级可靠性

#### `JESD22-B111A`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（18 节 / 37 数值行）
- **适用范围**：手持产品板级跌落试验
- **关键条目**：★ 板级（PCB 组装后）而非器件级；与 JESD22-B113 弯折互补
- **文档自述**：版本号 `IPC-9701A、J-STD-020、J-STD-033、JESD22-B110`；日期线索 `（未识别到日期）`
- **规模**：24 页，文本层 14,619 字符
- **出处**：`references/sources/standards/jedec/JESD22-B111A.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B111A：2016 Board Level Drop Test Method of Components for Handheld Electronic Products - 完整英文电子版（24页）_1_24_translate_20240815164218.pdf`
- **SHA256(16)**：`4a22b13a8757d4f8`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B113B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（14 节 / 29 数值行）
- **适用范围**：板级循环弯折（互连可靠性表征）
- **关键条目**：手持产品 SMT IC 互连弯折疲劳
- **文档自述**：版本号 `JESD22-B113B`；日期线索 `（未识别到日期）`
- **规模**：26 页，文本层 16,942 字符
- **出处**：`references/sources/standards/jedec/JESD22-B113B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B113B：2018 Board Level Cyclic Bend Test Method for Interconnect Reliability Characterization of SMT ICs for Handheld Electronic Products - 完整英文电子版（24页）_1_24_translate_20240815164421.pdf`
- **SHA256(16)**：`7e79c83de1436f3c`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 几何/外观

#### `JESD22-B100B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（0 节 / 0 数值行）
- **适用范围**：物理尺寸
- **关键条目**：外形尺寸测量方法
- **文档自述**：版本号 `JESD22、JESD22-B100B`；日期线索 `（未识别到日期）`
- **规模**：5 页，文本层 1,281 字符
- **出处**：`references/sources/standards/jedec/JESD22-B100B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B100B：2003 Physical Dimensions - 完整英文电子版（5页）_1_5_translate_20240815163533.pdf`
- **SHA256(16)**：`fec632c7e412ca08`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B101C`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（23 节 / 2 数值行）
- **适用范围**：外部目检 External Visual
- **关键条目**：外观验收准则；与 B118（晶圆/芯片背面）配套
- **文档自述**：版本号 `JESD22、JESD22-B100、JESD22-B101C、JESD22-B114`；日期线索 `2015`
- **规模**：13 页，文本层 5,802 字符
- **出处**：`references/sources/standards/jedec/JESD22-B101C.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B101C：2015 External Visual - 完整英文电子版（13页）_1_13_translate_20240815163437.pdf`
- **SHA256(16)**：`364bdf61d6b1ca21`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B108B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（2 节 / 1 数值行）
- **适用范围**：共面性 Coplanarity
- **关键条目**：表面贴装器件引脚/焊球共面性测量
- **文档自述**：版本号 `JESD22-B108B、JESD22-B112`；日期线索 `（未识别到日期）`
- **规模**：11 页，文本层 4,497 字符
- **出处**：`references/sources/standards/jedec/JESD22-B108B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B108B：2010 Coplanarity Test for Surface-Mount Semiconductor Devices - 完整英文电子版（11页）_1_11_translate_20240815163752.pdf`
- **SHA256(16)**：`53327def11e19499`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B112B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（30 节 / 11 数值行）
- **适用范围**：高温下封装翘曲测量
- **关键条目**：★ 与回流温度相关的动态翘曲；是 BGA 焊接良率的关键参数
- **文档自述**：版本号 `J-STD-020、JESD22、JESD22-A113、JESD22-B100`；日期线索 `（未识别到日期）`
- **规模**：27 页，文本层 11,304 字符
- **出处**：`references/sources/standards/jedec/JESD22-B112B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B112B ：2018 Package Warpage Measurement of Surface-Mount Integrated Circuits at Elevated Temperature - 完整英文电子版（27页）_1_27_translate_20240815164338.pdf`
- **SHA256(16)**：`f3d63f368f2fff0a`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B118`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（7 节 / 0 数值行）
- **适用范围**：晶圆与芯片背面外部目检
- **关键条目**：背面外观验收准则；与 B101（封装外观）配套
- **文档自述**：版本号 `JESD22-B118`；日期线索 `（未识别到日期）`
- **规模**：15 页，文本层 5,159 字符
- **出处**：`references/sources/standards/jedec/JESD22-B118.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B118 ：2011 Semiconductor Wafer and Die Backside External Visual Inspection - 完整英文电子版（15页）_1_15_translate_20240815165020.pdf`
- **SHA256(16)**：`d0029c6651248acc`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 标识

#### `JESD22-B107D`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（10 节 / 8 数值行）
- **适用范围**：标识永久性 Mark Permanency
- **关键条目**：溶剂擦拭后标识保留；与 B114（标识可读性）配套
- **文档自述**：版本号 `JESD22、JESD22-B107D`；日期线索 `（未识别到日期）`
- **规模**：11 页，文本层 4,237 字符
- **出处**：`references/sources/standards/jedec/JESD22-B107D.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B107D：2011 Mark Permanency - 完整英文电子版（11页）_1_11_translate_20240815163902.pdf`
- **SHA256(16)**：`abb9c30aff1133c5`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

#### `JESD22-B114B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（14 节 / 1 数值行）
- **适用范围**：标识可读性 Mark Legibility
- **关键条目**：字符可辨识度；与 B107（永久性）配套
- **文档自述**：版本号 `JESD22-B114B`；日期线索 `1990`
- **规模**：15 页，文本层 6,198 字符
- **出处**：`references/sources/standards/jedec/JESD22-B114B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-B114B：2020 Mark Legibility - 完整英文电子版（16页）_1_16_translate_20240815164604.pdf`
- **SHA256(16)**：`1d4d982d786536bc`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 环境腐蚀

#### `JESD22-A107C`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（0 节 / 0 数值行）
- **适用范围**：盐雾 Salt Atmosphere
- **关键条目**：盐雾浓度/温度/时长；考核引线框架与镀层
- **文档自述**：版本号 `JESD22、JESD22-A107C`；日期线索 `（未识别到日期）`
- **规模**：5 页，文本层 1,345 字符
- **出处**：`references/sources/standards/jedec/JESD22-A107C.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A107C：2013 Salt Atmosphere - 完整英文电子版（5页）_1_5_translate_20240815161321.pdf`
- **SHA256(16)**：`dd8ec7c9ceb08a8b`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 封装完整性

#### `JESD22-A109B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（0 节 / 0 数值行）
- **适用范围**：气密性 Hermeticity（细检/粗检）
- **关键条目**：氦细检泄漏率、氟碳粗检；判据按封装腔体积分档
- **文档自述**：版本号 `JESD22、JESD22-A109、JESD22-A109B、JESD22A`；日期线索 `（未识别到日期）`
- **规模**：6 页，文本层 1,392 字符
- **出处**：`references/sources/standards/jedec/JESD22-A109B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A109B：2011 HERMETICITY - 完整英文电子版（5页）_1_5_translate_20240815162032.pdf`
- **SHA256(16)**：`15a0354dae3b357f`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 预处理

#### `JESD22-A113I`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（20 节 / 27 数值行）
- **适用范围**：非气密封装器件可靠性试验前的预处理
- **关键条目**：★ 回流前烘烤 → 吸湿 → 3 次回流模拟 → 后续试验；与 J-STD-020 的 MSL 配合使用
- **文档自述**：版本号 `J-STD-020、J-STD-033、J-STD-035、J-STD-075`；日期线索 `2010`
- **规模**：36 页，文本层 20,025 字符
- **出处**：`references/sources/standards/jedec/JESD22-A113I.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A113I：2020 Preconditioning of Nonhermetic Surface Mount Devices Prior to Reliability Testing - 完整英文电子版（36页）_1_36_translate_20240815162658.pdf`
- **SHA256(16)**：`7fc990dc052aca27`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 工艺能力

#### `JESD22-A111B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（28 节 / 40 数值行）
- **适用范围**：整器件浸焊评估底面贴装能力
- **关键条目**：小外形表面贴装器件底部焊接的评估程序
- **文档自述**：版本号 `J-STD-020、J-STD-035、JESD22、JESD22-A111B`；日期线索 `（未识别到日期）`
- **规模**：20 页，文本层 11,174 字符
- **出处**：`references/sources/standards/jedec/JESD22-A111B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A111B ：2018 Evaluation Procedure for Determining Capability to Bottom Side Board Attach by Full Body Solder Immersion of Small Surface Mount Solid State Devices - 完整英文电子版（19页）_1_19_translate_20240815162305.pdf`
- **SHA256(16)**：`68d407db2eede0e9`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 存储器专项

#### `JESD22-A117E`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（23 节 / 38 数值行）
- **适用范围**：EEPROM 擦写耐久与数据保持
- **关键条目**：擦写循环次数 + 数据保持（高温烘烤后读）双考核
- **文档自述**：版本号 `JESD22、JESD22-A117E`；日期线索 `（未识别到日期）`
- **规模**：22 页，文本层 16,536 字符
- **出处**：`references/sources/standards/jedec/JESD22-A117E.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A117E：2018 Electrically Erasable Programmable ROM (EEPROM) Program Erase Endurance and Data Retention Stress Test- 完整英文电子版（21页）_1_21_translate_20240815162607.pdf`
- **SHA256(16)**：`9e25a919ddfd8a30`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 失效机理专项

#### `JESD22-A121A`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（28 节 / 19 数值行）
- **适用范围**：锡及锡合金镀层锡须生长测量
- **关键条目**：★ 锡须浸泡模式 = 5~10 min，等价 soak mode 2（A104 §5.5.3 有交叉引用）
- **文档自述**：版本号 `JESD22-A104、JESD22-A121、JESD22-A121A`；日期线索 `（未识别到日期）`
- **规模**：31 页，文本层 14,798 字符
- **出处**：`references/sources/standards/jedec/JESD22-A121A.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A121A(R2019) Test Method for Measuring Whisker Growth on Tin and Tin Alloy Surface Finishes - 完整英文电子版（29页）_1_29_translate_20240815163337.pdf`
- **SHA256(16)**：`3331b88d2976d143`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 材料表征

#### `JESD22-A120B`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（28 节 / 36 数值行）
- **适用范围**：有机材料水分扩散系数与溶解度测量
- **关键条目**：为吸湿仿真提供 D 与 S 参数；不是可靠性试验，是材料参数试验
- **文档自述**：版本号 `J-STD-020、JESD22-A120B`；日期线索 `2008`
- **规模**：13 页，文本层 6,798 字符
- **出处**：`references/sources/standards/jedec/JESD22-A120B.txt`
- **源文件**：`JEDEC JESD22/JEDEC JESD22-A120B：2014 Test Method for the Measurement of Moisture Diffusivity and Water Solubility in Organic Materials Used in Electronic Devices - 完整英文电子版（13页）_1_13_translate_20240815163200.pdf`
- **SHA256(16)**：`a6e630697a327d96`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 热测试

#### `JESD51-2A`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：集成电路热测试环境条件—自然对流（静止空气）
- **关键条目**：静止空气下的 Rθja 测试环境；与 JESD51-6 强制对流成对
- **文档自述**：版本号 `JESD51`；日期线索 `December 1995、January 2008、1995`
- **规模**：22 页，文本层 32,309 字符
- **出处**：`references/sources/standards/jedec/JESD51-2A.txt`
- **源文件**：`JESD51-2A：集成电路热测试方法环境条件——自然对流（静止空气）.pdf`
- **SHA256(16)**：`09b313ebf43ee869`

#### `JESD51-6`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：集成电路热测试环境条件—强制对流（流动空气）
- **关键条目**：风冷下的 Rθja 测试环境；风速与测试板规格相关
- **文档自述**：版本号 `JESD51`；日期线索 `March 1999、1999、2025`
- **规模**：20 页，文本层 32,039 字符
- **出处**：`references/sources/standards/jedec/JESD51-6.txt`
- **源文件**：`JESD51-6集成电路热测试方法环境条件——强制对流（流动空气）.pdf`
- **SHA256(16)**：`3d8f467a99d4896e`

### 电应力/ESD

#### `JS-001`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（59 节 / 34 数值行）
- **适用范围**：HBM 人体模型组件级 ESD 敏感度测试
- **关键条目**：★ 机翻件。JS-001-2017 新增 50V 测试级别与新分类（原文前言自述）；替代 JS-001-2014。分类等级须回英文原文核对
- **文档自述**：版本号 `JS-001-2010、JS-001-2012、JS-001-2014、JS-001-2017`；日期线索 `2010、2012、2014`
- **规模**：63 页，文本层 56,902 字符
- **出处**：`references/sources/standards/jedec/JS-001.txt`
- **源文件**：`JEDEC JESD22/ANSI ESDA JEDEC JS-001-2017 For Electrostatic Discharge Sensitivity Testing Human Body Model (HBM) -Component Level - 完整英文电子版（60页）_1_59_translate_20240815155533.pdf`
- **SHA256(16)**：`5d55bce3b2f1f887`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 封装/回流

#### `J-STD-020`　<span style='color:#888'>[L3 机器翻译在库]</span>

- **蒸馏状态**：🟢 digest（34 节 / 40 数值行）
- **适用范围**：非气密封装湿敏等级 MSL 分级与回流分类
- **关键条目**：★ 机翻件。MSL 1~6 分级、回流峰值温度与 profile；与 JESD22-A113 预处理配套使用
- **文档自述**：版本号 `J-STD-020、J-STD-020D、J-STD-020E`；日期线索 `2014`
- **规模**：23 页，文本层 25,278 字符
- **出处**：`references/sources/standards/jedec/J-STD-020.txt`
- **源文件**：`JEDEC JESD22/IPC JEDEC J-STD-020E：2014 Moisture Reflow Sensitivity Classification for Nonhermetic Surface Mount Devices - 完整英文电子版（22页）_1_22_translate_20240815155850.pdf`
- **SHA256(16)**：`52b8eb2da9962f78`
- **⚠ 引用限制**：机翻件——可引用数值与条款号，**术语必须回英文原文**

### 资格标准（裁判）

#### `JESD47L`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：集成电路应力试验驱动型资格考核
- **关键条目**：★ 中英对照双语。Table1 零失效样本量 / Table2 器件考核 / Table3 非易失存储器附加 / Table4 ELFR 样本量（60% 置信度）/ Table5 非气密封装 / Table6 气密封装 / Table7 变更选型 / Table8 键合最小拉力 / Table10 90% 置信度最大不良率。正文明确：ELFR 按 60% 置信度评估；通用数据可用卡方分布按 90% 置信限换算；单件昂贵器件可用 1/3 样本量
- **文档自述**：版本号 `JESD47K、JESD47L`；日期线索 `August 2018、December 2022、2018`
- **规模**：59 页，文本层 93,587 字符
- **出处**：`references/sources/standards/jedec/JESD47L.txt`
- **源文件**：`JEDEC-JESD47L.pdf`
- **SHA256(16)**：`30f731b3159a51d6`

### 设计/焊盘图形

#### `IPC-7351`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：表面贴装设计与连接盘图形通用要求（2005-02 原版）
- **关键条目**：★ 英文原文。2005 年 2 月版，取代 IPC-SM-782A（含修正 1&2）
- **文档自述**：版本号 `IPC-7351`；日期线索 `December 1999、February 2005、May 1995`
- **规模**：92 页，文本层 299,099 字符
- **出处**：`references/sources/standards/ipc/IPC-7351.txt`
- **源文件**：`IPC_7351 表面贴装设计及连接盘图形标准通用要求-en.pdf`
- **SHA256(16)**：`c5ada1cb16b85844`

#### `IPC-7351B`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：表面贴装设计与连接盘图形通用要求（2010-06 B 版）
- **关键条目**：★ 英文原文。取代 IPC-7351A（2007-02）；含密度等级 A/B/C 与焊盘生成公式
- **文档自述**：版本号 `IPC-7351A、IPC-7351B`；日期线索 `February 2007、June 2010、May 1995`
- **规模**：112 页，文本层 378,845 字符
- **出处**：`references/sources/standards/ipc/IPC-7351B.txt`
- **源文件**：`IPC-7351B - Generic Requirements for Surface Mount Design and Land Pattern Standard.pdf`
- **SHA256(16)**：`50ff86e25d564480`

### 封装/组装工艺

#### `IPC-7095D`　<span style='color:#888'>[L2 官方中文译本在库]</span>

- **适用范围**：BGA 设计与组装工艺的实施（2019，含修正 1）
- **关键条目**：★ 官方中文译本（IPC-7095D-WAM1 CN，取代 IPC-7095D-2018）。文档自带声明：中英冲突以英文版为准
- **文档自述**：版本号 `IPC-7095C、IPC-7095D、IPC-7095D-WAM1`；日期线索 `2013、2018、2019`
- **规模**：208 页，文本层 227,244 字符
- **出处**：`references/sources/standards/ipc/IPC-7095D.txt`
- **源文件**：`IPC-7095D-CHINESE  NP 2019-BGA 设计与组装工艺的实施.pdf`
- **SHA256(16)**：`ca64f9cc6e5d57f3`

### 试验方法

#### `IPC-TM-650-2.4.22c`　<span style='color:#888'>[L1 英文原文在库]</span>

- **适用范围**：印制板弓曲与扭曲（bow & twist）测量
- **关键条目**：★ 英文原文。三种程序；非矩形样品的特殊处理
- **文档自述**：版本号 `IPC-2422`；日期线索 `（未识别到日期）`
- **规模**：5 页，文本层 10,605 字符
- **出处**：`references/sources/standards/ipc/IPC-TM-650-2.4.22c.txt`
- **源文件**：`IPC-TM-650 2.4.22c.pdf`
- **SHA256(16)**：`92c29cd0a7b77614`

### 军标（试验方法）

#### `MIL-STD-883F`　<span style='color:#888'>[L4-OCR 扫描件已定向 OCR]</span>

- **适用范围**：微电子器件试验方法与程序 F 版
- **关键条目**：★ 扫描件，未文字识别。仅可声明持有（708 页全本 + 1-349/359-708 分卷）
- **文档自述**：版本号 `（未识别到版本号）`；日期线索 `（未识别到日期）`
- **规模**：—，文本层 0 字符
- **出处**：`references/sources/standards/mil_ocr/MIL-STD-883F.txt`
- **源文件**：`美军标 MIL-STD-883F.pdf`
- **SHA256(16)**：`8dd59bd8d9820838`

#### `MIL-STD-883K`　<span style='color:#888'>[L4-OCR 扫描件已定向 OCR]</span>

- **适用范围**：微电子器件试验方法与程序 K 版
- **关键条目**：★ 扫描件，未文字识别。仅可声明持有（768 页全本 + 1-399/400-768 分卷）
- **文档自述**：版本号 `（未识别到版本号）`；日期线索 `（未识别到日期）`
- **规模**：—，文本层 0 字符
- **出处**：`references/sources/standards/mil_ocr/MIL-STD-883K.txt`
- **源文件**：`美军标 MIL-STD-883K.pdf`
- **SHA256(16)**：`e3ab56a8e0c314bb`

### 国军标（试验方法）

#### `GJB-548B`　<span style='color:#888'>[L4-OCR 扫描件已定向 OCR]</span>

- **适用范围**：微电子器件试验方法和程序 B 版（2005）
- **关键条目**：★ 扫描件，未文字识别。仅可声明持有（393 页全本 + 1-199/200-396 分卷）
- **文档自述**：版本号 `（未识别到版本号）`；日期线索 `（未识别到日期）`
- **规模**：—，文本层 0 字符
- **出处**：`references/sources/standards/mil_ocr/GJB-548B.txt`
- **源文件**：`国军标GJB 548B-2005微电子器件试验方法和程序.pdf`
- **SHA256(16)**：`fd1a6e47f63bb665`

#### `GJB-548C`　<span style='color:#888'>[L4-OCR 扫描件已定向 OCR]</span>

- **适用范围**：微电子器件试验方法和程序 C 版（2021）
- **关键条目**：★ 扫描件，未文字识别。仅可声明持有（460 页）
- **文档自述**：版本号 `（未识别到版本号）`；日期线索 `（未识别到日期）`
- **规模**：—，文本层 0 字符
- **出处**：`references/sources/standards/mil_ocr/GJB-548C.txt`
- **源文件**：`GJB 548C-2021-.pdf`
- **SHA256(16)**：`76d9085acf0c20d5`

---

## 四、机翻标准（L3）的条款级蒸馏

机翻件不能引用措辞，但**结构与数值可用**。已对全部 37 份 L3 标准生成条款级 digest，落在 `references/digests/`。

| 指标 | 数量 |
|---|---|
| 已蒸馏 L3 标准 | 37 份 |
| 提取出的章节条目 | 672 |
| 其中条款号需还原 | 136（20%）|
| 提取出的数值条件行 | 565 |
| 命中的机翻术语错误 | 431 次 |

### ★ 条款号错位：机翻件的第三个缺陷（本轮新发现）

实测机翻件有约 **20% 的条款号存在确定性错位**——**首位数字被移到末尾**：

| 语料里写的 | 实际应为 | 验证依据 |
|---|---|---|
| `.32` | `2.3` | A104F 上下文夹在 2.2 与 2.4 之间 |
| `.162` | `2.16` | 同上（A104F 第 2 章末条） |
| `.21` | `1.2` | J-STD-020 目录：`1.1范围` / `.21背景` / `.31术语和定义` 顺序 |
| `.32.联合行业标准` | `2.3 联合行业标准` | J-STD-020 正文：`2.1` / `2.2` / 此条 |

→ 错位是**可逆的**，digest 已按规则还原并标注 `（还原）`。
→ 但**直接读机翻件原文时看到的条款号是错的**，这比术语错误更隐蔽。

**完整清单**：`references/digests/_INDEX.md`　**机读索引**：`references/digests/_index.json`

### 机翻术语纠错表（已核实，逐条对齐英文原件）

| 机翻译法 | 应为 | 英文原词 | 核实依据 |
|---|---|---|---|
| 「模具垫」 | **芯片焊盘 / 芯片键合垫** | `die pad` | B116B 机翻 L95「模具垫金属化」↔ 英文原件 L206「the die pad metallization」 |
| 「模具」 | **芯片 / 裸片** | `die` | B116B 机翻 L202「模具的表面与剪切工具的剪切面」↔ 英文 L461「surface of the die … shearing plane」 |
| 「球键」 | **球焊点** | `ball bond` | B116B 机翻 L68「球键的质量」↔ 英文 L149 上下文 ball bond |
| 「线束」 | **键合线** | `wire bond` | B116B 机翻「线束剪切试验」↔ 英文标题「Wire Bond Shear Test Method」 |
| 「热膜」 | **热超声** | `thermosonic` | B116B 机翻 L69「热膜（球）键」↔ 英文 L153「thermosonic (ball) bonds」 |
| 「针线」 | **针脚焊点** | `stitch bond` | B116B 机翻 L73「通常为针线」↔ 英文 L162「typically a stitch bond」 |
| 「冶金键」 | **冶金结合** | `metallurgical bond` | B116B 机翻 L67「已形成的冶金键」↔ 英文 L149「the metallurgical bond」 |
| 「骰子」 | **芯片 / 晶粒** | `dice` | J-STD-020 目录「JEP160 电子固态晶片、骰子和设备…」↔ JEP160 英文标题「Wafers, Dice, and Devices」 |
| 「偏见」 | **偏压 / 偏置** | `bias` | A110E「偏见指南」= Bias Guidelines；同一文件他处已用「偏置」，前后不一致 |
| 「偏差」 | **偏压 / 偏置** | `bias` | A110E L159「连续或周期性偏差」——同一文件内 bias 有「偏见/偏差/偏置」三种译法 |

> 用法：读到左列词时**心里替换成中间列**，引用时用英文原词。
> 这样 L3 语料就从「完全不可用」变成「可用但需转译」。

---

## 五、扫描件（军标 / 国军标）

以下军标/国军标在库，PDF 为**纯图像扫描**（每页一张图，0 字符文本层）。

| 标准 | 类别 | 持有文件 | OCR 进度 | 备注 |
|---|---|---|---|---|
| `GJB-548B` | 国军标（试验方法） | `国军标GJB 548B-2005微电子器件试验方法和程序.pdf`（全本）；`国军标GJB 548B-2005微电子器件试验方法和程序200-396.pdf`（分卷）；`国军标GJB 548B-2005微电子器件试验方法和程序1-199.pdf`（分卷） | 393 页 | ★ 扫描件，未文字识别。仅可声明持有（393 页全本 + 1-199/200-396 分卷） |
| `GJB-548C` | 国军标（试验方法） | `GJB 548C-2021-.pdf`（全本） | 460 页 | ★ 扫描件，未文字识别。仅可声明持有（460 页） |
| `MIL-STD-883F` | 军标（试验方法） | `美军标 MIL-STD-883F.pdf`（全本）；`美军标 MIL-STD-883F(359-708).pdf`（分卷）；`美军标 MIL-STD-883F(1-349).pdf`（分卷） | 9 页 | ★ 扫描件，未文字识别。仅可声明持有（708 页全本 + 1-349/359-708 分卷） |
| `MIL-STD-883K` | 军标（试验方法） | `美军标 MIL-STD-883K.pdf`（全本）；`美军标 MIL-STD-883K(400-768).pdf`（分卷）；`美军标 MIL-STD-883K(1-399).pdf`（分卷） | 102 页 | ★ 扫描件，未文字识别。仅可声明持有（768 页全本 + 1-399/400-768 分卷） |

> **OCR 的现实约束**（实测数据，非推测）：本机 OCR 实测 **36~130 秒/页**（RapidOCR PP-OCRv3，onnxruntime CPU；已试 1.30.0 与 1.22.0 两个版本、dpi 100/150/200/300 四档、强制 CPU 与默认两种 providers 配置，最快 36 s/页）。
> 4 个军标合计 **2,229 页** → 全量 OCR 需约 **22~80 小时**，不具可行性。
>
> 因此采用**定向 OCR**：优先识别每份军标的**目录与方法索引页**（这是军标最有价值的部分——完整的方法号清单），而非全本。

---

## 六、军标方法索引（OCR 产出）

> **来源**：本库对军标扫描件**目录页**的 OCR。**引用层级 L4-OCR**。
>
> **方法号可信**（四位数字）→ 可用于定位；**标题为 OCR 产物，引用前必须核对原页**。

| 标准 | 方法号 | 有标题 | 目录页来源 | 同源参考 | 号段不连续处 |
|---|---:|---:|---:|---:|---|
| `GJB-548B` | 75 | 72 | 70 | 5 | 1xxx 1005、1018、1024~1029；2xxx 2008、2017、2033~2034 |
| `GJB-548C` | 74 | 70 | 50 | 24 | 2xxx 2008、2018、2024、2033~2034 |
| `MIL-STD-883F` | 76 | 58 | 76 | 0 | 1xxx 1004~1005、1018~1021、1024~1029；2xxx 2002~2003、2005、2011~2012、2015、2018~2019、2023、2031、2033~2034；3xxx 3002~3004、3010、3012；4xxx 4004~4006；5xxx 5005、5007~5008 |
| `MIL-STD-883K` | 105 | 81 | 105 | 0 | 1xxx 1018、1024~1029；2xxx 2004、2023、2033~2034 |

### 交叉校验（GJB 548 与 MIL-STD-883 方法号同源）

| 标准 | 与 883 重合 | 仅本标准有 | 结论 |
|---|---|---|---|
| `GJB-548B` | **74/75 = 99%** | ['2023'] | 两侧方法号高度一致，互为独立佐证 |
| `GJB-548C` | **73/74 = 99%** | ['2023'] | 两侧方法号高度一致，互为独立佐证 |

> **这个校验的价值**：GJB 548 源自 MIL-STD-883，两者方法号应一致。
> 实测 99% 重合，说明**两侧的 OCR 与解析都没有系统性错位** ——
> 这是对方法索引可信度的一个独立验证，不是自证。

**完整清单**：`references/MIL-METHODS.md`（330 条）　**机读**：`references/mil-methods.json`

---

## 七、已知的资料缺口

| 缺口 | 影响 |
|---|---|
| JESD22 系列 37 份均无英文原文 | 术语类问题必须回 JEDEC 官网核对，不能凭本库作答 |
| 机翻件条款号 20% 错位 | 引用条款号前必须回英文原文核对（digest 已还原，原语料未改） |
| MIL-STD-883F/K、GJB 548B/C 为扫描件 | 全量 OCR 不可行（22~80 小时），仅做定向 OCR |
| A104 在库版本为 **F（2020-11）**，非 **F.01** | 引用 F.01 独有内容时须标「本库未持有」 |
| 无 IEC 60749 系列正文 | 涉及 IEC 的引用只能依赖 AQG 324 的引用表与二手资料 |
| 无 AEC-Q100 正文 | 车规 IC 资格问题只能依赖 AQG 324 与 JESD47 |
| 企业标准（VW80000/GMW/USCAR、客户 TS）均不可得 | 涉及时只能给反查路径 |

> 缺口必须在回答中**显式声明**。宁可说「本库未覆盖，需回原文确认」，
> 也不要给出看似完整但无出处的答案。
