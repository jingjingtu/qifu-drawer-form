# 奇富抽屉表单 Skill 协作说明

## 仓库用途

本仓库用于分发 `qifu-drawer-form` Skill，使具备相同 Figma 组件库权限的协作者，可以根据业务提示词生成结构、组件与视觉规则一致的奇富中后台抽屉表单。

- 组件库文件：<https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/奇富科技中后台组件库-新>
- 试生成统一目标 Page：`测试`，node `3497:651`
- 核心 Skill：`skills/qifu-drawer-form/SKILL.md`

## 每次生成前

完整读取 `skills/qifu-drawer-form/SKILL.md`，并根据场景继续读取页面蓝图、组合注册表、字段控件映射和相关 Golden Sample。使用 Figma 写入工具前，加载该工具要求的官方 Figma Skill。

## 目标位置

- 试生成、效果验证和 Skill 回归统一放入既有 Page `测试`。
- 用户明确指定正式交付 Page 时，以用户要求为准。
- 不覆盖已有画板；新画板放入不重叠的空白区域。

## 组件规则

- 优先使用组件库真实组件实例与已发布组件。
- 不分离实例后重画，不用截图冒充可编辑页面。
- 同文件按节点或精确名称定位；跨文件按发布 Key 导入。
- 发现缺口时记录 `COMPONENT_MISSING` 或 `COMPONENT_SOURCE_GAP`，不得声称缺失能力已存在。
- 未获得明确授权时，不修改或发布组件库母版。

## 验证要求

- 逐区截图检查，再检查整张画板。
- 验证组件实例、Slot、Auto Layout、文本样式、间距、尺寸、表格、分页与示例数据。
- 检查孤儿实例、重复节点、小数几何、文字截断、节点重叠和画板溢出。
- 完成时返回画板名称、节点 ID、组合名称、主要组件、假设、缺口和验证结果。

## 安全

- 不提交 Figma Access Token、GitHub Token、Cookie、密码或个人凭证。
- 公开仓库中的 Figma 地址、节点 ID 和发布 Key 只用于定位资产，不代表授权。
