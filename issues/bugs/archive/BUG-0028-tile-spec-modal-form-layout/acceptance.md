---
bug_id: BUG-0028-tile-spec-modal-form-layout
status: pending_review
created_at: 2026-06-28 13:21:30
updated_at: 2026-06-28 13:21:30
related_requirement: REQ-0009-tile-spec-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0009 **AC-019**（弹窗字段）、**AC-020**（禁止字段）、**AC-046**（弹窗 HTML 并排），且不得回归规格弹窗 CRUD、`display_name` 生成逻辑与后端唯一性校验。

## AC-001 弹窗字段顺序 MUST 对齐 REQ-0009 AC-019

**Given** 管理员已登录并打开「新增瓷砖规格」或「编辑瓷砖规格」弹窗  
**When** 自上而下观察表单字段  
**Then** 顺序 MUST 为：宽度 (mm)* → 长度 (mm)* → **尺寸名称（只读，跨列）** → 厚度 (mm) → 排序* → 备注（跨列）  
**And** 尺寸名称 MUST NOT 出现在厚度、排序之后

## AC-002 只读尺寸名称 preview MUST 保持 `{w}×{l}mm` 格式

**Given** 弹窗中宽度=600、长度=1200  
**When** 用户观察只读尺寸名称  
**Then** MUST 显示 `600×1200mm`（乘号 `×`，含 `mm` 后缀）  
**And** MUST NOT 改为去掉 `mm` 或改用自由文本 `x` 连字符（除非与后端 `display_name` 规则同步变更——本 BUG 范围外）

## AC-003 备注文本框 MUST 占满整行

**Given** 弹窗已打开  
**When** 观察「备注」字段  
**Then** `textarea` MUST 在 `.form-full` 容器内横向占满弹窗内容区宽度（`width: 100%`）  
**And** MUST 具备固定高度与 `resize: none`（对齐 `tile-size-management-modal.html` port CSS）  
**And** MUST NOT 出现仅占半列或默认窄宽度 textarea

## AC-004 弹窗禁止字段 MUST 仍不存在（AC-020）

**Given** 新增或编辑弹窗  
**When** 检查全部表单字段  
**Then** MUST NOT 出现：单位选择、规格类型、常用尺寸、系统状态、可编辑尺寸名称

## AC-005 弹窗宽度与网格 MUST 保持 720px 双列布局

**Given** 视口宽度 ≥ 640px  
**When** 打开弹窗  
**Then** 弹窗卡片宽度 MUST 为 720px（`.tile-spec-modal-card`）  
**And** 宽/长、厚度/排序 MUST 为双列 grid；尺寸名称与备注 MUST 跨列

## AC-006 弹窗 CRUD 功能 MUST 保持可用

**Given** 修复已部署  
**When** 用户通过弹窗创建或更新规格（含厚度可选、排序、备注 ≤200 字）  
**Then** 保存 MUST 成功；服务端 MUST 继续生成 `display_name` 并执行 `(width_mm, length_mm, unit)` 唯一性校验  
**And** 编辑模式 MUST 正确回填现有规格数据

## AC-007 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 修改 `buildDisplayName()` 存储语义（除非单独 REQ/Change 明确变更）

## AC-008 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** MUST 使用 semantic token（`var(--admin-*)` / Tailwind semantic class）  
**And** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部样式

## AC-009 弹窗 HTML 并排验收 MUST 通过（AC-046）

**Given** 修复完成  
**When** 在 1440×1024 并排对比 `/admin/tile-specs` 弹窗与 `prototype/web/tile-size-management-modal.html`  
**Then** 字段网格、只读尺寸名称区块、备注整行宽度 MUST 视觉对齐原型  
**And** MUST 在 Change `trace.md` 记录并排验收结论

## AC-010 AC-021 宽长冲突提示 SHOULD 纳入（可选同 scope）

**Given** 新增模式下输入已存在的 `(width_mm, length_mm)` 组合  
**When** 只读尺寸名称更新  
**Then** SHOULD 展示「该尺寸已存在，请勿重复创建」类 inline 提示并禁止提交（对齐原型 `#duplicateTip`）  
**Note** 若本 Change 范围不包含此项，MUST 在 review 或 tasks 中明确延后并单独跟踪

## AC-011 测试与记录 MUST 补齐

**Given** 进入 `fix-tile-spec-modal-form-layout`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `TileSpecFormModal` 相关 Vitest（字段 DOM 顺序、备注 textarea 整行）  
**And** MUST 更新 `add-tile-spec-management` 或新 Change trace checklist 第 7–9 项为 pass
