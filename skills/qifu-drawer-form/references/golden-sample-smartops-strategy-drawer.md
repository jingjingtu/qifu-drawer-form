# 智能运营平台策略关联抽屉 Golden Sample

## 基线与范围

唯一抽屉基线位于组件库文件 `gTV3VdC6a5e9vpkRHIZSXA`，Page `02 From 训练过程`：

```text
Golden Sample / Drawer / 智能运营平台 / 新增短信模板策略 / 680 · 0825
node: 5058:9322
compositionName: Qifu Drawer Form / Sectioned Create
platformKey: zhineng-yunying
themeKey: smartops-blue
widthTier: 680
```

本 Golden Sample 是抽屉本体的结构和组件基线。默认打开态样例位于 `5066:9446`：它使用 `1366×768` 的中性结构预览底图 + Overlay Mask + 右侧 680px 抽屉，用来先验证抽屉打开态，且不借用智客星或毓数菜单。该预览不是智能运营平台正式列表页；用户提供已验收的智能运营平台 `EXISTING_LIST_PAGE` 后，才用真实底图替换预览背景。不得把图片背景当作平台模板。

## 固定结构

```text
Drawer / 新增短信模板策略
├── Header: 标题 + Close
├── Body
│   ├── 策略名称
│   ├── 有效期
│   ├── 主模板: Select + 模板明细表
│   ├── 关联运营策略: 多选 Select + 策略明细表
│   └── 灰度比例
└── Footer: 关闭 + 保存
```

- Header Title 使用 `标题/Large` 18/26；Close 是 `Icon/basic/close`，图形 Fill 绑定 `图标颜色/--qifu-icon-color-secondary`。
- “关联运营策略”是字段标签，绑定 `Body/Regular` 14/22；其余短字段标签沿用 `标题/Small`。
- 主模板和关联运营策略均为“选择器-明细组合模块”：Select 与明细表的垂直 gap=8px，模块高度随内容撑开。
- 关联运营策略使用真实多选 Select；已选项是 `Data Display / Tag / Tag`，`size=small 小尺寸`，关闭能力来自 Tag 自身。
- 明细表使用真实 Header Cell 与 Content Cell；表格外层无描边。只有 Table Header 使用 `INNER_SHADOW`：x=0、y=1、blur=2、spread=0、rgba(0,0,0,0.08)。
- Footer 的关闭按钮是 `Button / variant=text 文字`，保存按钮是 `Button / variant=base 基础`；两者均不加页面级描边。

## 字段契约

| fieldKey | 字段 | 控件 | 必填 | 内容 |
| --- | --- | --- | --- | --- |
| strategyName | 策略名称 | Input | 是 | 占位 `请输入` |
| validPeriod | 有效期 | DateRange | 是 | 占位 `开始时间 - 结束时间` |
| mainTemplate | 主模板 | Select + 明细表 | 是 | 选择短信模板后展示模板名称、模板内容、模板类型、创建人 |
| relatedStrategy | 关联运营策略 | Multiple Select + 明细表 | 是 | Tag 已选项；展示序号、运营策略名称、运营策略ID、创建人 |
| grayRatio | 灰度比例 | Select | 是 | 示例值 `100%` |

## 完整抽屉提示词

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“新增短信模板策略”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。
platformKey：zhineng-yunying
platformName：智能运营平台
themeKey：smartops-blue
themePrimary：#1677FF
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：680

使用“智能运营平台策略关联抽屉 Golden Sample”。
标题使用标题/Large 18/26；关闭图标使用 qifu-icon-color-secondary。

字段依次为：
1. 策略名称，必填，Input，占位“请输入”。
2. 有效期，必填，DateRange，占位“开始时间 - 结束时间”。
3. 主模板，必填，Select，占位“请选择短信模板”；选择器下方展示模板明细表，列为模板名称、模板内容、模板类型、创建人。
4. 关联运营策略，必填，Multiple Select；已选项使用 Tag / small，并支持 Tag 自带关闭；选择器下方展示运营策略明细表，列为序号、运营策略名称、运营策略ID、创建人。
5. 灰度比例，必填，Select，默认值“100%”。

主模板与关联运营策略均为选择器-明细组合模块：内部间距 8px，高度随表格内容自适应。
表格外层不要描边，只给 Table Header 添加 INNER_SHADOW：x=0、y=1、blur=2、spread=0、黑色 8%。
底部按钮为关闭、保存：关闭使用文字按钮，保存使用主按钮，两个按钮均不描边。
```

## 完整页面生成示例提示词

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点>，根据“智能运营平台策略关联抽屉 Golden Sample”生成一个完整打开态页面。
不要新建 Figma Page；只在上述目标画布内生成。

平台：智能运营平台。
platformKey：zhineng-yunying。
themeKey：smartops-blue。
componentMode：REAL_COMPONENT_ONLY。
展示方式：完整页面打开态。
底图：background.source=AUTO。没有已验收智能运营平台列表页时，自动生成 STRUCTURE_PREVIEW + Overlay Mask；有列表页时，改为 background.source=EXISTING_LIST_PAGE；background.sourceNode=<已验收的智能运营平台列表页节点ID>。

在底图右侧打开“新增短信模板策略”抽屉，抽屉内容、组件、样式、表格、Tag、表头内阴影和 Footer 均严格复用“智能运营平台策略关联抽屉 Golden Sample”。
不要复制智客星或毓数菜单；不要使用截图或图片作为正式底图；抽屉外不新增解释性文字或审计卡片。
```

## 验收

1. 抽屉为 680px，Header/Body/Footer 完整且 Footer 固定在底部。
2. 所有 Input、DateRange、Select、Tag、Close、Button、Header Cell 和 Content Cell 均为真实 INSTANCE。
3. Header Title、关联运营策略标签、Tag 尺寸、关闭图标颜色、两组 8px 组合间距和 Footer 变体均回读通过。
4. 两张明细表无外层描边，仅 Table Header 有单层内阴影。
5. 默认打开态必须有 `1366×768` Scene、结构预览底图和 Overlay Mask；提供真实智能运营平台列表页后，才标记为正式平台页面验收通过。
