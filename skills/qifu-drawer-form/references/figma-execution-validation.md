# Figma 执行与结构化验收

截图只能证明视觉结果，不能证明抽屉仍由真实组件实例组成。本文件把组件解析闭环、属性回读、Slot 验证、P0 失败即停和 PASS/BLOCKED/FAIL 结果约束落到右侧抽屉场景。

## 1. 验收顺序

严格按以下顺序执行：

```text
DrawerSpec 完整性
→ ComponentResolutionManifest
→ 实例属性回读
→ 页面结构计数
→ Slot 与父级关系
→ 变量与几何
→ 分区截图
→ 整页截图
```

前一阶段失败时停止，不使用截图或肉眼观感掩盖结构失败。

## 2. ComponentResolutionManifest

每个必需能力必须有一条记录：

```text
capability
exactName
source = localNode | publishedKey | exactName | portableLocal
sourceFile
componentId
publishedKey
instanceIds[]
expectedCount
publicProperties[]
propertyPlan[]
slotTarget
status = resolved | fallback | missing | ambiguous | unverified | failed
evidence = user-description | screenshot | component-map | target-file | inferred
```

解析顺序：

1. 同文件优先使用组件映射中的本地节点 ID 或目标文件已有组件节点。
2. 节点失效时按完整组件集名称精确搜索。
3. 跨文件使用已发布 Key 导入，并核对完整组件名称。
4. `PORTABLE_KIT` 模式按 Portable 清单精确查找当前文件本地组件，不依赖 `publishedKey`。
5. 候选为 0 报告 `COMPONENT_MISSING`；候选多于 1 报告 `COMPONENT_AMBIGUOUS`。
6. `REAL_COMPONENT_ONLY` 与 `PORTABLE_KIT` 下，只有所有必需能力均为 `resolved`，才能开始页面组装。

## 3. P0 重点检查

以下任一项失败，整页结构状态为 `FAIL`：

1. **真实实例关系**：Close、Input、Select、Radio、Checkbox、Switch、Textarea、Button、Table、Pagination 以及 Slot 内容均为 `INSTANCE`；每个实例有正确 `mainComponent`，不能用裸 Text、矩形、截图或 Group 替代。
2. **单一语义控件**：每个 `Control / <fieldKey>` 只有一个语义控件根节点；不存在旧实例、临时控件、重复边框、重复箭头或实例外同文案覆盖。
3. **属性闭环**：每个公开属性均完成“读取真实 Key → 校验类型和值域 → 写入 → 回读最终值”。`PROPERTY_NOT_FOUND`、`PROPERTY_AMBIGUOUS`、`PROPERTY_WRITE_FAILED`、`PROPERTY_READBACK_MISMATCH` 均判失败。
4. **Slot 与父级**：Drawer、Body、Section、Form Row、Footer 和 Table Slot 的父级关系正确；Slot 当前值指向刚创建的真实实例，Auto Layout 没有把内容裁切或推出抽屉边界。
5. **关键几何**：Drawer、Header、Body、Footer 层级唯一；内容 padding、Section 间距、字段同行对齐、按钮右对齐均符合 DrawerSpec；无重叠、溢出和异常空白。
6. **字体与变量**：新增自由文本绑定组件库文本样式；组件内部字体、颜色、间距和圆角仍由母组件或变量控制，不用页面级固定样式覆盖。

## 4. 抽屉结构计数

按 DrawerSpec 形成计数不变量：

```text
Drawer Frame = 1
Header = 1
Body = 1
Section = sections.length
Form Row = fields.length
每个字段语义控件 = 1
Close = 1
Footer 主按钮 = 1（若 DrawerSpec 要求）
Footer 次按钮 = 0..N（按 DrawerSpec）
```

如果抽屉内包含表格，额外验证：

```text
Table Shell = 1
Header Cell = columns.length
Row = rows.length
Content Cell per Row = columns.length
Pagination = showPagination ? 1 : 0
```

表格状态标签统一使用真实 Tag 组件，并回读形态、尺寸、禁用态、icon 和 close 属性。只有 DrawerSpec 明确要求额外状态内容能力且内部 Tag 仍满足该契约时，才允许使用特殊状态组件。

## 5. 变量、颜色与视觉矩阵

- Header 关闭实例不得叠加实例外 `×`、`x`、Vector 或线段。
- Radio 选项文字左侧只允许一个真实 Radio 实例，不得叠加圆环、圆点或自由绘制图形。
- 必填星号属于 Label 或 FormItem 组合，不能进入 Input/Select 实例或与标题重叠。
- 选中步骤、按钮层级、状态 Tag 和表格选择列必须按组件公开变体或变量设置；父节点状态正确但子图标颜色错误仍判失败。
- 表格中所有列使用同一列宽数组；Pagination 紧跟最后一行且右边缘与表格一致。
- 截图识别出的字段、操作和页面区域都要保留 evidence；截图噪声不得进入最终画板。

## 6. 失败码

| 代码 | 含义 | 处理 |
| --- | --- | --- |
| `COMPONENT_LIBRARY_UNAVAILABLE` | 目标文件无法调用组件库 | 严格模式停止写入 |
| `COMPONENT_MISSING` | 目标库没有能力 | 严格模式停止该区域；宽松模式才评估 Fallback |
| `COMPONENT_AMBIGUOUS` | 候选不唯一 | 停止，报告候选完整名称 |
| `PLATFORM_PROFILE_MISSING` | 指定平台缺少平台壳、导航或底图协议 | 独立抽屉可继续；平台壳交付停止并记录缺口 |
| `THEME_VARIABLE_MISSING` | 主题主色无法绑定到变量或组件公开属性 | 停止改色，不 detach 组件手工覆盖 |
| `PORTABLE_COMPONENT_MISSING` | Portable Kit 缺少本地组件 | 停止，报告缺失能力 |
| `STYLE_MISSING` | 必需文本样式或字体不可用 | 停止，不手填近似样式 |
| `PROPERTY_NOT_FOUND` | 属性 Key 不存在 | 停止，不覆盖实例文本 |
| `PROPERTY_AMBIGUOUS` | 属性 Key 不唯一 | 停止，不猜选第一个 |
| `PROPERTY_WRITE_FAILED` | 属性写入失败 | 停止，报告实例与错误 |
| `PROPERTY_READBACK_MISMATCH` | 回读与目标值不一致 | 停止，报告期望/实际值 |
| `SLOT_WRITE_FAILED` | Slot 无法替换 | 停止，不手绘对应区域 |
| `POSTCONDITION_FAILED` | 数量、父级、边界或变量验收失败 | 停止，不标记完成 |

## 7. 交付状态

```text
structuralValidation = PASS | BLOCKED | FAIL
visualValidation     = PASS | BLOCKED | FAIL
```

- `PASS`：结构、实例、属性、Slot、变量和截图均通过。
- `BLOCKED`：缺少会改变抽屉主结构、目标文件或组件权限的信息。
- `FAIL`：组件解析、属性写入、Slot、字体、实例关系或视觉验收失败。

只有两个状态都为 `PASS`，才能向用户说“已完成”。
