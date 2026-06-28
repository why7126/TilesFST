---
bug_id: BUG-0034-banner-modal-link-selector-combined
status: pending_review
created_at: 2026-06-28 16:17:29
updated_at: 2026-06-28 16:17:29
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0016 **AC-031**（SKU 可搜索选择）、**AC-036**（专题可搜索选择），且不得回归 Banner 弹窗其他 `jump_type` 字段、图片上传与保存逻辑。

## AC-001 关联 SKU MUST 为单一可搜索选择控件

**Given** 管理员在 Banner 弹窗且 `jump_type=SKU_DETAIL`  
**When** 观察「关联 SKU」字段区域  
**Then** MUST 仅存在一个关联 SKU 选择控件（Combobox / SearchableSelect 或等效）  
**And** MUST NOT 出现独立的「搜索 SKU」输入框与「请选择 SKU」下拉框双控件组合  
**And** 控件高度 MUST 为 40px，视觉与弹窗其他 `input` / `select` 一致

## AC-002 SKU 搜索 MUST 在同一控件内完成筛选与选择

**Given** 管理员在 SKU 详情跳转类型的 Banner 弹窗  
**When** 在选择控件内输入 SKU 名称或编码关键词  
**Then** MUST debounce 或等效机制调用 `GET /api/v1/admin/tile-skus`（含 keyword）刷新候选  
**And** 用户 MUST 能在同一控件内点选目标 SKU，无需在第二个控件中二次选择  
**And** 选中后控件 MUST 展示已选 SKU 标签（如 `名称 · 编码`）

## AC-003 关联专题 MUST 为单一可搜索选择控件

**Given** 管理员在 Banner 弹窗且 `jump_type=TOPIC_PAGE`  
**When** 观察「关联专题」字段区域  
**Then** MUST 仅存在一个关联专题选择控件  
**And** MUST NOT 出现独立的「搜索专题」输入框与「请选择专题」下拉框双控件组合  
**And** 控件高度 MUST 为 40px

## AC-004 专题搜索 MUST 在同一控件内完成筛选与选择

**Given** 管理员在专题页跳转类型的 Banner 弹窗  
**When** 在选择控件内输入专题名称或编码关键词  
**Then** MUST 调用 `GET /api/v1/admin/topics`（含 keyword，`status=ENABLED`）刷新候选  
**And** 用户 MUST 能在同一控件内点选目标专题  
**And** 选中后控件 MUST 展示已选专题标题

## AC-005 编辑模式 MUST 正确回显已选 SKU / 专题

**Given** 编辑一个已保存 `sku_id` 或 `topic_id` 的 Banner  
**When** 打开编辑弹窗且对应 `jump_type` 为 SKU 详情或专题页  
**Then** 关联选择控件 MUST 展示当前已关联的 SKU / 专题名称  
**And** MUST NOT 出现空白 select（即使该目标不在默认前 20 条列表中）  
**And** 用户 MAY 重新搜索并更换关联目标

## AC-006 选择 SKU 后主图联动 MUST 保持可用

**Given** `jump_type=SKU_DETAIL` 且用户通过新选择器选中 SKU  
**When** `image_source=sku_main_image`（默认或用户点击「使用 SKU 主图」）  
**Then** Banner 图片预览 MUST 仍更新为该 SKU 主图（现有 `handleSkuChange` 行为不得回归）

## AC-007 其他 jump_type MUST 不受影响

**Given** Banner 弹窗跳转类型为 `EXTERNAL_LINK` 或 `NO_JUMP`  
**When** 观察表单字段  
**Then** MUST NOT 出现 SKU / 专题关联选择控件  
**And** 外部链接、无跳转禁用态等现有字段 MUST 行为不变

## AC-008 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 引入新的后端逻辑

## AC-009 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** MUST 使用 semantic Token（`input` / `select` 同类边框、背景、文字色）  
**And** MUST NOT 新增裸 Hex  
**And** 新增共享组件 MUST 放入 `src/web/src/shared/ui/` 或 `src/web/src/components/ui/`（符合 `rules/directory-structure.md`）

## AC-010 原型并排验收 MUST 通过

**Given** 修复完成  
**When** 与 `banner-management-modal-sku-detail.png`、`banner-management-modal-topic-page.png` 并排对比（1440×1024）  
**Then** 「关联 SKU / 关联专题」区域 MUST 为单控件布局，与 prototype HTML 结构语义一致  
**And** MUST 在 Change `trace.md` 记录并排验收结论

## AC-011 测试 MUST 补齐

**Given** 进入 `fix-banner-modal-link-selector-combined`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `BannerFormModal` Vitest：SKU_DETAIL / TOPIC_PAGE 分支无独立搜索 input、单选择控件存在  
**And** SHOULD 覆盖编辑模式已选 id 回显（mock API）

## AC-012 REQ-0016 AC-031 / AC-036 对齐确认

**Given** BUG-0034 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0016-banner-management/acceptance.md` AC-031、AC-036  
**Then** 「必选关联 SKU / 专题（可搜索）」MUST 在 UX 层面满足可搜索选择语义，而非双控件近似实现
