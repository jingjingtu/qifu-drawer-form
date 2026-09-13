---
name: qifu-drawer-form
description: >-
  用于根据业务描述、字段清单、截图或线框，在 Figma 中以奇富组件库真实实例创建、更新或审查单平台或多平台对比的右侧抽屉。支持新建、编辑、只读和数据详情场景，并验证平台、主题、实例关系、结构与视觉结果。不用于向导、批量编辑列表、复杂看板或高度定制工作台。
---

# Qifu Drawer Form

把业务需求转换为可编辑、可回读、保持组件实例关系的右侧抽屉。参考图只提供信息架构和视觉证据，不作为最终控件或背景图片。

## 读取路由

每次先完整读取：

- [共享页面上下文](../qifu-shared/references/page-context.md)：平台、目标位置、状态、权限与默认值。
- [共享组件调用基线](../qifu-shared/references/component-invocation-baseline.md)：组件解析、写入回读与失败分类。
- [组件映射](../qifu-shared/references/component-map.md)：真实组件名称、节点 ID、发布 Key 与已知缺口。
- [抽屉组合注册表](references/drawer-compositions.md)：六个稳定组合及其选择规则。

按当前任务继续读取，未命中的资料不加载：

- 普通 Create / Edit / Readonly：读取[页面蓝图](references/page-blueprint.md)和[字段控件映射](references/field-control-map.md)。
- 解析平台或主题：读取[平台与主题切换协议](references/platform-theme-switching.md)，以及当前平台的唯一 Adapter。
- 用户要求同一抽屉复用到多个平台、生成对比稿，或一次列出两个及以上平台：读取[多平台批量生成协议](references/multi-platform-batch.md)、[平台注册表](../qifu-shared/references/platform-registry.json)和[主题注册表](../qifu-shared/theme/theme-registry.json)，用 `scripts/resolve_platform.py` 解析精确信号，再按目标加载各平台 Adapter。
- 开始写入与最终验收：读取[Figma 执行与结构化验收](references/figma-execution-validation.md)。
- 数据详情、智能运营策略关联、智客星超频流控：分别读取对应的[数据详情 Golden Sample](references/golden-sample-data-detail-drawer.md)、[智能运营 Golden Sample](references/golden-sample-smartops-strategy-drawer.md)、[智客星超频 Golden Sample](references/golden-sample-zhikexing-overfrequency-drawer.md)。
- 正式完整打开态：读取[打开态底图协议](references/zhikexing-list-background.md)。
- 用户明确指定 `PORTABLE_KIT`：读取[Portable Kit 模式](references/portable-kit.md)和[Portable 组件清单](references/portable-component-manifest.json)。
- 仅在诊断历史回归或维护本 Skill 时读取[已知限制与迁移记录](references/known-limitations.md)。

任何 `use_figma` 调用前加载并遵循 `figma-use`；创建或更新完整抽屉时同时加载 `figma-generate-design`。目标项目存在 `AGENTS.md` 或项目级规则时先遵循项目规则。

## 输入与默认值

先形成共享 `PageContext`，再形成 `DrawerSpec`。用户不需要填写完整表格；从自然语言提取并合理补全：

```text
generationMode=SINGLE|MULTI_PLATFORM_COMPARE
drawerTitle / operation=create|edit|readonly|view
componentMode=REAL_COMPONENT_ONLY|PORTABLE_KIT|VISUAL_FALLBACK
compositionName
platformKey / platformName / themeKey / themePrimary
presentationMode=DRAWER_OPEN_WITH_BACKGROUND|STANDALONE_DEBUG
background.source=AUTO|TEMPLATE|EXISTING_LIST_PAGE|STRUCTURE_PREVIEW
background.sourceNode / background.sidePath[] / background.pageName
widthTier=480|640|680|840|960
sections[].sectionTitle
sections[].fields[]:
  fieldKey, label, required, control, placeholder, options,
  defaultValue, helpText, widthTier=200|304|408|FULL, disabledCond
footer: okText, cancelText, showCancel, danger, extras[]
embeddedTable: columns[], rows[], tableSize, tableType, selection, pagination
targetFileUrl / targetPage / targetAnchor / targetPlacement

MULTI_PLATFORM_COMPARE additionally:
baseDrawer=<normalized shared DrawerSpec>
targets[].platformKey / platformName / themeKey / themePrimary
targets[].background / navigation
comparisonLayout=HORIZONTAL|GRID
failurePolicy=ALL_OR_NOTHING|CONTINUE_WITH_REPORT
```

统一默认：

- 未指定平台且目标文件无可靠上下文：`platformKey=qifu-generic`，不套用毓数或智客星菜单。
- 未指定组件模式：`REAL_COMPONENT_ONLY`。
- 未指定组合：按注册表推断，仍无法区分时使用 `Qifu Drawer Form / Sectioned Create`。
- 用户明确要求多平台复用、对比稿，或一次给出两个及以上已注册平台时：`generationMode=MULTI_PLATFORM_COMPARE`；否则为 `SINGLE`。
- 普通表单宽度 640；数据详情固定 680；智能运营策略关联 Golden Sample 固定 680；智客星超频 Golden Sample 固定 640。
- 普通字段宽度默认 304，只允许 `200 / 304 / 408 / FULL`。
- 正式交付默认 `DRAWER_OPEN_WITH_BACKGROUND + background.source=AUTO`，不交付裸抽屉。
- 缺少目标 Page 或落点且无法从链接唯一解析时先询问，不写入第一个 Page，也不新建近义 Page。

`target*` 字段决定写入位置；`platformKey` 决定业务壳和 Adapter；`themeKey` 只决定允许的语义颜色。三者不得互相代替。

## 组件模式

- `REAL_COMPONENT_ONLY`：使用正式 Library。任一必需组件、样式、属性或 Slot 无法解析时停止，不自动切换模式。
- `PORTABLE_KIT`：只使用目标文件内、清单可精确匹配的本地组件；创建后验证 `INSTANCE.mainComponent`。
- `VISUAL_FALLBACK`：仅当用户明确选择时允许。降级节点命名为 `Fallback / <Capability>`，并生成对应 Audit；不得冒充正式实例。

所有页面级新增 Text 必须绑定组件库 Text Style。组件内部文字由母版管理；母版未绑定样式时报告 `COMPONENT_SOURCE_GAP`，不 detach 或在实例层覆盖字体。

## 工作流

### 1. 解析规格

1. 先解析目标文件、Page、落点和平台，再解析操作类型、对象、组合、Section、字段与 Footer。
2. 参考图内容按 `user-description | screenshot | inferred` 记录证据；用户文字优先于截图。
3. 影响组件选择、层级或写入位置的推断必须列入交付假设。
4. 多平台模式只解析一次公共 `baseDrawer`，冻结内容指纹后为每个平台派生计划；平台目标不得改写公共字段结构。

### 2. 预检

1. 确认目标文件可编辑，组件 Library、变量、字体和 Text Style 可用。
2. 为必需组件建立 `ComponentResolutionManifest`；所有必需项为 `resolved` 后才写页面。
3. 为页面级文字建立 `TextStyleResolutionManifest`；必需样式缺失时返回 `STYLE_MISSING`。
4. 主题变量、背景来源和 Golden Sample 在写入前确认。预检失败不留下半成品。
5. 多平台模式默认先预检全部目标；任一目标失败时按 `ALL_OR_NOTHING` 停止，不反复尝试同类替代方案。只有用户明确选择 `CONTINUE_WITH_REPORT` 才生成已通过目标并返回 `PARTIAL`。

### 3. 创建完整打开态

正式交付创建唯一 `1366×768` Scene，层级固定为：

```text
Scene / Drawer / <pageName> / <drawerTitle>
├── Background
├── Overlay Mask
└── Drawer
    ├── Drawer / Header
    ├── Drawer / Body
    │   └── Section / <name> × N
    └── Drawer / Footer
```

- `EXISTING_LIST_PAGE` 和 `TEMPLATE` 必须保留完整可编辑页面与真实实例。
- `STRUCTURE_PREVIEW` 只表达中性结构边界，不伪造平台菜单、业务数据或交互控件。
- `STANDALONE_DEBUG` 只用于内部调试，不作为正式交付。

### 4. 组装抽屉

1. 按组合注册表和页面蓝图创建 Header、Body、Section、字段和 Footer。
2. 每个语义控件只保留一个根实例；不保留覆盖文字、替代图标、旧控件或重叠副本。
3. 属性、变体、INSTANCE_SWAP 和 Slot 均执行“读取真实 Key → 校验类型和值域 → 写入 → 回读”。
4. 颜色优先绑定语义变量，文本绑定 Text Style；原始十六进制和字号仅作为 Golden Sample 核对值。
5. Edit 回填默认值；Readonly 禁用字段且只保留关闭动作；同一画板只交付一种状态。

### 5. 专项组合

- `Data Detail with Table`：严格使用对应 Golden Sample 的 680px、内容卡片、真实 Table Shell 和独立 Pagination 结构。
- 智能运营策略关联：只在路由条件命中时应用专用标题、Select → 明细表、Tag 与 Footer 规则。
- 智客星超频流控：固定六个字段、640px、超频规则面板和 `取消 / 确定`；不得混入其他平台案例字段。
- 其他复合业务能力使用 `Custom(<BizSlot>)`；只有组件库确实缺少该能力时才能进入已授权的 Fallback。

### 6. 多平台对比

按多平台批量协议在同一目标 Page 创建 `Comparison / Drawer / <drawerTitle>`。每个平台保留独立 `1366×768` 完整打开态，结构、字段、控件、宽度和 Footer 使用相同 `contentFingerprint`；只允许 Adapter、背景、导航、平台词和主题变量不同。智能运营平台缺少正式背景时明确标记 `PREVIEW_ONLY`，不得冒充正式平台还原。

## 失败关闭

以下情况属于执行失败，不是组件缺口：属性 Key 不存在、属性回读不一致、INSTANCE_SWAP/Slot 写入失败、字体或样式缺失、权限不足、目标不可编辑。

失败时：

1. 停止依赖该结果的后续写入；
2. 记录组件名、节点、候选 Key、期望值、实际值和错误码；
3. 返回 `FAIL` 或 `BLOCKED`，不使用“完成”“已生成”；
4. 不用截图、裸 Text、矩形、覆盖层、替代图标或分离实例掩盖失败。

只有 `COMPONENT_MISSING` 可以进入 Fallback 判断；`REAL_COMPONENT_ONLY` 和 `PORTABLE_KIT` 都不得自动视觉降级。

## 验证与交付

按执行与结构化验收文件完成预检、实例回读、结构计数、父子关系、变量、整数几何、分区截图和整页截图。至少确认：

- `structuralValidation` 与 `visualValidation` 分别为 `PASS`；
- Scene、Background、Mask、Drawer 层级唯一且尺寸正确；
- 所有控件属于 Header、Section 或 Footer，不存在 Page 根级孤儿；
- 不存在重复节点、实例外同文案覆盖或替代图标；
- 组合名、宽度档、字段顺序、状态和 Footer 与 DrawerSpec 一致；
- 页面级 Text 100% 使用解析成功的组件库 Text Style；
- 无未声明的截断、重叠、溢出和异常空白；
- Golden Sample 专项检查全部通过；
- Scene 内所有 Select / Cascader 后缀均通过统一契约：`Down-small`、16px、0°、规格对应右边距，以及 `图标颜色/--qifu-icon-color-tertiary` 变量绑定；
- 缺口、Fallback 和假设均可追踪。
- 多平台模式额外确认所有目标内容指纹一致，并返回每个平台的识别证据、壳状态与 `crossPlatformConsistency`。

单平台只有结构和视觉都为 `PASS` 才能宣称完成。多平台只有全部目标双重验证通过、内容指纹一致且壳状态符合用户要求时，才能返回 `batchValidation=PASS`。返回节点 ID、平台与主题回读、组合名、背景来源、字段与 Section 摘要、组件与 Text Style 解析摘要、属性/Slot 回读、缺口、假设和验证结果。

## 硬性约束

- 不修改或发布组件库母版，不分离实例，不把参考图作为正式内容。
- 不把平台、主题和写入位置混为一谈。
- 不创建 `DrawerShell` 母版；Drawer 是页面级组合。
- 不静默切换组件模式或跨平台借用菜单、模板和业务字段。
- 不用主题色、Logo 相似度或截图观感猜测平台；多平台目标必须由注册表中的确定性信号解析。
- 不把向导、复杂看板或批量编辑列表硬塞进本 Skill。
- 页面生成授权不包含修改本仓库或同步到其他目录；发现规则缺口时先报告。
