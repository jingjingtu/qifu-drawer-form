# Portable Kit 模式

## 适用场景

当协作者没有「奇富科技中后台组件库 新」的 Library 访问权限,但需要继续使用同一套组件结构与视觉规范时,使用 `PORTABLE_KIT`。Portable Kit 是复制到当前目标文件的本地组件,不是远程 Library,不会接收原库更新。

## 交付 Portable Kit

优先从组件库源文件创建一个副本,命名为 `奇富科技中后台组件库 - Portable Kit`,删除不需要分享的业务页面,保留组件集、Variants、嵌套组件、变量和文字样式。不要把截图或已分离的图层当作 Portable Kit。

数据详情抽屉至少保留:

- `通知反馈 / Drawer / Header`
- `Icon/basic/close`
- `Data Display / Tag / Tag`
- `录入组件 / Select / Base`
- `Data Display / Table / Shell-V2`
- `Data Display / Table / Header Cell-V2`
- `Data Display / Table / Row-V2`
- `Data Display / Table / Content Cell-V2`
- `Data Display / Table / Cell Content / Text-V2`
- `Navigation / Pagination / Pagination-V2`
- `Body/Regular`、`标题/Medium`、`标题/Small` 与所需颜色/间距/圆角变量

分享时允许对方复制文件到 Draft。最稳定的消费方式是在 Portable Kit 副本中直接生成;若必须在已有业务文件中生成,先把上述本地主组件/组件集复制到业务文件,再运行 Skill。

## 运行前预检

`PORTABLE_KIT` 不使用发布 Key,必须使用本地组件名称查找:

1. 调用 `figma.getLocalComponentsAsync()`;
2. 按 `portable-component-manifest.json` 的 `name` 精确匹配 `COMPONENT` / `COMPONENT_SET`;
3. 检查所有 `required=true` 项和需要的 Variant 名称;
4. 检查所需文字样式和 PingFang SC 字体可用;
5. 创建一个测试实例,确认 `type=INSTANCE` 且 `mainComponent` 属于当前文件;
6. 任一项失败时返回 `PORTABLE_COMPONENT_MISSING` 或 `STYLE_MISSING`,不要开始创建业务 Frame。

## 与正式 Library 的区别

| 项目 | REAL_COMPONENT_ONLY | PORTABLE_KIT |
| --- | --- | --- |
| 组件来源 | 已启用的发布 Library | 当前文件本地组件 |
| 查找方式 | published key / 组件映射 | 精确名称 / 本地组件 API |
| 主组件关系 | 远程 Library 主组件 | 当前文件本地主组件 |
| 组件更新 | 可接收 Library 更新 | 不会自动同步 |
| 缺失行为 | 停止并返回 COMPONENT_LIBRARY_UNAVAILABLE | 停止并返回 PORTABLE_COMPONENT_MISSING |

## 禁止事项

- 不把 Portable Kit 的本地组件描述成正式 Library 实例;
- 不使用原 Library 的发布 Key 作为 Portable Kit 唯一查找依据;
- 不在预检失败后静默切换到 `VISUAL_FALLBACK`;
- 不为补齐缺失组件而 detach、重画或修改组件母版;
- 不把 Portable Kit 中的 README、审计文字或截图当作业务组件。
