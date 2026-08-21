---
name: qifu-drawer-form
description: 根据业务描述、字段清单、截图或线框,在 Figma 中使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台右侧抽屉表单(新建/编辑/查看)。适用于按稳定名称调用 Simple Create / Sectioned Create / Advanced Create / Edit / Readonly / Data Detail with Table 六种组合，并完成 Header、Form Section、Footer 或摘要+筛选+内嵌表格结构；也用于审查组件缺口。不要用于复杂看板、向导流(Wizard)、带批量编辑的列表页或高度定制的工作台。
---

# Qifu Drawer Form

将简短业务描述转换为结构清楚、可编辑、保持组件实例关系的右侧滑出抽屉表单。把参考图作为信息架构基线,不机械复刻其中的品牌、业务名称或固定字段数。

本 Skill 与 [qifu-list-page](https://github.com/BitPan666/qifu-list-page) 共享同一套 5 层 AI 设计体系;L1 Token、L2 Component、L5 业务上下文是跨原型共享资产,L4 抽屉蓝图是本 Skill 独有。

## 必读资料

开始前完整读取:

- [页面蓝图](references/page-blueprint.md):抽屉结构、宽度阶梯、Header/Footer、Section 与字段规则。
- [字段控件映射](references/field-control-map.md):字段类型 → 真实控件 的路由表。
- [抽屉组合注册表](references/drawer-compositions.md):稳定组合名称、适用场景、组件结构和按名称调用规则。
- 当抽屉包含“摘要信息 + 区块标题 + 筛选控件 + 内嵌表格/分页”时，完整读取[数据详情抽屉 Golden Sample](references/golden-sample-data-detail-drawer.md)，并使用 `Qifu Drawer Form / Data Detail with Table`。
- 当 `platform=yushu` 或用户提到"毓数"时,完整读取[毓数平台导航基线](references/platform-yushu.md)。
- 组件名 / 节点 ID / 发布 Key 全部复用[组件映射](references/component-map.md),不在 `SKILL.md` 重复维护。

任何 `use_figma` 调用前加载并遵循 `figma-use`;创建或更新完整抽屉时同时加载并遵循 `figma-generate-design`。若目标项目另有 `AGENTS.md` 或项目级 Figma 规则,先读取并以其为准。

## 输入契约

接受自然语言,不要求用户填写完整表格。提取或合理补全以下 `DrawerSpec`:

```text
drawerTitle      抽屉标题(动宾:新建 X / 编辑 X / 查看 X)
compositionName  抽屉组合的完整注册名称;未指定时按场景匹配,默认使用 Qifu Drawer Form / Sectioned Create
platform         所属平台;当前默认基准为 yushu
widthTier        480 / 640 / 680 / 840;普通表单默认 640，数据详情表格组合固定 680
maskClosable     默认 false
escClosable      默认 false
sections[]       1..N 个分区,按业务顺序排列
  ├─ sectionTitle   名词性 2-4 字短语:基础信息 / 任务规则 / 选择客群 / 权限设置
  └─ fields[]       1..M 个字段
      ├─ fieldKey     英文字段 ID,如 taskName / triggerEvent
      ├─ label        名词性标签:任务名称 / 所属项目
      ├─ required     是否必填
      ├─ control      Input | Textarea | Select | Radio.Group | Checkbox | Switch | DatePicker |
      │               DateRange | Cascader | Search | InputNumber | Upload | Custom(<BizSlot>)
      ├─ placeholder  空态提示文案
      ├─ options[]    仅 Select / Radio.Group / Checkbox.Group
      ├─ defaultValue 初始值(Edit 组合必填)
      ├─ helpText     控件下方说明
      ├─ widthTier    200 / 304 / 408 / FULL;未指定按 field-control-map 默认值
      └─ disabledCond 何时禁用(可选,文本描述)
footer           覆盖默认 Footer(可选)
  ├─ okText     默认 Create=确定 / Edit=保存 / Readonly=关闭
  ├─ cancelText 默认 取消
  ├─ showCancel 默认 true(Readonly 时 false)
  ├─ danger     可选 {label, confirm} 危险动作,出现在 Footer 最左
  └─ extras[]   可选次要按钮
data             示例数据或 Edit 组合下的回填数据
embeddedTable    仅 Data Detail with Table 使用(可选)
  ├─ columns[]      表头、列宽、排序/筛选开关
  ├─ rows[]         真实数据行
  ├─ tableSize      默认 small 36px
  ├─ tableType      默认 bordered
  ├─ selection      默认 off
  └─ pagination     total / pageSize / current / showPageSize / showJumper
targetPage       Figma 目标 Page;默认与 qifu-list-page 相同,测试固定 Page `测试`(node 3497:651)
```

仅在缺少的信息会改变抽屉主结构或带来高风险误导时提问。其余内容按常见后台表单场景补全,并在交付说明中列出假设。

推荐用户按以下自然语言顺序描述;字段可省略:

```text
在【平台】上【新建/编辑/查看】【对象】,
抽屉标题为【标题】。
分区【1】【名称】包含字段:【标签 + 控件 + 必填?】...
分区【2】【名称】包含字段:...
【可选】Footer 危险/次要动作。
```

解析优先级固定为:平台 → 操作类型(Create/Edit/Readonly)→ 对象 → 抽屉标题 → sections[] → fields[] → Footer。不要把页面对象当成字段标签。

## 工作流

### 1. 形成 DrawerSpec

1. 从描述、截图或线框提取 `DrawerSpec`。
2. 先从[抽屉组合注册表](references/drawer-compositions.md)确定唯一的 `compositionName`:精确匹配的优先,其次按规则推断,无法区分默认 `Sectioned Create`。不得临时创造近义名称或把业务对象名写进组合名。
3. 含摘要、筛选和内嵌表格的数据详情抽屉使用 `Qifu Drawer Form / Data Detail with Table` 与 680px；其余抽屉按字段数与分组判断 `widthTier`:≤ 6 字段无分组可选 480;7–15 字段默认 640;> 12 字段或显式双列用 840。
4. 按 [field-control-map](references/field-control-map.md) 为每个字段分配控件与默认 widthTier。
5. 在 DrawerSpec 中**显式列出**哪些字段是必填,哪些是禁用态及其条件,不允许留空让 AI 自行猜。

### 2. 盘点目标文件

1. 确认目标 Figma 文件、页面和插入位置;不写到组件介绍页或业务 Page。
2. 凡提示词包含"测试""效果验证""试生成"或"Skill 回归",必须复用 Page `测试`(node `3497:651`),规则与 qifu-list-page 完全一致。
3. 检查同文件已有抽屉,优先复用其宽度档位、变量、文字样式和 Section 节奏。
4. 按[组件映射](references/component-map.md)中的精确名称解析所需组件;节点 ID 失效时按名称重新发现。
5. 同文件使用本地组件节点创建实例;跨文件使用发布键导入。
6. 记录组件覆盖结果:`resolved`、`fallback`、`missing`。未完成盘点前不得开始写抽屉。

### 3. 创建抽屉骨架

先创建唯一顶层 Frame(Drawer),再把所有区域直接创建在 Frame 内部。使用 Auto Layout 表达结构关系。以 `Qifu Drawer Form / Sectioned Create` 为例:

```text
Drawer / <pageName> / Create / <compositionName>
├── Drawer / Header (Horizontal, 56px, padding 0 24px, border-bottom)
│   ├── Title
│   └── CloseBtn
├── Drawer / Body (Vertical, fill, scrollable, padding 24px, gap 24px)
│   ├── Section / <name1>
│   │   ├── SectionTitle (16px / 600, bottom 1px border)
│   │   └── FormItem × n
│   ├── Section / <name2>
│   └── Section / <name3>
├── Drawer / Footer (Horizontal, 52px, padding 12 24px, border-top, right-aligned, gap 12)
│   ├── [危险动作区 - 最左]
│   ├── [spacer]
│   ├── Button / Cancel
│   └── Button / OK (primary)
└── Audit / Missing Components(仅有缺口时,放 Drawer 外右侧)
```

抽屉外层用 `frame` 直接管理,不创建"DrawerShell"母版;抽屉宽度档位 = [page-blueprint](references/page-blueprint.md) 中的 Narrow/Standard/Wide。

`Qifu Drawer Form / Data Detail with Table` 不套用上面的通用表单 Section 骨架。必须按 [Golden Sample](references/golden-sample-data-detail-drawer.md) 创建 680px 抽屉、16px 内容安全边距、20/24 内容卡片、真实 Select / Table Shell-V2 / Pagination-V2 实例，以及分页器与表格描边分离的结构。

### 4. 组装 Header 与 Footer

- Header 高度 56px；自由文本 Title 必须应用组件库 `标题/Medium` 文本样式（当前真实定义 16/24），不得手填字体属性。数据详情类标题可使用名词短语；Create/Edit 仍使用动宾结构。
- Header 内**禁止**面包屑、tabs、副标题、secondary 图标——抽屉是单一任务。
- CloseBtn 使用组件库真实 `Icon/basic/close`，可见尺寸固定 16×16，右侧 24px、上下居中；不得用字符 `×`、自绘矢量或错误命名的返回图标代替。
- Footer 高度 52px;按钮从右到左排列:`[OK] [Cancel] [Spacer] [Danger]`。
- 主操作**唯一**,文案严格遵循组合:Create=确定 / Edit=保存 / Readonly=关闭;Advanced Create 的情形才允许 `[提交] [上一步/下一步] [取消]` 组合。
- 危险动作放在 Footer 最左,使用 `Button / variant=danger` + `Popconfirm theme=Danger`;**不放进主操作组**。

### 5. 组装 Form Section

- 按 `DrawerSpec.sections[]` 顺序生成每个 Section。
- 每个 Section:SectionTitle 16px / 600 / `#111827`,padding-bottom 12px,bottom 1px 边。
- Section 间 gap 固定 24px;Section 内字段 gap 固定 16px。
- Section 标题只使用名词性 2-4 字短语:`基础信息` / `任务规则` / `选择客群` / `权限设置`;不写句子,不写疑问。
- 字段顺序:必填在左,短字段在前,Textarea / Upload / RichText 在 Section 末尾。

### 6. 组装字段

- 每个字段使用 FormItem 容器,按 [page-blueprint](references/page-blueprint.md) 第 6 节渲染 label、required 星、controlSlot。
- `control` 由 [field-control-map](references/field-control-map.md) 决定;复合场景(圈选、地图、富文本)使用 `Custom(<BizSlot>)`,节点命名 `Fallback / <BizSlot>`。
- 所有控件**默认 32px 高度**;`widthTier` 严格取 200/304/408/FULL 阶梯。
- `Edit` 组合必须按 `defaultValue` 回填初始值;`Readonly` 组合所有控件为 `disabled=true`,Footer 单一关闭按钮。
- 必填字段的 `*` 由 FormItem 提供,**不手画**,颜色 `#dc2626`,与 label 间距 4px。

### 7. 状态管理

一个抽屉只交付一种状态;默认 `Data`。

- `Data`:字段全部为可编辑默认态,无骨架、无错误提示。
- `Loading`:Footer `OK` 进入 loading,字段用 Skeleton 占位。
- `Disabled`:全部字段 disabled,无主操作。
- `Error`:Body 上方插入 `Alert type=error`,不打断已填值;Loading 失败时使用。

状态切换通过 `DrawerSpec.defaultState` 指定,**不允许在同一抽屉内同时出现两种状态**。

### 8. 处理组件缺口

发现缺失能力时:

1. 优先使用现有组件的合法组合。
2. 不修改组件库母版,不分离实例,不在业务抽屉中创建冒充正式库组件的母版。
3. 使用页面级最小降级实现,节点命名为 `Fallback / <Capability>`。
4. 在 Drawer 右侧创建 `Audit / Missing Components`,逐项写明:
   - 需要的组件或能力;
   - 当前抽屉场景;
   - 当前降级方案;
   - 建议的组件属性与状态。
5. 在交付信息中重复列出缺口,便于维护者补齐组件库。

### 9. 验证

逐区截图检查,再检查整体。至少验证:

- **层级归属检查**:抽屉内所有 Input / Select / Radio / Checkbox / Textarea / Button / Tag 等真实组件 INSTANCE,都必须嵌套在 `Drawer / Header`、`Section / <name>`、`Drawer / Footer` 这三个容器之内;不允许出现在 Page 根级或抽屉 Frame 之外的"孤儿组件"。发现即归位到正确容器。
- **重复节点检查**:抽屉 Frame 内不存在与已嵌实例位置、尺寸几乎一致的重复节点(常见于 AI 未清理旧实例);发现即删除,并计入 Audit / Missing Components。
- 所有设计系统元素仍为 `INSTANCE`,且主组件名称正确。
- `compositionName` 与注册表完全一致,且 Section 数、列模式、Footer 按钮组、默认状态符合该组合;没有出现未注册别名。
- 抽屉宽度属于 `480 / 640 / 840` 三档。
- Header 仅含 Title + CloseBtn,无面包屑/tabs;Title 使用动宾且与 `drawerTitle` 一致。
- Footer 按钮顺序正确,主操作唯一;危险动作使用 `Popconfirm / Danger` 且位于最左。
- Section 间距 24px、字段间距 16px、SectionTitle padding-bottom 12px 且下边 1px。
- Section 顺序符合"基础信息 → 业务规则 → 范围/对象 → 高级"。
- 每个字段 label 宽 96px、右对齐,label 与 control 间距 12px。
- 必填字段的 `*` 位于 label 左侧、色 `#dc2626`。
- 控件可见宽度属于 `200 / 304 / 408 / FULL` 阶梯,默认值符合 field-control-map。
- 所有控件高度均为 32px;同抽屉不混 28/32px。
- `Edit` 组合所有字段已按 `defaultValue` 回填;`Readonly` 全部 disabled,仅"关闭"按钮。
- Textarea / Upload 不会和其他字段并列为 double 列。
- 状态唯一:Data / Loading / Disabled / Error 只有一种。
- 存在缺口时已生成 `Audit / Missing Components`。
- 无文字截断、节点重叠、画板溢出。
- 抽屉外层 Frame 不叠加自定义 padding;所有留白来自 page-blueprint 第 7 节的 10 项铁律。
- `Data Detail with Table` 额外通过 Golden Sample QA：抽屉 680px；Body 内容卡片距抽屉四周 16px；卡片使用纵向 Auto Layout、上下 20px/左右 24px；区块标题使用 `标题/Small`，品牌色 3×12 rail 与标题 gap=5；标题后 Tag gap 绑定 `--qifu-size/8`；标题与正文 gap=16；Form label 左对齐且各控件左边缘对齐，默认 label-control gap=24。
- `Data Detail with Table` 的页面级普通正文与 Form label 必须绑定组件库 `Body/Regular`（PingFang SC Regular 14/22）；禁止使用 `Body/Medium`、Bold 或手填字体属性。Header Title、Section Title、表头和链接仍保持各自语义样式，不得为了“统一”一并改成 Regular。
- 表格正文必须由 `Data Display / Table / Cell Content / Text-V2` 的 `contentFont 内容字号=14px` 组件变体继承 `Body/Regular` 14/22；不得在 30 个页面实例上逐个覆盖。表头继续使用 Header Cell-V2 的 Semibold 层级。
- 内嵌表格的 Table Shell-V2、Header Cell-V2、Row-V2、Content Cell-V2、Text-V2、Pagination-V2 必须全部为组件库真实实例；表格描边只包围表头与数据行，分页器位于描边外。
- `Data Detail with Table` 的内容 Section 与 `Table Border / 四边完整` 统一使用 4px 圆角。Table Border 必须是单独 Frame：1px Inside 描边、`Clip content=true`；表头、数据行和列分割线放入其中，Pagination 不得成为该边框的可见内容。
- 非 Empty / Loading 状态下，表格每个可见数据行的每个可见单元格必须有真实内容；表头与数据行逐列同宽，所有列宽之和必须精确等于 Table Border 内容宽度，不得依赖裁剪隐藏横向溢出。
- 全部页面级 Frame / Rectangle / Instance 的 x、y、width、height、padding、gap、圆角和描边宽度必须为整数；发现缩放造成的小数即 FAIL，替换为未缩放组件实例或整数重建，不做四舍五入式视觉蒙混。
- 自由文本必须应用组件库文本样式；组件实例内部文字由组件自身管理。组件库不存在指定文本样式时报告 `STYLE_MISSING`，不得自行生成近似字体。

## 硬性约束

- 不把参考图直接作为图片放进抽屉交付。
- 不重画已有组件,不分离实例来改外观。
- 不为追求截图相似度破坏组件属性或变量绑定。
- 不擅自改动、补充或发布组件库母版。
- 不为抽屉新增"DrawerShell"等 Figma 母版;Drawer 是页面级框架组合,不是组件库资产。
- 不在同一抽屉堆叠多状态或混合控件高度。
- 不把复杂看板、向导流、批量编辑硬塞进本 Skill。
- 不宣称缺失组件已存在;明确区分正式实例与降级组合。

## 已知限制

> 按时间倒序,最新在最前。跑通后发现的限制统一放这里,不散落在正文各处。
> 仓库内回填方式见 `_docs/limit-backfill.md`(仅发布仓)。

### 2026-08-21 · 数据详情抽屉 Golden Sample
- Golden Sample 为组件库文件 Page `02 From 训练过程` 的 `Page / Drawer / 数据详情 / 本地组件重制版 · 0820`（node `4659:420`）；未来同类抽屉先复用其版式语法，再替换业务数据。
- 自动生成验证样例为同 Page 的 `Golden Sample / Drawer / 数据详情 / 680 · 0821`（node `4725:1548`）；其表格四边框、独立分页器、真实组件引用、Auto Layout 和整数几何已按本 Skill 验收。
- 两张样例中的页面级任务正文与 Form label 已统一绑定 `Body/Regular` 14/22；`Body/Medium` 会造成正文误加粗，后续生成与回归验收均判定为 FAIL。
- 组件库现有 `标题/Medium` 的真实定义是 16/24，没有独立 16/20 标题样式；必须使用现有样式并报告此差异，不允许手工覆盖行高。
- `Text-V2 / contentFont 内容字号=14px` 的组件母版正文已绑定 `Body/Regular` 14/22。Tag、Select、Header Cell、Pagination 等其余部分组件内部 Text 仍可能未绑定 Text Style；页面层不得 detach 或覆盖字体，只报告 `COMPONENT_SOURCE_GAP` 并把修复留给组件母版。页面级自由 Text 仍必须 100% 绑定组件库 Text Style。
- 手工样例中存在缩放遗留的小数尺寸，生成稿必须使用未缩放实例与整数几何消除。

### 2026-08-12 · 新建触发式任务抽屉
- 抽屉 Frame 内所有控件 INSTANCE 必须嵌套在 `Drawer/Header | Section/<name> | Drawer/Footer` 三容器之一,不允许 Page 根级孤儿(详见验证清单"层级归属检查")
- 抽屉 Frame 内不允许存在与已嵌实例位置/尺寸几乎一致的重复节点(详见验证清单"重复节点检查")
- 配套兜底工具:`Component Library/.figma-plugins/qifu-drawer-cleanup/`(在外部仓,可改写为"选中即清"版本)

## 交付内容

完成后返回:

- 抽屉节点 ID 与名称;
- 使用的 `compositionName`;
- 使用的主要组件及关键变体;
- Section 清单与字段总数;
- 对输入描述做出的假设;
- 组件缺口及建议补充项;
- 视觉和结构验证结果。
