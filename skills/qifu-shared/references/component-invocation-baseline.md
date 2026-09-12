# 共享组件调用基线

本文件定义所有 Qifu 页面 Skill 共同遵守的组件解析与失败语义。页面级 Slot、数量和布局规则由各 Archetype 的验证文件补充。

## 解析顺序

1. 按业务语义选择 `component-map.md` 中的组件集。
2. 同文件优先使用节点 ID，跨文件优先使用发布 Key。
3. 节点或 Key 失效时按完整组件集名称重新发现；必须唯一匹配，不凭相似名称猜测。
4. 创建实例后读取 `mainComponent` 与 `componentProperties`，确认来源、属性真实 Key、类型和值域。
5. 写入属性、变体、INSTANCE_SWAP 或 Slot 后立即回读；只有期望值与实际值一致才算成功。

## 最小解析记录

```yaml
component:
  semanticName: <business capability>
  componentSet: <exact Figma name>
  sourceFileKey: <file key>
  sourceNodeId: <node id or null>
  publishedKey: <published key or null>
  instanceId: <created instance id or null>
  status: resolved | missing | ambiguous | failed
  readback: <expected versus actual>
```

## 失败分类

- `COMPONENT_MISSING`：组件库经确认不存在该能力；只有此类错误可以进入受限 Fallback 判断。
- `COMPONENT_AMBIGUOUS`：完整名称仍匹配多个候选；停止并报告候选。
- `PROPERTY_NOT_FOUND` / `PROPERTY_READBACK_MISMATCH`：属性不存在或写后不一致；属于执行失败。
- `INSTANCE_SWAP_FAILED` / `SLOT_WRITE_FAILED`：替换失败；属于执行失败。
- `STYLE_MISSING` / `FONT_UNAVAILABLE`：语义变量、Text Style 或字体不可用；属于执行失败。
- `PERMISSION_DENIED` / `TARGET_NOT_EDITABLE`：权限或目标不可编辑；停止，不换文件规避。

不得用裸 Text、矩形、截图、覆盖层、分离实例或隐藏真实实例来伪装成功。原始十六进制颜色和像素值只能作为核对信息；正式写入优先绑定组件库语义变量或公开组件属性。

## 交付门禁

页面专属结构验收和视觉验收都为 `PASS` 才能宣称完成。`BLOCKED` 表示缺少用户输入、模板或已授权依赖；`FAIL` 表示已执行但关键契约未满足。两者不得写成“已完成”。
