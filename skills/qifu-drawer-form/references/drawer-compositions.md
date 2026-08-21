# 抽屉表单组合注册表

## 目的

用稳定名称描述右侧滑出的表单抽屉结构。后续调用必须使用下表中的完整 `compositionName`;这些名称属于 Skill 的调用协议,不是 Figma 组件母版名称。

与 `qifu-list-page/references/table-compositions.md` 的关系:同一份"配方协议"思想在不同原型上的复用;不得把列表页的 6 个组合名搬到抽屉,也不得临时创造第 7 个抽屉组合。

## 已注册组合

| `compositionName` | 适用场景 | Section 数 | 单列/双列 | Footer 操作 | 默认状态 |
| --- | --- | --- | --- | --- | --- |
| `Qifu Drawer Form / Simple Create` | 新建,字段 ≤ 6,无业务分组 | 1 | 单列 | 取消 + 确定 | Data |
| `Qifu Drawer Form / Sectioned Create` | 新建,7–15 字段,有明确业务分组 | 2–3 | 单列 | 取消 + 确定 | Data |
| `Qifu Drawer Form / Advanced Create` | 新建,> 15 字段或需分步 | 3+ 或 Steps | 单列/双列 | 取消 + 上一步/下一步/提交 | Data |
| `Qifu Drawer Form / Edit` | 编辑已有记录,字段需回填 | 同 Sectioned | 单列/双列 | 取消 + 保存 | Data 已回填 |
| `Qifu Drawer Form / Readonly` | 查看(不可编辑),与 Detail 配合使用 | 1–N | 描述列表 | 关闭 | Disabled |
| `Qifu Drawer Form / Data Detail with Table` | 数据详情、跟进详情、任务明细等含摘要、筛选与内嵌表格的抽屉 | 2 个内容卡片 | 单列 + 表格 | 可无 Footer；表格独立分页 | Data |

## 调用规则

1. 用户给出完整 `compositionName` 时精确匹配,大小写、空格和斜杠保持一致。
2. 用户未给名称时按以下优先级选择:含摘要/筛选/内嵌表格的数据详情 → Readonly 需求 → Edit 需求(字段需回填) → 字段数 > 15 或步骤 ≥ 3 → 字段数 7–15 且有分组 → 字段数 ≤ 6 无分组。
3. 未指定且无法区分时使用 `Qifu Drawer Form / Sectioned Create`。
4. 组合名称只决定稳定结构(分区框架、按钮组、默认状态);业务字段、文案、控件、数据、`widthTier` 仍由当前 `DrawerSpec` 决定。
5. 不把业务对象、页面名称、状态文案或视觉尺寸拼进 `compositionName`,也不创建 `Basic`、`Normal`、`Default` 等未注册别名。
6. 新场景无法由现有组合表达时,先使用最接近的已注册组合并记录缺口;只有用户确认需要形成长期复用结构后,才新增组合名称并同步本注册表、`SKILL.md` 和验证规则。
7. `Data Detail with Table` 必须完整读取 `golden-sample-data-detail-drawer.md`，并以 680px、16px 内容安全边距、真实组件表格、独立分页器和整数几何为验收门槛。

## 解析结果

每次调用在内部形成以下结构,并在交付时回报 `compositionName`:

```text
compositionName
sectionCount
columnMode          single | double
footerButtons[]     cancel | prev | next | ok | save | close
defaultState        data | loading | disabled | error
```

不得以重命名 Figma 组件的方式实现上述协议。真实组件仍按[组件映射](component-map.md)中的正式名称解析。

## 与列表页 6 组合的对照

仅为理解迁移成本,不构成调用允许:

| 列表页 `compositionName` | 抽屉页对应 | 关键差异 |
| --- | --- | --- |
| `Basic Table` / `Basic Filter Table` | `Simple Create` | 列表页按筛选数选,抽屉按字段数选 |
| `Advanced Filter Table` | `Sectioned Create` | 列表按"筛选行数"分,抽屉按"分区数"分 |
| `Selectable Filter Table` | `Advanced Create` | 都涉及"更复杂的操作上下文" |
| `Loading Table` / `Empty Table` | `Readonly` + 将来如需补 `Loading / Error` | 抽屉的 Loading / Error 目前在 `defaultState` 字段标记,不单独成组合 |
