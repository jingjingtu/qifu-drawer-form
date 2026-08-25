---
name: qifu-drawer-form
description: 根据业务描述、字段清单、截图或线框,在 Figma 中使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台右侧抽屉表单(新建/编辑/查看)。正式交付一律生成 1366×768 页面打开态:完整底图 + 蒙层 + 右侧抽屉。适用于按稳定名称调用 Simple Create / Sectioned Create / Advanced Create / Edit / Readonly / Data Detail with Table 六种组合，并完成 Header、Form Section、Footer 或摘要+筛选+内嵌表格结构。不要用于复杂看板、向导流(Wizard)、带批量编辑的列表页或高度定制的工作台。
---

# Qifu Drawer Form

将简短业务描述转换为结构清楚、可编辑、保持组件实例关系的右侧滑出抽屉表单。把参考图作为信息架构基线,不机械复刻其中的品牌、业务名称或固定字段数。

本 Skill 与 [qifu-list-page](https://github.com/BitPan666/qifu-list-page) 共享同一套 5 层 AI 设计体系;L1 Token、L2 Component、L5 业务上下文是跨原型共享资产,L4 抽屉蓝图是本 Skill 独有。

## 必读资料

开始前完整读取:

- [页面蓝图](references/page-blueprint.md):抽屉结构、宽度阶梯、Header/Footer、Section 与字段规则。
- [字段控件映射](references/field-control-map.md):字段类型 → 真实控件 的路由表。
- [抽屉组合注册表](references/drawer-compositions.md):稳定组合名称、适用场景、组件结构和按名称调用规则。
- [平台与主题切换协议](references/platform-theme-switching.md):`platformKey`、`themeKey`、智客星/毓数/智能运营平台切换、主题变量回读和示例提示词。
- [Figma 执行与结构化验收](references/figma-execution-validation.md):截图解析、组件解析闭环、Slot 验证、P0 失败即停和 PASS/BLOCKED/FAIL 判定。
- 当抽屉包含“摘要信息 + 区块标题 + 筛选控件 + 内嵌表格/分页”时，完整读取[数据详情抽屉 Golden Sample](references/golden-sample-data-detail-drawer.md)，并使用 `Qifu Drawer Form / Data Detail with Table`。
- 当 `platform=yushu` 或用户提到"毓数"时,完整读取[毓数平台导航基线](references/platform-yushu.md)。
- 当创建正式抽屉交付时，必须完整读取[智客星列表页底图协议](references/zhikexing-list-background.md)，以及其中列出的 `zhikexing-list-page` 资料；智客星默认使用该协议的模板底图。
- 当用户指定 `PORTABLE_KIT` 或说明没有正式组件库权限时,完整读取[Portable Kit 模式](references/portable-kit.md)与[Portable 组件清单](references/portable-component-manifest.json)。
- 组件名 / 节点 ID / 发布 Key 全部复用[组件映射](references/component-map.md),不在 `SKILL.md` 重复维护。

任何 `use_figma` 调用前加载并遵循 `figma-use`;创建或更新完整抽屉时同时加载并遵循 `figma-generate-design`。若目标项目另有 `AGENTS.md` 或项目级 Figma 规则,先读取并以其为准。

## 输入契约

接受自然语言,不要求用户填写完整表格。提取或合理补全以下 `DrawerSpec`:

```text
drawerTitle      抽屉标题(动宾:新建 X / 编辑 X / 查看 X)
componentMode    组件来源模式:REAL_COMPONENT_ONLY(默认) | PORTABLE_KIT | VISUAL_FALLBACK
compositionName  抽屉组合的完整注册名称;未指定时按场景匹配,默认使用 Qifu Drawer Form / Sectioned Create
platformKey      平台唯一标识:zhikexing | yushu | zhineng-yunying | qifu-generic
platformName     平台中文名:智客星 | 毓数 | 智能运营平台 | 奇富通用后台
themeKey         主题标识:zhikexing-green | yushu-green | smartops-blue | custom
themePrimary     主题主色;custom 必填,如 #1677FF
themeMode        light;当前仅支持浅色后台
presentationMode  展示模式:DRAWER_OPEN_WITH_BACKGROUND(默认) | OVERLAY_ON_ZHIKEXING_LIST(智客星兼容别名) | STANDALONE_DEBUG(仅内部调试)
background        正式交付必填或自动补全
  ├─ source       TEMPLATE(智客星默认) | EXISTING_LIST_PAGE
  ├─ sourceNode   EXISTING_LIST_PAGE 时必填
  ├─ sidePath[]   底图菜单路径，仅修改模板中已存在的菜单状态
  └─ pageName     底图业务页名称，仅用于 Scene 命名
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

平台与主题必须分开处理:

- `platformKey` 决定平台壳、菜单、业务词汇、底图协议和平台缺口;不得用主题色当平台名。
- `themeKey` / `themePrimary` 只决定主按钮、选中态、链接色、轻量标签和强调色;不得改变字段顺序、控件类型、间距、圆角、阴影或 Slot 结构。
- 用户明确说“智客星”时,解析为 `platformKey=zhikexing` 与 `themeKey=zhikexing-green`;默认 `presentationMode=DRAWER_OPEN_WITH_BACKGROUND`，等价使用已验证智客星列表页底图。
- 用户明确说“毓数”时,解析为 `platformKey=yushu` 并读取 `platform-yushu.md`;不再把毓数作为跨平台默认值。
- 用户明确说“智能运营平台”或“蓝色主题智能运营平台”时,解析为 `platformKey=zhineng-yunying`、`themeKey=smartops-blue`、`themePrimary=#1677FF`；仍必须生成 `1366×768` 打开态，若缺少专属底图模板则停止并返回 `BACKGROUND_TEMPLATE_MISSING`。
- 用户未指定平台时,使用 `platformKey=qifu-generic`；仍必须生成 `1366×768` 打开态，不得退回裸抽屉。若没有用户指定或已批准的通用底图，返回 `BACKGROUND_TEMPLATE_MISSING`。

组件来源模式必须显式区分:

- `REAL_COMPONENT_ONLY`:使用已启用的正式 Figma Library 与发布组件。任一必需组件、变体、样式或 Slot 无法解析时,在写入业务画板前停止并返回 `COMPONENT_LIBRARY_UNAVAILABLE` 或 `COMPONENT_MISSING`;不得创建视觉降级图层。
- `PORTABLE_KIT`:使用当前目标文件内已复制的本地组件。不得依赖原 Library 的 `publishedKey`;按[Portable 组件清单](references/portable-component-manifest.json)的精确名称查找本地 `COMPONENT` / `COMPONENT_SET`,创建后必须验证 `INSTANCE.mainComponent`。
- `VISUAL_FALLBACK`:只有用户明确选择时才允许页面级降级。所有降级节点必须命名为 `Fallback / ...`,并在抽屉外生成 `Audit / Missing Components`;它们不是正式组件实例。

未指定 `componentMode` 时一律使用 `REAL_COMPONENT_ONLY`,不能根据导入失败自动切换到 `VISUAL_FALLBACK`。

文本样式必须显式区分:

- 正式交付 Scene 内所有新增 `TEXT` 节点都必须绑定组件库自带 Text Style，禁止手填 `fontName / fontSize / lineHeight / letterSpacing` 来近似。
- 创建任何文字前先读取目标文件可用 Text Style，并形成 `TextStyleResolutionManifest`：`usage / requiredStyleName / styleId / fontFamily / fontSize / lineHeight / status`。
- 默认映射：Header Title 使用 `标题/Medium`；Section Title 使用 `标题/Small`；Form label、帮助文字、说明正文、审计说明、规则区域中的连接文字使用 `Body/Regular`；表格正文通过真实 `Text-V2` 实例继承 `Body/Regular`。
- 组件实例内部文字由组件母版管理，不 detach、不在实例层手工覆盖字体。若真实组件母版内部文字未绑定 Text Style，返回 `COMPONENT_SOURCE_GAP`，并说明需要回到组件母版修复。
- `TextStyleResolutionManifest` 任一必需样式缺失时返回 `STYLE_MISSING`，不得继续生成游离字体或手工字号。

仅在缺少的信息会改变抽屉主结构或带来高风险误导时提问。其余内容按常见后台表单场景补全,并在交付说明中列出假设。

推荐用户按以下自然语言顺序描述;字段可省略:

```text
在【平台】上【新建/编辑/查看】【对象】,
平台标识为【platformKey】,主题为【themeKey / themePrimary】。
抽屉标题为【标题】。
分区【1】【名称】包含字段:【标签 + 控件 + 必填?】...
分区【2】【名称】包含字段:...
【可选】Footer 危险/次要动作。
```

智客星完整打开态可追加；未写时也默认使用该模式：

```text
展示方式：完整页面打开态；底图使用智客星列表页模板；
当前菜单：【一级菜单 / 二级菜单】。
```

解析优先级固定为:平台与主题 → 操作类型(Create/Edit/Readonly)→ 对象 → 抽屉标题 → sections[] → fields[] → Footer。不要把页面对象当成字段标签。

### 截图与参考图输入规则

当用户提供截图、PNG、线框或 Sketch 时，参考图只用于识别结构、层级、比例和可见字段，不作为最终交付图层，也不能覆盖用户文字描述。

1. 从参考图识别 Header、Body、Section、Form Row、Footer、遮罩、抽屉边界和背景页；截图中的水印、批注、红线、演示光标、浏览器边框和讲解黑底全部视为噪声。
2. 从用户描述确定业务文案、字段语义、必填状态、选项、交互和目标文件；参考图只能补充用户未写明的视觉结构。
3. 为每个识别结果记录 `evidence = user-description | screenshot | inferred`。影响组件选择、页面层级或写入位置的内容不得只依赖 `inferred`，必须在交付说明中列为假设。
4. 参考图中看起来像输入框、下拉框、单选、表格或按钮的图层，不得直接复制为最终控件；必须按组件映射和目标文件已启用的库重新解析为真实组件实例。
5. 参考素材可放在目标画板外侧并锁定，命名 `Reference / <drawerTitle> / Source`；最终 Drawer 或 Scene 内不得包含参考图栅格、讲解黑底、标题或红色标注箭头。

## 工作流

### 1. 形成 DrawerSpec

1. 从描述、截图或线框提取 `DrawerSpec`。
2. 按[平台与主题切换协议](references/platform-theme-switching.md)解析 `platformKey / platformName / themeKey / themePrimary`。平台缺失时使用 `qifu-generic`,不得默认套用毓数。
3. 解析 `presentationMode`：未指定时固定为 `DRAWER_OPEN_WITH_BACKGROUND`。`OVERLAY_ON_ZHIKEXING_LIST` 视为智客星旧提示词兼容别名；`STANDALONE_DEBUG` 只允许在用户明确说“内部调试抽屉本体/不交付”时使用。
4. 先从[抽屉组合注册表](references/drawer-compositions.md)确定唯一的 `compositionName`:精确匹配的优先,其次按规则推断,无法区分默认 `Sectioned Create`。不得临时创造近义名称或把业务对象名写进组合名。
5. 含摘要、筛选和内嵌表格的数据详情抽屉使用 `Qifu Drawer Form / Data Detail with Table` 与 680px；其余抽屉按字段数与分组判断 `widthTier`:≤ 6 字段无分组可选 480;7–15 字段默认 640;> 12 字段或显式双列用 840。
6. 按 [field-control-map](references/field-control-map.md) 为每个字段分配控件与默认 widthTier。
7. 将操作分为 Header 关闭、Body 局部操作、Footer 次操作和唯一主操作；同一动作只出现一次。
8. 在 DrawerSpec 中**显式列出**哪些字段是必填,哪些是禁用态及其条件,不允许留空让 AI 自行猜。

### 2. 盘点目标文件

1. 确认目标 Figma 文件、页面和插入位置;不写到组件介绍页或业务 Page。
2. 凡提示词包含"测试""效果验证""试生成"或"Skill 回归",必须复用 Page `测试`(node `3497:651`),规则与 qifu-list-page 完全一致。
3. 用户已指定 `targetPage`、当前画板或明确要求“只改这个画板”时，将该 Page 和画板 ID 视为唯一读写边界；不得因调试、审计、截图或 Skill 默认值切换到 `测试` 或其他 Page。
4. 检查同文件已有抽屉,优先复用其宽度档位、变量、文字样式和 Section 节奏。
5. 正式交付模式下，先按[智客星列表页底图协议](references/zhikexing-list-background.md)解析并验证背景来源；背景模板或现有列表页不合格时停止并返回相应错误，未完成底图预检前不得创建 Drawer。智客星可默认使用模板；其他平台必须有已批准模板或用户指定 `EXISTING_LIST_PAGE`，否则返回 `BACKGROUND_TEMPLATE_MISSING`。
6. 先执行组件来源预检:
   - `REAL_COMPONENT_ONLY`:确认目标文件已启用奇富组件库,并逐项验证发布 Key 可导入;
   - `PORTABLE_KIT`:读取[Portable 组件清单](references/portable-component-manifest.json),使用 `figma.getLocalComponentsAsync()` 按精确名称解析;
   - `VISUAL_FALLBACK`:记录用户明确授权的视觉降级范围。
7. 按[组件映射](references/component-map.md)中的精确名称解析所需组件;节点 ID 失效时按名称重新发现。
8. 组件解析必须遵循“精确名称/本地节点 → 发布 Key → 唯一候选”顺序。同名候选为 0 或多于 1 时分别报告 `COMPONENT_MISSING` 或 `COMPONENT_AMBIGUOUS`，不得按相似外观、末段名称或第一个搜索结果猜选。
9. 同文件使用本地组件节点创建实例;跨文件使用发布键导入。创建任何业务 Frame 前,确认必需组件的来源模式检查已通过。
10. 形成 `ComponentResolutionManifest`：每项必须包含 `capability / exactName / sourceFile / nodeId 或 publishedKey / publicProperties / expectedCount / slotTarget / status / evidence`。
11. 记录组件覆盖结果:`resolved`、`fallback`、`missing`、`ambiguous`、`unverified`。`REAL_COMPONENT_ONLY` 与 `PORTABLE_KIT` 下必需能力未全部 `resolved` 时停止写入业务画板。
12. 主题来源预检必须在写入页面前完成：优先绑定目标文件现有变量或组件公开属性；无法绑定主题主色时返回 `THEME_VARIABLE_MISSING` 或记录 `COMPONENT_SOURCE_GAP`，不得 detach 组件手工改色。
13. 文本样式预检必须在写入任何 `TEXT` 前完成：枚举并解析 `标题/Medium`、`标题/Small`、`Body/Regular` 等必需组件库 Text Style，形成 `TextStyleResolutionManifest`；任一缺失即返回 `STYLE_MISSING`。

### 3. 创建抽屉骨架

正式交付时必须先创建 `1366 x 768` 的 `Scene / Drawer / <pageName> / <drawerTitle>`，再按[智客星列表页底图协议](references/zhikexing-list-background.md)放入完整列表页 `Background`，其上创建绑定语义遮罩变量的 `Overlay Mask`，最后把本节 Drawer 放在最上层并右侧贴边。`presentationMode=OVERLAY_ON_ZHIKEXING_LIST` 仅作为智客星旧提示词兼容别名；该模式不改变 `compositionName`、字段、Footer 或抽屉宽度规则。`STANDALONE_DEBUG` 不得作为正式交付。

在 Scene 内创建唯一 Drawer Frame,再把所有区域直接创建在 Drawer 内部。使用 Auto Layout 表达结构关系。以 `Qifu Drawer Form / Sectioned Create` 为例:

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

`Qifu Drawer Form / Data Detail with Table` 不套用上面的通用表单 Section 骨架。必须按 [Golden Sample](references/golden-sample-data-detail-drawer.md) 创建 `1366×768` Scene：完整真实列表页底图 < Overlay Mask < 右侧 680px 抽屉；不得用 IMAGE 矩形或截图充当底图。抽屉内部使用 16px 内容安全边距、20/24 内容卡片、真实 Select / Table Shell-V2 / Pagination-V2 实例，以及分页器与表格描边分离的结构。

骨架阶段只能建立最终父级和空的 `Control / <fieldKey>` 容器，或无外观占位节点。禁止先用矩形、边框、箭头、图标、文字或旧控件画出一套可见的临时 Input、Select、Radio、Textarea、Table 或 Button。

### 4. 组装 Header 与 Footer

- Header 高度 56px；自由文本 Title 必须应用组件库 `标题/Medium` 文本样式（当前真实定义 16/24），不得手填字体属性。数据详情类标题可使用名词短语；Create/Edit 仍使用动宾结构。
- Header 内**禁止**面包屑、tabs、副标题、secondary 图标——抽屉是单一任务。
- CloseBtn 使用组件库真实 `Icon/basic/close`，可见尺寸固定 16×16，右侧 24px、上下居中；不得用字符 `×`、自绘矢量或错误命名的返回图标代替。
- Footer 高度 52px;按钮从右到左排列:`[OK] [Cancel] [Spacer] [Danger]`。
- 主操作**唯一**,文案严格遵循组合:Create=确定 / Edit=保存 / Readonly=关闭;Advanced Create 的情形才允许 `[提交] [上一步/下一步] [取消]` 组合。
- 危险动作放在 Footer 最左,使用 `Button / variant=danger` + `Popconfirm theme=Danger`;**不放进主操作组**。
- Footer 主按钮、Radio 选中态、链接、轻量标签和强调色必须来自 `themeKey/themePrimary` 对应变量或组件公开属性；平台切换不得改变按钮顺序或主操作数量。

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
- 每个字段只能有一个语义控件：`Control / <fieldKey>` 内只能保留一个真实组件实例，或一个已记录的合法 `Fallback / <Capability>` 子树；禁止实例与临时控件、旧实例、自由文本、边框或图标重叠共存。
- 占位文案、值、箭头、单选状态和按钮文案必须来自组件实例及其公开属性；不得在实例上方额外覆盖同文案或同图形。
- 若目标位置已有临时控件或旧控件，替换必须作为一次原子操作完成：创建并定位真实实例，验证 `type=INSTANCE` 与 `mainComponent`，随后立即删除原控件的完整旧子树。隐藏、透明度 `0`、移出画板或锁定旧层均不算删除。
- 实例必须位于对应字段标签右侧并与标签同行。移动或重新归属实例时，先将实例放入最终父层，再重新读取实例与标签的 `absoluteBoundingBox`，使用当前绝对坐标差值调整位置；禁止用归层前缓存的父容器边界计算相对坐标。
- 每个组件属性必须完成闭环：读取实例 `componentProperties` → 解析唯一真实 Key → 校验类型和值域 → 写入 → 重新读取 → 验证最终值。写入失败、Key 不唯一、枚举值不匹配或回读不一致均为失败，不得用实例外文字覆盖。
- Slot 只能放真实实例或已批准的空占位；禁止把裸 Text、矩形、Group、截图或页面级手绘表格写入 Drawer、Section、Form Row、Table 或 Pagination Slot。替换 Slot 后必须回读当前值、实例数量、`mainComponent` 和父级 Auto Layout。
- Close、Radio、Checkbox、Switch 等小控件替换后，必须扫描实例实际图形区域附近的实例外 `VECTOR`、`ELLIPSE`、`LINE`、`BOOLEAN_OPERATION`、`GROUP` 和 `TEXT`。Close 的旧自由文本 `×/x` 也属于残留；Radio 的扫描锚点是选项文字左侧的圆形控件区域。

### 6.1 关键控件细节规则

以下规则属于生成步骤的一部分，不能只在最后验收时发现再补救。

#### DateRange / 有效期

- `有效期`、`创建时间`、`发生时间` 等日期范围字段必须使用真实 `录入组件 / DatePicker / Input / DateRange` 实例。
- 当 DateRange 被拉宽到 304 / 408 / FULL 或跟随 controlSlot 宽度时，日历图标必须仍然位于实例内部最右侧，右边距跟随组件 padding（通常 12px），视觉上与同宽 Select 的后缀箭头对齐。
- 若日历图标贴在占位文字后方，先尝试设置 DateRange 实例外层 Auto Layout 为 `primaryAxisAlignItems=SPACE_BETWEEN`，同时保持 `paddingLeft=12 / paddingRight=12`。
- 不允许把日历图标从实例内部拖出来，也不允许在实例外叠加 `Icon/basic/calendar`、裸 Vector、截图或覆盖层。
- 如果 Figma 拒绝实例级布局覆盖，返回 `COMPONENT_SOURCE_GAP: DateRange suffix alignment`，说明需要修组件母版；不得 detach DateRange。

#### Custom(OverFrequencyRule) / 超频规则

- 当字段语义为“超频规则 / 频控规则 / 触达频次规则”时，`control` 必须解析为 `Custom(OverFrequencyRule)`。
- `Custom(OverFrequencyRule)` 不是缺失组件 Fallback，而是一个由真实 Select、Input、Icon 组件组合成的页面级规则面板；不得命名为 `Fallback / ...`。
- 面板节点命名 `Custom Rule Area / 超频规则`，放在 `Control / overFrequencyRule` 内，宽度跟随 controlSlot，右边缘与其他控件右边缘对齐。
- 面板填充 `#F5F7FA` 或绑定等价背景变量，圆角 4px；内容自适应高度，三行规则示例高度为 152px，不用 144px 压缩。
- 规则面板内边距：top 16px、bottom 16px、left 24px；right 默认 24px，可按图标和控件的视觉平衡微调，但不能导致内容贴边。
- 规则行高度统一 32px；策略类型行、第一行规则、第二行规则之间的垂直间距统一 12px。
- “策略类型”这类面板内部短标签称为“规则区内联标签”，使用页面级 Text 且绑定组件库 `Body/Regular`；它到 Select 左边的距离固定 8px。
- 规则行内的连接文字“每 / 天，触达 / 条”使用页面级 Text 且绑定 `Body/Regular`；文字、Input、图标之间默认 8px 间距。
- 添加按钮必须使用真实 `Icon/basic/plus-square` 实例；减少按钮必须使用真实 `Icon/basic/Minus-Square` 实例；均使用 24×24 容器、内部 16×16 图形，不允许手绘。
- 标准结构：

```text
Control / overFrequencyRule
└── Custom Rule Area / 超频规则
    ├── Rule Row / 策略类型
    │   ├── Rule Inner Label / 策略类型
    │   └── INSTANCE / Select / 策略类型
    ├── Rule Row / 01
    │   ├── Rule Text 每
    │   ├── INSTANCE / Input / 天数
    │   ├── Rule Text 天，触达
    │   ├── INSTANCE / Input / 条数
    │   ├── Rule Text 条
    │   └── INSTANCE / Icon/basic/plus-square
    └── Rule Row / 02
        ├── Rule Text 每
        ├── INSTANCE / Input / 天数
        ├── Rule Text 天，触达
        ├── INSTANCE / Input / 条数
        ├── Rule Text 条
        ├── INSTANCE / Icon/basic/plus-square
        └── INSTANCE / Icon/basic/Minus-Square
```

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
3. `REAL_COMPONENT_ONLY` 与 `PORTABLE_KIT` 模式下不得自动降级:
   - `REAL_COMPONENT_ONLY` 返回 `COMPONENT_LIBRARY_UNAVAILABLE` / `COMPONENT_MISSING` 并停止写入;
   - `PORTABLE_KIT` 返回 `PORTABLE_COMPONENT_MISSING` 并停止写入。
4. 仅 `VISUAL_FALLBACK` 模式使用页面级最小降级实现,节点命名为 `Fallback / <Capability>`。
5. 在允许降级的模式下,于 Drawer 右侧创建 `Audit / Missing Components`,逐项写明:
   - 需要的组件或能力;
   - 当前抽屉场景;
   - 当前降级方案;
   - 建议的组件属性与状态。
6. 在交付信息中重复列出缺口,便于维护者补齐组件库或 Portable Kit。

### 9. 验证

按 [Figma 执行与结构化验收](references/figma-execution-validation.md) 的顺序执行：`DrawerSpec 完整性 → ComponentResolutionManifest → 实例属性回读 → 页面结构计数 → Slot 与父级关系 → 变量与几何 → 分区截图 → 整页截图`。前一阶段失败时停止，不使用截图或肉眼观感掩盖结构失败。逐区截图检查,再检查整体。至少验证:

- 交付结果必须分别给出 `structuralValidation = PASS|BLOCKED|FAIL` 和 `visualValidation = PASS|BLOCKED|FAIL`；只有两者均为 `PASS` 才能宣称完成。
- **层级归属检查**:抽屉内所有 Input / Select / Radio / Checkbox / Textarea / Button / Tag 等真实组件 INSTANCE,都必须嵌套在 `Drawer / Header`、`Section / <name>`、`Drawer / Footer` 这三个容器之内;不允许出现在 Page 根级或抽屉 Frame 之外的"孤儿组件"。发现即归位到正确容器。
- **重复节点检查**:抽屉 Frame 内不存在与已嵌实例位置、尺寸几乎一致的重复节点(常见于 AI 未清理旧实例);发现即删除,并计入 Audit / Missing Components。
- 所有设计系统元素仍为 `INSTANCE`,且主组件名称正确。
- `REAL_COMPONENT_ONLY` 下不得出现任何 `Fallback /` 节点;`PORTABLE_KIT` 下所有控件 INSTANCE 的 `mainComponent` 必须属于当前文件本地组件;`VISUAL_FALLBACK` 下必须存在对应审计。
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
- DateRange 拉宽后日历图标必须仍在组件内部右侧，右边距跟随组件 padding；优先用实例外层 `primaryAxisAlignItems=SPACE_BETWEEN` 修正，不允许实例外覆盖图标或 detach。
- `Custom(OverFrequencyRule)` 超频规则面板必须符合 field-control-map 专项规则：浅灰底 `#F5F7FA`、top/bottom padding 16px、left padding 24px、规则区内联标签到 Select gap 8px、内部规则行 gap 12px、添加/减少为真实图标实例。
- 每个 Form Row 只有一个语义控件根节点；不存在临时控件、旧实例或自由文本与真实实例占用同一控件区域。
- 组件文案、箭头、选中圆点和按钮内容位于组件实例子树内，没有实例外的同文案或同图形覆盖层。
- Close 实例的图形边界附近不存在实例外 `×/x`、线段或矢量；Radio 每个选项文字左侧的控件区域不存在实例外圆环、椭圆或矢量。不能只验证实例数量、父层、坐标和 `mainComponent`。
- `Edit` 组合所有字段已按 `defaultValue` 回填;`Readonly` 全部 disabled,仅"关闭"按钮。
- Textarea / Upload 不会和其他字段并列为 double 列。
- 状态唯一:Data / Loading / Disabled / Error 只有一种。
- 存在缺口时已生成 `Audit / Missing Components`。
- 无文字截断、节点重叠、画板溢出。
- 正式交付额外验证 Scene、Background、Overlay Mask 均为 `1366 x 768`，图层顺序为 Background < Overlay Mask < Drawer，Drawer 贴 Scene 右侧，且截图中底图被压暗而 Drawer 保持清晰。
- 组合模式背景必须继续通过 `zhikexing-list-page` 的 Header、侧栏、Shell、Filter Bar、Table Shell 与 Pagination 结构检查；底图不得是截图、展平图层、裸 Text 或 Slot 覆盖物。
- 抽屉外层 Frame 不叠加自定义 padding;所有留白来自 page-blueprint 第 7 节的 10 项铁律。
- `Data Detail with Table` 额外通过 Golden Sample QA：抽屉 680px；Body 内容卡片距抽屉四周 16px；卡片使用纵向 Auto Layout、上下 20px/左右 24px；区块标题使用 `标题/Small`，品牌色 3×12 rail 与标题 gap=5；标题后 Tag gap 绑定 `--qifu-size/8`；标题与正文 gap=16；Form label 左对齐且各控件左边缘对齐，默认 label-control gap=24。
- `Data Detail with Table` 的页面级普通正文与 Form label 必须绑定组件库 `Body/Regular`（PingFang SC Regular 14/22）；禁止使用 `Body/Medium`、Bold 或手填字体属性。Header Title、Section Title、表头和链接仍保持各自语义样式，不得为了“统一”一并改成 Regular。
- 字体预检必须在写入文字前完成;`PingFang SC Regular` 与 `Body/Regular` 不可用时,`REAL_COMPONENT_ONLY` / `PORTABLE_KIT` 直接返回 `STYLE_MISSING`,不得仅加载字体后继续使用 Figma 默认字体。
- 正式交付 Scene 内所有新增页面级 `TEXT` 必须有非空 `textStyleId`，且 `textStyleId` 来自 `TextStyleResolutionManifest`；禁止仅用相同字体名、字号或行高冒充组件库文本样式。
- 表格正文必须由 `Data Display / Table / Cell Content / Text-V2` 的 `contentFont 内容字号=14px` 组件变体继承 `Body/Regular` 14/22；不得在 30 个页面实例上逐个覆盖。表头继续使用 Header Cell-V2 的 Semibold 层级。
- 内嵌表格的 Table Shell-V2、Header Cell-V2、Row-V2、Content Cell-V2、Text-V2、Pagination-V2 必须全部为组件库真实实例；表格描边只包围表头与数据行，分页器位于描边外。
- `Data Detail with Table` 的内容 Section 与 `Table Border / 四边完整` 统一使用 4px 圆角。Table Border 必须是单独 Frame：1px Inside 描边、`Clip content=true`；表头、数据行和列分割线放入其中，Pagination 不得成为该边框的可见内容。
- 非 Empty / Loading 状态下，表格每个可见数据行的每个可见单元格必须有真实内容；表头与数据行逐列同宽，所有列宽之和必须精确等于 Table Border 内容宽度，不得依赖裁剪隐藏横向溢出。
- 新建的页面组合层（Scene、Background、Overlay Mask、Drawer、内容卡片、Table Border、Pagination 容器）以及其自由布局属性的 x、y、width、height、padding、gap、圆角和描边宽度必须为整数；发现本次缩放造成的小数即 FAIL，替换为未缩放实例或整数重建。正式组件实例内部的 Vector、Text、Slot 或由母版 Auto Layout 计算出的分数值不做页面层修正，不得为凑整数 detach 或改写母版。
- 自由文本必须应用组件库文本样式；组件实例内部文字由组件自身管理。组件库不存在指定文本样式时报告 `STYLE_MISSING`，不得自行生成近似字体。
- 整页截图前必须扫描最终 Scene 内所有 `TEXT`：页面级 Text 无 `textStyleId`、使用非组件库 Text Style、或出现手填字体属性覆盖均为 `FAIL`；组件实例内部 Text 若未绑定样式，记录 `COMPONENT_SOURCE_GAP` 并保持实例关系。
- 截图识别出的每个字段、操作和页面区域都有 `evidence`，且截图噪声未进入最终画板。
- 平台与主题回读通过：交付结果中 `platformKey / platformName / themeKey / themePrimary` 与用户输入一致；主题主色只影响允许的语义颜色，不改变抽屉结构、控件高度、间距、圆角、阴影和 Slot 关系。

## 硬性约束

- 不把参考图直接作为图片放进抽屉交付。
- 正式交付不得临时手绘、截图化或缩放底图；只允许复制已验证模板或用户指定并验收通过的现有列表页。
- 不把 `yushu` 当作跨平台默认值；用户未指定平台时使用 `qifu-generic`，但仍必须生成 `1366×768` 打开态，不能退回裸抽屉。
- 不把主题色当作平台,也不因为 `themeKey=smartops-blue` 改变业务字段、组件组合或页面结构。
- 不为蓝色主题复制一套组件库、分离组件实例或手改组件内部颜色；主题切换只能走变量、公开属性或记录组件缺口。
- 不重画已有组件,不分离实例来改外观。
- 不为追求截图相似度破坏组件属性或变量绑定。
- 不擅自改动、补充或发布组件库母版。
- 不为抽屉新增"DrawerShell"等 Figma 母版;Drawer 是页面级框架组合,不是组件库资产。
- 不在同一抽屉堆叠多状态或混合控件高度。
- 不把复杂看板、向导流、批量编辑硬塞进本 Skill。
- 不宣称缺失组件已存在;明确区分正式实例与降级组合。
- 不因发布 Key 导入失败而静默切换模式;模式只能由用户在 DrawerSpec 中显式指定。
- 不允许 `Control Text Cover`、`Button Text Cover`、`Table / Clean` 或隐藏正式实例后展示手绘控件。
- 组件属性、Slot、字体加载、权限和实例关系失败均不得降级为“视觉通过”；必须报告失败码和节点位置。
- 不允许在最终 Scene 内出现未绑定组件库 Text Style 的页面级文字；不允许用手工字体参数替代组件库文本样式。

## 已知限制

> 按时间倒序,最新在最前。跑通后发现的限制统一放这里,不散落在正文各处。
> 仓库内回填方式见 `_docs/limit-backfill.md`(仅发布仓)。

### 2026-08-25 · 平台与主题切换
- 平台切换统一走 `platformKey`，当前支持 `zhikexing / yushu / zhineng-yunying / qifu-generic`；用户未指定平台时不再默认毓数。
- 主题切换统一走 `themeKey / themePrimary`，当前支持 `zhikexing-green / yushu-green / smartops-blue / custom`；主题只改语义颜色，不改结构。
- `zhineng-yunying` 是蓝色主题智能运营平台的预留平台壳；在专属导航与平台模板未补齐前，不得生成正式打开态，必须返回 `BACKGROUND_TEMPLATE_MISSING` 或使用用户明确指定并验收通过的 `EXISTING_LIST_PAGE`。
- 正式交付 Scene 内所有新增页面级文字必须绑定组件库 Text Style；执行前形成 `TextStyleResolutionManifest`，执行后扫描 Scene 内 `TEXT.textStyleId`，无样式即 FAIL。

### 2026-08-21 · 数据详情抽屉 Golden Sample
- 唯一 Golden Sample 为组件库文件 Page `02 From 训练过程` 的 `Golden Sample / Drawer / 数据详情 / 680 · 0821 根据手搓重生成`（node `4725:1548`）；未来同类抽屉先复用其 Scene、抽屉和表格结构，再替换业务数据。旧的 `4659:420` 仅作历史对照。
- Golden Sample Scene 固定 `1366×768`。原有 `底图 1` 是 IMAGE 填充矩形，不能作为交付底图；生成或重制时必须换成完整真实列表页。当前可验证底图源为 `Template / List Page / 智客星 / 1440 / 手动调整`（node `4892:34812`，实际 `1366×768`），且 Header、侧栏、Shell、Filter Bar、Table Shell 与 Pagination 必须保持真实组件实例。
- 两张样例中的页面级任务正文与 Form label 已统一绑定 `Body/Regular` 14/22；`Body/Medium` 会造成正文误加粗，后续生成与回归验收均判定为 FAIL。
- 组件库现有 `标题/Medium` 的真实定义是 16/24，没有独立 16/20 标题样式；必须使用现有样式并报告此差异，不允许手工覆盖行高。
- `Text-V2 / contentFont 内容字号=14px` 的组件母版正文已绑定 `Body/Regular` 14/22。Tag、Select、Header Cell、Pagination 等其余部分组件内部 Text 仍可能未绑定 Text Style；页面层不得 detach 或覆盖字体，只报告 `COMPONENT_SOURCE_GAP` 并把修复留给组件母版。页面级自由 Text 仍必须 100% 绑定组件库 Text Style。
- 手工样例中存在缩放遗留的小数尺寸，生成稿必须使用未缩放实例与整数几何消除。

### 2026-08-12 · 新建触发式任务抽屉
- 抽屉 Frame 内所有控件 INSTANCE 必须嵌套在 `Drawer/Header | Section/<name> | Drawer/Footer` 三容器之一,不允许 Page 根级孤儿(详见验证清单"层级归属检查")
- 抽屉 Frame 内不允许存在与已嵌实例位置/尺寸几乎一致的重复节点(详见验证清单"重复节点检查")
- 配套兜底工具:`Component Library/.figma-plugins/qifu-drawer-cleanup/`(在外部仓,可改写为"选中即清"版本)

### 2026-08-20 · qifu-figma-drawer-builder 合并
- `qifu-figma-drawer-builder` 的有效规则已合并进本 Skill，后续统一使用 `qifu-drawer-form`；旧 builder 只作为历史来源，不再作为运行入口。
- 合并范围包括截图证据解析、ComponentResolutionManifest、精确组件解析、属性写入回读、Slot 验证、单一语义控件、小控件残留扫描、P0 失败即停和双状态交付。
- 旧 builder 中与新版冲突的内容不继承：过时组合名、固定 1440 根画板、默认复制列表页双画板、以及对 `qifu-list-page` 的完整列表页规则。
- 后续如果发现抽屉生成偏差，优先补充 `references/figma-execution-validation.md` 和组件映射，不再新增第二个抽屉生成 Skill。

## 交付内容

完成后返回:

- 抽屉节点 ID 与名称;
- `presentationMode`、Scene 节点及底图来源节点（组合模式时）；
- `platformKey / platformName / themeKey / themePrimary` 与主题变量回读结果;
- 使用的 `compositionName`;
- 使用的主要组件及关键变体;
- Section 清单与字段总数;
- 对输入描述做出的假设;
- 组件缺口及建议补充项;
- 组件来源模式与预检结果;
- `TextStyleResolutionManifest` 摘要与整页 Text Style 扫描结果;
- `ComponentResolutionManifest` 摘要、属性回读结果、Slot 验证结果;
- `structuralValidation` 与 `visualValidation` 状态;
- 实例、变量、布局、滚动、原型和截图验证结果。
