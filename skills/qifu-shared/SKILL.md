---
name: qifu-shared
description: >-
  Qifu 页面生成 Skill 的共享依赖包，提供列表页、详情页和抽屉表单所需的组件映射、组件调用基线、统一页面上下文、平台适配器与主题变量。安装任一 Qifu 页面 Skill 时一并安装；不用于单独生成页面或填写业务内容。
---

# Qifu Shared References

共享依赖包，不是独立页面生成工作流。

## Required companion skills

- `qifu-list-page`
- `qifu-detail-page`
- `qifu-drawer-form`

Keep this Skill installed beside those companion Skills. They resolve shared component maps, platform baselines, and theme variables from `../qifu-shared/`.

## Contents

- `references/component-map.md`: 组件名称、节点 ID、发布键、属性与已知缺口（仓库唯一权威；2026-09-11 起 `qifu-list-page` 不再保留副本）
- `references/component-invocation-baseline.md`: 跨页面共享的组件解析、写入回读与失败分类基线。
- `references/page-context.md`: 列表、详情、抽屉与编排入口共用的页面上下文。
- `references/platform-yushu.md`: 毓数导航基线。
- `references/platform-zhikexing.md`: 智客星列表页基线与 copyTemplate 策略（仓库唯一权威；2026-09-11 起 `qifu-list-page` 不再保留副本）。
- `references/platform-generic.md`: 通用 B 端平台适配器（`platform=generic` 时使用）。
- `theme/`: Figma 变量快照（`tokens.json` + `source/*.json` + `*.less`）。AI 先读 `tokens.json`，需要核对模式和值时读 `source/<collection>.json`。

## 版本

- 当前版本：`VERSION` 字段（2026-09-11 起新建）。
- `qifu-list-page` `references/component-map.md` 与 `references/platform-zhikexing.md` 已删除；任何页面 Skill 的文档契约不再单独维护这两份文件，校验脚本 `scripts/validate_skill_contract.py` 直接读 `../qifu-shared/references/`。
