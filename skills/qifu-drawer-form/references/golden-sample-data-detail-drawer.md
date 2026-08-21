# 数据详情抽屉 Golden Sample

## 适用范围

用于右侧数据详情抽屉：顶部展示对象摘要，下方以筛选控件和内嵌表格展示明细。稳定组合名称：

`Qifu Drawer Form / Data Detail with Table`

Golden Sample：组件库文件 `gTV3VdC6a5e9vpkRHIZSXA`，Page `3932:405`，人工精修源 Frame `4659:420`。自动生成验证 Frame 为 `4725:1548`，用于检查组件引用、Auto Layout、整数几何和表格边框实现。参考其信息层级和节奏，不复制固定业务文案。

## 组件覆盖

必须先在同文件按精确名称解析，并保留 `mainComponent`：

- `Icon/basic/close`
- `Data Display / Tag / Tag`
- `录入组件 / Select / Base`
- `Data Display / Table / Shell-V2`
- `Data Display / Table / Header Cell-V2`
- `Data Display / Table / Row-V2`
- `Data Display / Table / Content Cell-V2`
- `Data Display / Table / Cell Content / Text-V2`
- `Navigation / Pagination / Pagination-V2`

缺失时返回 `COMPONENT_MISSING` 并停止对应区域，不自绘近似组件。页面级 Auto Layout、Section 容器、3×12 标题 rail 和 Table Border 属于组合结构，不冒充组件库母版。

## 结构

```text
Page / Drawer / <Object> / Golden Sample
├── Background Page
├── Overlay Mask
└── Drawer / <Object>                         680px
    ├── Drawer / Header                      680×56
    │   ├── Title                            x=24，标题/Medium
    │   └── INSTANCE / Icon/basic/close      16×16，right=24
    └── Drawer / Body                        padding=16，Vertical
        └── Content Stack                    width=648，gap=16，Vertical
            ├── Section / Summary            padding=20 24，gap=16
            │   ├── Section Heading Row      Horizontal
            │   │   ├── Heading Group        rail 3×12 + 标题/Small，gap=5
            │   │   └── Tag                  与 Heading Group gap=8
            │   └── Body/Regular
            └── Section / Detail             padding=20 24，gap=16
                ├── Section Heading Row      rail 3×12 + 标题/Small
                ├── Form Row                 label + Select，gap=24
                └── Table Region             Vertical
                    ├── Table Border          仅表头+数据行
                    └── Pagination-V2         描边外，右对齐
```

所有结构容器使用 Auto Layout；仅顶层页面、遮罩与右侧抽屉定位允许绝对坐标。

## 尺寸与间距

- 本组合抽屉宽 680px；未来按内容梯度调整时必须使用已注册档位，不能任意缩放实例。
- Header 高 56px。Title 左 24px、上下 16px；Close 16×16，右 24px并垂直居中。
- Body 内容距抽屉四周 16px。不要叠加旧的 24/32 padding。
- 内容卡片宽 648px，圆角 4；上下 padding 20px、左右 24px；卡片间 gap 16px。
- 卡片标题与正文/控件/表格区域纵向 gap 16px，内容增加时由 Auto Layout 自动撑高。
- 标题 rail 为 3×12，使用品牌色变量；rail 与标题 gap 5px。
- 标题后 Tag 的 gap 绑定 `--qifu-size/8`（Variable `--qifu-size/8`）。Tag 必须使用未缩放的真实实例。
- Form label 与控件默认 gap 24px。label 左对齐；同一 Section 内控件左边缘对齐。标签超过四字时统一扩大 label 列宽，不单独挤压某一行。
- 内嵌表格使用 small 36px 规格；表格和分页器都不得超出卡片 600px 内容宽。
- 全局几何值只允许整数。任何 Instance 被 scale 后产生小数尺寸，必须换成源 Component 的新实例，再设置合法变体与整数宽高。

## 文本样式

- Header Title：组件库 `标题/Medium`，当前真实定义 PingFang SC Semibold 16/24。
- Section Title：组件库 `标题/Small`，14/22。
- 普通正文与 Form label：组件库 `Body/Regular`，PingFang SC Regular 14/22。禁止使用 `Body/Medium`、Bold 或手填字体属性。
- 表头继续使用表格组件自身的 Semibold 层级；链接继续使用链接语义样式。不要为了统一正文而削弱标题、表头或链接的层级。
- 表格正文由 `Text-V2 / contentFont 内容字号=14px` 组件母版统一绑定 `Body/Regular` 14/22，所有数据单元格通过真实实例继承；禁止在页面实例内逐个覆盖字体或文本样式。
- 组件内部文本由组件母版样式管理，不直接覆盖字体。

页面级自由 Text 必须 100% 绑定组件库 Text Style。若 Tag、Select、Table、Pagination 等真实组件的母版内部 Text 当前没有 `textStyleId`，返回 `COMPONENT_SOURCE_GAP: <component> 内部文本未绑定 Text Style`；保持真实 Instance 和母版关联，不 detach、不在实例层手工覆盖字体。该缺口应回到组件母版修复，不由页面 Skill 伪造。

组件库当前没有独立的 16/20 Header 标题样式。若提示词写 16/20，返回 `STYLE_MISSING: 标题 16/20`，仍使用真实 `标题/Medium` 16/24；不得创建游离字体或手工改行高。

## 表格与分页

1. Table Shell-V2 使用 `small 小 36px / bordered 边框线 / selection off 隐藏`。
2. Header Cell-V2、Row-V2、Content Cell-V2 逐层同步 small + both divider；表头 `showSort=false`、`showFilter=false`，除非业务明确要求。
3. 自定义 Slot 内容遵守“先插入新内容，再按稳定名称删除默认内容”；不要缓存 Slot 动态 ID。
4. `Table Border / 四边完整` 是单独的页面级 Frame：圆角 4、1px Inside 描边、`Clip content=true`，描边颜色绑定组件库 divider 变量。
5. Table Border 只包围表头与数据行。Pagination-V2 位于其下方、边框之外并右对齐；不得把分页器包含在外边框中。
6. Table Shell 的默认 paginationSlot 需替换为空 Slot 内容或在 Table Border 内裁掉；页面只保留一个可见 Pagination-V2 实例。
7. Table Border 内不得裁掉表格内容；其高度精确等于 headerHeight + rowCount × rowHeight。分页器不计入该高度。
8. 非 Empty / Loading 状态下，每个可见数据行的每个可见单元格都必须有真实内容。不得用空字符串、Skeleton 或装饰线冒充已完成数据。
9. 表头列宽与数据行列宽必须逐列一致，所有列宽之和精确等于 Table Border 内容宽度；本 Golden Sample 为 `114 + 114 + 95 + 95 + 95 + 87 = 600px`。

## QA

- Drawer 宽 680，Header 56，Body/卡片/标题/Form/Table 全部整数几何。
- 页面级自由文本 100% 应用组件库 Text Style；无 `textStyleId=""` 的自由 Text。
- 页面级普通正文和 Form label 100% 使用 `Body/Regular` 14/22；出现 `Body/Medium` 或 Bold 即 FAIL。Header Title、Section Title、表头与链接按各自语义样式单独验收。
- `Text-V2 / contentFont 内容字号=14px` 的组件母版与全部可见表格正文实例均解析为 `Body/Regular` 14/22；任一实例脱离组件关系或单独覆盖即 FAIL。
- Header 只有 Title + `Icon/basic/close`；Close 是 16×16、right=24。
- 两张内容卡片均在 Body 16px 安全边距内，使用 Vertical Auto Layout。
- 每个 Section Heading 都是 `3×12 rail + 标题/Small` 的 Auto Layout；Tag gap=8 并绑定 `--qifu-size/8`。
- 表格所有可见单元格为真实组件 INSTANCE，表头和行列宽一致。
- 内容 Section 与 Table Border 均为 4px 圆角；Table Border 为 1px Inside、Clip=true，截图四个圆角没有内部直线伸出。
- 非空状态下所有可见数据行均为完整六列内容；表头与数据行逐列对齐，总宽无溢出。
- Pagination 位于 Table Border 外，仅一个可见实例。
- 无缩放小数、无孤儿实例、无重复节点、无文字截断、无越界。
