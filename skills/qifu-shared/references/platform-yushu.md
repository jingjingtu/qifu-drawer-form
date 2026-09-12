# 毓数平台导航基线

## 目录

- [适用范围](#1-适用范围)
- [顶部导航](#2-顶部导航)
- [侧栏菜单树](#3-侧栏菜单树)
- [侧栏图标映射](#4-侧栏图标映射)
- [组装规则](#5-组装规则)
- [输入解析示例](#6-输入解析示例)

## 1. 适用范围

当前标准数据表格页默认以毓数平台为基准。用户明确指定其他平台时，不套用本文件的菜单名称；先读取对应平台参考，缺少参考时仅询问会改变页面框架的导航信息。

平台规格使用以下字段：

```text
platform        yushu
navigationMode  yushuPreset | custom；未填默认 yushuPreset
headerActive    数据资产 | 自助查询 | 数据开发 | 指标管理 | QBI
sideActive      当前页面所在的侧栏菜单
sideActiveLevel 1 | 2 | 3；固定等于 sidePath.length
sideExpanded[]  当前展开的父菜单；固定等于 sidePath 中除最后一项外的祖先
sideAncestorsActive[] 当前页的祖先菜单；固定等于 sideExpanded[]
sidePath[]      从一级菜单到当前页面的完整路径
```

`sideActive` 固定为 `sidePath` 最后一项并决定唯一当前菜单。只有当前路径祖先可以进入 `sideExpanded` 与 `sideAncestorsActive`；其他菜单即使有子集也保持收起。

### 导航模式

`navigationMode=yushuPreset` 使用本文件的默认菜单树和图标映射；`sidePath` 必须真实存在，不存在时停止并请用户确认真实父级或切换为 `custom`。

`navigationMode=custom` 时必须提供：

```text
customSideMenu.level1[]: label, iconComponentName, hasChildren
customSideMenu.activeLevel1Children[]: label, hasChildren
customSideMenu.activeLevel2Children[]: label
```

- `sidePath` 只允许 1–3 段，最后一段是唯一当前项。
- 当前路径中的父项必须完整列出其可见子项；非当前路径父项保持收起。
- 每个一级 `iconComponentName` 必须使用 `Icon/<system>/<purpose>` 形式的完整名称，唯一解析并完成 INSTANCE_SWAP 回读；缺失、多解或写入失败都停止，不模糊匹配或绘制替代图标。

## 2. 顶部导航

使用真实组件：

- 组件集：`Navigation / HeaderMenu / Yushu Header-V2`
- 节点 ID：`3639:1529`
- 发布 Key：`13dd3304a68853196f2a683bba7ebd034e2928ee`
- 属性：`activeMenu 当前菜单`
- 画板宽度：1366px；放入宽屏页面时横向填充，保持 48px 高。

固定内容：

- 左侧 Logo；
- 菜单顺序：数据资产、自助查询、数据开发、指标管理、QBI；
- 中文顶部菜单使用目标组件库已批准的中文 Text Style；不得用不支持中文的字体造成截断或只显示末尾单字。
- 右侧功能图标顺序：帮助、通知、申请工单、问题上报；
- 头像与用户名使用用户明确提供的账号上下文；未提供时保留组件的中性占位状态，不把组件库样例中的个人信息复制到业务页面；
- 用户名右侧保留下拉箭头。

用户指定顶部入口时设置对应 `activeMenu 当前菜单`。未指定时：

1. 根据页面业务推断入口；
2. 无可靠映射时默认 QBI；
3. 不因侧栏菜单名称擅自新增顶部菜单。

## 3. 侧栏菜单树

当前已确认的一级结构：

```text
探索分析
智能分析
├── 智能探查
└── 智能报表
仪表板
图表管理
在线Excel
数据集
数据源
订阅管理
├── 订阅计划
└── 群组管理
权限管理
├── 用户授权
└── 角色授权
归因配置
```

结构属性：

| 菜单 | Level | Has Submenu | 默认展开 | 已确认子项 |
| --- | ---: | --- | --- | --- |
| 探索分析 | 1 | False | — | — |
| 智能分析 | 1 | True | False | 智能探查、智能报表 |
| 智能探查 | 2 | False | — | — |
| 智能报表 | 2 | False | — | — |
| 仪表板 | 1 | False | — | — |
| 图表管理 | 1 | False | — | — |
| 在线Excel | 1 | False | — | — |
| 数据集 | 1 | False | — | — |
| 数据源 | 1 | False | — | — |
| 订阅管理 | 1 | True | False | 订阅计划、群组管理 |
| 订阅计划 | 2 | False | — | — |
| 群组管理 | 2 | False | — | — |
| 权限管理 | 1 | True | False | 用户授权、角色授权 |
| 用户授权 | 2 | False | — | — |
| 角色授权 | 2 | False | — | — |
| 归因配置 | 1 | False | — | — |

默认树中所有一级菜单初始均为收起。只有 `sidePath` 经过的祖先展开；父菜单使用祖先激活样式，不出现当前页背景和指示条，但文字、图标和展开箭头使用主题色。

## 4. 侧栏图标映射

图标使用奇富本地图标组件，显示尺寸为 16×16。默认预设优先使用下表节点 ID 或发布 Key；节点失效时按完整名称重新发现，不凭图形相似度猜测。

| 一级菜单 | 图标组件 | 节点 ID | 发布 Key |
| --- | --- | --- | --- |
| 探索分析 | `Icon/dashboard` | `2312:176` | `cddd55e261b7284efe5494d80e3c2dbf09998bd5` |
| 智能分析 | `1.通用/Icon图标/QBI/智能问数`（组件卡片标签 `icon-icon_zhinengfenxi`） | `3721:11165` | `04c1d64632ac2521859af7ac7c7944e433e7c243` |
| 仪表板 | `Icon/yibiaoban1` | `2422:108` | `6a427095b3dceb7ec1bc607d8fd8a48f05113049` |
| 图表管理 | `Icon/table` | `2312:226` | `a1fd6e8cf04cc27cd41ba569c2dc5c6179f89e09` |
| 在线Excel | `Icon/xianshangexcel` | `2422:102` | `ab07f8c04fc81477141d1ad1a9abf3a70710fdb5` |
| 数据集 | `Icon/flow-manage` | `2423:444` | `b7831e070308984a7cff8e645596c627969e9973` |
| 数据源 | `Icon/shuju` | `2312:130` | `7694e996fbaa935b8cf853cea903ae1d560134bd` |
| 订阅管理 | `Icon/manage` | `2312:248` | `5099bcf783cfb7d636ee2d8bbfa721cdae565820` |
| 权限管理 | `Icon/quanxianguanli` | `2422:111` | `48a797b2fddf5e3636d610221a02772dd2584868` |
| 归因配置 | `Icon/gongdanliucheng` | `2423:82` | `8fa63bc0c95f2d7f21479b6377eaa7d578405634` |

二级和三级菜单不显示业务图标，只保留文本、层级缩进和必要的展开箭头。

## 5. 组装规则

使用真实 `Navigation / SideMenu / SideMenuItem-V2` 实例逐项组装，不创建固定业务大组件：

1. 宽度固定为 200px；一级菜单高 44px，二、三级菜单高 40px。
2. 每个实例按共享组件调用基线动态解析 `Label`、`Level`、`Has Submenu`、`State` 的真实 Key，写入后立即回读。
3. 一级菜单将 `showIcon 显示图标` 设为 `true`；默认模式使用本文件映射，自定义模式使用完整唯一的 `iconComponentName`。两者都必须完成 INSTANCE_SWAP 回读。
4. 二、三级菜单保持纯文本层级，不显示业务图标；`Has Submenu=True` 时仅保留组件自带的展开箭头。
5. `sideActive` 是唯一的当前页菜单并使用 `State=Selected`；如果它是无子菜单叶子，则显示绿色选中背景与右侧指示条。
6. `sideExpanded` 中的路径祖先设置 `expanded 展开=True` 并插入已确认子项；所有不在当前路径的一级、二级父项设置为 `False`。
7. 页面落在二级或三级菜单时，从 `sidePath` 排除 `sideActive` 得到 `sideAncestorsActive`。所有祖先都使用 `State=Selected` 且保持 `expanded 展开=True`，呈现白底、文字/一级图标/展开箭头主题绿；这表示祖先路径高亮，不表示父菜单是当前页。
8. 不在 `sideAncestorsActive` 中的菜单必须保持 `State=Default` 和收起；不能为了展示更多菜单而额外展开。
9. 菜单区域使用垂直 Auto Layout。侧栏整体填满 Header 以下高度；菜单滚动区 `layoutGrow=1`、裁切内容并允许纵向滚动。
10. 底部固定保留 `collapse-button`：分割线 + `Icon/shouqi`，组件节点 `2423:450`。滚动只作用于菜单区域，不让收起按钮随菜单滚走。
11. 静态画板需要展示完整菜单时允许增加画板高度；不得压缩菜单项高度，也不得让菜单覆盖底部收起按钮。
12. Label、图标或状态写入失败时停止，不创建导航文字覆盖层、裸文字或替代图标。

### 各级菜单状态视觉矩阵（P0）

| 菜单角色 | 状态 | 背景与指示 | 文字/图标/箭头 |
| --- | --- | --- | --- |
| 当前页叶子 | `Selected` | 选中背景与右侧指示条 | 主题色 |
| 当前路径祖先 | `Selected` + `expanded=True` | 白底、无当前页指示条 | 主题色 |
| 非当前路径菜单 | `Default` + 收起 | 白底、无指示条 | 中性色 |

一级图标完成 INSTANCE_SWAP 后还要检查最终可见 paint 或语义变量。图标仍为黑色或其他中性色时本项判 `FAIL`；不得用页面级固定色覆盖修正。

## 6. 输入解析示例

输入：

```text
在毓数平台的权限管理 > 用户授权下新增用户授权列表页，顶部位于 QBI。
```

解析：

```text
platform=yushu
headerActive=QBI
sidePath=[权限管理, 用户授权]
sideActive=用户授权
sideExpanded=[权限管理]
sideAncestorsActive=[权限管理]
```

输入：

```text
在订阅管理 > 群组管理新增群组管理列表页。
```

解析：

```text
platform=yushu
headerActive=QBI（未提供且无可靠业务映射时的默认值）
sidePath=[订阅管理, 群组管理]
sideActive=群组管理
sideExpanded=[订阅管理]
sideAncestorsActive=[订阅管理]
```

输入：

```text
在智能分析 > 智能报表增加报表任务列表。
```

解析：

```text
platform=yushu
headerActive=QBI（未提供且无可靠业务映射时的默认值）
sidePath=[智能分析, 智能报表]
sideActive=智能报表
sideExpanded=[智能分析]
sideAncestorsActive=[智能分析]
```
