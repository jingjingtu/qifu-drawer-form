# Qifu Drawer Form 发布仓库

本仓库是 `jingjingtu/qifu-skills` 的单向发布镜像。

## 使用 Skill

执行抽屉任务时，先完整读取：

- `skills/qifu-drawer-form/SKILL.md`
- 该文件按场景指定的 `references/`
- `skills/qifu-shared/` 中被抽屉 Skill 引用的共享组件、平台和主题资料

正式交付遵循抽屉 Skill 的组件实例、结构化验收和视觉验收要求；未获得明确授权时，不修改或发布 Figma 组件库母版。

## 维护边界

- 不直接编辑 `skills/qifu-drawer-form` 或 `skills/qifu-shared`；改动回到主仓库完成。
- 不手工复制单个共享文件，不在抽屉目录重新建立 `component-map.md` 或平台基线副本。
- 不提交 Figma Access Token、GitHub Token、Cookie、密码或个人凭证。
- 发布后运行 `python3 scripts/validate_release.py`，并确认 `RELEASE_MANIFEST.json` 与当前文件一致。
