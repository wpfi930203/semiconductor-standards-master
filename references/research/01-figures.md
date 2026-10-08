# Track 01 — Figures（行业大佬 / 关键人物与组织）

> **调研定位**：本track 记录「标准背后的 人」。聚焦**标准制定者**与**可靠性方法奠基人**，而非商业人物。
>
> **调研日期**：2026-10-05
> **调研方法**：以 Crossref API（权威 DOI 元数据）、JEDEC/IEC/ECPE/AEC 官方站点、学术出版商页面为主；辅以技术媒体。
>
> **可信度标注约定**：
> - `[一手]` = 标准组织官方页面 / 出版商 DOI 记录 / 官方 PDF
> - `[权威]` = 同行评审期刊/会议，或权威教材
> - `[媒体]` = 技术媒体、会议讲者页、二手转述
> - `[未核实]` = 检索未能确认，**不得写入 skill 作为事实**
>
> ---
>
> ## ⚠️ 首要警告：本track 中最常见的 6 个错误
>
> 本次调研发现了若干**广泛流传但错误**的「人名/模型名」。这些错误在中文技术圈尤其普遍，因为二手转述经常音译或臆造。**在写入 skill 前必须先纠正**：
>
> | 错误说法（常见误传） | 正确事实 | 证据等级 |
> |---|---|---|
> | "**Darcy** 模型"（焊点疲劳） | 是 **Darveaux** 模型，提出者 **Robert Darveaux**（Amkor Technology）。中文资料常误写为 Darcy | [一手] Crossref DOI `10.1115/1.1413764` |
> | "**Zard**" 是 TDDB/HTOL 领域奠基人 | **完全检索不到该人名**。TDDB 领域公认奠基人是 **J. W. McPherson**（Joe W. McPherson）。任务描述中"Martin A.綿?"亦无法确认 | [未核实]，见§1.5 |
> | "**Peck 1974**" | Peck 湿热模型的关键文献是 **1973**（IRPS）与 **1986**（IRPS），不是 1974 | [一手] Crossref DOI `10.1109/irps.1973.362586` / `10.1109/irps.1986.362110` |
> | "**Specht 加速模型**"与"**SN 加速关系**"是同一人/同一报告 | Specht 的加速模型综述报告确有其文，但 "SN 加速关系"未在任何一手来源中检索到，**疑为对Specht 报告内容的误记或与 Snively 混淆** | [未核实] |
> | "**Navraj S. Sandhu**（X-FAB）" | 姓名与机构未能一手核实。检索到的相关书作者为 **Navraj S. Sandhu**（书名对得上），但 **X-FAB 任职关系未核实** | [部分核实]，见§1.4 |
> | "LESIT 模型提出者含 Pascal LESIT 团队 / L.M.J. / Duval" | **"Pascal LESIT"不是人名**（LESIT 是项目缩写 Low Effort Solder Interconnect Test）。可核实的相关人员是 **Reinhold Bayerer**（Infineon）与 **Josef Lutz**（同为 CIPS08 相关作者），但 LESIT 原始提案人未一手确认 | [未核实]，见§2 |

---
>
> ## 1. 可靠性物理模型的提出者（技术层面的大师）
>
> ### 1.1 D. Stewart Peck — 湿热（power law）加速模型
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | D. Stewart Peck（部分文献署名 D. S. Peck） |
> | **所属机构** | Bell Laboratories, Allentown, PA（**已证实**，见下方1979 年论文的 Crossref 机构字段） |
> | **领域贡献（一句话）** | 提出湿热加速的"Peck 模型"——逆幂律（RH<sup>-n</sup>）与Arrhenius 温度项相乘，是 JESD22-A101 温湿偏试验与 HAST/H3TRB 加速因子计算的理论基石 |
> | **代表文献** | ① D. S. Peck, C. H. Zierdt, *"Temperature-Humidity Acceleration of Metal-Electrolysis Failure in Semiconductor Devices"*, **11th Reliability Physics Symposium (IRPS), 1973, pp. 146-152**, DOI `10.1109/irps.1973.362586` [一手]<br>② D. Stewart Peck, *"Comprehensive Model for Humidity Testing Correlation"*, **24th IRPS, 1986, pp. 44-50**, DOI `10.1109/irps.1986.362110` [一手]<br>③ D. S. Peck, *"New concerns about integrated circuit reliability"*, IEEE Trans. Electron Devices, vol. 26, no. 1, pp. 38-43, Jan 1979（**Crossref 机构字段明确标注 Bell Laboratories, Allentown, PA**）[一手] |
> | **关键参数** | Peck 1986 论文中报告 **n = 2.7, Ea = 0.79 eV**（来源：Accendo Reliability 技术文，引用 Peck 原文与 Nelson 讨论）[媒体，但两处独立来源一致] |
> | **值得读** | ① Peck 1986 IRPS 论文（模型本体，14 页短文，必读）<br>② Wayne B. Nelson, *Accelerated Testing: Statistical Models, Test Plans, and Data Analysis*, Wiley, 1990（**Peck 模型的统计侧权威教科书**，多篇二手文献的 n/Ea 取值来源）<br>③ JEDEC **JESD22-A101D.01**（2021-01）标准正文（见 §3.1） |
> | **是否仍活跃** | **已故/退休**。Peck 生涯跨度约 1960s-1980s，2019 年后未见新作品。**推断，非直接证据** |
> | **来源 URL** | `https://api.crossref.org/works/10.1109/irps.1986.362110`；`https://api.crossref.org/works/10.1109/irps.1973.362586`；`https://accendoreliability.com/temperature-humidity-accelerated-life-testing/` |
>
> **对用户的价值**：Peck 模型是**唯一**一个把「湿度」显式写进加速因子的工业标准模型。做 THB/HAST/H3TRB 试验设计时，n 和 Ea 的取值直接决定加速倍数。常见坑：n 常被取 2~4（电化学迁移）、Ea 0.4~0.9 eV，但**必须按自己的封装体系重新拟合**。
>
> ---
>
> ### 1.2 J. W. (Joe W.) McPherson — TDDB / 介质击穿模型的四十年第一人
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | J. W. McPherson（全名 Joe W. McPherson；部分文献署名 James W. McPherson） |
> | **所属机构** | 历经 **Texas Instruments Inc., Dallas, TX**（2002 年著作机构字段）→ 现 **McPherson Reliability Consulting LLC, 2805 Shelton Way, Plano, Texas 75093, USA**（2023/2025 年论文机构字段）[一手] |
> | **领域贡献（一句话）** | 系统化TDDB 的 E-model / 1/E-model / power-law(VN-model) / thermodynamic(VF-model) 物理模型族，是 HTOL/TDDB 试验应力条件设计与外推的**理论裁判** |
> | **代表文献** | ① **J. W. McPherson, *"Four Decades of E-Model Development for Time-Dependent Dielectric Breakdown (TDDB)"*, IEEE Electron Devices Reviews, vol. 2, pp. 253-263, 2025**, DOI `10.1109/edr.2025.3620381` [一手，**最新、最重要的综述，2025 年发表，必读**]<br>② J. W. McPherson, *"Time dependent dielectric breakdown physics – Models revisited"*, Microelectronics Reliability, vol. 52, pp. 1753-1760, 2012, DOI `10.1016/j.microrel.2012.06.007` [一手]<br>③ J. W. McPherson, *"On why dielectric breakdown strength reduces with dielectric thickness"*, IRPS 2016, pp. 3A-3-1~3A-3-8, DOI `10.1109/irps.2016.7574512` [一手]<br>④ J. W. McPherson, *"Physics and Chemistry of Intrinsic Time-Dependent Dielectric Breakdown in SiO₂ Dielectrics"*, in *Selected Topics in Electronics and Systems: Oxide Reliability*, World Scientific, 2002, pp. 135-171 [一手]<br>⑤ J. W. McPherson & D. A. Wesson, *"Disturbed bonding states in SiO₂ thin-films and their impact on TDDB"*, IRPS 1998, pp. 47-56（含 **H. C. Mogul**，TI）[一手] |
> | **代表标准关联** | TDDB 试验方法对应 **JESD22-A108**（Gate Oxide Reliability）；AQG 324 / IEC 63275 系列中的栅氧相关测试均引其模型体系 |
> | **值得读** | ① 2025 年 EDR 综述（一篇顶掉十篇）<br>② 2012 年 "Models revisited"（对各模型适用边界的批判性梳理）<br>③ McPherson 著 ***Reliability Physics and Engineering: Tools, Diagrams, Stress Models, Accelerated Testing***, Springer（2013 初版，399 页，ISBN 978-3-319-00329-7 系列）[权威，OpenLibrary 记录 ISBN 3319001221 / 9783319001210 等多个版本] |
> | **是否仍活跃** | **是，明确活跃**。2025 年仍在 IEEE Electron Devices Reviews 发表综述，2026 年 IRPS 论文中亦有合作者引用 |
> | **来源 URL** | `https://api.crossref.org/works/10.1109/edr.2025.3620381`；`https://api.openalex.org/works?search=humidity+effects+...`（用于交叉验证）；OpenLibrary `https://openlibrary.org/search.json?q=Reliability+Physics+and+Engineering` |
>
> **对用户的价值（对本知识 OS 最重要的一条）**：McPherson 2025 年那篇 EDR 综述的标题就是「**Four Decades of E-Model Development**」。当有人告诉你「用 1/E model 外推 TDDB 更保守/更准确」时，答案在这篇里。**这篇应作为 skill 中 TDDB 章节的锚点文献。**
>
> ---
>
> ### 1.3 Wayne B. Nelson — 加速试验统计设计的实际奠基人
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | Wayne B. Nelson |
> | **所属机构** | **General Electric Company, New York**（1982 年 *Applied Life Data Analysis* 出版机构；后为顾问）[权威，NCCU 机构典藏的参考文献条目] |
> | **领域贡献（一句话）** | 加速试验的**统计设计**奠基人：最优截尾加速试验计划、阶梯应力模型、Weibull/对数正态下的最优应力分配 |
> | **代表文献** | ① Wayne B. Nelson, *Accelerated Testing: Statistical Models, Test Plans, and Data Analysis*, John Wiley & Sons, New York, **1990**（**该领域被引用最多的教科书**，多次再版）[权威]<br>② W. B. Nelson, *"Accelerated Life Testing: Step-Stress Models and Data Analysis"*, IEEE Trans. Reliability, vol. R-29, no. 2, pp. 103-108, 1980 [权威，NCCU 参考文献著录]<br>③ W. Q. Meeker & W. B. Nelson, *"Optimum accelerated life-tests for the Weibull and extreme value distributions"*, IEEE Trans. Reliability, vol. R-24, no. 5, pp. 321-332, **1975**, DOI `10.1109/TR.1975.5214922` [一手，Crossref 确认 DOI]<br>④ W. Nelson, *"Analysis of Accelerated Life Test Data"*, IEEE Trans. Electrical Insulation, Part I (E1-6, no. 4, 1971, pp. 165-181) / Part II (E1-7, no. 1, 1972, pp. 36-55) / Part III (E1-7, no. 2, 1972, pp. 99-119) [权威] |
> | **值得读** | ① 1990 年教科书（**唯一的系统性入口**）<br>② 1975 年Meeker & Nelson 论文（理解"为什么要最优分配应力点"的源头） |
> | **是否仍活跃** | **不活跃**。教科书最后再版约2004 年（ISBN 978-0-471-69736-2）。**推断** |
> | **来源 URL** | `https://api.crossref.org/works/10.1109/TR.1975.5214922`；`https://nccur.lib.nccu.edu.tw/handle/140.119/90495`（参考文献著录）；`https://ro.vvikipedla.com/wiki/Points_of_failure`（书目信息） |
>
> **对用户的价值**：做**分组/阶梯加速试验设计**时，「几组应力、每组几个样品、总共多少失效」不是拍脑袋，是有最优解理论的。Meeker & Nelson 1975 给出了 Weibull 与极值分布下的最优计划。
>
> ---
>
> ### 1.4 Navraj S. Sandhu — 半导体失效物理与可靠性（部分核实）
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | Navraj S. Sandhu（缩写 N. S. Sandhu） |
> | **所属机构** | **X-FAB 任职关系：[未核实]**。见下方说明 |
> | **领域贡献（一句话）** | 撰写《Reliability and Failure Physics of Electronic Devices and Materials》，是**唯一一本以"器件+材料"全栈视角系统讲失效物理的专著** |
> | **代表文献** | **N. S. Sandhu, *Reliability and Failure Physics of Electronic Devices and Materials*, Academic Press / Elsevier** [部分核实：书名与作者在检索中反复出现，但**未能从Crossref/OpenLibrary 取得权威书目记录**] |
> | **值得读** | ① Sandhu 上述专著<br>② Milton Ohring & Lucian A. Kasprzak, ***Reliability and Failure of Electronic Materials and Devices***, Academic Press（**书目已一手证实**：1998 初版，Ohring；2007 版加入 James R. Lloyd；2015 版 Ohring + Kasprzak。ISBN 见 OpenLibrary）[权威] |
> | **是否仍活跃** | **未核实** |
> | **来源 URL** | OpenLibrary `https://openlibrary.org/search.json?q=Reliability+of+Electronic+Materials+and+Devices+Ohring` |
>
> **⚠️ 诚实说明**：**X-FAB 与 Sandhu 的绑定关系本次未能一手核实。** Crossref 以"Sandhu + reliability"检索返回的是同名他人的无关结果（复合材料、射频等）。检索中出现的 **N. S. Sandhu（1993, Nuclear Instruments and Methods B, 与 M.A. Sarfaraz、You-Wen Yau 合作，陶瓷电子封装）** 与 **R. S. Sandhu（AFIT 复合材料）** 均为不同人。
> **写入 skill 时的处理建议**：写"Navraj S. Sandhu 著作《Reliability and Failure Physics of Electronic Devices and Materials》"（书名可查，但出版社/年份需再核），**不要写"X-FAB"**。
>
> **替代推荐（书目已完全核实）**：**Milton Ohring（Stevens Institute of Technology）+ Lucian A. Kasprzak**的 *Reliability and Failure of Electronic Materials and Devices*，Academic Press，1998/2007/2015 三版。这本书的传承关系本身就是个信息点：Ohring（2007 年后由 James R. Lloyd 接手）→ Kasprzak（2015 版接手）。
>
> ---
>
> ### 1.5 关于"Specht / Snively / Gall / Verson / McGann / Zard" — 核实结果
>
> 这一组是任务清单中风险最高的部分。**逐条如实报告**：
>
> | 人物 | 核实结论 | 说明 |
> |---|---|---|
> | **E. J. Specht** | **[部分核实]** 其加速模型综述报告在加速寿命试验文献中被广泛引用为经典来源；但**本次未能取得报告原文或DTIC/Archive.org 的一手书目记录**（DTIC 与 archive.org 在本环境下均不可访问，Web 搜索结果被无关内容淹没）。NSWC/美国海军的机构归属**未核实** | 检索中出现的"Sir Donald McGann"、"Henry A. Schade"、"John Stapp"等均为同名或无关人物，**不可采用** |
> | **William E. Snively** | **[未核实]**。Crossref 以"Snively + acceleration model"检索仅返回核物理领域（"Novel Structure Acceleration"，G. Andonian & E. Snively, NIM-A, 2025）与 Raytheon 的封装 SAM 分析（Todd Snively, Bruce Oliver, John Goings, SMTA International, 2001）——**均非加速模型奠基人** | ⚠️ **"SN 加速关系"未在任何来源中出现。高度存疑，建议 skill 中不写** |
> | **Leslie A. Gall** | **[未核实]**。未检��到 Gall 的温度加速模型原始文献 | 检索到的 "William A. Gallus Jr." 是气象学家（Iowa State University，天气预报），**完全无关** |
> | **R. A. Verson** | **[未核实]**。应力-寿命曲线（stress-life curve）本身是 S-N 曲线的标准术语，但未找到以该人命名的独立模型 | 建议 skill 中不写 |
> | **Edward J. McGann** | **[未核实]**。检索返回的"Donald McGann"为美国海军水面作战中心（NSWC）**退役指挥官、时任历史与遗产司令部负责人**，2011 年曾到访中国舰艇研究院并作报告——**他是海军官员，不是加速模型提出者**。任务描述中"Edward J. McGann 等"与该人**无法建立关联** | ⚠️ 高度存疑 |
> | **Christoph Zard** | **[未核实——检索无任何结果]** | ⚠️ 该人名在 TDDB/HTOL 语境下**完全检索不到**。TDDB 领域的奠基人已由 Crossref 确认为 **J. W. McPherson**（§1.2）。**建议 skill 中删除 "Zard"** |
> | "Martin A.綿?" | **无法核实**（原始任务描述中该名字本身残缺） | 建议放弃 |
> | **Arrhenius 适用性争议** | **未核实具体代表人物**。但可确认这一争议的**技术焦点**：McPherson 2012/2025 两篇论文的核心论点即「不同击穿模型（E / 1/E / power-law / thermodynamic）**都能同样好地拟合高场加速数据，却在使用条件下外推得彼此差异极大**」（IEEE Electron Devices Reviews 2025 与 IRPS 2026 引文均如此表述）[一手，McPherson 论文摘要] | ✅ **争议的实质已核实：这是"外推失效性"之争，不是"谁对谁错"之争** |
>
> ---
>
> ## 2. 焊点/功率模块可靠性模型的提出者
>
> ### 2.1 Robert Darveaux — 能量法焊点疲劳模型（"Darveaux 模型"，非"Darcy"）
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | **Robert Darveaux**（部分早期文献署名 R. Darveaux） |
> | **所属机构** | 历经 **Motorola**（1990s，提出模型时）→ **Amkor Technology Inc., 1900 S. Price Rd., Chandler, AZ 85286** → **Skyworks Solutions, Irvine, CA**（2013）→ **Arizona State University, Dept. of Electronic Systems**（2007，双挂职）[全部一手，Crossref 机构字段] |
> | **领域贡献（一句话）** | 提出**体积加权平均非弹性功密度**驱动的焊点疲劳寿命模型：把「裂纹萌生循环数」与「裂纹扩展速率」解耦，是能量法（energy-based）焊点寿命模型的**事实标准** |
> | **模型形式** | 萌生：N₀ = K₁·ΔW^(-K₂)；扩展：da/dN = K₃·ΔW^(-K₄)；特征寿命 N_f = N₀ + a/(da/dN)。ΔW = 非弹性应变能密度 = 应力-应变迟滞回线面积 |
> | **代表文献** | ① **R. Darveaux, *"Effect of Simulation Methodology on Solder Joint Crack Growth Correlation and Fatigue Life Prediction"*, Journal of Electronic Packaging, vol. 124, pp. 147-154, 2002**, DOI `10.1115/1.1413764` [一手]<br>② R. Darveaux, A. Mawer, *"Solder joint fatigue life of fleXBGA/sup assemblies"*, ECTC 1998, pp. 707-712, DOI `10.1109/ectc.1998.678776` [一手]<br>③ Robert Darveaux, Jim Heckman, Ahmer Syed, Andrew Mawer, *"Solder joint fatigue life of fine pitch BGAs – impact of design and material choices"*, Microelectronics Reliability, vol. 40, pp. 1117-1127, 2000, DOI `10.1016/s0026-2714(00)00038-x` [一手]<br>④ R. Darveaux, *"Effect of simulation methodology on solder joint crack growth correlation"*, ECTC 2000, pp. 1048-1058, DOI `10.1109/ectc.2000.853299` [一手]<br>⑤ **Darveaux et al., *"Thermal Cycle Fatigue Life Prediction for Flip Chip Solder Joints"*, ECTC 2014, pp. 703-711**, DOI `10.1109/ectc.2014.6897361` [一手，**晚年的封装级应用**] |
> | **值得读** | ① **Arizona State 的 "Revisit of life-prediction model for solder joints"**（**技术细节极重要，见下**）<br>② ECTC 2014 论文（现代封装应用） |
> | **关键工程陷阱（必读）** | ⚠️ **Darveaux 模型的参数曾因 ANSYS 版本缺陷而全部作废并重算**。原参数由 Darveaux 用**旧版 ANSYS** 拟合曲线得到；**Anderson 等人发现旧版 ANSYS 计算的塑性功密度（plastic work density）是错误的**；Darveaux 随后用修正版 ANSYS **重新计算了全部参数**。任何引用旧参数的文献都应怀疑。[权威，Arizona Board of Regents 机构库论文摘要明确记载此事] |
> | **是否仍活跃** | **是**。2014 年仍有 ECTC 论文 |
> | **来源 URL** | `https://api.crossref.org/works?query.author=Darveaux&...`；`https://experts.azregents.edu/en/publications/revisit-of-life-prediction-model-for-solder-joints` |
>
> ### 2.2 Reinhold Bayerer — Bayerer / CIPS08 模型（功率循环领域最复杂的解析模型）
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | **Reinhold Bayerer**（早期文献署名 R. Bayerer） |
> | **所属机构** | **Infineon Technologies AG**（多处一手机构字段：Warstein, Germany；Neubiberg；Erlangen）[一手] |
> | **领域贡献（一句话）** | 提出 **Bayerer 模型（= CIPS08 模型）**：在 Coffin-Manson 基础上引入 **6 个变量**（ΔT_j、T_j-max、t_on、I、V、D），是**变量最多的解析寿命模型**，也是 Semikron Danfoss 等厂家的功率循环数据拟合基础 |
> | **模型形式** | N_f = K·(ΔT_j)^β1 · exp(β₂/(T_j+273)) · t_on^β3 · I^β4 · V^β5 · D^β6<br>其中 I = 单键合线电流、V = 阻断电压/100、D = 键合线直径 |
> | **代表文献** | ① **R. Bayerer, *"Advanced packaging yields higher performance and reliability in power electronics"*, Microelectronics Reliability, vol. 50, pp. 1715-1719, 2010**, DOI `10.1016/j.microrel.2010.07.016` [一手]<br>② **P. Friedrichs, R. Bayerer, *"SiC High Power Devices – Challenges for Assembly and Thermal Management"*, Materials Science Forum, vol. 740-742, pp. 869-872, 2013**, DOI `10.4028/www.scientific.net/msf.740-742.869` [一手]<br>③ C. Herold, P. Seidel, **J. Lutz**, **R. Bayerer**, *"Topologies for inverter like operation of power cycling tests"*, Microelectronics Reliability, vol. 64, pp. 453-457, 2016, DOI `10.1016/j.microrel.2016.07.130` [一手]<br>④ T. Herrmann, M. Feller, **J. Lutz**, **R. Bayerer**, T. Licht, *"Power cycling induced failure mechanisms in solder layers"*, EPE 2007, pp. 1-7, DOI `10.1109/epe.2007.4417702` [一手]<br>⑤ R. Bayerer, M. Lassmann, S. Kremp, *"Transient Hygrothermal-Response of Power Modules in Inverters"*, IEEE Trans. Power Electronics, vol. 31, pp. 613-620, 2016, DOI `10.1109/tpel.2015.2408117` [一手] |
> | **公开参数（可直接用于拟合初值）** | ① **Bayerer 原始值**（MDPI Energies 2024 综述著录）：β₁=-3.483, β₂=1917, β₃=-0.438, β₄=-0.717, β₅=-0.751, β₆=-0.564 [权威期刊综述]<br>② **Infineon EasyPACK（复现值）**：K=2.03×10¹⁴, β₁=-4.416, β₂=1285, β₃=-0.463, β₄=-0.716, β₅=-0.761, β₆=-0.5 [同上 + Energies 13, 3355 (2020) 独立印证]<br>**规律：主要变的是 β₁、β₂，β₃~β₆ 高度一致。** 这是极实用的工程经验 |
> | **适用边界（关键）** | ⚠️ **Bayerer 模型的参数只适用于绝缘基片材料为 Al₂O₃ 的模块，不适用于 AlN 和 AlSiC 基片** [权威，《机车车辆牵引逆变器 IGBT 模块的结温与疲劳寿命计算》明确指出]。这正是 SiC 时代的一个真实痛点 |
> | **值得读** | ① Microelectronics Reliability 2010 那篇（Bayerer 自述）<br>② MDPI *Energies* 17(11):2616 (2024) 的对比评估（有完整参数表）<br>③ Energies 13(14):3355 (2020) 的 Aalborg 大学论文（参数 + 适用温区：T_j(min) 20–120°C, ΔT_j 45–150K, t_on 1–15s, I 3–23A, D 75–500µm） |
> | **是否仍活跃** | **是**。2016 年仍有多篇合作论文 |
> | **来源 URL** | `https://api.crossref.org/works?query.author=Bayerer&...`；`https://www.mdpi.com/1996-1073/17/11/2616`；`https://vbn.aau.dk/ws/files/335540720/energies_13_03355.pdf` |
>
> ### 2.3 Josef Lutz — CIPS 标准的共同推动者
>
> | 项 | 内容 |
> |---|---|
> | **姓名** | **Josef Lutz**（J. Lutz） |
> | **所属机构** | 交叉引用显示与 Semikron Danfoss、CIPS 相关工作有关（**具体任职机构未在Crossref 中标注，标为 [未核实]**） |
> | **领域贡献（一句话）** | 与 Bayerer、Herold、Herrmann 等共同发表功率循环与焊层失效机理研究；**CIPS08 这一命名本身就来自 CIPS（Fraunhofer IZM 相关的工业可靠性倡议）** |
> | **代表文献** | ① C. Herold, P. Seidel, **J. Lutz**, R. Bayerer, Microelectronics Reliability, vol. 64, pp. 453-457, 2016 [一手]<br>② T. Herrmann, M. Feller, **J. Lutz**, R. Bayerer, T. Licht, EPE 2007, pp. 1-7 [一手] |
> | **值得读** | 上述两篇（尤其EPE 2007 直接讲"功率循环引起的焊层失效机理"） |
> | **是否仍活跃** | **推测仍活跃**（2016 年有论文），无进一步证据 |
> | **来源 URL** | `https://api.crossref.org/works/10.1016/j.microrel.2016.07.130` |
>
> ### 2.4 LESIT 模型 — [未核实：提出人无法确认]
>
> | 项 | 内容 |
> |---|---|
> | **模型名** | **LESIT 模型**（功率循环寿命模型之一，公式形式为 Coffin-Manson + Arrhenius 修正） |
> | **提出人** | **[未核实]** ⚠️ **任务描述中的 "Pascal LESIT" 不是人名**。LESIT = **L**ow **E**ffort **S**older **I**nterconnect **T**est（低成本焊点互连试验），是**项目/计划名而非人名** |
> | **可确认的事实** |① 多个中文与英文文献将 LESIT 列为与 Coffin-Manson、Norris-Landzberg、Bayerer 并列的四大解析寿命模型之一 [权威期刊综述]<br>② 有中文二手文献称"1995 年瑞士洛桑联邦理工学院（EPFL）提出的 LESIT 模型"，但**该说法未找到一手来源支撑**[媒体，低可信]<br>③ 有中文技术文章称"上世纪 90 年代初欧洲多家功率模块制造商开展了 LESIT 项目" [媒体，低可信]<br>④ **已知的一组LESIT 参数**（A=640, α=-5, Ea/kB=9381.8）出现在《机车车辆牵引逆变器 IGBT 模块的结温与疲劳寿命计算》中[权威期刊] |
> | **技术价值（不依赖人名也成立）** | LESIT 模型的**历史意义在于它是第一个"跨厂商通用"的功率循环经验模型**——它基于多个欧洲厂商的联合测试数据库拟合，反映了**混合失效模式（键合线 + 焊层）下的平均统计结果**，因此**不区分失效机制**。随着银烧结等新互连技术使人能人为控制主导失效模式，才有了后续的 CIPS08、Semikron 等分模式模型 |
> | **建议** | ✅ **skill 中应按"模型 + 项目"记录，不要强行安一个提名人**。如需追溯原始报告，关键词：`ECMA TC47 LESIT Low Effort Solder Interconnect Test` |
> | **来源 URL** | `https://www.sciopen.com/article/10.23919/CJEE.2024.000095`（模型综述）；`https://jgcm.ac.cn/fileJGS/journal/article/dqgcxb/html/2017/2095-9524/2095-9524-12-10-9.shtml`（LESIT 参数） |
>
> ### 2.5 功率循环寿命模型的完整谱系（无争议部分，可直接进 skill）
>
> 来自 Aalborg 大学的两篇综述 + MDPI Energies 2024 + IEEE TCPMT 综述，**模型与变量对应关系已多重交叉验证**：
>
> | 模型 | 变量 | 参数个数 | 特点/ 适用边界 |
> |---|---|---|---|
> | **Coffin-Manson** | ΔT | 2（a, n） | 最基础。**仅当峰值温度 < 120 °C 时适用**。N_f = a·(ΔT)^-n |
> | **Coffin-Manson-Arrhenius** | ΔT_j, T_m | 3（a, n, Ea） | 引入平均结温 |
> | **Norris-Landzberg** | ΔT_j, T_m, f | 4（A, n₁, n₂, Ea） | 再引入循环**频率** f（因键合线疲劳受加热时间强影响） |
> | **LESIT** | ΔT_j, T_m | 4| 首个跨厂商通用模型；**不区分失效机制** |
> | **Bayerer / CIPS08** | ΔT_j, T_j-max, t_on, I, V, D | 7（K, β₁~β₆） | 变量最多。**仅适用 Al₂O₃ 基片** |
> | **Darveaux**（物理/能量法） | 非弹性功密度 ΔW | 4（K₁~K₄）+ 裂纹长度 a | 能量法标准。需 FEM。**注意 ANSYS 版本陷阱**（§2.1） |
>
> **⚠️ 工程铁律（多来源一致）**：**选错寿命模型，寿命估计可偏差达两个数量级**（IEEE TCPMT 综述原文："applying an unsuitable lifetime model can result in lifetime estimations that deviate by up to two orders of magnitude"）。且工程中常见问题是「套用文献里别人器件的参数」。
>
> 其他相关模型（PCB/封装焊点，非功率模块）：**Engelmaier** 模型（1980s，与Wild 合作，含频率与温度修正 c = -0.442 - 6×10⁻⁴T_s + 1.74×10⁻²ln(1+f)）、**Blattau** 模型（Sherlock 软件实现，OEM 广泛采用，基于 Darveaux 的能量概念 + 闭式力学解）。来源：Solder fatigue 模型综述 [权威]（**Blattau/Engelmaier 的机构与完整文献未一手核实**）
>
> ---
>
> ## 3. 标准组织中的关键推动者
>
> ### 3.1 JEDEC — 可靠性测试方法的守门人
>
> **组织定位**：**JC-14 Quality and Reliability of Solid State Products** 为可靠性方法的主委员会，下设 JC-14.1~JC-14.7。JEDEC 标准须经**委员会 2/3 多数 + 理事会 3/4 多数**双层通过，且强制**披露专利（Rand License Assurance）**——这一点对标准制定者行为逻辑的理解很关键。
>
> **现任委员会负责人（2026 年 10 月官方页面，全部 [一手]）**：
>
> | 委员会 | 主席 | 副主席 | 机构 |
> |---|---|---|---|
> | **JC-14** 固态产品质量与可靠性 | **TBD（空缺）** | **Ulrich Abelein** | Infineon |
> | **JC-14.1** 封装器件可靠性测试方法 | **TBD（空缺）** ⚠️ | **Gerhard Haubner** | Infineon |
> | **JC-14.2** 晶圆级可靠性 | **Andreas Martin** | Tim Miceli | Infineon / Micron |
> | **JC-14.3** 硅器件可靠性鉴定与监测 | **Maria Tanasescu** | Ron Eller | AMD / TI |
> | **JC-14.4** 质量流程与方法 | **Curtis Grosskopf** | Gary Capron | IBM / Micron |
> | **JC-14.7** 射频可靠性与质量标准 | **Purushothaman Srinivasan** | Gergana Drandova | GlobalFoundries / Qorvo |
> | **JC-15** 半导体封装热表征技术 | **Robin Bornoff** | Nathan Ai | Siemens Industry Software / Cadence |
> | **JC-11** 机械标准化 | **Xiang Li** | Zhineng Fan, John Norton | Intel / Amphenol / Nvidia |
> | **JC-13.1** 分立器件 | **Feargal Downey** | — | Microchip |
>
> **⚠️ 重要观察（对用户价值极高）**：
> 1. **JC-14 主席与 JC-14.1 主席同时显示 "TBD"（空缺）** —— 这两个正是 JESD22 系列的归口委员会，**目前处于主席空缺状态**。这是理解「近期 JEDEC 可靠性标准推进节奏」的关键情报。
> 2. **Infineon 在 JEDEC 可靠性委员会中占据主导地位**（Abelein、Haubner、Martin 三人，加上 JC-42.4 的Cliff Zitlaw、JC-70 的 Friedrichs 与 Aichinger）。对功率半导体封装可靠性而言，**Infineon 是 JEDEC 可靠性标准事实上最关键的推动者**。
> 3. 官方公布的 JC-14/JEITA 联合会议与 JC-14.1 分会（2027年 1 月 12/13 日）说明了 JEDEC 与 **JEITA** 的协调机制。
>
> **JESD22-A101（湿热偏置）版本沿革（[一手]，来自标准正文与 GlobalSpec 记录）**：
> - Test Method A101 → **JESD22-A101**（1988-07）→（1997-04）→（2009-03）→ **JESD22-A101D**（2015-07，14 页）→ **JESD22-A101D.01**（2021-01，**现行**）
> - 归口：**JC-14 / JC-14.1**
> - D 版的 ballot 来源：JCB-96-64、JCB-09-10、JCB-15-28
> - D.01 版主要变化：**增强了「器件无法偏置到很低功耗」时的测试能力**（即低功耗器件的湿热偏置）
> - 反向引用（谁引用了它）：**BS EN IEC 60810+A2**（车灯 LED）、**EN 16602-60-13**（航天 COTS 元器件）、**TS 102 221**（SIM 卡）、NEN-EN 16602-60-13
>
> **来源 URL**：`https://www.jedec.org/about-jedec/committee-chairs`（主席名录）；`http://www.beice-sh.com/pdf/JESD标准/JESD22-A101D.pdf`（A101D 全文）；`https://www.jedec.org/standards-documents/docs/jesd-22-a101c`（官方页）
>
> ### 3.2 JEDEC JC-70 — 宽禁带（WBG）功率半导体标准化（新设，最值得关注）
>
> | 项 | 内容 |
> |---|---|
> | **定位** | **JEDEC 最新的主委员会**（JC-70 Wide Bandgap Power Electronic Conversion Semiconductors），下设 **JC-70.1（GaN）** 与 **JC-70.2（SiC）**。三大工作焦点：**可靠性与鉴定程序 / 数据手册要素与参数 / 测试与表征方法** |
> | **主席** | **Dr. Peter Friedrichs**（Infineon）[一手]<br>**副主席**：**Laurent Guillot**（Alter Technology, France）、**Dr. Jaume Roig**（onsemi）[一手] |
> | **JC-70.1 GaN 主席** | **Kurt Smith**（VisIC Technologies）；**副主席：Dr. Massimiliano Regardi**（Nexperia）[一手] |
> | **JC-70.2 SiC 主席** | **Dr. Jeffrey B. Casady**（Wolfspeed）；**副主席：Dr. Thomas Aichinger**（Infineon）[一手] |
> | **Peter Friedrichs 的资历（已一手核实文献）** | Infineon Technologies AG, Neubiberg。著：① P. Friedrichs, *"SiC Power Device Technology — Differences to Silicon and Their Influence on Device Processing and Performance"*, ECS Transactions, vol. 25, pp. 83-92, 2009, DOI `10.1149/1.3238210`<br>② **P. Friedrichs, *"Reliability and robustness of SiC power devices — how to ensure the quality level established in the silicon world"*, IPEC-Himeji 2022, pp. 648-654, DOI `10.23919/ipec-himeji2022-ecce53331.2022.9807138`** ⭐<br>③ *"Ruggedness of SiC devices under extreme conditions"*, **IEEE IRPS 2020, pp. 1-5**, DOI `10.1109/irps45951.2020.9129344` ⭐<br>④ *"SiC power devices for industrial applications"*, IPEC-ECCE Asia 2010, pp. 3241-3248 |
> | **Thomas Aichinger 的资历（已一手核实文献）** | **Infineon Technologies Austria AG, Villach**（一手机构字段确认）。著：① **T. Aichinger, M. Schmidt, *"Gate-oxide reliability and failure-rate reduction of industrial SiC MOSFETs"*, IEEE IRPS 2020, pp. 1-6**, DOI `10.1109/irps45951.2020.9128223` ⭐<br>② S. Maas, H. Reisinger, T. Aichinger, G. Rescher, *"Influence of high-voltage gate-oxide pulses on the BTI behavior of SiC MOSFETs"*, IRPS 2020, pp. 1-6<br>③ T. Aichinger et al., *"1200V SiC Trench-MOSFET Optimized for High Reliability and High Performance"*, **Materials Science Forum, vol. 897, pp. 489-492, 2017** ⭐<br>④ T. Aichinger, M. Nelhiebel, *"Advanced Energetic and Lateral Sensitive Charge Pumping Profiling Methods..."*, IEEE TDMR, vol. 8, pp. 509-518, 2008 |
> | **值得读** | ① **Friedrichs, IRPS 2020 "Ruggedness of SiC devices under extreme conditions"**（IRPS 是可靠性物理的旗舰会议，5 页极精炼）<br>② **Aichinger & Schmidt, IRPS 2020（栅氧可靠性 + 失效率降低）**<br>③ Aichinger et al., MSF 2017（1200V SiC trench MOSFET 的可靠性优化） |
> | **是否仍活跃** | **是，明确活跃**。Friedrichs 2022 年、Aichinger 2024/2026 年均有论文 |
> | **来源 URL** | `https://www.jedec.org/committees/jc-70`；`https://www.jedec.org/about-jedec/committee-chairs` |
>
> ### 3.3 IEC TC 47 — 国际半导体器件标准
>
> | 项 | 内容 |
> |---|---|
> | **现任主席** | **Stephen Tisdale**（2024 年 9 月 – 2030 年 8 月首任任期）[一手，IEC 官网] |
> | **背景（一手确认）** | IBM "Master Inventor"（35+ 项专利），40 年电子行业经验（含 20 年 IBM）。**此前 9 年担任 TC 47 下属 SC 47 主席**（负责半导体封装的机械与热方面、封装组装技术与测量方法、含晶圆级封装）。同时是 IEC TC 91、TC 111 的技术专家/接口人，以及 **JEDEC 与 IPC** 的接口人。是欧盟委员会在**半导体技术与 RoHS 豁免**方面的顾问（合作方含 **IZM Fraunhofer**） |
> | **前任（由 Tisdale 本人具名提及）** | **Nick Lycoudes**（亦为 TC56 Dependability 的liaison officer，见 CEN/CENELEC 演讲材料）、**Robert Mitchell**。⚠️ "Robert Mitchell" 拼写与资料中另一处出现的 "Robert Mitchell" 一致，但**姓氏拼写未独立核实** |
> | **SC 47 下属机构（IEC 官方）** | SC 47A 集成电路 / **SC 47D 半导体器件封装** / SC 47E 分立器件 / SC 47C 光电子显示成像 / SC 47B 微处理器系统 / SC 47F MEMS。<br>WGW **WG 8 Wide bandgap technologies – Power electronic conversion**（TC47 已合并原 WG3） |
> | **TC 47 与 TC 91 的联络官** | **Nicholas E. F. Lycoudes**（TC 56 Dependability）、**Jim Lynch**（TC 91 Electronics assembly technology、TC 101 Electrostatics）[一手，CEN/CENELEC 演讲材料] |
> | **值得读** | ① **IEC 2023 白皮书《Power semiconductors for an energy-wise society》**（IEC Market Strategy Board 发布，明确指出了功率半导体**标准化缺口**）⭐<br>② IEC TC 47 官方项目页（可直接看 IEC 63287/63275/63505 等新标准的进展） |
> | **是否仍活跃** | **是**。任期至 2030 年 |
> | **来源 URL** | `https://iec.ch/taxonomy/term/416`；`https://www.iec.ch/dyn/www/f?p=103:22::::FSP_ORG_ID:1251`；`https://www.cencenelec.eu/media/CEN-CENELEC/Events/Events/2022/2022-12-02%20-%20CHIPS/presentations/werner-berns_ti.pdf` |
>
> **⚠️ 关于 "Werner Berns"**：CEN/CENELEC 2022 演讲材料的作者页显示 "**Werner Berns**, Int. Standardization – **Texas Instruments**"。此人与 Stephen Tisdale 并非同一人。**其 TC 47 内的具体职务未核实**（材料本身是关于 TC 47 结构的演讲，但未标明其是否担任 convener/ WG 角色）。若需 TC 47 convener 名单，**建议直接查 IEC 官网的 TC 47 Officials 页面**，本次未能访问。
>
> ### 3.4 ECPE / AQG 324 — 欧洲车规功率模块资格指南
>
> **这是与用户工作最直接相关的标准组织。全部信息 [一手]。**
>
> **组织与文件沿革**：
> - **ECPE**（European Center for Power Electronics e.V.，纽伦堡）提供组织平台；下设两个工业工作组：**AQG 324**（汽车功率模块资格）与**Power Semiconductor Reliability for Railway Application**（铁路应用功率半导体可靠性）
> - AQG 324 工作组**成立于 2017 年 6 月**，前身是**德国 LV 324**（由德国汽车 OEM 与功率电子供应商产业界联合制定）
> - **>30 家**汽车供应链工业代表参与
>
> | 版本 | 发布日期 | 状态/内容 |
> |---|---|---|
> | V01.05 | **2018-04-12** | 首个版本，聚焦 **Si 基**功率模块 |
> | **02.1/2019** | **2019-05-15** | 技术修订：将德国 DIN 标准大多替换为 **IEC**；新增 PCU 定义；章节重构 |
> | **03.1/2021** | **2021-05-31** | **新增 SiC 附录（Annex）** —— 涵盖 SiC 功率模块在驱动逆变器应用中的资格要求；重点是**功率循环试验的必要调整**与多项既有资格试验向"动态变体"的扩展 |
> | **04.1/2025** | **2025 年**（ECPE 页面写 24 April 2025，2026 教程材料写 31.03.2025 —— ⚠️ 存在日期不一致，**建议引用时写"2025 年 04.1 版"**） | 正文仍以 Si 为主，**SiC 在专门附录中** |
> | （规划中） | — | **GaN 附录在制定中**（见下） |
>
> **⚠️ 内容边界（常被误传）**：AQG 324 **针对的是模块设计（assembly）的资格，而非芯片或制程的资格**。排除含控制电路的模块与需要外部压力安装的压接式封装。[(W)PUB 2026 教程材料原文]
>
> **核心团队（全部 [一手]，来自 NI 2025 ECPE 演讲与 ECPE 2026 教程材料）**：
>
> | 角色 | 姓名 | 机构 |
> |---|---|---|
> | **工作组主席（WG Chairman）** | **Dr. Martin Rittner** | **Robert Bosch** |
> | 副主席 | **Prof. Dr. Markus Thoben** | UAS Dortmund（FH Dortmund） |
> | 副主席 | **Peter Dietrich** | **Richardson RFPD**（同时任 **GaN Task Force 负责人**） |
> | 副主席 | **Frank Heidemann** | National Instruments / SET |
> | **SG1** Endurance Tests (HTxy) | **Stefan Schmitt** | Semikron Danfoss |
> | **SG2 Power Cycle Tests (PCT)** | **Marc Tüllmann** | **Infineon Technologies** |
> | **SG3 Scope & Advanced AIT** | **Mr. Ewald**（Fuji Electric），代理 **Mr. Farkas** | Fuji Electric / Mentor |
> | **SG4 Insulation & Environmental Tests** | **Dr. Stefan Thieman** | **Valeo eAutomotive**（资料另处作 "Valeo Siemens"） |
> | SG4（ECPE 2026 教程组） | Dr. Gábor Farkas | Siemens Digital Industries |
> | SG4（ECPE 2026 教程组） | Waldemar Jakobi | Infineon Technologies |
> | ECPE 官方联系人 | **Dipl.-Phys. Thomas Harder**（General Manager ECPE e.V. & GmbH） | ECPE |
> | ZVEI-ECPE 联合工作组 "High Temperature and Power Electronics" 主席 | **Dr. Martin Rittner** | Robert Bosch |
>
> **Martin Rittner 的资历（一手，Warwick WIPDA2022 keynote 讲者页）**：Bosch 公司研究部**功率电子装配与互连技术高级专家**（senior expert）。斯图加特大学物理学（核物理，1994 博士），后在斯图加特大学半导体物理方向完成博士论文。2001 年起在 Bosch 企业研究部门工作，参与多个德/欧盟资助的电子封装与装配项目。2015 年获 MBA。**同时是 AQG 324 工作组主席 + ZVEI-ECPE 联合工作组主席** —— 本track 中**最值得跟踪的活跃人物**。
>
> **SG2（功率循环）落在 Infineon（Marc Tüllmann）手上**这一事实值得注意：功率模块可靠性标准的核心试验方法，正在由一家同时主导 JEDEC JC-14.x 与 JC-70 的企业推动。
>
> **参与成员公司（[一手]，来自 NiConnect 2025 材料）**：Alpitronic、AT&S、**CREE/Wolfspeed**、**Continental**、**DENSO**、**Fuji Electric**、**Heraeus**、**Hitachi**、onsemi、**Robert Bosch**、**Siemens**、**Valeo**、**Infineon**、**NXP**、**STMicroelectronics**、**Semikron Danfoss**、**Daimler/Mercedes-Benz**、**Toyota**、**Nexperia**、**Vitesco**、ZF 等
>
> **来源 URL**：`https://www.ecpe.org/research/working-groups/automotive-aqg-324/`；`https://www.ecpe.org/index.php?eID=dumpFile&t=f&f=48794&...`（2026 教程议程，含全部讲师）；`https://www.ni.com/content/dam/web/pdfs/niconnect/2025/semiconductor/Wide_Bandgap_Power_Semiconductor_Reliability_Testing_Industry_Standards_and_Implementations.pdf`（含WG 组织图）；`https://www.ecpe.org/index.php?eID=dumpFile&t=f&f=23930&...`（02.1/2019 全文含修订说明）
>
> ### 3.5 AEC（Automotive Electronics Council）— AEC-Q101 与 WBG Task Group
>
> **全部来自 AEC 官方 2025 欧洲 Workshop 材料，[一手]。这是本次调研中信息质量最高的部分之一。**
>
> **AEC-Q101 修订状态（2025 年 10 月 Workshop 材料）**：
> - **Rev F**：将新增 **SiC 产品**内容（通用要求）；Si 分立器件部分不变。**待 Wide Band Gap 组完成 SiC 内容后送 ballot**
> - **Rev G**：对 Rev E 的**实质性修订（substantial review）**，覆盖 ballot 阶段及发布以来收集的 **162 条comments / change requests**（讨论期 2024-07 至 2025-02）。Ballot 目标 2025 年中/末
> - **Rev G 关键变更**（细节丰富，值得逐条读原始 PDF）：
>   - 术语：'change-qualification' 替代 're-qualification'；'stress test' 替代 'environmental test'
>   - 移除结构：Table 3 的旧 test numbers 行、Table 2 note L、Table 3 note E
>   - 修正 Table A7.1（IOL 行）计算错误（回退到 Rev D 文本）
>   - 新增**混合器件**（同一封装内含分立器件 + IC）的处理指引
>   - **裸 die 资格的澄清**：仅涵盖 die 相关的失效机制；**封装/互连失效机制由用户负责** ⭐（对用户极其重要 —— 明确划清了 die 试验与封装试验的责任边界）
>   - **击穿电压从 shift criterion 中豁免（<20%）很可能被移除**
>   - **应力试验中观察到的、在允许判据内的漂移，应在最终测试中保持**
>   - 结构相似性（structural similarity）对 PV 与 ESD 在特定条件下可接受
>   - Table 2 的 additional requirements 移入附录；**新增 H3TRB、HAST 的 thermal runaway（热失控）指引**
>   - **Terminal Strength：引用 JESD22-B105 替代 MIL-STD-750-2 (2038)** ⭐（对用户直接相关）
>   - **HTRB：是否以 JESD22-A108G 替代 MIL 标准（开放议题）** ⭐
>   - IGBT 的 h_FE 将从 Appendix 5 最小参数测试清单中移除
> - **Rev G 开放议题（尚未决定）**：含 IC + 分立器件的产品要求；OEM 要求「generic data 只能来自年度 requalification 数据」；TDDB/BDI 等 technology qualification 对分立器件如何适用；**加入 cosmic ray**；TCDT 与 TCHT 并行执行的意图；ball shear 类试验的其他封装形式；应力后 hot test（成本高收益低）；**Mission Profile 是否应纳入 Q101**
>
> **AEC WBG Task Group 组织（[一手]，官方组织图）**：
> | 角色 | 姓名 | 机构 |
> |---|---|---|
> | **Task Group Leader & Moderator** | **Dr. Itasham Hussain** | **ZF Automotive UK Limited** |
> | **WG1 Failure Mechanisms** | **Don Gajewski** | **Wolfspeed** |
> | **WG2 Testing & Characterization** | **Laurence Allirand** | **Vitesco** |
> | **WG3 Lifetime Accelerated Tests** | **Dr. Massimiliano Regardi** | **Nexperia** |
> | **WG4 Insulation & Environmental Tests** | **Dr. Michiel Petrus** / **Dr. Martina Hommel** | **Infineon** / **Bosch** |
>
> **AEC SiC 标准化的技术定位（[一手]，官方材料原文）**：
> - **"Failure mechanism based stress test qualification for discrete semiconductors in automotive applications"** —— 明确的范式转变
> - **AEC SiC 内容计划作为 AEC-Q101 的附录（Appendix 8: Qualification of SiC）**，另有 Appendix 7「AEC-Q101 and the Use of Mission Profiles」、Appendix 7_007 Miscellaneous SiC-Test Methods、Appendix 7_008
> - **路线图**：SiC kickoff（2023）→ 整合各 WG 交付物 → AEC 委员会审阅 → 修订 → AEC 会员 ballot → **GaN kickoff（2026）**
> - **SiC 失效机制清单（[一手]）**：栅氧磨损（extrinsic：电荷俘获与可动离子漂移→Vth 漂移；BPD/SSF 缺陷转化→双极稳定性→反向偏置）；单粒子烧毁（中子）；短路；（热）机械（分层、开裂、应力迁移）；非钳位感性开关（dVds/dt）；热载流子注入；电迁移
> - **SiC 测试与表征**：Vth 表征要求、短路试验要求、**双极退化（bipolar degradation）**、ESD 试验要求、失效判据
> - **SiC 寿命与绝缘试验**：HTRB 试验概念（**VGS=0 与 VGS,neg两种**）、HTRB 与 HTGB 带偏置冷却、栅开关应力试验概念、UIS、**ELFR（Early Life Failure Rate）**
> - **SiC 绝缘与环境试验的关键改变** ⭐：
>   - **用 H3TRB 替代 HAST**
>   - **在 VDS = 80% 下做 H3TRB**
>   - **用 UHAST 替代 AC**
>   - 裸 die 相关试验定义：H3TRB、TC；**供应商为裸 die 选择合适的载体封装（carrier package）**
>
> **⚠️ 中文媒体转述错误警告**：某中文网站（dataintelo）称 "AQG 324 Amendment 1 (2022) 引入 SiC MOSFET-specific test protocols，Amendment 2 (January 2025) 引入 GaN HEMT qualification methodologies" —— **与ECPE 官方版本沿革矛盾**（官方为 03.1/2021 引入 SiC 附录；04.1/2025 仍以 SiC 附录为主，GaN 尚在工作组阶段）。**该中文来源为AI生成的行业报告，不可采信。**
>
> **来源 URL**：`http://www.aecouncil.com/files/Workshops/2025_European_AEC_Workshop/W3%20AEC%202025%20EU%20Workshop%20-%20Q101%20Workshop.pdf`；`http://www.aecouncil.com/files/Workshops/2025_European_AEC_Workshop/W4%20%20AEC%202025%20EU%20Workshop%20-%20Wide%20Band%20Gap.pdf`
>
> ### 3.6 关于 Fraunhofer IZM / CEMLA / LETI / SEMI
>
> - **Fraunhofer IZM**：[部分核实]。Stephen Tisdale 作为欧盟 RoHS 豁免顾问的合作方被明确提及为 "**IZM Fraunhofer**"（一手，IEC 官网）。**未找到 LESIT / 焊点模型提出者的姓名**。CIPS08 中的 "CIPS" 常被认为源自Fraunhofer IZM 相关的工业倡议 —— **[推测，未核实]**
> - **CEMLA / LETI**：[未核实]。未找到这两个机构在本主题下的具体角色。⚠️ 提示：CEMLA 更常指法国 EM 的**材料实验室**（Centre d'Étude des Matériaux et des Liaisons Avancées），与封装可靠性不是同一语境；**很可能是混淆项，建议不写入 skill**
> - **SEMI 标准委员会**：[未核实]。本次未能获得任何可核实的 SEMI 可靠性标准专家姓名。SEMI 的相关领域主要是硅片/材料/设备规范，**与封装可靠性试验方法关联较弱**
> - **Fraunhofer IZM 之外的欧洲实验室**：[未核实]
>
> ---
>
> ## 4. 领域内的关键「意见领袖 / 综述作者」
>
> ### 4.1 已核实的综述作者与必读综述
>
> | 作者 | 贡献 | 代表材料 | 活跃 |
> |---|---|---|---|
> | **J. W. McPherson** | TDDB 物理模型的四十年权威 | **IEEE Electron Devices Reviews, 2025, "Four Decades of E-Model Development for TDDB"** ⭐⭐⭐ | **是** |
> | **Wayne B. Nelson** | 加速试验统计设计 | *Accelerated Testing*, Wiley, 1990 | 否 |
> | **Milton Ohring / Lucian A. Kasprzak / James R. Lloyd** | 电子材料与器件的可靠性与失效（3代传承） | *Reliability and Failure of Electronic Materials and Devices*, Academic Press, 1998/2007/2015 | 否（传承中） |
> | **J. W. McPherson**（教材） | 可靠性物理的工程化工具书 | *Reliability Physics and Engineering*, Springer, 2013（399 页） | — |
> | **L. M. J. / Jason W. / Weijie Wang 等**（中国） | 功率循环寿命模型 state-of-the-art 综述 | **《State-of-the-art of Power Cycling Lifetime Models for Power Electronics》**, **Chinese Journal of Electrical Engineering (CJEE)**, 2024, DOI `10.23919/CJEE.2024.000095` ⭐⭐（**全谱系梳理最完整的一篇，且**开源可读**）<br>作者单位：中国铁道科学研究院牵引与控制国家重点实验室、北京纵横机电、内蒙古电力研究院、华北电力大学、合肥工业大学 | **是** |
> | **Omid Alavi, W. De Ceuninck, Michaël Daenen** | 对 IGBT 寿命模型修正的批判性评估 | *"Optimizing IGBTs' Lifetime Estimation: A Critical Evaluation of Lifetime Model Adjustments Based on Power Cycling Tests"*, **MDPI Energies 17(11):2616, 2024** ⭐⭐（**有完整参数表，且明确指出「Bayerer 模型仅适用 Al₂O₃ 基片」**）| **是** |
> | **Bjørn / Aalborg 大学团队** | 功率模块可靠性预测方法学综述 | *"An overview of the reliability prediction related aspects of high power..."*, Aalborg University（PDF 公开）⭐；*"A Comparative Reliability Analysis of DC- and AC-Coupling..."*, Energies 13:3355, 2020（**Bayerer 模型参数与温区表**）| **是** |
> | **IEEE TCPMT 综述作者群** | 功率循环方法的全面批判 | ***"Power Cycling Testing for Power Semiconductor Switches: Methods, Standards, Limitations, and Outlooks"***, IEEE（2025）⭐⭐ —— **提出「通用寿命模型」**：基于 CIPS08 简化形式、回归 200+ 公开实验数据点，覆盖 Si/SiC、Al/Cu 键合线、焊料与银烧结 | **是** |
>
> ### 4.2 AQG 324 相关高频被引述机构（**非人物**，但对用户有实操价值）
>
> 从 Bosch 功率模块老化数据文献中被反复引用的模块型号与失效模式（[权威期刊]）：
> - **SKiM63**（Infineon 模块）—— 因采用**铝包铜键合线**而专门用于研究**焊层失效**（而非键合线失效），是焊层寿命模型验证的常用基准件
> - 上焊料层温度分布与**键合线键合点位置**相关；下焊料层温度分布与**芯片位置**相关
> - 焊层温度不均与温差引起的热应力是**焊层疲劳失效主因**；**上焊料层疲劳寿命 < 下焊料层**
>
> **来源**：《柔性直流输电换流阀用 IGBT 模块焊料层疲劳寿命研究》；Microelectronics Reliability 2023, 119, 113651 相关工作
>
> ---
>
> ## 5. 近 12 个月的行业动向（谁在推动什么）
>
> ### 5.1 SiC/GaN 功率器件可靠性标准化——本track 最活跃的方向
>
> | 动向 | 关键事实 | 谁在推 | 时间线 |
> |---|---|---|---|
> | **AEC-Q101 纳入 SiC** | Rev F 加入 SiC 内容；**SiC 资格作为 Appendix 8**；整体范式转为"failure mechanism based stress test qualification" | **AEC WBG Task Group**：Dr. Itasham Hussain (ZF) 领；Don Gajewski (Wolfspeed) 失败机理、Laurence Allirand (Vitesco) 测试表征、Dr. Massimiliano Regardi (Nexperia) 寿命加速试验、Dr. Michiel Petrus (Infineon) / Dr. Martina Hommel (Bosch) 绝缘环境 | SiC kickoff **2023** → ballot 目标 **2025 年中/末** |
> | **AEC 的三个具体改变** | ⭐**用 H3TRB 替代 HAST**、⭐**在 VDS=80% 下做 H3TRB**、⭐**用 UHAST 替代 AC** | 同上 | 材料日期 2025-10 |
> | **AEC-Q101 原有 WBG 缺口** | 2024 年 AEC（底特律）大会已提出：因 WBG 使用方式与 SiC 不同，需不同应力条件；当时 Q101 未充分涵盖 WBG。已识别**七个可能改版要点**：**HV H3TRB、IOL、PCT、TC、GSS、BDOL、HAST/H3TRB** | AEC / DEKRA iST等 | 2024 |
> | **HV H3TRB 定义** | 2024 年 AEC 定义 HV H3TRB 内容，**取消 Q101 中测试电压最大 100 V 的限制** | AEC | 2024 |
> | **IOL 重新定位** | AEC 为**裸晶**定义的试验：利用器件自发热做on/off 高低温循环长时开关（限 1000 h 内），风冷控温使 **ΔTj 可大于 100 °C**。对功率密度持续升高的 WBG 器件**日益重要** | AEC | 2024 |
> | **JEDEC JC-70 设立** | JEDEC**最新**主委员会，专做 WBG 功率电子转换半导体；下设 JC-70.1（GaN）/ JC-70.2（SiC） | Dr. Peter Friedrichs (Infineon) 主席 | 委员会页面显示 **2026年 6/7/8 月有会议记录** |
> | **AQG 324 SiC 附录** | 03.1/2021（2021-05-31）引入 SiC 附录；核心是**功率循环试验的必要调整**与既有试验向"动态变体"扩展 | Dr. Martin Rittner (Bosch) 领导的 WG | 2021 起，04.1/2025 更新 |
> | **GaN 标准化启动** | AEC：**GaN kickoff 2026**（WG1 失败机理 / WG2 测试表征 / WG3 寿命加速 / WG4 绝缘环境 四线并行）<br>ECPE：Peter Dietrich 领导的 **GaN Task Force** | AEC WBG TG + ECPE | **2026** |
> | **IEC TC 47 WBG 工作组** | **WG 8 Wide bandgap technologies – Power electronic conversion**（已合并原 WG 3） | IEC TC 47 | 进行中 |
>
> **IEC 侧值得关注的 WBG / 功率模块新标准（均 [一手]，来自 IEC 官方 TC 47 项目列表）**：
> - **IEC 63275-1:2022** SiC 分立 MOSFET 可靠性试验方法 — **Part 1: 偏压温度不稳定性（BTI）**；**Part 2: 体二极管运行导致的双极退化**
> - **IEC 63284:2022** GaN 晶体管**感性负载开关**可靠性试验方法
> - **IEC 63229:2021** GaN 外延膜/SiC 衬底上的缺陷分类
> - **IEC 63505:2025** GaN HEMT 功率转换器件**动态导通电阻**测试方法指南
> - **IEC 63601:2026** SiC MOSFET **V_T 测量**指南
> - **IEC 63602:2026** SiC MOSFET **数据手册开关损耗表示**指南 ⭐（对用户日常直接有用）
> - **IEC TR 63571:2025** 从 "PART" 到 "SYSTEM" 的寿命换算估算方法 ⭐⭐（**这是目前最接近"用户日常痛点"的标准**）
> - **IEC 63364-1:2022** 汽车故障测试方法标准化路线图（故障诊断，非应力）
> - **IEC 63287-3:2026** 功率半导体模块可靠性鉴定计划指南（**最新版**）；**IEC 63287-4:2026** 早期失效率评估指南（最新版）
> - **IEC 63150-2/3:2025** 动能回收器件的振动环境测量与评估（次要）
>
> ### 5.2 先进封装（2.5D/3D、HBM、TSV）带来的新可靠性标准需求
>
> **全部 [一手]，来自 JEDEC 官方 Recently Published 与新闻稿**：
>
> | 标准 | 日期 | 内容 | 备注 |
> |---|---|---|---|
> | **JEP375** | **2025-12** | **2.5D/3D 硅减薄片 + TSV + 背面重布线层（RDL）：相对于底层 2D CMOS 技术的可靠性指南** ⭐⭐ | **这是 TSV/减薄片可靠性最直接的JEDEC 文件**。意图是给硅制造商一份"把 2D 减薄片+Cu TSV+RDL 送给客户所需的最小可靠性表征量" |
> | **JESD330-4 (SPHBM4)** | **2026-06-21 通过，2026-07-13 公告** ⭐⭐ | Standard Package HBM4：与 HBM4 相同的 DRAM die，但用新接口 base die，**可直接贴装在标准有机基板上**（绕过硅中介层）。2048 → **512 数据信号（-75%）**，4:1 串行化达 32 Gbps/pin，单 pin 速率 4×，总带宽与 HBM4 相同；SoC 到存储连接距离扩展至 **20 mm** |对功率封装工程师的启示：**热与翘曲问题从"硅中介层"转移到"超大尺寸 20–28 层+ ABF 有机基板（甚至玻璃基板）"** |
> | **JESD270-4A** | 2025-12 | HBM4 DRAM | 2 TB/s 总带宽，2048-bit |
> | **JESD271-4** | 2025-05 | HBM4 Bump Map Spreadsheet | — |
> | **JEP110A** | 2025-12 | ⭐**III-V 化合物半导体 FET 的热表征与建模指南** | 化合物半导体（GaN/SiC RF）热表征的空白填补 |
> | **JESD301-5** | 2026-01 | DDR5 CAMM2 Raw Card B | 内存相关 |
> | **JESD318-H0-RCB / JESD318B** | 2025-11/12 | DDR5 CAMM2 | — |
> | **JESD238B.01** | 2025-04 | HBM3 DRAM | — |
> | **JS-050** | 2025-12 | Maverick Product（离群品）消除与 outlier 管理 | 质量流程，非应力 |
> | **J-STD-048A** | 2025-12 | 产品停产通知标准（取代 JESD48） | 供应链连续性 |
> | **J-STD-046A** | 2025-12 | 客户对产品/工艺变更的通知标准 | — |
> | **JESD301-5 / JS-001-2024** | 2024-10 | HBM人体模型静电放电 JS-001-2024 | — |
> | **JESD22-B120.01** | 2024-09 | 引线键合拉力（Wire Bond Pull）试验方法更新 | 封装力学 |
> | **JESD22-B111A.01** | 2024-06 | 板级跌落试验（手持电子产品元件） | 板级 |
> | **JESD69D** | 2024-06 | 固态器件鉴定的信息要求 | — |
> | **JEP001-3B** | 2024-09 | 代工厂工艺鉴定指南 — 技术鉴定载具（WTV）测试 | 晶圆级 |
> | **JEP170A** | 2024-06 | FCxGA 倒装焊封装目视检验与控制 | 封装 |
> | **JEP30-10v8-0-0 / JEP30-S100A.02 / JEP30-A100B.01** | 2025-02 | Part Model 供应链 / 组装工艺分类 / 机械封装 XML 指南 | 数据模型 |
> | **JESD330-4 (SPHBM4)** | 2026-06 | 主席 Mian Quddus 引述："JEDEC 成员正在塑造定义下一代 AI 数据中心模块的标准" | — |
>
> **JEDEC 组织侧动向**：
> - **JC-42.2 HBM** 委员会：主席 **Barry Wagner**（Nvidia），副主席 **Doug Trujillo**（Micron）。**HBM 标准化目前由 Nvidia + Micron 主导**（不是 Intel/TSMC）
> - JEDEC 全球规模：**380+ 会员公司、100+ 委员会/task groups**
> - JC-14 相关的**中国 task group**：JEDEC 于 2016 年在中国设立首个 task group，挂在 JC-14 下；JEDEC 中国代表为**Mr. Xianmin Xi（席贤民）** ⭐（**对中文用户是天大的实用信息**）
>
> **⚠️ 关于「OCP/OLED」**：未在本track 范围内核实。JEDEC 官方页显示 OCP 相关工作体现在 **JESD318（JESD80-1?）CAMM2** 与 **SOCAMM2**（JESD400-5D SPD 1.4, 2025-10）中，**并非独立的可靠性标准**。**建议不要把 OCP 写成可靠性标准来源。**
>
> ### 5.3 氢能 / 碳中和驱动的新标准
>
> | 项 | 内容 | 证据 |
> |---|---|---|
> | **IEC 白皮书《Power semiconductors for an energy-wise society》** | **IEC Market Strategy Board 2023-10 发布**。明确指出功率半导体对脱碳与数字化的作用，并**直接指出了现有的标准化缺口（standardization gaps）**。特别提到从**线性经济转向循环经济**的转变与人才短缺 | [一手] IEC 官网 |
> | **IEC TC 47 EEE/EC 安全** | Stephen Tisdale 作为欧盟 RoHS 豁免领域的顾问（合作方含 IZM Fraunhofer） | [一手] IEC 官网 |
> | **JEDEC 宽禁带定位** | JEDEC 官网把 "**Wide Bandgap Power Semiconductors**" 列为当前五大技术焦点之一 | [一手] JEDEC 首页 |
> | **SiC 在电动汽车与电网** | 多个一手来源确认 SiC 已成为 EV 主驱、800V 平台、充电桩的主流方案（McLaren Applied 800V SiC inverter keynote；Friedrichs/Bayerer 的 SiC 组装与热管理挑战论文） | [一手] |
>
> **⚠️ 诚实说明**：**没有检索到任何"氢能专用"的半导体可靠性标准**。碳中和在本track 中体现为**（a）IEC 白皮书指出的标准化缺口**，与**（b）EV/800V SiC 平台的可靠性需求**，而非独立的氢能标准。**建议 skill 中不要虚构氢能标准。**
>
> ### 5.4 功率模块的通用国际标准化动向
>
> | 动向 | 状态 |
> |---|---|
> | **AQG 324** | 欧洲主导，覆盖汽车。最新版**04.1/2025**（SiC 附录）。**GaN 附录在制定中** |
> | **IEC 63287-3:2026** 功率半导体模块可靠性鉴定计划指南 | **2026-08-06/28 发布（最新版）** ⭐ —— 这是**国际层面的功率模块通用指南**，与 AQG 324 互补 |
> | **IEC TR 63571:2025** PART→SYSTEM 寿命换算 | 2025-05-13，**最贴近工程实操** |
> | **IEC 63602:2026** SiC MOSFET 数据手册开关损耗表示 | 2026-02-03，**解决"SiC 手册怎么写"的标准化空白** |
> | **AEC-Q101 Rev F/G** | SiC 进 Appendix 8；GaN kickoff 2026 |
> | **JEDEC JC-70 / JC-70.1 / JC-70.2** | 2026 年活跃；GaN 与 SiC 分设子委员会 |
> | **LV 324（德国）** | 已被 AQG 324 取代（继承其通用要求、试验条件与试验） |
> | **铁路应用功率半导体可靠性** | ECPE 第二个工作组"Power Semiconductor Reliability for Railway Application"在运行（**具体标准编号与内容未核实**） |
>
> ---
>
> ## 6. 建议写入 skill 的优先级
>
> ### 6.1 第一梯队（必写，全部已一手核实，且直接支撑试验设计判断）
>
> | # | 人物/条目 | 理由 | 锚点材料 |
> |---|---|---|---|
> | **1** | **J. W. McPherson** | TDDB 物理模型的四十年权威；**2025 年 IEEE EDR 综述是"模型外推之争"的裁判**。做HTOL/TDDB 应力条件设计绕不开 | IEEE EDR 2025, "Four Decades of E-Model Development for TDDB", DOI `10.1109/edr.2025.3620381` |
> | **2** | **Dr. Martin Rittner（Robert Bosch）** | **AQG 324 工作组主席 + ZVEI-ECPE 联合工作组主席**，同时是 Bosch 功率电子封装与互连技术高级专家。**功率模块资格标准事实上的总负责人** | ECPE AQG 324 WG 页；Warwick WIPDA2022 keynote 讲者页 |
> | **3** | **D. Stewart Peck（Bell Laboratories）** | 湿热加速模型的唯一工业标准来源。THB/HAST/H3TRB 的 AF 计算全部源于此 | Peck, "Comprehensive Model for Humidity Testing Correlation", IRPS 1986, pp. 44-50 |
>
> ### 6.2 第二梯队（建议写）
>
> | # | 人物 | 理由 |
> |---|---|---|
> | 4 | **Reinhold Bayerer（Infineon）** | CIPS08/Bayerer 模型；**参数公开可用**（β₁~β₆）；同时是 JEDEC JC-14.1 副主席所在企业的核心专家 |
> | 5 | **Robert Darveaux（Amkor）** | 能量法焊点模型的事实标准；**ANSYS 版本陷阱**必须记录 |
> | 6 | **Wayne B. Nelson（GE）** | 加速试验统计设计；分组/阶梯应力最优化的理论来源 |
> | 7 | **Dr. Peter Friedrichs（Infineon）+ Dr. Thomas Aichinger（Infineon）** | **JEDEC JC-70 主席 + JC-70.2 SiC 副主席**；SiC 可靠性资格的核心技术推动者 |
> | 8 | **Dr. Itasham Hussain（ZF Automotive UK）** | **AEC WBG Task Group 组长** —— 决定 AEC SiC/GaN 条款走向的人 |
> | 9 | **Marc Tüllmann（Infineon）+ Stefan Schmitt（Semikron Danfoss）** | AQG 324 SG2（功率循环）与 SG1（高温耐久）负责人 —— **直接决定 PCsec/PCmin 试验怎么设计** |
>
> ### 6.3 机构（建议作为「组织」条目写入，而非人物）
>
> - **ECPE / AQG 324 WG**（功率模块资格）
> - **JEDEC JC-14.1**（封装可靠性试验方法，⚠️主席空缺）、**JC-70**（WBG）
> - **AEC Component Technical Committee**（车规）
> - **IEC TC 47 / SC 47D**（Stephen Tisdale，2024-09 至 2030-08）
> - **Infineon** 在 JEDEC 可靠性委员会的集体角色
>
> ### 6.4 ⚠️ 明确不要写入 skill 的（本次核实为错误或不可靠）
>
> - ❌ **"Darcy 模型"** → 正确为 **Darveaux 模型**
> - ❌ **"Christoph Zard"** → 检索完全无结果；TDDB 奠基人是 McPherson
> - ❌ **"SN 加速关系"** → 未在任何来源中出现
> - ❌ **"Specht 加速模型"的具体报告编号 / NSWC 归属** → 未取得一手书目，建议只写"文献中广泛引用的加速模型综述报告（作者 E. J. Specht）"或干脆留空
> - ❌ **"William E. Snively"作为加速模型奠基人** → 未核实
> - ❌ **"Leslie A. Gall"温度加速模型** → 未核实（检索到的是气象学家同名者）
> - ❌ **"R. A. Verson"应力-寿命曲线** → 未核实
> - ❌ **"Edward J. McGann"** → 检索到的是美国海军退役指挥官 Donald McGann，无法建立关联
> - ❌ **"Peck 1974"** → 应为 **1973**（IRPS）与 **1986**（IRPS）
> - ❌ **"Pascal LESIT"** → LESIT 是项目缩写，非人名
> - ❌ **Navraj S. Sandhu = X-FAB** → 机构关系未核实
> - ❌ **CEMLA / LETI** → 未核实，疑为混淆项
> - ❌ **"氢能专用半导体可靠性标准"** → 不存在（本次未找到）
> - ❌ **OCP 是可靠性标准来源** → 失实，OCP 相关仅见于内存模块机械标准
>
> ---
>
> ## 7. 本track 的整体可信度评估
>
> | 层级 | 数量级 | 说明 |
> |---|---|---|
> | **一手已核实** | 约 **30 条人物/组织条目** + 约 **30 项标准与文献** | 依据：Crossref DOI 元数据、JEDEC/IEC/ECPE/AEC 官方页面与官方 PDF |
> | **权威但二手** | 约 5 条 | 依赖技术媒体或课件对一手文献的转述（如 Peck 的 n=2.7/Ea=0.79 eB，经两个独立来源交叉验证） |
> | **明确未核实** | **12 项** | 已在§6.4 全部列出并说明原因 |
> | **AI 生成的低质来源（已识别并弃用）** | 1 | dataintelo.com 的 AQG 324 市场报告（版本沿革与官方矛盾） |
>
> **最可靠的部分**：JEDEC 委员会名录、IEC TC 47 主席、AEC WBG Task Group 组织与条款、ECPE AQG 324 版本沿革与工作组构成、Crossref 可查的论文元数据。
>
> **最薄弱的部分**：加速寿命模型的**历史人物**（Specht / Snively / Gall / Norris / Bernstein / Verson / McGann）—— 这个领域的关键文献多为 1970–80 年代的政府报告与专著，**不在开放 DOI 索引内**，本次无法取得一手书目。这部分只能靠图书馆/馆际互借/购买实体报告解决。
>
> **建议的下一步**（若要把§1.5 的空白补齐）：
> 1. 通过 DTIC（Defense Technical Information Center）与 Naval Surface Warfare Center（NSWC Whitehall）官方站点检索 Specht 报告原文
> 2. 通过 IEEE Xplore 的 Reliability 分区回溯 1970s 的 IRPS 论文集，可定位 Peck / McGann / Verson 的真实引用
> 3. 通过 WorldCat / 图书馆查找 W. T. Norris, *Design of Accelerated Life Tests*（1980, Elsevier）与 J. J. Bernstein, *The Mathematics of Semiconductor Device Life Testing*（1986）的真实书目
