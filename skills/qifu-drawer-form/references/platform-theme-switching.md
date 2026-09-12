# 平台与主题切换协议

平台切换和主题切换是两个独立维度：平台决定业务壳、菜单路径、业务词汇和默认底图；主题决定品牌色、选中态、链接色、按钮主色和辅助高亮。不得为了换主题复制一套组件库或改写抽屉结构。

## 1. 输入字段

每次生成抽屉时优先解析以下字段：

```text
platformKey    平台唯一标识：zhikexing | yushu | zhineng-yunying | qifu-generic
platformName   中文平台名：智客星 | 毓数 | 智能运营平台 | 奇富通用后台
themeKey       主题标识：zhikexing-green | yushu-green | smartops-blue | custom
themePrimary   主题主色；custom 必填，例如 #1677FF
themeMode      light；当前仅支持浅色后台
presentationMode  DRAWER_OPEN_WITH_BACKGROUND(默认) | OVERLAY_ON_ZHIKEXING_LIST(智客星兼容别名) | STANDALONE_DEBUG(仅内部调试)
background.source AUTO(默认) | TEMPLATE | EXISTING_LIST_PAGE | STRUCTURE_PREVIEW
```

`platformKey` 与 `themeKey` 必须分开写。只说“蓝色平台”时，不得把 `platformKey` 改成 `blue`；应解析为某个平台 + 蓝色主题。

## 2. 已知平台

| platformKey | platformName | 默认 themeKey | 适用说明 |
| --- | --- | --- | --- |
| `zhikexing` | 智客星 | `zhikexing-green` | 当前用户主平台。正式交付默认生成 `1366×768` 完整打开态，使用智客星列表页模板底图 + 蒙层 + 右侧抽屉。 |
| `yushu` | 毓数 | `yushu-green` | 仅当用户明确说“毓数”或指定 `platformKey=yushu` 时使用，不再作为跨平台默认值。 |
| `zhineng-yunying` | 智能运营平台 | `smartops-blue` | 正式交付仍是 `1366×768` 完整打开态；没有专属底图时默认使用中性 `STRUCTURE_PREVIEW + Overlay Mask`。 |
| `qifu-generic` | 奇富通用后台 | `zhikexing-green` | 用户未指定平台时的保守默认；仍生成 `1366×768` 完整打开态，不套用任何平台菜单或业务壳。缺少通用底图时使用 `STRUCTURE_PREVIEW`。 |

## 3. 主题 Token

| themeKey | themePrimary | 用途 |
| --- | --- | --- |
| `zhikexing-green` | `#00B578` | 智客星默认绿色主题；用于主按钮、选中态、链接、轻量标签和强调线。 |
| `yushu-green` | `#00B578` | 毓数当前默认绿色主题；如目标文件变量不同，以真实变量为准。 |
| `smartops-blue` | `#1677FF` | 智能运营平台蓝色主题；用于主按钮、选中态、链接、轻量标签和强调线。 |
| `custom` | 用户指定 | 仅当用户明确给出 `themePrimary` 时启用。 |

主题替换优先使用 Figma 变量、组件公开属性或已存在主题变量；不得 detach 实例后手动改内部颜色。无法绑定变量时返回 `THEME_VARIABLE_MISSING` 或 `COMPONENT_SOURCE_GAP`，并说明哪些组件需要母版补齐。

## 4. 解析顺序

```text
用户描述
→ platformName/platformKey
→ themeKey/themePrimary
→ presentationMode
→ DrawerSpec
→ ComponentResolutionManifest
→ 真实实例组装
→ 主题变量回读
→ 结构与视觉验收
```

平台和主题缺失时按以下规则处理：

1. 用户明确说“智客星”：`platformKey=zhikexing`，默认 `themeKey=zhikexing-green`。
2. 用户明确说“毓数”：`platformKey=yushu`，读取 `platform-yushu.md`。
3. 用户明确说“智能运营平台”或“蓝色主题智能运营平台”：`platformKey=zhineng-yunying`，默认 `themeKey=smartops-blue`。
4. 用户只说“蓝色主题”：保持已解析的平台不变，设置 `themeKey=custom` 或 `smartops-blue`；不得改变字段、组合和结构。
5. 用户没有说平台：使用 `platformKey=qifu-generic`，但仍按完整打开态处理；不得默认套用毓数菜单。没有已批准通用底图时，使用 `STRUCTURE_PREVIEW`。

## 5. 生成约束

- 平台切换不得改变 `compositionName`、字段顺序、控件类型、Footer 主操作和校验规则。
- 主题切换只影响颜色变量、选中态、主按钮和轻量强调，不影响间距、字号、圆角、阴影、控件高度或 Slot 结构。
- 正式交付必须生成 `1366×768` 完整打开态，结构固定为 `Background < Overlay Mask < Drawer`，不得交付裸抽屉。
- `background.source=AUTO` 是默认值：优先使用已验收 `EXISTING_LIST_PAGE`，其次平台 `TEMPLATE`，均不可用时创建 `STRUCTURE_PREVIEW`。预览背景只展示 Header、导航、筛选、表格、分页五类结构，不是正式平台页面。
- 智客星未指定 `background` 时同样使用 `AUTO`：优先使用用户指定且已验收的智客星列表页，其次使用智客星模板，均不可用时使用 `STRUCTURE_PREVIEW`；`OVERLAY_ON_ZHIKEXING_LIST` 作为旧提示词兼容写法等同完整打开态。
- 智能运营平台在平台壳尚未建立前，默认以 `STRUCTURE_PREVIEW` 交付打开态结构；用户提供已验收 `EXISTING_LIST_PAGE` 后才升级为正式平台页面。不得借用毓数或智客星菜单冒充。
- 交付结果必须回报 `platformKey / platformName / themeKey / themePrimary` 和主题变量回读结果。

## 6. 示例提示词

### 智客星绿色主题完整打开态

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“超频流控配置”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。
platformKey：zhikexing
themeKey：zhikexing-green
展示方式：完整页面打开态
底图：使用智客星列表页模板
componentMode：REAL_COMPONENT_ONLY
使用“智客星超频流控配置抽屉 Golden Sample”
widthTier：640
```

### 智客星旧写法兼容

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“超频流控配置”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。
platformKey：zhikexing
themeKey：zhikexing-green
presentationMode：OVERLAY_ON_ZHIKEXING_LIST
background.source：TEMPLATE
当前菜单：客户运营 / 流控管理
使用“智客星超频流控配置抽屉 Golden Sample”
widthTier：640
```

### 蓝色主题智能运营平台

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“超频流控配置”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。
platformKey：zhineng-yunying
platformName：智能运营平台
themeKey：smartops-blue
themePrimary：#1677FF
展示方式：完整页面打开态
background.source：EXISTING_LIST_PAGE
background.sourceNode：<智能运营平台已验收列表页节点 ID>
componentMode：REAL_COMPONENT_ONLY
```
