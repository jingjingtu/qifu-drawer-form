# 智客星平台基线

## 目录

- [平台标识](#1-平台标识)
- [生成策略](#2-生成策略)
- [基线模板](#3-基线模板)
- [页面外壳](#4-页面外壳)
- [侧栏菜单树](#5-侧栏菜单树)
- [筛选与表格差异](#6-筛选与表格差异)
- [变量与文字](#7-变量与文字)
- [输入解析示例](#8-输入解析示例)

## 1. 平台标识

```yaml
adapter:
  id: platform-zhikexing
  displayName: 智客星
  generationStrategy: copyTemplate
  theme:
    primary: '#00B578'
  shell:
    header: 模板内置智客星 Header（48px，不单独解析组件节点）
    sidebar: 模板内置智客星 SideNavigation（200px）
```

- `platform=zhikexing` 时，`generationStrategy` 固定为 `copyTemplate`，不得改回 `assemble`。
- 智客星 Header / SideMenu 没有独立发布的组件映射（不同于毓数的 `Yushu Header-V2` + `SideMenuItem-V2`）；外壳由复制基线模板整体获得，不逐项组装。

## 2. 生成策略

`copyTemplate` 与毓数的 `assemble` 是两条不同的落图路径，共用同一套组件库 `gTV3VdC6a5e9vpkRHIZSXA`：

| 策略 | 平台 | 落图方式 | Slot 处理 | 失败处理 |
| --- | --- | --- | --- | --- |
| `assemble` | yushu / generic | 从组件库解析组件并逐项组装实例 | Slot 逐层同步 | 写失败即 `FAIL` |
| `copyTemplate` | zhikexing | 复制人工基线模板整页，再改可回读属性 | 不直接写 Slot，保留模板原有内容 | 结构需变则 `BLOCKED_TEMPLATE` |

`copyTemplate` 存在的原因是：当前 Figma Connector 对 Slot 写入不稳定，复制已调好的完整模板能保证"改不动的地方也保持有效"。选择哪条路径由平台文件声明，不由业务字段决定。

## 3. 基线模板

当前唯一智客星基线位于组件库文件：

```text
Template / List Page / 智客星 / 1440 / 手动调整
node: 4892:34812
实际尺寸: 1366 x 768
```

- 名称中的 `1440` 是历史命名，不得据此改变画板宽度；后续新页面一律按实际 `1366 x 768`。
- 模板重命名由人工单独处理，不在生成任务中改动。
- 解析顺序：先用节点 `4892:34812`；节点不可用时按完整名称 `Template / List Page / 智客星 / 1440 / 手动调整` 搜索，再校验真实尺寸仍为 `1366 x 768`。

## 4. 页面外壳

- 顶部栏 48px，使用模板中已有的智客星 Logo、帮助、通知、头像和用户信息；不重新绘制 Logo 或用户区。
- 侧栏宽 200px，底部保留 40px 的收起控制区，收起图标为已有 16px 图标实例。
- 一级菜单高 44px，二级菜单高 40px。一级菜单有真实图标，二级菜单不显示图标。
- 当前叶子菜单使用既有品牌色文字、浅色背景和右侧绿色指示条；当前路径祖先使用品牌色文字与图标。
- 未选中菜单使用既有中性色；不得直接填充绿色或改用别的平台变量。

## 5. 侧栏菜单树

```text
首页
客户管理
客户添加
  加微渠道
  客服场景
  加微链接
  欢迎语模板
智能运营
客户经营
团队辅助
资产管理
系统管理
```

- 业务输入中的 `sidePath` 可以改写该树中既有项的激活状态，不新增菜单层级。
- 需要新增一级、二级或三级菜单时，用户必须提供完整路径、层级和组件库中唯一的图标组件名；否则 `BLOCKED_TEMPLATE`。

## 6. 筛选与表格差异

智客星当前标准组合为「4+1 筛选 + selectable 表格」，与毓数 `compositionName` 注册表的差异：

- 首行 4 个带标题筛选项，行高 32px；每项总宽 265.25px，标题 70px，控件约 195px，项间 12px。
- 第二行在第一项放日期或日期范围筛选；日期项标题宽按文本 Hug，默认控件宽 240px。
- `确定` 和 `重置` 位于第二行右侧，均为 32px；确定为主按钮，重置为线框按钮。
- 筛选栏高度 76px；筛选栏底部到列表操作栏顶部固定 16px。
- 表格为 `selectable / 44px / bordered`；表头与数据行均为 44px。
- 可见列宽数组固定为 `[48, 80, 160, 160, 90, 90, 120, 100, 100, 160]`，可见内容宽 1108px；表格外壳宽 1110px。
- 默认 Data 状态展示 8 行，最少 5 行、最多 8 行。
- 状态一律使用真实 Tag：`variant=light`、`size=medium`、`shape=square`、`disabled=false`、`Show icon=false`、`Show closeBtn=false`。

筛选数量不是 4+1、或是否多选/列数/表格密度/状态与上述不符时，先寻找同文件中已人工确认的匹配智客星模板；找不到时停止并报告 `BLOCKED_TEMPLATE`。不得为满足业务字段改写 Slot、手绘表格或临时拼装另一套页面。

## 7. 变量与文字

- 品牌色 `#00B578`、菜单选中背景、文字、边框和表格底色均继承复制模板中的变量绑定。
- 标题、筛选 Label、表头、表格正文和链接继承原实例的文本样式；不可改成未绑定的 MiSans 或裸字。
- 一级菜单图标在选中祖先或当前项中必须实际呈现品牌色，而不仅是完成 INSTANCE_SWAP。

## 8. 输入解析示例

输入：

```text
在智客星的客户添加 > 加微链接下创建加微链接列表页。
```

解析：

```text
platform=zhikexing
generationStrategy=copyTemplate
sidePath=[客户添加, 加微链接]
sideActive=加微链接
sideExpanded=[客户添加]
sideAncestorsActive=[客户添加]
基线模板节点=4892:34812
```
