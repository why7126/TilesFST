---
bug_id: BUG-0028-tile-spec-modal-form-layout
title: 瓷砖规格弹窗表单字段顺序与备注宽度不符合 REQ-0009 规范
severity: medium
status: draft
owner: product
discovered_at: 2026-06-28 13:13:16
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_change: add-tile-spec-management
---

# 缺陷说明

Web 管理端「瓷砖规格」新增/编辑弹窗（`TileSpecFormModal`）表单布局与 REQ-0009 / 原型 `tile-size-management-modal.html` 不一致，主要体现在：

1. **字段顺序错误**：只读「尺寸名称」当前位于厚度、排序之后；规范顺序应为 **宽度* → 长度* → 尺寸名称（只读，跨列）→ 厚度 → 排序* → 备注（跨列）**。
2. **备注文本框未占满整行**：DOM 虽含 `form-full`（`grid-column: 1 / -1`），但 `tile-spec-management.css` 未 port 原型中的 `.textarea { width: 100%; … }` 规则，导致备注框宽度不足、高度与 `resize` 行为也与原型不符。
3. **CSS Port 缺口（附带）**：弹窗表单缺少原型中的 `.input`/`.textarea` 宽度与备注固定高度、`resize: none` 等样式；只读区 help 文案与 AC-021 要求的宽长冲突提示亦未实现（可作为同 change 或后续项纳入 acceptance）。

**说明（非缺陷）**：只读尺寸名称显示 `{w}×{l}mm`（如 `600×1200mm`）符合 REQ-0009 FR-006、AC-021 及后端 `display_name` 生成规则；capture 中「去掉 mm 后缀」的期望与规范冲突，**不应**作为修复目标。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local `5173` 或 Docker `3000` 均可）。
2. 进入「瓷砖规格」列表页（侧栏 OPERATIONS → 瓷砖规格，或 `/admin/tile-specs`）。
3. 点击「+ 新增瓷砖规格」或某行「编辑」，打开弹窗。
4. 在宽度、长度输入框填写数值（如 600、1200），观察只读「尺寸名称」在表单中的位置（当前在厚度、排序下方）。
5. 观察「备注」文本框是否横向占满整行、高度是否与原型一致。
6. 可选：并排对照 `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.html` 与截图 `screenshots/tile-spec-modal-form-layout.png`。

# 期望结果

- 弹窗 720px，字段网格顺序与 REQ-0009 AC-019、原型一致：
  - 宽度 (mm)*、长度 (mm)*（双列）
  - **尺寸名称（只读，跨列）** — 宽长变化后实时显示 `{w}×{l}mm`
  - 厚度 (mm)、排序*（双列）
  - 备注（跨列）
- 备注 `textarea` 占满整行宽度，固定高度，`resize: none`，样式对齐原型 port CSS。
- 弹窗 MUST NOT 包含：单位选择、规格类型、常用尺寸、系统状态、可编辑尺寸名称（AC-020）。
- 视觉验收：1440×1024 并排 `/admin/tile-specs` 弹窗与 `tile-size-management-modal.html`（AC-046）。

# 实际结果

- `TileSpecFormModal.tsx` 字段顺序为：宽 → 长 → **厚度 → 排序 → 尺寸名称 → 备注**，尺寸名称被置于厚度/排序之后。
- `tile-spec-management.css` 仅有 `.form-full { grid-column: 1 / -1 }` 与 `.tile-spec-readonly`，**未**定义 `.textarea` 的 `width: 100%`、固定高度等；全局 `user-management.css` 的 `.input` 宽度规则也不覆盖 `.textarea`。
- 备注框在视觉上仅占部分列宽，与截图 `tile-spec-modal-form-layout.png` 一致。
- 只读尺寸名称 preview 使用 `buildDisplayName()` 输出 `{w}×{l}mm`，**此项符合规范**，不是缺陷。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖规格弹窗 | 新增、编辑弹窗表单布局与原型不一致 |
| REQ-0009 验收 | AC-019、AC-046 弹窗字段网格与 HTML 并排未达标 |
| 关联 Change | `add-tile-spec-management` trace checklist 第 7–9 项仍为「待人工」 |
| 同域 BUG | 可与 BUG-0027（列表 UI）、BUG-0029（创建后刷新）合并为同一 `fix-*` change |

不影响 API 契约、数据库、`display_name` 存储逻辑、权限边界或小程序/店主端。

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断规格的新增、编辑、保存与列表查询等核心流程。
- 属于可见管理端 UI / CSS Port 缺口，影响 REQ-0009 弹窗验收与运营对「尺寸名称」字段位置的预期。
- 修复范围小（组件字段重排 + CSS port），无后端或数据迁移风险；但需在 `bug-complete` 阶段明确是否同期纳入 AC-021 冲突提示。

# 代码线索

| 线索 | 路径 |
|---|---|
| 规格弹窗组件 | `src/web/src/features/admin/components/TileSpecFormModal.tsx` |
| 弹窗样式（缺 textarea port） | `src/web/src/features/admin/styles/tile-spec-management.css` |
| display_name 预览（符合规范） | `src/web/src/features/admin/api/tile-specs-api.ts` → `buildDisplayName()` |
| 弹窗原型 HTML | `issues/requirements/archive/REQ-0009-tile-spec-management/prototype/web/tile-size-management-modal.html` |
| 品牌弹窗 textarea 参考 | `src/web/src/features/admin/styles/brand-management.css` → `.brand-textarea` |
| 关联 Change trace | `openspec/changes/add-tile-spec-management/trace.md` |
| UI 规范 | `rules/ui-design.md` |
