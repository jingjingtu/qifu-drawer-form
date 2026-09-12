# 智能运营平台适配器

## 平台标识

```yaml
adapter:
  id: platform-zhineng-yunying
  displayName: 智能运营平台
  generationStrategy: existing-or-preview
  defaultTheme: smartops-blue
  shellReadiness: partial
```

当前已经确认智能运营平台的蓝色主题变量和抽屉 Golden Sample，但尚未登记可作为全局基线的专属 Header、SideNavigation 与列表页模板。因此本 Adapter 能稳定生成抽屉本体和主题，不能在缺少真实来源时宣称完整还原平台外壳。

## 背景策略

按以下顺序解析：

1. 用户提供已验收的智能运营平台列表页节点时，使用 `EXISTING_LIST_PAGE`。
2. 目标 Page 中存在唯一、已验收且可回读的平台列表页时，可以自动采用该节点，并在交付摘要中记录证据。
3. 找不到可靠来源时使用 `STRUCTURE_PREVIEW + Overlay Mask`，只表达页面结构，不绘制虚构 Logo、菜单或业务数据。

在专属模板完成登记前，不使用 `TEMPLATE`，也不借用智客星或毓数页面壳。

## 主题与术语

- 默认 `themeKey=smartops-blue`，对应 `基础` collection 的 `智能运营/Light` 模式和 `mode/blue` 颜色变量组。
- 新建、编辑、查看等通用操作词沿用业务输入；平台特有术语以用户提供的页面或文案为准，不自行扩写。
- 主按钮、链接、选中态、轻量 Tag 和强调线绑定蓝色语义变量；组件未暴露对应属性时返回 `COMPONENT_SOURCE_GAP`，不 detach 实例改色。

## 验收边界

- 使用 `EXISTING_LIST_PAGE` 且平台来源、主题变量和抽屉双重验证均通过时，可以标记为正式平台打开态。
- 使用 `STRUCTURE_PREVIEW` 时，抽屉本体可以通过结构和视觉验收，但平台外壳状态必须返回 `PREVIEW_ONLY`。
- 批量对比中必须保留与其他平台一致的 `baseDrawer` 内容指纹；不得因为智能运营平台缺少模板而修改字段、组合或 Footer。
