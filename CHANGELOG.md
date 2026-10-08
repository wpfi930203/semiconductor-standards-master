# Changelog

本项目的所有重要变更都记录在此文件。
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [v1.5.0] — 2026-10-08

**军标全量 OCR（GJB 两份完成）+ 方法索引建成 + 三处解析缺陷修复**

- GJB-548B 全量 OCR 完成（393/393 页）、GJB-548C 全量完成（460/460 页）；MIL-STD-883K 全量进行中
- ★ 建成军标方法索引：883K 105 个 / 883F 76 个 / GJB-548B 75 个 / GJB-548C 74 个方法号
- ★ 交叉校验：GJB 548 与 MIL-STD-883 方法号同源，实测重合 99%（74/75、73/74）—— 独立佐证两侧 OCR 与解析无系统性错位
- 新增三种来源标记：目录页 / 同源标准参考 / OCR归一，逐条标注可信度
- 新增缺口声明（按系列内检测号段不连续），并明确「不判断是标准跳号还是 OCR 漏识」
- 修复数字内空格漏项：OCR 把 1011 拆成 '101 1' → squeeze_digits（883K 100→105 个方法号，交叉一致率 95%→99%）
- 修复正文污染标题：初版扫全文，正文句子被当标题 → 改为只在各标准目录页范围解析
- 修复中文空格：Windows OCR 在汉字间插空格 → CJK 空格折叠
- 修复 GJB-548C 文件一致性：前 16 页旧格式 + 其余新格式导致重复块 → 重 OCR 并按页序合并（460 页）
- 同源补齐：GJB-548C 目录 I 页在扫描件中缺失（1001~1030），用 GJB-548B 目录补齐并标注「可能已被修订，不得直接引用」
- 放弃不可靠做法：曾试从正文节标题补齐缺口，但产出的是正文句子（如 1005 → 交叉引用句），已回退
- CLI 新增 `stdq mil <方法号>`；SKILL.md §0.6 重写（引擎选型实测 + 方法索引 + 三种 OCR 误差 + 来源标记）

## [v1.4.0] — 2026-10-07

**军标 OCR（定向）+ 机翻标准完整蒸馏（条款级 digest + 术语纠错表）**

- ★ 机翻标准全部蒸馏：为 37 份 L3 生成条款级 digest（references/digests/），含章节结构 + 数值条件 + 本文件命中的术语错误
- ★ 新发现机翻件第三个缺陷：约 20% 的条款号存在确定性错位（首位数字被移到末尾），如 .32 实为 2.3、.162 实为 2.16、.21 实为 1.2；错位可逆，digest 已按规则还原并标注（还原）
- 条款号错位验证依据：A104F 上下文（夹在 2.2 与 2.4 之间）+ J-STD-020 目录三重交叉（1.1范围 → .21背景 → .31术语和定义）
- ★ 建机翻术语纠错表 10 条，每条与英文原件逐行对齐核实：模具←die / 模具垫←die pad / 球键←ball bond / 线束←wire bond / 热膜←thermosonic / 针线←stitch bond / 冶金键←metallurgical bond / 骰子←dice / 偏见·偏差←bias
- digest 产出规模：672 章节条目（其中 136 条需还原，占 20%）+ 565 条数值条件行 + 431 次术语错误命中
- ★ 军标 OCR：建立 tools/ocr_military.py（逐页落盘 / 断点续跑 / 版面还原 / 限页）
- ★ OCR 性能实测（非推测）：本机 36~236 秒/页。已试 onnxruntime 1.30.0 与 1.22.0 两版、dpi 100/150/200/300 四档、强制 CPU 与默认 providers 两种配置、RapidOCR PP-OCRv3 det/rec。最快 36 s/页
- → 全量 OCR 2,229 页需 22~75 小时，判定不可行；改用定向 OCR（各军标目录/方法索引页）
- 新增引用层级 L4-OCR：扫描件 OCR 后「可用于理解与索引，引用前必须人工核对原扫描页」
- CLI 新增 2 子命令：digest（单份/全部条款级 digest）、terms（机翻术语纠错表）；subcommands 15→17
- SKILL.md 新增 §0.6「军标 OCR 的实测约束」+ §0.5 扩充（L4-OCR 层 / digest 资源 / 术语纠错表 / 条款号错位警示 / 回答纪律 5→7 条）
- LOCAL-CORPUS.md 扩至 777 行：新增「机翻标准条款级蒸馏」与「条款号错位」两节，逐份标注蒸馏状态与 OCR 进度
- 新增 tools/corpus/distill_l3.py（L3 蒸馏器）与 tools/ocr_military.py（军标 OCR 运行器）

## [v1.3.0] — 2026-10-07

**并入用户本地标准资料库（63 PDF / 52 编号）+ 建立引用分层纪律**

- 源目录 <本地标准资料库>（63 个 PDF / 827MB / 5,749 页）
- 按仓颉蒸馏流程执行：盘点去重 → 文本层抽取 → 文档自述元数据 → 分层定级 → 整合入 skill（未新建任何独立 skill）
- ★ 实测发现文件名声明语种与正文实际语种严重不符：标注「完整英文电子版」的 38 份实为机翻中文，仅 7 份是真英文原文
- ★ 发现文件名与内容语种完全错位：中文名文件是英文原件，英文名文件反而是机翻件（B116B 案例）
- 抽取 49 份标准文本层语料（≈1.4M 字符 / 2.4MB）至 references/sources/standards/（jedec 41 / ipc 4）
- 4 个军标/国军标（MIL-STD-883F/K、GJB-548B/C，2,228 页）确认纯扫描件，0 字符文本层；如实登记为 L4，不做 OCR
- 建立五层引用分层模型 L1~L5：L1 英文原文 7 / L2 官方译本 1 / L3 机翻 37 / L4 扫描件 4 / L0 不在库
- ★ 实测机翻件术语硬错：Wire Bond→「线束」、thermosonic→「热膜」、stitch bond→「针线」、metallurgical bond→「冶金键」—— 确立「L3 只能定位、不能引用译名」规则
- ★ 实测表格抽取丢符号：A104 表1 的 H 条件 -55°C 被抽成 55°C、J/K 的 0°C 被抽成 -0 —— 数值也须交叉核对
- CLI 新增 3 个子命令：corpus（资料库概览+分层）/ coverage（按类别总账）/ source（单份出处与引用规则）
- ★ cmd_find 增强：每条 find 结果自动附「本地资料库持有情况 + 可引用程度」，让引用纪律无需额外查询即生效
- 新增 references/LOCAL-CORPUS.md（682 行）人读覆盖清单：逐份列类别/适用范围/关键条目/出处/层级
- 新增 data/corpus.json 机器可读索引；references/sources/corpus_index.json 抽取台账；corpus_metadata.json 自述元数据
- 新增 tools/corpus/ 五步抽取流水线（盘点/抽取/元数据/索引/清单）+ README（含 5 个已知陷阱）
- SKILL.md 新增 §0.5「本地资料库与引用纪律」——六条强制回答纪律；§11.1 新增 6 条实测边界；§13.1 资料库索引；§14.1 刷新流程
- 诚实边界新增：A104 在库为 F(2020-11) 而非 F.01；JESD47 在库为 L(2022-12)，正文另处「N 版 2026-08」来自二手须外部核实
- 本地资料库不含 IEC 60749 系列正文与 AEC-Q100 正文 —— 涉及时只能依赖 AQG 324 引用表与二手资料
- Win32 陷阱处理：路径 ≥240 字符时 stat() 报错、rglob 静默漏项 → 改用 \\?\ 前缀 + os.scandir 递归

## [v1.2.0] — 2026-10-07

**呈现层刷新：图标 / 中文名 / 介绍（内容层按 Phase 0C 判定不重跑）**

- master-skill tools/update_skill.py plan 判定：age_months=0 → rejected（too recent），6轨 research 全部保留不重跑
- CLI 健康检查通过：stats 92 条/57 边/29 未核实/15 误传；抽样 find JESD22-A104、ql QL-01 输出正常
- 新增图标：icons/logo.png (200x200) + icons/logo.svg，主题「芯片 + JESD」——铜金引脚壳体=封装互连、靛蓝裸片=die、青色 JESD=JEDEC 编号前缀；刻意区别于本机chip-fa-* / semiconductor-process-master 的通用芯片图形
- 新增 tools/make_icon.py（纯 Pillow 手绘，4x 超采样，不调图像生成 API，零版权风险）
- frontmatter 补齐 master-skill 标准字段：displayName=半导体标准专家 / slug / icon / version=1.2.0
- 介绍（description）重写：从「OS 定位陈述」改为「四项硬能力 + 2 条核心心智模型 + 边界纪律 + 典型问题」的激活导向结构，保留全部原触发词并补充 HAMT/标准选型等实际问法
- 修正 CLI 路径：/root/.codebuddy/skills → ~/.workbuddy/skills（原为 Linux 路径，Windows 下无效）
- 修复 stdq check 静默缺陷：干净编号原先无任何输出且 rc=0，调用方无法区分「检查通过」与「库中无此编号」。现补显式回执（标题+匹配方式+状态+可信度+CAUTION 提示），库中查无此编号时改为告警并 rc=1
- 新增 tools/verify_skill.py：frontmatter/icon/meta 三方一致性 + description 关键词覆盖 + 16 项 CLI 回归（含 check 的正例与两类按设计拒绝样本）

## [v1.1] — 2026-10-05

**AQG 324 全文入库（Round 2）**

- 从 ECPE 官网（token 化 dumpFile 链接）下载 AQG 324 三版 PDF：04.1/2025（145 页，现行）、03.1/2021（129 页）、02.1/2019（70 页）+ 2018 介绍与新闻稿
- 一手转录 QL-01~QL-11 全部条件表（Table 9.1~9.17）→ 新增 stdq ql 子命令
- 一手转录 Annex I.C 统计判据（B5 + CL 80% 下界 + 右删失/success run）→ 新增 stdq aqg
- 一手转录 Annex II.B 寿命公式 5/6/7/8（LESIT / Bayerer / Ag 烧结扩展式）+ 23 条文献 → 新增 stdq lifetime
- 全文正则实测引用构成：IEC 71.5% / JEP 10.6% / JEDEC_std 5.7%（修正 v1.0 的 67/10/24 估算）
- ★ 发现并记录双层引用体系：5 个 JEP 全部锁在 Annex SiC，正文硅基零 JEP 引用
- ★ 发现文档缺陷：IEC 60749-6 版本在第3章引用表(2017)与 §9.4 正文(2002)自相矛盾
- 补齐 24 个缺失标准节点（IEC 60747/60749/60068/60664 系列、5 个 SiC JEP、LV324、VDA Vol.3 P2、ASTM E1049、IATF 16949、ISO/IEC 17025）
- 引用边 25→57 条，其中 A 级 37 条；标准条目 68→92 条，A 级 14→38 条（占比 20%→41%）
- 修正 MM-4 LESIT 公式错误（原文无 f^a 项）
- 修正 EOL 判据张冠李戴（PCsec/PCmin 判据完全相同：Vf+5%/Rth+20%）
- 修正 AQG 324 标题（原误写为 Electronic Components，实为 Power Modules for Use in Power Electronics Converter Units in Motor Vehicles）
- 删除 refs/cited-by 未实现的 IEC 60749-11 边（实测全文未引用该 Part）
- 修复三位 MIL 编号拦截漏判（find M-101 需去掉 MIL 上下文依赖）
- 修复 wrap() 显示宽度计算与多行字段缩进对齐
- 回归测试 47/47 全通过（含 7 项安全拦截回归）

## [1.0.0] — 2026-10-05

**首版：6 轨调研(7070行/554来源) + 68 条标准库 + 25 条引用边 + 零依赖 CLI + 5 心智模型/12 playbook/7 维 Agentic Protocol**

