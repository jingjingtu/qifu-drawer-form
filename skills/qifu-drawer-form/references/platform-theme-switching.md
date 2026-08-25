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
presentationMode  STANDALONE | OVERLAY_ON_ZHIKEXING_LIST
```

`platformKey` 与 `themeKey` 必须分开写。只说“蓝色平台”时，不得把 `platformKey` 改成 `blue`；应解析为某个平台 + 蓝色主题。

## 2. 已知平台

| platformKey | platformName | 默认 themeKey | 适用说明 |
| --- | --- | --- | --- |
| `zhikexing` | 智客星 | `zhikexing-green` | 当前用户主平台。可单独生成抽屉，也可用 `OVERLAY_ON_ZHIKEXING_LIST` 叠加到智客星列表页底图。 |
| `yushu` | 毓数 | `yushu-green` | 仅当用户明确说“毓数”或指定 `platformKey=yushu` 时使用，不再作为跨平台默认值。 |
| `zhineng-yunying` | 智能运营平台 | `smartops-blue` | 未来蓝色主题平台。当前先复用抽屉表单结构和通用组件；缺少专属导航壳时生成独立抽屉并记录平台壳缺口。 |
| `qifu-generic` | 奇富通用后台 | `zhikexing-green` | 用户未指定平台时的保守默认，只生成抽屉本体，不套用任何平台菜单或业务壳。 |

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
5. 用户没有说平台：使用 `platformKey=qifu-generic`，只生成抽屉本体；不得默认套用毓数菜单。

## 5. 生成约束

- 平台切换不得改变 `compositionName`、字段顺序、控件类型、Footer 主操作和校验规则。
- 主题切换只影响颜色变量、选中态、主按钮和轻量强调，不影响间距、字号、圆角、阴影、控件高度或 Slot 结构。
- 智客星底图叠加只在 `platformKey=zhikexing` 且 `presentationMode=OVERLAY_ON_ZHIKEXING_LIST` 时启用。
- 智能运营平台在平台壳尚未建立前，只能交付独立抽屉或记录 `PLATFORM_PROFILE_MISSING`；不得借用毓数菜单冒充。
- 交付结果必须回报 `platformKey / platformName / themeKey / themePrimary` 和主题变量回读结果。

## 6. 示例提示词

### 智客星绿色主题独立抽屉

```text
使用 qifu-drawer-form，在智客星平台生成“超频流控配置”右侧抽屉。
platformKey：zhikexing
themeKey：zhikexing-green
presentationMode：STANDALONE
componentMode：REAL_COMPONENT_ONLY
```

### 智客星叠加到列表页

```text
使用 qifu-drawer-form 和 zhikexing-list-page，在智客星平台生成“超频流控配置”右侧抽屉。
platformKey：zhikexing
themeKey：zhikexing-green
presentationMode：OVERLAY_ON_ZHIKEXING_LIST
background.source：TEMPLATE
当前菜单：客户运营 / 流控管理
```

### 蓝色主题智能运营平台

```text
使用 qifu-drawer-form，在智能运营平台生成“超频流控配置”右侧抽屉。
platformKey：zhineng-yunying
platformName：智能运营平台
themeKey：smartops-blue
themePrimary：#1677FF
presentationMode：STANDALONE
componentMode：REAL_COMPONENT_ONLY
```
