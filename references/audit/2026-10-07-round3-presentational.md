# 审计记录 · 2026-10-07 · v1.2.0（呈现层刷新）

> 触发：用户要求「用 master-skill 的检查刷新半导体标准专家 skill，刷新图标为『芯片 JESD』SVG、中文名『半导体标准专家』、刷新介绍」
> 方法：走 master-skill Phase 0C 更新路径 + Phase 4 质量验证

---

## 0. 刷新强度判定（Phase 0C）

用官方工具判定，不靠感觉：

```
python {master_skill_dir}/tools/update_skill.py plan --skill-dir .
→ {"status": "rejected",
   "reason": "last_research_date 2026-10-05 is only 0 months old. Refusing refresh — too recent.",
   "age_months": 0,
   "tracks_to_refresh": [],
   "tracks_to_keep": [01-figures, 02-tools, 03-workflows, 04-canon, 05-sources, 06-glossary]}
```

**结论：6 轨 research 全部保留，一行不重跑。**

这不是偷懒，是 Phase 0C 的设计意图：`last_research_date` 是 2 天前（2026-10-05），
且那两天刚做完 AQG 324 三版 PDF 全文入库（v1.1 changelog 有完整记录）。
按 master-skill 的"品味守则"——**工具/工作流 3-6 月衰减，心智模型 1-2 年才动**——
现在重跑六轨只会产生噪声并把已一手化的 AQG 324 条目冲淡。

→ 本轮刷新范围限定在**呈现层**：图标 / 中文名 / 介绍 / 版本元数据 / 一处 CLI 缺陷。

---

## 1. 图标：为什么是「芯片 + JESD」而不是「芯片」

本机已有多个芯片类 skill，若画一颗通用芯片必然撞图：

| 已有 skill | 图标语义 |
|---|---|
| `chip-fa-router` + 10 个 `chip-fa-*` 原子 skill | 芯片失效分析 |
| `semiconductor-process-master` | 芯片制造工艺 |
| `semiconductor-standards-master`（本 skill） | **半导体制程标准** |

通用芯片只能表达"半导体"，无法区分这三种。**芯片身上压"JESD"** 才把语义收窄到
JEDEC 编号体系——而这恰好是本 skill 的独占能力（编号反查 / 引用链追溯）。

| 元素 | 颜色 | 语义 |
|---|---|---|
| 背景 | `#0E2038 → #1A3A5C` 深硅蓝渐变 | 硅基半导体 |
| 20 根引脚 + 壳体 | `#F5B942 → #D98A1F` 铜金渐变 | 封装与互连金属（Cu/Au）——本 skill 考核的正是键合与焊点 |
| pin-1 定位点 | `#784E10` | 让方形读成"芯片"而非"色块" |
| 裸片 die | `#0C1C30` + `#3A6E96` 描边 | 芯片本体 |
| **JESD 字样 + 下划条** | `#6FE3D6` 青 | **JEDEC 标准编号前缀 + "这是一条标准"的读法** |

- 输出：`icons/logo.png`（200×200，9,270 bytes）+ `icons/logo.svg`（矢量源，2,285 bytes）
- 生成：`tools/make_icon.py`，纯 Pillow 手绘矢量，4× 超采样 + LANCZOS 降采样，**不调用任何图像生成 API**（零版权风险）
- 已实际渲染查看确认：引脚数量、圆角、JESD 字形、下划条位置均正确

**避开的坑**：初版 `make_icon.py` 把 `SHELL_T/SHELL_B` 误写成坐标元组导致 `TypeError`，
已改为 float 标量。这类错误在纯文本 review 时看不出来，必须真跑。

---

## 2. frontmatter 补齐

原 frontmatter 只有 7 个字段，缺 master-skill 模板与本机其他 skill 都在用的
`displayName` / `slug` / `icon` / `version`——**中文名"半导体标准专家"无处声明**。

| 字段 | 变更 |
|---|---|
| `displayName` | 新增 = `半导体标准专家` |
| `slug` | 新增 = `semiconductor-standards-master` |
| `icon` | 新增 = `icons/logo.png` |
| `version` | 新增 = `1.2.0`（原文件无版本号） |
| `description` | 全部重写（见 §3） |
| 其余字段 | 保留不动（industry / locale / profile / last_research_date / source_count / allowed-tools） |

---

## 3. 介绍（description）重写：从「定位陈述」到「激活导向」

**改前的结构**（问题：只讲了 skill 是什么，没讲它能干什么、什么不能用）

```
半导体标准体系 OS（JEDEC / SEMI / ...）—— 从标准编号反查内容、追溯标准间引用关系、
按失效机理选择试验方法、把标准条款翻译成试验方案。
当用户问「JESD22-A104 是什么」...时加载。
触发词：...
```

**改后的结构**（对齐 lean-production-expert / chip-fa-router 的写法）：

1. **定位 + 否定式定位**：「用标准做工程判定，不是查标准」——一句话划清边界
2. **四项硬能力**（编号反查 / 引用链追溯 / 按机理选试验 / 条款→试验方案），
   每项带具体数字（92 条库、7 大体系、PCsec/PCmin 双轨、七步法）
3. **差异化资产**：AQG 324 三版 PDF 全文 + QL-01~QL-11 一手转录 + B5/CL80% 统计判据
4. **两条核心心智模型内嵌**（方法库 vs 裁判、零失效只能给上界）——
   把最重要的判断纪律写进介绍，让 Agent 在**决定加载之前**就知道边界
5. **数值纪律**：来源层级必标、29 项未核实禁止断言
6. **典型问题 9 例**（用户真实问法，不是抽象名词）
7. **触发词**：原全部保留 + 补充「HAMT 条件能不能用」「加速因子 Ea 怎么定」等实际问法

长度 1,247 字符。**原触发词 0 丢失**（verify_skill.py 逐项断言）。

---

## 4. 顺手修的两个真实缺陷

### 4.1 CLI 路径是 Linux 路径，Windows 下无效

SKILL.md §0 写的是：

```
S=/root/.codebuddy/skills/semiconductor-standards-master/scripts/stdq.py
```

本 skill 实际装在 `~/.workbuddy/skills/...`，照抄这行在 Windows 上必然跑不通。
已改为 `~/.workbuddy/skills/...`（跨平台写法），并在 meta.json 加 `path_note` 注明实际路径。

### 4.2 `stdq check` 静默缺陷（真实 bug，非风格问题）

**现象**：`stdq check IEC60749-34`（干净编号、无误传、无废止）**不输出任何内容**，
返回 rc=0。Agent 无法区分"检查通过"和"库里根本没这个编号"。

**根因**：`cmd_check()` 只在 `issues > 0` 时打印，末尾直接 `return 1 if issues else 0`。

**修复**：无异常时补显式回执——标题 + 匹配方式 + 状态 + 可信度 + CAUTION 提示；
库中查无此编号时改为告警并 `rc=1`（原来会静默 rc=0，等于把"拼错编号"当成"检查通过"）。

```
✓ check IEC60749-34   → ✓ 未发现误传/废止问题 + 标题 + 状态/可信度   rc=0
✓ check JESD22-A104   → ⚠ 常见误传（A104 规定了 1000 次）            rc=1  ← 按设计报警
✓ check M-101         → ✗ 编号错误（883 是四位）                    rc=1  ← 按设计拒绝
✓ check ZZZZ-999      → ⚠ 库中无此编号                              rc=1  ← 新增拦截
```

### 4.3 修正我自己的测试断言（过程记录）

第一版 `verify_skill.py` 断言 `check M-101` 应 rc=0，测试报红。
复核后确认**是断言写错、CLI 行为正确**——`check` 的语义就是"有问题就非零退出"，
误传拦截器命中时返回非零是设计意图。同理 `check JESD22-A104` 也报红，
因为它命中误传纠正表第 1 条。已把这两个样本显式标注为「按设计拒绝」，
并另找 `IEC60749-34` 作干净正例。

> 这条记录留档，是因为它和 §4.1 那个 bug 构成对照：
> **同样是 rc≠0，一个是 bug（静默放过未知编号），一个是特性（正确拦截已知误传）。**
> 不写下来，下次回归时有人会"顺手"把拦截器的非零退出改成 0。

---

## 5. 新增 `tools/verify_skill.py`（自动化 Phase 4）

对应 master-skill Phase 4「质量验证」的自动化部分，
思路借自 lean-production-expert 的 `verify_icon.py`，扩到全skill 维度：

| 检查组 | 项数 | 内容 |
|---|---|---|
| frontmatter | 8 | 必填字段存在性 + name/displayName/version 取值 + description 块标量可解析 |
| description | 14 | 9 个新关键词必含 + 5 个原触发词**必须保留**（防退化） |
| icon | 8 | 路径可解析 / PNG 魔数 / 200×200 尺寸 / SVG 存在 / SVG 含 JESD / viewBox 正确 / 生成脚本存在 |
| meta.json | 5 | name / icon / version / changelog 首条 / last_research_date 与 frontmatter 交叉一致 |
| CLI 回归 | 16 | 全 12 子命令 + `--json` 可解析 + check 的 1 正例 3 反例（含退出码方向） |

**当前状态：全部通过（exit 0）。**

---

## 6. 本轮未做（及原因）

| 项 | 原因 |
|---|---|
| 6 轨 research 重跑 | Phase 0C 判定 `rejected`（0 个月）。内容层 2 天前刚刷新 |
| `references/research/archive/2026-10-07/` | 无research 变动，不产生空archive |
| JESD22 系列 B→A 升级 | JEDEC 服务条款禁止自动抓取（curl 实测 403），只能人工核对 |
| 29 项未核实补齐 | 需付费墙（IEC CHF 260 / JEDEC $284 / SEMI $148-370）或一手内部文件 |
| `master-skill` 的 `skill_writer.py create` 重跑 | 会重写整个 SKILL.md，覆盖本轮手工精修的 14 章正文 |

---

## 7. 变更文件清单

| 文件 | 变更 |
|---|---|
| `SKILL.md` | frontmatter 重写（+displayName/slug/icon/version，description 全换）+ 标题改「半导体标准专家」+ §0 CLI 路径修正 |
| `meta.json` | +displayName/icon/icon_svg/icon_generator/version；name 改中文；+path_note；changelog 加 v1.2.0 条目 |
| `icons/logo.png` | **新增** 200×200「芯片 + JESD」 |
| `icons/logo.svg` | **新增** 矢量源 |
| `tools/make_icon.py` | **新增** 图标生成脚本 |
| `tools/verify_skill.py` | **新增** 全量校验 + CLI 回归 |
| `scripts/stdq.py` | **修复** `cmd_check` 静默缺陷 |
| `README-安装说明.md` | 版本号 v1.1→v1.2.0 + 中文名 + 图标 + 修正安装路径 + 新增自检节 + check 退出码约定 |

**未改动**：`data/standards.json`、`data/relations.json`、`references/**`（含 AQG 324 三版 PDF）——
内容层一字未动，符合 Phase 0C 判定。
