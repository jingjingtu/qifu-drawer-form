# 已知限制与迁移记录

按时间倒序记录。普通抽屉生成不读取；仅在诊断历史回归或维护 Skill 时使用。仓库内回填方式见 `_docs/limit-backfill.md`。

## 2026-09-12 · 多平台批量对比

- 新增 `MULTI_PLATFORM_COMPARE`：公共 `baseDrawer` 只解析一次，以内容指纹约束各平台字段、控件、顺序、宽度和 Footer 一致。
- 平台识别改为读取 `qifu-shared/references/platform-registry.json` 的确定性信号；不根据颜色、Logo 相似度或截图观感猜测平台。
- 主题切换读取 `qifu-shared/theme/theme-registry.json`；`mode/green` 与 `mode/blue` 是颜色变量路径分组，不是 Figma mode。
- 智客星和毓数已有正式外壳路径；智能运营平台仅在提供已验收列表页时为正式打开态，否则保留 `PREVIEW_ONLY`。
- 批量模式默认全目标预检与 `ALL_OR_NOTHING`，同一失败原因只允许一次确定性替代尝试，避免循环降级。

## 2026-08-25 · 平台、主题与打开态底图

- 平台切换统一走 `platformKey`；主题切换统一走 `themeKey / themePrimary`，主题只改语义颜色，不改结构。
- 智能运营平台专属导航和模板尚未补齐；没有已验收底图时使用中性 `STRUCTURE_PREVIEW`，不能标记为正式平台页面。
- `background.source=AUTO` 依次尝试已验收列表页、平台模板、中性结构预览；不生成裸抽屉。
- 页面级文字必须绑定组件库 Text Style；组件内部缺口回到母版修复。

## 2026-08-21 · 数据详情抽屉

- Golden Sample：组件库 Page `02 From 训练过程`，节点 `4725:1548`；旧节点 `4659:420` 只作历史对照。
- 原样例 IMAGE 底图不是正式交付底图；需替换为完整真实列表页。
- 当前组件库 `标题/Medium` 为 16/24；使用真实样式，不手工覆盖行高。
- `Text-V2` 14px 正文继承 `Body/Regular` 14/22。其他组件内部 Text Style 缺口记录为 `COMPONENT_SOURCE_GAP`。
- 页面级几何使用整数；不为修正母版内部小数而 detach。

## 2026-08-12 · 层级与重复节点

- 控件实例必须归属于 Header、Section 或 Footer，不允许 Page 根级孤儿。
- 抽屉内不允许保留与正式实例重叠的重复节点。
- 外部清理插件只用于历史修复，不是正常生成依赖，也不能把清理成功视为结构验收通过。

## 2026-08-20 · 旧 builder 合并

- `qifu-figma-drawer-builder` 已并入本 Skill，不再作为运行入口。
- 不继承旧 builder 的 1440 根画板、双画板默认值和旧组合名。
- 新偏差优先修正验证契约或组件映射，不新增第二个抽屉生成 Skill。
