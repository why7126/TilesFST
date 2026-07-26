## ADDED Requirements

### Requirement: SKU 弹窗规格未匹配提示 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 编辑 SKU 弹窗（`TileSkuFormModal`）中，当 SKU 无 `spec_id`（迁移失败）时在「瓷砖规格」下拉下方展示的辅助提示样式问题：提示 MUST 使用与管理端共享的 `.form-help` 样式（11px、`var(--admin-weak)`、`margin-top: 7px`），与用户管理、品牌弹窗字段辅助文案一致。修复 MUST NOT 修改 SKU API、数据库、Orval、提示文案语义或显隐条件逻辑。

#### Scenario: 规格未匹配提示使用 form-help

- **WHEN** 用户编辑一条 `spec_id` 为 NULL 的历史 SKU 且规格下拉未选择
- **THEN** MUST 展示提示「历史 SKU 未匹配规格，请手动选择后保存」
- **AND** 提示元素 MUST 使用 class `form-help`
- **AND** MUST NOT 使用 `form-hint` 或未定义样式类名

#### Scenario: 提示 Typography 对齐管理端字段辅助文案

- **WHEN** AC-001 场景
- **THEN** 提示 MUST 呈现 11px、`var(--admin-weak)` 次要文字色
- **AND** 视觉层级 MUST 低于字段标签（12px `--admin-muted`）

#### Scenario: 提示显隐逻辑不变

- **WHEN** 用户从规格下拉选择有效规格
- **THEN** 提示 MUST 消失
- **WHEN** 新增 SKU 或编辑已有有效 `spec_id` 的 SKU
- **THEN** MUST NOT 展示该提示

#### Scenario: 同弹窗既有修复不回退

- **WHEN** 本修复合并后
- **THEN** BUG-0010（modal-desc）、BUG-0011（弹窗滚动）、BUG-0012（字段规则）相关行为 MUST 保持
