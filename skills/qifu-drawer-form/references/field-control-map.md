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
