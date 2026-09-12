# Qifu Theme / Figma Variables

本目录 **Figma Variables 是唯一的命名与值来源**。

- Figma 文件：[奇富科技中后台组件库-新](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/%E5%A5%87%E5%AF%8C%E7%A7%91%E6%8A%80%E4%B8%AD%E5%90%8E%E5%8F%B0%E7%BB%84%E4%BB%B6%E5%BA%93-%E6%96%B0?node-id=2874-9924&view=variables)
- 采集范围：`基础` 107、`色彩` 82、`字体` 27、`圆角` 7、`尺寸` 55，共 **278** 个变量。
- 原始数据：[`source/`](source/)；可供 AI 精确检索的总索引：[`tokens.json`](tokens.json)。
- 人读核对表：[`figma-variable-inventory.md`](figma-variable-inventory.md)。

## 目录

```text
skills/qifu-shared/theme/
├── _index.less
├── _light.less          # 基础 collection，默认导出毓数/Light
├── _font.less
├── _radius.less
├── _size.less
├── tokens.json          # collection / mode / Figma 原路径与真实值或 alias
├── figma-variable-inventory.md
└── source/              # collection 级原始变量数据
```

## AI 调用规则

1. 先读取 `tokens.json`，再按 `source/<collection>.json` 查 `figmaPath`、`name`、`type`、`values`。
2. 仅使用 `figmaPath` 和 `name` 作为 Figma 资产名称。例如 `--qifu-text-color-primary`、`--qifu-bg-color-canvas`、`--qifu-size/16` 均保持原样。
3. `基础颜色拓展/brand/default` 这种路径是 Figma 的真实分组路径；不要擅自改为 `--qifu-brand-default`。
4. `.less` 内的 `@...` 标识符是为代码合法性生成的导出映射（`/`、`%` 等字符被转换），**不是 Figma 原变量名**；回写 Figma 或描述设计资产时必须用 JSON 中的原路径。
5. 选择主题时使用 `基础` collection 的真实模式：`毓数/Light` 或 `智能运营/Light`；`色彩` collection 的模式是 `mode/green` 与 `mode/blue`。

## Less 使用

```less
@import 'skills/qifu-shared/theme/_index.less';
// @qifu-text-color-primary  ← Figma: 文本颜色/--qifu-text-color-primary
```

> `tokens.json` 是 AI/自动化的权威输入；Less 是面向工程的辅助导出。
