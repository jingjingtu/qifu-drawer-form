# 智客星超频流控配置抽屉 Golden Sample

## 基线与范围

唯一视觉与结构基线位于组件库文件 `gTV3VdC6a5e9vpkRHIZSXA`，Page `测试 qifu-drawer-form skill`：

```text
Scene / Drawer / 超频流控配置 / Skill规则回归版
reference node: 4954:20064（手搓精修一版）
compositionName: Qifu Drawer Form / Sectioned Create
platformKey: zhikexing
themeKey: zhikexing-green
widthTier: 640
presentationMode: DRAWER_OPEN_WITH_BACKGROUND
```

本 Golden Sample 是智客星平台下“超频流控配置”抽屉的最高优先级基线。用户说“智客星 + 超频流控配置 / 超频规则 / 频控规则”时，必须优先套用本文件，不得套用 README 中的通用字段示例、智能运营平台策略关联样例，或自行扩展成“触达间隔 / 单日上限 / 状态说明”等另一套业务结构。

## 固定场景结构

```text
Scene / Drawer / 超频流控配置 / DRAWER_OPEN       1366 x 768
├── Background / 智客星列表页底图                 1366 x 768
├── Overlay Mask / 蒙层                           1366 x 768
└── Drawer / 右侧抽屉 / 超频流控配置              x=726, y=0, w=640, h=768
    ├── Drawer / Header                           h=56
    ├── Drawer / Body                             x=0, y=56, w=640, h=660
    └── Drawer / Footer                           x=0, y=716, w=640, h=52
```

- 顶层只能有一个 `1366 x 768` Scene；底图、蒙层、抽屉都必须在同一个 Scene 内，不能拆成两个画板。
- Drawer 必须贴右侧，宽度固定 640；不得因字段少改成 600，也不得套用智能运营策略关联抽屉的 680。
- Header 高度 56，标题为 `超频流控配置`，使用组件库 `标题/Medium`；关闭按钮使用真实 `Icon/basic/close`，位置在右上角，16 x 16。
- Body 内边距上下左右 24；本样例只有一个内容区 `Section / 基础信息`，不显示单独的 SectionTitle，字段直接从 Body 顶部开始。
- Footer 高度 52，右侧按钮为 `取消` + `确定`；取消为描边按钮，确定为主按钮。不得改成“取消 / 保存”，也不得套用智能运营的“关闭 / 保存”。

## 字段契约

字段顺序、字段名和控件类型固定如下：

| fieldKey | 字段 | 控件 | 必填 | 内容 |
| --- | --- | --- | --- | --- |
| ruleName | 规则名称 | Select | 是 | 占位 `请选择`，宽度跟随 controlSlot |
| audienceType | 超频人群 | Radio.Group | 是 | 选项 `人群包 / 客群`，默认选中 `人群包` |
| selectedAudience | 选择人群 | Tag | 否 | `26年企微活动 - 3K-2W新客250721 - 3K-2W新客250721 S102180`，文字左对齐 |
| validPeriod | 有效期 | DateRange | 是 | 占位 `开始日期 至 结束日期`，日历图标必须在组件内部右侧 |
| touchMethod | 触达方式 | Select | 是 | 占位 `请选择` |
| overFrequencyRule | 超频规则 | Custom(OverFrequencyRule) | 是 | 浅灰规则面板，包含策略类型和两行规则 |

禁止把 `规则名称` 改成 Input；禁止把 `选择人群` 改成 Search；禁止新增 `策略类型 / 触达间隔 / 单日上限 / 生效时间 / 优先级 / 状态 / 规则说明` 作为外层 FormItem。这些属于旧提示词偏差，不是本 Golden Sample。

## 表单布局

```text
Drawer / Body
└── Section / 基础信息                     x=24, y=24, w=592
    ├── FormItem / ruleName               y=0
    ├── FormItem / audienceType           y=48
    ├── FormItem / selectedAudience       y=96
    ├── FormItem / validPeriod            y=144
    ├── FormItem / touchMethod            y=192
    └── FormItem / overFrequencyRule      y=240
```

- FormItem 高度 32，字段垂直间距 16（相邻 FormItem 的 y 差为 48）。
- FormLabel 宽度 96，标签文字左对齐；必填星号在 label 文本左侧，星号与文本间距 4。
- Label 到 Control 的水平间距为 12；Control 宽度 484，右边缘距离 Drawer 右边框 24。
- 所有页面级文字必须绑定组件库 Text Style：标题用 `标题/Medium`，label、必填星号、规则区连接文字用 `Body/Regular`。
- 控件高度统一 32；Radio 实例可使用组件自身 28/32 的真实高度，但行盒仍按 32 对齐。

## 超频规则面板

超频规则必须使用 `Custom(OverFrequencyRule)`，它不是 Fallback。结构如下：

```text
Control / overFrequencyRule
└── Custom Rule Area / 超频规则             w=484, h=152, fill=#F5F7FA, radius=4
    ├── Rule Row / 策略类型                x=24, y=16, h=32
    │   ├── Rule Inner Label / 策略类型
    │   └── INSTANCE / Select / 策略类型
    ├── Rule Row / 01                      x=24, y=60, h=32
    │   ├── Rule Text 每
    │   ├── INSTANCE / Input / 天数
    │   ├── Rule Text 天，触达
    │   ├── INSTANCE / Input / 条数
    │   ├── Rule Text 条
    │   └── INSTANCE / Icon/basic/plus-square
    └── Rule Row / 02                      x=24, y=104, h=32
        ├── Rule Text 每
        ├── INSTANCE / Input / 天数
        ├── Rule Text 天，触达
        ├── INSTANCE / Input / 条数
        ├── Rule Text 条
        ├── INSTANCE / Icon/basic/plus-square
        └── INSTANCE / Icon/basic/Minus-Square
```

- 面板填充 `#F5F7FA`；上下内边距 16，左内边距 24，右侧按图标排布保持不贴边。
- 策略类型内联标签到 Select 的间距 8；规则行之间间距 12。
- 规则行内文字、Input、图标之间默认 8；Input 宽度 72，高度 32。
- 添加图标固定为 `Icon/basic/plus-square`；减少图标固定为 `Icon/basic/Minus-Square`。智客星本样例不得替换成智能运营的 `Icon/basic/icon_add`。

## 与智能运营平台的隔离规则

本 Golden Sample 只在 `platformKey=zhikexing` 时生效。即使主题色被改成蓝色，只要平台仍是智客星，也不得套用智能运营平台的结构规则。

以下规则只属于智能运营平台策略关联抽屉，不得进入本样例：

- 680px 抽屉宽度；
- Header Title 使用 `标题/Large`；
- `主模板 + 模板明细表`、`关联运营策略 + 策略明细表`；
- 多选 Select 内可关闭 Tag；
- Footer 使用 `关闭 / 保存`，且关闭为文字按钮。

## 完整提示词

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“超频流控配置”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。

使用“智客星超频流控配置抽屉 Golden Sample”。
页面平台：智客星。
platformKey：zhikexing
themeKey：zhikexing-green
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：640
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：TEMPLATE

只生成一个 1366×768 的完整打开态 Scene，内部层级为：
1. Background / 智客星列表页底图
2. Overlay Mask / 蒙层
3. Drawer / 右侧抽屉 / 超频流控配置

抽屉标题：超频流控配置
Footer：取消、确定。

字段按以下顺序生成，不要新增其他字段：
1. 规则名称：Select，必填，占位文字“请选择”。
2. 超频人群：Radio.Group，必填，选项“人群包、客群”，默认选中“人群包”。
3. 选择人群：Tag，展示“26年企微活动 - 3K-2W新客250721 - 3K-2W新客250721 S102180”，文字左对齐。
4. 有效期：DateRange，必填，占位文字“开始日期 至 结束日期”，日历图标在组件内部最右侧。
5. 触达方式：Select，必填，占位文字“请选择”。
6. 超频规则：Custom(OverFrequencyRule)，必填，浅灰底 #F5F7FA，面板内边距 top/bottom 16px、left 24px、right 不贴边；策略类型标签与 Select 间距 8px；规则行间距 12px。

超频规则内包含：
- 策略类型 Select，占位“请选择”。
- 第一行：每【Input】天，触达【Input】条，右侧 Icon/basic/plus-square。
- 第二行：每【Input】天，触达【Input】条，右侧 Icon/basic/plus-square 和 Icon/basic/Minus-Square。

验收：必须与“Scene / Drawer / 超频流控配置 / Skill规则回归版”保持一致；Drawer 宽度 640，Header 56，Footer 52，Body padding 24，标签左对齐，控件右边距 24，所有控件和图标使用组件库真实实例，所有页面级文字绑定组件库 Text Style。
```

## 验收

1. Scene 为 `1366 x 768`，只有一个顶层打开态画板；Background、Overlay Mask、Drawer 均在 Scene 内。
2. Drawer 为 640px，贴右侧；Header 56、Body 660、Footer 52。
3. 字段只能是本文件 6 项，且顺序、控件类型、文案、Footer 均一致。
4. `规则名称 / 触达方式 / 策略类型` 均为真实 Select；`有效期` 为真实 DateRange；`超频人群` 为真实 Radio；`选择人群` 为真实 Tag。
5. 超频规则面板灰底、内边距、间距、图标名称全部回读通过。
6. 不出现智能运营平台专属结构、旧提示词字段或 680px 抽屉宽度。
