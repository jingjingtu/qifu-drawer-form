# Qifu Drawer Form

奇富科技中后台 Figma 右侧抽屉生成 Skill。根据业务描述、字段清单、截图或线框，使用真实组件实例生成可编辑、可回读、可验收的抽屉打开态；也可以把同一个抽屉批量适配到多个平台并生成对比稿。

> 当前版本：`qifu-drawer-form 1.5.0`，共享依赖 `qifu-shared 1.2.0`。

本仓库是 Codex / Claude Code Skill 安装仓库，不是带 `.codex-plugin/plugin.json` 的 Codex Plugin。仓库由私有主仓库 `jingjingtu/qifu-skills` 单向生成，`skills/qifu-drawer-form` 和 `skills/qifu-shared` 不在本仓库单独维护。

## 能做什么

- 生成新建、编辑、查看、只读和数据详情右侧抽屉。
- 使用「奇富科技中后台组件库 新」中的真实组件实例、Text Style 和 Figma Variables。
- 生成完整 `1366×768` 打开态：平台背景、蒙层、右侧抽屉。
- 根据确定性信号识别智客星、毓数、智能运营平台和奇富通用后台。
- 复用同一份字段结构，一次生成多个平台版本。
- 对平台、主题、组件实例、字段结构和视觉结果进行回读验收。

不适合向导、批量编辑列表、复杂看板或高度定制工作台。

## 工作方式

```text
业务字段与抽屉结构（baseDrawer）
                │
                ├── 智客星 Adapter ── 智客星背景 + 绿色主题
                ├── 毓数 Adapter   ── 毓数导航 + 绿色主题
                └── 智能运营 Adapter ── 智能运营背景 + 蓝色主题
```

多平台模式只解析一次公共字段。平台切换不会改变字段数量、顺序、控件类型、抽屉宽度和 Footer；只允许切换平台背景、导航、平台词和主题变量。

## 当前平台注册情况

| 平台 | `platformKey` | 默认主题 | 平台外壳能力 |
| --- | --- | --- | --- |
| 智客星 | `zhikexing` | `zhikexing-green` | 已登记完整模板，可生成正式平台打开态 |
| 毓数 | `yushu` | `yushu-green` | 已登记导航 Adapter，可使用真实组件组装 |
| 智能运营平台 | `zhineng-yunying` | `smartops-blue` | 有蓝色主题和抽屉基线；需提供已验收列表页才能成为正式平台打开态 |
| 奇富通用后台 | `qifu-generic` | `yushu-green` | 中性结构，不虚构平台菜单和 Logo |

智能运营平台没有真实背景来源时，会生成 `STRUCTURE_PREVIEW` 并标记 `PREVIEW_ONLY`，不会借用其他平台背景冒充正式结果。

## 使用前提

1. 使用支持 Figma Connector / `use_figma` 的 Codex 或 Claude Code。
2. 在客户端中连接自己的 Figma 账号。
3. 对目标 Figma 文件拥有编辑权限。
4. 对「奇富科技中后台组件库 新」拥有访问权限。
5. 正式交付默认使用 `REAL_COMPONENT_ONLY`；组件或变量不可解析时会停止，不会偷偷改成矩形和文字。

GitHub 仓库不包含 Figma 登录状态、访问令牌或组件库授权。

## 安装到 Codex

同时安装 `qifu-drawer-form` 和 `qifu-shared`，不能只安装抽屉目录：

```bash
git clone https://github.com/jingjingtu/qifu-drawer-form.git ~/Documents/qifu-drawer-form
mkdir -p ~/.codex/skills
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-shared ~/.codex/skills/qifu-shared
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-drawer-form ~/.codex/skills/qifu-drawer-form
```

安装后新开一个 Codex 任务，让客户端重新发现 Skill。可以显式输入 `$qifu-drawer-form`，也可以直接描述“使用 qifu-drawer-form 在 Figma 中生成抽屉”。

## 安装到 Claude Code

```bash
mkdir -p ~/.claude/skills
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-shared ~/.claude/skills/qifu-shared
ln -sfn ~/Documents/qifu-drawer-form/skills/qifu-drawer-form ~/.claude/skills/qifu-drawer-form
```

## 第一次使用

准备三项信息：

- 目标 Figma 文件或节点链接。
- 已存在的目标 Page 名称或 ID。
- 抽屉字段、操作类型和目标平台。

推荐明确写出目标 Page 和落点。Skill 不会默认写入第一个 Page，也不会创建名字相近的新 Page。

### 最简提示词

```text
使用 $qifu-drawer-form，并调用 @figma，在下面 Figma 文件的“测试”Page 空白处生成“新增策略”右侧抽屉：
<Figma 文件或节点链接>

平台：智客星。
字段：策略名称 Input 必填；有效期 DateRange 必填；策略类型 Select 必填；备注 Textarea 选填。
底部按钮：取消、确定。
使用真实组件实例，完成后返回节点 ID、结构验证和视觉验证结果。
```

## 单平台生成

下面的模板适合新建、编辑和查看抽屉。替换 `<...>`，没有的分区直接删除。

```text
使用 $qifu-drawer-form，并调用 @figma，在 <目标 Figma 文件或节点链接> 的 <目标 Page> 中 <指定落点> 生成“<新建 / 编辑 / 查看><业务对象>”右侧抽屉。
不要新建 Figma Page，不要覆盖已有画板。

generationMode：SINGLE
页面平台：<智客星 / 毓数 / 智能运营平台 / 奇富通用后台>
platformKey：<zhikexing / yushu / zhineng-yunying / qifu-generic>
themeKey：<不填自动采用平台默认主题 / zhikexing-green / yushu-green / smartops-blue>
componentMode：REAL_COMPONENT_ONLY
compositionName：<不填自动判断 / Qifu Drawer Form / Sectioned Create>
widthTier：<480 / 640 / 680 / 840 / 960，普通表单默认 640>
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：<AUTO / TEMPLATE / EXISTING_LIST_PAGE / STRUCTURE_PREVIEW>
<使用已验收列表页时> background.sourceNode：<节点 ID>

分区：
- <基础信息>：<字段名> <控件> <必填/选填>；<字段名> <控件> <必填/选填>。
- <业务配置>：<字段名> <控件> <必填/选填>；<字段名> <控件> <必填/选填>。

<编辑场景> 默认值：<字段名>=<值>。
Footer：<取消/关闭>、<确定/保存>。

使用真实组件实例和组件库 Text Style。完成后返回 platformKey、themeKey、背景来源、组件解析、节点 ID、structuralValidation 和 visualValidation。
```

### 单平台完整示例：智能运营平台

```text
使用 $qifu-drawer-form，并调用 @figma，在 <Figma 文件链接> 的“测试”Page 空白处生成“新增短信模板策略”右侧抽屉。
不要新建 Figma Page，不要覆盖已有画板。

generationMode：SINGLE
页面平台：智能运营平台
platformKey：zhineng-yunying
themeKey：smartops-blue
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：680
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：AUTO

分区：
- 基础信息：策略名称 Input 必填；有效期 DateRange 必填。
- 策略配置：主模板 Select 必填，选择后展示模板明细表；关联运营策略 Multiple Select 必填，已选项显示可关闭 Tag，选择后展示策略明细表；灰度比例 Select 必填，选项“10%/30%/50%/100%”，默认“100%”。

Footer：关闭、保存。
使用“智能运营平台策略关联抽屉 Golden Sample”。如果没有已验收的智能运营平台列表页，允许使用 STRUCTURE_PREVIEW，但必须标记 PREVIEW_ONLY。
完成后返回节点 ID、主题变量回读、structuralValidation 和 visualValidation。
```

## 多平台批量生成

用户说“复用到多个平台”“生成多平台对比稿”，或一次给出两个以上已注册平台时，会进入 `MULTI_PLATFORM_COMPARE`。

推荐提示词：

```text
使用 $qifu-drawer-form，并调用 @figma，把同一个“新增策略”抽屉生成到智客星、毓数和智能运营平台，放在 <目标 Figma 文件链接> 的 <目标 Page> 空白处，生成一个多平台对比组。
不要新建 Figma Page，不要覆盖已有画板。

generationMode：MULTI_PLATFORM_COMPARE
baseDrawer：
- operation：create
- compositionName：Qifu Drawer Form / Sectioned Create
- widthTier：640
- 基础信息：策略名称 Input 必填；有效期 DateRange 必填。
- 策略配置：策略类型 Select 必填；备注 Textarea 选填。
- Footer：取消、确定。

targets：
- 智客星：platformKey=zhikexing，themeKey 自动，background.source=AUTO。
- 毓数：platformKey=yushu，themeKey 自动，background.source=AUTO。
- 智能运营平台：platformKey=zhineng-yunying，themeKey 自动，background.source=AUTO；没有已验收正式背景时允许 STRUCTURE_PREVIEW，并标记 PREVIEW_ONLY。

comparisonLayout：HORIZONTAL
failurePolicy：ALL_OR_NOTHING
componentMode：REAL_COMPONENT_ONLY

三个版本必须共用同一个 contentFingerprint。不得改变不同平台之间的字段数量、顺序、控件类型、抽屉宽度和 Footer；只允许平台背景、导航、平台词和主题变量不同。
完成后返回每个平台的 detectedBy、adapter、themeKey、backgroundSource、shellStatus、节点 ID、结构/视觉验证，以及 crossPlatformConsistency 和 batchValidation。
```

平台超过三个时，可以改为：

```text
comparisonLayout：GRID
```

默认 `failurePolicy=ALL_OR_NOTHING`：所有平台先通过预检才开始生成。只有明确允许部分交付时，才使用：

```text
failurePolicy：CONTINUE_WITH_REPORT
```

此时失败平台不会被其他平台背景或近似主题替代，最终状态为 `PARTIAL`。

## 平台如何自动识别

识别优先级：

1. 提示词明确提供的 `platformKey`。
2. 明确平台注册名或别名，例如“智客星”“毓数”“智能运营平台”。
3. 已验收背景的精确模板节点 ID 或完整节点名称。
4. 目标文件中唯一命中的 Figma Variable mode 或平台壳组件。

Skill 不会根据“看起来是绿色”、Logo 相似或截图观感猜测平台。信号冲突时会返回 `CONFLICT`；没有确定性信号时返回 `UNRESOLVED`，需要补充平台信息。

如果希望稳定复现，推荐始终显式填写 `platformKey`。

## 字段怎么描述

字段使用“字段名 + 控件 + 必填/选填 + 默认值/选项/说明”的格式：

| 业务字段 | 提示词示例 |
| --- | --- |
| 短文本 | `策略名称 Input 必填，placeholder“请输入策略名称”` |
| 单选下拉 | `策略类型 Select 必填，选项“自动/手动”` |
| 多选下拉 | `关联策略 Multiple Select 必填，已选项显示可关闭 Tag` |
| 单选 | `触达方式 Radio.Group 必填，选项“短信/企微”` |
| 日期范围 | `有效期 DateRange 必填` |
| 长文本 | `备注 Textarea 选填，rows=4` |
| 开关 | `是否启用 Switch 必填，默认开启` |
| 复合业务区 | `超频规则 Custom(OverFrequencyRule) 必填` |

## 组件模式

| 模式 | 用途 | 缺失组件时 |
| --- | --- | --- |
| `REAL_COMPONENT_ONLY` | 正式交付，默认模式 | 停止并报告，不自动降级 |
| `PORTABLE_KIT` | 目标文件中已经放入本地 Portable 组件 | 缺少精确组件时停止 |
| `VISUAL_FALLBACK` | 只做视觉预览，必须由用户明确选择 | 使用 `Fallback / <Capability>` 命名并返回审计结果 |

参考截图只用于识别结构和比例，不会作为图片放进最终画板。

## 应该得到什么结果

单平台完成后至少返回：

```text
nodeId
platformKey / platformName
themeKey / themePrimary
backgroundSource
componentResolution
textStyleResolution
structuralValidation=PASS|BLOCKED|FAIL
visualValidation=PASS|BLOCKED|FAIL
```

多平台完成后还会返回：

```text
contentFingerprint=sha256:<...>
crossPlatformConsistency=PASS|FAIL
batchValidation=PASS|PARTIAL|BLOCKED|FAIL
targets[].detectedBy
targets[].shellStatus=FORMAL|PREVIEW_ONLY
```

只有结构和视觉都为 `PASS` 才算正式完成。多平台还要求所有目标内容指纹一致。

## 常见阻塞

| 状态或错误 | 含义 | 怎么处理 |
| --- | --- | --- |
| `UNRESOLVED` | 无法确定平台 | 补充 `platformKey` 或明确平台名称 |
| `CONFLICT` | 提示词平台与目标模板不一致 | 确认应该使用哪个平台或更换背景节点 |
| `THEME_VARIABLE_MISSING` | 主题变量无法绑定 | 在目标文件启用正确变量，或检查平台注册主题 |
| `COMPONENT_SOURCE_GAP` | 组件母版未暴露所需属性 | 修复组件库母版；不要 detach 实例 |
| `BLOCKED_TEMPLATE` | 平台模板无法支持要求的结构 | 提供匹配模板或已验收列表页节点 |
| `PREVIEW_ONLY` | 抽屉可验收，但平台背景只是中性结构预览 | 提供该平台已验收列表页节点 |

同一失败原因只进行一次确定性替代尝试；再次失败会停止并报告，不会反复循环。

## 更新

```bash
cd ~/Documents/qifu-drawer-form
git pull
python3 scripts/validate_release.py
```

使用软链安装时不需要重新创建软链。更新后建议新开一个 Codex 或 Claude Code 任务。

## 仓库验证

```bash
python3 scripts/validate_release.py
python3 -m unittest discover -s skills/qifu-drawer-form/tests -v
```

发布清单 [RELEASE_MANIFEST.json](RELEASE_MANIFEST.json) 记录源提交、包版本和所有发布文件哈希。

更多实现细节：

- [抽屉 Skill 入口](skills/qifu-drawer-form/SKILL.md)
- [抽屉详细案例与字段说明](skills/qifu-drawer-form/README.md)
- [多平台批量生成协议](skills/qifu-drawer-form/references/multi-platform-batch.md)
- [平台注册表](skills/qifu-shared/references/platform-registry.json)
- [主题注册表](skills/qifu-shared/theme/theme-registry.json)

本仓库未声明开源许可证；公开可读不等于授权复制、修改或再分发。
