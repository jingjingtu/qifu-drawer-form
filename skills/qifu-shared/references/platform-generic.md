# 通用 B 端平台适配器

用于需求未指定平台、正在做跨平台抽象，或目标平台尚未建立正式适配器时。

```yaml
adapter:
  id: platform-generic
  displayName: Generic B-end Platform
  shell:
    header: Navigation / HeaderMenu / HeaderMenu
    sidebar: Navigation / SideMenu / SideMenuItem-V2
    breadcrumb: Navigation / Breadcrumb / BreadcrumbItem
  navigation:
    menuSource: user-provided
    selectedRule: current-leaf-selected
  vocabulary:
    create: 新建
    edit: 编辑
    view: 查看
    search: 查询
  slots: []
  permissions:
    actionVisibility: explicit
```

## 默认行为

- 不创建虚构菜单项；使用用户给出的菜单路径，未知层级标记 `TODO`；
- 使用 `component-map.md` 中的正式导航组件；
- 页面主体由对应 Archetype Skill 负责；
- 平台专属能力放入 `Slot / <name>`；只有共享调用基线确认 `COMPONENT_MISSING`，且当前页面 Skill 与用户授权允许降级时，才使用 `Fallback / <capability>`；
- 交付时列出需要新建的平台适配器字段。
