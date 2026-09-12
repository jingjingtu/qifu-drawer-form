# Qifu Drawer Form

奇富科技中后台 Figma 右侧抽屉生成 Skill 的独立安装仓库。

本仓库由私有主仓库 `jingjingtu/qifu-skills` 单向生成。`skills/qifu-drawer-form` 和 `skills/qifu-shared` 是同步产物；请不要在这里单独修改这两个目录，否则下一次发布会覆盖这些改动。

## 包含内容

- `qifu-drawer-form`：新建、编辑、查看和数据详情右侧抽屉工作流。
- `qifu-shared`：组件映射、页面上下文、平台适配器和主题 Tokens，是抽屉 Skill 的必需依赖。
- `RELEASE_MANIFEST.json`：源提交、包版本和发布文件哈希。

## 安装到 Codex

```bash
git clone https://github.com/jingjingtu/qifu-drawer-form.git ~/Documents/qifu-drawer-form
mkdir -p ~/.codex/skills
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-shared ~/.codex/skills/qifu-shared
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-drawer-form ~/.codex/skills/qifu-drawer-form
```

安装完成后新开一个 Codex 任务，使用 `$qifu-drawer-form`。更新时在仓库目录运行 `git pull`，无需重新创建软链。

## 安装到 Claude Code

```bash
mkdir -p ~/.claude/skills
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-shared ~/.claude/skills/qifu-shared
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-drawer-form ~/.claude/skills/qifu-drawer-form
```

## 使用前提

使用者需要连接自己的 Figma 账号，并拥有目标业务文件和「奇富科技中后台组件库 新」的访问权限。仓库不包含 Figma 登录状态、访问令牌或组件库授权。

完整提示词、案例和验收说明见 [抽屉 Skill README](skills/qifu-drawer-form/README.md)。

## 验证

```bash
python3 scripts/validate_release.py
python3 skills/qifu-drawer-form/scripts/validate_portable_manifest.py
```

本仓库未声明开源许可证；公开可读不等于授权复制、修改或再分发。
