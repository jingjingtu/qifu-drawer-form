# 智客星列表页底图协议

## 适用范围

正式抽屉交付默认启用本协议：先生成完整 `1366×768` 页面打开态，再把右侧抽屉放在底图和蒙层之上。本协议不是新的抽屉组合；抽屉仍从 `drawer-compositions.md` 选择 `compositionName`。

`STANDALONE_DEBUG` 仅用于用户明确要求“内部调试抽屉本体/不交付”时检查抽屉结构，不能作为正式交付结果。

## 输入

```text
presentationMode  DRAWER_OPEN_WITH_BACKGROUND(默认) | OVERLAY_ON_ZHIKEXING_LIST(智客星兼容别名) | STANDALONE_DEBUG
background
  source          TEMPLATE(智客星默认) | EXISTING_LIST_PAGE
  sourceNode      EXISTING_LIST_PAGE 时必填
  sidePath[]      仅控制底图中已有菜单的展开与选中
  pageName        底图业务页名称；仅用于 Scene 命名
```

- `TEMPLATE`：复制 `zhikexing-list-page` 的人工基线 `4892:34812`，即 `Template / List Page / 智客星 / 1440 / 手动调整`，真实尺寸必须为 `1366 x 768`。
- `EXISTING_LIST_PAGE`：复制用户明确提供的已完成智客星列表页；创建前必须验证其为 `1366 x 768`，并通过 `zhikexing-list-page` 的结构化验收。
- 智客星未提供 `background` 时，`TEMPLATE` 为默认来源；若模板不可解析，返回 `BACKGROUND_TEMPLATE_MISSING`，不得临时手绘底图。
- 非智客星平台未提供已批准平台模板或 `EXISTING_LIST_PAGE` 时，返回 `BACKGROUND_TEMPLATE_MISSING`；不得退回裸抽屉，也不得借用其他平台菜单冒充。

## 读取与边界

启用前必须完整读取：

- `../zhikexing-list-page/SKILL.md`
- `../zhikexing-list-page/references/platform-zhikexing.md`
- `../zhikexing-list-page/references/component-invocation-contract.md`
- `../zhikexing-list-page/references/structural-validation.md`

不得写入列表页组件的 `pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`rowsSlot`、`cellsSlot` 或 `paginationSlot`。底图业务内容需要调整时，先按 `zhikexing-list-page` 单独生成并验收，再用 `EXISTING_LIST_PAGE` 引用它。

## 场景结构

```text
Scene / Drawer / <pageName> / <drawerTitle>       1366 x 768, clip content=true
├── Background / <Platform> List Page             1366 x 768, whole-frame clone
├── Overlay Mask                                  1366 x 768, semantic overlay variable
└── Drawer / <object> / <action>                  right aligned, width=DrawerSpec.widthTier
```

- Scene、Background、Overlay Mask、Drawer 使用整数几何；只有这四个页面级节点允许绝对定位。
- Background 必须保留整页真实组件实例、文字样式、变量与 Slot 内容关系；禁止截图、展平、分离实例或改变其尺寸。
- Overlay Mask 必须覆盖完整 `1366 x 768` Scene，位于 Background 与 Drawer 之间；填充绑定组件库已经存在的语义遮罩变量。变量不可解析时返回 `STYLE_MISSING`，不得手填透明黑色。
- Drawer 必须贴 Scene 右侧、上下贴边，层级始终高于 Overlay Mask；`maskClosable` 与 `escClosable` 仍由 DrawerSpec 控制，默认均为 `false`。

## 验收

正式打开态额外通过以下检查：

1. Scene、Background、Overlay Mask 均为 `1366 x 768`，Drawer 的右边和 Scene 右边相等。
2. 图层顺序严格为 `Background < Overlay Mask < Drawer`；蒙层不遮挡抽屉。
3. Background 的 Header=48px、SideNavigation=200px，且仍可见唯一当前叶子菜单与品牌色选中图标。
4. Background 中仍存在 List Page Shell-V2、Filter Bar-V2、Table Shell-V2、Pagination-V2；无 `Navigation Text Overlay`、裸 Text 或截图替代物。
5. 截图检查能同时看见被蒙层压暗的底图和清晰的右侧 Drawer；无溢出、截断或小数几何。

## 调用示例

```text
使用 qifu-drawer-form 和 zhikexing-list-page，在智客星平台查看加微方式。
展示方式：完整页面打开态；底图使用智客星列表页模板；
当前菜单：客户添加 / 加微方式；抽屉标题：加微方式详情；宽度：680。
```
