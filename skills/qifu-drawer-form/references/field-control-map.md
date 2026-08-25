# 字段类型 → 控件映射

## 目的

决定每个 `fields[]` 在抽屉里使用哪种真实控件。优先命中本表,本表没有时使用 `Custom` Slot 并记录缺口。

所有真实组件的 `节点 ID / 发布 Key / 属性`,请直接查询[组件映射](component-map.md);本表只做"语义 → 控件"的路由,不重复维护组件清单。

## 通用映射

| 字段语义 | 控件 | 关键属性 | 默认 widthTier |
| --- | --- | --- | --- |
| 单行文本(name、title、id、code) | `录入组件 / Input / Base-V2` | `size=M 32px`、`content=Placeholder/Value` | 320 |
| 长文本 / 描述 / 备注 | `录入组件 / Textarea` | `rows=4`、`maxLength` 按业务 | FULL |
| 数字 / 金额 / 百分比 | `录入组件 / InputNumber` | `size=M`、precision、`min/max` | 200 |
| 单选枚举(≤ 4 项、文案短) | `录入组件 / Radio.Group` | `direction=horizontal`、`optionType=default` | FULL |
| 单选枚举(> 4 项 / 文案长) | `录入组件 / Select / Base` | `size=LG 32px`、`mode=single` | 320 |
| 多选枚举 | `录入组件 / Select / Base` | `mode=multiple` | 320 |
| 布尔开关 | `录入组件 / Switch` | `checked`、`disabled` | — |
| 单个布尔勾选(同意、包含) | `录入组件 / Checkbox` | `label`、`checked` | — |
| 日期(单日) | `录入组件 / DatePicker / Input / Date` | `placeholder`、`size=M` | 200 |
| 日期范围 | `录入组件 / DatePicker / Input / DateRange` | `placeholder`、`size=M` | 320 |
| 级联层级(组织、地区) | `录入组件 / Cascader / Base` | `path`、`size=M` | 320 |
| 模糊搜索(人员、客户、群组) | `录入组件 / Search / Base` 或 `Select` 带 `search` | `trigger=Icon`、`size=M` | 320 |
| 上传 | `录入组件 / Upload` | 限制文案、缩略预览 | FULL |
| 富文本 | 不默认提供,记录缺口 | — | — |

## 抽屉特有场景

### 必填红星

必填 = `FormItem.required=true`。红星由 FormItem 渲染在 label 左侧,颜色 `#dc2626`,**不允许手画**。

### 单选 vs 下拉 的判定

```
选项数 ≤ 4 且文案 ≤ 4 字 → Radio.Group
否则                       → Select
需要同时展示选项说明       → Radio.Group + Card 式选项(记录缺口:卡片式选项)
```

### 快捷时间范围

抽屉内**不提供**"今天 / 本周 / 本月"的快捷项——这是列表页 FilterBar 的能力;抽屉中用户应主动选择日期。

### 日期范围 DateRange

`DateRange` 必须使用真实 `录入组件 / DatePicker / Input / DateRange` 实例。实例拉宽到 304 / 408 / FULL 等宽度时，日历图标仍必须作为组件内部后缀图标靠右展示，右侧间距跟随组件 padding（通常 12px）。

- 不允许在 DateRange 实例外额外叠加日历图标、文本或边框。
- 若图标因为实例拉宽后仍停留在占位文字后方，优先设置该 DateRange 实例外层 Auto Layout 为 `primaryAxisAlignItems=SPACE_BETWEEN`，保持 `paddingLeft=12 / paddingRight=12`，让 Text 与 Suffix 两端分布。
- 如果组件不允许该实例级布局覆盖，记录 `COMPONENT_SOURCE_GAP: DateRange suffix alignment`，不要 detach 或手动移动实例内部 `Suffix / Calendar Icon`。

### 超频规则 Custom(OverFrequencyRule)

当字段语义为“超频规则 / 频控规则 / 触达频次规则”时，`DrawerSpec.fields[].control` 写 `Custom(OverFrequencyRule)`，但该业务区不是缺失组件 Fallback；它是由真实 Input / Select / Icon 组件组成的页面级规则面板，节点命名 `Custom Rule Area / 超频规则`。

推荐中文术语：

- “规则区内联标签”：面板内部和下拉框同行的短标签，如 `策略类型`。
- “Select 下拉选择器”：规则区内的策略类型选择控件。
- “规则面板内边距”：浅灰规则区内容到面板边框的距离。
- “内部元素间距”：策略类型行、规则行之间的垂直距离，或同一规则行内文字/输入框/图标之间的水平距离。

布局固定规则：

| 项 | 数值 | 说明 |
| --- | ---: | --- |
| 面板填充 | `#F5F7FA` | 用于区分主次关系；可绑定等价背景变量 |
| 面板圆角 | 4px | 与普通内容区一致 |
| 面板宽度 | 跟随 controlSlot，默认 FULL | 右边缘与其他控件右边缘对齐 |
| 面板高度 | 内容自适应，示例 152px | 不用 144px 压缩三行规则 |
| 内边距 | top/bottom 16px，left 24px | right 按视觉和控件排布补齐，默认 24px |
| 规则行高度 | 32px | 与抽屉控件高度一致 |
| 规则行间距 | 12px | 策略类型行、第一行规则、第二行规则之间一致 |
| 规则区内联标签 → Select | 8px | 例如 `策略类型` 文本右边到 Select 左边 |
| 规则行内元素间距 | 8px | “每 / Input / 天，触达 / Input / 条 / 图标”之间 |
| 添加图标 | `Icon/basic/plus-square` | 真实图标实例，24×24 容器，图形 16×16 |
| 减少图标 | `Icon/basic/Minus-Square` | 真实图标实例，24×24 容器，图形 16×16 |

标准结构：

```text
FormItem / overFrequencyRule
├── FormLabel / left aligned
└── Control / overFrequencyRule
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

`Rule Text` 与 `Rule Inner Label` 是页面级文字，必须绑定组件库 `Body/Regular` Text Style；Input / Select / 添加 / 减少必须保持真实组件实例，不允许用矩形、裸文本或手绘图标代替。

### 添加地图、圈选、上传文件类复合控件

一律使用 `Custom` Slot 占位,在 `DrawerSpec.fields[].control` 写 `Custom(<BizSlotName>)`,并把占位区命名为 `Fallback / <BizSlotName>`,同步到 `Audit / Missing Components`。

## 字段宽度阶梯(widthTier)

| widthTier | 宽度 | 用法 |
| --- | ---: | --- |
| 200 | 200px | 短枚举、数字、百分比、年份、月份 |
| 304 | 304px | 普通文本、单选 Select(默认档) |
| 408 | 408px | 长文本、URL、Webhook、复杂 Select |
| FULL | 剩余 | Textarea、Upload、RichText、跨列字段 |

- **默认值**:文本字段用 304,日期用 200 或 304,描述用 FULL。
- **禁止**写入阶梯外的任意数值;并列两个窄字段时,宽度仍为各自阶梯,不允许合并到 408。

## 高度规格

抽屉内**全部控件高度统一为 32px**,对应:

- Input V2 → `size=M 默认尺寸`(原生 32px)
- Select → `size=LG 大尺寸`
- Button → `size=large 大尺寸`
- DatePicker → `size=M`
- Radio.Group / Checkbox → 行高 32px

**铁律**:同一抽屉内不允许混用 28px 和 32px 两种高度;在 840px `Wide` 抽屉中也不调到 36px——保持 32px 统一。

明确要求"紧凑模式"时,改用 28px 全联动:`Input size=S`、`Select size=MD`、`Button size=small`。
