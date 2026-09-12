# 多平台抽屉批量生成协议

当用户要求“同一个抽屉复用到多个平台”“生成多平台对比稿”或一次列出两个及以上平台时启用。普通单平台生成不读取本文件。

## 输入契约

先解析一次公共业务结构，再解析平台目标：

```yaml
generationMode: MULTI_PLATFORM_COMPARE
baseDrawer:
  drawerTitle: 新增策略
  operation: create
  compositionName: Qifu Drawer Form / Sectioned Create
  widthTier: 640
  sections: []
  footer: {}
targets:
  - platformKey: zhikexing
    themeKey: zhikexing-green
    background:
      source: AUTO
  - platformKey: yushu
    themeKey: yushu-green
    background:
      source: AUTO
  - platformKey: zhineng-yunying
    themeKey: smartops-blue
    background:
      source: AUTO
comparisonLayout: HORIZONTAL | GRID
failurePolicy: ALL_OR_NOTHING | CONTINUE_WITH_REPORT
targetFileUrl: <figma-url>
targetPage: <existing-page>
targetAnchor: <optional-node>
targetPlacement: <blank-area-or-explicit-position>
```

默认 `comparisonLayout=HORIZONTAL`、`failurePolicy=ALL_OR_NOTHING`。平台数量超过三个时使用 `GRID`。不创建新的 Figma Page；所有版本放入用户指定的同一个 Page。

`targets[]` 至少包含两个不同的已注册平台。每个目标可以覆盖 `themeKey`、背景来源、导航路径和平台文案，但不得覆盖字段结构、控件类型、组合、宽度或 Footer。确需业务差异时拆成另一组 `baseDrawer`，不要把结构差异伪装成平台适配。

## 平台识别

读取 `../../qifu-shared/references/platform-registry.json` 和 `../../qifu-shared/theme/theme-registry.json`，按以下优先级解析每个目标：

1. 用户显式提供的 `platformKey`。
2. 用户明确写出的平台注册名称或唯一别名。
3. 用户指定的已验收背景节点中，平台注册表记录的精确模板节点 ID 或完整节点名称。
4. 目标文件中唯一命中的 Figma Variable mode 或平台壳组件名称。

同一级信号命中多个平台、只有颜色相似或只有截图视觉相似时，不自动猜测。返回候选平台和证据，请用户确认。未识别平台只有在用户明确接受通用版本时才使用 `qifu-generic`。

获得目标文件的精确信号后，可调用确定性解析器并保留其 JSON 结果作为 `detectedBy` 证据：

```bash
python3 scripts/resolve_platform.py --name "智能运营平台"
python3 scripts/resolve_platform.py --template-node-id "4892:34812"
python3 scripts/resolve_platform.py --figma-variable-mode "毓数/Light"
```

解析器返回 `UNRESOLVED`、`AMBIGUOUS` 或 `CONFLICT` 时停止该目标的预检，不自行改用 generic。

平台确定后，加载注册表中唯一的 Adapter；主题未指定时使用该平台的 `defaultTheme`。显式主题与平台注册默认不一致时允许切换主题，但平台壳、菜单和业务词仍由 `platformKey` 决定。

## 冻结公共结构

创建任何节点前，将 `baseDrawer` 归一化并冻结为 `BaseDrawerManifest`：

```text
drawerTitle
operation
compositionName
widthTier
sections[].sectionTitle
sections[].fields[].fieldKey
sections[].fields[].label
sections[].fields[].control
sections[].fields[].required
sections[].fields[].options
sections[].fields[].defaultValue
footer
embeddedTable
```

将上述字段序列化为 UTF-8 JSON：对象键按字典序排列、数组保持业务顺序、使用紧凑分隔符，然后计算 SHA-256，格式为 `sha256:<64位小写十六进制>`，作为 `contentFingerprint`。该指纹只比较公共业务结构，不包含 `platformKey`、`themeKey`、背景节点、导航、坐标或平台展示名。

每个目标生成一个 `PlatformDrawerPlan`，只追加：

```text
platformKey / platformName
adapter / generationStrategy / shellReadiness
themeKey / themePrimary / variable bindings
background.source / sourceNode / sidePath
target coordinates
```

所有 `PlatformDrawerPlan.contentFingerprint` 必须与 `BaseDrawerManifest` 相同，否则预检失败。

## 批量预检与失败策略

先完成全部平台预检，再开始写入：

- 注册表、Adapter 和主题必须可解析。
- 每个平台的组件、Text Style、变量和背景来源分别建立解析清单。
- `ALL_OR_NOTHING` 下任一平台预检失败，整个批次不写入，返回每个平台状态。
- 只有用户明确选择 `CONTINUE_WITH_REPORT` 时，才生成已通过平台；失败平台不得用通用背景或近似主题顶替，批次状态返回 `PARTIAL`。
- 同一失败原因最多按确定性替代路径重试一次；再次失败立即返回 `BLOCKED` 或 `FAIL`，不循环尝试同类方案。

## Figma 画布结构

创建一个比较组，内部每个平台版本仍是独立完整打开态：

```text
Comparison / Drawer / <drawerTitle>
├── Platform / zhikexing / <drawerTitle>
│   └── Scene / Drawer / <pageName> / <drawerTitle>
├── Platform / yushu / <drawerTitle>
│   └── Scene / Drawer / <pageName> / <drawerTitle>
└── Platform / zhineng-yunying / <drawerTitle>
    └── Scene / Drawer / <pageName> / <drawerTitle>
```

- 每个 Scene 固定 `1366×768`，内部仍为 `Background < Overlay Mask < Drawer`。
- `HORIZONTAL` 从左到右按 `targets[]` 排列，Scene 间距 80px。
- `GRID` 每行最多两个 Scene，横纵间距均为 80px。
- 平台名称放在 Scene 外的比较标签中；不得在正式平台 Scene 内增加说明性裸文字。
- 智能运营平台使用 `STRUCTURE_PREVIEW` 时，外部标签增加 `PREVIEW_ONLY`，不能标为正式平台还原。

## 一致性验收

逐个平台完成原有结构与视觉验收，再执行跨平台比较：

| 检查项 | 必须一致 | 允许不同 |
| --- | --- | --- |
| 内容 | 字段数量、顺序、label、控件、必填、默认值、Footer | 平台特有词仅在用户明确提供映射时不同 |
| 结构 | composition、widthTier、Section、字段父子关系 | Scene 坐标、背景内部平台壳 |
| 组件 | 同语义控件能力、真实实例关系 | 平台 Adapter 指定的壳组件或模板来源 |
| 主题 | Token 语义角色 | 变量模式、主色、链接色、选中态和强调色 |
| 状态 | operation、data state | 平台背景成熟度 `FORMAL` 或 `PREVIEW_ONLY` |

交付摘要必须返回：

```text
batchValidation=PASS | PARTIAL | BLOCKED | FAIL
contentFingerprint=<stable-value>
targets:
  - platformKey
    detectedBy
    adapter
    themeKey
    backgroundSource
    shellStatus=FORMAL|PREVIEW_ONLY
    structuralValidation
    visualValidation
crossPlatformConsistency=PASS|FAIL
```

只有全部目标双重验证通过、内容指纹一致且平台壳状态符合用户要求时，才能返回 `batchValidation=PASS`。

## 推荐提示词

```text
使用 qifu-drawer-form，并调用 @figma 插件，把同一个“新增策略”抽屉生成到智客星、毓数和智能运营平台，放在指定 Page 的同一个多平台对比组中。

公共结构：Sectioned Create，宽度 640。
基础信息：策略名称 Input 必填；有效期 DateRange 必填。
策略配置：策略类型 Select 必填；备注 Textarea 选填。
Footer：取消、确定。

平台主题自动采用平台注册默认值；优先使用各平台已验收背景。没有正式智能运营平台背景时允许 STRUCTURE_PREVIEW，并明确标记 PREVIEW_ONLY。
comparisonLayout：HORIZONTAL。
failurePolicy：ALL_OR_NOTHING。
不要改变不同平台之间的字段、控件、顺序、宽度和 Footer。完成后返回 contentFingerprint、每个平台解析证据和跨平台一致性验证。
```
