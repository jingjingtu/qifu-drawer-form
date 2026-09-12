# 智客星列表页底图协议

## 适用范围

正式抽屉交付默认启用本协议：先生成完整 `1366×768` 页面打开态，再把右侧抽屉放在底图和蒙层之上。本协议不是新的抽屉组合；抽屉仍从 `drawer-compositions.md` 选择 `compositionName`。

`STANDALONE_DEBUG` 仅用于用户明确要求“内部调试抽屉本体/不交付”时检查抽屉结构，不能作为正式交付结果。

## 输入

```text
presentationMode  DRAWER_OPEN_WITH_BACKGROUND(默认) | OVERLAY_ON_ZHIKEXING_LIST(智客星兼容别名) | STANDALONE_DEBUG
background
  source          AUTO(默认) | TEMPLATE | EXISTING_LIST_PAGE | STRUCTURE_PREVIEW
  sourceNode      EXISTING_LIST_PAGE 时必填
  sidePath[]      仅控制底图中已有菜单的展开与选中
  pageName        底图业务页名称；仅用于 Scene 命名
```

- `TEMPLATE`：按 `qifu-list-page` 的 `platform=zhikexing / generationStrategy=copyTemplate` 复制人工基线 `4892:34812`，即 `Template / List Page / 智客星 / 1440 / 手动调整`，真实尺寸必须为 `1366 x 768`。
- `EXISTING_LIST_PAGE`：复制用户明确提供的已完成智客星列表页；创建前必须验证其为 `1366 x 768`，并通过 `qifu-list-page` 的智客星结构化验收。
- `AUTO`：优先使用用户明确提供且已验收的智客星 `EXISTING_LIST_PAGE`，其次复制上述 `TEMPLATE`；两者都不可用时使用中性 `STRUCTURE_PREVIEW + Overlay Mask + Drawer`。不得退回裸抽屉、临时手绘底图或借用其他平台菜单。
- 用户显式指定 `TEMPLATE` 或 `EXISTING_LIST_PAGE` 且该来源不可解析时，返回 `BACKGROUND_TEMPLATE_MISSING`，不得静默改用另一来源。

## 读取与边界

启用前必须完整读取 `../../qifu-shared/references/platform-zhikexing.md`。如果本地同时安装了 `qifu-list-page`，再读取该 Skill 的 `SKILL.md`、`references/component-invocation-contract.md` 和 `references/structural-validation.md`；独立安装抽屉 Skill 时，不把 `qifu-list-page` 作为强制依赖。

> `zhikexing-list-page` 已于 2026-09-11 归档为历史兼容入口，`references/` 已删除；底图协议不再依赖该目录。

不得写入列表页组件的 `pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`rowsSlot`、`cellsSlot` 或 `paginationSlot`。底图业务内容需要调整时，先按 `qifu-list-page platform=zhikexing` 单独生成并验收，再用 `EXISTING_LIST_PAGE` 引用它。

## 场景结构

```text
Scene / Drawer / <pageName> / <drawerTitle>       1366 x 768, clip content=true
├── Background / <Platform> List Page | Structure Preview
│                                                   1366 x 768, whole-frame clone or neutral structure preview
├── Overlay Mask                                  1366 x 768, semantic overlay variable
└── Drawer / <object> / <action>                  right aligned, width=DrawerSpec.widthTier
```

- Scene、Background、Overlay Mask、Drawer 使用整数几何；只有这四个页面级节点允许绝对定位。
- `EXISTING_LIST_PAGE` / `TEMPLATE` 的 Background 必须保留整页真实组件实例、文字样式、变量与 Slot 内容关系；禁止截图、展平、分离实例或改变其尺寸。
- `STRUCTURE_PREVIEW` 的 Background 只表达 Header、导航、筛选、表格和分页的布局边界；不得伪装为智客星正式列表页、使用业务数据或借用其他平台菜单。
- Overlay Mask 必须覆盖完整 `1366 x 768` Scene，位于 Background 与 Drawer 之间；填充绑定组件库已经存在的语义遮罩变量。变量不可解析时返回 `STYLE_MISSING`，不得手填透明黑色。
- Drawer 必须贴 Scene 右侧、上下贴边，层级始终高于 Overlay Mask；`maskClosable` 与 `escClosable` 仍由 DrawerSpec 控制，默认均为 `false`。

## 验收

正式打开态额外通过以下检查：

1. Scene、Background、Overlay Mask 均为 `1366 x 768`，Drawer 的右边和 Scene 右边相等。
2. 图层顺序严格为 `Background < Overlay Mask < Drawer`；蒙层不遮挡抽屉。
3. `EXISTING_LIST_PAGE` / `TEMPLATE` 的 Background：Header=48px、SideNavigation=200px，且仍可见唯一当前叶子菜单与品牌色选中图标。
4. `EXISTING_LIST_PAGE` / `TEMPLATE` 的 Background 中仍存在 List Page Shell-V2、Filter Bar-V2、Table Shell-V2、Pagination-V2；无 `Navigation Text Overlay`、裸 Text 或截图替代物。
5. `STRUCTURE_PREVIEW` 的 Background 至少可见 Header、导航区、筛选区、表格区和分页区边界；不要求、也不得冒充正式列表页组件实例。
6. 截图检查能同时看见被蒙层压暗的底图和清晰的右侧 Drawer；无溢出、截断或小数几何。

## 调用示例

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“查看加微方式”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。
展示方式：完整页面打开态；底图使用智客星列表页模板；
当前菜单：客户添加 / 加微方式；抽屉标题：加微方式详情；宽度：680。
```
