# 共享页面上下文

所有页面 Skill 先解析同一份 `PageContext`，再追加自己的 Archetype Spec。字段名称和默认值不得在页面 Skill 中另起方言。

```yaml
platform: generic | yushu | zhikexing | zhineng-yunying | <registered-platform>
platformName: <display name>
themeKey: <registered-theme-or-null>
target:
  fileUrl: <figma file or node url>
  page: <target page name or id>
  anchor: <optional node name or id>
  placement: <blank area | right of anchor | explicit coordinates>
navigation:
  headerActive: <optional>
  sidePath: [<level-1>, <level-2>, <level-3>]
state: data | loading | empty | error | disabled
permissions: [view, create, edit, delete, export, approve]
viewport: 1366x768 | 1920x1080
assumptions: []
```

## 统一默认值

- 未指定平台且目标文件没有可靠平台上下文：`platform=generic`，不得静默套用毓数或智客星。
- 未指定状态：`state=data`。
- 未指定权限：只保留完成用户明确任务所需的最小动作，不推断删除、发布或审批权限。
- 未指定目标 Page 或插入位置且无法从链接唯一解析：先询问，不写入第一个 Page，也不新建近义 Page。
- 测试或 Skill 回归仅在组件库测试环境中复用已登记的测试 Page；正式交付始终使用用户指定位置。

## 页面 Spec 映射

| 公共字段 | List | Drawer | Detail |
| --- | --- | --- | --- |
| `platform` | `platform` | `platformKey` | `platform` |
| `target.fileUrl` | Figma 目标链接 | `targetFileUrl` | Figma 目标链接 |
| `target.page` | `targetPage` | `targetPage` | `targetPage` |
| `target.anchor` | 插入位置 | `targetAnchor` | 插入位置 |
| `target.placement` | 插入位置 | `targetPlacement` | 插入位置 |
| `navigation.sidePath` | `sidePath[]` | `background.sidePath[]` | `sidePath[]` |
| `state` | 页面状态 | 抽屉状态 | `defaultState` |

页面 Skill 可以保留兼容字段名，但内部决策先归一化为 `PageContext`。交付摘要返回公共字段以及页面专属 Spec。

## 授权边界

生成页面不等于获准修改组件库母版、发布组件、改写本仓库或同步到其他目录。发现可复用规则时只记录建议；只有用户明确要求维护仓库或组件库时才执行对应修改。
