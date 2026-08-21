# 标准抽屉表单页蓝图

> `Qifu Drawer Form / Data Detail with Table` 是本蓝图的专用例外：完整结构、680px 宽度、16px Body 安全边距、20/24 内容卡片、文本样式和表格外框规则以 [数据详情抽屉 Golden Sample](golden-sample-data-detail-drawer.md) 为准。不要把下文普通 Create/Edit 表单的 640px、24px Body padding 或 Footer 规则覆盖到该组合。

## 目录

- [参考图的可复用信息](#1-参考图的可复用信息)
- [抽屉与主体结构](#2-抽屉与主体结构)
- [宽度阶梯](#3-宽度阶梯)
- [Header 与 Footer](#4-header-与-footer)
- [Form Section 分区](#5-form-section-分区)
- [字段规则](#6-字段规则)
- [布局与间距铁律](#7-布局与间距铁律)
- [状态与校验](#8-状态与校验)
- [响应与约束](#9-响应与约束)
- [推荐节点命名](#10-推荐节点命名)

## 1. 参考图的可复用信息

参考图(新建触发式任务)是一个典型 B 端业务的"多分区新建抽屉"。其稳定结构为:

1. 右侧滑入、覆盖主内容、背景加遮罩;
2. Header:抽屉标题 + 关闭按钮;
3. Body:1..N 个 Form Section,每个 Section 有标题与字段集合;
4. Footer:固定的底部操作条,主操作唯一。

参考图中的业务名(触发式任务、所属项目、人群圈选、任务规则)只用于理解场景,不得成为默认输出。

## 2. 抽屉与主体结构

```text
Drawer (position=right, width=widthTier, mask=true, maskClosable=false)
├── DrawerHeader (Horizontal, padding 16/24, border-bottom)
│   ├── Title (17px / 600)
│   └── CloseBtn (× icon, 24×24)
├── DrawerBody (Vertical, fill, scrollable, padding 24, gap 24)
│   └── FormSection × N
│       ├── SectionTitle (16px / 600, padding-bottom 12, border-bottom 1px)
│       └── FormItem × M (Horizontal, label + control)
└── DrawerFooter (Horizontal, padding 12/16, border-top, right-aligned, gap 12)
    ├── Button (variant=base)   取消
    └── Button (variant=primary) 确定 | 保存 | 关闭
```

**铁律**:

- 抽屉只从右侧滑出;左侧、中央模态场景不属于本 Skill。
- Footer 永远 pinned 在底部,不随 Body 滚动。
- Body 内容超过抽屉高度时,Body 内部 `overflow-y=auto`,Header / Footer 保持可见。
- `maskClosable` 默认 `false`——防止误关闭丢失未保存内容;需要改动必须在 DrawerSpec 显式声明。
- `escClosable` 默认 `false`,同 maskClosable 规则。

## 3. 宽度阶梯

抽屉宽度只允许从 3 档选择,不任意取值:

| 档位 | 宽度 | 适用场景 | 典型 columnMode |
| --- | ---: | --- | --- |
| Narrow | 480px | 字段少、控件短、无说明文案 | single |
| Standard | 640px | 默认;普通新建/编辑抽屉 | single(可 double 列于宽字段) |
| Data Detail | 680px | 摘要 + 筛选 + 内嵌表格的详情抽屉 | single + table |
| Wide | 840px | 含双列布局、复杂表格/树、说明文案多 | double |

普通表单默认使用 **Standard 640px**；`Data Detail with Table` 固定使用 **Data Detail 680px**；字段超过 12 个或显式要求分双列时使用 Wide。Narrow 只用于 4–6 个纯文字字段的极简单场景。

## 4. Header 与 Footer

### Header

- 高度固定 56px,padding `0 24px`,背景 #fff,bottom border `#e5e7eb`。
- Title 17px / 600 / `#111827`,文案使用动宾结构(`新建 X` / `编辑 X` / `查看 X`);不写"X Form"、"详细设置"这类弱标题。
- 右侧关闭按钮 24×24,仅 icon `×`。
- Header 内**禁止**放面包屑、tabs、secondary actions——抽屉是单一任务容器。

### Footer

- 高度固定 52px,padding `12 24px`,top border `#e5e7eb`,背景 `#fff`。
- 按钮从右到左排列,顺序固定:`[主操作] [取消] [其他次要]`。
- 主操作唯一。同一 Footer 内**只允许一个 Primary Button**。
- 标准 Footer 按钮组合:
  - Create 类:`[确定] [取消]`
  - Edit 类:`[保存] [取消]`
  - Readonly 类:`[关闭]`
  - Advanced 类:`[提交] [上一步] [下一步] [取消]`(仅在 Steps 场景)
- 危险动作(删除、停用)放在 Footer **最左侧**,使用 `danger` 语义,与右侧主操作分开;不放进主操作组。

## 5. Form Section 分区

每个 Section 由 `title + 1..M 字段` 组成:

- SectionTitle 16px / 600 / `#111827`,padding-bottom 12px,下边框 `1px solid #e5e7eb`。
- Section 间距(gap)固定 24px。
- Section 的标题使用**名词性 2-4 字短语**,不写疑问句、不写说明:`基础信息` / `任务规则` / `选择客群` / `权限设置`,不写"请填写以下基础信息"。
- Section 顺序:`基础信息` → `业务规则` → `范围/对象` → `高级/可选`。
- 每个 Section 至少包含 1 个字段。空 Section 不保留。
- 折叠 Section(`collapsible`)仅在 `Advanced Create` 组合中允许;Create / Edit 组合不使用折叠。

### Section 的内边距

- Section 容器自身 **padding 0**;所有留白由 `SectionTitle` 的 padding-bottom + Section gap 与 Body padding 提供,**禁止叠加**。

## 6. 字段规则

### label

- 位置:每个字段的 label 在 control 的左侧,横向排列,顶部对齐。
- 宽度:固定 96px(`Advanced Create` 中可调至 120px,同抽屉内必须一致)。
- 对齐:右对齐。
- 文案:名词性,不带冒号;冒号由 FormItem 组件自动添加。
- 必填红星 `*` 位于 label 左侧,颜色 `#dc2626`,与 label 间隔 4px。

### controlSlot

- 控件类型由 [field-control-map](field-control-map.md) 决定。
- 控件默认宽度 320px;需要时可设置 `widthTier` ∈ `200 / 304 / 408 / FULL`,FULL 表示填满扣除 label 后的剩余宽度。
- `Textarea` 默认 rows=4,`FULL` 宽度。
- `Radio.Group` 方向默认 horizontal;字段数 ≥ 4 或文案超过 4 字时使用 vertical。
- `Upload` 单独成行,与其他字段不做 columnMode=double 并列。

### 错误 / 帮助

- helpText 出现在控件下方,字号 12px,颜色 `#6b7280`。
- errorMessage 取代 helpText 位置,颜色 `#dc2626`。
- errorMessage 文案必须说明**为什么**错,不写"格式错误"这类无信息文案:`任务名称至少 4 个字符`。

### 字段顺序

同一 Section 内字段顺序按"必填优先、短字段优先、常用优先";长文本(Textarea)、Upload、富文本永远放在 Section 末尾。

## 7. 布局与间距铁律

| 项 | 数值 | 说明 |
| --- | --- | --- |
| Drawer 距 viewport 边 | 0 | 完全贴右 |
| Header 高度 | 56px | padding `0 24px` |
| Footer 高度 | 52px | padding `12 24px` |
| Body padding | 24px | 上下左右一致 |
| Section 间距 | 24px | Body 的 `gap` |
| Section 内字段间距 | 16px | FormItem 的垂直 gap |
| Label 宽度 | 96px(默认) | Advanced 可 120px |
| Label 与 control 间距 | 12px | FormItem 的内部 gap |
| Label 顶部 offset | 6px | 让 label 文本与 control 第一行垂直对齐 |
| control 默认宽度 | 320px | narrow 场景;FULL = 剩余宽度 |

**铁律**:除上述值之外,**不允许在 Drawer、Body、Section、FormItem 上叠加自定义 padding/margin/gap**——所有留白从这 10 项中取。

## 8. 状态与校验

一个抽屉**同时只展示一种状态**:

| 状态 | 处理 |
| --- | --- |
| Data | 默认值;字段为可编辑 Data 状态 |
| Loading | 抽屉打开后异步加载字段初始值时使用;Footer `确定` Button loading,字段为 Skeleton |
| Disabled | 全部字段不可编辑,Footer 无主操作;用于 Readonly / 无权限场景 |
| Error | 加载失败;Body 显示 Error 提示 + 重试;不使用 Empty |

**禁止**:

- 在同一抽屉内同时堆叠 Data + Loading + Disabled 字段,也不能在一个字段上同时显示"必填红*"与"错误红框",除非用户刚触发校验。
- 切换状态时不修改 Section / Field 结构,只切换可见性和 disabled 属性。

### 校验时机

- required 校验:失焦 + 点击主操作时触发,不实时触发。
- 格式 / 范围校验:失焦时。
- 跨字段校验(如 startDate < endDate):点击主操作时。
- 提交失败:在 Footer 上方显示 `Alert type=error` + 错误描述,不打断字段值。

## 9. 响应与约束

- 抽屉宽度不随 viewport 拉伸;`widthTier` 一旦选定不再变化。
- viewport 高度变化时,Footer 保持 pinned,Body 滚动。
- 内容超出抽屉宽度时,单个控件允许 `text-overflow: ellipsis`,不换行;不压缩 label 宽度。
- 不为抽屉在窄屏(<1280px)下做"宽度自适应"——B 端默认桌面端使用,移动端不属于本 Skill 的范围。

## 10. 推荐节点命名

```text
Drawer / <Object> / <Action>                  例:Drawer / TriggerTask / Create
├── Drawer / Header
│   ├── Title
│   └── CloseBtn
├── Drawer / Body
│   ├── Section / <Name>                    例:Section / 基础信息
│   │   ├── SectionTitle
│   │   └── FormItem / <fieldKey>           例:FormItem / taskName
│   │       ├── FormLabel
│   │       ├── Required Mark
│   │       └── Control / <controlName>
│   └── Section / <Name>.error / <Name>.loading   (同名 Section 的状态变体)
├── Drawer / Footer
│   ├── Button / Cancel
│   ├── Button / OK
│   └── Button / Danger(可选)
└── Audit / Missing Components(仅有缺口时)
```
